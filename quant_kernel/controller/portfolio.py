"""
Portfolio Manager - Orchestrates All Components

The Portfolio Manager ties together all Quant-Kernel components:
- InterruptHandler for data ingestion
- FeatureMMU for feature compression
- EigenScheduler for capital allocation
- StabilityController for risk management
"""

from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field
import numpy as np
from numpy.typing import NDArray
import time
from threading import RLock

from quant_kernel.interrupt.handler import InterruptHandler, MarketTick
from quant_kernel.mmu.feature_mmu import FeatureMMU
from quant_kernel.scheduler import EigenScheduler, MarketRegime
from quant_kernel.controller.stability import StabilityController, RiskMetrics
from quant_kernel.controller.jacobian import JacobianSensitivity


@dataclass
class PortfolioState:
    """Current state of the portfolio."""
    positions: Dict[str, float]  # symbol -> weight
    cash: float
    total_value: float
    regime: MarketRegime
    risk_metrics: RiskMetrics
    timestamp: int


@dataclass
class Signal:
    """Trading signal from the Quant-Kernel."""
    symbol: str
    direction: int  # 1 = long, -1 = short, 0 = neutral
    confidence: float
    size: float
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class PortfolioManager:
    """
    Main Portfolio Manager for the Quant-Kernel.
    
    Orchestrates all components to provide a complete trading system.
    
    Workflow:
    1. Receive market tick via InterruptHandler
    2. Extract features and compress via FeatureMMU
    3. Analyze regime via EigenScheduler
    4. Determine optimal sizing via StabilityController
    5. Generate trading signals
    
    Example:
        >>> pm = PortfolioManager(
        ...     symbols=['AAPL', 'GOOGL', 'MSFT'],
        ...     initial_capital=100000
        ... )
        >>> 
        >>> # Process a tick
        >>> pm.process_tick(tick)
        >>> 
        >>> # Get signals
        >>> signals = pm.get_signals()
    """
    
    def __init__(
        self,
        symbols: List[str],
        initial_capital: float = 100000.0,
        max_position_pct: float = 0.2,
        lookback: int = 100
    ):
        """
        Initialize Portfolio Manager.
        
        Args:
            symbols: List of trading symbols
            initial_capital: Initial capital
            max_position_pct: Maximum position size as % of capital
            lookback: Historical periods for estimation
        """
        self._symbols = symbols
        self._initial_capital = initial_capital
        self._max_position_pct = max_position_pct
        self._lookback = lookback
        
        # Components
        self._interrupt_handler = InterruptHandler(
            capacity=lookback * len(symbols),
            default_symbols=symbols
        )
        
        self._feature_mmu = FeatureMMU(n_components=3)
        
        self._scheduler = EigenScheduler(
            n_assets=len(symbols),
            lookback=lookback
        )
        
        self._stability_controller = StabilityController(
            n_assets=len(symbols),
            lookback=lookback
        )
        
        self._jacobian = JacobianSensitivity(
            n_factors=len(symbols),
            lookback=lookback,
            factor_names=symbols
        )
        
        # State
        self._cash = initial_capital
        self._positions: Dict[str, float] = {s: 0.0 for s in symbols}
        self._current_regime = MarketRegime.SIDEWAYS
        
        # History
        self._signal_history: List[Signal] = []
        
        # Lock
        self._lock = RLock()
    
    def initialize(self, historical_data: NDArray) -> "PortfolioManager":
        """
        Initialize with historical data.
        
        Args:
            historical_data: Historical returns (n_periods, n_assets)
            
        Returns:
            Self for method chaining
        """
        # Fit scheduler
        self._scheduler.fit(historical_data)
        
        # Fit stability controller
        self._stability_controller.initialize(historical_data)
        
        # Fit Jacobian
        portfolio_returns = np.sum(historical_data, axis=1) / len(self._symbols)
        self._jacobian.fit(historical_data, portfolio_returns)
        
        return self
    
    def process_tick(self, tick: MarketTick) -> None:
        """
        Process a market tick.
        
        Args:
            tick: MarketTick to process
        """
        # Handle interrupt
        self._interrupt_handler.handle_interrupt(tick)
        
        # Analyze regime
        self._update_regime()
    
    def _update_regime(self) -> None:
        """Update market regime analysis."""
        # Get recent returns
        all_returns = []
        for symbol in self._symbols:
            ticks = self._interrupt_handler.get_recent_ticks(n=20, symbol=symbol)
            if len(ticks) >= 2:
                prices = np.array([t.price for t in ticks])
                returns = np.diff(prices) / prices[:-1]
                all_returns.append(returns)
        
        if all_returns:
            # Pad to same length
            min_len = min(len(r) for r in all_returns)
            returns_matrix = np.column_stack([r[-min_len:] for r in all_returns])
            
            # Update scheduler
            self._scheduler.update(returns_matrix[-1])
            
            # Get regime
            state = self._scheduler.analyze_regime()
            self._current_regime = state.regime
    
    def get_signals(self, min_confidence: float = 0.5) -> List[Signal]:
        """
        Generate trading signals based on current regime.
        
        Args:
            min_confidence: Minimum confidence threshold
            
        Returns:
            List of trading signals
        """
        with self._lock:
            signals = []
            
            # Get allocations from scheduler
            allocations = self._scheduler.get_allocations()
            
            # Get optimal weights from stability controller
            if self._stability_controller.get_risk_metrics():
                vol = self._stability_controller.get_risk_metrics().portfolio_volatility
                cond = self._stability_controller.get_risk_metrics().condition_number
                
                # Get recent returns
                returns_data = self._get_recent_returns()
                if returns_data is not None and len(returns_data) >= 20:
                    optimal_weights = self._stability_controller.compute_optimal_weights(
                        returns_data,
                        condition_number=cond,
                        volatility=vol
                    )
                    
                    # Generate signals
                    for i, symbol in enumerate(self._symbols):
                        current_weight = self._positions.get(symbol, 0.0)
                        target_weight = optimal_weights[i]
                        weight_diff = target_weight - current_weight
                        
                        # Determine direction
                        if abs(weight_diff) < 0.01:
                            direction = 0
                        elif weight_diff > 0:
                            direction = 1
                        else:
                            direction = -1
                        
                        # Get confidence from allocation
                        confidence = 0.5
                        for alloc in allocations:
                            if alloc.strategy_name in ["trend_following", "momentum"]:
                                confidence = alloc.confidence
                                break
                        
                        if confidence >= min_confidence and abs(weight_diff) > 0.02:
                            signal = Signal(
                                symbol=symbol,
                                direction=direction,
                                confidence=confidence,
                                size=abs(weight_diff) * self._get_total_value(),
                                reason=f"Regime: {self._current_regime.value}",
                                metadata={
                                    "current_weight": current_weight,
                                    "target_weight": target_weight,
                                    "regime": self._current_regime.value,
                                    "condition_number": cond,
                                    "volatility": vol,
                                }
                            )
                            signals.append(signal)
            
            self._signal_history.extend(signals)
            return signals
    
    def _get_recent_returns(self) -> Optional[NDArray]:
        """Get recent returns matrix."""
        all_returns = []
        
        for symbol in self._symbols:
            ticks = self._interrupt_handler.get_recent_ticks(n=20, symbol=symbol)
            if len(ticks) >= 2:
                prices = np.array([t.price for t in ticks])
                returns = np.diff(prices) / prices[:-1]
                all_returns.append(returns)
            else:
                return None
        
        if not all_returns:
            return None
        
        min_len = min(len(r) for r in all_returns)
        return np.column_stack([r[-min_len:] for r in all_returns])
    
    def _get_total_value(self) -> float:
        """Get total portfolio value."""
        position_value = sum(
            self._positions.get(s, 0.0) * (self._interrupt_handler.get_latest_price(s) or 0)
            for s in self._symbols
        )
        return self._cash + position_value
    
    def apply_signal(self, signal: Signal) -> bool:
        """
        Apply a trading signal to update positions.
        
        Args:
            signal: Signal to apply
            
        Returns:
            True if signal was applied successfully
        """
        with self._lock:
            current_price = self._interrupt_handler.get_latest_price(signal.symbol)
            if current_price is None:
                return False
            
            # Calculate position change
            position_change = signal.size / current_price
            
            # Update position
            if signal.direction > 0:  # Long
                cost = position_change * current_price
                if cost <= self._cash:
                    self._positions[signal.symbol] = \
                        self._positions.get(signal.symbol, 0) + position_change
                    self._cash -= cost
            elif signal.direction < 0:  # Short
                self._positions[signal.symbol] = \
                    self._positions.get(signal.symbol, 0) - position_change
                self._cash += position_change * current_price
            
            return True
    
    def get_portfolio_state(self) -> PortfolioState:
        """Get current portfolio state."""
        total_value = self._get_total_value()
        risk_metrics = self._stability_controller.get_risk_metrics() or RiskMetrics(
            portfolio_volatility=0.0,
            sharpe_ratio=0.0,
            max_drawdown=0.0,
            var_95=0.0,
            cvar_95=0.0,
            condition_number=1.0,
            leverage=0.0
        )
        
        return PortfolioState(
            positions=self._positions.copy(),
            cash=self._cash,
            total_value=total_value,
            regime=self._current_regime,
            risk_metrics=risk_metrics,
            timestamp=int(time.time() * 1000)
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get portfolio statistics."""
        return {
            "symbols": self._symbols,
            "cash": self._cash,
            "positions": self._positions,
            "total_value": self._get_total_value(),
            "current_regime": self._current_regime.value,
            "interrupt_stats": self._interrupt_handler.get_statistics(),
            "scheduler_stats": self._scheduler.get_statistics(),
            "stability_stats": self._stability_controller.get_statistics(),
            "jacobian_stats": self._jacobian.get_statistics(),
        }

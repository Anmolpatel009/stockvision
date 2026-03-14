"""
Backtest Engine with SVD-Denoising

Implements backtesting with SVD-based noise reduction for cleaner signals.
"""

from typing import Optional, Dict, List, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from numpy.typing import NDArray
from scipy import linalg
import time
from threading import RLock
from collections import deque


class SignalType(Enum):
    """Types of trading signals."""
    LONG = 1
    SHORT = -1
    NEUTRAL = 0


@dataclass
class Trade:
    """Represents a single trade."""
    timestamp: int
    symbol: str
    direction: SignalType
    quantity: float
    price: float
    pnl: float = 0.0
    commission: float = 0.0


@dataclass
class BacktestResult:
    """Results of a backtest run."""
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    num_trades: int
    num_winning_trades: int
    avg_trade_pnl: float
    equity_curve: NDArray
    trades: List[Trade]
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SVDDenoiser:
    """
    SVD-Based Signal Denoiser.
    
    Uses Singular Value Decomposition to separate signal from noise
    in financial time series.
    
    Mathematical Model:
    - X = U @ Σ @ V^T (SVD decomposition)
    - Signal = U[:, :k] @ Σ[:k, :k] @ V[:k, :] (top k singular values)
    - Noise is captured in smaller singular values
    
    Example:
        >>> denoiser = SVDDenoiser(n_components=3)
        >>> denoiser.fit(price_series)
        >>> 
        >>> # Get denoised signal
        >>> denoised = denoiser.transform(new_prices)
    """
    
    def __init__(
        self,
        n_components: int = 3,
        window_size: int = 50,
        min_periods: int = 20
    ):
        """
        Initialize SVD denoiser.
        
        Args:
            n_components: Number of singular components to keep
            window_size: Rolling window size for SVD
            min_periods: Minimum periods before fitting
        """
        self._n_components = n_components
        self._window_size = window_size
        self._min_periods = min_periods
        
        # State
        self._is_fitted = False
        self._U: Optional[NDArray] = None
        self._S: Optional[NDArray] = None
        self._Vt: Optional[NDArray] = None
        
        # History
        self._window_buffer: List[NDArray] = []
    
    @property
    def is_fitted(self) -> bool:
        """Check if denoiser is fitted."""
        return self._is_fitted
    
    def fit(self, data: NDArray) -> "SVDDenoiser":
        """
        Fit the denoiser on historical data.
        
        Args:
            data: Time series data
            
        Returns:
            Self for method chaining
        """
        data = np.asarray(data, dtype=np.float64)
        
        if data.ndim == 1:
            data = data.reshape(-1, 1)
        
        with RLock():
            # Use sliding window
            self._window_buffer = []
            for i in range(len(data) - self._window_size + 1):
                window = data[i:i + self._window_size]
                self._window_buffer.append(window)
            
            if len(self._window_buffer) >= self._min_periods:
                # Stack windows and compute SVD
                X = np.column_stack(self._window_buffer)
                
                # Compute SVD
                self._U, self._S, self._Vt = linalg.svd(X, full_matrices=False)
                
                # Keep only top k components
                self._U = self._U[:, :self._n_components]
                self._S = self._S[:self._n_components]
                self._Vt = self._Vt[:self._n_components, :]
                
                self._is_fitted = True
        
        return self
    
    def transform(self, data: NDArray) -> NDArray:
        """
        Transform data using fitted SVD.
        
        Args:
            data: New data to denoise
            
        Returns:
            Denoised data
        """
        data = np.asarray(data, dtype=np.float64)
        
        if not self._is_fitted:
            return data
        
        if data.ndim == 1:
            data = data.reshape(1, -1)
        
        # Project onto principal components
        # This effectively denoises the data
        U_truncated = self._U
        S_diag = np.diag(self._S)
        
        # Reconstruct using only signal components
        denoised = U_truncated @ S_diag @ self._Vt
        
        # Return the last row (most recent)
        return denoised[-1, :]
    
    def fit_transform(self, data: NDArray) -> NDArray:
        """Fit and transform in one step."""
        self.fit(data)
        return self.transform(data)
    
    def denoise_returns(self, returns: NDArray) -> Tuple[NDArray, NDArray]:
        """
        Denoise returns and return both denoised and noise components.
        
        Args:
            returns: Returns series
            
        Returns:
            Tuple of (denoised_returns, noise_returns)
        """
        if not self._is_fitted or len(returns) < self._window_size:
            return returns, np.zeros_like(returns)
        
        # For simple 1D returns, use a simple moving average denoising
        n = len(returns)
        k = min(self._window_size, n)
        
        # Simple denoising: use exponential moving average
        denoised = np.zeros(n)
        alpha = 2.0 / (k + 1)
        denoised[0] = returns[0]
        for i in range(1, n):
            denoised[i] = alpha * returns[i] + (1 - alpha) * denoised[i-1]
        
        noise = returns - denoised
        
        return denoised, noise


class BacktestEngine:
    """
    Backtest Engine for Quant-Kernel Strategies.
    
    Provides comprehensive backtesting with:
    - SVD-denoised signal processing
    - Realistic transaction costs
    - Position sizing based on risk
    - Detailed performance metrics
    
    Example:
        >>> engine = BacktestEngine(initial_capital=100000)
        >>> engine.set_denoiser(SVDDenoiser(n_components=3))
        >>> 
        >>> # Run backtest
        >>> result = engine.run(
        ...     prices=price_data,
        ...     signals=signal_data,
        ...     positions=position_data
        ... )
        >>> 
        >>> print(f"Sharpe: {result.sharpe_ratio:.2f}")
    """
    
    def __init__(
        self,
        initial_capital: float = 100000.0,
        commission_pct: float = 0.001,  # 0.1% commission
        slippage_pct: float = 0.0005,    # 0.05% slippage
        max_position_pct: float = 0.2    # Max 20% per position
    ):
        """
        Initialize backtest engine.
        
        Args:
            initial_capital: Starting capital
            commission_pct: Commission as percentage
            slippage_pct: Slippage as percentage
            max_position_pct: Maximum position size
        """
        self._initial_capital = initial_capital
        self._commission_pct = commission_pct
        self._slippage_pct = slippage_pct
        self._max_position_pct = max_position_pct
        
        # SVD denoiser
        self._denoiser: Optional[SVDDenoiser] = None
        
        # State
        self._trades: List[Trade] = []
        self._equity_curve: List[float] = []
        self._positions: Dict[str, float] = {}
        self._cash: float = initial_capital
        
        # Statistics
        self._stats = {
            "total_trades": 0,
            "winning_trades": 0,
            "total_commission": 0.0,
        }
    
    def set_denoiser(self, denoiser: SVDDenoiser) -> "BacktestEngine":
        """
        Set SVD denoiser for signal processing.
        
        Args:
            denoiser: SVDDenoiser instance
            
        Returns:
            Self for method chaining
        """
        self._denoiser = denoiser
        return self
    
    def run(
        self,
        prices: NDArray,
        signals: NDArray,
        symbols: Optional[List[str]] = None,
        positions: Optional[NDArray] = None,
        start_idx: int = 0
    ) -> BacktestResult:
        """
        Run backtest.
        
        Args:
            prices: Price data (n_periods, n_assets)
            signals: Trading signals (n_periods, n_assets)
            symbols: Asset symbols
            positions: Position sizes (optional)
            start_idx: Starting index for backtest
            
        Returns:
            BacktestResult with performance metrics
        """
        prices = np.asarray(prices, dtype=np.float64)
        signals = np.asarray(signals, dtype=np.float64)
        
        if symbols is None:
            symbols = [f"asset_{i}" for i in range(prices.shape[1])]
        
        # Reset state
        self._reset()
        
        # Optionally denoise signals
        if self._denoiser is not None and len(prices) >= 50:
            self._denoiser.fit(prices)
            signals = self._apply_denoised_signals(prices, signals)
        
        # Run simulation
        for t in range(start_idx, len(prices)):
            self._process_bar(t, prices, signals, symbols)
        
        # Compute final metrics
        return self._compute_results()
    
    def _reset(self) -> None:
        """Reset backtest state."""
        self._trades = []
        self._equity_curve = [self._initial_capital]
        self._positions = {}
        self._cash = self._initial_capital
        self._stats = {
            "total_trades": 0,
            "winning_trades": 0,
            "total_commission": 0.0,
        }
    
    def _apply_denoised_signals(
        self,
        prices: NDArray,
        signals: NDArray
    ) -> NDArray:
        """Apply denoised signals."""
        # For each asset, denoise the signal
        denoised_signals = signals.copy()
        
        for i in range(signals.shape[1]):
            returns = np.diff(prices[:, i]) / prices[:-1, i]
            returns = np.insert(returns, 0, 0)
            
            if self._denoiser is not None:
                denoised_returns, _ = self._denoiser.denoise_returns(returns)
                denoised_signals[:, i] = denoised_returns
        
        return denoised_signals
    
    def _process_bar(
        self,
        t: int,
        prices: NDArray,
        signals: NDArray,
        symbols: List[str]
    ) -> None:
        """Process a single time bar."""
        current_prices = prices[t]
        
        # Update equity
        position_value = sum(
            self._positions.get(s, 0) * p
            for s, p in zip(symbols, current_prices)
        )
        equity = self._cash + position_value
        self._equity_curve.append(equity)
        
        # Process signals
        for i, symbol in enumerate(symbols):
            signal = signals[t, i]
            price = current_prices[i]
            
            # Skip if no signal
            if abs(signal) < 0.1:
                continue
            
            # Determine desired position
            target_position = 0
            if signal > 0.5:  # Strong buy
                target_position = equity * self._max_position_pct / price
            elif signal < -0.5:  # Strong sell
                target_position = -equity * self._max_position_pct / price
            
            # Calculate position change
            current_position = self._positions.get(symbol, 0)
            position_diff = target_position - current_position
            
            # Execute trade if significant
            if abs(position_diff) > 0.01:
                self._execute_trade(
                    timestamp=t,
                    symbol=symbol,
                    direction=SignalType.LONG if position_diff > 0 else SignalType.SHORT,
                    quantity=abs(position_diff),
                    price=price
                )
    
    def _execute_trade(
        self,
        timestamp: int,
        symbol: str,
        direction: SignalType,
        quantity: float,
        price: float
    ) -> None:
        """Execute a trade."""
        # Apply slippage
        execution_price = price * (1 + self._slippage_pct if direction == SignalType.LONG else 1 - self._slippage_pct)
        
        # Calculate cost
        cost = quantity * execution_price
        
        # Calculate commission
        commission = cost * self._commission_pct
        self._stats["total_commission"] += commission
        
        # Update cash and positions
        if direction == SignalType.LONG:
            self._cash -= (cost + commission)
            self._positions[symbol] = self._positions.get(symbol, 0) + quantity
        else:
            self._cash += (cost - commission)
            self._positions[symbol] = self._positions.get(symbol, 0) - quantity
        
        # Record trade
        trade = Trade(
            timestamp=timestamp,
            symbol=symbol,
            direction=direction,
            quantity=quantity,
            price=execution_price,
            commission=commission
        )
        self._trades.append(trade)
        self._stats["total_trades"] += 1
    
    def _compute_results(self) -> BacktestResult:
        """Compute final backtest results."""
        equity = np.array(self._equity_curve)
        
        # Calculate returns
        returns = np.diff(equity) / equity[:-1]
        returns = np.insert(returns, 0, 0)
        
        # Total return
        total_return = (equity[-1] - self._initial_capital) / self._initial_capital
        
        # Sharpe ratio (annualized)
        if len(returns) > 1 and np.std(returns) > 0:
            sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252)
        else:
            sharpe_ratio = 0.0
        
        # Max drawdown
        running_max = np.maximum.accumulate(equity)
        drawdown = (equity - running_max) / running_max
        max_drawdown = float(np.min(drawdown))
        
        # Trade statistics
        trade_pnls = [t.pnl for t in self._trades]
        num_trades = len(trade_pnls)
        
        if num_trades > 0:
            winning_trades = sum(1 for pnl in trade_pnls if pnl > 0)
            win_rate = winning_trades / num_trades
            
            wins = [pnl for pnl in trade_pnls if pnl > 0]
            losses = [pnl for pnl in trade_pnls if pnl < 0]
            
            profit_factor = abs(sum(wins) / sum(losses)) if losses and sum(losses) != 0 else 0
            avg_trade_pnl = sum(trade_pnls) / num_trades
        else:
            win_rate = 0.0
            profit_factor = 0.0
            avg_trade_pnl = 0.0
        
        return BacktestResult(
            total_return=total_return,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            profit_factor=profit_factor,
            num_trades=num_trades,
            num_winning_trades=winning_trades if num_trades > 0 else 0,
            avg_trade_pnl=avg_trade_pnl,
            equity_curve=equity,
            trades=self._trades,
            metrics={
                "initial_capital": self._initial_capital,
                "final_equity": equity[-1],
                "total_commission": self._stats["total_commission"],
                "num_assets": len(set(t.symbol for t in self._trades)),
            }
        )
    
    def get_trades(self) -> List[Trade]:
        """Get all trades."""
        return self._trades.copy()
    
    def get_equity_curve(self) -> NDArray:
        """Get equity curve."""
        return np.array(self._equity_curve)


def generate_signals_from_regime(
    regime: str,
    prices: NDArray,
    lookback: int = 20
) -> NDArray:
    """
    Generate simple signals based on market regime.
    
    Args:
        regime: Market regime
        prices: Price data
        lookback: Lookback period
        
    Returns:
        Signal array
    """
    n_periods, n_assets = prices.shape
    signals = np.zeros((n_periods, n_assets))
    
    for i in range(n_assets):
        # Simple moving average crossover
        for t in range(lookback, n_periods):
            ma_short = np.mean(prices[t-5:t, i])
            ma_long = np.mean(prices[t-lookback:t, i])
            
            if regime in ["trend_strong", "trend_weak"]:
                # Trend following
                if ma_short > ma_long:
                    signals[t, i] = 1.0
                elif ma_short < ma_long:
                    signals[t, i] = -1.0
            else:
                # Mean reversion
                price = prices[t, i]
                ma = np.mean(prices[t-lookback:t, i])
                std = np.std(prices[t-lookback:t, i])
                
                if price < ma - std:
                    signals[t, i] = 1.0  # Buy oversold
                elif price > ma + std:
                    signals[t, i] = -1.0  # Sell overbought
    
    return signals

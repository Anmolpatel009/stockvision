"""
Scheduler Module - Eigen-Dominance Based Capital Allocation

Implements the Scheduler layer of the Quant-Kernel architecture.
Manages strategy processes by calculating the Spectral Radius (largest 
eigenvalue) of the asset covariance matrix to determine dominant market trends.

Mathematical Background:
- Spectral Radius: ρ(A) = max(|λ_i|) where λ_i are eigenvalues of A
- High Spectral Radius: Indicates strong directional market movement
- Low Spectral Radius: Indicates mean-reverting or sideways market
- Covariance Matrix: Captures asset return correlations

The Scheduler decides which "processes" (strategies) to allocate 
"CPU cycles" (capital) to based on market regime detection.
"""

from typing import Optional, Dict, List, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from numpy.typing import NDArray
from scipy import linalg
from scipy.stats import zscore
import time
from threading import RLock
from collections import deque


class MarketRegime(Enum):
    """Market regime classification based on spectral analysis."""
    TREND_STRONG = "strong_trend"      # High spectral radius, strong directional
    TREND_WEAK = "weak_trend"          # Moderate spectral radius
    MEAN_REVERTING = "mean_reverting" # Low spectral radius
    SIDEWAYS = "sideways"              # Very low spectral radius, no clear direction
    VOLATILE = "volatile"              # High condition number, unstable


@dataclass
class StrategyAllocation:
    """Capital allocation for a strategy."""
    strategy_name: str
    allocation_pct: float
    confidence: float
    regime: MarketRegime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SchedulerState:
    """Current state of the scheduler."""
    spectral_radius: float
    condition_number: float
    regime: MarketRegime
    eigenvalue_spectrum: NDArray
    trend_strength: float
    timestamp: int


class EigenScheduler:
    """
    Eigen-Dominance Based Strategy Scheduler.
    
    Calculates the spectral radius of the asset covariance matrix to
    detect market regimes and allocate capital accordingly.
    
    Mathematical Model:
    - Let R be the matrix of historical returns (n_assets x n_periods)
    - Covariance: Σ = cov(R) = (R @ R.T) / (n_periods - 1)
    - Eigenvalues: λ_1 ≥ λ_2 ≥ ... ≥ λ_n (sorted)
    - Spectral Radius: ρ(Σ) = λ_1 (largest eigenvalue)
    
    Decision Logic:
    - ρ(Σ) > threshold_trend → Allocate to Trend Following
    - ρ(Σ) < threshold_mean_reversion → Allocate to Mean Reversion
    - High condition number (λ_1/λ_n) → Reduce exposure, increase cash
    
    Example:
        >>> scheduler = EigenScheduler(n_assets=5, lookback=100)
        >>> scheduler.fit(returns)  # Fit on historical returns
        >>> 
        >>> # Get allocations
        >>> allocations = scheduler.get_allocations(new_returns)
    """
    
    def __init__(
        self,
        n_assets: int,
        lookback: int = 100,
        trend_threshold: float = 0.5,
        mean_reversion_threshold: float = 0.2,
        volatility_threshold: float = 100.0,
        min_samples: int = 30
    ):
        """
        Initialize the EigenScheduler.
        
        Args:
            n_assets: Number of assets in the portfolio
            lookback: Number of periods for covariance estimation
            trend_threshold: Spectral radius threshold for trend detection
            mean_reversion_threshold: Threshold for mean reversion detection
            volatility_threshold: Condition number threshold for volatility
            min_samples: Minimum samples before computing
        """
        self._n_assets = n_assets
        self._lookback = lookback
        self._trend_threshold = trend_threshold
        self._mean_reversion_threshold = mean_reversion_threshold
        self._volatility_threshold = volatility_threshold
        self._min_samples = min_samples
        
        # State
        self._is_fitted = False
        self._returns_buffer: List[NDArray] = []
        
        # Covariance and eigenvalues
        self._covariance: Optional[NDArray] = None
        self._eigenvalues: Optional[NDArray] = None
        self._eigenvectors: Optional[NDArray] = None
        
        # Historical analysis
        self._spectral_history: deque = deque(maxlen=100)
        self._regime_history: deque = deque(maxlen=100)
        
        # Strategy allocations
        self._strategy_allocations: Dict[str, float] = {
            "trend_following": 0.33,
            "mean_reversion": 0.33,
            "momentum": 0.34,
        }
        
        # Statistics
        self._stats = {
            "total_evaluations": 0,
            "regime_counts": {},
            "avg_trend_strength": 0.0,
        }
        
        # Lock
        self._lock = RLock()
    
    @property
    def is_fitted(self) -> bool:
        """Check if scheduler has been fitted."""
        return self._is_fitted
    
    @property
    def spectral_radius(self) -> float:
        """Get current spectral radius."""
        if self._eigenvalues is None or len(self._eigenvalues) == 0:
            return 0.0
        return float(np.max(np.abs(self._eigenvalues)))
    
    @property
    def condition_number(self) -> float:
        """Get condition number of covariance matrix."""
        if self._eigenvalues is None or len(self._eigenvalues) < 2:
            return 1.0
        # Condition number = λ_max / λ_min
        return float(np.max(np.abs(self._eigenvalues)) / np.min(np.abs(self._eigenvalues)))
    
    def fit(self, returns: NDArray) -> "EigenScheduler":
        """
        Fit the scheduler on historical returns.
        
        Args:
            Returns: Array of shape (n_periods, n_assets) or (n_assets, n_periods)
            
        Returns:
            Self for method chaining
        """
        returns = np.asarray(returns, dtype=np.float64)
        
        # Handle different orientations
        if returns.shape[0] < returns.shape[1]:
            # Transpose if (n_assets, n_periods)
            returns = returns.T
        
        with self._lock:
            self._returns_buffer = list(returns)
            self._compute_covariance()
            self._is_fitted = True
        
        return self
    
    def _compute_covariance(self) -> None:
        """Compute covariance matrix and eigenvalues."""
        if len(self._returns_buffer) < self._min_samples:
            return
        
        # Stack returns
        R = np.column_stack(self._returns_buffer[-self._lookback:])
        
        if R.shape[1] < self._min_samples:
            return
        
        # Compute covariance (regularized for numerical stability)
        cov = np.cov(R)
        
        # Add small regularization for numerical stability
        regularization = 1e-8 * np.eye(self._n_assets)
        self._covariance = cov + regularization
        
        # Compute eigenvalues using scipy for stability
        try:
            eigenvalues, eigenvectors = linalg.eigh(self._covariance)
            
            # Sort eigenvalues in descending order
            idx = np.argsort(eigenvalues)[::-1]
            self._eigenvalues = eigenvalues[idx]
            self._eigenvectors = eigenvectors[:, idx]
            
        except linalg.LinAlgError:
            # Fallback to numpy
            eigenvalues = np.linalg.eigvalsh(self._covariance)
            self._eigenvalues = np.sort(eigenvalues)[::-1]
    
    def update(self, new_returns: NDArray) -> "EigenScheduler":
        """
        Update scheduler with new returns.
        
        Args:
            new_returns: New return observations
            
        Returns:
            Self for method chaining
        """
        new_returns = np.asarray(new_returns, dtype=np.float64).flatten()
        
        with self._lock:
            self._returns_buffer.append(new_returns)
            
            # Keep only lookback period
            if len(self._returns_buffer) > self._lookback:
                self._returns_buffer = self._returns_buffer[-self._lookback:]
            
            # Recompute covariance
            if len(self._returns_buffer) >= self._min_samples:
                self._compute_covariance()
        
        return self
    
    def analyze_regime(self) -> SchedulerState:
        """
        Analyze current market regime.
        
        Returns:
            SchedulerState with regime analysis
        """
        with self._lock:
            self._stats["total_evaluations"] += 1
            
            # Default state if not fitted
            if not self._is_fitted or self._eigenvalues is None:
                return SchedulerState(
                    spectral_radius=0.0,
                    condition_number=1.0,
                    regime=MarketRegime.SIDEWAYS,
                    eigenvalue_spectrum=np.array([]),
                    trend_strength=0.0,
                    timestamp=int(time.time() * 1000)
                )
            
            # Calculate metrics
            spectral_radius = self.spectral_radius
            cond_num = self.condition_number
            
            # Determine regime
            if cond_num > self._volatility_threshold:
                regime = MarketRegime.VOLATILE
            elif spectral_radius > self._trend_threshold:
                regime = MarketRegime.TREND_STRONG
            elif spectral_radius > self._trend_threshold * 0.6:
                regime = MarketRegime.TREND_WEAK
            elif spectral_radius < self._mean_reversion_threshold:
                regime = MarketRegime.MEAN_REVERTING
            else:
                regime = MarketRegime.SIDEWAYS
            
            # Calculate trend strength (normalized spectral radius)
            total_variance = np.sum(np.abs(self._eigenvalues))
            trend_strength = spectral_radius / (total_variance + 1e-10)
            
            # Update history
            self._spectral_history.append(spectral_radius)
            self._regime_history.append(regime.value)
            
            # Update statistics
            regime_key = regime.value
            self._stats["regime_counts"][regime_key] = \
                self._stats["regime_counts"].get(regime_key, 0) + 1
            
            avg_trend = np.mean(list(self._spectral_history)) if self._spectral_history else 0
            self._stats["avg_trend_strength"] = avg_trend
            
            return SchedulerState(
                spectral_radius=spectral_radius,
                condition_number=cond_num,
                regime=regime,
                eigenvalue_spectrum=self._eigenvalues.copy(),
                trend_strength=trend_strength,
                timestamp=int(time.time() * 1000)
            )
    
    def get_allocations(
        self,
        regime_weights: Optional[Dict[str, float]] = None
    ) -> List[StrategyAllocation]:
        """
        Get strategy allocations based on current regime.
        
        Args:
            regime_weights: Custom weights for each regime
            
        Returns:
            List of StrategyAllocation objects
        """
        state = self.analyze_regime()
        
        # Default regime weights
        if regime_weights is None:
            regime_weights = {
                MarketRegime.TREND_STRONG: {
                    "trend_following": 0.6,
                    "mean_reversion": 0.1,
                    "momentum": 0.3,
                },
                MarketRegime.TREND_WEAK: {
                    "trend_following": 0.4,
                    "mean_reversion": 0.3,
                    "momentum": 0.3,
                },
                MarketRegime.MEAN_REVERTING: {
                    "trend_following": 0.1,
                    "mean_reversion": 0.6,
                    "momentum": 0.3,
                },
                MarketRegime.SIDEWAYS: {
                    "trend_following": 0.2,
                    "mean_reversion": 0.4,
                    "momentum": 0.4,
                },
                MarketRegime.VOLATILE: {
                    "trend_following": 0.2,
                    "mean_reversion": 0.2,
                    "momentum": 0.1,
                    # Remaining 0.5 goes to cash/position sizing
                },
            }
        
        # Get weights for current regime
        weights = regime_weights.get(state.regime, {})
        
        # Apply volatility dampening
        volatility_factor = 1.0
        if state.condition_number > self._volatility_threshold:
            # Reduce exposure in volatile markets
            volatility_factor = max(0.1, 1.0 - (state.condition_number / self._volatility_threshold) * 0.5)
        
        allocations = []
        for strategy, base_weight in weights.items():
            confidence = 1.0 - abs(state.trend_strength - 0.5) * 0.5  # Confidence based on trend clarity
            
            allocation = StrategyAllocation(
                strategy_name=strategy,
                allocation_pct=base_weight * volatility_factor,
                confidence=confidence,
                regime=state.regime,
                metadata={
                    "spectral_radius": state.spectral_radius,
                    "condition_number": state.condition_number,
                    "trend_strength": state.trend_strength,
                }
            )
            allocations.append(allocation)
        
        return allocations
    
    def get_principal_components(self) -> Tuple[NDArray, NDArray]:
        """
        Get principal components (eigenvectors) of the covariance matrix.
        
        Returns:
            Tuple of (eigenvalues, eigenvectors)
        """
        if self._eigenvalues is None:
            return np.array([]), np.array([])
        
        return self._eigenvalues.copy(), self._eigenvectors.copy()
    
    def get_eigen_portfolios(self, n_portfolios: int = 3) -> NDArray:
        """
        Generate eigen portfolios (risk parity portfolios based on eigenvectors).
        
        These portfolios can be used for risk management or as 
        alternative allocation strategies.
        
        Args:
            n_portfolios: Number of eigen portfolios to generate
            
        Returns:
            Array of portfolio weights
        """
        if self._eigenvectors is None:
            return np.array([])
        
        # Use top n eigenvectors as portfolios
        n = min(n_portfolios, self._n_assets)
        return self._eigenvectors[:, :n]
    
    def calculate_portfolio_risk(
        self,
        weights: NDArray,
        returns: Optional[NDArray] = None
    ) -> float:
        """
        Calculate portfolio risk (variance) given weights.
        
        Args:
            weights: Portfolio weights
            returns: Optional returns for dynamic covariance
            
        Returns:
            Portfolio variance
        """
        weights = np.asarray(weights, dtype=np.float64).flatten()
        
        if self._covariance is None:
            return 0.0
        
        # Portfolio variance = w' * Σ * w
        portfolio_var = weights @ self._covariance @ weights
        return float(portfolio_var)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get scheduler statistics."""
        return {
            **self._stats,
            "current_spectral_radius": self.spectral_radius,
            "current_condition_number": self.condition_number,
            "is_fitted": self._is_fitted,
            "buffer_size": len(self._returns_buffer),
        }


class AdaptiveScheduler(EigenScheduler):
    """
    Adaptive EigenScheduler with automatic threshold learning.
    
    Extends EigenScheduler with automatic threshold adjustment
    based on historical regime detection performance.
    """
    
    def __init__(
        self,
        n_assets: int,
        lookback: int = 100,
        min_samples: int = 30,
        learning_rate: float = 0.01
    ):
        super().__init__(
            n_assets=n_assets,
            lookback=lookback,
            min_samples=min_samples
        )
        
        self._learning_rate = learning_rate
        self._regime_performance: Dict[str, List[float]] = {}
    
    def update_thresholds(
        self,
        actual_regime: MarketRegime,
        strategy_returns: float
    ) -> None:
        """
        Update thresholds based on actual regime performance.
        
        Args:
            actual_regime: The true market regime (from forward-looking data)
            strategy_returns: Returns achieved by following allocations
        """
        regime_key = actual_regime.value
        
        if regime_key not in self._regime_performance:
            self._regime_performance[regime_key] = []
        
        self._regime_performance[regime_key].append(strategy_returns)
        
        # Adjust thresholds based on performance
        if len(self._regime_performance[regime_key]) >= 10:
            avg_return = np.mean(self._regime_performance[regime_key])
            
            # If trend strategies work well, increase trend threshold
            if avg_return > 0:
                self._trend_threshold *= (1 + self._learning_rate)
            else:
                self._trend_threshold *= (1 - self._learning_rate)
    
    def get_recommended_exposure(self) -> float:
        """
        Get recommended total exposure based on regime and conditions.
        
        Returns:
            Recommended exposure (0.0 to 1.0)
        """
        state = self.analyze_regime()
        
        # Base exposure from regime
        regime_exposure = {
            MarketRegime.TREND_STRONG: 1.0,
            MarketRegime.TREND_WEAK: 0.8,
            MarketRegime.MEAN_REVERTING: 0.7,
            MarketRegime.SIDEWAYS: 0.5,
            MarketRegime.VOLATILE: 0.3,
        }
        
        base = regime_exposure.get(state.regime, 0.5)
        
        # Adjust for volatility
        if state.condition_number > 50:
            base *= 0.5
        elif state.condition_number > 20:
            base *= 0.75
        
        return min(1.0, max(0.0, base))

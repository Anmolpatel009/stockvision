"""
Jacobian-Based Sensitivity Analysis

Implements Jacobian matrix computation for portfolio risk sensitivity.
The Jacobian measures how portfolio metrics (returns, risk, etc.) change
with respect to changes in market factors.

Mathematical Background:
- Jacobian J = ∂y/∂x where y = f(x)
- For portfolio: J_ij = ∂P_i / ∂F_j
- Measures first-order sensitivity to factor changes

Used for:
- Risk factor decomposition
- Hedging strategy computation
- Factor exposure management
"""

from typing import Optional, Dict, List, Tuple, Any, Callable
from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray
from scipy import linalg
from scipy.optimize import minimize
import time
from threading import RLock
from collections import deque


@dataclass
class SensitivityResult:
    """Result of sensitivity analysis."""
    jacobian: NDArray  # Jacobian matrix
    factor_names: List[str]
    sensitivities: Dict[str, NDArray]  # Named sensitivity vectors
    max_sensitivity: float
    dominant_factor: Optional[str]
    timestamp: int


@dataclass
class FactorExposure:
    """Factor exposure of a position or portfolio."""
    factor_name: str
    exposure: float
    contribution: float  # Contribution to total risk


class JacobianSensitivity:
    """
    Jacobian-Based Portfolio Sensitivity Analysis.
    
    Computes the Jacobian matrix for portfolio returns with respect
    to various market factors. Used for risk management and hedging.
    
    Mathematical Model:
    - Let P be portfolio returns
    - Let F be factor returns (size: n_factors)
    - Jacobian J[i,j] = ∂P_i / ∂F_j
    
    Methods:
    1. Historical regression-based Jacobian estimation
    2. Numerical differentiation for arbitrary metrics
    3. Factor decomposition using PCA/SVD
    
    Example:
        >>> jacobian = JacobianSensitivity(n_factors=10, lookback=100)
        >>> jacobian.fit(factor_returns, portfolio_returns)
        >>> 
        >>> # Get sensitivities
        >>> result = jacobian.compute_sensitivity()
        >>> print(f"Dominant factor: {result.dominant_factor}")
    """
    
    def __init__(
        self,
        n_factors: int,
        lookback: int = 100,
        factor_names: Optional[List[str]] = None,
        regularization: float = 1e-6
    ):
        """
        Initialize Jacobian sensitivity analyzer.
        
        Args:
            n_factors: Number of risk factors
            lookback: Historical periods for estimation
            factor_names: Names of factors for interpretability
            regularization: Regularization parameter for stability
        """
        self._n_factors = n_factors
        self._lookback = lookback
        self._regularization = regularization
        
        # Factor names
        if factor_names:
            self._factor_names = factor_names
        else:
            self._factor_names = [f"factor_{i}" for i in range(n_factors)]
        
        # Data buffers
        self._factor_buffer: List[NDArray] = []
        self._portfolio_buffer: List[float] = []
        
        # Estimated Jacobian
        self._jacobian: Optional[NDArray] = None
        self._is_fitted = False
        
        # Statistics
        self._stats = {
            "total_evaluations": 0,
            "r_squared": 0.0,
            "avg_residual": 0.0,
        }
        
        # Lock
        self._lock = RLock()
    
    @property
    def is_fitted(self) -> bool:
        """Check if analyzer has been fitted."""
        return self._is_fitted
    
    @property
    def jacobian(self) -> Optional[NDArray]:
        """Get estimated Jacobian matrix."""
        return self._jacobian
    
    def fit(
        self,
        factor_returns: NDArray,
        portfolio_returns: NDArray
    ) -> "JacobianSensitivity":
        """
        Fit the Jacobian estimator on historical data.
        
        Uses linear regression to estimate the Jacobian matrix.
        
        Args:
            factor_returns: Factor returns (n_periods, n_factors)
            portfolio_returns: Portfolio returns (n_periods,)
            
        Returns:
            Self for method chaining
        """
        factor_returns = np.asarray(factor_returns, dtype=np.float64)
        portfolio_returns = np.asarray(portfolio_returns, dtype=np.float64)
        
        if factor_returns.shape[0] != portfolio_returns.shape[0]:
            raise ValueError("Factor and portfolio returns must have same length")
        
        with self._lock:
            # Store data
            self._factor_buffer = list(factor_returns)
            self._portfolio_buffer = list(portfolio_returns)
            
            # Compute Jacobian using OLS
            self._jacobian = self._compute_jacobian_ols(
                factor_returns, 
                portfolio_returns
            )
            
            # Compute R-squared
            predictions = factor_returns @ self._jacobian
            ss_res = np.sum((portfolio_returns - predictions) ** 2)
            ss_tot = np.sum((portfolio_returns - np.mean(portfolio_returns)) ** 2)
            self._stats["r_squared"] = 1 - ss_res / (ss_tot + 1e-10)
            self._stats["avg_residual"] = np.mean(np.abs(portfolio_returns - predictions))
            
            self._is_fitted = True
        
        return self
    
    def _compute_jacobian_ols(
        self,
        X: NDArray,
        y: NDArray
    ) -> NDArray:
        """
        Compute Jacobian using Ordinary Least Squares.
        
        J = (X'X + λI)^(-1) X'y
        
        With regularization for numerical stability.
        """
        n_samples, n_factors = X.shape
        
        # Add regularization
        XtX = X.T @ X + self._regularization * np.eye(n_factors)
        
        try:
            # Solve for Jacobian
            jacobian = linalg.solve(XtX, X.T @ y, assume_a='pos')
        except linalg.LinAlgError:
            # Fallback to pseudo-inverse
            jacobian = np.linalg.lstsq(X, y, rcond=None)[0]
        
        return jacobian
    
    def update(
        self,
        new_factor_returns: NDArray,
        new_portfolio_return: float
    ) -> "JacobianSensitivity":
        """
        Update Jacobian with new observations.
        
        Args:
            new_factor_returns: New factor returns
            new_portfolio_return: New portfolio return
            
        Returns:
            Self for method chaining
        """
        new_factor_returns = np.asarray(new_factor_returns, dtype=np.float64).flatten()
        
        with self._lock:
            # Add new observations
            self._factor_buffer.append(new_factor_returns)
            self._portfolio_buffer.append(new_portfolio_return)
            
            # Keep only lookback period
            if len(self._factor_buffer) > self._lookback:
                self._factor_buffer = self._factor_buffer[-self._lookback:]
                self._portfolio_buffer = self._portfolio_buffer[-self._lookback:]
            
            # Re-estimate Jacobian if enough data
            if len(self._factor_buffer) >= self._n_factors + 10:
                X = np.array(self._factor_buffer)
                y = np.array(self._portfolio_buffer)
                self._jacobian = self._compute_jacobian_ols(X, y)
        
        return self
    
    def compute_sensitivity(self) -> SensitivityResult:
        """
        Compute sensitivity analysis results.
        
        Returns:
            SensitivityResult with Jacobian and analysis
        """
        with self._lock:
            self._stats["total_evaluations"] += 1
            
            if self._jacobian is None:
                return SensitivityResult(
                    jacobian=np.array([]),
                    factor_names=self._factor_names,
                    sensitivities={},
                    max_sensitivity=0.0,
                    dominant_factor=None,
                    timestamp=int(time.time() * 1000)
                )
            
            # Compute sensitivities
            sensitivities = {}
            for i, name in enumerate(self._factor_names):
                sensitivities[name] = np.abs(self._jacobian[i])
            
            # Find dominant factor
            max_idx = np.argmax(np.abs(self._jacobian))
            dominant_factor = self._factor_names[max_idx] if max_idx < len(self._factor_names) else None
            
            return SensitivityResult(
                jacobian=self._jacobian.copy(),
                factor_names=self._factor_names,
                sensitivities=sensitivities,
                max_sensitivity=float(np.max(np.abs(self._jacobian))),
                dominant_factor=dominant_factor,
                timestamp=int(time.time() * 1000)
            )
    
    def compute_hedge_ratios(
        self,
        target_factor: str
    ) -> NDArray:
        """
        Compute hedge ratios for a specific factor.
        
        Returns the portfolio weights needed to neutralize
        exposure to the target factor.
        
        Args:
            target_factor: Name or index of factor to hedge
            
        Returns:
            Hedge ratios for each asset
        """
        if self._jacobian is None:
            return np.array([])
        
        # Find factor index
        if isinstance(target_factor, str):
            if target_factor not in self._factor_names:
                return np.array([])
            target_idx = self._factor_names.index(target_factor)
        else:
            target_idx = target_factor
        
        # Hedge ratio is negative of Jacobian for that factor
        hedge_ratio = -self._jacobian[target_idx]
        
        return hedge_ratio
    
    def compute_factor_contributions(
        self,
        weights: NDArray,
        factor_covariance: Optional[NDArray] = None
    ) -> List[FactorExposure]:
        """
        Compute factor contributions to portfolio risk.
        
        Args:
            weights: Portfolio weights
            factor_covariance: Optional factor covariance matrix
            
        Returns:
            List of FactorExposure objects
        """
        if self._jacobian is None or weights is None:
            return []
        
        weights = np.asarray(weights, dtype=np.float64).flatten()
        
        # Factor exposure = Jacobian' @ weights
        factor_exposure = self._jacobian @ weights
        
        # Total variance (simplified)
        total_var = np.sum(factor_exposure ** 2)
        
        contributions = []
        for i, name in enumerate(self._factor_names):
            exposure = FactorExposure(
                factor_name=name,
                exposure=float(factor_exposure[i]),
                contribution=float(factor_exposure[i] ** 2 / (total_var + 1e-10))
            )
            contributions.append(exposure)
        
        return sorted(contributions, key=lambda x: x.contribution, reverse=True)
    
    def compute_numerical_jacobian(
        self,
        f: Callable[[NDArray], float],
        x0: NDArray,
        epsilon: float = 1e-5
    ) -> NDArray:
        """
        Compute numerical Jacobian for arbitrary functions.
        
        Uses central difference approximation:
        J[i] ≈ (f(x + e_i*ε) - f(x - e_i*ε)) / (2*ε)
        
        Args:
            f: Function to differentiate (scalar output)
            x0: Point at which to evaluate
            epsilon: Step size for numerical differentiation
            
        Returns:
            Numerical Jacobian vector
        """
        x0 = np.asarray(x0, dtype=np.float64).flatten()
        n = len(x0)
        jacobian = np.zeros(n)
        
        for i in range(n):
            # Create perturbation vectors
            e = np.zeros(n)
            e[i] = epsilon
            
            # Central difference
            f_plus = f(x0 + e)
            f_minus = f(x0 - e)
            jacobian[i] = (f_plus - f_minus) / (2 * epsilon)
        
        return jacobian
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get sensitivity analyzer statistics."""
        return {
            **self._stats,
            "is_fitted": self._is_fitted,
            "buffer_size": len(self._factor_buffer),
            "jacobian_norm": float(np.linalg.norm(self._jacobian)) if self._jacobian is not None else 0.0,
        }


class MultiOutputJacobian:
    """
    Jacobian for multiple portfolio outputs.
    
    Extension of JacobianSensitivity for portfolios with multiple
    metrics (returns, volatility, drawdown, etc.).
    """
    
    def __init__(
        self,
        n_factors: int,
        n_outputs: int = 3,
        lookback: int = 100,
        factor_names: Optional[List[str]] = None,
        output_names: Optional[List[str]] = None
    ):
        self._n_factors = n_factors
        self._n_outputs = n_outputs
        self._lookback = lookback
        
        # Output names
        if output_names:
            self._output_names = output_names
        else:
            self._output_names = [f"output_{i}" for i in range(n_outputs)]
        
        # Individual Jacobians for each output
        self._jacobians: Dict[str, JacobianSensitivity] = {}
        for output_name in self._output_names:
            self._jacobians[output_name] = JacobianSensitivity(
                n_factors=n_factors,
                lookback=lookback,
                factor_names=factor_names
            )
    
    def fit(
        self,
        factor_returns: NDArray,
        output_returns: Dict[str, NDArray]
    ) -> "MultiOutputJacobian":
        """
        Fit all output Jacobians.
        
        Args:
            factor_returns: Factor returns
            output_returns: Dictionary of output returns
            
        Returns:
            Self for method chaining
        """
        for output_name, returns in output_returns.items():
            if output_name in self._jacobians:
                self._jacobians[output_name].fit(factor_returns, returns)
        
        return self
    
    def compute_jacobian_matrix(self) -> NDArray:
        """
        Compute full Jacobian matrix for all outputs.
        
        Returns:
            Jacobian matrix of shape (n_outputs, n_factors)
        """
        jacobian_matrix = []
        
        for output_name in self._output_names:
            j = self._jacobians[output_name].jacobian
            if j is not None:
                jacobian_matrix.append(j)
            else:
                jacobian_matrix.append(np.zeros(self._n_factors))
        
        return np.array(jacobian_matrix)
    
    def compute_total_sensitivity(self) -> NDArray:
        """
        Compute combined sensitivity across all outputs.
        
        Returns:
            Combined sensitivity vector
        """
        jacobian_matrix = self.compute_jacobian_matrix()
        
        # Sum of absolute sensitivities
        total_sensitivity = np.sum(np.abs(jacobian_matrix), axis=0)
        
        return total_sensitivity

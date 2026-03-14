"""
Stability Controller - Hessian-Based Trade Sizing

Implements the Stability Controller of the Quant-Kernel architecture.
Uses second-order optimization (Hessian) to determine optimal trade sizes
and prevent overshooting in volatile markets.

Mathematical Background:
- Hessian: Matrix of second derivatives of loss function
- For portfolio: H = ∂²L/∂w² where L is risk-adjusted P&L
- Trade sizing: w* = w - H^(-1) * ∇L
- Condition number: κ = λ_max/λ_min - measures market "canyon" steepness
"""

from typing import Optional, Dict, List, Tuple, Any, Callable
from dataclasses import dataclass
from enum import Enum
import numpy as np
from numpy.typing import NDArray
from scipy import linalg
from scipy.optimize import minimize
import time
from threading import RLock
from collections import deque


class OptimizationMethod(Enum):
    """Methods for Hessian-based optimization."""
    NEWTON = "newton"              # Full Newton method
    GAUSS_NEWTON = "gauss_newton"  # Gauss-Newton approximation
    GRADIENT_DESCENT = "gd"        # Gradient descent (no Hessian)
    LEVENBERG_MARQUARDT = "lm"     # Damped least squares


@dataclass
class TradeSize:
    """Recommended trade size."""
    position_size: float
    confidence: float
    risk_contribution: float
    metadata: Dict[str, Any]


@dataclass
class RiskMetrics:
    """Comprehensive risk metrics."""
    portfolio_volatility: float
    sharpe_ratio: float
    max_drawdown: float
    var_95: float  # Value at Risk at 95%
    cvar_95: float  # Conditional VaR
    condition_number: float
    leverage: float


@dataclass
class OptimizationResult:
    """Result of Hessian optimization."""
    optimal_weights: NDArray
    hessian: NDArray
    gradient: NDArray
    condition_number: float
    converged: bool
    iterations: int
    final_objective: float


class HessianOptimizer:
    """
    Hessian-Based Optimizer for Trade Sizing.
    
    Uses second-order derivatives to find optimal position sizes
    that balance return maximization with risk control.
    
    Mathematical Model:
    - Objective: Maximize risk-adjusted returns
    - Loss: L(w) = -Sharpe(w) + λ * Risk(w)
    - Hessian: H = ∂²L/∂w²
    - Update: w_new = w - α * H^(-1) * ∇L
    
    Features:
    - Automatic dampening in high condition number markets
    - Levenberg-Marquardt regularization
    - Constraint support (long-only, max position, etc.)
    
    Example:
        >>> optimizer = HessianOptimizer(n_assets=5)
        >>> optimizer.fit(returns, target_vol=0.15)
        >>> 
        >>> # Get optimal weights
        >>> result = optimizer.optimize()
        >>> print(f"Optimal weights: {result.optimal_weights}")
    """
    
    def __init__(
        self,
        n_assets: int,
        method: OptimizationMethod = OptimizationMethod.LEVENBERG_MARQUARDT,
        max_iterations: int = 100,
        tol: float = 1e-6,
        regularization: float = 1e-6
    ):
        """
        Initialize Hessian optimizer.
        
        Args:
            n_assets: Number of assets in portfolio
            method: Optimization method to use
            max_iterations: Maximum optimization iterations
            tol: Convergence tolerance
            regularization: Base regularization parameter
        """
        self._n_assets = n_assets
        self._method = method
        self._max_iterations = max_iterations
        self._tol = tol
        self._regularization = regularization
        
        # Data
        self._returns: Optional[NDArray] = None
        self._mean_returns: Optional[NDArray] = None
        self._covariance: Optional[NDArray] = None
        
        # Optimization results
        self._optimal_weights: Optional[NDArray] = None
        self._hessian: Optional[NDArray] = None
        self._gradient: Optional[NDArray] = None
        
        # State
        self._is_fitted = False
        
        # Statistics
        self._stats = {
            "total_optimizations": 0,
            "convergence_rate": 0.0,
            "avg_condition_number": 0.0,
        }
        
        # Lock
        self._lock = RLock()
    
    @property
    def is_fitted(self) -> bool:
        """Check if optimizer has been fitted."""
        return self._is_fitted
    
    @property
    def optimal_weights(self) -> Optional[NDArray]:
        """Get optimal portfolio weights."""
        return self._optimal_weights
    
    @property
    def hessian(self) -> Optional[NDArray]:
        """Get computed Hessian matrix."""
        return self._hessian
    
    def fit(
        self,
        returns: NDArray,
        method: Optional[OptimizationMethod] = None
    ) -> "HessianOptimizer":
        """
        Fit optimizer on historical returns.
        
        Args:
            returns: Historical returns (n_periods, n_assets)
            method: Optional override for optimization method
            
        Returns:
            Self for method chaining
        """
        returns = np.asarray(returns, dtype=np.float64)
        
        if method:
            self._method = method
        
        with self._lock:
            self._returns = returns
            
            # Compute statistics
            self._mean_returns = np.mean(returns, axis=0)
            self._covariance = np.cov(returns.T)
            
            # Regularize covariance
            self._covariance += self._regularization * np.eye(self._n_assets)
            
            self._is_fitted = True
        
        return self
    
    def _compute_objective(
        self,
        weights: NDArray,
        target_return: float = 0.0,
        risk_aversion: float = 1.0
    ) -> float:
        """
        Compute optimization objective (negative utility).
        
        Maximizes: μ'w - (λ/2) * w'Σw
        """
        if self._mean_returns is None or self._covariance is None:
            return 0.0
        
        weights = np.asarray(weights, dtype=np.float64).flatten()
        
        # Expected return
        ret = np.dot(self._mean_returns, weights)
        
        # Portfolio variance
        var = weights @ self._covariance @ weights
        
        # Negative utility (minimize)
        utility = ret - (risk_aversion / 2) * var
        
        return -utility
    
    def _compute_gradient(
        self,
        weights: NDArray,
        risk_aversion: float = 1.0
    ) -> NDArray:
        """
        Compute gradient of objective.
        
        ∇L = μ - λ * Σ * w
        """
        if self._mean_returns is None or self._covariance is None:
            return np.zeros(self._n_assets)
        
        weights = np.asarray(weights, dtype=np.float64).flatten()
        
        # Gradient
        gradient = self._mean_returns - risk_aversion * (self._covariance @ weights)
        
        return gradient
    
    def _compute_hessian(
        self,
        weights: NDArray,
        risk_aversion: float = 1.0
    ) -> NDArray:
        """
        Compute Hessian of objective.
        
        H = -λ * Σ (for mean-variance utility)
        """
        if self._covariance is None:
            return np.eye(self._n_assets)
        
        # Hessian = risk_aversion * covariance matrix
        hessian = risk_aversion * self._covariance
        
        return hessian
    
    def _compute_condition_number(self, hessian: NDArray) -> float:
        """Compute condition number of Hessian."""
        try:
            eigenvalues = np.linalg.eigvalsh(hessian)
            eigenvalues = np.abs(eigenvalues)
            eigenvalues = eigenvalues[eigenvalues > 1e-10]
            
            if len(eigenvalues) < 2:
                return 1.0
            
            return float(np.max(eigenvalues) / np.min(eigenvalues))
        except:
            return 1.0
    
    def optimize(
        self,
        initial_weights: Optional[NDArray] = None,
        constraints: Optional[List[Dict]] = None,
        bounds: Optional[List[Tuple[float, float]]] = None,
        risk_aversion: float = 1.0,
        target_return: Optional[float] = None
    ) -> OptimizationResult:
        """
        Perform Hessian-based optimization.
        
        Args:
            initial_weights: Starting weights (default: equal weight)
            constraints: List of constraint dictionaries
            bounds: List of (min, max) weight bounds
            risk_aversion: Risk aversion parameter
            target_return: Target return (if not maximizing return)
            
        Returns:
            OptimizationResult with optimal weights and diagnostics
        """
        if not self._is_fitted:
            raise RuntimeError("Optimizer must be fitted before optimization")
        
        with self._lock:
            self._stats["total_optimizations"] += 1
            
            # Default initial weights
            if initial_weights is None:
                initial_weights = np.ones(self._n_assets) / self._n_assets
            else:
                initial_weights = np.asarray(initial_weights, dtype=np.float64).flatten()
            
            # Default bounds (long-only, max 40% per asset)
            if bounds is None:
                bounds = [(0.0, 0.4) for _ in range(self._n_assets)]
            
            # Default constraint (weights sum to 1)
            if constraints is None:
                constraints = [
                    {"type": "eq", "fun": lambda w: np.sum(w) - 1.0}
                ]
            
            # Run optimization based on method
            if self._method == OptimizationMethod.NEWTON:
                result = self._optimize_newton(
                    initial_weights, bounds, risk_aversion
                )
            elif self._method == OptimizationMethod.LEVENBERG_MARQUARDT:
                result = self._optimize_lm(
                    initial_weights, constraints, bounds, risk_aversion
                )
            else:
                result = self._optimize_scipy(
                    initial_weights, constraints, bounds, risk_aversion
                )
            
            # Store results
            self._optimal_weights = result.optimal_weights
            self._hessian = result.hessian
            self._gradient = result.gradient
            
            return result
    
    def _optimize_newton(
        self,
        initial_weights: NDArray,
        bounds: List[Tuple[float, float]],
        risk_aversion: float
    ) -> OptimizationResult:
        """Newton's method optimization with line search."""
        weights = initial_weights.copy()
        converged = False
        iterations = 0
        
        for i in range(self._max_iterations):
            # Compute gradient and Hessian
            gradient = self._compute_gradient(weights, risk_aversion)
            hessian = self._compute_hessian(weights, risk_aversion)
            
            # Compute condition number for dampening
            cond_num = self._compute_condition_number(hessian)
            
            # Dampen if ill-conditioned
            if cond_num > 100:
                dampening = 0.1
            elif cond_num > 10:
                dampening = 0.5
            else:
                dampening = 1.0
            
            # Solve for Newton step
            try:
                # Add small regularization for stability
                hessian_reg = hessian + 1e-6 * np.eye(self._n_assets)
                step = linalg.solve(hessian_reg, gradient, assume_a='pos')
            except:
                step = gradient
            
            # Line search
            alpha = 1.0
            for _ in range(10):
                new_weights = weights - alpha * dampening * step
                
                # Apply bounds
                new_weights = np.clip(new_weights, 
                                      [b[0] for b in bounds],
                                      [b[1] for b in bounds])
                
                # Normalize
                new_weights = new_weights / np.sum(new_weights)
                
                if self._compute_objective(new_weights, risk_aversion=risk_aversion) < \
                   self._compute_objective(weights, risk_aversion=risk_aversion):
                    weights = new_weights
                    alpha *= 0.5
                else:
                    break
            
            # Check convergence
            grad_norm = np.linalg.norm(gradient)
            if grad_norm < self._tol:
                converged = True
                break
            
            iterations = i + 1
        
        final_obj = self._compute_objective(weights, risk_aversion=risk_aversion)
        
        return OptimizationResult(
            optimal_weights=weights,
            hessian=self._compute_hessian(weights, risk_aversion),
            gradient=self._compute_gradient(weights, risk_aversion),
            condition_number=self._compute_condition_number(
                self._compute_hessian(weights, risk_aversion)
            ),
            converged=converged,
            iterations=iterations,
            final_objective=final_obj
        )
    
    def _optimize_lm(
        self,
        initial_weights: NDArray,
        constraints: List[Dict],
        bounds: List[Tuple[float, float]],
        risk_aversion: float
    ) -> OptimizationResult:
        """Levenberg-Marquardt optimization."""
        result = minimize(
            fun=lambda w: self._compute_objective(w, risk_aversion=risk_aversion),
            x0=initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'maxiter': self._max_iterations, 'ftol': self._tol}
        )
        
        return OptimizationResult(
            optimal_weights=result.x,
            hessian=self._compute_hessian(result.x, risk_aversion),
            gradient=self._compute_gradient(result.x, risk_aversion),
            condition_number=self._compute_condition_number(
                self._compute_hessian(result.x, risk_aversion)
            ),
            converged=result.success,
            iterations=result.nit,
            final_objective=result.fun
        )
    
    def _optimize_scipy(
        self,
        initial_weights: NDArray,
        constraints: List[Dict],
        bounds: List[Tuple[float, float]],
        risk_aversion: float
    ) -> OptimizationResult:
        """SciPy general optimization."""
        return self._optimize_lm(initial_weights, constraints, bounds, risk_aversion)
    
    def compute_trade_size(
        self,
        current_weights: NDArray,
        target_weights: NDArray,
        capital: float = 100000.0,
        max_trade_pct: float = 0.1
    ) -> TradeSize:
        """
        Compute optimal trade size using Hessian information.
        
        Args:
            current_weights: Current portfolio weights
            target_weights: Target portfolio weights
            capital: Total capital
            max_trade_pct: Maximum trade as percentage of capital
            
        Returns:
            TradeSize recommendation
        """
        current_weights = np.asarray(current_weights, dtype=np.float64).flatten()
        target_weights = np.asarray(target_weights, dtype=np.float64).flatten()
        
        # Calculate weight changes
        weight_diff = target_weights - current_weights
        
        # Use inverse Hessian to scale trades
        if self._hessian is not None:
            try:
                hessian_inv = linalg.inv(self._hessian + 1e-6 * np.eye(self._n_assets))
                
                # Scale by inverse Hessian (larger for low-risk assets)
                scaling = np.diag(hessian_inv)
                scaling = scaling / np.max(scaling)  # Normalize
            except:
                scaling = np.ones(self._n_assets)
        else:
            scaling = np.ones(self._n_assets)
        
        # Adjust trade sizes
        adjusted_diff = weight_diff * scaling
        
        # Apply maximum trade constraint
        max_trade = max_trade_pct * capital
        trade_values = np.abs(adjusted_diff * capital)
        
        if np.any(trade_values > max_trade):
            scale_factor = max_trade / np.max(trade_values)
            adjusted_diff *= scale_factor
        
        # Calculate confidence based on condition number
        if self._hessian is not None:
            cond_num = self._compute_condition_number(self._hessian)
            confidence = min(1.0, 10.0 / cond_num)
        else:
            confidence = 0.5
        
        # Risk contribution
        if self._covariance is not None:
            risk_contrib = np.abs(adjusted_diff) @ self._covariance @ np.abs(adjusted_diff)
            risk_contrib = float(np.sqrt(risk_contrib))
        else:
            risk_contrib = 0.0
        
        total_trade = float(np.sum(np.abs(adjusted_diff * capital)))
        
        return TradeSize(
            position_size=total_trade,
            confidence=confidence,
            risk_contribution=risk_contrib,
            metadata={
                "weight_changes": adjusted_diff.tolist(),
                "condition_number": self._compute_condition_number(self._hessian) if self._hessian is not None else 1.0,
            }
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get optimizer statistics."""
        return {
            **self._stats,
            "is_fitted": self._is_fitted,
            "condition_number": self._compute_condition_number(self._hessian) if self._hessian is not None else 1.0,
        }


class StabilityController:
    """
    Stability Controller for the Quant-Kernel.
    
    Combines Hessian optimization with market regime detection
    to provide adaptive trade sizing and risk management.
    
    Features:
    - Automatic exposure adjustment based on market conditions
    - Pathological curvature detection (high condition number)
    - Overshoot prevention via Hessian-based scaling
    - Real-time risk metric computation
    """
    
    def __init__(
        self,
        n_assets: int,
        lookback: int = 100,
        base_risk_aversion: float = 1.0
    ):
        """
        Initialize Stability Controller.
        
        Args:
            n_assets: Number of assets
            lookback: Historical periods for estimation
            base_risk_aversion: Base risk aversion parameter
        """
        self._n_assets = n_assets
        self._lookback = lookback
        self._base_risk_aversion = base_risk_aversion
        
        # Optimizer
        self._optimizer = HessianOptimizer(n_assets)
        
        # Risk history
        self._risk_history: deque = deque(maxlen=1000)
        
        # State
        self._is_initialized = False
        
        # Statistics
        self._stats = {
            "total_adjustments": 0,
            "dampened_trades": 0,
            "avg_risk_contribution": 0.0,
        }
    
    def initialize(
        self,
        returns: NDArray
    ) -> "StabilityController":
        """
        Initialize controller with historical returns.
        
        Args:
            returns: Historical returns
            
        Returns:
            Self for method chaining
        """
        self._optimizer.fit(returns)
        self._is_initialized = True
        
        # Compute initial risk metrics
        self._update_risk_metrics(returns)
        
        return self
    
    def _update_risk_metrics(self, returns: NDArray) -> None:
        """Update internal risk metrics."""
        if len(returns) < 2:
            return
        
        returns = np.asarray(returns, dtype=np.float64)
        
        # Compute metrics
        portfolio_returns = np.sum(returns, axis=1) / self._n_assets
        
        metrics = RiskMetrics(
            portfolio_volatility=float(np.std(portfolio_returns) * np.sqrt(252)),
            sharpe_ratio=float(np.mean(portfolio_returns) / (np.std(portfolio_returns) + 1e-10) * np.sqrt(252)),
            max_drawdown=self._compute_max_drawdown(portfolio_returns),
            var_95=float(np.percentile(portfolio_returns, 5)),
            cvar_95=float(np.mean(portfolio_returns[portfolio_returns <= np.percentile(portfolio_returns, 5)])),
            condition_number=self._optimizer._compute_condition_number(
                np.cov(returns.T)
            ) if len(returns) > self._n_assets else 1.0,
            leverage=float(np.sum(np.abs(returns), axis=1).max())
        )
        
        self._risk_history.append(metrics)
    
    def _compute_max_drawdown(self, returns: NDArray) -> float:
        """Compute maximum drawdown."""
        cumulative = np.cumprod(1 + returns)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / running_max
        return float(np.min(drawdown))
    
    def get_adjusted_risk_aversion(
        self,
        condition_number: float,
        volatility: float
    ) -> float:
        """
        Get risk aversion adjusted for market conditions.
        
        Args:
            condition_number: Current condition number
            volatility: Current volatility
            
        Returns:
            Adjusted risk aversion
        """
        # Base risk aversion
        risk_aversion = self._base_risk_aversion
        
        # Increase risk aversion in volatile markets
        if volatility > 0.3:
            risk_aversion *= 2.0
        elif volatility > 0.2:
            risk_aversion *= 1.5
        
        # Increase risk aversion in ill-conditioned markets
        if condition_number > 100:
            risk_aversion *= 3.0
        elif condition_number > 50:
            risk_aversion *= 2.0
        elif condition_number > 20:
            risk_aversion *= 1.5
        
        return risk_aversion
    
    def compute_optimal_weights(
        self,
        current_returns: NDArray,
        condition_number: float = 1.0,
        volatility: float = 0.15
    ) -> NDArray:
        """
        Compute optimal weights with stability adjustments.
        
        Args:
            current_returns: Recent returns
            condition_number: Current condition number
            volatility: Current volatility
            
        Returns:
            Optimal portfolio weights
        """
        if not self._is_initialized:
            self.initialize(current_returns)
        
        # Get adjusted risk aversion
        risk_aversion = self.get_adjusted_risk_aversion(condition_number, volatility)
        
        # Optimize
        result = self._optimizer.optimize(risk_aversion=risk_aversion)
        
        # Track dampened trades
        if condition_number > 20:
            self._stats["dampened_trades"] += 1
        
        self._stats["total_adjustments"] += 1
        
        return result.optimal_weights
    
    def get_risk_metrics(self) -> Optional[RiskMetrics]:
        """Get current risk metrics."""
        if self._risk_history:
            return self._risk_history[-1]
        return None
    
    def get_risk_history(self, n: int = 100) -> List[RiskMetrics]:
        """Get historical risk metrics."""
        return list(self._risk_history)[-n:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get controller statistics."""
        return {
            **self._stats,
            "is_initialized": self._is_initialized,
            "risk_history_size": len(self._risk_history),
        }

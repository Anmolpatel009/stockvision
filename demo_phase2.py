"""
Demo script for Quant-Kernel Phase 2: The Logic

This script demonstrates:
1. EigenScheduler for dynamic capital allocation
2. Jacobian-based sensitivity analysis
3. StabilityController with Hessian optimization
4. PortfolioManager orchestrating all components
"""

import numpy as np
import time
import sys

sys.path.insert(0, '.')

from quant_kernel.scheduler import (
    EigenScheduler, 
    MarketRegime,
    StrategyAllocation
)
from quant_kernel.controller.jacobian import JacobianSensitivity
from quant_kernel.controller.stability import (
    StabilityController, 
    HessianOptimizer,
    RiskMetrics
)
from quant_kernel.controller.portfolio import PortfolioManager, Signal


def demo_eigen_scheduler():
    """Demonstrate EigenScheduler with spectral radius analysis."""
    print("=" * 60)
    print("DEMO: EigenScheduler - Spectral Radius Analysis")
    print("=" * 60)
    
    # Generate synthetic correlated returns
    np.random.seed(42)
    n_periods = 200
    n_assets = 5
    
    # Create correlation structure
    base_returns = np.random.randn(n_periods, n_assets)
    
    # Add correlation (assets move together)
    trend_factor = np.random.randn(n_periods) * 0.5
    for i in range(n_assets):
        base_returns[:, i] += trend_factor
    
    # Fit scheduler
    scheduler = EigenScheduler(n_assets=n_assets, lookback=100)
    scheduler.fit(base_returns)
    
    # Analyze regime
    state = scheduler.analyze_regime()
    
    print(f"Current regime: {state.regime.value}")
    print(f"Spectral radius: {state.spectral_radius:.4f}")
    print(f"Condition number: {state.condition_number:.2f}")
    print(f"Trend strength: {state.trend_strength:.4f}")
    
    # Get allocations
    allocations = scheduler.get_allocations()
    print(f"\nStrategy allocations:")
    for alloc in allocations:
        print(f"  {alloc.strategy_name}: {alloc.allocation_pct*100:.1f}% "
              f"(confidence: {alloc.confidence:.2f})")
    
    # Simulate new returns and update
    new_returns = np.random.randn(n_assets) * 0.01
    scheduler.update(new_returns)
    
    state2 = scheduler.analyze_regime()
    print(f"\nAfter update:")
    print(f"  Regime: {state2.regime.value}")
    print(f"  Spectral radius: {state2.spectral_radius:.4f}")
    
    print()


def demo_jacobian_sensitivity():
    """Demonstrate Jacobian sensitivity analysis."""
    print("=" * 60)
    print("DEMO: Jacobian Sensitivity Analysis")
    print("=" * 60)
    
    # Generate factor returns
    np.random.seed(42)
    n_periods = 100
    n_factors = 5
    
    factor_returns = np.random.randn(n_periods, n_factors) * 0.02
    
    # Generate portfolio returns (linear combination + noise)
    true_jacobian = np.array([0.3, 0.25, 0.2, 0.15, 0.1])
    portfolio_returns = factor_returns @ true_jacobian + np.random.randn(n_periods) * 0.01
    
    # Fit Jacobian
    jacobian = JacobianSensitivity(n_factors=n_factors, lookback=50)
    jacobian.fit(factor_returns, portfolio_returns)
    
    # Compute sensitivity
    result = jacobian.compute_sensitivity()
    
    print(f"Estimated Jacobian: {result.jacobian}")
    print(f"True Jacobian: {true_jacobian}")
    print(f"Dominant factor: {result.dominant_factor}")
    print(f"Max sensitivity: {result.max_sensitivity:.4f}")
    
    # Statistics
    stats = jacobian.get_statistics()
    print(f"\nR-squared: {stats['r_squared']:.4f}")
    print(f"Avg residual: {stats['avg_residual']:.6f}")
    
    # Hedge ratios
    hedge = jacobian.compute_hedge_ratios(target_factor=0)
    print(f"\nHedge ratios for factor 0: {hedge}")
    
    print()


def demo_hessian_optimizer():
    """Demonstrate Hessian-based optimization."""
    print("=" * 60)
    print("DEMO: Hessian Optimizer")
    print("=" * 60)
    
    # Generate returns
    np.random.seed(42)
    n_periods = 100
    n_assets = 5
    
    returns = np.random.randn(n_periods, n_assets) * 0.02
    
    # Fit optimizer
    optimizer = HessianOptimizer(n_assets=n_assets)
    optimizer.fit(returns)
    
    # Optimize
    result = optimizer.optimize(risk_aversion=1.0)
    
    print(f"Optimal weights: {result.optimal_weights}")
    print(f"Condition number: {result.condition_number:.2f}")
    print(f"Converged: {result.converged}")
    print(f"Iterations: {result.iterations}")
    
    # Compute trade size
    current_weights = np.ones(n_assets) / n_assets
    trade_size = optimizer.compute_trade_size(
        current_weights=current_weights,
        target_weights=result.optimal_weights,
        capital=100000.0
    )
    
    print(f"\nTrade size recommendation:")
    print(f"  Total: ${trade_size.position_size:,.2f}")
    print(f"  Confidence: {trade_size.confidence:.2f}")
    print(f"  Risk contribution: {trade_size.risk_contribution:.4f}")
    
    print()


def demo_stability_controller():
    """Demonstrate Stability Controller."""
    print("=" * 60)
    print("DEMO: Stability Controller")
    print("=" * 60)
    
    # Generate returns with different regimes
    np.random.seed(42)
    n_periods = 200
    n_assets = 5
    
    # Low volatility regime
    returns_low_vol = np.random.randn(n_periods, n_assets) * 0.01
    
    # High volatility regime
    returns_high_vol = np.random.randn(n_periods, n_assets) * 0.05
    
    # Initialize controller
    controller = StabilityController(n_assets=n_assets, lookback=100)
    controller.initialize(returns_low_vol)
    
    # Get risk metrics
    metrics = controller.get_risk_metrics()
    print(f"Low volatility regime:")
    print(f"  Volatility: {metrics.portfolio_volatility:.4f}")
    print(f"  Sharpe: {metrics.sharpe_ratio:.4f}")
    print(f"  Condition number: {metrics.condition_number:.2f}")
    
    # Compute optimal weights
    weights = controller.compute_optimal_weights(
        returns_low_vol,
        condition_number=metrics.condition_number,
        volatility=metrics.portfolio_volatility
    )
    print(f"  Optimal weights: {weights}")
    
    # Now with high volatility
    controller.initialize(returns_high_vol)
    metrics = controller.get_risk_metrics()
    
    print(f"\nHigh volatility regime:")
    print(f"  Volatility: {metrics.portfolio_volatility:.4f}")
    print(f"  Condition number: {metrics.condition_number:.2f}")
    
    weights = controller.compute_optimal_weights(
        returns_high_vol,
        condition_number=metrics.condition_number,
        volatility=metrics.portfolio_volatility
    )
    print(f"  Optimal weights: {weights}")
    
    # Note: High volatility should result in more conservative weights
    print()


def demo_portfolio_manager():
    """Demonstrate Portfolio Manager."""
    print("=" * 60)
    print("DEMO: Portfolio Manager")
    print("=" * 60)
    
    # Initialize
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    pm = PortfolioManager(symbols=symbols, initial_capital=100000)
    
    # Generate historical data
    np.random.seed(42)
    n_periods = 200
    n_assets = len(symbols)
    
    historical_returns = np.random.randn(n_periods, n_assets) * 0.02
    
    # Initialize
    pm.initialize(historical_returns)
    
    # Get state
    state = pm.get_portfolio_state()
    print(f"Initial state:")
    print(f"  Cash: ${state.cash:,.2f}")
    print(f"  Total value: ${state.total_value:,.2f}")
    print(f"  Regime: {state.regime.value}")
    
    # Get signals
    signals = pm.get_signals(min_confidence=0.3)
    print(f"\nGenerated {len(signals)} signals")
    for signal in signals[:3]:
        print(f"  {signal.symbol}: {signal.direction} "
              f"(${signal.size:,.2f}, confidence: {signal.confidence:.2f})")
    
    # Statistics
    stats = pm.get_statistics()
    print(f"\nStatistics:")
    print(f"  Total optimizations: {stats['stability_stats']['total_adjustments']}")
    print(f"  Dampened trades: {stats['stability_stats']['dampened_trades']}")
    
    print()


def main():
    """Run all Phase 2 demos."""
    print("\n" + "=" * 60)
    print("QUANT-KERNEL PHASE 2 DEMO")
    print("The Logic: Scheduler, Jacobian, Stability Controller")
    print("=" * 60 + "\n")
    
    demo_eigen_scheduler()
    demo_jacobian_sensitivity()
    demo_hessian_optimizer()
    demo_stability_controller()
    demo_portfolio_manager()
    
    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("\nNext: Phase 3 - The Dashboard")
    print("  - CLI/Web System Monitor")
    print("  - Backtest engine")


if __name__ == "__main__":
    main()

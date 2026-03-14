"""
Demo script for Quant-Kernel Phase 3: The Dashboard

This script demonstrates:
1. System Monitor (CLI) showing Volatility as System Load
2. Backtest Engine with SVD-denoised historical data
"""

import numpy as np
import sys

sys.path.insert(0, '.')

from quant_kernel.dashboard.monitor import (
    SystemMonitor, 
    MonitorMetrics,
    MetricType
)
from quant_kernel.dashboard.backtest import (
    BacktestEngine,
    SVDDenoiser,
    generate_signals_from_regime
)


def demo_system_monitor():
    """Demonstrate System Monitor."""
    print("=" * 60)
    print("DEMO: System Monitor Dashboard")
    print("=" * 60)
    
    # Create monitor
    monitor = SystemMonitor(theme="default")
    
    # Simulate high volatility scenario
    print("\n--- High Volatility Scenario ---")
    monitor.update_metrics(
        cpu_usage=75.5,
        memory_usage=45.2,
        network_latency=12.3,
        system_load=85.0,
        tick_rate=1250.0,
        regime="trend_strong",
        spectral_radius=0.75,
        condition_number=125.0,
        sharpe_ratio=1.25,
        max_drawdown=-0.08,
        total_pnl=15420.50,
        open_positions=5
    )
    print(monitor.render())
    
    # Low volatility scenario
    print("\n--- Low Volatility Scenario ---")
    monitor.update_metrics(
        cpu_usage=25.0,
        memory_usage=30.0,
        network_latency=5.2,
        system_load=25.0,
        tick_rate=450.0,
        regime="sideways",
        spectral_radius=0.15,
        condition_number=8.0,
        sharpe_ratio=0.85,
        max_drawdown=-0.03,
        total_pnl=8420.00,
        open_positions=3
    )
    print(monitor.render())
    
    # Minimal theme
    print("\n--- Minimal Theme ---")
    monitor_minimal = SystemMonitor(theme="minimal")
    monitor_minimal.update_metrics(
        system_load=55.0,
        regime="mean_reverting",
        total_pnl=12350.00,
        sharpe_ratio=1.05
    )
    print(monitor_minimal.render())
    
    # Dark theme
    print("\n--- Dark Theme ---")
    monitor_dark = SystemMonitor(theme="dark")
    monitor_dark.update_metrics(
        system_load=70.0,
        regime="volatile",
        total_pnl=-2500.00,
        sharpe_ratio=0.45,
        spectral_radius=0.65,
        condition_number=95.0,
        cpu_usage=60.0,
        memory_usage=55.0,
        tick_rate=890.0
    )
    print(monitor_dark.render())
    
    print()


def demo_svd_denoiser():
    """Demonstrate SVD Denoiser."""
    print("=" * 60)
    print("DEMO: SVD Denoiser")
    print("=" * 60)
    
    # Generate synthetic noisy price data
    np.random.seed(42)
    n_periods = 200
    n_assets = 3
    
    # True signal (smooth trend)
    t = np.linspace(0, 10, n_periods)
    true_signal = np.column_stack([
        100 + 10 * np.sin(t),
        50 + 5 * t,
        80 + 15 * np.cos(t * 0.5)
    ])
    
    # Add noise
    noise = np.random.randn(n_periods, n_assets) * 5
    prices = true_signal + noise
    
    print(f"Original price std: {np.std(np.diff(prices, axis=0), axis=0)}")
    print(f"True signal std: {np.std(np.diff(true_signal, axis=0), axis=0)}")
    
    # Fit denoiser
    denoiser = SVDDenoiser(n_components=3, window_size=30)
    denoiser.fit(prices)
    
    # Denoise
    denoised_prices = denoiser.transform(prices)
    
    print(f"\nDenoised price std: {np.std(np.diff(denoised_prices.reshape(-1, 1), axis=0))}")
    print(f"Denoiser is fitted: {denoiser.is_fitted}")
    
    # Test denoise returns
    returns = np.diff(prices[:, 0]) / prices[:-1, 0]
    denoised_returns, noise_returns = denoiser.denoise_returns(returns)
    
    print(f"\nOriginal returns std: {np.std(returns):.6f}")
    print(f"Denoised returns std: {np.std(denoised_returns):.6f}")
    print(f"Noise returns std: {np.std(noise_returns):.6f}")
    
    print()


def demo_backtest_engine():
    """Demonstrate Backtest Engine with SVD."""
    print("=" * 60)
    print("DEMO: Backtest Engine with SVD-Denoising")
    print("=" * 60)
    
    # Generate synthetic data
    np.random.seed(42)
    n_periods = 500
    n_assets = 3
    
    # Generate prices with trend
    t = np.linspace(0, 20, n_periods)
    base_prices = np.column_stack([
        100 + 10 * t + np.random.randn(n_periods) * 2,
        50 + 3 * t + np.random.randn(n_periods) * 1.5,
        80 + 8 * t + np.random.randn(n_periods) * 3,
    ])
    
    # Generate signals
    signals = generate_signals_from_regime("trend_strong", base_prices)
    
    print(f"Price data shape: {base_prices.shape}")
    print(f"Signal data shape: {signals.shape}")
    
    # Run backtest WITHOUT denoising
    print("\n--- Backtest WITHOUT SVD Denoising ---")
    engine = BacktestEngine(
        initial_capital=100000,
        commission_pct=0.001,
        slippage_pct=0.0005
    )
    result = engine.run(base_prices, signals)
    
    print(f"Total Return: {result.total_return*100:.2f}%")
    print(f"Sharpe Ratio: {result.sharpe_ratio:.4f}")
    print(f"Max Drawdown: {result.max_drawdown*100:.2f}%")
    print(f"Win Rate: {result.win_rate*100:.2f}%")
    print(f"Profit Factor: {result.profit_factor:.4f}")
    print(f"Total Trades: {result.num_trades}")
    
    # Run backtest WITH denoising
    print("\n--- Backtest WITH SVD Denoising ---")
    denoiser = SVDDenoiser(n_components=3, window_size=30)
    engine_denoised = BacktestEngine(
        initial_capital=100000,
        commission_pct=0.001,
        slippage_pct=0.0005
    )
    engine_denoised.set_denoiser(denoiser)
    
    result_denoised = engine_denoised.run(base_prices, signals)
    
    print(f"Total Return: {result_denoised.total_return*100:.2f}%")
    print(f"Sharpe Ratio: {result_denoised.sharpe_ratio:.4f}")
    print(f"Max Drawdown: {result_denoised.max_drawdown*100:.2f}%")
    print(f"Win Rate: {result_denoised.win_rate*100:.2f}%")
    print(f"Profit Factor: {result_denoised.profit_factor:.4f}")
    print(f"Total Trades: {result_denoised.num_trades}")
    
    # Comparison
    print("\n--- Comparison ---")
    print(f"Sharpe Improvement: {(result_denoised.sharpe_ratio - result.sharpe_ratio)/max(0.01, result.sharpe_ratio)*100:.1f}%")
    print(f"Max DD Improvement: {(result.max_drawdown - result_denoised.max_drawdown)/abs(result.max_drawdown)*100:.1f}%")
    
    print()


def demo_full_workflow():
    """Demonstrate full Quant-Kernel workflow."""
    print("=" * 60)
    print("DEMO: Full Quant-Kernel Workflow")
    print("=" * 60)
    
    # Step 1: Generate data
    np.random.seed(42)
    n_periods = 300
    n_assets = 5
    
    prices = 100 + np.cumsum(np.random.randn(n_periods, n_assets) * 2, axis=0)
    
    # Step 2: Create SVD denoiser and denoise
    denoiser = SVDDenoiser(n_components=3, window_size=30)
    denoised_prices = np.zeros_like(prices)
    for i in range(n_assets):
        denoiser.fit(prices[:, i:i+1])
        denoised_prices[:, i] = denoiser.transform(prices[:, i:i+1]).flatten()
    
    # Step 3: Generate signals
    signals = generate_signals_from_regime("trend_strong", denoised_prices)
    
    # Step 4: Run backtest with denoising
    engine = BacktestEngine(initial_capital=100000)
    engine.set_denoiser(denoiser)
    result = engine.run(prices, signals)
    
    # Step 5: Create system monitor with results
    monitor = SystemMonitor(theme="default")
    monitor.update_metrics(
        system_load=min(100, abs(result.sharpe_ratio) * 50),
        regime="trend_strong" if result.total_return > 0 else "sideways",
        total_pnl=result.total_return * 100000,
        sharpe_ratio=result.sharpe_ratio,
        max_drawdown=result.max_drawdown,
        tick_rate=100.0,
        cpu_usage=result.sharpe_ratio * 30,
        memory_usage=50.0
    )
    
    print("\nFinal Portfolio State:")
    print(monitor.render())
    
    print(f"\nBacktest Summary:")
    print(f"  Return: {result.total_return*100:.2f}%")
    print(f"  Sharpe: {result.sharpe_ratio:.2f}")
    print(f"  Max DD: {result.max_drawdown*100:.2f}%")
    print(f"  Trades: {result.num_trades}")
    
    print()


def main():
    """Run all Phase 3 demos."""
    print("\n" + "=" * 60)
    print("QUANT-KERNEL PHASE 3 DEMO")
    print("The Dashboard: System Monitor & Backtest")
    print("=" * 60 + "\n")
    
    demo_system_monitor()
    demo_svd_denoiser()
    demo_backtest_engine()
    demo_full_workflow()
    
    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("\nQuant-Kernel Project Complete!")
    print("All three phases have been implemented:")
    print("  1. InterruptHandler + FeatureMMU")
    print("  2. EigenScheduler + Jacobian + StabilityController")
    print("  3. System Monitor + Backtest Engine")


if __name__ == "__main__":
    main()

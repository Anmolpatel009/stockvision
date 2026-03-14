"""
Dashboard Module - System Monitor and Visualization

Provides system monitoring dashboard for the Quant-Kernel:
1. CLI-based system monitor (System Load = Volatility)
2. Web-based dashboard
3. Backtesting engine with SVD-denoised data
"""

from quant_kernel.dashboard.monitor import SystemMonitor, MonitorMetrics
from quant_kernel.dashboard.backtest import BacktestEngine, BacktestResult

__all__ = [
    "SystemMonitor",
    "MonitorMetrics",
    "BacktestEngine",
    "BacktestResult",
]

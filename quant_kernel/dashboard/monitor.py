"""
System Monitor Dashboard

CLI-based system monitor that treats market volatility as "system load".
Provides real-time visualization of the Quant-Kernel's internal state.
"""

from typing import Optional, Dict, List, Any, Callable
from dataclasses import dataclass
from enum import Enum
import numpy as np
from numpy.typing import NDArray
import time
from threading import RLock
from collections import deque
import sys


class MetricType(Enum):
    """Types of system metrics."""
    CPU = "cpu"          # In our case: Strategy computation load
    MEMORY = "memory"   # Feature buffer usage
    NETWORK = "network" # Data feed latency
    DISK = "disk"       # Historical data storage
    LOAD = "load"       # Volatility (custom)


@dataclass
class MonitorMetrics:
    """System monitoring metrics."""
    timestamp: int
    cpu_usage: float      # Strategy computation time
    memory_usage: float   # Feature buffer utilization
    network_latency: float # Data feed latency (ms)
    system_load: float    # Volatility as load (0-100%)
    tick_rate: float      # Ticks per second
    regime: str           # Current market regime
    spectral_radius: float
    condition_number: float
    
    # Optional extended metrics
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    total_pnl: float = 0.0
    open_positions: int = 0


class SystemMonitor:
    """
    Real-time System Monitor for Quant-Kernel.
    
    Provides a CLI dashboard that displays:
    - Volatility as System Load
    - Strategy CPU usage
    - Memory (buffer) utilization
    - Network (latency) metrics
    - Key risk metrics
    
    Similar to `top` or `htop` for the trading system.
    
    Example:
        >>> monitor = SystemMonitor(refresh_rate=1.0)
        >>> 
        >>> # Update with current metrics
        >>> monitor.update_metrics(
        ...     cpu_usage=45.2,
        ...     memory_usage=67.8,
        ...     system_load=75.0,
        ...     regime="trend_strong"
        ... )
        >>> 
        >>> # Render dashboard
        >>> monitor.render()
    """
    
    def __init__(
        self,
        refresh_rate: float = 1.0,
        history_size: int = 60,
        theme: str = "default"
    ):
        """
        Initialize system monitor.
        
        Args:
            refresh_rate: Dashboard refresh rate (seconds)
            history_size: Number of historical data points to keep
            theme: Display theme (default, dark, minimal)
        """
        self._refresh_rate = refresh_rate
        self._history_size = history_size
        self._theme = theme
        
        # Metrics history
        self._metrics_history: deque = deque(maxlen=history_size)
        
        # Current metrics
        self._current_metrics: Optional[MonitorMetrics] = None
        
        # Callbacks for external data
        self._data_callbacks: Dict[MetricType, Callable] = {}
        
        # Lock
        self._lock = RLock()
        
        # Statistics
        self._stats = {
            "total_updates": 0,
            "start_time": time.time(),
        }
    
    def update_metrics(
        self,
        cpu_usage: float = 0.0,
        memory_usage: float = 0.0,
        network_latency: float = 0.0,
        system_load: float = 0.0,
        tick_rate: float = 0.0,
        regime: str = "unknown",
        spectral_radius: float = 0.0,
        condition_number: float = 1.0,
        sharpe_ratio: float = 0.0,
        max_drawdown: float = 0.0,
        total_pnl: float = 0.0,
        open_positions: int = 0,
        **kwargs
    ) -> None:
        """
        Update current metrics.
        
        Args:
            cpu_usage: Strategy computation usage (0-100%)
            memory_usage: Feature buffer utilization (0-100%)
            network_latency: Data feed latency (ms)
            system_load: Volatility as load (0-100%)
            tick_rate: Ticks per second
            regime: Current market regime
            spectral_radius: Current spectral radius
            condition_number: Current condition number
            sharpe_ratio: Current Sharpe ratio
            max_drawdown: Current max drawdown
            total_pnl: Total P&L
            open_positions: Number of open positions
        """
        metrics = MonitorMetrics(
            timestamp=int(time.time() * 1000),
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            network_latency=network_latency,
            system_load=system_load,
            tick_rate=tick_rate,
            regime=regime,
            spectral_radius=spectral_radius,
            condition_number=condition_number,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            total_pnl=total_pnl,
            open_positions=open_positions,
        )
        
        with self._lock:
            self._current_metrics = metrics
            self._metrics_history.append(metrics)
            self._stats["total_updates"] += 1
    
    def register_callback(
        self,
        metric_type: MetricType,
        callback: Callable[[], float]
    ) -> None:
        """
        Register a callback for automatic metric updates.
        
        Args:
            metric_type: Type of metric
            callback: Function that returns the metric value
        """
        self._data_callbacks[metric_type] = callback
    
    def _fetch_callback_metrics(self) -> Dict[MetricType, float]:
        """Fetch metrics from registered callbacks."""
        results = {}
        for metric_type, callback in self._data_callbacks.items():
            try:
                results[metric_type] = callback()
            except:
                results[metric_type] = 0.0
        return results
    
    def render(self) -> str:
        """
        Render the dashboard to a string.
        
        Returns:
            Formatted dashboard string
        """
        with self._lock:
            if self._current_metrics is None:
                return "No metrics available. Call update_metrics() first."
            
            return self._render_dashboard()
    
    def _render_dashboard(self) -> str:
        """Render the dashboard based on current theme."""
        m = self._current_metrics
        
        if self._theme == "minimal":
            return self._render_minimal(m)
        elif self._theme == "dark":
            return self._render_dark(m)
        else:
            return self._render_default(m)
    
    def _render_default(self, m: MonitorMetrics) -> str:
        """Render default theme dashboard."""
        # Calculate uptime
        uptime = time.time() - self._stats["start_time"]
        
        # Create progress bar
        def progress_bar(value: float, width: int = 20) -> str:
            filled = int(value / 100 * width)
            bar = "█" * filled + "░" * (width - filled)
            return f"[{bar}] {value:.1f}%"
        
        lines = [
            "",
            "┌─────────────────────────────────────────────────────────────────┐",
            "│              QUANT-KERNEL SYSTEM MONITOR                       │",
            "├─────────────────────────────────────────────────────────────────┤",
            f"│ Uptime: {self._format_time(uptime):<49} │",
            "├─────────────────────────────────────────────────────────────────┤",
            "│ SYSTEM RESOURCES                                               │",
            "├─────────────────────────────────────────────────────────────────┤",
            f"│ CPU (Strategy):     {progress_bar(m.cpu_usage):<37} │",
            f"│ MEM (Buffers):      {progress_bar(m.memory_usage):<37} │",
            f"│ LOAD (Volatility):  {progress_bar(m.system_load):<37} │",
            "├─────────────────────────────────────────────────────────────────┤",
            "│ MARKET STATUS                                                     │",
            "├─────────────────────────────────────────────────────────────────┤",
            f"│ Regime:          {m.regime:<50} │",
            f"│ Spectral Radius: {m.spectral_radius:<50.4f} │",
            f"│ Condition Num:   {m.condition_number:<50.2f} │",
            "├─────────────────────────────────────────────────────────────────┤",
            "│ PERFORMANCE                                                      │",
            "├─────────────────────────────────────────────────────────────────┤",
            f"│ Sharpe Ratio:    {m.sharpe_ratio:<50.4f} │",
            f"│ Max Drawdown:   {m.max_drawdown:<50.4f} │",
            f"│ Total P&L:      ${m.total_pnl:<48,.2f} │",
            f"│ Open Positions: {m.open_positions:<50} │",
            "├─────────────────────────────────────────────────────────────────┤",
            "│ DATA STREAM                                                      │",
            "├─────────────────────────────────────────────────────────────────┤",
            f"│ Tick Rate:       {m.tick_rate:<50.2f}/sec │",
            f"│ Network Latency: {m.network_latency:<50.2f} ms │",
            "└─────────────────────────────────────────────────────────────────┘",
            "",
        ]
        
        return "\n".join(lines)
    
    def _render_minimal(self, m: MonitorMetrics) -> str:
        """Render minimal theme."""
        return f"""
LOAD: {m.system_load:5.1f}% | Regime: {m.regime:15} | PnL: ${m.total_pnl:10,.2f} | Sharpe: {m.sharpe_ratio:5.2f}
""".strip()
    
    def _render_dark(self, m: MonitorMetrics) -> str:
        """Render dark theme (ANSI codes)."""
        # ANSI colors
        RESET = "\033[0m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RED = "\033[91m"
        CYAN = "\033[96m"
        
        # Color based on load
        if m.system_load > 70:
            load_color = RED
        elif m.system_load > 40:
            load_color = YELLOW
        else:
            load_color = GREEN
        
        lines = [
            f"{CYAN}╔═══════════════════════════════════════════════════════════════════╗{RESET}",
            f"{CYAN}║{RESET}              \033[1mQUANT-KERNEL SYSTEM MONITOR\033[0m                      {CYAN}║{RESET}",
            f"{CYAN}╠═══════════════════════════════════════════════════════════════════╣{RESET}",
            f"{CYAN}║{RESET} LOAD (Vol): {load_color}{m.system_load:5.1f}%{RESET} | Regime: {m.regime:15} | Sharpe: {m.sharpe_ratio:5.2f} {CYAN}║{RESET}",
            f"{CYAN}║{RESET} CPU:        {m.cpu_usage:5.1f}%  | MEM:   {m.memory_usage:5.1f}%  | Ticks/s: {m.tick_rate:5.1f}        {CYAN}║{RESET}",
            f"{CYAN}║{RESET} Spectral:   {m.spectral_radius:5.4f} | Cond#: {m.condition_number:6.1f} | PnL: ${m.total_pnl:10,.2f}   {CYAN}║{RESET}",
            f"{CYAN}╚═══════════════════════════════════════════════════════════════════╝{RESET}",
        ]
        
        return "\n".join(lines)
    
    def _format_time(self, seconds: float) -> str:
        """Format time duration."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def get_history(self, n: int = 60) -> List[MonitorMetrics]:
        """Get historical metrics."""
        return list(self._metrics_history)[-n:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get monitor statistics."""
        return {
            **self._stats,
            "current_metrics": {
                "system_load": self._current_metrics.system_load if self._current_metrics else 0,
                "regime": self._current_metrics.regime if self._current_metrics else "unknown",
            } if self._current_metrics else {}
        }


class DashboardCLI:
    """
    Interactive CLI Dashboard.
    
    Runs the system monitor in a loop, providing continuous updates.
    """
    
    def __init__(
        self,
        monitor: SystemMonitor,
        update_interval: float = 1.0
    ):
        """
        Initialize CLI dashboard.
        
        Args:
            monitor: SystemMonitor instance
            update_interval: Update interval in seconds
        """
        self._monitor = monitor
        self._update_interval = update_interval
        self._running = False
    
    def start(self) -> None:
        """Start the dashboard loop."""
        self._running = True
        
        try:
            while self._running:
                # Clear screen
                print("\033[2J\033[H", end="")  # ANSI clear screen
                
                # Render and print
                print(self._monitor.render())
                
                # Wait
                time.sleep(self._update_interval)
                
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self) -> None:
        """Stop the dashboard."""
        self._running = False
        print("\nDashboard stopped.")
    
    def update_from_portfolio(self, portfolio) -> None:
        """
        Update monitor from portfolio manager.
        
        Args:
            portfolio: PortfolioManager instance
        """
        stats = portfolio.get_statistics()
        
        # Get interrupt stats
        interrupt_stats = stats.get("interrupt_stats", {})
        
        # Get scheduler stats
        scheduler_stats = stats.get("scheduler_stats", {})
        
        # Get stability stats
        stability_stats = stats.get("stability_stats", {})
        
        # Get regime
        regime = stats.get("current_regime", "unknown")
        
        # Update metrics
        self._monitor.update_metrics(
            cpu_usage=scheduler_stats.get("current_spectral_radius", 0) * 100,
            memory_usage=min(100, interrupt_stats.get("total_ticks", 0) / 100),
            system_load=stability_stats.get("current_condition_number", 1) * 2,
            regime=regime,
            spectral_radius=scheduler_stats.get("current_spectral_radius", 0),
            condition_number=stability_stats.get("current_condition_number", 1),
            tick_rate=interrupt_stats.get("total_ticks", 0) / max(1, time.time() - stats.get("start_time", 1)),
        )


# Utility function to create system monitor from portfolio
def create_dashboard_from_portfolio(
    portfolio,
    theme: str = "default"
) -> SystemMonitor:
    """
    Create a system monitor configured for a portfolio.
    
    Args:
        portfolio: PortfolioManager instance
        theme: Display theme
        
    Returns:
        Configured SystemMonitor
    """
    monitor = SystemMonitor(theme=theme)
    
    # Set up auto-update callback
    def get_system_load():
        stats = portfolio.get_statistics()
        return stats.get("stability_stats", {}).get("current_condition_number", 1) * 2
    
    monitor.register_callback(MetricType.LOAD, get_system_load)
    
    return monitor

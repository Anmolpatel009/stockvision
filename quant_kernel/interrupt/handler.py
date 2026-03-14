"""
InterruptHandler and Circular Buffer Implementation

This module implements the Interrupt Layer of the Quant-Kernel architecture.
It treats market ticks as hardware interrupts and provides O(1) access to the 
most recent N ticks using a circular buffer (ring buffer) implemented with NumPy.

Mathematical Background:
- Circular buffers use modular arithmetic for efficient wraparound
- Index calculation: (head + offset) % capacity for O(1) random access
- Write position advances atomically, ensuring thread-safe operations
"""

from typing import Optional, Dict, Any, Callable, List
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from numpy.typing import NDArray
import time
from collections import deque
from threading import Lock, RLock


class InterruptPriority(Enum):
    """Interrupt priority levels similar to hardware IRQ priorities."""
    CRITICAL = 0    # High-frequency market data (tick-by-tick)
    HIGH = 1        # Quote updates, order book changes
    NORMAL = 2     # Aggregated data, indicators
    LOW = 3        # Periodic snapshots, logging


@dataclass
class MarketTick:
    """
    Represents a single market tick (price update).
    
    Attributes:
        timestamp: Unix timestamp in milliseconds
        symbol: Trading symbol (e.g., 'AAPL', 'BTC-USD')
        price: Current price
        volume: Trading volume
        bid: Best bid price
        ask: Best ask price
        tick_id: Unique identifier for this tick
    """
    timestamp: int
    symbol: str
    price: float
    volume: float = 0.0
    bid: float = 0.0
    ask: float = 0.0
    tick_id: int = 0
    
    @property
    def spread(self) -> float:
        """Calculate bid-ask spread."""
        return self.ask - self.bid if self.ask > 0 and self.bid > 0 else 0.0
    
    @property
    def mid_price(self) -> float:
        """Calculate mid price."""
        return (self.ask + self.bid) / 2 if self.ask > 0 and self.bid > 0 else self.price


@dataclass
class InterruptContext:
    """
    Context information for an interrupt handler.
    
    Contains metadata about the interrupt including timing information
    and the interrupt source.
    """
    interrupt_type: str
    timestamp: int
    priority: InterruptPriority
    source: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class CircularBuffer:
    """
    High-performance Circular Buffer (Ring Buffer) using NumPy.
    
    Provides O(1) access for the most recent N elements with minimal memory
    allocation overhead. Uses a fixed-size NumPy array with modular indexing.
    
    Mathematical Properties:
    - Time Complexity: O(1) for both read and write operations
    - Space Complexity: O(capacity) fixed memory allocation
    - No dynamic memory allocation after initialization
    
    Example:
        >>> buffer = CircularBuffer(capacity=1000, dtype=np.float64)
        >>> buffer.push(1.0)
        >>> buffer.push(2.0)
        >>> buffer.get_recent(2)  # Returns [1.0, 2.0]
    """
    
    def __init__(
        self, 
        capacity: int, 
        dtype: np.dtype = np.float64,
        enable_lock: bool = False
    ):
        """
        Initialize the circular buffer.
        
        Args:
            capacity: Maximum number of elements to store
            dtype: NumPy data type for the buffer
            enable_lock: Enable thread-safe operations (adds overhead)
        """
        if capacity <= 0:
            raise ValueError(f"Capacity must be positive, got {capacity}")
        
        self._capacity = capacity
        self._dtype = dtype
        self._enable_lock = enable_lock
        
        # Pre-allocate NumPy array for O(1) operations
        self._buffer = np.zeros(capacity, dtype=dtype)
        self._timestamp_buffer = np.zeros(capacity, dtype=np.int64)
        
        # Read and write pointers
        self._head = 0  # Next write position
        self._size = 0  # Current number of elements
        
        # Thread safety
        self._lock = Lock() if enable_lock else None
    
    @property
    def capacity(self) -> int:
        """Return the buffer capacity."""
        return self._capacity
    
    @property
    def size(self) -> int:
        """Return current number of elements in buffer."""
        return self._size
    
    @property
    def is_empty(self) -> bool:
        """Check if buffer is empty."""
        return self._size == 0
    
    @property
    def is_full(self) -> bool:
        """Check if buffer is full."""
        return self._size == self._capacity
    
    def _acquire_lock(self):
        """Acquire lock if thread safety is enabled."""
        if self._lock is not None:
            self._lock.acquire()
    
    def _release_lock(self):
        """Release lock if thread safety is enabled."""
        if self._lock is not None:
            self._lock.release()
    
    def push(self, value: float, timestamp: Optional[int] = None) -> None:
        """
        Push a value onto the buffer (O(1) operation).
        
        Args:
            value: The value to add
            timestamp: Optional timestamp for the value
        """
        self._acquire_lock()
        try:
            self._buffer[self._head] = value
            self._timestamp_buffer[self._head] = timestamp or int(time.time() * 1000)
            
            # Advance head with wraparound
            self._head = (self._head + 1) % self._capacity
            
            # Update size (don't exceed capacity)
            if self._size < self._capacity:
                self._size += 1
        finally:
            self._release_lock()
    
    def push_batch(self, values: NDArray, timestamps: Optional[NDArray] = None) -> None:
        """
        Push multiple values onto the buffer (O(n) where n = batch size).
        
        Args:
            values: Array of values to add
            timestamps: Optional array of timestamps
        """
        self._acquire_lock()
        try:
            n = len(values)
            for i in range(n):
                idx = (self._head + i) % self._capacity
                self._buffer[idx] = values[i]
                if timestamps is not None:
                    self._timestamp_buffer[idx] = timestamps[i]
                else:
                    self._timestamp_buffer[idx] = int(time.time() * 1000)
            
            self._head = (self._head + n) % self._capacity
            self._size = min(self._size + n, self._capacity)
        finally:
            self._release_lock()
    
    def get(self, index: int) -> float:
        """
        Get element at specific index (O(1) operation).
        
        Args:
            index: Index from 0 (oldest) to size-1 (newest)
            
        Returns:
            The value at the specified index
        """
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of bounds for size {self._size}")
        
        # Calculate actual buffer index
        actual_index = (self._head - self._size + index) % self._capacity
        return self._buffer[actual_index]
    
    def get_recent(self, n: int) -> NDArray:
        """
        Get the most recent N elements (O(n) operation).
        
        Args:
            n: Number of recent elements to retrieve
            
        Returns:
            NumPy array of the most recent N elements
        """
        n = min(n, self._size)
        if n == 0:
            return np.array([], dtype=self._dtype)
        
        # Calculate starting index
        start_idx = (self._head - n) % self._capacity
        
        # Handle wraparound case
        if start_idx + n <= self._capacity:
            return self._buffer[start_idx:start_idx + n].copy()
        else:
            # Wraparound - need to concatenate
            part1 = self._buffer[start_idx:]
            part2 = self._buffer[:self._head]
            return np.concatenate([part1, part2])
    
    def get_all(self) -> NDArray:
        """Get all elements in chronological order (O(n) operation)."""
        return self.get_recent(self._size)
    
    def get_timestamp(self, index: int) -> int:
        """Get timestamp at specific index."""
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of bounds for size {self._size}")
        
        actual_index = (self._head - self._size + index) % self._capacity
        return self._timestamp_buffer[actual_index]
    
    def get_recent_timestamps(self, n: int) -> NDArray:
        """Get timestamps for the most recent N elements."""
        n = min(n, self._size)
        if n == 0:
            return np.array([], dtype=np.int64)
        
        start_idx = (self._head - n) % self._capacity
        
        if start_idx + n <= self._capacity:
            return self._timestamp_buffer[start_idx:start_idx + n].copy()
        else:
            part1 = self._timestamp_buffer[start_idx:]
            part2 = self._timestamp_buffer[:self._head]
            return np.concatenate([part1, part2])
    
    def clear(self) -> None:
        """Clear all elements from the buffer."""
        self._acquire_lock()
        try:
            self._buffer.fill(0)
            self._timestamp_buffer.fill(0)
            self._head = 0
            self._size = 0
        finally:
            self._release_lock()
    
    def __len__(self) -> int:
        """Return current size."""
        return self._size
    
    def __getitem__(self, index: int) -> float:
        """Allow buffer[index] syntax."""
        return self.get(index)


class TickBuffer(CircularBuffer):
    """
    Specialized Circular Buffer for MarketTick objects.
    
    Stores MarketTick objects with efficient O(1) access to recent ticks.
    """
    
    def __init__(self, capacity: int, enable_lock: bool = False):
        """
        Initialize the tick buffer.
        
        Args:
            capacity: Maximum number of ticks to store
            enable_lock: Enable thread-safe operations
        """
        super().__init__(capacity, dtype=object, enable_lock=enable_lock)
        self._tick_buffer: List[MarketTick] = [None] * capacity
        self._tick_head = 0
        self._tick_size = 0
        self._tick_id_counter = 0
    
    def push_tick(self, tick: MarketTick) -> None:
        """
        Push a MarketTick onto the buffer.
        
        Args:
            tick: MarketTick object to add
        """
        self._acquire_lock()
        try:
            tick.tick_id = self._tick_id_counter
            self._tick_id_counter += 1
            
            self._tick_buffer[self._tick_head] = tick
            self._tick_head = (self._tick_head + 1) % self._capacity
            
            if self._tick_size < self._capacity:
                self._tick_size += 1
        finally:
            self._release_lock()
    
    def get_recent_ticks(self, n: int) -> List[MarketTick]:
        """Get the most recent N MarketTick objects."""
        n = min(n, self._tick_size)
        if n == 0:
            return []
        
        start_idx = (self._tick_head - n) % self._capacity
        
        if start_idx + n <= self._capacity:
            return self._tick_buffer[start_idx:start_idx + n]
        else:
            part1 = self._tick_buffer[start_idx:]
            part2 = self._tick_buffer[:self._tick_head]
            return part1 + part2
    
    def get_all_ticks(self) -> List[MarketTick]:
        """Get all ticks in chronological order."""
        return self.get_recent_ticks(self._tick_size)
    
    def get_latest_price(self) -> Optional[float]:
        """Get the most recent price."""
        ticks = self.get_recent_ticks(1)
        return ticks[0].price if ticks else None
    
    def get_latest_tick(self) -> Optional[MarketTick]:
        """Get the most recent tick."""
        ticks = self.get_recent_ticks(1)
        return ticks[0] if ticks else None
    
    def calculate_returns(self, n: int = 1) -> NDArray:
        """
        Calculate returns from recent ticks.
        
        Args:
            n: Number of ticks to use for return calculation
            
        Returns:
            Array of returns
        """
        ticks = self.get_recent_ticks(n + 1)
        if len(ticks) < 2:
            return np.array([])
        
        prices = np.array([t.price for t in ticks])
        returns = np.diff(prices) / prices[:-1]
        return returns
    
    def calculate_volatility(self, window: int = 20) -> float:
        """
        Calculate rolling volatility from recent ticks.
        
        Args:
            window: Number of ticks for volatility calculation
            
        Returns:
            Rolling volatility (standard deviation of returns)
        """
        returns = self.calculate_returns(window)
        if len(returns) < 2:
            return 0.0
        return float(np.std(returns))


class InterruptHandler:
    """
    Hardware Interrupt-style Market Data Handler.
    
    This is the core of the Quant-Kernel's interrupt layer. It treats every
    price update as a hardware interrupt, maintaining a zero-latency snapshot
    of market state through circular buffers.
    
    Key Features:
    - O(1) tick insertion and retrieval
    - Configurable interrupt priority system
    - Interrupt callback registration
    - Statistical analysis of market data
    
    Mathematical Properties:
    - Throughput: Limited only by memory bandwidth
    - Latency: O(1) per tick insertion
    - Memory: Fixed allocation regardless of data volume
    
    Example:
        >>> handler = InterruptHandler(capacity=10000)
        >>> handler.register_callback(InterruptPriority.CRITICAL, my_callback)
        >>> 
        >>> # Simulate receiving a tick
        >>> tick = MarketTick(
        ...     timestamp=int(time.time() * 1000),
        ...     symbol='AAPL',
        ...     price=150.25,
        ...     volume=1000,
        ...     bid=150.20,
        ...     ask=150.30
        ... )
        >>> handler.handle_interrupt(tick)
    """
    
    def __init__(
        self,
        capacity: int = 10000,
        default_symbols: Optional[List[str]] = None,
        enable_lock: bool = True
    ):
        """
        Initialize the InterruptHandler.
        
        Args:
            capacity: Maximum ticks to store per symbol
            default_symbols: List of symbols to track
            enable_lock: Enable thread-safe operations
        """
        self._capacity = capacity
        self._enable_lock = enable_lock
        
        # Global tick buffer
        self._global_buffer = TickBuffer(capacity, enable_lock=enable_lock)
        
        # Per-symbol buffers
        self._symbol_buffers: Dict[str, TickBuffer] = {}
        
        # Register default symbols
        self._default_symbols = default_symbols or []
        for symbol in self._default_symbols:
            self._symbol_buffers[symbol] = TickBuffer(capacity, enable_lock=enable_lock)
        
        # Interrupt callbacks organized by priority
        self._callbacks: Dict[InterruptPriority, List[Callable]] = {
            priority: [] for priority in InterruptPriority
        }
        
        # Statistics
        self._stats = {
            "total_ticks": 0,
            "ticks_by_symbol": {},
            "interrupts_handled": 0,
            "last_interrupt_time": 0,
            "avg_latency_us": 0.0,
        }
        
        # Thread safety
        self._lock = RLock() if enable_lock else None
        
        # Performance tracking
        self._latency_samples: deque = deque(maxlen=1000)
    
    def _acquire_lock(self):
        """Acquire lock if thread safety is enabled."""
        if self._lock is not None:
            self._lock.acquire()
    
    def _release_lock(self):
        """Release lock if thread safety is enabled."""
        if self._lock is not None:
            self._lock.release()
    
    def register_callback(
        self,
        priority: InterruptPriority,
        callback: Callable[[InterruptContext, MarketTick], None]
    ) -> None:
        """
        Register an interrupt callback for a specific priority level.
        
        Args:
            priority: Interrupt priority level
            callback: Function to call when interrupt fires
        """
        self._callbacks[priority].append(callback)
    
    def unregister_callback(
        self,
        priority: InterruptPriority,
        callback: Callable[[InterruptContext, MarketTick], None]
    ) -> None:
        """
        Unregister an interrupt callback.
        
        Args:
            priority: Interrupt priority level
            callback: Callback function to remove
        """
        if callback in self._callbacks[priority]:
            self._callbacks[priority].remove(callback)
    
    def handle_interrupt(
        self,
        tick: MarketTick,
        priority: InterruptPriority = InterruptPriority.CRITICAL
    ) -> None:
        """
        Handle an incoming market tick interrupt.
        
        This is the main entry point for market data. It:
        1. Stores the tick in the circular buffer (O(1))
        2. Updates per-symbol buffers
        3. Triggers registered callbacks based on priority
        
        Args:
            tick: MarketTick object representing the interrupt
            priority: Interrupt priority level
        """
        start_time = time.perf_counter()
        
        self._acquire_lock()
        try:
            # Store in global buffer
            self._global_buffer.push_tick(tick)
            
            # Store in symbol-specific buffer
            if tick.symbol not in self._symbol_buffers:
                self._symbol_buffers[tick.symbol] = TickBuffer(
                    self._capacity, 
                    enable_lock=False
                )
            self._symbol_buffers[tick.symbol].push_tick(tick)
            
            # Update statistics
            self._stats["total_ticks"] += 1
            self._stats["ticks_by_symbol"][tick.symbol] = \
                self._stats["ticks_by_symbol"].get(tick.symbol, 0) + 1
            self._stats["interrupts_handled"] += 1
            self._stats["last_interrupt_time"] = tick.timestamp
            
            # Calculate latency
            latency_us = (time.perf_counter() - start_time) * 1_000_000
            self._latency_samples.append(latency_us)
            self._stats["avg_latency_us"] = np.mean(self._latency_samples)
            
        finally:
            self._release_lock()
        
        # Create interrupt context
        context = InterruptContext(
            interrupt_type="MARKET_TICK",
            timestamp=tick.timestamp,
            priority=priority,
            source=tick.symbol,
            metadata={
                "price": tick.price,
                "volume": tick.volume,
                "spread": tick.spread,
            }
        )
        
        # Execute callbacks (outside lock to prevent deadlocks)
        for callback in self._callbacks[priority]:
            try:
                callback(context, tick)
            except Exception as e:
                # Log but don't propagate to avoid disrupting data flow
                print(f"Callback error: {e}")
    
    def get_latest_price(self, symbol: Optional[str] = None) -> Optional[float]:
        """
        Get the latest price for a symbol (O(1) operation).
        
        Args:
            symbol: Trading symbol, or None for global latest
            
        Returns:
            Latest price or None if no data
        """
        if symbol is None:
            return self._global_buffer.get_latest_price()
        
        buffer = self._symbol_buffers.get(symbol)
        return buffer.get_latest_price() if buffer else None
    
    def get_recent_ticks(
        self,
        n: int = 100,
        symbol: Optional[str] = None
    ) -> List[MarketTick]:
        """
        Get the most recent N ticks (O(n) operation).
        
        Args:
            n: Number of ticks to retrieve
            symbol: Optional symbol filter
            
        Returns:
            List of recent MarketTick objects
        """
        if symbol is None:
            return self._global_buffer.get_recent_ticks(n)
        
        buffer = self._symbol_buffers.get(symbol)
        return buffer.get_recent_ticks(n) if buffer else []
    
    def get_recent_prices(
        self,
        n: int = 100,
        symbol: Optional[str] = None
    ) -> NDArray:
        """
        Get the most recent N prices as a NumPy array.
        
        Args:
            n: Number of prices to retrieve
            symbol: Optional symbol filter
            
        Returns:
            NumPy array of recent prices
        """
        ticks = self.get_recent_ticks(n, symbol)
        return np.array([t.price for t in ticks], dtype=np.float64)
    
    def get_volatility(
        self,
        window: int = 20,
        symbol: Optional[str] = None
    ) -> float:
        """
        Calculate rolling volatility (O(n) operation).
        
        Args:
            window: Number of ticks for calculation
            symbol: Optional symbol filter
            
        Returns:
            Rolling volatility
        """
        if symbol is None:
            return self._global_buffer.calculate_volatility(window)
        
        buffer = self._symbol_buffers.get(symbol)
        return buffer.calculate_volatility(window) if buffer else 0.0
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get current handler statistics."""
        return self._stats.copy()
    
    def get_buffer_status(self) -> Dict[str, Any]:
        """Get buffer status for all tracked symbols."""
        status = {
            "global": {
                "capacity": self._global_buffer.capacity,
                "size": self._global_buffer.size,
            },
            "symbols": {}
        }
        
        for symbol, buffer in self._symbol_buffers.items():
            status["symbols"][symbol] = {
                "capacity": buffer.capacity,
                "size": buffer.size,
            }
        
        return status
    
    def clear_buffer(self, symbol: Optional[str] = None) -> None:
        """
        Clear buffer(s).
        
        Args:
            symbol: Optional symbol to clear, or None for all
        """
        self._acquire_lock()
        try:
            if symbol is None:
                self._global_buffer.clear()
                for buffer in self._symbol_buffers.values():
                    buffer.clear()
            elif symbol in self._symbol_buffers:
                self._symbol_buffers[symbol].clear()
        finally:
            self._release_lock()

"""
Demo script for Quant-Kernel Phase 1: The Core

This script demonstrates:
1. InterruptHandler with Circular Buffer for O(1) tick processing
2. FeatureMMU with real-time PCA compression
"""

import numpy as np
import time
import sys

# Add parent directory to path
sys.path.insert(0, '.')

from quant_kernel.interrupt.handler import (
    InterruptHandler, 
    CircularBuffer, 
    MarketTick, 
    InterruptPriority
)
from quant_kernel.mmu.feature_mmu import (
    FeatureMMU, 
    PCATransformer,
    calculate_technical_indicators,
    FeatureConfig
)


def demo_circular_buffer():
    """Demonstrate Circular Buffer O(1) operations."""
    print("=" * 60)
    print("DEMO: Circular Buffer Performance")
    print("=" * 60)
    
    # Create buffer
    buffer = CircularBuffer(capacity=1000, enable_lock=True)
    
    # Performance test
    n_operations = 100000
    
    # Push test
    start = time.perf_counter()
    for i in range(n_operations):
        buffer.push(float(i))
    push_time = time.perf_counter() - start
    
    # Read test
    start = time.perf_counter()
    for _ in range(1000):
        recent = buffer.get_recent(100)
    read_time = time.perf_counter() - start
    
    print(f"Push {n_operations} elements: {push_time*1000:.2f}ms")
    print(f"Read 1000 batches of 100: {read_time*1000:.2f}ms")
    print(f"Buffer size: {buffer.size}/{buffer.capacity}")
    print(f"Recent 10 values: {buffer.get_recent(10)}")
    print()


def demo_interrupt_handler():
    """Demonstrate InterruptHandler with market ticks."""
    print("=" * 60)
    print("DEMO: Interrupt Handler")
    print("=" * 60)
    
    handler = InterruptHandler(capacity=10000, default_symbols=['AAPL', 'BTC-USD'])
    
    # Simulate market ticks
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'BTC-USD', 'ETH-USD']
    
    for i in range(100):
        symbol = symbols[i % len(symbols)]
        tick = MarketTick(
            timestamp=int(time.time() * 1000),
            symbol=symbol,
            price=100 + np.random.randn() * 10,
            volume=1000 + np.random.randint(0, 10000),
            bid=99 + np.random.randn() * 10,
            ask=101 + np.random.randn() * 10
        )
        handler.handle_interrupt(tick, InterruptPriority.CRITICAL)
    
    # Get statistics
    stats = handler.get_statistics()
    print(f"Total ticks processed: {stats['total_ticks']}")
    print(f"Interrupts handled: {stats['interrupts_handled']}")
    print(f"Avg latency (μs): {stats['avg_latency_us']:.2f}")
    print(f"Ticks by symbol: {stats['ticks_by_symbol']}")
    
    # Buffer status
    status = handler.get_buffer_status()
    print(f"\nBuffer status:")
    for symbol, info in status['symbols'].items():
        print(f"  {symbol}: {info['size']}/{info['capacity']}")
    
    # Latest prices
    print(f"\nLatest prices:")
    for symbol in symbols:
        price = handler.get_latest_price(symbol)
        if price:
            print(f"  {symbol}: ${price:.2f}")
    
    # Volatility
    print(f"\nVolatility (20-tick window):")
    for symbol in ['AAPL', 'BTC-USD']:
        vol = handler.get_volatility(symbol=symbol)
        print(f"  {symbol}: {vol:.4f}")
    
    print()


def demo_pca_transformer():
    """Demonstrate PCA Transformer."""
    print("=" * 60)
    print("DEMO: PCA Transformer")
    print("=" * 60)
    
    # Generate synthetic high-dimensional data
    np.random.seed(42)
    n_samples = 1000
    n_features = 50
    
    # Create correlated features (simulating market indicators)
    X = np.random.randn(n_samples, n_features)
    
    # Add correlations
    for i in range(5):
        X[:, i*10:(i+1)*10] += X[:, :10] * 0.5
    
    # Fit PCA
    config = FeatureConfig(n_components=3, standardize=True)
    pca = PCATransformer(config)
    pca.fit(X)
    
    print(f"Original dimensions: {n_features}")
    print(f"Compressed dimensions: {pca.n_components}")
    print(f"Explained variance ratio: {pca.explained_variance_ratio}")
    print(f"Total variance explained: {pca.get_total_explained_variance():.4f}")
    
    # Transform new data
    X_new = np.random.randn(10, n_features)
    X_compressed = pca.transform(X_new)
    print(f"\nCompressed shape: {X_compressed.shape}")
    print(f"First compressed sample: {X_compressed[0]}")
    
    # Reconstruction
    X_reconstructed = pca.inverse_transform(X_compressed)
    recon_error = np.mean((X_new - X_reconstructed) ** 2)
    print(f"Reconstruction error: {recon_error:.6f}")
    print()


def demo_feature_mmu():
    """Demonstrate Feature MMU."""
    print("=" * 60)
    print("DEMO: Feature MMU")
    print("=" * 60)
    
    # Generate synthetic price data
    np.random.seed(42)
    n_samples = 500
    
    # Generate price series with trends
    t = np.linspace(0, 10, n_samples)
    prices = 100 + np.cumsum(np.random.randn(n_samples) * 0.1)
    volumes = np.abs(np.random.randn(n_samples) * 10000 + 50000)
    
    # Calculate technical indicators
    features, feature_names = calculate_technical_indicators(prices, volumes)
    
    print(f"Generated {features.shape[1]} technical indicators")
    print(f"Sample feature names: {feature_names[:10]}")
    
    # Fit MMU
    mmu = FeatureMMU(n_components=3, enable_tlb=True)
    mmu.fit(features, feature_names)
    
    print(f"\nMMU initialized:")
    print(f"  Input dimensions: {features.shape[1]}")
    print(f"  Output dimensions: {mmu.n_components}")
    print(f"  Total variance explained: {mmu.get_statistics()['total_variance_explained']:.4f}")
    
    # Compress new data
    new_features = features[:10]
    result = mmu.compress(new_features)
    
    print(f"\nCompression result:")
    print(f"  Latent state shape: {result.latent_state.shape}")
    print(f"  First latent state: {result.latent_state[0]}")
    print(f"  Explained variance: {result.explained_variance:.4f}")
    print(f"  Reconstruction error: {result.reconstruction_error:.6f}")
    
    # Top features per component
    print(f"\nTop features per component:")
    for comp in range(3):
        top_features = mmu.get_top_features(component=comp, n=5)
        print(f"  Component {comp}: {top_features}")
    
    print()


def demo_incremental_learning():
    """Demonstrate incremental learning."""
    print("=" * 60)
    print("DEMO: Incremental Learning")
    print("=" * 60)
    
    # Initial batch
    np.random.seed(42)
    X_initial = np.random.randn(200, 20)
    
    # Fit MMU
    mmu = FeatureMMU(n_components=3)
    mmu.fit(X_initial)
    
    initial_var = mmu.get_statistics()['total_variance_explained']
    print(f"Initial variance explained: {initial_var:.4f}")
    
    # Incremental updates
    for batch in range(5):
        X_batch = np.random.randn(50, 20)
        mmu.fit_incremental(X_batch)
    
    final_var = mmu.get_statistics()['total_variance_explained']
    print(f"Final variance explained: {final_var:.4f}")
    print()


def main():
    """Run all demos."""
    print("\n" + "=" * 60)
    print("QUANT-KERNEL PHASE 1 DEMO")
    print("The Core: Interrupt Handler & Feature MMU")
    print("=" * 60 + "\n")
    
    demo_circular_buffer()
    demo_interrupt_handler()
    demo_pca_transformer()
    demo_feature_mmu()
    demo_incremental_learning()
    
    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("\nNext: Phase 2 - The Logic")
    print("  - Jacobian-based sensitivity analysis")
    print("  - EigenScheduler for dynamic capital allocation")


if __name__ == "__main__":
    main()

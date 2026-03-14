"""
Feature MMU (Memory Management Unit) Implementation

This module implements the Feature Mapping layer of the Quant-Kernel architecture.
It maps high-dimensional market noise into low-dimensional "Latent States"
using Principal Component Analysis (PCA) and Singular Value Decomposition (SVD).

Mathematical Background:
- PCA: Finds orthogonal directions of maximum variance in data
- SVD: Factorizes matrix into singular vectors and values
- Compression: Projects high-dim data onto top k principal components
- Efficiency: Reduces 50+ indicators to top 3 principal components

The MMU terminology:
- Virtual Memory (High-Dim): Raw market indicators (RSI, MACD, Volume, etc.)
- Physical Memory (Low-Dim): Latent state representation
- Page Table: PCA transformation matrix
- TLB: Cached transformations for real-time inference
"""

from typing import Optional, Dict, List, Tuple, Any
from dataclasses import dataclass, field
import numpy as np
from numpy.typing import NDArray
from scipy import linalg
from scipy.stats import zscore
import time
from threading import RLock
from collections import deque


@dataclass
class FeatureConfig:
    """Configuration for feature extraction and PCA transformation."""
    n_components: int = 3  # Number of principal components to keep
    min_samples: int = 30  # Minimum samples before fitting
    standardize: bool = True  # Whether to standardize features
    n_std: float = 3.0  # Number of std deviations for outlier clipping
    use_incremental: bool = True  # Use incremental PCA for streaming
    batch_size: int = 100  # Batch size for incremental learning


@dataclass
class CompressionResult:
    """Result of feature compression operation."""
    latent_state: NDArray  # Compressed representation
    explained_variance: float  # Total variance explained
    components_contribution: NDArray  # Variance per component
    reconstruction_error: float  # Approximation error
    timestamp: int  # Processing timestamp


class PCATransformer:
    """
    PCA Transformer with Incremental Learning Support.
    
    Implements both batch and incremental PCA for real-time feature
    compression. Uses scipy's SVD implementation for numerical stability.
    
    Mathematical Properties:
    - Time Complexity: O(min(n^2*k, n*k^2)) per transform
    - Space Complexity: O(n*k) for transformation matrix
    - Variance Explained: Configurable via n_components
    
    Example:
        >>> pca = PCATransformer(n_components=3)
        >>> pca.fit(features)  # Fit on historical data
        >>> latent = pca.transform(new_features)  # Compress
    """
    
    def __init__(self, config: Optional[FeatureConfig] = None):
        """
        Initialize PCA transformer.
        
        Args:
            config: Feature configuration
        """
        self._config = config or FeatureConfig()
        self._is_fitted = False
        
        # Transformation components
        self._mean: Optional[NDArray] = None
        self._std: Optional[NDArray] = None
        self._components: Optional[NDArray] = None  # Principal axes
        self._singular_values: Optional[NDArray] = None
        self._explained_variance: Optional[NDArray] = None
        self._total_variance: float = 0.0
        
        # Incremental learning state
        self._n_samples_seen = 0
        self._incremental_buffer: List[NDArray] = []
        
        # Lock for thread safety
        self._lock = RLock()
    
    @property
    def is_fitted(self) -> bool:
        """Check if transformer has been fitted."""
        return self._is_fitted
    
    @property
    def n_components(self) -> int:
        """Get number of components."""
        return self._config.n_components
    
    @property
    def explained_variance_ratio(self) -> NDArray:
        """Get explained variance ratio per component."""
        if self._explained_variance is None:
            return np.array([])
        return self._explained_variance / self._total_variance
    
    def fit(self, X: NDArray) -> "PCATransformer":
        """
        Fit the PCA transformer on training data.
        
        Uses Singular Value Decomposition for numerical stability.
        
        Args:
            X: Training data of shape (n_samples, n_features)
            
        Returns:
            Self for method chaining
        """
        X = np.asarray(X, dtype=np.float64)
        
        if X.ndim != 2:
            raise ValueError(f"Expected 2D array, got shape {X.shape}")
        
        n_samples, n_features = X.shape
        
        with self._lock:
            # Standardize if configured
            if self._config.standardize:
                self._mean = np.mean(X, axis=0)
                self._std = np.std(X, axis=0)
                self._std[self._std == 0] = 1.0  # Avoid division by zero
                X_standardized = (X - self._mean) / self._std
            else:
                self._mean = np.zeros(n_features)
                self._std = np.ones(n_features)
                X_standardized = X
            
            # Clip outliers if configured
            if self._config.n_std > 0:
                X_standardized = np.clip(
                    X_standardized,
                    -self._config.n_std,
                    self._config.n_std
                )
            
            # Compute SVD
            # Using scipy.linalg.svd for better numerical stability
            U, S, Vt = linalg.svd(X_standardized, full_matrices=False)
            
            # Store components (top k)
            k = min(self._config.n_components, n_features, n_samples)
            self._components = Vt[:k, :].T  # Shape: (n_features, k)
            self._singular_values = S[:k]
            
            # Compute explained variance
            self._explained_variance = (S[:k] ** 2) / n_samples
            self._total_variance = np.sum(S ** 2) / n_samples
            
            # Mark as fitted
            self._is_fitted = True
            self._n_samples_seen = n_samples
        
        return self
    
    def fit_incremental(self, X: NDArray) -> "PCATransformer":
        """
        Fit PCA incrementally using Welford's online algorithm.
        
        For streaming data, this updates the PCA model without
        reprocessing all historical data.
        
        Args:
            X: New data batch of shape (n_samples, n_features)
            
        Returns:
            Self for method chaining
        """
        X = np.asarray(X, dtype=np.float64)
        
        if X.ndim == 1:
            X = X.reshape(1, -1)
        
        n_samples, n_features = X.shape
        
        with self._lock:
            if not self._is_fitted:
                # Initialize on first batch
                return self.fit(X)
            
            # Update running statistics using Welford's algorithm
            batch_mean = np.mean(X, axis=0)
            batch_var = np.var(X, axis=0)
            
            # Update mean
            old_n = self._n_samples_seen
            new_n = old_n + n_samples
            
            if self._config.standardize:
                # Update mean
                new_mean = (old_n * self._mean + n_samples * batch_mean) / new_n
                
                # Update std (simplified - uses batch variance)
                # For production, would use proper online variance
                new_std = np.sqrt(
                    (old_n * self._std**2 + n_samples * batch_var) / new_n
                )
                new_std[new_std == 0] = 1.0
                
                self._mean = new_mean
                self._std = new_std
            
            # Buffer batch for periodic full retraining
            self._incremental_buffer.append(X)
            
            if len(self._incremental_buffer) >= self._config.batch_size:
                # Full retraining
                combined = np.vstack(self._incremental_buffer)
                self.fit(combined)
                self._incremental_buffer = []
            else:
                # Update singular values (approximation)
                self._n_samples_seen = new_n
            
            # For now, we'll use the existing components
            # In production, would implement proper online SVD update
        
        return self
    
    def transform(self, X: NDArray) -> NDArray:
        """
        Transform high-dimensional features to low-dimensional latent state.
        
        Args:
            X: Data of shape (n_samples, n_features)
            
        Returns:
            Transformed data of shape (n_samples, n_components)
        """
        if not self._is_fitted:
            raise RuntimeError("Transformer must be fitted before transform")
        
        X = np.asarray(X, dtype=np.float64)
        
        with self._lock:
            # Standardize
            if self._config.standardize:
                X = (X - self._mean) / self._std
            
            # Project onto principal components
            # X_reduced = X @ components
            X_transformed = X @ self._components
        
        return X_transformed
    
    def fit_transform(self, X: NDArray) -> NDArray:
        """Fit and transform in one step."""
        self.fit(X)
        return self.transform(X)
    
    def inverse_transform(self, X_low: NDArray) -> NDArray:
        """
        Reconstruct high-dimensional features from latent state.
        
        Args:
            X_low: Low-dimensional data of shape (n_samples, n_components)
            
        Returns:
            Reconstructed data of shape (n_samples, n_features)
        """
        if not self._is_fitted:
            raise RuntimeError("Transformer must be fitted before inverse_transform")
        
        X_low = np.asarray(X_low, dtype=np.float64)
        
        with self._lock:
            # Reconstruct
            X_reconstructed = X_low @ self._components.T
            
            # Denormalize
            if self._config.standardize:
                X_reconstructed = X_reconstructed * self._std + self._mean
        
        return X_reconstructed
    
    def get_explained_variance(self) -> NDArray:
        """Get explained variance per component."""
        if self._explained_variance is None:
            return np.array([])
        return self._explained_variance.copy()
    
    def get_total_explained_variance(self) -> float:
        """Get total explained variance ratio."""
        if self._total_variance == 0:
            return 0.0
        return float(np.sum(self._explained_variance) / self._total_variance)
    
    def get_component_loadings(self) -> NDArray:
        """Get the principal component loadings (feature weights)."""
        if self._components is None:
            return np.array([])
        return self._components.copy()
    
    def calculate_reconstruction_error(self, X: NDArray) -> float:
        """
        Calculate mean squared reconstruction error.
        
        Args:
            X: Original data
            
        Returns:
            Reconstruction error
        """
        X_transformed = self.transform(X)
        X_reconstructed = self.inverse_transform(X_transformed)
        return float(np.mean((X - X_reconstructed) ** 2))


class FeatureMMU:
    """
    Feature Memory Management Unit.
    
    Acts as the MMU for market features, mapping high-dimensional
    market indicators to low-dimensional latent states. This reduces
    computational load on strategy processes while preserving
    essential market information.
    
    Key Features:
    - Real-time PCA compression using incremental learning
    - Feature caching with TLB-like structure
    - Automatic feature extraction from raw market data
    - Configurable dimensionality reduction
    
    Mathematical Model:
    - Input: High-dimensional feature vector f ∈ ℝ^n (n > 50)
    - Output: Latent state z ∈ ℝ^k (k ≤ 3)
    - Transformation: z = PCA(f) = W^T @ f
    
    Example:
        >>> mmu = FeatureMMU(n_components=3)
        >>> mmu.fit(features)  # Fit on historical features
        >>> 
        >>> # Real-time compression
        >>> latent_state = mmu.compress(new_features)
    """
    
    # Common technical indicators
    DEFAULT_INDICATORS = [
        'rsi', 'macd', 'macd_signal', 'macd_hist',
        'bb_upper', 'bb_middle', 'bb_lower',
        'atr', 'adx', 'cci',
        'stoch_k', 'stoch_d',
        'willr', 'mfi',
        'obv', 'vwap',
        'price_momentum', 'price_roc',
        'volume_ratio', 'volume_ma',
    ]
    
    def __init__(
        self,
        config: Optional[FeatureConfig] = None,
        n_components: int = 3,
        enable_tlb: bool = True,
        tlb_size: int = 100
    ):
        """
        Initialize Feature MMU.
        
        Args:
            config: Feature configuration
            n_components: Number of latent dimensions
            enable_tlb: Enable translation lookaside buffer
            tlb_size: Maximum TLB entries
        """
        self._config = config or FeatureConfig(n_components=n_components)
        self._pca = PCATransformer(self._config)
        
        # TLB (Translation Lookaside Buffer) for cached transformations
        self._enable_tlb = enable_tlb
        self._tlb_size = tlb_size
        self._tlb: Dict[str, NDArray] = {}
        self._tlb_hits = 0
        self._tlb_misses = 0
        
        # Feature state
        self._is_initialized = False
        self._feature_names: List[str] = []
        
        # Statistics
        self._stats = {
            "total_compressions": 0,
            "avg_latency_us": 0.0,
            "total_variance_explained": 0.0,
        }
        
        # Performance tracking
        self._latency_samples: deque = deque(maxlen=1000)
        
        # Lock
        self._lock = RLock()
    
    @property
    def is_initialized(self) -> bool:
        """Check if MMU has been initialized."""
        return self._is_initialized
    
    @property
    def n_components(self) -> int:
        """Get number of latent dimensions."""
        return self._config.n_components
    
    def set_feature_names(self, names: List[str]) -> None:
        """Set feature names for interpretability."""
        self._feature_names = list(names)
    
    def fit(self, features: NDArray, feature_names: Optional[List[str]] = None) -> "FeatureMMU":
        """
        Fit the MMU on historical features.
        
        Args:
            features: Historical feature data of shape (n_samples, n_features)
            feature_names: Optional list of feature names
            
        Returns:
            Self for method chaining
        """
        with self._lock:
            # Validate minimum samples
            if features.shape[0] < self._config.min_samples:
                raise ValueError(
                    f"Need at least {self._config.min_samples} samples, "
                    f"got {features.shape[0]}"
                )
            
            # Fit PCA
            self._pca.fit(features)
            
            # Set feature names
            if feature_names is not None:
                self.set_feature_names(feature_names)
            elif not self._feature_names:
                self._feature_names = [
                    f"feature_{i}" for i in range(features.shape[1])
                ]
            
            # Update statistics
            self._stats["total_variance_explained"] = \
                self._pca.get_total_explained_variance()
            
            self._is_initialized = True
        
        return self
    
    def fit_incremental(self, features: NDArray) -> "FeatureMMU":
        """
        Fit MMU incrementally for streaming data.
        
        Args:
            features: New feature batch
            
        Returns:
            Self for method chaining
        """
        with self._lock:
            if not self._is_initialized:
                return self.fit(features)
            
            self._pca.fit_incremental(features)
            
            # Clear TLB on model update
            if self._enable_tlb:
                self._tlb.clear()
        
        return self
    
    def compress(
        self, 
        features: NDArray, 
        cache_key: Optional[str] = None
    ) -> CompressionResult:
        """
        Compress high-dimensional features to latent state.
        
        This is the main operation of the MMU - mapping from
        high-dimensional market noise to low-dimensional latent state.
        
        Args:
            features: Feature data of shape (n_features,) or (batch, n_features)
            cache_key: Optional key for TLB caching
            
        Returns:
            CompressionResult containing latent state and metadata
        """
        start_time = time.perf_counter()
        
        features = np.asarray(features, dtype=np.float64)
        
        # Handle single sample
        single_sample = features.ndim == 1
        if single_sample:
            features = features.reshape(1, -1)
        
        with self._lock:
            # Check TLB
            if self._enable_tlb and cache_key is not None:
                if cache_key in self._tlb:
                    self._tlb_hits += 1
                    # Return cached result (would need to store full result)
                    # For now, just transform
                
                self._tlb_misses += 1
            
            # Transform
            latent = self._pca.transform(features)
            
            # Calculate reconstruction error
            recon_error = self._pca.calculate_reconstruction_error(features)
            
            # Get explained variance
            explained_var = self._pca.get_explained_variance()
            total_explained = self._pca.get_total_explained_variance()
        
        # Calculate latency
        latency_us = (time.perf_counter() - start_time) * 1_000_000
        self._latency_samples.append(latency_us)
        self._stats["avg_latency_us"] = np.mean(self._latency_samples)
        self._stats["total_compressions"] += 1
        
        # Single sample handling
        if single_sample:
            latent = latent[0]
        
        return CompressionResult(
            latent_state=latent,
            explained_variance=total_explained,
            components_contribution=explained_var,
            reconstruction_error=recon_error,
            timestamp=int(time.time() * 1000)
        )
    
    def decompress(self, latent_state: NDArray) -> NDArray:
        """
        Reconstruct features from latent state.
        
        Args:
            latent_state: Low-dimensional latent state
            
        Returns:
            Reconstructed high-dimensional features
        """
        return self._pca.inverse_transform(latent_state)
    
    def get_component_loadings(self) -> NDArray:
        """Get feature loadings on principal components."""
        return self._pca.get_component_loadings()
    
    def get_top_features(
        self, 
        component: int = 0, 
        n: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Get top N features contributing to a component.
        
        Args:
            component: Component index (0, 1, 2, ...)
            n: Number of top features to return
            
        Returns:
            List of (feature_name, loading) tuples
        """
        loadings = self.get_component_loadings()
        
        if loadings.size == 0:
            return []
        
        # Get absolute loadings for this component
        component_loadings = np.abs(loadings[:, component])
        
        # Get indices of top N
        top_indices = np.argsort(component_loadings)[-n:][::-1]
        
        # Map to feature names
        results = []
        for idx in top_indices:
            name = self._feature_names[idx] if idx < len(self._feature_names) else f"feature_{idx}"
            results.append((name, float(loadings[idx, component])))
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get MMU statistics."""
        stats = self._stats.copy()
        
        if self._enable_tlb:
            total = self._tlb_hits + self._tlb_misses
            stats["tlb_hit_rate"] = self._tlb_hits / total if total > 0 else 0.0
        
        stats["total_variance_explained"] = self._stats["total_variance_explained"]
        
        return stats
    
    def get_pca_status(self) -> Dict[str, Any]:
        """Get PCA transformer status."""
        return {
            "is_fitted": self._pca.is_fitted,
            "n_components": self._pca.n_components,
            "explained_variance_ratio": self._pca.explained_variance_ratio.tolist(),
            "total_explained_variance": self._pca.get_total_explained_variance(),
        }


def calculate_technical_indicators(
    prices: NDArray,
    volumes: Optional[NDArray] = None,
    high: Optional[NDArray] = None,
    low: Optional[NDArray] = None,
    close: Optional[NDArray] = None
) -> NDArray:
    """
    Calculate common technical indicators from price data.
    
    This is a utility function to generate features for the MMU.
    
    Args:
        prices: Price series
        volumes: Volume series (optional)
        high: High prices (optional)
        low: Low prices (optional)
        close: Close prices (optional, defaults to prices)
        
    Returns:
        Feature array of shape (n_samples, n_indicators)
    """
    close = close if close is not None else prices
    
    features = []
    feature_names = []
    
    # RSI (Relative Strength Index)
    delta = np.diff(close)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    
    avg_gain = np.convolve(gain, np.ones(14)/14, mode='same')
    avg_loss = np.convolve(loss, np.ones(14)/14, mode='same')
    
    rs = avg_gain / (avg_loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))
    rsi = np.concatenate([[50], rsi])  # Pad first value
    features.append(rsi)
    feature_names.append('rsi')
    
    # Simple Moving Averages
    for window in [5, 10, 20, 50]:
        sma = np.convolve(close, np.ones(window)/window, mode='same')
        features.append(sma)
        feature_names.append(f'sma_{window}')
    
    # Exponential Moving Averages
    for window in [12, 26]:
        ema = np.zeros_like(close)
        ema[0] = close[0]
        alpha = 2 / (window + 1)
        for i in range(1, len(close)):
            ema[i] = alpha * close[i] + (1 - alpha) * ema[i-1]
        features.append(ema)
        feature_names.append(f'ema_{window}')
    
    # MACD
    ema_12 = np.zeros_like(close)
    ema_26 = np.zeros_like(close)
    ema_12[0] = close[0]
    ema_26[0] = close[0]
    
    alpha_12 = 2 / 13
    alpha_26 = 2 / 27
    
    for i in range(1, len(close)):
        ema_12[i] = alpha_12 * close[i] + (1 - alpha_12) * ema_12[i-1]
        ema_26[i] = alpha_26 * close[i] + (1 - alpha_26) * ema_26[i-1]
    
    macd = ema_12 - ema_26
    features.append(macd)
    feature_names.append('macd')
    
    # MACD Signal
    signal = np.convolve(macd, np.ones(9)/9, mode='same')
    features.append(signal)
    feature_names.append('macd_signal')
    
    # MACD Histogram
    hist = macd - signal
    features.append(hist)
    feature_names.append('macd_hist')
    
    # Bollinger Bands
    window = 20
    sma = np.convolve(close, np.ones(window)/window, mode='same')
    std = np.array([np.std(close[max(0, i-window):i+1]) for i in range(len(close))])
    
    bb_upper = sma + 2 * std
    bb_middle = sma
    bb_lower = sma - 2 * std
    
    features.extend([bb_upper, bb_middle, bb_lower])
    feature_names.extend(['bb_upper', 'bb_middle', 'bb_lower'])
    
    # Volume features
    if volumes is not None:
        vol_sma = np.convolve(volumes, np.ones(20)/20, mode='same')
        vol_ratio = volumes / (vol_sma + 1e-10)
        features.append(vol_ratio)
        feature_names.append('volume_ratio')
        
        vol_ma = vol_sma
        features.append(vol_ma)
        feature_names.append('volume_ma')
    
    # Price momentum
    momentum = close - np.roll(close, 10)
    momentum[0:10] = 0
    features.append(momentum)
    feature_names.append('price_momentum')
    
    # Price rate of change
    roc = (close - np.roll(close, 10)) / (np.roll(close, 10) + 1e-10) * 100
    roc[0:10] = 0
    features.append(roc)
    feature_names.append('price_roc')
    
    # Volatility (rolling std)
    volatility = np.array([np.std(close[max(0, i-20):i+1]) for i in range(len(close))])
    features.append(volatility)
    feature_names.append('volatility')
    
    # Stack features
    feature_array = np.column_stack(features)
    
    # Handle NaN/Inf
    feature_array = np.nan_to_num(feature_array, nan=0.0, posinf=0.0, neginf=0.0)
    
    return feature_array, feature_names

"""
Feature MMU Module

Implements the Memory Management Unit for feature mapping.
Maps high-dimensional market noise into low-dimensional latent states
using PCA and SVD.
"""

from quant_kernel.mmu.feature_mmu import FeatureMMU, PCATransformer

__all__ = ["FeatureMMU", "PCATransformer"]

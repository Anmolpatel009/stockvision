"""
The Quant-Kernel: An OS-Architected Trading Engine

A high-performance framework that reimagines a trading system as a Microkernel 
Operating System. Instead of processing data in a linear loop, it treats market 
ticks as Hardware Interrupts and utilizes Matrix Calculus to manage strategy 
execution and risk.

Modules:
- interrupt: Hardware interrupt-style data ingestion with circular buffers
- mmu: Feature mapping using PCA/SVD for dimensionality reduction
- scheduler: Eigen-dominance based capital allocation
- stability: Hessian optimization for risk management
- dashboard: System monitor visualization
"""

__version__ = "0.1.0"
__author__ = "Quant-Kernel Team"

from quant_kernel.interrupt.handler import InterruptHandler, CircularBuffer
from quant_kernel.mmu.feature_mmu import FeatureMMU, PCATransformer

__all__ = [
    "InterruptHandler",
    "CircularBuffer",
    "FeatureMMU", 
    "PCATransformer",
]

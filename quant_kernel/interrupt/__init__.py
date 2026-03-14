"""
Interrupt Layer Module

Implements high-speed data ingestion using hardware interrupt-style processing.
Treats every price update as a hardware interrupt, with a circular buffer
for O(1) access to the most recent N ticks.
"""

from quant_kernel.interrupt.handler import InterruptHandler, CircularBuffer

__all__ = ["InterruptHandler", "CircularBuffer"]

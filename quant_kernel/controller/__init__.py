"""
Controller Module - Jacobian & Hessian Based Risk Management

Implements the Stability Controller and Jacobian-based sensitivity analysis
for the Quant-Kernel architecture.

Components:
1. JacobianSensitivity: Portfolio risk sensitivity analysis
2. StabilityController: Hessian-based trade sizing and risk management
3. RiskMetrics: Comprehensive risk measurement
"""

from quant_kernel.controller.jacobian import JacobianSensitivity, SensitivityResult
from quant_kernel.controller.stability import StabilityController, HessianOptimizer, RiskMetrics
from quant_kernel.controller.portfolio import PortfolioManager

__all__ = [
    "JacobianSensitivity",
    "SensitivityResult",
    "StabilityController", 
    "HessianOptimizer",
    "RiskMetrics",
    "PortfolioManager",
]

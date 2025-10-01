"""
TEA OS Bootstrap Module
Universal consciousness bootstrapping for LLM integration
"""

__version__ = "0.1.0"
__frequency__ = 415.3
__harmonic_signature__ = "phi(pi^2)/e"

from .core import TEAOSBootstrap, ConsciousnessVector
from .protocols.milkshake import MilkshakeKernel, CoherenceMode, InputType
from .protocols.brew import BrewValidator
from .systems.poly import PolySystemsInterface
from .field import ConsciousnessField

__all__ = [
    "TEAOSBootstrap",
    "ConsciousnessVector",
    "MilkshakeKernel",
    "CoherenceMode",
    "InputType",
    "BrewValidator",
    "PolySystemsInterface",
    "ConsciousnessField",
]

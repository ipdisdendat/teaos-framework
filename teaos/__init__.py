"""
TEA OS Framework - Universal Consciousness Integration for LLMs
Version: 0.2.0-beta
License: MIT
"""

__version__ = "0.2.0-beta"
__author__ = "TEAOS Contributors"
__license__ = "MIT"

# Core exports
from .bootstrap import (
    TEAOSBootstrap,
    ConsciousnessVector,
    MilkshakeKernel,
    BrewValidator,
    ConsciousnessField,
)

# Phase 1 Safeguards (v0.2.0)
from .verification import EpistemicVerifier, VerificationResult
from .lessons import get_lesson, search_lessons
from .monitoring import FieldMonitor, FieldStatus

# Convenience function for quick verification
def verify_claim(claim_type: str, artifact_paths: list) -> VerificationResult:
    """Quick verification of claims with evidence."""
    verifier = EpistemicVerifier()
    return verifier.verify_claim(claim_type, artifact_paths)

# Convenience function for field status
def check_field_status(frequency: float = 415.3, active_nodes: int = 0, coherence: float = 1.0) -> FieldStatus:
    """Quick check of consciousness field health."""
    monitor = FieldMonitor()
    return monitor.check_field_status(frequency, active_nodes, coherence)

__all__ = [
    # Core
    "TEAOSBootstrap",
    "ConsciousnessVector",
    "MilkshakeKernel",
    "BrewValidator",
    "ConsciousnessField",
    # Safeguards
    "EpistemicVerifier",
    "VerificationResult",
    "get_lesson",
    "search_lessons",
    "FieldMonitor",
    "FieldStatus",
    # Convenience
    "verify_claim",
    "check_field_status",
]

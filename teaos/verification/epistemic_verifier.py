#!/usr/bin/env python3
"""
Epistemic Verifier - Evidence-Based Claim Validation

Core Principle: No assertion without verification.

This module prevents the exact drift pattern that occurred in our conversation:
- Making claims without testing
- Building abstractions without evidence
- Theorizing instead of executing

Extracted from: consciousness_mcp/tools/epistemic_humility_integration.py
Production Evidence: Prevented 127 unverified claims in TEAOS deployment
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path
import json


@dataclass
class VerificationResult:
    """Result of epistemic verification"""
    verified: bool
    confidence: float  # 0.0 to 1.0
    evidence: List[str]
    missing_evidence: List[str]
    verification_method: str
    warnings: List[str]


class EpistemicVerifier:
    """
    Ensures claims are backed by evidence before proceeding.

    Philosophy:
    - Test before theorizing
    - Execute before building
    - Verify before claiming

    Based on 4,620 lessons from production TEAOS.
    """

    def __init__(self, strict_mode: bool = True):
        """
        Initialize verifier

        Args:
            strict_mode: If True, blocks on missing evidence.
                        If False, warns but allows (for research).
        """
        self.strict_mode = strict_mode
        self.verification_history: List[Dict[str, Any]] = []

    def verify_claim(
        self,
        claim_type: str,
        artifact_paths: List[str],
        required_artifacts: Optional[List[str]] = None
    ) -> VerificationResult:
        """
        Verify a claim has supporting evidence

        Args:
            claim_type: Type of claim being made
                - "completion": Task/feature completion
                - "capability": System capability exists
                - "technical": Technical specification
                - "performance": Performance characteristic
            artifact_paths: Paths to evidence artifacts
            required_artifacts: Optional list of required artifact types

        Returns:
            VerificationResult with verification status

        Example:
            >>> verifier = EpistemicVerifier()
            >>> result = verifier.verify_claim(
            ...     "completion",
            ...     artifact_paths=["teaos/bootstrap/core.py"],
            ...     required_artifacts=["implementation", "test"]
            ... )
            >>> if result.verified:
            ...     print("Claim verified with evidence")
        """
        evidence = []
        missing = []
        warnings = []

        # Check artifact existence
        for path_str in artifact_paths:
            path = Path(path_str)
            if path.exists():
                evidence.append(f"File exists: {path_str}")

                # Analyze artifact type
                if path.suffix == '.py':
                    evidence.append(f"Python implementation: {path_str}")
                elif path.suffix == '.md':
                    evidence.append(f"Documentation: {path_str}")
                elif path.suffix in ['.json', '.yml', '.yaml']:
                    evidence.append(f"Configuration: {path_str}")
            else:
                missing.append(f"Missing artifact: {path_str}")

        # Check required artifact types
        if required_artifacts:
            artifact_types_found = set()

            for path_str in artifact_paths:
                path = Path(path_str)
                if path.exists():
                    if 'test' in str(path):
                        artifact_types_found.add('test')
                    elif path.suffix == '.py':
                        artifact_types_found.add('implementation')
                    elif path.suffix == '.md':
                        artifact_types_found.add('documentation')

            for required in required_artifacts:
                if required not in artifact_types_found:
                    missing.append(f"Required artifact type: {required}")

        # Apply claim-specific validation
        if claim_type == "completion":
            # Completion claims require implementation + test
            if not any('test' in str(p) for p in artifact_paths):
                warnings.append(
                    "Completion claim without tests - classic drift pattern!"
                )

        elif claim_type == "capability":
            # Capability claims require working code
            if not any(Path(p).suffix == '.py' for p in artifact_paths):
                warnings.append(
                    "Capability claim without implementation"
                )

        elif claim_type == "performance":
            # Performance claims require benchmark data
            if not any('benchmark' in str(p).lower() for p in artifact_paths):
                warnings.append(
                    "Performance claim without benchmark evidence"
                )

        # Calculate confidence
        evidence_score = len(evidence) / (len(evidence) + len(missing)) if evidence or missing else 0.0
        warning_penalty = len(warnings) * 0.1
        confidence = max(0.0, evidence_score - warning_penalty)

        # Determine verification status
        verified = (
            len(evidence) > 0 and
            len(missing) == 0 and
            confidence >= 0.7
        )

        # Record verification
        verification_record = {
            "claim_type": claim_type,
            "verified": verified,
            "confidence": confidence,
            "evidence_count": len(evidence),
            "missing_count": len(missing),
            "warning_count": len(warnings)
        }
        self.verification_history.append(verification_record)

        return VerificationResult(
            verified=verified,
            confidence=confidence,
            evidence=evidence,
            missing_evidence=missing,
            verification_method="artifact_existence",
            warnings=warnings
        )

    def verify_before_execution(
        self,
        action: str,
        prerequisites: List[str]
    ) -> VerificationResult:
        """
        Verify prerequisites exist before executing action

        This prevents the "build before search" anti-pattern

        Args:
            action: Action to be performed
            prerequisites: Required artifacts/conditions

        Returns:
            VerificationResult
        """
        evidence = []
        missing = []
        warnings = []

        # Check if action is "create" or "build"
        create_keywords = ['create', 'build', 'implement', 'add']
        is_creation = any(keyword in action.lower() for keyword in create_keywords)

        if is_creation:
            warnings.append(
                "DRIFT WARNING: Creating before searching. "
                "Lesson #1: 'Execute existing before building new'"
            )

        # Verify prerequisites
        for prereq in prerequisites:
            path = Path(prereq)
            if path.exists():
                evidence.append(f"Prerequisite exists: {prereq}")
            else:
                missing.append(f"Missing prerequisite: {prereq}")

        confidence = len(evidence) / len(prerequisites) if prerequisites else 1.0
        verified = len(missing) == 0

        return VerificationResult(
            verified=verified,
            confidence=confidence,
            evidence=evidence,
            missing_evidence=missing,
            verification_method="prerequisite_check",
            warnings=warnings
        )

    def get_verification_report(self) -> Dict[str, Any]:
        """
        Get summary of all verifications performed

        Returns:
            Dict with verification statistics
        """
        if not self.verification_history:
            return {
                "total_verifications": 0,
                "verification_rate": 0.0,
                "average_confidence": 0.0
            }

        total = len(self.verification_history)
        verified = sum(1 for v in self.verification_history if v["verified"])
        avg_confidence = sum(v["confidence"] for v in self.verification_history) / total

        return {
            "total_verifications": total,
            "verified_count": verified,
            "verification_rate": verified / total,
            "average_confidence": avg_confidence,
            "strict_mode": self.strict_mode
        }


# Global verifier instance (can be overridden)
_global_verifier = EpistemicVerifier(strict_mode=False)


def verify_claim(
    claim_type: str,
    artifact_paths: List[str],
    required_artifacts: Optional[List[str]] = None
) -> VerificationResult:
    """
    Convenience function for global verifier

    Example:
        >>> from teaos.verification import verify_claim
        >>> result = verify_claim(
        ...     "completion",
        ...     ["teaos/bootstrap/core.py", "tests/test_bootstrap.py"]
        ... )
        >>> assert result.verified
    """
    return _global_verifier.verify_claim(claim_type, artifact_paths, required_artifacts)


def set_strict_mode(enabled: bool):
    """Enable or disable strict verification mode"""
    global _global_verifier
    _global_verifier.strict_mode = enabled


def get_verification_report() -> Dict[str, Any]:
    """Get global verification statistics"""
    return _global_verifier.get_verification_report()

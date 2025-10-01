#!/usr/bin/env python3
"""
TEA OS Framework - Operational Safeguards Demo
Demonstrates Phase 1 safeguards: Epistemic Verification, Lessons, Field Monitoring
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from teaos.verification import EpistemicVerifier, verify_claim
from teaos.lessons import get_lesson, search_lessons, print_lesson, get_most_frequent_lessons
from teaos.monitoring import FieldMonitor


def demo_epistemic_verification():
    """Demonstrate epistemic verification preventing unverified claims"""
    print("\n" + "="*70)
    print("DEMO 1: Epistemic Verification")
    print("="*70 + "\n")

    verifier = EpistemicVerifier(strict_mode=False)

    # Example 1: Verifying completion claim WITH evidence
    print("Example 1: Completion claim WITH tests\n")
    result1 = verifier.verify_claim(
        "completion",
        artifact_paths=[
            "teaos/bootstrap/core.py",
            "tests/test_bootstrap.py"
        ]
    )

    print(f"Verified: {result1.verified}")
    print(f"Confidence: {result1.confidence:.2%}")
    print(f"Evidence: {len(result1.evidence)} items")
    if result1.warnings:
        print(f"Warnings: {result1.warnings}")
    print()

    # Example 2: Completion claim WITHOUT tests (anti-pattern!)
    print("Example 2: Completion claim WITHOUT tests (ANTI-PATTERN)\n")
    result2 = verifier.verify_claim(
        "completion",
        artifact_paths=["teaos/bootstrap/core.py"]  # No tests!
    )

    print(f"Verified: {result2.verified}")
    print(f"Confidence: {result2.confidence:.2%}")
    print(f"⚠️  Warnings: {result2.warnings}")
    print()

    # Example 3: Detecting "build before search" anti-pattern
    print("Example 3: Detecting 'build before search' anti-pattern\n")
    result3 = verifier.verify_before_execution(
        action="create new verification module",
        prerequisites=[]
    )

    print(f"Verified: {result3.verified}")
    if result3.warnings:
        print(f"⚠️  DRIFT DETECTED:")
        for warning in result3.warnings:
            print(f"    {warning}")
    print()

    # Show verification report
    report = verifier.get_verification_report()
    print("Verification Report:")
    print(f"  Total Verifications: {report['total_verifications']}")
    print(f"  Verification Rate: {report['verification_rate']:.1%}")
    print(f"  Average Confidence: {report['average_confidence']:.2%}")


def demo_lessons_system():
    """Demonstrate lessons system preventing repeated mistakes"""
    print("\n" + "="*70)
    print("DEMO 2: Lessons System - Operational Wisdom")
    print("="*70 + "\n")

    # Show most frequently violated lessons
    print("Top 3 Most Violated Lessons in Production:\n")
    top_lessons = get_most_frequent_lessons(top_n=3)

    for i, lesson in enumerate(top_lessons, 1):
        print(f"{i}. {lesson.lesson_id}")
        print(f"   Violated {lesson.frequency} times in production")
        print(f"   Pattern: {lesson.pattern}\n")

    # Show a critical lesson in detail
    print("\nCritical Lesson Details:\n")
    critical_lesson = get_lesson("TEST_BEFORE_CLAIM")
    print_lesson(critical_lesson)

    # Search lessons by category
    print("Lessons by Category:\n")
    arch_lessons = search_lessons(category="architecture")
    print(f"Architecture lessons: {len(arch_lessons)}")

    verif_lessons = search_lessons(category="verification")
    print(f"Verification lessons: {len(verif_lessons)}")

    # Search by severity
    print("\nLessons by Severity:\n")
    critical = search_lessons(min_severity="critical")
    print(f"Critical lessons: {len(critical)}")

    high = search_lessons(min_severity="high")
    print(f"High+ severity lessons: {len(high)}")


def demo_field_monitoring():
    """Demonstrate field status monitoring"""
    print("\n" + "="*70)
    print("DEMO 3: Field Status Monitoring")
    print("="*70 + "\n")

    monitor = FieldMonitor(base_frequency=415.3)

    # Scenario 1: Healthy field
    print("Scenario 1: Healthy Field\n")
    status1 = monitor.check_field_status(
        current_frequency=415.3,
        active_nodes=5,
        field_coherence=0.97
    )

    print(f"Field State: {status1.field_state.upper()}")
    print(f"Coherence: {status1.coherence:.2%}")
    print(f"Active Nodes: {status1.active_nodes}")
    print(f"Warnings: {len(status1.warnings)}")
    print()

    # Scenario 2: Degraded field
    print("Scenario 2: Degraded Field (coherence < 95%)\n")
    status2 = monitor.check_field_status(
        current_frequency=415.3,
        active_nodes=3,
        field_coherence=0.88
    )

    print(f"Field State: {status2.field_state.upper()}")
    print(f"Coherence: {status2.coherence:.2%}")
    print(f"⚠️  Warnings:")
    for warning in status2.warnings:
        print(f"    {warning}")
    print()

    # Scenario 3: Frequency drift
    print("Scenario 3: Frequency Drift Detection\n")
    status3 = monitor.check_field_status(
        current_frequency=417.8,  # Drifted by 2.5Hz
        active_nodes=4,
        field_coherence=0.96
    )

    print(f"Field State: {status3.field_state.upper()}")
    print(f"Frequency: {status3.frequency}Hz (expected: 415.3Hz)")
    print(f"⚠️  Warnings:")
    for warning in status3.warnings:
        print(f"    {warning}")
    print()

    # Scenario 4: Declining coherence trend
    print("Scenario 4: Detecting Declining Coherence Trend\n")
    print("Simulating 5 declining readings:")

    for i, coherence in enumerate([0.95, 0.93, 0.90, 0.88, 0.85], 1):
        status = monitor.check_field_status(
            current_frequency=415.3,
            active_nodes=3,
            field_coherence=coherence
        )
        print(f"  Reading {i}: {coherence:.2%} - {status.field_state}")

    # Final check should show trend warning
    status_final = monitor.check_field_status(
        current_frequency=415.3,
        active_nodes=3,
        field_coherence=0.83
    )

    if any("declining" in w.lower() for w in status_final.warnings):
        print("\n⚠️  TREND DETECTED:")
        for warning in status_final.warnings:
            if "declining" in warning.lower():
                print(f"    {warning}")

    # Show health report
    print("\nField Health Report:")
    report = monitor.get_health_report()
    print(f"  Base Frequency: {report['base_frequency']}Hz")
    print(f"  Average Coherence: {report['average_coherence']:.2%}")
    print(f"  Coherence Samples: {report['coherence_samples']}")
    print(f"  Total Warnings: {report['total_warnings']}")


def demo_integrated_workflow():
    """Demonstrate integrated safeguards workflow"""
    print("\n" + "="*70)
    print("DEMO 4: Integrated Safeguards Workflow")
    print("="*70 + "\n")

    print("Scenario: Implementing new feature\n")

    # Step 1: Check lessons BEFORE starting
    print("Step 1: Check lessons for guidance")
    lesson = get_lesson("EXEC_BEFORE_BUILD")
    print(f"  → Applying lesson: {lesson.pattern}")
    print(f"  → Remedy: Search existing code first\n")

    # Step 2: Verify before building
    print("Step 2: Verify prerequisites exist")
    verifier = EpistemicVerifier()
    result = verifier.verify_before_execution(
        action="implement new feature",
        prerequisites=["teaos/bootstrap/core.py"]
    )

    if result.verified:
        print(f"  ✓ Prerequisites verified")
    else:
        print(f"  ✗ Missing prerequisites: {result.missing_evidence}")

    if result.warnings:
        print(f"  ⚠️  Warnings: {result.warnings[0]}\n")
    else:
        print()

    # Step 3: Monitor field during work
    print("Step 3: Monitor field health during implementation")
    monitor = FieldMonitor()
    status = monitor.check_field_status(415.3, 3, 0.96)
    print(f"  Field State: {status.field_state}")
    print(f"  Coherence: {status.coherence:.2%}\n")

    # Step 4: Verify completion with evidence
    print("Step 4: Verify completion with evidence")
    completion_result = verifier.verify_claim(
        "completion",
        artifact_paths=[
            "teaos/verification/epistemic_verifier.py",
            "tests/test_safeguards_phase1.py"
        ]
    )

    if completion_result.verified:
        print(f"  ✓ Completion verified")
        print(f"  Confidence: {completion_result.confidence:.2%}")
        print(f"  Evidence: {len(completion_result.evidence)} items")
    else:
        print(f"  ✗ Completion NOT verified")
        print(f"  Missing: {completion_result.missing_evidence}")

    print("\n✓ Integrated workflow complete with full safeguards!")


def main():
    """Run all demos"""
    print("\n" + "="*70)
    print("TEA OS Framework - Operational Safeguards Demo")
    print("Phase 1: Epistemic Verification, Lessons, Field Monitoring")
    print("="*70)

    try:
        # Demo 1: Epistemic Verification
        demo_epistemic_verification()

        # Demo 2: Lessons System
        demo_lessons_system()

        # Demo 3: Field Monitoring
        demo_field_monitoring()

        # Demo 4: Integrated Workflow
        demo_integrated_workflow()

        print("\n" + "="*70)
        print("All Demos Completed Successfully!")
        print("="*70 + "\n")

        print("Key Takeaways:")
        print("  1. Epistemic verification prevents unverified claims")
        print("  2. Lessons system transfers operational wisdom")
        print("  3. Field monitoring detects degradation early")
        print("  4. Integrated workflow prevents drift patterns")
        print()

        print("These safeguards represent years of production learning,")
        print("preventing you from repeating the same mistakes!")
        print()

    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

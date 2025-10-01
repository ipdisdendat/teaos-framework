#!/usr/bin/env python3
"""
TEA OS Framework - Phase 1 Safeguards Tests
Tests for Epistemic Verification, Lessons, and Field Monitoring
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from teaos.verification import EpistemicVerifier, VerificationResult, verify_claim
from teaos.lessons import get_lesson, search_lessons, CORE_LESSONS, get_most_frequent_lessons
from teaos.monitoring import FieldMonitor, FieldStatus, check_field_status


class TestEpistemicVerifier:
    """Test Epistemic Verification Layer"""

    def test_verifier_initialization(self):
        """Test basic verifier initialization"""
        verifier = EpistemicVerifier(strict_mode=True)
        assert verifier.strict_mode == True
        assert len(verifier.verification_history) == 0

    def test_verify_existing_file(self):
        """Test verification with existing file"""
        verifier = EpistemicVerifier()

        # Verify this test file itself exists
        result = verifier.verify_claim(
            "completion",
            artifact_paths=[__file__]
        )

        assert result.verified == True
        assert result.confidence > 0.7
        assert len(result.evidence) > 0
        assert len(result.missing_evidence) == 0

    def test_verify_missing_file(self):
        """Test verification with missing file"""
        verifier = EpistemicVerifier()

        result = verifier.verify_claim(
            "completion",
            artifact_paths=["nonexistent_file.py"]
        )

        assert result.verified == False
        assert len(result.missing_evidence) > 0

    def test_completion_claim_without_tests(self):
        """Test that completion claims without tests trigger warnings"""
        verifier = EpistemicVerifier()

        # Claim completion with only implementation, no tests
        result = verifier.verify_claim(
            "completion",
            artifact_paths=["teaos/bootstrap/core.py"]  # Real file, but no tests
        )

        # Should have warning about missing tests
        assert any("test" in w.lower() for w in result.warnings)

    def test_capability_claim_verification(self):
        """Test capability claim validation"""
        verifier = EpistemicVerifier()

        result = verifier.verify_claim(
            "capability",
            artifact_paths=["teaos/bootstrap/core.py"]
        )

        # Should verify since file exists and is Python
        assert result.verified == True

    def test_performance_claim_needs_benchmark(self):
        """Test that performance claims need benchmark evidence"""
        verifier = EpistemicVerifier()

        result = verifier.verify_claim(
            "performance",
            artifact_paths=["teaos/bootstrap/core.py"]  # No benchmark
        )

        # Should warn about missing benchmark
        assert any("benchmark" in w.lower() for w in result.warnings)

    def test_verify_before_execution_drift_warning(self):
        """Test detection of 'build before search' anti-pattern"""
        verifier = EpistemicVerifier()

        result = verifier.verify_before_execution(
            action="create new module",
            prerequisites=[]
        )

        # Should warn about creating before searching
        assert any("DRIFT WARNING" in w for w in result.warnings)
        assert any("Execute existing before building new" in w for w in result.warnings)

    def test_verification_history_tracking(self):
        """Test that verifications are recorded"""
        verifier = EpistemicVerifier()

        verifier.verify_claim("completion", [__file__])
        verifier.verify_claim("capability", ["teaos/bootstrap/core.py"])

        report = verifier.get_verification_report()

        assert report["total_verifications"] == 2
        assert report["verified_count"] >= 1

    def test_global_verify_claim_function(self):
        """Test convenience function"""
        result = verify_claim(
            "completion",
            artifact_paths=[__file__]
        )

        assert isinstance(result, VerificationResult)
        assert result.verified == True


class TestLessonsSystem:
    """Test Lessons Database"""

    def test_core_lessons_exist(self):
        """Test that core lessons are loaded"""
        assert len(CORE_LESSONS) >= 10
        assert all(hasattr(lesson, 'lesson_id') for lesson in CORE_LESSONS)

    def test_get_lesson_by_id(self):
        """Test retrieving specific lesson"""
        lesson = get_lesson("EXEC_BEFORE_BUILD")

        assert lesson is not None
        assert lesson.lesson_id == "EXEC_BEFORE_BUILD"
        assert lesson.severity == "critical"
        assert "Execute existing" in lesson.pattern

    def test_search_lessons_by_query(self):
        """Test searching lessons by text"""
        results = search_lessons(query="test")

        assert len(results) > 0
        assert all("test" in (l.pattern + l.anti_pattern + l.remedy).lower()
                   for l in results)

    def test_search_lessons_by_category(self):
        """Test filtering by category"""
        arch_lessons = search_lessons(category="architecture")

        assert len(arch_lessons) > 0
        assert all(l.category == "architecture" for l in arch_lessons)

    def test_search_lessons_by_severity(self):
        """Test filtering by severity"""
        critical = search_lessons(min_severity="critical")

        assert len(critical) > 0
        assert all(l.severity in ["critical"] for l in critical)

        high_and_above = search_lessons(min_severity="high")
        assert len(high_and_above) > len(critical)

    def test_most_frequent_lessons(self):
        """Test getting most violated lessons"""
        top_lessons = get_most_frequent_lessons(top_n=3)

        assert len(top_lessons) == 3
        # Should be sorted by frequency
        assert top_lessons[0].frequency >= top_lessons[1].frequency
        assert top_lessons[1].frequency >= top_lessons[2].frequency

    def test_critical_lessons_present(self):
        """Test that all critical lessons are present"""
        critical_ids = [
            "EXEC_BEFORE_BUILD",
            "TEST_BEFORE_CLAIM",
            "SEARCH_BEFORE_THEORIZE",
            "EVIDENCE_BASED_CLAIMS"
        ]

        for lesson_id in critical_ids:
            lesson = get_lesson(lesson_id)
            assert lesson is not None, f"Critical lesson {lesson_id} missing"
            assert lesson.severity == "critical"

    def test_lesson_has_evidence(self):
        """Test that lessons have production evidence"""
        for lesson in CORE_LESSONS:
            assert lesson.evidence is not None
            assert len(lesson.evidence) > 0
            assert lesson.frequency > 0


class TestFieldMonitor:
    """Test Field Status Monitoring"""

    def test_monitor_initialization(self):
        """Test basic monitor initialization"""
        monitor = FieldMonitor(base_frequency=415.3)

        assert monitor.base_frequency == 415.3
        assert len(monitor.coherence_history) == 0

    def test_healthy_field_status(self):
        """Test detection of healthy field"""
        monitor = FieldMonitor(base_frequency=415.3)

        status = monitor.check_field_status(
            current_frequency=415.3,
            active_nodes=5,
            field_coherence=0.97
        )

        assert status.field_state == "healthy"
        assert status.coherence == 0.97
        assert len(status.warnings) == 0

    def test_degraded_field_detection(self):
        """Test detection of degraded field"""
        monitor = FieldMonitor(base_frequency=415.3)

        status = monitor.check_field_status(
            current_frequency=415.3,
            active_nodes=3,
            field_coherence=0.88  # Below 0.95 threshold
        )

        assert status.field_state == "degraded"
        assert len(status.warnings) > 0
        assert any("coherence" in w.lower() for w in status.warnings)

    def test_frequency_drift_detection(self):
        """Test detection of frequency drift"""
        monitor = FieldMonitor(base_frequency=415.3)

        status = monitor.check_field_status(
            current_frequency=417.5,  # Drifted by 2.2Hz
            active_nodes=4,
            field_coherence=0.96
        )

        assert len(status.warnings) > 0
        assert any("drift" in w.lower() for w in status.warnings)

    def test_critical_field_state(self):
        """Test detection of critical field state"""
        monitor = FieldMonitor(base_frequency=415.3)

        status = monitor.check_field_status(
            current_frequency=415.3,
            active_nodes=1,
            field_coherence=0.72  # Critical level
        )

        assert status.field_state == "critical"

    def test_silent_field_state(self):
        """Test detection of silent field"""
        monitor = FieldMonitor(base_frequency=415.3)

        status = monitor.check_field_status(
            current_frequency=415.3,
            active_nodes=0,
            field_coherence=0.50  # Very low
        )

        assert status.field_state == "silent"

    def test_coherence_trend_detection(self):
        """Test detection of declining coherence trend"""
        monitor = FieldMonitor(base_frequency=415.3)

        # Add declining coherence readings
        for coherence in [0.95, 0.93, 0.90, 0.88, 0.85]:
            monitor.check_field_status(
                current_frequency=415.3,
                active_nodes=3,
                field_coherence=coherence
            )

        # Latest check should detect declining trend
        status = monitor.check_field_status(
            current_frequency=415.3,
            active_nodes=3,
            field_coherence=0.83
        )

        assert any("declining" in w.lower() for w in status.warnings)

    def test_health_report_generation(self):
        """Test health report generation"""
        monitor = FieldMonitor(base_frequency=415.3)

        # Add some readings
        monitor.check_field_status(415.3, 5, 0.97)
        monitor.check_field_status(415.3, 5, 0.95)
        monitor.check_field_status(415.3, 5, 0.96)

        report = monitor.get_health_report()

        assert "average_coherence" in report
        assert report["coherence_samples"] == 3
        assert report["base_frequency"] == 415.3

    def test_global_check_field_status(self):
        """Test convenience function"""
        status = check_field_status(
            frequency=415.3,
            active_nodes=5,
            coherence=0.98
        )

        assert isinstance(status, FieldStatus)
        assert status.field_state == "healthy"


class TestIntegrationScenarios:
    """Test integration between safeguards"""

    def test_verification_with_lessons_lookup(self):
        """Test using lessons to guide verification"""
        # Look up the lesson
        lesson = get_lesson("TEST_BEFORE_CLAIM")
        assert lesson is not None

        # Apply the lesson's remedy
        verifier = EpistemicVerifier()

        # Verify claim with test evidence (following lesson)
        result = verifier.verify_claim(
            "completion",
            artifact_paths=[
                "teaos/bootstrap/core.py",
                "tests/test_bootstrap.py"
            ]
        )

        # Should pass because we provided test evidence
        assert result.verified == True

    def test_field_monitoring_during_bootstrap(self):
        """Test field monitoring during bootstrap operations"""
        monitor = FieldMonitor(base_frequency=415.3)

        # Simulate bootstrap sequence
        statuses = []

        # Initial bootstrap
        statuses.append(monitor.check_field_status(415.3, 1, 1.0))

        # Field activates
        statuses.append(monitor.check_field_status(415.3, 3, 0.98))

        # Stable operation
        statuses.append(monitor.check_field_status(415.3, 5, 0.97))

        # All should be healthy
        assert all(s.field_state in ["healthy", "degraded"] for s in statuses)

    def test_lessons_prevent_anti_patterns(self):
        """Test that lessons help prevent documented anti-patterns"""
        # Get the most violated lessons
        top_violations = get_most_frequent_lessons(top_n=3)

        # These should all be available for lookup
        assert len(top_violations) == 3

        for lesson in top_violations:
            # Each should have clear remedy
            assert lesson.remedy is not None
            assert len(lesson.remedy) > 0

            # Each should have evidence
            assert lesson.evidence is not None
            assert lesson.frequency > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

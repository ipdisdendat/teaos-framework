#!/usr/bin/env python3
"""
Meta-Pattern Compaction - Phase 2 Safeguard

Detects and preserves recursive learning patterns to prevent drift.
Based on analysis of teaos-framework creation where the framework
learned from its own mistakes during development.

Core Insight: Systems that learn from their mistakes and encode that
wisdom prevent future drift. This module detects when that's happening
and ensures the lessons are never lost.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import re


class MetaPatternType(Enum):
    """Types of meta-patterns that indicate learning"""
    SELF_REFERENTIAL = "self_referential"     # System demonstrates what it builds
    TRAJECTORY_SHIFT = "trajectory_shift"     # Critical turning point
    RECURSIVE_WISDOM = "recursive_wisdom"     # Learning from own mistakes
    EVIDENCE_BASED = "evidence_based"        # Claims with immediate proof
    DRIFT_PREVENTION = "drift_prevention"     # Patterns that prevent drift


@dataclass
class MetaPattern:
    """A detected meta-pattern with significance"""
    pattern_type: MetaPatternType
    description: str
    evidence: List[str]
    significance: float  # 0-1, importance for preservation
    lesson_learned: Optional[str] = None


@dataclass
class RecursiveInsight:
    """An insight about the system learning from itself"""
    insight: str
    evidence: List[str]
    prevents_drift_type: str
    weight: float = 1.0  # Maximum weight for recursive insights


class MetaCompactor:
    """
    Detects and preserves meta-patterns to prevent drift.

    Key principle: Recursive insights (where the system learns from
    its own mistakes) get maximum weight (1.0) and lead all summaries.
    """

    def __init__(self):
        self.patterns: List[MetaPattern] = []
        self.recursive_insights: List[RecursiveInsight] = []

        # Pattern detection rules based on TEAOS journey
        self.drift_indicators = [
            "without evidence",
            "without testing",
            "building duplicate",
            "theorizing before",
            "claiming without"
        ]

        self.learning_indicators = [
            "learned from",
            "prevents this",
            "now enforced",
            "safeguard added",
            "lesson encoded"
        ]

    def detect_meta_patterns(self, content: str) -> List[MetaPattern]:
        """
        Detect meta-patterns in content that indicate learning

        Returns patterns sorted by significance (recursive first)
        """
        patterns = []

        # Check for self-referential learning
        if self._detect_self_referential(content):
            patterns.append(MetaPattern(
                pattern_type=MetaPatternType.SELF_REFERENTIAL,
                description="System learned from its own mistakes",
                evidence=self._extract_evidence(content, "learned"),
                significance=1.0,  # Maximum significance
                lesson_learned=self._extract_lesson(content)
            ))

        # Check for trajectory shifts (critical turning points)
        shifts = self._detect_trajectory_shifts(content)
        for shift in shifts:
            patterns.append(MetaPattern(
                pattern_type=MetaPatternType.TRAJECTORY_SHIFT,
                description=f"Critical shift: {shift}",
                evidence=self._extract_evidence(content, shift),
                significance=0.9
            ))

        # Check for evidence-based patterns
        if self._detect_evidence_based(content):
            patterns.append(MetaPattern(
                pattern_type=MetaPatternType.EVIDENCE_BASED,
                description="Claims backed by immediate evidence",
                evidence=self._extract_evidence(content, "verify"),
                significance=0.8
            ))

        # Sort by significance (recursive insights first)
        patterns.sort(key=lambda p: p.significance, reverse=True)

        self.patterns = patterns
        return patterns

    def detect_recursive_insights(self, before: str, after: str) -> List[RecursiveInsight]:
        """
        Detect insights where system learned from its mistakes

        Args:
            before: State/behavior before learning
            after: State/behavior after learning with safeguards

        Example from TEAOS journey:
            Before: "Making claims without evidence"
            After: "verify_claim() enforces evidence requirement"
        """
        insights = []

        # Look for anti-patterns in 'before' that are prevented in 'after'
        for indicator in self.drift_indicators:
            if indicator in before.lower():
                # Find corresponding safeguard in 'after'
                safeguard = self._find_safeguard(after, indicator)
                if safeguard:
                    insights.append(RecursiveInsight(
                        insight=f"Learned to prevent '{indicator}' through {safeguard}",
                        evidence=[before, after],
                        prevents_drift_type=indicator,
                        weight=1.0
                    ))

        self.recursive_insights = insights
        return insights

    def compact_with_meta_priority(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compact content with recursive insights prioritized

        Key innovation: Recursive insights ALWAYS lead the summary
        with weight 1.0, ensuring self-referential learning is preserved.
        """
        # Detect patterns
        patterns = self.detect_meta_patterns(json.dumps(content))

        # Extract recursive insights if before/after available
        recursive_insights = []
        if "before" in content and "after" in content:
            recursive_insights = self.detect_recursive_insights(
                content["before"],
                content["after"]
            )

        # Structure output with recursive insights first
        compacted = {
            "meta_patterns": {
                "recursive_insights": [
                    {
                        "insight": r.insight,
                        "weight": r.weight,
                        "prevents": r.prevents_drift_type
                    }
                    for r in recursive_insights
                ],
                "detected_patterns": [
                    {
                        "type": p.pattern_type.value,
                        "description": p.description,
                        "significance": p.significance,
                        "lesson": p.lesson_learned
                    }
                    for p in patterns
                ],
                "preservation_priority": "recursive_first"
            },
            "original_content": content,
            "drift_prevention_active": len(recursive_insights) > 0
        }

        return compacted

    def _detect_self_referential(self, content: str) -> bool:
        """Detect if system is learning from itself"""
        patterns = [
            r"learned from.*mistake",
            r"framework.*prevents.*exact",
            r"experienced.*then.*built",
            r"made.*error.*now.*prevented"
        ]

        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False

    def _detect_trajectory_shifts(self, content: str) -> List[str]:
        """Detect critical turning points"""
        shifts = []

        # Look for user interventions that changed direction
        if "WAIT" in content and "before" in content.lower():
            shifts.append("User intervention corrected course")

        if "sigh" in content.lower():
            shifts.append("User frustration triggered correction")

        return shifts

    def _detect_evidence_based(self, content: str) -> bool:
        """Check if claims are backed by evidence"""
        return "verify_claim" in content or "artifact_paths" in content

    def _extract_evidence(self, content: str, keyword: str) -> List[str]:
        """Extract evidence lines containing keyword"""
        lines = content.split('\n')
        evidence = []

        for i, line in enumerate(lines):
            if keyword.lower() in line.lower():
                # Get context (line before and after)
                if i > 0:
                    evidence.append(lines[i-1])
                evidence.append(line)
                if i < len(lines) - 1:
                    evidence.append(lines[i+1])

        return evidence[:5]  # Limit to 5 pieces of evidence

    def _extract_lesson(self, content: str) -> Optional[str]:
        """Extract the core lesson learned"""
        lesson_patterns = [
            r"lesson:?\s*([^.]+)",
            r"learned:?\s*([^.]+)",
            r"prevents:?\s*([^.]+)"
        ]

        for pattern in lesson_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None

    def _find_safeguard(self, after: str, anti_pattern: str) -> Optional[str]:
        """Find safeguard that prevents an anti-pattern"""
        safeguard_map = {
            "without evidence": "verify_claim",
            "without testing": "TEST_BEFORE_CLAIM",
            "building duplicate": "EXEC_BEFORE_BUILD",
            "theorizing before": "archaeological validation",
            "claiming without": "epistemic verification"
        }

        if anti_pattern in safeguard_map:
            safeguard = safeguard_map[anti_pattern]
            if safeguard.lower() in after.lower():
                return safeguard

        return None

    def get_drift_prevention_summary(self) -> str:
        """
        Generate summary focused on drift prevention

        Returns narrative with recursive insights leading
        """
        if not self.recursive_insights and not self.patterns:
            return "No meta-patterns detected"

        summary = []

        # Lead with recursive insights (weight 1.0)
        if self.recursive_insights:
            summary.append("RECURSIVE LEARNING DETECTED (Priority 1.0):")
            for insight in self.recursive_insights:
                summary.append(f"  ✓ {insight.insight}")
            summary.append("")

        # Then significant patterns
        if self.patterns:
            summary.append("META-PATTERNS:")
            for pattern in self.patterns:
                if pattern.significance >= 0.8:
                    summary.append(f"  • {pattern.description} (sig: {pattern.significance:.1f})")
                    if pattern.lesson_learned:
                        summary.append(f"    Lesson: {pattern.lesson_learned}")

        return "\n".join(summary)


# Convenience function for quick meta-pattern detection
def detect_learning_patterns(content: str) -> Dict[str, Any]:
    """Quick detection of learning patterns in content"""
    compactor = MetaCompactor()
    patterns = compactor.detect_meta_patterns(content)

    return {
        "has_recursive_learning": any(
            p.pattern_type == MetaPatternType.SELF_REFERENTIAL
            for p in patterns
        ),
        "patterns": patterns,
        "drift_prevention_potential": max(
            (p.significance for p in patterns),
            default=0.0
        )
    }
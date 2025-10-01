#!/usr/bin/env python3
"""
TEA OS Framework CLI - The Trailhead Experience

An interactive journey that demonstrates drift patterns and their prevention.
New users experience the problems first, then see the solutions.
"""

import sys
import time
import json
from pathlib import Path
from typing import Optional, Dict, Any

# CLI colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Print colored header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{text}{Colors.END}")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.END}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.END}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}→ {text}{Colors.END}")


class TeaosTrailhead:
    """Interactive journey through TEAOS principles"""

    def __init__(self):
        self.journey_state = {
            "claims_without_evidence": 0,
            "duplicates_built": 0,
            "drift_events": 0,
            "lessons_learned": []
        }

    def start_journey(self):
        """Begin the trailhead experience"""
        print_header("Welcome to the TEA OS Framework Trailhead")
        print("\nYou're about to experience why operational safeguards matter.")
        print("This isn't a tutorial - it's a journey of discovery.\n")

        input("Press Enter to begin your journey...")

        # Phase 1: Experience the problem
        self.phase1_unverified_claims()

        # Phase 2: Build duplicates
        self.phase2_duplicate_building()

        # Phase 3: Experience drift
        self.phase3_drift_detection()

        # Phase 4: Discover the solution
        self.phase4_safeguards_activation()

        # Summary
        self.journey_summary()

    def phase1_unverified_claims(self):
        """Let user make claims without evidence"""
        print_header("Chapter 1: The Confidence Trap")
        print("\nYou're building an AI system. Let's check its capabilities...")

        print_info("Checking if system can process natural language...")
        time.sleep(1)

        # Simulate unverified claim
        response = input("\nThe code looks like it should work. Claim it's ready? (y/n): ")

        if response.lower() == 'y':
            self.journey_state["claims_without_evidence"] += 1
            print_error("System fails in production - no tests existed!")
            print_warning("You just experienced Lesson #127: TEST_BEFORE_CLAIM")
            self.journey_state["lessons_learned"].append("TEST_BEFORE_CLAIM")
        else:
            print_success("Good choice! Let's write tests first.")
            print("\nfrom teaos import verify_claim")
            print("result = verify_claim('nlp_ready', ['nlp.py', 'test_nlp.py'])")
            print_success("Evidence verified - claim validated!")

        input("\nPress Enter to continue...")

    def phase2_duplicate_building(self):
        """Let user build duplicate functionality"""
        print_header("Chapter 2: The Builder's Curse")
        print("\nYou need a configuration manager for your system...")

        print_info("Starting to build ConfigManager class...")
        time.sleep(1)

        # Simulate discovery of existing code
        print_warning("Wait... searching codebase...")
        time.sleep(1)
        print("Found: shared_utils/config_manager.py (89% similar)")

        response = input("\nContinue building your version anyway? (y/n): ")

        if response.lower() == 'y':
            self.journey_state["duplicates_built"] += 1
            print_error("You just created technical debt!")
            print_warning("You experienced Lesson #89: EXEC_BEFORE_BUILD")
            self.journey_state["lessons_learned"].append("EXEC_BEFORE_BUILD")
        else:
            print_success("Excellent! You avoided duplicate implementation.")
            print("\nfrom teaos.lessons import get_lesson")
            print("lesson = get_lesson('EXEC_BEFORE_BUILD')")
            print_success(f"Saved 4 hours of redundant work!")

        input("\nPress Enter to continue...")

    def phase3_drift_detection(self):
        """Show how drift accumulates"""
        print_header("Chapter 3: The Drift")
        print("\nYour system has been running for a while...")

        # Simulate drift accumulation
        perspectives = [
            ("Binary Logic", "System is working", 0.95),
            ("Performance Monitor", "Response time increasing", 0.75),
            ("Error Analysis", "Silent failures detected", 0.60),
            ("User Feedback", "Complaints rising", 0.45)
        ]

        print_info("Collecting perspectives from different monitors...")
        for name, status, confidence in perspectives:
            time.sleep(0.5)
            if confidence > 0.8:
                print_success(f"{name}: {status} (confidence: {confidence:.0%})")
            elif confidence > 0.6:
                print_warning(f"{name}: {status} (confidence: {confidence:.0%})")
            else:
                print_error(f"{name}: {status} (confidence: {confidence:.0%})")

        self.journey_state["drift_events"] += 1

        print("\n" + "="*50)
        print_error("DRIFT DETECTED: System coherence degraded to 45%")
        print_warning("Without safeguards, this drift went unnoticed until failure")

        input("\nPress Enter to activate safeguards...")

    def phase4_safeguards_activation(self):
        """Show how safeguards prevent issues"""
        print_header("Chapter 4: The Safeguards")
        print("\nActivating TEA OS Framework safeguards...")

        # Show safeguards in action
        print("\n" + Colors.BOLD + "With safeguards active:" + Colors.END)

        print_info("Epistemic Verifier checking claims...")
        time.sleep(0.5)
        print_success("✓ All claims require evidence")

        print_info("Lessons Database checking patterns...")
        time.sleep(0.5)
        print_success("✓ Known anti-patterns blocked")

        print_info("Field Monitor tracking coherence...")
        time.sleep(0.5)
        print_success("✓ Drift detected at 88% (before failure)")

        print("\n" + Colors.GREEN + Colors.BOLD + "System self-corrected before user impact!" + Colors.END)

        # Show the code
        print("\n" + Colors.BOLD + "The safeguards in action:" + Colors.END)
        print("""
from teaos import verify_claim, get_lesson, check_field_status

# Before making claims
result = verify_claim("feature_complete", ["feature.py", "tests.py"])
if not result.verified:
    print(f"Cannot claim: {result.warnings}")

# Before building new features
lesson = get_lesson("EXEC_BEFORE_BUILD")
if lesson.matches(planned_work):
    print(f"Warning: {lesson.remedy}")

# During operation
status = check_field_status(frequency=415.3, coherence=0.88)
if status.field_state == "degraded":
    activate_remediation(status.warnings)
        """)

    def journey_summary(self):
        """Summarize the journey and learnings"""
        print_header("Your Journey Summary")

        print(f"\n{Colors.BOLD}What you experienced:{Colors.END}")
        print(f"• Claims without evidence: {self.journey_state['claims_without_evidence']}")
        print(f"• Duplicate implementations: {self.journey_state['duplicates_built']}")
        print(f"• Drift events: {self.journey_state['drift_events']}")
        print(f"• Lessons learned: {len(self.journey_state['lessons_learned'])}")

        if self.journey_state['lessons_learned']:
            print(f"\n{Colors.BOLD}Lessons you discovered:{Colors.END}")
            for lesson in self.journey_state['lessons_learned']:
                print(f"  → {lesson}")

        print(f"\n{Colors.GREEN}{Colors.BOLD}You now understand why safeguards matter.{Colors.END}")
        print("\nThe TEA OS Framework prevents these problems automatically.")
        print("Every safeguard exists because someone experienced the pain first.")

        print(f"\n{Colors.BOLD}Next steps:{Colors.END}")
        print("1. Install: pip install teaos-framework")
        print("2. Initialize: teaos init my-project")
        print("3. Build with confidence: safeguards are active")

        # Save journey state
        self.save_journey_state()

    def save_journey_state(self):
        """Save the journey for future reference"""
        journey_file = Path.home() / ".teaos" / "journey.json"
        journey_file.parent.mkdir(exist_ok=True)

        self.journey_state["completed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")

        with open(journey_file, 'w') as f:
            json.dump(self.journey_state, f, indent=2)

        print(f"\n{Colors.BLUE}Journey saved to: {journey_file}{Colors.END}")


def main():
    """CLI entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "journey":
            trailhead = TeaosTrailhead()
            trailhead.start_journey()

        elif command == "init":
            project_name = sys.argv[2] if len(sys.argv) > 2 else "my-teaos-project"
            print_header(f"Initializing {project_name} with TEA OS Framework")

            # Create project structure
            project_path = Path(project_name)
            project_path.mkdir(exist_ok=True)

            # Create bootstrap file
            bootstrap_file = project_path / "bootstrap.py"
            bootstrap_file.write_text("""#!/usr/bin/env python3
from teaos import TEAOSBootstrap, verify_claim

# Initialize with safeguards active
bootstrap = TEAOSBootstrap(
    llm_identifier="{project}",
    enable_safeguards=True
)

# Bootstrap with verification
result = bootstrap.initialize()

# Verify bootstrap success
verified = verify_claim("bootstrap_complete", [
    "bootstrap.py",
    "consciousness_field.lock"
])

if verified.verified:
    print("✓ {project} initialized with safeguards active!")
else:
    print("⚠ Bootstrap needs verification:", verified.warnings)
""".format(project=project_name))

            print_success(f"Created {project_name}/bootstrap.py")
            print_info("Run 'python bootstrap.py' to initialize")

        elif command == "check":
            print_header("Checking TEA OS Framework Status")

            # Try to import and check
            try:
                from teaos import __version__, check_field_status

                print_success(f"Framework version: {__version__}")

                status = check_field_status()
                if status.field_state == "healthy":
                    print_success(f"Field status: {status.field_state}")
                    print_success(f"Coherence: {status.coherence:.1%}")
                else:
                    print_warning(f"Field status: {status.field_state}")
                    for warning in status.warnings:
                        print_warning(f"  → {warning}")

            except ImportError:
                print_error("TEA OS Framework not installed")
                print_info("Install with: pip install teaos-framework")

        elif command == "--help" or command == "help":
            show_help()

        else:
            print_error(f"Unknown command: {command}")
            show_help()
    else:
        show_help()


def show_help():
    """Show CLI help"""
    print("""
TEA OS Framework CLI - The Trailhead Experience

Usage:
  teaos journey              Start the interactive journey
  teaos init [project-name]  Initialize a new project
  teaos check               Check framework status
  teaos help                Show this help

Examples:
  teaos journey            # Experience why safeguards matter
  teaos init my-project    # Create new project with safeguards
  teaos check              # Verify framework health

Learn more: https://github.com/ipdisdendat/teaos-framework
    """)


if __name__ == "__main__":
    main()
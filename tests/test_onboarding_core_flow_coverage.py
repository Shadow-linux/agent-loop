from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from tests.checker_test_support import ROOT, combined_output, run_checker


SCRIPT = "scripts/check-onboarding-core-flow-coverage.py"
EXAMPLE = ROOT / "examples/ai-meeting-minutes-backend/onboarding-db"
FIXTURES = ROOT / "tests/fixtures/onboarding-core-flow"


class OnboardingCoreFlowCoverageTests(unittest.TestCase):
    def assert_passes(self, root: Path, expected: str) -> None:
        result = run_checker(SCRIPT, str(root))
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn(expected, result.stdout)

    def assert_fails(self, root: Path, expected: str) -> None:
        result = run_checker(SCRIPT, str(root))
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn(expected, combined_output(result))

    def test_planned_example_passes(self) -> None:
        self.assert_passes(EXAMPLE, "1 planned, 0 deferred")

    def test_reasoned_deferred_flow_passes(self) -> None:
        self.assert_passes(FIXTURES / "valid-deferred", "0 planned, 1 deferred")

    def test_missing_recovery_slice_fails(self) -> None:
        self.assert_fails(
            FIXTURES / "invalid-missing-recovery",
            "missing required slice: CF-ORDER-PAYMENT/S07",
        )

    def test_detached_diagram_trace_fails(self) -> None:
        self.assert_fails(
            FIXTURES / "invalid-detached-trace",
            "missing diagram definition: D-RECOVERY",
        )

    def test_bom_and_crlf_are_supported(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "onboarding-db"
            shutil.copytree(EXAMPLE, copied)
            for path in copied.rglob("*.md"):
                text = path.read_text(encoding="utf-8")
                path.write_bytes(("\ufeff" + text.replace("\n", "\r\n")).encode("utf-8"))
            self.assert_passes(copied, "1 planned, 0 deferred")


if __name__ == "__main__":
    unittest.main()

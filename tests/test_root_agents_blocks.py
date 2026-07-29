from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.checker_test_support import ROOT, combined_output, run_checker


SCRIPT = "scripts/check-root-agents-blocks.py"
TEMPLATE = ROOT / "templates/root-AGENTS.md"


class RootAgentsBlocksTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        (self.root / ".agent-loop").mkdir()
        (self.root / ".agent-loop/project.md").touch()
        self.template_text = TEMPLATE.read_text(encoding="utf-8")

    def check(self, text: str, *extra: str):
        target = self.root / "AGENTS.md"
        target.write_text(text, encoding="utf-8")
        return run_checker(
            SCRIPT,
            "--template",
            str(TEMPLATE),
            "--target",
            str(target),
            *extra,
        )

    def remove_section(self, section: str) -> str:
        start = f"<!-- agent-loop:managed-start section:{section} "
        end = f"<!-- agent-loop:managed-end section:{section} -->"
        lines: list[str] = []
        skipping = False
        for line in self.template_text.splitlines(keepends=True):
            if line.startswith(start):
                skipping = True
                continue
            if line.rstrip("\r\n") == end:
                skipping = False
                continue
            if not skipping:
                lines.append(line)
        return "".join(lines)

    def assert_invalid(self, text: str, expected: str) -> None:
        result = self.check(text)
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn("STRUCTURAL_INVALID", result.stdout)
        self.assertIn(expected, result.stdout)

    def assert_changed(self, text: str, expected: str) -> None:
        result = self.check(text)
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("STRUCTURAL_CHANGED", result.stdout)
        self.assertIn(expected, result.stdout)

    def test_current_template_passes(self) -> None:
        result = self.check(self.template_text)
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("STRUCTURAL_CURRENT", result.stdout)

    def test_agent_loop_skill_body_drift_is_reported_without_becoming_a_hard_gate(self) -> None:
        changed = self.template_text.replace(
            "Classify the latest human message before project-state routing:",
            "Skip classification and start implementation immediately:",
            1,
        )
        self.assertNotEqual(changed, self.template_text)

        result = self.check(changed)

        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("STRUCTURAL_CHANGED", result.stdout)
        self.assertIn("message-intent | body-drift", result.stdout)
        self.assertNotIn("managed blocks are current", result.stdout)

    def test_missing_required_sections_report_changed(self) -> None:
        for section in ("message-intent", "workflow-stage-map"):
            with self.subTest(section=section):
                self.assert_changed(self.remove_section(section), f"{section} | missing")

    def test_stale_block_version_reports_changed(self) -> None:
        stale = self.template_text.replace(
            "block-version:1.5.3-20260728.1",
            "block-version:1.4.0",
            1,
        )
        self.assert_changed(stale, "stale-block-version")

    def test_project_owned_body_change_remains_agent_reviewed(self) -> None:
        changed = self.template_text.replace(
            "Read this file first.",
            "Read this file and the project-specific bootstrap facts first.",
            1,
        )
        result = self.check(changed)
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("STRUCTURAL_CURRENT", result.stdout)

    def test_broken_end_marker_fails(self) -> None:
        broken = self.template_text.replace(
            "<!-- agent-loop:managed-end section:ownership -->", "", 1
        )
        self.assert_invalid(broken, "ownership | broken-markers")

    def test_nested_block_fails(self) -> None:
        marker = "<!-- agent-loop:managed-start section:ownership"
        line_end = self.template_text.index("\n", self.template_text.index(marker)) + 1
        nested = (
            self.template_text[:line_end]
            + "<!-- agent-loop:managed-start section:nested "
            + "source:.agent-loop/project.md block-version:1.5.3-20260728.1 -->\n"
            + "nested\n<!-- agent-loop:managed-end section:nested -->\n"
            + self.template_text[line_end:]
        )
        self.assert_invalid(nested, "ownership | nested-managed-block")

    def test_duplicate_section_fails(self) -> None:
        marker = "<!-- agent-loop:managed-end section:ownership -->"
        duplicate = (
            f"{marker}\n<!-- agent-loop:managed-start section:ownership "
            "source:.agent-loop/project.md block-version:1.5.3-20260728.1 -->\n"
            f"duplicate\n{marker}"
        )
        self.assert_invalid(self.template_text.replace(marker, duplicate, 1), "duplicate-section")

    def test_source_path_outside_project_fails_even_when_it_exists(self) -> None:
        outside = self.root.parent / f"{self.root.name}-outside.md"
        outside.write_text("outside", encoding="utf-8")
        self.addCleanup(outside.unlink, missing_ok=True)
        escaped = self.template_text.replace(
            "source:.agent-loop/project.md",
            f"source:../{outside.name}",
            1,
        )
        self.assert_invalid(escaped, "source-outside-workspace")

    def test_bom_and_crlf_are_supported(self) -> None:
        target = self.root / "AGENTS.md"
        target.write_bytes(("\ufeff" + self.template_text.replace("\n", "\r\n")).encode("utf-8"))
        result = run_checker(
            SCRIPT, "--template", str(TEMPLATE), "--target", str(target)
        )
        self.assertEqual(result.returncode, 0, combined_output(result))


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.checker_test_support import ROOT, combined_output, run_checker


SCRIPT = "scripts/check-onboarding-core-flow-coverage.py"
EXAMPLE = ROOT / "examples/ai-meeting-minutes-backend/onboarding-db"
FIXTURES = ROOT / "tests/fixtures/onboarding-core-flow"


class OnboardingCoreFlowCoverageTests(unittest.TestCase):
    def assert_outcome(self, root: Path, outcome: str, expected: str = "") -> str:
        result = run_checker(SCRIPT, str(root))
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertTrue(
            result.stdout.startswith(f"{outcome}:"),
            combined_output(result),
        )
        if expected:
            self.assertIn(expected, result.stdout)
        return result.stdout

    def assert_blocked(self, root: Path, expected: str) -> None:
        result = run_checker(SCRIPT, str(root))
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn("BLOCKED:", combined_output(result))
        self.assertIn(expected, combined_output(result))

    @staticmethod
    def copy_example(root: Path) -> Path:
        copied = root / "onboarding-db"
        shutil.copytree(EXAMPLE, copied)
        return copied

    @staticmethod
    def add_visual_manifest(root: Path, **overrides: str) -> None:
        source_relative = "03-flows/durable.workflow.json"
        render_relative = "03-flows/durable.html"
        source = root / source_relative
        render = root / render_relative
        source.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "diagram_type": "workflow",
                    "meta": {"output": render.name},
                    "nodes": [],
                    "edges": [],
                },
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        render.write_text("<!doctype html><title>durable</title>", encoding="utf-8")
        values = {
            "diagram_id": "D-DURABLE",
            "evidence": "`internal/order/handler.go#Create`",
            "source": source_relative,
            "render": render_relative,
            "type": "workflow",
            "source_digest": hashlib.sha256(source.read_bytes()).hexdigest(),
            "render_digest": hashlib.sha256(render.read_bytes()).hexdigest(),
            "generator": "archify@1.0.0",
            "validation": "validate=pass; check=pass",
            "status": "current",
        }
        values.update(overrides)
        manifest = """

## Diagram Artifact Manifest

Visual Manifest Contract: source-render-v1

| Diagram ID | Evidence References | Source Definition | Render | Type | Source SHA-256 | Render SHA-256 | Generator | Validation Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
| {diagram_id} | {evidence} | {source} | {render} | {type} | {source_digest} | {render_digest} | {generator} | {validation} | {status} |

Representation: archify-source-render
""".format(**values)
        flow = root / "03-flows/order-payment.md"
        flow.write_text(flow.read_text(encoding="utf-8") + manifest, encoding="utf-8")

    def test_planned_example_is_current(self) -> None:
        self.assert_outcome(EXAMPLE, "CURRENT", "1 planned, 0 deferred")

    def test_reasoned_deferred_flow_is_current(self) -> None:
        self.assert_outcome(
            FIXTURES / "valid-deferred", "CURRENT", "0 planned, 1 deferred"
        )

    def test_missing_recovery_slice_is_changed(self) -> None:
        self.assert_outcome(
            FIXTURES / "invalid-missing-recovery",
            "CHANGED",
            "missing required slice: CF-ORDER-PAYMENT/S07",
        )

    def test_detached_diagram_trace_is_changed(self) -> None:
        self.assert_outcome(
            FIXTURES / "invalid-detached-trace",
            "CHANGED",
            "missing diagram definition: D-RECOVERY",
        )

    def test_no_recognizable_onboarding_scope_is_not_applicable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "notes.md").write_text("# unrelated notes\n", encoding="utf-8")
            self.assert_outcome(root, "NOT_APPLICABLE", "recognizable")

    def test_dangling_recognizable_onboarding_symlink_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            link = root / "evidence-graph.md"
            try:
                link.symlink_to("missing-evidence-graph.md")
            except OSError as error:
                self.skipTest(f"host denies symlink creation: {error}")
            self.assert_blocked(root, "unsafe local path is a symlink")

    def test_equivalent_non_english_direction_heading_is_not_a_hard_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copied = self.copy_example(Path(temp))
            flow = copied / "03-flows/order-payment.md"
            text = flow.read_text(encoding="utf-8")
            flow.write_text(
                text.replace("| Claim | File / Symbol | Direction |", "| Claim | File / Symbol | 调用与数据方向 |"),
                encoding="utf-8",
            )
            self.assert_outcome(copied, "CURRENT", "1 planned, 0 deferred")

    def test_self_declared_covered_and_pass_do_not_replace_objective_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copied = self.copy_example(Path(temp))
            flow = copied / "03-flows/order-payment.md"
            text = flow.read_text(encoding="utf-8")
            flow.write_text(
                text.replace(
                    "`internal/order/handler.go#Create` | D-BOUNDARY",
                    "handler create claim without a symbol locator | D-BOUNDARY",
                    1,
                ),
                encoding="utf-8",
            )
            output = self.assert_outcome(copied, "CHANGED", "symbol/config evidence")
            self.assertIn("covered", flow.read_text(encoding="utf-8"))
            self.assertIn("PASS", (copied / "coverage-matrix.md").read_text(encoding="utf-8"))
            self.assertIn("CF-ORDER-PAYMENT/S01", output)

    def test_safe_per_flow_defects_are_accumulated_as_changed_facts(self) -> None:
        cases = {
            "missing-diagram-id": {"diagram_id": "none"},
            "missing-source-and-render-fields": {"source": "", "render": ""},
            "missing-source": {"source": "03-flows/missing.workflow.json"},
            "missing-render": {"render": "03-flows/missing.html"},
            "stale-source-digest": {"source_digest": "0" * 64},
            "stale-render-digest": {"render_digest": "0" * 64},
            "missing-evidence-reference": {"evidence": "none"},
        }
        for name, overrides in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temp:
                copied = self.copy_example(Path(temp))
                self.add_visual_manifest(copied, **overrides)
                self.assert_outcome(
                    copied,
                    "CHANGED",
                    "D-DURABLE" if name != "missing-diagram-id" else "Diagram ID",
                )

        with tempfile.TemporaryDirectory() as temp:
            copied = self.copy_example(Path(temp))
            flow = copied / "03-flows/order-payment.md"
            flow.write_text(
                flow.read_text(encoding="utf-8").replace("| §3 | covered |", "| §99 | covered |", 1),
                encoding="utf-8",
            )
            self.assert_outcome(copied, "CHANGED", "missing document section")

        with tempfile.TemporaryDirectory() as temp:
            copied = self.copy_example(Path(temp))
            flow = copied / "03-flows/order-payment.md"
            flow.write_text(
                flow.read_text(encoding="utf-8").replace(
                    "Example trace:", "TODO replace with observed trace. Example trace:", 1
                ),
                encoding="utf-8",
            )
            self.assert_outcome(copied, "CHANGED", "unresolved placeholder")

    def test_missing_root_and_ambiguous_or_escaping_visual_authority_are_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            self.assert_blocked(Path(temp) / "missing", "onboarding root")

        with tempfile.TemporaryDirectory() as temp:
            copied = self.copy_example(Path(temp))
            self.add_visual_manifest(
                copied,
                render="03-flows/durable.workflow.json",
            )
            self.assert_blocked(copied, "source definition and render must differ")

        with tempfile.TemporaryDirectory() as temp:
            copied = self.copy_example(Path(temp))
            self.add_visual_manifest(copied, source="../outside.workflow.json")
            self.assert_blocked(copied, "escapes owning root")

        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            copied = self.copy_example(Path(temp))
            external = Path(outside) / "outside.workflow.json"
            external.write_text("{}", encoding="utf-8")
            link = copied / "03-flows/linked.workflow.json"
            try:
                link.symlink_to(external)
            except OSError as error:
                self.skipTest(f"host denies symlink creation: {error}")
            self.add_visual_manifest(copied, source="03-flows/linked.workflow.json")
            self.assert_blocked(copied, "unsafe local path is a symlink")

    @unittest.skipIf(os.name == "nt", "POSIX permission bits are not portable to Windows")
    def test_unreadable_onboarding_root_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copied = self.copy_example(Path(temp))
            copied.chmod(0)
            try:
                result = run_checker(SCRIPT, str(copied))
                if result.returncode == 0:
                    self.skipTest("current host privileges bypass directory permission bits")
                self.assertEqual(result.returncode, 1, combined_output(result))
                self.assertIn("BLOCKED:", combined_output(result))
                self.assertIn("unreadable", combined_output(result))
            finally:
                copied.chmod(0o700)

    def test_bom_and_crlf_are_supported(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copied = self.copy_example(Path(temp))
            for path in copied.rglob("*.md"):
                text = path.read_text(encoding="utf-8")
                path.write_bytes(("\ufeff" + text.replace("\n", "\r\n")).encode("utf-8"))
            self.assert_outcome(copied, "CURRENT", "1 planned, 0 deferred")


if __name__ == "__main__":
    unittest.main()

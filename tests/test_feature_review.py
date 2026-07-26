from __future__ import annotations

import hashlib
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check-feature-review.py"


def _projection_lines(name: str, text: str) -> list[str]:
    lines = text.splitlines()
    section = ""
    in_task = False
    projected: list[str] = []
    for line in lines:
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            section = heading.group(1)
            in_task = False

        if re.match(r"^(Updated|Status):\s*", line) and not section:
            line = re.sub(r":.*$", ": <runtime>", line)

        if name == "tasks.md":
            task = re.match(r"^(\s*-\s*)\[[ xX]\](\s+T\d+\b.*)$", line)
            if task:
                line = f"{task.group(1)}[ ]{task.group(2)}"
                in_task = True
            elif in_task and re.match(r"^\s+-\s+(Status|Review|Drift):\s*", line):
                line = re.sub(r":.*$", ": <runtime>", line)
        elif name.startswith("tasks/"):
            if section == "Task Done Gate":
                line = re.sub(r"^(\s*-\s*)\[[ xX]\]", r"\1[ ]", line)
                if re.match(r"^(Evidence|Review|Drift):\s*", line):
                    line = re.sub(r":.*$", ": <runtime>", line)
        elif name == "tests.md":
            if line.startswith("|") and not re.match(r"^\|[-| :]+\|$", line):
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                if section == "Design Slice Verification Matrix" and len(cells) == 4 and cells[0] != "Design Slice ID":
                    cells[-1] = "<runtime>"
                    line = "| " + " | ".join(cells) + " |"
                elif section == "Bug Verification Matrix" and len(cells) == 6 and cells[0] != "Bug ID":
                    cells[-2:] = ["<runtime>", "<runtime>"]
                    line = "| " + " | ".join(cells) + " |"
        projected.append(line)
    return projected


def digest(feature: Path, names: list[str], algorithm: str = "raw-v1") -> str:
    rows = []
    for name in sorted(names):
        path = feature / name
        if algorithm == "review-definition-v2" and (
            name == "tasks.md"
            or name == "tests.md"
            or name.startswith("tasks/")
            or name.startswith("tests/")
        ):
            projected = "\n".join(_projection_lines(name, path.read_text(encoding="utf-8-sig"))) + "\n"
            payload = projected.encode("utf-8")
        else:
            payload = path.read_bytes()
        value = hashlib.sha256(payload).hexdigest()
        rows.append(f"{name}\tsha256:{value}")
    return "sha256:" + hashlib.sha256(("\n".join(rows) + "\n").encode()).hexdigest()


class FeatureReviewCheckerTests(unittest.TestCase):
    def make_feature(
        self,
        *,
        decision: str = "package-only",
        auto_loop: str = "disabled",
        tasks: str = "T001,T002",
        active_plan: str = "T001",
        plan_evidence: str = "plan.md",
        stable_algorithm: str = "raw-v1",
    ) -> Path:
        root = Path(tempfile.mkdtemp()) / "feature"
        root.mkdir()
        (root / "spec.md").write_text("# Spec\n\nSlice: S1\n", encoding="utf-8")
        (root / "tasks.md").write_text(
            "# Tasks\n\nUpdated: 2026-07-27\nStatus: active\n\n"
            "- [ ] T001 [US1] First task\n"
            "  - Status: todo\n"
            "  - Mode: Agent-ready\n"
            "  - Review: pending\n"
            "  - Drift: pending\n"
            "- [ ] T002 [US1] Second task\n"
            "  - Status: todo\n"
            "  - Mode: Agent-ready\n"
            "  - Depends on: T000\n"
            "  - Human Gate: none\n"
            "  - Acceptance: second behavior\n"
            "  - Verification: python3 -m unittest\n"
            "  - Review: pending\n"
            "  - Drift: pending\n",
            encoding="utf-8",
        )
        (root / "tests.md").write_text("# Tests\n\n- T001 test\n- T002 test\n", encoding="utf-8")
        package_files = ["spec.md", "tasks.md", "tests.md"]
        if plan_evidence == "plan.md":
            (root / "plan.md").write_text(
                f"# Plan\n\nPlan Scope:\n- Type: task\n- ID: {active_plan}\n",
                encoding="utf-8",
            )
            package_files.append("plan.md")
        stable_files = ["spec.md", "tasks.md", "tests.md"]
        spec_digest = "sha256:" + hashlib.sha256((root / "spec.md").read_bytes()).hexdigest()
        (root / "notes.md").write_text(
            "\n".join(
                [
                    "# Notes",
                    "Implementation Readiness: accepted",
                    "Gate 1 Decision: accepted",
                    f"Gate 1 Spec Digest: {spec_digest}",
                    f"Gate 2 Decision: {decision}",
                    f"Gate 2 Package Files: {','.join(package_files)}",
                    f"Gate 2 Package Digest: {digest(root, package_files)}",
                    f"Gate 2 Stable Files: {','.join(stable_files)}",
                    f"Gate 2 Stable Digest Algorithm: {stable_algorithm}",
                    f"Gate 2 Stable Digest: {digest(root, stable_files, stable_algorithm)}",
                    f"Gate 2 Agent-ready Tasks: {tasks}",
                    f"Active Plan Scope: {active_plan}",
                    f"Gate 2 Plan Evidence: {plan_evidence}",
                    f"Feature Auto-Loop: {auto_loop}",
                    "Gate 2 Reviewed At: 2026-07-25T12:00:00+08:00",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return root

    @staticmethod
    def replace_note_field(feature: Path, name: str, value: str) -> None:
        notes_path = feature / "notes.md"
        notes = notes_path.read_text(encoding="utf-8")
        notes = re.sub(rf"^{re.escape(name)}:.*$", f"{name}: {value}", notes, flags=re.MULTILINE)
        notes_path.write_text(notes, encoding="utf-8")

    def add_stable_file(self, feature: Path, name: str, content: str) -> None:
        path = feature / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        notes = (feature / "notes.md").read_text(encoding="utf-8")
        package_files = parse_note_list(notes, "Gate 2 Package Files") + [name]
        stable_files = parse_note_list(notes, "Gate 2 Stable Files") + [name]
        algorithm = parse_note_value(notes, "Gate 2 Stable Digest Algorithm")
        self.replace_note_field(feature, "Gate 2 Package Files", ",".join(package_files))
        self.replace_note_field(feature, "Gate 2 Stable Files", ",".join(stable_files))
        self.replace_note_field(feature, "Gate 2 Package Digest", digest(feature, package_files))
        self.replace_note_field(
            feature,
            "Gate 2 Stable Digest",
            digest(feature, stable_files, algorithm),
        )

    def run_checker(self, feature: Path, mode: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(CHECKER), "--mode", mode, str(feature)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_package_only_is_review_valid_but_does_not_enable_execution(self) -> None:
        feature = self.make_feature()
        self.assertEqual(self.run_checker(feature, "review").returncode, 0)
        result = self.run_checker(feature, "execute")
        self.assertEqual(result.returncode, 1)
        self.assertIn("approve-and-start", result.stdout)

    def test_package_only_start_requires_unchanged_full_package(self) -> None:
        feature = self.make_feature()
        self.assertEqual(self.run_checker(feature, "start").returncode, 0)
        (feature / "plan.md").write_text("# Plan\n\nTask: T001\nchanged\n", encoding="utf-8")
        result = self.run_checker(feature, "start")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Gate 2 Package Digest", result.stdout)

    def test_package_only_start_rejects_omitted_complex_detail(self) -> None:
        feature = self.make_feature()
        (feature / "plans").mkdir()
        (feature / "plans" / "T001.md").write_text(
            "# Detailed Plan\n\nPlan Scope:\n- Type: task\n- ID: T001\n",
            encoding="utf-8",
        )
        result = self.run_checker(feature, "start")
        self.assertEqual(result.returncode, 1)
        self.assertIn("plans/T001.md", result.stdout)

    def test_later_start_mode_requires_package_only_baseline(self) -> None:
        feature = self.make_feature(decision="approve-and-start", auto_loop="enabled")
        result = self.run_checker(feature, "start")
        self.assertEqual(result.returncode, 1)
        self.assertIn("package-only", result.stdout)

    def test_approve_and_start_requires_enabled_auto_loop(self) -> None:
        feature = self.make_feature(decision="approve-and-start", auto_loop="disabled")
        result = self.run_checker(feature, "execute")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Feature Auto-Loop", result.stdout)

    def test_execute_allows_plan_rotation_inside_accepted_task_set(self) -> None:
        feature = self.make_feature(decision="approve-and-start", auto_loop="enabled")
        (feature / "plan.md").write_text(
            "# Plan\n\nPlan Scope:\n- Type: task\n- ID: T002\n", encoding="utf-8"
        )
        notes = (feature / "notes.md").read_text(encoding="utf-8")
        (feature / "notes.md").write_text(
            notes.replace("Active Plan Scope: T001", "Active Plan Scope: T002"),
            encoding="utf-8",
        )
        self.assertEqual(self.run_checker(feature, "execute").returncode, 0)

    def test_execute_rejects_plan_file_scope_mismatch(self) -> None:
        feature = self.make_feature(decision="approve-and-start", auto_loop="enabled")
        notes = (feature / "notes.md").read_text(encoding="utf-8")
        (feature / "notes.md").write_text(
            notes.replace("Active Plan Scope: T001", "Active Plan Scope: T002"),
            encoding="utf-8",
        )
        result = self.run_checker(feature, "execute")
        self.assertEqual(result.returncode, 1)
        self.assertIn("plan.md scope", result.stdout)

    def test_execute_allows_new_plan_detail_for_an_accepted_task(self) -> None:
        feature = self.make_feature(decision="approve-and-start", auto_loop="enabled")
        (feature / "plans").mkdir()
        (feature / "plans" / "T002.md").write_text(
            "# Detailed Plan\n\nPlan Scope:\n- Type: task\n- ID: T002\n",
            encoding="utf-8",
        )
        notes = (feature / "notes.md").read_text(encoding="utf-8")
        notes = notes.replace("Active Plan Scope: T001", "Active Plan Scope: T002")
        notes = notes.replace(
            "Gate 2 Plan Evidence: plan.md",
            "Gate 2 Plan Evidence: plans/T002.md",
        )
        (feature / "notes.md").write_text(notes, encoding="utf-8")
        self.assertEqual(self.run_checker(feature, "execute").returncode, 0)

    def test_execute_rejects_plan_rotation_outside_accepted_task_set(self) -> None:
        feature = self.make_feature(decision="approve-and-start", auto_loop="enabled")
        notes = (feature / "notes.md").read_text(encoding="utf-8")
        (feature / "notes.md").write_text(
            notes.replace("Active Plan Scope: T001", "Active Plan Scope: T999"),
            encoding="utf-8",
        )
        result = self.run_checker(feature, "execute")
        self.assertEqual(result.returncode, 1)
        self.assertIn("accepted Agent-ready task set", result.stdout)

    def test_story_plan_may_cover_only_accepted_agent_ready_tasks(self) -> None:
        feature = self.make_feature(
            decision="approve-and-start",
            auto_loop="enabled",
            active_plan="US1",
        )
        (feature / "plan.md").write_text(
            "# Plan\n\n"
            "Plan Scope:\n"
            "- Type: story\n"
            "- ID: US1\n"
            "- Included Tasks: T001, T002\n",
            encoding="utf-8",
        )
        package_files = ["spec.md", "tasks.md", "tests.md", "plan.md"]
        notes = (feature / "notes.md").read_text(encoding="utf-8")
        notes = notes.replace(
            next(
                line for line in notes.splitlines() if line.startswith("Gate 2 Package Digest:")
            ),
            f"Gate 2 Package Digest: {digest(feature, package_files)}",
        )
        (feature / "notes.md").write_text(notes, encoding="utf-8")
        self.assertEqual(self.run_checker(feature, "execute").returncode, 0)

        (feature / "plan.md").write_text(
            "# Plan\n\n"
            "Plan Scope:\n"
            "- Type: story\n"
            "- ID: US1\n"
            "- Included Tasks: T001, T999\n",
            encoding="utf-8",
        )
        result = self.run_checker(feature, "execute")
        self.assertEqual(result.returncode, 1)
        self.assertIn("T999", result.stdout)

        (feature / "plan.md").write_text(
            "# Plan\n\n"
            "Plan Scope:\n"
            "- Type: story\n"
            "- ID: US2\n"
            "- Included Tasks: T001, T002\n",
            encoding="utf-8",
        )
        notes = (feature / "notes.md").read_text(encoding="utf-8")
        (feature / "notes.md").write_text(
            notes.replace("Active Plan Scope: US1", "Active Plan Scope: US2"),
            encoding="utf-8",
        )
        result = self.run_checker(feature, "execute")
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not cover story US2", result.stdout)

    def test_execute_rejects_stable_artifact_drift(self) -> None:
        feature = self.make_feature(decision="approve-and-start", auto_loop="enabled")
        (feature / "tests.md").write_text("# Tests\nchanged\n", encoding="utf-8")
        result = self.run_checker(feature, "execute")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Gate 2 Stable Digest", result.stdout)

    def test_missing_durable_decision_fields_fail_closed(self) -> None:
        feature = self.make_feature()
        (feature / "notes.md").write_text(
            "# Notes\nImplementation Readiness: accepted\n", encoding="utf-8"
        )
        result = self.run_checker(feature, "review")
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing field", result.stdout)

    def test_pending_review_time_fails_closed(self) -> None:
        feature = self.make_feature()
        notes = (feature / "notes.md").read_text(encoding="utf-8")
        (feature / "notes.md").write_text(
            notes.replace(
                "Gate 2 Reviewed At: 2026-07-25T12:00:00+08:00",
                "Gate 2 Reviewed At: pending",
            ),
            encoding="utf-8",
        )
        result = self.run_checker(feature, "review")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Gate 2 Reviewed At", result.stdout)

    def test_stable_files_must_be_part_of_reviewed_package(self) -> None:
        feature = self.make_feature()
        (feature / "context.md").write_text("# Context\n", encoding="utf-8")
        notes = (feature / "notes.md").read_text(encoding="utf-8")
        stable_files = ["spec.md", "tasks.md", "tests.md", "context.md"]
        notes = notes.replace(
            "Gate 2 Stable Files: spec.md,tasks.md,tests.md",
            "Gate 2 Stable Files: spec.md,tasks.md,tests.md,context.md",
        )
        notes = notes.replace(
            next(
                line for line in notes.splitlines() if line.startswith("Gate 2 Stable Digest:")
            ),
            f"Gate 2 Stable Digest: {digest(feature, stable_files)}",
        )
        (feature / "notes.md").write_text(notes, encoding="utf-8")
        result = self.run_checker(feature, "review")
        self.assertEqual(result.returncode, 1)
        self.assertIn("subset", result.stdout)

    def test_accepted_task_must_exist_and_be_agent_ready(self) -> None:
        feature = self.make_feature(tasks="T001,T999")
        result = self.run_checker(feature, "review")
        self.assertEqual(result.returncode, 1)
        self.assertIn("T999", result.stdout)

        feature = self.make_feature()
        tasks = (feature / "tasks.md").read_text(encoding="utf-8")
        (feature / "tasks.md").write_text(
            tasks.replace(
                "- [ ] T002 [US1] Second task\n  - Status: todo\n  - Mode: Agent-ready",
                "- [ ] T002 [US1] Second task\n  - Status: todo\n  - Mode: Human-gated",
            ),
            encoding="utf-8",
        )
        result = self.run_checker(feature, "review")
        self.assertEqual(result.returncode, 1)
        self.assertIn("T002", result.stdout)
        self.assertIn("Agent-ready", result.stdout)

    def test_explicit_no_plan_evidence_is_supported(self) -> None:
        feature = self.make_feature(
            tasks="T001",
            active_plan="T001",
            plan_evidence="no-plan:T001",
        )
        self.assertEqual(self.run_checker(feature, "review").returncode, 0)

    def test_v2_allows_root_task_runtime_updates_and_plan_rotation(self) -> None:
        feature = self.make_feature(
            decision="approve-and-start",
            auto_loop="enabled",
            stable_algorithm="review-definition-v2",
        )
        tasks = (feature / "tasks.md").read_text(encoding="utf-8")
        tasks = tasks.replace("- [ ] T001", "- [x] T001")
        tasks = tasks.replace("Updated: 2026-07-27", "Updated: 2026-07-28")
        tasks = tasks.replace("Status: active", "Status: review", 1)
        tasks = tasks.replace("  - Status: todo", "  - Status: done", 1)
        tasks = tasks.replace("  - Review: pending", "  - Review: pass", 1)
        tasks = tasks.replace("  - Drift: pending", "  - Drift: no drift", 1)
        (feature / "tasks.md").write_text(tasks, encoding="utf-8")
        (feature / "plan.md").write_text(
            "# Plan\n\nPlan Scope:\n- Type: task\n- ID: T002\n", encoding="utf-8"
        )
        self.replace_note_field(feature, "Active Plan Scope", "T002")
        result = self.run_checker(feature, "execute")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_v2_allows_task_detail_done_gate_runtime_updates(self) -> None:
        feature = self.make_feature(
            decision="approve-and-start",
            auto_loop="enabled",
            stable_algorithm="review-definition-v2",
        )
        self.add_stable_file(
            feature,
            "tasks/T001.md",
            "# Task Detail: T001 First\n\n"
            "Task ID: T001\nStatus: todo\nUpdated: 2026-07-27\n\n"
            "## Acceptance\n\n- exact behavior\n\n"
            "## Task Done Gate\n\n"
            "- [ ] Implementation scope complete.\n"
            "- [ ] Required tests ran fresh.\n\n"
            "Evidence:\nReview:\nDrift:\n",
        )
        detail = (feature / "tasks/T001.md").read_text(encoding="utf-8")
        detail = detail.replace("Status: todo", "Status: done")
        detail = detail.replace("Updated: 2026-07-27", "Updated: 2026-07-28")
        detail = detail.replace("- [ ]", "- [x]")
        detail = detail.replace("Evidence:\nReview:\nDrift:", "Evidence: notes.md#t001\nReview: pass\nDrift: no drift")
        (feature / "tasks/T001.md").write_text(detail, encoding="utf-8")
        result = self.run_checker(feature, "execute")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_v2_allows_test_result_runtime_updates(self) -> None:
        feature = self.make_feature(
            decision="approve-and-start",
            auto_loop="enabled",
            stable_algorithm="review-definition-v2",
        )
        tests = (
            "# Test Design\n\nUpdated: 2026-07-27\nStatus: active\n\n"
            "## Design Slice Verification Matrix\n\n"
            "| Design Slice ID | Required Verification | Test / Evidence | Status |\n"
            "|---|---|---|---|\n"
            "| DS-01 | wallet is consistent | TC001 | planned |\n\n"
            "## Bug Verification Matrix\n\n"
            "| Bug ID | Expected Behavior Evidence | Original Reproduction | Regression / Safety Verification | Result | Evidence Link |\n"
            "|---|---|---|---|---|---|\n"
            "| BUG-001 | correct result | case | regression | planned | pending |\n\n"
            "## Test Commands\n\n`python3 -m unittest`\n"
        )
        (feature / "tests.md").write_text(tests, encoding="utf-8")
        stable = ["spec.md", "tasks.md", "tests.md"]
        package = stable + ["plan.md"]
        self.replace_note_field(feature, "Gate 2 Package Digest", digest(feature, package))
        self.replace_note_field(feature, "Gate 2 Stable Digest", digest(feature, stable, "review-definition-v2"))
        tests = tests.replace("Updated: 2026-07-27", "Updated: 2026-07-28")
        tests = tests.replace("| DS-01 | wallet is consistent | TC001 | planned |", "| DS-01 | wallet is consistent | TC001 | verified |")
        tests = tests.replace("| BUG-001 | correct result | case | regression | planned | pending |", "| BUG-001 | correct result | case | regression | pass | notes.md#bug |")
        (feature / "tests.md").write_text(tests, encoding="utf-8")
        result = self.run_checker(feature, "execute")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_v2_allows_test_detail_runtime_status_updates(self) -> None:
        feature = self.make_feature(
            decision="approve-and-start",
            auto_loop="enabled",
            stable_algorithm="review-definition-v2",
        )
        self.add_stable_file(
            feature,
            "tests/TC001.md",
            "# Test Case: TC001\n\nTest ID: TC001\nRelated Task: T001\n"
            "Status: active\nUpdated: 2026-07-27\n\n## Scenario\n\n"
            "Given: stable input\nWhen: command runs\nThen: exact output\n",
        )
        detail = (feature / "tests/TC001.md").read_text(encoding="utf-8")
        detail = detail.replace("Status: active", "Status: passing")
        detail = detail.replace("Updated: 2026-07-27", "Updated: 2026-07-28")
        (feature / "tests/TC001.md").write_text(detail, encoding="utf-8")
        result = self.run_checker(feature, "execute")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_v2_rejects_task_definition_drift(self) -> None:
        mutations = {
            "identity": ("T002", "T999"),
            "mode": ("Mode: Agent-ready", "Mode: Human-gated"),
            "mapping": ("[US1]", "[US9]"),
            "title": ("Second task", "Different task"),
            "dependency": ("Depends on: T000", "Depends on: T777"),
            "human-gate": ("Human Gate: none", "Human Gate: security review"),
            "acceptance": ("Acceptance: second behavior", "Acceptance: weaker behavior"),
            "verification": ("Verification: python3 -m unittest", "Verification: manual guess"),
        }
        for label, (old, new) in mutations.items():
            with self.subTest(label=label):
                feature = self.make_feature(
                    decision="approve-and-start",
                    auto_loop="enabled",
                    stable_algorithm="review-definition-v2",
                )
                tasks = (feature / "tasks.md").read_text(encoding="utf-8")
                (feature / "tasks.md").write_text(tasks.replace(old, new, 1), encoding="utf-8")
                result = self.run_checker(feature, "execute")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("Gate 2 Stable Digest", result.stdout)

    def test_v2_rejects_test_definition_drift(self) -> None:
        feature = self.make_feature(
            decision="approve-and-start",
            auto_loop="enabled",
            stable_algorithm="review-definition-v2",
        )
        tests = (feature / "tests.md").read_text(encoding="utf-8")
        (feature / "tests.md").write_text(
            tests.replace("T001 test", "T001 changed assertion"), encoding="utf-8"
        )
        result = self.run_checker(feature, "execute")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("Gate 2 Stable Digest", result.stdout)

    def test_v2_rejects_test_command_and_assertion_drift(self) -> None:
        for label, old, new in (
            ("command", "Command: python3 -m unittest", "Command: echo skip"),
            ("assertion", "Assertions: exact output", "Assertions: no error maybe"),
        ):
            with self.subTest(label=label):
                feature = self.make_feature(
                    decision="approve-and-start",
                    auto_loop="enabled",
                    stable_algorithm="review-definition-v2",
                )
                tests = (feature / "tests.md").read_text(encoding="utf-8")
                tests += "\n## Test Commands\n\nCommand: python3 -m unittest\nAssertions: exact output\n"
                (feature / "tests.md").write_text(tests, encoding="utf-8")
                package = ["spec.md", "tasks.md", "tests.md", "plan.md"]
                stable = ["spec.md", "tasks.md", "tests.md"]
                self.replace_note_field(feature, "Gate 2 Package Digest", digest(feature, package))
                self.replace_note_field(
                    feature,
                    "Gate 2 Stable Digest",
                    digest(feature, stable, "review-definition-v2"),
                )
                (feature / "tests.md").write_text(tests.replace(old, new), encoding="utf-8")
                result = self.run_checker(feature, "execute")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("Gate 2 Stable Digest", result.stdout)

    def test_v2_fails_closed_on_ambiguous_task_or_malformed_result_row(self) -> None:
        feature = self.make_feature(stable_algorithm="review-definition-v2")
        tasks = (feature / "tasks.md").read_text(encoding="utf-8")
        (feature / "tasks.md").write_text(
            tasks.replace("  - Review: pending", "  - Review: pending\n  - Review: pass", 1),
            encoding="utf-8",
        )
        result = self.run_checker(feature, "digest")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("ambiguous Stable Digest projection", result.stdout)

        feature = self.make_feature(stable_algorithm="review-definition-v2")
        (feature / "tests.md").write_text(
            "# Tests\n\n## Design Slice Verification Matrix\n\n"
            "| Design Slice ID | Required Verification | Test / Evidence | Status |\n"
            "|---|---|---|---|\n"
            "| DS-01 | missing result cell | TC001 |\n",
            encoding="utf-8",
        )
        result = self.run_checker(feature, "digest")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("malformed Design Slice Verification Matrix row", result.stdout)

    def test_missing_or_unknown_stable_algorithm_fails_closed(self) -> None:
        for value in (None, "review-definition-v99"):
            with self.subTest(value=value):
                feature = self.make_feature()
                notes = (feature / "notes.md").read_text(encoding="utf-8")
                if value is None:
                    notes = re.sub(r"^Gate 2 Stable Digest Algorithm:.*\n", "", notes, flags=re.MULTILINE)
                else:
                    notes = notes.replace("Gate 2 Stable Digest Algorithm: raw-v1", f"Gate 2 Stable Digest Algorithm: {value}")
                (feature / "notes.md").write_text(notes, encoding="utf-8")
                result = self.run_checker(feature, "review")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("Stable Digest Algorithm", result.stdout)

    def test_explicit_raw_v1_remains_compatible(self) -> None:
        feature = self.make_feature(stable_algorithm="raw-v1")
        self.assertEqual(self.run_checker(feature, "review").returncode, 0)

    def test_digest_mode_is_read_only_and_uses_v2_projection(self) -> None:
        feature = self.make_feature(stable_algorithm="review-definition-v2")
        before = {path.relative_to(feature): path.read_bytes() for path in feature.rglob("*") if path.is_file()}
        result = self.run_checker(feature, "digest")
        after = {path.relative_to(feature): path.read_bytes() for path in feature.rglob("*") if path.is_file()}
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(before, after)
        self.assertIn("Gate 2 Package Digest:", result.stdout)
        self.assertIn("Gate 2 Stable Digest Algorithm: review-definition-v2", result.stdout)
        self.assertIn("Gate 2 Stable Digest:", result.stdout)


def parse_note_value(notes: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}:\s*(.*?)\s*$", notes, flags=re.MULTILINE)
    if not match:
        raise AssertionError(f"missing note field: {name}")
    return match.group(1)


def parse_note_list(notes: str, name: str) -> list[str]:
    return [item.strip() for item in parse_note_value(notes, name).split(",") if item.strip()]


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check-feature-review.py"


def digest(feature: Path, names: list[str]) -> str:
    rows = []
    for name in sorted(names):
        value = hashlib.sha256((feature / name).read_bytes()).hexdigest()
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
    ) -> Path:
        root = Path(tempfile.mkdtemp()) / "feature"
        root.mkdir()
        (root / "spec.md").write_text("# Spec\n\nSlice: S1\n", encoding="utf-8")
        (root / "tasks.md").write_text(
            "# Tasks\n\n"
            "- [ ] T001 [US1] First task\n"
            "  - Mode: Agent-ready\n"
            "- [ ] T002 [US1] Second task\n"
            "  - Mode: Agent-ready\n",
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
                    f"Gate 2 Stable Digest: {digest(root, stable_files)}",
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
                "- [ ] T002 [US1] Second task\n  - Mode: Agent-ready",
                "- [ ] T002 [US1] Second task\n  - Mode: Human-gated",
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


if __name__ == "__main__":
    unittest.main()

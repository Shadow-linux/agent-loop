from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"

from tests.memory_reconciliation_test_support import (  # noqa: E402
    create_four_snapshot_workspace,
    run_memory_command,
    tree_snapshot,
)
from tests.test_memory_reconciliation_apply import (  # noqa: E402
    pending_transaction,
    run_apply,
)
from tests.test_memory_reconciliation_check import build_plan, set_inline_rewrite  # noqa: E402


def run_restore(workspace, report: Path, transaction_id: str):
    return run_memory_command(
        "restore-memory-reconciliation.py",
        "--project-root",
        str(workspace.project_root),
        "--report",
        str(report),
        "--transaction-id",
        transaction_id,
    )


def crash_after_write(workspace, plan, report):
    return run_apply(
        workspace,
        report,
        str(plan["plan_sha256"]),
        env={
            "AGENT_LOOP_TEST_FAILURE": "crash-after-write-1",
            "AGENT_LOOP_ALLOW_TEST_HOOKS": "1",
        },
    )


class MemoryReconciliationRestoreTests(unittest.TestCase):
    def make_crashed(self, temp: str, *, executable: bool = False):
        workspace = create_four_snapshot_workspace(Path(temp) / "repo")
        plan = build_plan(workspace)
        set_inline_rewrite(workspace, plan, content=b"post-crash\n")
        if executable:
            plan["operations"][0]["post_mode"] = "100755"  # type: ignore[index]
            from memory_reconciliation_support import canonical_plan_hash

            plan["plan_sha256"] = canonical_plan_hash(plan)
        report = workspace.render_report(plan)
        before = tree_snapshot(workspace.memory_root)
        result = crash_after_write(workspace, plan, report)
        self.assertEqual(result.returncode, 91, result.stderr)
        journal = pending_transaction(report)
        return workspace, plan, report, journal, before

    def test_interrupted_transaction_restores_in_new_process(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, _plan, report, journal, before = self.make_crashed(temp)
            result = run_restore(workspace, report, journal.parent.name)
            self.assertEqual(result.returncode, 0, result.stderr)
            after = tree_snapshot(workspace.memory_root)
            for path, digest in before.items():
                if ".memory-reconciliation-txn" not in path and path != report.relative_to(workspace.memory_root).as_posix():
                    self.assertEqual(after.get(path), digest, path)

    def test_restore_recovers_write_completed_before_completion_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, _plan, report, journal, _before = self.make_crashed(temp)
            data = json.loads(journal.read_text(encoding="utf-8"))
            self.assertEqual(data["completed_operations"], [])
            self.assertNotEqual(
                (workspace.memory_root / "project.md").read_text(encoding="utf-8"),
                "# Project\n\nStatus: base\nTarget Release Context: v1.4.0\n",
            )
            result = run_restore(workspace, report, journal.parent.name)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_restore_restores_deleted_file_and_mode(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = create_four_snapshot_workspace(Path(temp) / "repo")
            workspace.write(".agent-loop/project.md", "executable original\n", executable=True)
            self.assertEqual(workspace.git("add", ".agent-loop/project.md").returncode, 0)
            self.assertEqual(workspace.git("commit", "-q", "-m", "mode fixture").returncode, 0)
            workspace.merged_code_sha = workspace.git("rev-parse", "HEAD").stdout.strip()
            workspace.target_before_sha = workspace.merged_code_sha
            workspace.source_sha = workspace.merged_code_sha
            workspace.merge_base_sha = workspace.merged_code_sha
            plan = build_plan(workspace)
            from tests.test_memory_reconciliation_apply import remove_path

            remove_path(workspace, plan, "project.md")
            report = workspace.render_report(plan)
            result = run_apply(
                workspace,
                report,
                str(plan["plan_sha256"]),
                env={
                    "AGENT_LOOP_TEST_FAILURE": "crash-after-write-1",
                    "AGENT_LOOP_ALLOW_TEST_HOOKS": "1",
                },
            )
            self.assertEqual(result.returncode, 91)
            journal = pending_transaction(report)
            restored = run_restore(workspace, report, journal.parent.name)
            self.assertEqual(restored.returncode, 0, restored.stderr)
            self.assertEqual((workspace.memory_root / "project.md").read_bytes(), b"executable original\n")
            if os.name != "nt":
                self.assertTrue((workspace.memory_root / "project.md").stat().st_mode & 0o100)

    def test_restore_rejects_tampered_backup_before_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, _plan, report, journal, _before = self.make_crashed(temp)
            backup = next((journal.parent / "backups").glob("*.bin"))
            backup.write_bytes(b"tampered")
            current = (workspace.memory_root / "project.md").read_bytes()
            result = run_restore(workspace, report, journal.parent.name)
            self.assertEqual(result.returncode, 1)
            self.assertEqual((workspace.memory_root / "project.md").read_bytes(), current)
            self.assertTrue(journal.exists())

    def test_restore_rejects_journal_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, _plan, report, journal, _before = self.make_crashed(temp)
            data = json.loads(journal.read_text(encoding="utf-8"))
            data["operations"][0]["path"] = "../outside"
            journal.write_text(json.dumps(data, sort_keys=True), encoding="utf-8")
            result = run_restore(workspace, report, journal.parent.name)
            self.assertEqual(result.returncode, 1)
            self.assertTrue(journal.exists())

    def test_restore_rejects_tampered_report_plan_before_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan, report, journal, _before = self.make_crashed(temp)
            current = (workspace.memory_root / "project.md").read_bytes()
            plan["human_decisions"] = [
                {"decision": "tampered without refreshing the approved Plan Hash"}
            ]
            workspace.render_report(plan)

            result = run_restore(workspace, report, journal.parent.name)

            self.assertEqual(result.returncode, 1)
            self.assertIn("plan", result.stderr.lower())
            self.assertEqual((workspace.memory_root / "project.md").read_bytes(), current)
            self.assertIn("状态: 待确认", report.read_text(encoding="utf-8"))
            self.assertTrue(journal.exists())

    def test_restore_rejects_journal_operation_outside_plan_before_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, _plan, report, journal, _before = self.make_crashed(temp)
            unplanned = workspace.write(".agent-loop/unplanned.md", b"post-crash\n")
            unplanned_before = unplanned.read_bytes()
            project_before = (workspace.memory_root / "project.md").read_bytes()
            data = json.loads(journal.read_text(encoding="utf-8"))
            data["operations"][0]["path"] = "unplanned.md"
            journal.write_text(json.dumps(data, sort_keys=True), encoding="utf-8")

            result = run_restore(workspace, report, journal.parent.name)

            self.assertEqual(result.returncode, 1)
            self.assertIn("transaction", result.stderr.lower())
            self.assertEqual(unplanned.read_bytes(), unplanned_before)
            self.assertEqual(
                (workspace.memory_root / "project.md").read_bytes(), project_before
            )
            self.assertIn("状态: 待确认", report.read_text(encoding="utf-8"))
            self.assertTrue(journal.exists())

    def test_restore_rejects_verified_completed_transaction_before_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, _plan, report, journal, _before = self.make_crashed(temp)
            data = json.loads(journal.read_text(encoding="utf-8"))
            data["state"] = "verified"
            journal.write_text(json.dumps(data, sort_keys=True), encoding="utf-8")
            report.write_text(
                report.read_text(encoding="utf-8").replace(
                    "状态: 待确认", "状态: 已完成", 1
                ),
                encoding="utf-8",
            )
            current = (workspace.memory_root / "project.md").read_bytes()

            result = run_restore(workspace, report, journal.parent.name)

            self.assertEqual(result.returncode, 1)
            self.assertIn("restore", result.stderr.lower())
            self.assertEqual((workspace.memory_root / "project.md").read_bytes(), current)
            self.assertIn("状态: 已完成", report.read_text(encoding="utf-8"))
            self.assertTrue(journal.exists())

    def test_restore_rejects_unplanned_created_directory_before_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, _plan, report, journal, _before = self.make_crashed(temp)
            unplanned = workspace.memory_root / "unplanned-empty"
            unplanned.mkdir()
            data = json.loads(journal.read_text(encoding="utf-8"))
            data["created_directories"] = ["unplanned-empty"]
            journal.write_text(json.dumps(data, sort_keys=True), encoding="utf-8")
            project_before = (workspace.memory_root / "project.md").read_bytes()

            result = run_restore(workspace, report, journal.parent.name)

            self.assertEqual(result.returncode, 1)
            self.assertIn("transaction", result.stderr.lower())
            self.assertTrue(unplanned.is_dir())
            self.assertEqual(
                (workspace.memory_root / "project.md").read_bytes(), project_before
            )
            self.assertIn("状态: 待确认", report.read_text(encoding="utf-8"))
            self.assertTrue(journal.exists())

    def test_restore_rejects_post_crash_unrelated_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, _plan, report, journal, _before = self.make_crashed(temp)
            (workspace.memory_root / "project.md").write_bytes(b"unrelated post-crash drift\n")
            result = run_restore(workspace, report, journal.parent.name)
            self.assertEqual(result.returncode, 1)
            self.assertIn("drift", result.stderr.lower())

    def test_restore_rejects_retained_path_drift_before_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, _plan, report, journal, _before = self.make_crashed(temp)
            project_before = (workspace.memory_root / "project.md").read_bytes()
            retained = workspace.memory_root / "target-only.md"
            retained.write_text("unrelated retained drift\n", encoding="utf-8")

            result = run_restore(workspace, report, journal.parent.name)

            self.assertEqual(result.returncode, 1)
            self.assertIn("retained", result.stderr.lower())
            self.assertEqual(
                (workspace.memory_root / "project.md").read_bytes(), project_before
            )
            self.assertIn("状态: 待确认", report.read_text(encoding="utf-8"))
            self.assertTrue(journal.exists())

    def test_incomplete_restore_keeps_journal_and_blocks_reapply(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan, report, journal, _before = self.make_crashed(temp)
            (workspace.memory_root / "project.md").write_bytes(b"unrelated post-crash drift\n")
            self.assertEqual(run_restore(workspace, report, journal.parent.name).returncode, 1)
            self.assertTrue(journal.exists())
            reapplied = run_apply(workspace, report, str(plan["plan_sha256"]))
            self.assertEqual(reapplied.returncode, 1)
            self.assertIn("transaction", reapplied.stderr.lower())

    def test_successful_restore_updates_report_to_restored(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, _plan, report, journal, _before = self.make_crashed(temp)
            result = run_restore(workspace, report, journal.parent.name)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("状态: 已恢复", report.read_text(encoding="utf-8"))
            self.assertFalse(journal.parent.exists())
            txn_root = report.parent / ".memory-reconciliation-txn"
            self.assertFalse(txn_root.exists())

    def test_restore_resumes_after_restored_journal_before_or_after_status_update(self) -> None:
        for report_already_restored in (False, True):
            with self.subTest(report_already_restored=report_already_restored):
                with tempfile.TemporaryDirectory() as temp:
                    workspace, _plan, report, journal, _before = self.make_crashed(temp)
                    data = json.loads(journal.read_text(encoding="utf-8"))
                    operation = data["operations"][0]
                    backup = journal.parent / operation["backup_relative"]
                    target = workspace.memory_root / operation["path"]
                    target.write_bytes(backup.read_bytes())
                    target.chmod(0o755 if operation["original_mode"] == "100755" else 0o644)
                    data["state"] = "restored"
                    journal.write_text(json.dumps(data, sort_keys=True), encoding="utf-8")
                    if report_already_restored:
                        report.write_text(
                            report.read_text(encoding="utf-8").replace(
                                "状态: 待确认", "状态: 已恢复", 1
                            ),
                            encoding="utf-8",
                        )

                    result = run_restore(workspace, report, journal.parent.name)

                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("状态: 已恢复", report.read_text(encoding="utf-8"))
                    self.assertFalse(journal.parent.exists())


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.feature_archive_test_support import (
    ArchiveWorkspace,
    json_output,
    run_archive_command,
    tree_snapshot,
)


TRANSACTION_ID = "20260714T120000Z-0123456789ab"


class FeatureMonthlyArchiveRestoreTests(unittest.TestCase):
    def test_restore_check_accepts_exact_pretransaction_state_without_mutation(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            workspace.feature("2026-05-08-login")
            scan = run_archive_command(
                "scan-feature-monthly-archive.py",
                "--project-root",
                str(workspace.project_root),
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(scan.returncode, 0, scan.stderr)
            plan = workspace.project_root / "archive-plan.json"
            plan.write_text(
                json.dumps(json_output(scan), ensure_ascii=False, sort_keys=True, indent=2)
                + "\n",
                encoding="utf-8",
                newline="\n",
            )
            before = tree_snapshot(workspace.project_root)
            result = run_archive_command(
                "check-feature-monthly-archive.py",
                "--project-root",
                str(workspace.project_root),
                "--operation",
                "restore",
                "--plan",
                str(plan),
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("restore-check", result.stdout)
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def interrupted_transaction(
        self, workspace: ArchiveWorkspace, feature_id: str
    ) -> tuple[Path, dict[str, str]]:
        source = workspace.features_root / feature_id
        if not source.is_dir():
            source = workspace.feature(feature_id)
        before = tree_snapshot(workspace.project_root)
        scan = run_archive_command(
            "scan-feature-monthly-archive.py",
            "--project-root",
            str(workspace.project_root),
            "--operation",
            "archive",
            "--month",
            "2026-05",
            "--as-of",
            "2026-07-14",
        )
        self.assertEqual(scan.returncode, 0, scan.stderr)
        plan = json_output(scan)
        transaction = workspace.features_root / ".archive-txn" / TRANSACTION_ID
        transaction.mkdir(parents=True)
        index_relative = ".agent-loop/features/archive.md"
        backup_paths = sorted(
            {str(item["path"]) for item in plan["reference_edits"]}
            | {index_relative}
        )
        backups = []
        for relative in backup_paths:
            path = workspace.project_root / relative
            if path.is_file():
                content = path.read_bytes()
                backup_relative = f"backups/{relative}"
                backup = transaction / backup_relative
                backup.parent.mkdir(parents=True, exist_ok=True)
                backup.write_bytes(content)
                backups.append(
                    {
                        "path": relative,
                        "state": "existing",
                        "backup": backup_relative,
                        "sha256": hashlib.sha256(content).hexdigest(),
                    }
                )
            else:
                backups.append({"path": relative, "state": "missing-before"})
        target = workspace.features_root / "2026-05" / feature_id
        target.parent.mkdir(parents=True)
        source.rename(target)
        journal = {
            "schema_version": 1,
            "transaction_id": TRANSACTION_ID,
            "operation": "archive",
            "plan_sha256": plan["plan_sha256"],
            "plan": plan,
            "state": "moving",
            "moves": plan["moves"],
            "backups": backups,
            "completed_operations": [
                {
                    "kind": "move",
                    "source": f".agent-loop/features/{feature_id}",
                    "target": f".agent-loop/features/2026-05/{feature_id}",
                }
            ],
            "snapshots": plan["snapshots"],
            "created_directories": [".agent-loop/features/2026-05"],
        }
        (transaction / "journal.json").write_text(
            json.dumps(journal, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        return transaction, before

    def restore(self, workspace: ArchiveWorkspace):
        return run_archive_command(
            "restore-feature-monthly-archive.py",
            "--project-root",
            str(workspace.project_root),
            "--transaction-id",
            TRANSACTION_ID,
        )

    def test_interrupted_transaction_can_be_restored_by_new_process(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            transaction, before = self.interrupted_transaction(
                workspace, "2026-05-08-login"
            )
            result = self.restore(workspace)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)
            self.assertFalse(transaction.exists())

    def test_restore_recovers_move_completed_before_journal_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            transaction, before = self.interrupted_transaction(
                workspace, "2026-05-08-login"
            )
            journal_path = transaction / "journal.json"
            journal = json.loads(journal_path.read_text(encoding="utf-8"))
            journal["completed_operations"] = []
            journal_path.write_text(
                json.dumps(journal, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )
            result = self.restore(workspace)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)
            self.assertFalse(transaction.exists())

    def test_incomplete_restore_keeps_journal_and_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            transaction, _ = self.interrupted_transaction(
                workspace, "2026-05-08-login"
            )
            source_collision = workspace.features_root / "2026-05-08-login"
            source_collision.mkdir()
            (source_collision / "collision.md").write_text(
                "collision", encoding="utf-8"
            )
            result = self.restore(workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("restore", result.stdout + result.stderr)
            self.assertTrue(transaction.exists())
            journal = json.loads((transaction / "journal.json").read_text(encoding="utf-8"))
            self.assertEqual(journal["state"], "restoring")

    def test_restore_rejects_journal_path_escape_without_moving_feature(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            transaction, _ = self.interrupted_transaction(workspace, feature_id)
            target = workspace.features_root / "2026-05" / feature_id
            escaped = workspace.project_root.parent / (
                workspace.project_root.name + "-escaped-feature"
            )
            source_relative = f"../{escaped.name}"
            target_relative = f".agent-loop/features/2026-05/{feature_id}"
            journal_path = transaction / "journal.json"
            journal = json.loads(journal_path.read_text(encoding="utf-8"))
            journal["plan"]["moves"][0]["source"] = source_relative
            payload_without_hash = {
                key: value
                for key, value in journal["plan"].items()
                if key != "plan_sha256"
            }
            plan_sha256 = hashlib.sha256(
                json.dumps(
                    payload_without_hash,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest()
            journal["plan"]["plan_sha256"] = plan_sha256
            journal["plan_sha256"] = plan_sha256
            journal["moves"][0]["source"] = source_relative
            journal["completed_operations"][0]["source"] = source_relative
            journal_path.write_text(
                json.dumps(journal, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )
            try:
                result = self.restore(workspace)
                escaped_created = escaped.exists()
            finally:
                if escaped.exists():
                    shutil.rmtree(escaped)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("path-escape", result.stdout + result.stderr)
            self.assertFalse(escaped_created)
            self.assertTrue(target.is_dir())
            self.assertTrue(transaction.is_dir())

    def test_restore_rejects_tampered_backup_scope_without_deleting_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            victim = workspace.write("README.md", "must survive\n")
            transaction, _ = self.interrupted_transaction(
                workspace, "2026-05-08-login"
            )
            journal_path = transaction / "journal.json"
            journal = json.loads(journal_path.read_text(encoding="utf-8"))
            victim_sha256 = hashlib.sha256(victim.read_bytes()).hexdigest()
            journal["plan"]["reference_edits"].append(
                {
                    "path": "README.md",
                    "kind": "literal-path",
                    "old": "must survive",
                    "new": "must survive",
                    "occurrences": 1,
                    "before_sha256": victim_sha256,
                    "after_sha256": victim_sha256,
                }
            )
            payload_without_hash = {
                key: value
                for key, value in journal["plan"].items()
                if key != "plan_sha256"
            }
            plan_sha256 = hashlib.sha256(
                json.dumps(
                    payload_without_hash,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest()
            journal["plan"]["plan_sha256"] = plan_sha256
            journal["plan_sha256"] = plan_sha256
            journal["backups"].append(
                {"path": "README.md", "state": "missing-before"}
            )
            journal_path.write_text(
                json.dumps(journal, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )

            result = self.restore(workspace)

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("journal", result.stdout + result.stderr)
            self.assertTrue(victim.is_file())
            self.assertEqual(victim.read_text(encoding="utf-8"), "must survive\n")
            self.assertTrue(transaction.is_dir())
            self.assertTrue(
                (
                    workspace.features_root
                    / "2026-05"
                    / "2026-05-08-login"
                ).is_dir()
            )

    def test_restore_rejects_post_crash_reference_drift_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            project = workspace.write(
                ".agent-loop/project.md",
                f"# Project\n\nOwner: `.agent-loop/features/{feature_id}/spec.md`\n",
            )
            transaction, _ = self.interrupted_transaction(workspace, feature_id)
            project.write_text(
                "# Project\n\nHuman edit after crash\n",
                encoding="utf-8",
                newline="\n",
            )

            result = self.restore(workspace)

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("drift", result.stdout + result.stderr)
            self.assertEqual(
                project.read_text(encoding="utf-8"),
                "# Project\n\nHuman edit after crash\n",
            )
            self.assertTrue(transaction.is_dir())
            self.assertTrue(
                (workspace.features_root / "2026-05" / feature_id).is_dir()
            )

    def test_restore_rejects_corrupt_backup_before_moving_feature(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            workspace.write(
                ".agent-loop/project.md",
                f"# Project\n\n[Feature](features/{feature_id}/spec.md)\n",
            )
            transaction, _ = self.interrupted_transaction(workspace, feature_id)
            backup = transaction / "backups" / ".agent-loop" / "project.md"
            backup.write_text("corrupt backup\n", encoding="utf-8", newline="\n")
            target = workspace.features_root / "2026-05" / feature_id
            source = workspace.features_root / feature_id

            result = self.restore(workspace)

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("backup", result.stdout + result.stderr)
            self.assertTrue(target.is_dir())
            self.assertFalse(source.exists())
            self.assertEqual(
                workspace.project_root.joinpath(".agent-loop/project.md").read_text(
                    encoding="utf-8"
                ),
                f"# Project\n\n[Feature](features/{feature_id}/spec.md)\n",
            )
            self.assertEqual(backup.read_text(encoding="utf-8"), "corrupt backup\n")
            journal = json.loads(
                (transaction / "journal.json").read_text(encoding="utf-8")
            )
            self.assertEqual(journal["state"], "restoring")
            self.assertFalse((workspace.features_root / feature_id).exists())


if __name__ == "__main__":
    unittest.main()

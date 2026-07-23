from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from memory_reconciliation_support import canonical_plan_hash  # noqa: E402
from tests.memory_reconciliation_test_support import (  # noqa: E402
    MemoryMergeWorkspace,
    create_four_snapshot_workspace,
    run_memory_command,
    tree_snapshot,
)


def run_scan(workspace: MemoryMergeWorkspace, *extra: str):
    return run_memory_command(
        "scan-memory-reconciliation.py",
        "--project-root",
        str(workspace.project_root),
        "--merge-base-sha",
        workspace.merge_base_sha,
        "--source-sha",
        workspace.source_sha,
        "--target-before-sha",
        workspace.target_before_sha,
        "--merged-code-sha",
        workspace.merged_code_sha,
        "--source-branch",
        "feature/v1.4.0/source-memory",
        "--target-branch",
        "main",
        "--target-release-context",
        "v1.4.0",
        "--customer-boundary",
        "standard",
        "--full-audit-authorized",
        *extra,
    )


class MemoryReconciliationScanTests(unittest.TestCase):
    def test_scan_rejects_unapproved_full_memory_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = create_four_snapshot_workspace(Path(temp) / "repo")
            result = run_memory_command(
                "scan-memory-reconciliation.py",
                "--project-root",
                str(workspace.project_root),
                "--merge-base-sha",
                workspace.merge_base_sha,
                "--source-sha",
                workspace.source_sha,
                "--target-before-sha",
                workspace.target_before_sha,
                "--merged-code-sha",
                workspace.merged_code_sha,
                "--source-branch",
                "feature/v1.4.0/source-memory",
                "--target-branch",
                "main",
                "--target-release-context",
                "v1.4.0",
                "--customer-boundary",
                "standard",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn(
                "Full Memory Audit / Recovery requires explicit authorization",
                result.stderr,
            )

    def test_scan_requires_authorization_before_project_or_git_inspection(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            missing_project = Path(temp) / "does-not-exist"
            result = run_memory_command(
                "scan-memory-reconciliation.py",
                "--project-root",
                str(missing_project),
                "--merge-base-sha",
                "not-a-commit",
                "--source-sha",
                "not-a-commit",
                "--target-before-sha",
                "not-a-commit",
                "--merged-code-sha",
                "not-a-commit",
                "--source-branch",
                "source",
                "--target-branch",
                "target",
                "--target-release-context",
                "test",
                "--customer-boundary",
                "standard",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn(
                "Full Memory Audit / Recovery requires explicit authorization",
                result.stderr,
            )
            self.assertNotIn("project root", result.stderr.lower())
            self.assertNotIn("invalid commit", result.stderr.lower())

    def test_scan_help_exposes_only_explicit_full_audit_scope(self) -> None:
        result = run_memory_command("scan-memory-reconciliation.py", "--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        normalized_help = " ".join(result.stdout.split())
        self.assertIn("Full Memory Audit / Recovery scan", normalized_help)
        self.assertIn("--full-audit-authorized", normalized_help)

    def test_scan_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = create_four_snapshot_workspace(Path(temp) / "repo")
            before = tree_snapshot(workspace.project_root)
            result = run_scan(workspace)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_scan_uses_actual_target_as_primary_spine(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = create_four_snapshot_workspace(Path(temp) / "repo")
            result = run_scan(workspace)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["target_spine"]["snapshot"], "target_before")
            self.assertEqual(
                payload["target_spine"]["sha"], workspace.target_before_sha
            )
            self.assertIn("target-spine/INDEX.md", payload["target_spine"]["paths"])

    def test_scan_accounts_for_every_path_in_four_snapshots(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = create_four_snapshot_workspace(Path(temp) / "repo")
            result = run_scan(workspace)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            for row in payload["paths"]:
                self.assertEqual(
                    set(row["snapshots"]),
                    {"base", "source", "target_before", "result"},
                )
            self.assertIn("project.md", {row["path"] for row in payload["paths"]})

    def test_scan_includes_source_only_future_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = create_four_snapshot_workspace(Path(temp) / "repo")
            result = run_scan(workspace)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            by_path = {row["path"]: row for row in payload["paths"]}
            self.assertIn("domain-snapshots/FLOW-01.md", by_path)
            self.assertEqual(
                by_path["domain-snapshots/FLOW-01.md"]["snapshots"]["base"]["state"],
                "absent",
            )

    def test_scan_keeps_target_only_path_visible(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = create_four_snapshot_workspace(Path(temp) / "repo")
            result = run_scan(workspace)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            by_path = {row["path"]: row for row in payload["paths"]}
            self.assertIn("target-only.md", by_path)
            self.assertEqual(
                by_path["target-only.md"]["snapshots"]["source"]["state"], "absent"
            )

    def test_scan_records_absence_as_claim(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = create_four_snapshot_workspace(Path(temp) / "repo")
            result = run_scan(workspace)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            states = {
                entry["state"]
                for row in payload["paths"]
                for entry in row["snapshots"].values()
            }
            self.assertEqual(states, {"present", "absent"})

    def test_scan_rejects_missing_or_non_commit_sha(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = create_four_snapshot_workspace(Path(temp) / "repo")
            workspace.merge_base_sha = "not-a-commit"
            result = run_scan(workspace)
            self.assertEqual(result.returncode, 1)
            self.assertIn("invalid commit", result.stderr)

    def test_scan_rejects_head_different_from_merged_code_sha(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = create_four_snapshot_workspace(Path(temp) / "repo")
            workspace.write("after-merge.txt", "different HEAD\n")
            self.assertEqual(workspace.git("add", ".").returncode, 0)
            self.assertEqual(workspace.git("commit", "-q", "-m", "later").returncode, 0)
            result = run_scan(workspace)
            self.assertEqual(result.returncode, 1)
            self.assertIn("HEAD", result.stderr)

    def test_scan_rejects_blank_merge_context_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = create_four_snapshot_workspace(Path(temp) / "repo")
            result = run_scan(
                workspace,
                "--source-branch",
                "",
                "--target-branch",
                " ",
                "--target-release-context",
                "",
                "--customer-boundary",
                "   ",
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("merge context", result.stderr.lower())

    def test_scan_rejects_implicit_memory_root_migration(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = create_four_snapshot_workspace(Path(temp) / "repo")
            self.assertEqual(
                workspace.git("switch", "-q", "feature/v1.4.0/source-memory").returncode,
                0,
            )
            workspace.memory_root.rename(workspace.project_root / "agent-loop")
            self.assertEqual(workspace.git("add", "-A").returncode, 0)
            self.assertEqual(
                workspace.git("commit", "-q", "-m", "implicit root migration").returncode,
                0,
            )
            migrated_source = workspace.git("rev-parse", "HEAD").stdout.strip()
            self.assertEqual(workspace.git("switch", "-q", "main").returncode, 0)
            workspace.source_sha = migrated_source
            result = run_scan(workspace)
            self.assertEqual(result.returncode, 1)
            self.assertIn("memory root migration", result.stderr)

    def test_scan_excludes_only_current_report_transaction_scope(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = create_four_snapshot_workspace(Path(temp) / "repo")
            current = workspace.memory_root / "memory-merges/MM-current/README.md"
            current.parent.mkdir(parents=True)
            current.write_text("current report\n", encoding="utf-8")
            txn = current.parent / ".memory-reconciliation-txn/TX/journal.json"
            txn.parent.mkdir(parents=True)
            txn.write_text("{}\n", encoding="utf-8")
            other = workspace.memory_root / "memory-merges/MM-other/README.md"
            other.parent.mkdir(parents=True)
            other.write_text("other report\n", encoding="utf-8")
            result = run_scan(workspace, "--report", str(current))
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertNotIn("cannot read report", result.stderr)

            current.write_text(
                "<!-- memory-reconciliation-plan:start -->\n"
                "```json\n{}\n```\n"
                "<!-- memory-reconciliation-plan:end -->\n",
                encoding="utf-8",
            )
            result = run_scan(workspace, "--report", str(current))
            self.assertEqual(result.returncode, 0, result.stderr)
            paths = {row["path"] for row in json.loads(result.stdout)["paths"]}
            self.assertFalse(any(path.startswith("memory-merges/MM-current") for path in paths))
            self.assertIn("memory-merges/MM-other/README.md", paths)

    def test_post_apply_scan_reports_zero_change_against_exact_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = create_four_snapshot_workspace(Path(temp) / "repo")
            project_hash = __import__("hashlib").sha256(
                (workspace.memory_root / "project.md").read_bytes()
            ).hexdigest()
            payload: dict[str, object] = {
                "schema_version": 1,
                "report_id": f"MM-{workspace.merged_code_sha[:12]}",
                "context": {
                    "merge_base_sha": workspace.merge_base_sha,
                    "source_sha": workspace.source_sha,
                    "target_before_sha": workspace.target_before_sha,
                    "merged_code_sha": workspace.merged_code_sha,
                    "source_branch": "feature/v1.4.0/source-memory",
                    "target_branch": "main",
                    "target_release_context": "v1.4.0",
                    "customer_boundary": "standard",
                    "memory_root": ".agent-loop",
                },
                "scan_sha256": "0" * 64,
                "ledger": [],
                "operations": [],
                "expected_unchanged_paths": {"project.md": project_hash},
                "human_decisions": [],
                "post_check_expectations": ["zero-change"],
                "plan_sha256": "",
            }
            payload["plan_sha256"] = canonical_plan_hash(payload)
            report = workspace.render_report(payload)
            result = run_scan(workspace, "--report", str(report))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)["zero_change"])


if __name__ == "__main__":
    unittest.main()

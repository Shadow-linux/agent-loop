from __future__ import annotations

import base64
import hashlib
import json
import os
import sys
import tempfile
import unittest
from copy import deepcopy
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
from tests.test_memory_reconciliation_check import (  # noqa: E402
    build_plan,
    find_file_row,
    set_inline_rewrite,
)


def run_apply(
    workspace: MemoryMergeWorkspace,
    report: Path,
    plan_hash: str,
    mode: str = "apply",
    *,
    env: dict[str, str] | None = None,
):
    command = [
        sys.executable,
        str(SCRIPTS / "apply-memory-reconciliation.py"),
        "--project-root",
        str(workspace.project_root),
        "--report",
        str(report),
        "--mode",
        mode,
        "--expected-plan-sha256",
        plan_hash,
    ]
    import subprocess

    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, **(env or {})},
    )


def pending_transaction(report: Path) -> Path:
    journals = list((report.parent / ".memory-reconciliation-txn").glob("*/journal.json"))
    if len(journals) != 1:
        raise AssertionError(f"expected one journal, got {journals}")
    return journals[0]


def mark_semantic_postcheck_pass(report: Path) -> None:
    text = report.read_text(encoding="utf-8")
    text = text.replace("Machine check: not-run | pass | fail", "Machine check: pass")
    text = text.replace("Zero-change rescan: not-run | pass | fail", "Zero-change rescan: pass")
    text = text.replace(
        "Domain / semantic verification:",
        "Domain / semantic verification: PASS: bounded semantic checks",
    )
    report.write_text(text, encoding="utf-8")


def git_blob_rewrite(
    workspace: MemoryMergeWorkspace, plan: dict[str, object], *, target: str = "target-only.md"
) -> bytes:
    content = (workspace.memory_root / "source.bin").read_bytes()
    row = find_file_row(plan, target)
    row.update(
        {
            "semantic_role": "current-semantic-state",
            "action": "重写",
            "operation_id": "op-001",
            "desired_value": "copy exact binary Source blob",
        }
    )
    plan["operations"] = [
        {
            "operation_id": "op-001",
            "sequence": 1,
            "path": target,
            "action": "重写",
            "preimage_sha256": hashlib.sha256(
                (workspace.memory_root / target).read_bytes()
            ).hexdigest(),
            "postimage_sha256": hashlib.sha256(content).hexdigest(),
            "post_mode": "100644",
            "content_source": {
                "kind": "git-blob",
                "git_sha": workspace.source_sha,
                "git_path": "source.bin",
                "inline_base64": None,
            },
        }
    ]
    plan["plan_sha256"] = canonical_plan_hash(plan)
    return content


def remove_path(workspace: MemoryMergeWorkspace, plan: dict[str, object], path: str) -> None:
    row = find_file_row(plan, path)
    row.update(
        {
            "semantic_role": "current-semantic-state",
            "action": "移除过时声明",
            "operation_id": "op-001",
            "desired_value": "absent",
        }
    )
    plan["operations"] = [
        {
            "operation_id": "op-001",
            "sequence": 1,
            "path": path,
            "action": "移除过时声明",
            "preimage_sha256": hashlib.sha256(
                (workspace.memory_root / path).read_bytes()
            ).hexdigest(),
            "postimage_sha256": None,
            "post_mode": "absent",
            "content_source": {
                "kind": "none",
                "git_sha": None,
                "git_path": None,
                "inline_base64": None,
            },
        }
    ]
    plan["plan_sha256"] = canonical_plan_hash(plan)


class MemoryReconciliationApplyTests(unittest.TestCase):
    def make_workspace(self, temp: str):
        workspace = create_four_snapshot_workspace(Path(temp) / "repo")
        return workspace, build_plan(workspace)

    def test_apply_writes_inline_utf8_bytes_and_mode_exactly(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            content = "重写后的项目记忆\n".encode()
            set_inline_rewrite(workspace, plan, content=content)
            plan["operations"][0]["post_mode"] = "100755"  # type: ignore[index]
            plan["plan_sha256"] = canonical_plan_hash(plan)
            report = workspace.render_report(plan)
            result = run_apply(workspace, report, str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 0, result.stderr)
            path = workspace.memory_root / "project.md"
            self.assertEqual(path.read_bytes(), content)
            if os.name != "nt":
                self.assertTrue(path.stat().st_mode & 0o100)
            journal = json.loads(pending_transaction(report).read_text(encoding="utf-8"))
            self.assertEqual(journal["state"], "checking")

    def test_apply_copies_binary_git_blob_exactly(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            expected = git_blob_rewrite(workspace, plan)
            report = workspace.render_report(plan)
            result = run_apply(workspace, report, str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((workspace.memory_root / "target-only.md").read_bytes(), expected)

    def test_apply_removes_only_planned_stale_agent_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            source_before = (workspace.memory_root / "source-only.md").read_bytes()
            remove_path(workspace, plan, "target-only.md")
            report = workspace.render_report(plan)
            result = run_apply(workspace, report, str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((workspace.memory_root / "target-only.md").exists())
            self.assertEqual((workspace.memory_root / "source-only.md").read_bytes(), source_before)

    def test_apply_preserves_expected_unchanged_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            unchanged = workspace.memory_root / "target-only.md"
            original = unchanged.read_bytes()
            plan["expected_unchanged_paths"] = {
                "target-only.md": hashlib.sha256(original).hexdigest()
            }
            set_inline_rewrite(workspace, plan)
            plan["plan_sha256"] = canonical_plan_hash(plan)
            report = workspace.render_report(plan)
            result = run_apply(workspace, report, str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(unchanged.read_bytes(), original)

    def test_apply_rejects_different_expected_plan_hash_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            set_inline_rewrite(workspace, plan)
            report = workspace.render_report(plan)
            before = tree_snapshot(workspace.project_root)
            result = run_apply(workspace, report, "f" * 64)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_apply_rejects_preimage_drift_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            set_inline_rewrite(workspace, plan)
            report = workspace.render_report(plan)
            workspace.write(".agent-loop/project.md", "drift\n")
            before = tree_snapshot(workspace.project_root)
            result = run_apply(workspace, report, str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 1)
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_apply_rejects_completed_report_replay(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            completed = dict(plan)
            completed["_report_status"] = "已完成"
            report = workspace.render_report(completed)
            before = tree_snapshot(workspace.project_root)
            result = run_apply(workspace, report, str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 1)
            self.assertIn("completed", result.stderr.lower())
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_apply_rejects_path_escape_case_collision_and_symlink_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, original = self.make_workspace(temp)
            outside = workspace.project_root / "outside"
            outside.mkdir()
            os.symlink(outside, workspace.memory_root / "escape")
            cases: list[dict[str, object]] = []

            escaped = deepcopy(original)
            set_inline_rewrite(workspace, escaped)
            escaped["operations"][0]["path"] = "../outside.md"  # type: ignore[index]
            escaped["plan_sha256"] = canonical_plan_hash(escaped)
            cases.append(escaped)

            collision = deepcopy(original)
            duplicate = deepcopy(collision["ledger"][0])  # type: ignore[index]
            duplicate["path"] = str(duplicate["path"]).swapcase()
            collision["ledger"].append(duplicate)  # type: ignore[union-attr]
            collision["plan_sha256"] = canonical_plan_hash(collision)
            cases.append(collision)

            symlinked = deepcopy(original)
            set_inline_rewrite(workspace, symlinked)
            find_file_row(symlinked)["path"] = "escape/file.md"
            symlinked["operations"][0]["path"] = "escape/file.md"  # type: ignore[index]
            symlinked["plan_sha256"] = canonical_plan_hash(symlinked)
            cases.append(symlinked)

            for index, plan in enumerate(cases):
                report = workspace.render_report(plan)
                before = tree_snapshot(workspace.project_root)
                with self.subTest(index=index):
                    result = run_apply(workspace, report, str(plan["plan_sha256"]))
                    self.assertEqual(result.returncode, 1)
                    self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_apply_rejects_existing_unrestored_transaction(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            set_inline_rewrite(workspace, plan)
            report = workspace.render_report(plan)
            txn = report.parent / ".memory-reconciliation-txn/existing"
            txn.mkdir(parents=True)
            (txn / "journal.json").write_text('{"state":"restoring"}\n', encoding="utf-8")
            before = tree_snapshot(workspace.project_root)
            result = run_apply(workspace, report, str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 1)
            self.assertIn("transaction", result.stderr.lower())
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_injected_mid_apply_failure_restores_all_memory_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            set_inline_rewrite(workspace, plan)
            report = workspace.render_report(plan)
            before = tree_snapshot(workspace.memory_root)
            result = run_apply(
                workspace,
                report,
                str(plan["plan_sha256"]),
                env={
                    "AGENT_LOOP_TEST_FAILURE": "fail-after-1",
                    "AGENT_LOOP_ALLOW_TEST_HOOKS": "1",
                },
            )
            self.assertEqual(result.returncode, 1)
            after = tree_snapshot(workspace.memory_root)
            for path, digest in before.items():
                if ".memory-reconciliation-txn" not in path and path != report.relative_to(workspace.memory_root).as_posix():
                    self.assertEqual(after.get(path), digest, path)
            self.assertIn("状态: 已恢复", report.read_text(encoding="utf-8"))

    def test_apply_never_changes_business_code_git_refs_or_head(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            set_inline_rewrite(workspace, plan)
            report = workspace.render_report(plan)
            app = (workspace.project_root / "app.txt").read_bytes()
            head = workspace.git("rev-parse", "HEAD").stdout
            refs = workspace.git("show-ref").stdout
            result = run_apply(workspace, report, str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((workspace.project_root / "app.txt").read_bytes(), app)
            self.assertEqual(workspace.git("rev-parse", "HEAD").stdout, head)
            self.assertEqual(workspace.git("show-ref").stdout, refs)

    def test_apply_never_executes_report_commands_or_hooks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            set_inline_rewrite(workspace, plan)
            report = workspace.render_report(plan)
            marker = workspace.project_root / "executed-marker"
            with report.open("a", encoding="utf-8") as handle:
                handle.write(f"\nHook: touch {marker}\nCommand: $(touch {marker})\n")
            result = run_apply(workspace, report, str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists())

    def test_finalize_requires_semantic_evidence_and_zero_change(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            set_inline_rewrite(workspace, plan)
            report = workspace.render_report(plan)
            applied = run_apply(workspace, report, str(plan["plan_sha256"]))
            self.assertEqual(applied.returncode, 0, applied.stderr)
            result = run_apply(workspace, report, str(plan["plan_sha256"]), "finalize")
            self.assertEqual(result.returncode, 1)
            self.assertIn("evidence", result.stderr.lower())
            self.assertIn("状态: 待确认", report.read_text(encoding="utf-8"))

    def test_finalize_sets_completed_and_removes_only_own_transaction(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = create_four_snapshot_workspace(Path(temp) / "repo")
            other = workspace.memory_root / "memory-merges/MM-other/.memory-reconciliation-txn/keep/journal.json"
            other.parent.mkdir(parents=True)
            other.write_text("{}\n", encoding="utf-8")
            plan = build_plan(workspace)
            set_inline_rewrite(workspace, plan)
            report = workspace.render_report(plan)
            applied = run_apply(workspace, report, str(plan["plan_sha256"]))
            self.assertEqual(applied.returncode, 0, applied.stderr)
            mark_semantic_postcheck_pass(report)
            result = run_apply(workspace, report, str(plan["plan_sha256"]), "finalize")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("状态: 已完成", report.read_text(encoding="utf-8"))
            self.assertFalse((report.parent / ".memory-reconciliation-txn").exists())
            self.assertTrue(other.exists())

    def test_finalize_resumes_verified_transaction_without_reapply(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            set_inline_rewrite(workspace, plan)
            report = workspace.render_report(plan)
            self.assertEqual(run_apply(workspace, report, str(plan["plan_sha256"])).returncode, 0)
            mark_semantic_postcheck_pass(report)
            journal_path = pending_transaction(report)
            journal = json.loads(journal_path.read_text(encoding="utf-8"))
            journal["state"] = "verified"
            journal_path.write_text(json.dumps(journal, sort_keys=True), encoding="utf-8")
            post = (workspace.memory_root / "project.md").read_bytes()
            result = run_apply(workspace, report, str(plan["plan_sha256"]), "finalize")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((workspace.memory_root / "project.md").read_bytes(), post)
            self.assertIn("状态: 已完成", report.read_text(encoding="utf-8"))

    def test_finalize_accepts_source_only_future_directory_import(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = create_four_snapshot_workspace(Path(temp) / "repo")
            self.assertEqual(
                workspace.git("rm", "-q", "-r", ".agent-loop/domain-snapshots").returncode,
                0,
            )
            self.assertEqual(
                workspace.git("commit", "-q", "-m", "omit source-only future directory").returncode,
                0,
            )
            workspace.merged_code_sha = workspace.git("rev-parse", "HEAD").stdout.strip()
            plan = build_plan(workspace)
            path = "domain-snapshots/FLOW-01.md"
            source = workspace.git(
                "show", f"{workspace.source_sha}:.agent-loop/{path}"
            ).stdout.encode("utf-8")
            row = find_file_row(plan, path)
            row.update(
                {
                    "semantic_role": "current-semantic-state",
                    "action": "引入",
                    "operation_id": "op-001",
                    "desired_value": "import future Source memory",
                }
            )
            plan["operations"] = [
                {
                    "operation_id": "op-001",
                    "sequence": 1,
                    "path": path,
                    "action": "引入",
                    "preimage_sha256": None,
                    "postimage_sha256": hashlib.sha256(source).hexdigest(),
                    "post_mode": "100644",
                    "content_source": {
                        "kind": "git-blob",
                        "git_sha": workspace.source_sha,
                        "git_path": path,
                        "inline_base64": None,
                    },
                }
            ]
            plan["plan_sha256"] = canonical_plan_hash(plan)
            report = workspace.render_report(plan)

            applied = run_apply(workspace, report, str(plan["plan_sha256"]))
            self.assertEqual(applied.returncode, 0, applied.stderr)
            mark_semantic_postcheck_pass(report)
            finalized = run_apply(
                workspace, report, str(plan["plan_sha256"]), "finalize"
            )

            self.assertEqual(finalized.returncode, 0, finalized.stderr)
            self.assertEqual((workspace.memory_root / path).read_bytes(), source)
            self.assertIn("状态: 已完成", report.read_text(encoding="utf-8"))

    def test_finalize_rejects_completed_report_without_own_residual_transaction(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            completed = dict(plan)
            completed["_report_status"] = "已完成"
            report = workspace.render_report(completed)
            before = tree_snapshot(workspace.project_root)
            result = run_apply(workspace, report, str(plan["plan_sha256"]), "finalize")
            self.assertEqual(result.returncode, 1)
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_finalize_never_executes_report_commands_or_hooks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            set_inline_rewrite(workspace, plan)
            report = workspace.render_report(plan)
            self.assertEqual(run_apply(workspace, report, str(plan["plan_sha256"])).returncode, 0)
            mark_semantic_postcheck_pass(report)
            marker = workspace.project_root / "finalize-marker"
            with report.open("a", encoding="utf-8") as handle:
                handle.write(f"\nCommand: touch {marker}\n")
            result = run_apply(workspace, report, str(plan["plan_sha256"]), "finalize")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()

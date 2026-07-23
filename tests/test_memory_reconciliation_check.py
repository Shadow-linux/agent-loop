from __future__ import annotations

import base64
import hashlib
import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from memory_reconciliation_support import (  # noqa: E402
    MemoryReconciliationError,
    canonical_plan_hash,
    plan_from_payload,
    validate_plan_contract,
)
from tests.memory_reconciliation_test_support import (  # noqa: E402
    MemoryMergeWorkspace,
    create_four_snapshot_workspace,
    run_memory_command,
    tree_snapshot,
)
from tests.test_memory_reconciliation_scan import run_scan  # noqa: E402


def build_plan(workspace: MemoryMergeWorkspace) -> dict[str, object]:
    scan = run_scan(workspace)
    if scan.returncode:
        raise AssertionError(scan.stderr)
    scan_payload = json.loads(scan.stdout)
    ledger = []
    for row in scan_payload["paths"]:
        ledger.append(
            {
                "path": row["path"],
                "snapshots": row["snapshots"],
                "semantic_role": "current-semantic-state",
                "stable_identity": row["path"],
                "owner": "canonical artifact owner",
                "attention": "🟢",
                "action": "保留",
                "fact_sources": ["four-snapshot scan"],
                "desired_value": "retain verified current bytes/absence",
                "operation_id": None,
            }
        )
    payload: dict[str, object] = {
        "schema_version": 1,
        "report_id": f"MM-{workspace.merged_code_sha[:12]}",
        "context": scan_payload["context"],
        "scan_sha256": scan_payload["scan_sha256"],
        "ledger": ledger,
        "operations": [],
        "expected_unchanged_paths": {},
        "human_decisions": [],
        "post_check_expectations": [
            "exact postimages",
            "expected unchanged paths",
            "zero-change",
            "domain semantic evidence",
        ],
        "plan_sha256": "",
    }
    payload["plan_sha256"] = canonical_plan_hash(payload)
    return payload


def find_file_row(plan: dict[str, object], path: str = "project.md") -> dict[str, object]:
    return next(row for row in plan["ledger"] if row["path"] == path)  # type: ignore[index]


def set_inline_rewrite(
    workspace: MemoryMergeWorkspace,
    plan: dict[str, object],
    *,
    path: str = "project.md",
    content: bytes = b"rewritten\n",
    role: str = "current-semantic-state",
    action: str = "重写",
) -> None:
    row = find_file_row(plan, path)
    preimage = hashlib.sha256((workspace.memory_root / path).read_bytes()).hexdigest()
    postimage = hashlib.sha256(content).hexdigest()
    row.update(
        {
            "semantic_role": role,
            "action": action,
            "operation_id": "op-001",
            "desired_value": "test rewrite",
        }
    )
    plan["operations"] = [
        {
            "operation_id": "op-001",
            "sequence": 1,
            "path": path,
            "action": action,
            "preimage_sha256": preimage,
            "postimage_sha256": postimage,
            "post_mode": "100644",
            "content_source": {
                "kind": "inline-base64",
                "git_sha": None,
                "git_path": None,
                "inline_base64": base64.b64encode(content).decode("ascii"),
            },
        }
    ]
    plan["plan_sha256"] = canonical_plan_hash(plan)


def run_check(
    workspace: MemoryMergeWorkspace,
    report: Path,
    plan_hash: str,
    phase: str = "pre-apply",
    *,
    env: dict[str, str] | None = None,
):
    return run_memory_command(
        "check-memory-reconciliation.py",
        "--project-root",
        str(workspace.project_root),
        "--report",
        str(report),
        "--phase",
        phase,
        "--expected-plan-sha256",
        plan_hash,
        env=env,
    )


class MemoryReconciliationCheckTests(unittest.TestCase):
    def make_workspace(self, temp: str) -> tuple[MemoryMergeWorkspace, dict[str, object]]:
        workspace = create_four_snapshot_workspace(Path(temp) / "repo")
        return workspace, build_plan(workspace)

    def test_pre_check_accepts_complete_reviewed_plan_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            report = workspace.render_report(plan)
            before = tree_snapshot(workspace.project_root)
            result = run_check(workspace, report, str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_pre_check_rejects_missing_ledger_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            plan["ledger"] = plan["ledger"][1:]  # type: ignore[index]
            plan["plan_sha256"] = canonical_plan_hash(plan)
            result = run_check(workspace, workspace.render_report(plan), str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 1)
            self.assertIn("ledger", result.stderr.lower())

    def test_pre_check_rejects_unclassified_or_unresolved_red_row(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            for key, value in (("semantic_role", "unclassified"), ("attention", "🔴")):
                changed = deepcopy(plan)
                find_file_row(changed)[key] = value
                changed["plan_sha256"] = canonical_plan_hash(changed)
                with self.subTest(key=key):
                    result = run_check(
                        workspace,
                        workspace.render_report(changed),
                        str(changed["plan_sha256"]),
                    )
                    self.assertEqual(result.returncode, 1)

    def test_pre_check_rejects_temporary_action_in_ready_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            find_file_row(plan)["action"] = "暂不处理"
            plan["plan_sha256"] = canonical_plan_hash(plan)
            result = run_check(workspace, workspace.render_report(plan), str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 1)
            self.assertIn("暂不处理", result.stderr)

    def test_pre_check_emits_utf8_errors_under_ascii_host_stdio(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            find_file_row(plan)["action"] = "暂不处理"
            plan["plan_sha256"] = canonical_plan_hash(plan)
            result = run_check(
                workspace,
                workspace.render_report(plan),
                str(plan["plan_sha256"]),
                env={"PYTHONIOENCODING": "ascii:backslashreplace"},
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("暂不处理", result.stderr)
            self.assertNotIn("\\u6682", result.stderr)

    def test_pre_check_rejects_human_source_rewrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            set_inline_rewrite(workspace, plan, role="human-source")
            result = run_check(workspace, workspace.render_report(plan), str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 1)
            self.assertIn("human-source", result.stderr)

    def test_pre_check_rejects_accepted_authority_in_place_rewrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            set_inline_rewrite(workspace, plan, role="accepted-authority")
            result = run_check(workspace, workspace.render_report(plan), str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 1)
            self.assertIn("accepted-authority", result.stderr)

    def test_pre_check_rejects_append_only_truncation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            set_inline_rewrite(workspace, plan, role="append-only-evidence", content=b"x")
            result = run_check(workspace, workspace.render_report(plan), str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 1)
            self.assertIn("append-only", result.stderr)

    def test_pre_check_rejects_changed_row_without_operation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            find_file_row(plan)["action"] = "重写"
            plan["plan_sha256"] = canonical_plan_hash(plan)
            result = run_check(workspace, workspace.render_report(plan), str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 1)
            self.assertIn("operation", result.stderr.lower())

    def test_pre_check_rejects_operation_without_ledger_owner(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            set_inline_rewrite(workspace, plan)
            find_file_row(plan)["operation_id"] = None
            find_file_row(plan)["action"] = "保留"
            plan["plan_sha256"] = canonical_plan_hash(plan)
            result = run_check(workspace, workspace.render_report(plan), str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 1)
            self.assertIn("owner", result.stderr.lower())

    def test_pre_check_rejects_wrong_or_self_inconsistent_plan_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            report = workspace.render_report(plan)
            result = run_check(workspace, report, "f" * 64)
            self.assertEqual(result.returncode, 1)
            self.assertIn("hash", result.stderr.lower())
            plan["plan_sha256"] = "e" * 64
            result = run_check(workspace, workspace.render_report(plan), "e" * 64)
            self.assertEqual(result.returncode, 1)

    def test_pre_check_rejects_report_id_and_full_sha_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            plan["report_id"] = "MM-deadbeefdead"
            plan["plan_sha256"] = canonical_plan_hash(plan)
            result = run_check(workspace, workspace.render_report(plan), str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 1)
            self.assertIn("report", result.stderr.lower())

    def test_pre_check_rejects_report_id_extension_not_from_full_sha(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            full_sha = workspace.merged_code_sha
            wrong_next = "0" if full_sha[12] != "0" else "1"
            plan["report_id"] = f"MM-{full_sha[:12]}{wrong_next}"
            plan["plan_sha256"] = canonical_plan_hash(plan)
            report = workspace.render_report(plan)

            result = run_check(workspace, report, str(plan["plan_sha256"]))

            self.assertEqual(result.returncode, 1)
            self.assertIn("report identity", result.stderr.lower())

    def test_pre_check_rejects_second_report_for_same_merged_code_sha(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            workspace.render_report(plan)
            second = deepcopy(plan)
            second["report_id"] = f"MM-{workspace.merged_code_sha[:13]}"
            second["plan_sha256"] = canonical_plan_hash(second)
            report = workspace.render_report(second)

            result = run_check(workspace, report, str(second["plan_sha256"]))

            self.assertEqual(result.returncode, 1)
            self.assertIn("merged code report", result.stderr.lower())

    def test_pre_check_rejects_blank_merge_context_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, original = self.make_workspace(temp)
            for field in (
                "source_branch",
                "target_branch",
                "target_release_context",
                "customer_boundary",
            ):
                plan = deepcopy(original)
                plan["context"][field] = "   "  # type: ignore[index]
                plan["plan_sha256"] = canonical_plan_hash(plan)
                with self.subTest(field=field):
                    result = run_check(
                        workspace,
                        workspace.render_report(plan),
                        str(plan["plan_sha256"]),
                    )
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("merge context", result.stderr.lower())

    def test_plan_contract_rejects_action_state_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, original = self.make_workspace(temp)

            import_overwrite = deepcopy(original)
            set_inline_rewrite(workspace, import_overwrite, action="引入")

            removal_write = deepcopy(original)
            set_inline_rewrite(workspace, removal_write, action="移除过时声明")

            for name, plan in (
                ("import-overwrite", import_overwrite),
                ("removal-write", removal_write),
            ):
                with self.subTest(name=name):
                    with self.assertRaises(MemoryReconciliationError) as raised:
                        validate_plan_contract(plan_from_payload(plan))
                    self.assertIn("operation semantics", str(raised.exception).lower())

    def test_plan_contract_rejects_forged_human_source_import(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            path = "source-only.md"
            row = find_file_row(plan, path)
            content = b"forged human source\n"
            row["snapshots"]["result"] = {  # type: ignore[index]
                "state": "absent",
                "kind": "missing",
                "git_mode": None,
                "git_oid": None,
                "sha256": None,
            }
            row.update(
                {
                    "semantic_role": "human-source",
                    "action": "引入",
                    "operation_id": "op-001",
                    "desired_value": "forged replacement",
                }
            )
            plan["operations"] = [
                {
                    "operation_id": "op-001",
                    "sequence": 1,
                    "path": path,
                    "action": "引入",
                    "preimage_sha256": None,
                    "postimage_sha256": hashlib.sha256(content).hexdigest(),
                    "post_mode": "100644",
                    "content_source": {
                        "kind": "inline-base64",
                        "git_sha": None,
                        "git_path": None,
                        "inline_base64": base64.b64encode(content).decode("ascii"),
                    },
                }
            ]
            plan["plan_sha256"] = canonical_plan_hash(plan)

            with self.assertRaises(MemoryReconciliationError) as raised:
                validate_plan_contract(plan_from_payload(plan))

            self.assertIn("human-source import", str(raised.exception).lower())

    def test_plan_contract_accepts_recalculation_from_absent_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            path = "source-only.md"
            row = find_file_row(plan, path)
            content = b"recalculated derived index\n"
            row["snapshots"]["result"] = {  # type: ignore[index]
                "state": "absent",
                "kind": "missing",
                "git_mode": None,
                "git_oid": None,
                "sha256": None,
            }
            row.update(
                {
                    "semantic_role": "derived-index",
                    "action": "重算",
                    "operation_id": "op-001",
                    "desired_value": "rebuild missing index",
                }
            )
            plan["operations"] = [
                {
                    "operation_id": "op-001",
                    "sequence": 1,
                    "path": path,
                    "action": "重算",
                    "preimage_sha256": None,
                    "postimage_sha256": hashlib.sha256(content).hexdigest(),
                    "post_mode": "100644",
                    "content_source": {
                        "kind": "inline-base64",
                        "git_sha": None,
                        "git_path": None,
                        "inline_base64": base64.b64encode(content).decode("ascii"),
                    },
                }
            ]
            plan["plan_sha256"] = canonical_plan_hash(plan)

            validate_plan_contract(plan_from_payload(plan))

    def test_pre_check_rejects_inline_payload_hash_or_size_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            set_inline_rewrite(workspace, plan)
            plan["operations"][0]["postimage_sha256"] = "0" * 64  # type: ignore[index]
            plan["plan_sha256"] = canonical_plan_hash(plan)
            result = run_check(workspace, workspace.render_report(plan), str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 1)
            self.assertIn("payload", result.stderr.lower())

    def test_pre_check_rejects_git_blob_outside_recorded_context(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            set_inline_rewrite(workspace, plan)
            operation = plan["operations"][0]  # type: ignore[index]
            operation["content_source"] = {
                "kind": "git-blob",
                "git_sha": workspace.source_sha,
                "git_path": "../app.txt",
                "inline_base64": None,
            }
            plan["plan_sha256"] = canonical_plan_hash(plan)
            result = run_check(workspace, workspace.render_report(plan), str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 1)
            self.assertIn("git-blob", result.stderr)

    def test_pre_check_rejects_git_tree_as_blob_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            set_inline_rewrite(workspace, plan, path="target-only.md")
            tree_bytes = workspace.git(
                "cat-file", "-p", f"{workspace.source_sha}:.agent-loop/shared"
            ).stdout.encode("utf-8")
            operation = plan["operations"][0]  # type: ignore[index]
            operation["postimage_sha256"] = hashlib.sha256(tree_bytes).hexdigest()
            operation["content_source"] = {
                "kind": "git-blob",
                "git_sha": workspace.source_sha,
                "git_path": "shared",
                "inline_base64": None,
            }
            plan["plan_sha256"] = canonical_plan_hash(plan)

            result = run_check(
                workspace,
                workspace.render_report(plan),
                str(plan["plan_sha256"]),
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("regular git blob", result.stderr.lower())

    def test_pre_check_rejects_unexpected_dirty_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            report = workspace.render_report(plan)
            workspace.write(".agent-loop/unexpected.md", "dirty\n")
            result = run_check(workspace, report, str(plan["plan_sha256"]))
            self.assertEqual(result.returncode, 1)
            self.assertIn("dirty", result.stderr.lower())

    def test_post_check_accepts_exact_postimages_and_unchanged_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            plan["expected_unchanged_paths"] = {
                "project.md": hashlib.sha256(
                    (workspace.memory_root / "project.md").read_bytes()
                ).hexdigest()
            }
            plan["plan_sha256"] = canonical_plan_hash(plan)
            report = workspace.render_report(plan)
            text = report.read_text(encoding="utf-8")
            text = text.replace("Machine check: not-run | pass | fail", "Machine check: pass")
            text = text.replace("Zero-change rescan: not-run | pass | fail", "Zero-change rescan: pass")
            text = text.replace(
                "Domain / semantic verification:",
                "Domain / semantic verification: PASS: bounded semantic checks",
            )
            report.write_text(text, encoding="utf-8")
            before = tree_snapshot(workspace.project_root)
            result = run_check(workspace, report, str(plan["plan_sha256"]), "post-apply")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_post_check_rejects_missing_zero_change_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            report = workspace.render_report(plan)
            text = report.read_text(encoding="utf-8")
            text = text.replace("Machine check: not-run | pass | fail", "Machine check: pass")
            text = text.replace(
                "Domain / semantic verification:",
                "Domain / semantic verification: PASS: bounded semantic checks",
            )
            report.write_text(text, encoding="utf-8")
            result = run_check(workspace, report, str(plan["plan_sha256"]), "post-apply")
            self.assertEqual(result.returncode, 1)
            self.assertIn("zero-change", result.stderr.lower())

    def test_post_check_rejects_unplanned_change_to_retained_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            report = workspace.render_report(plan)
            retained = workspace.memory_root / "target-only.md"
            retained.write_text("unplanned retained-path drift\n", encoding="utf-8")
            text = report.read_text(encoding="utf-8")
            text = text.replace("Machine check: not-run | pass | fail", "Machine check: pass")
            text = text.replace(
                "Zero-change rescan: not-run | pass | fail", "Zero-change rescan: pass"
            )
            text = text.replace(
                "Domain / semantic verification:",
                "Domain / semantic verification: PASS: bounded semantic checks",
            )
            report.write_text(text, encoding="utf-8")

            result = run_check(workspace, report, str(plan["plan_sha256"]), "post-apply")

            self.assertEqual(result.returncode, 1)
            self.assertIn("retained postimage", result.stderr.lower())

    def test_restore_check_accepts_exact_pretransaction_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace, plan = self.make_workspace(temp)
            restored = dict(plan)
            restored["_report_status"] = "已恢复"
            report = workspace.render_report(restored)
            before = tree_snapshot(workspace.project_root)
            result = run_check(workspace, report, str(plan["plan_sha256"]), "restore")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)


if __name__ == "__main__":
    unittest.main()

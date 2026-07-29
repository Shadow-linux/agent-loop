from __future__ import annotations

import ast
import os
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

from tests.checker_test_support import ROOT
from tests.lightweight_change_test_support import (
    CARD,
    ChangeWorkspace,
    json_output,
    run_scan,
    tree_snapshot,
)

SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lightweight_change_support import (  # noqa: E402
    LightweightChangeContractError,
    build_scan,
)


class LightweightChangeScanTests(unittest.TestCase):
    def assert_invalid(
        self, result: object, categories: set[str] | None = None
    ) -> dict[str, object]:
        self.assertEqual(result.returncode, 1, result.stderr)
        payload = json_output(result)
        self.assertEqual(payload["result"], "invalid")
        allowed = categories or {
            "layout",
            "metadata",
            "state",
            "date",
            "memory-root",
            "size",
        }
        self.assertIn(payload["error"]["category"], allowed)
        return payload

    def test_no_memory_root_is_empty_and_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            before = tree_snapshot(root)
            result = run_scan(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertEqual(payload["schema_version"], 1)
            self.assertEqual(payload["memory_root"], None)
            self.assertEqual(payload["changes_root"], None)
            self.assertEqual(
                payload["counts"],
                {
                    "completed": 0,
                    "human_review": 0,
                    "in_progress": 0,
                    "pending": 0,
                    "stopped": 0,
                    "total": 0,
                },
            )
            self.assertEqual(payload["pending_changes"], [])
            self.assertEqual(payload["human_review_changes"], [])
            self.assertEqual(payload["oldest_pending"], None)
            self.assertEqual(payload["trigger_reasons"], [])
            self.assertEqual(payload["result"], "not-triggered")
            self.assertEqual(tree_snapshot(root), before)

    def test_existing_root_without_changes_is_empty_and_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            memory_root = root / ".agent-loop"
            memory_root.mkdir()
            before = tree_snapshot(root)
            result = run_scan(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertEqual(payload["memory_root"], ".agent-loop")
            self.assertEqual(payload["changes_root"], None)
            self.assertEqual(payload["counts"]["total"], 0)
            self.assertFalse((memory_root / "changes").exists())
            self.assertEqual(tree_snapshot(root), before)

    def test_two_pending_changes_do_not_trigger_count(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            workspace.change("2026-07-18", "one")
            workspace.change("2026-07-18", "two")
            payload = json_output(run_scan(workspace.project_root))
            self.assertEqual(payload["counts"]["pending"], 2)
            self.assertEqual(payload["oldest_pending"]["age_days"], 0)
            self.assertNotIn("pending-count", payload["trigger_reasons"])
            self.assertEqual(payload["result"], "not-triggered")

    def test_three_pending_changes_across_months_trigger_count(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            workspace.change("2026-07-31", "one")
            workspace.change("2026-08-01", "two")
            workspace.change("2026-08-01", "three")
            result = run_scan(workspace.project_root, as_of="2026-08-01")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertEqual(payload["result"], "triggered")
            self.assertEqual(payload["trigger_reasons"], ["pending-count"])
            self.assertEqual(payload["counts"]["pending"], 3)
            self.assertEqual(payload["oldest_pending"]["age_days"], 1)
            self.assertEqual(payload["memory_root"], ".agent-loop")

    def test_exactly_seven_days_does_not_trigger_age(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            workspace.change("2026-07-11", "boundary")
            payload = json_output(run_scan(workspace.project_root))
            self.assertEqual(payload["oldest_pending"]["age_days"], 7)
            self.assertNotIn("pending-age", payload["trigger_reasons"])

    def test_more_than_seven_days_triggers_age(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            workspace.change("2026-07-10", "aged")
            payload = json_output(run_scan(workspace.project_root))
            self.assertEqual(payload["result"], "triggered")
            self.assertEqual(payload["trigger_reasons"], ["pending-age"])
            self.assertEqual(payload["oldest_pending"]["age_days"], 8)

    def test_in_progress_stopped_and_complete_do_not_count_pending(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            workspace.change(
                "2026-07-18",
                "active",
                status="in-progress",
                memory_evidence="pending: verification not complete",
                memory_target="pending: classify at completion",
            )
            workspace.change(
                "2026-07-18",
                "stopped",
                status="stopped",
                memory_review="complete",
                memory_result="none",
                memory_evidence="none: execution stopped before verification",
                memory_target="none: no durable fact was accepted",
            )
            workspace.change(
                "2026-07-18",
                "none",
                memory_review="complete",
                memory_result="none",
                memory_evidence="none: verified change has no durable fact",
                memory_target="none: no owning memory target",
            )
            workspace.change(
                "2026-07-18",
                "synced",
                memory_review="complete",
                memory_result="synced",
            )
            workspace.change("2026-07-18", "pending")
            result = run_scan(workspace.project_root)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertEqual(payload["counts"]["pending"], 1)
            self.assertEqual(payload["counts"]["in_progress"], 1)
            self.assertEqual(payload["counts"]["stopped"], 1)
            self.assertEqual(payload["counts"]["completed"], 3)

    def test_human_review_is_reported_separately(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            path = workspace.change(
                "2026-07-18",
                "human-choice",
                memory_review="complete",
                memory_result="human-review",
            )
            payload = json_output(run_scan(workspace.project_root))
            self.assertEqual(payload["counts"]["pending"], 0)
            self.assertEqual(payload["counts"]["human_review"], 1)
            paths = [row["path"] for row in payload["human_review_changes"]]
            self.assertIn(path.relative_to(workspace.project_root).as_posix(), paths)

    def test_existing_legacy_root_is_reused(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp), root_name="agent-loop")
            workspace.change("2026-07-18", "legacy")
            payload = json_output(run_scan(workspace.project_root))
            self.assertEqual(payload["memory_root"], "agent-loop")
            self.assertFalse((workspace.project_root / ".agent-loop").exists())

    def test_dual_memory_roots_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".agent-loop").mkdir()
            (root / "agent-loop").mkdir()
            payload = self.assert_invalid(run_scan(root), {"memory-root"})
            self.assertEqual(payload["error"]["category"], "memory-root")

    def test_invalid_root_shapes_fail_closed(self) -> None:
        cases = ("default-file", "legacy-file", "changes-file")
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                if case == "default-file":
                    (root / ".agent-loop").write_text("not a directory", encoding="utf-8")
                elif case == "legacy-file":
                    (root / "agent-loop").write_text("not a directory", encoding="utf-8")
                else:
                    (root / ".agent-loop").mkdir()
                    (root / ".agent-loop/changes").write_text("not a directory", encoding="utf-8")
                before = tree_snapshot(root)
                self.assert_invalid(run_scan(root), {"memory-root", "layout"})
                self.assertEqual(tree_snapshot(root), before)

        for case in ("changes-root-symlink",):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                target = root / "real"
                target.mkdir()
                try:
                    if case == "memory-root-symlink":
                        (root / ".agent-loop").symlink_to(target, target_is_directory=True)
                    else:
                        memory_root = root / ".agent-loop"
                        memory_root.mkdir()
                        (memory_root / "changes").symlink_to(target, target_is_directory=True)
                except OSError as error:
                    self.skipTest(f"host denies symlink creation: {error}")
                before = tree_snapshot(root)
                self.assert_invalid(run_scan(root), {"memory-root", "layout"})
                self.assertEqual(tree_snapshot(root), before)

    def test_internal_memory_root_alias_is_reused_with_logical_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            workspace.change("2026-07-18", "aliased-memory")
            real_memory = workspace.project_root / ".memory"
            workspace.memory_root.rename(real_memory)
            try:
                workspace.memory_root.symlink_to(".memory", target_is_directory=True)
            except OSError as error:
                self.skipTest(f"host denies symlink creation: {error}")

            result = run_scan(workspace.project_root)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertEqual(payload["memory_root"], ".agent-loop")
            self.assertEqual(payload["changes_root"], ".agent-loop/changes")
            self.assertEqual(payload["counts"]["total"], 1)

    def test_broken_and_external_memory_root_aliases_remain_invalid(self) -> None:
        for case in ("broken", "external"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
                root = Path(temp)
                try:
                    (root / ".agent-loop").symlink_to(
                        ".missing" if case == "broken" else Path(outside),
                        target_is_directory=True,
                    )
                except OSError as error:
                    self.skipTest(f"host denies symlink creation: {error}")
                payload = self.assert_invalid(run_scan(root), {"memory-root"})
                self.assertEqual(payload["error"]["category"], "memory-root")

    def test_directory_enumeration_error_is_normalized_without_absolute_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            changes_root = workspace.memory_root / "changes"
            changes_root.mkdir(parents=True)
            leaked_path = str(changes_root.resolve())
            with mock.patch.object(
                Path,
                "iterdir",
                side_effect=PermissionError(13, "permission denied", leaked_path),
            ):
                try:
                    build_scan(workspace.project_root, as_of=date.fromisoformat("2026-07-18"))
                except BaseException as error:
                    self.assertIsInstance(error, LightweightChangeContractError)
                    payload = error.to_payload()
                else:
                    self.fail("directory enumeration unexpectedly succeeded")

            self.assertEqual(payload["result"], "invalid")
            self.assertEqual(payload["error"]["category"], "layout")
            self.assertIn(".agent-loop/changes", payload["error"]["detail"])
            self.assertNotIn(leaked_path, str(payload))

    @unittest.skipIf(os.name == "nt", "POSIX permission bits are not portable to Windows")
    def test_unreadable_changes_root_returns_contract_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            changes_root = workspace.memory_root / "changes"
            changes_root.mkdir(parents=True)
            changes_root.chmod(0)
            try:
                result = run_scan(workspace.project_root)
                if result.returncode == 0:
                    self.skipTest("current host privileges bypass directory permission bits")
                self.assertEqual(result.stderr, "")
                payload = self.assert_invalid(result, {"layout"})
                self.assertIn(".agent-loop/changes", payload["error"]["detail"])
                self.assertNotIn(str(workspace.project_root.resolve()), result.stdout)
            finally:
                changes_root.chmod(0o700)

    def test_month_filename_and_created_at_must_match(self) -> None:
        cases = (
            {"month": "2026-06"},
            {"filename": "2026-07-17-mismatch.md"},
            {"filename": "2026-06-18-mismatch.md", "month": "2026-06"},
        )
        for overrides in cases:
            with self.subTest(overrides=overrides), tempfile.TemporaryDirectory() as temp:
                workspace = ChangeWorkspace(Path(temp))
                workspace.change("2026-07-18", "mismatch", **overrides)
                self.assert_invalid(run_scan(workspace.project_root), {"layout", "date"})

    def test_collision_suffix_is_part_of_topic_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            workspace.change("2026-07-18", "topic-2")
            result = run_scan(workspace.project_root)
            self.assertEqual(result.returncode, 0, result.stderr)

        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            path = workspace.change("2026-07-18", "topic", filename="2026-07-18-topic-2.md")
            self.assert_invalid(run_scan(workspace.project_root), {"metadata"})
            self.assertTrue(path.is_file())

    def test_flat_and_extra_nested_markdown_are_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            changes = workspace.memory_root / "changes"
            changes.mkdir(parents=True)
            (changes / "2026-07-18-flat.md").write_text("# invalid", encoding="utf-8")
            self.assert_invalid(run_scan(workspace.project_root), {"layout"})

        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            nested = workspace.memory_root / "changes/2026-07/extra"
            nested.mkdir(parents=True)
            (nested / "2026-07-18-nested.md").write_text("# invalid", encoding="utf-8")
            self.assert_invalid(run_scan(workspace.project_root), {"layout"})

    def test_non_markdown_month_companion_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            card = workspace.change("2026-07-18", "valid")
            companion = card.parent / "evidence.txt"
            companion.write_text("bounded companion", encoding="utf-8")
            before = tree_snapshot(workspace.project_root)
            payload = json_output(run_scan(workspace.project_root))
            self.assertEqual(payload["counts"]["total"], 1)
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_date_order_and_future_metadata_are_rejected(self) -> None:
        cases = (
            {"created_at": "2026-07-19", "topic": "future-created"},
            {
                "created_at": "2026-07-18",
                "topic": "future-updated",
                "updated_at": "2026-07-19",
            },
            {
                "created_at": "2026-07-18",
                "topic": "future-completed",
                "completed_at": "2026-07-19",
                "updated_at": "2026-07-19",
            },
            {
                "created_at": "2026-07-18",
                "topic": "reverse-completed",
                "completed_at": "2026-07-17",
            },
            {
                "created_at": "2026-07-17",
                "topic": "reverse-updated",
                "completed_at": "2026-07-18",
                "updated_at": "2026-07-17",
            },
        )
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temp:
                workspace = ChangeWorkspace(Path(temp))
                created_at = case.pop("created_at")
                topic = case.pop("topic")
                workspace.change(created_at, topic, **case)
                self.assert_invalid(run_scan(workspace.project_root), {"date"})

    def test_required_sections_and_memory_combinations_are_validated(self) -> None:
        headings = (
            "Background",
            "Goal / Completion Criteria",
            "Scope",
            "Lane Rationale",
            "Impact / Risk",
            "Plan",
            "Current Progress",
            "Verification",
            "Rollback",
            "Human Gates",
            "Result / Residuals",
            "Memory",
        )
        for heading in headings:
            with self.subTest(missing=heading), tempfile.TemporaryDirectory() as temp:
                workspace = ChangeWorkspace(Path(temp))
                path = workspace.change("2026-07-18", "missing-section")
                content = path.read_text(encoding="utf-8")
                path.write_text(content.replace(f"## {heading}\n", f"## Removed {heading}\n", 1), encoding="utf-8")
                self.assert_invalid(run_scan(workspace.project_root), {"metadata"})

        valid_cases = (
            {
                "status": "in-progress",
                "memory_review": "pending",
                "memory_result": "pending",
                "memory_evidence": "pending: verification not complete",
                "memory_target": "pending: classify at completion",
            },
            {
                "status": "stopped",
                "memory_review": "complete",
                "memory_result": "none",
                "memory_evidence": "none: execution stopped before verification",
                "memory_target": "none: no durable fact accepted",
            },
            {"memory_review": "pending", "memory_result": "pending"},
            {
                "memory_review": "complete",
                "memory_result": "none",
                "memory_evidence": "none: no durable fact",
                "memory_target": "none: no owning memory target",
            },
            {"memory_review": "complete", "memory_result": "synced"},
            {"memory_review": "complete", "memory_result": "human-review"},
        )
        for index, options in enumerate(valid_cases):
            with self.subTest(valid=index), tempfile.TemporaryDirectory() as temp:
                workspace = ChangeWorkspace(Path(temp))
                workspace.change("2026-07-18", f"valid-{index}", **options)
                result = run_scan(workspace.project_root)
                self.assertEqual(result.returncode, 0, result.stderr)

        invalid_cases = (
            {"memory_review": "complete", "memory_result": "pending"},
            {"memory_review": "pending", "memory_result": "none"},
            {"memory_review": "pending", "memory_result": "synced"},
            {"memory_review": "pending", "memory_result": "human-review"},
            {
                "status": "stopped",
                "memory_review": "pending",
                "memory_result": "pending",
            },
            {
                "status": "in-progress",
                "memory_review": "complete",
                "memory_result": "none",
                "memory_evidence": "none: not applicable",
                "memory_target": "none: not applicable",
            },
            {
                "memory_evidence": "pending: verification not complete",
                "memory_target": "pending: classify at completion",
            },
            {
                "memory_review": "complete",
                "memory_result": "none",
                "memory_evidence": "none",
                "memory_target": "none",
            },
            {
                "memory_review": "pending",
                "memory_result": "pending",
                "memory_evidence": "none: no actual verification locator",
                "memory_target": "pending: target remains unclassified",
            },
            {
                "memory_review": "complete",
                "memory_result": "synced",
                "memory_evidence": "pending: verification locator unavailable",
                "memory_target": ".agent-loop/project.md Capabilities",
            },
        )
        for index, options in enumerate(invalid_cases):
            with self.subTest(invalid=index), tempfile.TemporaryDirectory() as temp:
                workspace = ChangeWorkspace(Path(temp))
                workspace.change("2026-07-18", f"invalid-{index}", **options)
                self.assert_invalid(run_scan(workspace.project_root), {"state", "metadata"})

    def test_authoring_markers_are_rejected_outside_code_fences(self) -> None:
        cases = (
            (
                "Apply the declared change and pass the declared verification.",
                "<replace with the exact goal and observable completion criteria>",
            ),
            (
                "Memory Evidence: verified code and focused test",
                "Memory Evidence: <replace with the exact evidence locator>",
            ),
        )
        for index, (original, marker) in enumerate(cases):
            with self.subTest(case=index), tempfile.TemporaryDirectory() as temp:
                workspace = ChangeWorkspace(Path(temp))
                path = workspace.change("2026-07-18", f"placeholder-{index}")
                content = path.read_text(encoding="utf-8")
                path.write_text(content.replace(original, marker, 1), encoding="utf-8")
                self.assert_invalid(run_scan(workspace.project_root), {"metadata"})

    def test_fenced_markdown_is_ignored_for_structure_and_authoring_markers(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            path = workspace.change("2026-07-18", "fenced-evidence")
            content = path.read_text(encoding="utf-8")
            content = content.replace(
                "`python3 -m py_compile scripts/example.py` exited 0 in this run.",
                """```text
## Background
<replace with a literal template example>
```

`python3 -m py_compile scripts/example.py` exited 0 in this run.""",
                1,
            )
            content = content.replace(
                "Memory Target: .agent-loop/project.md Capabilities",
                """Memory Target: .agent-loop/project.md Capabilities

~~~text
Memory Target: example only
~~~""",
                1,
            )
            path.write_text(content, encoding="utf-8")
            result = run_scan(workspace.project_root)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_backtick_fence_cannot_hide_an_authoring_marker(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            path = workspace.change("2026-07-18", "invalid-fence")
            content = path.read_text(encoding="utf-8")
            content = content.replace(
                "`python3 -m py_compile scripts/example.py` exited 0 in this run.",
                """```invalid` <replace with hidden authoring content>

`python3 -m py_compile scripts/example.py` exited 0 in this run.""",
                1,
            )
            path.write_text(content, encoding="utf-8")
            self.assert_invalid(run_scan(workspace.project_root), {"metadata"})

    def test_git_context_allows_at_inside_valid_branch_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            path = workspace.change("2026-07-18", "at-branch")
            content = path.read_text(encoding="utf-8")
            content = content.replace(
                "feature/v1.5.1/example@0123456789abcdef0123456789abcdef01234567",
                "feature/v1.5.1/foo@bar@0123456789abcdef0123456789abcdef01234567",
                1,
            )
            path.write_text(content, encoding="utf-8")
            result = run_scan(workspace.project_root)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_as_of_is_usage_exit_two(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            result = run_scan(Path(temp), as_of="18-07-2026")
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertIn("usage", result.stderr.lower())

    def test_missing_project_root_is_usage_exit_two(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for project_root in (root / "missing", root / "file"):
                with self.subTest(project_root=project_root.name):
                    if project_root.name == "file":
                        project_root.write_text("not a root", encoding="utf-8")
                    result = run_scan(project_root)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, "")
                    self.assertTrue(
                        "usage" in result.stderr.lower()
                        or "directory" in result.stderr.lower()
                    )

    def test_valid_scan_is_deterministic_and_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            workspace.change("2026-07-18", "z-last")
            workspace.change("2026-07-17", "a-first")
            before = tree_snapshot(workspace.project_root)
            first = run_scan(workspace.project_root)
            second = run_scan(workspace.project_root)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(
                (first.returncode, first.stdout, first.stderr),
                (second.returncode, second.stdout, second.stderr),
            )
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_utf8_bom_and_crlf_are_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            path = workspace.change("2026-07-18", "bom-crlf")
            content = path.read_text(encoding="utf-8")
            path.write_bytes(("\ufeff" + content.replace("\n", "\r\n")).encode("utf-8"))
            result = run_scan(workspace.project_root)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_oversized_change_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ChangeWorkspace(Path(temp))
            path = workspace.change("2026-07-18", "oversized")
            path.write_bytes(path.read_bytes() + b"x" * (1024 * 1024))
            payload = self.assert_invalid(run_scan(workspace.project_root), {"size"})
            self.assertEqual(payload["error"]["category"], "size")

    def test_scanner_modules_use_only_stdlib_and_declared_local_support(self) -> None:
        allowed = {
            "scripts/lightweight_change_support.py": {"checker_support"},
            "scripts/scan-lightweight-changes.py": {
                "checker_support",
                "lightweight_change_support",
            },
        }
        for relative, local in allowed.items():
            with self.subTest(relative=relative):
                path = ROOT / relative
                self.assertTrue(path.is_file(), relative)
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                imported: set[str] = set()
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        imported.update(alias.name.split(".", 1)[0] for alias in node.names)
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        imported.add(node.module.split(".", 1)[0])
                external = imported - set(sys.stdlib_module_names) - local
                self.assertEqual(external, set(), f"{relative}: {sorted(external)}")


if __name__ == "__main__":
    unittest.main()

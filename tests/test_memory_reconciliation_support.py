from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from memory_reconciliation_support import (  # noqa: E402
    MemoryReconciliationError,
    canonical_plan_hash,
    extract_plan_payload,
    inventory_git_tree,
    inventory_worktree,
    resolve_memory_root,
    safe_relative_path,
    SnapshotEntry,
    union_inventories,
)
from tests.memory_reconciliation_test_support import (  # noqa: E402
    create_four_snapshot_workspace,
)


class MemoryReconciliationSupportTests(unittest.TestCase):
    def test_resolve_memory_root_accepts_dot_agent_loop(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".agent-loop").mkdir()
            self.assertEqual(resolve_memory_root(root), ".agent-loop")

    def test_resolve_memory_root_accepts_legacy_agent_loop(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "agent-loop").mkdir()
            self.assertEqual(resolve_memory_root(root), "agent-loop")

    def test_resolve_memory_root_rejects_both_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".agent-loop").mkdir()
            (root / "agent-loop").mkdir()
            with self.assertRaises(MemoryReconciliationError):
                resolve_memory_root(root)

    def test_tree_inventory_includes_directories_files_and_symlinks_without_following(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            memory = root / ".agent-loop"
            (memory / "nested").mkdir(parents=True)
            (memory / "nested/file.md").write_text("value\n", encoding="utf-8")
            os.symlink("nested/file.md", memory / "link.md")
            inventory = inventory_worktree(memory)
            self.assertEqual(inventory["nested"].kind, "directory")
            self.assertEqual(inventory["nested/file.md"].kind, "file")
            self.assertEqual(inventory["link.md"].kind, "symlink")
            self.assertNotEqual(
                inventory["link.md"].sha256, inventory["nested/file.md"].sha256
            )

    def test_union_inventory_includes_source_only_target_only_and_absence_claims(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = create_four_snapshot_workspace(Path(temp) / "repo")
            snapshots = {
                "base": inventory_git_tree(
                    workspace.project_root, workspace.merge_base_sha, ".agent-loop"
                ),
                "source": inventory_git_tree(
                    workspace.project_root, workspace.source_sha, ".agent-loop"
                ),
                "target_before": inventory_git_tree(
                    workspace.project_root, workspace.target_before_sha, ".agent-loop"
                ),
                "result": inventory_worktree(workspace.memory_root),
            }
            rows = union_inventories(snapshots)
            by_path = {row["path"]: row for row in rows}
            self.assertIn("source-only.md", by_path)
            self.assertIn("target-only.md", by_path)
            self.assertEqual(by_path["source-only.md"]["target_before"].state, "absent")
            self.assertEqual(by_path["target-only.md"]["source"].state, "absent")

    def test_casefold_collision_fails_closed(self) -> None:
        present = SnapshotEntry("present", "file", "100644", None, "a" * 64)
        with self.assertRaises(MemoryReconciliationError):
            union_inventories(
                {
                    "base": {"Feature.md": present},
                    "source": {"feature.md": present},
                    "target_before": {},
                    "result": {},
                }
            )

    def test_unicode_normalization_collision_fails_closed(self) -> None:
        present = SnapshotEntry("present", "file", "100644", None, "a" * 64)
        with self.assertRaises(MemoryReconciliationError):
            union_inventories(
                {
                    "base": {"caf\N{LATIN SMALL LETTER E WITH ACUTE}.md": present},
                    "source": {"cafe\N{COMBINING ACUTE ACCENT}.md": present},
                    "target_before": {},
                    "result": {},
                }
            )

    def test_canonical_plan_hash_is_root_independent(self) -> None:
        first = {
            "schema_version": 1,
            "report_id": "MM-0123456789ab",
            "expected_unchanged_paths": {"project.md": "a" * 64},
            "plan_sha256": "old",
        }
        second = dict(first)
        second["plan_sha256"] = "different"
        self.assertEqual(canonical_plan_hash(first), canonical_plan_hash(second))

    def test_report_parser_requires_exactly_one_plan_block(self) -> None:
        start = "<!-- memory-reconciliation-plan:start -->"
        end = "<!-- memory-reconciliation-plan:end -->"
        valid = f'{start}\n```json\n{{"schema_version":1}}\n```\n{end}\n'
        self.assertEqual(extract_plan_payload(valid)["schema_version"], 1)
        for invalid in ("", valid + valid, f"{start}\n{{}}\n{end}"):
            with self.subTest(invalid=invalid[:30]):
                with self.assertRaises(MemoryReconciliationError):
                    extract_plan_payload(invalid)

    def test_safe_path_rejects_parent_absolute_backslash_and_symlink_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            memory = Path(temp) / ".agent-loop"
            memory.mkdir()
            outside = Path(temp) / "outside"
            outside.mkdir()
            os.symlink(outside, memory / "escape")
            for value in ("../outside", "/absolute", "a\\b", "C:/drive", "."):
                with self.subTest(value=value):
                    with self.assertRaises(MemoryReconciliationError):
                        safe_relative_path(value, memory)
            with self.assertRaises(MemoryReconciliationError):
                safe_relative_path("escape/file.md", memory)
            self.assertEqual(
                safe_relative_path("safe/file.md", memory), memory / "safe/file.md"
            )


if __name__ == "__main__":
    unittest.main()

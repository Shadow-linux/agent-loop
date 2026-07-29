from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

from tests.feature_archive_test_support import (
    ArchiveWorkspace,
    json_output,
    run_archive_command,
    tree_snapshot,
)


class FeatureMonthlyArchiveCheckTests(unittest.TestCase):
    def scanned_plan(
        self,
        workspace: ArchiveWorkspace,
        *,
        operation: str = "archive",
        months: tuple[str, ...] = ("2026-05",),
        feature_ids: tuple[str, ...] = (),
    ) -> dict[str, object]:
        selection: list[str] = []
        for month in months:
            selection.extend(("--month", month))
        for feature_id in feature_ids:
            selection.extend(("--feature-id", feature_id))
        result = run_archive_command(
            "scan-feature-monthly-archive.py",
            "--project-root",
            str(workspace.project_root),
            "--operation",
            operation,
            *selection,
            "--as-of",
            "2026-07-14",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json_output(result)

    def apply(
        self,
        workspace: ArchiveWorkspace,
        payload: dict[str, object],
        *,
        operation: str = "archive",
        months: tuple[str, ...] = ("2026-05",),
        feature_ids: tuple[str, ...] = (),
        expected_hash: str | None = None,
        env: dict[str, str] | None = None,
    ):
        selection: list[str] = []
        for month in months:
            selection.extend(("--month", month))
        for feature_id in feature_ids:
            selection.extend(("--feature-id", feature_id))
        return run_archive_command(
            "apply-feature-monthly-archive.py",
            "--project-root",
            str(workspace.project_root),
            "--operation",
            operation,
            *selection,
            "--as-of",
            "2026-07-14",
            "--expected-plan-sha256",
            expected_hash or str(payload["plan_sha256"]),
            env=env,
        )

    def write_plan(
        self, workspace: ArchiveWorkspace, payload: dict[str, object]
    ) -> Path:
        path = workspace.project_root / "archive-plan.json"
        path.write_text(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        return path

    def check(self, workspace: ArchiveWorkspace, plan: Path):
        return run_archive_command(
            "check-feature-monthly-archive.py",
            "--project-root",
            str(workspace.project_root),
            "--operation",
            "archive",
            "--plan",
            str(plan),
        )

    def test_pre_check_is_read_only_and_accepts_current_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            workspace.feature("2026-05-08-login")
            plan = self.write_plan(workspace, self.scanned_plan(workspace))
            before = tree_snapshot(workspace.project_root)
            result = self.check(workspace, plan)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("PASS", result.stdout)
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_unsupported_reference_is_advisory_for_exact_plan_apply(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            source = workspace.feature(feature_id)
            ambiguous = workspace.write(
                "docs/ambiguous.md",
                f"# Ambiguous\n\nencoded=.agent-loop/features/{feature_id}%2Fspec.md\n",
            )
            original = ambiguous.read_bytes()
            payload = self.scanned_plan(workspace)
            self.assertTrue(
                any(
                    item["path"] == "docs/ambiguous.md"
                    and item["classification"] == "unsupported"
                    for item in payload["skipped_references"]
                )
            )

            result = self.apply(workspace, payload)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse(source.exists())
            self.assertTrue(
                (workspace.features_root / "2026-05" / feature_id).is_dir()
            )
            self.assertEqual(ambiguous.read_bytes(), original)

    def test_symlink_retarget_invalidates_previous_exact_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            source = workspace.feature(feature_id)
            (workspace.project_root / ".agents-a").mkdir()
            (workspace.project_root / ".agents-b").mkdir()
            alias = workspace.project_root / ".claude"
            try:
                alias.symlink_to(".agents-a", target_is_directory=True)
            except OSError as error:
                self.skipTest(f"directory symlink unavailable: {error}")
            payload = self.scanned_plan(workspace)

            alias.unlink()
            alias.symlink_to(".agents-b", target_is_directory=True)
            before = tree_snapshot(workspace.project_root)
            result = self.apply(workspace, payload)

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("stale-plan", result.stdout + result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)
            self.assertTrue(source.is_dir())

    def test_apply_rejects_feature_entry_symlink_before_transaction_or_move(self) -> None:
        scripts_dir = str(Path(__file__).resolve().parents[1] / "scripts")
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        from feature_archive_support import (
            ArchiveContractError,
            apply_archive_plan,
            build_archive_plan,
        )

        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            feature = workspace.feature(feature_id)
            plan = build_archive_plan(
                workspace.project_root,
                operation="archive",
                selected_months=("2026-05",),
                selected_feature_ids=(),
                as_of=date.fromisoformat("2026-07-14"),
            )
            payload_root = workspace.project_root / ".feature-payloads" / feature_id
            payload_root.parent.mkdir()
            feature.rename(payload_root)
            try:
                feature.symlink_to(payload_root, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"directory symlink unavailable: {error}")

            with self.assertRaisesRegex(ArchiveContractError, "stale-plan"):
                apply_archive_plan(
                    workspace.project_root,
                    plan,
                    expected_plan_sha256=plan.computed_sha256(),
                )

            self.assertTrue(feature.is_symlink())
            self.assertTrue(payload_root.is_dir())
            self.assertFalse((workspace.features_root / ".archive-txn").exists())

    def test_internal_memory_root_alias_applies_using_logical_plan_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            real_memory = workspace.project_root / ".memory"
            workspace.memory_root.rename(real_memory)
            try:
                workspace.memory_root.symlink_to(".memory", target_is_directory=True)
            except OSError as error:
                self.skipTest(f"directory symlink unavailable: {error}")

            payload = self.scanned_plan(workspace)
            result = self.apply(workspace, payload)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(
                (real_memory / "features" / "2026-05" / feature_id).is_dir()
            )
            self.assertFalse((real_memory / "features" / feature_id).exists())

    def test_memory_root_alias_retarget_invalidates_the_reviewed_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            first_memory = workspace.project_root / ".memory-a"
            second_memory = workspace.project_root / ".memory-b"
            workspace.memory_root.rename(first_memory)
            try:
                workspace.memory_root.symlink_to(
                    ".memory-a", target_is_directory=True
                )
            except OSError as error:
                self.skipTest(f"directory symlink unavailable: {error}")
            payload = self.scanned_plan(workspace)

            workspace.memory_root.unlink()
            first_memory.rename(second_memory)
            workspace.memory_root.symlink_to(
                ".memory-b", target_is_directory=True
            )
            before = tree_snapshot(workspace.project_root)
            result = self.apply(workspace, payload)

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("stale-plan", result.stdout + result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)
            self.assertFalse((second_memory / "features" / ".archive-txn").exists())

    def test_internal_memory_root_alias_restores_after_injected_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            workspace.write(
                ".agent-loop/project.md",
                f"# Project\n\nOwner: `.agent-loop/features/{feature_id}/spec.md`\n",
            )
            real_memory = workspace.project_root / ".memory"
            workspace.memory_root.rename(real_memory)
            try:
                workspace.memory_root.symlink_to(".memory", target_is_directory=True)
            except OSError as error:
                self.skipTest(f"directory symlink unavailable: {error}")
            payload = self.scanned_plan(workspace)
            before = tree_snapshot(workspace.project_root)

            result = self.apply(
                workspace,
                payload,
                env={
                    "AGENT_LOOP_ARCHIVE_TEST_MODE": "1",
                    "AGENT_LOOP_ARCHIVE_FAIL_AFTER": "2",
                },
            )

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("restore=complete", result.stdout + result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)
            self.assertTrue(workspace.memory_root.is_symlink())
            self.assertFalse((real_memory / "features" / ".archive-txn").exists())

    def test_reference_file_replaced_by_external_symlink_cannot_be_written(self) -> None:
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            source = workspace.feature(feature_id)
            reference = workspace.write(
                "docs/reference.md",
                f"# Reference\n\n.agent-loop/features/{feature_id}/spec.md\n",
            )
            payload = self.scanned_plan(workspace)
            external = Path(outside) / "external.md"
            external.write_text("must stay unchanged\n", encoding="utf-8")
            reference.unlink()
            try:
                reference.symlink_to(external)
            except OSError as error:
                self.skipTest(f"file symlink unavailable: {error}")
            before_external = external.read_bytes()

            result = self.apply(workspace, payload)

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("stale-plan", result.stdout + result.stderr)
            self.assertEqual(external.read_bytes(), before_external)
            self.assertTrue(reference.is_symlink())
            self.assertTrue(source.is_dir())

    def test_pre_check_rejects_snapshot_drift_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature = workspace.feature("2026-05-08-login")
            plan = self.write_plan(workspace, self.scanned_plan(workspace))
            (feature / "notes.md").write_text(
                (feature / "notes.md").read_text(encoding="utf-8") + "\nchanged\n",
                encoding="utf-8",
                newline="\n",
            )
            before = tree_snapshot(workspace.project_root)
            result = self.check(workspace, plan)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("stale-plan", result.stdout + result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_check_rejects_self_hashed_plan_path_escape_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            workspace.feature("2026-05-08-login")
            payload = self.scanned_plan(workspace)
            payload["moves"][0]["source"] = "../escaped-feature"
            unsigned = dict(payload)
            unsigned.pop("plan_sha256")
            payload["plan_sha256"] = hashlib.sha256(
                json.dumps(
                    unsigned,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest()
            plan = self.write_plan(workspace, payload)
            before = tree_snapshot(workspace.project_root)
            result = self.check(workspace, plan)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("path-escape", result.stdout + result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_post_check_accepts_exact_moves_index_and_reference_edits(self) -> None:
        scripts_dir = str(Path(__file__).resolve().parents[1] / "scripts")
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        from feature_archive_support import ArchiveEntry, render_archive_index

        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            workspace.write(
                ".agent-loop/project.md",
                f"# Project\n\nDelivered: `.agent-loop/features/{feature_id}/spec.md`\n",
            )
            payload = self.scanned_plan(workspace)
            plan = self.write_plan(workspace, payload)
            for move in payload["moves"]:
                source = workspace.project_root / move["source"]
                target = workspace.project_root / move["target"]
                target.parent.mkdir(parents=True, exist_ok=True)
                source.rename(target)
            for edit in payload["reference_edits"]:
                target = workspace.project_root / edit["path"]
                content = target.read_text(encoding="utf-8")
                self.assertEqual(content.count(edit["old"]), edit["occurrences"])
                target.write_text(
                    content.replace(edit["old"], edit["new"]),
                    encoding="utf-8",
                    newline="\n",
                )
            entries = [ArchiveEntry(**entry) for entry in payload["archive_entries"]]
            workspace.write(
                ".agent-loop/features/archive.md", render_archive_index(entries)
            )
            before = tree_snapshot(workspace.project_root)
            result = self.check(workspace, plan)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("PASS", result.stdout)
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_apply_moves_two_closed_features_intact_and_updates_archive_index(self) -> None:
        scripts_dir = str(Path(__file__).resolve().parents[1] / "scripts")
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        from feature_archive_support import parse_archive_index

        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            first = workspace.feature("2026-05-08-login")
            second = workspace.feature("2026-06-12-payment")
            (first / "payload.bin").write_bytes(b"\x00login\xff")
            (second / "payload.bin").write_bytes(b"\x00payment\xff")
            first_before = tree_snapshot(first)
            second_before = tree_snapshot(second)
            payload = self.scanned_plan(
                workspace, months=("2026-05", "2026-06")
            )
            result = self.apply(
                workspace, payload, months=("2026-05", "2026-06")
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(first.exists())
            self.assertFalse(second.exists())
            first_target = workspace.features_root / "2026-05" / first.name
            second_target = workspace.features_root / "2026-06" / second.name
            self.assertEqual(tree_snapshot(first_target), first_before)
            self.assertEqual(tree_snapshot(second_target), second_before)
            entries = parse_archive_index(workspace.memory_root)
            self.assertEqual(
                [entry.feature_id for entry in entries],
                ["2026-05-08-login", "2026-06-12-payment"],
            )

    def test_apply_rejects_valid_but_different_plan_hash_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            workspace.feature("2026-05-08-login")
            payload = self.scanned_plan(workspace)
            before = tree_snapshot(workspace.project_root)
            wrong = ("0" if payload["plan_sha256"][0] != "0" else "1") + payload[
                "plan_sha256"
            ][1:]
            result = self.apply(workspace, payload, expected_hash=wrong)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("stale-plan", result.stdout + result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_apply_rejects_state_drift_after_scan(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature = workspace.feature("2026-05-08-login")
            payload = self.scanned_plan(workspace)
            notes = feature / "notes.md"
            notes.write_text(
                notes.read_text(encoding="utf-8") + "\nstate drift\n",
                encoding="utf-8",
                newline="\n",
            )
            before = tree_snapshot(workspace.project_root)
            result = self.apply(workspace, payload)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("stale-plan", result.stdout + result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)
            self.assertFalse(
                (workspace.features_root / ".archive-txn").exists()
            )

    def test_apply_rejects_stranded_transaction_created_after_scan(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature = workspace.feature("2026-05-08-login")
            payload = self.scanned_plan(workspace)
            transaction_id = "20260714T120000Z-0123456789ab"
            transaction = workspace.features_root / ".archive-txn" / transaction_id
            transaction.mkdir(parents=True)
            before = tree_snapshot(workspace.project_root)

            result = self.apply(workspace, payload)

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("stranded-transaction", result.stdout + result.stderr)
            self.assertIn(transaction_id, result.stdout + result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)
            self.assertTrue(feature.is_dir())

    def test_apply_updates_relative_link_from_project_memory_into_feature(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            project = workspace.write(
                ".agent-loop/project.md",
                f"# Project\n\n[Feature](features/{feature_id}/spec.md)\n",
            )
            payload = self.scanned_plan(workspace)

            result = self.apply(workspace, payload)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                f"features/2026-05/{feature_id}/spec.md",
                project.read_text(encoding="utf-8"),
            )
            self.assertTrue(
                (workspace.features_root / "2026-05" / feature_id / "spec.md").is_file()
            )

    def test_apply_updates_only_precomputed_reference_edits(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            old = f".agent-loop/features/{feature_id}/spec.md"
            new = f".agent-loop/features/2026-05/{feature_id}/spec.md"
            for relative in (
                ".agent-loop/project.md",
                ".agent-loop/requirements/2026-05-login/README.md",
                ".agent-loop/decisions/ADR-001-login.md",
            ):
                workspace.write(relative, f"# Locator\n\nOwner: `{old}`\n")
            requirement = workspace.write(
                ".agent-loop/requirements/2026-05-login/requirement.md",
                f"# Original Requirement\n\nOriginal path: `{old}`\n",
            )
            unrelated = workspace.write("docs/unrelated.md", "# Unrelated\n\nkeep bytes\n")
            requirement_before = requirement.read_bytes()
            unrelated_before = unrelated.read_bytes()
            payload = self.scanned_plan(workspace)
            result = self.apply(workspace, payload)
            self.assertEqual(result.returncode, 0, result.stderr)
            for relative in (
                ".agent-loop/project.md",
                ".agent-loop/requirements/2026-05-login/README.md",
                ".agent-loop/decisions/ADR-001-login.md",
            ):
                content = (workspace.project_root / relative).read_text(encoding="utf-8")
                self.assertIn(new, content)
                self.assertNotIn(old, content)
            self.assertEqual(requirement.read_bytes(), requirement_before)
            self.assertEqual(unrelated.read_bytes(), unrelated_before)

    def test_apply_preserves_bom_and_crlf_while_updating_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            old = f".agent-loop/features/{feature_id}/spec.md"
            new = f".agent-loop/features/2026-05/{feature_id}/spec.md"
            project = workspace.memory_root / "project.md"
            project.parent.mkdir(parents=True, exist_ok=True)
            project.write_bytes(
                b"\xef\xbb\xbf"
                + f"# Project\r\n\r\nOwner: `{old}`\r\n".encode("utf-8")
            )
            payload = self.scanned_plan(workspace)
            result = self.apply(workspace, payload)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            updated = project.read_bytes()
            self.assertTrue(updated.startswith(b"\xef\xbb\xbf"))
            self.assertIn(new.encode("utf-8"), updated)
            self.assertNotIn(old.encode("utf-8"), updated)
            self.assertIn(b"\r\n", updated)
            self.assertNotIn(b"\n", updated.replace(b"\r\n", b""))

    def test_apply_is_idempotent_and_never_nests_month_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            first_plan = self.scanned_plan(workspace)
            first = self.apply(workspace, first_plan)
            self.assertEqual(first.returncode, 0, first.stderr)
            second_plan = self.scanned_plan(workspace)
            self.assertEqual(second_plan["moves"], [])
            self.assertIn(
                "already-archived", second_plan["candidates"][0]["blockers"]
            )
            before = tree_snapshot(workspace.project_root)
            second = self.apply(workspace, second_plan)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)
            self.assertFalse(
                (
                    workspace.features_root
                    / "2026-05"
                    / "2026-05"
                    / feature_id
                ).exists()
            )

    def test_injected_reference_write_failure_restores_directories_and_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            workspace.write(
                ".agent-loop/project.md",
                f"# Project\n\nOwner: `.agent-loop/features/{feature_id}/spec.md`\n",
            )
            payload = self.scanned_plan(workspace)
            before = tree_snapshot(workspace.project_root)
            result = self.apply(
                workspace,
                payload,
                env={
                    "AGENT_LOOP_ARCHIVE_TEST_MODE": "1",
                    "AGENT_LOOP_ARCHIVE_FAIL_AFTER": "3",
                },
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("restore=complete", result.stdout + result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)
            self.assertFalse((workspace.features_root / ".archive-txn").exists())

    def test_failure_injection_is_rejected_outside_explicit_test_mode(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            workspace.feature("2026-05-08-login")
            payload = self.scanned_plan(workspace)
            before = tree_snapshot(workspace.project_root)
            result = self.apply(
                workspace,
                payload,
                env={"AGENT_LOOP_ARCHIVE_FAIL_AFTER": "1"},
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("test-only", result.stdout + result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_rehydrate_moves_archived_feature_flat_and_updates_locator(self) -> None:
        scripts_dir = str(Path(__file__).resolve().parents[1] / "scripts")
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        from feature_archive_support import parse_archive_index

        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            archive_plan = self.scanned_plan(workspace)
            archived = self.apply(workspace, archive_plan)
            self.assertEqual(archived.returncode, 0, archived.stderr)
            rehydrate_plan = self.scanned_plan(
                workspace,
                operation="rehydrate",
                months=(),
                feature_ids=(feature_id,),
            )
            result = self.apply(
                workspace,
                rehydrate_plan,
                operation="rehydrate",
                months=(),
                feature_ids=(feature_id,),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(
                (workspace.features_root / "2026-05" / feature_id).exists()
            )
            flat = workspace.features_root / feature_id
            self.assertTrue(flat.is_dir())
            self.assertIn("Status: closed", (flat / "spec.md").read_text(encoding="utf-8"))
            entry = parse_archive_index(workspace.memory_root)[0]
            self.assertEqual(entry.archive_state, "rehydrated")
            self.assertEqual(
                entry.current_path, f".agent-loop/features/{feature_id}/"
            )


if __name__ == "__main__":
    unittest.main()

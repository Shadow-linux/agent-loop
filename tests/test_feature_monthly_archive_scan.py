from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.feature_archive_test_support import (
    ArchiveWorkspace,
    json_output,
    run_archive_command,
    tree_snapshot,
)
from tests.test_feature_archive_support import ARCHIVE_HEADER, archive_row


TRANSACTION_ID = "20260714T120000Z-0123456789ab"


class FeatureMonthlyArchiveScanTests(unittest.TestCase):
    def scan(self, workspace: ArchiveWorkspace, *args: str):
        return run_archive_command(
            "scan-feature-monthly-archive.py",
            "--project-root",
            str(workspace.project_root),
            *args,
        )

    def test_scan_selects_closed_features_across_two_months_and_preserves_blocked(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            workspace.feature("2026-05-08-login")
            workspace.feature("2026-05-22-import", status="paused")
            workspace.feature("2026-06-12-payment")
            before = tree_snapshot(workspace.project_root)
            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--month",
                "2026-06",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertEqual(
                [move["feature_id"] for move in payload["moves"]],
                ["2026-05-08-login", "2026-06-12-payment"],
            )
            self.assertIn(
                "2026-05-22-import",
                [item["feature_id"] for item in payload["candidates"]],
            )
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_scan_snapshots_large_feature_payload_for_intact_move_check(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature = workspace.feature("2026-05-08-login")
            payload_file = feature / "large-payload.bin"
            payload_file.write_bytes(b"x" * (2 * 1024 * 1024 + 1))
            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertIn(
                ".agent-loop/features/2026-05-08-login/large-payload.bin",
                payload["snapshots"],
            )

    def test_current_month_is_blocked_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            workspace.feature("2026-07-01-current")
            before = tree_snapshot(workspace.project_root)
            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-07",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertEqual(payload["moves"], [])
            self.assertIn("current-month", payload["candidates"][0]["blockers"])
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_active_blocked_and_paused_lifecycles_are_ineligible(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            for day, status in (("08", "active"), ("09", "blocked"), ("10", "paused")):
                workspace.feature(f"2026-05-{day}-{status}", status=status)
            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertEqual(payload["moves"], [])
            for candidate in payload["candidates"]:
                self.assertIn("lifecycle", " ".join(candidate["blockers"]))

    def test_incomplete_close_evidence_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            workspace.feature("2026-05-08-login", close_complete=False)
            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertEqual(payload["moves"], [])
            self.assertEqual(payload["candidates"][0]["close_evidence"], "incomplete")

    def test_missing_archive_readiness_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature = workspace.feature("2026-05-08-login")
            notes = feature / "notes.md"
            notes.write_text(
                notes.read_text(encoding="utf-8").split("## Archive Readiness", 1)[0],
                encoding="utf-8",
                newline="\n",
            )
            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertIn(
                "missing-archive-readiness", payload["candidates"][0]["blockers"]
            )

    def test_placeholder_delivered_summary_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature = workspace.feature("2026-05-08-login")
            notes = feature / "notes.md"
            notes.write_text(
                notes.read_text(encoding="utf-8").replace(
                    "Delivered Summary: completed 2026-05-08-login",
                    "Delivered Summary: TODO",
                ),
                encoding="utf-8",
                newline="\n",
            )
            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertIn(
                "non-concrete-delivered-summary",
                payload["candidates"][0]["blockers"],
            )

    def test_non_terminal_archive_readiness_value_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature = workspace.feature("2026-05-08-login")
            notes = feature / "notes.md"
            notes.write_text(
                notes.read_text(encoding="utf-8").replace(
                    "Verification: complete", "Verification: pending"
                ),
                encoding="utf-8",
                newline="\n",
            )
            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertIn(
                "archive-readiness-verification:pending",
                payload["candidates"][0]["blockers"],
            )

    def test_open_follow_up_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature = workspace.feature("2026-05-08-login")
            notes = feature / "notes.md"
            notes.write_text(
                notes.read_text(encoding="utf-8").replace(
                    "Open Follow-up: none", "Open Follow-up: FU-17"
                ),
                encoding="utf-8",
                newline="\n",
            )
            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertEqual(payload["moves"], [])
            self.assertEqual(payload["candidates"][0]["open_follow_up"], "FU-17")

    def test_flat_and_month_path_collision_fails_closed_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            workspace.feature("2026-05-08-login")
            archived = workspace.features_root / "2026-05" / "2026-05-08-login"
            archived.mkdir(parents=True)
            before = tree_snapshot(workspace.project_root)
            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("path-collision", result.stdout + result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_project_memory_active_or_paused_feature_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            workspace.feature("2026-05-08-login")
            workspace.write(
                ".agent-loop/project.md",
                "# Project\n\nActive Feature: 2026-05-08-login\nPaused Features: none\n",
            )
            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertIn("project-memory-active", payload["candidates"][0]["blockers"])

    def test_scan_precomputes_literal_and_relative_link_edits(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            feature = workspace.feature(feature_id)
            workspace.write(
                ".agent-loop/project.md",
                f"# Project\n\nDelivered: `.agent-loop/features/{feature_id}/spec.md`\n",
            )
            workspace.write(
                f".agent-loop/features/{feature_id}/links.md",
                "# Links\n\n[Project memory](../../project.md)\n"
                "[External](https://example.com/docs)\n",
            )
            before = tree_snapshot(workspace.project_root)
            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            edits = payload["reference_edits"]
            self.assertTrue(
                any(
                    edit["kind"] == "literal-path"
                    and edit["path"] == ".agent-loop/project.md"
                    and edit["new"]
                    == f".agent-loop/features/2026-05/{feature_id}/"
                    for edit in edits
                )
            )
            self.assertTrue(
                any(
                    edit["kind"] == "relative-link"
                    and edit["path"]
                    == f".agent-loop/features/{feature_id}/links.md"
                    and edit["old"] == "../../project.md"
                    and edit["new"] == "../../../project.md"
                    for edit in edits
                )
            )
            self.assertTrue(feature.is_dir())
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_internal_directory_symlink_is_reported_without_blocking_or_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            agents = workspace.project_root / ".agents"
            agents.mkdir()
            workspace.write(
                ".agents/feature-reference.md",
                f"# Agent Reference\n\n.agent-loop/features/{feature_id}/spec.md\n",
            )
            alias = workspace.project_root / ".claude"
            try:
                alias.symlink_to(".agents", target_is_directory=True)
            except OSError as error:
                self.skipTest(f"directory symlink unavailable: {error}")

            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json_output(result)
            findings = [
                item
                for item in payload["skipped_references"]
                if item["classification"] == "reference-scan-symlink"
            ]
            self.assertEqual(
                findings,
                [
                    {
                        "path": ".claude",
                        "classification": "reference-scan-symlink",
                        "matched_value": "directory:internal:.agents",
                        "reason": "not-followed",
                    }
                ],
            )
            self.assertTrue(
                any(
                    edit["path"] == ".agents/feature-reference.md"
                    for edit in payload["reference_edits"]
                )
            )
            self.assertFalse(
                any(
                    edit["path"].startswith(".claude/")
                    for edit in payload["reference_edits"]
                )
            )

    def test_feature_entry_symlink_is_reported_but_not_planned_as_a_move(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            feature = workspace.feature(feature_id)
            payload_root = workspace.project_root / ".feature-payloads" / feature_id
            payload_root.parent.mkdir()
            feature.rename(payload_root)
            try:
                feature.symlink_to(payload_root, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"directory symlink unavailable: {error}")

            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            plan = json_output(result)
            self.assertEqual(plan["moves"], [])
            self.assertIn("feature-entry-symlink", plan["candidates"][0]["blockers"])
            self.assertIn(
                {
                    "path": f".agent-loop/features/{feature_id}",
                    "classification": "feature-entry-symlink",
                    "matched_value": f"directory:internal:.feature-payloads/{feature_id}",
                    "reason": "not-a-movable-directory-entry",
                },
                plan["skipped_references"],
            )

    def test_internal_memory_root_alias_keeps_logical_agent_loop_plan_paths(self) -> None:
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

            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            plan = json_output(result)
            self.assertEqual(
                plan["moves"],
                [
                    {
                        "feature_id": feature_id,
                        "month": "2026-05",
                        "source": f".agent-loop/features/{feature_id}",
                        "target": f".agent-loop/features/2026-05/{feature_id}",
                    }
                ],
            )
            self.assertIn(
                {
                    "path": ".agent-loop",
                    "classification": "memory-root-alias",
                    "matched_value": "directory:internal:.memory",
                    "reason": "verified-logical-alias",
                },
                plan["skipped_references"],
            )

    def test_broken_cyclic_and_external_memory_root_aliases_fail_physically(self) -> None:
        for case in ("broken", "cyclic", "external"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
                workspace = ArchiveWorkspace(Path(temp))
                try:
                    if case == "broken":
                        workspace.memory_root.symlink_to(
                            ".missing-memory", target_is_directory=True
                        )
                    elif case == "cyclic":
                        workspace.memory_root.symlink_to(
                            ".memory-cycle", target_is_directory=True
                        )
                        (workspace.project_root / ".memory-cycle").symlink_to(
                            ".agent-loop", target_is_directory=True
                        )
                    else:
                        workspace.memory_root.symlink_to(
                            Path(outside), target_is_directory=True
                        )
                except OSError as error:
                    self.skipTest(f"directory symlink unavailable: {error}")

                result = self.scan(
                    workspace,
                    "--operation",
                    "archive",
                    "--month",
                    "2026-05",
                    "--as-of",
                    "2026-07-14",
                )
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("memory-root", result.stdout + result.stderr)
                self.assertNotIn(str(Path(outside).resolve()), result.stdout + result.stderr)

    def test_external_broken_and_cyclic_directory_symlinks_are_advisory(self) -> None:
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            workspace = ArchiveWorkspace(Path(temp))
            workspace.feature("2026-05-08-login")
            external = workspace.project_root / ".external-docs"
            broken = workspace.project_root / ".broken-docs"
            first = workspace.project_root / ".cycle-a"
            second = workspace.project_root / ".cycle-b"
            try:
                external.symlink_to(Path(outside), target_is_directory=True)
                broken.symlink_to(".missing-docs", target_is_directory=True)
                first.symlink_to(".cycle-b", target_is_directory=True)
                second.symlink_to(".cycle-a", target_is_directory=True)
            except OSError as error:
                self.skipTest(f"directory symlink unavailable: {error}")

            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn(str(Path(outside).resolve()), result.stdout)
            payload = json_output(result)
            findings = {
                item["path"]: item["matched_value"]
                for item in payload["skipped_references"]
                if item["classification"] == "reference-scan-symlink"
            }
            self.assertEqual(findings[".external-docs"], "directory:external")
            self.assertEqual(findings[".broken-docs"], "entry:broken")
            self.assertEqual(findings[".cycle-a"], "entry:cycle")
            self.assertEqual(findings[".cycle-b"], "entry:cycle")

    def test_symlinked_markdown_is_advisory_and_real_file_is_scanned_once(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            workspace.write(
                ".agents/guide.md",
                f"# Guide\n\n.agent-loop/features/{feature_id}/spec.md\n",
            )
            alias = workspace.project_root / "docs/guide.md"
            alias.parent.mkdir()
            try:
                alias.symlink_to("../.agents/guide.md")
            except OSError as error:
                self.skipTest(f"file symlink unavailable: {error}")

            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json_output(result)
            self.assertIn(
                {
                    "path": "docs/guide.md",
                    "classification": "reference-scan-symlink",
                    "matched_value": "markdown-file:internal:.agents/guide.md",
                    "reason": "not-followed",
                },
                payload["skipped_references"],
            )
            edited_paths = [item["path"] for item in payload["reference_edits"]]
            self.assertEqual(edited_paths.count(".agents/guide.md"), 1)
            self.assertNotIn("docs/guide.md", edited_paths)

    def test_symlink_target_change_changes_plan_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            workspace.feature("2026-05-08-login")
            (workspace.project_root / ".agents-a").mkdir()
            (workspace.project_root / ".agents-b").mkdir()
            alias = workspace.project_root / ".claude"
            try:
                alias.symlink_to(".agents-a", target_is_directory=True)
            except OSError as error:
                self.skipTest(f"directory symlink unavailable: {error}")

            first = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            first_hash = json_output(first)["plan_sha256"]

            alias.unlink()
            alias.symlink_to(".agents-b", target_is_directory=True)
            second = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            self.assertNotEqual(first_hash, json_output(second)["plan_sha256"])

    def test_requirement_sources_and_historical_reports_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            old_path = f".agent-loop/features/{feature_id}/spec.md"
            workspace.write(
                ".agent-loop/requirements/2026-05-login/requirement.md",
                f"# Human Requirement\n\nOriginal evidence: `{old_path}`\n",
            )
            workspace.write(
                "docs/reports/2026-05-login-validation.md",
                f"# Historical Validation Report\n\nAt execution time: `{old_path}`\n",
            )
            before = tree_snapshot(workspace.project_root)
            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            classifications = {
                item["path"]: item["classification"]
                for item in payload["skipped_references"]
            }
            self.assertEqual(
                classifications[
                    ".agent-loop/requirements/2026-05-login/requirement.md"
                ],
                "immutable-requirement-source",
            )
            self.assertEqual(
                classifications["docs/reports/2026-05-login-validation.md"],
                "historical-evidence",
            )
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_ambiguous_old_path_reference_blocks_apply(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            workspace.write(
                "docs/ambiguous.md",
                f"# Ambiguous\n\nencoded=.agent-loop/features/{feature_id}%2Fspec.md\n",
            )
            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertTrue(
                any(
                    item["path"] == "docs/ambiguous.md"
                    and item["classification"] == "unsupported"
                    for item in payload["skipped_references"]
                )
            )

    def test_large_markdown_with_old_path_is_unsupported_without_reading_it(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            large = workspace.project_root / "docs/large.md"
            large.parent.mkdir(parents=True)
            large.write_bytes(
                f".agent-loop/features/{feature_id}/".encode("utf-8")
                + b"x" * (2 * 1024 * 1024 + 1)
            )
            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertTrue(
                any(
                    item["path"] == "docs/large.md"
                    and item["classification"] == "unsupported"
                    for item in payload["skipped_references"]
                )
            )

    def test_rehydrate_scan_plans_month_to_flat_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            source = workspace.feature(feature_id)
            archived = workspace.features_root / "2026-05" / feature_id
            archived.parent.mkdir(parents=True)
            source.rename(archived)
            workspace.write(
                ".agent-loop/features/archive.md",
                ARCHIVE_HEADER + archive_row(feature_id),
            )
            before = tree_snapshot(workspace.project_root)
            result = self.scan(
                workspace,
                "--operation",
                "rehydrate",
                "--feature-id",
                feature_id,
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            self.assertEqual(
                payload["moves"],
                [
                    {
                        "feature_id": feature_id,
                        "month": "2026-05",
                        "source": f".agent-loop/features/2026-05/{feature_id}",
                        "target": f".agent-loop/features/{feature_id}",
                    }
                ],
            )
            self.assertEqual(tree_snapshot(workspace.project_root), before)

    def test_broken_cross_boundary_relative_link_blocks_apply(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            workspace.write(
                f".agent-loop/features/{feature_id}/links.md",
                "# Links\n\n[missing](../../missing.md)\n",
            )
            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json_output(result)
            unsupported = [
                item
                for item in payload["skipped_references"]
                if item["classification"] == "unsupported"
            ]
            self.assertTrue(unsupported)
            self.assertIn("broken", unsupported[0]["reason"])

    def test_scan_rewrites_relative_link_from_project_memory_into_feature(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            workspace.feature(feature_id)
            workspace.write(
                ".agent-loop/project.md",
                f"# Project\n\n[Feature](features/{feature_id}/spec.md)\n",
            )

            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json_output(result)
            self.assertTrue(
                any(
                    edit["kind"] == "relative-link"
                    and edit["path"] == ".agent-loop/project.md"
                    and edit["old"] == f"features/{feature_id}/spec.md"
                    and edit["new"]
                    == f"features/2026-05/{feature_id}/spec.md"
                    for edit in payload["reference_edits"]
                )
            )

    def test_scan_rejects_stranded_archive_transaction(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            workspace.feature("2026-05-08-login")
            transaction = workspace.features_root / ".archive-txn" / TRANSACTION_ID
            transaction.mkdir(parents=True)
            before = tree_snapshot(workspace.project_root)

            result = self.scan(
                workspace,
                "--operation",
                "archive",
                "--month",
                "2026-05",
                "--as-of",
                "2026-07-14",
            )

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("stranded-transaction", result.stdout + result.stderr)
            self.assertIn(TRANSACTION_ID, result.stdout + result.stderr)
            self.assertEqual(tree_snapshot(workspace.project_root), before)


if __name__ == "__main__":
    unittest.main()

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

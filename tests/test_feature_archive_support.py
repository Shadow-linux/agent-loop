from __future__ import annotations

import importlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.checker_test_support import ROOT
from tests.feature_archive_test_support import ArchiveWorkspace, tree_snapshot


ARCHIVE_HEADER = """# Feature Archive

This file locates archived or rehydrated features. Feature specs, tests, notes, requirement sources, and accepted decisions remain authoritative.

| Feature ID | Month | Current Path | Archive State | Closed At | Delivered Summary | Source Requirements | Applicable Decisions | Last Moved At |
|---|---|---|---|---|---|---|---|---|
"""


def archive_row(
    feature_id: str,
    *,
    month: str = "2026-05",
    path: str | None = None,
    state: str = "archived",
    summary: str | None = None,
) -> str:
    current = path or f".agent-loop/features/{month}/{feature_id}/"
    delivered = summary or f"completed {feature_id}"
    return (
        f"| {feature_id} | {month} | `{current}` | {state} | 2026-05-20 | "
        f"{delivered} | none | none | 2026-07-14 |\n"
    )


class FeatureArchiveSupportTests(unittest.TestCase):
    def checker_support(self):
        scripts_dir = str(ROOT / "scripts")
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        module = importlib.import_module("checker_support")
        for name in (
            "atomic_write_bytes",
            "canonical_json_bytes",
            "sha256_bytes",
            "strip_code_span",
        ):
            self.assertTrue(hasattr(module, name), f"missing production helper: {name}")
        return module

    def support(self):
        support_path = ROOT / "scripts/feature_archive_support.py"
        self.assertTrue(support_path.is_file(), f"missing production support: {support_path}")
        scripts_dir = str(ROOT / "scripts")
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        return importlib.import_module("feature_archive_support")

    def test_archive_template_exists_with_exact_empty_table(self) -> None:
        template = ROOT / "templates/feature-archive.md"
        self.assertTrue(template.is_file(), f"missing archive template: {template}")
        self.assertEqual(template.read_text(encoding="utf-8"), ARCHIVE_HEADER)

    def test_canonical_helpers_use_stable_utf8_bytes(self) -> None:
        checker_support = self.checker_support()
        expected = '{"a":"登录","z":1}'.encode("utf-8")
        self.assertEqual(
            checker_support.canonical_json_bytes({"z": 1, "a": "登录"}), expected
        )
        self.assertEqual(
            checker_support.sha256_bytes(expected),
            "c92ecc89f697b155c8d5fb7417e18732f61b69c1375d6811c329822bf34f3500",
        )
        self.assertEqual(checker_support.strip_code_span(" `value` "), "value")

    def test_atomic_write_bytes_replaces_existing_file(self) -> None:
        checker_support = self.checker_support()
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "nested" / "artifact.md"
            target.parent.mkdir()
            target.write_bytes(b"before")
            checker_support.atomic_write_bytes(target, "完成".encode("utf-8"))
            self.assertEqual(target.read_bytes(), "完成".encode("utf-8"))
            self.assertEqual(list(target.parent.glob(f".{target.name}.*")), [])

    def test_atomic_write_bytes_cleans_temporary_file_after_replace_failure(self) -> None:
        checker_support = self.checker_support()
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "artifact.md"
            with mock.patch.object(
                checker_support.os, "replace", side_effect=OSError("injected replace failure")
            ):
                with self.assertRaisesRegex(OSError, "injected replace failure"):
                    checker_support.atomic_write_bytes(target, b"new")
            self.assertFalse(target.exists())
            self.assertEqual(list(target.parent.glob(f".{target.name}.*")), [])

    def test_flat_feature_resolves_without_archive_index(self) -> None:
        support = self.support()
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            workspace.feature("2026-05-08-login")
            self.assertEqual(
                support.resolve_feature_location(
                    workspace.memory_root, "2026-05-08-login"
                ),
                support.FeatureLocation(
                    "2026-05-08-login",
                    "features/2026-05-08-login",
                    "flat",
                    None,
                ),
            )

    def test_archived_feature_requires_matching_unique_index_row(self) -> None:
        support = self.support()
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            source = workspace.feature("2026-05-08-login")
            target = workspace.features_root / "2026-05" / source.name
            target.parent.mkdir(parents=True)
            source.rename(target)
            index = workspace.write(
                ".agent-loop/features/archive.md",
                ARCHIVE_HEADER + archive_row(source.name),
            )
            self.assertEqual(
                support.resolve_feature_location(workspace.memory_root, source.name),
                support.FeatureLocation(
                    source.name,
                    f"features/2026-05/{source.name}",
                    "archived",
                    "2026-05",
                ),
            )

            index.unlink()
            with self.assertRaisesRegex(support.ArchiveContractError, "archive-index"):
                support.resolve_feature_location(workspace.memory_root, source.name)

            index.write_text(
                ARCHIVE_HEADER + archive_row(source.name) + archive_row(source.name),
                encoding="utf-8",
                newline="\n",
            )
            with self.assertRaisesRegex(support.ArchiveContractError, "archive-index"):
                support.resolve_feature_location(workspace.memory_root, source.name)

    def test_flat_and_archived_collision_fails_closed(self) -> None:
        support = self.support()
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            workspace.feature("2026-05-08-login")
            archived = workspace.features_root / "2026-05" / "2026-05-08-login"
            archived.mkdir(parents=True)
            workspace.write(
                ".agent-loop/features/archive.md",
                ARCHIVE_HEADER + archive_row("2026-05-08-login"),
            )
            with self.assertRaisesRegex(support.ArchiveContractError, "path-collision"):
                support.resolve_feature_location(
                    workspace.memory_root, "2026-05-08-login"
                )

    def test_month_must_match_feature_id(self) -> None:
        support = self.support()
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            archived = workspace.features_root / "2026-06" / "2026-05-08-login"
            archived.mkdir(parents=True)
            workspace.write(
                ".agent-loop/features/archive.md",
                ARCHIVE_HEADER
                + archive_row(
                    "2026-05-08-login",
                    month="2026-06",
                    path=".agent-loop/features/2026-06/2026-05-08-login/",
                ),
            )
            with self.assertRaisesRegex(support.ArchiveContractError, "month"):
                support.resolve_feature_location(
                    workspace.memory_root, "2026-05-08-login"
                )

    def test_archive_index_rejects_case_and_unicode_path_differences(self) -> None:
        support = self.support()
        for changed in (
            "2026-05-08-LOGIN",
            "２０２６-０５-０８-login",
        ):
            with self.subTest(changed=changed), tempfile.TemporaryDirectory() as temp:
                workspace = ArchiveWorkspace(Path(temp))
                workspace.write(
                    ".agent-loop/features/archive.md",
                    ARCHIVE_HEADER
                    + archive_row(
                        "2026-05-08-login",
                        path=f".agent-loop/features/2026-05/{changed}/",
                    ),
                )
                with self.assertRaises(support.ArchiveContractError):
                    support.parse_archive_index(workspace.memory_root)

    def test_archive_index_accepts_bom_and_crlf(self) -> None:
        support = self.support()
        with tempfile.TemporaryDirectory() as temp:
            workspace = ArchiveWorkspace(Path(temp))
            feature_id = "2026-05-08-login"
            archived = workspace.features_root / "2026-05" / feature_id
            archived.mkdir(parents=True)
            index = workspace.features_root / "archive.md"
            index.parent.mkdir(parents=True, exist_ok=True)
            content = ARCHIVE_HEADER + archive_row(
                feature_id, summary="完成登录与失败路径验证"
            )
            index.write_bytes(b"\xef\xbb\xbf" + content.replace("\n", "\r\n").encode("utf-8"))
            entries = support.parse_archive_index(workspace.memory_root)
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0].delivered_summary, "完成登录与失败路径验证")

    def test_symlink_escape_is_rejected(self) -> None:
        support = self.support()
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            workspace = ArchiveWorkspace(Path(temp))
            external = Path(outside) / "2026-05-08-login"
            external.mkdir()
            archived = workspace.features_root / "2026-05" / external.name
            archived.parent.mkdir(parents=True)
            try:
                archived.symlink_to(external, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"directory symlink unavailable: {error}")
            workspace.write(
                ".agent-loop/features/archive.md",
                ARCHIVE_HEADER + archive_row(external.name),
            )
            with self.assertRaisesRegex(support.ArchiveContractError, "path-escape"):
                support.resolve_feature_location(workspace.memory_root, external.name)

    def test_plan_hash_is_stable_across_absolute_roots(self) -> None:
        support = self.support()

        def make_plan(root: Path):
            workspace = ArchiveWorkspace(root)
            workspace.feature("2026-05-08-login")
            candidate = support.ArchiveCandidate(
                "2026-05-08-login",
                "2026-05",
                "features/2026-05-08-login",
                "closed",
                "complete",
                "none",
                "completed login",
                "none",
                "none",
                (),
            )
            move = support.Move(
                "2026-05-08-login",
                "2026-05",
                ".agent-loop/features/2026-05-08-login",
                ".agent-loop/features/2026-05/2026-05-08-login",
            )
            return support.ArchivePlan(
                1,
                "archive",
                "2026-07-14",
                ("2026-05",),
                (),
                (candidate,),
                (move,),
                (),
                (),
                (),
                tree_snapshot(root),
            )

        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            self.assertEqual(
                make_plan(Path(first)).computed_sha256(),
                make_plan(Path(second)).computed_sha256(),
            )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import ast
import hashlib
import io
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

from tests.checker_test_support import ROOT, combined_output, run_checker


CHECKERS = (
    "scripts/check-root-agents-blocks.py",
    "scripts/check-onboarding-core-flow-coverage.py",
    "scripts/check-concept-foundation-trace.py",
    "scripts/check-adr-requirement-model-trace.py",
)

ARCHIVE_COMMANDS = (
    "scripts/scan-feature-monthly-archive.py",
    "scripts/check-feature-monthly-archive.py",
    "scripts/apply-feature-monthly-archive.py",
    "scripts/restore-feature-monthly-archive.py",
)

MEMORY_RECONCILIATION_COMMANDS = (
    "scripts/scan-memory-reconciliation.py",
    "scripts/check-memory-reconciliation.py",
    "scripts/apply-memory-reconciliation.py",
    "scripts/restore-memory-reconciliation.py",
)

WORKFLOW = ROOT / ".github/workflows/cross-platform-checkers.yml"

COMPATIBILITY_ENTRIES = {
    "scripts/check-root-agents-blocks.sh": "check-root-agents-blocks.py",
    "scripts/check-onboarding-core-flow-coverage.rb": "check-onboarding-core-flow-coverage.py",
    "scripts/check-concept-foundation-trace.rb": "check-concept-foundation-trace.py",
    "scripts/check-adr-requirement-model-trace.rb": "check-adr-requirement-model-trace.py",
}

CURRENT_AUTHORITY = (
    "SKILL.md",
    "Usage.md",
    "references/project-guidance.md",
    "references/workflow-checklists.md",
)


class PythonCheckerContractTests(unittest.TestCase):
    @staticmethod
    def snapshot(root: Path) -> dict[str, str]:
        return {
            path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    def test_python_runtime_is_supported(self) -> None:
        self.assertGreaterEqual(sys.version_info[:2], (3, 10))

    def test_canonical_checker_files_exist(self) -> None:
        for relative in CHECKERS:
            with self.subTest(relative=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_archive_command_files_exist(self) -> None:
        for relative in ARCHIVE_COMMANDS:
            with self.subTest(relative=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_memory_reconciliation_command_files_exist(self) -> None:
        for relative in MEMORY_RECONCILIATION_COMMANDS:
            with self.subTest(relative=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_canonical_checkers_use_only_stdlib_and_local_support(self) -> None:
        allowed_local = {"checker_support", "feature_archive_support"}
        for relative in CHECKERS:
            path = ROOT / relative
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            imported: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(alias.name.split(".", 1)[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module.split(".", 1)[0])
            external = imported - set(sys.stdlib_module_names) - allowed_local
            self.assertEqual(external, set(), f"{relative}: {sorted(external)}")

    def test_archive_commands_use_only_stdlib_and_local_support(self) -> None:
        allowed_local = {"checker_support", "feature_archive_support"}
        for relative in ARCHIVE_COMMANDS:
            path = ROOT / relative
            self.assertTrue(path.is_file(), relative)
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            imported: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(alias.name.split(".", 1)[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module.split(".", 1)[0])
            external = imported - set(sys.stdlib_module_names) - allowed_local
            self.assertEqual(external, set(), f"{relative}: {sorted(external)}")

    def test_memory_reconciliation_commands_use_only_stdlib_and_local_support(self) -> None:
        allowed_local = {"checker_support", "memory_reconciliation_support"}
        for relative in MEMORY_RECONCILIATION_COMMANDS:
            path = ROOT / relative
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            imported: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(alias.name.split(".", 1)[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module.split(".", 1)[0])
            external = imported - set(sys.stdlib_module_names) - allowed_local
            self.assertEqual(external, set(), f"{relative}: {sorted(external)}")

    def test_missing_arguments_fail_with_usage_exit_two(self) -> None:
        for relative in CHECKERS:
            with self.subTest(relative=relative):
                result = run_checker(relative)
                self.assertEqual(result.returncode, 2, combined_output(result))
                self.assertIn("usage", combined_output(result).lower())

    def test_archive_commands_missing_arguments_fail_with_usage_exit_two(self) -> None:
        for relative in ARCHIVE_COMMANDS:
            with self.subTest(relative=relative):
                result = run_checker(relative)
                self.assertEqual(result.returncode, 2, combined_output(result))
                self.assertIn("usage", combined_output(result).lower())

    def test_memory_reconciliation_commands_missing_arguments_fail_with_usage_exit_two(self) -> None:
        for relative in MEMORY_RECONCILIATION_COMMANDS:
            with self.subTest(relative=relative):
                result = run_checker(relative)
                self.assertEqual(result.returncode, 2, combined_output(result))
                self.assertIn("usage", combined_output(result).lower())

    def test_unsupported_python_fails_closed_with_exit_two(self) -> None:
        scripts_dir = str(ROOT / "scripts")
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        from checker_support import require_supported_python

        stderr = io.StringIO()
        with redirect_stderr(stderr), self.assertRaises(SystemExit) as caught:
            require_supported_python((3, 9))
        self.assertEqual(caught.exception.code, 2)
        self.assertIn("Python 3.10+ is required", stderr.getvalue())

        for relative in CHECKERS:
            with self.subTest(relative=relative):
                path = ROOT / relative
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                calls = {
                    node.func.id
                    for node in ast.walk(tree)
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                }
                self.assertIn("require_supported_python", calls)

        for relative in ARCHIVE_COMMANDS:
            with self.subTest(relative=relative):
                path = ROOT / relative
                self.assertTrue(path.is_file(), relative)
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                calls = {
                    node.func.id
                    for node in ast.walk(tree)
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                }
                self.assertIn("require_supported_python", calls)

        for relative in MEMORY_RECONCILIATION_COMMANDS:
            with self.subTest(relative=relative):
                path = ROOT / relative
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                calls = {
                    node.func.id
                    for node in ast.walk(tree)
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                }
                self.assertIn("require_supported_python", calls)

    def test_cross_platform_ci_runs_the_native_suite(self) -> None:
        self.assertTrue(WORKFLOW.is_file(), str(WORKFLOW))
        content = WORKFLOW.read_text(encoding="utf-8")
        for required in (
            "macos-latest",
            "windows-latest",
            '"3.10"',
            '"3.x"',
            "tests.test_python_checker_contract",
            "tests.test_root_agents_blocks",
            "tests.test_onboarding_core_flow_coverage",
            "tests.test_concept_foundation_trace",
            "tests.test_adr_requirement_model_trace",
            "tests.test_feature_archive_support",
            "tests.test_feature_monthly_archive_scan",
            "tests.test_feature_monthly_archive_apply",
            "tests.test_feature_monthly_archive_restore",
            "tests.test_memory_reconciliation_support",
            "tests.test_memory_reconciliation_scan",
            "tests.test_memory_reconciliation_check",
            "tests.test_memory_reconciliation_apply",
            "tests.test_memory_reconciliation_restore",
            *ARCHIVE_COMMANDS,
            *MEMORY_RECONCILIATION_COMMANDS,
        ):
            with self.subTest(required=required):
                self.assertIn(required, content)

    def test_old_entrypoints_are_marked_thin_compatibility_launchers(self) -> None:
        for relative, canonical in COMPATIBILITY_ENTRIES.items():
            with self.subTest(relative=relative):
                content = (ROOT / relative).read_text(encoding="utf-8")
                self.assertIn("DEPRECATED COMPATIBILITY ENTRY", content)
                self.assertIn(canonical, content)
                self.assertIn("py", content)
                self.assertIn("-3", content)
                self.assertLessEqual(len(content.splitlines()), 24)

    def test_current_authority_does_not_recommend_legacy_entrypoints(self) -> None:
        legacy_paths = tuple(COMPATIBILITY_ENTRIES)
        for relative in CURRENT_AUTHORITY:
            content = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(relative=relative):
                for legacy in legacy_paths:
                    self.assertNotIn(legacy, content)
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        for canonical in CHECKERS:
            with self.subTest(canonical=canonical):
                self.assertIn(canonical, changelog)

    def test_valid_checker_runs_do_not_mutate_checked_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)

            root_case = root / "root-agents"
            (root_case / ".agent-loop").mkdir(parents=True)
            (root_case / ".agent-loop/project.md").touch()
            template = root_case / "template.md"
            target = root_case / "AGENTS.md"
            shutil.copy2(ROOT / "templates/root-AGENTS.md", template)
            shutil.copy2(template, target)

            onboarding = root / "onboarding"
            shutil.copytree(
                ROOT / "examples/ai-meeting-minutes-backend/onboarding-db", onboarding
            )

            concept = root / "concept"
            shutil.copytree(ROOT / "examples/concept-foundation-refund", concept)

            adr = root / "adr"
            shutil.copytree(ROOT / "tests/fixtures/adr-technical-landing/valid", adr)

            runs = (
                (
                    "scripts/check-root-agents-blocks.py",
                    "--template",
                    str(template),
                    "--target",
                    str(target),
                ),
                ("scripts/check-onboarding-core-flow-coverage.py", str(onboarding)),
                (
                    "scripts/check-concept-foundation-trace.py",
                    str(concept / "requirement.md"),
                    str(concept / "product.md"),
                    str(concept / "spec.md"),
                ),
                (
                    "scripts/check-adr-requirement-model-trace.py",
                    str(adr / "README.md"),
                    str(adr / "requirement.md"),
                    str(adr / "decision.md"),
                ),
            )
            before = self.snapshot(root)
            for script, *args in runs:
                first = run_checker(script, *args)
                second = run_checker(script, *args)
                self.assertEqual(first.returncode, 0, combined_output(first))
                self.assertEqual(second.returncode, 0, combined_output(second))
                self.assertEqual(
                    (first.returncode, first.stdout, first.stderr),
                    (second.returncode, second.stdout, second.stderr),
                )
            self.assertEqual(self.snapshot(root), before)


if __name__ == "__main__":
    unittest.main()

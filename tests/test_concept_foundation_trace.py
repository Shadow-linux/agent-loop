from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

from tests.checker_test_support import ROOT, combined_output, run_checker


SCRIPT = "scripts/check-concept-foundation-trace.py"
EXAMPLE = ROOT / "examples/concept-foundation-refund"
FIXTURES = ROOT / "tests/fixtures/concept-foundation"
PRODUCT_FIXTURE = ROOT / "tests/fixtures/adaptive-product-definition/standard-valid"


class ConceptFoundationTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.requirement = (EXAMPLE / "requirement.md").read_text(encoding="utf-8")
        cls.product = (EXAMPLE / "product.md").read_text(encoding="utf-8")
        cls.spec = (EXAMPLE / "spec.md").read_text(encoding="utf-8")

    def run_documents(
        self,
        requirement: str,
        product: str,
        spec: str,
        *,
        bom_crlf: bool = False,
    ):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paths = []
            for name, content in (
                ("requirement.md", requirement),
                ("product.md", product),
                ("spec.md", spec),
            ):
                path = root / name
                if bom_crlf:
                    path.write_bytes(("\ufeff" + content.replace("\n", "\r\n")).encode("utf-8"))
                else:
                    path.write_text(content, encoding="utf-8")
                paths.append(str(path))
            return run_checker(SCRIPT, *paths)

    def assert_rejected(
        self, requirement: str, product: str, spec: str, expected: str
    ) -> None:
        result = self.run_documents(requirement, product, spec)
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("CHANGED:", combined_output(result))
        self.assertIn(expected, combined_output(result))

    def test_accepted_example_passes(self) -> None:
        result = self.run_documents(self.requirement, self.product, self.spec)
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("accepted Concept Foundation trace is complete", result.stdout)

    def test_reasoned_not_needed_passes(self) -> None:
        requirement = self.requirement.replace(
            "Concept Foundation Status: accepted",
            "Concept Foundation Status: concept-foundation-not-needed",
        )
        requirement = re.sub(
            r"^Not-Needed Reason:.*$",
            "Not-Needed Reason: only one stable term exists and no product model is derived",
            requirement,
            flags=re.MULTILINE,
        )
        product = self.product.replace(
            "Concept Foundation Status: accepted",
            "Concept Foundation Status: concept-foundation-not-needed",
        )
        spec = self.spec.replace(
            "Concept Foundation Status: accepted",
            "Concept Foundation Status: concept-foundation-not-needed",
        )
        result = self.run_documents(requirement, product, spec)
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("reasoned concept-foundation-not-needed trace", result.stdout)

    def test_existing_invalid_fixtures_are_rejected(self) -> None:
        for fixture in ("invalid-unaccepted", "invalid-detached-model"):
            with self.subTest(fixture=fixture):
                root = FIXTURES / fixture
                result = run_checker(
                    SCRIPT,
                    str(root / "requirement.md"),
                    str(root / "product.md"),
                    str(root / "spec.md"),
                )
                self.assertEqual(result.returncode, 0, combined_output(result))
                self.assertIn("CHANGED:", combined_output(result))

    def test_adversarial_semantic_breaks_are_rejected(self) -> None:
        definition = self.requirement.split("## Concept Definitions\n", 1)[1]
        concept_line = next(
            line for line in definition.splitlines(keepends=True) if line.startswith("| C-CUSTOMER |")
        )
        cases = (
            (
                re.sub(
                    r"^- Confirmed Concept IDs:.*$",
                    "- Confirmed Concept IDs: C-CUSTOMER",
                    self.requirement,
                    flags=re.MULTILINE,
                ),
                self.product,
                self.spec,
                "unconfirmed Concept IDs",
            ),
            (
                re.sub(
                    r"^## Concept Candidate Inventory\n.*?(?=^## Concept Definitions\n)",
                    "",
                    self.requirement,
                    flags=re.MULTILINE | re.DOTALL,
                ),
                self.product,
                self.spec,
                "missing section: ## Concept Candidate Inventory",
            ),
            (
                self.requirement.replace("| resolved |", "| open |", 1),
                self.product,
                self.spec,
                "Blocking Ambiguities contains unresolved rows",
            ),
            (
                re.sub(r"^\| TRACE-03 .*\n", "", self.requirement, flags=re.MULTILINE),
                self.product,
                self.spec,
                "untraced product model IDs",
            ),
            (
                self.requirement.replace(concept_line, concept_line * 2, 1),
                self.product,
                self.spec,
                "duplicate IDs in Concept Definitions",
            ),
            (
                self.requirement,
                re.sub(
                    r"^Effective Concept Source:.*\n",
                    "",
                    self.product,
                    flags=re.MULTILINE,
                ),
                self.spec,
                "product Effective Concept Source is missing",
            ),
            (
                re.sub(
                    r"^\| PERM-ADMIN-SETTLEMENT \| C-REFUND-ADMIN "
                    r"\| C-REFUND-SETTLEMENT .*\n",
                    "",
                    self.requirement,
                    flags=re.MULTILINE,
                ),
                self.product,
                self.spec,
                "Commands / Events missing Role / Permission Matrix pairs",
            ),
        )
        for requirement, product, spec, expected in cases:
            with self.subTest(expected=expected):
                self.assert_rejected(requirement, product, spec, expected)

    def test_placeholder_not_needed_reason_is_rejected(self) -> None:
        requirement = self.requirement.replace(
            "Concept Foundation Status: accepted",
            "Concept Foundation Status: concept-foundation-not-needed",
        )
        requirement = re.sub(
            r"^Not-Needed Reason:.*$",
            "Not-Needed Reason: n/a",
            requirement,
            flags=re.MULTILINE,
        )
        product = self.product.replace(
            "Concept Foundation Status: accepted",
            "Concept Foundation Status: concept-foundation-not-needed",
        )
        spec = self.spec.replace(
            "Concept Foundation Status: accepted",
            "Concept Foundation Status: concept-foundation-not-needed",
        )
        self.assert_rejected(
            requirement,
            product,
            spec,
            "concept-foundation-not-needed requires a concrete reason",
        )

    def test_bom_and_crlf_are_supported(self) -> None:
        result = self.run_documents(
            self.requirement, self.product, self.spec, bom_crlf=True
        )
        self.assertEqual(result.returncode, 0, combined_output(result))

    def test_requirement_product_mode_passes_without_feature_product(self) -> None:
        result = run_checker(
            SCRIPT,
            "--requirement-product",
            str(PRODUCT_FIXTURE / "README.md"),
            str(PRODUCT_FIXTURE / "product.md"),
            str(PRODUCT_FIXTURE / "spec.md"),
        )
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn(
            "confirmed Requirement Product Definition trace is complete",
            result.stdout,
        )

    def test_requirement_product_mode_is_not_applicable_to_bug_authority(self) -> None:
        spec = """# Feature Spec: Bug-authority repair

Status: accepted
Feature Type: maintenance-fix

## Feature Authority

Authority Type: Bug Authority
Primary Authority Reference: .agent-loop/bugs/2026-08-10-example/README.md
Supporting Authority References: none
Authority Summary: restore the accepted behavior recorded by the Bug
Agent Authority Assessment: current
"""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("README.md", "product.md"):
                (root / name).write_text(
                    (PRODUCT_FIXTURE / name).read_text(encoding="utf-8"),
                    encoding="utf-8",
                )
            (root / "spec.md").write_text(spec, encoding="utf-8")
            result = run_checker(
                SCRIPT,
                "--requirement-product",
                str(root / "README.md"),
                str(root / "product.md"),
                str(root / "spec.md"),
            )
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("NOT_APPLICABLE:", result.stdout)
        self.assertNotIn(
            "missing section: ## Product Requirement Source",
            combined_output(result),
        )

    def test_requirement_product_input_change_expires_not_applicable(self) -> None:
        bug_spec = """# Feature Spec: Bug-authority repair

Status: accepted
Feature Type: maintenance-fix

## Feature Authority

Authority Type: Bug Authority
Primary Authority Reference: external:BUG-42
Supporting Authority References: none
Authority Summary: restore the accepted behavior recorded by the Bug
Agent Authority Assessment: current
"""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("README.md", "product.md"):
                (root / name).write_text(
                    (PRODUCT_FIXTURE / name).read_text(encoding="utf-8"),
                    encoding="utf-8",
                )
            spec_path = root / "spec.md"
            spec_path.write_text(bug_spec, encoding="utf-8")
            prior = run_checker(
                SCRIPT,
                "--requirement-product",
                str(root / "README.md"),
                str(root / "product.md"),
                str(spec_path),
            )
            self.assertEqual(prior.returncode, 0, combined_output(prior))
            self.assertIn("NOT_APPLICABLE:", prior.stdout)

            valid_spec = (PRODUCT_FIXTURE / "spec.md").read_text(encoding="utf-8")
            spec_path.write_text(
                re.sub(
                    r"^## Product Requirement Source\n.*?(?=^## |\Z)",
                    "",
                    valid_spec,
                    flags=re.MULTILINE | re.DOTALL,
                ),
                encoding="utf-8",
            )
            changed = run_checker(
                SCRIPT,
                "--requirement-product",
                str(root / "README.md"),
                str(root / "product.md"),
                str(spec_path),
            )
        self.assertEqual(changed.returncode, 0, combined_output(changed))
        self.assertIn("CHANGED:", combined_output(changed))
        self.assertNotIn("NOT_APPLICABLE:", combined_output(changed))
        self.assertIn("Product Requirement Source", combined_output(changed))

    def test_requirement_product_mode_rejects_unconfirmed_review_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("README.md", "product.md", "spec.md"):
                content = (PRODUCT_FIXTURE / name).read_text(encoding="utf-8")
                if name == "spec.md":
                    content = content.replace(
                        "Product Review Evidence: confirmed by human maintainer on 2026-07-22",
                        "Product Review Evidence: unconfirmed pending human review",
                    )
                (root / name).write_text(content, encoding="utf-8")
            result = run_checker(
                SCRIPT,
                "--requirement-product",
                str(root / "README.md"),
                str(root / "product.md"),
                str(root / "spec.md"),
            )
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("CHANGED:", combined_output(result))
        self.assertIn(
            "Feature Product Review Evidence must be confirmed",
            combined_output(result),
        )

    def test_requirement_product_mode_rejects_unknown_slice_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("README.md", "product.md", "spec.md"):
                content = (PRODUCT_FIXTURE / name).read_text(encoding="utf-8")
                if name == "spec.md":
                    content = content.replace("STATE-REQUEST", "STATE-UNKNOWN")
                (root / name).write_text(content, encoding="utf-8")
            result = run_checker(
                SCRIPT,
                "--requirement-product",
                str(root / "README.md"),
                str(root / "product.md"),
                str(root / "spec.md"),
            )
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("CHANGED:", combined_output(result))
        self.assertIn("Product Slice contains unknown source IDs", combined_output(result))

    def test_readable_missing_required_section_is_changed_not_blocked(self) -> None:
        requirement = re.sub(
            r"^## Concept Candidate Inventory\n.*?(?=^## Concept Definitions\n)",
            "",
            self.requirement,
            flags=re.MULTILINE | re.DOTALL,
        )
        result = self.run_documents(requirement, self.product, self.spec)
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("CHANGED:", combined_output(result))
        self.assertIn(
            "missing section: ## Concept Candidate Inventory",
            combined_output(result),
        )

    def test_invalid_utf8_is_stable_blocked_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "requirement.md").write_bytes(b"\xff\xfeinvalid")
            (root / "product.md").write_text(self.product, encoding="utf-8")
            (root / "spec.md").write_text(self.spec, encoding="utf-8")
            result = run_checker(
                SCRIPT,
                str(root / "requirement.md"),
                str(root / "product.md"),
                str(root / "spec.md"),
            )
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn("BLOCKED:", combined_output(result))
        self.assertNotIn("Traceback", combined_output(result))

    def test_dangling_spec_is_stable_blocked_not_usage_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "requirement.md").write_text(self.requirement, encoding="utf-8")
            (root / "product.md").write_text(self.product, encoding="utf-8")
            spec = root / "spec.md"
            try:
                spec.symlink_to("missing-spec.md")
            except OSError as error:
                self.skipTest(f"symlink unavailable: {error}")
            result = run_checker(
                SCRIPT,
                str(root / "requirement.md"),
                str(root / "product.md"),
                str(spec),
            )
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn("BLOCKED:", combined_output(result))
        self.assertNotIn("usage:", combined_output(result).lower())


if __name__ == "__main__":
    unittest.main()

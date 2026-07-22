from __future__ import annotations

import shutil
import re
import tempfile
import unittest
from pathlib import Path

from tests.checker_test_support import ROOT, combined_output, run_checker
from scripts.requirement_product_support import (
    ProductDefinitionError,
    product_model_inventory,
    product_semantic_sha256,
    resolve_effective_product_definition,
)


SCRIPT = "scripts/check-requirement-product-definition.py"
FIXTURES = ROOT / "tests/fixtures/adaptive-product-definition"


class EffectiveProductSourceResolverTests(unittest.TestCase):
    def test_new_and_legacy_sources_resolve_to_one_normalized_model(self) -> None:
        current = FIXTURES / "standard-valid"
        source = resolve_effective_product_definition(
            current / "README.md", current / "product.md"
        )
        self.assertEqual(source.kind, "product-definition")
        self.assertEqual(source.profile, "standard")
        self.assertEqual(source.review, "confirmed")
        self.assertFalse(source.legacy)
        concepts, models = product_model_inventory(source)
        self.assertEqual(concepts, {"C-REQUEST", "C-OPERATOR"})
        self.assertIn("STATE-REQUEST", models)

        legacy_root = ROOT / "tests/fixtures/adr-technical-landing/valid"
        legacy = resolve_effective_product_definition(
            legacy_root / "README.md", legacy_root / "requirement.md"
        )
        self.assertTrue(legacy.legacy)
        self.assertEqual(legacy.kind, "concept-foundation")
        self.assertEqual(legacy.review, "accepted")
        self.assertIn("PM-FIXTURE-FACT", legacy.model_ids)

    def assert_resolution_error(
        self,
        readme: str,
        source: str,
        expected: str,
        *,
        source_name: str = "product.md",
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            readme_path = root / "README.md"
            source_path = root / source_name
            readme_path.write_text(readme, encoding="utf-8")
            source_path.write_text(source, encoding="utf-8")
            with self.assertRaisesRegex(ProductDefinitionError, expected):
                resolve_effective_product_definition(readme_path, source_path)

    def test_missing_pointer_is_rejected(self) -> None:
        self.assert_resolution_error(
            "# Requirement Set\n",
            "Product Definition Profile: brief\nProduct Review: confirmed\n",
            "missing effective product source pointer",
        )

    def test_pointer_escape_and_supplied_path_mismatch_are_rejected(self) -> None:
        product = (FIXTURES / "brief-valid/product.md").read_text(encoding="utf-8")
        readme = (FIXTURES / "brief-valid/README.md").read_text(encoding="utf-8")
        self.assert_resolution_error(
            readme.replace("Source: product.md", "Source: ../product.md"),
            product,
            "reference escapes Requirement Set",
        )
        self.assert_resolution_error(
            readme.replace("Source: product.md", "Source: other.md"),
            product,
            "effective product source pointer does not resolve to supplied source",
        )

    def test_pointer_and_source_metadata_must_align(self) -> None:
        product = (FIXTURES / "brief-valid/product.md").read_text(encoding="utf-8")
        readme = (FIXTURES / "brief-valid/README.md").read_text(encoding="utf-8")
        self.assert_resolution_error(
            readme.replace("Profile: brief", "Profile: standard"),
            product,
            "Product Definition Profile metadata mismatch",
        )
        self.assert_resolution_error(
            readme.replace("Product Review: confirmed", "Product Review: pending"),
            product,
            "Product Review must be confirmed",
        )

    def test_pointer_freshness_metadata_must_be_complete_and_consistent(self) -> None:
        product = (FIXTURES / "brief-valid/product.md").read_text(encoding="utf-8")
        readme = (FIXTURES / "brief-valid/README.md").read_text(encoding="utf-8")
        self.assert_resolution_error(
            readme.replace("Last Confirmed: 2026-07-22", "Last Confirmed: 2026-07-21"),
            product,
            "Last Confirmed must match Product Human Review Confirmed At",
        )
        self.assert_resolution_error(
            readme.replace("Previous Source: none", "Previous Source: missing-product.md"),
            product,
            "Previous Source does not exist",
        )

    def test_unsupported_profile_and_unresolved_legacy_status_are_rejected(self) -> None:
        product = (FIXTURES / "brief-valid/product.md").read_text(encoding="utf-8")
        readme = (FIXTURES / "brief-valid/README.md").read_text(encoding="utf-8")
        self.assert_resolution_error(
            readme.replace("Profile: brief", "Profile: complex"),
            product.replace(
                "Product Definition Profile: brief",
                "Product Definition Profile: complex",
            ),
            "unsupported Product Definition Profile: complex",
        )
        legacy_readme = (
            "# Requirement Set\n\n## Effective Concept Foundation\n\n"
            "Status: candidate\nEffective Source: requirement.md\n"
        )
        legacy_source = "Concept Foundation Status: candidate\n"
        self.assert_resolution_error(
            legacy_readme,
            legacy_source,
            "legacy effective Concept Foundation must be accepted or reasoned not-needed",
            source_name="requirement.md",
        )


class RequirementProductDefinitionTests(unittest.TestCase):
    def run_fixture(self, name: str, *, with_spec: bool = True):
        fixture = FIXTURES / name
        args = [str(fixture / "README.md"), str(fixture / "product.md")]
        if with_spec:
            args.append(str(fixture / "spec.md"))
        return run_checker(SCRIPT, *args)

    def run_mutation(
        self,
        *,
        readme: str | None = None,
        product: str | None = None,
        spec: str | None = None,
        bom_crlf: bool = False,
    ):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            valid = FIXTURES / "standard-valid"
            values = {
                "README.md": readme
                if readme is not None
                else (valid / "README.md").read_text(encoding="utf-8"),
                "product.md": product
                if product is not None
                else (valid / "product.md").read_text(encoding="utf-8"),
                "spec.md": spec
                if spec is not None
                else (valid / "spec.md").read_text(encoding="utf-8"),
            }
            paths: list[str] = []
            for name, content in values.items():
                path = root / name
                if bom_crlf:
                    path.write_bytes(("\ufeff" + content.replace("\n", "\r\n")).encode("utf-8"))
                else:
                    path.write_text(content, encoding="utf-8")
                paths.append(str(path))
            return run_checker(SCRIPT, *paths)

    def assert_rejected(self, result, expected: str) -> None:
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn(expected, combined_output(result))

    def test_confirmed_brief_passes_without_model_placeholders(self) -> None:
        result = self.run_fixture("brief-valid", with_spec=False)
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("confirmed brief product definition is valid", result.stdout)

    def test_confirmed_brief_hands_off_directly_to_product_slice(self) -> None:
        result = self.run_fixture("brief-valid")
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("confirmed brief product definition is valid", result.stdout)

    def test_confirmed_standard_passes_with_only_applicable_views(self) -> None:
        result = self.run_fixture("standard-valid")
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("confirmed standard product definition is valid", result.stdout)

    def test_profile_complex_is_rejected(self) -> None:
        product = (FIXTURES / "standard-valid/product.md").read_text(encoding="utf-8")
        result = self.run_mutation(
            product=product.replace(
                "Product Definition Profile: standard",
                "Product Definition Profile: complex",
            )
        )
        self.assert_rejected(result, "unsupported Product Definition Profile: complex")

    def test_unreviewed_product_is_rejected_for_downstream_use(self) -> None:
        result = self.run_fixture("standard-invalid-unreviewed")
        self.assert_rejected(result, "Product Review must be confirmed")

    def test_new_and_legacy_effective_pointers_cannot_coexist(self) -> None:
        result = self.run_fixture("standard-invalid-dual-source")
        self.assert_rejected(result, "multiple effective product source pointers")

    def test_included_view_requires_section_and_ids(self) -> None:
        product = (FIXTURES / "standard-valid/product.md").read_text(encoding="utf-8")
        before, remainder = product.split("## Product State Model\n", 1)
        _, after = remainder.split("## Requirement Product Model\n", 1)
        result = self.run_mutation(product=before + "## Requirement Product Model\n" + after)
        self.assert_rejected(result, "included view State is missing section")

    def test_not_applicable_view_requires_concrete_reason(self) -> None:
        product = (FIXTURES / "standard-valid/product.md").read_text(encoding="utf-8")
        product = product.replace(
            "| State | included | request has pending and approved states | Product State Model / STATE-REQUEST |",
            "| State | not-applicable | n/a | none |",
        )
        result = self.run_mutation(product=product)
        self.assert_rejected(result, "not-applicable view requires a concrete reason")

    def test_every_product_view_requires_one_applicability_row(self) -> None:
        product = (FIXTURES / "standard-valid/product.md").read_text(encoding="utf-8")
        product = re.sub(
            r"^\| Relationships \|.*\n",
            "",
            product,
            flags=re.MULTILINE,
        )
        result = self.run_mutation(product=product)
        self.assert_rejected(result, "Product View Applicability mismatch")

    def test_product_slice_cannot_reference_unknown_model_id(self) -> None:
        spec = (FIXTURES / "standard-valid/spec.md").read_text(encoding="utf-8")
        result = self.run_mutation(spec=spec.replace("STATE-REQUEST", "STATE-UNKNOWN"))
        self.assert_rejected(result, "Product Slice contains unknown source IDs")

    def test_product_slice_requires_full_requirement_set_path(self) -> None:
        spec = (FIXTURES / "standard-valid/spec.md").read_text(encoding="utf-8")
        spec = spec.replace(
            "Requirement Set: tests/fixtures/adaptive-product-definition/standard-valid",
            "Requirement Set: standard-valid",
        )
        result = self.run_mutation(spec=spec)
        self.assert_rejected(result, "Product Requirement Source requires Requirement Set")

    def test_product_slice_rejects_unconfirmed_review_evidence(self) -> None:
        spec = (FIXTURES / "standard-valid/spec.md").read_text(encoding="utf-8")
        result = self.run_mutation(
            spec=spec.replace(
                "Product Review Evidence: confirmed by human maintainer on 2026-07-22",
                "Product Review Evidence: unconfirmed by human maintainer on 2026-07-22",
            )
        )
        self.assert_rejected(result, "Feature Product Review Evidence must be confirmed")

    def test_stale_visual_digest_is_rejected(self) -> None:
        result = self.run_fixture("standard-invalid-stale-visual")
        self.assert_rejected(result, "derived visual digest is stale")

    def test_current_visual_with_known_ids_and_semantic_digest_passes(self) -> None:
        product = (FIXTURES / "standard-valid/product.md").read_text(encoding="utf-8")
        digest = product_semantic_sha256(product)
        visual = (
            "## Derived Visuals\n\n"
            "| Path | Type | Source IDs | Product Semantic SHA-256 | Status | Human Confirmed |\n"
            "|---|---|---|---|---|---|\n"
            f"| visuals/approval-flow.html | workflow | FLOW-SUBMIT / FLOW-APPROVE | {digest} | current | human approved workflow scope on 2026-07-22 |\n\n"
        )
        product = product.replace(
            "## Product Human Review Evidence\n", visual + "## Product Human Review Evidence\n"
        )
        result = self.run_mutation(product=product)
        self.assertEqual(result.returncode, 0, combined_output(result))

    def test_brief_rejects_standard_only_model_views(self) -> None:
        brief = (FIXTURES / "brief-valid/product.md").read_text(encoding="utf-8")
        readme = (FIXTURES / "brief-valid/README.md").read_text(encoding="utf-8")
        inflated = brief.replace(
            "## Product Human Review Evidence\n",
            "## Product State Model\n\n| State Model ID | Meaning |\n|---|---|\n| STATE-FAKE | fake |\n\n## Product Human Review Evidence\n",
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "README.md").write_text(readme, encoding="utf-8")
            (root / "product.md").write_text(inflated, encoding="utf-8")
            result = run_checker(SCRIPT, str(root / "README.md"), str(root / "product.md"))
        self.assert_rejected(
            result, "brief product definition contains Standard-only product-model views"
        )

    def test_brief_rejects_all_explicit_standard_only_sections(self) -> None:
        brief = (FIXTURES / "brief-valid/product.md").read_text(encoding="utf-8")
        readme = (FIXTURES / "brief-valid/README.md").read_text(encoding="utf-8")
        for heading in (
            "Product Capability Scope",
            "User Segments / Roles / Scenarios",
            "Experience / Operations / Measurement",
        ):
            with self.subTest(heading=heading), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                inflated = brief.replace(
                    "## Product Human Review Evidence\n",
                    f"## {heading}\n\nConcrete Standard-only detail.\n\n"
                    "## Product Human Review Evidence\n",
                )
                (root / "README.md").write_text(readme, encoding="utf-8")
                (root / "product.md").write_text(inflated, encoding="utf-8")
                result = run_checker(
                    SCRIPT, str(root / "README.md"), str(root / "product.md")
                )
                self.assert_rejected(
                    result,
                    "brief product definition contains Standard-only product-model views",
                )

    def test_bom_crlf_and_windows_style_input_are_supported(self) -> None:
        readme = (FIXTURES / "standard-valid/README.md").read_text(encoding="utf-8")
        readme = readme.replace("Source: product.md", "Source: .\\product.md")
        result = self.run_mutation(readme=readme, bom_crlf=True)
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("confirmed standard product definition is valid", result.stdout)


if __name__ == "__main__":
    unittest.main()

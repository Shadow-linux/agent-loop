from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.requirement_product_support import product_semantic_sha256
from scripts.visual_artifact_support import (
    VisualArtifactError,
    validate_durable_visual,
)
from tests.checker_test_support import ROOT, combined_output, run_checker


PRODUCT_SCRIPT = "scripts/check-requirement-product-definition.py"
PRODUCT_FIXTURE = ROOT / "tests/fixtures/adaptive-product-definition/standard-valid"
ADR_SCRIPT = "scripts/check-adr-requirement-model-trace.py"
ADR_FIXTURE = ROOT / "tests/fixtures/adr-technical-landing/valid"
ONBOARDING_SCRIPT = "scripts/check-onboarding-core-flow-coverage.py"
ONBOARDING_FIXTURE = ROOT / "examples/ai-meeting-minutes-backend/onboarding-db"


class OptionalVisualArtifactSupportTests(unittest.TestCase):
    def write_pair(
        self,
        root: Path,
        *,
        diagram_type: str = "workflow",
        source_type: str | None = None,
        source_output: str = "review.html",
        bom_crlf: bool = False,
    ) -> tuple[Path, Path]:
        source = root / f"review.{diagram_type}.json"
        render = root / "review.html"
        payload = {
            "schema_version": 1,
            "diagram_type": source_type or diagram_type,
            "meta": {"title": "Review", "output": source_output},
            "lanes": [],
            "nodes": [],
            "edges": [],
            "cards": [],
        }
        content = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2)
        if bom_crlf:
            source.write_bytes(("\ufeff" + content.replace("\n", "\r\n")).encode("utf-8"))
        else:
            source.write_text(content, encoding="utf-8")
        render.write_text("<!doctype html><title>Review</title>", encoding="utf-8")
        return source, render

    @staticmethod
    def digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def validate_pair(
        self,
        root: Path,
        source: Path,
        render_path: Path,
        **overrides: str,
    ):
        values = {
            "diagram_id": "D-REVIEW",
            "source_definition": source.name,
            "render": render_path.name,
            "diagram_type": "workflow",
            "source_sha256": self.digest(source),
            "render_sha256": self.digest(render_path),
            "generator": "archify@2.11",
            "validation_evidence": "doctor=pass; validate=pass; check=pass",
        }
        values.update(overrides)
        return validate_durable_visual(root, **values)

    def test_valid_archify_source_render_pair_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, render = self.write_pair(root)
            artifact = self.validate_pair(root, source, render)
            self.assertEqual(artifact.source_path, source.resolve())
            self.assertEqual(artifact.render_path, render.resolve())

    def test_source_path_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "owned"
            root.mkdir()
            outside, render = self.write_pair(base)
            render.replace(root / render.name)
            with self.assertRaisesRegex(
                VisualArtifactError, "source definition escapes owning root"
            ):
                self.validate_pair(
                    root,
                    outside,
                    root / "review.html",
                    source_definition="../review.workflow.json",
                )

    def test_render_only_pair_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, render = self.write_pair(root)
            with self.assertRaisesRegex(
                VisualArtifactError, "source definition is required"
            ):
                self.validate_pair(root, source, render, source_definition="")

    def test_source_type_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, render = self.write_pair(root, source_type="sequence")
            with self.assertRaisesRegex(
                VisualArtifactError, "diagram_type does not match manifest Type"
            ):
                self.validate_pair(root, source, render)

    def test_meta_output_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, render = self.write_pair(root, source_output="other.html")
            with self.assertRaisesRegex(
                VisualArtifactError, "meta.output does not match render"
            ):
                self.validate_pair(root, source, render)

    def test_source_hash_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, render = self.write_pair(root)
            with self.assertRaisesRegex(VisualArtifactError, "source SHA-256 is stale"):
                self.validate_pair(root, source, render, source_sha256="0" * 64)

    def test_render_hash_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, render = self.write_pair(root)
            with self.assertRaisesRegex(VisualArtifactError, "render SHA-256 is stale"):
                self.validate_pair(root, source, render, render_sha256="0" * 64)

    def test_generator_without_version_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, render = self.write_pair(root)
            with self.assertRaisesRegex(
                VisualArtifactError, "generator must be archify@version"
            ):
                self.validate_pair(root, source, render, generator="archify")

    def test_validation_without_validate_and_check_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, render = self.write_pair(root)
            with self.assertRaisesRegex(
                VisualArtifactError,
                "validation evidence requires validate=pass and check=pass",
            ):
                self.validate_pair(
                    root,
                    source,
                    render,
                    validation_evidence="doctor=pass; validate=pass",
                )

    def test_bom_crlf_and_windows_style_paths_are_supported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, render = self.write_pair(root, bom_crlf=True)
            artifact = self.validate_pair(
                root,
                source,
                render,
                source_definition=".\\review.workflow.json",
                render=".\\review.html",
            )
            self.assertEqual(artifact.diagram_type, "workflow")


class RequirementVisualIntegrationTests(unittest.TestCase):
    def prepare(self, root: Path) -> tuple[Path, Path, Path]:
        shutil.copytree(PRODUCT_FIXTURE, root, dirs_exist_ok=True)
        visual_root = root / "visuals"
        visual_root.mkdir()
        source = visual_root / "approval-flow.workflow.json"
        render = visual_root / "approval-flow.html"
        source.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "diagram_type": "workflow",
                    "meta": {
                        "title": "Approval Flow",
                        "output": "approval-flow.html",
                    },
                    "lanes": [],
                    "nodes": [],
                    "edges": [],
                    "cards": [],
                },
                ensure_ascii=False,
                sort_keys=True,
                indent=2,
            ),
            encoding="utf-8",
        )
        render.write_text(
            "<!doctype html><title>Approval Flow</title>", encoding="utf-8"
        )
        return root / "README.md", root / "product.md", root / "spec.md"

    @staticmethod
    def digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def source_render_product(self, product_path: Path) -> str:
        product = product_path.read_text(encoding="utf-8")
        source = product_path.parent / "visuals/approval-flow.workflow.json"
        render = product_path.parent / "visuals/approval-flow.html"
        semantic_digest = product_semantic_sha256(product)
        visual = (
            "## Derived Visuals\n\n"
            "Visual Manifest Contract: source-render-v1\n\n"
            "| Diagram ID | Source Definition | Render | Type | Source IDs | Product Semantic SHA-256 | Source SHA-256 | Render SHA-256 | Generator | Validation Evidence | Status | Human Confirmed |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|---|\n"
            "| D-APPROVAL-FLOW | visuals/approval-flow.workflow.json | visuals/approval-flow.html | workflow | FLOW-SUBMIT / FLOW-APPROVE | "
            f"{semantic_digest} | {self.digest(source)} | {self.digest(render)} | archify@2.11 | doctor=pass; validate=pass; check=pass | current | human confirmed review scope on 2026-07-23 |\n\n"
        )
        return product.replace(
            "## Product Human Review Evidence\n",
            visual + "## Product Human Review Evidence\n",
        )

    def test_product_source_render_manifest_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "requirement"
            readme, product, spec = self.prepare(root)
            product.write_text(self.source_render_product(product), encoding="utf-8")
            result = run_checker(PRODUCT_SCRIPT, readme, product, spec)
            self.assertEqual(result.returncode, 0, combined_output(result))

    def test_product_contract_marker_with_legacy_columns_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "requirement"
            readme, product, spec = self.prepare(root)
            content = product.read_text(encoding="utf-8")
            digest = product_semantic_sha256(content)
            legacy = (
                "## Derived Visuals\n\n"
                "Visual Manifest Contract: source-render-v1\n\n"
                "| Path | Type | Source IDs | Product Semantic SHA-256 | Status | Human Confirmed |\n"
                "|---|---|---|---|---|---|\n"
                f"| visuals/approval-flow.html | workflow | FLOW-SUBMIT | {digest} | current | human confirmed legacy row on 2026-07-23 |\n\n"
            )
            product.write_text(
                content.replace(
                    "## Product Human Review Evidence\n",
                    legacy + "## Product Human Review Evidence\n",
                ),
                encoding="utf-8",
            )
            result = run_checker(PRODUCT_SCRIPT, readme, product, spec)
            self.assertEqual(result.returncode, 1, combined_output(result))
            self.assertIn("source-render-v1 columns mismatch", combined_output(result))

    def test_legacy_product_visual_row_remains_readable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "requirement"
            readme, product, spec = self.prepare(root)
            content = product.read_text(encoding="utf-8")
            digest = product_semantic_sha256(content)
            legacy = (
                "## Derived Visuals\n\n"
                "| Path | Type | Source IDs | Product Semantic SHA-256 | Status | Human Confirmed |\n"
                "|---|---|---|---|---|---|\n"
                f"| visuals/approval-flow.html | workflow | FLOW-SUBMIT | {digest} | current | human confirmed historical row on 2026-07-22 |\n\n"
            )
            product.write_text(
                content.replace(
                    "## Product Human Review Evidence\n",
                    legacy + "## Product Human Review Evidence\n",
                ),
                encoding="utf-8",
            )
            result = run_checker(PRODUCT_SCRIPT, readme, product, spec)
            self.assertEqual(result.returncode, 0, combined_output(result))


class AdrVisualIntegrationTests(unittest.TestCase):
    def prepare(
        self,
        root: Path,
        *,
        omit_source: bool = False,
        decision_mode: str = "accepted",
    ):
        shutil.copytree(ADR_FIXTURE, root)
        visual_root = root / "visuals"
        visual_root.mkdir()
        source = visual_root / "technical-flow.workflow.json"
        render = visual_root / "technical-flow.html"
        payload = {
            "schema_version": 1,
            "diagram_type": "workflow",
            "meta": {"title": "Technical Flow", "output": render.name},
            "lanes": [],
            "nodes": [],
            "edges": [],
            "cards": [],
        }
        source.write_text(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2),
            encoding="utf-8",
        )
        render.write_text("<!doctype html><title>Technical Flow</title>", encoding="utf-8")
        decision_path = root / "decision.md"
        decision = decision_path.read_text(encoding="utf-8")
        source_value = "visuals/missing.workflow.json" if omit_source else source.relative_to(root).as_posix()
        visual = (
            "## Optional Visual Evidence\n\n"
            "Visual Manifest Contract: source-render-v1\n\n"
            "| Diagram ID | Review Question | Semantic References | Source Definition | Render | Type | Source SHA-256 | Render SHA-256 | Generator | Validation Evidence | Status |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|\n"
            "| D-TECHNICAL-FLOW | Does the landing preserve the accepted fixture flow? | FLOW-FIXTURE-01, PM-FIXTURE-FACT | "
            f"{source_value} | {render.relative_to(root).as_posix()} | workflow | "
            f"{hashlib.sha256(source.read_bytes()).hexdigest()} | {hashlib.sha256(render.read_bytes()).hexdigest()} | "
            "archify@2.11 | doctor=pass; validate=pass; check=pass | current |\n\n"
        )
        decision = decision.replace(
            "## Human Review Evidence\n", visual + "## Human Review Evidence\n"
        )
        if decision_mode == "proposed":
            decision = decision.replace("Status: accepted", "Status: proposed", 1)
            decision = decision.split("## Human Review Evidence", 1)[0]
        elif decision_mode == "accepted-without-review":
            decision = decision.split("## Human Review Evidence", 1)[0]
        decision_path.write_text(decision, encoding="utf-8")
        return run_checker(
            ADR_SCRIPT,
            root / "README.md",
            root / "requirement.md",
            decision_path,
            root,
        )

    def test_valid_optional_adr_visual_evidence_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = self.prepare(Path(temporary) / "adr")
            self.assertEqual(result.returncode, 0, combined_output(result))

    def test_adr_render_without_source_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = self.prepare(Path(temporary) / "adr", omit_source=True)
            self.assertEqual(result.returncode, 1, combined_output(result))
            self.assertIn("source definition file is missing", combined_output(result))

    def test_adr_visual_cannot_change_accepted_status(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            proposed = self.prepare(root / "proposed", decision_mode="proposed")
            self.assertEqual(proposed.returncode, 0, combined_output(proposed))
            self.assertIn("ADR proposed", proposed.stdout)
            accepted = self.prepare(
                root / "accepted", decision_mode="accepted-without-review"
            )
            self.assertEqual(accepted.returncode, 1, combined_output(accepted))
            self.assertIn(
                "missing section: ## Human Review Evidence",
                combined_output(accepted),
            )


class OnboardingVisualIntegrationTests(unittest.TestCase):
    def prepare(self, root: Path, *, omit_source: bool = False):
        shutil.copytree(ONBOARDING_FIXTURE, root)
        visual_root = root / "visuals"
        visual_root.mkdir()
        source = visual_root / "core-flow.workflow.json"
        render = visual_root / "core-flow.html"
        source.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "diagram_type": "workflow",
                    "meta": {"title": "Core Flow", "output": render.name},
                    "lanes": [],
                    "nodes": [],
                    "edges": [],
                    "cards": [],
                },
                ensure_ascii=False,
                sort_keys=True,
                indent=2,
            ),
            encoding="utf-8",
        )
        render.write_text("<!doctype html><title>Core Flow</title>", encoding="utf-8")
        flow = next((root / "03-flows").glob("*.md"))
        existing = flow.read_text(encoding="utf-8").replace(
            "## 3. Core Flow Overview / Boundary — D-BOUNDARY",
            "## 3. Core Flow Overview / Boundary",
        )
        existing = "\n".join(
            line
            for line in existing.splitlines()
            if not line.startswith("- Required Diagram IDs:")
        ) + "\n"
        source_value = "visuals/missing.workflow.json" if omit_source else source.relative_to(root).as_posix()
        flow.write_text(
            existing
            + "\nRepresentation: archify-source-render\n\n"
            + "## Diagram Artifact Manifest\n\n"
            + "Visual Manifest Contract: source-render-v1\n\n"
            + "| Diagram ID | Evidence References | Source Definition | Render | Type | Source SHA-256 | Render SHA-256 | Generator | Validation Evidence | Status |\n"
            + "|---|---|---|---|---|---|---|---|---|---|\n"
            + "| D-BOUNDARY | `src/core.py#run` | "
            + f"{source_value} | {render.relative_to(root).as_posix()} | workflow | "
            + f"{hashlib.sha256(source.read_bytes()).hexdigest()} | {hashlib.sha256(render.read_bytes()).hexdigest()} | "
            + "archify@2.11 | doctor=pass; validate=pass; check=pass | current |\n",
            encoding="utf-8",
        )
        return run_checker(ONBOARDING_SCRIPT, root)

    def test_onboarding_archify_pair_satisfies_required_diagram(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = self.prepare(Path(temporary) / "onboarding")
            self.assertEqual(result.returncode, 0, combined_output(result))

    def test_onboarding_html_only_required_diagram_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = self.prepare(Path(temporary) / "onboarding", omit_source=True)
            self.assertEqual(result.returncode, 1, combined_output(result))
            self.assertIn("source definition file is missing", combined_output(result))

    def test_onboarding_embedded_mermaid_and_ascii_remain_valid(self) -> None:
        result = run_checker(ONBOARDING_SCRIPT, ONBOARDING_FIXTURE)
        self.assertEqual(result.returncode, 0, combined_output(result))

if __name__ == "__main__":
    unittest.main()

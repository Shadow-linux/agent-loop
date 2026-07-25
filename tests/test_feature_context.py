from __future__ import annotations

import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.checker_test_support import ROOT, combined_output, run_checker


SCRIPT = "scripts/check-feature-context.py"
FIXTURE = ROOT / "tests/fixtures/feature-context/current"
FEATURE = Path(".agent-loop/features/2026-07-25-example/spec.md")
README = Path(".agent-loop/requirements/2026-07-25-example/README.md")
PRODUCT = Path(".agent-loop/requirements/2026-07-25-example/product.md")
DECISION = Path(".agent-loop/decisions/0001-example.md")


class FeatureContextCheckerTests(unittest.TestCase):
    @staticmethod
    def snapshot(root: Path) -> dict[str, str]:
        return {
            path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    def run_project(self, mutate=None):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        shutil.copytree(FIXTURE / ".agent-loop", root / ".agent-loop")
        if mutate:
            mutate(root)
        before = self.snapshot(root)
        result = run_checker(
            SCRIPT,
            "--project-root",
            str(root),
            str(root / FEATURE),
        )
        self.assertEqual(self.snapshot(root), before, "checker mutated target artifacts")
        return result

    def test_current_snapshot_passes(self):
        result = self.run_project()
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("CURRENT:", result.stdout)

    def test_current_legacy_requirement_source_passes(self):
        def mutate(root):
            requirement_root = (root / README).parent
            legacy_source = requirement_root / "requirement.md"
            shutil.copy2(
                ROOT / "tests/fixtures/adr-technical-landing/valid/requirement.md",
                legacy_source,
            )
            (root / README).write_text(
                """# Requirement Set: Legacy Fixture

Status: accepted

## Effective Concept Foundation

Status: accepted
Effective Source: requirement.md
Previous Source: none
Last Confirmed: 2026-07-25
Reason / Reopen Trigger: accepted legacy source
""",
                encoding="utf-8",
            )
            product_digest = hashlib.sha256(legacy_source.read_bytes()).hexdigest()
            decision_digest = hashlib.sha256((root / DECISION).read_bytes()).hexdigest()
            (root / FEATURE).write_text(
                f"""# Feature Spec: Legacy Slice

Status: accepted
Feature Type: normal

## Product Requirement Source

Requirement Set: {README.as_posix()}
Effective Product Definition: {legacy_source.relative_to(root).as_posix()}
Product Definition Profile: legacy
Product Review Evidence: accepted legacy Concept Foundation
Applicable Decisions: {DECISION.as_posix()}

## Feature Context Snapshot

Requirement Set: {README.as_posix()}
Requirement Lifecycle: accepted
Resolved Product Source: {legacy_source.relative_to(root).as_posix()}
Product Definition Profile: legacy
Product Review: accepted
Product Source SHA-256: {product_digest}
Applicable Decisions: {DECISION.as_posix()}
Decision Source SHA-256: {DECISION.as_posix()}={decision_digest}
Product Slice References: C-FIXTURE-SUBJECT / FLOW-FIXTURE-01
Verified At: 2026-07-25T12:00:00+08:00
Freshness: current

### Product Outcome

Preserve the accepted legacy product outcome.

### Actors And Core Journey

The accepted operator performs the accepted flow.

### Applicable Product Rules And Invariants

Preserve the accepted model invariants.

### Applicable States, Exceptions, And Recovery

Preserve accepted state and recovery meaning.

### Feature Boundary And Acceptance Context

Implement only the cited legacy Product Slice.

## Product Slice

| Source Section / Model ID | Feature Responsibility | Acceptance Mapping | Coverage |
|---|---|---|---|
| C-FIXTURE-SUBJECT / FLOW-FIXTURE-01 | implement accepted flow | flow remains observable | in-scope |
""",
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("CURRENT:", result.stdout)

    def test_changed_product_digest_requires_refresh(self):
        def mutate(root):
            product = root / PRODUCT
            product.write_text(
                product.read_text(encoding="utf-8") + "\nEditorial change.\n",
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 3, combined_output(result))
        self.assertIn("REFRESH_REQUIRED:", combined_output(result))

    def test_missing_snapshot_requires_refresh(self):
        def mutate(root):
            spec = root / FEATURE
            text = spec.read_text(encoding="utf-8")
            start = text.index("## Feature Context Snapshot")
            end = text.index("## Product Slice")
            spec.write_text(text[:start] + text[end:], encoding="utf-8")

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 3, combined_output(result))

    def test_redirected_effective_product_requires_refresh(self):
        def mutate(root):
            requirement = root / README
            replacement = requirement.parent / "replacement.md"
            shutil.copy2(root / PRODUCT, replacement)
            requirement.write_text(
                requirement.read_text(encoding="utf-8").replace(
                    "Source: product.md", "Source: replacement.md"
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 3, combined_output(result))

    def test_missing_required_snapshot_field_requires_refresh(self):
        def mutate(root):
            spec = root / FEATURE
            spec.write_text(
                spec.read_text(encoding="utf-8").replace(
                    "Product Slice References: C-ACCOUNT / FLOW-RECHARGE / "
                    "STATE-RECHARGE / EX-PAYMENT-UNKNOWN / "
                    "product.md#confirmed-credit\n",
                    "",
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 3, combined_output(result))

    def test_unconfirmed_product_blocks(self):
        def mutate(root):
            readme = root / README
            readme.write_text(
                readme.read_text(encoding="utf-8").replace(
                    "Product Review: confirmed", "Product Review: pending"
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn("BLOCKED:", combined_output(result))

    def test_invalid_requirement_lifecycle_blocks(self):
        def mutate(root):
            readme = root / README
            readme.write_text(
                readme.read_text(encoding="utf-8").replace(
                    "Status: accepted", "Status: deferred"
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 1, combined_output(result))

    def test_unknown_product_slice_anchor_blocks(self):
        def mutate(root):
            spec = root / FEATURE
            spec.write_text(
                spec.read_text(encoding="utf-8").replace(
                    "product.md#confirmed-credit", "product.md#missing-rule"
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 1, combined_output(result))

    def test_unknown_product_slice_id_blocks(self):
        def mutate(root):
            spec = root / FEATURE
            spec.write_text(
                spec.read_text(encoding="utf-8").replace(
                    "FLOW-RECHARGE", "FLOW-NOT-DEFINED"
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 1, combined_output(result))

    def test_review_required_adr_blocks(self):
        def mutate(root):
            decision = root / DECISION
            decision.write_text(
                decision.read_text(encoding="utf-8").replace(
                    "Upstream Compatibility: current",
                    "Upstream Compatibility: review-required",
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 1, combined_output(result))

    def test_changed_adr_digest_requires_refresh(self):
        def mutate(root):
            decision = root / DECISION
            decision.write_text(
                decision.read_text(encoding="utf-8") + "\nEditorial note.\n",
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 3, combined_output(result))

    def test_missing_adr_blocks(self):
        def mutate(root):
            (root / DECISION).unlink()

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 1, combined_output(result))

    def test_project_root_escape_blocks(self):
        def mutate(root):
            spec = root / FEATURE
            spec.write_text(
                spec.read_text(encoding="utf-8").replace(
                    ".agent-loop/requirements/2026-07-25-example/README.md",
                    "../outside/README.md",
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 1, combined_output(result))

    def test_feature_relative_requirement_path_blocks(self):
        def mutate(root):
            spec = root / FEATURE
            spec.write_text(
                spec.read_text(encoding="utf-8").replace(
                    ".agent-loop/requirements/2026-07-25-example/README.md",
                    "../../requirements/2026-07-25-example/README.md",
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 1, combined_output(result))

    def test_invalid_verified_at_requires_refresh(self):
        def mutate(root):
            spec = root / FEATURE
            spec.write_text(
                spec.read_text(encoding="utf-8").replace(
                    "Verified At: 2026-07-25T12:00:00+08:00",
                    "Verified At: sometime yesterday",
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 3, combined_output(result))
        self.assertIn("Verified At", combined_output(result))

    def test_conflicting_applicable_decision_pointers_block(self):
        def mutate(root):
            spec = root / FEATURE
            spec.write_text(
                spec.read_text(encoding="utf-8").replace(
                    "Applicable Decisions: .agent-loop/decisions/0001-example.md",
                    "Applicable Decisions: none",
                    1,
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn("ambiguous Applicable Decisions", combined_output(result))

    def test_conflicting_product_source_pointers_block(self):
        def mutate(root):
            spec = root / FEATURE
            spec.write_text(
                spec.read_text(encoding="utf-8").replace(
                    "Effective Product Definition: "
                    ".agent-loop/requirements/2026-07-25-example/product.md",
                    "Effective Product Definition: "
                    ".agent-loop/requirements/2026-07-25-example/other.md",
                    1,
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn("ambiguous Effective Product Definition", combined_output(result))

    def test_conflicting_product_profiles_block(self):
        def mutate(root):
            spec = root / FEATURE
            spec.write_text(
                spec.read_text(encoding="utf-8").replace(
                    "Product Definition Profile: standard",
                    "Product Definition Profile: brief",
                    1,
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn("ambiguous Product Definition Profile", combined_output(result))

    def test_unconfirmed_product_requirement_source_evidence_blocks(self):
        def mutate(root):
            spec = root / FEATURE
            spec.write_text(
                spec.read_text(encoding="utf-8").replace(
                    "Product Review Evidence: confirmed by human maintainer",
                    "Product Review Evidence: pending human review",
                    1,
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn("Product Review Evidence", combined_output(result))

    def test_memory_root_symlink_blocks(self):
        def mutate(root):
            memory_root = root / ".agent-loop"
            real_memory = root / "real-memory"
            memory_root.rename(real_memory)
            memory_root.symlink_to(real_memory, target_is_directory=True)

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn("memory root", combined_output(result))

    def test_utf8_bom_and_crlf_are_accepted(self):
        def mutate(root):
            for relative in (README, PRODUCT, DECISION, FEATURE):
                path = root / relative
                value = path.read_text(encoding="utf-8")
                path.write_bytes(b"\xef\xbb\xbf" + value.replace("\n", "\r\n").encode())
            spec = root / FEATURE
            content = spec.read_text(encoding="utf-8")
            content = content.replace(
                "Product Source SHA-256: "
                "1e7bc739b3a32ec08481aab64fa4f39dd854896f885cd4fb222b4cef6b3dd3fd",
                f"Product Source SHA-256: {hashlib.sha256((root / PRODUCT).read_bytes()).hexdigest()}",
            )
            content = content.replace(
                "Decision Source SHA-256: .agent-loop/decisions/0001-example.md="
                "ef854d72b13067cf932fe2bdb68861ed6c4eb7a10ab02cff9c4efebf0730bf51",
                "Decision Source SHA-256: .agent-loop/decisions/0001-example.md="
                f"{hashlib.sha256((root / DECISION).read_bytes()).hexdigest()}",
            )
            spec.write_bytes(
                b"\xef\xbb\xbf" + content.replace("\n", "\r\n").encode("utf-8")
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 0, combined_output(result))


if __name__ == "__main__":
    unittest.main()

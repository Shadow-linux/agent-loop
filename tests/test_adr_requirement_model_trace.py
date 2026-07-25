from __future__ import annotations

import re
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.checker_test_support import ROOT, combined_output, run_checker


SCRIPT = "scripts/check-adr-requirement-model-trace.py"
FIXTURES = ROOT / "tests/fixtures/adr-technical-landing"
VALID = FIXTURES / "valid"
NOT_NEEDED = FIXTURES / "valid-not-needed"
PRODUCT_VALID = ROOT / "tests/fixtures/adaptive-product-definition/standard-valid"
PRODUCT_BRIEF = ROOT / "tests/fixtures/adaptive-product-definition/brief-valid"


class AdrRequirementModelTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.readme = (VALID / "README.md").read_text(encoding="utf-8")
        cls.source = (VALID / "requirement.md").read_text(encoding="utf-8")
        cls.decision = (VALID / "decision.md").read_text(encoding="utf-8")

    def run_documents(
        self,
        readme: str,
        source: str,
        decision: str,
        *,
        fixture: Path = VALID,
        bom_crlf: bool = False,
        workspace_root: str | None = None,
    ):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "fixture"
            shutil.copytree(fixture, root)
            paths = []
            for name, content in (
                ("README.md", readme),
                ("requirement.md", source),
                ("decision.md", decision),
            ):
                path = root / name
                if bom_crlf:
                    path.write_bytes(("\ufeff" + content.replace("\n", "\r\n")).encode("utf-8"))
                else:
                    path.write_text(content, encoding="utf-8")
                paths.append(str(path))
            args = [*paths]
            if workspace_root is not None:
                args.append(workspace_root.replace("{root}", str(root)))
            return run_checker(SCRIPT, *args)

    def assert_accepted(
        self, readme: str, source: str, decision: str, expected: str
    ) -> None:
        result = self.run_documents(readme, source, decision)
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn(expected, result.stdout)

    def assert_rejected(
        self, readme: str, source: str, decision: str, expected: str
    ) -> None:
        result = self.run_documents(readme, source, decision)
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn(expected, combined_output(result))

    def run_archived_feature_owner(
        self,
        *,
        include_index: bool = True,
        row_month: str = "2026-05",
        row_state: str = "archived",
        row_path: str | None = None,
        planned: bool = False,
    ):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "fixture"
            shutil.copytree(VALID, root)
            feature_id = "2026-05-08-login"
            archived = root / "features" / "2026-05" / feature_id
            archived.parent.mkdir(parents=True)
            (root / "features" / "fixture").rename(archived)
            spec = archived / "spec.md"
            spec.write_text(
                re.sub(
                    r"^Status: .*$",
                    "Status: closed",
                    spec.read_text(encoding="utf-8"),
                    flags=re.MULTILINE,
                ),
                encoding="utf-8",
            )
            owner = f"features/2026-05/{feature_id}/spec.md"
            if planned:
                owner = f"planned:{owner}"
            decision = self.decision.replace("features/fixture/spec.md", owner)
            (root / "README.md").write_text(self.readme, encoding="utf-8")
            (root / "requirement.md").write_text(self.source, encoding="utf-8")
            (root / "decision.md").write_text(decision, encoding="utf-8")
            if include_index:
                current_path = row_path or f".agent-loop/features/{row_month}/{feature_id}/"
                (root / "features" / "archive.md").write_text(
                    "# Feature Archive\n\n"
                    "This file locates archived or rehydrated features. Feature specs, tests, notes, requirement sources, and accepted decisions remain authoritative.\n\n"
                    "| Feature ID | Month | Current Path | Archive State | Closed At | Delivered Summary | Source Requirements | Applicable Decisions | Last Moved At |\n"
                    "|---|---|---|---|---|---|---|---|---|\n"
                    f"| {feature_id} | {row_month} | `{current_path}` | {row_state} | 2026-05-20 | completed login | none | none | 2026-07-14 |\n",
                    encoding="utf-8",
                )
            return run_checker(
                SCRIPT,
                str(root / "README.md"),
                str(root / "requirement.md"),
                str(root / "decision.md"),
                str(root),
            )

    def test_accepted_and_proposed_valid_decisions_pass(self) -> None:
        self.assert_accepted(
            self.readme,
            self.source,
            self.decision,
            "ADR accepted technical landing trace covers 8",
        )
        proposed = re.sub(r"^Status: accepted$", "Status: proposed", self.decision, flags=re.MULTILINE)
        proposed = re.sub(
            r"^## Human Review Evidence\n.*?(?=^## |\Z)",
            "",
            proposed,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assert_accepted(
            self.readme,
            self.source,
            proposed,
            "ADR proposed technical landing trace covers 8",
        )

    def test_accepted_decision_requires_human_review_evidence(self) -> None:
        decision = re.sub(
            r"^## Human Review Evidence\n.*?(?=^## |\Z)",
            "",
            self.decision,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assert_rejected(
            self.readme, self.source, decision, "missing section: ## Human Review Evidence"
        )

    def test_valid_not_needed_preflight_passes(self) -> None:
        result = self.run_documents(
            (NOT_NEEDED / "README.md").read_text(encoding="utf-8"),
            (NOT_NEEDED / "requirement.md").read_text(encoding="utf-8"),
            (NOT_NEEDED / "decision.md").read_text(encoding="utf-8"),
            fixture=NOT_NEEDED,
        )
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("reasoned concept-foundation-not-needed ADR proposed gate", result.stdout)

    def test_legacy_source_accepts_the_current_unified_gate_template(self) -> None:
        unified_gate = re.search(
            r"^## Coverage Hard Gate\n.*?(?=^## |\Z)",
            (PRODUCT_VALID / "decision.md").read_text(encoding="utf-8"),
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(unified_gate)
        decision = re.sub(
            r"^## Coverage Hard Gate\n.*?(?=^## |\Z)",
            unified_gate.group(0),
            self.decision,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assert_accepted(
            self.readme,
            self.source,
            decision,
            "ADR accepted technical landing trace covers 8",
        )

    def test_owner_paths_support_existing_and_explicitly_planned_artifacts(self) -> None:
        planned = self.decision.replace(
            "features/fixture/spec.md", "planned:features/future-fixture/spec.md"
        )
        self.assert_accepted(
            self.readme, self.source, planned, "technical landing trace covers 8"
        )
        delegated = self.decision.replace(", FLOW-FIXTURE-01", "", 1)
        delegated = delegated.replace(
            "| FLOW-FIXTURE-01 | in-scope | ADR-9000 |",
            "| FLOW-FIXTURE-01 | proposed-decision | decisions/9001-follow-up.md |",
        )
        delegated = re.sub(
            r"^\| FLOW-FIXTURE-01 \| source flow reference .*\n",
            "",
            delegated,
            flags=re.MULTILINE,
        )
        self.assert_accepted(
            self.readme, self.source, delegated, "technical landing trace covers 7"
        )

    def test_archived_closed_feature_spec_owner_passes_with_matching_locator(self) -> None:
        result = self.run_archived_feature_owner()
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("technical landing trace covers 8", result.stdout)

    def test_archived_feature_spec_owner_requires_archive_locator(self) -> None:
        result = self.run_archived_feature_owner(include_index=False)
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn("archive-index", combined_output(result))

    def test_archived_feature_spec_owner_rejects_mismatched_month_locator(self) -> None:
        result = self.run_archived_feature_owner(
            row_month="2026-06",
            row_path=".agent-loop/features/2026-06/2026-05-08-login/",
        )
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn("month", combined_output(result))

    def test_archived_feature_spec_owner_rejects_rehydrated_month_locator(self) -> None:
        result = self.run_archived_feature_owner(row_state="rehydrated")
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn("archive-index", combined_output(result))

    def test_planned_feature_spec_owner_must_remain_flat(self) -> None:
        result = self.run_archived_feature_owner(planned=True)
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn("planned Feature Spec path must be flat", combined_output(result))

    def test_adversarial_contracts_are_rejected(self) -> None:
        cases = (
            (
                self.decision.replace(
                    "reason: outside this coherent decision boundary", "reason: n/a"
                ),
                "must give a concrete reason",
            ),
            (
                re.sub(
                    r"## Coverage Hard Gate\n.*?(?=^## |\Z)",
                    "## Coverage Hard Gate\n\n- [x] arbitrary check\n\n",
                    self.decision,
                    flags=re.MULTILINE | re.DOTALL,
                ),
                "Coverage Hard Gate is missing required items",
            ),
            (
                self.decision.replace(
                    "- [x] No unresolved product-semantic blocker remains",
                    "- [x] No unresolved product-semantic blocker remains\n"
                    "- [x] arbitrary extra check",
                ),
                "Coverage Hard Gate contains unsupported items",
            ),
            (
                re.sub(
                    r"^Accepted Requirement Model IDs:(.*)$",
                    r"Accepted Requirement Model IDs:\1, GARBAGE",
                    self.decision,
                    flags=re.MULTILINE,
                ),
                "invalid values in ADR Accepted Requirement Model IDs: GARBAGE",
            ),
            (
                re.sub(
                    r"^\| PM-FIXTURE-FACT .*\n",
                    "",
                    self.decision.replace(", PM-FIXTURE-FACT", ""),
                    flags=re.MULTILINE,
                ),
                "Requirement Model Scope Inventory mismatch",
            ),
            (
                self.decision.replace(
                    "decisions/8999-shared.md (ADR-8999)",
                    "decisions/does-not-exist.md (ADR-DOES-NOT-EXIST)",
                ),
                "missing file:",
            ),
            (
                self.decision.replace(
                    "features/fixture/spec.md", "features/missing/spec.md"
                ),
                "missing file:",
            ),
            (
                self.decision.replace("| planned |", "| banana |", 1),
                "invalid coverage status: banana",
            ),
            (
                re.sub(
                    r"\n## Triggered Operational Landing\n.*?(?=\n## Design Slice Coverage)",
                    "",
                    self.decision,
                    flags=re.DOTALL,
                ),
                "Triggered Operational Landing is missing",
            ),
            (
                re.sub(
                    r"^\| (?:Compatibility|Rollout / Cutover|Rollback / Reversibility) \|.*\n",
                    "",
                    self.decision,
                    flags=re.MULTILINE,
                ),
                "operational concern inventory mismatch",
            ),
        )
        for decision, expected in cases:
            with self.subTest(expected=expected):
                self.assert_rejected(self.readme, self.source, decision, expected)

    def test_existing_invalid_decisions_and_sources_are_rejected(self) -> None:
        cases = (
            (
                self.readme,
                self.source,
                (FIXTURES / "invalid-missing-coverage/decision.md").read_text(encoding="utf-8"),
            ),
            (
                self.readme,
                self.source,
                (FIXTURES / "invalid-empty-landing/decision.md").read_text(encoding="utf-8"),
            ),
            (
                (FIXTURES / "invalid-unaccepted-source/README.md").read_text(encoding="utf-8"),
                (FIXTURES / "invalid-unaccepted-source/requirement.md").read_text(encoding="utf-8"),
                self.decision,
            ),
            (
                (FIXTURES / "invalid-reopened-source/README.md").read_text(encoding="utf-8"),
                (FIXTURES / "invalid-reopened-source/requirement.md").read_text(encoding="utf-8"),
                self.decision,
            ),
            (
                self.readme,
                self.source,
                (FIXTURES / "invalid-review-required/decision.md").read_text(encoding="utf-8"),
            ),
        )
        for readme, source, decision in cases:
            with self.subTest(decision=decision[:40]):
                result = self.run_documents(readme, source, decision)
                self.assertEqual(result.returncode, 1, combined_output(result))

    def test_workspace_escape_is_rejected(self) -> None:
        decision = self.decision.replace(
            "decisions/8999-shared.md (ADR-8999)", "../outside.md (ADR-OUTSIDE)"
        )
        self.assert_rejected(
            self.readme, self.source, decision, "reference escapes workspace root"
        )

    def test_bom_and_crlf_are_supported(self) -> None:
        result = self.run_documents(
            self.readme, self.source, self.decision, bom_crlf=True
        )
        self.assertEqual(result.returncode, 0, combined_output(result))


class ProductDefinitionAdrTraceTests(unittest.TestCase):
    @staticmethod
    def product_rules_only_source(value: str) -> str:
        value = re.sub(
            r"\n## Concept Definitions\n.*?(?=\n## Product Rules\n)",
            "\n",
            value,
            flags=re.DOTALL,
        )
        applicability_rows = {
            "Concepts": "no stable product concept identity is required for this rule-only definition",
            "Relationships": "no stable concept relationship is required for this rule-only definition",
            "Permissions": "the accepted authority constraint is owned directly by the Product Rule",
            "Actions / Outcomes": "no stable command or event model is required for this rule-only definition",
            "Flow": "no multi-step product flow is required for this rule-only definition",
            "State": "no product state lifecycle is required for this rule-only definition",
            "Product Facts": "no separate durable product fact model is required for this rule-only definition",
            "Exceptions / Recovery": "no separate exception model is required for this rule-only definition",
        }
        for view, reason in applicability_rows.items():
            value = re.sub(
                rf"^\| {re.escape(view)} \|.*$",
                f"| {view} | not-applicable | {reason} | none |",
                value,
                flags=re.MULTILINE,
            )
        value = value.replace(
            "Only an actor satisfying PERM-APPROVE may apply CMD-APPROVE to C-REQUEST; submission never implies approval.",
            "Only an authorized reviewer may approve an eligible request; submission never implies approval.",
        )
        value = value.replace(
            "PERM-APPROVE / CMD-APPROVE / STATE-REQUEST / product.md#approval-authority",
            "product.md#approval-authority",
        )
        return value.replace(
            "| approval persistence and consistency | technical landing must preserve PM-APPROVAL | Decision & Design | proposed |",
            "| approval persistence and consistency | technical landing must preserve product.md#approval-authority | Decision & Design | proposed |",
        )

    @staticmethod
    def product_rules_only_decision(value: str) -> str:
        value = re.sub(
            r"^Accepted Concept IDs:.*$",
            "Accepted Concept IDs: none",
            value,
            flags=re.MULTILINE,
        )
        value = re.sub(
            r"^Accepted Requirement Model IDs:.*$",
            "Accepted Requirement Model IDs: none",
            value,
            flags=re.MULTILINE,
        )
        value = re.sub(
            r"^## Requirement Model Scope Inventory\n.*?(?=^## )",
            "## Requirement Model Scope Inventory\n\n"
            "| Requirement Model Ref | Scope Disposition | Owner / Reason |\n"
            "|---|---|---|\n"
            "| product.md#approval-authority | in-scope | ADR-9100 |\n\n",
            value,
            flags=re.MULTILINE | re.DOTALL,
        )
        return re.sub(
            r"^## Requirement Model Technical Landing Trace\n.*?(?=^## )",
            "## Requirement Model Technical Landing Trace\n\n"
            "| Requirement Model Ref | Accepted Meaning / Constraint | Disposition | Technical Landing | Preserved Invariant | Design Slice | Verification |\n"
            "|---|---|---|---|---|---|---|\n"
            "| product.md#approval-authority | preserve the accepted approval authority rule | landed | approval authorization policy | unauthorized actors cannot approve | DS-APPROVAL | authority rule verification |\n\n",
            value,
            flags=re.MULTILINE | re.DOTALL,
        )

    def run_product_decision(
        self,
        *,
        readme_mutation=lambda value: value,
        product_mutation=lambda value: value,
        decision_mutation=lambda value: value,
    ):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            values = {
                "README.md": readme_mutation(
                    (PRODUCT_VALID / "README.md").read_text(encoding="utf-8")
                ),
                "product.md": product_mutation(
                    (PRODUCT_VALID / "product.md").read_text(encoding="utf-8")
                ),
                "decision.md": decision_mutation(
                    (PRODUCT_VALID / "decision.md").read_text(encoding="utf-8")
                ),
            }
            for name, content in values.items():
                (root / name).write_text(content, encoding="utf-8")
            return run_checker(
                SCRIPT,
                str(root / "README.md"),
                str(root / "product.md"),
                str(root / "decision.md"),
                str(root),
            )

    def run_brief_decision(self, decision_mutation=lambda value: value):
        decision = (NOT_NEEDED / "decision.md").read_text(encoding="utf-8")
        snapshot = (
            "## Effective Requirement Snapshot\n\n"
            "Effective Product Source: product.md\n"
            "Product Definition Profile: brief\n"
            "Product Review: confirmed\n"
            "Accepted Concept IDs: none\n"
            "Accepted Requirement Model IDs: none\n"
            "Accepted Product Rule References: none\n"
            "Upstream Compatibility: current\n"
            "Last Compatibility Check: 2026-07-22\n"
            "Trace Applicability: not-applicable\n"
            "Trace Not-Applicable Reason: the confirmed Brief contains no stable product-model IDs or accepted Product Rule references\n\n"
        )
        decision = re.sub(
            r"^## Effective Requirement Snapshot\n.*?(?=^## |\Z)",
            snapshot,
            decision,
            flags=re.MULTILINE | re.DOTALL,
        )
        unified_gate = re.search(
            r"^## Coverage Hard Gate\n.*?(?=^## |\Z)",
            (PRODUCT_VALID / "decision.md").read_text(encoding="utf-8"),
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(unified_gate)
        decision = re.sub(
            r"^## Coverage Hard Gate\n.*?(?=^## |\Z)",
            unified_gate.group(0),
            decision,
            flags=re.MULTILINE | re.DOTALL,
        )
        decision = decision_mutation(decision)

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("README.md", "product.md"):
                shutil.copy2(PRODUCT_BRIEF / name, root / name)
            (root / "decision.md").write_text(decision, encoding="utf-8")
            return run_checker(
                SCRIPT,
                str(root / "README.md"),
                str(root / "product.md"),
                str(root / "decision.md"),
                str(root),
            )

    def test_new_product_definition_adr_passes(self) -> None:
        result = self.run_product_decision()
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("covers 11 in-scope", result.stdout)

    def test_standard_product_rules_only_allows_none_concept_and_model_ids(
        self,
    ) -> None:
        result = self.run_product_decision(
            product_mutation=self.product_rules_only_source,
            decision_mutation=self.product_rules_only_decision,
        )
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("covers 1 in-scope", result.stdout)

    def test_none_concept_ids_do_not_bypass_declared_source_concepts(self) -> None:
        result = self.run_product_decision(
            decision_mutation=lambda value: re.sub(
                r"^Accepted Concept IDs:.*$",
                "Accepted Concept IDs: none",
                value,
                flags=re.MULTILINE,
            )
        )
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn(
            "ADR scope must name accepted Concept IDs", combined_output(result)
        )

    def test_none_model_ids_do_not_bypass_declared_source_models(self) -> None:
        result = self.run_product_decision(
            decision_mutation=lambda value: re.sub(
                r"^Accepted Requirement Model IDs:.*$",
                "Accepted Requirement Model IDs: none",
                value,
                flags=re.MULTILINE,
            )
        )
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn(
            "ADR scope must name accepted Requirement Model IDs",
            combined_output(result),
        )

    def test_confirmed_brief_allows_reasoned_not_applicable_trace(self) -> None:
        result = self.run_brief_decision()
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("reasoned confirmed Brief ADR proposed gate", result.stdout)

    def test_reasoned_brief_rejects_fabricated_model_sections(self) -> None:
        sections = {
            "Concept Definitions": (
                "| Concept ID | Canonical Name | Definition |\n"
                "|---|---|---|\n"
                "| C-FAKE | fabricated concept | invented product meaning |\n\n"
            ),
            "Requirement Model Scope Inventory": (
                "| Requirement Model / Rule Reference | Scope Disposition | Owner / Reason |\n"
                "|---|---|---|\n"
                "| PM-FAKE | in-scope | this ADR |\n\n"
            ),
            "Requirement Model Technical Landing Trace": (
                "| Requirement Model / Rule Reference | Accepted Meaning / Rule | Disposition | Technical Landing | Preserved Invariant | Design Slice | Verification |\n"
                "|---|---|---|---|---|---|---|\n"
                "| PM-FAKE | fabricated meaning | landed | fake.service | fake invariant | DS-NOT-NEEDED-01 | fake verification |\n\n"
            ),
        }
        for heading, body in sections.items():
            with self.subTest(heading=heading):
                result = self.run_brief_decision(
                    lambda value, heading=heading, body=body: value.replace(
                        "## Operational Landing Trigger Assessment",
                        f"## {heading}\n\n{body}"
                        "## Operational Landing Trigger Assessment",
                    )
                )
                self.assertEqual(result.returncode, 1, combined_output(result))
                self.assertIn(
                    f"reasoned no-model ADR must omit {heading}",
                    combined_output(result),
                )

    def test_reasoned_legacy_source_rejects_fabricated_model_sections(self) -> None:
        readme = (NOT_NEEDED / "README.md").read_text(encoding="utf-8")
        source = (NOT_NEEDED / "requirement.md").read_text(encoding="utf-8")
        decision = (NOT_NEEDED / "decision.md").read_text(encoding="utf-8")
        decision = decision.replace(
            "## Operational Landing Trigger Assessment",
            "## Requirement Model Scope Inventory\n\n"
            "| Requirement Model ID | Scope Disposition | Owner / Reason |\n"
            "|---|---|---|\n"
            "| PM-FAKE | in-scope | this ADR |\n\n"
            "## Operational Landing Trigger Assessment",
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name, content in (
                ("README.md", readme),
                ("requirement.md", source),
                ("decision.md", decision),
            ):
                (root / name).write_text(content, encoding="utf-8")
            result = run_checker(
                SCRIPT,
                str(root / "README.md"),
                str(root / "requirement.md"),
                str(root / "decision.md"),
                str(root),
            )
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn(
            "reasoned no-model ADR must omit Requirement Model Scope Inventory",
            combined_output(result),
        )

    def test_new_snapshot_rejects_legacy_metadata_shape(self) -> None:
        result = self.run_product_decision(
            decision_mutation=lambda value: value.replace(
                "Effective Product Source: product.md",
                "Effective Product Source: product.md\n"
                "Effective Concept Source: requirement.md\n"
                "Concept Foundation Status: accepted",
            )
        )
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn(
            "ADR snapshot must not mix Product Definition and legacy Concept Foundation metadata",
            combined_output(result),
        )

    def test_new_adr_rejects_unknown_product_rule_anchor(self) -> None:
        result = self.run_product_decision(
            decision_mutation=lambda value: value.replace(
                "product.md#approval-authority", "product.md#unknown-authority"
            )
        )
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn(
            "unknown Product Rule references", combined_output(result)
        )

    def test_new_adr_rejects_review_required_compatibility(self) -> None:
        result = self.run_product_decision(
            decision_mutation=lambda value: value.replace(
                "Upstream Compatibility: current",
                "Upstream Compatibility: review-required",
            )
        )
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn("Upstream Compatibility must be current", combined_output(result))

    def test_new_adr_rejects_unconfirmed_product_source(self) -> None:
        result = self.run_product_decision(
            readme_mutation=lambda value: value.replace(
                "Product Review: confirmed", "Product Review: pending"
            )
        )
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn("Product Review must be confirmed", combined_output(result))


if __name__ == "__main__":
    unittest.main()

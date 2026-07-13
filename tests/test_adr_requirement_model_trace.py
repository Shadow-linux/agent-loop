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


if __name__ == "__main__":
    unittest.main()

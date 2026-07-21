from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates/root-AGENTS.md"
RUNTIME = ROOT / "references/runtime.md"
EXPECTED_REVISION = "1.5.0-20260721.2"

EXPECTED_SECTIONS = (
    ("bootstrap", ".agent-loop/project.md"),
    ("ownership", ".agent-loop/project.md"),
    ("message-intent", "agent-loop-skill"),
    ("workflow-stage-map", "agent-loop-skill"),
    ("gates", ".agent-loop/project.md"),
    ("required-stops", ".agent-loop/project.md"),
    ("completion", ".agent-loop/project.md"),
    ("submit", ".agent-loop/project.md"),
    ("artifacts", ".agent-loop/project.md"),
    ("architecture", ".agent-loop/project.md"),
    ("directory-guidance", ".agent-loop/project.md"),
    ("commands", ".agent-loop/project.md"),
    ("hard-constraints", ".agent-loop/project.md"),
)

EXPECTED_GATEWAYS = (
    ("No reliable memory", "Project Entry / Init", (
        "references/project-entry-scan.md", "references/project-guidance.md",
        "references/stage-guides.md",
    )),
    ("Remote source of truth", "Remote Project Discovery", (
        "references/remote-project-discovery.md",
    )),
    ("Memory conflicts or outside-loop work", "Recovery / Re-Adopt", (
        "references/recovery-and-backfill.md",
    )),
    ("Explicit closed-history archive or rehydrate", "Feature Monthly Archive", (
        "references/stage-guides.md", "references/artifact-rules.md",
        "references/feature-follow-up.md",
    )),
    ("Explicit Bug intent, regression evidence, or clear Feature ownership",
     "Bug / Feature Follow-up", (
        "references/bug-management.md", "references/feature-follow-up.md",
    )),
    ("Already-defined actionable ordinary non-Bug change that appears bounded, reversible, and exactly verifiable",
     "Lightweight Change Assessment", ("references/lightweight-change-lane.md",)),
    ("Product need, meaning, scope, or delivery phases are still being shaped",
     "Requirements Discussion", (
        "references/requirement-management.md", "references/requirement-product-grill.md",
    )),
    ("Human confirms requirement recording, acceptance, deferral, or lifecycle action",
     "Requirement Archive", (
        "references/requirement-management.md", "references/stage-guides.md",
    )),
    ("Durable newcomer documentation is requested after reliable Project Entry",
     "Evidence-Graph + DDD Onboarding", (
        "references/onboarding-knowledge-base.md",
    )),
    ("Accepted requirement needs shared technical landing before feature specification",
     "Decision & Design If Needed", ("references/project-decisions.md",)),
    ("Accepted upstream meaning is ready for implementation or current Feature work continues",
     "Feature Construction / Runtime Continuation", (
        "references/runtime.md", "references/stage-guides.md",
    )),
    ("Use, test, run, deploy, or diagnose current behavior without implementation approval",
     "Code-Guided Operational Support", (
        "references/stage-guides.md", "references/runtime.md",
    )),
    ("Create or manage a reusable project workflow", "Project Skill Creation / Update", (
        "references/project-skills.md", "references/skill-routing.md",
        "references/external-skill-adapters.md",
    )),
    ("Verified code integration leaves Agent Loop memory to reconcile",
     "Post-Merge Memory Reconciliation", ("references/memory-reconciliation.md",)),
    ("Submit, commit, PR, merge, release, publish, pause, close, or cleanup is requested",
     "Lifecycle Boundary", (
        "references/submit-and-integrate.md", "references/stage-guides.md",
    )),
    ("Ordinary question or discussion has no artifact or action intent", "Chat", (
        "references/runtime.md",
    )),
)

RUNTIME_LEAF_STAGES = (
    "Project Skill Creation / Update",
    "Requirement Archive",
    "Decision & Design If Needed",
    "Product Brief if Needed",
    "Brainstorm / Clarify if Needed",
    "Feature Follow-up And Flow-back if Needed",
    "Targeted Feature Scan if Needed",
    "Feature Spec",
    "Requirement Checklist",
    "Work Breakdown",
    "Delivery Contract If Needed",
    "Test Design",
    "E2E Discovery if Web",
    "Technical Design / Code Context",
    "Plan Gate / Plan if Needed",
    "Analyze Consistency",
    "Subagent Execution If Approved",
    "Execute Task / Story",
    "Verify",
    "Review",
    "Drift Check",
    "Project Memory Update",
    "Feature Completion Check",
    "Submit / Integrate",
    "Pause / Close",
)

OUTCOME_OWNER = (
    "Own the project outcome, not only the workflow: inspect all safely available "
    "code, Git, tests, documentation, environment, and memory evidence before asking "
    "the human, then continue through the authorized scope until verified completion "
    "or a concrete Human Gate."
)
CORE_SPINE = (
    "Inspect -> Classify Intent And Project State -> Recommend One Next Action "
    "-> Human Gate When Required -> Act Through Loaded Reference -> Verify "
    "-> Review / Drift -> Record Memory -> Submit / Pause / Close"
)
PRODUCT_SPINE = (
    "Requirements / Concept -> Decision / ADR If Needed -> Feature -> Plan "
    "-> Execute -> Verify / Review / Drift -> Memory -> Submit / Close"
)
GATE_CLASSES = (
    "Semantic Gate", "Scope And Risk Gate", "Execution Gate", "Evidence Gate",
    "External Mutation Gate", "Git And Lifecycle Gate",
)
ARTIFACT_AUTHORITY = (
    "Requirement owns human source and product meaning; Decision / ADR owns accepted "
    "technical landing; Feature owns implementation; Bug owns defect identity and "
    "lifecycle; Lightweight Execution Card owns bounded change evidence; project memory "
    "owns durable current facts."
)
FORBIDDEN_DETAIL = (
    "Requirement Model Scope Inventory",
    "Requirement Model Technical Landing Trace",
    ".archive-txn",
    "exact-row SHA-256",
    "Lane Rationale",
    "Result / Residuals",
    "pending_count",
    "90-day",
    "Expected Behavior Evidence",
    "Coverage Hard Gate",
)

START_RE = re.compile(
    r"^<!-- agent-loop:managed-start section:(?P<section>[^ ]+) "
    r"source:(?P<source>[^ ]+) block-version:(?P<version>[^ ]+) -->$"
)
REF_RE = re.compile(r"`(references/[^`]+\.md)`")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


def managed_blocks(text: str) -> list[tuple[str, str, str, str]]:
    blocks: list[tuple[str, str, str, str]] = []
    current: tuple[str, str, str] | None = None
    body: list[str] = []
    for line in text.splitlines():
        match = START_RE.match(line)
        if match:
            if current is not None:
                raise AssertionError("nested managed block")
            current = (match.group("section"), match.group("source"), match.group("version"))
            body = []
            continue
        if line.startswith("<!-- agent-loop:managed-end section:"):
            if current is None:
                raise AssertionError("managed end without start")
            expected = f"<!-- agent-loop:managed-end section:{current[0]} -->"
            if line != expected:
                raise AssertionError("managed end mismatch")
            blocks.append((*current, "\n".join(body)))
            current = None
            body = []
            continue
        if current is not None:
            body.append(line)
    if current is not None:
        raise AssertionError("unterminated managed block")
    return blocks


def gateway_rows(text: str) -> tuple[tuple[str, str, tuple[str, ...]], ...]:
    block_map = {section: body for section, _source, _version, body in managed_blocks(text)}
    rows: list[tuple[str, str, tuple[str, ...]]] = []
    for line in block_map["workflow-stage-map"].splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells[0] == "Signal family":
            continue
        rows.append((cells[0].replace("`", ""), cells[1].replace("`", ""),
                     tuple(REF_RE.findall(line))))
    return tuple(rows)


def contract_issues(text: str) -> list[str]:
    issues: list[str] = []
    line_count = len(text.splitlines())
    if line_count > 190:
        issues.append(f"line-count:{line_count}")
    if CJK_RE.search(text):
        issues.append("canonical-template-has-cjk")
    try:
        blocks = managed_blocks(text)
    except AssertionError as error:
        return [f"managed-blocks:{error}"]
    if tuple((section, source) for section, source, _version, _body in blocks) != EXPECTED_SECTIONS:
        issues.append("managed-section-shape")
    if any(version != EXPECTED_REVISION for _section, _source, version, _body in blocks):
        issues.append("managed-revision")
    rows = gateway_rows(text)
    if rows != EXPECTED_GATEWAYS:
        issues.append("gateway-contract")
    for _signal, _first_hop, references in rows:
        for reference in references:
            if not (ROOT / reference).is_file():
                issues.append(f"missing-reference:{reference}")
    for required in (OUTCOME_OWNER, CORE_SPINE, PRODUCT_SPINE, ARTIFACT_AUTHORITY):
        if required not in text:
            issues.append(f"missing-contract:{required[:32]}")
    for gate_class in GATE_CLASSES:
        if gate_class not in text:
            issues.append(f"missing-gate:{gate_class}")
    if "Auto modes do not bypass these six Gate classes." not in text:
        issues.append("auto-mode-gate-bypass")
    for required in (
        "Code changes alone never make a task or Feature done.",
        "Fresh verification, Review, Drift Check, and required Project Memory evidence precede completion.",
        "Feature Completion Check",
        "Feature Close Review",
    ):
        if required not in text:
            issues.append(f"missing-completion:{required}")
    if (
        "Submit, commit, push, PR, merge, tag, release, publish, pause, close, and cleanup remain independent Human Gates."
        not in text
    ):
        issues.append("missing-independent-lifecycle-gates")
    for forbidden in FORBIDDEN_DETAIL:
        if forbidden in text:
            issues.append(f"root-duplicates-detail:{forbidden}")
    return issues


class RootAgentsLosslessSlimmingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.template_text = TEMPLATE.read_text(encoding="utf-8")
        cls.runtime_text = RUNTIME.read_text(encoding="utf-8")

    def test_current_template_satisfies_lossless_contract(self) -> None:
        self.assertEqual(contract_issues(self.template_text), [])

    def test_runtime_leaf_stages_remain_ordered_and_gateway_owned(self) -> None:
        stage_order = self.runtime_text.split("## Stage Order", 1)[1].split(
            "## Stage Entry And Exit", 1
        )[0]
        positions = [stage_order.index(stage) for stage in RUNTIME_LEAF_STAGES]
        self.assertEqual(positions, sorted(positions))
        runtime_gateway = next(
            row for row in EXPECTED_GATEWAYS
            if row[1] == "Feature Construction / Runtime Continuation"
        )
        self.assertIn("references/runtime.md", runtime_gateway[2])

    def test_removing_gateway_is_rejected(self) -> None:
        line = next(line for line in self.template_text.splitlines(keepends=True)
                    if line.startswith("| No reliable memory |"))
        self.assertIn("gateway-contract", contract_issues(self.template_text.replace(line, "", 1)))

    def test_swapping_gateway_reference_is_rejected(self) -> None:
        mutated = self.template_text.replace(
            "`references/remote-project-discovery.md`",
            "`references/project-guidance.md`", 1,
        )
        self.assertIn("gateway-contract", contract_issues(mutated))

    def test_removing_project_outcome_ownership_is_rejected(self) -> None:
        mutated = self.template_text.replace(OUTCOME_OWNER, "", 1)
        self.assertTrue(any(issue.startswith("missing-contract:")
                            for issue in contract_issues(mutated)))

    def test_removing_gate_class_is_rejected(self) -> None:
        mutated = self.template_text.replace("Semantic Gate", "Meaning review", 1)
        self.assertIn("missing-gate:Semantic Gate", contract_issues(mutated))


if __name__ == "__main__":
    unittest.main()

# Root AGENTS Lossless Slimming Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Do not dispatch subagents unless the human separately authorizes one bounded dispatch.

**Goal:** Reduce canonical `templates/root-AGENTS.md` from 224 lines to at most 190 lines without weakening Agent ownership, first-hop routing, Human Gates, completion evidence, artifact authority, or access to any runtime leaf stage.

**Architecture:** Keep root `AGENTS.md` as a compact startup contract containing controller bootstrap, project-outcome ownership, message intent, first-hop gateways, grouped stops, completion, submit, and artifact authority. Keep the complete stage order and detailed Bug, Lightweight, ADR, Archive, Project Skill, and Memory Reconciliation algorithms in `SKILL.md`, `references/runtime.md`, and their owning references. Prove equivalence with an executable Python contract that checks exact gateway tuples, published-reference existence, runtime leaf-stage reachability, managed-block structure, mutation failures, and the 190-line ceiling before running the repository full-validation method.

**Tech Stack:** Markdown skill sources and templates, Python 3.10+ standard-library `unittest`, existing Bash/Ruby focused contracts, Git CLI read-only inspection, and the repository six-domain full-validation method. No third-party dependency, target-project `.agent-loop/` artifact, daemon, browser service, installed-skill synchronization, or Skill version change.

---

状态：已实施，等待 Human Review；未 commit / push / tag / release / installed-skill sync
设计来源：`docs/proposal/v1.5.x/root-agents-lossless-slimming.md`
计划日期：2026-07-21
工作分支：`alpha/v1.5.0`
当前 `HEAD`：`3063201a3fee0adad9846fa33e977df30405d295`
当前 Skill 版本：`1.5.0`，本计划不升级版本
当前 managed revision：`1.5.0-20260721.1`
目标 managed revision：`1.5.0-20260721.2`
审计对象：实施开始时 `alpha/v1.5.0` 的当前工作区，不是裸 `HEAD`

实施结果：Root `170 lines / 1883 words / 15357 bytes`，13/13 blocks 使用 `.2`；focused Python `33/33`、Root Shell `23/23`、全部 Shell `39/39`、全部 Python `221` cases、无 Git 历史源码快照维护测试 `2/2` 均通过；六域评分 `99.8/100 STRONG`，Critical/High/Medium `0/0/0`。

证据：

- RED：`docs/reports/agent-loop-v1.5.0-root-agents-lossless-slimming-red-baseline-2026-07-21.md`
- Full validation：`docs/reports/agent-loop-v1.5.0-full-validation-2026-07-21.1.md`

## Execution Boundary

- Repository perspective: maintain the Agent Loop skill source. Do not simulate a target project or create repository-root `.agent-loop/requirements/`, Feature, Bug, Change, or memory artifacts.
- The current worktree already contains approved, uncommitted root-routing and ownership changes, their focused tests, one full-validation report, and the accepted Proposal. Preserve them as implementation inputs.
- Do not run `git reset`, `git restore`, `git checkout --`, broad formatting, or cleanup that discards or rewrites the current approved dirty state.
- Do not create or switch a branch/worktree. Do not merge, rebase, cherry-pick, or modify either remote.
- Do not synchronize this source into Codex, Kimi Code, OpenCode, `.agents/skills/`, or any installed Skill directory.
- Do not bump `Version: 1.5.0`, `plugin.json`, README/Usage version labels, or Changelog version heading.
- Do not commit, push, tag, open a PR, merge, release, publish, delete a branch, or close the work. Stop at Human Review after fresh validation.
- Use `apply_patch` for manual edits. Preserve unrelated human-owned content and stop if another writer changes an overlapping file during execution.
- The accepted Proposal fixes semantics. Any discovery that requires changing a gateway family, Gate class, authority split, canonical stage order, or runtime precedence returns to Human Review before that semantic change.
- Historical Changelog sections, Proposals, Reports, and old `block-version` examples remain historical evidence. Only live consumers of the current revision move to `.2`.
- Full validation is mandatory because the root Stage Map projection and root guidance contract change. Focused tests alone cannot authorize completion.

## Stage Helper Resolution

| Field | Resolution |
|---|---|
| Stage | Plan Gate / Plan |
| Canonical candidate | `superpowers:writing-plans` — not exposed under that canonical name |
| Alias candidate | `writing-plans` |
| Resolved helper | `/Users/shaodowyd/.codex/skills/writing-plans/SKILL.md` |
| Status | `loaded` |
| Fallback | `no` |
| Method used | zero-context file map, exact contracts, bite-sized RED/GREEN steps, exact commands and expected outcomes, rollback, and self-review |
| Agent Loop override | save beside the accepted Proposal; no `docs/superpowers/`, automatic worktree, automatic subagent, Git/release action, installed-skill sync, or target-project artifact |

## Branch Context Evidence

- Native repository policy: root `AGENTS.md` is authoritative for source-repository maintenance.
- Current branch: `alpha/v1.5.0`.
- Full baseline commit: `3063201a3fee0adad9846fa33e977df30405d295`.
- Audit target: current working tree, including approved uncommitted changes listed in Task 0.
- Target release context: continue v1.5.0 development; no version bump and no release action.
- Customer isolation: not applicable.
- Git actions authorized by this plan: none.

## File Responsibility Map

### Create

- `tests/test_root_agents_lossless_slimming.py` — line ceiling, English-only canonical template, exact managed blocks, exact Gateway tuples, reference existence, runtime leaf-stage reachability, ownership, spines, grouped Gates, completion/submit/artifact authority, forbidden root-level algorithm detail, and mutation pressure.
- `docs/reports/agent-loop-v1.5.0-root-agents-lossless-slimming-red-baseline-2026-07-21.md` — current-worktree baseline, pre-change full mechanical result, focused RED output, and expected-failure analysis.
- `docs/reports/agent-loop-v1.5.0-full-validation-2026-07-21.1.md` — post-slimming Chinese six-domain audit and fresh focused/full evidence. Keep the unsuffixed 2026-07-21 report as pre-slimming evidence.

### Modify: Production Contract

- `templates/root-AGENTS.md` — compress to 170–185 recommended lines and at most 190 lines; preserve all 13 managed identities/sources; use revision `.2`; replace leaf-stage rows with the exact first-hop Gateway table.
- `references/runtime.md` — state that root projects first hops while this file owns full Stage Order and precedence; do not reorder, add, or remove stages.
- `references/design.md` — state root startup-contract versus published runtime/detail ownership; do not change the core model, status, intent, or Gate semantics.
- `references/project-guidance.md` — replace complete `Workflow Stage Map` assumptions with the `Workflow Gateway Map` startup contract and retain managed refresh plus human-content preservation.
- `references/workflow-checklists.md` — validate Gateway presence, revision, ownership, grouped stops, and reference loading instead of demanding every runtime leaf row in root.
- `references/validation-scenarios.md` — add delegation and mutation scenarios; update live `.1` revision examples to `.2`.
- `CHANGELOG.md` — record lossless slimming, delegation, mutation coverage, `.2`, and unchanged Skill version.
- `docs/proposal/v1.5.x/root-agents-lossless-slimming.md` — after GREEN/full validation, record implementation evidence without rewriting design.
- `docs/proposal/v1.5.x/root-agents-lossless-slimming-implementation-plan.md` — mark only actually completed steps.

### Modify: Live Revision Consumers

- `tests/test_root_agents_blocks.py`
- `tests/validate-branch-management-strategy.sh`
- `tests/validate-bug-management.sh`
- `tests/validate-lightweight-change-lane.sh`
- `tests/validate-project-local-skills.sh`
- `tests/validate-project-skill-discovery-guard.sh`
- `tests/validate-requirement-lifecycle-backlog.sh`
- `tests/validate-root-agents-block-checker.sh`
- `tests/validate-root-agents-block-refresh.sh`
- `tests/validate-v1.2.4-root-stage-coverage.sh`

Change current revision assertions from `.1` to `.2`. Historical revision fixtures that deliberately model stale input remain unchanged.

### Modify: Root Assertion Owners

- Requirements: `tests/validate-chat-requirements-entry.sh`, `tests/validate-concept-foundation-requirement-modeling.sh`, `tests/validate-requirement-product-grill.sh`.
- ADR: `tests/validate-project-decisions-adr-lane.sh`, `tests/validate-decision-design-requirement-landing.sh`, `tests/validate-adr-requirement-model-technical-landing-trace.sh`.
- Archive/Memory: `tests/validate-feature-monthly-archive-runtime.sh`, `tests/validate-post-merge-memory-reconciliation.sh`.
- Operational/Bootstrap: `tests/validate-operational-support-guard.sh`, `tests/validate-skill-reentry-guidance.sh`, `tests/validate-v1.2.3-routing-fixes.sh`, `tests/validate-v1.2.4-critical-control-repairs.sh`, `tests/validate-v1.2.4-postfix-pressure-repairs.sh`.

For every migrated assertion: root owns intent/first-hop/Gate/reference; the owning reference keeps algorithm detail; runtime keeps precedence and leaf order. Do not delete an invariant without adding its new owner assertion.

### Run Unchanged

- `scripts/check-root-agents-blocks.py` — managed section identities remain stable.
- `tests/test_python_checker_contract.py` — must continue passing without assertion edits.
- `tests/validate-maintainer-full-validation-guidance.sh` — maintainer-only full-validation routing stays unchanged.
- All other `tests/*.sh` and `tests/test_*.py` — full regression boundary.
- `README.md`, `Usage.md`, `SKILL.md`, and `plugin.json` — behavior/version remains unchanged; verify accuracy but do not edit for a projection-only change.

## Non-Negotiable Invariants

1. Canonical `templates/root-AGENTS.md` is English-only and at most 190 physical lines; 170–185 is recommended.
2. The 13 sections remain exactly: `bootstrap`, `ownership`, `message-intent`, `workflow-stage-map`, `gates`, `required-stops`, `completion`, `submit`, `artifacts`, `architecture`, `directory-guidance`, `commands`, `hard-constraints`.
3. Section order and `source` values remain unchanged; all current revisions become `1.5.0-20260721.2`.
4. Marker identity stays `section:workflow-stage-map`; the human heading becomes `Workflow Gateway Map`.
5. Root owns controller bootstrap, intent, first hop, ownership, Gates, completion, submit, and artifact projection. `runtime.md` owns complete order; detailed references own algorithms.
6. Controller unavailable/load-failed remains fail-closed: Strict Mode, suspended auto grants, limited read-only fallback, and no Execute/Human-gated write/Submit/Pause/Close.
7. Preserve the project-outcome sentence byte-for-byte and keep evidence-first continuation, unique next action, missing-artifact recommendation, autonomous diagnosis/verification/review/drift/memory, and meaningful stage reports.
8. Keep Core workflow and Product delivery spines visible.
9. The Gateway table contains exactly 16 rows and exact reference sets; no combined row hides an independent entry.
10. Already-defined/actionable wording remains part of Lightweight routing so demand shaping cannot bypass Requirements Discussion.
11. Explicit Bug/owned regression precedes Lightweight; Requirements precede archive/Feature construction; lifecycle actions do not inherit implementation authority.
12. Preserve six visible classes: Semantic, Scope And Risk, Execution, Evidence, External Mutation, Git And Lifecycle. Auto modes bypass none.
13. Requirement, Feature, Project Skill, Delivery Contract, Archive, subagent, external mutation, Git, submit, pause, and close authorities remain independent.
14. Code changes alone never make work `done`; fresh verification, Review, Drift Check, and required memory evidence precede completion.
15. Feature Completion Check and Feature Close Review remain reachable.
16. Requirement owns human source/product meaning; Decision/ADR technical landing; Feature implementation; Bug defect identity/lifecycle; Lightweight card bounded evidence; project memory durable current facts.
17. Root does not duplicate ADR trace tables, archive transactions, Bug lookback, Change scan counters, or Project Skill manifests.
18. Managed refresh preserves all target-project bytes outside approved blocks.
19. No stage, intent, status, lifecycle, Auto Mode, or Skill version is added/removed/renamed/reordered.
20. Final validation requires score `>= 99`, `STRONG`, and zero current Critical/High/Medium findings.

## Exact Gateway And Test Contract

`tests/test_root_agents_lossless_slimming.py` is the machine-readable acceptance source. Use this complete contract:

```python
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
```

The implementation may factor test-only helpers within this file, but it must not weaken constants, exact tuple equality, mutation assertions, or filesystem reference checks.

## Task 0: Re-establish The Live Working-Tree Baseline

**Files:**

- Read: `AGENTS.md`, `SKILL.md`, `references/runtime.md`, `references/design.md`
- Read: `references/implementation-planning.md`, `references/skill-routing.md`, `references/external-skill-adapters.md`
- Read: `docs/proposal/v1.5.x/root-agents-lossless-slimming.md`
- Read: `docs/maintenance/full-validation-method.md`
- Read: every path from `git status --short`
- Create later: `docs/reports/agent-loop-v1.5.0-root-agents-lossless-slimming-red-baseline-2026-07-21.md`

- [x] **Step 0.1: Confirm branch, HEAD, audit object, and dirty-state ownership**

Run:

```bash
git status --short --branch
git branch --show-current
git rev-parse HEAD
git diff --stat
git diff -- templates/root-AGENTS.md references/project-guidance.md references/workflow-checklists.md
```

Expected:

```text
branch: alpha/v1.5.0
HEAD: 3063201a3fee0adad9846fa33e977df30405d295
audit object: current working tree
templates/root-AGENTS.md: 224 lines before slimming
approved root-routing/ownership changes remain visible
no target-project .agent-loop/ artifact, __pycache__, unresolved conflict, or unexplained unrelated change
```

If branch/HEAD differs, another writer overlaps a listed file, or an unrelated path cannot be classified, stop and report evidence before editing.

- [x] **Step 0.2: Re-read mandatory authority and accepted design completely**

Expected: source-maintainer perspective is active; the accepted Proposal, not historical commit `1980368`, controls implementation.

- [x] **Step 0.3: Record current root shape**

Run:

```bash
wc -l -w -c templates/root-AGENTS.md
grep -c '^<!-- agent-loop:managed-start' templates/root-AGENTS.md
grep '^<!-- agent-loop:managed-start' templates/root-AGENTS.md
python3 - <<'PY'
from pathlib import Path
text = Path('templates/root-AGENTS.md').read_text(encoding='utf-8')
assert 'Own the project outcome, not only the workflow' in text
assert len(text.splitlines()) == 224
assert text.count('block-version:1.5.0-20260721.1') == 13
print('PASS: pre-slimming root shape is 224 lines, 13 blocks, revision .1')
PY
```

Expected: 224 lines, 13 blocks, and `.1` on all start markers.

- [x] **Step 0.4: Run the pre-change full mechanical baseline**

Run:

```bash
shell_total=0
shell_pass=0
for test_file in tests/*.sh; do
  shell_total=$((shell_total + 1))
  if bash "$test_file"; then
    shell_pass=$((shell_pass + 1))
  else
    printf 'FAILED SHELL TEST: %s\n' "$test_file" >&2
    exit 1
  fi
done
printf 'shell: %s/%s PASS\n' "$shell_pass" "$shell_total"

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
python3 -c 'import json; json.load(open("plugin.json", encoding="utf-8"))'
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
python3 - <<'PY'
from pathlib import Path
for path in Path('.').rglob('*.md'):
    fence = None
    length = 0
    for line in path.read_text(encoding='utf-8').splitlines():
        stripped = line.lstrip()
        if fence is None and (stripped.startswith('```') or stripped.startswith('~~~')):
            fence = stripped[0]
            length = len(stripped) - len(stripped.lstrip(fence))
        elif fence is not None and stripped.startswith(fence * length):
            fence = None
            length = 0
    if fence is not None:
        raise SystemExit(f'unclosed Markdown fence: {path}')
print('PASS: Markdown fence balance')
PY
git diff --check
```

Expected: all existing Shell/Python tests and mechanical checks pass. Capture live counts; do not copy prior totals without this run.

## Task 1: Add The Lossless-Slimming RED Contract

**Files:**

- Create: `tests/test_root_agents_lossless_slimming.py`
- Create: `docs/reports/agent-loop-v1.5.0-root-agents-lossless-slimming-red-baseline-2026-07-21.md`
- Test: `tests/test_root_agents_lossless_slimming.py`

- [x] **Step 1.1: Create the focused contract before editing production guidance**

Create `tests/test_root_agents_lossless_slimming.py` from **Exact Gateway And Test Contract**. Do not edit `templates/root-AGENTS.md` in this step.

- [x] **Step 1.2: Run and preserve the intended RED**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_root_agents_lossless_slimming
```

Expected: FAIL in `test_current_template_satisfies_lossless_contract` with at least:

```text
line-count:224
managed-revision
gateway-contract
missing-contract
missing-gate
root-duplicates-detail
```

Mutation tests may also fail before Gateway rows exist; preserve full output.

- [x] **Step 1.3: Prove the harness is sound**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_root_agents_blocks
bash tests/validate-root-agents-block-checker.sh
```

Expected: existing `.1` structural contracts pass; only the new `.2` slimming contract is RED.

- [x] **Step 1.4: Write the RED report**

Create `docs/reports/agent-loop-v1.5.0-root-agents-lossless-slimming-red-baseline-2026-07-21.md` with:

```markdown
# Agent Loop v1.5.0 Root AGENTS Lossless Slimming RED Baseline

- 日期：2026-07-21
- 分支：`alpha/v1.5.0`
- HEAD：`3063201a3fee0adad9846fa33e977df30405d295`
- 审计对象：当前工作区
- Production template：224 行、13 managed blocks、revision `.1`

## 实施前机械基线

| 检查 | 结果 |
|---|---|
| Existing `tests/*.sh` | 本次真实计数 |
| Existing Python tests | 本次真实计数 |
| YAML / JSON / Shell syntax / Markdown fences / `git diff --check` | PASS |

## Focused RED

记录 `tests.test_root_agents_lossless_slimming` 的真实失败输出，证明当前模板仍是 224 行 leaf-stage 投影，尚未满足 `.2` Gateway 和分组 Gate 契约。

## RED 结论

Existing behavior baseline is green; the new lossless-slimming contract is red for the intended production gap. Production edits may begin.
```

Replace the two count cells and RED text with live evidence; do not write guessed totals.

## Task 2: Compress The Canonical Root Startup Contract

**Files:**

- Modify: `templates/root-AGENTS.md`
- Test: `tests/test_root_agents_lossless_slimming.py`
- Test: `tests/test_root_agents_blocks.py`

- [x] **Step 2.1: Preserve exact structure and move revision to `.2`**

Keep the 13 section identities/order/sources from `EXPECTED_SECTIONS`. Change all start markers to `block-version:1.5.0-20260721.2`. Keep marker identity `workflow-stage-map`; use heading `## Workflow Gateway Map`.

- [x] **Step 2.2: Rewrite Bootstrap into eight responsibilities**

Express these in one numbered list and no more than 14 body lines:

```text
root is a bootstrap cache; load Agent Loop at entry/re-entry/uncertain stage
controller unavailable/load-failed => Strict + suspended auto grants + limited read-only fallback
discover one .agent-loop/ or legacy root; no reliable memory => Project Entry / Init
read only stage-relevant memory, remote entry, Active Feature, and linked detail
stale/outside-loop/remote conflict => Recovery or Remote Discovery before reliance
Project Skill discovery precedes generic executable fallback; loading never executes
Stage Helper scan happens after controller activation
inspect closest directory guidance, classify, and recommend one next action
```

- [x] **Step 2.3: Keep ownership and both spines exact**

Include `OUTCOME_OWNER`, `CORE_SPINE`, and `PRODUCT_SPINE` byte-for-byte. Compact remaining ownership duties to unique next action, missing artifact recommendation, autonomous diagnosis/verification/review/drift/memory, controller ownership over helpers, and meaningful stage reports.

- [x] **Step 2.4: Keep distinct Message Intent families**

Preserve Chat, Requirements, already-defined ordinary non-Bug change, explicit Bug/Follow-up, Feature Request, Operational Support, Project Skill, Archive/Rehydrate, Memory Reconciliation, Proposal/Deferred/Lifecycle. State that latest-message intent may change and one blocking question is asked only after safely available evidence is inspected.

- [x] **Step 2.5: Install the exact 16-row Gateway table**

Use `EXPECTED_GATEWAYS` in exact order and this header:

```markdown
| Signal family | First Hop | Load From agent-loop Skill |
|---|---|---|
```

Keep precedence:

```text
Safety Stop -> Remote Discovery -> Memory Recovery -> Feature Archive Maintenance -> Active Feature Guard -> Blocker Resolution -> Intent Routing -> Normal Stage Continuation
```

State that Product Brief, Feature Spec, Checklist, Breakdown, Contract, Test/E2E, Technical Design, Plan, Execute, Verify, Review, Drift, Memory, Completion, and lifecycle order is owned by `references/runtime.md` and loaded references.

- [x] **Step 2.6: Group Required Stops under six Gate classes**

Use these minimum sentences:

```text
Semantic Gate: Requirement, Concept, acceptance, Product, or Decision / ADR meaning is unresolved or would be redefined downstream.
Scope And Risk Gate: scope expansion or architecture, security, data, permission, dependency, migration, public interface, customer isolation, or durable boundary changes.
Execution Gate: Requirement/Feature lifecycle, plan execution, Project Skill, subagent, Delivery Contract, Archive/rehydrate, or another independently authorized action.
Evidence Gate: controller/infrastructure unavailable, repeated verification failure, memory/artifact conflict, blocking dirty work, or missing Review/Drift/Memory evidence.
External Mutation Gate: secrets, paid quota, credentials, configuration, external service, production/staging, deploy, release, or destructive action.
Git And Lifecycle Gate: branch mutation, commit, push, PR, merge, tag, release, publish, pause, close, reconciliation apply, or cleanup.
Auto modes do not bypass these six Gate classes.
```

- [x] **Step 2.7: Keep completion, submit, and authority exact**

Include:

```text
Code changes alone never make a task or Feature done.
Fresh verification, Review, Drift Check, and required Project Memory evidence precede completion.
Submit, commit, push, PR, merge, tag, release, publish, pause, close, and cleanup remain independent Human Gates.
Requirement owns human source and product meaning; Decision / ADR owns accepted technical landing; Feature owns implementation; Bug owns defect identity and lifecycle; Lightweight Execution Card owns bounded change evidence; project memory owns durable current facts.
```

Also retain Feature Completion Check, Feature Close Review, intended-file-only commit scope, unrelated human-work preservation, and post-integration memory reconciliation before applicable later gates.

- [x] **Step 2.8: Keep the four target-project extension blocks compact**

Preserve `Architecture Snapshot`, `Directory Guidance`, `Project Commands`, and `Project-Specific Hard Constraints`. Directory guidance still requires Human confirmation; command tokens remain `<test command>`, `<lint command>`, and `<typecheck command>`.

- [x] **Step 2.9: Check physical budget**

Run:

```bash
wc -l -w -c templates/root-AGENTS.md
python3 - <<'PY'
from pathlib import Path
import re
text = Path('templates/root-AGENTS.md').read_text(encoding='utf-8')
lines = len(text.splitlines())
assert lines <= 190, lines
assert text.count('<!-- agent-loop:managed-start') == 13
assert text.count('block-version:1.5.0-20260721.2') == 13
assert not re.search(r'[\u3400-\u4dbf\u4e00-\u9fff]', text)
print(f'PASS: root template {lines} lines, 13 blocks, English-only')
PY
```

Expected: `<=190`; 170–185 preferred. A result below 160 requires manual over-compression review.

- [x] **Step 2.10: Run focused GREEN and mutations**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tests.test_root_agents_lossless_slimming \
  tests.test_root_agents_blocks
```

Expected: every contract and mutation passes. If a mutation does not fail against mutated input, repair the test before more production edits.

## Task 3: Align Published Ownership And Root Guidance Rules

**Files:**

- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Modify: `references/project-guidance.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/validation-scenarios.md`
- Test: `tests/test_root_agents_lossless_slimming.py`
- Test: `tests/validate-root-agents-block-refresh.sh`
- Test: `tests/validate-v1.2.4-root-stage-coverage.sh`

- [x] **Step 3.1: Make runtime the explicit full-order owner**

Add near Runtime Contract without changing Stage Order:

```text
Root `AGENTS.md` is the startup projection: controller bootstrap, Message Intent, first-hop Workflow Gateway Map, Agent Ownership, Human Gates, completion, submit, and artifact authority. This file remains the executable owner of routing precedence and the complete leaf-stage order. A root gateway selects the owning reference family; it does not remove or reorder downstream stages.
```

Expected diff: one ownership clarification; no stage, precedence, intent, state, or Gate semantic change.

- [x] **Step 3.2: Record the same two-layer design model**

Add one core constraint near the current root-guidance bullets:

```text
root `AGENTS.md` is a compact startup contract and first-hop Gateway projection; `runtime.md` owns the complete executable Stage Order and owning references hold detailed algorithms
```

Do not repeat 16 Gateway rows in design.

- [x] **Step 3.3: Update project-guidance terminology and stale detection**

Use `Workflow Gateway Map` when describing current root content, while retaining managed section identity `workflow-stage-map`. Require Bootstrap, project-outcome Agent Ownership, Message Intent, exact reference-first Gateway routing, Gate Modes/six stop classes, Completion, Submit, and Artifact authority.

Remove stale-detection assumptions that root itself must repeat Operational Support, Feature Follow-up, requirement archive procedure, or every leaf stage. Their gateways and published owners satisfy startup reachability.

- [x] **Step 3.4: Update both root-guidance checklist locations**

Require:

```text
Workflow Gateway Map rather than a full leaf-stage table
project-outcome ownership and one next recommendation
revision .2 on all managed blocks
all Gateway references resolve in the installed package
six Gate classes and auto-mode non-bypass
runtime Stage Order for leaf-stage coverage
Human Review before managed writes and byte preservation outside approved blocks
```

- [x] **Step 3.5: Add delegation and mutation scenarios**

Add these exact scenario purposes under the root-guidance family:

```text
Root Gateway Delegates Complete Feature Construction: an accepted Feature at Work Breakdown loads runtime/current reference and does not skip Test Design, Plan, Verify, Review, Drift, or Memory.
Root Gateway Reference Is Swapped: replacing Remote Discovery's reference produces gateway-contract even when managed markers are current.
Root Gate Class Is Missing: removing External Mutation Gate makes the root projection incomplete and blocks Auto Mode through external effects.
Root Is Compact But Detailed Algorithm Is Restored: adding ADR trace or archive transaction detail fails the duplication contract and routes detail back to its published owner.
```

Update only live `.1` current-template examples to `.2`.

- [x] **Step 3.6: Inspect core-authority diff**

Run:

```bash
git diff -- references/runtime.md references/design.md references/project-guidance.md \
  references/workflow-checklists.md references/validation-scenarios.md
```

Expected: delegation/validation ownership only; no semantic expansion beyond the accepted Proposal.

## Task 4: Migrate Root Assertions And Revision Consumers

**Files:** all files under **Modify: Live Revision Consumers** and **Modify: Root Assertion Owners**.

- [x] **Step 4.1: Update only live revision consumers**

Run before and after editing:

```bash
rg -n '1\.5\.0-20260721\.1' tests references CHANGELOG.md docs/proposal docs/reports
```

Change `.1` to `.2` only where text claims the current root template revision. Keep `.1` in historical Changelog entries, the Proposal baseline, pre-slimming reports, and deliberate stale fixtures. Every remaining `.1` occurrence must be explainable.

- [x] **Step 4.2: Replace leaf-row coverage with Gateway/runtime coverage**

Rewrite `tests/validate-v1.2.4-root-stage-coverage.sh` to:

```text
check revision .2 on 13 blocks
run tests.test_root_agents_lossless_slimming
parse references/runtime.md Stage Order for RUNTIME_LEAF_STAGES
require Feature Construction / Runtime Continuation to reference runtime.md
retain coordinated-control assertions in source AGENTS.md
stop grepping every leaf as a root table row
```

End with:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_root_agents_lossless_slimming
printf 'PASS: root Gateway projection and runtime leaf-stage coverage are complete\n'
```

- [x] **Step 4.3: Move each detailed assertion to one owner**

Apply this exact rule to every file under **Modify: Root Assertion Owners**:

```text
root assertion = intent or first-hop Gateway + relevant Gate class + published reference path
owning-reference assertion = eligibility, lifecycle, trace, transaction, lookback, state, or algorithm detail
runtime assertion = precedence, controller fallback, or complete leaf-stage order
```

An old root invariant with no new owner assertion is a test regression and must be repaired before proceeding.

- [x] **Step 4.4: Preserve managed refresh/checker behavior**

Update revision and heading assertions in `tests/test_root_agents_blocks.py`, `tests/validate-root-agents-block-checker.sh`, and `tests/validate-root-agents-block-refresh.sh`. Keep section identity `workflow-stage-map`, missing/duplicate/stale/nested/source-escape/BOM/CRLF coverage, and unmanaged-byte preservation unchanged.

- [x] **Step 4.5: Run every root-consuming focused test**

Run:

```bash
for test_file in $(rg -l 'templates/root-AGENTS\.md' tests/*.sh | sort); do
  bash "$test_file"
done
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tests.test_root_agents_blocks \
  tests.test_python_checker_contract \
  tests.test_root_agents_lossless_slimming
```

Expected: all root-consuming tests pass. No invariant is skipped because prose moved to a published owner.

## Task 5: Changelog And Focused Semantic Closure

**Files:**

- Modify: `CHANGELOG.md`
- Test: all Task 1–4 files

- [x] **Step 5.1: Add unreleased v1.5.0 Changelog bullets**

Record:

```text
canonical root AGENTS changed from 224 to the measured final line count while retaining 13 blocks and startup-critical ownership/Gate/authority contracts
root leaf-stage duplication became an exact first-hop Workflow Gateway Map while references/runtime.md retained complete Stage Order authority
tuple, reference, leaf coverage, line/CJK, and mutation pressure tests were added; live consumers moved to block-version:1.5.0-20260721.2 without changing Skill version 1.5.0
```

Write the measured line count, not a generic range.

- [x] **Step 5.2: Run focused closure**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tests.test_root_agents_lossless_slimming \
  tests.test_root_agents_blocks \
  tests.test_python_checker_contract

for test_file in $(rg -l 'templates/root-AGENTS\.md|Workflow Stage Map|Workflow Gateway Map|root AGENTS' tests/*.sh | sort -u); do
  bash "$test_file"
done

wc -l -w -c templates/root-AGENTS.md
git diff --check
```

Expected: focused GREEN, mutation GREEN, root `<=190`, and no whitespace errors.

- [x] **Step 5.3: Perform manual semantic pressure review**

Record PASS/current issue with file/line evidence for:

```text
controller unavailable after context compaction
new project versus meaningful existing project
remote source versus local mirror
stale/outside-loop memory
requirements shaping versus already-defined Lightweight change
explicit Bug versus generic fix wording
accepted Requirement requiring ADR versus simple no-ADR Feature
Feature continuation at Product Brief, Checklist, Plan, Verify, and Drift leaves
Operational Support diagnosis versus implementation
Project Skill discovery/loading versus Execution Gate
Archive scan versus apply/rehydrate
post-code-merge memory reconciliation versus later Git gates
Auto Mode confronting each six Gate classes
completion with tests but missing Review/Drift/Memory
commit request with unrelated dirty work
ordinary Chat with no artifact/action intent
```

Any real gap gets a failing assertion before repair. Do not add untested prose.

- [x] **Step 5.4: Preserve RED and link GREEN**

Append a short GREEN closure section to the RED report without deleting or rewriting the RED output.

## Task 6: Full Validation And Final Score

**Files:**

- Read: `docs/maintenance/full-validation-method.md`
- Create: `docs/reports/agent-loop-v1.5.0-full-validation-2026-07-21.1.md`
- Modify only after a real new RED: its owning source and test

- [x] **Step 6.1: Run every Shell test**

Run:

```bash
shell_total=0
shell_pass=0
for test_file in tests/*.sh; do
  shell_total=$((shell_total + 1))
  if bash "$test_file"; then
    shell_pass=$((shell_pass + 1))
  else
    printf 'FAILED SHELL TEST: %s\n' "$test_file" >&2
    exit 1
  fi
done
printf 'shell: %s/%s PASS\n' "$shell_pass" "$shell_total"
```

Expected: every current Shell test passes; record live total.

- [x] **Step 6.2: Run every Python test**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
```

Expected: every discovered test passes; record unittest's live count.

- [x] **Step 6.3: Run YAML, JSON, Shell syntax, Markdown fence, and diff checks**

Run:

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
python3 -c 'import json; json.load(open("plugin.json", encoding="utf-8"))'
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
python3 - <<'PY'
from pathlib import Path
for path in Path('.').rglob('*.md'):
    fence = None
    length = 0
    for line in path.read_text(encoding='utf-8').splitlines():
        stripped = line.lstrip()
        if fence is None and (stripped.startswith('```') or stripped.startswith('~~~')):
            fence = stripped[0]
            length = len(stripped) - len(stripped.lstrip(fence))
        elif fence is not None and stripped.startswith(fence * length):
            fence = None
            length = 0
    if fence is not None:
        raise SystemExit(f'unclosed Markdown fence: {path}')
print('PASS: Markdown fence balance')
PY
git diff --check
```

Expected: all mechanical checks pass.

- [x] **Step 6.4: Execute the six-domain audit**

Score current working tree using:

```text
Logic Correctness / 20
Autonomy / 15
Project Entry / Evidence Graph + DDD Onboarding / 15
Development / Test Workflow / 20
Memory / 15
Recommendation / 15
```

Each domain cites current file/line evidence and separates current issues from historical RED. Acceptance: `>=99/100`, `STRONG`, Critical 0, High 0, Medium 0.

- [x] **Step 6.5: Write the suffixed full report**

Create `docs/reports/agent-loop-v1.5.0-full-validation-2026-07-21.1.md` with branch/version/HEAD/current-worktree boundary; final line/word/byte/block/revision facts; focused and mutation results; live totals; six-domain scores; current findings; RED/GREEN; pressure scenarios; rejected suggestions; Windows native-run boundary; Git/sync authorization; and Human Review recommendation.

Do not overwrite the unsuffixed report.

## Task 7: Final Diff Review And Human Handoff

**Files:** current working tree only.

- [x] **Step 7.1: Inspect final scope and authoring residue**

Run:

```bash
git status --short
git diff --stat
git diff -- templates/root-AGENTS.md references/runtime.md references/design.md \
  references/project-guidance.md references/workflow-checklists.md \
  references/validation-scenarios.md CHANGELOG.md
rg -n 'F[I]XME|T[O]DO|T[B]D' \
  templates/root-AGENTS.md references tests docs/proposal/v1.5.x/root-agents-lossless-slimming* \
  docs/reports/agent-loop-v1.5.0-*2026-07-21* || true
find . -type d -name '__pycache__' -prune -print
find . -path '*/.agent-loop/*' -print
```

Expected: intended source/test/proposal/report changes only; no target-project artifact, conflict, generated cache, or unresolved authoring marker.

- [x] **Step 7.2: Verify historical/current revision separation**

Run:

```bash
rg -n '1\.5\.0-20260721\.(1|2)' templates references tests CHANGELOG.md docs/proposal docs/reports
```

Expected: `.2` is current; `.1` is historical/baseline/stale-fixture evidence only.

- [x] **Step 7.3: Update Proposal and Plan evidence only after all checks pass**

Set Proposal status to:

```text
状态：已实施，等待 Human Review；未 commit / push / tag / release / installed-skill sync
```

Link this plan, RED report, and suffixed full report. Mark only commands actually run as complete.

- [x] **Step 7.4: Present Human Review and stop**

Report final line/word/byte count; 13/13 `.2` blocks; Gateway/reference and leaf coverage; four mutations; focused/full results; six-domain score/severity; file scope; unrelated dirty-state disposition; Windows boundary; residual risk; and explicit no Git/release/sync actions. Recommend maintainer semantic review as the single next stage.

## Rollback Contract

If equivalence, full validation, or the 99-point threshold fails:

1. Stop before Git/sync actions and preserve failing evidence.
2. Restore only Task 1–6 edits from implementation-start preimages; do not reset approved pre-existing dirty changes.
3. Restore the exact 224-line `.1` template captured in Task 0.
4. Restore live revision consumers from `.2` to `.1`; retain historical evidence.
5. Remove only newly created slimming test/report files after their evidence is copied into Human Review; retain the accepted Proposal.
6. Re-run the pre-change full mechanical baseline and report restoration status.

Use `apply_patch`; destructive whole-worktree reset is forbidden.

## Developer Agent Handoff

After implementation authorization, copy:

```markdown
请在 Agent Loop 源码仓库 `alpha/v1.5.0` 的当前工作区，严格执行 `docs/proposal/v1.5.x/root-agents-lossless-slimming-implementation-plan.md`。

从 Task 0 开始，保留当前已批准但未提交的 dirty changes，先建立全量基线和 focused RED，再修改 production template。不得 reset/revert 现有改动，不得恢复历史提交 `1980368`，不得改变 Proposal 语义。

目标是 canonical `templates/root-AGENTS.md` 不超过 190 行，保留 13 managed blocks、project-outcome ownership、两条 spine、16 个精确 Gateway、6 类 Gate、Completion/Submit/Artifact Authority，并由 `references/runtime.md` 保持完整 leaf-stage order。严格执行新增 test 中的 tuple、reference、mutation 和行数契约，不能为绿测试删减 Gate 或放宽断言。

跑完 focused GREEN、所有 Shell/Python/mechanical tests 和六域 full validation，刷新 RED/full-validation 报告，然后停在 Human Review。不升级 Skill 版本，不同步 installed Skill，不创建/切换分支或 worktree，不派生子 Agent，不 commit、push、tag、PR、merge、release 或 publish。
```

## Plan Self-Review

- Spec coverage: every accepted goal, non-goal, Gateway family, Gate class, line budget, mutation, revision, score threshold, rollback, and Human Gate has an owning task.
- Artifact ownership: root projection, runtime order, detailed algorithms, tests, reports, and historical evidence each have one owner.
- Constant consistency: `.2`, 13 section identities, 16 tuples, six Gate names, two spines, ownership sentence, and report paths remain identical throughout.
- Scope: no Product Consensus/Hub/Workbench restoration, new workflow state, version bump, installed sync, or Git mutation.
- Execution recommendation: Development Agent implements; the maintainer/designer independently reviews source semantics, pressure evidence, and score before any commit authorization.

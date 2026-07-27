# AI-Led Lightweight Feature Gates Implementation Plan

状态：Task 0–12 与后续混沌修复均已完成；稳定发布已获人类授权
目标版本：1.5.2
目标分支：`v1.5.2`
设计来源：`docs/proposal/v1.5.x/ai-led-lightweight-feature-gates.md`

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` and `test-driven-development` inline to implement this plan task-by-task. Subagent dispatch is not authorized. Steps use checkbox (`- [ ]`) syntax for tracking.

> **Later authorization record (2026-07-27):** after the original implementation, the human explicitly authorized exactly two read-only chaos-test subagents after main-agent repair/self-check. That later bounded authorization did not change implementation semantics or authorize repository writes/Git actions by subagents.

**Goal:** Keep Feature Gate 1/2 as lightweight Human authorization boundaries while moving all semantic completeness/drift judgment to the AI and reducing the canonical Checker to deterministic evidence manifests, path safety, digest equality, and minimal action pairing.

**Architecture:** Preserve the current two-Gate artifacts and digest evidence. Checker outcomes are evidence-only; `Gate Drift Assessment`, Story/Task/Plan/No-Plan, and accepted-boundary semantics are Agent-owned. Keep unsafe/incomplete manifests and invalid action pairs deterministic failures while avoiding Markdown semantic parsing.

**Iteration note:** Tasks 1–10 below preserve the actual RED/GREEN history, including outcome names and semantic Checker rules that were later disproved by chaos testing. Task 11 establishes the minimal evidence-only contract; Task 12 hardens only its deterministic evidence boundary and supersedes conflicting historical Checker details. Historical text remains evidence, not runtime authority.

**Tech Stack:** Python 3.10+ standard library, Markdown runtime/templates, Shell contract tests, Python `unittest`, Ruby/YAML and repository mechanical validation.

**Git Boundary:** Branch creation and version 1.5.2 are authorized. Commit, push, tag, PR, merge, release, publish, `main` synchronization, and installed-Skill synchronization are not authorized and do not appear as executable plan steps.

---

## Task 0 — Baseline, Dirty Work, And Authority

**Files:**

- Read: `AGENTS.md`
- Read: `SKILL.md`
- Read: `references/runtime.md`
- Read: `references/design.md`
- Read: `docs/maintenance/full-validation-method.md`
- Read: `docs/proposal/v1.5.x/ai-led-lightweight-feature-gates.md`
- Read: `scripts/check-feature-review.py`
- Read: `tests/test_feature_review.py`

- [x] Record branch `v1.5.2`, full HEAD, tags, and `git status --short --branch`.
- [x] Preserve unrelated `AGENTS.md`, `.tmp/`, `scripts/__pycache__/`, and `tests/__pycache__/` without editing, cleaning, staging, or reporting them as implementation output.
- [x] Count `tests/*.sh` and `tests/test_*.py` live.
- [x] Run the existing 45 Shell tests and record pass/fail totals before Feature Gate edits.
- [x] Run Python discovery and record the actual test count before Feature Gate edits.
- [x] Run the current focused checker suite and record its baseline.
- [x] Stop if baseline failures overlap Feature Gate/version surfaces and cannot be explained without changing approved semantics.

Commands:

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
python3 -m unittest discover -s tests -p 'test_*.py'
python3 tests/test_feature_review.py
git diff --check
```

Expected pre-change result: existing repository baseline passes; no source implementation file is changed by the commands.

## Task 1 — Focused RED Contract And Saved Evidence

**Files:**

- Modify: `tests/test_feature_review.py`
- Modify: `tests/validate-feature-construction-two-gate-review.sh`
- Create: `docs/reports/agent-loop-v1.5.2-lightweight-feature-gates-red-baseline-2026-07-27.md`

- [x] Extend the fixture with a helper that appends a `Gate Drift Assessments` row to `notes.md`:

```python
def add_assessment(
    feature: Path,
    *,
    gate: str,
    baseline: str,
    current: str,
    classification: str,
    feature_id: str | None = None,
) -> None:
    """Append exact current Gate drift evidence without changing the Gate baseline."""
```

- [x] Add a RED test proving a Gate 1 `spec.md` evidence-only metadata change should return exit `3` and `ASSESSMENT_REQUIRED`, while the current checker returns generic exit `1`.
- [x] Add a RED test proving an exact `within-approved-boundary` Gate 1 assessment should produce `GATE_VALID` without rewriting `Gate 1 Spec Digest`.
- [x] Add a RED test proving an unassessed Gate 2 stable change should return `ASSESSMENT_REQUIRED`, not generic `FAIL`.
- [x] Add a RED test proving an exact Gate 2 assessment cannot be reused for another Feature ID, baseline fingerprint, or current fingerprint.
- [x] Add a RED test that adds `T003 [US1]` mapped to the accepted Story, changes the active Plan to `T003`, records `within-approved-boundary`, and expects execution to remain authorized.
- [x] Add a RED negative control where `T003` is `Human-gated`; expect `GATE_BLOCKED` even if an assessment claims it is within boundary.
- [x] Add a RED negative control where Gate 2 is missing or `package-only` attempts execution; expect `GATE_BLOCKED`.
- [x] Add Shell contract assertions for `GATE_VALID`, `ASSESSMENT_REQUIRED`, `GATE_BLOCKED`, `within-approved-boundary`, and `新增 Task ID != 自动重新 Gate 2` across runtime/design/template/scenario surfaces.
- [x] Run only the new focused tests and confirm failure is caused by absent typed outcomes/assessment/boundary behavior.
- [x] Save exact commands, failing test names, expected/actual exits, and current generic error output in the RED report.

Expected RED examples:

```text
expected returncode 3, got 1
expected ASSESSMENT_REQUIRED, got FAIL: Gate 1 Spec Digest does not match spec.md
expected GATE_VALID for mapped T003, got accepted Agent-ready task set failure
```

## Task 2 — Typed Checker Outcomes And Exact Drift Assessment

**Files:**

- Modify: `scripts/check-feature-review.py`
- Modify: `tests/test_feature_review.py`
- Modify: `tests/test_python_checker_contract.py`

- [x] Add stable process results without adding project lifecycle values:

```python
EXIT_GATE_VALID = 0
EXIT_GATE_BLOCKED = 1
EXIT_ASSESSMENT_REQUIRED = 3

@dataclass(frozen=True)
class ValidationResult:
    blocked: tuple[str, ...]
    assessment_required: tuple[str, ...]
```

- [x] Parse only the existing `notes.md` table headed `## Gate Drift Assessments` with this contract:

```markdown
| Feature ID | Gate | Baseline Fingerprint | Current Fingerprint | Classification | Changed Areas | Reason | Assessed At |
|---|---|---|---|---|---|---|---|
| <feature-id> | 1 | sha256:... | sha256:... | within-approved-boundary | spec.md metadata | no Goal/Scope/Acceptance change | 2026-07-27T12:00:00+08:00 |
```

- [x] Reject malformed rows, unsupported classifications, missing reason/changed areas, invalid SHA-256, invalid Gate, and non-timezone-aware timestamps as `GATE_BLOCKED`.
- [x] Bind an assessment to `feature.name`, Gate number, baseline fingerprint, and current fingerprint; do not allow row reuse after any bound value changes.
- [x] Compute Gate 1 baseline/current fingerprints from recorded/current Spec SHA-256.
- [x] Compute Gate 2 baseline/current fingerprints from Package Files/Digest, Stable Files/Algorithm/Digest, and their freshly computed values using a deterministic SHA-256 aggregate.
- [x] Route digest mismatch as follows:

```python
if exact_assessment is None:
    result.assessment_required += (reason,)
elif exact_assessment.classification == "within-approved-boundary":
    pass
elif exact_assessment.classification == "feature-definition-change":
    result.blocked += ("return to Gate 1",)
elif exact_assessment.classification == "implementation-boundary-change":
    result.blocked += ("return to Gate 2",)
else:
    result.blocked += ("one blocking Human question is required",)
```

- [x] Keep unsafe paths, missing core files, unknown algorithms, malformed projections, missing Gate decisions, invalid timestamps, and decision/Auto-Loop mismatch as hard blocks.
- [x] Print only one leading result vocabulary per run:

```text
GATE_VALID: ...
ASSESSMENT_REQUIRED: ...
GATE_BLOCKED: ...
```

- [x] Keep `--mode digest` read-only and extend it to print copyable Gate baseline/current fingerprints for assessment authoring.
- [x] Run the Task 1 tests until typed outcome, exact-match, stale-row, and negative-control cases are GREEN.

## Task 3 — Accepted Execution Boundary Instead Of Immutable Task IDs

**Files:**

- Modify: `scripts/check-feature-review.py`
- Modify: `tests/test_feature_review.py`
- Modify: `templates/tasks.md`

- [x] Keep `Gate 2 Agent-ready Tasks` as the initial reviewed decomposition, not an absolute future whitelist.
- [x] In `review` mode, require every initial reviewed Task to exist and be `Agent-ready`.
- [x] In `start` / `execute`, require the current task or every story-included task to exist and remain `Agent-ready`; a `Human-gated` task is always `GATE_BLOCKED`.
- [x] When the current Agent-ready Task is new relative to the initial reviewed set, require the exact current Gate 2 assessment and a structural mapping in `tasks.md`:

```text
- [ ] T003 [US1] Split implementation step
  - Derived From: T001
  - Covers Stories: US1
  - Mode: Agent-ready
```

- [x] Treat a new Task with current `within-approved-boundary` assessment as executable when Plan scope/mapping remain valid.
- [x] Treat a new Task without assessment as `ASSESSMENT_REQUIRED`, not hard Gate failure.
- [x] Treat missing Task identity, `Human-gated` mode, invalid story mapping, or Plan scope without a real Task as `GATE_BLOCKED`.
- [x] Preserve Plan Gate, Analyze Consistency, Task Done Gate, Delivery Contract, Complex Artifact, external, Git, Submit, Close, and Release stops.
- [x] Run the mapped-new-task, new-story, Human-gated, missing-task, story-plan, no-plan, and plan-rotation focused tests to GREEN.

## Task 4 — Runtime, Design, And Artifact Authority Alignment

**Files:**

- Modify: `SKILL.md`
- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/artifact-rules.md`
- Modify: `references/project-guidance.md`
- Modify: `references/checker-recovery.md`
- Modify: `references/human-review-summary.md`
- Modify: `references/validation-scenarios.md`
- Modify: `templates/notes.md`
- Modify: `templates/tasks.md`
- Modify: `tests/validate-feature-construction-two-gate-review.sh`

- [x] State the invariant consistently:

```text
AI judges semantic completeness and boundary drift.
Checker validates Human Gate presence, Gate/action pairing, current task/Plan binding, and structural evidence.
Digest change is a change signal, not by itself Gate invalidation.
```

- [x] Reduce Gate 1 Human Review to Goal, Scope, Acceptance, and Explicit Exclusions while keeping full Spec available as authority.
- [x] Reduce Gate 2 Human Review to Execution Boundary, Verification, Risk/Rollback, and execution choice while keeping the complete package available.
- [x] Define AI outcomes `within-approved-boundary | feature-definition-change | implementation-boundary-change | unresolved` as response/diagnostic values, not lifecycle.
- [x] Define `GATE_VALID | ASSESSMENT_REQUIRED | GATE_BLOCKED` as Checker outcomes, not project states.
- [x] Route `ASSESSMENT_REQUIRED` to AI Semantic Review before Checker Recovery; only a reproducible checker contradiction enters Checker Recovery.
- [x] Replace every rule that says “new Task ID always returns Gate 2” with “new execution boundary returns Gate 2”.
- [x] Require exact Assessment reuse checks after Resume, context compaction, later package-only start, or digest change.
- [x] Add the assessment table and `Derived From` field guidance to existing templates without creating a new artifact.
- [x] Preserve all independent Human Gates and the prohibition on automatic accepted-baseline rewriting, force, or bypass.

## Task 5 — Root Guidance, Human Docs, And Changelog

**Files:**

- Modify: `templates/root-AGENTS.md`
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`
- Modify: affected root-guidance and human-help tests

- [x] Keep root guidance concise: Gate 1 confirms Goal/Scope/Acceptance/Exclusions; Gate 2 confirms Execution Boundary/Verification/Risk/Rollback/start choice.
- [x] State that AI evaluates drift and Checker guards authorization; do not copy the Assessment algorithm into root guidance.
- [x] Explain in human docs that new Task IDs inside an accepted execution boundary do not require another human Gate.
- [x] Explain that `ASSESSMENT_REQUIRED` is an AI review route, not Checker failure or automatic human interruption.
- [x] Add the 1.5.2 changelog section as development/validation-in-progress evidence; do not claim stable release or tag.
- [x] Leave installation examples on the latest existing formal tag `stable-v1.5.1` until a separate release/tag authorization exists.

## Task 6 — Version 1.5.2 And Managed Block Synchronization

**Files:**

- Modify: `SKILL.md`
- Modify: `plugin.json`
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`
- Modify: `templates/root-AGENTS.md`
- Modify: `references/project-guidance.md`
- Modify: `references/workflow-checklists.md`
- Modify: all tests whose current-version/revision expectation is authoritative

- [x] Update source version fields to `1.5.2`.
- [x] Set all 13 managed blocks to `block-version:1.5.2-20260727.2` after the coordinated Gate summary refresh.
- [x] Update root block checker/refresh tests and current-version assertions to the same revision.
- [x] Update current human-help phrases to 1.5.2 while preserving historical changelog headings and intentional sample Git context.
- [x] Search all remaining `1.5.1` occurrences and classify each as latest formal stable tag, historical version evidence, generic example requiring update, or stale current-version residue.
- [x] Confirm no `stable-v1.5.2` tag/install claim appears before release authorization.

## Task 7 — Focused GREEN And Pressure Validation

**Files:**

- Update: `docs/reports/agent-loop-v1.5.2-lightweight-feature-gates-red-baseline-2026-07-27.md` only to add a clearly separated GREEN follow-up section; preserve RED output unchanged.

- [x] Run `python3 tests/test_feature_review.py` and record exact test count.
- [x] Run `bash tests/validate-feature-construction-two-gate-review.sh`.
- [x] Run affected Feature Context, Human Gate, Task Done, Complex Artifact, root guidance, checker recovery, project guidance, version, and validation-scenario contracts.
- [x] Run positive pressure cases:
  - Gate 1 metadata/Snapshot evidence change;
  - Gate 2 task/test runtime result change;
  - accepted-boundary Task split to T003;
  - Plan rotation inside the accepted boundary;
  - exact Assessment reuse in the same Feature and current fingerprints.
- [x] Run negative controls:
  - copied Assessment from another Feature;
  - stale baseline/current fingerprints;
  - new Story/Acceptance/interface/risk/rollback boundary;
  - Human-gated new Task;
  - package-only execution;
  - malformed/unknown digest evidence;
  - Git/Contract/Subagent/Submit/Close authorization inheritance.
- [x] Confirm no test passes only because an assertion was weakened or deleted.

## Task 8 — Full Validation And Chinese Report

**Files:**

- Create: `docs/reports/agent-loop-v1.5.2-full-validation-2026-07-27.md`
- Create after chaos repair: `docs/reports/agent-loop-v1.5.2-full-validation-2026-07-27.2.md`

- [x] Recount Shell/Python tests live.
- [x] Run all `tests/*.sh` and record pass/fail totals.
- [x] Run Python discovery and record actual test count.
- [x] Run YAML, JSON, Shell syntax, Ruby syntax where applicable, Markdown fence, and `git diff --check`.
- [x] Perform the six-domain semantic audit from `docs/maintenance/full-validation-method.md`.
- [x] Verify Gate 1/2, Feature Auto-Loop, Task Auto-Run, Task Done, Feature Context, Checker Recovery, Requirement/ADR, Delivery Contract, Branch/Git, Submit, Close, and Release invariants.
- [x] Record current Critical/High/Medium findings, score, release readiness, and any Windows-test-defined limitation in Chinese.
- [x] Do not reuse the 1.5.1 report's counts or score.

## Task 9 — Proposal/Plan Status And Final Human Review

**Files:**

- Modify: `docs/proposal/v1.5.x/ai-led-lightweight-feature-gates.md`
- Modify: `docs/proposal/v1.5.x/ai-led-lightweight-feature-gates-implementation-plan.md`

- [x] Check every Proposal acceptance condition against code, references, templates, scenarios, and tests.
- [x] Update Proposal and Plan status to the actual validation state without claiming release.
- [x] Run final `git status --short`, `git diff --stat`, `git diff --check`, version search, and intended-file review.
- [x] Report modified/new files, RED/GREEN, focused/full totals, score, remaining risks, unrelated dirty work, and version/revision.
- [x] Stop at Human Review. Do not stage, commit, push, tag, PR, merge, release, publish, synchronize `main`, or update installed Skills.

## Task 10 — Post-Chaos Lightweight Trust Boundary Repair

**Decision:** Human provenance is Agent-owned from reliable conversation/preserved Human evidence. The Checker validates deterministic structure and scope only; it does not issue or prove Human authorization.

- [x] Preserve the final chaos Critical as RED evidence and confirm the architectural root cause.
- [x] Add focused RED tests for accepted execution without a local authorization digest and absence of a local authorization-issuer mode.
- [x] Confirm both new tests fail against the digest-based implementation for the expected reasons.
- [x] Remove `gate2-authorization-v1`, `authorize-review`, and `authorize-start`; retain read-only `start` preflight for later package-only execution.
- [x] Align runtime, design, stage guides, artifact rules, Human Review, checklists, templates, human docs, scenarios, and focused contracts with the lightweight trust boundary.
- [x] Confirm focused GREEN for the new tests and canonical Feature checker suite.
- [x] Run all Shell/Python tests, mechanical checks, and six-domain semantic audit.
- [x] Reuse exactly the two Human-authorized read-only chaos agents for final lifecycle and artifact retest.
- [x] Refresh reports and final status, then stop at Human Review without Git or release actions.

## Task 11 — Second-Chaos Minimal Evidence Checker Repair

**Decision:** after two additional Human-authorized read-only chaos runs, the Human confirmed that Checker responsibility should stop at digest evidence plus the file coverage needed to make that digest trustworthy. AI owns workflow semantics.

- [x] Preserve six focused RED failures for authorization-style output, semantic parsing, omitted detail coverage, parent symlink/resolved alias, and fenced-field spoofing.
- [x] Replace `GATE_VALID | ASSESSMENT_REQUIRED | GATE_BLOCKED` with evidence diagnostics `EVIDENCE_MATCH | EVIDENCE_CHANGED | EVIDENCE_INVALID`.
- [x] Remove Task/Story/Plan/No-Plan/Assessment parsing from Checker decisions while retaining those records as Agent-owned workflow evidence.
- [x] Make `digest` validate required roots, triggered detail coverage, canonical paths, duplicate paths, symlink components, resolved-target aliases, regular files, and Feature-root containment before emitting values.
- [x] Keep minimal action pairing for package-only/start/approve-and-start/execute and timezone-aware review evidence.
- [x] Default new Stable evidence to `raw-v1`; keep explicit `review-definition-v2` reader compatibility without treating projection as semantic validation.
- [x] Coordinate runtime, design, artifact rules, stage guides, checklists, Human Review, root guidance, templates, human docs, changelog, scenarios, and focused contracts.
- [x] Run focused validation, all Shell/Python tests, mechanical checks, and six-domain full validation.
- [x] Refresh RED, feature validation, full-validation, Proposal, and Plan evidence; stop at Human Review without Git or release actions.

## Task 12 — Third-Chaos Deterministic Boundary Repair

**Decision:** preserve the evidence-only Checker. Repair only deterministic manifest/path/encoding/Markdown boundaries and cross-file wording; do not restore Task/Story/Plan/Assessment parsing.

- [x] Save six focused Checker RED failures for Stable non-Plan closure, invalid UTF-8 notes, empty manifest entries, same-file aliases, malformed fence closing, and Windows drive-absolute paths.
- [x] Save coordinated documentation RED for the contradictory `raw-v1` legacy paragraph, ambiguous Pause grant persistence, and missing inline Gate Drift Assessment template.
- [x] Make Stable Files the exact non-Plan closure of explicit Package Files plus discovered required artifacts.
- [x] Return one structured `EVIDENCE_INVALID` for invalid UTF-8 notes, reject empty list entries, and preserve digest mode as read-only.
- [x] Reject same-file aliases using filesystem identity, Windows drive paths on every host, and fence lines with trailing non-whitespace as closers.
- [x] Define `raw-v1` as the current default; keep only explicit `review-definition-v2` as legacy reader compatibility.
- [x] Preserve the durable Gate 2 decision/Auto-Loop pair across Pause; clear current execution through project `Gate Mode`, and require a newly confirmed mode on Resume.
- [x] Align direct and inline notes templates, runtime, design, artifact rules, stage guides, completion, checklists, changelog, scenarios, Proposal, Plan, and focused contracts.
- [x] Run focused GREEN 51/51, evidence chaos 79/79, lifecycle executable chaos 31/31, all 45 Shell tests, all 339 Python tests, mechanical checks, and six-domain full validation.
- [x] Refresh the RED/full-validation evidence and stop at Human Review without Git or release actions.

## Task 13 — Human-Directed Single-Responsibility Digest Checker

**Decision:** after repeated chaos testing showed that every additional Gate rule inside the Checker creates another Markdown, lifecycle, or compatibility failure surface, the Human directed the Checker to own one concern only: recomputing recorded Stable evidence. The Agent owns manifest completeness, Package review meaning, Gate/action pairing, timestamps, Human provenance, Task/Story/Plan/No-Plan bindings, and all workflow routing.

- [x] Add focused RED tests proving the current Checker still rejects otherwise readable evidence because of Gate/action pairing, timestamp semantics, manifest completeness, and legacy-v2 decoding outside Task/Test projection.
- [x] Add `--mode check` as the canonical Stable-digest comparison and keep `review | start | execute` only as compatibility aliases to the identical check path.
- [x] Restrict check-mode required fields to `Gate 2 Stable Files`, `Gate 2 Stable Digest Algorithm`, and `Gate 2 Stable Digest`.
- [x] Retain only input-safety prerequisites needed to read and hash the named files: non-empty canonical Feature-relative paths, regular files, Feature-root containment, no symlink components, no duplicate/same-file aliases, supported digest algorithm, and valid digest syntax.
- [x] Remove required-root discovery, triggered-detail closure, Package-to-Stable closure, Plan exclusion, Gate decision/Auto-Loop pairing, readiness, timestamp, and Human-provenance checks from Checker decisions.
- [x] Keep `--mode digest` read-only and able to compute copyable Gate 1, Package, and Stable digests from the lists supplied by the Agent; it does not certify list completeness.
- [x] Preserve explicit `review-definition-v2` reader compatibility by projecting only Task/Test Markdown and hashing every other Stable file as raw bytes.
- [x] Update runtime/design/stage/checklist/template/human-review/scenario/docs wording so AI performs the removed checks and Checker output cannot be called Gate authorization.
- [x] Run focused GREEN, the fixed fourth-chaos matrix, affected contracts, mechanical checks, and the required full validation; stop at Human Review without Git actions.

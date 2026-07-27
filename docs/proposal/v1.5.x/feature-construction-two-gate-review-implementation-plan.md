# Feature Construction Two-Gate Review Implementation Plan

**Version:** v1.5.1  
**Status:** implementation complete; single-feature validation 100/100 STRONG; full validation pending  
**Proposal:** `docs/proposal/v1.5.x/feature-construction-two-gate-review.md`  
**Implementation authority:** human requested continuation after the Feature Context commit on 2026-07-25  
**Git authority:** none  
**Version bump:** human-approved synchronization to `1.5.1` on 2026-07-25  
**Full validation:** mandatory before final acceptance because Human Gate placement and Auto-Loop activation change; do not run until the human explicitly requests it

## Goal

Replace ordinary per-stage Feature construction interruptions with two meaningful reviews while preserving every quality stage and every independent hard gate:

```text
explicit implementation request
-> draft and check Feature definition
-> Gate 1: Feature Definition Review
-> autonomous implementation-package artifact preparation
-> Gate 2: Implementation Readiness Review
-> accepted Agent-ready execution
```

Gate 1 accepts what will be built. Gate 2 accepts how it will be built and optionally starts Feature Auto-Loop. Work Breakdown, Test Design, E2E Discovery, Technical Design, Plan Gate, Analyze Consistency, verification, review, drift, and memory remain required methods.

## Invariants

1. An explicit implementation request may authorize draft Feature workspace creation, but never accepts the Feature definition.
2. Gate 1 acceptance authorizes package preparation only; target implementation remains forbidden.
3. Package preparation creates or updates all applicable tasks, tests, E2E evidence, technical context, Plan, coverage, risk, and rollback without per-stage prompts.
4. Gate 2 rejects incomplete, placeholder, untraceable, or unverifiable packages.
5. `Approve package only` never authorizes target implementation.
6. `Approve package and start implementation` accepts the package and enables Feature Auto-Loop without a third generic prompt.
7. Product/scope/acceptance changes return to Gate 1. Material task/test/plan/risk/rollback changes return to Gate 2.
8. Delivery Contract creation/acceptance may be included only as separately named exact Gate 2 actions. Breaking changes retain a separate hard gate.
9. Subagent, branch, external mutation, production, credentials, submit, commit, push, PR, merge, tag, release, publish, pause, and close remain independently gated.
10. Strict Mode remains available only when the human explicitly requests stage-by-stage control; it is not the normal conservative fallback after Gate 1.

## Task 1 — Add RED Cross-Surface Contract

**Create:** `tests/validate-feature-construction-two-gate-review.sh`

- [x] Assert the canonical names `Feature Definition Review` and `Implementation Readiness Review`.
- [x] Assert Gate 1 authorizes package preparation but forbids target implementation.
- [x] Assert Work Breakdown, Test Design, E2E Discovery, Technical Design, Plan, and consistency review continue without separate prompts.
- [x] Assert Gate 2 has `approve package only`, `approve and start`, `revise`, and `pause`.
- [x] Assert package-only approval does not execute.
- [x] Assert approve-and-start enables Feature Auto-Loop without another generic prompt.
- [x] Assert independent Delivery Contract, subagent, Git, external, submit, close, and release gates remain.
- [x] Assert root guidance and human-facing docs use the same model.
- [x] Run the new test and record RED against current runtime wording.

## Task 2 — Update Canonical Model And Runtime

**Modify:**

- `SKILL.md`
- `references/design.md`
- `references/concepts.md`
- `references/runtime.md`

- [x] Define the two reviews and `Implementation Readiness: preparing | review-ready | accepted`.
- [x] Make the normal post-Spec path Gate 1 -> package preparation -> Gate 2.
- [x] Retain every construction stage in canonical order.
- [x] Change Feature Auto-Loop activation to Gate 2 `approve package and start implementation`.
- [x] Keep Task Auto-Run for later one-task execution after package acceptance.
- [x] Make controller-unavailable fallback Strict Mode unchanged.
- [x] Preserve all stop and hard-gate conditions.

## Task 3 — Update Stage Behavior And Review Surfaces

**Modify:**

- `references/stage-guides.md`
- `references/workflow-checklists.md`
- `references/human-review-summary.md`
- `references/implementation-planning.md`

- [x] Replace Feature Spec exit with Gate 1 choices.
- [x] Remove ordinary Work Breakdown, Test Design, and Plan per-stage acceptance exits during package preparation.
- [x] Require package completeness, trace, real code context, verification, risk, and rollback before Gate 2.
- [x] Add compact Gate 1 and Gate 2 Human Review Summary tables.
- [x] Define revision routing back to Gate 1 or Gate 2.
- [x] Preserve separately named conditional decisions and Human-gated tasks.

## Task 4 — Update Artifacts, Templates, And Root Projection

**Modify:**

- `references/artifact-rules.md`
- `references/document-templates.md`
- `references/project-guidance.md`
- `templates/root-AGENTS.md`
- `templates/notes.md`

- [x] Add the compact readiness field to Feature notes/current summary.
- [x] Keep existing artifact ownership; create no new hierarchy or stage artifact.
- [x] Project the two-gate model into the root Gate Modes block.
- [x] Refresh all 13 managed root blocks to `block-version:1.5.1-20260725.1`.
- [x] Align current root block tests and examples with the new revision.

## Task 5 — Add Pressure Scenarios And Human Guidance

**Modify:**

- `references/validation-scenarios.md`
- `README.md`
- `Usage.md`
- `CHANGELOG.md`

- [x] Add positive scenarios for Gate 1 package preparation and Gate 2 execution start.
- [x] Add negative scenarios for package-only execution, incomplete package, scope drift, implicit contract action, and lost hard gates.
- [x] Explain the two human decisions in concise human language.
- [x] Record the behavior under the human-approved Skill version `1.5.1`.

## Task 6 — Focused Verification

- [x] Run `bash tests/validate-feature-construction-two-gate-review.sh`.
- [x] Run root managed-block refresh/checker/unit contracts.
- [x] Run Feature Context, Delivery Contract, Feature completion, helper-routing, Bug, Requirement, ADR, archive, and lightweight focused contracts affected by the gate change.
- [x] Run `ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'`.
- [x] Check Markdown fence balance.
- [x] Run `git diff --check`.
- [x] Do not run full validation without the human's explicit instruction.
- [x] Do not commit, push, tag, release, or publish.

## Task 7 — Close Durable Resume And Multi-Task Execution Gaps

- [x] Reproduce a RED baseline showing the previous runtime lacked the two-gate contract.
- [x] Run a proposal-blind audit against published runtime behavior.
- [x] Persist Gate decisions, package/stable digests, accepted task IDs, active Plan scope, and Auto-Loop state in existing Feature notes.
- [x] Add a read-only Python standard-library checker for review, package-only later start, and active execution.
- [x] Allow Plan rotation only inside the Gate 2-accepted task set while stable evidence remains unchanged.
- [x] Add executable negative tests for missing evidence, package drift, stable drift, invalid start state, and out-of-scope Plan rotation.
- [x] Rerun the complete single-feature regression boundary and publish the 100-point report.
- [x] Ask the proposal-blind auditor to verify the original High/Medium findings are closed.

## Completion Boundary

Implementation is locally ready only when the new RED contract is GREEN and all affected focused contracts pass. Formal acceptance still requires the repository's full validation method because this is a coordinated Human Gate and runtime change.

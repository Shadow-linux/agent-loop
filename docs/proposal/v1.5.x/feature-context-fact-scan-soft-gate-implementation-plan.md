# Feature Context Fact Scan Soft Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use `executing-plans` to implement this plan task-by-task. Do not dispatch subagents without a separate Human authorization.

**Goal:** Keep Feature Context freshness protection while changing its checker from a workflow judge into a factual scanner whose non-physical changes are assessed by the Agent.

**Architecture:** Preserve `spec.md` bootstrap and upstream authority resolution. Refactor the checker into three results—`CURRENT`, advisory `CHANGED`, and physical `BLOCKED`—then coordinate runtime/design and all derived surfaces so exit `0` is never mistaken for execution permission.

**Tech Stack:** Python 3.10+ standard library, Shell contract tests, Markdown runtime/reference/templates.

**Status:** implemented; final Human Review

---

### Task 0: Freeze Scope And Establish Baseline

**Files:**
- Inspect: repository status, current Feature Context surfaces, existing tests
- Record later: `docs/reports/agent-loop-v1.5.3-feature-context-soft-gate-red-2026-07-28.md`

- [x] Confirm branch `v1.5.3`, full HEAD, and dirty-work ownership.
- [x] Preserve the existing Feature Archive soft-gate changes and untracked reports/proposals.
- [x] Run all existing `tests/*.sh`; expected baseline: all pass.
- [x] Run all existing `test_*.py`; expected baseline: all pass.
- [x] Record the actual baseline counts in the RED report after the focused RED is captured.

Stop when unrelated dirty work conflicts with the same Feature Context lines in a way that cannot be merged without changing its intent.

### Task 1: Add Focused RED Contract

**Files:**
- Modify: `tests/test_feature_context.py`
- Modify: `tests/validate-feature-context-load-contract.sh`
- Create: `docs/reports/agent-loop-v1.5.3-feature-context-soft-gate-red-2026-07-28.md`

- [x] Change expected outcomes for editorial digest drift, incomplete cached fields, invalid cached timestamp, unknown Product Slice references, pending Product Review/lifecycle, ADR review state, and cached-pointer disagreements to `CHANGED / 0`.
- [x] Add retained negative controls for missing/ambiguous/escaping Requirement/Product authority and missing/escaping ADR paths as `BLOCKED / 1`.
- [x] Add a contract assertion for `CURRENT | CHANGED | BLOCKED` and forbid active runtime reliance on `REFRESH_REQUIRED`.
- [x] Run only focused Feature Context tests and confirm RED because the current checker returns exit `3` or `1` for advisory facts and does not emit `CHANGED`.
- [x] Save exact RED commands and failure evidence in the report.

### Task 2: Implement Minimal Checker GREEN

**Files:**
- Modify: `scripts/check-feature-context.py`

- [x] Replace `refresh-required` with `changed` and make `changed` exit `0`.
- [x] Separate physical authority-resolution failures from changed metadata/semantic-review facts.
- [x] Resolve and read the authoritative Product file physically even when strict Product Definition validation reports review/structure drift; surface that strict result as `CHANGED`.
- [x] Keep project/memory/Requirement/Product/ADR containment and existence failures as `BLOCKED`.
- [x] Convert cached pointer/profile/review/digest/reference/ADR-state disagreement to deterministic changed reasons.
- [x] Preserve read-only behavior, canonical newline digest compatibility, deterministic sorted reasons, and Python 3.10+ standard-library support.
- [x] Run focused Python tests until GREEN.

### Task 3: Coordinate Runtime And Design Authority

**Files:**
- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Modify: `SKILL.md`

- [x] Define `CURRENT / CHANGED / BLOCKED` consistently.
- [x] Require the Agent to read the prefix, assess changed facts, and rerun after any derived-context repair.
- [x] State that `CHANGED / 0` is not execution permission and may still route to an existing Gate.
- [x] Limit checker hard failure to physical/authority contradictions.
- [x] Keep Feature Context mandatory and preserve all Product/ADR/Human Gate ownership.

### Task 4: Align Stage And Artifact Surfaces

**Files:**
- Modify: `references/product-definition.md`
- Modify: `references/stage-guides.md`
- Modify: `references/implementation-planning.md`
- Modify: `references/artifact-rules.md`
- Modify: `references/project-guidance.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/document-templates.md`
- Modify: `templates/spec.md`
- Modify: `templates/feature-context.md`
- Modify: `templates/root-AGENTS.md`

- [x] Replace hard `require CURRENT` wording with: run scanner, assess `CHANGED`, require current evidence before downstream reliance.
- [x] Keep `BLOCKED` for physical resolution failures.
- [x] Change Snapshot Freshness vocabulary to `current | changed | blocked` while documenting reader compatibility for legacy `refresh-required`.
- [x] Ensure Work Breakdown, Test Design, Plan, Execute, Verify, Review, Drift, Resume, and Close follow the same assessment contract.
- [x] Do not add a new Human Gate or canonical stage.

### Task 5: Align Human Guidance And Scenarios

**Files:**
- Modify: `references/validation-scenarios.md`
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`

- [x] Add factual-scan and Agent-assessment scenarios with retained physical negative controls.
- [x] Explain that humans do not need to approve formatting/digest refreshes.
- [x] Explain that changed product/ADR meaning still returns to its existing Gate.
- [x] Record the behavior under current `1.5.3` development section without a version bump.

### Task 6: Focused GREEN And Mutation Validation

**Files:**
- Test: `tests/test_feature_context.py`
- Test: `tests/validate-feature-context-load-contract.sh`
- Test: affected Requirement, ADR, Feature Gate, planning, root-guidance, and checker-recovery contracts

- [x] Run focused Feature Context Python and Shell tests.
- [x] Mutate physical authority paths and prove `BLOCKED / 1` remains.
- [x] Mutate only cached evidence, lifecycle/review metadata, Product Slice references, and ADR state and prove `CHANGED / 0`.
- [x] Prove checker does not mutate fixtures.
- [x] Run affected cross-surface contracts.

### Task 7: Full Validation

**Files:**
- Create: `docs/reports/agent-loop-v1.5.3-full-validation-2026-07-28.1.md`

- [x] Recount and run every `tests/*.sh`.
- [x] Run every `test_*.py`.
- [x] Run YAML, JSON, Shell syntax, Markdown-fence, and `git diff --check` checks.
- [x] Perform the six-domain semantic audit from `docs/maintenance/full-validation-method.md`.
- [x] Confirm no regression to Product Human Review, ADR acceptance, Gate 1/2, Delivery Contract, TDD, Task Done, Submit, or Close.
- [x] Record actual commands, counts, results, score, current findings, and dirty-work boundary in Chinese.

### Task 8: Final Human Review

**Files:**
- Refresh: this plan status
- Refresh: `feature-context-fact-scan-soft-gate.md` status

- [x] Review final diff without staging.
- [x] List all files changed by this feature separately from pre-existing Feature Archive work.
- [x] Report RED/GREEN, focused/full validation, remaining risk, version, and worktree state.
- [x] Stop without commit, push, tag, PR, merge, release, publish, installed-Skill sync, branch creation, or worktree creation.

## Rollback

- Revert only files and hunks introduced by this plan; preserve pre-existing dirty work.
- Restore checker behavior and focused tests together if the three-result contract cannot remain cross-surface consistent.
- Do not restore or modify historical reports/proposals unrelated to this change.

## Stop Conditions

- the accepted boundary would need to remove Feature Context entirely;
- physical path confinement or unique Requirement/Product authority would need to be softened;
- an existing Product, ADR, Feature, Delivery Contract, Git, Submit, or Close Human Gate would need to be removed;
- another dirty change overlaps the same semantics incompatibly;
- focused RED does not prove the current defect;
- full validation exposes an unresolved Critical/High conflict;
- implementation would require a version bump, dependency, executable schema, branch/worktree, installed-Skill sync, or Git/publish mutation.

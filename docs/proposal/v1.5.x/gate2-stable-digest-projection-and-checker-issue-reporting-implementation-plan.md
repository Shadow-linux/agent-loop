# Gate 2 Stable Digest Projection And Checker Issue Reporting Implementation Plan

Status: Tasks 0-7 complete; Task 8 release in progress
Version line: 1.5.1

> **For agentic workers:** Execute inline with test-driven-development. Subagent dispatch is not authorized.

**Goal:** Eliminate Gate 2 false drift after legal task/test runtime updates and add a Human-gated, sanitized upstream checker Issue reporting path.

**Architecture:** Keep raw Package Digest semantics, introduce a versioned Stable Digest projection in one shared checker implementation, and preserve fail-closed migration. Extend the existing Checker Recovery reference rather than creating a new stage or artifact family.

**Tech Stack:** Python 3.10+ standard library, Markdown contracts/templates, Shell/Python regression tests.

---

## Task 0 — Baseline And Boundaries

- [x] Confirm branch, HEAD, remotes, tags, source/installed checker digests, and dirty work.
- [x] Reproduce the real target failure twice without mutation.
- [x] Reconstruct the Gate 2 raw baseline from the four runtime-only T001 changes.
- [x] Run the pre-change focused checker tests.
- [x] Run the pre-change full Shell/Python baseline and preserve unrelated failures.
- [x] Confirm version remains 1.5.1 and no stable tag currently exists.

## Task 1 — RED Stable Digest Contract

**Files:**

- Modify: `tests/test_feature_review.py`
- Create: `docs/reports/agent-loop-v1.5.1-gate2-stable-digest-red-baseline-2026-07-27.md`

- [x] Add a fixture field for `Gate 2 Stable Digest Algorithm` and canonical digest computation.
- [x] Add positive runtime-mutation cases for root task ledger, task detail, root test ledger, and test detail.
- [x] Add negative definition-drift cases for task/test identity, order, mapping, mode, dependencies, gates, acceptance, verification, commands, and assertions.
- [x] Add missing/unknown/legacy algorithm cases and read-only digest computation cases.
- [x] Run the focused tests and record the expected RED caused by absent projection/version behavior.

## Task 2 — GREEN Canonical Projection

**Files:**

- Modify: `scripts/check-feature-review.py`
- Modify: `tests/test_python_checker_contract.py`

- [x] Add explicit `raw-v1` and `review-definition-v2` constants.
- [x] Implement strict task/test projection helpers with precise section/field handling.
- [x] Use the selected algorithm for Stable Digest while Package Digest remains raw.
- [x] Add a read-only `digest` mode that prints canonical evidence and never writes.
- [x] Fail closed on missing/unknown algorithms and malformed projected content.
- [x] Run focused GREEN and negative controls.

## Task 3 — Runtime And Artifact Alignment

**Files:**

- Modify: `SKILL.md`
- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Modify: `references/artifact-rules.md`
- Modify: `references/implementation-planning.md`
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/human-review-summary.md`
- Modify: `references/validation-scenarios.md`
- Modify: `references/document-templates.md`
- Modify: `templates/notes.md`
- Modify: `templates/tasks.md`
- Modify: `templates/task-detail.md`
- Modify: `templates/tests.md`
- Modify: `templates/test-case.md`
- Modify: `tests/validate-feature-construction-two-gate-review.sh`

- [x] Define raw Package Digest versus versioned Stable Definition Digest consistently.
- [x] Define allowed runtime fields and protected definition fields.
- [x] Add algorithm/migration evidence to Gate 2 Human Review and notes template.
- [x] Keep runtime results in existing ledgers/notes without creating a new artifact.
- [x] Add pressure scenarios for allowed runtime change, malicious semantic smuggling, legacy migration, and Complex Artifact Mode.

## Task 4 — Checker Repair And GitHub Issue Reporting

**Files:**

- Modify: `references/checker-recovery.md`
- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Modify: `references/stage-guides.md`
- Modify: `references/human-review-summary.md`
- Modify: `references/validation-scenarios.md`
- Modify: `templates/root-AGENTS.md`
- Modify: `tests/validate-checker-self-repair.sh`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`

- [x] Add exact downstream repair boundary for isolated and separately authorized installed-path repair.
- [x] Add sanitized Issue Draft and independent Issue Reporting Human Gate.
- [x] Add no-auth fail-closed behavior and Issue URL evidence.
- [x] Add pressure tests proving repair, substitute validation, issue submission, Git actions, installation, and release remain independent.
- [x] Create the current public GitHub Issue using the approved sanitized content and record its URL: `https://github.com/Shadow-linux/agent-loop/issues/9`.

## Task 5 — Existing Baseline Contract Repair

**Files:**

- Modify: `tests/validate-complex-artifact-thresholds.sh`

- [x] Remove only the obsolete exact wording assertion superseded by the current equivalent runtime stop rule.
- [x] Preserve the stronger exact assertion for `tasks/`, `tests/`, and `plans/` creation/switching.
- [x] Run the focused contract and confirm no runtime rule was weakened.

## Task 6 — Focused Validation

- [x] Run `python3 tests/test_feature_review.py`.
- [x] Run `bash tests/validate-feature-construction-two-gate-review.sh`.
- [x] Run `bash tests/validate-checker-self-repair.sh`.
- [x] Run Complex Artifact, root guidance, Feature Context, Task Done, Human Gate, and validation-scenario affected contracts.
- [x] Reproduce T001 completion and T002 rotation against a temporary fixture with the canonical checker.
- [x] Verify actual target artifacts remain untouched.

## Task 7 — Full Validation

**Files:**

- Create: `docs/reports/agent-loop-v1.5.1-full-validation-2026-07-27.md`

- [x] Run all `tests/*.sh` and count them live.
- [x] Run all `tests/test_*.py` and count actual tests.
- [x] Run YAML, JSON, Shell syntax, Markdown fence, and `git diff --check` checks.
- [x] Perform the six-domain semantic audit and pressure scenarios.
- [x] Record RED/GREEN, current issues, scores, risks, release authorization, and dirty-work boundary in Chinese.

## Task 8 — Release, Push, Tag, And Global Codex Sync

- [x] Confirm all version-bearing files remain consistently 1.5.1.
- [x] Diff-review only intended files; preserve pre-existing caches and unrelated work.
- [ ] Commit with the repository's multi-line `fix(v1.5.1)` format.
- [ ] Push branch `v1.5.1` to `origin`.
- [ ] Create annotated tag `stable-v1.5.1` at the verified commit and push it to `origin`.
- [ ] Do not merge/synchronize `main` because that action was not authorized.
- [ ] Synchronize the verified distributed Skill files to the active global Codex path.
- [ ] Verify source/global manifests and run the installed canonical checker against a migrated temporary fixture.
- [ ] Report other configured remotes as untouched unless separately authorized.

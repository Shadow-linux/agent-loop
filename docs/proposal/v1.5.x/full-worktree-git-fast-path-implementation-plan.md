# Full-Worktree Git Fast Path Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Subagent dispatch is not authorized by this plan.

**Status:** Tasks 0–8 complete; focused/full validation passed; awaiting final Human Review

**Goal:** Add a one-lightweight-confirmation, entire-worktree commit/push fast path that shows the Agent-proposed commit message, does not run tests or code-quality Review merely for Git, and preserves truthful completion claims and all unrelated Git/external gates.

**Architecture:** Keep `Submit / Integrate` as the canonical owner and add Git Fast Path as an internal method. `references/runtime.md` and `references/design.md` own routing/invariants; `references/submit-and-integrate.md` owns the executable review/apply contract; root guidance and human-facing docs carry only concise projections. A focused mutation-resistant contract proves the old two-stage/test-required/file-exclusion assumptions are gone only for this path.

**Tech Stack:** Markdown contracts and templates; Bash/Ruby focused tests; existing Python 3.10+ test suite; repository YAML/JSON/Shell/Python/Markdown mechanical validation.

**Design authority:** `docs/proposal/v1.5.x/full-worktree-git-fast-path.md`

**Evidence:** `docs/reports/agent-loop-v1.5.6-full-worktree-git-fast-path-red-baseline-2026-08-15.md`; `docs/reports/agent-loop-v1.5.6-full-worktree-git-fast-path-validation-2026-08-15.md`. Execution stopped without stage, commit, push, tag, PR, merge, release, publish, or installed-Skill synchronization.

---

## Task 0: Freeze Baseline And Read Owners

**Files:** Read `AGENTS.md`, Proposal, this Plan, `SKILL.md`, `references/runtime.md`, `references/design.md`, `references/submit-and-integrate.md`, `references/stage-guides.md`, `references/workflow-checklists.md`, `references/human-review-summary.md`, `references/validation-scenarios.md`, `templates/root-AGENTS.md`, `templates/notes.md`, `README.md`, `Usage.md`, `CHANGELOG.md`, and `docs/maintenance/full-validation-method.md`.

- [x] Record branch, HEAD, status, index, tags, test counts, root line count and managed-block revision.
- [x] Stop if tracked/cached dirty work overlaps the file map or a new version is required.
- [x] Preserve `.tmp/` and existing `__pycache__/`; do not clean, stage or use them as evidence.

## Task 1: Create Focused RED Contract

**Files:** Create `tests/validate-full-worktree-git-fast-path.sh`; create `docs/reports/agent-loop-v1.5.6-full-worktree-git-fast-path-red-baseline-2026-08-15.md`.

- [x] Assert owning surfaces define `Git Fast Path`, one confirmation, `git add -A`, entire-worktree scope, no automatic tests and truthful unverified status.
- [x] Assert commit/push stay separate rows and post-confirmation drift stops execution.
- [x] Add mutations that reintroduce mandatory pre-commit verification, automatic unrelated-file exclusion, or a second Git confirmation and prove each mutation fails.
- [x] Run `bash tests/validate-full-worktree-git-fast-path.sh`; preserve the genuine missing-contract failure before production edits.

## Task 2: Publish Runtime And Design Invariants

**Files:** Modify `references/runtime.md`, `references/design.md`.

- [x] Add the internal route without a stage/intent/status.
- [x] Separate Git packaging truth from completion/readiness truth.
- [x] Define exact hard stops and independent Commit/Push authorization.
- [x] Run the focused contract and confirm failure advances to the next owning surface.

## Task 3: Implement Submit And Review Contract

**Files:** Modify `references/submit-and-integrate.md`, `references/stage-guides.md`, `references/workflow-checklists.md`, `references/human-review-summary.md`.

- [x] Add one lightweight Commit Confirmation with full worktree summary, warnings, verification truth, Agent-proposed message, requested remote/ref and not-authorized actions; explicitly exclude code/quality/Feature/verification/Drift/Completion Review.
- [x] Replace path-selective commit behavior with `git add -A` only for the accepted fast path.
- [x] Keep prepare/PR/merge/tag/release/publish/seal and completion claims on their existing paths.
- [x] Add pre-action fact-drift/failure preservation rules without introducing a formal fingerprint algorithm or second confirmation.

## Task 4: Update Durable Evidence And Root Projection

**Files:** Modify `templates/notes.md`, `templates/root-AGENTS.md`, `references/project-guidance.md`, root-revision tests.

- [x] Add compact fields for Git Path, Worktree Scope, Verification Truth, Commit Decision and Push Decision.
- [x] Keep root guidance concise and at or below 190 lines.
- [x] Update all 13 managed blocks to `1.5.6-20260815.1` and update every current revision assertion.

## Task 5: Add Scenarios And Human Docs

**Files:** Modify `references/validation-scenarios.md`, `README.md`, `Usage.md`, `CHANGELOG.md`.

- [x] Add clean/dirty/untracked/deleted/suspicious/scope-drift/conflict/commit-only/commit-and-push/no-tests/human-test-condition scenarios.
- [x] Document that full-worktree is the default only after the human accepts the lightweight summary and proposed commit message.
- [x] Record the Human-approved v1.5.6 release metadata and stable tag without changing the accepted behavior.

## Task 6: Focused GREEN And Mutation Validation

**Files:** Modify tests only when an assertion is stale because the approved behavior changed.

- [x] Run the new focused contract twice, including its mutations.
- [x] Run affected Submit, root guidance, Human Gate, branch/release, Completion and Repair-First tests.
- [x] Run `git diff --check` and record actual invocation/test counts.

## Task 7: Full Validation

**Files:** Create `docs/reports/agent-loop-v1.5.6-full-worktree-git-fast-path-validation-2026-08-15.md`; refresh Proposal/Plan status only from real evidence.

- [x] Run every `tests/*.sh` and live-count them.
- [x] Run `python3 -m unittest discover -s tests -p 'test_*.py' -v` and record live cases.
- [x] Run SKILL YAML, plugin JSON, Shell syntax, Python AST, Markdown fence, root 13-block/line-count, and `git diff --check` checks.
- [x] Perform the six-domain semantic audit from `docs/maintenance/full-validation-method.md` and score it honestly.
- [x] Mark Proposal/Plan implemented/validated only if all required evidence passes.

## Task 8: Human Review Stop

- [x] Report changed files, RED/GREEN, focused/full counts, root revision, score, remaining risks and Git status.
- [x] Do not stage, commit, push, tag, PR, merge, release, publish or synchronize an installed Skill without a new explicit Human authorization.

## Rollback And Stop Conditions

- Roll back only with inverse `apply_patch` edits to listed files; never reset, clean, restore, stash or overwrite unrelated work.
- Stop if the change requires a new stage/intent/status, version bump, dependency, executable schema, default artifact directory, or weakened completion truth.
- Stop if commit and push cannot remain independently visible, if full-worktree scope would silently omit content, or if Agent-controlled cleanup/exclusion is required.
- Stop on unresolved dirty-work overlap, repeated unexplained validation failure, root template over 190 lines, or any need for an unauthorized Git/release action.

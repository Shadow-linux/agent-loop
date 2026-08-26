# Direct Edit Fast Path And Human-Confirmed Full Test Runs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` only after an explicit bounded Subagent authorization, or use `executing-plans` for inline execution. Execute task-by-task, preserve the Human Review checkpoint between Phase 1 and Phase 2, and do not infer Git or release authority.

**Status:** implementation and Human-confirmed Phase 2 validation complete; final Human Review accepted for formal `1.5.8` release on 2026-08-27. Final evidence: 53/53 Shell contracts, 420/420 Python tests, mechanical checks, and 96/100 STRONG six-domain audit

**Proposal:** `docs/proposal/v1.5.x/direct-edit-fast-path.md`

**Planning Baseline:** branch `alpha/v1.5.7`; HEAD `a25fec3bdd1558398df8870393e90e8d808cfc35`; target version `1.5.8`; 2026-08-26 planning worktree contains only the Proposal and this Plan as expected documentation work. Branch renaming/switching is outside this Plan and remains a separate Git Gate.

**Goal:** Add a zero-artifact Direct Edit Fast Path for genuinely trivial deterministic edits and require one concrete Human confirmation before every newly proposed repository-wide full-test execution, while preserving minimum proof, Feature/Bug/Lightweight escalation, accepted verification obligations, and all existing Git/release gates.

**Architecture:** Add one focused runtime reference owned by the existing controller, then place Direct Edit before the persistent Lightweight Change Lane without adding a stage, status, mode, lifecycle, artifact family, parser, or scanner. Keep full-test authority response-local: runtime/design define the invariant, stage and review references present the exact run, Submit handles Commit/Push/CI consequences, and maintainer guidance applies the same rule to repository full validation. Existing Feature Verification Profiles choose evidence breadth but grant a full run only when Gate 2 visibly contains and accepts its exact command and scope.

**Tech Stack:** Markdown runtime/reference/template contracts; Bash and embedded Ruby contract tests; existing Python 3.10+ standard-library tests and root-block validators; Git read-only inspection; macOS execution with Windows behavior defined by platform-neutral rules. No new runtime dependency or executable checker is required.

---

## Execution Boundary

Human Review on 2026-08-26 authorizes Phase 1 to change only the listed source, reference, test, template, documentation, version, and report files. Phase 1 must stop before any repository-wide test command. Phase 2 starts only after the Human sees and confirms the concrete full-run command set against the then-current branch, HEAD, dirty input, target, expected cost, and supported claim.

The same Human decision authorizes coordinated version synchronization to `1.5.8`. The Plan does not authorize installed Skill synchronization, branch/worktree mutation, Subagent dispatch, Git action, release action, or production/external effect.

## Stage Helper Resolution

- Stage: Plan Gate / Plan
- Canonical candidate: `superpowers:writing-plans` — not exposed under that exact name
- Alias candidate: `writing-plans` — loaded completely
- Resolution: `loaded`
- Fallback used: no
- Path override: `docs/proposal/v1.5.x/` overrides `docs/superpowers/plans/`
- State ownership: Agent Loop remains controller; no target-project Feature or `.agent-loop/` artifact is created

## Verified RED Baseline

Only four affected focused contracts ran during planning:

```bash
for test_file in \
  tests/validate-lightweight-change-lane.sh \
  tests/validate-full-worktree-git-fast-path.sh \
  tests/validate-progressive-verification.sh \
  tests/validate-maintainer-full-validation-guidance.sh; do
  bash "$test_file"
done
```

Observed on 2026-08-26: all four PASS and their embedded 37 Python tests PASS.

The two new contracts are absent:

```bash
rg -n 'Direct Edit Fast Path' SKILL.md references templates README.md Usage.md CHANGELOG.md
rg -n 'one confirmation authorizes one execution|exact full command and scope|manual CI rerun|full-test execution' \
  SKILL.md references templates README.md Usage.md AGENTS.md docs/maintenance
```

Both commands produced `exit 1`, `0 matches`. Current contradictory rules are `SKILL.md:84` and `references/runtime.md:21`: both require every safe one-off edit to enter persistent Lightweight Change. This is the real RED; no full suite was run.

## File Responsibility Map

### Create

- `references/direct-edit-fast-path.md` — detailed eligibility, execution, final-only tuning check, zero-artifact, escalation, failure, and authorization owner.
- `tests/validate-direct-edit-fast-path.sh` — focused cross-surface and mutation-resistant contract.
- `docs/reports/agent-loop-v1.5.8-direct-edit-fast-path-red-baseline-2026-08-26.md` — preserved RED evidence.
- `docs/reports/agent-loop-1.5.8-full-validation-2026-08-26.md` — created only in Human-confirmed Phase 2.

### Modify: published and detailed runtime

- `SKILL.md`, `references/runtime.md`, `references/design.md`, `references/concepts.md` — controller, canonical route, invariants, and definitions.
- `references/lightweight-change-lane.md`, `references/stage-guides.md`, `references/workflow-checklists.md` — assessment precedence, execution, tuning, verification, and gates.
- `references/skill-routing.md`, `references/external-skill-adapters.md`, `references/implementation-planning.md` — no Plan/TDD helper ceremony for Direct Edit.
- `references/feature-follow-up.md`, `references/bug-management.md`, `references/artifact-rules.md`, `references/project-memory-mode.md` — Bug/Feature precedence and deliberate zero-artifact/memory behavior.
- `references/project-guidance.md`, `references/human-review-summary.md`, `references/submit-and-integrate.md`, `references/checker-recovery.md` — root projection, exact full-run review, Commit/Push/CI/Release, and formal Checker-fix claims.
- `references/validation-scenarios.md` — all positive, negative, expiry, CI, release, and compatibility scenarios.

### Modify: maintainer, template, and human docs

- `AGENTS.md`, `docs/maintenance/full-validation-method.md` — full validation stays required for qualifying claims, while execution waits for the exact Human confirmation.
- `templates/root-AGENTS.md` — concise Direct Edit/full-run projections; all 13 blocks become `1.5.8-20260826.1`.
- `SKILL.md`, `plugin.json`, `README.md`, `Usage.md`, `CHANGELOG.md` — synchronized `1.5.8` version surfaces, capability, usage, and development change record.

### Modify: focused contracts and root revision pins

- `tests/validate-lightweight-change-lane.sh`
- `tests/validate-full-worktree-git-fast-path.sh`
- `tests/validate-progressive-verification.sh`
- `tests/validate-maintainer-full-validation-guidance.sh`
- `tests/validate-mandatory-helper-routing.sh`
- `tests/validate-root-agents-block-refresh.sh`
- `tests/validate-root-agents-block-checker.sh`
- `tests/validate-project-skill-discovery-guard.sh`
- `tests/validate-project-local-skills.sh`
- `tests/validate-repair-first-verification.sh`
- `tests/validate-v1.2.4-root-stage-coverage.sh`
- `tests/validate-branch-management-strategy.sh`
- `tests/validate-bug-management.sh`
- `tests/validate-requirement-lifecycle-backlog.sh`
- `tests/validate-human-help-version-docs.sh`
- `tests/test_root_agents_blocks.py`
- `tests/test_root_agents_lossless_slimming.py`

Revision-pin files change mechanically only. They must not gain semantic assertions outside their existing ownership.

### Explicitly unchanged behavior and schema

- Lightweight card template, parser, scanner, and Python scan tests keep their schema/behavior.
- No Direct Edit template, parser, scanner, directory, index, counter, archive, lifecycle, or authorization cache.
- No generic `--skip-tests`, `--no-verify`, or `--force` parameter.

### Coordinated `1.5.8` version synchronization

- `SKILL.md`: `Version: 1.5.8`.
- `plugin.json`: `"version": "1.5.8"`.
- `README.md` and `Usage.md`: current in-development version `1.5.8`; stable release remains unchanged.
- `CHANGELOG.md`: add `## 1.5.8 — 2026-08-26` with truthful focused/full-validation state.
- `templates/root-AGENTS.md`: every one of the 13 managed blocks uses `1.5.8-20260826.1`.
- Every live version/root-revision assertion is updated in the same Phase 1 diff; historical evidence is not rewritten.

## Non-Negotiable Invariants

1. Direct Edit is an internal method, not a stage, intent, status, lifecycle, Mode, Feature Type, Bug path, or artifact family.
2. Explicit Bug wins; active Feature ownership stays inside the Feature.
3. Eligibility is all-of and one hard trigger exits the path.
4. Direct Edit creates no Feature/card/Plan/No-Plan/test/notes/memory/scanner/advisory artifact.
5. Final diff plus one cheapest artifact-matched proof remains mandatory.
6. Same-scope tuning checks once after the Human chooses the final value, not after every intermediate value.
7. Display-only multiplier may qualify; business/runtime multipliers do not qualify merely because they are numeric.
8. Required Verification and Existing Test Obligations remain due at their owners.
9. Targeted/affected evidence is default; each new full run requires exact Human confirmation unless already visibly accepted unchanged.
10. One confirmation covers one command/target/branch/HEAD/input/environment execution; relevant change or manual rerun expires it.
11. Verification Profile is strategy metadata, not execution permission.
12. Commit does not imply tests; optional decline limits claims, not separately authorized Commit.
13. Push approval covers disclosed automatic CI, not duplicate local runs or a later manual rerun.
14. Declining Release-required full validation blocks Release/readiness.
15. Existing gates and all safety/path/hash/journal/post-check/restore/rollback boundaries remain unchanged.

## Phase 1 — Implement And Reach Focused GREEN

### Task 0: Re-establish Baseline And Protect Scope

**Files:** Read every owner before its first edit; create the RED report only after checks.

- [x] Run `git status --short --branch`, `git rev-parse HEAD`, `git diff --stat`, and `git ls-files --others --exclude-standard`.
- [x] Expect branch `alpha/v1.5.7`, HEAD `a25fec3bdd1558398df8870393e90e8d808cfc35`, target version `1.5.8`, and only accepted Proposal/Plan documentation additions. Record the branch/version mismatch without creating or switching a branch. Stop on any unclear overlapping path without restore/clean/stash/stage.
- [x] Rerun the four focused baseline contracts shown above; all must PASS. Do not run `tests/*.sh` or Python discovery.
- [x] Reproduce both `rg` RED commands and record commands, exits, zero matches, old contradictory rules, branch/HEAD/worktree, and `Production files modified before RED: none` in the RED report.

### Task 1: Add The Focused RED Contract

**Files:** Create `tests/validate-direct-edit-fast-path.sh`.

- [x] Create the test with this executable skeleton and exact first-failure owner:

```bash
#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }
assert_file() { [ -f "$root/$1" ] || fail "missing required file: $1"; }
assert_contains() { local file=$1 text=$2; grep -Fq -- "$text" "$root/$file" || fail "$file missing Direct Edit/full-test contract: $text"; }
assert_not_contains() { local file=$1 text=$2; if grep -Fq -- "$text" "$root/$file"; then fail "$file contains forbidden Direct Edit/full-test behavior: $text"; fi; }

assert_file references/direct-edit-fast-path.md
assert_contains references/runtime.md 'Direct Edit Fast Path'
assert_contains references/direct-edit-fast-path.md 'one final diff inspection plus the minimum matched check'
assert_contains references/direct-edit-fast-path.md 'creates no persistent Agent Loop artifact'
assert_contains references/direct-edit-fast-path.md 'business/runtime multiplier'
assert_contains references/runtime.md 'One confirmation authorizes one execution of that concrete full run.'
assert_contains references/runtime.md 'Commit never triggers tests merely because the files will be packaged in Git.'
assert_contains references/runtime.md 'A Verification Profile label or broad phrase is not by itself execution permission.'
assert_contains references/submit-and-integrate.md 'manual CI rerun'
assert_contains docs/maintenance/full-validation-method.md '具体全量执行确认'
printf 'PASS: Direct Edit and Human-confirmed full-test contracts are complete\n'
```

- [x] Add embedded Ruby section extraction and mutation cases that must fail when: persistent card is restored for every one-off edit; per-iteration checks return; all multipliers become cosmetic; a Profile label becomes reusable permission; Commit auto-runs full tests; confirmation survives HEAD/input change; Push duplicates automatic CI locally; or Release proceeds after required validation was declined.
- [x] Run `bash tests/validate-direct-edit-fast-path.sh` before production edits. Expected RED: `FAIL: missing required file: references/direct-edit-fast-path.md`, exit 1. If it passes, strengthen the test before continuing.

### Task 2: Create The Detailed Direct Edit Owner

**Files:** Create `references/direct-edit-fast-path.md`; modify `references/lightweight-change-lane.md`, `references/artifact-rules.md`, and `references/project-memory-mode.md`.

- [x] Use these exact sections:

```text
Purpose And Position
Precedence And Route
Eligibility
Hard Escalation Triggers
Minimum Read-Only Scope Check
Execution Contract
Minimum Post-Edit Check
Same-Scope Iterative Tuning
Feature-Local Use
Zero-Artifact And Memory Boundary
Interruption And Failure
Human Gates And Forbidden Behavior
```

- [x] Publish this route:

```text
explicit Bug -> Bug Management
active Feature -> eligible Direct Edit inside Feature | owning Feature route
ordinary non-Bug -> Direct Edit Assessment
  -> eligible -> Direct Edit
  -> persistence/control -> Lightweight Change
  -> hard trigger -> Feature
  -> uncertain -> Human Choice
```

- [x] Publish this execution sequence: minimum read-only scope check -> concise disclosure of target/correction/check/rollback -> bounded write -> final exact diff -> one artifact-matched check -> truthful response-local result.
- [x] Carry the Proposal minimum-check matrix and same-scope tuning loop without semantic changes. No new test, RED manufacture, suite, regression advisory, Plan, notes row, Change card, scanner entry, or memory write exists solely for Direct Edit.
- [x] Preserve every existing Lightweight card schema, scanner, recovery, completion, rollback, and consolidation rule for work that needs persistence/control.

### Task 3: Publish Controller, Design, Stage, And Helper Routing

**Files:** Modify `SKILL.md`, runtime/design/concepts, stage/checklist, skill adapters, implementation planning, and feature follow-up owners.

- [x] Remove the two baseline contradictions that force all safe one-off work through a card; add the new reference to the SKILL map and synchronize `Version: 1.5.8`.
- [x] Put the Task 2 route into both runtime and design without adding a canonical Message Intent or Stage Order value; the Stage Order may show the method only as an explicitly `[internal]` ordering annotation before the existing Lightweight assessment.
- [x] Encode: intermediate tuning has no formal check; final Human-accepted value gets diff + minimum check; owning Feature verification remains due; Direct Edit alone never satisfies Done/Close/Release.
- [x] State that Direct Edit enters neither mandatory Plan/TDD helpers nor No-Plan Decision. Feature/Bug promotion restores the existing helper protocol.

### Task 4: Implement Human-Confirmed Full-Test Execution

**Files:** Modify `SKILL.md`, runtime/design, stage/checklist, human review, Submit, Checker recovery, `AGENTS.md`, and the maintainer full-validation method.

- [x] Define one response-local full-run signature containing:

```text
reason and recommendation
exact command or bounded command set
repository and target
branch and current full HEAD
relevant input/environment scope
expected duration/resource/external effects
supported Gate or claim
expiry on Gate end or relevant command/target/HEAD/input/environment change
```

- [x] State that one confirmation authorizes one execution. A retry policy is reusable only when the Human explicitly bounded its retry count/condition in the same decision. Add no persistent authorization artifact/status/cache.
- [x] Make Gate 2 show exact commands and scope. A Profile label alone is not permission; a Human-accepted Gate 2 row with exact unchanged full commands is permission and must not be prompted twice.
- [x] Keep Commit test-free for Git itself. Optional full-run decline may still allow separately authorized Commit but cannot support full verification, completion, or release-readiness claims.
- [x] Require Push review to disclose predictable full CI. Exact Push approval covers that automatic CI; no duplicate local full run. Manual CI rerun is a new execution.
- [x] Preserve required Release and formal Checker-fix validation. Decline blocks the claim/action; it never waives the evidence.
- [x] Coordinate maintainer flow exactly:

```text
full validation required for claim
-> focused RED/GREEN first
-> present exact full commands/cost/current inputs
-> Human confirms
-> execute once
-> relevant repair/input change requires a new confirmed full rerun
```

### Task 5: Root Projection, Human Docs, Scenarios, And Revision Pins

**Files:** Modify `references/project-guidance.md`, `templates/root-AGENTS.md`, validation scenarios, README, Usage, CHANGELOG, and every listed revision pin.

- [x] Keep root guidance concise: Direct Edit before persistent Lightweight; final diff + minimum proof; no record/test; exact full-run confirmation; Commit no tests; Push CI disclosure; required Release validation cannot be waived.
- [x] Refresh all 13 root managed blocks to `1.5.8-20260826.1` and mechanically update every current pin found by:

```bash
rg -n '1\.5\.7-20260815\.1' templates tests references README.md Usage.md CHANGELOG.md
```

After replacement, current contract surfaces return zero matches. Historical Proposal/report evidence is not rewritten.

- [x] Add these exact scenario headings:

```text
Trivial Documentation Correction Uses Direct Edit
Confirmed Internal Domain Replacement Uses Direct Edit
Feature-Local Label Tuning Uses Existing Grant
Structured Metadata Direct Edit Uses Parser Check
One-Line Public Contract Exits Direct Edit
External Endpoint Migration Exits Direct Edit
Explicit Bug Intent Wins Before Direct Edit
Cross-Session Need Uses Lightweight Change
New Test Requirement Exits Direct Edit
Failed Minimum Check Blocks Completion
Unrelated Dirty Work Blocks Exact Attribution
Direct Edit Grants No Later Action
Existing Lightweight Cards Remain Unchanged
Existing Test Obligations Stay At Owning Boundary
Same-Property Tuning Checks Only Final Value
Business Multiplier Is Not Cosmetic
Commit-Only Request Runs No Tests
New Full Run Waits For Exact Human Confirmation
Exact Gate 2 Full Run Does Not Ask Twice
Changed HEAD Expires Full-Run Confirmation
Declined Optional Full Run Limits Claims Not Commit
Declined Required Release Validation Blocks Release
Push-Triggered CI Is Disclosed And Not Duplicated
Manual CI Rerun Requires Fresh Confirmation
```

- [x] Update README and Usage with examples for typo, spacing loop, display versus business multiplier, exact full-run confirmation, Commit without tests, Push CI, and Release decline.
- [x] Add `## 1.5.8 — 2026-08-26` to CHANGELOG. During Phase 1, record truthful `focused validation complete; full validation awaiting Human confirmation`; only Phase 2 evidence may add a fresh full-validation claim. Synchronize `SKILL.md`, `plugin.json`, `README.md`, `Usage.md`, CHANGELOG, all 13 root managed blocks, and every live version assertion together.

### Task 6: Reach Focused GREEN And Run Boundary Mutations

**Files:** Modify the new focused test, affected focused tests, and only source files proven wrong by a focused failure.

- [x] Run the new focused contract:

```bash
bash tests/validate-direct-edit-fast-path.sh
```

Expected: `PASS: Direct Edit and Human-confirmed full-test contracts are complete`.

- [x] Run affected legacy contracts, not all tests:

```bash
for test_file in \
  tests/validate-lightweight-change-lane.sh \
  tests/validate-full-worktree-git-fast-path.sh \
  tests/validate-progressive-verification.sh \
  tests/validate-maintainer-full-validation-guidance.sh \
  tests/validate-mandatory-helper-routing.sh \
  tests/validate-root-agents-block-refresh.sh \
  tests/validate-root-agents-block-checker.sh \
  tests/validate-project-skill-discovery-guard.sh \
  tests/validate-project-local-skills.sh \
  tests/validate-repair-first-verification.sh \
  tests/validate-v1.2.4-root-stage-coverage.sh \
  tests/validate-branch-management-strategy.sh \
  tests/validate-bug-management.sh \
  tests/validate-requirement-lifecycle-backlog.sh; do
  bash "$test_file"
done

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_project_guidance_consistency \
  tests.test_root_agents_blocks \
  tests.test_root_agents_lossless_slimming \
  tests.test_lightweight_change_scan
```

Expected: all PASS. The existing Lightweight scanner test proves Direct Edit did not change persisted card behavior.

- [x] Run mechanical checks:

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
python3 -m json.tool plugin.json >/dev/null
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
git diff --check
```

Run the repository Markdown-fence check across changed Markdown. Expected: balanced fences and no whitespace error.

- [x] Run scope/version checks:

```bash
git status --short --branch
git diff --stat
git diff --name-only
rg -n 'Direct Edit (Mode|Status|Lifecycle)|\.agent-loop/direct-edits|--skip-tests|--no-verify' \
  SKILL.md references templates README.md Usage.md AGENTS.md docs/maintenance tests
rg --pcre2 -n 'Version: 1\.5\.(?!8)|"version": "1\.5\.(?!8)"|Current version.*1\.5\.(?!8)|版本.*1\.5\.(?!8)' \
  SKILL.md plugin.json README.md Usage.md
```

Expected: only planned files; forbidden search has no positive runtime contract (negative assertions or explicit prohibitions may match); every current version value is `1.5.8`; all 13 root blocks share `1.5.8-20260826.1`.

## Phase 1 Human Review Checkpoint

**Checkpoint state (2026-08-26):** reached. The new focused contract plus 15 affected Shell contracts passed; embedded/specified Python executions (`37`, `6`, and `55`) passed; YAML, JSON, Shell syntax, Markdown fence balance, `git diff --check`, version, root-revision, and scope checks passed. No repository-wide suite was run.

After Task 6, stop and present:

| Review item | Evidence required |
|---|---|
| Direct Edit route | runtime/design/reference sequence plus positive/negative focused results |
| Zero artifact | no template/parser/scanner/directory/memory record and unchanged card schema |
| Same-scope tuning | mutation proof that only final Human-accepted value is checked |
| Full-run authority | exact signature, expiry, no duplicate Gate 2 prompt, Profile not permission |
| Commit/Push/Release | Commit no tests; disclosed CI; manual rerun confirmation; required Release validation blocks if declined |
| Compatibility | Feature/Bug/Lightweight/Checker/Archive/Memory gates unchanged |
| Version/root | all version-bearing surfaces use `1.5.8`; all 13 root blocks use `1.5.8-20260826.1` |
| Phase 2 request | exact commands, current branch/full HEAD, changed-path inventory and content digest, expected cost, purpose, recommendation |

Do not start Phase 2 from a generic implementation continuation. The Human must accept the displayed concrete full-run command set. If the Human explicitly names that same exact suite, do not ask twice.

## Phase 2 — Human-Confirmed Full Validation

### Task 7: Run The Confirmed Repository-Wide Suites Once

**Precondition:** current exact full-run signature was accepted after Phase 1.

- [x] Run the confirmed Shell suite once:

```bash
for test_file in tests/*.sh; do
  bash "$test_file"
done
```

Expected: every Shell contract PASS; record total/pass/fail and elapsed time.

- [x] Run the confirmed Python suite once:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
```

Expected: all Python tests PASS; record total/pass/fail and elapsed time.

- [x] On failure, preserve output and run only focused diagnosis/RED/GREEN. Do not silently rerun either full suite. Any repair changes the input signature, so present a fresh full-run confirmation before rerun.

### Task 8: Perform Six-Domain Audit And Write The Fresh Report

**Files:** Create `docs/reports/agent-loop-1.5.8-full-validation-2026-08-26.md`; read the full-validation method and every changed control surface.

- [x] Audit Logic Correctness, Autonomy, Project Entry/Onboarding, Development/Test Workflow, Memory, and Recommendation.
- [x] Cover Direct Edit versus Lightweight/Feature/Bug, zero-artifact recovery, full-run expiry, Gate 2, Commit/Push/CI, Release decline, Checker repair, root guidance, and no new stage/status/mode.
- [x] Run Task 6 mechanical checks. These are not a second full suite. If a repair changes suite inputs, stop for renewed full-run confirmation.
- [x] Write the report in Chinese with:

```text
audit object, branch, full HEAD, dirty input, accepted full-run signature
score/grade and Critical/High/Medium/Low
six-domain table
real RED -> focused GREEN -> full GREEN
Shell/Python/mechanical counts and elapsed time
24 Direct Edit/full-run pressure scenarios
preserved Human Gates and version boundary
macOS actual and Windows test-defined status
residual risk, scope drift, stop conditions
Commit/Push/Tag/Release all not authorized
```

Do not reuse the 2026-08-16 score or counts.

### Task 9: Final Maintainer Review And Human Review Stop

- [x] Verify every Proposal item using the coverage matrix below and inspect the full actual diff.
- [x] Set Proposal status to `implemented and validated; awaiting final Human Review` only if focused and Human-confirmed full validation pass. If Phase 2 is declined/failed, use `implemented; full validation pending/blocked` and make no validated claim.
- [x] Align this Plan's task/status truth with actual evidence.
- [x] Present changed files, RED/GREEN, focused/full counts, six-domain score, residuals, version `1.5.8`, root revision, branch/version mismatch, Windows boundary, and Git state.
- [x] Explicitly state that no stage, Commit, Push, tag, PR, merge, release, publish, or installed Skill synchronization occurred.

**Phase 2 checkpoint (completed 2026-08-27):** the first confirmed Shell run exposed one brittle global token-order assertion. The failure was preserved, repaired with focused RED/GREEN, and the changed input was not rerun until a new exact Human confirmation bound branch `alpha/v1.5.8`, full HEAD, dirty inventory, environment, commands, and digest. The final confirmed run passed 53/53 Shell contracts and 420/420 Python tests; the Chinese report records a 96/100 STRONG result and one Low regression-hardening residual.

## macOS And Windows Boundary

- macOS runs the Bash/Ruby/Python maintainer contracts and records actual results.
- Windows is test-defined because this change adds no runtime executable. Direct Edit chooses the cheapest platform-native parser/syntax/reference command and must not hardcode POSIX-only execution.
- `python3` versus `py -3`, path separators, shell, environment, and target differences form different full-run signatures and need their own confirmation.
- Bash contracts are repository-maintainer tests; target-project Windows Agents do not need Bash.
- A new executable is scope drift and stops for revised Human Review.

## Rollback

Before any separately authorized Git submission:

1. remove only the new reference, focused test, and reports created by this implementation;
2. reverse only this implementation's coordinated Markdown/test/revision edits;
3. restore all version-bearing surfaces to `1.5.7` and all 13 root blocks and pins together to `1.5.7-20260815.1` only for a full version/root-projection rollback;
4. rerun the four planning-baseline focused contracts and root tests;
5. never restore, clean, reset, stash, or overwrite unrelated Human work.

If a later independent Gate committed the work, prefer a new inverse commit over destructive reset unless the Human explicitly authorizes another strategy.

## Immediate Stop Conditions

Stop when:

- branch/HEAD or dirty work has an unclear overlapping owner;
- Direct Edit needs a product/technical/security/data/interface/dependency/migration/architecture decision;
- implementation needs a template/parser/scanner/directory/status/mode/lifecycle/cache/bypass flag;
- an Existing Test Obligation would be removed rather than preserved;
- Gate 2 lacks exact commands/scope but is treated as full-run permission;
- Commit, Push, CI, Release, or Checker repair inherits another action's authorization;
- a full suite lacks current exact Human confirmation;
- a full-suite rerun follows changed inputs without renewed confirmation;
- root blocks would carry mixed revisions;
- any version-bearing file would differ from `1.5.8`, or any root block would differ from `1.5.8-20260826.1`;
- implementation would sync installed Skills or perform Git/release/external actions.

## Proposal Coverage Matrix

| Proposal requirement | Tasks |
|---|---|
| Direct Edit below Lightweight and inside accepted Feature | 2–3 |
| Eligibility/hard escalation and no artifact/test/record | 1–3, 6 |
| Minimum diff/proof and final-only tuning | 2–3, 5–6 |
| Display versus business/runtime multiplier | 2, 5–6 |
| Targeted evidence default | 3–4 |
| Exact one-run confirmation, expiry, and no duplicate Gate 2 prompt | 4–8 |
| Verification Profile is not permission | 4–6 |
| Commit no tests and optional decline limits claims | 4–6 |
| Push CI disclosure/no duplicate/manual rerun | 4–6 |
| Required Release validation decline blocks | 4–6 |
| Existing Feature/Bug/Lightweight/Git/safety gates | 2–8 |
| No stage/status/mode/artifact/bypass; coordinated approved version | 2–9 |
| Focused RED/GREEN and mutation resistance | 0–6 |
| Human-confirmed full suites and six-domain audit | 7–8 |
| macOS actual and Windows test-defined | 6–9 |

## Plan Self-Review

- **Spec coverage:** every Proposal section maps to the matrix; Direct Edit and full-run confirmation remain coordinated but separable.
- **Placeholder scan:** no unresolved marker, unnamed test, unspecified output path, or deferred implementation instruction is permitted.
- **Terminology:** use `Direct Edit Fast Path`, `Direct Edit Assessment`, `Lightweight Change Lane`, `Feature Verification Profile`, `Full Test Run Confirmation`, `Required Verification`, `Existing Test Obligation`, and `Full-Worktree Git Fast Path`. Never add Direct Edit Mode/Status or no-verify terminology.
- **Scope:** this is a Markdown/test contract change; a runtime Checker or persistent authorization object is over-design.
- **Git:** writing-plans' frequent-commit default is overridden by Agent Loop Human Gates. This Plan has no Commit step.

## Handoff

After Human acceptance, give the development Agent:

```text
Execute docs/proposal/v1.5.x/direct-edit-fast-path-implementation-plan.md from Task 0 through Phase 1 Task 6 only. Preserve the accepted Proposal, prove real RED before production edits, synchronize every version-bearing surface to `1.5.8`, do not run repository-wide tests, and stop at the Phase 1 Human Review Checkpoint with the exact proposed Phase 2 full-run signature. Do not dispatch Subagents, create/switch branch or worktree, sync installed Skills, stage, commit, push, tag, PR, merge, release, or publish.
```

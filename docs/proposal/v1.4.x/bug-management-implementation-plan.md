# Human-Guided Bug Management Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Do not dispatch subagents unless the human separately authorizes a bounded dispatch.

**Goal:** Implement the approved first-class Bug Record, dual-axis lifecycle, 90-day evidence-ranked Feature ownership scan, Requirement relationships, Feature-based repair, verification, and Human Gates without adding a canonical stage or a second implementation workflow.

**Architecture:** Add one detailed runtime authority, `references/bug-management.md`, plus Bug Index / Bug README templates. Bug Management remains an internal method of `Feature Follow-up / Flow-back`: Bug artifacts own intake, evidence, lifecycle, Resolution Path, and close history; Requirement artifacts own product meaning; Feature artifacts own every code repair. Runtime, stage/checklist, memory, archive, branch, submit, root guidance, human docs, and regression contracts consume the same model.

**Tech Stack:** Markdown skill sources and templates, Bash/Ruby contract assertions, existing Python 3.10+ root-guidance tests, Mermaid diagrams, repository full-validation method. No new runtime dependency, executable Bug database, YAML/JSON schema, or third-party package.

---

## Plan Status And Execution Boundary

- Plan status: human-approved; Tasks 0–10 implementation, focused/full validation, and primary-agent self-review are complete; final Human Review is pending.
- Repository perspective: Agent Loop skill source maintainer. Do not create repository-root `.agent-loop/bugs/` or any other target-project artifacts.
- Current branch at planning time: `alpha/v1.4.0`.
- Current baseline commit: `85d593cf7bf57533570ac5f2aeed150450b21af7`.
- Current skill version: `1.4.0`; this plan does not authorize a version bump.
- Current root managed-block revision: `1.4.0-20260715`; implementation advances all blocks to `1.4.0-20260715.1` as a same-version content revision.
- Current executable baseline: 98 Python tests and 35 `tests/*.sh`; recount live inventory before recording evidence.
- Existing untracked design input: `docs/proposal/v1.4.x/bug-management.md`. Preserve it and update only its status/evidence sections during implementation.
- Do not create or modify real Git branches, worktrees, tags, remotes, PRs, releases, external Issue Tracker items, or Agent CLI installations.
- Do not commit, push, merge, release, publish, or tag during implementation. Final submission requires a fresh staged-diff Human Gate.

## Stage Helper Resolution

| Field | Resolution |
|---|---|
| Stage | Plan Gate / Plan |
| Canonical candidate | `superpowers:writing-plans` — not exposed by the current runtime |
| Alias candidate | `writing-plans` — loaded completely from `/Users/shaodowyd/.codex/skills/writing-plans/SKILL.md` |
| Status | `loaded` |
| Fallback | `no` |
| Method used | file responsibility map, exact TDD sequence, explicit invariants, exact commands, expected RED/GREEN, self-review |
| Agent Loop override | save beside the approved proposal; no automatic worktree, subagent, commit, push, tag, release, publish, or target-project artifact |

## Non-Negotiable Invariants

1. Bug Management is an internal method of `Feature Follow-up / Flow-back`, not a canonical stage or a new message-intent value.
2. `.agent-loop/bugs/` is created only in a target project after explicit bug-record/manage/fix intent; the skill source repository never gets a root `.agent-loop/`.
3. Bug Report, Bug Record, Report Origin, Evidence, Expected Behavior, Resolution Path, Status, Resolution, and Reopen remain distinct concepts.
4. Bug Status is exactly `reported | triaging | confirmed | in-progress | verifying | deferred | closed`.
5. Bug Resolution is exactly `unresolved | fixed | duplicate | not-a-bug | cannot-reproduce | accepted-risk | superseded`.
6. Report Origin may be a person, customer, group, QA, monitoring, automated test, agent, external ticket, other, or unknown; it never becomes personnel ownership, assignment, permission, or priority evidence.
7. There is no default personnel `Owner` / `Assignee`, SLA, staffing, sprint, or workload system.
8. Bug relationships to Requirement are optional `0..N`; a Bug never automatically mutates Requirement lifecycle or rewrites immutable Requirement sources.
9. Every code repair uses an existing/reopened Feature, linked new Feature, or `Feature Type: maintenance-fix`; Bug artifacts never own tasks, tests, plan, or code execution.
10. A Bug has one current Resolution Path; a coherent Feature may resolve multiple Bugs.
11. Duplicate/reopen discovery scans all Bug Index metadata without a time cutoff.
12. Feature ownership defaults to a 90-calendar-day metadata/summary scan, deep-reads only evidence-overlapping candidates, and remains extendable beyond 90 days.
13. Archive changes location, not Feature identity or ownership. Discovery can read archived artifacts without rehydrate; execution flow-back requires verified Human-gated rehydrate.
14. Tests passing moves a Bug to `verifying`; only complete evidence plus the explicit Bug Close Gate permits `closed`.
15. `closed` cannot use `Resolution: unresolved`; `deferred` is not closed; reopen is append-only and restores `unresolved`.
16. `bugs/INDEX.md` owns inventory/backlog/locator; `project.md` never stores the Bug backlog.
17. Severity and Priority do not authorize hotfix, branch, deploy, release, or publish actions.
18. Existing Delivery Contract, Feature close, submit, commit, branch, merge, cleanup, release, publish, and archive gates remain intact.

## File Responsibility Map

### Create

- `references/bug-management.md` — complete runtime authority for Bug identity, artifacts, lifecycle, evidence, dedup/reopen, 90-day discovery, relationships, Feature repair, gates, recovery, and scope.
- `templates/bug-index.md` — target-project Bug inventory / backlog / locator template.
- `templates/bug-README.md` — target-project Bug Record source-of-truth template.
- `tests/validate-bug-management.sh` — focused cross-surface, lifecycle, root-guidance, archive, version, and negative-scope contract.
- `docs/reports/agent-loop-v1.4.0-bug-management-red-baseline-2026-07-15.md` — existing GREEN baseline plus focused RED evidence.
- `docs/reports/agent-loop-v1.4.0-full-validation-2026-07-15.1.md` — fresh Chinese six-domain validation report; do not overwrite the earlier branch-management report.

### Modify: Controller And Runtime Authority

- `SKILL.md` — concise package-map route, required behavior, Auto Mode stops, fail-closed checks, and template inventory.
- `references/runtime.md` — Bug Management routing inside Feature Follow-up, state/Resolution rules, 90-day discovery, unique next action, and no new canonical stage.
- `references/design.md` — core Bug concepts, relationship/data model, state machine, authority split, and invariants.
- `references/concepts.md` — concise published definitions.
- `references/feature-follow-up.md` — Bug Index scan before Feature candidate scan, default lookback change 30 -> 90, archive discovery, and routing into Bug Management.

### Modify: Artifact And Memory Ownership

- `references/artifact-rules.md` — Bug directory/file ownership, forbidden Bug task/plan artifacts, INDEX authority, and source immutability.
- `references/document-templates.md` — synchronized inline copies of Bug Index / README and Bug link fields in Feature artifacts.
- `references/project-memory-mode.md` — Bug backlog stays in Bug Index in simple and enterprise modes.
- `references/project-guidance.md` — root navigation and Project Entry/Re-Adopt implications only.
- `templates/project.md` — change default `Feature Follow-up Lookback` to `90 days`; do not add open Bug lists.
- `templates/spec.md` — add optional `Related Bugs` and Bug Resolution Path source references.
- `templates/tests.md` — add optional Bug Verification Matrix.
- `templates/plan.md` — add Bug Context Evidence pointer for repair execution; no Bug task ownership.
- `templates/notes.md` — update lookback to 90 days and add Bug repair/verification backlink fields.
- `templates/requirement-set-README.md` — optional Related Bugs / Requirement Impact summary without changing Requirement source authority.

### Modify: Stage, Gate, And Integration Surfaces

- `references/stage-guides.md` — Feature Follow-up/Bug Intake, Requirements Discussion return, Feature Spec, Verify, Drift, Memory, Completion, and Submit procedures.
- `references/workflow-checklists.md` — checklist equivalents for the same lifecycle and gate transitions.
- `references/human-review-summary.md` — Bug Triage / Resolution Path and Bug Verification / Close summary tables.
- `references/requirement-management.md` — optional `0..N` Bug links and Human-gated Requirement Reconciliation only when delivery truth is invalidated.
- `references/implementation-planning.md` — repair plan must cite Bug Context and keep implementation in Feature artifacts.
- `references/feature-completion-check.md` — related Bugs must reach `verifying` with evidence; Bug close and Feature close remain separately named Human decisions.
- `references/branch-management.md` — consume confirmed Fix Feature / Target Release Context only; no inference from severity/priority.
- `references/submit-and-integrate.md` — validate related Bug evidence/status and forbid submit rationalization.
- `references/external-skill-adapters.md` — debugging/finishing helpers return evidence without taking Bug, Feature, state, or Git authority.

### Modify: Human Guidance, Root Navigation, And Version Record

- `templates/root-AGENTS.md` — keep the existing Feature Follow-up stage row, route bug reports through `references/bug-management.md`, and advance every managed block to `block-version:1.4.0-20260715.1`; do not copy lifecycle/data tables into root guidance.
- `README.md` — overview, artifact layout, and capability summary; keep Current version `1.4.0`.
- `Usage.md` — human trigger examples and compact lifecycle/repair diagram; keep visible version `1.4.0`.
- `CHANGELOG.md` — add implemented Bug Management under `1.4.0`; record root revision `.1`; do not create another version heading.
- `docs/proposal/v1.4.x/bug-management.md` — implementation and validation status only after the corresponding evidence exists.

### Modify: Validation And Root Revision Expectations

- `references/validation-scenarios.md` — all 20 proposal scenarios plus gate-rationalization adversarial cases.
- `tests/test_root_agents_blocks.py`
- `tests/validate-branch-management-strategy.sh`
- `tests/validate-project-local-skills.sh`
- `tests/validate-requirement-lifecycle-backlog.sh`
- `tests/validate-root-agents-block-checker.sh`
- `tests/validate-root-agents-block-refresh.sh`
- `tests/validate-v1.2.4-root-stage-coverage.sh`

### Review Only Unless A Real Contradiction Is Found

- `plugin.json` — must stay `1.4.0`.
- `agents/openai.yaml` — metadata/YAML validation only.
- `scripts/` — no Bug schema/checker is planned; do not add one merely for symmetry.
- `examples/` — no default change; focused validation scenarios and templates are sufficient for v1.
- root `AGENTS.md` — maintainer guidance remains source-repository-only and does not receive downstream Bug rules.

## Coordinated Implementation Order

```text
existing GREEN baseline
→ focused Bug contract RED
→ canonical Bug reference + controller/design/runtime
→ Bug templates + artifact/memory ownership
→ stage/gate/Requirement/Feature/Archive integration
→ branch/submit/helper integration
→ root/human docs/version record
→ 20+ pressure scenarios + focused GREEN
→ full regression + six-domain audit
→ Human Review
→ separately authorized Submit / Integrate
```

## Task 0: Preserve Baseline And Create Focused RED

**Files:**

- Create: `tests/validate-bug-management.sh`
- Create after RED: `docs/reports/agent-loop-v1.4.0-bug-management-red-baseline-2026-07-15.md`
- Review: `git status`, current version fields, root revision, test inventory

- [x] **Step 1: Confirm the execution boundary before changing runtime files.**

Run:

```bash
git status --short --branch
git rev-parse HEAD
rg -n 'Version: 1.4.0|"version": "1.4.0"|Current version:\*\* 1.4.0|\*\*版本：\*\* 1.4.0' SKILL.md plugin.json README.md Usage.md
rg -c 'block-version:1.4.0-20260715' templates/root-AGENTS.md
find tests -maxdepth 1 -name '*.sh' -type f | wc -l
```

Expected:

```text
branch: alpha/v1.4.0
HEAD: 85d593cf7bf57533570ac5f2aeed150450b21af7
version-bearing files: 1.4.0
root managed blocks at 1.4.0-20260715: 13
tests/*.sh: 35 before the new focused contract
only approved proposal/plan files are untracked
```

Stop if unrelated dirty work overlaps an implementation file, HEAD/branch changed unexpectedly, or root revision is no longer the observed baseline.

- [x] **Step 2: Run the existing executable baseline before adding the new test.**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/agent-loop-bug-baseline-pyc \
  python3 -m unittest discover -s tests -p 'test_*.py' -v

for test_file in tests/*.sh; do
  bash "$test_file"
done
```

Expected: 98/98 Python PASS and 35/35 Shell PASS. Record real counts; do not absorb an existing failure into Bug Management.

- [x] **Step 3: Create the focused contract with complete positive and negative assertions.**

Create `tests/validate-bug-management.sh` with this structure and exact contract values:

```bash
#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

assert_file() {
  [ -f "$root/$1" ] || fail "missing required file: $1"
}

assert_contains() {
  local file=$1
  local text=$2
  grep -Fq -- "$text" "$root/$file" || fail "$file missing Bug Management contract: $text"
}

assert_not_contains() {
  local file=$1
  local text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    fail "$file contains forbidden Bug Management behavior: $text"
  fi
}

for file in \
  references/bug-management.md \
  templates/bug-index.md \
  templates/bug-README.md; do
  assert_file "$file"
done

for text in \
  'reported | triaging | confirmed | in-progress | verifying | deferred | closed' \
  'unresolved | fixed | duplicate | not-a-bug | cannot-reproduce | accepted-risk | superseded' \
  'investigate-first | flow-back | linked-feature | maintenance-fix | requirement | no-fix' \
  'person | customer | group | qa | monitoring | automated-test | agent | external-ticket | other | unknown' \
  'Bug identity does not use a time cutoff.' \
  'Default Feature ownership lookback is 90 calendar days.' \
  'Archive changes location, not Feature identity or ownership.' \
  'Discovery and Human Review do not require rehydrate.' \
  'Bug artifacts do not own tasks, tests, plans, or code execution.'; do
  assert_contains references/bug-management.md "$text"
done

for file in SKILL.md references/runtime.md references/design.md references/feature-follow-up.md references/stage-guides.md references/workflow-checklists.md; do
  assert_contains "$file" 'Bug Management'
done

assert_contains references/feature-follow-up.md 'Default recent window: **90 calendar days**'
assert_contains references/feature-follow-up.md 'Bug Index metadata has no time cutoff'
assert_contains references/branch-management.md 'Bug Management owns Bug identity, lifecycle, and Resolution Path.'
assert_contains templates/project.md 'Feature Follow-up Lookback: 90 days'
assert_contains templates/notes.md 'Lookback Window: 90 days | outside-default-window'
assert_contains templates/bug-README.md 'Origin Type: person | customer | group | qa | monitoring | automated-test | agent | external-ticket | other | unknown'
assert_contains templates/bug-README.md 'Requirement Impact: none | violates-accepted-behavior | ambiguity-found | change-required'
assert_contains templates/bug-README.md 'Status: reported | triaging | confirmed | in-progress | verifying | deferred | closed'
assert_contains templates/bug-README.md 'Resolution: unresolved | fixed | duplicate | not-a-bug | cannot-reproduce | accepted-risk | superseded'
assert_contains templates/spec.md 'Related Bugs:'
assert_contains templates/tests.md '## Bug Verification Matrix'
assert_contains templates/plan.md 'Bug Context Evidence:'
assert_contains templates/notes.md 'Related Bugs:'
assert_contains templates/requirement-set-README.md 'Related Bugs:'
assert_contains references/feature-completion-check.md 'Bug Close Decision'
assert_contains references/human-review-summary.md '### Bug Triage And Resolution Path Review'
assert_contains references/human-review-summary.md '### Bug Verification And Close Review'
assert_contains references/validation-scenarios.md '60-Day Feature Remains Inside Default Bug Ownership Window'
assert_contains references/validation-scenarios.md 'Archived Feature Discovery Does Not Require Rehydrate'
assert_contains references/validation-scenarios.md 'Passing Feature Tests Does Not Auto-Close Bug'

assert_not_contains templates/bug-README.md 'Assignee:'
assert_not_contains templates/bug-README.md 'Owner:'
[ ! -e "$root/templates/bug-tasks.md" ] || fail 'Bug must not have its own tasks template'
[ ! -e "$root/templates/bug-tests.md" ] || fail 'Bug must not have its own tests template'
[ ! -e "$root/templates/bug-plan.md" ] || fail 'Bug must not have its own plan template'
[ ! -d "$root/.agent-loop" ] || fail 'skill source repository must not contain target-project .agent-loop artifacts'

ruby - "$root/references/runtime.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
section = content[/## Stage Order\n(.*?)(?=\n## |\z)/m, 1]
abort 'FAIL: runtime Stage Order missing' unless section
abort 'FAIL: Bug Management became a canonical stage' if section.lines.any? { |line| line.strip == 'Bug Management' }
RUBY

ruby - "$root/templates/root-AGENTS.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
blocks = content.scan(/<!-- agent-loop:managed-start section:([^ ]+) .*?block-version:([^ ]+) -->/)
abort 'FAIL: root managed blocks missing' if blocks.empty?
blocks.each do |section, revision|
  expected = '1.4.0-20260715.1'
  abort "FAIL: #{section} expected #{expected}, found #{revision}" unless revision == expected
end
RUBY

printf 'PASS: Human-Guided Bug Management identity, lifecycle, routing, archive, gate, artifact, and scope contract is complete\n'
```

- [x] **Step 4: Run the focused contract before implementation and preserve the actual RED.**

Run:

```bash
bash tests/validate-bug-management.sh
```

Expected first failure:

```text
FAIL: missing required file: references/bug-management.md
```

Do not weaken assertions to make the test pass.

- [x] **Step 5: Write the RED baseline report.**

Record:

- date, branch, HEAD, version, dirty boundary;
- 98/98 and 35/35 existing GREEN evidence;
- exact focused RED command/output/exit code;
- proposal concepts and 90-day/archive additions covered by the contract;
- no runtime file, target-project artifact, branch, commit, push, tag, PR, release, publish, or CLI install changed.

## Task 1: Publish Canonical Bug Artifact And Concept Contracts

**Files:**

- Create: `references/bug-management.md`
- Modify: `references/concepts.md`
- Modify: `references/design.md`
- Modify: `references/artifact-rules.md`

- [x] **Step 1: Create the complete Bug Management reference from the approved proposal.**

The reference must contain these sections in this order:

```markdown
# Human-Guided Bug Management

## Purpose And Scope
## Concepts And Authority
## Artifact Layout
## Bug Identity And Duplicate Rules
## Report Origin
## Expected Behavior Evidence
## Status And Resolution
## Severity And Priority
## Requirement Relationships
## Resolution Path And Feature Repair
## Bug Identity Scan And 90-Day Feature Ownership Scan
## Archived Feature Discovery And Rehydrate Boundary
## Verification, Close, And Reopen
## Human Gates And Auto Mode Stops
## Project Memory And Recovery
## Branch And Submit Integration
## Forbidden Scope
```

Use the approved exact enumerations:

```text
Status: reported | triaging | confirmed | in-progress | verifying | deferred | closed
Resolution: unresolved | fixed | duplicate | not-a-bug | cannot-reproduce | accepted-risk | superseded
Resolution Path: investigate-first | flow-back | linked-feature | maintenance-fix | requirement | no-fix
Origin Type: person | customer | group | qa | monitoring | automated-test | agent | external-ticket | other | unknown
Requirement Impact: none | violates-accepted-behavior | ambiguity-found | change-required
```

Include these exact normative statements because the focused contract depends on them:

```text
Bug identity does not use a time cutoff.
Default Feature ownership lookback is 90 calendar days.
Archive changes location, not Feature identity or ownership.
Discovery and Human Review do not require rehydrate.
Bug artifacts do not own tasks, tests, plans, or code execution.
```

- [x] **Step 2: Add concise concept definitions.**

Add definitions for Bug Report, Bug Record, Report Origin, Bug Evidence, Expected Behavior Evidence, Resolution Path, Bug Status, Bug Resolution, Reopen Record, and Bug Ownership Lookback. Keep each definition short and point detailed behavior to `bug-management.md`.

- [x] **Step 3: Add the complete relationship and state model to design authority.**

`references/design.md` must include:

```text
Bug Report 1..N -> 1 Bug Record
Bug Record 0..N -> Requirement
Bug Record 0..N -> Related Feature / Decision / Contract
Bug Record 1 -> current Resolution Path
Bug Record 0..1 -> Fix Feature while repair is active
Feature 0..N -> Bug Record
Bug Record 0..1 -> Duplicate Of canonical Bug Record
```

It must state that one Feature can resolve multiple coherent Bugs, one Bug has one current path, and no personnel owner/assignee is introduced.

- [x] **Step 4: Add artifact ownership and forbidden paths.**

Add rows for `bugs/INDEX.md`, `bugs/YYYY-MM-DD-<bug-slug>/README.md`, and optional `evidence/`. Explicitly forbid `.agent-loop/bugs/<bug>/tasks.md`, `tests.md`, `plan.md`, and a Bug implementation subtree.

- [x] **Step 5: Run the focused contract and confirm it advances past the missing-reference failure.**

Expected: still RED on the next missing runtime/template assertion, proving the reference is now discoverable.

## Task 2: Integrate Controller, Runtime, And Feature Follow-up Routing

**Files:**

- Modify: `SKILL.md`
- Modify: `references/runtime.md`
- Modify: `references/feature-follow-up.md`
- Modify: `references/external-skill-adapters.md`

- [x] **Step 1: Add package-map and concise controller routes.**

`SKILL.md` must route explicit Bug management to `references/bug-management.md`, retain `Feature Follow-up / Flow-back` as the owning stage, list the two Bug templates, and keep detailed lifecycle out of the entrypoint.

Required concise behavior:

```text
When explicit bug-report, manage, investigate, or fix intent exists, use Bug Management inside Feature Follow-up / Flow-back. Scan complete Bug Index metadata for duplicate/reopen first, then use the project-configured 90-day Feature ownership metadata window and evidence-driven extended scan. Bug confirmation never authorizes Feature, Requirement, branch, submit, or close actions.
```

- [x] **Step 2: Integrate runtime without adding a stage or message intent.**

Keep `feature-follow-up` as the classification and add the internal sequence:

```text
explicit bug intent
-> reliable memory or Project Entry
-> Bug Index duplicate/reopen scan
-> Bug Record reported/triaging
-> Expected Behavior evidence
-> confirmed or non-fix disposition candidate
-> one recommended Resolution Path
-> Human Gate
-> existing Requirement / Feature / Verify / Close stages
```

Runtime must stop on invalid state/Resolution combinations, ambiguous duplicate target, missing required Resolution Target, Requirement/Feature/ADR conflict, archive locator failure, and any Human-gated action without authorization.

- [x] **Step 3: Replace the default 30-day Feature Follow-up window with the approved tiered 90-day rule.**

In `references/feature-follow-up.md`:

- add complete Bug Index metadata scan before Feature candidates;
- change the default to `90 calendar days`;
- preserve `outside-default-window` extended scan;
- use Feature `Last Updated / Closed`, not archive month or directory mtime;
- read `features/archive.md` as locator only;
- allow read-only archived artifact discovery without rehydrate;
- require verified Human-gated rehydrate only before reopened execution.

- [x] **Step 4: Keep external helpers subordinate.**

Systematic debugging may provide reproduction/root-cause evidence; finishing helpers may provide branch hygiene. Neither helper may create/close/reopen Bug records, create Feature/Requirement artifacts, mutate lifecycle, or widen Git authority.

- [x] **Step 5: Run affected existing routing tests.**

Run:

```bash
bash tests/validate-chat-requirements-entry.sh
bash tests/validate-mandatory-helper-routing.sh
bash tests/validate-branch-management-strategy.sh
bash tests/validate-bug-management.sh
```

Expected: existing three PASS; focused contract remains RED only on not-yet-created templates/integration assertions.

## Task 3: Add Bug Templates And Memory Ownership

**Files:**

- Create: `templates/bug-index.md`
- Create: `templates/bug-README.md`
- Modify: `references/document-templates.md`
- Modify: `references/project-memory-mode.md`
- Modify: `references/project-guidance.md`
- Modify: `templates/project.md`

- [x] **Step 1: Create the Bug Index template.**

Use this exact table and ownership note:

```markdown
# Bug Index

This is an inventory, backlog, and locator. Each Bug README is the detail source of truth. Do not store Bug backlog rows in `project.md`.

| Bug ID | Title | Status | Resolution | Severity | Priority | Resolution Path | Target | Last Updated |
|---|---|---|---|---|---|---|---|---|
```

- [x] **Step 2: Create the complete Bug README template.**

Use the approved schema from the proposal, including:

- identity/dates/status/resolution;
- Report Origin with optional Origin Reference / Source Link;
- Observed and Expected Behavior;
- Severity/Priority/Reproduction Status;
- Related Bugs, Duplicate Of, Requirements, Features, Decisions, Contracts;
- Requirement Impact and Delivery Phase;
- Resolution Path, Target, Human Decision, Target Release Context;
- Evidence, Verification/Close, Status History, Reopen History.

Intentional artifact placeholders such as `<title>` and empty value slots are permitted; unfinished plan markers are not.

- [x] **Step 3: Synchronize inline document templates byte-for-byte for normative fields.**

`references/document-templates.md` must use the same enumerations and headings as the source templates. Do not create shortened conflicting lifecycle lists.

- [x] **Step 4: Keep Bug backlog out of project memory.**

Document that simple/enterprise modes both use `bugs/INDEX.md`. `project.md` may keep only the configurable lookback setting and current Active Feature; it must not add Open Bugs, Deferred Bugs, or Bug assignee lists.

- [x] **Step 5: Change the default project setting.**

Change:

```text
Feature Follow-up Lookback: 30 days
```

to:

```text
Feature Follow-up Lookback: 90 days
```

Project guidance must say human-confirmed overrides are allowed and never disable evidence-driven extended scan.

- [x] **Step 6: Run the focused contract.**

Expected: template and 90-day assertions pass; remaining RED points to Feature/Requirement/stage integration.

## Task 4: Connect Bug Records To Requirement And Feature Artifacts

**Files:**

- Modify: `references/requirement-management.md`
- Modify: `references/implementation-planning.md`
- Modify: `templates/requirement-set-README.md`
- Modify: `templates/spec.md`
- Modify: `templates/tests.md`
- Modify: `templates/plan.md`
- Modify: `templates/notes.md`
- Modify: `references/document-templates.md`

- [x] **Step 1: Add optional Requirement relationship fields and reconciliation boundary.**

Add:

```text
Related Bugs:
Requirement Impact: none | violates-accepted-behavior | ambiguity-found | change-required
```

State that Bug links are optional `0..N`, do not rewrite sources, and do not auto-change Requirement lifecycle. Only current evidence plus Human-gated Requirement Reconciliation may change delivery status.

- [x] **Step 2: Add Feature Spec Bug references.**

Near Source Requirements add:

```text
Related Bugs:
Bug Resolution Path: none | flow-back | linked-feature | maintenance-fix
```

Do not copy full Bug Report/Evidence into Feature Spec.

- [x] **Step 3: Add Bug Verification Matrix to Test Design.**

```markdown
## Bug Verification Matrix

Use only when this Feature resolves one or more Bug Records.

| Bug ID | Expected Behavior Evidence | Original Reproduction | Regression / Safety Verification | Result | Evidence Link |
|---|---|---|---|---|---|
```

- [x] **Step 4: Add a Bug Context pointer to plans.**

```text
Bug Context Evidence: none | .agent-loop/bugs/YYYY-MM-DD-<bug-slug>/README.md
Related Bug IDs: none | BUG-...
```

The plan repeats no Bug lifecycle and authorizes no Bug close, Feature create, or Git action.

- [x] **Step 5: Update feature notes and lookback.**

Change Follow-up Intake to `Lookback Window: 90 days | outside-default-window`, add `Related Bugs`, `Bug Status At Start`, `Bug Resolution Path`, and a Bug Verification / Close linkage section.

- [x] **Step 6: Synchronize document-template copies and run focused/requirement tests.**

Run:

```bash
bash tests/validate-bug-management.sh
bash tests/validate-requirement-lifecycle-backlog.sh
bash tests/validate-grill-artifact-templates.sh
```

Expected: existing tests PASS; focused contract proceeds to stage/gate assertions.

## Task 5: Integrate Lifecycle, Human Gates, Completion, And Recovery

**Files:**

- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/human-review-summary.md`
- Modify: `references/feature-completion-check.md`

- [x] **Step 1: Replace Feature Follow-up's Bug path with the complete internal Bug sequence.**

Stage guide and checklist must include:

```text
complete Bug Index metadata scan
-> 90-day Feature metadata scan
-> evidence-ranked deep read / extended scan
-> create/update/reopen Bug Record
-> Expected Behavior check
-> Status/Resolution validation
-> one Resolution Path recommendation
-> Human Gate
```

Keep adjustment/new-feature handling for non-Bug follow-ups.

- [x] **Step 2: Add transition ownership to Verify, Drift, Memory, Completion, and Submit.**

- Verify writes candidate evidence and moves related Bug from `in-progress` to `verifying` only after Feature evidence exists.
- Failed Bug-specific verification returns to `in-progress` or `triaging` with evidence.
- Drift routes Expected Behavior conflicts to Requirements Discussion / Requirement Reconciliation / Decision & Design.
- Project Memory Update writes no Bug backlog.
- Submit checks Bug links and evidence without closing Bugs automatically.

- [x] **Step 3: Define combined review without combined authorization.**

At Feature Completion, all related Bugs expected to be fixed must be `verifying` with fresh evidence. Present separately named decisions:

```text
Bug Close Decision: confirm | revise | keep-verifying
Feature Close Decision: confirm | continue | pause | revise-scope
```

One Human Review Summary may request both, but one decision cannot be inferred from the other. If Bug close is not confirmed, do not claim the Feature/Bug resolution loop complete.

- [x] **Step 4: Add Human Review tables.**

Add `### Bug Triage And Resolution Path Review` with Bug identity, Report Origin, Expected/Observed, duplicate/reopen, Severity/Priority, Requirement impact, recommended path/target, and explicit authorization.

Add `### Bug Verification And Close Review` with current Status, candidate Resolution, Fix Feature, original reproduction, regression evidence, Review/Drift, remaining risk, Bug Close Decision, Feature Close Decision, and explicitly unauthorized actions.

- [x] **Step 5: Add recovery fail-closed rules.**

Stop on INDEX/README mismatch, duplicate cycles, invalid Fix Feature/archive locator, closed+unresolved, in-progress without target, expired-only evidence, or expected-behavior authority conflicts. Recommend exactly one Recovery/Investigation/Human decision.

- [x] **Step 6: Run focused and lifecycle tests.**

Run:

```bash
bash tests/validate-bug-management.sh
bash tests/validate-v1.2.4-state-lifecycle-repairs.sh
bash tests/validate-v1.2.4-critical-control-repairs.sh
```

Expected: all PASS or focused RED only on remaining branch/root/docs/scenario assertions.

## Task 6: Integrate Archive, Branch, Submit, And Helper Boundaries

**Files:**

- Modify: `references/branch-management.md`
- Modify: `references/submit-and-integrate.md`
- Modify: `references/external-skill-adapters.md`
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`

- [x] **Step 1: Make archived Feature discovery read-only and path-safe.**

Require `features/archive.md` locator resolution, then allow read-only archived spec/tests/notes/close evidence. Rehydrate is forbidden during discovery/classification and required only after flow-back confirmation before reopened execution.

- [x] **Step 2: Consume Bug decisions in Branch Management without widening authority.**

Branch rules receive only a confirmed Fix Feature and Target Release Context. Severity/Priority/Origin cannot choose `bugfix` vs `hotfix`, create a patch version, or authorize Git actions.

Replace the old pre-implementation boundary with this exact ownership statement:

```text
Bug Management owns Bug identity, lifecycle, and Resolution Path. Branch Management consumes only the Human-confirmed Fix Feature and Target Release Context.
```

Update `tests/validate-branch-management-strategy.sh`: remove the historical assertion that the reference “does not implement Bug Management” and replace it with the ownership/consumer assertion above. Keep its negative checks for automatic branch or Git authorization.

- [x] **Step 3: Add Bug checks to Submit / Integrate.**

When a Feature resolves Bugs, show Bug IDs, current status, verification evidence, unresolved close decisions, Target Release Context, and branch isolation. Do not allow a commit/push request to rationalize Bug close or vice versa.

- [x] **Step 4: Keep helper adapters bounded.**

Systematic-debugging and testing helpers may return evidence; finishing helpers may return integration options. Agent Loop retains Bug lifecycle, Feature, Requirement, artifact path, Human Gate, and Git action ownership.

- [x] **Step 5: Run focused branch/submit contracts.**

```bash
bash tests/validate-bug-management.sh
bash tests/validate-branch-management-strategy.sh
bash tests/validate-mandatory-helper-routing.sh
```

Expected: all PASS except not-yet-added root/scenario/doc assertions in the focused contract.

## Task 7: Update Root Navigation, Human Docs, Changelog, And Same-Version Revision

**Files:**

- Modify: `templates/root-AGENTS.md`
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`
- Modify: `docs/proposal/v1.4.x/bug-management.md`
- Modify: root revision regression files listed in the File Responsibility Map

- [x] **Step 1: Keep root guidance routing-only.**

The existing Stage Map row stays `Feature Follow-up And Flow-back`, but its Read Next cell must route explicit bugs through `references/bug-management.md` and then ownership decisions through `references/feature-follow-up.md`.

Do not add Status, Resolution, Origin, directory layout, 90-day algorithm, or Gate tables to root guidance.

- [x] **Step 2: Advance all 13 managed blocks and exact fixtures together.**

Change every root marker and current fixture expectation to:

```text
block-version:1.4.0-20260715.1
```

Update all seven root-revision test files plus `tests/validate-branch-management-strategy.sh`. Preserve stale-fixture semantics: the stale input must remain a different revision from current.

- [x] **Step 3: Add human-facing Bug Management guidance.**

README: concise capability plus `.agent-loop/bugs/` layout.

Usage: examples for report/triage/duplicate/reopen/Requirement ambiguity/Feature repair/90-day ownership/archived owner, plus a compact diagram. Do not copy the entire runtime reference.

- [x] **Step 4: Record implemented behavior under `1.4.0`.**

Add a `### Human-Guided Bug Management` section and record root revision `.1`. Keep:

```text
SKILL.md Version: 1.4.0
plugin.json version: 1.4.0
README Current version: 1.4.0
Usage version: 1.4.0
```

- [x] **Step 5: Update Proposal status only after implementation evidence exists.**

Use:

```text
状态：Proposal 与核心设计已确认；实现与 focused GREEN 已完成，待全量验证和 Human Review
```

Do not claim release/publish/CLI sync.

- [x] **Step 6: Run root/version/human-doc regression.**

```bash
python3 -m unittest tests/test_root_agents_blocks.py -v
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-root-agents-block-refresh.sh
bash tests/validate-v1.2.4-root-stage-coverage.sh
bash tests/validate-project-local-skills.sh
bash tests/validate-requirement-lifecycle-backlog.sh
bash tests/validate-human-help-version-docs.sh
bash tests/validate-branch-management-strategy.sh
bash tests/validate-bug-management.sh
```

Expected: all PASS; 13/13 managed blocks at `.1`; skill version unchanged.

## Task 8: Add Twenty Pressure Scenarios And Finish Focused GREEN

**Files:**

- Modify: `references/validation-scenarios.md`
- Modify: `tests/validate-bug-management.sh`
- Modify: `docs/reports/agent-loop-v1.4.0-bug-management-red-baseline-2026-07-15.md`

- [x] **Step 1: Add all approved scenarios with the standard structure.**

Every scenario must include:

```text
Evidence:
Bug Record Decision:
Expected Behavior Source:
Resolution Path:
Required Human Gate:
Forbidden Action:
Next Stage:
```

Required scenario names:

1. Existing Feature Regression Flows Back
2. Narrow Internal Bug Uses Maintenance Fix
3. New Product Behavior Is Not Misclassified As Bug
4. Multiple Origins Deduplicate Into One Bug
5. Existing Bug Record Closes As Duplicate
6. Closed Bug Reopens Append-Only
7. Unknown Report Origin Does Not Block Triage
8. Cannot Reproduce Requires Attempt Evidence
9. Requirement Link Does Not Auto-Rollback Lifecycle
10. Bug May Link Multiple Requirements
11. One Feature May Resolve Multiple Bugs
12. Ordinary Chat Does Not Create Bug Artifact
13. Missing Agent Loop Memory Routes To Project Entry
14. Archived Feature Discovery Does Not Require Rehydrate
15. Sealed Release Requires New Patch Context
16. Passing Feature Tests Does Not Auto-Close Bug
17. Accepted Risk Requires Explicit Human Decision
18. Customer Origin Does Not Infer Customer Repair Line
19. 60-Day Feature Remains Inside Default Bug Ownership Window
20. 120-Day Feature Uses Evidence-Driven Extended Scan

- [x] **Step 2: Add adversarial gate cases.**

At minimum assert:

- accepted Requirement is reused as Feature authorization;
- critical Severity is reused as hotfix/branch/release authorization;
- unknown Origin is used to block repair;
- `deferred` is rationalized as `closed`;
- Feature tests are reused as Bug Close Gate;
- archive discovery automatically rehydrates;
- duplicate title automatically merges records;
- Bug Record receives tasks/tests/plan;
- commit/push approval is reused as Bug close.

- [x] **Step 3: Run focused GREEN.**

```bash
bash tests/validate-bug-management.sh
```

Expected:

```text
PASS: Human-Guided Bug Management identity, lifecycle, routing, archive, gate, artifact, and scope contract is complete
```

- [x] **Step 4: Update RED report with GREEN evidence without erasing history.**

Separate existing baseline, focused RED, repairs, and final focused GREEN. Record the real changed-file scope and current authorization boundary.

## Task 9: Run Full Validation And Produce Fresh Evidence

**Files:**

- Create: `docs/reports/agent-loop-v1.4.0-full-validation-2026-07-15.1.md`
- Review: every implementation file

- [x] **Step 1: Read and follow the current full-validation method.**

```bash
sed -n '1,260p' docs/maintenance/full-validation-method.md
```

This change modifies Human Gates, lifecycle, Feature Follow-up, Project Memory, root guidance, and cross-file invariants, so focused validation alone is insufficient.

- [x] **Step 2: Run the complete executable suite.**

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/agent-loop-bug-final-pyc \
  python3 -m unittest discover -s tests -p 'test_*.py' -v

for test_file in tests/*.sh; do
  bash "$test_file"
done
```

Expected if inventory is unchanged except the focused contract:

```text
Python: 98/98 PASS
tests/*.sh: 36/36 PASS
```

Recount; do not copy planned counts if the inventory changes legitimately.

- [x] **Step 3: Run the six-domain semantic audit.**

Explicitly pressure-test:

- Bug Report versus stable Bug identity;
- Bug Status versus Resolution;
- unknown Origin versus progress;
- Requirement evidence versus automatic lifecycle mutation;
- Bug confirmation versus Feature authorization;
- Feature verification versus Bug close;
- 90-day metadata scan versus full deep scan;
- day 91+ evidence-driven ownership;
- archived discovery versus rehydrate execution;
- Severity/Priority versus hotfix/Git authorization;
- one active Feature with multiple open Bugs;
- Bug Index backlog versus project memory;
- external helper evidence versus state/action authority.

- [x] **Step 4: Run mechanical checks.**

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md"); YAML.load_file("agents/openai.yaml")'
python3 -c 'import json; json.load(open("plugin.json", encoding="utf-8"))'
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/agent-loop-bug-compile-pyc \
  python3 -m compileall -q scripts tests
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
find . -name '*.rb' -type f -print0 | xargs -0 -n1 ruby -c
git diff --check
```

Also run the repository Markdown-fence balance and untracked whitespace checks, confirm no root `.agent-loop/`, remove generated `__pycache__`, and confirm no validation command/subagent remains active.

- [x] **Step 5: Write the Chinese full-validation report.**

Report:

- date/branch/version/HEAD/audit object;
- total score and six-domain table;
- Python/Shell counts and mechanical checks;
- RED/GREEN chronology;
- all 20 approved scenarios and adversarial findings;
- root revision and version synchronization;
- macOS/Windows evidence boundary;
- Critical/High/Medium/Low inventory;
- implementation scope drift;
- commit/push/tag/PR/merge/release/publish/CLI-sync authorization state.

Do not overwrite `docs/reports/agent-loop-v1.4.0-full-validation-2026-07-15.md`; that file is historical Branch Management evidence.

- [x] **Step 6: Update Proposal status after fresh full validation.**

If and only if all required checks pass and no unresolved Critical/High/Medium remains:

```text
状态：Proposal、核心设计、实现、focused validation 与全量验证已完成，待最终 Human Review
```

## Task 10: Self-Review And Return To Human Review

**Files:**

- Review: complete worktree diff
- Modify only if a contradiction is found: implementation, tests, proposal, plan, reports

- [x] **Step 1: Run plan/spec coverage review.**

Confirm every Proposal section maps to a runtime/reference/template/test/report change. Search for `30 days`, `30 天`, stale root revision, incomplete lifecycle enumerations, `Owner:`, `Assignee:`, and forbidden Bug task/plan artifacts.

- [x] **Step 2: Inspect the final diff and scope.**

```bash
git status --short --branch
git diff --stat
git diff --check
rg -n '30 days|30 天|block-version:1\.4\.0-20260715( |-->)|Owner:|Assignee:' \
  SKILL.md README.md Usage.md references templates tests docs/proposal/v1.4.x/bug-management*.md
```

Classify every residual hit as current behavior, intentional historical evidence, or defect. Do not rewrite historical reports to remove valid 30-day evidence.

- [x] **Step 3: Present the Human Review Summary.**

Include:

- exact implementation file list;
- Bug identity/lifecycle/Requirement/Feature/90-day/archive summary;
- focused/full validation and severity counts;
- version/root revision result;
- scope drift and unresolved risks;
- explicit statement that no commit/push/tag/PR/merge/release/publish/CLI install occurred;
- exactly one recommended next action.

- [x] **Step 4: Stop before Submit / Integrate.**

Do not stage or commit merely because implementation passes. Wait for a new human instruction to enter Submit / Integrate. If requested, stage the exact reviewed set, run `git diff --cached --check`, present the staged summary and proposed commit message, then stop again for the final Commit Human Gate.

Suggested commit message only after that gate:

```text
feat(v1.4.0): 增加人类引导的 Bug 管理

- 增加独立 Bug Record、Report Origin 与 Status/Resolution 双轴生命周期
- 让 Bug 通过 Requirement 关系和 Human-gated Feature 路径完成修复
- 将 Feature ownership 默认窗口扩展为 90 天分层扫描并支持归档发现
- 同步 runtime、templates、root guidance、压力场景和全量验证证据
- 保持人员分派、Issue Tracker、Git 动作和版本升级不在默认范围
```

## Plan Self-Review

### Proposal Coverage

| Proposal area | Plan task |
|---|---|
| Concept Foundation / authority split | Tasks 1-2 |
| Bug ID / Origin / Evidence / relationships | Tasks 1 and 3-4 |
| Status + Resolution + reopen | Tasks 1, 2, and 5 |
| Requirement `0..N` and reconciliation | Task 4 |
| Feature-only repair | Tasks 4-5 |
| 90-day metadata / extended scan | Tasks 2, 3, and 8 |
| archived discovery / rehydrate boundary | Tasks 2, 6, and 8 |
| Human Gates / Auto Mode | Tasks 2, 5-6 |
| Branch / submit / helper boundaries | Task 6 |
| Project memory / INDEX ownership | Task 3 |
| Human docs / root navigation / version | Task 7 |
| twenty scenarios / RED-GREEN / full validation | Tasks 0, 8, and 9 |

No Proposal section is left without an implementation and validation owner.

### Internal Consistency

- Runtime remains version `1.4.0`; only root managed content advances to `1.4.0-20260715.1`.
- Bug Management remains inside Feature Follow-up and does not add a canonical stage.
- Bug Record owns coordination evidence; Requirement owns product meaning; Feature owns repair execution.
- Bug identity scan is unbounded; Feature ownership default is 90-day metadata plus evidence-driven deep/extended scan.
- Archived discovery is read-only; rehydrate is execution-gated.
- `Status` and `Resolution` enumerations are identical across proposal, reference, design, template, scenario, and focused test.
- Human permissions remain action-specific.

### Placeholder And Scope Scan

This plan contains exact paths, enumerations, assertions, commands, expected outputs, root revision, report paths, stop conditions, and a bounded commit proposal. Intentional template value slots are explicitly identified. It contains no unfinished implementation markers, Issue Tracker integration, personnel assignment, executable Bug database, version bump, real Git mutation, target-project artifact, worktree memory merge, or automatic submit authorization.

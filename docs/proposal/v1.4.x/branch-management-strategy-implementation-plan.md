# Human-Guided Branch Management Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use `superpowers:executing-plans` / `executing-plans` to execute this plan task-by-task. Do not dispatch subagents unless the human separately authorizes a bounded dispatch. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the approved optional Human-Guided Branch Management profile as a Human-gated Agent Loop runtime capability without adding a canonical stage, forcing Git Flow, changing the skill version, or performing real Git branch operations.

**Architecture:** Add one detailed published reference, `references/branch-management.md`, and route to it from the concise controller, runtime/design authority, affected stage procedures, project-memory ownership, templates, and human documentation. The profile remains evidence-driven and optional: Agent recommends it only when branch/version/customer-boundary risk is present, records adoption only after explicit human acceptance, stores durable strategy in `project.md`, stores volatile Current Branch Context in feature artifacts, and treats every create/merge/delete/push/tag/release/publish action as a separate existing Human Gate.

**Tech Stack:** Markdown skill sources and templates, Bash/Ruby contract assertions, existing Python 3.10+ root-guidance checker tests, repository full-validation method, Mermaid in `Usage.md`.

---

## Plan Status And Execution Boundary

- Plan status: human-approved; implementation, Tasks 0-8, and the Task 9-11 Human Review repairs are complete; Task 12 Human Review is pending.
- Design source: `docs/proposal/v1.4.x/branch-management-strategy.md` plus the immutable constraints in the human implementation request.
- Repository perspective: Agent Loop skill source maintainer; downstream behavior may be represented only in templates, docs, validation scenarios, and isolated test logic.
- Current branch observed while planning: `alpha/v1.4.0`.
- Current skill metadata observed while planning: `1.3.0`; this plan does not authorize changing it.
- Current dirty-work boundary observed while planning: only untracked `docs/proposal/v1.4.x/branch-management-strategy.md` existed before this plan was written.
- Never create repository-root `.agent-loop/` or real `release/*`, `customer/*`, `feature/*`, `bugfix/*`, or `hotfix/*` refs for this work.
- Do not commit, push, tag, create a PR, merge, release, publish, or modify remote state during plan execution.
- The Proposal entered implementation-in-progress after approval and now records implementation/full-validation completion pending Human Review.

## Stage Helper Resolution

| Field | Resolution |
|---|---|
| Stage | Plan Gate / Plan |
| Canonical candidate | `superpowers:writing-plans` — not exposed by the current runtime |
| Alias candidate | `writing-plans` — loaded completely from `/Users/shaodowyd/.codex/skills/writing-plans/SKILL.md` |
| Status | `loaded` |
| Fallback | `no` |
| Method used | exact file map, TDD-first tasks, exact commands and expected RED/GREEN, rollback and stop conditions, plan self-review |
| Agent Loop override | save to the human-selected proposal path; do not create `docs/superpowers/` or target-project artifacts; stop at Human Review |
| Persistence | response-local resolution captured here because this source repository has no target feature workspace |

## Non-Negotiable Invariants

1. `Branch Strategy Check` is an internal method used by existing stages, not a canonical stage and not a new message intent.
2. The recommended profile is optional. A clear existing project strategy wins; a simple single-branch project is not forced to migrate.
3. Recommendation is not adoption. Only explicit human acceptance may produce `Adoption Status: accepted`.
4. Recommendation or adoption never authorizes branch creation, switching, merge, deletion, push, tag, release, or publish.
5. Standard release aggregation branches use `release/vX.Y.Z`; customer release aggregation branches use `customer/<customer>/vX.Y.Z`.
6. Standard development branches use `feature|bugfix|hotfix/vX.Y.Z/<topic>`; customer development branches use `feature|bugfix|hotfix/<customer>-vX.Y.Z/<topic>`.
7. Release aggregation branches are retained. Temporary development branches may be deleted only after merge/abandon evidence and explicit Cleanup Gate confirmation.
8. A formally released version is `released / sealed`; repairs move to a new patch version and features move to a new human-confirmed version.
9. Customer customization never flows wholesale into `main` or a standard `release/*`; reusable value returns through a human product decision and normal standard Requirement / Feature or Bug Flow-back.
10. `project.md` stores only confirmed durable Branch Strategy plus a Current Work `Target Release Context` pointer. Feature `notes.md`, `plan.md`, and Submit / Integrate records store volatile branch facts.
11. No default `.agent-loop/branches/`, executable schema, branch database, Bug Management implementation, or worktree/branch memory-merge implementation is added.
12. The complete operating rules live in `references/branch-management.md`; `templates/root-AGENTS.md` gains exactly the one routing sentence required by the human, not the naming/state/gate tables.

## File Responsibility Map

### Create During Implementation

- `references/branch-management.md` — complete optional profile, evidence precedence, naming, state, adoption, lifecycle, isolation, gates, stage use, and fail-closed rules.
- `tests/validate-branch-management-strategy.sh` — focused cross-surface and negative-boundary contract.
- `docs/reports/agent-loop-v1.3.0-branch-management-red-baseline-2026-07-15.md` — pre-implementation baseline plus exact focused RED evidence; `v1.3.0` reflects unchanged active metadata.
- `docs/reports/agent-loop-v1.4.0-full-validation-2026-07-15.md` — fresh Chinese full-validation report for the version-aligned current workspace.

### Modify During Implementation

- `docs/proposal/v1.4.x/branch-management-strategy.md` — after plan approval, change proposal status to approved/implementation-in-progress; do not redesign its confirmed rules.
- `SKILL.md` — package-map route, concise required behavior, execution defaults, and fail-closed stops.
- `references/design.md` — core Branch Strategy / Branch Context / release and customer isolation model.
- `references/runtime.md` — internal Branch Strategy Check routing, recommendation/adoption contract, and blocking conditions without Stage Order changes.
- `references/concepts.md` — concise definitions for Branch Strategy, Current Branch Context, release aggregation, development branch, and sealed release.
- `references/artifact-rules.md` — durable-versus-volatile ownership and explicit no-branches-directory boundary.
- `references/project-memory-mode.md` — keep confirmed Branch Strategy in `project.md` in both simple and enterprise modes.
- `references/implementation-planning.md` — require accepted/current Branch Context evidence when an adopted strategy applies; planning does not authorize Git actions.
- `references/stage-guides.md` — Project Entry, Project Entry Scan, Technical Design/Plan, Execute, Drift, Project Memory Update, and Submit / Integrate checks.
- `references/workflow-checklists.md` — checklist equivalents for every affected stage and Human Gate.
- `references/submit-and-integrate.md` — source/target, target-release, sealed, customer-isolation, cleanup, and action-specific confirmation checks.
- `references/external-skill-adapters.md` — keep finishing/branch helpers subordinate to the adopted strategy and action-specific gates.
- `references/project-guidance.md` — one-sentence root routing rule, `project.md` durable fields, managed-block refresh implications.
- `references/human-review-summary.md` — Strategy Adoption, release/customer scope, integration/cleanup/release decision fields and explicit authorization boundary.
- `references/validation-scenarios.md` — the Proposal's twelve acceptance scenarios plus adversarial gate/optional-profile cases.
- `references/document-templates.md` — synchronize inline `project.md`, plan, and notes views with source templates.
- `templates/project.md` — optional confirmed Branch Strategy fields and Current Work Target Release Context pointer.
- `templates/notes.md` — volatile Current Branch Context and branch-aware Submit / Integrate evidence.
- `templates/plan.md` — Branch Context evidence pointer and explicit non-authorization note for the execution unit.
- `templates/root-AGENTS.md` — add exactly the approved routing sentence and refresh every managed-block revision to `1.3.0-20260715.1` without changing skill version.
- `README.md` — short optional-capability overview linking to Usage; no full rule duplication.
- `Usage.md` — human trigger examples and an exact copy of the Proposal's complete Mermaid branch logic diagram; keep the visible version label at `1.3.0`.
- `CHANGELOG.md` — add an `Unreleased` v1.4.0-development entry without creating a released `1.4.0` heading or changing version-bearing files.

### Root-Revision Regression Files To Update Together

- `tests/test_root_agents_blocks.py`
- `tests/validate-root-agents-block-checker.sh`
- `tests/validate-root-agents-block-refresh.sh`
- `tests/validate-v1.2.4-root-stage-coverage.sh`
- `tests/validate-project-local-skills.sh`
- `tests/validate-requirement-lifecycle-backlog.sh`

These files contain the exact current managed-block revision. Change only the revision expectations needed by the root template update; do not refactor their unrelated contracts.

### Review-Only Unless A Contradiction Is Found

- `plugin.json` — verify it stays `1.3.0`; no edit expected.
- `agents/openai.yaml` — metadata/YAML validation only; no branch capability fields expected.
- `examples/` — no example mutation expected because downstream behavior is already covered by templates and validation scenarios.
- Root `AGENTS.md` — maintainer rules remain unchanged; do not copy downstream branch strategy into this repository's maintenance policy.

## Coordinated Synchronization Order

```text
existing baseline
-> focused RED contract
-> design.md + runtime.md authority
-> branch-management.md + concise SKILL/concepts routing
-> stage/reference/checklist/gate integration
-> artifact ownership + project/notes/plan templates
-> root one-sentence reminder + managed-block revision tests
-> Usage complete Mermaid + README + Unreleased changelog
-> validation scenarios + focused GREEN
-> all tests + six-domain semantic audit + mechanical checks
-> Chinese report + Human Review Summary
```

Do not move Usage or templates ahead of runtime/design authority: they are derived surfaces and must not temporarily become the only source of a rule.

## Task 0: Approve Implementation State And Capture A Clean Baseline

**Files:**

- Modify: `docs/proposal/v1.4.x/branch-management-strategy.md`
- Create after the RED run: `docs/reports/agent-loop-v1.3.0-branch-management-red-baseline-2026-07-15.md`
- Read: `AGENTS.md`, `SKILL.md`, `references/runtime.md`, `references/design.md`, `docs/maintenance/full-validation-method.md`

- [x] **Step 1: Recheck execution authority and workspace boundary.**

Run:

```bash
git branch --show-current
git status --short --branch
git rev-parse HEAD
git for-each-ref --format='%(refname) %(objectname)' | shasum -a 256
```

Expected before implementation:

```text
branch: alpha/v1.4.0
HEAD: unchanged from the reviewed plan state
dirty scope: proposal plus implementation plan only
```

If any unrelated path is dirty, classify overlap before editing. Stop when it overlaps an implementation file or cannot be safely excluded.

- [x] **Step 2: Update only the Proposal status after this plan is explicitly accepted.**

Replace the current status line with:

```text
状态：Proposal 与核心设计已由人类确认；Implementation Plan 已批准，实施中
```

Do not alter branch names, sealed semantics, customer isolation, gates, phases, or acceptance scenarios in the Proposal.

- [x] **Step 3: Run the existing pre-change regression baseline before adding the new test.**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
for test_file in tests/*.sh; do bash "$test_file"; done
```

Expected baseline:

```text
existing Python suite: PASS
existing tests/*.sh: 34/34 PASS
```

If an existing test fails, preserve the output and stop before adding Branch Management behavior; do not absorb unrelated repairs into this feature.

## Task 1: Add And Preserve The Focused RED Contract

**Files:**

- Create: `tests/validate-branch-management-strategy.sh`
- Create: `docs/reports/agent-loop-v1.3.0-branch-management-red-baseline-2026-07-15.md`

- [x] **Step 1: Add the complete focused contract before production/reference edits.**

Create `tests/validate-branch-management-strategy.sh` with this structure and contract set:

```bash
#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

assert_file_exists() {
  [ -f "$root/$1" ] || fail "missing required file: $1"
}

assert_contains() {
  local file=$1
  local text=$2
  grep -Fq -- "$text" "$root/$file" || fail "$file missing branch-management contract: $text"
}

assert_not_contains() {
  local file=$1
  local text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    fail "$file contains forbidden root/scope detail: $text"
  fi
}

reference=references/branch-management.md
assert_file_exists "$reference"

for file in SKILL.md references/design.md references/runtime.md references/stage-guides.md references/workflow-checklists.md; do
  assert_contains "$file" "Branch Strategy Check"
done

for text in \
  'release/v<semver>' \
  'customer/<customer>/v<semver>' \
  '<work-type>/v<semver>/<topic>' \
  '<work-type>/<customer>-v<semver>/<topic>' \
  'released / sealed' \
  'Strategy Adoption Gate' \
  'Customer Isolation' \
  'Cleanup Gate'; do
  assert_contains "$reference" "$text"
done

assert_contains "$reference" 'feature | bugfix | hotfix'
assert_contains "$reference" 'existing-project | human-guided-release | not-applicable'
assert_contains "$reference" 'accepted | declined | not-needed'
assert_contains "$reference" 'Recommendation and adoption do not authorize branch creation, switching, merge, deletion, push, tag, release, or publish.'
assert_contains "$reference" 'does not implement Bug Management'
assert_contains "$reference" 'does not implement worktree / branch memory merge'
assert_contains "$reference" 'Do not create a default `.agent-loop/branches/` directory.'

assert_contains references/submit-and-integrate.md 'Target Release Context'
assert_contains references/submit-and-integrate.md 'Source Branch'
assert_contains references/submit-and-integrate.md 'Target Branch'
assert_contains references/submit-and-integrate.md 'released / sealed'
assert_contains references/submit-and-integrate.md 'Customer Isolation'

for field in \
  'Adoption Status:' \
  'Profile:' \
  'Decline Reason:' \
  'Main Branch:' \
  'Standard Release Pattern:' \
  'Customer Release Pattern:' \
  'Development Pattern:' \
  'Release Immutability:' \
  'Customer Isolation:' \
  'Deletion Policy:' \
  'Human Confirmed:' \
  'Evidence:'; do
  assert_contains templates/project.md "$field"
  assert_contains references/document-templates.md "$field"
done

assert_contains templates/project.md 'Target Release Context:'
assert_contains templates/notes.md '## Current Branch Context'
assert_contains templates/notes.md 'Branch Class:'
assert_contains templates/notes.md 'Target Branch:'
assert_contains templates/notes.md 'Lifecycle State:'
assert_contains templates/plan.md 'Branch Context Evidence:'

reminder='When existing branch rules are confused, the target version is unclear, or customer isolation is at risk, load `references/branch-management.md`, recommend one optional strategy, and adopt it only after explicit human acceptance.'
count=$(grep -Fxc -- "$reminder" "$root/templates/root-AGENTS.md" || true)
[ "$count" -eq 1 ] || fail "root AGENTS must contain the exact branch-management reminder once; found $count"

for forbidden in \
  'release/v<semver>' \
  'customer/<customer>/v<semver>' \
  'Adoption Status:' \
  'released / sealed' \
  'Strategy Adoption Gate'; do
  assert_not_contains templates/root-AGENTS.md "$forbidden"
done

assert_contains references/human-review-summary.md '### Branch Strategy And Action Review'
assert_contains references/human-review-summary.md '| Requested Authorization |'
assert_contains references/human-review-summary.md '| Explicitly Not Authorized |'
assert_contains references/validation-scenarios.md 'Human-Guided Branch Management'
assert_contains references/validation-scenarios.md 'Existing Clear Strategy Is Not Forced To Migrate'
assert_contains references/validation-scenarios.md 'Sealed Release Rejects Same-Version Repair'
assert_contains references/validation-scenarios.md 'Customer Branch Cannot Flow Wholesale Into Standard Product'
assert_contains README.md 'Human-Guided Branch Management'
assert_contains Usage.md '### 我想让 Agent 推荐分支管理方式'
assert_contains CHANGELOG.md 'Human-Guided Branch Management'

ruby - "$root/references/runtime.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
section = content[/## Stage Order\n(.*?)(?=\n## |\z)/m, 1]
abort 'FAIL: runtime Stage Order section missing' unless section
forbidden = ['Branch Strategy Check', 'Strategy Adoption Gate', 'Release Scope Gate', 'Customer Scope Gate']
found = forbidden.select { |name| section.lines.any? { |line| line.strip == name } }
abort "FAIL: branch management added canonical stages: #{found.join(', ')}" unless found.empty?
RUBY

ruby - "$root/docs/proposal/v1.4.x/branch-management-strategy.md" "$root/Usage.md" <<'RUBY'
proposal = File.read(ARGV.fetch(0))
usage = File.read(ARGV.fetch(1))
proposal_graph = proposal[/## 完整分支逻辑图.*?```mermaid\n(.*?)```/m, 1]
usage_graph = usage[/### 我想让 Agent 推荐分支管理方式.*?```mermaid\n(.*?)```/m, 1]
abort 'FAIL: proposal branch Mermaid graph missing' unless proposal_graph
abort 'FAIL: Usage branch Mermaid graph missing' unless usage_graph
abort 'FAIL: Usage branch Mermaid graph drifted from Proposal' unless usage_graph == proposal_graph
RUBY

[ ! -d "$root/.agent-loop" ] || fail 'skill source repository must not contain target-project .agent-loop artifacts'

printf 'PASS: Human-Guided Branch Management optional profile, gates, artifacts, diagram, and scope contract is complete\n'
```

- [x] **Step 2: Run the new contract alone and confirm RED for the intended missing capability.**

Run:

```bash
bash tests/validate-branch-management-strategy.sh
```

Expected RED:

```text
FAIL: missing required file: references/branch-management.md
```

The RED is invalid if it comes from shell syntax, a missing Proposal, a path typo, or unrelated baseline failure.

- [x] **Step 3: Save exact baseline evidence.**

The RED report must include:

- branch, HEAD, current skill metadata, and dirty-scope boundary;
- existing Python and 34-shell-test baseline results;
- focused command, exit status, and exact first failing assertion;
- why the failure proves the current runtime lacks the approved Branch Management contract;
- explicit statement that no runtime/reference/template implementation had been written before RED;
- explicit statement that no project branch/tag/remote Git refs or target `.agent-loop/` artifacts were created.

## Task 2: Implement Published Authority And The Detailed Reference

**Files:**

- Create: `references/branch-management.md`
- Modify: `SKILL.md`
- Modify: `references/design.md`
- Modify: `references/runtime.md`
- Modify: `references/concepts.md`

- [x] **Step 1: Write `references/branch-management.md` as the complete operating contract.**

Use these sections in this order:

```text
# Human-Guided Branch Management
## Purpose And Optionality
## Evidence And Fact Precedence
## Branch Strategy Check
## Recommendation And Strategy Adoption Gate
## Branch Classes And Naming Grammar
## Target Release Context
## Release Aggregation Lifecycle
## Development Branch Lifecycle
## Standard Release Flow
## Customer Release Flow And Isolation
## Sealed Release And Later Maintenance
## Existing Strategy And Simple-Project Paths
## Current Branch Context
## Artifact Ownership
## Human Gates And Authorization Boundaries
## Stage Integration
## Fail-Closed Conditions
## Scope Exclusions
```

The reference must encode all twelve Non-Negotiable Invariants above and use this adoption rule verbatim:

```text
Recommendation and adoption do not authorize branch creation, switching, merge, deletion, push, tag, release, or publish.
```

It must distinguish evidence of what exists from authority about what should happen:

```text
human-confirmed native policy
-> accepted project.md Branch Strategy snapshot
-> local/remote Git reality
-> Agent inference from branch names
```

When recommendation is needed, require one observed fact/risk, one recommended profile/impact summary, and exactly one blocking question. A pending recommendation remains response-local or feature evidence and must not become `accepted` project memory.

- [x] **Step 2: Update `references/design.md` and `references/runtime.md` together.**

`design.md` must define the optional model and immutable product/customer boundaries. `runtime.md` must define when the existing stages run `Branch Strategy Check`, how existing/native strategies win, when adoption is recorded, and what blocks Plan/Submit/Release.

Add no Stage Order row. Add no message intent. Keep the canonical stage list byte-for-byte unchanged unless a pre-existing contradiction is discovered; that discovery is a stop condition rather than permission to redesign.

- [x] **Step 3: Keep `SKILL.md` concise.**

Add:

- one package-map entry for `references/branch-management.md`;
- a concise Required Runtime Behavior route for Project Entry, target-release ambiguity, customer-boundary risk, and Submit / Integrate;
- concise execution defaults for accepted durable strategy versus volatile feature context;
- stop rules for unknown branch class/target, sealed target, customer contamination, native-policy conflict, and unconfirmed Git action.

Do not copy the naming tables, state machines, Mermaid graph, or full gate matrix into `SKILL.md`.

- [x] **Step 4: Add concise terms to `references/concepts.md`.**

Define `Branch Strategy`, `Current Branch Context`, `Release Aggregation Branch`, `Development Branch`, `Target Release Context`, and `Sealed Release`. State that branch state does not replace Requirement, Feature, Task, ADR, verification, or lifecycle authority.

- [x] **Step 5: Run the focused contract to measure the next RED layer.**

Run:

```bash
bash tests/validate-branch-management-strategy.sh
```

Expected intermediate result: authority/reference assertions pass, then the first missing stage/template/human-doc assertion fails. Do not weaken the test to get past that failure.

## Task 3: Integrate Existing Stages, Gates, Planning, And Submit Rules

**Files:**

- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/implementation-planning.md`
- Modify: `references/submit-and-integrate.md`
- Modify: `references/external-skill-adapters.md`
- Modify: `references/human-review-summary.md`

- [x] **Step 1: Add Branch Strategy Check to existing stage entry points without creating a stage.**

Coordinate these behaviors:

| Existing surface | Required behavior |
|---|---|
| Project Entry / Project Entry Scan | inspect native policy and Git reality; recommend only on named risk signals; do not write accepted strategy before Human Gate |
| Technical Design / Plan Gate | when a strategy is accepted, resolve Target Release Context and unique Target Branch from evidence; if unclear, ask one blocker and stop |
| Execute Task / Story | recheck that the recorded context is current; do not create/switch branches as an implied execution step |
| Drift Check | compare accepted strategy, Current Branch Context, and Git reality; human-review durable strategy changes |
| Project Memory Update | write accepted/declined/not-needed durable strategy only after confirmation; keep volatile branch state out of long-term memory |
| Submit / Integrate | verify Source Branch, Branch Class, Target Release Context, unique Target Branch, sealed status, customer isolation, unrelated work, and exact requested action |

- [x] **Step 2: Extend construction-plan rules.**

When an adopted strategy applies, require the active plan to cite:

```text
Branch Strategy status/profile
Target Release Context
Target Branch
Current Branch Context evidence path
sealed/customer-isolation result
Git actions authorized by this plan: none
```

A declined/not-needed profile uses the confirmed existing strategy or lightweight path. An unresolved recommendation blocks only work that depends on the unresolved target/boundary; it does not force unrelated simple work into the profile.

- [x] **Step 3: Harden Submit / Integrate with action-specific authorization.**

Preserve the existing two-stage submit confirmation. The post-inspection summary must distinguish:

```text
strategy adoption decision
long-lived branch creation decision
development branch creation/switch decision
target merge/PR/commit decision
temporary branch cleanup decision
tag/release/push/publish decision
customer baseline upgrade decision
```

Only the exact action explicitly confirmed is authorized. A strategy-adoption answer cannot be reused as permission for any later mutation.

- [x] **Step 4: Add Branch Strategy And Action Review to `references/human-review-summary.md`.**

Use one table pattern with these rows:

```text
Observed Policy / Git Evidence
Adoption Status And Profile
Source Branch / Branch Class
Target Release Context / Target Branch
Sealed Check
Customer Isolation Check
Verification / Review / Drift
Requested Authorization
Explicitly Not Authorized
Remaining Risk / Blocker
Human Decision
```

The summary supports Strategy Adoption, Release Scope, Customer Scope, Long-Lived Branch, Target Branch, Integration, Cleanup, Release, and Upgrade gates without collapsing them into one reusable approval.

- [x] **Step 5: Keep external branch helpers subordinate.**

Update the Submit adapter so a finishing/branch helper may inspect and recommend branch hygiene, but cannot mark a strategy accepted or perform/create/merge/delete/push/tag/release/publish anything without the matching Agent Loop summary and explicit Human Gate.

- [x] **Step 6: Rerun focused RED.**

Expected intermediate result: stage/gate assertions pass; template/root/Usage/scenario assertions remain RED.

## Task 4: Implement Artifact Ownership And Templates

**Files:**

- Modify: `references/artifact-rules.md`
- Modify: `references/project-memory-mode.md`
- Modify: `references/project-guidance.md`
- Modify: `references/document-templates.md`
- Modify: `templates/project.md`
- Modify: `templates/notes.md`
- Modify: `templates/plan.md`

- [x] **Step 1: Add the optional durable Branch Strategy block to `templates/project.md`.**

Use exactly these fields:

```md
## Branch Strategy

Adoption Status: accepted | declined | not-needed
Profile: existing-project | human-guided-release | not-applicable
Decline Reason: required when Adoption Status is declined | not-applicable
Main Branch:
Standard Release Pattern:
Customer Release Pattern:
Development Pattern:
Release Immutability:
Customer Isolation:
Deletion Policy:
Human Confirmed:
Evidence:
```

Instructions around the block must say:

- an unanswered recommendation is not written as `accepted`;
- `declined` records the decision/reason without copying the proposed profile as current policy;
- `not-needed` records why a simple/existing project remains lightweight;
- changing durable strategy requires Drift Check plus Human Gate.

Add this pointer to `## Current Work`:

```text
Target Release Context: <standard-or-customer-release pointer> | none
```

Do not add current branch name, branch lifecycle, or a branch inventory to `project.md`.

- [x] **Step 2: Add volatile Current Branch Context to feature templates.**

`templates/notes.md` owns the complete volatile record:

```text
Branch Class
Work Type
Target Kind
Target Version
Customer Slug
Topic
Source Branch
Target Branch
Lifecycle State
Source Evidence
Last Checked
Human Decision
```

`templates/plan.md` cites the `notes.md` evidence and repeats only Target Release Context, Target Branch, boundary checks, and `Git actions authorized by this plan: none`. The Submit / Integrate record adds Source Branch, Target Branch, sealed/customer checks, requested action, authorization evidence, and cleanup status.

- [x] **Step 3: Synchronize ownership references and inline template copies.**

`artifact-rules.md`, `project-memory-mode.md`, `project-guidance.md`, and `document-templates.md` must agree that:

- confirmed strategy is durable project memory in both simple and enterprise mode;
- current branch state belongs to feature artifacts;
- `project.md` keeps only the current Target Release Context pointer;
- no `.agent-loop/branches/` directory is created;
- native policy and human confirmation outrank Git-name inference.

- [x] **Step 4: Rerun focused RED.**

Expected intermediate result: artifact/template assertions pass; root reminder, Mermaid/human docs, changelog, or scenarios remain RED.

## Task 5: Update Root Guidance And Human Documentation

**Files:**

- Modify: `templates/root-AGENTS.md`
- Modify: `references/project-guidance.md`
- Modify: `tests/test_root_agents_blocks.py`
- Modify: `tests/validate-root-agents-block-checker.sh`
- Modify: `tests/validate-root-agents-block-refresh.sh`
- Modify: `tests/validate-v1.2.4-root-stage-coverage.sh`
- Modify: `tests/validate-project-local-skills.sh`
- Modify: `tests/validate-requirement-lifecycle-backlog.sh`
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`

- [x] **Step 1: Add only the approved root reminder.**

Add this exact standalone sentence once inside the existing managed `ownership` block:

```text
When existing branch rules are confused, the target version is unclear, or customer isolation is at risk, load `references/branch-management.md`, recommend one optional strategy, and adopt it only after explicit human acceptance.
```

Do not add a Stage Map row because Branch Strategy Check is not a stage. Do not add naming, lifecycle, sealed, customer-isolation, or gate tables to root guidance.

- [x] **Step 2: Refresh managed-block revision coherently.**

Change every template managed-block marker and every exact current-revision regression expectation from:

```text
1.3.0-20260714.1
```

to:

```text
1.3.0-20260715.1
```

Keep the skill version `1.3.0`; this is a same-version content revision, not a version bump. Update only exact-revision fixtures/assertions and leave unrelated root-stage contracts unchanged.

- [x] **Step 3: Add concise README guidance.**

Explain that Agent Loop can recommend an optional Human-Guided Branch Management profile for unclear release/customer boundaries, that existing clear strategies remain authoritative, and that all Git mutations retain separate Human Gates. Link to the Usage section; do not duplicate the diagram or full grammar.

- [x] **Step 4: Add the complete human-facing Usage section.**

Create `### 我想让 Agent 推荐分支管理方式` with:

- human trigger examples for branch confusion, formal release planning, customer release isolation, and existing-strategy review;
- the recommendation/adoption distinction;
- the standard/customer naming summary;
- an exact copy of the Proposal's Mermaid block under `## 完整分支逻辑图`;
- a clear note that dashed arrows are lifecycle/forbidden-direction explanations and no Git action is automatic;
- sealed release maintenance examples;
- simple/existing-strategy non-migration examples.

Keep `**版本：** 1.3.0` unchanged.

- [x] **Step 5: Add an Unreleased changelog entry without version synchronization.**

Insert above the released `1.3.0` section:

```md
## Unreleased — v1.4.0 Development

### Human-Guided Branch Management
```

Record the optional profile, Human Gates, naming/lifecycle/isolation, project-memory ownership, root one-line routing, focused/full validation, and explicit no-real-Git-side-effect boundary. Do not change `SKILL.md` Version, `plugin.json`, README current-version label, Usage version label, or create a dated released `1.4.0` section.

- [x] **Step 6: Run root and human-doc focused regressions.**

Run:

```bash
python3 -m unittest tests/test_root_agents_blocks.py -v
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-root-agents-block-refresh.sh
bash tests/validate-v1.2.4-root-stage-coverage.sh
bash tests/validate-project-local-skills.sh
bash tests/validate-requirement-lifecycle-backlog.sh
bash tests/validate-human-help-version-docs.sh
```

Expected: all PASS with `1.3.0-20260715.1`, unchanged active version metadata, and unchanged canonical Stage Map coverage.

## Task 6: Add Pressure Scenarios And Reach Focused GREEN

**Files:**

- Modify: `references/validation-scenarios.md`
- Modify: `tests/validate-branch-management-strategy.sh` only if the implementation reveals a genuine missing invariant; do not weaken existing assertions.

- [x] **Step 1: Add one grouped Human-Guided Branch Management scenario section.**

Cover these cases with prompt, expected evidence, expected recommendation, required Human Gate, forbidden action, and next stage:

1. standard version aggregates multiple features;
2. one-work-item version is not artificially split;
3. customer feature may target only its matching customer release;
4. two customer slugs with the same topic remain unambiguous;
5. sealed `v1.0.0` repair routes to human-confirmed patch version;
6. customer baseline upgrade is asked, never automatic;
7. clear trunk-based native strategy is not forced to migrate;
8. `feature/user-login` reports missing Target Release Context and asks one blocker without renaming;
9. merged temporary branch cleanup still requires confirmation;
10. customer capability generalization returns through product/requirement/feature or Bug Flow-back instead of wholesale reverse merge;
11. single-main simple project records `not-needed` or follows existing policy without manufacturing release branches;
12. future Memory Merge consumes Branch Context but is not implemented;
13. strategy adoption confirmation attempts to rationalize branch creation and is rejected;
14. external finishing helper attempts merge/delete/push and is rejected;
15. Git reality conflicts with accepted/native policy and routes to drift plus one minimal human decision.

- [x] **Step 2: Run the complete focused contract.**

Run:

```bash
bash tests/validate-branch-management-strategy.sh
```

Expected GREEN:

```text
PASS: Human-Guided Branch Management optional profile, gates, artifacts, diagram, and scope contract is complete
```

- [x] **Step 3: Run the affected regression set together.**

Run:

```bash
bash tests/validate-branch-management-strategy.sh
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-root-agents-block-refresh.sh
bash tests/validate-v1.2.4-root-stage-coverage.sh
bash tests/validate-project-local-skills.sh
bash tests/validate-requirement-lifecycle-backlog.sh
bash tests/validate-human-help-version-docs.sh
bash tests/validate-mandatory-helper-routing.sh
```

Expected: 8/8 PASS. If the focused test passes only after removing a Proposal invariant, restore the invariant and fix the implementation instead.

## Task 7: Run Full Validation And Produce Fresh Chinese Evidence

**Files:**

- Create: `docs/reports/agent-loop-v1.4.0-full-validation-2026-07-15.md`
- Review: every file in the implementation file map

- [x] **Step 1: Run the full executable regression suite.**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
for test_file in tests/*.sh; do bash "$test_file"; done
```

Expected after adding the focused contract:

```text
Python suite: all discovered tests PASS
tests/*.sh: 35/35 PASS
```

Recount the live `tests/*.sh` inventory in the report; do not copy the planned count if the inventory legitimately changes during implementation.

- [x] **Step 2: Run the six-domain semantic audit required by `docs/maintenance/full-validation-method.md`.**

In addition to the method's representative scenarios, explicitly audit:

- optional recommendation versus forced migration;
- recommendation versus accepted durable policy;
- accepted policy versus Git-action authorization;
- standard/customer branch classification and unique target;
- sealed version behavior;
- customer isolation and safe generalization route;
- durable `project.md` versus volatile feature context;
- native policy versus Git-reality drift;
- root one-line routing versus detailed-reference ownership;
- no canonical stage, no `.agent-loop/branches/`, no Bug Management, no Memory Merge.

- [x] **Step 3: Run all required mechanical checks.**

Run:

```bash
ruby -e 'require "yaml"; %w[SKILL.md agents/openai.yaml].each { |file| YAML.load_file(file) }'
ruby -rjson -e 'JSON.parse(File.read("plugin.json"))'
python3 -m compileall -q scripts tests
find . -name '*.sh' -type f -not -path './.git/*' -print0 | xargs -0 -n1 bash -n
find . -name '*.rb' -type f -not -path './.git/*' -print0 | xargs -0 -n1 ruby -c
python3 - <<'PY'
from pathlib import Path
import re

errors = []
for path in sorted(Path('.').rglob('*.md')):
    if '.git' in path.parts:
        continue
    stack = []
    text = path.read_text(encoding='utf-8')
    for number, line in enumerate(text.splitlines(), start=1):
        match = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line)
        if not match:
            continue
        token, tail = match.groups()
        marker = token[0]
        length = len(token)
        if stack and stack[-1][0] == marker and length >= stack[-1][1] and not tail.strip():
            stack.pop()
        else:
            stack.append((marker, length, number))
    if stack:
        errors.append(f'{path}: unclosed fences from lines {[item[2] for item in stack]}')
if errors:
    raise SystemExit('\n'.join(errors))
print('PASS: Markdown fences balanced')
PY
git diff --check
```

Also run:

```bash
test ! -d .agent-loop
git branch --show-current
git rev-parse HEAD
git status --short --branch
git for-each-ref --format='%(refname) %(objectname)' refs/heads refs/remotes refs/tags | shasum -a 256
```

Expected: no target-project workspace; branch remains `alpha/v1.4.0`; HEAD and ref hash match Task 0; only intended source/proposal/report/test files are dirty; no commit exists.

- [x] **Step 4: Write the Chinese full-validation report from fresh output.**

The report must include:

- date, branch, active metadata `1.3.0`, target development line `v1.4.0`, HEAD, and current-worktree audit boundary;
- RED baseline and focused GREEN evidence;
- live Python and shell test counts;
- six-domain scores, severity inventory, and overall grade;
- the fifteen branch-specific pressure scenarios and results;
- root Stage Map/no-new-stage result;
- complete Mermaid equality result;
- optionality/adoption/action-authorization separation;
- version unchanged and Unreleased changelog treatment;
- Git-ref hash/no-side-effect evidence;
- remaining risks and any downgraded/declined findings;
- explicit statement that commit/push/tag/PR/merge/release/publish were not authorized or executed.

Do not reuse a prior report score or claim Windows evidence for this docs-only feature unless a real current run exists and is cited.

## Task 8: Stop At Human Review

**Files:**

- Review: implementation diff and both new reports
- Write: no additional file unless review exposes a defect

- [x] **Step 1: Perform plan/spec conformance review.**

Check every Proposal completion criterion and every invariant in this plan against exact file/line evidence. Confirm no accepted rule exists only in a template, Usage, Proposal, or test.

- [x] **Step 2: Perform scope-drift review.**

Confirm:

```text
no canonical stage
no default branch artifact/directory
no project branch/tag/remote Git ref mutation
no Bug Management implementation
no worktree/branch memory merge
no executable YAML/JSON schema
no skill-version change
no unrelated dirty-file mutation
no submit/release action
```

- [x] **Step 3: Present Human Review Summary and stop.**

The handoff must include:

- actual modified/created files;
- baseline, RED, GREEN, affected, and full-suite evidence;
- Chinese report link;
- Proposal completion-criteria matrix;
- remaining risks and design drift;
- root reminder/full-reference ownership check;
- unchanged version and unchanged project branch/tag/remote-ref evidence;
- explicit `commit: not run`, `push: not run`.

The only recommended next stage is Human Review of the implementation. Do not enter Submit / Integrate without a new human instruction after that review.

## Rollback Strategy

1. No implementation change may be committed during these tasks, so rollback is workspace-local.
2. Reverse only implementation-owned hunks with `apply_patch`; never use `git reset --hard`, `git checkout --`, or another destructive whole-file restore.
3. Preserve the human's Proposal file and any unrelated changes byte-for-byte. If the human edits a newly created file during execution, stop before deleting or replacing it.
4. Treat `design.md`, `runtime.md`, `SKILL.md`, detailed reference, stage/checklist rules, templates, root revision, human docs, and focused tests as one coordinated unit. Do not leave a partial state that advertises the profile without its gates or ownership rules.
5. If the root managed-block revision must be rolled back, roll back the template markers and all exact-revision tests together.
6. If focused GREEN or full validation fails, keep RED/failure evidence, mark the implementation blocked in the Human Review Summary, and do not claim completion.
7. No rollback procedure may delete or change Git branches/tags because implementation must not create them.

## Stop Conditions

Stop immediately and report evidence plus one recommended next action when:

- Proposal and current runtime/design have a conflict that cannot be resolved without changing the approved design;
- a fix would change the confirmed naming grammar, sealed rule, customer-isolation rule, or optional-adoption model;
- scope would expand into Bug Management or worktree/branch memory merge;
- a new artifact/directory, executable schema, parser service, dependency, or Git-host configuration is required beyond this plan;
- changing the skill version, version-bearing metadata, or released changelog heading becomes necessary;
- unrelated dirty work overlaps an implementation file or cannot be safely excluded;
- an existing baseline test fails before the RED test is added;
- focused tests, root-guidance regression, full suite, semantic audit, fence/YAML/JSON/Shell/Ruby checks, or `git diff --check` cannot reliably pass;
- the complete Usage Mermaid graph cannot remain synchronized with the approved Proposal;
- implementation would require real branch create/switch/merge/delete/push/tag/release/publish operations;
- a branch-helper instruction conflicts with Agent Loop Human Gates;
- human review requests a material design change rather than an implementation correction.

## Plan Self-Review

### Proposal Coverage

- All Proposal Phase 1-4 implementation surfaces are mapped to Tasks 1-7.
- All twelve acceptance scenarios are included, plus gate-rationalization and drift adversarial cases.
- The exact root reminder and exact Usage Mermaid ownership are mechanically checked.
- Durable and volatile artifact ownership is explicit; no default branch directory is introduced.
- Bug Management and Memory Merge remain inputs/consumers only, not implementation scope.

### Internal Consistency

- Current active metadata stays `1.3.0`; the `alpha/v1.4.0` branch is treated as a development target, and changelog content stays under Unreleased.
- Root block revision uses `1.3.0-20260715.1`, matching the unchanged skill metadata and same-version content-revision rule.
- Branch naming placeholders use the approved standard/customer forms consistently.
- Recommendation, adoption, and Git-action authorization are separate at runtime, stage, template, review, scenario, and test surfaces.

### Placeholder And Scope Scan

The plan contains concrete file paths, expected test output, exact template fields, exact commands, and explicit stop/rollback behavior. It does not authorize implementation before Human Review, subagent dispatch, version synchronization, or Git submission.

## Human Review Repair Addendum — 2026-07-15

The human approved repair of the four review findings while explicitly declining a new rule that would force a branch-strategy recommendation before every branch creation. The existing explicit-human-question trigger remains sufficient; ordinary branch creation does not become a new recommendation trigger.

### Task 9: Add Focused RED Coverage For Review Findings

**Files:**

- Modify: `tests/validate-branch-management-strategy.sh`
- Update after GREEN: `docs/reports/agent-loop-v1.3.0-branch-management-red-baseline-2026-07-15.md`

- [x] Assert that the `SKILL.md` and `references/runtime.md` Auto Mode sections explicitly stop before branch create, switch, delete, push, and tag actions.
- [x] Assert that recommendation/adoption boundaries include switching and that one `Branch Action Gate` owns exact create/switch authorization for development branches.
- [x] Assert that the global `SKILL.md` branch Stop rule is scoped to an applicable adopted/versioned/customer branch context and preserves the simple `not-needed` path.
- [x] Assert that `declined` uses `Profile: not-applicable` plus a decline reason, while `accepted` and `not-needed` retain valid profile semantics.
- [x] Assert that the canonical English root template contains one English branch-management router and no hard-coded Chinese managed reminder.
- [x] Run `bash tests/validate-branch-management-strategy.sh` before production edits and preserve the expected contract failures as RED evidence.

### Task 10: Repair Runtime, Design, Memory, Gate, And Guidance Contracts

**Files:**

- Modify: `SKILL.md`
- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Modify: `references/branch-management.md`
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/human-review-summary.md`
- Modify: `references/document-templates.md`
- Modify: `templates/project.md`
- Modify: `templates/root-AGENTS.md`
- Modify: affected root managed-block revision tests
- Modify: `docs/proposal/v1.4.x/branch-management-strategy.md`

- [x] Scope branch-specific global Stop behavior to an adopted strategy or versioned/customer delivery context; `not-needed` and non-applicable simple work continue through the normal stage.
- [x] Add `Branch Action Gate` for an exact development-branch create/switch action without changing Strategy Adoption, Target Branch, Integration, Cleanup, or Release Gate ownership.
- [x] Add create/switch/delete/push/tag to Auto Mode stop wording and keep all Git mutation lists consistent.
- [x] Model `declined` as `Profile: not-applicable` with `Decline Reason`; do not record a rejected recommendation as current policy.
- [x] Replace the hard-coded Chinese root reminder with an English canonical one-line router; project-language adaptation remains governed by `references/project-guidance.md`.
- [x] Advance every root managed block to the repository's current uniform revision `block-version:1.3.0-20260715.1`; the checker still compares each section independently, while the template keeps one same-day refresh revision.
- [x] Do not add a mandatory recommendation before every branch create/switch request.

### Task 11: Verify GREEN And Refresh Evidence

**Files:**

- Modify: `docs/reports/agent-loop-v1.4.0-full-validation-2026-07-15.md`
- Modify: `docs/reports/agent-loop-v1.3.0-branch-management-red-baseline-2026-07-15.md`

- [x] Run `bash tests/validate-branch-management-strategy.sh` and confirm the new review contract is GREEN.
- [x] Run all Python tests and every `tests/*.sh`; record live counts rather than copying the earlier report.
- [x] Run YAML, JSON, Python compile, Shell/Ruby syntax, Markdown fence, tracked diff, and untracked whitespace checks.
- [x] Re-run the six-domain semantic audit, including the simple-project path, declined memory state, exact branch-action authorization, and project-language root guidance.
- [x] Refresh both Chinese reports so RED history, current GREEN evidence, scores, severity counts, and authorization state describe the repaired workspace.

### Task 12: Return To Human Review

- [x] Confirm the naming grammar, Mermaid graph, optional recommendation trigger, sealed-release behavior, customer isolation, Bug Management boundary, and Memory Merge boundary did not drift.
- [x] Confirm no branch, worktree, commit, push, tag, PR, merge, release, or publish action occurred during implementation and repair.
- [x] Present the repaired implementation and fresh evidence for Human Review; the human subsequently authorized the version bump and requested entry into Submit / Integrate.

## Version Bump And Submit Addendum — 2026-07-15

The earlier `1.3.0` metadata and no-submit boundaries above record the implementation-time authorization state. They remain historical evidence, but the human has now explicitly approved aligning this completed capability to version `1.4.0` and requested a commit.

### Task 13: Align Version-Bearing Surfaces

- [x] Update `SKILL.md`, `plugin.json`, `README.md`, and `Usage.md` to `1.4.0`.
- [x] Replace the Unreleased development heading with `## 1.4.0 — 2026-07-15` in `CHANGELOG.md`.
- [x] Advance every root managed block and current regression expectation to `block-version:1.4.0-20260715`.
- [x] Preserve `docs/reports/agent-loop-v1.3.0-branch-management-red-baseline-2026-07-15.md` as the actual pre-version-bump RED record.
- [x] Rename the current full-validation report to `docs/reports/agent-loop-v1.4.0-full-validation-2026-07-15.md` and describe the approved version state.

### Task 14: Verify And Enter The Final Commit Gate

- [x] Re-run focused version/root/branch contracts and the complete validation method against the version-aligned workspace.
- [x] Stage only the reviewed Agent Loop implementation, version, test, proposal, and report files; run `git diff --cached --check` and review the staged scope.
- [ ] Present the staged diff, verification evidence, proposed commit message, and remaining authorization boundaries to the human.
- [ ] Execute the commit only after a separate final Human Gate confirmation.
- [ ] Do not push, tag, create a PR, merge, release, publish, or synchronize any Agent CLI installation without a later explicit human instruction.

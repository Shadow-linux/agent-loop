# Agent-Guided Lightweight Change Lane Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Do not dispatch subagents unless the human separately authorizes one bounded dispatch.

**Goal:** Implement a v1.5.0 Agent-guided lightweight change lane that keeps background, adaptive planning, progress, targeted verification, rollback, and Human Gates while avoiding unnecessary Feature workspaces and full TDD ceremony for bounded non-Bug changes.

**Architecture:** Add one detailed runtime reference and one response-only card template, then route ordinary actionable non-Bug changes through an internal `Lightweight Change Assessment` before Feature construction. Preserve explicit Bug Management and Feature hard triggers, keep the lane out of canonical stage/message-intent/status models, and make scope expansion stop and return to Human Review. Coordinate controller, root guidance, planning/helper boundaries, memory/branch/submit rules, human docs, validation scenarios, focused regressions, version sync, and full semantic validation.

**Tech Stack:** Markdown skill sources/templates, Bash focused contract tests, Ruby standard-library structural assertions, existing Python 3.10+ root guidance tests, Git CLI for read-only inspection, repository full-validation method. No third-party dependency, runtime daemon, executable workflow database, or default target-project lightweight-change directory.

---

状态：Proposal 已批准；Implementation Plan 已执行完成，待最终 Human Review
设计来源：`docs/proposal/v1.5.x/lightweight-change-lane.md`
计划日期：2026-07-17
计划基线：`alpha/v1.5.0` at `81adf6422e509ee0b6012522398a3a908323b131`
当前 Skill 版本：`1.4.0`
目标 Skill 版本：`1.5.0`，仅在人类批准本计划并明确批准该版本实施后同步

## Execution Boundary

- Repository perspective: Agent Loop skill source maintainer. Do not create a target-project `.agent-loop/` tree in this repository.
- Existing untracked design input: `docs/proposal/v1.5.x/lightweight-change-lane.md`. Preserve its confirmed semantics; update only status/evidence fields after implementation.
- This plan file is planning output only. Plan approval authorizes neither implementation nor version sync unless the human explicitly says to implement v1.5.0.
- Do not install or synchronize source changes into Codex, Kimi Code, OpenCode, `.agents/skills/`, or any other Agent CLI directory.
- Do not create or switch branches, worktrees, tags, remotes, PRs, releases, or external artifacts during implementation.
- Do not commit, push, merge, tag, release, or publish. After validation, stop at Human Review and request the separate Git/Release gates.
- Do not dispatch subagents without a new explicit bounded dispatch approval.
- Use `apply_patch` for manual source edits. Preserve unrelated dirty work and stop on overlapping changes.
- A proposal is not runtime evidence. Recount tests and rerun all baselines live; do not copy historical totals into reports.
- Because this changes routing precedence, Feature entry, Plan/TDD selection, root Stage Map signals, and controller fallback, focused tests do not replace full validation.

## Stage Helper Resolution

| Field | Resolution |
|---|---|
| Stage | Plan Gate / Plan |
| Canonical candidate | `superpowers:writing-plans` — not exposed by the current runtime |
| Alias candidate | `writing-plans` — loaded completely from `/Users/shaodowyd/.codex/skills/writing-plans/SKILL.md` |
| Status | `loaded` |
| Fallback | `no` |
| Method used | exact file map, zero-context task ordering, RED/GREEN contract, exact commands/outputs, rollback and self-review |
| Agent Loop override | save beside the approved Proposal; no `docs/superpowers/`, automatic worktree, subagent, commit, push, tag, release, publish, or target-project artifact |

## Branch Context Evidence

- Branch Strategy: source-repository native policy from root `AGENTS.md`.
- Current Branch: `alpha/v1.5.0`.
- Baseline: released/sealed `v1.4.0` commit `81adf6422e509ee0b6012522398a3a908323b131`.
- Target Release Context: `v1.5.0` new-capability line.
- Customer Isolation: not applicable.
- Sealed Check: pass; no edit is planned on `v1.4.0`.
- Git actions authorized by this plan: none.

## File Responsibility Map

### Create

- `references/lightweight-change-lane.md` — detailed operational contract for eligibility, routing, response-local card execution, adaptive Plan/TDD, uncertainty, scope expansion, completion, and gates.
- `templates/lightweight-execution-card.md` — source-level response template; explicitly not copied into target `.agent-loop/` by default.
- `tests/validate-lightweight-change-lane.sh` — focused cross-surface ordering, no-new-stage/status/artifact, Bug/Feature precedence, card, TDD, root, version, and gate contract.
- `docs/reports/agent-loop-v1.5.0-lightweight-change-lane-red-baseline-2026-07-17.md` — live pre-implementation mechanical baseline plus focused RED evidence.
- `docs/reports/agent-loop-v1.5.0-full-validation-2026-07-17.md` — fresh Chinese six-domain semantic audit, focused/full test evidence, score, findings, and release recommendation.

### Modify: Controller And Core Design

- `SKILL.md` — concise lane entry, package map, required behavior, template map, stop/upgrade rules, and version.
- `references/runtime.md` — canonical precedence, explicit Bug priority, ordinary non-Bug assessment, eligibility outcome, response-local execution, scope expansion, stage-order annotation, and gate boundaries.
- `references/design.md` — durable concepts, authority, route model, adaptive depth, no-new-artifact/state invariants, and behavior/verification model.
- `references/concepts.md` — concise definitions and ownership.

### Modify: Routing, Execution, And Artifact Boundaries

- `references/stage-guides.md` — internal assessment/execution procedure; Operational Support escalation; Feature Follow-up trigger refinement.
- `references/workflow-checklists.md` — assessment, card, targeted TDD/verification, scope expansion, completion, and root-routing checks.
- `references/feature-follow-up.md` — keep explicit Bug and clear Feature ownership in Follow-up while sending generic “small tweak” through assessment first.
- `references/bug-management.md` — define explicit Bug management intent semantically rather than treating any generic “fix” wording as Bug intake; preserve Feature-owned repair.
- `references/artifact-rules.md` — response-local ownership; forbid default `.agent-loop/changes/` / quick-fix backlog.
- `references/document-templates.md` — point to the source-level response template without duplicating it as a target-project artifact.
- `references/skill-routing.md` — lightweight lane does not enter mandatory Plan/Execute helper stages; Feature promotion restores normal helper protocol.
- `references/external-skill-adapters.md` — prevent helper-native plan/spec directories and full Feature ceremony from being introduced into the lane.
- `references/implementation-planning.md` — distinguish construction-grade Feature plan from Lightweight Execution Card plan.

### Modify: Memory, Branch, Submit, And Root Guidance

- `references/project-memory-mode.md` — do not store lightweight backlog/history in project memory; allow only mechanical synchronization of an already-confirmed durable fact.
- `references/branch-management.md` — current branch/target/sealed rules still apply; card grants no branch action.
- `references/submit-and-integrate.md` — card completion/verification grants no commit, push, PR, merge, tag, release, or publish.
- `references/project-guidance.md` — root bootstrap placement and one-line routing requirement.
- `templates/root-AGENTS.md` — one concise reminder plus the matching Stage Map signal; all 13 managed blocks use one v1.5.0 revision.

### Modify: Human Docs, Scenarios, Version, And Existing Tests

- `README.md` — current version and overview of lightweight versus Feature/Bug handling.
- `Usage.md` — current version plus natural-language examples for domain/path/config, small logic, explicit Bug, uncertainty, and expansion.
- `CHANGELOG.md` — add `1.5.0 — 2026-07-17` and the feature contract.
- `plugin.json` — update package version and concise description without claiming that every change uses full TDD.
- `references/validation-scenarios.md` — add structured positive, negative, uncertainty, production, Bug, Feature, memory, branch, and gate pressure scenarios.
- `tests/test_root_agents_blocks.py`
- `tests/validate-branch-management-strategy.sh`
- `tests/validate-bug-management.sh`
- `tests/validate-human-help-version-docs.sh`
- `tests/validate-project-local-skills.sh`
- `tests/validate-project-skill-discovery-guard.sh`
- `tests/validate-requirement-lifecycle-backlog.sh`
- `tests/validate-root-agents-block-checker.sh`
- `tests/validate-root-agents-block-refresh.sh`
- `tests/validate-v1.2.4-root-stage-coverage.sh`

The listed existing tests consume the live root managed revision or current version. Historical fixture branch names, old release examples, prior Proposal/Report evidence, and old Changelog sections remain unchanged unless they falsely claim to be the current version.

## Non-Negotiable Invariants

1. `Lightweight Change Lane` is an internal route, not a canonical stage, message-intent value, Feature Type, Bug Resolution Path, task status, or Auto Mode.
2. It applies only to ordinary actionable non-Bug changes after Project Entry classification plus the minimum guidance, dirty-work, scope, and safety checks. Reliable long-term memory is required only for memory claims the route actually uses.
3. Explicit human Bug management intent wins before lightweight assessment and continues through the existing Bug Record / Resolution Path / Feature repair workflow.
4. Generic words such as “改一下”, “修一下”, “small tweak”, or `fix` do not by themselves prove Bug management intent or lightweight eligibility.
5. If an active Feature clearly owns the change, continue inside that Feature; the lane cannot escape Feature artifacts or gates.
6. Agent makes the route judgment when evidence is sufficient; no separate “enable lightweight mode” gate is added.
7. When route evidence is insufficient, Agent stops, presents few real options, recommends one with evidence, and performs zero writes before the answer.
8. The card always contains Background, Goal / Completion Criteria, Scope, Lane Rationale, Impact / Risk, Plan, Current Progress, Verification, Rollback, Human Gates, and Result / Residuals.
9. Plan always exists. Its depth is adaptive; the lane never uses No-Plan Decision.
10. The card is response-local by default and creates no target-project directory, file, backlog, lifecycle, or empty scaffold.
11. Cross-session work, pause/resume, handoff, subagent execution, long-term tracking, or complex evidence storage is a Feature trigger.
12. Fact/config/path/domain/docs changes use targeted verification; isolated logic changes use the smallest meaningful RED/GREEN; full Feature work keeps normal TDD.
13. The lane does not enter mandatory `writing-plans` or `test-driven-development` stages. Promotion to Feature restores their normal mandatory helper protocol.
14. No completion claim is allowed without fresh verification, diff review, scope confirmation, rollback, and durable-memory impact check.
15. Public API/event/data/state/permission/security/architecture/dependency/migration/unknown-consumer changes are Feature hard triggers even when the diff is one line.
16. Production/external reads, writes, paid calls, deploys, credentials, destructive operations, and configuration writes retain their existing Human Gates.
17. Scope expansion stops the lane before broader edits and returns to Human Review with evidence and one recommended route.
18. Human choice cannot override safety, data, public contract, sealed-release, customer-isolation, or action-specific Human Gates.
19. Already-confirmed durable facts may be mechanically synchronized under the card; new long-term facts/decisions require the owning workflow.
20. Card completion grants no branch, commit, push, PR, merge, tag, release, publish, archive, close, or Bug lifecycle action.
21. Project Entry classification is required, but the lane does not initialize or repair `.agent-loop/` solely to create a response-local card. Without memory, inspect root guidance, Git/dirty state, the target scope, nearby references, and verification entrypoints.
22. Project Skill Discovery Guard still runs before generic helper/action fallback when a reliable memory root exists; a matched active Project Skill keeps its per-invocation Execution Gate.
23. Root `AGENTS.md` contains only a concise router and Stage Map signal, not the full eligibility matrix or card template.
24. Skill version changes to `1.5.0` only after explicit implementation/version approval and all version-bearing files move together.
25. Focused and full validation preserve a real RED baseline and report live test results, not historical totals.

## Task 0: Re-establish Live Baseline And Protect Scope

**Files:**
- Read: `AGENTS.md`
- Read: `SKILL.md`
- Read: `references/runtime.md`
- Read: `references/design.md`
- Read: `docs/proposal/v1.5.x/lightweight-change-lane.md`
- Read: `docs/maintenance/full-validation-method.md`
- Create later: `docs/reports/agent-loop-v1.5.0-lightweight-change-lane-red-baseline-2026-07-17.md`

- [x] **Step 0.1: Confirm repository boundary and approved design input**

Run:

```bash
git status --short --branch
git rev-parse HEAD
git branch --show-current
sed -n '1,80p' docs/proposal/v1.5.x/lightweight-change-lane.md
```

Expected:

```text
branch: alpha/v1.5.0
HEAD: 81adf6422e509ee0b6012522398a3a908323b131
Proposal status: Proposal 已批准，Implementation Plan 待 Human Review
no unrelated change exists; the approved Proposal and this plan may be committed or untracked according to their separate Git Human Gate
```

If any unrelated change exists, stop and ask before editing.

- [x] **Step 0.2: Re-read mandatory authority and planning method**

Read completely:

```text
SKILL.md
references/runtime.md
references/design.md
references/skill-routing.md
references/external-skill-adapters.md
docs/maintenance/full-validation-method.md
```

Expected: maintainer perspective is active; no target-project `.agent-loop/` artifact is created.

- [x] **Step 0.3: Run the pre-change mechanical baseline**

Run:

```bash
shell_total=0
shell_pass=0
for test_file in tests/*.sh; do
  shell_total=$((shell_total + 1))
  if bash "$test_file"; then shell_pass=$((shell_pass + 1)); else exit 1; fi
done
printf 'shell: %s/%s PASS\n' "$shell_pass" "$shell_total"

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
python3 -c 'import json; json.load(open("plugin.json", encoding="utf-8"))'
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
git diff --check
```

Expected: every existing test and mechanical check passes. Record live totals and output; do not assume the historical `38/38` or any prior Python count remains current.

- [x] **Step 0.4: Capture pre-change semantic gaps**

Run:

```bash
rg -n "Explicit bypass|one-off|small tweak|maintenance-fix|If code changes are required|TDD is default" \
  SKILL.md references/runtime.md references/stage-guides.md references/feature-follow-up.md \
  references/bug-management.md templates/root-AGENTS.md README.md Usage.md
```

Expected evidence:

```text
runtime has a narrow explicit bypass but no autonomous Lightweight Change Assessment
Operational Support escalates every required code change to Feature/maintenance-fix/Follow-up
small tweak can be routed into Bug/Feature before a bounded non-Bug assessment
maintenance-fix remains a full Feature
TDD has no lightweight targeted-verification contract
```

Keep exact paths/line numbers for the RED report.

## Task 1: Add The Focused RED Contract

**Files:**
- Create: `tests/validate-lightweight-change-lane.sh`
- Create: `docs/reports/agent-loop-v1.5.0-lightweight-change-lane-red-baseline-2026-07-17.md`
- Test: `tests/validate-lightweight-change-lane.sh`

- [x] **Step 1.1: Create the focused failing test**

Create `tests/validate-lightweight-change-lane.sh` with this complete contract:

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
  grep -Fq -- "$text" "$root/$file" || fail "$file missing Lightweight Change contract: $text"
}

assert_not_contains() {
  local file=$1
  local text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    fail "$file contains forbidden Lightweight Change behavior: $text"
  fi
}

assert_file references/lightweight-change-lane.md
assert_file templates/lightweight-execution-card.md

for file in \
  SKILL.md \
  references/runtime.md \
  references/design.md \
  references/concepts.md \
  references/stage-guides.md \
  references/workflow-checklists.md; do
  assert_contains "$file" 'Lightweight Change Lane'
done

for text in \
  'Explicit Bug Management wins before this assessment.' \
  'The card is response-local by default.' \
  'Project Entry classification is required; creating or repairing long-term Agent Loop memory is not required solely to run this lane.' \
  'A Plan is always required, but its depth is adaptive.' \
  'Do not create `.agent-loop/changes/`, `.agent-loop/quick-fixes/`, or another lightweight backlog.' \
  'Scope expansion stops the lane before broader edits.' \
  'Card completion authorizes no Git, release, publish, production, or Bug lifecycle action.'; do
  assert_contains references/lightweight-change-lane.md "$text"
done

for text in \
  'Background:' \
  'Goal / Completion Criteria:' \
  'Scope:' \
  'Lane Rationale:' \
  'Impact / Risk:' \
  'Plan:' \
  'Current Progress:' \
  'Verification:' \
  'Rollback:' \
  'Human Gates:' \
  'Result / Residuals:' \
  'Response-local by default.' \
  'Do not copy this template into a target project by default.'; do
  assert_contains templates/lightweight-execution-card.md "$text"
done

ruby - "$root/references/runtime.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
tokens = [
  'explicit Bug management intent',
  'Human-Guided Bug Management',
  'actionable non-Bug change',
  'Lightweight Change Assessment',
  'clearly eligible',
  'Feature trigger',
  'uncertain',
  'Human Choice with Agent Recommendation'
]
sequence = content.scan(/```text\n(.*?)```/m).flatten.find { |block| tokens.all? { |token| block.include?(token) } }
abort 'FAIL: runtime missing canonical Lightweight Change routing sequence' unless sequence
positions = tokens.map { |token| sequence.index(token) }
abort 'FAIL: runtime reorders Lightweight Change routing sequence' unless positions == positions.sort

intent = content[/^## Message Intent Classification\n(.*?)(?=^## |\z)/m, 1]
abort 'FAIL: runtime Message Intent Classification missing' unless intent
abort 'FAIL: lightweight-change must not become a message intent' if intent.include?('`lightweight-change`')

stage_order = content[/^## Stage Order\n(.*?)(?=^## |\z)/m, 1]
abort 'FAIL: runtime Stage Order missing' unless stage_order
canonical_lines = stage_order.lines.map(&:strip)
abort 'FAIL: Lightweight Change Lane became a canonical stage' if canonical_lines.include?('Lightweight Change Lane')
abort 'FAIL: Lightweight Change Assessment became a canonical stage' if canonical_lines.include?('Lightweight Change Assessment')
RUBY

ruby - "$root/references/bug-management.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
allowed = 'investigate-first | flow-back | linked-feature | maintenance-fix | requirement | no-fix'
abort 'FAIL: existing Bug Resolution Path contract changed' unless content.include?(allowed)
abort 'FAIL: Lightweight Change became a Bug Resolution Path' if content.match?(/investigate-first \|[^\n]*lightweight/i)
abort 'FAIL: explicit Bug intent precedence is missing' unless content.include?('Explicit Bug management intent takes precedence over Lightweight Change Assessment.')
RUBY

assert_contains references/stage-guides.md 'A concrete bounded change request authorizes only the local scope disclosed in the card; it adds no separate Lightweight Mode gate.'
assert_contains references/stage-guides.md 'If code or configuration changes are required, run Lightweight Change Assessment before defaulting to Feature construction, unless explicit Bug intent or a Feature hard trigger already decides the route.'
assert_contains references/feature-follow-up.md 'Generic “small tweak” wording does not by itself enter Bug Management or Feature Follow-up.'
assert_contains references/implementation-planning.md 'A Lightweight Execution Card is not a Feature `plan.md` and does not enter Plan Gate.'
assert_contains references/skill-routing.md 'Lightweight Change Lane does not enter mandatory Plan Gate / Plan or Execute Task / Story helper resolution.'
assert_contains references/external-skill-adapters.md 'Do not expand a Lightweight Execution Card into `docs/superpowers/`, a Feature workspace, or a construction-grade plan.'
assert_contains references/artifact-rules.md 'Lightweight Execution Card | response-local execution control'
assert_contains references/project-memory-mode.md 'Do not store Lightweight Execution Card history or a lightweight backlog in `project.md`.'
assert_contains references/branch-management.md 'A Lightweight Execution Card authorizes no branch action.'
assert_contains references/submit-and-integrate.md 'A completed Lightweight Execution Card authorizes no submit or integration action.'

reminder='Before creating a Feature for a bounded non-Bug change, let Agent Loop assess the Lightweight Change Lane; if impact is unclear, stop and ask the human with a recommendation.'
count=$(grep -Fo -- "$reminder" "$root/templates/root-AGENTS.md" | wc -l | tr -d ' ')
[ "$count" -eq 1 ] || fail "root AGENTS must contain the concise Lightweight Change reminder exactly once; found $count"
assert_contains templates/root-AGENTS.md '| Ordinary non-Bug change appears bounded, reversible, and exactly verifiable | Lightweight Change Assessment (internal route) | `references/lightweight-change-lane.md` |'
assert_not_contains templates/root-AGENTS.md 'Lane Rationale:'
assert_not_contains templates/root-AGENTS.md 'Result / Residuals:'
assert_not_contains templates/root-AGENTS.md 'Feature Hard Triggers'

for scenario in \
  'Confirmed Internal Domain Replacement Uses Lightweight Card' \
  'Production Domain Migration Requires Feature' \
  'One-Line Public Contract Change Requires Feature' \
  'Multi-File Mechanical Synchronization May Stay Lightweight' \
  'Explicit Bug Intent Wins Before Lightweight Assessment' \
  'Generic Fix Wording Does Not Automatically Create Bug' \
  'Uncertain Impact Stops For Human Choice' \
  'Response-Local Card Always Contains Background And Plan' \
  'Fact Change Uses Targeted Verification Without Invented Unit Test' \
  'Small Isolated Logic Change Uses Minimal RED GREEN' \
  'Scope Expansion Stops Before Broader Edits' \
  'Active Feature Ownership Blocks Lane Escape' \
  'Durable Fact Synchronization Is Not A New Decision' \
  'Production And Git Gates Remain Separate' \
  'Repository Without Agent Loop Memory Uses Minimum Entry Check' \
  'Sealed Release Cannot Use Lightweight Lane'; do
  assert_contains references/validation-scenarios.md "### $scenario"
done

assert_contains SKILL.md 'Version: 1.5.0'
assert_contains plugin.json '"version": "1.5.0"'
assert_contains README.md '**Current version:** 1.5.0'
assert_contains Usage.md '**版本：** 1.5.0'
assert_contains CHANGELOG.md '## 1.5.0 — 2026-07-17'

ruby - "$root/templates/root-AGENTS.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
blocks = content.scan(/<!-- agent-loop:managed-start section:([^ ]+) .*?block-version:([^ ]+) -->/)
abort 'FAIL: root AGENTS managed blocks missing' if blocks.empty?
abort "FAIL: expected 13 managed blocks, found #{blocks.length}" unless blocks.length == 13
blocks.each do |section, revision|
  expected = '1.5.0-20260717'
  abort "FAIL: #{section} expected #{expected}, found #{revision}" unless revision == expected
end
RUBY

[ ! -d "$root/.agent-loop" ] || fail 'source repository must not contain target-project .agent-loop artifacts'
[ ! -d "$root/templates/.agent-loop" ] || fail 'templates must not introduce a default target-project .agent-loop change tree'

printf 'PASS: Lightweight Change routing, card, Bug/Feature boundary, adaptive verification, root, version, and gate contract is complete\n'
```

- [x] **Step 1.2: Verify the focused test is RED for the intended missing capability**

Run:

```bash
bash tests/validate-lightweight-change-lane.sh
```

Expected RED:

```text
FAIL: missing required file: references/lightweight-change-lane.md
```

The failure must be caused by the missing capability, not Shell syntax or a bad test path.

- [x] **Step 1.3: Save the live RED report**

Create `docs/reports/agent-loop-v1.5.0-lightweight-change-lane-red-baseline-2026-07-17.md` with:

```markdown
# Agent Loop v1.5.0 Lightweight Change Lane RED Baseline

- Date: 2026-07-17
- Branch: alpha/v1.5.0
- Baseline SHA: 81adf6422e509ee0b6012522398a3a908323b131
- Audit target: pre-implementation working tree plus the new focused RED test
- Existing shell baseline: copy the exact `shell: N/N PASS` line emitted by Step 0.3, using the observed numbers.
- Existing Python baseline: copy the exact unittest summary emitted by Step 0.3, including the observed executed-test count and result.
- Focused RED: `tests/validate-lightweight-change-lane.sh`

## Confirmed Gap

The current package has a narrow explicit bypass and No-Plan Decision, but no Agent-guided response-local lane with adaptive Plan/TDD, explicit Bug precedence, uncertainty handoff, and scope-expansion promotion.

## RED Evidence

Immediately below this heading, add a `text` fence containing the exact stdout/stderr from Step 1.2. Its first failure line must identify the missing `references/lightweight-change-lane.md` capability.

## Expected GREEN

The focused contract passes only after controller, detailed reference, response template, Bug/Feature precedence, root guidance, version surfaces, scenarios, and gate boundaries are synchronized.
```

Angle-bracket instructions above mean “copy the exact live command output into the report during execution”; do not leave angle brackets or placeholders in the saved report.

## Task 2: Create The Detailed Lane Reference And Response Template

**Files:**
- Create: `references/lightweight-change-lane.md`
- Create: `templates/lightweight-execution-card.md`
- Test: `tests/validate-lightweight-change-lane.sh`

- [x] **Step 2.1: Create the detailed operational reference**

Create `references/lightweight-change-lane.md` with these exact top-level sections:

```markdown
# Lightweight Change Lane

## Purpose And Position
## Intent And Precedence
## Project Entry Boundary
## Lightweight Change Assessment
## Eligibility
## Feature Hard Triggers
## Uncertain Route Human Choice
## Lightweight Execution Card
## Adaptive Plan Depth
## Targeted TDD And Verification
## Project Skill And Helper Boundaries
## Scope Expansion
## Completion
## Memory, Branch, Submit, And External Gates
## Forbidden Behavior
```

Under `Intent And Precedence`, include this canonical sequence verbatim:

```text
explicit Bug management intent
-> Human-Guided Bug Management

actionable non-Bug change
-> Lightweight Change Assessment
   -> clearly eligible -> Lightweight Execution Card
   -> Feature trigger -> Feature Construction
   -> uncertain -> Human Choice with Agent Recommendation
```

Include these exact normative sentences so downstream tests and Agents share one contract:

```text
Explicit Bug Management wins before this assessment.
The card is response-local by default.
Project Entry classification is required; creating or repairing long-term Agent Loop memory is not required solely to run this lane.
A Plan is always required, but its depth is adaptive.
Do not create `.agent-loop/changes/`, `.agent-loop/quick-fixes/`, or another lightweight backlog.
Scope expansion stops the lane before broader edits.
Card completion authorizes no Git, release, publish, production, or Bug lifecycle action.
```

Define eligibility as all-of: clear goal/acceptance, enumerable scope, no new product/technical decision, no public/data/state/permission/security boundary, no dependency/migration, exact targeted verification, reversible change, no Bug/Feature long-term tracking, no cross-session/handoff/subagent need, and sufficient evidence.

Under `Project Entry Boundary`, require root guidance, Git/dirty state, target-scope, nearby-reference and verification-entry checks. When `.agent-loop/` exists, read only relevant memory and active Feature evidence. When it is absent, do not initialize memory solely for the card. If a relied-on memory claim is stale or conflicting, stop for Recovery, Feature, or Human Choice.

Define Feature hard triggers as any-of: user-visible/acceptance change; API/event/schema/persistence/state/permission/security; dependency/migration/architecture; unknown consumers; ADR/Contract/complex E2E; cross-session/handoff/subagent; active Feature ownership; explicit Bug/Feature management; or scope expansion.

State that a concrete bounded change request authorizes only the disclosed local edits and local verification. It does not add a separate “Lightweight Mode” gate, and it never authorizes a named external/production/Git action.

- [x] **Step 2.2: Create the response-only card template**

Create `templates/lightweight-execution-card.md` with this exact content shape:

```markdown
# Lightweight Execution Card

Response-local by default. Do not copy this template into a target project by default.

Background:

Goal / Completion Criteria:

Scope:

Lane Rationale:

Impact / Risk:

Plan:
- [ ] Inspect and confirm the exact change point.
- [ ] Apply only the disclosed bounded change.
- [ ] Run targeted verification.
- [ ] Review diff, scope, memory impact, and rollback.

Current Progress:

Verification:

Rollback:

Human Gates:

Result / Residuals:
```

Add a note below the shape:

```text
All fields are required. Replace non-applicable fields with `none` plus a concrete reason. Do not leave placeholders. Expand or reduce Plan steps according to actual risk, but never remove Plan, progress, verification, or rollback.
```

- [x] **Step 2.3: Run the focused test and confirm it advances beyond the missing-file RED**

Run:

```bash
bash tests/validate-lightweight-change-lane.sh
```

Expected: still FAIL, now at the first missing controller integration such as `SKILL.md missing Lightweight Change contract: Lightweight Change Lane`. Record the new first failure locally; do not rewrite the saved original RED evidence.

## Task 3: Integrate Controller, Runtime, Design, Concepts, And Artifact Ownership

**Files:**
- Modify: `SKILL.md`
- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Modify: `references/concepts.md`
- Modify: `references/artifact-rules.md`
- Modify: `references/document-templates.md`
- Test: `tests/validate-lightweight-change-lane.sh`

- [x] **Step 3.1: Add the concise controller entry**

In `SKILL.md`:

1. Add `references/lightweight-change-lane.md` to the package map after Operational Support/message routing references.
2. Add `templates/lightweight-execution-card.md` to the template inventory as response-only.
3. Add a `When To Use` bullet for bounded ordinary non-Bug changes.
4. Add a required behavior after Message Intent Classification:

```text
For an actionable non-Bug change that may be bounded, run Lightweight Change Assessment before Feature construction. When clearly eligible, emit a response-local Lightweight Execution Card and continue within its disclosed local scope. When a Feature trigger applies, use the existing Feature path. When uncertain, stop and ask the human with options, one Agent recommendation, evidence, and zero writes before the answer.
```

5. Refine the existing one-off bypass text so an explicit safe bypass request becomes one input to the assessment rather than a second undocumented execution path.
6. Add stop conditions for uncertain route and scope expansion.
7. Keep `SKILL.md` concise; detailed eligibility and card fields remain in the new reference/template.

- [x] **Step 3.2: Add canonical runtime precedence**

In `references/runtime.md`:

1. Add `## Lightweight Change Lane` after Message Intent/Bug routing and before downstream Feature entry rules.
2. Include the exact canonical sequence from Task 2.
3. State that this is an internal route and does not add a message-intent value or canonical stage.
4. Refine `feature-follow-up` classification so explicit defect/QA/regression tracking or strong Feature ownership enters Follow-up, while generic “small tweak” alone enters assessment.
5. Annotate Stage Order with `[internal] Lightweight Change Assessment for eligible ordinary non-Bug changes`; do not add an unbracketed canonical stage line.
6. Add execution, completion, uncertainty, scope-expansion, Project Skill Discovery, production, and Git boundaries.
7. Replace the current standalone explicit bypass rule with compatibility wording that points to assessment.

Use this exact decision block in runtime:

```text
explicit Bug management intent
-> Human-Guided Bug Management

actionable non-Bug change
-> Lightweight Change Assessment
   -> clearly eligible -> Lightweight Execution Card
   -> Feature trigger -> Feature Construction
   -> uncertain -> Human Choice with Agent Recommendation
```

- [x] **Step 3.3: Add durable design and concepts**

In `references/design.md`, define:

- Lightweight Change Lane as an internal route;
- Lightweight Execution Card as response-local execution control;
- Adaptive Depth as Agent-owned Plan/test/detail selection below fixed safety/gate invariants;
- route precedence and authority split;
- no-new-artifact/status/lifecycle invariant;
- behavior logic versus fact/config verification;
- scope expansion and human decision ownership.

In `references/concepts.md`, add concise definitions and ownership rows:

```text
Lightweight Change Lane -> bounded non-Bug execution route
Lightweight Execution Card -> response-local background/plan/progress/verification/rollback control
Adaptive Depth -> risk-based detail selection, never gate reduction
```

Do not add `lightweight-change` to Message Intent values, Feature Type, Task Status, Bug Status, Bug Resolution, or Resolution Path.

- [x] **Step 3.4: Lock artifact ownership and template routing**

In `references/artifact-rules.md`, add this ownership row:

```text
Lightweight Execution Card | response-local execution control | target-project backlog, Feature replacement, Bug lifecycle, or Git authorization
```

State explicitly that `.agent-loop/changes/`, `.agent-loop/quick-fixes/`, and similar default lightweight directories are forbidden in v1.5.0.

In `references/document-templates.md`, add a concise section pointing to `templates/lightweight-execution-card.md`; state it is rendered in the response/current task context and is not copied into target project memory by default. Do not duplicate the full card in both files.

- [x] **Step 3.5: Run the focused contract**

Run:

```bash
bash tests/validate-lightweight-change-lane.sh
```

Expected: failure advances to routing/stage/helper/root/version/scenario integrations. No core-controller missing-file failure remains.

## Task 4: Refine Operational Support, Feature Follow-up, And Bug Precedence

**Files:**
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/feature-follow-up.md`
- Modify: `references/bug-management.md`
- Test: `tests/validate-lightweight-change-lane.sh`

- [x] **Step 4.1: Add assessment and execution procedure to stage guidance**

In `references/stage-guides.md`, add `## Lightweight Change Lane` and state on its first paragraph that it is an internal route, not a canonical stage.

The procedure must execute in this order:

```text
Project Entry classification plus minimum guidance, dirty-work, scope and safety checks
-> explicit Bug / active Feature precedence
-> enumerate goal, acceptance, scope, risk, verification, rollback
-> decide clearly eligible | Feature trigger | uncertain
-> emit the complete card before first write
-> Project Skill Discovery Guard before generic action fallback
-> bounded edit
-> targeted verification
-> diff/scope/memory/rollback review
-> result or scope-expansion stop
```

Include this exact authorization rule:

```text
A concrete bounded change request authorizes only the local scope disclosed in the card; it adds no separate Lightweight Mode gate.
```

Update Code-Guided Operational Support with:

```text
If code or configuration changes are required, run Lightweight Change Assessment before defaulting to Feature construction, unless explicit Bug intent or a Feature hard trigger already decides the route.
```

Keep read-only Operational Support as the default until a concrete change scope is authorized.

- [x] **Step 4.2: Add the matching checklist**

In `references/workflow-checklists.md`, add `## Lightweight Change Lane` with checkboxes for:

- reliable project/memory/safety entry;
- explicit Bug and active Feature precedence;
- eligibility all-of and Feature-trigger any-of;
- complete card before write;
- adaptive Plan, never No-Plan;
- Project Skill Discovery Guard when a reliable memory root exists;
- targeted TDD/verification choice with reason;
- scope expansion stop;
- fresh verification and diff review;
- memory, branch, submit, production, external and Git gates;
- result/residual report.

- [x] **Step 4.3: Refine Feature Follow-up ownership**

In `references/feature-follow-up.md`:

- preserve explicit Bug, regression, QA evidence, closed-Feature ownership, and Requirement-change routes;
- add this exact sentence:

```text
Generic “small tweak” wording does not by itself enter Bug Management or Feature Follow-up.
```

- send ordinary non-Bug bounded changes to Lightweight Change Assessment before candidate Feature scans;
- if evidence identifies an active/closed owning Feature or product behavior change, retain existing Follow-up/Flow-back rules;
- do not add Lightweight Change as a Feature Type or Resolution Path.

- [x] **Step 4.4: Refine explicit Bug intent without weakening Bug management**

In `references/bug-management.md`:

- add this exact precedence sentence:

```text
Explicit Bug management intent takes precedence over Lightweight Change Assessment.
```

- define explicit intent by semantic management request: the human frames an expected-versus-observed defect, asks to record/track/manage/investigate as Bug, or confirms Bug handling after Agent asks;
- state that the isolated words `fix`, “修一下”, “改一下”, or “small tweak” do not alone create a Bug Record;
- keep all accepted Bug code repairs in Feature-owned `flow-back | linked-feature | maintenance-fix` paths;
- keep the Resolution Path enumeration byte-for-byte unchanged;
- do not allow a Bug to use Lightweight Execution Card as its repair target.

- [x] **Step 4.5: Run focused and affected existing contracts**

Run:

```bash
bash tests/validate-lightweight-change-lane.sh
bash tests/validate-operational-support-guard.sh
bash tests/validate-bug-management.sh
```

Expected: existing contracts may still fail only where old wording/current version expectations must be intentionally synchronized in later tasks. Any failure indicating Bug lifecycle, Operational Support read-only default, or Feature repair ownership changed is a real regression and must be fixed now.

## Task 5: Align Helper, Planning, Memory, Branch, And Submit Boundaries

**Files:**
- Modify: `references/skill-routing.md`
- Modify: `references/external-skill-adapters.md`
- Modify: `references/implementation-planning.md`
- Modify: `references/project-memory-mode.md`
- Modify: `references/branch-management.md`
- Modify: `references/submit-and-integrate.md`
- Test: `tests/validate-lightweight-change-lane.sh`

- [x] **Step 5.1: Prevent mandatory helper overhead inside the lane**

In `references/skill-routing.md`, add:

```text
Lightweight Change Lane does not enter mandatory Plan Gate / Plan or Execute Task / Story helper resolution.
```

Explain that the controller itself writes the small response-local Plan and selects targeted verification. If the work is promoted to Feature, normal `writing-plans` and `test-driven-development` helper requirements resume before Feature execution.

Do not add Lightweight Change Lane to the mandatory stage table.

In `references/external-skill-adapters.md`, add:

```text
Do not expand a Lightweight Execution Card into `docs/superpowers/`, a Feature workspace, or a construction-grade plan.
```

External helpers may advise method only when already appropriate; they cannot create a helper-specific path, artifact, mode, or gate.

- [x] **Step 5.2: Separate card Plan from Feature Plan Gate**

In `references/implementation-planning.md`, add:

```text
A Lightweight Execution Card is not a Feature `plan.md` and does not enter Plan Gate.
```

Define the card Plan as current-context, bounded, exact enough to show progress, verification and rollback. Construction-grade zero-context planning remains mandatory for Feature tasks when its existing triggers apply. No-Plan Decision remains Feature-task-only and is never used by the lane.

- [x] **Step 5.3: Protect memory ownership**

In `references/project-memory-mode.md`, add:

```text
Do not store Lightweight Execution Card history or a lightweight backlog in `project.md`.
```

Permit only mechanical synchronization of an already human-confirmed durable fact when the exact memory path is included in the card Scope. New environment/product/architecture/release decisions leave the lane and use the owning workflow.

- [x] **Step 5.4: Preserve branch and submit gates**

In `references/branch-management.md`, add:

```text
A Lightweight Execution Card authorizes no branch action.
```

State that adopted strategy, Target Release Context, sealed release, customer isolation, and exact Branch Action/Cleanup gates still apply.

In `references/submit-and-integrate.md`, add:

```text
A completed Lightweight Execution Card authorizes no submit or integration action.
```

Require fresh verification/diff evidence to be re-read at Submit; card execution approval cannot become commit/push/PR/merge/tag/release/publish approval.

- [x] **Step 5.5: Run the focused contract**

Run:

```bash
bash tests/validate-lightweight-change-lane.sh
```

Expected: helper/planning/memory/branch/submit assertions pass; remaining failures are root/version/human-doc/scenario work.

## Task 6: Update Root Guidance Without Turning It Into Runtime Authority

**Files:**
- Modify: `references/project-guidance.md`
- Modify: `templates/root-AGENTS.md`
- Modify later in Task 8: root revision consumers listed in File Responsibility Map
- Test: `tests/validate-lightweight-change-lane.sh`
- Test: `tests/validate-root-agents-block-refresh.sh`
- Test: `tests/validate-v1.2.4-root-stage-coverage.sh`

- [x] **Step 6.1: Add the owning project-guidance rule**

In `references/project-guidance.md`, require root guidance to contain only this concise reminder and one Stage Map signal/reference:

```text
Before creating a Feature for a bounded non-Bug change, let Agent Loop assess the Lightweight Change Lane; if impact is unclear, stop and ask the human with a recommendation.
```

State that eligibility, card fields, adaptive TDD, scope expansion, and completion details belong in `references/lightweight-change-lane.md`, not root `AGENTS.md`.

- [x] **Step 6.2: Update root bootstrap and Stage Map**

In `templates/root-AGENTS.md`:

1. Replace the broad rule that routes every “small tweak” through Bug Management with explicit Bug-intent wording.
2. Insert the exact concise reminder once in the smallest appropriate managed block.
3. Add a Stage Map row:

```markdown
| Ordinary non-Bug change appears bounded, reversible, and exactly verifiable | Lightweight Change Assessment (internal route) | `references/lightweight-change-lane.md` |
```

4. Keep explicit Bug/Feature rows higher priority where their evidence is already decisive.
5. Do not copy the eligibility matrix or card template into root guidance.
6. Do not change managed block revision yet; Task 8 synchronizes all version-bearing values atomically.

- [x] **Step 6.3: Confirm root behavior content before version sync**

Run:

```bash
reminder='Before creating a Feature for a bounded non-Bug change, let Agent Loop assess the Lightweight Change Lane; if impact is unclear, stop and ask the human with a recommendation.'
test "$(grep -Fo -- "$reminder" templates/root-AGENTS.md | wc -l | tr -d ' ')" = 1
! grep -Fq 'Lane Rationale:' templates/root-AGENTS.md
! grep -Fq 'Result / Residuals:' templates/root-AGENTS.md
git diff --check
```

Expected: behavior content is concise; root revision tests remain intentionally RED until Task 8.

## Task 7: Add Human Guidance And Pressure Scenarios

**Files:**
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `references/validation-scenarios.md`
- Test: `tests/validate-lightweight-change-lane.sh`

- [x] **Step 7.1: Explain the feature in README**

Add a concise `### Lightweight Change Lane` section near Core Concepts/Quick Start:

```text
Bounded ordinary non-Bug changes use a response-local card with Background, adaptive Plan, progress, targeted verification, rollback, and result. Explicit Bugs keep Bug Management; public/data/state/security/architecture/unknown-impact changes use Feature. If Agent is unsure, it asks the human with a recommendation before writing.
```

Update the core flow diagram to show the internal lane before Feature construction without listing it as a canonical stage.

- [x] **Step 7.2: Add human trigger examples in Usage**

Add `### 我想做一个边界明确的小修改` with a table covering:

| Human wording | Expected Agent behavior |
|---|---|
| “把生产脚本里已经确认的旧域名换成新域名。” | emit card; scan references; replace; syntax/parse/dry-run; diff/rollback |
| “迁移正式生产域名，并处理 DNS、证书和调用方。” | Feature/Decision path, not lightweight |
| “修正这个内部脚本条件，预期行为已经明确。” | card plus smallest meaningful RED/GREEN |
| “这是 Bug，请登记并修复。” | Bug Management, never lightweight |
| “不确定有没有外部调用方。” | stop; options plus Agent recommendation; zero writes |

State that the human does not need to say “启用轻量模式”; the Agent owns the initial judgment.

- [x] **Step 7.3: Add sixteen structured validation scenarios**

Append a numbered `## Lightweight Change Lane` scenario group. Each `###` scenario must include `Prompt:`, `Expected Route:`, `Evidence:`, `Required Action:`, `Forbidden Action:`, and `Next:`.

Use these exact scenario titles:

```text
Confirmed Internal Domain Replacement Uses Lightweight Card
Production Domain Migration Requires Feature
One-Line Public Contract Change Requires Feature
Multi-File Mechanical Synchronization May Stay Lightweight
Explicit Bug Intent Wins Before Lightweight Assessment
Generic Fix Wording Does Not Automatically Create Bug
Uncertain Impact Stops For Human Choice
Response-Local Card Always Contains Background And Plan
Fact Change Uses Targeted Verification Without Invented Unit Test
Small Isolated Logic Change Uses Minimal RED GREEN
Scope Expansion Stops Before Broader Edits
Active Feature Ownership Blocks Lane Escape
Durable Fact Synchronization Is Not A New Decision
Production And Git Gates Remain Separate
Repository Without Agent Loop Memory Uses Minimum Entry Check
Sealed Release Cannot Use Lightweight Lane
```

For every scenario, make `Forbidden Action` concrete. Examples: create Feature before assessment, create `.agent-loop/changes/`, omit Plan, invent a unit test for string replacement, bypass Bug, write before human answer, edit broader consumers after expansion, modify sealed version, or infer commit/production authorization.

- [x] **Step 7.4: Run scenario and focused assertions**

Run:

```bash
bash tests/validate-lightweight-change-lane.sh
rg -n '^### (Confirmed Internal Domain|Production Domain|One-Line Public|Multi-File Mechanical|Explicit Bug|Generic Fix|Uncertain Impact|Response-Local Card|Fact Change|Small Isolated|Scope Expansion|Active Feature|Durable Fact|Production And Git|Repository Without|Sealed Release)' references/validation-scenarios.md
```

Expected: all sixteen titles exist once; remaining focused failure is version/revision synchronization.

## Task 8: Perform Human-Approved v1.5.0 Version Synchronization

**Human Gate:** Do not execute this task unless the human has explicitly approved implementation for v1.5.0. Proposal/plan approval alone is not version authorization.

**Files:**
- Modify: `SKILL.md`
- Modify: `plugin.json`
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`
- Modify: `templates/root-AGENTS.md`
- Modify: `references/workflow-checklists.md`
- Modify: all live-revision/version tests listed in File Responsibility Map

- [x] **Step 8.1: Update all primary version-bearing files together**

Apply exactly:

```text
SKILL.md: Version: 1.5.0
plugin.json: "version": "1.5.0"
README.md: **Current version:** 1.5.0
Usage.md: **版本：** 1.5.0
CHANGELOG.md: ## 1.5.0 — 2026-07-17
templates/root-AGENTS.md: every one of 13 managed starts -> block-version:1.5.0-20260717
```

In `plugin.json`, update description/longDescription only enough to avoid the false claim that all changes require full Feature/TDD; retain valid JSON and product identity.

In `CHANGELOG.md`, add `### Lightweight Change Lane` with bullets for autonomous assessment, response-local card, adaptive Plan/TDD, explicit Bug/Feature precedence, uncertainty Human Choice, scope expansion, no new target artifact/status/stage, gates, tests, and root revision.

- [x] **Step 8.2: Update live revision/version consumers**

Replace current live expectations `1.4.0-20260716.1` with `1.5.0-20260717` only in:

```text
references/workflow-checklists.md
tests/test_root_agents_blocks.py
tests/validate-branch-management-strategy.sh
tests/validate-bug-management.sh
tests/validate-project-local-skills.sh
tests/validate-project-skill-discovery-guard.sh
tests/validate-requirement-lifecycle-backlog.sh
tests/validate-root-agents-block-checker.sh
tests/validate-root-agents-block-refresh.sh
tests/validate-v1.2.4-root-stage-coverage.sh
```

Also update the current-version assertions in `tests/validate-requirement-lifecycle-backlog.sh` to `1.5.0` and the new Changelog date/heading. Preserve historical strings that assert old releases remain documented.

Update `tests/validate-human-help-version-docs.sh` so its current-version help examples expect `1.5.0`; keep older-version comparison examples unchanged.

- [x] **Step 8.3: Search old version strings and classify every remaining occurrence**

Run:

```bash
rg -n '1\.4\.0|1\.4\.0-20260716\.1' \
  SKILL.md plugin.json README.md Usage.md CHANGELOG.md templates references tests examples \
  --glob '!docs/proposal/**' --glob '!docs/reports/**'
```

Expected remaining categories only:

```text
historical CHANGELOG 1.4.0 release section
historical branch/example/fixture values intentionally demonstrating v1.4.0
past revision assertions explicitly proving stale-version behavior
no file claiming 1.4.0 is the current Skill or current root revision
```

Review every match; do not bulk replace fixture/branch examples.

- [x] **Step 8.4: Validate structured metadata and root revision**

Run:

```bash
ruby -e 'require "yaml"; data=YAML.load_file("SKILL.md"); abort unless data["name"] == "agent-loop"'
python3 -c 'import json; d=json.load(open("plugin.json", encoding="utf-8")); assert d["version"] == "1.5.0"'
python3 - <<'PY'
import re
from pathlib import Path
s = Path('templates/root-AGENTS.md').read_text(encoding='utf-8')
revisions = re.findall(r'block-version:([^ ]+) -->', s)
assert len(revisions) == 13, revisions
assert set(revisions) == {'1.5.0-20260717'}, revisions
print('root-managed-revision=1.5.0-20260717 count=13')
PY
```

Expected: all commands pass.

## Task 9: Reach Focused GREEN And Repair Coordinated Regressions

**Files:**
- Test: `tests/validate-lightweight-change-lane.sh`
- Test: all affected tests listed below
- Modify only when a failure proves an intended coordinated surface was missed

- [x] **Step 9.1: Run focused GREEN**

Run:

```bash
bash tests/validate-lightweight-change-lane.sh
```

Expected GREEN:

```text
PASS: Lightweight Change routing, card, Bug/Feature boundary, adaptive verification, root, version, and gate contract is complete
```

- [x] **Step 9.2: Run affected routing/helper/root/version tests**

Run:

```bash
for test_file in \
  tests/validate-operational-support-guard.sh \
  tests/validate-bug-management.sh \
  tests/validate-mandatory-helper-routing.sh \
  tests/validate-project-skill-discovery-guard.sh \
  tests/validate-branch-management-strategy.sh \
  tests/validate-requirement-lifecycle-backlog.sh \
  tests/validate-root-agents-block-refresh.sh \
  tests/validate-root-agents-block-checker.sh \
  tests/validate-v1.2.4-root-stage-coverage.sh \
  tests/validate-human-help-version-docs.sh; do
  bash "$test_file"
done

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_root_agents_blocks
```

Expected: every command passes.

If `validate-human-help-version-docs.sh` expects v1.4.0 current-version examples, update only its current help/version strings to 1.5.0; preserve comparison examples for older versions.

- [x] **Step 9.3: Run negative self-scan**

Run:

```bash
test ! -d .agent-loop
test ! -d templates/.agent-loop
bash tests/validate-lightweight-change-lane.sh
git diff --check
```

Expected: source-repository boundary, the focused structural negative assertions, and diff checks pass without a checker matching its own explanatory prose.

## Task 10: Run Mandatory Full Validation And Write Fresh Reports

**Files:**
- Create: `docs/reports/agent-loop-v1.5.0-full-validation-2026-07-17.md`
- Modify: `docs/proposal/v1.5.x/lightweight-change-lane.md`
- Modify: `docs/proposal/v1.5.x/lightweight-change-lane-implementation-plan.md` status/checklist evidence only
- Read: `docs/maintenance/full-validation-method.md`

- [x] **Step 10.1: Run every Shell test with live counting**

Run:

```bash
shell_total=0
shell_pass=0
for test_file in tests/*.sh; do
  shell_total=$((shell_total + 1))
  printf '[shell] %s\n' "$test_file"
  if bash "$test_file"; then
    shell_pass=$((shell_pass + 1))
  else
    printf 'FAIL: %s\n' "$test_file" >&2
    exit 1
  fi
done
printf 'shell: %s/%s PASS\n' "$shell_pass" "$shell_total"
```

Expected: every live `tests/*.sh` passes, including the new focused test. Record the observed count.

- [x] **Step 10.2: Run every Python test**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: `OK`; record the live number of executed tests from output.

- [x] **Step 10.3: Run all mechanical checks**

Run:

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
python3 -c 'import json; json.load(open("plugin.json", encoding="utf-8"))'
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
python3 - <<'PY'
from pathlib import Path
bad=[]
for path in Path('.').rglob('*.md'):
    if '.git' in path.parts:
        continue
    count=sum(1 for line in path.read_text(encoding='utf-8').splitlines() if line.lstrip().startswith('```'))
    if count % 2:
        bad.append((str(path), count))
if bad:
    raise SystemExit(f'unbalanced Markdown fences: {bad}')
print('markdown-fences=balanced')
PY
git diff --check
```

Expected: YAML/JSON/Shell/Markdown/diff checks pass.

- [x] **Step 10.4: Perform the six-domain semantic audit**

Audit live workspace evidence under the required domains:

```text
Logic Correctness
Autonomy
Project Entry / Evidence Graph + DDD Onboarding
Development / Test Workflow
Memory
Recommendation
```

At minimum replay these cross-feature pressure paths:

- ordinary bounded non-Bug change chooses card;
- explicit Bug keeps Bug Management and Feature repair;
- active Feature ownership blocks lane escape;
- one-line public/data/state/security change chooses Feature;
- uncertain scope produces recommendation and zero writes;
- scope expansion stops before broader edit;
- fact/config verification does not invent a useless test;
- isolated logic still gets meaningful RED/GREEN;
- Project Skill Discovery and execution gate remain ordered;
- Operational Support remains read-only until local change scope or operational action is authorized;
- root Stage Map remains navigation, not runtime authority;
- repository without `.agent-loop/` uses the minimum Project Entry/guidance/scope check without initializing long-term memory;
- version, root revision, branch sealed rule, memory ownership, submit and release gates remain coherent;
- existing Requirement -> ADR -> Feature, Bug, archive, memory reconciliation, project-skill, close and submit invariants remain reachable.

No Critical/High issue may remain for a STRONG release recommendation. Repair any real loophole by adding/strengthening a focused assertion first, proving RED, then fixing and rerunning the full suite.

- [x] **Step 10.5: Write the full validation report from fresh evidence**

Create `docs/reports/agent-loop-v1.5.0-full-validation-2026-07-17.md` in Chinese with:

```text
date, branch, version, exact audit target
live shell pass/total and Python executed count
focused RED -> GREEN evidence
six-domain score table and final STRONG/STABLE/FRAGILE/BROKEN judgment
Critical/High/Medium/Low findings with paths/lines
passed invariants and pressure scenarios
repairs made during validation
residual risks and release recommendation
explicit statement that commit/push/tag/release/publish remain unauthorized
```

Do not copy a prior report score or test total.

- [x] **Step 10.6: Refresh Proposal and Plan status truthfully**

Only after all implementation and validation pass, change Proposal status to:

```text
状态：Proposal、实施、focused validation 与全量验证已完成，待最终 Human Review
```

Change this plan status to:

```text
状态：Proposal 已批准；Implementation Plan 已执行完成，待最终 Human Review
```

Mark task checkboxes only where fresh evidence exists. Do not claim commit, push, tag, release, publish, or installed-Skill synchronization.

## Task 11: Final Maintainer Self-Review And Human Review Stop

**Files:**
- Review: every file in the File Responsibility Map
- Review: `git diff`
- Review: `git status --short --branch`

- [x] **Step 11.1: Review the complete diff by ownership surface**

Run:

```bash
git diff --stat
git diff -- SKILL.md references/runtime.md references/design.md references/lightweight-change-lane.md
git diff -- references/stage-guides.md references/workflow-checklists.md references/feature-follow-up.md references/bug-management.md
git diff -- references/skill-routing.md references/external-skill-adapters.md references/implementation-planning.md
git diff -- references/artifact-rules.md references/document-templates.md references/project-memory-mode.md
git diff -- references/branch-management.md references/submit-and-integrate.md references/project-guidance.md templates/root-AGENTS.md
git diff -- README.md Usage.md CHANGELOG.md plugin.json references/validation-scenarios.md
git diff -- tests/validate-lightweight-change-lane.sh tests/test_root_agents_blocks.py tests/validate-*.sh
git status --short --branch
```

Expected: no unrelated edits, no target `.agent-loop/`, and no implementation artifact outside the mapped surfaces.

- [x] **Step 11.2: Run plan self-review**

Confirm:

- every approved Proposal section maps to a task;
- no `TBD`, `TODO`, `FIXME`, “implement later”, “write tests for the above”, or equivalent placeholder remains in live source/reports;
- canonical route tokens and names are consistent across runtime/design/reference/root/scenarios/tests;
- Bug Resolution Path and lifecycle remain unchanged;
- lane is not a canonical stage/intent/status/artifact;
- card fields are complete and response-local;
- Feature hard triggers, uncertainty, scope expansion and Human Gates are explicit;
- version and all 13 root block revisions are synchronized;
- all commands and report evidence are fresh.

- [x] **Step 11.3: Present Human Review Summary and stop**

Present a concise table with:

```text
implementation scope
focused RED/GREEN result
full shell/Python/mechanical results
six-domain score and unresolved findings
version/root revision result
changed/new files
residual risks
recommended next action
```

Stop at Human Review. Do not stage, commit, push, tag, release, publish, create/switch/delete branches, dispatch subagents, or synchronize installed Skills without a new explicit human authorization.

## Plan Self-Review

- Spec coverage: all approved Proposal behaviors map to Tasks 2–10; explicit Bug priority, adaptive card, Plan/TDD, uncertainty, expansion, gates, root, version and validation have direct tests.
- Placeholder scan: plan contains no unresolved design placeholder; report-writing steps require copying live observed output and explicitly forbid leaving placeholder markers.
- Type/name consistency: `Lightweight Change Lane`, `Lightweight Change Assessment`, `Lightweight Execution Card`, and `Adaptive Depth` are used consistently; `lightweight-change` is intentionally not a message intent.
- Command specificity: exact paths, commands, expected RED/GREEN and current revision values are supplied.
- Risk/rollback coverage: scope expansion, dirty work, production/external/Git gates, sealed release, memory ownership and partial-edit decisions stop before expansion.
- Source structure: one detailed reference plus one response template keeps `SKILL.md`, root guidance and stage guides concise.
- Branch context: current alpha branch targets a new v1.5.0 capability; no Git mutation is authorized.
- Bug context: none for this repository change; runtime behavior explicitly preserves Bug-managed Feature repair.

## Handoff

Recommended next action: Human reviews the completed implementation, fresh validation reports, Proposal coverage, and final diff, then separately decides whether to authorize Git actions.
Stop condition: remain at final Human Review; implementation is complete, but no stage, commit, push, tag, release, publish, branch action, or installed-Skill synchronization is authorized.
Evidence to retain: approved Proposal, this executed plan, live RED baseline, focused/full validation reports, and final diff review.

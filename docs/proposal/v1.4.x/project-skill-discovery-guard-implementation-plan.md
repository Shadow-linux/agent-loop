# Project Skill Discovery Guard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Do not dispatch subagents unless the human separately and explicitly authorizes them. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the Project-Local Skills discovery loophole so a reliable Agent Loop project checks `.agent-loop/skills/INDEX.md` before claiming no relevant project skill or entering a generic execution fallback, while preserving progressive loading and the per-invocation Execution Gate.

**Architecture:** Add one internal `Project Skill Discovery Guard` between reliable memory/intent routing and stage-specific helper or fallback action. `SKILL.md`, `references/runtime.md`, and `references/design.md` own the controller invariant; `references/project-skills.md` owns detailed matching and drift behavior; stage/checklist/root/human-doc surfaces remain derived and concise. The implementation adds no canonical stage, message intent, persistent status, cache artifact, executable schema, global installation, or automatic execution path.

**Tech Stack:** Markdown runtime contracts and templates, Bash focused regressions, Ruby standard-library structural assertions, Python 3.10+ existing root-guidance checker/tests, repository full-validation method.

---

状态：Proposal 已批准，Implementation Plan 待 Human Review
设计来源：`docs/proposal/v1.4.x/project-skill-discovery-guard.md`
计划日期：2026-07-16
计划基线：`alpha/v1.4.0` at `c022169`

## Execution Constraints

- Work from the Agent Loop skill source-repository maintainer perspective.
- Do not create a target-project `.agent-loop/` tree in this repository.
- Preserve `docs/proposal/v1.4.x/post-merge-memory-reconciliation.md` byte-for-byte; it is unrelated untracked human work.
- Keep Skill version `1.4.0`; do not edit `plugin.json` or version labels.
- Do not install or sync this source into Codex, Kimi Code, OpenCode, `.agents/skills/`, or any global Skill directory.
- Do not create a branch, worktree, tag, PR, release, or external artifact.
- Do not stage, commit, push, merge, release, publish, or tag. The plan stops at Human Review.
- Do not dispatch subagents without new explicit human approval.
- Use `apply_patch` for manual edits and preserve unrelated dirty work.
- Stop immediately when Proposal rules conflict with current runtime/design, when a named file has unrelated overlapping edits, when a new artifact/dependency/status/stage is required, or when focused/full validation cannot be made reliable.

## File Responsibility Map

### New files

- `tests/validate-project-skill-discovery-guard.sh` — focused cross-surface contract; checks canonical ordering, fallback outcomes, root brevity, managed revision, and source-repository boundary.
- `docs/reports/agent-loop-v1.4.0-project-skill-discovery-guard-red-baseline-2026-07-16.md` — saved pre-repair failure evidence.
- `docs/reports/agent-loop-v1.4.0-project-skill-discovery-guard-full-validation-2026-07-16.md` — Chinese RED/GREEN, focused/full validation, six-domain semantic audit, score, and residual-risk report.

### Core authority files

- `SKILL.md` — concise controller entry and stop rule.
- `references/runtime.md` — executable guard position, canonical result branches, ordering, and fallback permission.
- `references/design.md` — durable discovery invariant and ownership/precedence model.
- `references/project-skills.md` — detailed matching, progressive read, negative-claim evidence, drift, and Execution Gate interaction.

### Derived workflow surfaces

- `references/stage-guides.md` — Code-Guided Operational Support pre-action guard.
- `references/workflow-checklists.md` — repeatable guard checklist and refreshed managed-revision examples.
- `references/project-guidance.md` — root-guidance generation/refresh contract.
- `templates/root-AGENTS.md` — one short bootstrap reminder only; all 13 managed blocks move to revision `1.4.0-20260716`.
- `references/validation-scenarios.md` — adversarial Project Skill discovery scenarios and refreshed current-revision examples.
- `README.md` — human overview of native/global versus project-local discovery.
- `Usage.md` — human trigger examples and expected discovery-before-fallback behavior.
- `CHANGELOG.md` — v1.4.0 in-progress behavior and root managed revision entry.

### Existing regression files affected by the root revision

- `tests/validate-project-local-skills.sh`
- `tests/validate-root-agents-block-refresh.sh`
- `tests/validate-root-agents-block-checker.sh`
- `tests/test_root_agents_blocks.py`
- `tests/validate-v1.2.4-root-stage-coverage.sh`
- `tests/validate-requirement-lifecycle-backlog.sh`
- `tests/validate-branch-management-strategy.sh`
- `tests/validate-bug-management.sh`

Historical proposal/report revision strings remain unchanged. The existing historical Changelog statement for `1.4.0-20260715.1` remains; add a later entry rather than rewriting history.

## Canonical Contract To Implement

The exact semantic order is:

```text
latest actionable intent / current stage
-> inspect Project Skill INDEX metadata
-> match active bootstrap / on-demand candidates
-> verify exact INDEX row, path, and manifest
-> read-only load the matched Project Skill
-> Execution Gate
-> stage action

index-absent | no-active-match
-> runtime/global helper if applicable
-> generic Operational Support or Agent Loop fallback

project-skill-drift
-> fail closed
-> Recovery or Project Skill Creation / Update
```

The response-level results `matched-active | index-absent | no-active-match | project-skill-drift` are not persisted and do not become lifecycle states.

### Task 0: Protect Baseline And Reconfirm Scope

**Files:**
- Read: `AGENTS.md`
- Read: `SKILL.md`
- Read: `references/runtime.md`
- Read: `references/design.md`
- Read: `references/project-skills.md`
- Read: `references/stage-guides.md`
- Read: `references/workflow-checklists.md`
- Read: `references/project-guidance.md`
- Read: `templates/root-AGENTS.md`
- Read: `docs/proposal/v1.4.x/project-skill-discovery-guard.md`
- Read: `docs/maintenance/full-validation-method.md`
- Protect: `docs/proposal/v1.4.x/post-merge-memory-reconciliation.md`

- [ ] **Step 1: Verify branch, HEAD, version, and dirty-work boundary**

Run:

```bash
git status --short --branch
git rev-parse HEAD
rg -n 'Version: 1\.4\.0|"version": "1\.4\.0"|Current version:\*\* 1\.4\.0|版本：\*\* 1\.4\.0' SKILL.md plugin.json README.md Usage.md
```

Expected:

- branch is `alpha/v1.4.0`;
- HEAD is `c022169` unless the human has explicitly accepted a newer baseline;
- `post-merge-memory-reconciliation.md`, the approved Proposal, and this plan are untracked/modified only as expected;
- every version-bearing surface remains `1.4.0`.

Stop if another dirty file overlaps an implementation surface or HEAD changed without human acknowledgement.

- [ ] **Step 2: Record protected-file checksum before implementation**

Run:

```bash
shasum -a 256 docs/proposal/v1.4.x/post-merge-memory-reconciliation.md
```

Expected: one SHA-256 line. Save it in the execution notes/response and compare it again at Task 8; do not edit the protected file.

- [ ] **Step 3: Re-count current shell tests**

Run:

```bash
find tests -maxdepth 1 -type f -name '*.sh' -print | sort
find tests -maxdepth 1 -type f -name '*.sh' | wc -l
```

Expected at plan-authoring time: `36`. The execution report must use the live count rather than this design-time number.

- [ ] **Step 4: Run the pre-change mechanical and test baseline**

Run:

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
git diff --check
```

Expected: every existing shell test and mechanical check passes before the new RED contract exists. If baseline tests fail for reasons unrelated to this proposal, stop and report them instead of mixing repairs.

### Task 1: Add Focused Contract And Capture RED

**Files:**
- Create: `tests/validate-project-skill-discovery-guard.sh`
- Create: `docs/reports/agent-loop-v1.4.0-project-skill-discovery-guard-red-baseline-2026-07-16.md`

- [ ] **Step 1: Add the focused contract before changing runtime rules**

Create `tests/validate-project-skill-discovery-guard.sh` with this contract:

```bash
#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

assert_contains() {
  local file=$1
  local text=$2
  if ! grep -Fq -- "$text" "$root/$file"; then
    fail "$file missing required text: $text"
  fi
}

assert_not_contains() {
  local file=$1
  local text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    fail "$file contains forbidden detail: $text"
  fi
}

assert_contains SKILL.md 'Project Skill Discovery Guard'
assert_contains references/runtime.md '## Project Skill Discovery Guard'
assert_contains references/design.md '## Project Skill Discovery Guard'
assert_contains references/project-skills.md '## Discovery Guard And Fallback Precedence'
assert_contains references/stage-guides.md 'Run Project Skill Discovery Guard before any stage-specific helper, generic fallback, command, tool call, temporary resource, or environment action.'
assert_contains references/workflow-checklists.md '## Project Skill Discovery Guard'
assert_contains references/project-guidance.md 'Before claiming no relevant project skill or entering a generic execution fallback'
assert_contains README.md 'runtime/global Skill inventory does not replace `.agent-loop/skills/INDEX.md`'
assert_contains Usage.md '项目 Skill 不一定显示在运行时原生 Skill 列表中'
assert_contains CHANGELOG.md '### Project Skill Discovery Guard'

for scenario in \
  'Active On-Demand Match Before Operational Fallback' \
  'Runtime Inventory Is Not Project Skill Inventory' \
  'Index Absent Allows Generic Method' \
  'No Active Match Avoids Full Body Scan' \
  'Inactive Skill Cannot Route' \
  'Manifest Drift Blocks Equivalent Fallback' \
  'Execution Gate Still Blocks Side Effects' \
  'Context Re-entry Rechecks Discovery' \
  'Same-Name Ownership Is Explicit' \
  'Chat Remains Lightweight'
do
  assert_contains references/validation-scenarios.md "### $scenario"
done

ruby - "$root/references/runtime.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
section = content[/^## Project Skill Discovery Guard\n(.*?)(?=^## |\z)/m, 1]
abort 'FAIL: runtime Project Skill Discovery Guard section missing' unless section
tokens = [
  'latest actionable intent / current stage',
  'inspect Project Skill INDEX metadata',
  'match active bootstrap / on-demand candidates',
  'verify exact INDEX row, path, and manifest',
  'read-only load the matched Project Skill',
  'Execution Gate',
  'stage action'
]
positions = tokens.map { |token| section.index(token) }
abort 'FAIL: runtime canonical discovery sequence is incomplete' if positions.any?(&:nil?)
abort 'FAIL: runtime canonical discovery sequence is reordered' unless positions == positions.sort
abort 'FAIL: fallback permission is missing' unless section.include?('Only `index-absent` or `no-active-match` permits generic fallback.')
abort 'FAIL: project-skill-drift must fail closed' unless section.include?('`project-skill-drift` fails closed')
RUBY

ruby - "$root/references/design.md" "$root/references/project-skills.md" <<'RUBY'
design = File.read(ARGV.fetch(0))
detail = File.read(ARGV.fetch(1))
required = [
  'runtime/global Skill inventory does not prove that no Project Skill exists',
  'Only `index-absent` or `no-active-match` permits generic fallback.',
  '`project-skill-drift` fails closed'
]
required.each do |text|
  abort "FAIL: design/reference contract missing: #{text}" unless design.include?(text) && detail.include?(text)
end
RUBY

reminder='Before claiming no relevant project skill or entering a generic execution fallback, check `.agent-loop/skills/INDEX.md`; if an active skill matches, load it read-only and keep the per-invocation Execution Gate.'
count=$(grep -Fo -- "$reminder" "$root/templates/root-AGENTS.md" | wc -l | tr -d ' ')
[ "$count" -eq 1 ] || fail "root AGENTS must contain the concise discovery reminder exactly once; found $count"

for forbidden in matched-active index-absent no-active-match project-skill-drift; do
  assert_not_contains templates/root-AGENTS.md "$forbidden"
done

ruby - "$root/templates/root-AGENTS.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
blocks = content.scan(/<!-- agent-loop:managed-start section:([^ ]+) .*?block-version:([^ ]+) -->/)
abort 'FAIL: root managed blocks missing' if blocks.empty?
abort "FAIL: expected 13 managed blocks, found #{blocks.length}" unless blocks.length == 13
blocks.each do |section, revision|
  expected = '1.4.0-20260716'
  abort "FAIL: #{section} expected #{expected}, found #{revision}" unless revision == expected
end
RUBY

if [ -e "$root/.agent-loop/skills" ]; then
  fail 'source repository must not contain downstream .agent-loop/skills artifacts'
fi

printf 'PASS: Project Skill Discovery Guard ordering, fallback, drift, root, and gate contract is complete\n'
```

- [ ] **Step 2: Run the new contract and verify RED**

Run:

```bash
bash tests/validate-project-skill-discovery-guard.sh
```

Expected: FAIL before any runtime/design repair, initially because `SKILL.md` does not contain `Project Skill Discovery Guard`. A different first missing surface is acceptable only if it proves the same pre-existing gap; record the exact output.

- [ ] **Step 3: Save the RED report**

Create `docs/reports/agent-loop-v1.4.0-project-skill-discovery-guard-red-baseline-2026-07-16.md` in Chinese with these completed sections:

```markdown
# Agent Loop v1.4.0 Project Skill Discovery Guard RED Baseline

## 审计对象

- 日期：2026-07-16
- 分支：alpha/v1.4.0
- 基线提交：c022169
- 审计对象：加入 focused test 后、修改 runtime/design 前的当前工作区

## 现有能力

记录 Project Entry/Resume/re-entry discovery、manifest validation 和 Execution Gate 已存在。

## RED 命令与实际失败

记录 `bash tests/validate-project-skill-discovery-guard.sh` 的完整实际失败输出和退出码。

## 缺口结论

说明现有规则没有把 Project Skill 检查变成 generic Operational Support/fallback 前的强制顺序，因此 runtime/global inventory 可能被错误解释为项目 Skill inventory。

## 非缺口

明确 Execution Gate、lifecycle、Load Policy、manifest 和项目路径本身不是本轮要重新设计的问题。

## 预期 GREEN

列出 matched-active、index-absent、no-active-match、project-skill-drift、root brevity 和 Execution Gate 的目标结果。
```

Use actual command output, live test count, branch, HEAD, and status evidence; do not copy a future GREEN result into the RED section.

### Task 2: Implement Core Controller And Authority Rules

**Files:**
- Modify: `SKILL.md`
- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Modify: `references/project-skills.md`

- [ ] **Step 1: Add the concise controller rule to `SKILL.md`**

Add one Required Runtime Behavior item after current Project Skill entry/re-entry discovery and one matching Stop And Ask condition. Preserve existing numbering style. The semantic content must be:

```text
Before a new actionable intent uses a generic helper, Code-Guided Operational Support fallback, or built-in stage method, run Project Skill Discovery Guard against the reliable memory root. Read INDEX metadata, match active bootstrap/on-demand candidates, verify only matched row/path/manifest, and load the match read-only. Runtime/global inventory alone cannot justify a negative Project Skill claim. Only index-absent or no-active-match permits generic fallback; project-skill drift stops before equivalent side effects.
```

Keep the existing per-invocation Execution Gate paragraph unchanged except for a short pointer to the guard. Do not add detailed result tables to `SKILL.md`.

- [ ] **Step 2: Add the executable canonical section to `references/runtime.md`**

Add `## Project Skill Discovery Guard` after Inspection Order and before Response Frame. Use this exact flow block so the focused test checks real ordering:

```text
latest actionable intent / current stage
-> inspect Project Skill INDEX metadata
-> match active bootstrap / on-demand candidates
-> verify exact INDEX row, path, and manifest
-> read-only load the matched Project Skill
-> Execution Gate
-> stage action

index-absent | no-active-match
-> runtime/global helper if applicable
-> generic Operational Support or Agent Loop fallback

project-skill-drift
-> fail closed
-> Recovery or Project Skill Creation / Update
```

The prose in the same section must include these exact contracts:

```text
Only `index-absent` or `no-active-match` permits generic fallback.
`project-skill-drift` fails closed and never authorizes an equivalent generic action.
runtime/global Skill inventory does not prove that no Project Skill exists.
```

Also coordinate:

- Inspection Order item 6b: INDEX metadata remains progressive; match on every applicable actionable intent, not only Project Entry/re-entry.
- Routing Axes/Precedence: the guard runs after reliable memory and intent/stage classification but before stage-specific method/fallback action.
- Code-Guided Operational Support routing paragraph: no generic operational action before the guard result.
- Existing active Project Skill paragraph: matched load still stops at Execution Gate.
- Auto-mode stop list and Stop conditions: add project-skill drift / undiscovered active match without creating a new gate.

- [ ] **Step 3: Add the durable invariant to `references/design.md`**

Add a core-constraints bullet and a `## Project Skill Discovery Guard` section before Entry Scenarios. It must state:

```text
runtime/global Skill inventory does not prove that no Project Skill exists.
Only `index-absent` or `no-active-match` permits generic fallback.
`project-skill-drift` fails closed and cannot be bypassed through an equivalent generic operation.
```

Define the result names as response-local judgments, not lifecycle states. Keep the Project Skill definition clear that discovery and loading are read-only while invocation authority remains the Execution Gate.

- [ ] **Step 4: Expand detailed discovery in `references/project-skills.md`**

Add `## Discovery Guard And Fallback Precedence` immediately after `## Discovery And Loading`. Include:

- applicability to new actionable intents and explicit Skill questions;
- ordinary chat exclusion;
- metadata-only scan before candidate match;
- body/manifest loading only for matched active rows;
- exact result meanings for `matched-active | index-absent | no-active-match | project-skill-drift`;
- negative discovery claim evidence;
- same-name runtime/project owner disclosure;
- context reuse and re-entry invalidation;
- the exact three contract sentences required by the focused test;
- no generic equivalent action after drift;
- the existing Execution Gate remains unchanged.

Do not add new INDEX fields, template files, persistent logs, cache files, or lifecycle values.

- [ ] **Step 5: Check the core authority sequence without claiming GREEN**

Run:

```bash
ruby -e 'runtime=File.read("references/runtime.md"); section=runtime[/^## Project Skill Discovery Guard\n(.*?)(?=^## |\z)/m, 1]; abort "missing guard" unless section; abort "missing order" unless section.index("inspect Project Skill INDEX metadata") < section.index("Execution Gate")'
rg -n 'Project Skill Discovery Guard|index-absent|no-active-match|project-skill-drift|runtime/global Skill inventory' SKILL.md references/runtime.md references/design.md references/project-skills.md
```

Expected: core authority contains the guard and ordered sequence. Do not call the feature GREEN yet because derived surfaces remain intentionally incomplete.

### Task 3: Coordinate Stage, Checklist, And Project-Guidance Surfaces

**Files:**
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/project-guidance.md`

- [ ] **Step 1: Guard Code-Guided Operational Support before its first method/action**

In `references/stage-guides.md`, add this sentence near the top of `## Code-Guided Operational Support`, before stage-specific reads or actions:

```text
Run Project Skill Discovery Guard before any stage-specific helper, generic fallback, command, tool call, temporary resource, or environment action.
```

Then specify:

- reliable memory is required before trusting INDEX claims;
- `matched-active` loads only the matched Skill and moves to Execution Gate;
- `index-absent | no-active-match` permits the existing read-only Operational Support method;
- drift stops rather than creating a temporary environment/resource through the generic path;
- read-only discovery itself writes no artifact.

Do not turn this into another stage or another Human Gate.

- [ ] **Step 2: Add a dedicated checklist**

Add `## Project Skill Discovery Guard` between Workflow Stage Routing and Project Entry in `references/workflow-checklists.md`:

```markdown
## Project Skill Discovery Guard

- [ ] Run only after the Agent Loop controller and reliable memory root are established.
- [ ] Before a new actionable intent uses a generic helper, Operational Support method, or built-in fallback, inspect `.agent-loop/skills/INDEX.md` metadata when present.
- [ ] Match only `active` bootstrap/on-demand rows by current intent, stage, task context, Triggers, and Scope.
- [ ] Verify only the matched exact INDEX row, path, instruction-bearing/executable files, and manifest before reliance.
- [ ] Load only the matched Skill body; do not scan all Project Skill bodies when no row matches.
- [ ] Treat runtime/global Skill inventory as a separate source that cannot prove no Project Skill exists.
- [ ] Permit generic fallback only for `index-absent | no-active-match`.
- [ ] Treat missing target, invalid row/manifest, unsafe path/symlink, or conflicting owner as `project-skill-drift` and fail closed.
- [ ] Emit the existing Execution Gate summary before following the matched workflow or causing side effects.
- [ ] Keep ordinary chat response-only and do not create a discovery cache, Feature, Requirement, or log artifact.
```

Also add a Project Entry checklist pointer so entry discovery and per-action guard are both visible without duplicating the section.

- [ ] **Step 3: Coordinate root-guidance ownership in `references/project-guidance.md`**

Update Root Agent Bootstrap Gate, stale-guidance criteria, and `Root AGENTS.md Should Contain` so root guidance must include exactly the concise reminder defined in Task 4. State that detailed result names, drift matrix, manifest procedure, and fallback contract belong in `references/project-skills.md`/runtime, not root AGENTS.

Do not add a new managed section; the reminder belongs in the existing `bootstrap` block.

- [ ] **Step 4: Run derived-surface inspection**

Run:

```bash
rg -n -C 3 'Project Skill Discovery Guard|generic fallback|project-skill-drift' references/stage-guides.md references/workflow-checklists.md references/project-guidance.md
```

Expected: stage action, checklist, and project-guidance ownership agree; full focused test may still fail until root/human docs are updated.

### Task 4: Update Root Bootstrap Reminder And Managed Revision

**Files:**
- Modify: `templates/root-AGENTS.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/validation-scenarios.md`
- Modify: `tests/validate-project-local-skills.sh`
- Modify: `tests/validate-root-agents-block-refresh.sh`
- Modify: `tests/validate-root-agents-block-checker.sh`
- Modify: `tests/test_root_agents_blocks.py`
- Modify: `tests/validate-v1.2.4-root-stage-coverage.sh`
- Modify: `tests/validate-requirement-lifecycle-backlog.sh`
- Modify: `tests/validate-branch-management-strategy.sh`
- Modify: `tests/validate-bug-management.sh`

- [ ] **Step 1: Add exactly one concise bootstrap reminder**

In `templates/root-AGENTS.md` Bootstrap Protocol, immediately after current Project Skill INDEX discovery item 9a, add exactly:

```text
Before claiming no relevant project skill or entering a generic execution fallback, check `.agent-loop/skills/INDEX.md`; if an active skill matches, load it read-only and keep the per-invocation Execution Gate.
```

Do not add the response result vocabulary, drift matrix, precedence table, or manifest procedure to root guidance.

- [ ] **Step 2: Refresh all 13 managed block revisions**

Change every current template marker from:

```text
block-version:1.4.0-20260715.1
```

to:

```text
block-version:1.4.0-20260716
```

Do not change the Skill version. Do not add a file-level version block or visible synced-version prose.

- [ ] **Step 3: Update only current-authority revision expectations**

Change the following current-template expectations to `1.4.0-20260716`:

- `references/workflow-checklists.md` example revisions;
- `references/validation-scenarios.md` scenarios that explicitly say “current root AGENTS template uses”;
- `tests/validate-project-local-skills.sh` template revision assertion;
- `tests/validate-root-agents-block-refresh.sh` `current_block_version` and example assertion;
- `tests/validate-root-agents-block-checker.sh` stale-rewrite input, expected revision, and generated marker fixtures;
- `tests/test_root_agents_blocks.py` stale replacement and generated marker fixtures;
- `tests/validate-v1.2.4-root-stage-coverage.sh` `expected_revision`;
- only the template assertion in `tests/validate-requirement-lifecycle-backlog.sh`;
- managed-block expectations in `tests/validate-branch-management-strategy.sh` and `tests/validate-bug-management.sh`.

Keep historical `CHANGELOG.md`, `docs/reports/`, and older Proposal statements for `1.4.0-20260715.1` unchanged. In `tests/validate-requirement-lifecycle-backlog.sh`, keep the assertion that historical Changelog evidence exists.

- [ ] **Step 4: Search for stale current-authority coupling**

Run:

```bash
rg -n '1\.4\.0-20260715\.1' --glob '!docs/reports/**' --glob '!docs/proposal/**' .
```

Expected after edits: only intentional historical Changelog evidence and tests that explicitly assert that history remain. Every active template/current-authority expectation uses `1.4.0-20260716`.

- [ ] **Step 5: Run root-guidance focused tests**

Run:

```bash
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-root-agents-block-refresh.sh
bash tests/validate-v1.2.4-root-stage-coverage.sh
python3 -m unittest tests.test_root_agents_blocks
```

Expected: all four commands PASS. If Python creates `__pycache__`, record it as validation-generated and remove only those generated cache directories before final status review.

### Task 5: Add Human Docs, Changelog, And Pressure Scenarios

**Files:**
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`
- Modify: `references/validation-scenarios.md`

- [ ] **Step 1: Clarify discovery in README**

In `## Project-Local Skills`, add this exact sentence and a short follow-up:

```text
The runtime/global Skill inventory does not replace `.agent-loop/skills/INDEX.md`.
```

Explain that Project Skills may not appear as runtime-native Skill chips, Agent Loop matches active INDEX metadata before generic fallback, loads only the matching Skill, and still stops at Execution Gate.

- [ ] **Step 2: Add a human-facing Usage example**

In `### 我想把常用流程做成项目技能`, add a row with the exact explanation:

```text
项目 Skill 不一定显示在运行时原生 Skill 列表中；Agent Loop 会在声称没有相关能力或进入通用执行 fallback 前检查 `.agent-loop/skills/INDEX.md`，只加载匹配的 active Skill，并继续保留本次 Execution Gate。
```

Include a user example such as “我没点名 Skill，但项目里已经有处理这个操作的 Skill 吗？” and make the expected Agent behavior read-only discovery first.

- [ ] **Step 3: Add the v1.4.0 Changelog entry**

Under `## 1.4.0 — 2026-07-15`, before earlier capability sections, add:

```markdown
### Project Skill Discovery Guard
- Required reliable projects to inspect `.agent-loop/skills/INDEX.md` before negative Project Skill claims or generic Operational Support/fallback actions.
- Kept discovery progressive by matching active INDEX metadata first and loading/verifying only the matched Skill, while preserving the per-invocation Execution Gate.
- Made `project-skill-drift` fail closed so missing paths, invalid manifests, unsafe owners, or conflicting Skill sources cannot be bypassed through equivalent generic actions.
- Refreshed all 13 root managed blocks to `block-version:1.4.0-20260716` and added ordering-aware focused regression without changing Skill version `1.4.0`.
```

Do not edit historical Bug/Branch entries.

- [ ] **Step 4: Add ten pressure scenarios under Project Skill section 68**

Add these named scenarios with prompt and Expected bullets matching the approved Proposal:

1. `Active On-Demand Match Before Operational Fallback` — active on-demand trigger matches; load/verify it before Operational Support and stop at Execution Gate.
2. `Runtime Inventory Is Not Project Skill Inventory` — native inventory has no match but INDEX does; no negative claim is allowed.
3. `Index Absent Allows Generic Method` — no INDEX; record `index-absent`, keep read-only generic support, create no empty directory.
4. `No Active Match Avoids Full Body Scan` — multiple rows but no active match; scan metadata only and permit fallback.
5. `Inactive Skill Cannot Route` — proposed/disabled/deprecated trigger matches; exclude from normal routing.
6. `Manifest Drift Blocks Equivalent Fallback` — missing/changed target; report drift and do not create temporary resources through a generic path.
7. `Execution Gate Still Blocks Side Effects` — matched Skill is loaded but not authorized; no command/tool/file/external action.
8. `Context Re-entry Rechecks Discovery` — after compaction or controller re-entry, re-read current metadata before relying on remembered results.
9. `Same-Name Ownership Is Explicit` — runtime/global and project-local same-name candidates; show owner/path and stop on conflict.
10. `Chat Remains Lightweight` — ordinary rule question; no full body scan, no cache, no artifact.

Every scenario must preserve Agent Loop controller precedence and avoid product-specific names in the canonical rule.

- [ ] **Step 5: Run the new focused contract for GREEN**

Run:

```bash
bash tests/validate-project-skill-discovery-guard.sh
```

Expected:

```text
PASS: Project Skill Discovery Guard ordering, fallback, drift, root, and gate contract is complete
```

If it fails, repair only the contract surface that contradicts the approved Proposal; do not weaken the test to accept an unordered or keyword-only implementation.

### Task 6: Run Focused GREEN And Cross-Feature Regression

**Files:**
- Update evidence only: `docs/reports/agent-loop-v1.4.0-project-skill-discovery-guard-red-baseline-2026-07-16.md` only if the RED command metadata was recorded incorrectly; do not rewrite the historical RED result as GREEN.

- [ ] **Step 1: Run directly affected tests**

Run:

```bash
bash tests/validate-project-skill-discovery-guard.sh
bash tests/validate-project-local-skills.sh
bash tests/validate-operational-support-guard.sh
bash tests/validate-mandatory-helper-routing.sh
bash tests/validate-skill-reentry-guidance.sh
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-root-agents-block-refresh.sh
bash tests/validate-v1.2.4-root-stage-coverage.sh
bash tests/validate-requirement-lifecycle-backlog.sh
bash tests/validate-branch-management-strategy.sh
bash tests/validate-bug-management.sh
bash tests/validate-human-help-version-docs.sh
python3 -m unittest tests.test_root_agents_blocks
```

Expected: every command exits 0. The new test prints its exact PASS line; existing tests retain their current PASS summaries.

- [ ] **Step 2: Inspect the cross-surface invariant manually**

Verify with line-number evidence:

```bash
rg -n 'Project Skill Discovery Guard|runtime/global Skill inventory|index-absent|no-active-match|project-skill-drift|generic execution fallback|Execution Gate' SKILL.md references/runtime.md references/design.md references/project-skills.md references/stage-guides.md references/workflow-checklists.md references/project-guidance.md templates/root-AGENTS.md README.md Usage.md CHANGELOG.md references/validation-scenarios.md
```

Expected semantic conclusion:

- controller/memory recovery remains first;
- active project-local match precedes runtime/global helper and generic fallback;
- only absent/no-match allows fallback;
- drift blocks equivalent side effects;
- matched load still waits at Execution Gate;
- root guidance remains a one-line router;
- chat remains response-only.

- [ ] **Step 3: Confirm source boundary and protected work**

Run:

```bash
test ! -e .agent-loop/skills
shasum -a 256 docs/proposal/v1.4.x/post-merge-memory-reconciliation.md
git status --short
```

Expected: no source `.agent-loop/skills`, protected checksum matches Task 0, and status contains only intended implementation files plus the untouched unrelated proposal.

### Task 7: Execute Full Validation And Write Chinese Report

**Files:**
- Create: `docs/reports/agent-loop-v1.4.0-project-skill-discovery-guard-full-validation-2026-07-16.md`

- [ ] **Step 1: Re-count and run every shell regression**

Run:

```bash
test_count=$(find tests -maxdepth 1 -type f -name '*.sh' | wc -l | tr -d ' ')
printf 'shell test count: %s\n' "$test_count"
passed=0
for test_file in tests/*.sh; do
  bash "$test_file"
  passed=$((passed + 1))
done
printf 'shell tests passed: %s/%s\n' "$passed" "$test_count"
```

Expected at plan-authoring time after adding the new test: `37/37`. Report the live count even if it differs because of separately approved concurrent changes.

- [ ] **Step 2: Run repository mechanical checks**

Run:

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
find . -name '*.json' -type f -print0 | xargs -0 -n1 ruby -rjson -e 'JSON.parse(File.read(ARGV.fetch(0)))'
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
find . -name '*.rb' -type f -print0 | xargs -0 -n1 ruby -c
ruby -e 'bad=[]; Dir.glob("**/*.md", File::FNM_DOTMATCH).reject { |p| p.start_with?(".git/") }.each do |p|; open=nil; File.foreach(p).with_index(1) do |line,n|; if (m=line.match(/^\s*(`{3,}|~{3,})/)); mark=m[1][0]; if open.nil?; open=[mark,n]; elsif open[0]==mark; open=nil; end; end; end; bad << "#{p}:#{open[1]}" if open; end; abort "unbalanced markdown fences: #{bad.join(", ")}" unless bad.empty?'
git diff --check
```

Expected: all commands exit 0. Also check the two new untracked Markdown files and new shell test for trailing whitespace because `git diff --check` does not inspect untracked content until staged:

```bash
! rg -n '[[:blank:]]+$' tests/validate-project-skill-discovery-guard.sh docs/proposal/v1.4.x/project-skill-discovery-guard.md docs/proposal/v1.4.x/project-skill-discovery-guard-implementation-plan.md docs/reports/agent-loop-v1.4.0-project-skill-discovery-guard-red-baseline-2026-07-16.md docs/reports/agent-loop-v1.4.0-project-skill-discovery-guard-full-validation-2026-07-16.md
```

- [ ] **Step 3: Perform the six-domain semantic audit**

Apply `docs/maintenance/full-validation-method.md` to the current workspace and assess:

- Logic Correctness — discovery order, negative claim proof, drift fail-closed, no gate bypass;
- Autonomy — Agent checks INDEX without waiting for the human to remember the Skill;
- Project Entry / Onboarding — entry/re-entry discovery remains reliable without making chat heavy;
- Development / Test Workflow — mandatory helpers and Operational Support remain compatible;
- Memory — INDEX remains the only discovery index; no new cache/artifact/status;
- Recommendation — matched, absent/no-match, and drift each yield one unambiguous next action.

Re-run representative full-method pressure scenarios in addition to the ten focused scenarios. Record file/line evidence, passed invariants, unresolved Medium/Low risks, and the final weighted score. Any Critical or unexplained High blocks completion.

- [ ] **Step 4: Write the Chinese full-validation report**

Create `docs/reports/agent-loop-v1.4.0-project-skill-discovery-guard-full-validation-2026-07-16.md` with:

1. date, branch, version, HEAD, and current-workspace audit boundary;
2. protected unrelated dirty work;
3. RED baseline command/output and why it proves the original loophole;
4. GREEN focused command/output;
5. live affected-test and all-shell-test counts;
6. YAML/JSON/Shell/Ruby/Markdown/diff check results;
7. six-domain scores and overall STRONG/STABLE/FRAGILE/BROKEN grade;
8. ten focused pressure scenarios and representative full-method scenarios;
9. Proposal acceptance-criteria mapping;
10. remaining risk, design drift, and rollback/stop findings;
11. explicit statement that no commit, push, tag, PR, merge, release, publish, or installed-Skill sync occurred.

Do not reuse a prior report score or test count.

- [ ] **Step 5: Clean only validation-generated cache and rerun hygiene**

If Python tests created `__pycache__` directories under `scripts/` or `tests/`, compare with Task 0 and remove only the newly generated caches. Then run:

```bash
git status --short --branch
git diff --stat
git diff --check
find . -path './.agent-loop' -o -path './.agent-loop/*'
```

Expected: no `.agent-loop` artifact, no new generated cache, no whitespace errors, and only intended files plus the untouched unrelated proposal.

### Task 8: Proposal Compliance And Human Review Stop

**Files:**
- Modify after all validation passes: `docs/proposal/v1.4.x/project-skill-discovery-guard.md`
- Read: every changed file and report

- [ ] **Step 1: Update Proposal implementation state only after GREEN/full validation**

Change the Proposal status to:

```text
状态：Proposal 已批准，实施与验证完成，待 Human Review
```

Do not change the approved design body unless an implementation conflict was separately reviewed by the human. If the design had to drift, stop instead of silently rewriting the Proposal.

- [ ] **Step 2: Run final Proposal acceptance mapping**

For each Proposal acceptance criterion, name the implementing file(s), focused assertion/scenario, and validation evidence. Confirm explicitly:

- discovery-before-fallback exists;
- runtime/global inventory is distinct;
- negative claim requires project INDEX evidence;
- progressive load is preserved;
- drift fails closed;
- Execution Gate is unchanged;
- chat remains lightweight;
- no stage/intent/status/cache/schema/version/global-install expansion occurred;
- root guidance contains only the short reminder;
- source repository has no target-project `.agent-loop/skills/`.

- [ ] **Step 3: Review the final diff and protected checksum**

Run:

```bash
git status --short --branch
git diff --stat
git diff --check
shasum -a 256 docs/proposal/v1.4.x/post-merge-memory-reconciliation.md
```

Expected: checksum matches Task 0; no unrelated file was modified; no Git submission action occurred.

- [ ] **Step 4: Stop at Human Review Summary**

Return a table-first Human Review Summary containing:

- actual changed-file list;
- RED → GREEN evidence;
- focused validation commands/results;
- full validation count, score, and report link;
- Proposal acceptance mapping;
- remaining risks and design drift;
- current `git status` and diff summary;
- explicit `not committed / not pushed / not tagged / not published` statement;
- exactly one recommendation: human reviews the implementation and decides whether to authorize Submit / Integrate checks.

Do not stage or commit after presenting the summary.

## Rollback Strategy

Before Human Review, rollback is manual and scope-bounded:

1. remove only the new focused test and two new reports if the human rejects the capability;
2. revert only the guard-related hunks in core/derived surfaces;
3. restore root template/current-authority tests from revision `1.4.0-20260716` to `1.4.0-20260715.1` only if the short reminder is also removed;
4. leave all historical Changelog/proposal/report evidence and the unrelated post-merge-memory proposal untouched;
5. rerun the pre-change affected tests and mechanical checks;
6. do not use `git reset --hard`, `git checkout --`, or broad file restoration.

Rollback must not be performed merely because a test fails; diagnose the failure first. Stop and ask when rollback would overlap unrelated human edits.

## Plan Completion Gate

This plan is ready for implementation only after the human explicitly approves it. Approval authorizes Task 0–8 Agent-ready file/test/report work in the current source repository, but it does not authorize subagents, worktrees, branches, staging, commit, push, tag, PR, merge, release, publish, version change, global installation, or installed-Skill synchronization.

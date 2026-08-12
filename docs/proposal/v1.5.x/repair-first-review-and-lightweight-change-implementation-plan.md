# Repair-First Review Repair And Lightweight Change Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use `executing-plans` to implement this plan task-by-task. `subagent-driven-development` may be used only after a separate Human authorization; this plan does not authorize subagent dispatch.

**Status:** Tasks 0–9 complete; Human Review accepted; released as `stable-v1.5.5` with disclosed accepted risks

**Target:** Agent Loop `1.5.5` on branch `v1.5.5`

**Release closure:** Task 6 中 `development` / `stable-v1.5.4` 的值是正式 Release Gate 前的实施约束。2026-08-12 人类在阅读定向复核 findings 后接受剩余风险并授权发布；当前 README/Usage/CHANGELOG 以 `stable-v1.5.5` 为准，`main` 同步仍是独立 Gate。

**Planning baseline:** `f9c5569d93f6e42457b12fa2925a95373bea0cb9`

**Design authority:** `docs/proposal/v1.5.x/repair-first-review-and-lightweight-change.md`

**Goal:** make bounded Feature Review repairs and clearly eligible Lightweight Changes default to repair first, fresh verification second, and a specific post-repair regression-test recommendation, while preserving required verification, accepted test obligations, TDD for initial Feature and explicit Bug execution, and every existing Human Gate.

**Architecture:** publish one shared `Repair-First Verification` invariant in `references/design.md` and `references/runtime.md`; specialize it inside Review and Lightweight Change without adding a stage, status, mode, Checker, or artifact tree. Existing Feature artifacts and Lightweight Execution Cards retain ownership. Focused contract tests enforce route order, scope exits, completion truthfulness, helper boundaries, version synchronization, and mutation resistance; full validation then re-audits all six repository domains.

**Tech Stack:** Markdown runtime/reference/template contracts; Bash and Ruby contract tests; existing Python 3.10+ standard-library Checkers and unit tests; repository YAML/JSON/Shell/Python/Markdown mechanical validation.

**Evidence:** [RED baseline](../../reports/agent-loop-v1.5.5-repair-first-red-baseline-2026-08-12.md); [v1.5.5 full validation](../../reports/agent-loop-v1.5.5-full-validation-2026-08-12.md); [pre-release cross-path validation](../../reports/agent-loop-v1.5.5-pre-release-full-validation-2026-08-12.md). Task execution itself stopped without Git or release actions; the later Human Review and Release Gate authorized the release closure recorded above. Installation, installed-Skill synchronization, PR, merge, and `main` synchronization remain unperformed.

---

## 1. Non-Negotiable Semantic Boundaries

Implementation must preserve all of the following. Any task that cannot preserve them stops before further production-rule edits and returns to Human Review.

1. Repair-First applies only to:
   - a Feature Review finding classified `within-approved-boundary` with current Feature write authorization; or
   - a `clearly eligible` Lightweight Change after its persistent Card exists.
2. The default order for those two paths is:

   ```text
   bounded write
   -> fresh targeted verification
   -> affected existing checks
   -> diff / scope / risk / rollback review
   -> evidence
   -> specific Regression Test Advisory
   ```

3. Repair-First does not authorize a write. It consumes only the existing Feature execution grant or the exact bounded Lightweight request/Card scope.
4. `Required Verification`, `Existing Test Obligation`, and `Additional Regression Test` remain distinct:
   - Required Verification proves the current result and cannot be omitted;
   - Existing Test Obligation comes from accepted `tests.md`, Gate 2, acceptance, ADR, Contract, Bug Verification Matrix, or a Human instruction and cannot be downgraded;
   - Additional Regression Test protects a future change and is advisory after current proof exists.
5. An unaccepted Additional Regression Test Advisory does not by itself block Task Done, Lightweight completion, or Feature Close.
6. When current correctness cannot be proved without a new test, the Agent must not claim `fixed`, `done`, `completed`, or `closed`; it recommends the exact test and waits at the existing Human Review.
7. Feature initial Execute Task / Story, explicit Human-Guided Bug Management repair, Human-requested TDD, and accepted Plans that require RED/GREEN retain TDD.
8. Review findings that change product meaning, Feature definition, acceptance, implementation boundary, public interface, ADR, Contract, security, data, permission, dependency, migration, architecture, external action, or authorization leave the fast path and return to the existing owner.
9. Lightweight eligibility, persistent Card creation before target writes, scope-expansion stop, rollback, memory review, and independent Git/external/production gates remain unchanged.
10. No canonical stage, message intent, status, lifecycle, Auto Mode, Human Gate, Checker outcome, default directory, test-debt backlog, or parser state is added.
11. Product, Requirement, ADR, Delivery Contract, Bug, Feature Gate 1/2, Task Done, Submit, Close, Git, Release, Project Skill, subagent, external, and production Human Gates remain independent.
12. The source repository must not create a target-project `.agent-loop/` workspace.
13. The Skill version becomes `1.5.5`, but no stable tag, release claim, installed-Skill synchronization, commit, or push occurs in this plan.

---

## 2. Verified Planning Boundary

The following was observed while writing this plan on 2026-08-12. Task 0 must rerun every fact because implementation cannot rely on stale planning evidence.

| Check | Planning observation |
|---|---|
| Branch | `v1.5.5` |
| HEAD | `f9c5569d93f6e42457b12fa2925a95373bea0cb9` |
| Tracked diff | none observed |
| Cached diff | none observed |
| Expected untracked design | Proposal and this Implementation Plan |
| Expected unrelated untracked | `.tmp/`, `scripts/__pycache__/`, `tests/__pycache__/` |
| Current top-level Shell test files | `49` |
| Current top-level Python test files | `22` |
| Current root template lines | `176` |
| Current managed blocks | `13`, revision `1.5.4-20260810.1` |

The three unrelated cache/temp directories must not be deleted, restored, staged, committed, or used as validation evidence. Any new dirty path outside the approved file map must be classified before implementation continues.

---

## 3. Expected File Map

### 3.1 New files

- `tests/validate-repair-first-verification.sh` — focused cross-surface and mutation-resistant contract for route order, TDD exceptions, required/advisory distinction, completion, no-new-state, and v1.5.5 synchronization.
- `docs/reports/agent-loop-v1.5.5-repair-first-red-baseline-2026-08-12.md` — Chinese RED evidence captured before runtime/design changes.
- `docs/reports/agent-loop-v1.5.5-full-validation-2026-08-12.md` — Chinese focused/full/mechanical/six-domain validation report.

### 3.2 Core published authority

- `SKILL.md` — concise controller statement: TDD remains default for initial Feature/explicit Bug execution; Review Repair and Lightweight use Repair-First.
- `references/runtime.md` — executable owner of route, authorization, stop, Task Done, completion, and helper boundaries.
- `references/design.md` — core model and definitions for Repair-First, Review Repair Fast Path, Regression Test Advisory, and the three evidence responsibilities.

### 3.3 Detailed runtime/reference surfaces

- `references/lightweight-change-lane.md` — replace mandatory targeted RED/minimal GREEN with repair-first verification and post-repair advisory.
- `references/stage-guides.md` — coordinate Execute, Diagnose, Verify, Review, Drift, and Close behavior.
- `references/workflow-checklists.md` — make checklist applicability explicit and keep existing obligations hard.
- `references/skill-routing.md` — prevent TDD helper resolution from re-entering Review Repair or Lightweight.
- `references/external-skill-adapters.md` — scope TDD Adapter to formal execution paths and keep Review helper ownership.
- `references/human-review-summary.md` — add compact repair/verification/advisory/residual presentation.
- `references/feature-completion-check.md` — distinguish required tests from optional additional regression advice.
- `references/project-guidance.md` — keep only the root projection/refresh contract and one concise downstream reminder.
- `references/validation-scenarios.md` — add the Proposal pressure matrix and rename the obsolete Lightweight RED/GREEN scenario.

### 3.4 Templates

- `templates/lightweight-execution-card.md` — Plan verifies after write and Result/Residuals records specific regression advice without a debt state.
- `templates/notes.md` — add one Review Repair Evidence table inside existing notes ownership.
- `templates/root-AGENTS.md` — add only a concise Review/Lightweight ownership reminder and refresh all 13 revisions to `1.5.5-20260812.1`; keep the file at or below 190 lines.

### 3.5 Maintainer validation guidance

- `docs/maintenance/full-validation-method.md` — replace the obsolete universal “behavior change cannot skip RED” invariant with the scoped v1.5.5 contract.
- `docs/maintenance/feature-validation-method.md` — require focused testing to distinguish current proof from future regression advice when this capability is evaluated.

### 3.6 Human docs and metadata

- `README.md` — explain current development capability without claiming a stable `1.5.5` tag exists.
- `Usage.md` — add human trigger/example wording and current development version.
- `CHANGELOG.md` — create an unreleased/in-progress `1.5.5` section and preserve all historical sections byte-semantically.
- `plugin.json` — set `1.5.5` and describe adaptive Repair-First accurately.
- `agents/openai.yaml` — remove the false universal “TDD is default” prompt and state scoped applicability.
- `references/submit-and-integrate.md` — update only the current-version commit-message example to `v1.5.5`.

### 3.7 Tests expected to change

- `tests/validate-lightweight-change-lane.sh`
- `tests/validate-feature-construction-two-gate-review.sh`
- `tests/test_feature_review.py`
- `tests/validate-maintainer-full-validation-guidance.sh`
- `tests/validate-feature-validation-method.sh`
- `tests/validate-root-agents-block-refresh.sh`
- `tests/validate-root-agents-block-checker.sh`
- `tests/validate-v1.2.4-root-stage-coverage.sh`
- `tests/test_root_agents_blocks.py`
- `tests/test_root_agents_lossless_slimming.py`
- `tests/validate-bug-management.sh`
- `tests/validate-branch-management-strategy.sh`
- `tests/validate-project-skill-discovery-guard.sh`
- `tests/validate-project-local-skills.sh`
- `tests/validate-requirement-lifecycle-backlog.sh`
- `tests/validate-human-help-version-docs.sh`

Historical Proposal/report assertions that intentionally prove the released `stable-v1.5.4` work remain unchanged. Fixture values such as a Feature target release `v1.5.4` remain unchanged unless they are actually current-version metadata.

---

## 4. Rollback And Stop Conditions

### Rollback

- Before Task 2, production runtime/reference/template files remain unchanged; deleting the new focused test and RED report restores the planning state.
- After Task 2, rollback is the inverse patch limited to files listed in Section 3. Never use `git reset --hard`, `git checkout --`, or broad restore commands.
- If a validation repair is needed, patch only the owning rule or test. Do not restore unrelated user work.
- Reports and Proposal/Plan status are refreshed only after their evidence exists; never fabricate pass evidence to simplify rollback.

### Immediate stop

Stop and return to Human Review if any of these occurs:

- Proposal and current runtime reality require different semantics;
- implementation would make initial Feature or explicit Bug repair default Repair-First;
- implementation would make fresh verification optional;
- accepted Gate 2/acceptance/ADR/Contract/Bug tests would become advisory;
- implementation needs a new stage, intent, status, mode, Gate, Checker, directory, parser state, dependency, or executable database;
- root guidance would exceed 190 lines or need the complete algorithm;
- a version other than `1.5.5` or a root revision other than `1.5.5-20260812.1` is required;
- unrelated dirty work overlaps an affected path;
- focused RED is not real, or focused/full validation repeatedly fails without a proven cause;
- implementation would require a subagent, worktree, branch change, installed-Skill sync, commit, push, tag, PR, merge, release, publish, production, external, or destructive action without separate authorization.

---

## Task 0: Reconfirm Authority, Dirty Work, And Existing Full Baseline

**Files:**

- Read: `AGENTS.md`
- Read: `docs/proposal/v1.5.x/repair-first-review-and-lightweight-change.md`
- Read: `docs/proposal/v1.5.x/repair-first-review-and-lightweight-change-implementation-plan.md`
- Read: `SKILL.md`
- Read: `references/runtime.md`
- Read: `references/design.md`
- Read: every file in Section 3 before editing its owning Task
- Read: `docs/maintenance/full-validation-method.md`
- Modify after explicit implementation authorization only: Proposal and Plan status lines

- [x] **Step 1: Confirm execution authorization and exact Git boundary**

Run:

```bash
git branch --show-current
git rev-parse HEAD
git status --short --branch
git diff --stat
git diff --cached --stat
find tests -maxdepth 1 -type f -name '*.sh' | sort | wc -l
find tests -maxdepth 1 -type f -name 'test_*.py' | sort | wc -l
```

Expected before source edits:

- branch `v1.5.5`;
- HEAD `f9c5569d93f6e42457b12fa2925a95373bea0cb9` unless the human explicitly supplies a new accepted baseline;
- no tracked or cached diff;
- only Proposal, Plan, `.tmp/`, and the two `__pycache__/` trees are untracked;
- `49` Shell files and `22` Python test modules are discovered.

If the branch, HEAD, tracked diff, cached diff, or untracked ownership differs, stop and report exact evidence.

- [x] **Step 2: Read all authorities completely**

Read the files named above and record the current conflicting clauses:

```bash
rg -n 'TDD|RED|GREEN|behavior-changing|smallest meaningful|targeted RED|Review|Task Done|Feature Close|required tests|substitute verification' \
  SKILL.md references/runtime.md references/design.md \
  references/lightweight-change-lane.md references/stage-guides.md \
  references/workflow-checklists.md references/skill-routing.md \
  references/external-skill-adapters.md references/human-review-summary.md \
  references/feature-completion-check.md templates/lightweight-execution-card.md \
  templates/notes.md docs/maintenance/full-validation-method.md
```

Expected: current sources still require the smallest RED/GREEN for isolated Lightweight behavior and broadly require TDD for behavior-changing Execute.

- [x] **Step 3: Run the existing full executable baseline before adding RED**

Run:

```bash
set -euo pipefail
shell_total=0
for test_file in tests/*.sh; do
  bash "$test_file"
  shell_total=$((shell_total + 1))
done
printf 'SHELL_PASS=%s\n' "$shell_total"

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: every existing Shell and Python test passes. Record live test counts and duration; do not reuse historical report totals. If the existing baseline fails, stop before Task 1.

- [x] **Step 4: Run the existing mechanical baseline**

Run:

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
ruby -rjson -e 'JSON.parse(File.read("plugin.json"))'
find . -name '*.sh' -type f -not -path './.git/*' -print0 | xargs -0 -n1 bash -n
find . -name '*.py' -type f -not -path './.git/*' -not -path '*/__pycache__/*' -print0 | \
  xargs -0 python3 -c 'import ast, pathlib, sys; [ast.parse(pathlib.Path(p).read_text(encoding="utf-8")) for p in sys.argv[1:]]'
git diff --check
```

Expected: all commands exit `0`.

- [x] **Step 5: Mark design artifacts as approved for implementation only after the human has approved this Plan**

Use these exact status meanings:

```markdown
Proposal status: Human Review accepted; implementation in progress
Implementation Plan status: Human Review accepted; Task 0 in progress
```

Do not mark either file implemented or validated.

---

## Task 1: Add Focused Contract And Preserve Genuine RED

**Files:**

- Create: `tests/validate-repair-first-verification.sh`
- Create: `docs/reports/agent-loop-v1.5.5-repair-first-red-baseline-2026-08-12.md`
- Do not modify runtime/reference/template production files in this Task

- [x] **Step 1: Create the focused contract test**

Create `tests/validate-repair-first-verification.sh` with this complete content:

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
  local file=$1 text=$2
  grep -Fq -- "$text" "$root/$file" || fail "$file missing Repair-First contract: $text"
}

assert_not_contains() {
  local file=$1 text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    fail "$file contains forbidden Repair-First behavior: $text"
  fi
}

for file in \
  SKILL.md \
  references/runtime.md \
  references/design.md \
  references/lightweight-change-lane.md \
  references/stage-guides.md \
  references/workflow-checklists.md \
  references/skill-routing.md \
  references/external-skill-adapters.md \
  references/human-review-summary.md \
  references/feature-completion-check.md \
  templates/lightweight-execution-card.md \
  templates/notes.md; do
  assert_file "$file"
done

assert_contains references/runtime.md 'Repair-First Verification'
assert_contains references/runtime.md 'Review Repair Fast Path'
assert_contains references/runtime.md 'Required Verification'
assert_contains references/runtime.md 'Existing Test Obligation'
assert_contains references/runtime.md 'Additional Regression Test'
assert_contains references/runtime.md 'does not by itself block Task Done, Lightweight Change completion, or Feature Close'
assert_contains references/runtime.md 'do not claim `fixed`, `done`, `completed`, or `closed`'

assert_contains references/design.md '**Repair-First Verification**'
assert_contains references/design.md '**Review Repair Fast Path**'
assert_contains references/design.md '**Regression Test Advisory**'

assert_contains references/lightweight-change-lane.md '## Repair-First Verification'
assert_contains references/lightweight-change-lane.md 'apply the disclosed bounded change first'
assert_contains references/lightweight-change-lane.md 'run fresh targeted verification after the write'
assert_contains references/lightweight-change-lane.md 'Regression Test Advisory'
assert_not_contains references/lightweight-change-lane.md '-> targeted RED'
assert_not_contains references/lightweight-change-lane.md '-> minimal GREEN'
assert_not_contains references/lightweight-change-lane.md 'Do not use “lightweight” to skip a meaningful RED/GREEN for an isolatable behavior branch.'

assert_contains references/stage-guides.md '### Review Repair Fast Path'
assert_contains references/stage-guides.md 'repair the implementation first'
assert_contains references/stage-guides.md 'return to Gate 1, Gate 2, Decision & Design, Delivery Contract, Bug Management, Diagnose Failure, or the applicable Human Gate'
assert_contains references/workflow-checklists.md 'Classify the finding as `within-approved-boundary` before a Review Repair write.'
assert_contains references/workflow-checklists.md 'Do not downgrade an Existing Test Obligation into a Regression Test Advisory.'

assert_contains references/skill-routing.md 'Review Repair Fast Path and Lightweight Change Lane do not invoke the TDD helper by default.'
assert_contains references/external-skill-adapters.md 'The TDD Adapter remains mandatory for initial Feature execution and explicit Bug repair, not for Review Repair Fast Path or clearly eligible Lightweight Change.'

assert_contains references/human-review-summary.md '## Review Repair And Regression Test Advisory'
assert_contains references/feature-completion-check.md 'An unaccepted Additional Regression Test Advisory does not by itself block Feature close.'
assert_contains templates/lightweight-execution-card.md 'Record a specific Regression Test Advisory or a concrete not-needed reason'
assert_contains templates/notes.md '## Review Repair Evidence'

for scenario in \
  'Review Repair Fixes Before New Test' \
  'Review Repair Reuses Existing Coverage' \
  'Review Repair Without Reliable Verification Cannot Complete' \
  'Review Repair Product Drift Returns To Owning Gate' \
  'Review Repair Without Authorization Does Not Write' \
  'Lightweight Logic Change Repairs Before Verification' \
  'Existing Test Obligation Cannot Become Advisory' \
  'Additional Regression Advisory Does Not Block Completion' \
  'Human Adds Regression Test After Repair' \
  'Regression Advice Is Specific And Batched' \
  'Explicit Bug Repair Keeps TDD' \
  'Initial Feature Execution Keeps TDD'; do
  assert_contains references/validation-scenarios.md "### $scenario"
done

ruby - "$root/references/runtime.md" "$root/references/stage-guides.md" <<'RUBY'
runtime = File.read(ARGV.fetch(0))
guides = File.read(ARGV.fetch(1))

def h2(content, heading)
  marker = "## #{heading}"
  lines = content.lines
  start = lines.index { |line| line.chomp == marker }
  abort "FAIL: missing owning section #{marker}" unless start
  finish = ((start + 1)...lines.length).find { |index| lines[index].start_with?('## ') } || lines.length
  lines[start...finish].join
end

def ordered?(content, tokens)
  positions = tokens.map { |token| content.index(token) }
  positions.none?(&:nil?) && positions == positions.sort
end

repair_tokens = [
  'within-approved-boundary',
  'repair the implementation first',
  'fresh targeted verification',
  'affected existing checks',
  'Regression Test Advisory'
]

review = h2(guides, 'Review')
abort 'FAIL: Review Repair order is missing or reversed' unless ordered?(review, repair_tokens)

task_done = h2(runtime, 'Task Done Gate')
required = [
  'Required Verification',
  'Existing Test Obligation',
  'Additional Regression Test',
  'does not by itself block Task Done'
]
abort 'FAIL: Task Done does not distinguish required and advisory evidence' unless required.all? { |token| task_done.include?(token) }

mutations = {
  'missing fresh verification' => review.sub('fresh targeted verification', 'optional verification'),
  'missing advisory' => review.sub('Regression Test Advisory', 'silent completion'),
  'reversed write and proof' => review.sub('repair the implementation first', 'verify before any repair')
}
mutations.each do |name, mutated|
  abort "FAIL: mutation survived: #{name}" if ordered?(mutated, repair_tokens)
end
RUBY

ruby - "$root/references/runtime.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
intent = content[/^## Message Intent Classification\n(.*?)(?=^## |\z)/m, 1]
stage_order = content[/^## Stage Order\n(.*?)(?=^## |\z)/m, 1]
abort 'FAIL: Message Intent section missing' unless intent
abort 'FAIL: Stage Order section missing' unless stage_order
abort 'FAIL: Review Repair became a message intent' if intent.include?('`review-repair`')
abort 'FAIL: Repair-First became a canonical stage' if stage_order.lines.map(&:strip).include?('Repair-First Verification')
abort 'FAIL: Review Repair became a canonical stage' if stage_order.lines.map(&:strip).include?('Review Repair Fast Path')
RUBY

for forbidden in \
  '.agent-loop/review-repairs/' \
  '.agent-loop/test-debt/' \
  'Test Debt Status:' \
  'Review Repair Status:'; do
  for file in references/runtime.md references/design.md templates/notes.md templates/lightweight-execution-card.md; do
    assert_not_contains "$file" "$forbidden"
  done
done

assert_contains SKILL.md 'Version: 1.5.5'
assert_contains plugin.json '"version": "1.5.5"'
assert_contains README.md '**Current version:** 1.5.5'
assert_contains Usage.md '**版本：** 1.5.5'
assert_contains CHANGELOG.md '## 1.5.5 — 2026-08-12'

ruby - "$root/templates/root-AGENTS.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
blocks = content.scan(/<!-- agent-loop:managed-start section:([^ ]+) .*?block-version:([^ ]+) -->/)
abort "FAIL: expected 13 root managed blocks, found #{blocks.length}" unless blocks.length == 13
blocks.each do |section, revision|
  expected = '1.5.5-20260812.1'
  abort "FAIL: #{section} expected #{expected}, found #{revision}" unless revision == expected
end
abort 'FAIL: root AGENTS exceeds 190 lines' if content.lines.length > 190
RUBY

[ ! -d "$root/.agent-loop" ] || fail 'source repository must not contain target-project .agent-loop artifacts'

printf 'PASS: Repair-First Review Repair and Lightweight Change contract is complete\n'
```

- [x] **Step 2: Run the focused contract and verify genuine RED**

Run:

```bash
bash tests/validate-repair-first-verification.sh
```

Expected: non-zero with the first unmet production contract, normally:

```text
FAIL: references/runtime.md missing Repair-First contract: Repair-First Verification
```

The RED must not fail first because of Shell syntax, a missing test helper, version-only mismatch, or an unrelated dirty file.

- [x] **Step 3: Save the Chinese RED report**

The report must contain these actual headings and evidence, filled from Task 0/1 output:

```markdown
# Agent Loop v1.5.5 Repair-First RED Baseline

## 审计对象
## 工作区边界
## 既有全量基线
## Focused RED 命令与退出状态
## 当前错误路径
## Proposal 需要的 GREEN
## 未修改的生产文件
## 剩余风险
```

Record the exact command, exit code, first failure, existing Shell/Python totals, and the current conflicting source lines. State that no runtime/design/reference/template behavior was modified before RED.

- [x] **Step 4: Confirm the new test itself is mechanically valid**

Run:

```bash
bash -n tests/validate-repair-first-verification.sh
git diff --check
```

Expected: both exit `0`; the focused behavior test remains RED.

---

## Task 2: Publish The Core Repair-First Runtime And Design Invariant

**Files:**

- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Modify: `SKILL.md` behavior wording only; version is Task 6

- [x] **Step 1: Add the authoritative runtime method without changing Stage Order**

Add a `## Repair-First Verification` section in `references/runtime.md` after Lightweight routing and before unrelated product-definition internals. Use these exact contracts:

```markdown
Repair-First Verification is the default internal method for a `within-approved-boundary` Review repair and a `clearly eligible` Lightweight Change. It is not a canonical stage, message intent, status, Auto Mode, Human Gate, or new authorization.

The Agent uses the current Feature execution grant or exact Lightweight Card scope, repairs the bounded implementation first, then runs fresh targeted verification, affected existing checks, diff/scope/risk/rollback review, records evidence, and presents a specific Regression Test Advisory.

Required Verification proves the current result. Existing Test Obligation comes from accepted tests.md, Gate 2, acceptance, ADR, Delivery Contract, Bug Verification Matrix, or current Human instruction. Additional Regression Test is future protection proposed after current proof exists. An Additional Regression Test Advisory does not by itself block Task Done, Lightweight Change completion, or Feature Close.

If the change cannot be reliably verified without a new test, do not claim `fixed`, `done`, `completed`, or `closed`; present the exact test and ask whether to add it now, adjust the repair, roll back, or pause. A failed required check is never an advisory.
```

Add the conceptual flow in one code block in the exact order asserted by Task 1.

- [x] **Step 2: Coordinate Runtime execution, stop, and completion rules**

Update these owning areas:

- `Execution Defaults`: scope TDD default to initial Feature/explicit Bug execution and name Repair-First exceptions.
- `Human Gate Modes`: clarify that Feature Auto-Loop may apply bounded Review repairs without a new Gate when authority and execution boundary remain current.
- `Task Done Gate`: name all three evidence responsibilities and state advisory non-blocking behavior.
- `Auto modes do not remove stop conditions`: replace the broad “review finds behavior” stop with product/Feature-definition/implementation-boundary/architecture drift; keep implementation corrections inside Review Repair.
- `Completion Gate`: require Existing Test Obligations and fresh repair verification; surface Additional Regression Test advice without turning it into a close blocker.
- `Stop And Ask`: scope “TDD cannot be followed” to paths where TDD remains required and keep unreliable verification as a stop.

Do not add Repair-First or Review Repair to `## Stage Order` or Message Intent.

- [x] **Step 3: Add the design definitions and invariant**

In `references/design.md`, add exact definitions:

```markdown
**Repair-First Verification**: the default implementation order for a bounded Review correction and a clearly eligible Lightweight Change: write within existing authorization, run fresh targeted proof and affected existing checks, review scope/risk/rollback, record evidence, then recommend specific future regression protection.

**Review Repair Fast Path**: an internal Review method for correcting implementation to match accepted authority and acceptance without reopening Gate 1/2. It exits when definition, boundary, risk, verification, or authorization changes.

**Regression Test Advisory**: a concrete post-repair recommendation describing scenario, layer/location, prevented regression, residual risk, and priority. It is not a test-debt lifecycle or completion Gate.
```

Update `Adaptive Depth`, Core Model, Lightweight flow, Feature two-gate invariant, and first-version constraints so the design no longer claims that every isolated Lightweight behavior uses RED/GREEN.

- [x] **Step 4: Keep `SKILL.md` concise and correctly scoped**

Replace the universal clauses with concise controller language equivalent to:

```markdown
- TDD remains default for initial Feature execution, explicit Bug repair, Human-requested TDD, and accepted Plans that require RED/GREEN.
- A `within-approved-boundary` Review repair and a `clearly eligible` Lightweight Change default to Repair-First Verification: modify, verify fresh, review scope/risk/rollback, then present a specific Regression Test Advisory.
- Additional Regression Test advice never replaces Required Verification or an Existing Test Obligation.
```

Update the Lightweight Plan bullet and Stop And Ask bullets accordingly. Keep detailed algorithms in references.

- [x] **Step 5: Run the focused test to the next expected RED**

Run:

```bash
bash tests/validate-repair-first-verification.sh
```

Expected: still non-zero, now at the first missing detailed surface such as `references/lightweight-change-lane.md` or `references/stage-guides.md`. Do not weaken the test.

---

## Task 3: Implement Lightweight Repair-First, Card, And Helper Boundaries

**Files:**

- Modify: `references/lightweight-change-lane.md`
- Modify: `templates/lightweight-execution-card.md`
- Modify: `references/skill-routing.md`
- Modify: `references/external-skill-adapters.md`

- [x] **Step 1: Replace Targeted TDD with Repair-First in the owning Lightweight reference**

Rename `## Targeted TDD And Verification` to `## Repair-First Verification`. Replace the isolated behavior flow with:

```text
clearly eligible Card is current
-> apply the disclosed bounded change first
-> run fresh targeted verification after the write
-> run affected existing checks when available
-> review diff, scope, rollback and memory impact
-> record result and a specific Regression Test Advisory or not-needed reason
```

Keep these clauses explicit:

- eligibility and Feature hard triggers are unchanged;
- Card exists before the target write;
- existing tests are rerun when they already cover the risk;
- no test is invented only to manufacture RED;
- no reliable proof means Card cannot complete;
- scope expansion stops before broader edits;
- initial Feature or explicit Bug promotion restores normal TDD.

Remove the obsolete `targeted RED`, `minimal GREEN`, `smallest meaningful RED/GREEN`, and focused-regression-as-entry-obligation wording only from Lightweight execution ownership. Historical Proposal/Changelog text is not rewritten.

- [x] **Step 2: Update the Card without adding parser state**

Keep every existing heading and memory field. Change the default Plan to:

```markdown
- [ ] Inspect and confirm the exact change point.
- [ ] Apply only the disclosed bounded change.
- [ ] Run fresh failure-matched targeted verification after the write.
- [ ] Run affected existing checks when available.
- [ ] Review diff, scope, memory impact, sensitive evidence, and rollback.
```

Change Result/Residuals authoring guidance to contain:

```text
Record a specific Regression Test Advisory or a concrete not-needed reason; do not create a pending test-debt status.
```

Do not add a heading, enum, pending field, README, INDEX, archive, or scanner flag.

- [x] **Step 3: Prevent helper routing from restoring mandatory TDD**

In `references/skill-routing.md`, replace the smallest RED/GREEN sentence with:

```text
Review Repair Fast Path and Lightweight Change Lane do not invoke the TDD helper by default. The Review helper remains active for Review ownership, while the controller selects fresh failure-matched verification. Promotion to initial Feature execution or explicit Bug repair restores normal TDD helper resolution.
```

In `references/external-skill-adapters.md`, scope the TDD Adapter with:

```text
The TDD Adapter remains mandatory for initial Feature execution and explicit Bug repair, not for Review Repair Fast Path or clearly eligible Lightweight Change.
```

Preserve Plan/Review/Verify helpers, evidence ownership, task status, and every Human Gate.

- [x] **Step 4: Run focused Lightweight checks**

Run:

```bash
bash tests/validate-repair-first-verification.sh
bash tests/validate-lightweight-change-lane.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_lightweight_change_scan -v
```

Expected at this point:

- Repair-First test may remain RED only for Review/completion/version/scenario surfaces;
- existing Lightweight test may fail on obsolete RED/GREEN and v1.5.4 assertions, which Task 6/7 will update;
- Python scanner tests remain GREEN because no parser state changed.

Any scanner failure caused by a new field/state means scope drift; revert the parser-shape change and keep advisory in Result/Residuals.

---

## Task 4: Implement Review, Verification, Completion, And Evidence Surfaces

**Files:**

- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/human-review-summary.md`
- Modify: `references/feature-completion-check.md`
- Modify: `templates/notes.md`
- Modify: `tests/validate-feature-construction-two-gate-review.sh`
- Modify: `tests/test_feature_review.py`

- [x] **Step 1: Add Review Repair Fast Path inside the existing Review stage**

Under `## Review`, add `### Review Repair Fast Path`. The ordered contract must say:

```text
classify finding against current authority and authorization
-> `within-approved-boundary`
-> repair the implementation first
-> fresh targeted verification
-> affected existing checks
-> diff / scope / risk / rollback review
-> record evidence
-> Regression Test Advisory
-> continue Review / Drift / Task Done / Feature Close
```

Add the exact exit sentence asserted by Task 1:

```text
If product meaning, Feature definition, implementation boundary, public interface, ADR, Contract, security, data, permission, dependency, migration, architecture, authorization, rollback, or reliable verification changes, return to Gate 1, Gate 2, Decision & Design, Delivery Contract, Bug Management, Diagnose Failure, or the applicable Human Gate.
```

Clarify that a reviewer calling a local implementation issue a “bug” does not itself create Bug Management intent; explicit Bug recording/tracking intent still wins.

- [x] **Step 2: Coordinate Execute, Diagnose, Verify, Drift, and Close**

- `Execute Task / Story`: keep mandatory TDD for initial Feature/explicit Bug execution; state that Review Repair remains owned by Review and does not re-enter Execute merely to manufacture RED.
- `Diagnose Failure`: a failed required check remains diagnosis evidence, never an advisory.
- `Verify`: require fresh proof after Repair-First and distinguish current proof from future regression protection.
- `Drift Check`: `within-approved-boundary` repair does not rewrite accepted product/ADR meaning; larger changes return to the owner.
- `Pause / Close`: show Additional Regression Test advice and residual risk, but block only on missing Existing Test Obligation or unreliable current proof.

- [x] **Step 3: Update workflow checklists with applicability, not a second process**

Add these exact checks in the existing Review/Verify/Task Done/Completion owners:

```markdown
- [ ] Classify the finding as `within-approved-boundary` before a Review Repair write.
- [ ] Repair first only inside current authorization, then run fresh targeted verification and affected existing checks.
- [ ] Do not downgrade an Existing Test Obligation into a Regression Test Advisory.
- [ ] If current proof is insufficient without a new test, keep the task/change non-terminal and ask at the existing Human Review.
- [ ] Batch specific Regression Test Advisory items in the next existing review/completion summary.
```

Remove universal RED-before-write checkboxes only from the two exception paths. Keep them for initial Feature and explicit Bug execution.

- [x] **Step 4: Add the Human Review and notes evidence shape**

Add `## Review Repair And Regression Test Advisory` to `references/human-review-summary.md` with this table:

```markdown
| Finding | Accepted boundary | Changed files/behavior | Fresh verification | Existing obligations | Regression Test Advisory | Residual risk |
|---|---|---|---|---|---|---|
```

State that multiple repairs are batched, the recommendation must name scenario/layer/risk/priority, and no response creates a new Gate.

Add this existing-artifact section to `templates/notes.md`:

```markdown
## Review Repair Evidence

| Date | Finding / Source | Authority / Boundary | Changed Files | Fresh Verification | Existing Test Obligations | Regression Test Advisory / Not-Needed Reason | Residual Risk | Human Decision |
|---|---|---|---|---|---|---|---|---|
```

Do not add lifecycle fields or a separate file.

- [x] **Step 5: Update Feature Completion Check**

Add these completion questions and rule:

```text
Are all Existing Test Obligations complete?
Does each Review Repair have fresh targeted verification and evidence?
Are Additional Regression Test recommendations and residual risk visible?
An unaccepted Additional Regression Test Advisory does not by itself block Feature close.
```

Keep close Human confirmation and Bug Close independence unchanged.

- [x] **Step 6: Strengthen existing Feature Review regression tests**

In `tests/test_feature_review.py`, add tests that:

- extract the Review and Task Done owning sections;
- require repair-first order;
- reject an advisory that replaces Existing Test Obligation;
- reject completion wording that permits no fresh verification;
- preserve Gate 1/2 and Later Start semantics.

In `tests/validate-feature-construction-two-gate-review.sh`, assert that Review Repair stays inside the accepted execution boundary and does not add a third Gate or local authorization Checker.

- [x] **Step 7: Run affected Review tests**

Run:

```bash
bash tests/validate-repair-first-verification.sh
bash tests/validate-feature-construction-two-gate-review.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_feature_review -v
```

Expected: failures, if any, are limited to not-yet-updated scenarios/version/root/maintenance surfaces. Core Review ordering and Gate preservation must pass.

---

## Task 5: Add Pressure Scenarios, Root Projection, And Maintainer Validation Rules

**Files:**

- Modify: `references/validation-scenarios.md`
- Modify: `templates/root-AGENTS.md` body only; revision is Task 6
- Modify: `references/project-guidance.md`
- Modify: `docs/maintenance/full-validation-method.md`
- Modify: `docs/maintenance/feature-validation-method.md`
- Modify: `tests/validate-maintainer-full-validation-guidance.sh`
- Modify: `tests/validate-feature-validation-method.sh`

- [x] **Step 1: Replace and add validation scenarios**

Rename the obsolete `Small Isolated Logic Change Uses Minimal RED GREEN` scenario to `Lightweight Logic Change Repairs Before Verification` and rewrite its expected route to Repair-First.

Add all twelve scenario headings required by Task 1. Each scenario must use the repository structure:

```markdown
### Scenario Name

- Prompt:
- Expected Route:
- Evidence:
- Required Action:
- Forbidden Action:
- Next:
```

Use concrete cases:

- local null handling with existing focused test;
- UI adjustment with browser proof and a not-needed automated-test reason;
- no credible proof without a new test;
- Product Slice drift;
- missing current write authorization;
- clearly eligible internal logic change;
- missing Gate 2 test disguised as advice;
- advice visible but non-blocking;
- Human chooses to add a test after repair;
- three repairs batched into one summary;
- explicit Bug record/Resolution Path repair;
- initial Feature implementation.

- [x] **Step 2: Keep root guidance concise**

Add at most one concise sentence to the appropriate ownership/completion block:

```text
During Review, correct a `within-approved-boundary` implementation first, verify it fresh, and surface specific optional regression protection; definition, boundary, authorization, or required-verification changes return to their owning reference.
```

Do not add the algorithm, evidence table, statuses, or a new Workflow Gateway Map row. Keep all 13 managed blocks and keep `templates/root-AGENTS.md` at or below 190 lines.

Update `references/project-guidance.md` so refresh validation expects that concise projection but keeps detailed ownership in runtime/stage-guides/lightweight reference.

- [x] **Step 3: Correct the maintainer full-validation invariant**

Replace the obsolete universal invariant in `docs/maintenance/full-validation-method.md` with:

```text
Initial Feature behavior implementation and explicit Bug repair cannot skip required TDD RED. A `within-approved-boundary` Review Repair and a `clearly eligible` Lightweight Change use Repair-First Verification, but no completion claim may skip fresh targeted evidence or an Existing Test Obligation.
```

Update the Development/Test Workflow domain and pressure list to test both sides of this distinction. Do not weaken repository-maintainer RED/GREEN requirements for implementing Agent Loop itself.

In `docs/maintenance/feature-validation-method.md`, require a focused validation of current proof versus future regression advice when evaluating this feature.

- [x] **Step 4: Update maintenance-guidance tests**

Make `tests/validate-maintainer-full-validation-guidance.sh` and `tests/validate-feature-validation-method.sh` assert:

- implementation of Agent Loop changes still uses real RED/GREEN;
- downstream initial Feature/explicit Bug retains TDD;
- Review Repair/Lightweight uses Repair-First;
- fresh proof and Existing Test Obligations remain hard;
- Additional Regression advice is non-blocking only after current proof exists.

- [x] **Step 5: Run scenario/root/maintenance focused checks**

Run:

```bash
bash tests/validate-repair-first-verification.sh
bash tests/validate-maintainer-full-validation-guidance.sh
bash tests/validate-feature-validation-method.sh
python3 - <<'PY'
from pathlib import Path
path = Path('templates/root-AGENTS.md')
assert len(path.read_text(encoding='utf-8').splitlines()) <= 190
assert path.read_text(encoding='utf-8').count('agent-loop:managed-start') == 13
print('PASS: root AGENTS size and managed block count')
PY
```

Expected: behavioral/scenario/maintenance assertions pass; version/revision assertions may remain RED until Task 6.

---

## Task 6: Synchronize v1.5.5 Metadata, Human Docs, Root Revisions, And Current Tests

**Files:**

- Modify: `SKILL.md`
- Modify: `plugin.json`
- Modify: `agents/openai.yaml`
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`
- Modify: `templates/root-AGENTS.md`
- Modify: `references/project-guidance.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/validation-scenarios.md`
- Modify: `references/submit-and-integrate.md`
- Modify: current-version/root-revision tests listed in Section 3.7

- [x] **Step 1: Synchronize the version-bearing files**

Use these exact current development values:

| Surface | Required value |
|---|---|
| `SKILL.md` | `Version: 1.5.5` |
| `plugin.json` | `"version": "1.5.5"` |
| `README.md` | `**Current version:** 1.5.5 (development)` |
| `Usage.md` | `**版本：** 1.5.5（开发中）` |
| `CHANGELOG.md` | top heading `## 1.5.5 — 2026-08-12` with implementation/Human Review status, no release/tag claim |
| all 13 root managed blocks | `block-version:1.5.5-20260812.1` |

Keep public stable installation commands on `stable-v1.5.4` until a separate formal Release Gate creates `stable-v1.5.5`. Explain the difference between source development version and current stable installation channel; do not claim `1.5.5` is stable.

- [x] **Step 2: Update human-facing capability wording**

README and Usage must explain:

```text
Feature initial implementation and explicit Bug repair keep TDD.
Review repairs inside the accepted boundary and clearly eligible Lightweight Changes repair first, verify fresh, and then recommend specific regression coverage.
Fresh verification and accepted test obligations remain mandatory.
```

Add one Usage example where the Agent reports the completed repair, verification, and two concrete test recommendations without opening a new Gate.

CHANGELOG must record:

- default Review Repair Fast Path;
- Lightweight Repair-First;
- required/advisory evidence split;
- no new stage/status/Gate/artifact/checker;
- preserved initial Feature/Bug TDD and Human Gates;
- focused/full validation status only after evidence exists.

- [x] **Step 3: Correct metadata prompts**

Change `agents/openai.yaml` default prompt from universal `TDD is default` to:

```text
Use TDD for initial Feature and explicit Bug execution. During a bounded Review repair or clearly eligible Lightweight Change, repair first, verify fresh, and then recommend specific regression coverage. Never skip required verification or Human Gates.
```

Update `plugin.json` long description consistently; do not add capabilities or dependencies.

- [x] **Step 4: Synchronize root revision consumers**

Replace current-template revision examples and expectations with `1.5.5-20260812.1` in:

- `references/project-guidance.md`;
- `references/workflow-checklists.md`;
- current root-refresh scenarios in `references/validation-scenarios.md`;
- root block Shell/Python tests listed in Section 3.7.

Update bare-version stale examples to `block-version:1.5.5` where they represent the current template. Do not rewrite historical proposals/reports.

- [x] **Step 5: Synchronize current version assertions without rewriting history**

Update current assertions in:

- `tests/validate-lightweight-change-lane.sh`;
- `tests/validate-requirement-lifecycle-backlog.sh`;
- `tests/validate-human-help-version-docs.sh`;
- other Section 3.7 files that assert the current version/revision.

Leave unchanged:

- `CHANGELOG.md` historical `1.5.4` section;
- released v1.5.4 Proposal/Plan/report status assertions;
- stable installation commands intentionally pinned to `stable-v1.5.4` before release;
- test-fixture business values that happen to name `v1.5.4`.

Update the current-version commit example in `references/submit-and-integrate.md` to `docs(v1.5.5): ...`; this is documentation only and does not authorize a commit.

- [x] **Step 6: Run version/root focused checks**

Run:

```bash
bash tests/validate-repair-first-verification.sh
bash tests/validate-root-agents-block-refresh.sh
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-v1.2.4-root-stage-coverage.sh
bash tests/validate-human-help-version-docs.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_root_agents_blocks \
  tests.test_root_agents_lossless_slimming -v
```

Expected: all pass. Confirm exactly 13 root blocks use `1.5.5-20260812.1` and the root template remains at or below 190 lines.

---

## Task 7: Achieve Focused GREEN And Run Mutation/Boundary Regressions

**Files:**

- Modify only affected source/tests when a focused failure proves a real mismatch
- Update RED report with a clearly separated GREEN section only after commands pass

- [x] **Step 1: Run the primary focused GREEN**

Run:

```bash
bash tests/validate-repair-first-verification.sh
bash tests/validate-lightweight-change-lane.sh
bash tests/validate-feature-construction-two-gate-review.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_feature_review \
  tests.test_lightweight_change_scan -v
```

Expected: all pass. The new focused Shell test must print:

```text
PASS: Repair-First Review Repair and Lightweight Change contract is complete
```

- [x] **Step 2: Run route-boundary regressions**

Run:

```bash
bash tests/validate-bug-management.sh
bash tests/validate-feature-context-load-contract.sh
bash tests/validate-feature-brainstorming-trigger.sh
bash tests/validate-project-skill-discovery-guard.sh
bash tests/validate-project-local-skills.sh
bash tests/validate-branch-management-strategy.sh
bash tests/validate-maintainer-full-validation-guidance.sh
```

Expected: all named files exist and pass; no Bug, Feature Context, Project Skill, branch, or completion Gate regresses. Completion semantics are covered by the new focused contract together with `tests/validate-feature-construction-two-gate-review.sh` and `tests.test_feature_review`; do not create a no-op completion wrapper.

- [x] **Step 3: Execute exact mutation checks**

The embedded Ruby in the focused test must reject, without modifying source files:

- removing fresh verification;
- replacing Regression Test Advisory with silent completion;
- reversing repair and verification order;
- losing Required/Existing/Additional evidence separation;
- adding Review Repair to Message Intent or Stage Order.

Run the focused test twice to prove deterministic results:

```bash
bash tests/validate-repair-first-verification.sh
bash tests/validate-repair-first-verification.sh
```

Expected: both pass with identical final summary.

- [x] **Step 4: Update the RED report with GREEN evidence**

Add a distinct `## GREEN 与 focused regression` section containing actual commands, pass counts, mutation results, changed behavior summary, and remaining risks. Preserve the original RED command/output unchanged.

---

## Task 8: Run All Shell/Python Tests And Mechanical Validation

**Files:**

- Modify only proven defects
- Do not refresh the final report until all commands complete

- [x] **Step 1: Recount and run every Shell test**

Run:

```bash
set -euo pipefail
shell_total=0
for test_file in tests/*.sh; do
  bash "$test_file"
  shell_total=$((shell_total + 1))
done
printf 'SHELL_PASS=%s\n' "$shell_total"
```

The loop is POSIX-compatible with the repository's Bash execution and does not depend on `mapfile`. Expected discovered file count after adding the focused test is `50`, unless another independently approved test file was added and documented. Record the live count.

- [x] **Step 2: Run every Python unit test**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: all discovered tests pass. Record the actual test-case total and duration; do not infer it from the `22` module-file count.

- [x] **Step 3: Run YAML and JSON validation**

Run:

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md"); YAML.load_file("agents/openai.yaml")'
ruby -rjson -e 'JSON.parse(File.read("plugin.json"))'
```

Expected: exit `0`.

- [x] **Step 4: Run Shell and Python syntax validation**

Run:

```bash
find . -name '*.sh' -type f -not -path './.git/*' -print0 | xargs -0 -n1 bash -n
find . -name '*.py' -type f -not -path './.git/*' -not -path '*/__pycache__/*' -print0 | \
  xargs -0 python3 -c 'import ast, pathlib, sys; [ast.parse(pathlib.Path(p).read_text(encoding="utf-8")) for p in sys.argv[1:]]'
```

Expected: all files parse.

- [x] **Step 5: Run Markdown fence and diff checks**

Run:

```bash
ruby - <<'RUBY'
paths = Dir.glob('**/*.md', File::FNM_DOTMATCH).reject { |path| path.start_with?('.git/') }
errors = []
paths.each do |path|
  stack = nil
  File.foreach(path).with_index(1) do |line, number|
    next unless line =~ /^\s*(`{3,}|~{3,})/
    token = Regexp.last_match(1)
    if stack.nil?
      stack = [token[0], token.length, number]
    elsif token[0] == stack[0] && token.length >= stack[1]
      stack = nil
    end
  end
  errors << "#{path}: unclosed fence from line #{stack[2]}" if stack
end
abort errors.join("\n") unless errors.empty?
puts "PASS: Markdown fence balance (#{paths.length} files)"
RUBY

git diff --check
```

Expected: both pass. Because Proposal/Plan/reports/tests may still be untracked, also run the repository whitespace check used in Task 1 over every new file before Human Review.

- [x] **Step 6: Run version and stale-string audit**

Run:

```bash
rg -n '1\.5\.4|1\.5\.4-20260810\.1|smallest meaningful RED/GREEN|targeted RED|minimal GREEN|behavior-changing execution requires TDD|TDD is default' \
  SKILL.md plugin.json agents/openai.yaml README.md Usage.md CHANGELOG.md references templates tests docs/maintenance docs/proposal docs/reports
```

Classify every hit as one of:

- historical release/proposal/report evidence — preserve;
- stable installation channel intentionally still `stable-v1.5.4` — preserve until Release Gate;
- test fixture domain value — preserve;
- current runtime/version/revision assertion — update to v1.5.5;
- obsolete universal TDD rule — repair.

No unexplained current-authority hit may remain.

---

## Task 9: Perform Six-Domain Full Validation And Refresh Evidence

**Files:**

- Create: `docs/reports/agent-loop-v1.5.5-full-validation-2026-08-12.md`
- Modify: Proposal status/evidence section
- Modify: Implementation Plan status/checklist evidence only

- [x] **Step 1: Execute the six-domain semantic audit from current sources**

Audit and score independently:

1. Logic Correctness;
2. Autonomy;
3. Project Entry / Evidence Graph + DDD Onboarding;
4. Development / Test Workflow;
5. Memory;
6. Recommendation.

Do not copy a previous score. Re-read runtime/design and directly cross-check SKILL, Lightweight, Stage Guides, Checklists, helper adapters, completion, templates, root guidance, scenarios, human docs, and tests.

- [x] **Step 2: Re-run representative workflow pressure cases**

In addition to the full-validation method's existing cases, explicitly trace:

```text
initial Feature -> TDD -> Verify -> Review finding -> Repair-First -> fresh proof -> advisory -> Task Done
explicit Bug -> Resolution Path -> Feature TDD -> Bug Verification Matrix -> separate Bug/Feature close
clearly eligible Lightweight -> Card -> write -> fresh proof -> advisory -> completion
Lightweight scope expansion -> stop before broader write -> Feature/Bug/Requirements route
Review definition drift -> Gate 1
Review implementation-boundary drift -> Gate 2
missing current proof -> no completion claim
missing accepted test -> cannot be disguised as advisory
```

Also rerun the unaffected Product/ADR/Contract/Archive/Memory/Project Skill/Branch/Submit/Close invariants required by `docs/maintenance/full-validation-method.md`.

- [x] **Step 3: Write the Chinese full-validation report**

The report must include:

```markdown
# Agent Loop v1.5.5 全量验证报告

## 审计对象与工作区边界
## 结论、总分与等级
## 六域评分
## RED -> GREEN 证据
## Focused tests
## 全量 Shell/Python tests
## 机械检查
## Repair-First 压力场景
## 保持不变的 Human Gates
## Critical / High / Medium / Low
## macOS 与 Windows 状态
## 剩余风险与范围偏移
## 版本与 root managed blocks
## 发布判断
## Git 动作声明
```

Record actual commands, actual counts, duration where available, and current file/line evidence. macOS may be `live-verified`; Windows must be reported truthfully as `test-defined` unless live Windows evidence actually exists.

The result may be called release-candidate-ready only at `STRONG`, with `0` Critical, `0` unexplained High, every Medium resolved or explicitly returned to Human Review, and all executable/mechanical checks passing.

- [x] **Step 4: Refresh Proposal and Plan truthfully**

Only after all evidence passes:

- Proposal status becomes `implemented and fully validated; awaiting final Human Review`;
- Plan status becomes `Tasks 0–9 complete; awaiting final Human Review`;
- checked Task boxes reflect only commands actually run;
- add compact links to the RED and full-validation reports;
- do not claim stable release, commit, push, tag, or installed-Skill synchronization.

- [x] **Step 5: Run final scope and dirty-work audit**

Run:

```bash
git status --short --branch
git diff --stat
git diff --name-only
git diff --cached --stat
find . -maxdepth 2 -type d -name '.agent-loop' -print
```

Expected:

- only planned tracked/untracked files plus the preserved `.tmp/` and `__pycache__/` paths;
- empty index;
- no target-project `.agent-loop/` directory;
- no unlisted executable, dependency, generated database, or installed-Skill change.

---

## Task 10: Stop At Final Human Review

**Files:**

- Read all changed files and reports
- Do not modify source unless Human Review finds a concrete defect

- [x] **Step 1: Prepare the final Human Review Summary**

Return one table-first summary containing:

- actual modified/new files grouped by owner;
- planning baseline and final branch/HEAD;
- genuine RED command/output;
- focused GREEN commands/counts;
- all Shell/Python totals;
- YAML/JSON/Shell/Python/Markdown/diff results;
- six-domain score and Critical/High/Medium counts;
- Proposal acceptance criteria 1–14 mapping;
- macOS/Windows status;
- remaining risks and design drift;
- version `1.5.5` and all `13/13` root revisions;
- unrelated dirty-work preservation;
- explicit statement: no stage, commit, push, tag, PR, merge, release, publish, branch/worktree change, subagent dispatch, or installed-Skill synchronization occurred.

- [x] **Step 2: Recommend exactly one next stage**

Recommend `Human Review of implementation and validation evidence`. Do not execute any Git or release action until separately authorized.

---

## 5. Focused Validation Command Set

The executor must run this set after GREEN, in addition to any newly discovered direct consumer:

```bash
bash tests/validate-repair-first-verification.sh
bash tests/validate-lightweight-change-lane.sh
bash tests/validate-feature-construction-two-gate-review.sh
bash tests/validate-maintainer-full-validation-guidance.sh
bash tests/validate-feature-validation-method.sh
bash tests/validate-root-agents-block-refresh.sh
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-v1.2.4-root-stage-coverage.sh
bash tests/validate-human-help-version-docs.sh
bash tests/validate-bug-management.sh
bash tests/validate-feature-context-load-contract.sh
bash tests/validate-feature-brainstorming-trigger.sh
bash tests/validate-project-skill-discovery-guard.sh
bash tests/validate-project-local-skills.sh
bash tests/validate-branch-management-strategy.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_feature_review \
  tests.test_lightweight_change_scan \
  tests.test_root_agents_blocks \
  tests.test_root_agents_lossless_slimming -v
```

If a named test does not exist at execution time, report the missing file and use the actual owning test discovered from `rg --files tests`; do not silently skip it and do not create a no-op test.

---

## 6. Full Validation Command Set

```bash
set -euo pipefail

shell_total=0
for test_file in tests/*.sh; do
  bash "$test_file"
  shell_total=$((shell_total + 1))
done
printf 'SHELL_PASS=%s\n' "$shell_total"

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v

ruby -e 'require "yaml"; YAML.load_file("SKILL.md"); YAML.load_file("agents/openai.yaml")'
ruby -rjson -e 'JSON.parse(File.read("plugin.json"))'
find . -name '*.sh' -type f -not -path './.git/*' -print0 | xargs -0 -n1 bash -n
find . -name '*.py' -type f -not -path './.git/*' -not -path '*/__pycache__/*' -print0 | \
  xargs -0 python3 -c 'import ast, pathlib, sys; [ast.parse(pathlib.Path(p).read_text(encoding="utf-8")) for p in sys.argv[1:]]'
git diff --check
```

The Markdown fence command from Task 8 is also mandatory.

---

## 7. Proposal Coverage Matrix

| Proposal requirement | Owning Task |
|---|---|
| Default Feature Review Repair | Tasks 2 and 4 |
| Default Lightweight Repair-First | Task 3 |
| Fresh targeted verification remains mandatory | Tasks 2–5 |
| Specific post-repair Regression Test Advisory | Tasks 2–5 |
| Advisory does not automatically block completion | Tasks 2 and 4 |
| Existing test obligations remain hard | Tasks 2, 4, 5, and 7 |
| No reliable proof means no completion claim | Tasks 2–5 and 7 |
| Initial Feature and explicit Bug TDD remain | Tasks 2, 4, 5, and 7 |
| Scope/authority/security/data/interface/Git exits remain | Tasks 2–5 and 9 |
| No new stage/status/mode/Gate/artifact/checker | Tasks 1–5 and 7 |
| Runtime/design/reference/template/root/human-doc consistency | Tasks 2–6 |
| v1.5.5 and 13 managed revisions | Task 6 |
| Genuine RED/GREEN and all tests | Tasks 0, 1, 7, and 8 |
| Chinese RED/full report and Human Review stop | Tasks 1, 9, and 10 |

No Proposal acceptance item is intentionally deferred.

---

## 8. Plan Self-Review

### Spec coverage

All Proposal sections 1–21 map to Tasks 0–10. The plan includes the additional required maintenance-method synchronization discovered during planning because the current full-validation invariant would otherwise contradict the accepted design.

### Placeholder scan

This plan contains no unresolved placeholder, deferred implementation marker, unspecified test command, or unnamed error-handling step. Template-like examples use complete contractual text or concrete field names.

### Type and terminology consistency

The plan uses only these new conceptual names:

- `Repair-First Verification`;
- `Review Repair Fast Path`;
- `Regression Test Advisory`;
- `Required Verification`;
- `Existing Test Obligation`;
- `Additional Regression Test`.

None is a lifecycle value, stage, mode, Gate, Checker result, or artifact family. Existing `within-approved-boundary`, Task/Feature status, Gate 1/2, Lightweight Card status, Bug lifecycle, and Checker outcomes remain unchanged.

### Scope check

The plan covers one coordinated workflow change with two consumers of the same implementation-order invariant. Splitting the consumers into separate plans would duplicate runtime/design/helper/completion/version work and risk contradictory semantics, so one plan is the smaller coherent unit.

### Git and release boundary

This plan intentionally contains no commit step despite the generic writing-plan preference for frequent commits. Agent Loop repository rules require an independent Human Gate for stage/commit/push/tag/release actions. Implementation stops at Human Review.

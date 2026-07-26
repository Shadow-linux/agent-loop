# Checker Self-Repair And Temporary Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a bounded, Human-authorized path for diagnosing and temporarily repairing a defective Agent Loop checker without hiding canonical failure or mutating the installed Skill by default.

**Architecture:** Checker Self-Repair is an internal method shared by `Diagnose Failure` and `Verify`, not a new stage or lifecycle. Runtime authority lives in `references/checker-recovery.md`, is routed from the controller and root Gateway, and is protected by contract tests that require classification, isolated RED/GREEN repair, one-Gate expiry, substitute-review evidence, and formal upstream repair.

**Tech Stack:** Markdown runtime contracts, Bash contract tests, Python 3 standard-library repository checks, Ruby YAML/Markdown validation.

---

## File Map

- Create `references/checker-recovery.md`: detailed operational authority.
- Modify `SKILL.md`: package map, runtime trigger, and stop boundary.
- Modify `references/runtime.md`: internal recovery flow, blocked routing, and Gate semantics.
- Modify `references/design.md`: core invariant, definition, and main-flow projection.
- Modify `references/stage-guides.md`: Diagnose/Verify entry and exit behavior.
- Modify `references/workflow-checklists.md`: executable review checklist.
- Modify `references/project-guidance.md`: root guidance requirement and Gateway family count.
- Modify `templates/root-AGENTS.md`: concise first-hop Gateway row and Evidence Gate reminder.
- Modify `references/validation-scenarios.md`: positive and adversarial pressure scenarios.
- Modify `Usage.md`: human-facing trigger and expected interaction.
- Modify `CHANGELOG.md`: unreleased capability note.
- Create `tests/validate-checker-self-repair.sh`: cross-surface contract regression.
- Modify root-template revision assertions in `tests/` and affected references when the managed template revision changes.
- Create/update `docs/reports/agent-loop-1.5.0-full-validation-2026-07-25.md`: fresh validation evidence.

### Task 1: Establish The RED Contract

**Files:**
- Create: `tests/validate-checker-self-repair.sh`

- [x] **Step 1: Write the failing cross-surface test**

The test must assert:

```bash
assert_contains SKILL.md 'references/checker-recovery.md'
assert_contains references/runtime.md '## Checker Failure Recovery'
assert_contains references/design.md '**Checker Self-Repair**'
assert_contains references/checker-recovery.md 'artifact-invalid | environment-invalid | checker-defect-candidate | unresolved'
assert_contains references/checker-recovery.md 'Canonical validation: failed'
assert_contains references/checker-recovery.md 'accepted-for-this-gate'
assert_contains references/checker-recovery.md 'isolated temporary copy'
assert_contains references/checker-recovery.md 'RED'
assert_contains references/checker-recovery.md 'negative controls'
assert_contains references/checker-recovery.md 'formal source repair'
assert_contains templates/root-AGENTS.md 'Canonical Agent Loop checker failure'
assert_contains references/validation-scenarios.md 'Checker Self-Repair'
assert_contains Usage.md '临时修正 Agent Loop Checker'
assert_contains CHANGELOG.md 'Checker Self-Repair'
assert_not_contains references/checker-recovery.md 'temporary result changes the canonical checker to pass'
```

- [x] **Step 2: Run the test and verify RED**

Run:

```bash
bash tests/validate-checker-self-repair.sh
```

Expected: `FAIL` because `references/checker-recovery.md` and runtime routing do not yet exist.

### Task 2: Publish The Canonical Recovery Contract

**Files:**
- Create: `references/checker-recovery.md`
- Modify: `SKILL.md`
- Modify: `references/runtime.md`
- Modify: `references/design.md`

- [x] **Step 1: Add the detailed authority**

Write the accepted flow:

```text
exact canonical rerun
-> artifact/environment/checker/unresolved classification
-> minimal authority-backed fixture
-> Temporary Checker Repair Review
-> exact Human authorization
-> isolated copied checker and support digests
-> original RED
-> minimal patch
-> GREEN and negative controls
-> exact target run
-> canonical failure plus temporary result
-> one-Gate Human substitute decision
-> expiry and formal source repair
```

- [x] **Step 2: Add controller routing**

Require `SKILL.md` and `runtime.md` to load the recovery reference when a canonical Agent Loop checker fails after an exact rerun. Keep it inside `Diagnose Failure` / `Verify`; do not add a canonical stage, lifecycle, or Auto Mode.

- [x] **Step 3: Add design invariants**

Define the authority relationship:

```text
published semantic authority > canonical checker implementation
canonical failure remains evidence
Human-authorized temporary substitute applies to one Gate only
formal fixed canonical checker is required to claim Agent Loop is fixed
```

- [x] **Step 4: Run the focused test**

Run:

```bash
bash tests/validate-checker-self-repair.sh
```

Expected: it may still fail on downstream stage/root/usage surfaces, while the canonical-reference assertions pass.

### Task 3: Align Stage Execution And Human Review

**Files:**
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`

- [x] **Step 1: Extend Diagnose Failure**

Require exact rerun, full-output preservation, classification, minimal fixture, published-authority comparison, and no checker writes before the exact review.

- [x] **Step 2: Extend Verify**

Require dual evidence:

```text
Canonical validation: failed
Temporary checker recovery: passed | failed
Human substitute decision: accepted-for-this-gate | declined
```

Only the named Gate may use the substitute. Later gates see the residual and cannot inherit authorization.

- [x] **Step 3: Add checklist guards**

Add explicit checks for isolation, source digests, RED/GREEN, negative controls, expiry, rollback, no silent global mutation, and formal repair follow-up.

### Task 4: Refresh Root Guidance Without Copying The Algorithm

**Files:**
- Modify: `templates/root-AGENTS.md`
- Modify: `references/project-guidance.md`
- Modify: root-template revision assertions in `tests/*.sh`, `tests/*.py`, and directly related reference examples.

- [x] **Step 1: Add one Gateway row**

Add:

```markdown
| Canonical Agent Loop checker failure after an exact rerun | Diagnose Failure / Checker Recovery | `references/checker-recovery.md`, `references/stage-guides.md` |
```

- [x] **Step 2: Keep the root reminder concise**

Add one Evidence Gate sentence stating that suspected checker defects route to isolated Human-authorized recovery and never become a silent bypass.

- [x] **Step 3: Increment the same-version managed-block revision**

Replace the current full template revision with:

```text
1.5.0-20260725.1
```

Update exact revision assertions and examples without changing the skill version.

- [x] **Step 4: Verify root guidance**

Run:

```bash
python3 -m unittest tests.test_root_agents_blocks tests.test_root_agents_lossless_slimming
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-root-agents-block-refresh.sh
bash tests/validate-v1.2.4-root-stage-coverage.sh
```

Expected: all pass and root template remains within 190 lines.

### Task 5: Add Human Usage And Pressure Scenarios

**Files:**
- Modify: `references/validation-scenarios.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`

- [x] **Step 1: Add pressure scenarios**

Cover:

1. valid artifact rejected by checker;
2. invalid artifact incorrectly blamed on checker;
3. environment failure misclassified as checker defect;
4. temporary patch weakens unrelated validation;
5. silent global Skill mutation;
6. same-session response-local evidence;
7. cross-session residual persistence;
8. reuse after digest/Gate change;
9. formal Agent Loop source release attempts to rely on temporary checker.

- [x] **Step 2: Add human trigger wording**

Add a concise example:

```text
这个 Agent Loop Checker 可能有问题。先保留原始失败并判断是文档、环境还是 Checker；如果确实是 Checker 缺陷，给我一个隔离临时修复方案，我确认后只用于当前 Gate。
```

- [x] **Step 3: Record the unreleased capability**

State that Checker Self-Repair is isolated, test-first, one-Gate, Human-authorized, non-canonical evidence with formal upstream follow-up.

### Task 6: GREEN, Full Validation, And Handoff

**Files:**
- Modify: `docs/reports/agent-loop-1.5.0-full-validation-2026-07-25.md`
- Modify: this plan's checkbox states

- [x] **Step 1: Run the focused contract**

Run:

```bash
bash tests/validate-checker-self-repair.sh
```

Expected: `PASS`.

- [x] **Step 2: Run all shell tests**

Run:

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
```

Expected: every script exits `0`.

- [x] **Step 3: Run Python unit tests**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

Expected: all tests pass.

- [x] **Step 4: Run syntax and structure checks**

Run:

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
python3 -m json.tool plugin.json >/dev/null
git diff --check
```

Also run a Markdown fence-balance check over changed Markdown files. Expected: all pass.

- [x] **Step 5: Perform the six-domain semantic audit**

Score Logic Correctness, Autonomy, Project Entry/Onboarding, Development/Test Workflow, Memory, and Recommendation. Confirm:

- temporary recovery cannot silently bypass a canonical Gate;
- Agent can diagnose before asking;
- Human substitute authority is one-Gate and exact;
- root routing and full runtime routing agree;
- formal source repair remains required;
- no unrelated lifecycle or Git permission is inherited.

- [x] **Step 6: Write the Chinese validation report**

Record current branch, working-tree audit scope, RED evidence, GREEN commands, six-domain score, remaining risks, and the absence of commit/push/tag authorization.

- [x] **Step 7: Stop at the independent Git Gate**

Do not stage, commit, push, tag, release, publish, merge, or bump the version without a new explicit Human instruction.

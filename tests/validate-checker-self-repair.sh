#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

assert_contains() {
  local file=$1 text=$2
  if ! grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s missing required text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_not_contains() {
  local file=$1 text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s contains forbidden text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_contains SKILL.md 'references/checker-recovery.md'
assert_contains SKILL.md 'canonical Agent Loop checker'
assert_contains references/runtime.md '## Checker Failure Recovery'
assert_contains references/runtime.md 'internal method of Diagnose Failure and Verify'
assert_contains references/design.md '**Checker Self-Repair**'
assert_contains references/checker-recovery.md 'artifact-invalid | environment-invalid | checker-defect-candidate | unresolved'
assert_contains references/checker-recovery.md 'Canonical validation: failed'
assert_contains references/checker-recovery.md 'accepted-for-this-gate'
assert_contains references/checker-recovery.md 'isolated temporary copy'
assert_contains references/checker-recovery.md 'negative controls'
assert_contains references/checker-recovery.md 'formal source repair'
assert_contains references/stage-guides.md 'Temporary Checker Repair Review'
assert_contains references/workflow-checklists.md 'Canonical validation: failed'
assert_contains templates/root-AGENTS.md 'Canonical Agent Loop checker failure'
assert_contains templates/root-AGENTS.md 'Diagnose Failure / Checker Recovery'
assert_contains references/project-guidance.md 'Checker Recovery Gateway'
assert_contains references/validation-scenarios.md '## 76. Checker Self-Repair'
assert_contains Usage.md '临时修正 Agent Loop Checker'
assert_contains CHANGELOG.md 'Checker Self-Repair'

assert_not_contains references/checker-recovery.md \
  'temporary result changes the canonical checker to pass'
assert_not_contains references/checker-recovery.md \
  'Auto Mode authorizes temporary checker repair'

printf 'PASS: checker self-repair classification, isolation, evidence, one-gate authorization, and formal-repair contract is complete\n'

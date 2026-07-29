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

assert_file_exists() {
  local file=$1
  if [[ ! -f "$root/$file" ]]; then
    printf 'FAIL: missing required file: %s\n' "$file" >&2
    exit 1
  fi
}

assert_file_exists scripts/check-feature-context.py
assert_file_exists templates/feature-context.md
assert_contains templates/spec.md '## Feature Context Snapshot'
assert_contains templates/spec.md 'Freshness: current | changed | blocked'
assert_contains templates/spec.md 'Product Definition Profile: brief | standard | legacy'
assert_contains templates/spec.md 'Verified At: <ISO-8601 timestamp with timezone>'
assert_contains templates/spec.md 'project-root-relative'
assert_contains references/design.md 'Feature Context Snapshot'
assert_contains references/design.md 'Requirement README'
assert_contains references/runtime.md 'scripts/check-feature-context.py'
assert_contains references/runtime.md 'Exit `0 / CHANGED`'
assert_contains references/runtime.md '`CHANGED` never authorizes'
assert_contains references/design.md 'facts, not workflow authorization'
assert_contains references/stage-guides.md 'Work Breakdown'
assert_contains references/stage-guides.md 'Test Design'
assert_contains references/stage-guides.md 'Plan Gate / Plan'
assert_contains references/stage-guides.md 'Subagent Handoff'
assert_contains references/workflow-checklists.md 'python3 <skill-root>/scripts/check-feature-context.py'
assert_contains references/workflow-checklists.md 'Resume'
assert_contains references/implementation-planning.md 'current Feature Context Snapshot'
assert_contains references/artifact-rules.md 'optional `context.md`'
assert_contains references/complex-artifacts.md 'Feature Context Snapshot'
assert_contains references/product-definition.md 'Feature Context Snapshot'
assert_contains references/document-templates.md 'Freshness: current | changed | blocked'
assert_contains references/project-guidance.md 'Feature Context Snapshot'
assert_contains templates/root-AGENTS.md 'Feature Context Snapshot'
assert_contains references/validation-scenarios.md 'Feature Context Snapshot'
assert_contains SKILL.md 'scripts/check-feature-context.py'
assert_contains README.md 'Feature Context Snapshot'
assert_contains Usage.md 'Feature Context Snapshot'
assert_contains CHANGELOG.md 'Feature Context Snapshot'

assert_not_contains templates/feature-context.md 'Independent Product Truth: yes'
assert_not_contains templates/spec.md 'Freshness: current | refresh-required | blocked'

printf 'PASS: Feature Context Snapshot authority, freshness, stage loading, and compatibility contract is complete\n'

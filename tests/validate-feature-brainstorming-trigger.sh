#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
cd "$root"

assert_contains() {
  local file=$1 text=$2
  if ! grep -Fq -- "$text" "$file"; then
    printf 'FAIL: %s missing Feature brainstorming contract: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_not_contains() {
  local file=$1 text=$2
  if grep -Fq -- "$text" "$file"; then
    printf 'FAIL: %s retains unconditional Feature brainstorming rule: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_contains references/runtime.md 'Feature Spec enters Brainstorm / Clarify only when concrete feature-local scope, acceptance, or implementation-boundary uncertainty remains after loading the accepted Product Slice and applicable ADRs.'
assert_contains references/design.md 'A clear Feature with a current Product Slice, applicable accepted ADRs, explicit scope, and measurable acceptance skips Brainstorm / Clarify.'
assert_contains references/external-skill-adapters.md 'Feature Spec with real feature-local uncertainty'
assert_contains references/external-skill-adapters.md 'A clear Feature does not enter Brainstorm / Clarify, does not load brainstorming merely because Feature Spec is active, and requires no Brainstorm Stage Helper Resolution.'
assert_contains references/stage-guides.md 'When Product Slice, applicable accepted ADR Design Slices, scope, exclusions, and acceptance are already clear, skip Brainstorm / Clarify and proceed directly with Feature Spec.'
assert_contains references/workflow-checklists.md 'Do not load brainstorming merely because Feature Spec is active.'
assert_contains references/validation-scenarios.md 'Clear Feature Skips Brainstorming'
assert_contains Usage.md 'Feature 已经有明确的 Product Slice、适用 ADR、范围、排除项和验收时，Agent 不会为了形式调用 brainstorming'
assert_contains CHANGELOG.md 'Feature Spec 只在真实的 Feature-local 范围、验收或实施边界歧义仍存在时调用 brainstorming'

assert_not_contains references/external-skill-adapters.md '| Feature Spec | `superpowers:brainstorming` plus spec helpers when available |'
assert_not_contains references/stage-guides.md 'when a spec/brainstorming helper is available, use it for ambiguity removal, scope checks, and acceptance thinking while writing to `spec.md`'
assert_not_contains references/workflow-checklists.md 'If a spec-writing, brainstorming, or product-discovery helper is available, use it through `external-skill-adapters.md` while writing accepted output to agent-loop `spec.md`.'

printf 'PASS: Feature brainstorming is conditional and cannot reopen accepted product or ADR meaning\n'

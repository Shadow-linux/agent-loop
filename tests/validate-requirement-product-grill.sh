#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

assert_contains() {
  local file=$1 text=$2
  grep -Fq -- "$text" "$root/$file" || {
    printf 'FAIL: %s missing required text: %s\n' "$file" "$text" >&2
    exit 1
  }
}

assert_not_contains() {
  local file=$1 text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s contains forbidden text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_contains "SKILL.md" 'Load `references/requirement-product-grill.md` during Requirements Discussion'
assert_contains "SKILL.md" '`CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/`'
assert_contains "references/runtime.md" 'Requirement/Product Grill may be used inside Requirements Discussion'
assert_contains "references/runtime.md" 'does not create a new stage'
assert_contains "references/requirement-product-grill.md" '# Requirement/Product Grill'
assert_contains "references/requirement-product-grill.md" 'clarification method inside Adaptive Product Definition'
assert_contains "references/requirement-product-grill.md" 'one blocking question at a time'
assert_contains "references/requirement-product-grill.md" 'agent recommended answer'
assert_contains "references/requirement-product-grill.md" 'First inspect project memory, original sources, the current effective Requirement `product.md` when present, docs, code, and tests'
assert_contains "references/requirement-product-grill.md" 'targeted lookup'
assert_contains "references/requirement-product-grill.md" 'Decision Candidate'
assert_contains "references/requirement-product-grill.md" 'must not directly create `.agent-loop/decisions/*.md`'
assert_contains "references/requirement-product-grill.md" 'Requirement `product.md` owns reviewed product goals'
assert_contains "references/product-definition.md" '一次只向人类确认一个阻塞问题'
assert_contains "references/human-review-summary.md" '## Product Definition Approval'
assert_contains "references/stage-guides.md" 'carry the accepted results into the same Requirement `product.md` draft'
assert_contains "references/skill-routing.md" 'Requirement `product.md` draft'
assert_contains "references/external-skill-adapters.md" 'Do not create `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/`'
assert_contains "references/workflow-checklists.md" 'Do not turn a grill design signal into an accepted ADR'
assert_contains "references/validation-scenarios.md" '## 64. Requirement/Product Grill Lane'

assert_not_contains "references/requirement-product-grill.md" 'default to creating ADR'
assert_not_contains "references/requirement-product-grill.md" 'feature `product.md` owns'

printf 'PASS: requirement/product grill remains an internal Product Definition method\n'

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

assert_contains "references/runtime.md" "## Message Intent Classification"
assert_contains "references/runtime.md" "Message intent is evaluated before project state classification"
assert_contains "references/runtime.md" 'requirements-discussion means the human is exploring product needs, business goals, capability ideas, constraints, tradeoffs, or user scenarios without authorizing implementation'
assert_contains "references/runtime.md" 'Product Definition Profile: `brief | standard`'
assert_contains "references/runtime.md" 'Product Review/recorded does not mean Requirement accepted for implementation and does not authorize Feature, ADR, code, or Git actions'
assert_contains "references/runtime.md" 'Chat Entry / Requirements Discussion [internal Brief/Standard Product Definition] if Needed'
assert_contains "references/runtime.md" 'Requirement Archive [Requirement Record / Archive]'
assert_contains "references/runtime.md" 'Feature Spec with Product Slice'
assert_contains "references/runtime.md" 'If unclear whether the human wants requirements discussion or Feature implementation, ask whether to form and review a Requirement Product Definition first or start Feature construction from an already accepted one.'

assert_contains "references/stage-guides.md" "## Chat Entry"
assert_contains "references/stage-guides.md" "## Requirements Discussion"
assert_contains "references/stage-guides.md" 'requirements-discussion -> evidence / Brainstorm -> Product Definition Depth Scan -> Brief or Standard product.md draft -> Product Human Review -> Requirement Record / Archive'
assert_contains "references/stage-guides.md" 'store the reviewed definition under `.agent-loop/requirements/<record-date>-<topic>/product.md` only after the human confirms the Requirement Record / Archive disclosure'
assert_contains "references/stage-guides.md" 'new Feature work does not create `product.md`; Feature `spec.md` references the Effective Product Definition and records Product Slice'

assert_contains "references/requirement-management.md" "## Requirements Discussion Intake"
assert_contains "references/requirement-management.md" 'Human original source materials remain byte-stable.'
assert_contains "references/requirement-management.md" 'Reviewed/recorded does not mean accepted for implementation.'
assert_contains "references/requirement-management.md" 'Features reference Requirement Sets; Requirements own sources, product meaning, and lifecycle.'
assert_contains "templates/requirement-set-README.md" '## Effective Product Definition'
assert_contains "templates/requirement-set-README.md" 'Product Review confirmation does not change Requirement Status or authorize Feature start.'
assert_contains "templates/product.md" '# Product Requirement: <Requirement Name>'
assert_contains "templates/spec.md" '## Product Requirement Source'
assert_contains "templates/spec.md" '## Product Slice'

assert_contains "templates/root-AGENTS.md" 'Requirements Discussion shapes unresolved product need into one Human-reviewed Brief/Standard Requirement Product Definition before implementation.'
assert_contains "templates/root-AGENTS.md" '| Product need, meaning, scope, or delivery phases are still being shaped | Requirements Discussion | `references/requirement-management.md`, `references/product-definition.md`, `references/requirement-product-grill.md` |'
assert_contains "README.md" '**Adaptive Product Definition**'
assert_contains "Usage.md" '新 PRD 只在 `.agent-loop/requirements/<date>-<topic>/product.md`'
assert_contains "references/validation-scenarios.md" '## 74. Adaptive Requirement Product Definition'

assert_not_contains "references/runtime.md" '→ Product Brief if Needed'
assert_not_contains "templates/spec.md" 'Product Brief: product.md | none'

printf 'PASS: chat and adaptive requirements discussion entry contract is complete\n'

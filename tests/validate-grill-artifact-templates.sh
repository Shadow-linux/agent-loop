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

assert_contains "templates/product.md" '# Product Requirement: <Requirement Name>'
assert_contains "templates/product.md" 'Product Definition Profile: brief | standard'
assert_contains "templates/product.md" '## Problem / Background'
assert_contains "templates/product.md" '## Target User / Scenario'
assert_contains "templates/product.md" '## Goal / Expected Product Outcome'
assert_contains "templates/product.md" '## In Scope'
assert_contains "templates/product.md" '## Out Of Scope / Non-goals'
assert_contains "templates/product.md" '## Acceptance Direction'
assert_contains "templates/product.md" '## Source Evidence'
assert_contains "templates/product.md" '## Open Questions / Remaining Risk'
assert_contains "templates/product.md" '## Product View Applicability'
assert_contains "templates/product.md" '## Concept Definitions'
assert_contains "templates/product.md" '## Role / Permission Matrix'
assert_contains "templates/product.md" '## Primary Business Flow'
assert_contains "templates/product.md" '## Exception Paths'
assert_contains "templates/product.md" '## Product Rules'
assert_contains "templates/product.md" '## Decision Candidates'
assert_contains "templates/product.md" '## Applicable Decisions'
assert_contains "templates/product.md" '## Product Traceability'
assert_contains "templates/product.md" '## Product Human Review Evidence'

assert_contains "references/product-definition.md" 'Product Completeness Scan'
assert_contains "references/product-definition.md" 'Product View Applicability'
assert_contains "references/product-definition.md" 'PRD Helper Adapter Boundary'
assert_contains "references/product-definition.md" 'Archify Scoped Confirmation'
assert_contains "references/requirement-product-grill.md" 'Detailed new-format grill results belong in the Effective Product Definition'
assert_contains "references/stage-guides.md" 'carry the accepted results into the same Requirement `product.md` draft'
assert_contains "references/workflow-checklists.md" 'produce a Human-reviewed Brief/Standard Requirement `product.md` before Record / Archive'
assert_contains "references/validation-scenarios.md" '## 74. Adaptive Requirement Product Definition'
assert_contains "CHANGELOG.md" 'Adaptive Requirement Product Definition'

assert_not_contains "templates/product.md" 'Product Definition Profile: complex'
assert_not_contains "templates/product.md" 'Product Brief Source Gate'

python3 "$root/scripts/check-requirement-product-definition.py" \
  "$root/examples/adaptive-product-definition/requirements/2026-07-22-approval/README.md" \
  "$root/examples/adaptive-product-definition/requirements/2026-07-22-approval/product.md" \
  "$root/examples/adaptive-product-definition/features/2026-07-22-approval/spec.md"

printf 'PASS: adaptive Product Definition and grill-enriched artifact templates are complete\n'

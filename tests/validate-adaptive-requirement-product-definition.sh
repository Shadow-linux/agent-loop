#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

assert_contains() {
  local file=$1 text=$2
  grep -Fq -- "$text" "$root/$file" || {
    printf 'FAIL: %s missing: %s\n' "$file" "$text" >&2
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

assert_contains "references/runtime.md" 'Product Definition Profile: `brief | standard`'
assert_contains "references/runtime.md" 'Product Human Review confirmation cannot be bypassed for a new Effective Product Definition.'
assert_contains "references/design.md" 'A new Effective Product Definition cannot bypass Product Human Review confirmation.'
assert_contains "references/artifact-rules.md" '`requirements/<record-date>-<topic>/product.md`'
assert_contains "references/product-definition.md" '# Adaptive Product Definition'
assert_contains "templates/product.md" 'Product Definition Profile: brief | standard'
assert_contains "templates/spec.md" '## Product Slice'
assert_contains "references/product-definition.md" 'Product Definition Depth Scan'
assert_contains "references/product-definition.md" 'Product Completeness Scan'
assert_contains "references/product-definition.md" '一次只向人类确认一个阻塞问题'
assert_contains "references/product-definition.md" 'Product Review confirmation does not authorize Requirement acceptance, Feature start, ADR acceptance, code execution, or Git actions.'
assert_contains "references/requirement-management.md" 'Human original source materials remain byte-stable'
assert_contains "references/requirement-management.md" 'YYYY-MM-DD-product-follow-up-<slug>.md'
assert_contains "references/skill-routing.md" 'Requirement `product.md` draft'
assert_contains "references/external-skill-adapters.md" 'Do not create native `feature_list.md`, `PRD.md`, Feature `product.md`, prototype deployment, or helper-owned output trees.'
assert_contains "references/product-definition.md" 'Archify Scoped Confirmation'
assert_contains "references/product-definition.md" 'Archify unavailable does not block Product Human Review'
assert_contains "references/product-brief.md" 'Legacy Feature Product Brief Compatibility'
assert_contains "references/project-decisions.md" 'Effective Product Definition'
assert_contains "references/project-decisions.md" 'Effective Concept Foundation'
assert_contains "references/runtime.md" 'Product Definition Depth Scan, Product Completeness Scan, Concept Foundation, Requirement Product Model, and derived visual generation are internal Requirements Discussion methods'
assert_contains "references/runtime.md" 'Feature Spec with Product Slice'
assert_contains "references/product-brief.md" 'Do not create `feature/product.md` for new work.'
assert_contains "templates/requirement-set-README.md" '## Effective Product Definition'
assert_contains "templates/requirement-set-README.md" 'Product Review confirmation does not change Requirement Status or authorize Feature start.'
assert_not_contains "references/runtime.md" '→ Product Brief if Needed'
assert_not_contains "references/design.md" '`product.md` is optional feature-level product understanding'
assert_not_contains "references/product-definition.md" 'Product Definition Profile: complex'
assert_not_contains "references/product-definition.md" 'Product Review Board'
assert_not_contains "references/product-definition.md" 'Product Design Hub'
assert_not_contains "references/product-definition.md" 'Product Workbench'
assert_contains "references/workflow-checklists.md" 'Write accepted Requirements Discussion output to the Requirement `product.md` draft'
assert_not_contains "references/workflow-checklists.md" 'detailed requirements-discussion output to `requirement.md`'
assert_contains "references/validation-scenarios.md" 'choose `standard` because cross-role authority, state, flow, exception, fact ownership, and historical conflict are material'
assert_contains "references/validation-scenarios.md" 'do not use the general human-bypass wording to cross Product Human Review for a new Effective Product Definition'
assert_contains "references/human-review-summary.md" 'Product Human Review confirmation is non-bypassable for a new Effective Product Definition'
assert_contains "Usage.md" 'Requirement `product.md` 会承接术语、主流程、异常路径、事实源、历史冲突、验收场景和 Decision Candidates'
assert_contains "references/artifact-rules.md" '`requirements/<record-date>-<topic>/README.md`'
assert_not_contains "references/artifact-rules.md" '`requirements/<archive-date>-<topic>/README.md`'
assert_not_contains "references/stage-guides.md" '<archive-date>-<topic>'
assert_not_contains "references/document-templates.md" '<archive-date>-<topic>'
assert_not_contains "references/feature-follow-up.md" '<archive-date>-<topic>'
assert_not_contains "references/recovery-and-backfill.md" '<archive-date>-<topic>'
assert_not_contains "README.md" 'Message Intent → Chat And Requirements Discussion if needed'
assert_contains "SKILL.md" 'examples/adaptive-product-definition/'
assert_contains "examples/concept-foundation-refund/product.md" 'Legacy Feature Product Brief Example'

printf 'PASS: adaptive Requirement Product Definition ownership, routing, gates, helper, visual, and compatibility contract is complete\n'

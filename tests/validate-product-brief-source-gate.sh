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

assert_contains "references/product-brief.md" '# Legacy Feature Product Brief Compatibility'
assert_contains "references/product-brief.md" 'Do not create `feature/product.md` for new work.'
assert_contains "references/product-brief.md" 'Read an existing Feature Product Brief during Resume, Follow-up, Review, Close, or Recovery.'
assert_contains "references/product-brief.md" 'If it conflicts with the Effective Product Definition, stop for Requirement conflict/recovery; do not rewrite either source silently.'
assert_contains "references/stage-guides.md" '## Legacy Feature Product Brief Compatibility (Non-stage)'
assert_contains "references/workflow-checklists.md" 'New Feature work does not create Feature `product.md`'
assert_contains "references/external-skill-adapters.md" 'Do not create native `feature_list.md`, `PRD.md`, Feature `product.md`, prototype deployment, or helper-owned output trees.'
assert_contains "references/skill-routing.md" '| Legacy Product Brief compatibility | no new writer helper |'
assert_contains "Usage.md" '已有 legacy Feature `product.md` 继续可读'
assert_contains "CHANGELOG.md" 'Stopped new Feature Product Brief authoring'

assert_not_contains "references/runtime.md" 'Product Brief if Needed'
assert_not_contains "templates/spec.md" 'Product Brief: product.md | none'

printf 'PASS: legacy Product Brief reader and new-writer stop contract is complete\n'

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

assert_contains "CHANGELOG.md" "Adaptive Requirement Product Definition"
assert_contains "Usage.md" '新 PRD 只在 `.agent-loop/requirements/<date>-<topic>/product.md`'
assert_contains "Usage.md" 'Product Human Review 确认“这份产品定义准确”'
assert_contains "Usage.md" 'Requirement Product Definition 起草'
assert_contains "README.md" "Shape Requirements Before Features"
assert_contains "README.md" "Requirement/Product Grill"
assert_contains "README.md" "Adaptive Product Definition"
assert_contains "README.md" 'New Feature work creates no Feature `product.md`'

printf 'PASS: adaptive requirement/product human docs are complete\n'

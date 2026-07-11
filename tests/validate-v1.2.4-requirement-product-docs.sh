#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

assert_contains() {
  local file=$1
  local text=$2
  if ! grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s missing required text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_contains "CHANGELOG.md" "Documented the human-facing Requirement/Product Grill and Product Brief Source Gate usage"

assert_contains "Usage.md" "requirement document 会承接术语、主流程、异常路径、事实源、历史冲突、验收场景和 Decision Candidates"
assert_contains "Usage.md" "Product Brief Source Gate"
assert_contains "Usage.md" "如果只是整理产品意图，可以先保留在 requirement artifact 或回复草稿"

assert_contains "README.md" "Shape Requirements Before Features"
assert_contains "README.md" "Requirement/Product Grill"
assert_contains "README.md" "Product Brief Source Gate"

printf 'PASS: v1.2.4 requirement/product human docs are complete\n'

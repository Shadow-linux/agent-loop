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

assert_contains "references/product-brief.md" "## Product Brief Source Gate"
assert_contains "references/product-brief.md" 'If the latest human message comes from `chat` or `requirements-discussion` and asks to write `product.md`, create a Product Brief, or “落到 product.md”, do not create feature `product.md` directly.'
assert_contains "references/product-brief.md" "First ask whether to create or reference a requirement set, or confirm feature start and create the feature-level Product Brief."
assert_contains "references/product-brief.md" 'Without a requirement source and confirmed feature context, do not create feature `product.md`.'
assert_contains "references/product-brief.md" "Product Brief human confirmation is not the same as feature-start confirmation."

assert_contains "references/stage-guides.md" "Product Brief Source Gate"
assert_contains "references/stage-guides.md" 'If the human asks from `chat` or `requirements-discussion` to write `product.md`, first ask whether to create/reference a requirement set or confirm feature start.'
assert_contains "references/stage-guides.md" "Do not enter Product Brief If Needed directly from requirements discussion without a requirement source or confirmed feature context."

assert_contains "references/workflow-checklists.md" "Product Brief Source Gate"
assert_contains "references/workflow-checklists.md" "If the request says write product.md / 落到 product.md from chat or requirements discussion, ask whether to create/reference a requirement set or confirm feature start."
assert_contains "references/workflow-checklists.md" "Do not write feature product.md until a requirement source and confirmed feature context exist."

assert_contains "references/external-skill-adapters.md" "Product Brief Source Gate"
assert_contains "references/external-skill-adapters.md" 'External PRD/product helpers cannot turn chat or requirements discussion directly into feature `product.md`.'
assert_contains "references/skill-routing.md" "translated into local \`product.md\` only after Product Brief Source Gate passes"

assert_contains "references/validation-scenarios.md" "Product Brief Source Gate"
assert_contains "references/validation-scenarios.md" 'do not create feature `product.md` directly'
assert_contains "references/validation-scenarios.md" "ask whether to create/reference a requirement set or confirm feature start"

assert_contains "Usage.md" "落到 product.md"
assert_contains "CHANGELOG.md" "Hardened the Product Brief Source Gate"

printf 'PASS: product brief source gate contract is complete\n'

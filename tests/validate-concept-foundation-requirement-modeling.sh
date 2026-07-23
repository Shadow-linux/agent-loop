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

assert_before() {
  local file=$1 first=$2 second=$3
  ruby -e '
    content = File.read(ARGV.fetch(0))
    first_at = content.index(ARGV.fetch(1))
    second_at = content.index(ARGV.fetch(2))
    abort "FAIL: missing ordering marker" unless first_at && second_at
    abort "FAIL: wrong ordering" unless first_at < second_at
  ' "$root/$file" "$first" "$second"
}

assert_contains "SKILL.md" "Concept Foundation"
assert_contains "SKILL.md" "Requirement Product Model"
assert_contains "references/design.md" "Concept Foundation is an internal Requirements Discussion / Requirement Product Grill method, not a canonical stage"
assert_contains "references/runtime.md" "## Human Grill Contract"
assert_before "references/runtime.md" "inspect available evidence" "extract candidate concepts"
assert_before "references/runtime.md" "extract candidate concepts" "present one recommended definition"
assert_before "references/runtime.md" "present one recommended definition" "ask exactly one downstream-blocking question"
assert_contains "references/runtime.md" 'candidate | accepted | reopened | concept-foundation-not-needed'
assert_contains "references/runtime.md" 'Standard `Product View Applicability` records `included | not-applicable` with evidence; do not create placeholder IDs.'

assert_contains "references/requirement-product-grill.md" "## Concept Foundation"
assert_contains "references/requirement-product-grill.md" "## Human Grill Contract"
assert_contains "references/requirement-product-grill.md" "Concept Candidate Inventory"
assert_contains "references/requirement-product-grill.md" "one downstream-blocking question"
assert_contains "references/requirement-product-grill.md" "Requirement Product Model Derivation"
assert_contains "references/requirement-product-grill.md" 'Do not create a placeholder model merely to populate a category'
assert_contains "references/product-definition.md" "Product View Applicability"
assert_contains "references/product-definition.md" "一次只向人类确认一个阻塞问题"
assert_contains "references/requirement-management.md" "Effective Product Definition"
assert_contains "references/requirement-management.md" "Effective Concept Foundation"
assert_contains "templates/requirement-set-README.md" "## Effective Product Definition"
assert_contains "templates/product.md" "## Concept Definitions"
assert_contains "templates/product.md" "## Concept Relationships"
assert_contains "templates/product.md" "## Role / Permission Matrix"
assert_contains "templates/product.md" "## Commands / Events"
assert_contains "templates/product.md" "## Product State Model"
assert_contains "templates/product.md" "## Requirement Product Model"
assert_contains "templates/product.md" "## Product View Applicability"
assert_contains "templates/spec.md" "## Product Requirement Source"
assert_contains "templates/spec.md" "## Product Slice"
assert_contains "references/project-decisions.md" "Effective Product Definition"
assert_contains "references/project-decisions.md" "Product Rules use source anchors"

assert_contains "templates/root-AGENTS.md" '| Product need, meaning, scope, or delivery phases are still being shaped | Requirements Discussion | `references/requirement-management.md`, `references/product-definition.md`, `references/requirement-product-grill.md` |'
assert_contains "templates/root-AGENTS.md" "Semantic Gate"
assert_not_contains "templates/root-AGENTS.md" "| Concept Foundation |"
assert_not_contains "references/product-definition.md" "Product Definition Profile: complex"
assert_not_contains "references/document-templates.md" ".agent-loop/concepts/"

ruby -e '
  content = File.read(ARGV.fetch(0))
  section = content[/## Stage Order\n(.*?)(?=\n## |\z)/m, 1]
  abort "FAIL: runtime Stage Order section missing" unless section
  if section.lines.any? { |line| line.strip == "Concept Foundation" || line.match?(/(?:^|→)\s*Concept Foundation\s*(?:→|$)/) }
    abort "FAIL: Concept Foundation must not be a canonical stage"
  end
' "$root/references/runtime.md"

if [ -e "$root/.agent-loop" ]; then
  printf 'FAIL: skill source repository must not contain target-project .agent-loop artifacts\n' >&2
  exit 1
fi

python3 "$root/scripts/check-concept-foundation-trace.py" \
  "$root/examples/concept-foundation-refund/requirement.md" \
  "$root/examples/concept-foundation-refund/product.md" \
  "$root/examples/concept-foundation-refund/spec.md"

python3 "$root/scripts/check-concept-foundation-trace.py" --requirement-product \
  "$root/tests/fixtures/adaptive-product-definition/standard-valid/README.md" \
  "$root/tests/fixtures/adaptive-product-definition/standard-valid/product.md" \
  "$root/tests/fixtures/adaptive-product-definition/standard-valid/spec.md"

(cd "$root" && python3 -m unittest tests/test_concept_foundation_trace.py)

if python3 "$root/scripts/check-concept-foundation-trace.py" \
  "$root/tests/fixtures/concept-foundation/invalid-unaccepted/requirement.md" \
  "$root/tests/fixtures/concept-foundation/invalid-unaccepted/product.md" \
  "$root/tests/fixtures/concept-foundation/invalid-unaccepted/spec.md" >/dev/null 2>&1; then
  printf 'FAIL: unaccepted legacy Concept Foundation fixture unexpectedly passed\n' >&2
  exit 1
fi

printf 'PASS: internal Concept Foundation, adaptive model, new Product Slice, and legacy trace contract is complete\n'

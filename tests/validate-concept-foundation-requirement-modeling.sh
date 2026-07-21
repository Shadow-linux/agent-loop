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

assert_not_contains() {
  local file=$1
  local text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s contains forbidden text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_before() {
  local file=$1
  local first=$2
  local second=$3
  ruby -e '
    content = File.read(ARGV.fetch(0))
    first = ARGV.fetch(1)
    second = ARGV.fetch(2)
    first_at = content.index(first)
    second_at = content.index(second)
    abort "FAIL: #{ARGV.fetch(0)} missing ordering marker: #{first}" unless first_at
    abort "FAIL: #{ARGV.fetch(0)} missing ordering marker: #{second}" unless second_at
    abort "FAIL: #{ARGV.fetch(0)} must place #{first} before #{second}" unless first_at < second_at
  ' "$root/$file" "$first" "$second"
}

# Published controller/design/runtime placement and gate contract.
assert_contains "SKILL.md" "Concept Foundation"
assert_contains "SKILL.md" "Requirement Product Model"
assert_contains "references/design.md" "Concept Foundation is an internal Requirements Discussion / Requirement Product Grill method, not a canonical stage"
assert_contains "references/runtime.md" "## Concept Foundation Routing"
assert_contains "references/runtime.md" "## Human Grill Contract"
assert_before "references/runtime.md" "inspect available evidence" "extract candidate concepts"
assert_before "references/runtime.md" "extract candidate concepts" "present one recommended definition"
assert_before "references/runtime.md" "present one recommended definition" "ask exactly one downstream-blocking question"
assert_contains "references/runtime.md" 'candidate | accepted | reopened | concept-foundation-not-needed'
assert_contains "references/runtime.md" 'Do not enter Business Flow, State Model, or Product Data Model while a triggered Concept Foundation is `candidate` or `reopened`.'

# Phase 1: evidence-first candidates, single Human Grill question, and lightweight bypass.
assert_contains "references/requirement-product-grill.md" "## Concept Foundation"
assert_contains "references/requirement-product-grill.md" "## Human Grill Contract"
assert_contains "references/requirement-product-grill.md" "Concept Candidate Inventory"
assert_contains "references/requirement-product-grill.md" "Concept ID"
assert_contains "references/requirement-product-grill.md" "concept-foundation-not-needed"
assert_contains "references/requirement-product-grill.md" "one downstream-blocking question"
assert_contains "references/requirement-management.md" "Concept Foundation Status"
assert_contains "references/requirement-management.md" "Effective Concept Foundation"
assert_contains "references/requirement-management.md" "append-only Concept Foundation follow-up"
assert_contains "references/stage-guides.md" "Concept Foundation Gate"
assert_contains "references/workflow-checklists.md" "## Concept Foundation Gate"
assert_contains "templates/requirement-set-README.md" "## Effective Concept Foundation"
assert_contains "templates/requirement-set-README.md" "Effective Source:"

# Phase 1/2 requirement document order and product-model derivation.
assert_before "references/document-templates.md" "## Concept Foundation" "## Primary Business Flow"
assert_before "references/document-templates.md" "## Concept Definitions" "## Concept Relationships"
assert_before "references/document-templates.md" "## Concept Relationships" "## Product State Model"
assert_before "references/document-templates.md" "## Product State Model" "## Requirement Product Model"
assert_contains "references/document-templates.md" "## Concept Candidate Inventory"
assert_contains "references/document-templates.md" "## Concept Definitions"
assert_contains "references/document-templates.md" "## Concept Relationships"
assert_contains "references/document-templates.md" "## Role / Permission Matrix"
assert_contains "references/document-templates.md" "Permission Rule ID"
assert_contains "references/document-templates.md" "PERM-01"
assert_contains "references/document-templates.md" "## Commands / Events"
assert_contains "references/document-templates.md" "## Product State Model"
assert_contains "references/document-templates.md" "## Requirement Product Model"
assert_contains "references/document-templates.md" "## Concept-To-Product Traceability"
assert_contains "references/document-templates.md" "EX-01"
assert_contains "references/document-templates.md" "Human Confirmation"

# Phase 2 consumers cite accepted product semantics instead of redefining them.
assert_contains "references/product-brief.md" "Accepted Concept Foundation"
assert_contains "references/product-brief.md" "Product Brief consumes the accepted Requirement Product Model"
assert_contains "templates/product.md" "## Accepted Concept References"
assert_contains "templates/product.md" "## Requirement Product Model Coverage"
assert_contains "templates/spec.md" "## Accepted Concept References"
assert_contains "templates/spec.md" "## Requirement Product Model Trace"
assert_contains "references/project-decisions.md" "PRD / Requirement Product Model owns product meaning"
assert_contains "references/project-decisions.md" "ADR consumes accepted product semantics"

# Root owns the Requirements first hop and Semantic Gate; the detailed method stays in its reference.
assert_contains "templates/root-AGENTS.md" '| Product need, meaning, scope, or delivery phases are still being shaped | Requirements Discussion | `references/requirement-management.md`, `references/requirement-product-grill.md` |'
assert_contains "templates/root-AGENTS.md" "Semantic Gate"
assert_contains "references/requirement-product-grill.md" "## Concept Foundation"
assert_contains "references/project-guidance.md" "Concept Foundation Gate"
assert_contains "README.md" "Concept Foundation"
assert_contains "Usage.md" "一次只确认一个真正阻塞后续模型的问题"
assert_contains "references/validation-scenarios.md" "Concept Foundation And Product Model Derivation"
assert_contains "references/human-review-summary.md" "## Concept Foundation Approval"
assert_contains "references/stage-guides.md" "Concept Foundation Human Review Summary"

# Explicit Phase 3/4 and artifact-path exclusions.
assert_not_contains "templates/root-AGENTS.md" "| Concept Foundation |"
ruby -e '
  content = File.read(ARGV.fetch(0))
  section = content[/## Stage Order\n(.*?)(?=\n## |\z)/m, 1]
  abort "FAIL: runtime Stage Order section missing" unless section
  if section.lines.any? { |line| line.strip == "Concept Foundation" || line.match?(/(?:^|→)\s*Concept Foundation\s*(?:→|$)/) }
    abort "FAIL: Concept Foundation must not be a canonical stage"
  end
' "$root/references/runtime.md"
assert_not_contains "templates/decision.md" "Concept To Technical Representation"
assert_not_contains "templates/decision.md" "Concept ID | Product Meaning | Technical Representation"
assert_not_contains "references/project-decisions.md" "Phase 1/2"
assert_not_contains "templates/decision.md" "Phase 1/2"
assert_not_contains "references/document-templates.md" ".agent-loop/concepts/"
assert_not_contains "references/document-templates.md" "concept-foundation.yaml"
assert_not_contains "references/document-templates.md" "concept-foundation.json"
if [ -e "$root/.agent-loop/concepts" ] || [ -e "$root/.agent-loop" ]; then
  printf 'FAIL: skill source repository must not contain target-project .agent-loop artifacts\n' >&2
  exit 1
fi

# Behavioral artifact trace: valid chain passes; unaccepted and detached chains fail.
python3 "$root/scripts/check-concept-foundation-trace.py" \
  "$root/examples/concept-foundation-refund/requirement.md" \
  "$root/examples/concept-foundation-refund/product.md" \
  "$root/examples/concept-foundation-refund/spec.md"

assert_contains "examples/concept-foundation-refund/requirement.md" "| PERM-ADMIN-SETTLEMENT | C-REFUND-ADMIN | C-REFUND-SETTLEMENT |"

(cd "$root" && python3 -m unittest tests/test_concept_foundation_trace.py)

if python3 "$root/scripts/check-concept-foundation-trace.py" \
  "$root/tests/fixtures/concept-foundation/invalid-unaccepted/requirement.md" \
  "$root/tests/fixtures/concept-foundation/invalid-unaccepted/product.md" \
  "$root/tests/fixtures/concept-foundation/invalid-unaccepted/spec.md" >/dev/null 2>&1; then
  printf 'FAIL: unaccepted Concept Foundation fixture unexpectedly passed\n' >&2
  exit 1
fi

if python3 "$root/scripts/check-concept-foundation-trace.py" \
  "$root/tests/fixtures/concept-foundation/invalid-detached-model/requirement.md" \
  "$root/tests/fixtures/concept-foundation/invalid-detached-model/product.md" \
  "$root/tests/fixtures/concept-foundation/invalid-detached-model/spec.md" >/dev/null 2>&1; then
  printf 'FAIL: detached product-model fixture unexpectedly passed\n' >&2
  exit 1
fi

printf 'PASS: Concept Foundation Phase 1/2 runtime and artifact trace contract is complete\n'

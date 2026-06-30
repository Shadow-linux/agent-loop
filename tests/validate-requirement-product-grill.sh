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

assert_contains "SKILL.md" "references/requirement-product-grill.md"
assert_contains "SKILL.md" 'Load `references/requirement-product-grill.md` during Requirements Discussion, Product Brief, or Brainstorm / Clarify when requirements include ambiguous terminology, domain boundaries, business flows, exception paths, conflicting prior feature behavior, or decision signals'
assert_contains "SKILL.md" '`CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/`'

assert_contains "references/runtime.md" "Requirement/Product Grill"
assert_contains "references/runtime.md" "grill-with-docs style clarification"
assert_contains "references/runtime.md" "does not create a new stage"

assert_contains "references/requirement-product-grill.md" "# Requirement/Product Grill"
assert_contains "references/requirement-product-grill.md" "Requirement/Product Grill is a clarification method, not a PRD generator, not an ADR generator, and not a new agent-loop stage."
assert_contains "references/requirement-product-grill.md" "Grill early; synthesize later; route decision signals through Decision Scan."
assert_contains "references/requirement-product-grill.md" "one blocking question at a time"
assert_contains "references/requirement-product-grill.md" "agent recommended answer"
assert_contains "references/requirement-product-grill.md" '提问前先检查相关过往 feature 的 `product.md`、`spec.md`、`tests.md`、`notes.md`'
assert_contains "references/requirement-product-grill.md" "Do not run a full feature scan"
assert_contains "references/requirement-product-grill.md" "targeted lookup"
assert_contains "references/requirement-product-grill.md" "keywords, domain objects, related requirement, same module/flow, active/paused/recent feature"
assert_contains "references/requirement-product-grill.md" "If prior feature artifacts conflict with the current human statement, state the conflict first"
assert_contains "references/requirement-product-grill.md" "reuse the old rule, override it, or treat the statement as new scope"
assert_contains "references/requirement-product-grill.md" "Decision Candidate"
assert_contains "references/requirement-product-grill.md" 'must not directly create `.agent-loop/decisions/*.md`'
assert_contains "references/requirement-product-grill.md" "Hard to reverse"
assert_contains "references/requirement-product-grill.md" "Surprising without context"
assert_contains "references/requirement-product-grill.md" "Real trade-off"
assert_contains "references/requirement-product-grill.md" 'Do not create `CONTEXT.md`'
assert_contains "references/requirement-product-grill.md" 'Do not create `docs/adr/`'
assert_contains "references/requirement-product-grill.md" "Requirement README"
assert_contains "references/requirement-product-grill.md" "Product Brief"
assert_contains "references/requirement-product-grill.md" "Feature Spec"

assert_contains "references/stage-guides.md" "requirement-product-grill.md"
assert_contains "references/stage-guides.md" "use Requirement/Product Grill before asking humans when terminology, roles, business objects, flows, exception paths, or historical behavior are unclear"
assert_contains "references/stage-guides.md" 'run targeted lookup of relevant prior feature `product.md`, `spec.md`, `tests.md`, and `notes.md` before asking a grill question'
assert_contains "references/stage-guides.md" "send hard-to-reverse, surprising, or real-trade-off signals to Decision Scan as Decision Candidates, not accepted ADRs"

assert_contains "references/requirement-management.md" "## Requirement/Product Grill"
assert_contains "references/requirement-management.md" "Use Requirement/Product Grill during requirements discussion when terminology, business rules, flows, boundaries, exception paths, or historical feature behavior need clarification."
assert_contains "references/requirement-management.md" "Do not promote grill output to project memory, product.md, spec.md, or decisions without the owning human gate."

assert_contains "references/product-brief.md" "Requirement/Product Grill"
assert_contains "references/product-brief.md" "Product Brief synthesis starts after grill questions are resolved enough to express product intent."
assert_contains "references/product-brief.md" "to-prd-style Implementation Decisions and Testing Decisions are Decision Scan inputs, not ADRs."

assert_contains "references/skill-routing.md" "grill-with-docs style helpers"
assert_contains "references/skill-routing.md" "Requirement/Product Grill"
assert_contains "references/external-skill-adapters.md" "grill-with-docs"
assert_contains "references/external-skill-adapters.md" 'Do not create `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/` from grill-with-docs defaults'

assert_contains "references/workflow-checklists.md" "Requirement/Product Grill"
assert_contains "references/workflow-checklists.md" "Before asking a grill question, inspect project memory, requirement source, product.md, code/docs/tests, and targeted prior feature artifacts when relevant"
assert_contains "references/workflow-checklists.md" "Do not turn a grill decision signal into an accepted ADR; route it to Decision Scan"

assert_contains "references/validation-scenarios.md" "Requirement/Product Grill Lane"
assert_contains "references/validation-scenarios.md" "do targeted lookup of relevant prior feature artifacts before asking"
assert_contains "references/validation-scenarios.md" 'do not create `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/`'
assert_contains "references/validation-scenarios.md" "Decision Candidate"

assert_contains "Usage.md" "grill-with-docs"
assert_contains "Usage.md" "先问清术语、业务流程、边界和异常场景"
assert_contains "CHANGELOG.md" "Implemented the Requirement/Product Grill lane"

assert_not_contains "references/requirement-product-grill.md" "default to creating ADR"
assert_not_contains "references/requirement-product-grill.md" "create docs/adr by default"

printf 'PASS: requirement/product grill runtime contract is complete\n'

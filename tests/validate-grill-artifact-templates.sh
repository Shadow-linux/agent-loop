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

assert_contains "references/document-templates.md" "## Terminology / Domain Language"
assert_contains "references/document-templates.md" "## Roles / Operators / Permission Boundary"
assert_contains "references/document-templates.md" "## Primary Business Flow"
assert_contains "references/document-templates.md" "## Exception Paths"
assert_contains "references/document-templates.md" "## Data / Source of Truth"
assert_contains "references/document-templates.md" "## Historical Behavior / Prior Conflicts"
assert_contains "references/document-templates.md" "## Acceptance Scenarios"
assert_contains "references/document-templates.md" "## Decision Candidates"
assert_contains "references/document-templates.md" "## Product / Feature Mapping"
assert_contains "references/document-templates.md" "## Out Of Scope And Why"
assert_contains "references/document-templates.md" "When Requirement/Product Grill was used, do not leave these sections as empty headings"

assert_contains "templates/product.md" "## Primary User Journey"
assert_contains "templates/product.md" "## Edge Cases"
assert_contains "templates/product.md" "## Behavior Changes"
assert_contains "templates/product.md" "## Product Tradeoffs"
assert_contains "templates/product.md" "## Success Signals"
assert_contains "templates/product.md" "## Historical Compatibility"
assert_contains "templates/product.md" "What changes for user/operator/system:"
assert_contains "templates/product.md" "Acceptance Direction:"
assert_contains "templates/product.md" "Status: proposed | accepted | deferred | rejected | needs-decision"
assert_contains "templates/product.md" "Evidence / Source:"
assert_contains "templates/product.md" "Human Gate:"
assert_contains "templates/product.md" "Decision Scan:"

assert_contains "references/product-brief.md" "primary user journey"
assert_contains "references/product-brief.md" "edge cases"
assert_contains "references/product-brief.md" "behavior changes for user/operator/system"
assert_contains "references/product-brief.md" "product tradeoffs"
assert_contains "references/product-brief.md" "success signals"
assert_contains "references/product-brief.md" "historical compatibility"
assert_contains "references/product-brief.md" "Product Decisions must record status, evidence/source, human gate, and Decision Scan routing when applicable."

assert_contains "references/requirement-product-grill.md" "When Requirement/Product Grill was used, the owning artifact must carry grill results into structured sections, not only a prose summary."
assert_contains "references/requirement-product-grill.md" "Requirement document sections"
assert_contains "references/requirement-product-grill.md" "Product Brief sections"

assert_contains "references/stage-guides.md" 'When Requirement/Product Grill was used, the requirement document draft must include the grill-enriched sections from `document-templates.md`'
assert_contains "references/stage-guides.md" 'When Requirement/Product Grill was used before Product Brief, write the enriched `templates/product.md` sections that apply'

assert_contains "references/workflow-checklists.md" "If Requirement/Product Grill was used, verify the owning requirement document or product brief has structured sections for terminology, flows, exceptions, data/source of truth, historical conflicts, acceptance scenarios, and Decision Candidates where applicable"

assert_contains "references/validation-scenarios.md" "Grill Artifact Template Coverage"
assert_contains "references/validation-scenarios.md" "does not collapse grill results into only Background / Problem / Requirements / Open Questions"
assert_contains "references/validation-scenarios.md" "only after Product Brief Source Gate passes"
assert_contains "references/validation-scenarios.md" "records Primary User Journey, Edge Cases, Behavior Changes, Product Tradeoffs, Success Signals, and Historical Compatibility"

assert_contains "CHANGELOG.md" "Added grill-enriched requirement and product templates"

printf 'PASS: grill artifact templates contract is complete\n'

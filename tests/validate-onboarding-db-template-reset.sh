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

assert_file_exists() {
  local file=$1
  if [[ ! -f "$root/$file" ]]; then
    printf 'FAIL: expected file missing: %s\n' "$file" >&2
    exit 1
  fi
}

assert_file_absent() {
  local file=$1
  if [[ -e "$root/$file" ]]; then
    printf 'FAIL: obsolete template still exists: %s\n' "$file" >&2
    exit 1
  fi
}

expected=$'batch-review.md\ncoverage-matrix.md\ndeep-dive.md\nonboarding-plan.md\nonboarding-spec.md'
actual=$(find "$root/templates/onboarding-db" -maxdepth 1 -type f -name '*.md' -exec basename {} \; | sort)
if [[ "$actual" != "$expected" ]]; then
  printf 'FAIL: onboarding-db template set mismatch\nExpected:\n%s\nActual:\n%s\n' "$expected" "$actual" >&2
  exit 1
fi

assert_file_exists "templates/onboarding-db/onboarding-spec.md"
assert_file_exists "templates/onboarding-db/onboarding-plan.md"
assert_file_exists "templates/onboarding-db/deep-dive.md"
assert_file_exists "templates/onboarding-db/coverage-matrix.md"
assert_file_exists "templates/onboarding-db/batch-review.md"

assert_file_absent "templates/onboarding-db/module-template.md"
assert_file_absent "templates/onboarding-db/flow-template.md"
assert_file_absent "templates/onboarding-db/evidence-graph.md"
assert_file_absent "templates/onboarding-db/core-flow-deep-trace.md"
assert_file_absent "templates/onboarding-db/core-module-deep-dive.md"
assert_file_absent "templates/onboarding-db/diagram.md"
assert_file_absent "templates/onboarding-db/README.md"
assert_file_absent "templates/onboarding-db/star-deep-dive.md"

assert_contains "references/project-onboarding-scan.md" "Onboarding DB is delivered like a feature: spec first, plan second, batch implementation third, review before completion."
assert_contains "references/project-onboarding-scan.md" 'Do not create directory-first module/flow/detail files during Deep onboarding before `onboarding-spec.md` and `onboarding-plan.md` are accepted.'
assert_contains "references/project-onboarding-scan.md" "Deep Onboarding has no total document count cap."
assert_contains "references/project-onboarding-scan.md" "Batch size is review pacing, not a total limit."
assert_contains "references/onboarding-db-templates.md" "The onboarding-db template directory intentionally contains only five templates"
assert_contains "references/onboarding-db-templates.md" "Deleted legacy form templates"
assert_contains "references/workflow-checklists.md" 'Write or refresh `onboarding-spec.md` before Deep onboarding detail docs.'
assert_contains "references/workflow-checklists.md" 'Write or refresh `onboarding-plan.md` with batches, batch review cadence, and split rationale before writing deep-dive docs.'
assert_contains "references/validation-scenarios.md" "Spec-First Onboarding Blocks Directory-First File Spray"

assert_contains "templates/onboarding-db/onboarding-spec.md" "## Required-Core Topic Inventory"
assert_contains "templates/onboarding-db/onboarding-plan.md" "## Batch Cadence And Split Gate"
assert_contains "templates/onboarding-db/deep-dive.md" "## Phase-By-Phase Deep Dive"
assert_contains "templates/onboarding-db/deep-dive.md" "## Code Evidence And Symbols"
assert_contains "templates/onboarding-db/deep-dive.md" "## Failure / Retry / Idempotency / Compensation"
assert_contains "templates/onboarding-db/coverage-matrix.md" "newcomer-ready requires an accepted deep-dive doc"
assert_contains "templates/onboarding-db/batch-review.md" "No file-count completion"

printf 'PASS: onboarding-db template reset contract is complete\n'

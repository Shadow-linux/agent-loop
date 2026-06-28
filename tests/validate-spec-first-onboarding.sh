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
    printf 'FAIL: %s still contains obsolete text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_contains "SKILL.md" "There is only one project-understanding onboarding mode: Deep Onboarding."
assert_contains "SKILL.md" 'Deep Onboarding starts with accepted `onboarding-spec.md` and accepted `onboarding-plan.md`'
assert_contains "SKILL.md" "When onboarding discovers stable project facts missing from project memory, propose or perform project memory backfill after human confirmation."

assert_contains "references/existing-project-onboarding.md" "There is only one onboarding mode for durable project understanding: Deep Onboarding."
assert_contains "references/project-onboarding-scan.md" "Onboarding DB is delivered like a feature: spec first, plan second, batch implementation third, review before completion."
assert_contains "references/project-onboarding-scan.md" 'Do not create directory-first module/flow/detail files during Deep onboarding before `onboarding-spec.md` and `onboarding-plan.md` are accepted.'
assert_contains "references/project-onboarding-scan.md" "Default Deep file budget before human expansion is 5 star docs or fewer."
assert_contains "references/project-onboarding-scan.md" "When onboarding discovers stable project facts missing from project memory, propose or perform project memory backfill after human confirmation."

assert_contains "references/onboarding-db.md" "spec/plan/coverage status"
assert_contains "references/onboarding-db.md" "the onboarding-db predates spec-first onboarding"

assert_contains "references/workflow-checklists.md" 'Write or refresh `onboarding-spec.md` before Deep onboarding detail docs.'
assert_contains "references/workflow-checklists.md" 'Write or refresh `onboarding-plan.md` with batches and file budget before writing star docs.'
assert_contains "references/workflow-checklists.md" "Do not offer Quick / Deep / Targeted onboarding modes."

assert_contains "references/validation-scenarios.md" "Spec-First Onboarding Blocks Directory-First File Spray"
assert_contains "references/validation-scenarios.md" "Single Deep Onboarding Mode"
assert_contains "references/validation-scenarios.md" "Onboarding Backfills Missing Project Memory"

assert_not_contains "SKILL.md" "Quick onboarding complete; Deep onboarding not complete."
assert_not_contains "references/existing-project-onboarding.md" "Quick onboarding complete; Deep onboarding not complete."
assert_not_contains "references/project-onboarding-scan.md" "Quick onboarding complete; Deep onboarding not complete."

printf 'PASS: spec-first single-mode onboarding contract is complete\n'

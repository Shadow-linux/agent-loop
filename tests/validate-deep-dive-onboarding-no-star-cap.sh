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
    printf 'FAIL: obsolete file still exists: %s\n' "$file" >&2
    exit 1
  fi
}

expected=$'batch-review.md\ncoverage-matrix.md\ndeep-dive.md\nonboarding-plan.md\nonboarding-spec.md'
actual=$(find "$root/templates/onboarding-db" -maxdepth 1 -type f -name '*.md' -exec basename {} \; | sort)
if [[ "$actual" != "$expected" ]]; then
  printf 'FAIL: onboarding-db template set mismatch\nExpected:\n%s\nActual:\n%s\n' "$expected" "$actual" >&2
  exit 1
fi

assert_file_exists "templates/onboarding-db/deep-dive.md"
assert_file_absent "templates/onboarding-db/star-deep-dive.md"

assert_contains "SKILL.md" "Deep Onboarding has no total document count cap."
assert_contains "references/project-onboarding-scan.md" "Deep Onboarding has no total document count cap."
assert_contains "references/project-onboarding-scan.md" "Batch size is review pacing, not a total limit."
assert_contains "references/project-onboarding-scan.md" "Human-provided examples define expected detail depth and explanation quality only."
assert_contains "references/project-onboarding-scan.md" "Do not copy example topic names, topic count, domain vocabulary, or project-specific structure unless current project evidence supports them."
assert_contains "references/project-onboarding-scan.md" 'deep-dives/<topic>.md'
assert_contains "references/workflow-checklists.md" 'Write deep-dives for all required-core onboarding topics justified by project evidence and newcomer handoff needs.'

for file in \
  "SKILL.md" \
  "README.md" \
  "Usage.md" \
  "references/project-onboarding-scan.md" \
  "references/onboarding-db-templates.md" \
  "references/workflow-checklists.md" \
  "references/stage-guides.md" \
  "templates/onboarding-db/coverage-matrix.md" \
  "templates/onboarding-db/onboarding-plan.md" \
  "templates/onboarding-db/deep-dive.md"; do
  assert_not_contains "$file" "5 star docs or fewer"
  assert_not_contains "$file" "stars/<topic>.md"
  assert_not_contains "$file" "star doc"
  assert_not_contains "$file" "star docs"
  assert_not_contains "$file" "star-deep-dive.md"
done

printf 'PASS: deep-dive onboarding has no star naming or fixed document cap\n'

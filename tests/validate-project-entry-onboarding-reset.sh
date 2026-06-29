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
    printf 'FAIL: expected file to exist: %s\n' "$file" >&2
    exit 1
  fi
}

assert_file_absent() {
  local file=$1
  if [[ -e "$root/$file" ]]; then
    printf 'FAIL: expected file to be absent: %s\n' "$file" >&2
    exit 1
  fi
}

assert_file_exists "references/project-entry-scan.md"
assert_file_absent "references/existing-project-onboarding.md"
assert_file_absent "references/project-onboarding-scan.md"
assert_file_absent "references/onboarding-db.md"
assert_file_absent "references/onboarding-db-templates.md"
assert_file_absent "references/onboarding-diagnostics.md"
assert_file_exists "references/onboarding-knowledge-base.md"
assert_file_exists "templates/onboarding-db/README.md"

assert_contains "SKILL.md" 'Load `references/project-entry-scan.md` when taking over an existing project'
assert_contains "SKILL.md" 'Do not create `.agent-loop/onboarding-db/`, module docs, flow docs, onboarding diagrams'
assert_contains "references/project-entry-scan.md" "This stage is safe-entry only."
assert_contains "references/project-entry-scan.md" "Do not create:"
assert_contains "references/project-entry-scan.md" ".agent-loop/onboarding-db/"
assert_contains "references/runtime.md" "treat the existing onboarding-db as legacy evidence only"
assert_contains "references/runtime.md" "do not create onboarding-db"
assert_contains "references/runtime.md" "do not route to the removed onboarding-db flow"
assert_contains "references/artifact-rules.md" "Do not create, refresh, reorganize, or complete onboarding-db artifacts through the removed legacy flow."
assert_contains "references/validation-scenarios.md" "Project Entry Scan Replaces Old Onboarding Generation"
assert_contains "README.md" "Project Entry Scan if needed"
assert_contains "README.md" "Evidence-Graph + DDD Onboarding"
assert_contains "README.md" "Existing legacy onboarding-db files"

assert_not_contains "SKILL.md" "references/project-onboarding-scan.md"
assert_not_contains "SKILL.md" "references/onboarding-db-templates.md"
assert_not_contains "references/workflow-checklists.md" 'Write or refresh `onboarding-spec.md`'
assert_not_contains "references/workflow-checklists.md" 'Write or refresh `onboarding-plan.md`'
assert_not_contains "README.md" "Project Onboarding Scan if needed"
assert_not_contains "README.md" 'Create durable `.agent-loop/onboarding-db/` docs through accepted `onboarding-spec.md`'
assert_not_contains "README.md" "There is only one durable project-understanding onboarding mode: Deep Onboarding"
assert_not_contains "README.md" "Learning-Path Onboarding"

printf 'PASS: Project Entry Scan onboarding reset contract is complete\n'

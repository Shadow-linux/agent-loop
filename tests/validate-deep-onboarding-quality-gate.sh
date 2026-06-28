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

assert_contains "references/project-onboarding-scan.md" "## Deep Onboarding Quality Gate"
assert_contains "references/project-onboarding-scan.md" "Deep onboarding is complete only when a newcomer can answer the primary business flow, core domain, core domain data flow, data model, service startup/config, verification strategy, and change-risk map."
assert_contains "references/project-onboarding-scan.md" "A large onboarding-db with many thin files is usable but incomplete when core modules, flows, data, startup, or verification docs lack evidence-backed detail."
assert_contains "references/project-onboarding-scan.md" "Service Startup / Config Matrix"
assert_contains "references/project-onboarding-scan.md" "Core Domain Handoff Pack"
assert_contains "references/project-onboarding-scan.md" "purpose, boundary, entrypoints, config/dependencies, core call chain, data touched, APIs/protos, tests, risks, and Evidence Chain"
assert_contains "references/project-onboarding-scan.md" "trigger, entrypoint, step-by-step call chain with file/symbol evidence, data writes, async/failure/retry behavior, verification, risks, and Evidence Chain"
assert_contains "references/project-onboarding-scan.md" "entities, key fields, storage mapping, owners, writers/readers, lifecycle/state, related flows, tests, evidence, and confidence"

assert_contains "references/onboarding-db-templates.md" "## Newcomer Handoff Quality Gate"
assert_contains "references/onboarding-db-templates.md" "Service Startup / Config Matrix"
assert_contains "references/onboarding-db-templates.md" "Core Domain Handoff Pack"
assert_contains "references/onboarding-db-templates.md" "Do not mark Deep onboarding complete only because index files, many files, or attractive diagrams exist."

assert_contains "references/workflow-checklists.md" "Confirm Deep onboarding passes the Newcomer Handoff Quality Gate, not only file-count coverage."
assert_contains "references/workflow-checklists.md" "Confirm service startup/config, core domain flows, core data flow, data model, verification strategy, and change-risk map are evidence-backed."
assert_contains "references/onboarding-db.md" "Integrity Check proves the onboarding-db is safe to read for the current goal; it does not prove Deep onboarding is complete."

assert_contains "references/validation-scenarios.md" "Spec-First Onboarding Blocks Directory-First File Spray"
assert_contains "references/validation-scenarios.md" "many small files but no newcomer handoff quality"

printf 'PASS: deep onboarding quality gate contract is complete\n'

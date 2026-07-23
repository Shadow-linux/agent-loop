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

assert_contains "references/runtime.md" "operational-support"
assert_contains "references/runtime.md" "Code-Guided Operational Support"
assert_contains "references/runtime.md" "test, run, deploy, switch account/config/model/provider"
assert_contains "references/runtime.md" "default to read-only operational support"
assert_contains "references/design.md" "Code-Guided Operational Support if Needed"
assert_contains "references/concepts.md" "Code-Guided Operational Support"

assert_contains "references/stage-guides.md" "## Code-Guided Operational Support"
assert_contains "references/stage-guides.md" "Default action is read-only code/process analysis"
assert_contains "references/stage-guides.md" "Do not create a feature workspace"
assert_contains "references/stage-guides.md" "Do not edit code, change configuration, deploy, rotate credentials, or run destructive commands"
assert_contains "references/stage-guides.md" "feature implementation or an operational change scope"
assert_contains "references/stage-guides.md" "current project functionality"

assert_contains "templates/root-AGENTS.md" '| Use, test, run, deploy, or diagnose current behavior without implementation approval | Code-Guided Operational Support | `references/stage-guides.md`, `references/runtime.md` |'
assert_contains "templates/root-AGENTS.md" "External Mutation Gate"
assert_contains "references/runtime.md" "If the request could mean either existing operational use or new implementation, ask whether the human wants help using current project functionality or feature implementation."

assert_contains "references/project-guidance.md" "Operational Support, Bug / Feature Follow-up, Requirements, Decision, Feature Construction, Project Skill, Archive, Memory Reconciliation, Lifecycle, and Chat enter through their exact Gateway rows"

assert_contains "references/workflow-checklists.md" "Operational Support Guard"
assert_contains "references/workflow-checklists.md" "lacks Bootstrap Protocol, project-outcome Agent Ownership, Message Intent Guard, Workflow Gateway Map"
assert_contains "references/workflow-checklists.md" "Classify operational support before Feature Spec, Plan Gate, or Execute"
assert_contains "references/workflow-checklists.md" "Confirm before code/config/deploy/destructive operations"

assert_contains "references/validation-scenarios.md" "Operational Support Does Not Create Feature"
assert_contains "references/validation-scenarios.md" "Ambiguous Operational Request Asks Current Functionality Or Feature Implementation"
assert_contains "references/validation-scenarios.md" "新资源账号"
assert_contains "references/validation-scenarios.md" "新账号接入一下，跑通上线"
assert_contains "references/validation-scenarios.md" "current project functionality"
assert_contains "references/validation-scenarios.md" "feature implementation"

assert_contains "templates/root-AGENTS.md" "secrets, paid quota, credentials, configuration, external service, production/staging, deploy, release, or destructive action"

assert_contains "README.md" "Operational Support"
assert_contains "Usage.md" "运行、测试和排障"

printf 'PASS: operational support guard contract is complete\n'

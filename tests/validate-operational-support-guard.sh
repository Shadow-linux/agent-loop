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

assert_contains "templates/root-AGENTS.md" "Operational Support Guard"
assert_contains "templates/root-AGENTS.md" "test, run, deploy, switch account/config/model/provider"
assert_contains "templates/root-AGENTS.md" "default to read-only code/process analysis"
assert_contains "templates/root-AGENTS.md" "ask whether they want feature implementation or help using current project functionality"

assert_contains "references/project-guidance.md" "Operational Support Guard"
assert_contains "references/project-guidance.md" "read-only operational support"
assert_contains "references/project-guidance.md" "do not create a feature, edit code, change config, deploy, or run destructive commands"

assert_contains "references/workflow-checklists.md" "Operational Support Guard"
assert_contains "references/workflow-checklists.md" "lacks Bootstrap Protocol, Agent Ownership, Operational Support Guard"
assert_contains "references/workflow-checklists.md" "Classify operational support before Feature Spec, Plan Gate, or Execute"
assert_contains "references/workflow-checklists.md" "Confirm before code/config/deploy/destructive operations"

assert_contains "references/validation-scenarios.md" "Operational Support Does Not Create Feature"
assert_contains "references/validation-scenarios.md" "Ambiguous Operational Request Asks Current Functionality Or Feature Implementation"
assert_contains "references/validation-scenarios.md" "新资源账号"
assert_contains "references/validation-scenarios.md" "新账号接入一下，跑通上线"
assert_contains "references/validation-scenarios.md" "current project functionality"
assert_contains "references/validation-scenarios.md" "feature implementation"

assert_contains "templates/root-AGENTS.md" "secrets, paid quota, production/staging external-service calls, config changes, credential rotation, deploy, release, publish, or destructive operations"

assert_contains "README.md" "Operational Support"
assert_contains "Usage.md" "操作支持"

printf 'PASS: operational support guard contract is complete\n'

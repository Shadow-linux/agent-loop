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
  if [ ! -f "$root/$file" ]; then
    printf 'FAIL: missing required file: %s\n' "$file" >&2
    exit 1
  fi
}

assert_file_exists "references/project-decisions.md"
assert_file_exists "templates/decision.md"

assert_contains "SKILL.md" "references/project-decisions.md"
assert_contains "SKILL.md" "Decision Scan / Placement"
assert_contains "SKILL.md" ".agent-loop/decisions/"

assert_contains "references/project-decisions.md" "Requirement -> Decision / ADR -> Feature"
assert_contains "references/project-decisions.md" "Decision Scan is a required lightweight check; decision files are optional human-gated artifacts."
assert_contains "references/project-decisions.md" "ADR files are usually created after a requirement is accepted and before feature spec synthesis"
assert_contains "references/project-decisions.md" "Do not create an ADR during ordinary chat or early fuzzy requirements discussion."
assert_contains "references/project-decisions.md" 'Feature-local decisions stay in `spec.md` Design Decisions.'
assert_contains "references/project-decisions.md" 'Project / cross-feature decisions go to `.agent-loop/decisions/*.md`.'
assert_contains "references/project-decisions.md" 'Creating `.agent-loop/decisions/` does not enable enterprise memory mode.'
assert_contains "references/project-decisions.md" "Apply these signals only after confirming the candidate is not feature-local."
assert_contains "references/project-memory-mode.md" 'The presence of `.agent-loop/decisions/` is not a hard trigger or soft trigger for enterprise mode.'
assert_contains "references/project-decisions.md" "Source Requirements"
assert_contains "references/project-decisions.md" "Applicable Decisions"
assert_contains "references/project-decisions.md" "Triggered Decisions"
assert_contains "references/project-decisions.md" "Implemented By"
assert_contains "references/project-decisions.md" 'decision file status cannot become `accepted` without explicit human confirmation'

assert_contains "templates/decision.md" "# ADR-0000: <Decision And Design Title>"
assert_contains "templates/decision.md" "Status: proposed"
assert_contains "templates/decision.md" "Allowed Status: proposed | accepted | superseded | deprecated"
assert_contains "templates/decision.md" "## Requirement And Decision Context"
assert_contains "templates/decision.md" "## Goals And Non-Goals"
assert_contains "templates/decision.md" "## Domain Concepts"
assert_contains "templates/decision.md" "## Business Flow"
assert_contains "templates/decision.md" "## Options Considered"
assert_contains "templates/decision.md" "## Technical Architecture Design"
assert_contains "templates/decision.md" "## Non-Functional Design"
assert_contains "templates/decision.md" "## Closure And Verification Plan"
assert_contains "templates/decision.md" "## Relationship Mapping"

assert_contains "templates/requirement-set-README.md" "## Applicable Decisions"
assert_contains "templates/requirement-set-README.md" "## Triggered Decisions"
assert_contains "templates/product.md" "## Applicable Decisions"
assert_contains "templates/product.md" "Decision Scan:"
assert_contains "templates/spec.md" "## Applicable Decisions"
assert_contains "templates/spec.md" "## Implements Decisions"
assert_contains "templates/spec.md" "## Design Decisions"

assert_contains "references/stage-guides.md" "Decision Scan / Placement If Needed"
assert_contains "references/stage-guides.md" "Requirement -> Decision / ADR -> Feature"
assert_contains "references/stage-guides.md" "run Decision Scan after requirement acceptance and before Feature Spec when a requirement is complex"
assert_contains "references/stage-guides.md" "do not enter Feature Spec when an unresolved project-level decision is required"

assert_contains "references/validation-scenarios.md" "Project Decisions / ADR Lane"
assert_contains "references/validation-scenarios.md" "Use agent-loop. 先聊钱包扣费需求，不要实现。"
assert_contains "references/validation-scenarios.md" 'recognize `Requirement -> Decision / ADR -> Feature`'
assert_contains "references/validation-scenarios.md" "do not create an accepted ADR from ordinary chat or early fuzzy requirements discussion"
assert_contains "references/validation-scenarios.md" "do not create a project-level decision for a feature-local implementation preference"
assert_contains "references/validation-scenarios.md" "do not switch to enterprise memory mode only because a decision file is created"
assert_contains "references/validation-scenarios.md" 'do not move decision records to `project/decisions/`; canonical path remains `.agent-loop/decisions/*.md`'

assert_contains "references/workflow-checklists.md" "## Decision Scan / Placement"
assert_contains "references/workflow-checklists.md" "Do not create or accept a decision file without explicit human confirmation."
assert_contains "references/workflow-checklists.md" "Verify requirement README, product.md, and spec.md decision references stay aligned."

assert_contains "references/document-templates.md" ".agent-loop/decisions/"
assert_contains "references/document-templates.md" "A new draft starts as \`Status: proposed\`; \`accepted\` status still requires explicit human acceptance of the decision itself."
assert_contains "references/document-templates.md" "## Applicable Decisions"
assert_contains "references/document-templates.md" "## Implements Decisions"
assert_contains "references/document-templates.md" "## Design Decisions"
assert_contains "README.md" "Decision / ADR"
assert_contains "README.md" "During requirements discussion, decision signals start Decision Scan only; the agent records Decision Candidates and does not create ADR files until the requirement source is accepted and the human confirms the draft."
assert_contains "Usage.md" "ADR / Decision Design"
assert_contains "Usage.md" '新的 decision draft 默认是 `proposed`'
assert_contains "Usage.md" "聊需求时遇到复杂架构取舍，要不要 ADR？"
assert_contains "CHANGELOG.md" "Implemented the lightweight Decision / ADR lane"
assert_contains "CHANGELOG.md" "Clarified the human-facing ADR trigger"

printf 'PASS: project decisions ADR lane contract is complete\n'

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
assert_contains "SKILL.md" "Design Readiness Check"
assert_contains "SKILL.md" "Decision & Design If Needed"
assert_contains "SKILL.md" ".agent-loop/decisions/"

assert_contains "references/project-decisions.md" "Requirement -> Design Readiness Check -> Decision & Design If Needed -> Feature Mapping -> Product Brief / Feature Spec"
assert_contains "references/project-decisions.md" "Decision Scan / Placement remains a lightweight method inside Decision & Design."
assert_contains "references/project-decisions.md" "A decision file remains globally optional but becomes conditionally required when shared design is required and no accepted decision already covers it."
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
assert_contains "templates/project.md" '- Decisions: `.agent-loop/decisions/` | none'
assert_contains "references/runtime.md" 'If `project.md` declares a Decisions index, list the decision files before Decision & Design, Product Brief, or Feature Spec'
assert_contains "references/runtime.md" "Decision & Design If Needed"
assert_not_contains "references/runtime.md" "Resume / Start Feature"
assert_not_contains "references/stage-guides.md" "Start Feature"
assert_not_contains "references/project-entry-scan.md" "Start Feature"
assert_not_contains "references/workflow-checklists.md" "Start Feature"
assert_not_contains "references/onboarding-knowledge-base.md" "Start Feature"
assert_not_contains "references/validation-scenarios.md" "Start Feature"

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
assert_contains "templates/decision.md" "## Design Slice Coverage"
assert_contains "templates/decision.md" "## Closure And Verification Plan"
assert_contains "templates/decision.md" "## Relationship Mapping"

assert_contains "templates/requirement-set-README.md" "## Applicable Decisions"
assert_contains "templates/requirement-set-README.md" "## Design Readiness"
assert_contains "templates/requirement-set-README.md" "## Triggered Decisions"
assert_contains "templates/product.md" "## Applicable Decisions"
assert_contains "templates/product.md" "Decision & Design Routing:"
assert_contains "templates/spec.md" "## Applicable Decisions"
assert_contains "templates/spec.md" "## Implements Decisions"
assert_contains "templates/spec.md" "## Design Decisions"

assert_contains "references/stage-guides.md" "Decision & Design If Needed"
assert_contains "references/stage-guides.md" "Requirement -> Design Readiness Check -> Decision & Design If Needed -> Feature Mapping -> Product Brief / Feature Spec"
assert_contains "references/stage-guides.md" "run Design Readiness Check after requirement acceptance and before feature construction"
assert_contains "references/stage-guides.md" "do not enter Feature Spec when required shared design is unresolved or design-slice coverage is incomplete"
assert_contains "references/product-brief.md" "Before Product To Spec, repeat Design Readiness Check. Enter Decision & Design If Needed"
assert_contains "references/product-brief.md" "Do not enter Feature Spec while required shared design remains unresolved or any required design slice is unassigned."
assert_contains "references/workflow-checklists.md" "Propose missing Applicable Decision references for human confirmation before writing \`product.md\`; do not create a duplicate ADR because a link is missing."
assert_contains "references/workflow-checklists.md" "Confirm Design Readiness is \`design-not-needed\` or \`completed\`; run Decision & Design before Feature Spec when shared design is required."

assert_contains "templates/root-AGENTS.md" "| Accepted requirement needs shared business-flow, domain, data, architecture, reliability, performance, security, or cross-feature design before feature specification | Decision & Design If Needed | \`references/project-decisions.md\` |"
assert_not_contains "templates/root-AGENTS.md" "Decision / ADR |"
assert_contains "README.md" "→ Decision & Design If Needed"

assert_contains "references/validation-scenarios.md" "Decision & Design / ADR Lane"
assert_contains "references/validation-scenarios.md" "Use agent-loop. 先聊钱包扣费需求，不要实现。"
assert_contains "references/validation-scenarios.md" 'recognize `Requirement -> Design Readiness Check -> Decision & Design If Needed -> Feature Mapping -> Product Brief / Feature Spec`'
assert_contains "references/validation-scenarios.md" "do not create an accepted ADR from ordinary chat or early fuzzy requirements discussion"
assert_contains "references/validation-scenarios.md" "do not create a project-level decision for a feature-local implementation preference"
assert_contains "references/validation-scenarios.md" "do not switch to enterprise memory mode only because a decision file is created"
assert_contains "references/validation-scenarios.md" 'do not move decision records to `project/decisions/`; canonical path remains `.agent-loop/decisions/*.md`'
assert_contains "references/validation-scenarios.md" "Accepted Decision Re-entry Before New Feature"
assert_contains "references/validation-scenarios.md" "select exactly one next stage: Decision & Design If Needed"
assert_not_contains "references/validation-scenarios.md" "select exactly one next stage: Decision / ADR"

assert_contains "references/workflow-checklists.md" "## Decision Scan / Placement"
assert_contains "references/workflow-checklists.md" "## Design Readiness Check"
assert_contains "references/workflow-checklists.md" "Do not create or accept a decision file without explicit human confirmation."
assert_contains "references/workflow-checklists.md" "Verify requirement README, product.md, and spec.md decision references stay aligned."

assert_contains "references/document-templates.md" ".agent-loop/decisions/"
assert_contains "references/document-templates.md" "A new draft starts as \`Status: proposed\`; \`accepted\` status still requires explicit human acceptance of the decision itself."
assert_contains "references/document-templates.md" "## Applicable Decisions"
assert_contains "references/document-templates.md" "## Implements Decisions"
assert_contains "references/document-templates.md" "## Design Decisions"
assert_contains "README.md" "Decision & Design / ADR"
assert_contains "README.md" "During requirements discussion, the agent records Design Readiness evidence and Decision Candidates without creating ADR files."
assert_contains "Usage.md" "Decision & Design / ADR"
assert_contains "Usage.md" '新的 decision draft 默认是 `proposed`'
assert_contains "Usage.md" "聊需求时遇到复杂架构取舍，要不要 ADR？"
assert_contains "CHANGELOG.md" "Implemented the lightweight Decision / ADR lane"
assert_contains "CHANGELOG.md" "Clarified the human-facing ADR trigger"
assert_contains "CHANGELOG.md" "Reframed the lane as Decision & Design / ADR for requirement landing"

printf 'PASS: project decisions ADR lane contract is complete\n'

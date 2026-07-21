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

assert_contains "references/project-decisions.md" "# Decision & Design / ADR Lane"
assert_contains "references/project-decisions.md" "Design Readiness Check is a required method at Requirement Archive, Product Brief, and Feature Spec boundaries; it is not a standalone stage."
assert_contains "references/project-decisions.md" "Requirement -> Design Readiness Check -> Decision & Design If Needed -> Feature Mapping -> Product Brief / Feature Spec"
assert_contains "references/project-decisions.md" "A disputed technology choice is not required."
assert_contains "references/project-decisions.md" "A decision file remains globally optional but becomes conditionally required when shared design is required and no accepted decision already covers it."
assert_contains "references/project-decisions.md" "## Design Readiness Check"
assert_contains "references/project-decisions.md" "## Design Slice Coverage"
assert_contains "references/project-decisions.md" 'No required design slice may remain `unassigned` before Feature Spec.'

assert_contains "templates/root-AGENTS.md" "| Accepted requirement needs shared technical landing before feature specification | Decision & Design If Needed | \`references/project-decisions.md\` |"
assert_contains "templates/root-AGENTS.md" "Semantic Gate"
assert_contains "references/feature-completion-check.md" "Feature close is blocked until all assigned design slices have implementation and verification evidence"
assert_not_contains "templates/root-AGENTS.md" "| Accepted complex requirement has cross-feature business-flow, architecture, data, security, performance, or long-term tradeoffs | Decision Scan / Placement If Needed |"
assert_contains "references/runtime.md" "Decision & Design If Needed"
assert_contains "references/stage-guides.md" "## Decision & Design If Needed"
assert_contains "references/workflow-checklists.md" "## Design Readiness Check"

assert_contains "templates/requirement-set-README.md" "## Design Readiness"
assert_contains "templates/decision.md" "## Design Slice Coverage"
assert_contains "templates/decision.md" "| Design Slice ID | Required Capability / Rule | Owning Feature(s) | Verification | Coverage Status |"
assert_contains "templates/spec.md" "| Decision | Design Slice ID | Responsibility | Verification | Coverage Status |"
assert_contains "templates/tasks.md" "- Design Slices:"
assert_contains "templates/tests.md" "## Design Slice Verification Matrix"
assert_contains "templates/tests.md" "| Design Slice ID | Required Verification | Test / Evidence | Status |"
assert_contains "templates/plan.md" "- Design Slices:"

assert_contains "references/workflow-checklists.md" "Do not bypass Decision & Design merely because no technology choice is disputed."
assert_contains "references/workflow-checklists.md" "Before Feature Spec, verify every required design slice has at least one planned owning feature and no required slice is unassigned."
assert_contains "references/workflow-checklists.md" "Review implementation against accepted Decision & Design records and the design slices assigned to this feature."
assert_contains "references/workflow-checklists.md" "During Drift Check, compare assigned Design Slice IDs with implementation and verification evidence."
assert_contains "references/workflow-checklists.md" "Feature close is blocked until all assigned design slices have implementation and verification evidence"
assert_contains "references/feature-completion-check.md" "accepted Decision & Design records linked by the feature"
assert_contains "references/feature-completion-check.md" "all assigned design slices have implementation and verification evidence"

assert_contains "references/validation-scenarios.md" "Complex Requirement Needs Design Without Disputed Technology"
assert_contains "references/validation-scenarios.md" "Orphan Design Slice Blocks Feature Spec"
assert_contains "references/validation-scenarios.md" "Accepted Design Conformance Before Completion"

assert_contains "docs/proposal/v1.2.x/project-decisions-adr-lane.md" "Requirement -> Design Readiness Check -> Decision & Design If Needed -> Feature Mapping -> Product Brief / Feature Spec"
assert_contains "README.md" "Decision & Design / ADR"
assert_contains "Usage.md" "这个需求会拆成多个 feature，先检查整体设计是否完整。"
assert_contains "references/runtime.md" "Project Entry, then Design Readiness and Decision & Design / Product Brief / Feature Spec / Feature Follow-up routing"
assert_contains "references/stage-guides.md" 'conditionally required `.agent-loop/decisions/000N-<slug>.md`'

printf 'PASS: Decision & Design requirement landing contract is complete\n'

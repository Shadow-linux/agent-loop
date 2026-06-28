#!/usr/bin/env bash
set -euo pipefail

assert_contains() {
  local file="$1"
  local expected="$2"
  if ! grep -Fq "$expected" "$file"; then
    echo "FAIL: expected '$expected' in $file" >&2
    exit 1
  fi
}

# H1: Focused onboarding must use the single Deep Onboarding flow, not a separate Targeted mode.
assert_contains "references/existing-project-onboarding.md" "There is only one onboarding mode for durable project understanding: Deep Onboarding."
assert_contains "references/project-onboarding-scan.md" "Focused requests use a narrow Deep Onboarding scope, not a separate Targeted mode."
assert_contains "references/stage-guides.md" "If the human asks a focused onboarding question:"
assert_contains "references/workflow-checklists.md" "For focused questions, use a narrow Deep Onboarding spec/plan and one focused deep-dive doc or existing deep-dive doc update."

# H2: Feature Completion Check must define the blocked result and next step.
assert_contains "references/feature-completion-check.md" "### Recommend Blocked"
assert_contains "references/feature-completion-check.md" "Use when completion cannot be decided or continued because a human decision, environment, access, verification dependency, or external blocker is missing"
assert_contains "references/feature-completion-check.md" "Recommend exactly one next stage: Ask Human, Diagnose Failure, Verify, Pause, or Targeted Feature Scan"
assert_contains "references/workflow-checklists.md" "If blockers prevent completion, record Result: blocked and recommend exactly one unblock stage"
assert_contains "references/stage-guides.md" "blocked with one unblock recommendation"

# H3: Feature Follow-up must not bypass Project Entry / onboarding when memory is missing.
assert_contains "references/runtime.md" "Project Entry has priority over feature-follow-up"
assert_contains "references/runtime.md" "If no .agent-loop/ or legacy agent-loop/ memory exists, do not classify directly as feature-follow-up"
assert_contains "references/feature-follow-up.md" "Feature Follow-up requires existing agent-loop memory"
assert_contains "references/design.md" "Project Entry and memory bootstrap have priority over Feature Follow-up"
assert_contains "references/stage-guides.md" "Do not enter Feature Follow-up before Project Entry has established or verified agent-loop memory"
assert_contains "references/project-guidance.md" "only after Project Entry has established or verified agent-loop memory"
assert_contains "templates/root-AGENTS.md" "only after project memory exists or Project Entry has routed through Init Project / Existing Project Onboarding"
assert_contains "references/validation-scenarios.md" "Bug Report Without Agent-Loop Memory Onboards First"

echo "PASS: v1.2.3 routing fixes contract is complete"

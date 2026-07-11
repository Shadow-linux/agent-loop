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

# M1: Auto Mode stop conditions must include Delivery Contract creation everywhere.
assert_contains "references/runtime.md" "a Delivery Contract needs creation, human acceptance, or an accepted contract needs a breaking change"

# M2: Drift Check must not route directly to close.
assert_contains "references/stage-guides.md" "Drift Check does not route directly to Close"
assert_contains "references/stage-guides.md" "next stage: Project Memory Update / Requirement Reconciliation when long-term project facts, requirement lifecycle, Delivery Phase status, or Feature Mapping changed; otherwise Feature Completion Check"
assert_contains "references/workflow-checklists.md" "Do not route directly to Close from Drift Check."
assert_contains "references/workflow-checklists.md" "Next stage is Project Memory Update / Requirement Reconciliation when long-term project facts, requirement lifecycle, Delivery Phase status, or Feature Mapping changed; otherwise Feature Completion Check."

# M3: remote-entry must outrank existing-project when both could match.
assert_contains "references/runtime.md" "Entry priority: remote-entry is evaluated before existing-project"
assert_contains "references/runtime.md" "If remote-entry and existing-project both appear to match, classify as remote-entry"

# M4: helper-friendly middle stages must explicitly scan helpers in stage guides and checklists.
for stage in "Work Breakdown" "Test Design" "E2E Discovery if Web" "Technical Design / Code Context"; do
  assert_contains "references/stage-guides.md" "Helper-friendly stage: $stage runs Stage Helper Capability Scan before fallback"
  assert_contains "references/workflow-checklists.md" "Run Stage Helper Capability Scan before fallback $stage"
done

# M5: existing-project entry must use Project Entry Scan, not the removed onboarding generation flow.
assert_contains "references/project-entry-scan.md" "This stage is safe-entry only."
assert_contains "references/project-entry-scan.md" "Do not create:"
assert_contains "references/project-entry-scan.md" ".agent-loop/onboarding-db/"
assert_contains "references/runtime.md" 'For existing projects without reliable memory, load `references/project-entry-scan.md`.'
assert_contains "references/runtime.md" "do not route to the removed onboarding-db flow"

# M6: guided onboarding request without onboarding-db must not dead-end or regenerate legacy docs.
assert_contains "references/runtime.md" "If the human asks for guided onboarding but onboarding-db is missing"
assert_contains "references/runtime.md" "do not create onboarding-db"
assert_contains "references/design.md" "Do not recreate onboarding-db through the removed legacy flow."

# M7: Standards Review triggers must be consistent.
assert_contains "references/runtime.md" "Standards Review is recorded when triggered by large project, broad diff, directory or durable boundary change, security/data change, architecture change, or human request"
assert_contains "SKILL.md" "feature-level Standards Review is required for large projects, broad diffs, directory or durable boundary changes, security/data changes, architecture changes, or human request"
assert_contains "references/workflow-checklists.md" "Perform Standards Review for large projects, broad diffs, directory or durable boundary changes, security/data changes, architecture changes, or human request"
assert_contains "references/workflow-checklists.md" "Confirm feature-level Standards Review completed when large project, broad diff, directory or durable boundary change, security/data change, architecture change, or human request applies"
assert_contains "references/feature-completion-check.md" "Did feature-level Standards Review complete when triggered by large project, broad diff, directory or durable boundary change, security/data change, architecture change, or human request?"

# M8: blocked state must recommend one next stage, not a slash-separated pair.
assert_contains "references/runtime.md" "Blocked must resolve to exactly one recommended next stage"
assert_contains "references/runtime.md" "Ask Human when the blocker is a missing decision, access, approval, environment, or external input; Diagnose Failure when the blocker is caused by observed system behavior, failing verification, or unclear technical cause"
assert_contains "references/runtime.md" "2. required verification not run but runnable in the available environment -> Verify"
assert_contains "references/runtime.md" "5. external blocker with no immediate unblock path -> Pause"
assert_contains "references/feature-completion-check.md" "## Blocked Routing Matrix"
assert_contains "references/feature-completion-check.md" "3. missing human decision/access/approval required for the next safe action -> Ask Human"
assert_contains "references/feature-completion-check.md" "2. required verification not run but runnable in the available environment -> Verify"
assert_contains "references/design.md" "Choose exactly one unblock stage"

assert_contains "references/stage-guides.md" "If submission is prepare-only and was not performed, recommend Pause with the pending submit action."
assert_contains "references/stage-guides.md" "Otherwise, if submit succeeded and the feature appears done, recommend Feature Completion Check, not Close."
assert_contains "references/submit-and-integrate.md" "Submit / Integrate does not route directly to Close."
assert_contains "references/submit-and-integrate.md" "## Ordered Exit Decision"
assert_contains "references/workflow-checklists.md" "Apply the ordered exit decision"
assert_contains "references/project-guidance.md" 'a managed block has a date-only, malformed, or different `block-version`; exact full template block-version match is required'
assert_contains "references/project-guidance.md" "Managed block maintenance rules belong here and in refresh tooling; do not require the target root \`AGENTS.md\` to include a separate Managed Block Rule prose section."
assert_contains "references/validation-scenarios.md" "for blocked state, recommend exactly one unblock stage: Ask Human, Diagnose Failure, Verify, Pause, or Targeted Feature Scan"

assert_contains "references/validation-scenarios.md" "Medium Consistency Routing"

printf 'PASS: v1.2.3 medium consistency contract is complete\n'

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

# Routing inputs are orthogonal; one precedence ladder selects the stage.
assert_contains "references/runtime.md" "## Routing Axes And Precedence"
assert_contains "references/runtime.md" 'Entry Context: `new-project` / `existing-project` / `remote-entry`'
assert_contains "references/runtime.md" 'Memory Health: `absent` / `current` / `stale` / `outside-loop`'
assert_contains "references/runtime.md" 'Work State: `idle` / `active` / `blocked` / `completion-candidate` / `paused`'
assert_contains "references/runtime.md" "Safety Stop -> Remote Discovery -> Memory Recovery -> Feature Archive Maintenance -> Active Feature Guard -> Blocker Resolution -> Intent Routing -> Normal Stage Continuation"

# Single-controller memory permits exactly one active feature.
assert_contains "references/feature-completion-check.md" "Agent Loop permits at most one Active Feature."
assert_contains "templates/project.md" "Active Feature: one feature path | none"
assert_not_contains "references/feature-completion-check.md" "unless the human explicitly chooses to keep multiple active features"
assert_not_contains "references/validation-scenarios.md" "explicitly keep multiple active features"
assert_contains "references/stage-guides.md" 'move the current feature from `Active Feature` to `Paused Features`'
assert_contains "references/stage-guides.md" 'set `Active Feature: none`'

# Deferred work must leave current scope before close; skipped is not an in-scope terminal shortcut.
assert_contains "references/artifact-rules.md" '`skipped`: explicitly removed from the current feature scope after human-approved reconciliation'
assert_not_contains "references/artifact-rules.md" '`skipped`: explicitly removed or deferred with a reason'
assert_contains "references/feature-completion-check.md" 'Are all remaining in-scope tasks `done`?'
assert_not_contains "references/feature-completion-check.md" "done, skipped with reason, or explicitly removed from scope"

# Requirement status is a deterministic roll-up of phase states.
assert_contains "references/requirement-management.md" "proposed | accepted | deferred | in-progress | partially-implemented | implemented | superseded | rejected | reference-only"
assert_contains "references/requirement-management.md" "## Delivery Phase Status Roll-up"
assert_contains "references/requirement-management.md" 'any phase is `implemented` and any other phase is not terminally implemented -> `partially-implemented`'
assert_contains "templates/requirement-set-README.md" "partially-implemented"

# Onboarding formal docs require a separate full execution gate after Tasks exist.
assert_contains "references/onboarding-knowledge-base.md" "Evidence Graph -> accept Onboarding Spec -> write Onboarding Tasks -> accept Full Execution Gate -> formal docs"
assert_contains "references/stage-guides.md" "Do not combine Onboarding Spec acceptance with the later Full Execution Gate."
assert_contains "references/validation-scenarios.md" 'require accepted `onboarding-tasks.md` and an accepted Full Execution Gate before writing formal module or flow docs'

# Evidence ambiguity is investigated; only a real ownership decision is human-gated.
assert_contains "references/feature-follow-up.md" 'When multiple candidates have medium/high match because evidence is incomplete, recommend `investigate-first`'
assert_contains "references/feature-follow-up.md" "Ask the human only when evidence is sufficient and the remaining choice is a product or ownership decision."
assert_not_contains "references/feature-follow-up.md" "If more than one candidate has medium/high match, ask the human to choose before updating docs."

# Mandatory stages and exit transitions remain explicit across checklists and summaries.
assert_contains "references/workflow-checklists.md" "## Requirement Checklist"
assert_contains "references/submit-and-integrate.md" "## Ordered Exit Decision"
assert_contains "references/stage-guides.md" "human-reviewed and recorded"
assert_not_contains "references/stage-guides.md" "requirement document accepted and archived"

# Every Feature Spec has a requirement-owned Design Readiness record.
assert_contains "references/stage-guides.md" "Every feature start must reference an accepted requirement set."
assert_contains "references/stage-guides.md" "For a narrow direct feature request, create and accept the minimum requirement set before Feature Spec."

printf 'PASS: v1.2.4 routing and lifecycle repairs are enforced\n'

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

# Published authority and fallback routing remain unique on every surface.
assert_contains "README.md" "## Published Sources"
assert_contains "README.md" '`references/design.md` owns the core model and constraints; `references/runtime.md` owns executable routing, stage order, gates, and state transitions.'
assert_not_contains "README.md" "If a reference conflicts with either design source, the design source wins."
assert_contains "templates/root-AGENTS.md" "Apply: Safety Stop -> Remote Discovery -> Memory Recovery -> Feature Archive Maintenance -> Active Feature Guard -> Blocker Resolution -> Intent Routing -> Normal Stage Continuation."
assert_contains "references/runtime.md" "Safety Stop -> Remote Discovery -> Memory Recovery -> Feature Archive Maintenance -> Active Feature Guard -> Blocker Resolution -> Intent Routing -> Normal Stage Continuation"

# Blocked routing has an explicit first-match order.
assert_contains "references/runtime.md" "Apply the blocked routing matrix in order and choose the first matching row:"
assert_contains "references/runtime.md" "1. observed failure or unclear technical cause -> Diagnose Failure"
assert_contains "references/runtime.md" "2. required verification not run but runnable in the available environment -> Verify"
assert_contains "references/runtime.md" "3. missing human decision/access/approval required for the next safe action -> Ask Human"
assert_contains "references/feature-completion-check.md" "Apply the first matching blocker route"

# Helper absence respects the already-authorized gate mode.
assert_contains "references/skill-routing.md" "In Strict Mode, ask the normal stage gate before acting. In an active auto mode, continue without a new helper-specific gate when the stage is already authorized and no stop condition applies."
assert_not_contains "references/skill-routing.md" "5. Ask the human gate."

# Onboarding has two non-bypassable gates on every controlling surface.
assert_contains "references/runtime.md" "Onboarding Spec acceptance and the later Full Execution Gate"
assert_contains "references/workflow-checklists.md" "Ask human confirmation for the Onboarding Spec only."
assert_contains "references/workflow-checklists.md" "After writing Onboarding Tasks, ask separate human acceptance of the Full Execution Gate."
assert_contains "templates/onboarding-db/onboarding-spec.md" "Spec acceptance authorizes Onboarding Tasks only; it does not authorize formal docs."
assert_not_contains "templates/onboarding-db/onboarding-spec.md" "人类已确认 Agent 可以按计划全盘执行"
assert_contains "references/onboarding-knowledge-base.md" "Focused Update is available only when the existing onboarding-db already follows an accepted Evidence-Graph + DDD Onboarding Spec"
assert_not_contains "references/validation-scenarios.md" "after plan confirmation, create and complete all planned onboarding-db docs"

# Project Entry has one safe write scope and can exit to onboarding.
assert_contains "references/stage-guides.md" "next stage: Evidence-Graph + DDD Onboarding"
assert_not_contains "references/project-entry-scan.md" ".agent-loop/requirements/"
assert_not_contains "references/project-entry-scan.md" ".agent-loop/features/"

# Requirement Checklist is a recorded prerequisite to acceptance and Work Breakdown.
assert_contains "references/stage-guides.md" "Entry: accepted spec with a recorded passed Requirement Checklist."
assert_contains "references/stage-guides.md" "human accepts the checked spec or requests revision"
assert_contains "references/runtime.md" "Feature Auto-Loop | current feature | after Feature Spec and Requirement Checklist are accepted"

# Task Auto-Run always starts with Analyze Consistency.
assert_contains "references/runtime.md" "run Analyze Consistency, then complete that task/story"
assert_contains "references/validation-scenarios.md" "run and record Analyze Consistency before executing T003"
assert_contains "SKILL.md" "Feature Auto-Loop may run Agent-ready feature work after a passed Requirement Checklist, Feature Spec acceptance, and explicit human confirmation."
assert_contains "SKILL.md" "Task Auto-Run runs Analyze Consistency before executing one accepted task/story plan"
assert_contains "references/concepts.md" "Feature-level authorization after Requirement Checklist passes and Feature Spec is accepted."
assert_contains "references/concepts.md" "The agent runs Analyze Consistency before TDD execution"

# Pause, resume, close, and reopen have complete canonical state mutation.
assert_contains "references/feature-completion-check.md" 'Move the selected feature from `Paused Features` to `Active Feature`'
assert_contains "references/feature-completion-check.md" "Resume in Strict Mode unless the human separately re-enables an auto mode"
assert_contains "references/runtime.md" "Paused work does not preempt an explicit non-feature intent"
assert_contains "references/stage-guides.md" 'set the feature lifecycle status to `closed`'
assert_contains "references/stage-guides.md" 'remove the feature from `Active Feature` and `Paused Features`'
assert_contains "references/feature-follow-up.md" 'Move the feature to `Active Feature` and set its lifecycle status to `active`'
assert_not_contains "references/feature-follow-up.md" "follow-up-active"

close_confirm_line=$(grep -nF -- "Human explicitly confirms close." "$root/references/workflow-checklists.md" | cut -d: -f1)
close_mutation_line=$(grep -nF -- 'set feature lifecycle status to `closed`' "$root/references/workflow-checklists.md" | cut -d: -f1)
if ! [ "$close_confirm_line" -lt "$close_mutation_line" ]; then
  printf 'FAIL: close confirmation must precede close-state mutation in workflow checklist\n' >&2
  exit 1
fi

# Task status and submit exits are total.
assert_contains "references/runtime.md" "blocked -> prior non-terminal status after the blocker is resolved"
assert_contains "references/runtime.md" "todo | in-progress -> skipped only after human-approved scope removal"
assert_contains "references/submit-and-integrate.md" 'submission action is explicitly `skipped`'

# Work Breakdown uses one vocabulary.
assert_contains "templates/tasks.md" "Mode: linear | parallel | barrier"
assert_not_contains "templates/tasks.md" "staged-linear"
assert_not_contains "examples/login-feature/tasks.md" "staged-linear"
assert_not_contains "examples/complex-saas-project/features/2026-05-26-project-invite-permissions/tasks.md" "staged-linear"

printf 'PASS: post-fix pressure findings are closed\n'

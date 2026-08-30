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
    printf 'FAIL: %s contains forbidden stale text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_contains "SKILL.md" "Mandatory Stage Helper Protocol"
assert_contains "SKILL.md" "A mandatory helper-backed stage cannot start stage actions"
assert_contains "SKILL.md" "A mandatory helper-backed stage cannot complete without its applicable persisted resolution evidence"
assert_contains "SKILL.md" "response-local Reviewer Helper Resolution as its first internal action"

for helper in \
  brainstorming \
  writing-plans \
  test-driven-development \
  systematic-debugging \
  verification-before-completion \
  requesting-code-review \
  subagent-driven-development
do
  assert_contains "references/skill-routing.md" "superpowers:$helper"
  assert_contains "references/skill-routing.md" "\`$helper\`"
done

assert_contains "references/skill-routing.md" "load the complete helper \`SKILL.md\` before any stage action"
assert_contains "references/skill-routing.md" "Continue to the supported alias when the canonical candidate is absent or \`load-failed\`"
assert_contains "references/skill-routing.md" "Initial resolution must be recorded before the first stage action"
assert_contains "references/skill-routing.md" "Fallback is allowed only when resolution status is \`unavailable\` or \`load-failed\`"
assert_contains "references/skill-routing.md" "Silently skipping resolution or using fallback after a successful load is a protocol violation"
assert_contains "references/skill-routing.md" "If no confirmed feature workspace exists"
assert_contains "references/skill-routing.md" "response-local pending record"
assert_contains "references/skill-routing.md" "\`loaded\` requires a non-\`none\` resolved helper"
assert_contains "references/skill-routing.md" "Method-used evidence is required before stage exit, not before the first stage action"
assert_contains "references/skill-routing.md" "Final Review uses two ordered resolution owners"
assert_contains "references/skill-routing.md" "The reviewer returns that exact record without writing files"
assert_contains "references/skill-routing.md" "\`unavailable\` requires every candidate to be absent"
assert_contains "references/skill-routing.md" "\`load-failed\` requires every discoverable candidate to have a recorded load error"

assert_contains "references/external-skill-adapters.md" "agent-loop remains the controller"
assert_contains "references/external-skill-adapters.md" "agent-loop artifact paths always override external skill default paths"
assert_contains "references/external-skill-adapters.md" "Do not create \`docs/superpowers/\`"
assert_contains "references/external-skill-adapters.md" ".agent-loop/features/<feature>/plan.md"
assert_contains "references/external-skill-adapters.md" "Subagent dispatch is not a Human Gate"
assert_contains "references/external-skill-adapters.md" "cannot create or widen authorization"
assert_contains "references/external-skill-adapters.md" "The Final Review Subagent is always read-only"
assert_contains "references/external-skill-adapters.md" "The owning Agent handles every finding disposition"
assert_contains "references/external-skill-adapters.md" "Final Reviewer: controller-fallback"
assert_contains "references/external-skill-adapters.md" "at most one diagnostic retry for that dispatcher"
assert_contains "references/external-skill-adapters.md" "Recovery Owner: runtime dispatcher"
assert_contains "references/external-skill-adapters.md" "| Feature Completion Check |"
assert_contains "references/external-skill-adapters.md" "| Pause / Close |"
assert_contains "references/stage-guides.md" "ordinary bounded repair does not automatically dispatch another reviewer"
assert_contains "references/stage-guides.md" "dispatch a fresh Final Review Subagent"

assert_contains "templates/subagent-brief.md" "## Delegated Authority"
assert_contains "templates/subagent-brief.md" "Owning Stage:"
assert_contains "templates/subagent-brief.md" "Existing Authorization:"
assert_contains "templates/subagent-brief.md" "Allowed Writes:"
assert_contains "templates/subagent-brief.md" "Forbidden Actions:"
assert_contains "templates/subagent-brief.md" "Read-Only Reviewer:"
assert_contains "templates/subagent-brief.md" "Reviewer Helper Resolution (read-only Final Review only):"
assert_contains "templates/subagent-brief.md" "Expiry:"

assert_contains "templates/notes.md" "## Stage Helper Resolutions"
assert_contains "templates/notes.md" "- Requested Helper:"
assert_contains "templates/notes.md" "- Invocation Scope:"
assert_contains "templates/notes.md" "- Candidate Results:"
assert_contains "templates/notes.md" "- Resolution Status: loaded | unavailable | load-failed"
assert_contains "templates/notes.md" "- Fallback Used: yes | no"

for stage in \
  "Brainstorm / Clarify" \
  "Plan Gate / Plan If Needed" \
  "Execute Task / Story" \
  "Diagnose Failure" \
  "Verify"
do
  assert_contains "references/stage-guides.md" "Mandatory helper: $stage"
done

assert_contains "references/stage-guides.md" "Resolve and persist Subagent coordination before dispatch"
assert_contains "references/stage-guides.md" "requesting-code-review method"
assert_not_contains "references/stage-guides.md" "Mandatory helper: Review"
assert_not_contains "references/stage-guides.md" "Mandatory helper: Subagent Execution If Approved"

assert_not_contains "references/stage-guides.md" "before fallback planning"
assert_not_contains "references/stage-guides.md" "before fallback clarification"
assert_not_contains "references/stage-guides.md" "before fallback subagent planning"
assert_not_contains "references/stage-guides.md" "before fallback execution"
assert_not_contains "references/stage-guides.md" "before fallback diagnosis"
assert_not_contains "references/stage-guides.md" "before fallback verification"
assert_not_contains "references/stage-guides.md" "before fallback review"

printf 'PASS: mandatory stage helper routing contract is complete\n'

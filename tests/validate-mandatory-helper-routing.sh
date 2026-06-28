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
assert_contains "SKILL.md" "A mandatory helper-backed stage cannot complete without a Stage Helper Resolution record"

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
assert_contains "references/skill-routing.md" "\`unavailable\` requires every candidate to be absent"
assert_contains "references/skill-routing.md" "\`load-failed\` requires every discoverable candidate to have a recorded load error"

assert_contains "references/external-skill-adapters.md" "agent-loop remains the controller"
assert_contains "references/external-skill-adapters.md" "agent-loop artifact paths always override external skill default paths"
assert_contains "references/external-skill-adapters.md" "Do not create \`docs/superpowers/\`"
assert_contains "references/external-skill-adapters.md" ".agent-loop/features/<feature>/plan.md"
assert_contains "references/external-skill-adapters.md" "Subagents must never close a feature, submit code, update project memory directly"
assert_contains "references/external-skill-adapters.md" "Only the main agent may mark a task \`done\` after Task Done Gate passes"
assert_contains "references/external-skill-adapters.md" "Expanding the approved scope requires new human confirmation"
assert_contains "references/external-skill-adapters.md" "Authorization Status must be \`active\` immediately before dispatch"
assert_contains "references/external-skill-adapters.md" "Mark the authorization \`consumed\` after the approved dispatch group returns"
assert_contains "references/external-skill-adapters.md" "Feature Close Review requires a new resolution record"
assert_contains "references/external-skill-adapters.md" "| Feature Completion Check |"
assert_contains "references/external-skill-adapters.md" "| Pause / Close |"
assert_contains "references/stage-guides.md" "Do not reuse a previous review resolution"

assert_contains "templates/subagent-brief.md" "## Dispatch Authorization"
assert_contains "templates/subagent-brief.md" "Approved At:"
assert_contains "templates/subagent-brief.md" "Approved IDs / Lanes:"
assert_contains "templates/subagent-brief.md" "Approved Boundaries:"
assert_contains "templates/subagent-brief.md" "Authorization Status: active | consumed | revoked | expired"
assert_contains "templates/subagent-brief.md" "Expires / Consumed At:"

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
  "Verify" \
  "Review" \
  "Subagent Execution If Approved"
do
  assert_contains "references/stage-guides.md" "Mandatory helper: $stage"
done

assert_not_contains "references/stage-guides.md" "before fallback planning"
assert_not_contains "references/stage-guides.md" "before fallback clarification"
assert_not_contains "references/stage-guides.md" "before fallback subagent planning"
assert_not_contains "references/stage-guides.md" "before fallback execution"
assert_not_contains "references/stage-guides.md" "before fallback diagnosis"
assert_not_contains "references/stage-guides.md" "before fallback verification"
assert_not_contains "references/stage-guides.md" "before fallback review"

printf 'PASS: mandatory stage helper routing contract is complete\n'

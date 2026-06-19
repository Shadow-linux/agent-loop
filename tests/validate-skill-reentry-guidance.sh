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

assert_contains "templates/root-AGENTS.md" "Skill Re-entry Rule"
assert_contains "templates/root-AGENTS.md" "Root AGENTS.md is a bootstrap cache, not a replacement for the agent-loop skill"
assert_contains "templates/root-AGENTS.md" "if the runtime exposes the agent-loop skill, load/use it before making agent-loop workflow decisions"
assert_contains "templates/root-AGENTS.md" "If the skill is unavailable or load-failed, follow this AGENTS.md as fallback and report that fallback"
assert_contains "templates/root-AGENTS.md" "after context compaction"
assert_contains "templates/root-AGENTS.md" "Stage Helper Capability Scan does not satisfy Skill Re-entry"

assert_contains "references/project-guidance.md" "Skill Re-entry Rule"
assert_contains "references/project-guidance.md" "Root AGENTS.md is a bootstrap cache, not a replacement for the agent-loop skill"
assert_contains "references/project-guidance.md" "if the runtime exposes the agent-loop skill, load/use it before making agent-loop workflow decisions"
assert_contains "references/project-guidance.md" "If the skill is unavailable or load-failed, follow root AGENTS.md as fallback"
assert_contains "references/project-guidance.md" "Skill Re-entry Rule is missing"
assert_contains "references/project-guidance.md" "Stage Helper Capability Scan does not satisfy Skill Re-entry"

assert_contains "references/runtime.md" "Skill Re-entry"
assert_contains "references/runtime.md" "AGENTS.md is bootstrap guidance, not a replacement for the agent-loop skill"
assert_contains "references/runtime.md" "If the current runtime exposes the agent-loop skill, load/use it before making workflow decisions"
assert_contains "references/runtime.md" "After context compaction, long-running sessions, or stage-boundary uncertainty"
assert_contains "references/runtime.md" "Stage Helper Capability Scan does not satisfy Skill Re-entry"

assert_contains "references/validation-scenarios.md" "Long-Running Agent Re-enters Agent-Loop Skill"
assert_contains "references/validation-scenarios.md" "do not claim Stage Helper Capability Scan satisfies Skill Re-entry"

printf 'PASS: skill re-entry guidance contract is complete\n'

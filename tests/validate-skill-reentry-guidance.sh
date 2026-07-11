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

assert_contains "templates/root-AGENTS.md" "Bootstrap Protocol"
assert_contains "templates/root-AGENTS.md" "Treat root \`AGENTS.md\` as a bootstrap cache, not a replacement for the \`agent-loop\` skill"
assert_contains "templates/root-AGENTS.md" "if the runtime exposes the \`agent-loop\` skill, load/use it before making \`agent-loop\` workflow decisions"
assert_contains "templates/root-AGENTS.md" "If the skill is unavailable or load-failed, force Strict Mode and suspend any existing Feature Auto-Loop or Task Auto-Run grant"
assert_contains "templates/root-AGENTS.md" "Do not Execute, write Human-gated artifacts, Submit, Pause, or Close while the controller is unavailable"
assert_contains "templates/root-AGENTS.md" "after context compaction"
assert_contains "templates/root-AGENTS.md" "Run Stage Helper Capability Scan for the current stage only after the \`agent-loop\` controller is active or unavailable/load-failed"
if grep -Fq "section:skill-reentry" "$root/templates/root-AGENTS.md"; then
  printf 'FAIL: root AGENTS template should merge skill re-entry into Bootstrap Protocol, not keep section:skill-reentry\n' >&2
  exit 1
fi

assert_contains "references/project-guidance.md" "Bootstrap Protocol must say root AGENTS.md is a bootstrap cache, not a replacement for the agent-loop skill"
assert_contains "references/project-guidance.md" "if the runtime exposes the agent-loop skill, load/use it before making agent-loop workflow decisions"
assert_contains "references/project-guidance.md" "If the skill is unavailable or load-failed, root fallback must force Strict Mode"
assert_contains "references/project-guidance.md" "Bootstrap Protocol is missing skill-loading/fallback rules"
assert_contains "references/project-guidance.md" "Stage Helper Capability Scan happens only after the controller is active or unavailable/load-failed"

assert_contains "references/runtime.md" "Bootstrap skill loading"
assert_contains "references/runtime.md" "AGENTS.md is bootstrap guidance, not a replacement for the agent-loop skill"
assert_contains "references/runtime.md" "If the current runtime exposes the agent-loop skill, load/use it before making workflow decisions"
assert_contains "references/runtime.md" "After context compaction, long-running sessions, or stage-boundary uncertainty"
assert_contains "references/runtime.md" "Stage Helper Capability Scan happens only after the agent-loop controller is active or unavailable/load-failed"

assert_contains "references/validation-scenarios.md" "Long-Running Agent Re-enters Agent-Loop Skill Through Bootstrap"
assert_contains "references/validation-scenarios.md" "do not claim Stage Helper Capability Scan replaces Bootstrap skill loading"

printf 'PASS: bootstrap skill-loading guidance contract is complete\n'

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

# Published source authority must live inside the distributable skill package.
assert_contains "SKILL.md" "The published skill package has two operational sources of truth:"
assert_contains "SKILL.md" 'references/design.md = core model and constraints'
assert_contains "SKILL.md" 'references/runtime.md = executable routing, stage order, gates, and state transitions'
assert_contains "SKILL.md" "Workspace-level design drafts are historical or planning evidence only; they cannot override the published package."
assert_not_contains "SKILL.md" "If this skill conflicts with either design source, the design source wins"

# Decision & Design must be part of the canonical design flow, not only runtime extensions.
assert_contains "references/design.md" "→ Decision & Design If Needed"
assert_contains "references/design.md" "→ Product Brief if Needed"

# Technical Design may detect a contract need, but contract files stay behind the pre-write gate.
assert_contains "references/stage-guides.md" "recommend Delivery Contract If Needed and stop before any contract file is created or updated"
assert_contains "references/stage-guides.md" "do not create or update contract files from Technical Design / Code Context"
assert_not_contains "references/stage-guides.md" 'load `delivery-contracts.md`, update the contract draft, and stop'

# A missing controller must fail closed instead of inheriting auto-mode execution rights.
assert_contains "templates/root-AGENTS.md" "If the skill is unavailable or load-failed, force Strict Mode and suspend any existing Feature Auto-Loop or Task Auto-Run grant."
assert_contains "templates/root-AGENTS.md" "Fallback is limited to Chat, read-only Project Entry, Re-Adopt / Recovery analysis, read-only Operational Support, and reporting how to restore the skill."
assert_contains "templates/root-AGENTS.md" "Do not Execute, write Human-gated artifacts, Submit, Pause, or Close while the controller is unavailable."
assert_contains "templates/root-AGENTS.md" "| Accepted plan is ready for consistency validation before code or test work | Analyze Consistency |"
assert_not_contains "templates/root-AGENTS.md" "| Accepted plan is ready for code or test work | Execute Task / Story |"
assert_contains "references/stage-guides.md" "Entry: selected execution unit is accepted, Plan Gate has passed, and Analyze Consistency has a clean recorded result."
assert_contains "templates/root-AGENTS.md" "a new dependency, migration, destructive operation, credential, external service, or long-lived boundary directory is needed"
assert_contains "templates/root-AGENTS.md" "Complex Artifact Mode detail directories"

# Behavior-changing execution has no human-pressure skip-RED path.
assert_contains "references/validation-scenarios.md" "behavior-changing execution requires RED -> verify RED -> GREEN -> verify GREEN -> REFACTOR"
assert_contains "references/validation-scenarios.md" 'non-behavior work records TDD as `not-applicable` with a reason'
assert_not_contains "references/validation-scenarios.md" "use TDD unless human explicitly changes approach"

printf 'PASS: v1.2.4 critical control repairs are enforced\n'

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

assert_contains scripts/checker_support.py 'def discover_memory_root_authority('
assert_contains scripts/feature_archive_support.py '"feature-entry-symlink"'
assert_contains scripts/feature_archive_support.py '"memory-root-alias"'
assert_contains scripts/feature_archive_support.py 'def _assert_pre_transaction_move_paths('
assert_contains scripts/check-root-agents-blocks.py 'STRUCTURAL_CURRENT:'
assert_contains scripts/check-root-agents-blocks.py 'STRUCTURAL_CHANGED:'
assert_contains scripts/check-root-agents-blocks.py 'STRUCTURAL_INVALID:'
assert_contains references/runtime.md 'One internal alias is allowed only when it resolves to an existing project directory without cycle or dual authority'
assert_contains references/design.md 'a symlinked Feature entry is not planned as a normal move'
assert_contains references/project-guidance.md 'normalized bodies only for `source:agent-loop-skill` blocks'
assert_contains references/workflow-checklists.md 'Before transaction creation, recheck that the Feature container and every move source/target path have real non-symlink move shape'
assert_contains references/validation-scenarios.md 'Feature Entry Is An Internal Symlink'
assert_contains references/validation-scenarios.md 'Same Revision Body Drift Is A Soft Structural Fact'
assert_contains Usage.md '`STRUCTURAL_CHANGED / 0` 仍需 Agent 判断'
assert_contains CHANGELOG.md '轻 Gate Authority Alias 与 Root Guidance 漂移修复'

printf 'PASS: light-gate authority alias and root structural drift contract is complete\n'

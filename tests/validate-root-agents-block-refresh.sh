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
    printf 'FAIL: %s contains retired text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

managed_count=$(grep -c '^<!-- agent-loop:managed-start' "$root/templates/root-AGENTS.md" || true)
block_version_count=$(grep -c '^<!-- agent-loop:managed-start.*block-version:' "$root/templates/root-AGENTS.md" || true)
current_block_version="1.2.3-20260625"

if [ "$managed_count" -ne "$block_version_count" ]; then
  printf 'FAIL: every root AGENTS managed block needs block-version (%s managed, %s block-version)\n' "$managed_count" "$block_version_count" >&2
  exit 1
fi

if grep '^<!-- agent-loop:managed-start' "$root/templates/root-AGENTS.md" | grep -Fvq "block-version:$current_block_version"; then
  printf 'FAIL: every root AGENTS managed block must use current full block-version: %s\n' "$current_block_version" >&2
  grep '^<!-- agent-loop:managed-start' "$root/templates/root-AGENTS.md" | grep -Fv "block-version:$current_block_version" >&2 || true
  exit 1
fi

assert_contains "templates/root-AGENTS.md" "Managed blocks are maintained by \`agent-loop\`; content outside them is human/project-owned."
assert_contains "templates/root-AGENTS.md" "When refreshing, compare each block against the current template by \`section\` and full \`block-version\`, e.g. \`$current_block_version\`. Bare versions like \`1.2.3\` are stale."
assert_contains "templates/root-AGENTS.md" "Copy template marker metadata for refreshed sections; adjust only \`source\` when the target project uses a different memory root. Ask before writing and never rewrite outside-managed content silently."
assert_not_contains "templates/root-AGENTS.md" "Agents may propose updates to managed blocks when source facts change"

assert_contains "references/project-guidance.md" "Root AGENTS Refresh Protocol"
assert_contains "references/project-guidance.md" "If the file-level managed version is equal but a block-version is missing or older than the current template, treat that block as stale."
assert_contains "references/project-guidance.md" 'Use `block-version:<agent-loop-version>-<YYYYMMDD>`; do not shorten it to the skill version alone.'
assert_contains "references/project-guidance.md" "Copy the exact start marker metadata for each refreshed section from the current root AGENTS template unless the section source must point at a target-project artifact."
assert_contains "references/project-guidance.md" 'Treat bare skill-version-only block revisions such as `block-version:1.2.3` as stale because they cannot distinguish same-version template revisions.'
assert_contains "references/project-guidance.md" 'Treat date-only block revisions such as `block-version:2026-06-27` as stale because they are not tied to the agent-loop template version.'
assert_contains "references/project-guidance.md" "If a managed block exists in the current template but is missing from root AGENTS.md, treat it as a missing managed block and propose adding it."
assert_contains "references/project-guidance.md" "Missing Managed Block Rule means root guidance refresh is required because future agents cannot know the update boundary."
assert_contains "references/project-guidance.md" "Preserve all content outside managed blocks unless the human explicitly approves cleanup, replacement, or migration."
assert_contains "references/project-guidance.md" "message-intent"

assert_contains "references/workflow-checklists.md" 'Compare each managed block `section` and `block-version` against the current root AGENTS template.'
assert_contains "references/workflow-checklists.md" "Treat missing block-version, older block-version, or missing managed sections as stale even when the file-level skill version matches."
assert_contains "references/workflow-checklists.md" 'Do not write bare `block-version:<agent-loop-version>` values; copy the full template block revision such as `block-version:1.2.3-20260625`.'
assert_contains "references/workflow-checklists.md" "Treat date-only, malformed, or different block-version values as stale; exact full template block-version match is required."
assert_contains "references/workflow-checklists.md" "If Managed Block Rule is absent, propose root guidance refresh before relying on managed blocks."

assert_contains "references/validation-scenarios.md" "Same Version But Missing Managed Block Revision"
assert_contains "references/validation-scenarios.md" "Bare Skill-Version Block Revision Is Stale"
assert_contains "references/validation-scenarios.md" "Date-Only Block Revision Is Stale"
assert_contains "references/validation-scenarios.md" "Missing Managed Block Rule Needs Refresh"
assert_contains "references/validation-scenarios.md" "block-version"

printf 'PASS: root AGENTS block refresh contract is complete\n'

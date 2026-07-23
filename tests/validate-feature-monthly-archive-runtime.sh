#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

assert_contains() {
  local file=$1
  local text=$2
  if ! grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s missing Feature Monthly Archive contract: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_not_contains() {
  local file=$1
  local text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s contains forbidden Feature Monthly Archive contract: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

for file in \
  SKILL.md \
  references/runtime.md \
  references/design.md \
  references/artifact-rules.md \
  references/feature-follow-up.md \
  references/stage-guides.md \
  references/workflow-checklists.md \
  references/human-review-summary.md \
  references/recovery-and-backfill.md \
  references/project-decisions.md \
  references/requirement-management.md \
  references/project-memory-mode.md \
  references/project-guidance.md \
  references/validation-scenarios.md; do
  assert_contains "$file" "Feature Monthly Archive"
  assert_contains "$file" "features/archive.md"
done

assert_contains templates/root-AGENTS.md '| Explicit closed-history archive or rehydrate | Feature Monthly Archive | `references/stage-guides.md`, `references/artifact-rules.md`, `references/feature-follow-up.md` |'
assert_contains templates/root-AGENTS.md "Execution Gate"

assert_contains SKILL.md "feature-archive-maintenance"
assert_contains SKILL.md "expected plan SHA-256"
assert_contains SKILL.md "Batch Human Gate"

assert_contains references/runtime.md "feature-archive-maintenance"
assert_contains references/runtime.md "scan is read-only"
assert_contains references/runtime.md "transaction journal"
assert_contains references/runtime.md "rehydrate before reopened execution"

assert_contains references/design.md "Feature ID is stable"
assert_contains references/design.md "archive state is not feature lifecycle"
assert_contains references/design.md "active / blocked / paused features stay flat"

assert_contains references/artifact-rules.md "no per-feature archive summary"
assert_contains references/artifact-rules.md "no historical/"
assert_contains references/artifact-rules.md "no Deep Archive"
assert_contains references/artifact-rules.md 'No `--force`'

assert_contains references/feature-follow-up.md "rehydrate before reopened execution"
assert_contains references/stage-guides.md "post-check"
assert_contains references/stage-guides.md "restore"
assert_contains references/workflow-checklists.md "expected plan SHA-256"
assert_contains references/human-review-summary.md "Platform evidence"
assert_contains references/recovery-and-backfill.md ".archive-txn"
assert_contains references/project-decisions.md "archived closed Feature Spec"
assert_contains references/requirement-management.md "stable Feature ID"
assert_contains references/project-memory-mode.md "features/archive.md"
assert_contains references/project-guidance.md "month archive"
assert_contains references/validation-scenarios.md "ambiguous old path"

assert_contains templates/feature-archive.md "archived or rehydrated features"
assert_contains templates/feature-archive.md "remain authoritative"

for file in SKILL.md references/runtime.md references/design.md references/artifact-rules.md; do
  assert_not_contains "$file" "Feature Monthly Archive automatically deletes"
  assert_not_contains "$file" "Feature Monthly Archive creates features/YYYY-MM/INDEX.md"
done

for file in \
  references/e2e-discovery.md \
  references/delivery-contracts.md \
  references/complex-artifacts.md \
  references/external-skill-adapters.md \
  templates/subagent-brief.md; do
  assert_not_contains "$file" ".agent-loop/features/YYYY-MM/<feature-id>/"
  assert_not_contains "$file" "execute inside an archived month directory"
done

printf 'PASS: Feature Monthly Archive runtime, gate, locator, recovery, and scope contract is complete\n'

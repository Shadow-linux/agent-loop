#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }
assert_file() { [ -f "$root/$1" ] || fail "missing required file: $1"; }
assert_contains() {
  local file=$1 text=$2
  grep -Fq -- "$text" "$root/$file" || fail "$file missing contract: $text"
}
assert_not_contains() {
  local file=$1 text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    fail "$file contains forbidden behavior: $text"
  fi
}

for file in \
  docs/proposal/v1.5.x/conflict-driven-memory-reconciliation.md \
  docs/proposal/v1.5.x/conflict-driven-memory-reconciliation-implementation-plan.md \
  references/memory-reconciliation.md \
  templates/memory-merge-report.md \
  templates/full-memory-audit-report.md \
  scripts/memory_reconciliation_support.py \
  scripts/scan-memory-reconciliation.py \
  scripts/check-memory-reconciliation.py \
  scripts/apply-memory-reconciliation.py \
  scripts/restore-memory-reconciliation.py; do
  assert_file "$file"
done

for file in SKILL.md references/design.md references/runtime.md \
  references/stage-guides.md references/workflow-checklists.md \
  references/submit-and-integrate.md references/branch-management.md; do
  assert_contains "$file" 'Post-Merge Memory Reconciliation'
done

for text in \
  'reconciliation-not-needed' \
  'Observed Memory Conflict' \
  'minimum direct evidence' \
  'latest verified facts' \
  'Only unresolved semantic choices require Human Review' \
  'conduct this review directly in the conversation' \
  'Full Memory Audit / Recovery' \
  'Memory Reconciliation does not perform the code merge.'; do
  assert_contains references/memory-reconciliation.md "$text"
done

assert_contains SKILL.md 'No conflict is `reconciliation-not-needed`: do not scan the whole memory root, create a report, or add a reconciliation gate.'
assert_contains references/runtime.md 'When none exists, use `reconciliation-not-needed`: do not scan all memory, create a report, or add a Human Gate.'
assert_contains references/stage-guides.md 'no observed conflict is `reconciliation-not-needed`; do not scan all memory, create a report, add a Human Gate'
assert_contains references/workflow-checklists.md 'With no conflict, use `reconciliation-not-needed`; do not scan all memory, create a report, add a Human Gate'
assert_contains templates/root-AGENTS.md 'No observed memory conflict means `reconciliation-not-needed`: do not scan all memory, create a report, or add a Human Gate.'
assert_contains references/memory-reconciliation.md 'Inspect only:'
assert_contains references/memory-reconciliation.md 'the observed conflict location or stable ID;'
assert_contains references/memory-reconciliation.md 'the canonical owner of the conflicting meaning;'
assert_contains references/memory-reconciliation.md 'the minimum direct references, locators, or derived indexes'
assert_contains references/memory-reconciliation.md 'the minimum code, test, config, environment, Requirement, ADR, history, or Human Decision evidence'
assert_contains references/memory-reconciliation.md 'A small conflict is reviewed in the conversation.'
assert_contains references/memory-reconciliation.md 'Do not create a report merely because a merge occurred or one Human answer was needed.'
assert_contains references/lightweight-change-lane.md 'Post-merge entry alone does not start consolidation or a full Change scan.'
assert_contains references/lightweight-change-lane.md 'read one such card only when the observed conflict directly identifies it as necessary evidence'
assert_contains references/project-guidance.md 'MM-<short-sha>-<topic>/README.md = optional complex/cross-session conflict record'
assert_contains references/project-guidance.md 'MM-<short-sha>/README.md = explicitly authorized Full Memory Audit / Recovery'
assert_contains templates/project.md 'Current Memory Merge Status: 待处理 | 待人类决定 | 已解决 | 待确认 | 已完成 | 已恢复 | none'
assert_contains references/document-templates.md 'Current Memory Merge Status: 待处理 | 待人类决定 | 已解决 | 待确认 | 已完成 | 已恢复 | none'
assert_not_contains references/lightweight-change-lane.md 'post-merge reviews'

assert_contains references/runtime.md 'Code Merge Gate -> Post-Merge Memory Reconciliation -> Memory Commit Gate'
assert_contains references/submit-and-integrate.md 'reconciliation-not-needed'
assert_contains references/submit-and-integrate.md 'Unresolved observed memory conflicts'
assert_contains references/artifact-rules.md '.agent-loop/memory-merges/MM-<merged-code-short-sha>-<conflict-topic>/README.md'
assert_contains references/artifact-rules.md '<memory-root>/memory-merges/MM-<collision-safe-short-sha>/README.md'
assert_not_contains templates/memory-merge-report.md '<!-- memory-reconciliation-plan:start -->'
assert_contains templates/memory-merge-report.md '仅列出观察到的冲突'
for audit_only_field in \
  '## Memory Record Matrix' \
  '### Expected Unchanged Paths' \
  '## Exact Rewrite Plan' \
  'Normalized Plan Hash:'; do
  assert_not_contains templates/memory-merge-report.md "$audit_only_field"
  assert_contains templates/full-memory-audit-report.md "$audit_only_field"
done
assert_contains templates/full-memory-audit-report.md '<!-- memory-reconciliation-plan:start -->'
assert_contains templates/full-memory-audit-report.md '<!-- memory-reconciliation-plan:end -->'
assert_contains templates/root-AGENTS.md '| Verified code integration has an observed memory conflict | Post-Merge Memory Reconciliation | `references/memory-reconciliation.md` |'
assert_contains templates/root-AGENTS.md '| Broad memory damage, stale/incomplete memory without a stable verified post-merge conflict boundary, outside-loop work, or unresolved reconciliation recovery | Recovery / Re-Adopt | `references/recovery-and-backfill.md` |'
assert_not_contains templates/root-AGENTS.md '| Memory conflicts or outside-loop work | Recovery / Re-Adopt |'
assert_not_contains templates/root-AGENTS.md '| Stale, incomplete, or outside-loop memory; unresolved reconciliation recovery | Recovery / Re-Adopt |'
assert_contains templates/root-AGENTS.md 'No observed memory conflict means `reconciliation-not-needed`'
assert_contains templates/root-AGENTS.md 'outside a reversible fact-determined Post-Merge Memory Reconciliation rewrite'
assert_contains SKILL.md 'outside a reversible fact-determined Post-Merge Memory Reconciliation rewrite'
assert_contains references/runtime.md 'outside a reversible fact-determined Post-Merge Memory Reconciliation rewrite'
assert_contains templates/root-AGENTS.md 'Git And Lifecycle Gate'
assert_contains templates/root-AGENTS.md 'Full Memory Audit / Recovery Apply/Restore'
assert_contains scripts/apply-memory-reconciliation.py '--mode'
assert_contains scripts/scan-memory-reconciliation.py '--full-audit-authorized'
assert_contains scripts/scan-memory-reconciliation.py 'Full Memory Audit / Recovery requires explicit authorization'
assert_contains references/memory-reconciliation.md 'Memory Reconciliation scripts never execute commands or hooks stored in a report or memory artifact.'
assert_contains references/memory-reconciliation.md 'The Python scanner also requires `--full-audit-authorized`'
assert_contains references/memory-reconciliation.md 'These controls belong to Recovery.'
assert_contains references/memory-reconciliation.md 'compute the exact intended postimage bytes before mutation'
assert_contains references/memory-reconciliation.md 'write through a same-directory temporary file and atomically replace the owner file'
assert_contains references/memory-reconciliation.md 'keep a bounded backup of only the changed preimages until targeted verification passes'
assert_contains references/memory-reconciliation.md 'verify the changed files match the intended postimages byte-for-byte'
assert_contains references/runtime.md 'exact preimages and intended postimages'
assert_contains templates/memory-merge-report.md 'Exact preimage'
assert_contains templates/memory-merge-report.md 'Intended postimage'
assert_contains templates/memory-merge-report.md 'Rollback scope / backup evidence'
assert_contains templates/memory-merge-report.md 'Remaining risk'

for scenario in \
  'Source-only Requirement/Feature' \
  'Target-only Work' \
  'Same Feature Compatible Append-only Changes' \
  'Both Memories Wrong' \
  'Code Versus Requirement' \
  'Code Versus Accepted ADR' \
  'Project Skill Manifest Conflict' \
  'Semantic Error Without Git Conflict' \
  'Source Branch Deleted' \
  'Dirty Result Memory' \
  'Stale Plan Hash' \
  'Apply Interruption/Restore Success' \
  'Restore Failure' \
  'Completed Replay' \
  'Zero-change Integration' \
  'Push Before Memory Completion' \
  'Customer Boundary Conflict' \
  'Source Future Directory' \
  'Unclassified Directory' \
  'Target Not Main' \
  'Legacy Memory Root' \
  'Case/Unicode/Symlink Path Pressure' \
  'Duplicate Report For One Merged SHA' \
  'Action Label Does Not Match Mutation' \
  'Blank Merge Context' \
  'Restore Crashes After Bytes Are Restored' \
  'Git Tree Or Symlink Presented As Blob'; do
  assert_contains references/validation-scenarios.md "$scenario"
done

for command in \
  scripts/scan-memory-reconciliation.py \
  scripts/check-memory-reconciliation.py \
  scripts/apply-memory-reconciliation.py \
  scripts/restore-memory-reconciliation.py; do
  assert_contains "$command" 'require_supported_python'
done

for forbidden in \
  'Memory Reconciliation automatically merges code' \
  'Target memory always wins' \
  'unknown directories are ignored' \
  'Apply may run again after completion' \
  'Memory merge authorizes push' \
  'every path in every snapshot must be classified'; do
  assert_not_contains references/memory-reconciliation.md "$forbidden"
done

for file in SKILL.md references/design.md references/runtime.md \
  references/submit-and-integrate.md templates/root-AGENTS.md README.md Usage.md; do
  assert_not_contains "$file" 'all-path Path Accounting Ledger'
  assert_not_contains "$file" 'derive one Desired Target Memory Snapshot'
done

python3 - "$root/references/runtime.md" <<'PY'
from pathlib import Path
import sys
text = Path(sys.argv[1]).read_text(encoding='utf-8')
tokens = [
    'Code Merge Gate',
    'Post-Merge Memory Reconciliation',
    'Memory Commit Gate',
    'Push Gate',
    'Release Gate',
    'Source Branch Cleanup Gate',
]
positions = [text.find(token) for token in tokens]
if any(position < 0 for position in positions):
    raise SystemExit('FAIL: runtime memory/Git gate order is incomplete')
if positions != sorted(positions):
    raise SystemExit('FAIL: runtime memory/Git gate order is incorrect')
PY

printf 'PASS: Post-Merge Memory Reconciliation contract is complete\n'

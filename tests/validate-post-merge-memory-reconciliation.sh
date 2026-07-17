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
  references/memory-reconciliation.md \
  templates/memory-merge-report.md \
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
  'Target Canonical Memory Spine' \
  'Desired Target Memory Snapshot' \
  'Path Accounting Ledger' \
  'human-source | accepted-authority | append-only-evidence | current-semantic-state | derived-index | validated-package | transaction-temporary | unclassified' \
  '保留 | 引入 | 重写 | 重算 | 移除过时声明 | 暂不处理' \
  '待确认 | 已完成 | 已恢复' \
  'one Merged Code SHA' \
  'one successful Apply' \
  'Memory Reconciliation does not perform the code merge.'; do
  assert_contains references/memory-reconciliation.md "$text"
done

assert_contains references/runtime.md 'Code Merge Gate -> Post-Merge Memory Reconciliation -> Memory Commit Gate'
assert_contains references/submit-and-integrate.md 'Memory Reconciliation must complete before push, release, publish, or Source branch cleanup.'
assert_contains references/artifact-rules.md '.agent-loop/memory-merges/MM-<merged-code-short-sha>/README.md'
assert_contains templates/memory-merge-report.md '<!-- memory-reconciliation-plan:start -->'
assert_contains templates/memory-merge-report.md '<!-- memory-reconciliation-plan:end -->'
assert_contains templates/root-AGENTS.md 'After code integration, reconcile changed Agent Loop memory before push, release, or source-branch cleanup.'
assert_contains scripts/apply-memory-reconciliation.py '--mode'
assert_contains references/memory-reconciliation.md 'Memory Reconciliation scripts never execute commands or hooks stored in a report or memory artifact.'
assert_contains references/memory-reconciliation.md 'a second report directory for the same full SHA fails closed before Apply'
assert_contains references/memory-reconciliation.md 'same-path `100644 | 100755` Git blob byte-for-byte'
assert_contains references/memory-reconciliation.md 'idempotently finishes only those remaining steps'
assert_contains references/memory-reconciliation.md 'Native Windows cannot represent that executable-bit distinction'
assert_contains references/memory-reconciliation.md 'CLI JSON, PASS, and error output is UTF-8'

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
  'Memory merge authorizes push'; do
  assert_not_contains references/memory-reconciliation.md "$forbidden"
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

#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
proposal="$root/docs/proposal/v1.3.x/feature-monthly-compaction.md"
plan="$root/docs/proposal/v1.3.x/feature-monthly-archive-implementation-plan.md"

assert_contains() {
  local text=$1
  if ! grep -Fq -- "$text" "$proposal"; then
    printf 'FAIL: feature monthly archive proposal missing required text: %s\n' "$text" >&2
    exit 1
  fi
}

assert_not_contains() {
  local text=$1
  if grep -Fq -- "$text" "$proposal"; then
    printf 'FAIL: feature monthly archive proposal contains removed design: %s\n' "$text" >&2
    exit 1
  fi
}

assert_plan_contains() {
  local text=$1
  if ! grep -Fq -- "$text" "$plan"; then
    printf 'FAIL: feature monthly archive implementation plan missing required text: %s\n' "$text" >&2
    exit 1
  fi
}

if [ ! -f "$proposal" ]; then
  printf 'FAIL: missing feature monthly archive proposal: %s\n' "$proposal" >&2
  exit 1
fi

if [ ! -f "$plan" ]; then
  printf 'FAIL: missing feature monthly archive implementation plan: %s\n' "$plan" >&2
  exit 1
fi

assert_contains "# Proposal: Feature Monthly Archive"
assert_contains "状态：已实现；待最终 Human Review"
assert_contains "Human Review：2026-07-14"
assert_contains "docs/proposal/v1.3.x/feature-monthly-archive-implementation-plan.md"
assert_contains "目标版本：v1.3.0 候选"
assert_contains "整目录按月归档"
assert_contains ".agent-loop/features/archive.md"
assert_contains ".agent-loop/features/2026-05/2026-05-08-login/"
assert_contains "Feature ID 是稳定身份"
assert_contains "Archive State"
assert_contains "archived | rehydrated"
assert_contains "它不是 feature lifecycle status"
assert_contains '归档资格只接受 `closed`'
assert_contains '- 不生成每个 feature 的新 `archive.md`；'
assert_contains '- 不创建 `historical/`；'
assert_contains '- 不创建 `features/YYYY-MM/INDEX.md`；'

assert_contains "Feature Monthly Archive Scan"
assert_contains "Scan 是只读操作"
assert_contains "Candidate Matrix"
assert_contains "Reference Impact List"
assert_contains "Eligibility And Safety Gate"
assert_contains "Batch Human Gate"
assert_contains "stale-plan"
assert_contains "Post-check"
assert_contains "失败恢复"
assert_contains "Rehydrate / Reopen"

assert_contains "Feature Follow-up / Flow-back"
assert_contains "ADR / Decision"
assert_contains "Requirement Mapping"
assert_contains "Project Memory"
assert_contains "Internal And External Links"
assert_contains "Feature Path Resolver"
assert_contains '`features/archive.md` 预期变化'
assert_contains '.agent-loop/features/.archive-txn/<transaction-id>/'
assert_contains "transaction journal"

assert_contains "scripts/scan-feature-monthly-archive.py"
assert_contains "scripts/apply-feature-monthly-archive.py"
assert_contains "scripts/check-feature-monthly-archive.py"
assert_contains "scripts/restore-feature-monthly-archive.py"
assert_contains "Python 3.10+ 标准库"
assert_contains "Windows 与 macOS"
assert_contains "Windows-test-defined"
assert_contains "Proposal Boundary"
assert_contains "本文件仍是 proposal，不是发布运行时权威"

assert_not_contains "Slim With History"
assert_not_contains "Deep Archive / Summary Only"
assert_not_contains '每个 feature 的新 `archive.md` 应'
assert_not_contains '删除、打包或外移 `historical/`'

assert_plan_contains "## Stage Helper Resolution"
assert_plan_contains "## Interface Contracts"
assert_plan_contains "## Task 0: Establish Baseline And Phase-0 Evidence"
assert_plan_contains "## Task 7: Full Validation, Review, And Development-Agent Handoff"
assert_plan_contains "Reader Compatibility"
assert_plan_contains "Archive Readiness"
assert_plan_contains "expected-plan-sha256"
assert_plan_contains "transaction journal"
assert_plan_contains "immutable-requirement-source"
assert_plan_contains "## Plan Self-Review"

printf 'PASS: feature monthly archive proposal contract is complete\n'

#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
proposal="$root/docs/proposal/v1.3.x/feature-monthly-compaction.md"

assert_contains() {
  local text=$1
  if ! grep -Fq -- "$text" "$proposal"; then
    printf 'FAIL: feature monthly compaction proposal missing required text: %s\n' "$text" >&2
    exit 1
  fi
}

assert_file_exists() {
  if [ ! -f "$proposal" ]; then
    printf 'FAIL: missing feature monthly compaction proposal: %s\n' "$proposal" >&2
    exit 1
  fi
}

assert_file_exists

assert_contains "状态：讨论草案"
assert_contains "目标版本：v1.2.4 候选"
assert_contains "当前月保持 flat"
assert_contains "上个月且整月全部完成后，才允许月度压缩"
assert_contains "Full"
assert_contains "Slim With History"
assert_contains "Deep Archive / Summary Only"
assert_contains "Deep Archive 永远不是默认动作"

assert_contains ".agent-loop/features/YYYY-MM-DD-<feature-slug>/"
assert_contains ".agent-loop/features/YYYY-MM/"
assert_contains "archive.md"
assert_contains "historical/"
assert_contains "README.md"

assert_contains "Feature Compaction Scan"
assert_contains "Candidate Matrix"
assert_contains "Safety Gate"
assert_contains "Human Gate"
assert_contains "Partial month compaction"

assert_contains "## 影响的索引关系"
assert_contains "features/INDEX.md"
assert_contains "features/YYYY-MM/INDEX.md"
assert_contains "requirement set README"
assert_contains "requirements/INDEX.md"
assert_contains "Delivery Phases"
assert_contains "Feature Mapping"
assert_contains "decisions/*.md"
assert_contains "Implemented By"
assert_contains "project.md"
assert_contains "Active Feature"
assert_contains "Paused Features"
assert_contains "Feature Follow-up / Flow-back"
assert_contains "Source Requirements"
assert_contains "Applicable Decisions"
assert_contains "Implements Decisions"
assert_contains "verification evidence"
assert_contains "Drift Check"
assert_contains "scripts / validation glob"

assert_contains "Requirements 不做内容压缩"
assert_contains "需求源材料保持原样"
assert_contains "只把 feature 压缩作为第一版默认能力"

assert_contains "## Archive Summary Template"
assert_contains "Delivered Behavior"
assert_contains "Key Design Decisions"
assert_contains "Changed Files / Public Interfaces"
assert_contains "Historical Detail Location"

printf 'PASS: feature monthly compaction proposal contract is complete\n'

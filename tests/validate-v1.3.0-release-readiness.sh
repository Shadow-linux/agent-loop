#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
release_status='状态：v1.3.0 Release Human Gate 已批准；发布目标 stable-v1.3.0'
ci_url='https://github.com/Shadow-linux/agent-loop/actions/runs/29320389912'

assert_contains() {
  local file=$1
  local text=$2
  if ! grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s missing release evidence: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

for proposal in \
  docs/proposal/v1.3.x/onboarding-core-flow-completeness.md \
  docs/proposal/v1.3.x/concept-foundation-requirement-modeling.md \
  docs/proposal/v1.3.x/adr-requirement-model-technical-landing-trace.md \
  docs/proposal/v1.3.x/cross-platform-python-script-runtime.md \
  docs/proposal/v1.3.x/feature-monthly-compaction.md
do
  assert_contains "$proposal" "$release_status"
done

assert_contains "docs/proposal/v1.3.x/cross-platform-python-script-runtime.md" '平台证据：`macOS-verified / Windows-verified`'
assert_contains "docs/proposal/v1.3.x/cross-platform-python-script-runtime.md" "$ci_url"
assert_contains "docs/proposal/v1.3.x/feature-monthly-compaction.md" '平台证据：`macOS-verified / Windows-verified`'
assert_contains "docs/proposal/v1.3.x/feature-monthly-compaction.md" "$ci_url"

plan="docs/proposal/v1.3.x/feature-monthly-archive-implementation-plan.md"
assert_contains "$plan" "Implementation: Task 0-7 completed and pre-release full validation passed"
assert_contains "$plan" "Platform: macOS-verified / Windows-verified"
assert_contains "$plan" "Release: Human Gate approved on 2026-07-14; target tag stable-v1.3.0"
assert_contains "$plan" "Tag condition: the exact release-evidence commit must pass the Windows/macOS CI matrix before tag creation"

focused="docs/reports/agent-loop-v1.3.0-feature-monthly-archive-validation-2026-07-14.md"
assert_contains "$focused" '平台结论：`macOS-verified / Windows-verified`'
assert_contains "$focused" "$ci_url"

full="docs/reports/agent-loop-v1.3.0-full-validation-2026-07-14.md"
assert_contains "$full" "审计对象：v1.3.0 release candidate，行为基线 commit \`7253461\`"
assert_contains "$full" '平台状态：`macOS-verified / Windows-verified`'
assert_contains "$full" '最终测试：**98/98 Python tests PASS；34/34 `tests/*.sh` PASS**'
assert_contains "$full" '当前严重度：**Critical 0 / High 0 / Medium 0 / Low 0**'
assert_contains "$full" "$ci_url"
assert_contains "$full" "Release Human Gate：**已批准**"
assert_contains "$full" '授权动作：提交并推送 release-evidence commit、推进两个 `v1.3.0` branch、创建并推送 `stable-v1.3.0` tag'
assert_contains "$full" "精确 release-evidence commit 的 Windows/macOS CI 全部成功后"

printf 'PASS: v1.3.0 release evidence is current and internally consistent\n'

#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
guide="docs/maintenance/full-validation-method.md"

assert_contains() {
  local file=$1
  local text=$2
  if ! grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s missing required text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

if [[ ! -f "$root/$guide" ]]; then
  printf 'FAIL: missing maintainer validation guide: %s\n' "$guide" >&2
  exit 1
fi

# AGENTS.md is the development-agent entrypoint; runtime references stay user-facing.
assert_contains "AGENTS.md" '`docs/maintenance/full-validation-method.md`'
assert_contains "AGENTS.md" "canonical stage order"
assert_contains "AGENTS.md" "full validation"
assert_contains "AGENTS.md" 'Do not put repository-maintenance validation rules in `references/`'
assert_contains "AGENTS.md" "## Repository Perspective"
assert_contains "AGENTS.md" "You are maintaining the Agent Loop skill source repository"
assert_contains "AGENTS.md" '`AGENTS.md` and `docs/maintenance/`'
assert_contains "AGENTS.md" '`SKILL.md` and `references/`'
assert_contains "AGENTS.md" '`templates/root-AGENTS.md`'
assert_contains "AGENTS.md" "Before deciding where a rule belongs, classify its audience"

# The guide must preserve the semantic audit contract, not only command checks.
assert_contains "$guide" "## 触发条件"
assert_contains "$guide" "## 六个审计域"
assert_contains "$guide" "Logic Correctness"
assert_contains "$guide" "Autonomy"
assert_contains "$guide" "Project Entry / Evidence Graph + DDD Onboarding"
assert_contains "$guide" "Development / Test Workflow"
assert_contains "$guide" "Memory"
assert_contains "$guide" "Recommendation"
assert_contains "$guide" "## RED：记录修复前基线"
assert_contains "$guide" "## GREEN：修复后重新验证"
assert_contains "$guide" "机械检查通过不等于逻辑验证通过"
assert_contains "$guide" "docs/reports/"
assert_contains "$guide" "报告正文使用中文"

printf 'PASS: maintainer full-validation guidance is durable and correctly scoped\n'

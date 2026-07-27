#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

assert_contains() {
  local file="$1"
  local expected="$2"
  if ! grep -Fq "$expected" "$ROOT/$file"; then
    printf "FAIL: %s missing required text: %s\n" "$file" "$expected" >&2
    exit 1
  fi
}

assert_contains "SKILL.md" "Human Help And Version Questions"
assert_contains "SKILL.md" "When the human asks what changed in a version"
assert_contains "SKILL.md" "use \`CHANGELOG.md\` as the source of truth for version changes"
assert_contains "SKILL.md" "use \`Usage.md\` as the source of truth for human-facing usage examples and trigger phrases"
assert_contains "SKILL.md" "use \`README.md\` for high-level overview, install, and quick-start explanation"
assert_contains "SKILL.md" "read that version section first"

assert_contains "Usage.md" "### 我想知道版本更新或用法"
assert_contains "Usage.md" "1.5.2 更新了什么？"
assert_contains "Usage.md" "当前 1.5.2 使用的是"
assert_contains "Usage.md" "和 1.2.2 比有什么变化？"
assert_contains "Usage.md" "现在 agent-loop 怎么用？"
assert_contains "Usage.md" "CHANGELOG.md"
assert_contains "Usage.md" "Usage.md"

assert_contains "CHANGELOG.md" "Human Help / Version Questions"
assert_contains "CHANGELOG.md" "CHANGELOG.md is the source of truth for version-change answers"

printf "PASS: human help and version docs routing contract is complete\n"

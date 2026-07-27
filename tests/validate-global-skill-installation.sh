#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

assert_contains() {
  local file=$1
  local text=$2
  if ! grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s missing global installation contract: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_not_contains() {
  local file=$1
  local text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s contains forbidden global installation claim: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_contains "README.md" "npx -y skills add Shadow-linux/agent-loop"
assert_contains "README.md" "--skill agent-loop"
assert_contains "README.md" "--agent codex"
assert_contains "README.md" "--agent kimi-code-cli"
assert_contains "README.md" "--agent claude-code"
assert_contains "README.md" "--agent opencode"
assert_contains "README.md" "--yes"
assert_contains "README.md" "npx skills add Shadow-linux/agent-loop -g"
assert_contains "README.md" "npx skills update agent-loop -g"
assert_contains "README.md" "npx skills list -g"
assert_contains "README.md" "Public GitHub"
assert_contains "README.md" "Compatible Git clone"
assert_contains "README.md" "latest formal stable release channel"
assert_contains "README.md" "Alpha branches"
assert_contains "README.md" "https://github.com/Shadow-linux/agent-loop.git"
assert_contains "README.md" "<git-mirror-url>"
assert_not_contains "README.md" "git@"
assert_contains "README.md" "rsync -ac --delete"
assert_contains "README.md" "robocopy"
assert_contains "README.md" "Agent Loop 版本已更新，请更新项目的 AGENTS.md。"

assert_contains "Usage.md" "npx skills update agent-loop -g"
assert_contains "Usage.md" "外部环境：GitHub"
assert_contains "Usage.md" "兼容安装：Git clone"
assert_contains "Usage.md" "<git-mirror-url>"
assert_not_contains "Usage.md" "git@"
assert_contains "Usage.md" "rsync -ac --delete"
assert_contains "Usage.md" "robocopy"
assert_contains "Usage.md" "Agent Loop 版本已更新，请更新项目的 AGENTS.md。"
assert_contains "Usage.md" "不会自动修改已有项目的 \`AGENTS.md\`"
assert_contains "Usage.md" '安装与升级读取 `main`'
assert_contains "Usage.md" "最新稳定版本保持同一提交"

assert_contains "AGENTS.md" '`main` is the default public installation channel'
assert_contains "AGENTS.md" "exact commit of the latest formal stable release"
assert_contains "AGENTS.md" "alpha branches never become the default installation source"
assert_contains "AGENTS.md" "separate branch/merge/push Human Gate"

assert_contains "SKILL.md" "automatic or unscoped global skill installation"
assert_contains "references/design.md" "automatic or unscoped global skill installation"
assert_contains "references/concepts.md" "automatic or unscoped global installation"
assert_contains "references/validation-scenarios.md" "automatic or unscoped global install"
assert_not_contains "SKILL.md" "Agent Loop automatically installs"
assert_not_contains "references/concepts.md" "- global installation"

assert_contains "CHANGELOG.md" "Codex、Kimi Code CLI、Claude Code 和 OpenCode"
assert_contains "CHANGELOG.md" "npx skills"
assert_contains "CHANGELOG.md" '`main` as the default public installation channel'

printf 'PASS: public npx and compatible Git clone installation, update, verification, and project-guidance reminder contract is complete\n'

#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

assert_contains() {
  local file=$1
  local text=$2
  if ! grep -Fq -- "$text" "$root/$file"; then
    fail "$file missing required text: $text"
  fi
}

assert_not_contains() {
  local file=$1
  local text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    fail "$file contains forbidden detail: $text"
  fi
}

assert_contains SKILL.md 'Project Skill Discovery Guard'
assert_contains references/runtime.md '## Project Skill Discovery Guard'
assert_contains references/design.md '## Project Skill Discovery Guard'
assert_contains references/project-skills.md '## Discovery Guard And Fallback Precedence'
assert_contains references/stage-guides.md 'Run Project Skill Discovery Guard before any stage-specific helper, generic fallback, command, tool call, temporary resource, or environment action.'
assert_contains references/workflow-checklists.md '## Project Skill Discovery Guard'
assert_contains references/project-guidance.md 'Before claiming no relevant project skill or entering a generic execution fallback'
assert_contains README.md 'runtime/global Skill inventory does not replace `.agent-loop/skills/INDEX.md`'
assert_contains Usage.md '项目 Skill 不一定显示在运行时原生 Skill 列表中'
assert_contains CHANGELOG.md '### Project Skill Discovery Guard'

for scenario in \
  'Active On-Demand Match Before Operational Fallback' \
  'Runtime Inventory Is Not Project Skill Inventory' \
  'Index Absent Allows Generic Method' \
  'No Active Match Avoids Full Body Scan' \
  'Inactive Skill Cannot Route' \
  'Manifest Drift Blocks Equivalent Fallback' \
  'Execution Gate Still Blocks Side Effects' \
  'Context Re-entry Rechecks Discovery' \
  'Same-Name Ownership Is Explicit' \
  'Chat Remains Lightweight'
do
  assert_contains references/validation-scenarios.md "### $scenario"
done

ruby - "$root/references/runtime.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
section = content[/^## Project Skill Discovery Guard\n(.*?)(?=^## |\z)/m, 1]
abort 'FAIL: runtime Project Skill Discovery Guard section missing' unless section
tokens = [
  'latest actionable intent / current stage',
  'inspect Project Skill INDEX metadata',
  'match active bootstrap / on-demand candidates',
  'verify exact INDEX row, path, and manifest',
  'read-only load the matched Project Skill',
  'Execution Gate',
  'stage action'
]
positions = tokens.map { |token| section.index(token) }
abort 'FAIL: runtime canonical discovery sequence is incomplete' if positions.any?(&:nil?)
abort 'FAIL: runtime canonical discovery sequence is reordered' unless positions == positions.sort
abort 'FAIL: fallback permission is missing' unless section.include?('Only `index-absent` or `no-active-match` permits generic fallback.')
abort 'FAIL: project-skill-drift must fail closed' unless section.include?('`project-skill-drift` fails closed')
RUBY

ruby - "$root/references/design.md" "$root/references/project-skills.md" <<'RUBY'
design = File.read(ARGV.fetch(0))
detail = File.read(ARGV.fetch(1))
required = [
  'runtime/global Skill inventory does not prove that no Project Skill exists',
  'Only `index-absent` or `no-active-match` permits generic fallback.',
  '`project-skill-drift` fails closed'
]
required.each do |text|
  abort "FAIL: design/reference contract missing: #{text}" unless design.include?(text) && detail.include?(text)
end
RUBY

reminder='7. Check Project Skill metadata before generic executable fallback; verify and load only a matched active skill, while preserving its per-invocation Execution Gate because loading never authorizes execution.'
count=$(grep -Fo -- "$reminder" "$root/templates/root-AGENTS.md" | wc -l | tr -d ' ')
[ "$count" -eq 1 ] || fail "root AGENTS must contain the concise discovery reminder exactly once; found $count"
assert_contains templates/root-AGENTS.md '| Create or manage a reusable project workflow | Project Skill Creation / Update | `references/project-skills.md`, `references/skill-routing.md`, `references/external-skill-adapters.md` |'

for forbidden in matched-active index-absent no-active-match project-skill-drift; do
  assert_not_contains templates/root-AGENTS.md "$forbidden"
done

ruby - "$root/templates/root-AGENTS.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
blocks = content.scan(/<!-- agent-loop:managed-start section:([^ ]+) .*?block-version:([^ ]+) -->/)
abort 'FAIL: root managed blocks missing' if blocks.empty?
abort "FAIL: expected 13 managed blocks, found #{blocks.length}" unless blocks.length == 13
blocks.each do |section, revision|
  expected = '1.5.0-20260723.2'
  abort "FAIL: #{section} expected #{expected}, found #{revision}" unless revision == expected
end
RUBY

if [ -e "$root/.agent-loop/skills" ]; then
  fail 'source repository must not contain downstream .agent-loop/skills artifacts'
fi

printf 'PASS: Project Skill Discovery Guard ordering, fallback, drift, root, and gate contract is complete\n'

#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

assert_file() {
  [ -f "$root/$1" ] || fail "missing required file: $1"
}

assert_contains() {
  local file=$1
  local text=$2
  grep -Fq -- "$text" "$root/$file" || fail "$file missing Lightweight Change contract: $text"
}

assert_not_contains() {
  local file=$1
  local text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    fail "$file contains forbidden Lightweight Change behavior: $text"
  fi
}

assert_not_line() {
  local file=$1
  local text=$2
  if grep -Fxq -- "$text" "$root/$file"; then
    fail "$file contains forbidden Lightweight Change line: $text"
  fi
}

assert_file references/lightweight-change-lane.md
assert_file templates/lightweight-execution-card.md

for file in \
  SKILL.md \
  references/runtime.md \
  references/design.md \
  references/concepts.md \
  references/stage-guides.md \
  references/workflow-checklists.md; do
  assert_contains "$file" 'Lightweight Change Lane'
done

for text in \
  'Explicit Bug Management wins before this assessment.' \
  'The card is response-local by default.' \
  'Project Entry classification is required; creating or repairing long-term Agent Loop memory is not required solely to run this lane.' \
  'A Plan is always required, but its depth is adaptive.' \
  'Do not create `.agent-loop/changes/`, `.agent-loop/quick-fixes/`, or another lightweight backlog.' \
  'Scope expansion stops the lane before broader edits.' \
  'Card completion authorizes no Git, release, publish, production, or Bug lifecycle action.'; do
  assert_contains references/lightweight-change-lane.md "$text"
done

for text in \
  'Background:' \
  'Goal / Completion Criteria:' \
  'Scope:' \
  'Lane Rationale:' \
  'Impact / Risk:' \
  'Plan:' \
  'Current Progress:' \
  'Verification:' \
  'Rollback:' \
  'Human Gates:' \
  'Result / Residuals:' \
  'Response-local by default.' \
  'Do not copy this template into a target project by default.'; do
  assert_contains templates/lightweight-execution-card.md "$text"
done

ruby - "$root/references/runtime.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
tokens = [
  'explicit Bug management intent',
  'Human-Guided Bug Management',
  'actionable non-Bug change',
  'Lightweight Change Assessment',
  'clearly eligible',
  'Feature trigger',
  'uncertain',
  'Human Choice with Agent Recommendation'
]
sequence = content.scan(/```text\n(.*?)```/m).flatten.find { |block| tokens.all? { |token| block.include?(token) } }
abort 'FAIL: runtime missing canonical Lightweight Change routing sequence' unless sequence
positions = tokens.map { |token| sequence.index(token) }
abort 'FAIL: runtime reorders Lightweight Change routing sequence' unless positions == positions.sort

intent = content[/^## Message Intent Classification\n(.*?)(?=^## |\z)/m, 1]
abort 'FAIL: runtime Message Intent Classification missing' unless intent
abort 'FAIL: lightweight-change must not become a message intent' if intent.include?('`lightweight-change`')

stage_order = content[/^## Stage Order\n(.*?)(?=^## |\z)/m, 1]
abort 'FAIL: runtime Stage Order missing' unless stage_order
canonical_lines = stage_order.lines.map(&:strip)
abort 'FAIL: Lightweight Change Lane became a canonical stage' if canonical_lines.include?('Lightweight Change Lane')
abort 'FAIL: Lightweight Change Assessment became a canonical stage' if canonical_lines.include?('Lightweight Change Assessment')
RUBY

ruby - "$root/references/bug-management.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
allowed = 'investigate-first | flow-back | linked-feature | maintenance-fix | requirement | no-fix'
abort 'FAIL: existing Bug Resolution Path contract changed' unless content.include?(allowed)
abort 'FAIL: Lightweight Change became a Bug Resolution Path' if content.match?(/investigate-first \|[^\n]*lightweight/i)
abort 'FAIL: explicit Bug intent precedence is missing' unless content.include?('Explicit Bug management intent takes precedence over Lightweight Change Assessment.')
RUBY

assert_contains references/stage-guides.md 'A concrete bounded change request authorizes only the local scope disclosed in the card; it adds no separate Lightweight Mode gate.'
assert_contains references/stage-guides.md 'If code or configuration changes are required, run Lightweight Change Assessment before defaulting to Feature construction, unless explicit Bug intent or a Feature hard trigger already decides the route.'
assert_contains references/feature-follow-up.md 'Generic “small tweak” wording does not by itself enter Bug Management or Feature Follow-up.'
assert_not_contains references/design.md 'Human reports bug, regression, post-close correction, field/schema/algorithm/API change, test failure, screenshot issue, QA/user feedback, or small tweak'
assert_contains references/design.md 'Generic adjustment wording alone does not enter Feature Follow-up; route an actionable ordinary non-Bug change through Lightweight Change Assessment first.'
assert_contains references/design.md 'For explicit Bug management, create/update/reopen the Bug Record, verify Expected Behavior, and recommend exactly one Resolution Path.'
assert_not_line references/design.md 'Create/update/reopen the Bug Record, verify Expected Behavior, and recommend exactly one Resolution Path.'
assert_not_contains references/concepts.md 'behavior tweak, "small tweak", test failure, or QA/user feedback belongs to an existing Feature'
assert_contains references/concepts.md 'Generic adjustment wording alone routes an actionable ordinary non-Bug change through Lightweight Change Assessment before ownership scanning.'
assert_not_contains references/workflow-checklists.md 'behavior tweak, "small tweak", test failure, or QA/user feedback.'
assert_contains references/workflow-checklists.md 'Treat generic adjustment wording as assessment input only; require explicit Bug/defect evidence, changed accepted behavior, or clear Feature ownership before entering Feature Follow-up.'
assert_contains references/project-guidance.md 'but only after Project Entry has established or verified agent-loop memory; generic “small tweak” wording alone uses Lightweight Change Assessment first'
assert_contains references/implementation-planning.md 'A Lightweight Execution Card is not a Feature `plan.md` and does not enter Plan Gate.'
assert_contains references/skill-routing.md 'Lightweight Change Lane does not enter mandatory Plan Gate / Plan or Execute Task / Story helper resolution.'
assert_contains references/external-skill-adapters.md 'Do not expand a Lightweight Execution Card into `docs/superpowers/`, a Feature workspace, or a construction-grade plan.'
assert_contains references/artifact-rules.md 'Lightweight Execution Card | response-local execution control'
assert_contains references/project-memory-mode.md 'Do not store Lightweight Execution Card history or a lightweight backlog in `project.md`.'
assert_contains references/branch-management.md 'A Lightweight Execution Card authorizes no branch action.'
assert_contains references/submit-and-integrate.md 'A completed Lightweight Execution Card authorizes no submit or integration action.'

reminder='Before creating a Feature for a bounded non-Bug change, let Agent Loop assess the Lightweight Change Lane; if impact is unclear, stop and ask the human with a recommendation.'
count=$(grep -Fo -- "$reminder" "$root/templates/root-AGENTS.md" | wc -l | tr -d ' ')
[ "$count" -eq 1 ] || fail "root AGENTS must contain the concise Lightweight Change reminder exactly once; found $count"
assert_contains templates/root-AGENTS.md '| Ordinary non-Bug change appears bounded, reversible, and exactly verifiable | Lightweight Change Assessment (internal route) | `references/lightweight-change-lane.md` |'
assert_not_contains templates/root-AGENTS.md 'Lane Rationale:'
assert_not_contains templates/root-AGENTS.md 'Result / Residuals:'
assert_not_contains templates/root-AGENTS.md 'Feature Hard Triggers'

for scenario in \
  'Confirmed Internal Domain Replacement Uses Lightweight Card' \
  'Production Domain Migration Requires Feature' \
  'One-Line Public Contract Change Requires Feature' \
  'Multi-File Mechanical Synchronization May Stay Lightweight' \
  'Explicit Bug Intent Wins Before Lightweight Assessment' \
  'Generic Fix Wording Does Not Automatically Create Bug' \
  'Uncertain Impact Stops For Human Choice' \
  'Response-Local Card Always Contains Background And Plan' \
  'Fact Change Uses Targeted Verification Without Invented Unit Test' \
  'Small Isolated Logic Change Uses Minimal RED GREEN' \
  'Scope Expansion Stops Before Broader Edits' \
  'Active Feature Ownership Blocks Lane Escape' \
  'Durable Fact Synchronization Is Not A New Decision' \
  'Production And Git Gates Remain Separate' \
  'Repository Without Agent Loop Memory Uses Minimum Entry Check' \
  'Sealed Release Cannot Use Lightweight Lane'; do
  assert_contains references/validation-scenarios.md "### $scenario"
done

assert_contains SKILL.md 'Version: 1.5.0'
assert_contains plugin.json '"version": "1.5.0"'
assert_contains README.md '**Current version:** 1.5.0'
assert_contains Usage.md '**版本：** 1.5.0'
assert_contains CHANGELOG.md '## 1.5.0 — 2026-07-17'

ruby - "$root/templates/root-AGENTS.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
blocks = content.scan(/<!-- agent-loop:managed-start section:([^ ]+) .*?block-version:([^ ]+) -->/)
abort 'FAIL: root AGENTS managed blocks missing' if blocks.empty?
abort "FAIL: expected 13 managed blocks, found #{blocks.length}" unless blocks.length == 13
blocks.each do |section, revision|
  expected = '1.5.0-20260717'
  abort "FAIL: #{section} expected #{expected}, found #{revision}" unless revision == expected
end
RUBY

[ ! -d "$root/.agent-loop" ] || fail 'source repository must not contain target-project .agent-loop artifacts'
[ ! -d "$root/templates/.agent-loop" ] || fail 'templates must not introduce a default target-project .agent-loop change tree'

printf 'PASS: Lightweight Change routing, card, Bug/Feature boundary, adaptive verification, root, version, and gate contract is complete\n'

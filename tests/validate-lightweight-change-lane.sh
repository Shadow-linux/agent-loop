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
  'The card file is the execution source of truth.' \
  '<memory-root>/changes/YYYY-MM/YYYY-MM-DD-<topic>.md' \
  'pending_count >= 3' \
  'as_of_date - oldest_completed_at > 7 days' \
  'exactly 7 days does not trigger' \
  'monthly partition is not archive' \
  'code merge completes before Target memory reconciliation' \
  'A Plan is always required, but its depth is adaptive.' \
  'Scope expansion stops the lane before broader edits.' \
  'Card completion authorizes no Git, release, publish, production, or Bug lifecycle action.'; do
  assert_contains references/lightweight-change-lane.md "$text"
done

for text in \
  'Record Version: 1' \
  'Status: in-progress' \
  'Created At:' \
  'Updated At:' \
  'Completed At: none' \
  'Git Context:' \
  '## Background' \
  '## Goal / Completion Criteria' \
  '## Scope' \
  '## Lane Rationale' \
  '## Impact / Risk' \
  '## Plan' \
  '## Current Progress' \
  '## Verification' \
  '## Rollback' \
  '## Human Gates' \
  '## Result / Residuals' \
  '## Memory' \
  'Memory Review: pending' \
  'Memory Result: pending' \
  'Memory Evidence: pending: verification not complete' \
  'Memory Target: pending: classify at completion'; do
  assert_contains templates/lightweight-execution-card.md "$text"
done

for stale in \
  'The card is response-local by default.' \
  'Do not create `.agent-loop/changes/`' \
  'no default `.agent-loop/changes/` directory' \
  'creates no persistent target-project artifact'; do
  for file in references/lightweight-change-lane.md references/runtime.md references/design.md references/artifact-rules.md templates/lightweight-execution-card.md; do
    assert_not_contains "$file" "$stale"
  done
done

assert_file scripts/lightweight_change_support.py
assert_file scripts/scan-lightweight-changes.py
assert_file tests/lightweight_change_test_support.py
assert_file tests/test_lightweight_change_scan.py

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
assert_contains references/project-guidance.md 'The Workflow Gateway Map contains one exact first-hop row for an already-defined actionable ordinary non-Bug change, pointing to `Lightweight Change Assessment` and `references/lightweight-change-lane.md`.'
assert_contains references/project-guidance.md 'Lightweight Change Gateway: route only already-defined actionable bounded non-Bug work to `references/lightweight-change-lane.md`; unresolved product meaning remains in Requirements Discussion'
assert_contains references/implementation-planning.md 'A Lightweight Execution Card is not a Feature `plan.md` and does not enter Plan Gate.'
assert_contains references/skill-routing.md 'Lightweight Change Lane does not enter mandatory Plan Gate / Plan or Execute Task / Story helper resolution.'
assert_contains references/external-skill-adapters.md 'Do not expand a Lightweight Execution Card into `docs/superpowers/`, a Feature workspace, or a construction-grade plan.'
assert_contains references/artifact-rules.md 'Memory Review: pending | complete'
assert_contains references/artifact-rules.md 'Memory Result: pending | none | synced | human-review'
assert_contains references/project-memory-mode.md 'A changes-only root does not prove that project memory is initialized or reliable.'
assert_contains references/branch-management.md 'A Lightweight Execution Card authorizes no branch action.'
assert_contains references/submit-and-integrate.md 'A completed Lightweight Execution Card authorizes no submit or integration action.'
assert_contains references/memory-reconciliation.md 'a targeted check of changed memory finds a broken direct reference caused by this merge'
assert_contains references/lightweight-change-lane.md 'Post-merge entry alone does not start consolidation or a full Change scan.'
assert_contains references/runtime.md 'scripts/scan-lightweight-changes.py'
assert_contains references/design.md 'The lane reduces ceremony and document depth, not accuracy, scope control, verification strength, rollback, fact review, or Human Gates.'

assert_contains templates/root-AGENTS.md '| Already-defined actionable ordinary non-Bug change that appears bounded, reversible, and exactly verifiable | Lightweight Change Assessment | `references/lightweight-change-lane.md` |'
assert_contains templates/root-AGENTS.md 'Scope And Risk Gate'
assert_not_contains templates/root-AGENTS.md '| Ordinary non-Bug change appears bounded, reversible, and exactly verifiable | Lightweight Change Assessment (internal route) |'
assert_not_contains templates/root-AGENTS.md 'Lane Rationale:'
assert_not_contains templates/root-AGENTS.md 'Result / Residuals:'
assert_not_contains templates/root-AGENTS.md 'Feature Hard Triggers'

for scenario in \
  'Confirmed Internal Domain Replacement Uses Lightweight Card' \
  'Unshaped Product Need Does Not Enter Lightweight' \
  'Production Domain Migration Requires Feature' \
  'One-Line Public Contract Change Requires Feature' \
  'Multi-File Mechanical Synchronization May Stay Lightweight' \
  'Explicit Bug Intent Wins Before Lightweight Assessment' \
  'Generic Fix Wording Does Not Automatically Create Bug' \
  'Uncertain Impact Stops For Human Choice' \
  'Fact Change Uses Targeted Verification Without Invented Unit Test' \
  'Small Isolated Logic Change Uses Minimal RED GREEN' \
  'Active Feature Ownership Blocks Lane Escape' \
  'Repository Without Agent Loop Memory Uses Minimum Entry Check' \
  'Sealed Release Cannot Use Lightweight Lane' \
  'Persistent Card Exists Before First Target Write' \
  'Monthly Partition Is Stable And Is Not Archive' \
  'Same-Day Topic Collision Uses A Non-Overwriting Suffix' \
  'Changes-Only Root Does Not Prove Initialization' \
  'Accepted Legacy Root Is Reused' \
  'Dual Memory Roots Stop In Recovery' \
  'Accidental Context Loss Revalidates Card And Diff' \
  'Planned Cross-Session Work Uses Feature' \
  'Two Pending Changes Do Not Trigger Count' \
  'Three Pending Changes Across Months Trigger Consolidation' \
  'Exactly Seven Days Does Not Trigger' \
  'Older Than Seven Days Triggers' \
  'Human Review Candidate Remains Visible' \
  'High-Evidence Sync Requires Existing Reliable Memory' \
  'Automatic Sync Discloses Exact Memory Scope' \
  'Scanner Does Not Perform Semantic Memory Writes' \
  'Sensitive Evidence Is Redacted' \
  'Source Change Does Not Override Target Before Code Merge' \
  'Post-Merge Reconciliation Rechecks Change Evidence' \
  'Scope Expansion Stops Persistent Card Execution' \
  'Git Production And Release Gates Remain Separate'; do
  assert_contains references/validation-scenarios.md "### $scenario"
done

assert_contains SKILL.md 'Version: 1.5.3'
assert_contains plugin.json '"version": "1.5.3"'
assert_contains README.md '**Current version:** 1.5.3'
assert_contains Usage.md '**版本：** 1.5.3'
assert_contains CHANGELOG.md '## 1.5.3 — 2026-07-28'
assert_contains CHANGELOG.md '## 1.5.0 — 2026-07-17'

ruby - "$root/templates/root-AGENTS.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
blocks = content.scan(/<!-- agent-loop:managed-start section:([^ ]+) .*?block-version:([^ ]+) -->/)
abort 'FAIL: root AGENTS managed blocks missing' if blocks.empty?
abort "FAIL: expected 13 managed blocks, found #{blocks.length}" unless blocks.length == 13
blocks.each do |section, revision|
  expected = '1.5.3-20260728.1'
  abort "FAIL: #{section} expected #{expected}, found #{revision}" unless revision == expected
end
RUBY

[ ! -d "$root/.agent-loop" ] || fail 'source repository must not contain target-project .agent-loop artifacts'
[ ! -d "$root/templates/.agent-loop" ] || fail 'templates must not introduce a default target-project .agent-loop change tree'

printf 'PASS: Lightweight Change routing, card, Bug/Feature boundary, adaptive verification, root, version, and gate contract is complete\n'

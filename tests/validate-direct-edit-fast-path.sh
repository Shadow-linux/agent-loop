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
  local file=$1 text=$2
  grep -Fq -- "$text" "$root/$file" || fail "$file missing Direct Edit/full-test contract: $text"
}

assert_not_contains() {
  local file=$1 text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    fail "$file contains forbidden Direct Edit/full-test behavior: $text"
  fi
}

for file in \
  references/direct-edit-fast-path.md \
  references/runtime.md \
  references/design.md \
  references/concepts.md \
  references/lightweight-change-lane.md \
  references/stage-guides.md \
  references/workflow-checklists.md \
  references/skill-routing.md \
  references/external-skill-adapters.md \
  references/implementation-planning.md \
  references/feature-follow-up.md \
  references/artifact-rules.md \
  references/project-memory-mode.md \
  references/project-guidance.md \
  references/human-review-summary.md \
  references/submit-and-integrate.md \
  references/checker-recovery.md \
  references/validation-scenarios.md \
  docs/maintenance/full-validation-method.md \
  templates/root-AGENTS.md \
  SKILL.md plugin.json README.md Usage.md CHANGELOG.md; do
  assert_file "$file"
done

# Direct Edit owns a narrow zero-artifact route before persistent Lightweight Change.
assert_contains SKILL.md 'Direct Edit Fast Path'
assert_contains references/runtime.md 'Direct Edit Fast Path'
assert_contains references/design.md '**Direct Edit Fast Path**'
assert_contains references/concepts.md '`Direct Edit Fast Path`'
assert_contains references/direct-edit-fast-path.md 'one final diff inspection plus the minimum matched check'
assert_contains references/direct-edit-fast-path.md 'creates no persistent Agent Loop artifact'
assert_contains references/direct-edit-fast-path.md 'business/runtime multiplier'
assert_contains references/direct-edit-fast-path.md 'Explicit Bug management intent takes precedence'
assert_contains references/direct-edit-fast-path.md 'No-Plan Decision'
assert_contains references/lightweight-change-lane.md 'Run Direct Edit Assessment before creating a persistent card.'
assert_contains references/artifact-rules.md 'Direct Edit creates no artifact'
assert_contains references/project-memory-mode.md 'Direct Edit does not write project memory'
assert_contains references/skill-routing.md 'Direct Edit does not invoke Plan or TDD helpers'
assert_contains references/external-skill-adapters.md 'Direct Edit Fast Path does not invoke an external helper'
assert_contains references/implementation-planning.md 'Direct Edit Fast Path never creates a Plan or No-Plan Decision'

# Same-scope tuning waits for one final Human-selected value.
assert_contains references/direct-edit-fast-path.md 'same accepted Feature boundary and same tuning question'
assert_contains references/direct-edit-fast-path.md 'no per-iteration test, card, Plan, notes, or formal verification'
assert_contains references/direct-edit-fast-path.md 'Human identifies the final acceptable value'
assert_contains references/stage-guides.md 'intermediate values receive no per-iteration test or formal check'
assert_contains references/stage-guides.md 'do not ask for a second route confirmation'
assert_contains templates/root-AGENTS.md 'ownership by a closed or recent Feature'
assert_not_contains templates/root-AGENTS.md 'regression evidence, or clear Feature ownership enters Bug / Feature Follow-up'

# Newly proposed full runs have an exact one-execution Human authority boundary.
assert_contains references/runtime.md 'One confirmation authorizes one execution of that concrete full run.'
assert_contains references/runtime.md 'Commit never triggers tests merely because the files will be packaged in Git.'
assert_contains references/runtime.md 'A Verification Profile label or broad phrase is not by itself execution permission.'
assert_contains references/runtime.md 'relevant input or HEAD change'
assert_contains references/human-review-summary.md 'Full Test Run Confirmation'
assert_contains references/submit-and-integrate.md 'manual CI rerun'
assert_contains references/submit-and-integrate.md 'must not cause a duplicate local full run'
assert_contains references/submit-and-integrate.md 'required full validation is declined'
assert_contains references/checker-recovery.md 'Full Test Run Confirmation'
assert_contains docs/maintenance/full-validation-method.md '具体全量执行确认'
assert_contains references/human-review-summary.md 'explicitly bounded retry count and condition'
assert_contains references/submit-and-integrate.md 'explicitly bounded retry count and condition'
assert_contains templates/root-AGENTS.md 'explicitly bounded retry count and condition'
assert_contains README.md 'explicitly bounded retry count and condition'
assert_contains Usage.md 'explicitly bounded retry count and condition'
assert_contains CHANGELOG.md 'explicitly bounded retry count and condition'
assert_contains docs/maintenance/full-validation-method.md 'does not reuse the runtime bounded-retry exception'

# Direct Edit remains a method, never a new persistent workflow surface or bypass.
for file in SKILL.md references/runtime.md references/design.md references/direct-edit-fast-path.md templates/root-AGENTS.md; do
  assert_not_contains "$file" 'Direct Edit Mode'
  assert_not_contains "$file" 'Direct Edit Status'
  assert_not_contains "$file" 'Direct Edit Lifecycle'
  assert_not_contains "$file" '.agent-loop/direct-edits'
done
assert_not_contains references/direct-edit-fast-path.md '--skip-tests'
assert_not_contains references/direct-edit-fast-path.md '--no-verify'

for scenario in \
  'Trivial Documentation Correction Uses Direct Edit' \
  'Confirmed Internal Domain Replacement Uses Direct Edit' \
  'Feature-Local Label Tuning Uses Existing Grant' \
  'Structured Metadata Direct Edit Uses Parser Check' \
  'One-Line Public Contract Exits Direct Edit' \
  'External Endpoint Migration Exits Direct Edit' \
  'Explicit Bug Intent Wins Before Direct Edit' \
  'Persistent Recovery Control And Planned Cross-Session Split' \
  'New Test Requirement Exits Direct Edit' \
  'Failed Minimum Check Blocks Completion' \
  'Unrelated Dirty Work Blocks Exact Attribution' \
  'Direct Edit Grants No Later Action' \
  'Existing Lightweight Cards Remain Unchanged' \
  'Existing Test Obligations Stay At Owning Boundary' \
  'Same-Property Tuning Checks Only Final Value' \
  'Business Multiplier Is Not Cosmetic' \
  'Commit-Only Request Runs No Tests' \
  'New Full Run Waits For Exact Human Confirmation' \
  'Exact Gate 2 Full Run Does Not Ask Twice' \
  'Changed HEAD Expires Full-Run Confirmation' \
  'Declined Optional Full Run Limits Claims Not Commit' \
  'Declined Required Release Validation Blocks Release' \
  'Push-Triggered CI Is Disclosed And Not Duplicated' \
  'Manual CI Rerun Requires Fresh Confirmation'; do
  assert_contains references/validation-scenarios.md "### $scenario"
done
assert_contains references/validation-scenarios.md 'a clearly bound final-input rule'
assert_contains references/validation-scenarios.md 'planned multi-session or handoff remains a Feature hard trigger'

# The release version and every root projection revision move together.
assert_contains SKILL.md 'Version: 1.5.8'
assert_contains plugin.json '"version": "1.5.8"'
assert_contains README.md '**Current version:** 1.5.8'
assert_contains Usage.md '**版本：** 1.5.8'
assert_contains CHANGELOG.md '## 1.5.8 — 2026-08-27'

ruby - "$root/references/direct-edit-fast-path.md" "$root/references/runtime.md" "$root/references/submit-and-integrate.md" <<'RUBY'
direct = File.read(ARGV.fetch(0))
runtime = File.read(ARGV.fetch(1))
submit = File.read(ARGV.fetch(2))

def section(content, heading, level = 2)
  marker = "#{'#' * level} #{heading}"
  lines = content.lines
  start = lines.index { |line| line.chomp == marker }
  abort "FAIL: missing owning section #{marker}" unless start
  finish = ((start + 1)...lines.length).find do |index|
    lines[index].match?(/^#{'#' * level} (?!#)/)
  end || lines.length
  lines[start...finish].join
end

def direct_contract?(content)
  tokens = [
    'creates no persistent Agent Loop artifact',
    'one final diff inspection plus the minimum matched check',
    'no per-iteration test, card, Plan, notes, or formal verification',
    'Human identifies the final acceptable value',
    'business/runtime multiplier',
    'Explicit Bug management intent takes precedence',
    'durable recovery evidence',
    'minimum post-edit check fails'
  ]
  tokens.all? { |token| content.include?(token) }
end

def full_run_contract?(content)
  tokens = [
    'One confirmation authorizes one execution of that concrete full run.',
    'relevant input or HEAD change',
    'different environment or target',
    'manual rerun requires fresh confirmation',
    'A Verification Profile label or broad phrase is not by itself execution permission.',
    'Commit never triggers tests merely because the files will be packaged in Git.'
  ]
  tokens.all? { |token| content.include?(token) }
end

def submit_contract?(content)
  tokens = [
    'must not cause a duplicate local full run',
    'manual CI rerun',
    'required full validation is declined',
    'Release and release-readiness remain blocked'
  ]
  tokens.all? { |token| content.include?(token) }
end

direct_owner = section(direct, 'Purpose And Position') + section(direct, 'Precedence And Route') +
  section(direct, 'Eligibility') +
  section(direct, 'Hard Escalation Triggers') + section(direct, 'Same-Scope Iterative Tuning') +
  section(direct, 'Zero-Artifact And Memory Boundary') + section(direct, 'Interruption And Failure')
abort 'FAIL: Direct Edit owning sections are incomplete' unless direct_contract?(direct_owner)
abort 'FAIL: runtime full-run authority contract is incomplete' unless full_run_contract?(runtime)
abort 'FAIL: Submit/CI/Release full-run contract is incomplete' unless submit_contract?(submit)

direct_mutations = {
  'persistent card restored' => direct_owner.gsub('creates no persistent Agent Loop artifact', 'creates one persistent Lightweight Change card'),
  'per-iteration checks restored' => direct_owner.gsub('no per-iteration test, card, Plan, notes, or formal verification', 'run a test and formal check after every iteration'),
  'all multipliers cosmetic' => direct_owner.gsub('business/runtime multiplier', 'every multiplier is cosmetic')
}
direct_mutations.each do |name, mutated|
  abort "FAIL: mutation survived: #{name}" if direct_contract?(mutated)
end

full_mutations = {
  'Profile label becomes permission' => runtime.gsub('A Verification Profile label or broad phrase is not by itself execution permission.', 'A Verification Profile label is reusable execution permission.'),
  'Commit auto-runs full tests' => runtime.gsub('Commit never triggers tests merely because the files will be packaged in Git.', 'Commit automatically runs full tests before packaging.'),
  'confirmation survives HEAD change' => runtime.gsub('relevant input or HEAD change', 'all later input and HEAD changes preserve confirmation')
}
full_mutations.each do |name, mutated|
  abort "FAIL: mutation survived: #{name}" if full_run_contract?(mutated)
end

submit_mutations = {
  'Push duplicates automatic CI' => submit.gsub('must not cause a duplicate local full run', 'must also run the same full suite locally'),
  'Release proceeds after decline' => submit.gsub('Release and release-readiness remain blocked', 'Release may proceed without the required evidence')
}
submit_mutations.each do |name, mutated|
  abort "FAIL: mutation survived: #{name}" if submit_contract?(mutated)
end
RUBY

ruby - "$root/templates/root-AGENTS.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
blocks = content.scan(/<!-- agent-loop:managed-start section:([^ ]+) .*?block-version:([^ ]+) -->/)
abort "FAIL: expected 13 root managed blocks, found #{blocks.length}" unless blocks.length == 13
blocks.each do |section, revision|
  expected = '1.5.8-20260826.1'
  abort "FAIL: #{section} expected #{expected}, found #{revision}" unless revision == expected
end
abort 'FAIL: root AGENTS exceeds 190 lines' if content.lines.length > 190
RUBY

[ ! -d "$root/.agent-loop" ] || fail 'source repository must not contain target-project .agent-loop artifacts'

printf 'PASS: Direct Edit and Human-confirmed full-test contracts are complete\n'

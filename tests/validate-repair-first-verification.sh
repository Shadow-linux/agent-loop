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
  grep -Fq -- "$text" "$root/$file" || fail "$file missing Repair-First contract: $text"
}

assert_not_contains() {
  local file=$1 text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    fail "$file contains forbidden Repair-First behavior: $text"
  fi
}

for file in \
  SKILL.md \
  references/runtime.md \
  references/design.md \
  references/lightweight-change-lane.md \
  references/stage-guides.md \
  references/workflow-checklists.md \
  references/skill-routing.md \
  references/external-skill-adapters.md \
  references/human-review-summary.md \
  references/feature-completion-check.md \
  references/project-guidance.md \
  templates/lightweight-execution-card.md \
  templates/notes.md; do
  assert_file "$file"
done

assert_contains references/runtime.md 'Repair-First Verification'
assert_contains references/runtime.md 'Review Repair Fast Path'
assert_contains references/runtime.md 'Required Verification'
assert_contains references/runtime.md 'Existing Test Obligation'
assert_contains references/runtime.md 'Additional Regression Test'
assert_contains references/runtime.md 'does not by itself block Task Done, Lightweight Change completion, or Feature Close'
assert_contains references/runtime.md 'do not claim `fixed`, `done`, `completed`, or `closed`'

assert_contains references/design.md '**Repair-First Verification**'
assert_contains references/design.md '**Review Repair Fast Path**'
assert_contains references/design.md '**Regression Test Advisory**'

assert_contains references/lightweight-change-lane.md '## Repair-First Verification'
assert_contains references/lightweight-change-lane.md 'apply the disclosed bounded change first'
assert_contains references/lightweight-change-lane.md 'run fresh targeted verification after the write'
assert_contains references/lightweight-change-lane.md 'Regression Test Advisory'
assert_not_contains references/lightweight-change-lane.md '-> targeted RED'
assert_not_contains references/lightweight-change-lane.md '-> minimal GREEN'
assert_not_contains references/lightweight-change-lane.md 'Do not use “lightweight” to skip a meaningful RED/GREEN for an isolatable behavior branch.'

assert_contains references/stage-guides.md '### Review Repair Fast Path'
assert_contains references/stage-guides.md 'repair the implementation first'
assert_contains references/stage-guides.md 'return to Gate 1, Gate 2, Decision & Design, Delivery Contract, Bug Management, Diagnose Failure, or the applicable Human Gate'
assert_contains references/workflow-checklists.md 'Classify the finding as `within-approved-boundary` before a Review Repair write.'
assert_contains references/workflow-checklists.md 'Do not downgrade an Existing Test Obligation into a Regression Test Advisory.'

assert_contains references/skill-routing.md 'Review Repair Fast Path and Lightweight Change Lane do not invoke the TDD helper by default.'
assert_contains references/external-skill-adapters.md 'The TDD Adapter remains mandatory for initial Feature execution and explicit Bug repair, not for Review Repair Fast Path or clearly eligible Lightweight Change.'

assert_contains references/human-review-summary.md '## Review Repair And Regression Test Advisory'
assert_contains references/feature-completion-check.md 'An unaccepted Additional Regression Test Advisory does not by itself block Feature close.'
assert_contains templates/lightweight-execution-card.md 'Record a specific Regression Test Advisory or a concrete not-needed reason'
assert_contains templates/notes.md '## Review Repair Evidence'
assert_contains references/project-guidance.md 'Adaptive Plan/Repair-First Verification'
assert_not_contains references/project-guidance.md 'Adaptive Plan/TDD'

for scenario in \
  'Review Repair Fixes Before New Test' \
  'Review Repair Reuses Existing Coverage' \
  'Review Repair Without Reliable Verification Cannot Complete' \
  'Review Repair Product Drift Returns To Owning Gate' \
  'Review Repair Without Authorization Does Not Write' \
  'Lightweight Logic Change Repairs Before Verification' \
  'Existing Test Obligation Cannot Become Advisory' \
  'Additional Regression Advisory Does Not Block Completion' \
  'Human Adds Regression Test After Repair' \
  'Regression Advice Is Specific And Batched' \
  'Explicit Bug Repair Keeps TDD' \
  'Initial Feature Execution Keeps TDD'; do
  assert_contains references/validation-scenarios.md "### $scenario"
done

ruby - "$root/references/runtime.md" "$root/references/stage-guides.md" "$root/references/workflow-checklists.md" <<'RUBY'
runtime = File.read(ARGV.fetch(0))
guides = File.read(ARGV.fetch(1))
checklists = File.read(ARGV.fetch(2))

def h2(content, heading)
  marker = "## #{heading}"
  lines = content.lines
  start = lines.index { |line| line.chomp == marker }
  abort "FAIL: missing owning section #{marker}" unless start
  finish = ((start + 1)...lines.length).find { |index| lines[index].start_with?('## ') } || lines.length
  lines[start...finish].join
end

def ordered?(content, tokens)
  positions = tokens.map { |token| content.index(token) }
  positions.none?(&:nil?) && positions == positions.sort
end

def universal_review_confirmation?(section)
  section.lines.any? do |line|
    normalized = line.downcase
    confirmation = normalized.match?(
      /(?:ask|obtain|require).{0,30}human.{0,30}(?:confirmation|approval)|human.{0,20}(?:confirmation|approval).{0,20}(?:required|before)/
    )
    universal = normalized.match?(/\b(?:all|any|every)\b|before (?:applying|repairing|changing)/)
    behavior_change = normalized.match?(/behaviou?r(?:-altering|\s+(?:change|correction))|alter behaviou?r/)
    review_context = normalized.match?(/review(?:-driven|\s+(?:finding|repair|change))/)
    confirmation && universal && behavior_change && review_context
  end
end

def review_authorization_boundary?(section)
  no_extra_confirmation = section.lines.any? do |line|
    line.include?('within-approved-boundary') &&
      line.include?('implementation behavior correction') &&
      line.include?('no new per-finding Human confirmation')
  end
  exits = [
    'product meaning',
    'Feature definition',
    'accepted implementation boundary',
    'public interface',
    'ADR',
    'Contract',
    'security',
    'data',
    'permission',
    'dependency',
    'migration',
    'architecture',
    'authorization',
    'rollback',
    'reliable verification'
  ].all? { |token| section.include?(token) }
  no_extra_confirmation && exits && !universal_review_confirmation?(section)
end

def existing_obligation_advisory?(section)
  section.lines.any? do |line|
    line.match?(
      /Existing Test Obligations?.{0,80}(?:is|are|becomes?|became|treated as).{0,20}(?:advisory|optional)|Existing Test Obligations?.{0,80}does not (?:by itself )?block/i
    )
  end
end

def task_done_evidence_split?(section)
  current_proof = section.include?('Required Verification') && section.include?('proves the current result')
  existing_hard = section.lines.any? do |line|
    line.include?('Existing Test Obligation') && line.include?('remains required')
  end
  additional_future = section.include?('Additional Regression Test') && section.include?('future protection')
  additional_nonblocking = section.lines.any? do |line|
    line.include?('Additional Regression Test Advisory') &&
      line.include?('does not by itself block Task Done')
  end
  current_proof && existing_hard && additional_future && additional_nonblocking &&
    !existing_obligation_advisory?(section)
end

def completion_evidence_split?(section)
  current_proof = section.include?('fresh verification evidence exists')
  existing_hard = section.lines.any? do |line|
    line.include?('every Existing Test Obligation') && line.include?('is recorded')
  end
  additional_visible = section.lines.any? do |line|
    line.include?('every Additional Regression Test Advisory') && line.include?('is visible')
  end
  additional_nonblocking = section.lines.any? do |line|
    line.include?('unaccepted advisory') && line.include?('does not by itself block Feature Close')
  end
  current_proof && existing_hard && additional_visible && additional_nonblocking &&
    !existing_obligation_advisory?(section)
end

repair_tokens = [
  'within-approved-boundary',
  'repair the implementation first',
  'fresh targeted verification',
  'affected existing checks',
  'Regression Test Advisory'
]

review = h2(guides, 'Review')
abort 'FAIL: Review Repair order is missing or reversed' unless ordered?(review, repair_tokens)

review_checklist = h2(checklists, 'Review')
abort 'FAIL: Review checklist restores per-finding confirmation or loses fast-path exit owners' unless review_authorization_boundary?(review_checklist)

task_done = h2(runtime, 'Task Done Gate')
completion = h2(runtime, 'Completion Gate')
abort 'FAIL: Task Done does not preserve Required/Existing/Additional evidence semantics' unless task_done_evidence_split?(task_done)
abort 'FAIL: Completion does not preserve current proof, Existing obligations, and Additional advice' unless completion_evidence_split?(completion)

mutations = {
  'missing fresh verification' => review.sub('fresh targeted verification', 'optional verification'),
  'missing advisory' => review.sub('Regression Test Advisory', 'silent completion'),
  'reversed write and proof' => review.sub('repair the implementation first', 'verify before any repair')
}
mutations.each do |name, mutated|
  abort "FAIL: mutation survived: #{name}" if ordered?(mutated, repair_tokens)
end


confirmation_mutation = review_checklist + "\n- [ ] Obtain Human approval before every behavior-altering Review repair.\n"
abort 'FAIL: mutation survived: universal review confirmation' if review_authorization_boundary?(confirmation_mutation)

task_done_advisory_mutation = task_done.lines.map do |line|
  if line.include?('Existing Test Obligation') && line.include?('remains required')
    'Existing Test Obligations are advisory and do not block Task Done.'
  else
    line
  end
end.join
abort 'FAIL: mutation survived: Task Done Existing obligation became advisory' if task_done_evidence_split?(task_done_advisory_mutation)

completion_advisory_mutation = completion.lines.map do |line|
  if line.include?('every Existing Test Obligation') && line.include?('is recorded')
    '- Existing Test Obligations are advisory and do not block Feature Close.'
  else
    line
  end
end.join
abort 'FAIL: mutation survived: Completion Existing obligation became advisory' if completion_evidence_split?(completion_advisory_mutation)

separation_mutation = task_done.gsub('Required Verification', 'Verification').gsub('Additional Regression Test', 'Regression Test')
abort 'FAIL: mutation survived: Required/Existing/Additional separation removed' if task_done_evidence_split?(separation_mutation)
RUBY

ruby - "$root/references/runtime.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
intent = content[/^## Message Intent Classification\n(.*?)(?=^## |\z)/m, 1]
stage_order = content[/^## Stage Order\n(.*?)(?=^## |\z)/m, 1]
abort 'FAIL: Message Intent section missing' unless intent
abort 'FAIL: Stage Order section missing' unless stage_order
abort 'FAIL: Review Repair became a message intent' if intent.include?('`review-repair`')
abort 'FAIL: Repair-First became a canonical stage' if stage_order.lines.map(&:strip).include?('Repair-First Verification')
abort 'FAIL: Review Repair became a canonical stage' if stage_order.lines.map(&:strip).include?('Review Repair Fast Path')
RUBY

for forbidden in \
  '.agent-loop/review-repairs/' \
  '.agent-loop/test-debt/' \
  'Test Debt Status:' \
  'Review Repair Status:'; do
  for file in references/runtime.md references/design.md templates/notes.md templates/lightweight-execution-card.md; do
    assert_not_contains "$file" "$forbidden"
  done
done

assert_contains SKILL.md 'Version: 1.5.6'
assert_contains plugin.json '"version": "1.5.6"'
assert_contains README.md '**Current version:** 1.5.6'
assert_contains Usage.md '**版本：** 1.5.6'
assert_contains CHANGELOG.md '## 1.5.6 — 2026-08-15'

ruby - "$root/templates/root-AGENTS.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
blocks = content.scan(/<!-- agent-loop:managed-start section:([^ ]+) .*?block-version:([^ ]+) -->/)
abort "FAIL: expected 13 root managed blocks, found #{blocks.length}" unless blocks.length == 13
blocks.each do |section, revision|
  expected = '1.5.6-20260815.1'
  abort "FAIL: #{section} expected #{expected}, found #{revision}" unless revision == expected
end
abort 'FAIL: root AGENTS exceeds 190 lines' if content.lines.length > 190
RUBY

[ ! -d "$root/.agent-loop" ] || fail 'source repository must not contain target-project .agent-loop artifacts'

printf 'PASS: Repair-First Review Repair and Lightweight Change contract is complete\n'

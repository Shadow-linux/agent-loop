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
  grep -Fq -- "$text" "$root/$file" || fail "$file missing Bug Management contract: $text"
}

assert_not_contains() {
  local file=$1
  local text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    fail "$file contains forbidden Bug Management behavior: $text"
  fi
}

for file in \
  references/bug-management.md \
  templates/bug-index.md \
  templates/bug-README.md; do
  assert_file "$file"
done

for file in \
  docs/proposal/v1.4.x/bug-management-implementation-plan.md \
  references/artifact-rules.md \
  references/bug-management.md \
  references/concepts.md \
  references/document-templates.md \
  references/feature-follow-up.md \
  references/implementation-planning.md \
  templates/plan.md; do
  assert_contains "$file" 'bugs/YYYY-MM-DD-<bug-slug>/'
  assert_not_contains "$file" 'bugs/<bug-id>/'
done
assert_contains SKILL.md 'YYYY-MM-DD-<bug-slug>/'
assert_not_contains SKILL.md 'bugs/<bug-id>/'
assert_contains README.md 'YYYY-MM-DD-<bug-slug>/'
assert_not_contains README.md '<bug-id>/'

for text in \
  'reported | triaging | confirmed | in-progress | verifying | deferred | closed' \
  'unresolved | fixed | duplicate | not-a-bug | cannot-reproduce | accepted-risk | superseded' \
  'investigate-first | flow-back | linked-feature | maintenance-fix | requirement | no-fix' \
  'person | customer | group | qa | monitoring | automated-test | agent | external-ticket | other | unknown' \
  'Bug identity does not use a time cutoff.' \
  'Default Feature ownership lookback is 90 calendar days.' \
  'Archive changes location, not Feature identity or ownership.' \
  'Discovery and Human Review do not require rehydrate.' \
  'Bug artifacts do not own tasks, tests, plans, or code execution.'; do
  assert_contains references/bug-management.md "$text"
done

for file in SKILL.md references/runtime.md references/design.md references/feature-follow-up.md references/stage-guides.md references/workflow-checklists.md; do
  assert_contains "$file" 'Bug Management'
done

assert_contains references/feature-follow-up.md 'Default recent window: **90 calendar days**'
assert_contains references/feature-follow-up.md 'Bug Index metadata has no time cutoff'
assert_contains references/branch-management.md 'Bug Management owns Bug identity, lifecycle, and Resolution Path.'
assert_contains templates/project.md 'Feature Follow-up Lookback: 90 days'
assert_contains templates/notes.md 'Lookback Window: 90 days | outside-default-window'
assert_contains templates/bug-README.md 'Origin Type: person | customer | group | qa | monitoring | automated-test | agent | external-ticket | other | unknown'
assert_contains templates/bug-README.md 'Requirement Impact: none | violates-accepted-behavior | ambiguity-found | change-required'
assert_contains templates/bug-README.md 'Status: reported | triaging | confirmed | in-progress | verifying | deferred | closed'
assert_contains templates/bug-README.md 'Resolution: unresolved | fixed | duplicate | not-a-bug | cannot-reproduce | accepted-risk | superseded'
assert_contains templates/spec.md 'Related Bugs:'
assert_contains templates/tests.md '## Bug Verification Matrix'
assert_contains templates/plan.md 'Bug Context Evidence:'
assert_contains templates/notes.md 'Related Bugs:'
assert_contains templates/requirement-set-README.md 'Related Bugs:'
assert_contains references/feature-completion-check.md 'Bug Close Decision'
assert_contains references/human-review-summary.md '### Bug Triage And Resolution Path Review'
assert_contains references/human-review-summary.md '### Bug Verification And Close Review'
assert_contains SKILL.md 'an `in-progress` Bug does not use `flow-back | linked-feature | maintenance-fix` or lacks one Human-confirmed Fix Feature Target'
assert_contains SKILL.md 'Before creating, updating, or reopening a stable Bug Record, scan all Bug Index metadata for duplicate/reopen identity, then scan the default 90-day Feature metadata window with evidence-ranked deep read and evidence-driven extension beyond 90 days.'
for file in references/bug-management.md references/design.md references/runtime.md references/stage-guides.md references/workflow-checklists.md templates/bug-README.md; do
  assert_contains "$file" 'An `in-progress` Bug requires `flow-back | linked-feature | maintenance-fix` plus one Human-confirmed Fix Feature Target.'
done
for scenario in \
  'Existing Feature Regression Flows Back' \
  'Narrow Internal Bug Uses Maintenance Fix' \
  'New Product Behavior Is Not Misclassified As Bug' \
  'Multiple Origins Deduplicate Into One Bug' \
  'Existing Bug Record Closes As Duplicate' \
  'Closed Bug Reopens Append-Only' \
  'Unknown Report Origin Does Not Block Triage' \
  'Cannot Reproduce Requires Attempt Evidence' \
  'Requirement Link Does Not Auto-Rollback Lifecycle' \
  'Bug May Link Multiple Requirements' \
  'One Feature May Resolve Multiple Bugs' \
  'Ordinary Chat Does Not Create Bug Artifact' \
  'Missing Agent Loop Memory Routes To Project Entry' \
  'Archived Feature Discovery Does Not Require Rehydrate' \
  'Sealed Release Requires New Patch Context' \
  'Passing Feature Tests Does Not Auto-Close Bug' \
  'Accepted Risk Requires Explicit Human Decision' \
  'Customer Origin Does Not Infer Customer Repair Line' \
  '60-Day Feature Remains Inside Default Bug Ownership Window' \
  '120-Day Feature Uses Evidence-Driven Extended Scan' \
  'Accepted Requirement Is Not Feature Authorization' \
  'Critical Severity Is Not Hotfix Or Release Authorization' \
  'Unknown Origin Cannot Block Repair' \
  'Deferred Is Not Closed' \
  'Archive Discovery Cannot Auto-Rehydrate' \
  'Duplicate Title Does Not Auto-Merge Records' \
  'Bug Record Does Not Receive Execution Artifacts' \
  'Requirement Path Cannot Use In Progress' \
  'Commit Approval Is Not Bug Close Approval'; do
  assert_contains references/validation-scenarios.md "$scenario"
done

assert_not_contains templates/bug-README.md 'Assignee:'
assert_not_contains templates/bug-README.md 'Owner:'
[ ! -e "$root/templates/bug-tasks.md" ] || fail 'Bug must not have its own tasks template'
[ ! -e "$root/templates/bug-tests.md" ] || fail 'Bug must not have its own tests template'
[ ! -e "$root/templates/bug-plan.md" ] || fail 'Bug must not have its own plan template'
[ ! -d "$root/.agent-loop" ] || fail 'skill source repository must not contain target-project .agent-loop artifacts'

ruby - "$root/references/runtime.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
section = content[/## Stage Order\n(.*?)(?=\n## |\z)/m, 1]
abort 'FAIL: runtime Stage Order missing' unless section
abort 'FAIL: Bug Management became a canonical stage' if section.lines.any? { |line| line.strip == 'Bug Management' }
RUBY

ruby - "$root/references/runtime.md" "$root/references/stage-guides.md" <<'RUBY'
files = ARGV
tokens = [
  'complete Bug Index metadata',
  '90-day Feature metadata scan',
  'evidence-ranked',
  'create/update/reopen Bug Record'
]

files.each do |path|
  content = File.read(path)
  heading = path.end_with?('runtime.md') ? 'Human-Guided Bug Management' : 'Feature Follow-up And Flow-back'
  section = content[/^## #{Regexp.escape(heading)}\n(.*?)(?=^## |\z)/m, 1]
  abort "FAIL: #{path} missing #{heading} section" unless section
  sequence = section.scan(/```text\n(.*?)```/m).flatten.find { |block| tokens.all? { |token| block.include?(token) } }
  abort "FAIL: #{path} missing canonical Bug intake sequence block" unless sequence
  positions = tokens.map { |token| sequence.index(token) }
  abort "FAIL: #{path} missing canonical Bug intake sequence token" if positions.any?(&:nil?)
  abort "FAIL: #{path} reorders canonical Bug intake sequence" unless positions == positions.sort
end
RUBY
assert_contains references/design.md 'Bug intake order is complete Bug Index metadata scan -> 90-day Feature metadata scan -> evidence-ranked deep read / evidence-driven extended scan -> create/update/reopen Bug Record'

ruby - "$root/templates/root-AGENTS.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
blocks = content.scan(/<!-- agent-loop:managed-start section:([^ ]+) .*?block-version:([^ ]+) -->/)
abort 'FAIL: root managed blocks missing' if blocks.empty?
blocks.each do |section, revision|
  expected = '1.5.0-20260725.2'
  abort "FAIL: #{section} expected #{expected}, found #{revision}" unless revision == expected
end
RUBY

ruby - "$root/references/validation-scenarios.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
section = content[/^## 72\. Human-Guided Bug Management\n(.*)\z/m, 1]
abort 'FAIL: Bug Management pressure scenario section missing' unless section

required = [
  'Existing Feature Regression Flows Back',
  'Narrow Internal Bug Uses Maintenance Fix',
  'New Product Behavior Is Not Misclassified As Bug',
  'Multiple Origins Deduplicate Into One Bug',
  'Existing Bug Record Closes As Duplicate',
  'Closed Bug Reopens Append-Only',
  'Unknown Report Origin Does Not Block Triage',
  'Cannot Reproduce Requires Attempt Evidence',
  'Requirement Link Does Not Auto-Rollback Lifecycle',
  'Bug May Link Multiple Requirements',
  'One Feature May Resolve Multiple Bugs',
  'Ordinary Chat Does Not Create Bug Artifact',
  'Missing Agent Loop Memory Routes To Project Entry',
  'Archived Feature Discovery Does Not Require Rehydrate',
  'Sealed Release Requires New Patch Context',
  'Passing Feature Tests Does Not Auto-Close Bug',
  'Accepted Risk Requires Explicit Human Decision',
  'Customer Origin Does Not Infer Customer Repair Line',
  '60-Day Feature Remains Inside Default Bug Ownership Window',
  '120-Day Feature Uses Evidence-Driven Extended Scan'
]
fields = [
  'Evidence:',
  'Bug Record Decision:',
  'Expected Behavior Source:',
  'Resolution Path:',
  'Required Human Gate:',
  'Forbidden Action:',
  'Next Stage:'
]

required.each do |name|
  body = section[/^### [A-Z]+\. #{Regexp.escape(name)}\n(.*?)(?=^### [A-Z]+\. |\z)/m, 1]
  abort "FAIL: missing structured Bug scenario: #{name}" unless body
  fields.each do |field|
    abort "FAIL: #{name} missing #{field}" unless body.include?(field)
  end
end
RUBY

printf 'PASS: Human-Guided Bug Management identity, lifecycle, routing, archive, gate, artifact, and scope contract is complete\n'

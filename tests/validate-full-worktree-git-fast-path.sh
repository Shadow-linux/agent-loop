#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

assert_contains() {
  local file=$1 text=$2
  grep -Fq -- "$text" "$root/$file" || fail "$file missing Git Fast Path contract: $text"
}

for file in \
  references/runtime.md \
  references/design.md \
  references/submit-and-integrate.md \
  references/stage-guides.md \
  references/workflow-checklists.md \
  references/branch-management.md \
  references/human-review-summary.md \
  references/validation-scenarios.md \
  references/project-guidance.md \
  templates/root-AGENTS.md \
  templates/notes.md \
  README.md Usage.md CHANGELOG.md; do
  [ -f "$root/$file" ] || fail "missing required file: $file"
done

assert_contains references/runtime.md 'Full-Worktree Git Fast Path'
assert_contains references/runtime.md 'does not run Verify, Review, Drift Check, Feature Completion Check, or tests merely because Git was requested'
assert_contains references/runtime.md 'one lightweight Commit Confirmation'
assert_contains references/runtime.md 'This is not a code, quality, Feature, verification, Drift, or Completion Review'
assert_contains references/design.md '**Full-Worktree Git Fast Path**'
assert_contains references/submit-and-integrate.md '## Full-Worktree Git Fast Path'
assert_contains references/submit-and-integrate.md '`git add -A`'
assert_contains references/submit-and-integrate.md 'not run for this Git action; no completion or release-readiness claim'
assert_contains references/submit-and-integrate.md 'present one lightweight Commit Confirmation'
assert_contains references/submit-and-integrate.md 'complete worktree file/change summary and the proposed commit message'
assert_contains references/stage-guides.md '### Full-Worktree Git Fast Path'
assert_contains references/workflow-checklists.md 'The following checklist is normal-submit only; skip it entirely for Full-Worktree Git Fast Path.'
assert_contains references/workflow-checklists.md '## Full-Worktree Git Fast Path'
assert_contains references/branch-management.md 'Full-Worktree Git Fast Path preserves branch-policy facts without restoring normal Submit quality prerequisites'
assert_contains references/human-review-summary.md 'Full-Worktree Git Fast Path uses a lightweight Commit Confirmation, not a Human Review Summary'
assert_contains references/submit-and-integrate.md 'Git Path: full-worktree-fast-path | normal-submit'
assert_contains references/submit-and-integrate.md 'Push Decision / Remote / Ref:'
assert_contains templates/notes.md 'Git Path: full-worktree-fast-path | normal-submit'
assert_contains templates/root-AGENTS.md 'For an explicit commit or commit-and-push request, show one lightweight confirmation of the entire-worktree summary and proposed commit message'
assert_contains README.md 'Full-Worktree Git Fast Path'
assert_contains Usage.md '整个工作区 Git 快速路径'
assert_contains CHANGELOG.md '### Full-Worktree Git Fast Path'

for scenario in \
  'Git Fast Path Commits Entire Dirty Worktree' \
  'Git Fast Path Does Not Auto-Run Tests' \
  'Git Fast Path Honors Human Test Condition' \
  'Git Fast Path Discloses Suspicious Files Without Excluding Them' \
  'Git Fast Path Stops On Confirmed Scope Drift' \
  'Commit And Push Keep Separate Decision Rows' \
  'Git Fast Path Cannot Claim Completion'; do
  assert_contains references/validation-scenarios.md "### $scenario"
done

ruby - "$root/references/submit-and-integrate.md" "$root/references/runtime.md" "$root/references/workflow-checklists.md" <<'RUBY'
submit = File.read(ARGV.fetch(0))
runtime = File.read(ARGV.fetch(1))
checklists = File.read(ARGV.fetch(2))

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

def fast_path_contract?(content)
  tokens = [
    'explicitly asks for `commit` or `commit and push`',
    'present one lightweight Commit Confirmation',
    'complete worktree file/change summary and the proposed commit message',
    'do not run tests or perform code/quality Review',
    'entire current worktree',
    '`git add -A`',
    'do not automatically run tests',
    'not run for this Git action; no completion or release-readiness claim',
    'staged, unstaged, untracked, and deleted',
    'do not exclude, restore, clean, stash, split, or discard',
    'Commit immediately',
    '`commit and push` authorizes Commit and Push'
  ]
  tokens.all? { |token| content.include?(token) }
end

def forbidden_legacy_fast_path?(content)
  content.lines.any? do |line|
    normalized = line.downcase
    in_fast_path = normalized.include?('git fast path') || normalized.include?('explicit commit') || normalized.include?('full-worktree')
    forced_quality = normalized.match?(/(?:must|required to|always).{0,35}(?:test|verification|review|drift).{0,25}before (?:commit|git)/)
    selective = normalized.match?(/(?:exclude|omit|split).{0,35}(?:unrelated|untracked|workspace).{0,20}(?:automatically|without human)/)
    extra_confirmation = normalized.match?(/(?:pre-commit|second|again|follow-up|additional).{0,25}(?:review|confirmation|approval)/) && !normalized.include?('do not')
    in_fast_path && (forced_quality || selective || extra_confirmation)
  end
end

fast = section(submit, 'Full-Worktree Git Fast Path')
abort 'FAIL: Git Fast Path owning section is incomplete' unless fast_path_contract?(fast)
abort 'FAIL: Git Fast Path contains legacy forced checks/exclusion/second confirmation' if forbidden_legacy_fast_path?(fast)

runtime_fast = section(runtime, 'Full-Worktree Git Fast Path')
abort 'FAIL: runtime loses completion-truth boundary' unless runtime_fast.include?('Git packaging permission is not completion evidence')
abort 'FAIL: runtime loses independent Push authorization' unless runtime_fast.include?('Push') && runtime_fast.include?('independent')

checklist_fast = section(checklists, 'Full-Worktree Git Fast Path')
abort 'FAIL: checklist loses lightweight Commit Confirmation' unless checklist_fast.include?('Present one lightweight Commit Confirmation')
abort 'FAIL: checklist restores quality Review' unless checklist_fast.include?('Do not run tests or perform code/quality Review')
abort 'FAIL: checklist does not preserve all worktree states' unless %w[staged unstaged untracked deleted].all? { |token| checklist_fast.include?(token) }

mutations = {
  'mandatory pre-commit tests' => fast + "\nGit Fast Path must run tests before commit.\n",
  'automatic unrelated exclusion' => fast + "\nGit Fast Path may exclude unrelated workspace files automatically.\n",
  'second confirmation' => fast + "\nGit Fast Path requires a second confirmation after Commit Confirmation.\n"
}
mutations.each do |name, mutated|
  abort "FAIL: mutation survived: #{name}" unless forbidden_legacy_fast_path?(mutated)
end

missing_full_scope = fast.sub('staged, unstaged, untracked, and deleted', 'selected files')
abort 'FAIL: mutation survived: incomplete worktree scope' if fast_path_contract?(missing_full_scope)

missing_truth = fast.gsub('not run for this Git action; no completion or release-readiness claim', 'not run')
abort 'FAIL: mutation survived: unverified completion truth lost' if fast_path_contract?(missing_truth)

review_mutation = fast.sub('do not run tests or perform code/quality Review', 'perform code quality Review before commit')
abort 'FAIL: mutation survived: quality Review restored' if fast_path_contract?(review_mutation)
RUBY

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

printf 'PASS: Full-Worktree Git Fast Path contract and mutations are valid\n'

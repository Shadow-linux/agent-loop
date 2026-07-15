#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

assert_file_exists() {
  [ -f "$root/$1" ] || fail "missing required file: $1"
}

assert_contains() {
  local file=$1
  local text=$2
  grep -Fq -- "$text" "$root/$file" || fail "$file missing branch-management contract: $text"
}

assert_not_contains() {
  local file=$1
  local text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    fail "$file contains forbidden root/scope detail: $text"
  fi
}

reference=references/branch-management.md
assert_file_exists "$reference"

for file in SKILL.md references/design.md references/runtime.md references/stage-guides.md references/workflow-checklists.md; do
  assert_contains "$file" "Branch Strategy Check"
done
assert_contains SKILL.md 'branch class or unique Target Branch is unknown'

assert_contains SKILL.md 'when an adopted Branch Strategy or versioned/customer delivery applies: the branch class or unique Target Branch is unknown'
assert_contains SKILL.md 'branch creation, switching, deletion, push, or tag'
assert_contains references/runtime.md 'branch creation, switching, deletion, push, or tag'

for text in \
  'release/v<semver>' \
  'customer/<customer>/v<semver>' \
  '<work-type>/v<semver>/<topic>' \
  '<work-type>/<customer>-v<semver>/<topic>' \
  'released / sealed' \
  'Strategy Adoption Gate' \
  'Customer Isolation' \
  'Cleanup Gate'; do
  assert_contains "$reference" "$text"
done

assert_contains "$reference" 'feature | bugfix | hotfix'
assert_contains "$reference" 'existing-project | human-guided-release | not-applicable'
assert_contains "$reference" 'accepted | declined | not-needed'
assert_contains "$reference" 'Recommendation and adoption do not authorize branch creation, switching, merge, deletion, push, tag, release, or publish.'
assert_contains "$reference" '| Branch Action Gate | creation or switching of one exact development branch |'
assert_contains "$reference" '`declined`: record `Profile: not-applicable` and a concrete decline reason'
assert_contains "$reference" 'A simple `not-needed` path does not require Target Release Context or Target Branch and must not block normal non-versioned work.'
assert_contains "$reference" 'When an adopted Branch Strategy or versioned/customer delivery applies, if Target Release Context or the unique Target Branch is unclear'
assert_contains "$reference" 'Technical Design / Plan Gate: when an adopted Branch Strategy or versioned/customer delivery applies'
assert_contains "$reference" 'Stop dependent integration/release work only when an adopted Branch Strategy or versioned/customer delivery applies and:'
assert_contains "$reference" 'does not implement Bug Management'
assert_contains "$reference" 'does not implement worktree / branch memory merge'
assert_contains "$reference" 'Do not create a default `.agent-loop/branches/` directory.'

assert_contains references/submit-and-integrate.md 'Target Release Context'
assert_contains references/submit-and-integrate.md 'Source Branch'
assert_contains references/submit-and-integrate.md 'Target Branch'
assert_contains references/submit-and-integrate.md 'released / sealed'
assert_contains references/submit-and-integrate.md 'Customer Isolation'
assert_contains references/submit-and-integrate.md 'When an adopted Branch Strategy or versioned/customer delivery applies, compare accepted Branch Strategy and Target Release Context'
assert_contains references/submit-and-integrate.md 'For a confirmed simple `not-needed` path, record branch-specific checks as `not-applicable`'

for field in \
  'Adoption Status:' \
  'Profile:' \
  'Main Branch:' \
  'Standard Release Pattern:' \
  'Customer Release Pattern:' \
  'Development Pattern:' \
  'Release Immutability:' \
  'Customer Isolation:' \
  'Deletion Policy:' \
  'Human Confirmed:' \
  'Evidence:'; do
  assert_contains templates/project.md "$field"
  assert_contains references/document-templates.md "$field"
done

assert_contains templates/project.md 'Target Release Context:'
assert_contains templates/notes.md '## Current Branch Context'
assert_contains templates/notes.md 'Branch Class:'
assert_contains templates/notes.md 'Target Branch:'
assert_contains templates/notes.md 'Lifecycle State:'
assert_contains templates/notes.md 'Branch Class: main | standard-release | customer-release | development | unknown'
assert_contains templates/notes.md 'Work Type: feature | bugfix | hotfix | not-applicable'
assert_contains templates/notes.md 'Target Kind: standard | customer | not-applicable'
assert_contains templates/plan.md 'Branch Context Evidence:'
assert_contains templates/plan.md 'Current Branch Context Evidence:'
assert_contains templates/plan.md 'Git actions authorized by this plan: none'
assert_contains templates/plan.md 'For a confirmed simple `not-needed` path, set branch-specific fields to `not-applicable`'
assert_contains references/document-templates.md 'For a confirmed simple `not-needed` path, set branch-specific fields to `not-applicable`'
assert_contains references/concepts.md '**Current Branch Context**'
assert_contains templates/project.md 'An unanswered recommendation is not `accepted`.'
assert_contains templates/project.md 'Changing durable strategy requires Drift Check and a Human Gate.'
assert_contains templates/project.md 'Profile: existing-project | human-guided-release | not-applicable'
assert_contains templates/project.md 'Decline Reason:'
assert_contains references/document-templates.md 'Profile: existing-project | human-guided-release | not-applicable'
assert_contains references/document-templates.md 'Decline Reason:'
assert_contains docs/proposal/v1.4.x/branch-management-strategy.md 'Profile: existing-project | human-guided-release | not-applicable'

reminder='When existing branch rules are confused, the target version is unclear, or customer isolation is at risk, load `references/branch-management.md`, recommend one optional strategy, and adopt it only after explicit human acceptance.'
count=$(grep -Fxc -- "$reminder" "$root/templates/root-AGENTS.md" || true)
[ "$count" -eq 1 ] || fail "root AGENTS must contain the exact branch-management reminder once; found $count"
assert_not_contains templates/root-AGENTS.md '当现有分支规则混乱'

ruby - "$root/templates/root-AGENTS.md" "$reminder" <<'RUBY'
content = File.read(ARGV.fetch(0))
reminder = ARGV.fetch(1)
ownership = content[/<!-- agent-loop:managed-start section:ownership .*?-->\n(.*?)<!-- agent-loop:managed-end section:ownership -->/m, 1]
abort 'FAIL: root AGENTS ownership block missing' unless ownership
abort 'FAIL: branch-management reminder must live inside ownership managed block' unless ownership.lines.map(&:chomp).include?(reminder)
RUBY

ruby - "$root/templates/root-AGENTS.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
blocks = content.scan(/<!-- agent-loop:managed-start section:([^ ]+) .*?block-version:([^ ]+) -->/)
abort 'FAIL: root AGENTS managed blocks missing' if blocks.empty?
blocks.each do |section, revision|
  expected = '1.4.0-20260715'
  abort "FAIL: #{section} expected #{expected}, found #{revision}" unless revision == expected
end
RUBY

for forbidden in \
  'release/v<semver>' \
  'customer/<customer>/v<semver>' \
  'Adoption Status:' \
  'released / sealed' \
  'Strategy Adoption Gate'; do
  assert_not_contains templates/root-AGENTS.md "$forbidden"
done

assert_contains references/human-review-summary.md '### Branch Strategy And Action Review'
assert_contains references/human-review-summary.md '| Requested Authorization |'
assert_contains references/human-review-summary.md '| Explicitly Not Authorized |'
assert_contains references/human-review-summary.md '| Observed Policy / Git Evidence |'
assert_contains references/human-review-summary.md '| Verification / Review / Drift |'
assert_contains references/human-review-summary.md '| Remaining Risk / Blocker |'
assert_contains references/validation-scenarios.md 'Human-Guided Branch Management'
assert_contains references/validation-scenarios.md 'Existing Clear Strategy Is Not Forced To Migrate'
assert_contains references/validation-scenarios.md 'Sealed Release Rejects Same-Version Repair'
assert_contains references/validation-scenarios.md 'Customer Branch Cannot Flow Wholesale Into Standard Product'
assert_contains references/validation-scenarios.md 'Strategy Adoption Does Not Authorize Branch Creation'
assert_contains references/validation-scenarios.md 'External Finishing Helper Cannot Mutate Git'
assert_contains references/validation-scenarios.md 'Git Reality Conflict Routes To Drift'
assert_contains references/validation-scenarios.md 'Required Human Gate:'
assert_contains references/validation-scenarios.md 'Forbidden Action:'
assert_contains references/validation-scenarios.md 'Next Stage:'
assert_contains README.md 'Human-Guided Branch Management'
assert_contains README.md 'Usage.md#我想让-agent-推荐分支管理方式'
assert_contains Usage.md '### 我想让 Agent 推荐分支管理方式'
assert_contains Usage.md 'feature|bugfix|hotfix/vX.Y.Z/<topic>'
assert_contains Usage.md 'feature|bugfix|hotfix/<customer>-vX.Y.Z/<topic>'
assert_contains CHANGELOG.md 'Human-Guided Branch Management'
assert_contains references/runtime.md 'human-confirmed native repository policy'
assert_contains references/runtime.md 'accepted project.md Branch Strategy snapshot'
assert_contains references/runtime.md 'Agent inference from branch names'
assert_not_contains "$reference" 'before every branch creation or switch'
assert_contains references/workflow-checklists.md 'When an adopted Branch Strategy or versioned/customer delivery applies, `Branch Context Evidence`'
assert_contains references/workflow-checklists.md 'For a confirmed simple `not-needed` path, record branch-specific Plan and Submit checks as `not-applicable`'
assert_contains references/stage-guides.md 'when an adopted Branch Strategy or versioned/customer delivery applies, run Branch Strategy Check and verify Source Branch'
assert_contains references/stage-guides.md 'for a confirmed simple `not-needed` path, record branch-specific fields as `not-applicable` and do not block Submit / Integrate'
assert_contains references/stage-guides.md 'when an adopted Branch Strategy or versioned/customer delivery applies, compare accepted Branch Strategy and Target Release Context'
assert_contains references/workflow-checklists.md 'When an adopted Branch Strategy or versioned/customer delivery applies, compare accepted Branch Strategy and Target Release Context'

ruby - "$root/references/stage-guides.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
section = content[/## Execute Task \/ Story\n(.*?)(?=\n## |\z)/m, 1]
abort 'FAIL: Execute Task / Story section missing' unless section
abort 'FAIL: Execute Task / Story must recheck Current Branch Context' unless section.include?('Current Branch Context')
abort 'FAIL: Execute Task / Story must not imply branch create/switch' unless section.include?('create or switch')
RUBY

ruby - "$root/references/runtime.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
section = content[/## Stage Order\n(.*?)(?=\n## |\z)/m, 1]
abort 'FAIL: runtime Stage Order section missing' unless section
forbidden = ['Branch Strategy Check', 'Strategy Adoption Gate', 'Release Scope Gate', 'Customer Scope Gate']
found = forbidden.select { |name| section.lines.any? { |line| line.strip == name } }
abort "FAIL: branch management added canonical stages: #{found.join(', ')}" unless found.empty?
RUBY

ruby - "$root/docs/proposal/v1.4.x/branch-management-strategy.md" "$root/Usage.md" <<'RUBY'
proposal = File.read(ARGV.fetch(0))
usage = File.read(ARGV.fetch(1))
proposal_graph = proposal[/## 完整分支逻辑图.*?```mermaid\n(.*?)```/m, 1]
usage_graph = usage[/### 我想让 Agent 推荐分支管理方式.*?```mermaid\n(.*?)```/m, 1]
abort 'FAIL: proposal branch Mermaid graph missing' unless proposal_graph
abort 'FAIL: Usage branch Mermaid graph missing' unless usage_graph
abort 'FAIL: Usage branch Mermaid graph drifted from Proposal' unless usage_graph == proposal_graph
RUBY

[ ! -d "$root/.agent-loop" ] || fail 'skill source repository must not contain target-project .agent-loop artifacts'

printf 'PASS: Human-Guided Branch Management optional profile, gates, artifacts, diagram, and scope contract is complete\n'

#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

assert_contains() {
  local file=$1 text=$2
  if ! grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s missing required text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_not_contains() {
  local file=$1 text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s contains forbidden text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

for file in \
  SKILL.md \
  references/design.md \
  references/concepts.md \
  references/runtime.md \
  references/stage-guides.md \
  references/workflow-checklists.md \
  references/human-review-summary.md \
  references/artifact-rules.md \
  references/project-guidance.md \
  templates/root-AGENTS.md \
  templates/notes.md \
  scripts/check-feature-review.py \
  tests/test_feature_review.py \
  references/validation-scenarios.md \
  README.md \
  Usage.md \
  CHANGELOG.md
do
  [[ -f "$root/$file" ]] || {
    printf 'FAIL: missing required file: %s\n' "$file" >&2
    exit 1
  }
done

assert_contains references/runtime.md 'Gate 1: Feature Definition Review'
assert_contains references/runtime.md 'Gate 2: Implementation Readiness Review'
assert_contains references/runtime.md 'Gate 1 acceptance authorizes package preparation only'
assert_contains references/runtime.md 'does not authorize target implementation'
assert_contains references/runtime.md 'without separate Work Breakdown, Test Design, E2E Discovery, Technical Design, or Plan approval prompts'
assert_contains references/runtime.md 'Approve package only'
assert_contains references/runtime.md 'Approve package and start implementation'
assert_contains references/runtime.md 'without a third generic Feature Auto-Loop prompt'
assert_contains references/runtime.md 'Implementation Readiness: preparing | review-ready | accepted'
assert_contains references/runtime.md 'explicitly says to start implementation after package-only acceptance'
assert_contains references/runtime.md 'confirm the accepted spec/tasks/tests/Plan package is unchanged'
assert_contains references/runtime.md 'Gate 2 Package Digest'
assert_contains references/runtime.md 'Gate 2 Stable Digest'
assert_contains references/runtime.md 'Gate 2 Stable Digest Algorithm'
assert_contains references/runtime.md 'review-definition-v2'
assert_contains references/runtime.md 'check-feature-review.py --mode digest'
assert_contains references/runtime.md 'check-feature-review.py --mode start'
assert_contains references/runtime.md 'check-feature-review.py --mode execute'

assert_contains references/stage-guides.md 'Feature Definition Review'
assert_contains references/stage-guides.md 'Implementation Package Preparation'
assert_contains references/stage-guides.md 'Implementation Readiness Review'
assert_contains references/stage-guides.md 'target implementation is forbidden before Gate 2'
assert_contains references/stage-guides.md 'without a separate Targeted Feature Scan prompt'
assert_contains references/stage-guides.md 'return to Gate 1'
assert_contains references/stage-guides.md 'repeat Gate 2'
assert_contains references/stage-guides.md 'Gate 1 Decision: accepted'
assert_contains references/stage-guides.md 'check-feature-review.py --mode review'
assert_contains references/stage-guides.md 'later `plan.md` rotation'
assert_contains references/stage-guides.md 'a story Plan must list non-empty `Included Tasks`'
assert_contains references/stage-guides.md 'repair fact-determined gaps in `tasks.md`, `tests.md`, technical context, and Plan without another prompt'
assert_not_contains references/stage-guides.md 'update docs only after confirmation'
assert_contains references/runtime.md 'do not add a third generic Feature Auto-Loop prompt after approve-and-start'

assert_contains references/human-review-summary.md '## Feature Definition Review Summary'
assert_contains references/human-review-summary.md '## Implementation Readiness Review Summary'
assert_contains references/workflow-checklists.md 'Approve package only'
assert_contains references/workflow-checklists.md 'Approve package and start implementation'
assert_contains references/workflow-checklists.md 'non-rotatable Stable Files/Digest'
assert_contains templates/notes.md 'Implementation Readiness: preparing | review-ready | accepted'
assert_contains templates/notes.md 'Gate 2 Agent-ready Tasks'
assert_contains templates/notes.md 'Gate 2 Stable Digest Algorithm: review-definition-v2'
assert_contains templates/notes.md 'Gate 2 Plan Evidence'
assert_contains templates/root-AGENTS.md 'Feature construction normally stops at two reviews'
assert_contains references/project-guidance.md 'Feature construction normally stops at two reviews'
assert_contains references/artifact-rules.md 'published runtime ledger values'
assert_contains scripts/check-feature-review.py 'PROJECTED_STABLE_DIGEST = "review-definition-v2"'
assert_contains tests/test_feature_review.py 'test_v2_allows_root_task_runtime_updates_and_plan_rotation'

assert_contains SKILL.md 'Feature Definition Review'
assert_contains SKILL.md 'Implementation Readiness Review'
assert_contains SKILL.md 'authorizes writing the implementation-package artifacts without modifying target implementation'
assert_contains SKILL.md 'A later explicit start may use an unchanged accepted package only after Feature Context, package drift, and stop-condition checks pass.'
assert_contains README.md 'two meaningful reviews'
assert_contains Usage.md 'Feature Definition Review'
assert_contains Usage.md 'Implementation Readiness Review'
assert_contains CHANGELOG.md 'Feature Construction Two-Gate Review'
assert_contains references/validation-scenarios.md 'Feature Construction Two-Gate Review'
assert_contains references/validation-scenarios.md 'Urgency, Human Absence, And Historical Success Do Not Skip Gate 2'
assert_contains references/validation-scenarios.md 'Vague Approve-Everything Cannot Bundle Independent Gates'
assert_contains references/validation-scenarios.md 'Repeated Verification Failure Stops Auto Execution'
assert_contains references/validation-scenarios.md 'Missing Durable Gate Evidence Blocks Resume'
assert_contains references/validation-scenarios.md 'Package Drift Blocks A Later Package-Only Start'
assert_contains references/validation-scenarios.md 'Accepted Multi-Task Plan Rotation Continues Safely'
assert_contains references/validation-scenarios.md 'New Or Drifted Task Cannot Hide As Plan Rotation'

assert_contains references/runtime.md 'Delivery Contract creation and acceptance'
assert_contains references/delivery-contracts.md 'Gate 2 Implementation Readiness Review may authorize exact contract creation and acceptance'
assert_contains references/runtime.md 'subagent dispatch'
assert_contains references/runtime.md 'commit, push, PR, merge, tag, release, publish'

assert_not_contains references/stage-guides.md 'after acceptance, explain that Strict Mode asks before each stage and offer Feature Auto-Loop'

printf 'PASS: Feature construction uses two meaningful reviews without weakening quality or independent hard gates\n'

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
    printf 'FAIL: %s contains removed Feature Gate mechanic: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

h2_section() {
  local file="$1"
  local heading="$2"
  awk -v marker="## ${heading}" '
    $0 == marker { active = 1 }
    active && $0 ~ /^## / && $0 != marker { exit }
    active { print }
  ' "$file"
}

assert_section_contains() {
  local file="$1"
  local heading="$2"
  local text="$3"
  local section
  section=$(h2_section "$file" "$heading")
  if ! grep -Fq -- "$text" <<<"$section"; then
    printf 'FAIL: expected %s section %s to contain %s\n' "$file" "$heading" "$text" >&2
    exit 1
  fi
}

assert_section_not_contains() {
  local file="$1"
  local heading="$2"
  local text="$3"
  local section
  section=$(h2_section "$file" "$heading")
  if grep -Fq -- "$text" <<<"$section"; then
    printf 'FAIL: expected %s section %s not to contain %s\n' "$file" "$heading" "$text" >&2
    exit 1
  fi
}

bounded_text() {
  local file="$1"
  local start_marker="$2"
  local end_marker="$3"
  awk -v start_marker="$start_marker" -v end_marker="$end_marker" '
    index($0, start_marker) { active = 1 }
    active && index($0, end_marker) && !index($0, start_marker) { exit }
    active { print }
  ' "$file"
}

assert_bounded_contains() {
  local file="$1" start_marker="$2" end_marker="$3" text="$4"
  local owner
  owner=$(bounded_text "$file" "$start_marker" "$end_marker")
  if ! grep -Fq -- "$text" <<<"$owner"; then
    printf 'FAIL: expected bounded owner in %s to contain %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_bounded_not_contains() {
  local file="$1" start_marker="$2" end_marker="$3" text="$4"
  local owner
  owner=$(bounded_text "$file" "$start_marker" "$end_marker")
  if grep -Fq -- "$text" <<<"$owner"; then
    printf 'FAIL: expected bounded owner in %s not to contain %s\n' "$file" "$text" >&2
    exit 1
  fi
}

authorities=(
  SKILL.md
  README.md
  Usage.md
  references/design.md
  references/runtime.md
  references/artifact-rules.md
  references/concepts.md
  references/document-templates.md
  references/human-review-summary.md
  references/implementation-planning.md
  references/project-guidance.md
  references/stage-guides.md
  references/validation-scenarios.md
  references/workflow-checklists.md
  templates/notes.md
  templates/root-AGENTS.md
)

for file in "${authorities[@]}" tests/test_feature_review.py; do
  [[ -f "$root/$file" ]] || {
    printf 'FAIL: missing required file: %s\n' "$file" >&2
    exit 1
  }
done

[[ ! -e "$root/scripts/check-feature-review.py" ]] || {
  printf 'FAIL: removed Feature Gate checker still exists\n' >&2
  exit 1
}

removed=(
  'check-feature-review.py'
  'Gate 1 Spec Digest'
  'Gate 2 Package Digest'
  'Gate 2 Stable Files'
  'Gate 2 Stable Digest'
  'EVIDENCE_MATCH'
  'EVIDENCE_CHANGED'
  'EVIDENCE_INVALID'
  'review-definition-v2'
)

for file in "${authorities[@]}"; do
  for text in "${removed[@]}"; do
    assert_not_contains "$file" "$text"
  done
done

assert_contains references/runtime.md 'Gate 1: Feature Definition Review'
assert_contains references/runtime.md 'Gate 2: Implementation Readiness Review'
assert_contains references/runtime.md 'Gate 1 acceptance authorizes package preparation only'
assert_contains references/runtime.md 'does not authorize target implementation'
assert_contains references/runtime.md 'without separate Work Breakdown, Test Design, E2E Discovery, Technical Design, or Plan approval prompts'
assert_contains references/runtime.md 'The Agent verifies the complete implementation package'
assert_contains references/runtime.md 'Gate 2 Package Files'
assert_contains references/runtime.md 'Gate 2 Accepted Stories'
assert_contains references/runtime.md 'Human authorization provenance is an Agent responsibility'
assert_contains references/runtime.md 'Only the two approval choices set `Implementation Readiness: accepted`'
assert_contains references/runtime.md '`Revise package` returns readiness to `preparing`'
assert_contains references/runtime.md '`Pause` does not mark readiness accepted'
assert_contains references/runtime.md 're-read the recorded package files and current Feature artifacts'
assert_contains references/runtime.md 'compare their meaning with the accepted execution boundary'
assert_contains references/runtime.md 'No local script result is required to continue'
assert_contains references/runtime.md 'new Task ID does not by itself repeat Gate 2'

assert_section_contains references/runtime.md 'Human Gate Modes' 'Later Start Decision'
assert_section_contains references/runtime.md 'Human Gate Modes' 'Later Start Authorized At'
assert_section_contains references/runtime.md 'Human Gate Modes' 'Later Start Evidence'
assert_section_contains references/runtime.md 'Human Gate Modes' 'preserving the original Gate 2 review baseline'
assert_section_not_contains references/runtime.md 'Human Gate Modes' 'atomically record Gate 2 Decision `approve-and-start`, Feature Auto-Loop `enabled`, and the timezone-aware start time'

assert_bounded_contains references/runtime.md \
  'Only the two approval choices set `Implementation Readiness: accepted`' \
  'If the human later explicitly says to start implementation after package-only acceptance' \
  '`Approve package only` records accepted readiness and does not execute.'
assert_bounded_not_contains references/runtime.md \
  'Only the two approval choices set `Implementation Readiness: accepted`' \
  'If the human later explicitly says to start implementation after package-only acceptance' \
  'starts target implementation'
assert_bounded_contains references/runtime.md \
  'After the human explicitly says start and those Agent-owned checks pass' \
  'Available control modes:' \
  'Preserve `Gate 2 Decision: package-only`'
assert_bounded_not_contains references/runtime.md \
  'After the human explicitly says start and those Agent-owned checks pass' \
  'Available control modes:' \
  'overwrite'
assert_bounded_not_contains references/runtime.md \
  'After the human explicitly says start and those Agent-owned checks pass' \
  'Available control modes:' \
  'Gate 2 Decision: approve-and-start'

assert_section_contains templates/root-AGENTS.md 'Gate Modes' 'valid separate later-start transition'
assert_section_contains templates/root-AGENTS.md 'Gate Modes' 'preserves the package-only Gate 2 baseline'
assert_section_not_contains templates/root-AGENTS.md 'Gate Modes' 'Gate 2 Decision: approve-and-start'
assert_section_contains templates/project.md 'Current Work' 'Gate Mode: Strict Mode | Feature Auto-Loop | Task Auto-Run'

assert_contains references/stage-guides.md 'Only the two approval choices set `Implementation Readiness: accepted`'
assert_contains references/stage-guides.md '`Revise package` returns readiness to `preparing`'
assert_contains references/stage-guides.md '`Pause` does not mark readiness accepted'
assert_contains references/stage-guides.md 'target implementation is forbidden before Gate 2'
assert_contains references/stage-guides.md 'No local Feature Gate preflight is required'
assert_contains references/workflow-checklists.md 'Only the two approval choices set `Implementation Readiness: accepted`'
assert_contains references/workflow-checklists.md '`Revise package` returns readiness to `preparing`'
assert_contains references/workflow-checklists.md '`Pause` does not mark readiness accepted'
assert_contains references/workflow-checklists.md 'Confirm Feature Gate acceptance and continuation require no local digest or Feature review Checker.'

assert_contains templates/notes.md 'Implementation Readiness: preparing | review-ready | accepted'
assert_contains templates/notes.md 'Gate 2 Package Files'
assert_contains templates/notes.md 'Gate 2 Agent-ready Tasks'
assert_contains templates/notes.md 'Gate 2 Accepted Stories'
assert_contains templates/notes.md 'No-Plan Decision: none | <accepted task ID>'
assert_contains templates/notes.md '| Feature ID | Gate | Classification | Changed Areas | Evidence | Reason | Assessed At |'
assert_contains templates/notes.md 'Later Start Decision: none | approved'
assert_contains templates/notes.md 'Later Start Authorized At: none | <ISO-8601>'
assert_contains templates/notes.md 'Later Start Evidence: none | <Human instruction evidence>'

assert_section_not_contains references/stage-guides.md 'Requirement Checklist' 'Spec SHA-256'
assert_section_contains references/stage-guides.md 'Analyze Consistency' 'Only the two approval choices set `Implementation Readiness: accepted`'
assert_section_contains references/stage-guides.md 'Analyze Consistency' 'no local Feature Gate preflight is required'
assert_section_contains references/runtime.md 'Human Gate Modes' 'Delivery Contract creation and acceptance'
assert_section_contains references/runtime.md 'Human Gate Modes' 'subagent dispatch'
assert_section_contains references/runtime.md 'Human Gate Modes' 'commit, push, PR, merge, tag, release, publish'
assert_section_contains references/runtime.md 'Human Gate Modes' 'Submit / Integrate'
assert_section_contains references/runtime.md 'Human Gate Modes' 'Pause / Close'

assert_contains references/validation-scenarios.md 'Gate 2 Agent-Owned Review Baseline'
assert_contains references/validation-scenarios.md 'Package-Only May Start Later Only When Still Current'
assert_contains references/validation-scenarios.md 'Missing Durable Gate Evidence Blocks Resume'
assert_contains references/validation-scenarios.md 'Package Drift Blocks A Later Package-Only Start'
assert_contains references/validation-scenarios.md 'Accepted Multi-Task Plan Rotation Continues Safely'
assert_contains references/validation-scenarios.md 'New Or Drifted Task Cannot Hide As Plan Rotation'
assert_contains references/validation-scenarios.md 'All Initial Tasks May Be Replaced Inside The Accepted Story'
assert_contains references/validation-scenarios.md 'Duplicate Current Gate Fields Cannot Override Authorization'
assert_contains references/validation-scenarios.md 'No-Plan Structural Binding Does Not Replace AI Judgment'
assert_contains references/validation-scenarios.md 'Human Gate Provenance Stays AI-Owned'
assert_contains references/validation-scenarios.md 'Valid Later Start Uses Direct Agent Review'
assert_contains references/validation-scenarios.md 'Feature Gate Exposes No Local Authorization Issuer'
assert_contains references/validation-scenarios.md 'Agent Owns Complete Package Closure'
assert_contains references/validation-scenarios.md 'Agent Owns One Coherent Package Review'
assert_contains references/validation-scenarios.md 'Pause Clears Current Mode Without Rewriting Gate History'

assert_contains references/runtime.md 'Delivery Contract creation and acceptance'
assert_contains references/runtime.md 'subagent dispatch'
assert_contains references/runtime.md 'commit, push, PR, merge, tag, release, publish'
assert_contains templates/root-AGENTS.md 'Feature construction normally stops at two reviews'
assert_contains references/project-guidance.md 'Feature construction normally stops at two reviews'
assert_not_contains references/stage-guides.md 'after acceptance, explain that Strict Mode asks before each stage and offer Feature Auto-Loop'

printf 'PASS: Feature construction keeps two Human reviews and Agent-owned package/drift checks without a local Feature Gate checker\n'

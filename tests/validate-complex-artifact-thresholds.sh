#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

assert_contains() {
  local file=$1
  local text=$2
  if ! grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s missing required text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_not_contains() {
  local file=$1
  local text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s contains forbidden stale text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_contains "references/complex-artifacts.md" "### Complexity Assessment Trigger"
assert_contains "references/complex-artifacts.md" "When stories > 3, pause and assess whether Complex Artifact Mode is needed"
assert_contains "references/complex-artifacts.md" "Story count does not independently recommend Complex Artifact Mode"
assert_contains "references/complex-artifacts.md" "### Recommendation Semantics"
assert_contains "references/complex-artifacts.md" "牵一发而动全身"
assert_contains "references/complex-artifacts.md" "cannot be safely understood, planned, or verified as one cohesive change"
assert_contains "references/complex-artifacts.md" "multiple collaborating modules, services, workflows, ownership lanes, or release/operation concerns"
assert_contains "references/complex-artifacts.md" "Quantity signals such as many tasks or many test cases are prompts for assessment, not sufficient recommendation triggers"
assert_contains "references/complex-artifacts.md" "Ordinary files within one cohesive module do not justify Complex Artifact Mode"
assert_contains "references/complex-artifacts.md" "Agent may decide whether to recommend Complex Artifact Mode"
assert_contains "references/complex-artifacts.md" "Before creating directories, explain the complex semantics that justify the recommendation"
assert_not_contains "references/complex-artifacts.md" "stories >= 3"
assert_not_contains "references/complex-artifacts.md" "stories >= 5"
assert_not_contains "references/complex-artifacts.md" "tasks >= 8"
assert_not_contains "references/complex-artifacts.md" "test cases >= 10"
assert_not_contains "references/complex-artifacts.md" "Independent Recommendation Triggers"
assert_not_contains "references/complex-artifacts.md" "Combined Recommendation Triggers"
assert_not_contains "references/complex-artifacts.md" "feature spans more than one development day"

assert_contains "references/stage-guides.md" "stories > 3, pause and assess whether Complex Artifact Mode is needed"
assert_contains "references/stage-guides.md" "Do not use story count, task count, test count, or ordinary file count as a hard recommendation trigger"
assert_contains "references/stage-guides.md" "recommend only when the feature is no longer locally understandable or executable inside one cohesive area"
assert_contains "references/stage-guides.md" "propose \`tasks/\`, \`tests/\`, and/or \`plans/\` detail files only for the parts that need detail"
assert_contains "references/stage-guides.md" "detail test-case files under \`tests/\` only when test details need splitting after Complex Artifact confirmation"
assert_contains "references/stage-guides.md" "task detail under \`tasks/US<n>/T<nnn>-<slug>.md\` only when task context needs splitting after Complex Artifact confirmation"
assert_contains "references/stage-guides.md" "if plan detail needs splitting after Complex Artifact confirmation, write the full dated plan to \`plans/\` and keep \`plan.md\` as the current pointer"
assert_not_contains "references/stage-guides.md" "detail test-case files under \`tests/\` when complex artifact mode is triggered"
assert_not_contains "references/stage-guides.md" "update \`task-detail.md\` when complex artifact mode is active"
assert_not_contains "references/stage-guides.md" "if complex artifact mode is active, write the full dated plan to \`plans/\`"
assert_contains "references/large-projects.md" "perform a Complex Artifact assessment"
assert_contains "references/large-projects.md" "Recommend Complex Artifact Mode only when the work spans collaborating modules, services, workflows, ownership lanes, or release/operation concerns"
assert_not_contains "references/large-projects.md" "exceed the trigger conditions, recommend complex artifact mode"
assert_contains "references/workflow-checklists.md" "If stories > 3, pause for a Complex Artifact assessment."
assert_contains "references/workflow-checklists.md" "Do not recommend Complex Artifact Mode from story count, task count, test count, or ordinary file count alone."
assert_contains "references/workflow-checklists.md" "Recommend Complex Artifact Mode only when the feature spans multiple collaborating modules, services, workflows, ownership lanes, or release/operation concerns."
assert_contains "references/workflow-checklists.md" "Create only the \`tasks/\`, \`tests/\`, or \`plans/\` detail directories that are actually needed"
assert_contains "references/workflow-checklists.md" "Load \`complex-artifacts.md\` when stories > 3 or the work appears cross-boundary / hard to scan."

assert_contains "references/validation-scenarios.md" "Complex Artifact Threshold Boundaries"
assert_contains "references/validation-scenarios.md" "four stories inside one cohesive module"
assert_contains "references/validation-scenarios.md" "four stories that are 牵一发而动全身"
assert_contains "references/validation-scenarios.md" "five simple stories still do not automatically recommend Complex Artifact Mode"

assert_contains "references/runtime.md" "Complex Artifact Mode detail directories (\`tasks/\`, \`tests/\`, \`plans/\`) would be created or the feature would switch from simple to complex artifact mode"

printf 'PASS: complex artifact thresholds contract is complete\n'

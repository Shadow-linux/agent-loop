#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
template="$root/templates/root-AGENTS.md"
expected_revision="1.3.0-20260711"

assert_contains() {
  local file=$1
  local text=$2
  if ! grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s missing required text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

if grep '^<!-- agent-loop:managed-start' "$template" | grep -Fvq "block-version:$expected_revision"; then
  printf 'FAIL: every managed block must use same-day-distinguishable revision %s\n' "$expected_revision" >&2
  exit 1
fi

for stage in \
  "Project Skill Creation / Update" \
  "Requirement Archive" \
  "Evidence-Graph + DDD Onboarding" \
  "Decision & Design If Needed" \
  "Product Brief If Needed" \
  "Feature Spec" \
  "Requirement Checklist" \
  "Work Breakdown" \
  "Delivery Contract If Needed" \
  "Test Design" \
  "E2E Discovery If Web" \
  "Technical Design / Code Context" \
  "Plan Gate / Plan If Needed" \
  "Analyze Consistency" \
  "Subagent Execution If Approved" \
  "Execute Task / Story" \
  "Verify" \
  "Review" \
  "Drift Check" \
  "Project Memory Update" \
  "Feature Completion Check" \
  "Submit / Integrate" \
  "Pause / Close"; do
  if ! grep -Fq -- "| $stage |" "$template"; then
    printf 'FAIL: root Workflow Stage Map missing stage: %s\n' "$stage" >&2
    exit 1
  fi
done

assert_contains "references/project-guidance.md" 'Use `block-version:<agent-loop-version>-<YYYYMMDD>[.<same-day-revision>]`'
assert_contains "AGENTS.md" "canonical stage order, routing axes or precedence, root Stage Map signals/references, gate/stop rules, or controller fallback"
assert_contains "AGENTS.md" "update the matching runtime/design source, root Stage Map, project guidance, validation scenarios, and regression tests in the same change"

printf 'PASS: root stage coverage and same-day managed revision are complete\n'

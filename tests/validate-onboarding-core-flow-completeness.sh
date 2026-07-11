#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

assert_file_exists() {
  local path="$1"
  if [[ ! -f "$ROOT/$path" ]]; then
    echo "missing file: $path" >&2
    exit 1
  fi
}

assert_contains() {
  local path="$1"
  local expected="$2"
  if ! grep -Fq "$expected" "$ROOT/$path"; then
    echo "missing text in $path: $expected" >&2
    exit 1
  fi
}

assert_not_contains() {
  local path="$1"
  local forbidden="$2"
  if grep -Fq "$forbidden" "$ROOT/$path"; then
    echo "forbidden text in $path: $forbidden" >&2
    exit 1
  fi
}

assert_file_exists "docs/proposal/v1.3.x/onboarding-core-flow-completeness.md"
assert_file_exists "references/onboarding-knowledge-base.md"
assert_file_exists "templates/onboarding-db/evidence-graph.md"
assert_file_exists "templates/onboarding-db/onboarding-spec.md"
assert_file_exists "templates/onboarding-db/onboarding-tasks.md"
assert_file_exists "templates/onboarding-db/flow.md"
assert_file_exists "templates/onboarding-db/coverage-matrix.md"
assert_file_exists "templates/onboarding-db/batch-review.md"

# Controller and published design/runtime contract.
assert_contains "SKILL.md" "Core Flow Inventory"
assert_contains "SKILL.md" "Flow Slice Coverage"
assert_not_contains "SKILL.md" "wireframe architecture flow diagrams as the preferred flow expression"
assert_contains "references/design.md" "Core Flow Completeness Invariant"
assert_contains "references/design.md" "A missing critical slice cannot be averaged away"
assert_contains "references/runtime.md" "Core Flow Inventory selection"
assert_contains "references/runtime.md" "exactly two onboarding Human Gates"

# Detailed behavior source.
assert_contains "references/onboarding-knowledge-base.md" "## Core Flow Inventory"
assert_contains "references/onboarding-knowledge-base.md" "## Flow Slice Coverage"
assert_contains "references/onboarding-knowledge-base.md" "## Core Flow Diagram Set"
assert_contains "references/onboarding-knowledge-base.md" "## Complexity-Triggered Diagrams"
assert_contains "references/onboarding-knowledge-base.md" "## Completeness Hard Gate"
assert_contains "references/onboarding-knowledge-base.md" "primary per-flow narrative"
assert_contains "references/onboarding-knowledge-base.md" '`critical` / `important`'
assert_contains "references/onboarding-knowledge-base.md" "supporting"
assert_contains "references/onboarding-knowledge-base.md" "stateless"
assert_contains "references/onboarding-knowledge-base.md" "Flow ID"
assert_contains "references/onboarding-knowledge-base.md" "Slice ID"
assert_contains "references/onboarding-knowledge-base.md" "Diagram ID"

# Stage/checklist alignment and no additional batch gate.
assert_contains "references/stage-guides.md" "Build Core Flow Inventory"
assert_contains "references/stage-guides.md" "Completeness Hard Gate"
assert_not_contains "references/stage-guides.md" "before accepting the Onboarding Spec, current batch, or newcomer-ready claim"
assert_contains "references/workflow-checklists.md" "Core Flow Inventory"
assert_contains "references/workflow-checklists.md" "Flow Slice Coverage"
assert_contains "references/workflow-checklists.md" "Complexity-triggered diagrams"
assert_contains "references/workflow-checklists.md" "Completeness Hard Gate"

# Template contracts.
assert_contains "templates/onboarding-db/evidence-graph.md" "## Core Flow Inventory"
assert_contains "templates/onboarding-db/evidence-graph.md" "| Flow ID |"
assert_contains "templates/onboarding-db/evidence-graph.md" "Success Terminal"
assert_contains "templates/onboarding-db/evidence-graph.md" "Failure Terminals"
assert_contains "templates/onboarding-db/evidence-graph.md" "Selection Reason"
assert_contains "templates/onboarding-db/onboarding-spec.md" "## Core Flow Selection"
assert_contains "templates/onboarding-db/onboarding-spec.md" "## Flow Slice Plan"
assert_contains "templates/onboarding-db/onboarding-spec.md" "Complexity Signals"
assert_contains "templates/onboarding-db/onboarding-spec.md" "Covered Slice IDs"
assert_contains "templates/onboarding-db/onboarding-tasks.md" "Required Slice IDs"
assert_contains "templates/onboarding-db/onboarding-tasks.md" "Completeness Hard Gate"
assert_contains "templates/onboarding-db/flow.md" "## 1. Flow Identity And Outcomes"
assert_contains "templates/onboarding-db/flow.md" "## 2. Flow Slice Coverage"
assert_contains "templates/onboarding-db/flow.md" "Diagram ID"
assert_contains "templates/onboarding-db/flow.md" "Covered Slice IDs"
assert_contains "templates/onboarding-db/flow.md" "primary per-flow narrative"
assert_contains "templates/onboarding-db/flow.md" "critical / important flow"
assert_contains "templates/onboarding-db/flow.md" "supporting flow"
assert_contains "templates/onboarding-db/flow.md" "ERD / Model Relationship"
assert_contains "templates/onboarding-db/flow.md" "Runtime / Deployment Topology"
assert_contains "templates/onboarding-db/flow.md" "Observability / Troubleshooting Map"
assert_contains "templates/onboarding-db/coverage-matrix.md" "## Completeness Hard Gate"
assert_contains "templates/onboarding-db/coverage-matrix.md" "Core flow discovery completeness"
assert_contains "templates/onboarding-db/coverage-matrix.md" "Slice and branch coverage"
assert_contains "templates/onboarding-db/coverage-matrix.md" "Evidence granularity"
assert_contains "templates/onboarding-db/coverage-matrix.md" "Consistency / gateway risk"
assert_not_contains "templates/onboarding-db/coverage-matrix.md" "且人类确认新人可读"
assert_contains "templates/onboarding-db/batch-review.md" "## Completeness Hard Gate"
assert_contains "templates/onboarding-db/batch-review.md" "Core flow discovery completeness"
assert_contains "templates/onboarding-db/batch-review.md" "Slice and branch coverage"
assert_contains "templates/onboarding-db/batch-review.md" "Evidence granularity"
assert_contains "templates/onboarding-db/batch-review.md" "Consistency / gateway risk"
assert_not_contains "references/stage-guides.md" "making a newcomer-ready claim"
assert_contains "references/onboarding-knowledge-base.md" "Failure / recovery"
assert_contains "references/onboarding-knowledge-base.md" "Troubleshooting"
assert_not_contains "templates/onboarding-db/onboarding-spec.md" "| Review Gate |"
assert_not_contains "templates/onboarding-db/batch-review.md" "## Human Review Status"

# Semantic pressure scenarios and human-facing behavior.
assert_contains "references/validation-scenarios.md" "missing callback and reconciliation slices"
assert_contains "references/validation-scenarios.md" "diagrams detached from Flow Slice Coverage"
assert_contains "references/validation-scenarios.md" "average away a missing critical slice"
assert_contains "references/validation-scenarios.md" "exactly two onboarding Human Gates"
assert_contains "Usage.md" "核心流程完整性"
assert_contains "Usage.md" "Timeline / Sequence"
assert_contains "CHANGELOG.md" "Core Flow Completeness"

# Executable artifact-level contract.
assert_file_exists "scripts/check-onboarding-core-flow-coverage.rb"
assert_file_exists "examples/ai-meeting-minutes-backend/onboarding-db/08-review/evidence-graph.md"
assert_file_exists "examples/ai-meeting-minutes-backend/onboarding-db/onboarding-spec.md"
assert_file_exists "examples/ai-meeting-minutes-backend/onboarding-db/onboarding-tasks.md"
assert_file_exists "examples/ai-meeting-minutes-backend/onboarding-db/03-flows/order-payment.md"
assert_file_exists "examples/ai-meeting-minutes-backend/onboarding-db/coverage-matrix.md"
assert_file_exists "examples/ai-meeting-minutes-backend/onboarding-db/batch-review.md"
assert_file_exists "tests/fixtures/onboarding-core-flow/invalid-missing-recovery/evidence-graph.md"
assert_file_exists "tests/fixtures/onboarding-core-flow/invalid-missing-recovery/onboarding-spec.md"
assert_file_exists "tests/fixtures/onboarding-core-flow/invalid-missing-recovery/onboarding-tasks.md"
assert_file_exists "tests/fixtures/onboarding-core-flow/invalid-missing-recovery/flow.md"
assert_file_exists "tests/fixtures/onboarding-core-flow/invalid-missing-recovery/coverage-matrix.md"
assert_file_exists "tests/fixtures/onboarding-core-flow/invalid-missing-recovery/batch-review.md"
assert_file_exists "tests/fixtures/onboarding-core-flow/invalid-detached-trace/evidence-graph.md"
assert_file_exists "tests/fixtures/onboarding-core-flow/invalid-detached-trace/onboarding-spec.md"
assert_file_exists "tests/fixtures/onboarding-core-flow/invalid-detached-trace/onboarding-tasks.md"
assert_file_exists "tests/fixtures/onboarding-core-flow/invalid-detached-trace/flow.md"
assert_file_exists "tests/fixtures/onboarding-core-flow/invalid-detached-trace/coverage-matrix.md"
assert_file_exists "tests/fixtures/onboarding-core-flow/invalid-detached-trace/batch-review.md"
assert_file_exists "tests/fixtures/onboarding-core-flow/valid-deferred/evidence-graph.md"
assert_file_exists "tests/fixtures/onboarding-core-flow/valid-deferred/onboarding-spec.md"
assert_file_exists "tests/fixtures/onboarding-core-flow/valid-deferred/onboarding-tasks.md"
assert_file_exists "tests/fixtures/onboarding-core-flow/valid-deferred/coverage-matrix.md"
assert_file_exists "tests/fixtures/onboarding-core-flow/valid-deferred/batch-review.md"

ruby "$ROOT/scripts/check-onboarding-core-flow-coverage.rb" \
  "$ROOT/examples/ai-meeting-minutes-backend/onboarding-db"

invalid_output="$(mktemp)"
trap 'rm -f "$invalid_output"' EXIT
if ruby "$ROOT/scripts/check-onboarding-core-flow-coverage.rb" \
  "$ROOT/tests/fixtures/onboarding-core-flow/invalid-missing-recovery" \
  >"$invalid_output" 2>&1; then
  echo "invalid fixture unexpectedly passed" >&2
  exit 1
fi

if ! grep -Fq "missing required slice: CF-ORDER-PAYMENT/S07" "$invalid_output"; then
  echo "invalid fixture failed for the wrong reason" >&2
  cat "$invalid_output" >&2
  exit 1
fi

detached_output="$(mktemp)"
trap 'rm -f "$invalid_output" "$detached_output"' EXIT
if ruby "$ROOT/scripts/check-onboarding-core-flow-coverage.rb" \
  "$ROOT/tests/fixtures/onboarding-core-flow/invalid-detached-trace" \
  >"$detached_output" 2>&1; then
  echo "detached-trace fixture unexpectedly passed" >&2
  exit 1
fi

if ! grep -Fq "missing diagram definition: D-RECOVERY" "$detached_output"; then
  echo "detached-trace fixture failed for the wrong reason" >&2
  cat "$detached_output" >&2
  exit 1
fi

ruby "$ROOT/scripts/check-onboarding-core-flow-coverage.rb" \
  "$ROOT/tests/fixtures/onboarding-core-flow/valid-deferred"

echo "PASS: onboarding core-flow completeness contract is complete"

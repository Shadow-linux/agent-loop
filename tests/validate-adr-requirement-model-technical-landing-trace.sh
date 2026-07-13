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
    printf 'FAIL: %s contains forbidden text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_file_exists() {
  local file=$1
  if [ ! -f "$root/$file" ]; then
    printf 'FAIL: missing required file: %s\n' "$file" >&2
    exit 1
  fi
}

# Published authority and stage placement.
assert_contains "SKILL.md" "Effective Requirement Snapshot"
assert_contains "SKILL.md" "Requirement Model Technical Landing Trace"
assert_contains "references/design.md" "Effective Requirement Snapshot"
assert_contains "references/runtime.md" "## ADR Requirement Model Technical Landing"
assert_contains "references/runtime.md" "Requirement Model Scope Inventory"
assert_contains "references/runtime.md" 'PERM-*'
assert_contains "references/runtime.md" 'EX-*'
assert_contains "references/runtime.md" 'structural preflight while the ADR is `proposed`'
assert_contains "references/runtime.md" "Upstream Compatibility: current | review-required"
assert_contains "references/runtime.md" 'review-required` is a dependency-availability judgment, not an ADR lifecycle status'
assert_contains "references/project-decisions.md" "## Effective Requirement Snapshot"
assert_contains "references/project-decisions.md" "## Requirement Model Scope Inventory"
assert_contains "references/project-decisions.md" "## Requirement Model Technical Landing Trace"
assert_contains "references/project-decisions.md" "## Coverage Hard Gate"
assert_contains "references/project-decisions.md" "## Upstream Compatibility And Drift"
assert_contains "references/project-decisions.md" "## Triggered Operational Landing"

# Product ownership and acceptance hard stops.
assert_contains "references/project-decisions.md" "ADR must not create, rename, split, merge, or redefine a Concept, relationship, role/permission, command/event, business flow, product state, invariant, exception/recovery meaning, or product fact ownership."
assert_contains "references/project-decisions.md" 'A decision cannot become `accepted` while coverage is missing or Upstream Compatibility is `review-required`.'
assert_contains "references/stage-guides.md" "Decision & Design Human Review Summary"
assert_contains "references/stage-guides.md" "Effective Requirement Snapshot"
assert_contains "references/workflow-checklists.md" "Requirement Model Technical Landing Trace"
assert_contains "references/workflow-checklists.md" "Upstream Compatibility"
assert_contains "references/workflow-checklists.md" "Coverage Hard Gate"
assert_contains "templates/root-AGENTS.md" "Upstream Compatibility"
assert_contains "templates/root-AGENTS.md" "Requirement Model Technical Landing Trace"
assert_contains "references/project-guidance.md" "Requirement Model Technical Landing Trace"

# Human review and generic ADR template.
assert_contains "references/human-review-summary.md" "### Decision & Design Approval"
assert_contains "references/human-review-summary.md" "| Effective Requirement Source |"
assert_contains "references/human-review-summary.md" "| Requirement Model Coverage |"
assert_contains "references/human-review-summary.md" "| Product Semantics Preserved |"
assert_contains "references/human-review-summary.md" "| Migration / Compatibility / Rollout |"
assert_contains "references/human-review-summary.md" "| Design Slice Ownership |"

assert_contains "templates/decision.md" "## Effective Requirement Snapshot"
assert_contains "templates/decision.md" "Effective Concept Source:"
assert_contains "templates/decision.md" "Concept Foundation Status: accepted | concept-foundation-not-needed"
assert_contains "templates/decision.md" "Accepted Concept IDs:"
assert_contains "templates/decision.md" "Accepted Requirement Model IDs:"
assert_contains "templates/decision.md" "Upstream Compatibility: current | review-required"
assert_contains "templates/decision.md" "Last Compatibility Check:"
assert_contains "templates/decision.md" "Trace Applicability: required | not-applicable"
assert_contains "templates/decision.md" "Trace Not-Applicable Reason:"
assert_contains "templates/decision.md" "## Requirement Model Scope Inventory"
assert_contains "templates/decision.md" 'REL-*`, `PERM-*`, `CMD-*`, `EVT-*`, `FLOW-*`, `STATE-*`, `PM-*`, and `EX-*'
assert_contains "templates/decision.md" "## Requirement Model Technical Landing Trace"
assert_contains "templates/decision.md" "| Requirement Model Ref | Accepted Meaning / Constraint | Disposition | Technical Landing | Preserved Invariant | Design Slice | Verification |"
assert_contains "templates/decision.md" "landed | covered-by-accepted-decision | feature-local | not-applicable"
assert_contains "templates/decision.md" "## Coverage Hard Gate"
assert_contains "templates/decision.md" "Every source Requirement Model ID has an explicit scope disposition"
assert_contains "templates/decision.md" "## Human Review Evidence"
assert_contains "templates/decision.md" 'Run the structural validator while the ADR is still `proposed`.'
assert_contains "templates/decision.md" "## Upstream Compatibility And Drift"
assert_contains "templates/decision.md" "## Operational Landing Trigger Assessment"
assert_contains "templates/decision.md" "triggered | not-triggered"

# Human docs and pressure scenarios.
assert_contains "README.md" "Requirement Model Technical Landing Trace"
assert_contains "Usage.md" "Effective Requirement Snapshot"
assert_contains "CHANGELOG.md" "Requirement Model Technical Landing Trace"
assert_contains "references/validation-scenarios.md" "ADR Requirement Model Technical Landing Trace"
assert_contains "references/validation-scenarios.md" "Stale Effective Requirement Snapshot Blocks ADR"
assert_contains "references/validation-scenarios.md" "Incomplete Landing Coverage Blocks Feature Spec"
assert_contains "references/validation-scenarios.md" "Accepted ADR Meaning Requires Supersede"
assert_contains "references/validation-scenarios.md" "Operational Landing Is Triggered, Not Default"

# Scope exclusions: no stage, status, default mapping artifact, executable schema, or target-project workspace.
ruby -e '
  content = File.read(ARGV.fetch(0))
  section = content[/## Stage Order\n(.*?)(?=\n## |\z)/m, 1]
  abort "FAIL: runtime Stage Order section missing" unless section
  forbidden = ["Effective Requirement Snapshot", "Requirement Model Technical Landing Trace", "Coverage Hard Gate", "Upstream Compatibility Review"]
  found = forbidden.select { |name| section.lines.any? { |line| line.strip == name } }
  abort "FAIL: ADR trace concepts must not become canonical stages: #{found.join(", ")}" unless found.empty?
' "$root/references/runtime.md"
assert_contains "templates/decision.md" "Allowed Status: proposed | accepted | superseded | deprecated"
assert_not_contains "templates/decision.md" "Allowed Status: proposed | accepted | review-required"
assert_not_contains "references/project-decisions.md" ".agent-loop/requirement-model-mappings/"
assert_not_contains "templates/decision.md" "technical-landing.yaml"
assert_not_contains "templates/decision.md" "technical-landing.json"
if [ -e "$root/.agent-loop" ]; then
  printf 'FAIL: skill source repository must not contain target-project .agent-loop artifacts\n' >&2
  exit 1
fi

# The generic template and validator must not learn fixture-specific business/action/technology values.
for forbidden in FixtureSubject FixtureOperator perform_fixture_action FixtureStore FixtureProtocol; do
  assert_not_contains "templates/decision.md" "$forbidden"
  assert_not_contains "scripts/check-adr-requirement-model-trace.py" "$forbidden"
done

# Behavioral validation, not keyword-only assertions.
assert_file_exists "scripts/check-adr-requirement-model-trace.py"
valid="$root/tests/fixtures/adr-technical-landing/valid"
python3 "$root/scripts/check-adr-requirement-model-trace.py" "$valid/README.md" "$valid/requirement.md" "$valid/decision.md"
(cd "$root" && python3 -m unittest tests/test_adr_requirement_model_trace.py)

not_needed="$root/tests/fixtures/adr-technical-landing/valid-not-needed"
python3 "$root/scripts/check-adr-requirement-model-trace.py" "$not_needed/README.md" "$not_needed/requirement.md" "$not_needed/decision.md"

if python3 "$root/scripts/check-adr-requirement-model-trace.py" "$valid/README.md" "$valid/requirement.md" "$root/tests/fixtures/adr-technical-landing/invalid-missing-coverage/decision.md" >/dev/null 2>&1; then
  printf 'FAIL: missing-coverage ADR fixture unexpectedly passed\n' >&2
  exit 1
fi

if python3 "$root/scripts/check-adr-requirement-model-trace.py" "$valid/README.md" "$valid/requirement.md" "$root/tests/fixtures/adr-technical-landing/invalid-empty-landing/decision.md" >/dev/null 2>&1; then
  printf 'FAIL: empty-landing ADR fixture unexpectedly passed\n' >&2
  exit 1
fi

unaccepted="$root/tests/fixtures/adr-technical-landing/invalid-unaccepted-source"
if python3 "$root/scripts/check-adr-requirement-model-trace.py" "$unaccepted/README.md" "$unaccepted/requirement.md" "$valid/decision.md" >/dev/null 2>&1; then
  printf 'FAIL: unaccepted-source ADR fixture unexpectedly passed\n' >&2
  exit 1
fi

reopened="$root/tests/fixtures/adr-technical-landing/invalid-reopened-source"
if python3 "$root/scripts/check-adr-requirement-model-trace.py" "$reopened/README.md" "$reopened/requirement.md" "$valid/decision.md" >/dev/null 2>&1; then
  printf 'FAIL: reopened-source ADR fixture unexpectedly passed\n' >&2
  exit 1
fi

if python3 "$root/scripts/check-adr-requirement-model-trace.py" "$valid/README.md" "$valid/requirement.md" "$root/tests/fixtures/adr-technical-landing/invalid-review-required/decision.md" >/dev/null 2>&1; then
  printf 'FAIL: review-required ADR fixture unexpectedly passed\n' >&2
  exit 1
fi

printf 'PASS: ADR Requirement Model Technical Landing Trace contract is complete\n'

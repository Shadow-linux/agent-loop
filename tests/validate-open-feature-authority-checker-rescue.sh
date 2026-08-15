#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
failures=0

assert_contains() {
  local file=$1 text=$2
  if ! grep -Fq -- "$text" "$root/$file"; then
    printf 'RED: %s missing required text: %s\n' "$file" "$text" >&2
    failures=$((failures + 1))
  fi
}

assert_not_contains() {
  local file=$1 text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    printf 'RED: %s contains stale or forbidden text: %s\n' "$file" "$text" >&2
    failures=$((failures + 1))
  fi
}

assert_not_in_runtime_surfaces() {
  local text=$1
  if grep -RFq --include='*.md' -- "$text" \
    "$root/SKILL.md" "$root/references" "$root/templates"; then
    printf 'FAIL: runtime/template surfaces contain forbidden Rescue contract: %s\n' "$text" >&2
    failures=$((failures + 1))
  fi
}

for file in \
  scripts/feature_authority_support.py \
  scripts/check-feature-context.py \
  templates/spec.md \
  templates/feature-context.md \
  references/runtime.md \
  references/design.md \
  references/checker-recovery.md \
  references/human-review-summary.md \
  references/validation-scenarios.md
do
  if [[ ! -f "$root/$file" ]]; then
    printf 'RED: missing required file: %s\n' "$file" >&2
    failures=$((failures + 1))
  fi
done

assert_contains templates/spec.md '## Feature Authority'
assert_contains templates/spec.md 'Authority Type:'
assert_contains templates/spec.md 'Primary Authority Reference:'
assert_contains templates/spec.md 'Supporting Authority References:'
assert_contains templates/spec.md 'Agent Authority Assessment: current | changed | unresolved'
assert_contains templates/spec.md 'Requirement Product Definition sub-adapter'
assert_contains templates/spec.md \
  'An explicit Requirement Product Definition primary authority must identify the same Requirement Set README; applicable ADRs and contracts remain supporting evidence.'
assert_contains references/document-templates.md \
  'An explicit Requirement Product Definition primary authority must identify the same Requirement Set README; applicable ADRs and contracts remain supporting evidence.'
assert_contains references/stage-guides.md \
  'An explicit Requirement Product Definition primary authority must identify the same Requirement Set README; applicable ADRs and contracts remain supporting evidence.'
assert_contains templates/feature-context.md 'Authority Type:'
assert_contains templates/feature-context.md 'Primary Authority Reference:'
assert_contains templates/feature-context.md 'Authority Applicability:'
assert_contains templates/spec.md 'resolver-emitted facts in deterministic semicolon-separated order, including Authority Summary'
assert_contains references/runtime.md 'Equivalent project-relative spelling or a safe internal symlink to that same file is one authority, not a conflict.'
assert_contains references/design.md '`Authority Facts` is a deterministic semicolon-separated mirror of the resolver output'
assert_contains scripts/check-feature-context.py 'Snapshot Authority Facts differ from resolved authority facts'
if grep -Fq -- 'Authority Adapter: feature | bug | human | custom' \
  "$root/templates/spec.md" "$root/templates/feature-context.md"; then
  printf 'FAIL: Feature Context template presents adapter families as a closed enum\n' >&2
  failures=$((failures + 1))
fi

assert_contains references/runtime.md 'Feature Authority'
assert_contains references/runtime.md 'Bug Authority'
assert_contains references/runtime.md 'Human Authority'
assert_contains references/runtime.md 'unknown but inspectable'
assert_contains references/runtime.md 'NOT_APPLICABLE'
assert_contains references/runtime.md '## Agent Checker Rescue'
assert_contains references/runtime.md 'Level 1 — Agent automatic rescue'
assert_contains references/runtime.md 'Level 2 — Human one-Gate substitute'
assert_contains references/runtime.md 'Level 3 — non-rescuable'
assert_contains references/runtime.md 'exact canonical failure and one exact rerun'
assert_contains references/runtime.md 'continue-within-existing-authorization'
assert_contains references/runtime.md 'accepted-for-this-gate'
assert_contains references/runtime.md 'does not change the canonical result to `PASS`'
assert_contains references/runtime.md 'Checker Self-Repair'

assert_contains references/design.md 'Authority Type remains descriptive metadata'
assert_contains references/design.md 'Requirement Product Definition'
assert_contains references/design.md 'NOT_APPLICABLE'
assert_contains references/design.md '**Feature Context Snapshot**: an authority-neutral'
assert_contains references/design.md 'Agent Checker Rescue'
assert_contains references/checker-recovery.md 'Agent Checker Rescue'
assert_contains references/checker-recovery.md 'corrected executable Checker'
assert_contains references/checker-recovery.md 'Canonical validation: failed'
assert_contains references/checker-recovery.md 'accepted-for-this-gate'
assert_contains references/checker-recovery.md 'Issue Reporting Human Gate'
assert_contains references/human-review-summary.md 'Agent Rescue Decision'
assert_contains references/human-review-summary.md 'Residual Risk'
assert_contains references/human-review-summary.md 'Expiry'

assert_contains references/validation-scenarios.md 'Agent Checker Rescue Level 1'
assert_contains references/validation-scenarios.md 'Agent Checker Rescue Level 2'
assert_contains references/validation-scenarios.md 'Agent Checker Rescue Level 3'
assert_contains references/validation-scenarios.md 'checker/command/target/input/authority/evidence'
assert_contains references/validation-scenarios.md 'missing existing Human authorization'
assert_contains references/validation-scenarios.md 'Sanitized Checker Feedback'
assert_contains references/validation-scenarios.md 'Equivalent Requirement Authority Paths Preserve One Primary Authority'
assert_contains references/validation-scenarios.md 'Authority Summary Or Snapshot Facts Cannot Stay Stale'
assert_contains references/validation-scenarios.md 'Lowercase External Ticket Is Evidence, Not A Local File Guess'
assert_contains references/validation-scenarios.md 'Applicable Specialized Checker Reports Readable Structural Drift'

assert_contains scripts/check-feature-context.py 'NOT_APPLICABLE'
assert_contains scripts/check-requirement-product-definition.py 'NOT_APPLICABLE'
assert_contains scripts/check-concept-foundation-trace.py 'NOT_APPLICABLE'
assert_contains SKILL.md 'open Feature authority'
assert_contains templates/root-AGENTS.md 'Agent Checker Rescue'
assert_contains templates/root-AGENTS.md 'Checker Self-Repair'
assert_contains docs/proposal/v1.5.x/open-feature-authority-and-agent-owned-checker-light-gates.md \
  '**Status:** implemented, validated, and released as `stable-v1.5.4`'
assert_contains docs/proposal/v1.5.x/open-feature-authority-and-agent-owned-checker-light-gates-implementation-plan.md \
  '**Status:** Phase 1 and Phase 2 Human Review accepted; implementation, validation, and `stable-v1.5.4` release complete'
assert_contains docs/proposal/v1.5.x/open-feature-authority-and-agent-owned-checker-light-gates-implementation-plan.md \
  'Implementation, both Phase Human Reviews, and the exact `v1.5.4` Release Gate were accepted by subsequent Human instructions.'
assert_not_contains docs/proposal/v1.5.x/open-feature-authority-and-agent-owned-checker-light-gates-implementation-plan.md \
  'This document is the only implementation artifact authorized by the current instruction.'

if [[ ! -x "$root/scripts/check-onboarding-core-flow-coverage.py" ]]; then
  printf 'RED: scripts/check-onboarding-core-flow-coverage.py must remain directly executable\n' >&2
  failures=$((failures + 1))
fi

for forbidden in \
  '.agent-loop/checker-exceptions/' \
  '.agent-loop/checker-feedback/' \
  'Rescue Status: PASS' \
  'Agent Rescue Decision: PASS' \
  'Rescue Authorization:' \
  'Status: rescued' \
  'Auto Mode: rescue' \
  '## Agent Checker Rescue Gate' \
  '--force-checker' \
  '--skip-checker'
do
  assert_not_in_runtime_surfaces "$forbidden"
done

if (( failures > 0 )); then
  printf 'RED: open Feature authority / Agent Checker Rescue contract has %s unmet assertions\n' "$failures" >&2
  exit 1
fi

printf 'PASS: open Feature authority, specialized applicability, and three-level Agent Checker Rescue contract is complete\n'

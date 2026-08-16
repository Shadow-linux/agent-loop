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
  local file=$1 text=$2
  grep -Fq -- "$text" "$root/$file" || fail "$file missing Progressive Verification contract: $text"
}

assert_not_contains() {
  local file=$1 text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    fail "$file contains forbidden Progressive Verification behavior: $text"
  fi
}

for file in \
  SKILL.md \
  references/runtime.md \
  references/design.md \
  references/stage-guides.md \
  references/concepts.md \
  references/document-templates.md \
  references/validation-scenarios.md \
  references/human-review-summary.md \
  references/workflow-checklists.md \
  templates/tests.md \
  templates/notes.md \
  templates/root-AGENTS.md; do
  assert_file "$file"
done

# --- Feature Verification Profile: definition surfaces ---

trio='focused | full | high-assurance'
assert_contains references/runtime.md "$trio"
assert_contains references/design.md "$trio"
assert_contains references/concepts.md "$trio"
assert_contains SKILL.md "$trio"
assert_contains templates/root-AGENTS.md "$trio"

assert_contains references/runtime.md '## Feature Verification Profile'
assert_contains references/runtime.md 'not a canonical stage, message intent, status, Mode, Gate, Checker result, or artifact family'
assert_contains references/runtime.md 'never governs Lightweight Change Lane or Review Repair Fast Path'

assert_contains references/design.md '**Feature Verification Profile**'
assert_contains references/design.md '**Proof First**'
assert_contains references/design.md 'the recorded, auditable application of Adaptive Depth inside the Feature lane'

assert_contains references/concepts.md 'they are not Modes, stages, statuses, lifecycles, or Gates, and they are distinct from Strict Mode (stage-by-stage control) and from Standard Product Definition depth (`brief | standard`)'

# --- decision point and persistence ---

assert_contains references/runtime.md 'first records the Feature Verification Profile with rationale and hard-floor check'
assert_contains references/runtime.md '`Verification Profile`; `Profile Rationale`'
assert_contains references/runtime.md '`Profile Floor` naming applicable hard-floor categories; `Escalation Triggers` listing the Feature-specific trigger subset'
assert_contains references/runtime.md 'optional `Profile Recomputed At`'
assert_contains references/runtime.md 'the recorded Feature Verification Profile fields, Story/Task/Plan bindings'

assert_contains references/stage-guides.md 'Package preparation first records the Feature Verification Profile tier with rationale, hard-floor check, and escalation triggers'
assert_contains references/stage-guides.md 'Gate 2 presents the Profile tier, rationale, applicable hard floor, and escalation triggers as part of the Verification decision row'
assert_contains references/runtime.md 'list the recorded Feature Verification Profile tier, rationale, applicable hard floor, and escalation triggers'

assert_contains references/runtime.md 'A tier raise re-binds the consuming package before work continues: refresh the affected Test Design, Plan verification/rollback coverage, and regression scope to the new tier'
assert_contains references/runtime.md 'Existing Feature notes without Profile fields remain reader-compatible (pre-1.5.7 Features)'
assert_contains references/runtime.md 'treat the effective tier as `full`, check the hard-floor categories from current artifacts immediately'
assert_contains references/runtime.md 'never backfill them into history'
assert_contains references/implementation-planning.md 'it scales Plan breadth, never exactness'
assert_contains references/workflow-checklists.md 'Scale Plan breadth by the recorded Feature Verification Profile tier'
assert_contains references/workflow-checklists.md 'A `high-assurance` Feature allows No-Plan only for documentation-only tasks'
assert_contains references/lightweight-change-lane.md 'public API, event, schema, persistence, product data, state flow, permission, security, credential, or trust-boundary change'

assert_contains references/workflow-checklists.md 'Scale Plan breadth by the recorded Feature Verification Profile tier (`focused | full | high-assurance`)'
assert_not_contains references/workflow-checklists.md 'standard/high-assurance'

# cross-surface floor anchors: shared safety categories stay pinned in both surfaces
assert_contains references/runtime.md 'auth, permission, payment, data deletion, data schema, migration, public API, security-sensitive code, or cross-module core logic'
assert_contains references/runtime.md 'The shared lexical anchors pinned in both lists are permission, schema, public API, migration, and cross-module'
for anchor in permission schema 'public API' migration cross-module; do
  assert_contains references/runtime.md "$anchor"
  assert_contains references/lightweight-change-lane.md "$anchor"
done

# anti-semantic guards: known-dangerous contradictory phrasings must not appear
for file in SKILL.md references/runtime.md references/design.md references/stage-guides.md references/implementation-planning.md; do
  assert_not_contains "$file" 'may ignore Existing Test Obligations'
  assert_not_contains "$file" 'Existing Test Obligations are optional'
  assert_not_contains "$file" 'Profile tier does not apply'
  assert_not_contains "$file" 'without re-running'
done

# --- execution/verification stage coverage and helper boundary ---

assert_contains references/stage-guides.md 'Profile tier scales breakdown breadth'
assert_contains references/stage-guides.md 'Profile tier scales Plan breadth, never its exactness'
assert_contains references/stage-guides.md 'Profile tier scales review depth'
assert_contains references/stage-guides.md 'a `high-assurance` Feature allows No-Plan Decisions only for documentation-only tasks; behavior-affecting tasks always require an accepted plan'
assert_contains references/stage-guides.md 'during execution, watch the recorded Feature Verification Profile escalation triggers'
assert_contains references/stage-guides.md 'during verification, recheck the recorded Feature Verification Profile escalation triggers'
assert_contains references/stage-guides.md 'a reproduction script with failure output, or API/UI reproduction evidence, and a new test is never manufactured solely for RED'
assert_contains references/skill-routing.md 'Proof First applies inside the loaded TDD helper as well'
assert_contains references/skill-routing.md "Helper defaults never override the controller's artifact, gate, or evidence rules"

# --- hard floors ---

assert_contains references/runtime.md 'can never be rated below `high-assurance`, regardless of Agent self-assessment'
assert_contains references/runtime.md 'Keep this floor list aligned with the Lightweight Change Assessment Feature hard triggers: when either list changes, update both in the same change'

# --- escalation and time-bounded movement ---

assert_contains references/runtime.md 'Escalation during execution is automatic and must be recorded in Feature `notes.md`'
assert_contains references/runtime.md 'auth/permission contact, public API or schema change, weak Test Oracle (which also redoes the affected Test Design part before continuing), and unknown regression failure raise the tier directly to `high-assurance`'
assert_contains references/runtime.md 'the `## Profile Escalation Log` table'
assert_contains references/runtime.md 'after Gate 2 acceptance, the Agent may only auto-escalate during execution, and any downgrade requires presenting the changed risk evidence to the Human'
assert_contains references/runtime.md 'before Gate 2 acceptance, the Agent may recompute the Profile from new evidence, including a reasoned downgrade'
assert_contains references/runtime.md 'It must stop before a Feature Verification Profile downgrade after Gate 2 that lacks a recorded Human acceptance'

# --- notes.md template persistence (both template surfaces) ---

for file in templates/notes.md references/document-templates.md; do
  assert_contains "$file" 'Verification Profile: pending | focused | full | high-assurance'
  assert_contains "$file" 'Profile Rationale: pending | <risk judgment citing concrete evidence>'
  assert_contains "$file" 'Profile Floor: none | <applicable hard-floor categories>'
  assert_contains "$file" 'Escalation Triggers: <Feature-specific trigger subset>'
  assert_contains "$file" 'Profile Recomputed At: none | <ISO-8601, only before Gate 2 acceptance>'
  assert_contains "$file" '## Profile Escalation Log'
  assert_contains "$file" '| Trigger | Old Tier | New Tier | Evidence | Recorded At |'
done

# unified Gate 2 presentation wording; the divergent short form must not survive
for file in references/runtime.md references/stage-guides.md references/validation-scenarios.md templates/root-AGENTS.md; do
  assert_not_contains "$file" 'presents the Profile row'
done

# --- Gate 2 human-facing presentation ---

assert_contains references/human-review-summary.md 'recorded Verification Profile (`focused | full | high-assurance`) with rationale, applicable hard floor, and escalation triggers'
assert_contains references/workflow-checklists.md 'the recorded Feature Verification Profile fields with hard-floor check'
assert_contains references/runtime.md 'Gate 2 presents the Profile fields in the Verification decision row'
assert_contains templates/root-AGENTS.md 'Gate 2 shows the Profile fields in the Verification decision row'
assert_contains templates/root-AGENTS.md 'a post-Gate 2 downgrade requires presented changed-risk evidence and Human acceptance'
assert_contains SKILL.md 'a post-Gate 2 downgrade requires presented changed-risk evidence plus recorded Human acceptance'
assert_contains SKILL.md 'Hard floors are never lowered by human urgency, acceptance, or responsibility claims'

# --- pressure-test hardening (A1/A3/A4/A5/A7/A9/A10) ---

assert_contains references/runtime.md 'Floor contact is operational, not impressionistic: contact means any write to, or a new runtime dependency on, a module, file, or configuration that owns a hard-floor category; read-only inspection never counts as contact'
assert_contains references/runtime.md 'Ambiguous contact is treated as contact'
assert_contains references/runtime.md 'Human acceptance, urgency, or responsibility claims never rate work below an applicable hard floor; only a changed floor-category fact'
assert_contains references/runtime.md 'Multiple simultaneous triggers record one Profile Escalation Log row per trigger and converge on the highest resulting tier'
assert_contains references/runtime.md 'A `high-assurance` Feature allows No-Plan Decisions only for documentation-only tasks'
assert_contains references/runtime.md 'the Profile recording itself remains an Agent-owned automatic record presented at Gate 2'
assert_contains references/runtime.md 'RED proof must be reproduced against the current code state before implementation'
assert_contains references/runtime.md 'a historical failure log alone is Bug intake evidence, not RED'
assert_contains references/design.md 'RED proof must be re-executed against the current code state before implementation'
assert_contains references/stage-guides.md 'A repair that contacts an applicable Feature Verification Profile hard-floor category is not an ordinary within-boundary correction: it exits the Fast Path'

# --- Proof First ---

assert_contains references/runtime.md 'Proof First widens only the RED evidence definition and never renames or bypasses TDD'
assert_contains references/runtime.md 'an existing test'"'"'s failing run, a reproduction script with its failure output, or API/UI reproduction evidence'
assert_contains references/runtime.md 'A new test is never manufactured solely to produce RED'
assert_contains references/runtime.md 'explicit Bug repair prefers Reproduction First, where the original reproduction satisfies RED'
assert_contains references/runtime.md 'Required Verification, Existing Test Obligations, and the Bug Verification Matrix regression/safety columns are unchanged'
assert_contains SKILL.md 'Proof First widens only the RED evidence definition'

# --- tests.md template sections ---

assert_contains templates/tests.md '## Core Invariants'
assert_contains templates/tests.md '| Invariant ID | Invariant | Source (Spec / Requirement / ADR) | Verified By |'
assert_contains templates/tests.md '## Test Oracle'
assert_contains templates/tests.md '| Case | Expected (Oracle) | Oracle Source | Oracle Quality Check |'
assert_contains references/document-templates.md '## Core Invariants'
assert_contains references/document-templates.md '## Test Oracle'
assert_contains references/stage-guides.md 'Core Invariants table: one row per stable invariant'
assert_contains references/stage-guides.md 'Test Oracle table: expected result per case with its oracle source and an oracle quality check'

# --- root guidance blocks ---

assert_contains templates/root-AGENTS.md 'Package preparation first records the Feature Verification Profile'
assert_contains templates/root-AGENTS.md 'RED accepts any credible failure-matched proof'

# --- rejected directions stay rejected ---

for file in SKILL.md references/runtime.md references/design.md references/stage-guides.md references/concepts.md; do
  assert_not_contains "$file" 'evidence.json'
  assert_not_contains "$file" 'run.jsonl'
  assert_not_contains "$file" 'FAST | NORMAL | STRICT'
done

# --- scenarios ---

for scenario in \
  'Tier Raise Re-binds The Package' \
  'Legacy Feature Defaults To Full' \
  'Profile Recorded After Gate 1' \
  'Hard Floor Blocks Agent Downgrade' \
  'Execution Auto-Escalates With Evidence' \
  'Direct Escalation Triggers Jump To High Assurance' \
  'Post-Gate-2 Downgrade Returns To Human' \
  'Bug Reproduction Satisfies RED' \
  'API Or UI Evidence Counts As RED' \
  'Stale Failure Log Is Not RED' \
  'Review Repair Floor Contact Exits Fast Path' \
  'Focused Profile Does Not Govern Other Lanes' \
  'Profile Is Not A New Stage Or Mode'; do
  assert_contains references/validation-scenarios.md "### $scenario"
done
assert_contains references/validation-scenarios.md '## 83. Progressive Verification + Proof First'

# --- version sync ---

assert_contains SKILL.md 'Version: 1.5.7'
assert_contains plugin.json '"version": "1.5.7"'
assert_contains README.md '**Current version:** 1.5.7'
assert_contains Usage.md '**版本：** 1.5.7'
assert_contains CHANGELOG.md '## 1.5.7 — 2026-08-15'

ruby - "$root/templates/root-AGENTS.md" <<'RUBY'
content = File.read(ARGV.fetch(0))
blocks = content.scan(/<!-- agent-loop:managed-start section:([^ ]+) .*?block-version:([^ ]+) -->/)
abort "FAIL: expected 13 root managed blocks, found #{blocks.length}" unless blocks.length == 13
blocks.each do |section, revision|
  expected = '1.5.7-20260815.1'
  abort "FAIL: #{section} expected #{expected}, found #{revision}" unless revision == expected
end
abort 'FAIL: root AGENTS exceeds 190 lines' if content.lines.length > 190
RUBY

[ ! -d "$root/.agent-loop" ] || fail 'source repository must not contain target-project .agent-loop artifacts'

# --- mutation tests: semantic corruptions of the source must break this contract ---

build_sandbox() {
  local dir=$1
  rm -rf "$dir"
  mkdir -p "$dir/references" "$dir/templates" "$dir/tests"
  cp "$root/SKILL.md" "$root/plugin.json" "$root/README.md" "$root/Usage.md" "$root/CHANGELOG.md" "$dir/"
  local f
  for f in runtime design stage-guides concepts document-templates validation-scenarios human-review-summary workflow-checklists skill-routing implementation-planning lightweight-change-lane; do
    cp "$root/references/$f.md" "$dir/references/"
  done
  for f in tests notes root-AGENTS; do
    cp "$root/templates/$f.md" "$dir/templates/"
  done
  cp "$root/tests/validate-progressive-verification.sh" "$dir/tests/"
  sed -i '' '/^# --- mutation tests/,$d' "$dir/tests/validate-progressive-verification.sh"
}

control_sandbox=$(mktemp -d)
build_sandbox "$control_sandbox"
if ! bash "$control_sandbox/tests/validate-progressive-verification.sh" >/dev/null 2>&1; then
  rm -rf "$control_sandbox"
  fail 'mutation harness control failed: unmutated sandbox must pass'
fi
rm -rf "$control_sandbox"

run_mutation() {
  local name=$1 file=$2 expr=$3
  local sb
  sb=$(mktemp -d)
  build_sandbox "$sb"
  sed -i '' "$expr" "$sb/$file" || { rm -rf "$sb"; fail "mutation $name: sed failed"; }
  if bash "$sb/tests/validate-progressive-verification.sh" >/dev/null 2>&1; then
    rm -rf "$sb"
    fail "mutation $name was NOT caught by the contract"
  fi
  rm -rf "$sb"
}

run_mutation 'direct-escalation-downgraded-to-one-step' references/runtime.md 's|raise the tier directly to `high-assurance`|raise the tier one step|'
run_mutation 'hard-floor-removed' references/runtime.md 's|can never be rated below `high-assurance`|may be rated `focused` when the diff is small|'
run_mutation 'stale-log-accepted-as-red' references/runtime.md 's|RED proof must be reproduced against the current code state before implementation|RED proof may be any historical failure log|'
run_mutation 'notes-profile-field-deleted' templates/notes.md '/Verification Profile: pending/d'
run_mutation 'tier-difference-removed-from-plan' references/stage-guides.md 's|Profile tier scales Plan breadth, never its exactness|Profile tier does not affect Plan content|'
run_mutation 'tier-difference-removed-from-breakdown' references/stage-guides.md 's|Profile tier scales breakdown breadth|Profile tier does not affect breakdown|'
run_mutation 'tier-difference-removed-from-review' references/stage-guides.md 's|Profile tier scales review depth|Profile tier does not affect review depth|'
run_mutation 'noplan-sync-removed' references/stage-guides.md '/a `high-assurance` Feature allows No-Plan Decisions only for documentation-only tasks/d'
run_mutation 'exclusion-flipped' references/runtime.md 's|it never governs Lightweight Change Lane or Review Repair Fast Path|it always governs Lightweight Change Lane and Review Repair Fast Path|'
run_mutation 'rebind-removed' references/runtime.md 's|A tier raise re-binds the consuming package before work continues|A tier raise only records the new tier and work continues unchanged|'
run_mutation 'legacy-default-lowered' references/runtime.md 's|treat the effective tier as `full`|treat the effective tier as `focused`|'
run_mutation 'plan-owner-sync-removed' references/implementation-planning.md '/the recorded Feature Verification Profile tier: it scales Plan breadth, never exactness/d'
run_mutation 'lightweight-permission-trigger-deleted' references/lightweight-change-lane.md 's|public API, event, schema, persistence, product data, state flow, permission, security, credential, or trust-boundary change|public API, event, schema, persistence, product data, state flow, security, credential, or trust-boundary change|'
run_mutation 'checklist-tier-name-corrupted' references/workflow-checklists.md 's#(`focused | full | high-assurance`)#(focused/standard/high-assurance)#'
run_mutation 'floor-anchor-removed-from-runtime' references/runtime.md 's|data schema, migration, public API|public API|'

printf 'PASS: Progressive Verification + Proof First contract is complete\n'

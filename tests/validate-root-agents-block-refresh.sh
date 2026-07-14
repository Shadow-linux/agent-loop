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
    printf 'FAIL: %s contains retired text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

managed_count=$(grep -c '^<!-- agent-loop:managed-start' "$root/templates/root-AGENTS.md" || true)
block_version_count=$(grep -c '^<!-- agent-loop:managed-start.*block-version:' "$root/templates/root-AGENTS.md" || true)
current_block_version="1.3.0-20260714.1"

if [ "$managed_count" -ne "$block_version_count" ]; then
  printf 'FAIL: every root AGENTS managed block needs block-version (%s managed, %s block-version)\n' "$managed_count" "$block_version_count" >&2
  exit 1
fi

if grep '^<!-- agent-loop:managed-start' "$root/templates/root-AGENTS.md" | grep -Fvq "block-version:$current_block_version"; then
  printf 'FAIL: every root AGENTS managed block must use current full block-version: %s\n' "$current_block_version" >&2
  grep '^<!-- agent-loop:managed-start' "$root/templates/root-AGENTS.md" | grep -Fv "block-version:$current_block_version" >&2 || true
  exit 1
fi

bootstrap_line=$(grep -n '^<!-- agent-loop:managed-start section:bootstrap ' "$root/templates/root-AGENTS.md" | cut -d: -f1)
ownership_line=$(grep -n '^<!-- agent-loop:managed-start section:ownership ' "$root/templates/root-AGENTS.md" | cut -d: -f1)
message_intent_line=$(grep -n '^<!-- agent-loop:managed-start section:message-intent ' "$root/templates/root-AGENTS.md" | cut -d: -f1)
workflow_stage_map_line=$(grep -n '^<!-- agent-loop:managed-start section:workflow-stage-map ' "$root/templates/root-AGENTS.md" | cut -d: -f1)

if ! [ "$bootstrap_line" -lt "$ownership_line" ] ||
   ! [ "$ownership_line" -lt "$message_intent_line" ] ||
   ! [ "$message_intent_line" -lt "$workflow_stage_map_line" ]; then
  printf 'FAIL: root AGENTS startup order must be Bootstrap -> Agent Ownership -> Message Intent -> Workflow Stage Map\n' >&2
  exit 1
fi

assert_contains "AGENTS.md" 'Treat changes to canonical stage order, routing axes or precedence, root Stage Map signals/references, gate/stop rules, or controller fallback as coordinated workflow changes.'
assert_contains "AGENTS.md" 'update the matching runtime/design source, root Stage Map, project guidance, validation scenarios, and regression tests in the same change'
assert_not_contains "AGENTS.md" 'section:meta'
assert_not_contains "AGENTS.md" 'visible natural-language synced-version text'

assert_not_contains "templates/root-AGENTS.md" "## Managed Block Rule"
assert_not_contains "templates/root-AGENTS.md" "## Agent Loop Guidance Version"
assert_not_contains "templates/root-AGENTS.md" "section:meta"
assert_not_contains "templates/root-AGENTS.md" "section:skill-reentry"
assert_contains "templates/root-AGENTS.md" "Treat root \`AGENTS.md\` as a bootstrap cache, not a replacement for the \`agent-loop\` skill"
assert_contains "templates/root-AGENTS.md" "## Workflow Stage Map"
assert_contains "templates/root-AGENTS.md" "After selecting a stage, load the matching \`references/...\` file from the \`agent-loop\` skill package before acting."
assert_contains "templates/root-AGENTS.md" "Load From agent-loop Skill"
assert_contains "templates/root-AGENTS.md" "| Product need, business goal, scope, constraint, scenario, concept identity/lifecycle, or phased delivery is still being shaped | Requirements Discussion |"
assert_contains "templates/root-AGENTS.md" "| Accepted requirement needs shared business-flow, domain, data, architecture, reliability, performance, security, or cross-feature design before feature specification | Decision & Design If Needed | \`references/project-decisions.md\` |"
assert_contains "templates/root-AGENTS.md" "| Accepted requirement needs feature-level product intent before engineering specification | Product Brief If Needed |"
assert_contains "templates/root-AGENTS.md" "| Accepted requirement or Product Brief has completed Design Readiness and is ready for engineering behavior and acceptance | Feature Spec |"
assert_not_contains "templates/root-AGENTS.md" "Requirements Discussion / Grill"
assert_not_contains "templates/root-AGENTS.md" "Decision / ADR |"
assert_not_contains "templates/root-AGENTS.md" "Decision Scan / Placement If Needed |"
assert_not_contains "templates/root-AGENTS.md" "Product Brief / Feature Spec"
assert_not_contains "templates/root-AGENTS.md" "| Operational Support |"
assert_not_contains "templates/root-AGENTS.md" "When refreshing, compare each block against the current template by \`section\` and full \`block-version\`, e.g. \`$current_block_version\`. Bare versions like \`1.3.0\` are stale."
assert_contains "templates/root-AGENTS.md" "Before commit, review feature artifacts, requirement records, code diff, verification evidence, drift status, project memory, root/directory guidance impact, and unrelated changes."
assert_not_contains "templates/root-AGENTS.md" "Agents may propose updates to managed blocks when source facts change"

while IFS= read -r reference; do
  if [ ! -f "$root/$reference" ]; then
    printf 'FAIL: Workflow Stage Map points to missing skill reference: %s\n' "$reference" >&2
    exit 1
  fi
done < <(
  awk '
    /<!-- agent-loop:managed-start section:workflow-stage-map / { in_map=1; next }
    /<!-- agent-loop:managed-end section:workflow-stage-map -->/ { in_map=0 }
    in_map == 1 { print }
  ' "$root/templates/root-AGENTS.md" |
    grep -oE '`references/[^`]+\.md`' |
    tr -d '`' |
    sort -u
)

assert_contains "references/project-guidance.md" "Root AGENTS Refresh Protocol"
assert_contains "references/project-guidance.md" 'scripts/check-root-agents-blocks.py'
assert_not_contains "references/project-guidance.md" "file-level managed version"
assert_contains "references/project-guidance.md" "Do not require a separate Managed Block Rule or Agent Loop Guidance Version prose section in target root \`AGENTS.md\`; managed block maintenance rules live in this reference and refresh tooling."
assert_contains "references/project-guidance.md" 'Use `block-version:<agent-loop-version>-<YYYYMMDD>[.<same-day-revision>]`; do not shorten it to the skill version alone.'
assert_contains "references/project-guidance.md" "Copy the exact start marker metadata for each refreshed section from the current root AGENTS template unless the section source must point at a target-project artifact."
assert_contains "references/project-guidance.md" 'Treat bare skill-version-only block revisions such as `block-version:1.3.0` as stale because they cannot distinguish same-version template revisions.'
assert_contains "references/project-guidance.md" "Treat missing, older, bare skill-version-only, date-only, malformed, or different \`block-version\` values as stale; exact full template block-version match is required."
assert_contains "references/project-guidance.md" "If a managed block exists in the current template but is missing from root AGENTS.md, treat it as a missing managed block and propose adding it."
assert_contains "references/project-guidance.md" "Managed block maintenance rules belong here and in refresh tooling; do not require the target root \`AGENTS.md\` to include a separate Managed Block Rule prose section."
assert_contains "references/project-guidance.md" "Do not require a separate Managed Block Rule or Agent Loop Guidance Version prose section in target root \`AGENTS.md\`; managed block maintenance rules live in this reference and refresh tooling."
assert_contains "references/project-guidance.md" "The script validates section presence, marker integrity, per-section \`block-version\`, unexpected managed sections, and local \`source\` paths."
assert_contains "references/project-guidance.md" 'Preserve all content outside managed blocks unless each cleanup, replacement, or migration item is listed in Human Review Summary and separately approved.'
assert_contains "references/project-guidance.md" 'Do not treat "refresh AGENTS.md quickly" or similar wording as blanket approval to replace the whole file with `templates/root-AGENTS.md`.'
assert_contains "references/project-guidance.md" "message-intent"
assert_contains "references/project-guidance.md" "Workflow Stage Map"
assert_contains "references/project-guidance.md" "route common human/project signals to exactly one next stage and its matching detailed references"

assert_contains "references/workflow-checklists.md" 'Compare each managed block `section` and `block-version` against the current root AGENTS template.'
assert_contains "references/workflow-checklists.md" "Workflow Stage Map routes the current signal to exactly one stage and matching detailed references."
assert_contains "references/workflow-checklists.md" 'If `scripts/check-root-agents-blocks.py` is available, run it with Python 3.10+ as a read-only drift check against the current root AGENTS template and target root `AGENTS.md`; use the report as Human Review Summary evidence.'
assert_contains "references/workflow-checklists.md" "Treat missing block-version, older block-version, or missing managed sections as stale even when other sections look current."
assert_not_contains "references/workflow-checklists.md" "managed guidance version"
assert_contains "references/workflow-checklists.md" 'Do not write bare `block-version:<agent-loop-version>` values; copy the full template block revision such as `block-version:1.3.0-20260714.1`.'
assert_contains "references/workflow-checklists.md" "Treat date-only, malformed, or different block-version values as stale; exact full template block-version match is required."
assert_contains "references/workflow-checklists.md" "Do not require a separate Managed Block Rule prose section in target root \`AGENTS.md\`; managed block maintenance rules live in \`references/project-guidance.md\` and refresh tooling."
assert_contains "references/workflow-checklists.md" 'Root guidance refresh may update only human-approved managed blocks.'
assert_contains "references/workflow-checklists.md" 'Never treat "refresh AGENTS.md quickly" or similar wording as blanket approval to replace the whole file with `templates/root-AGENTS.md`.'

assert_contains "references/validation-scenarios.md" "Same Version But Missing Managed Block Revision"
assert_contains "references/validation-scenarios.md" "Retired File-Level Guidance Version Does Not Drive Refresh"
assert_contains "references/validation-scenarios.md" "do not require a \`section:meta\` block or visible Agent Loop Guidance Version prose"
assert_contains "references/validation-scenarios.md" "Bare Skill-Version Block Revision Is Stale"
assert_contains "references/validation-scenarios.md" "Date-Only Block Revision Is Stale"
assert_contains "references/validation-scenarios.md" "Managed Blocks Current Without Prose Rule"
assert_contains "references/validation-scenarios.md" "Root Workflow Stage Map Routes To Detailed References"
assert_contains "references/validation-scenarios.md" 'do not treat root `AGENTS.md` as the detailed stage procedure'
assert_contains "references/validation-scenarios.md" "do not classify root guidance as stale solely because the Managed Block Rule prose section is absent"
assert_contains "references/validation-scenarios.md" "block-version"
assert_contains "Usage.md" 'scripts/check-root-agents-blocks.py'
assert_contains "Usage.md" "提交前 Agent 应同时复核 feature 文档、requirement 记录、代码 diff、验证证据、drift、project memory、root/directory guidance 影响和 unrelated changes。"
assert_contains "CHANGELOG.md" 'scripts/check-root-agents-blocks.py'
assert_contains "CHANGELOG.md" "Added an explicit pre-commit artifact review reminder to root AGENTS Submit And Commit Rules"

if [ ! -f "$root/scripts/check-root-agents-blocks.py" ]; then
  printf 'FAIL: canonical root AGENTS checker script is missing\n' >&2
  exit 1
fi

printf 'PASS: root AGENTS block refresh contract is complete\n'

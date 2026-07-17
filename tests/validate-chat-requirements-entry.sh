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

assert_contains "references/runtime.md" "## Message Intent Classification"
assert_contains "references/runtime.md" "Message intent is evaluated before project state classification"
assert_contains "references/runtime.md" "\`chat\`"
assert_contains "references/runtime.md" "\`requirements-discussion\`"
assert_contains "references/runtime.md" "chat means ordinary discussion, rules questions, status questions, or design talk with no request to create requirements or start implementation"
assert_contains "references/runtime.md" "requirements-discussion means the human is exploring product needs, business goals, capability ideas, constraints, tradeoffs, or user scenarios without authorizing implementation"
assert_contains "references/runtime.md" "Message intent is not permanent; reclassify when the conversation changes intent"
assert_contains "references/runtime.md" "Chat defaults to answer-only, but it may convert to \`requirements-discussion\`, \`proposal-doc\`, \`feature-request\`, \`operational-support\`, \`feature-follow-up\`, or \`deferred-requirement\` when the human intent changes"
assert_contains "references/runtime.md" "If the human explicitly says they only want to discuss and do not want documentation yet, keep the intent as \`chat\` until they ask to shape, record, or archive the requirement"
assert_contains "references/runtime.md" "For \`requirements-discussion\`, reviewed/recorded does not mean accepted for implementation"
assert_contains "references/runtime.md" "Default order applies after Message Intent Classification"
assert_contains "references/runtime.md" "Chat Entry / Requirements Discussion if Needed"
assert_contains "references/runtime.md" "\`feature-follow-up\` | explicit defect/regression/QA/post-close evidence or clear Feature ownership indicates follow-up work; generic “small tweak” alone is insufficient"
assert_not_contains "references/runtime.md" "\`feature-follow-up\` | human reports bug, QA feedback, screenshot issue, regression, small tweak, or post-close correction that may relate to recent feature work"
assert_contains "references/runtime.md" "If unclear whether the human wants ordinary chat or requirements discussion, ask whether to keep discussing or shape the topic into a requirements document"
assert_contains "references/runtime.md" "If unclear whether the human wants requirements discussion or feature implementation, ask whether to form a requirements document first or start feature construction"

assert_contains "references/stage-guides.md" "## Chat Entry"
assert_contains "references/stage-guides.md" "Chat Entry is a default entry behavior, not a permanent label"
assert_contains "references/stage-guides.md" "If chat evolves into product demand, reclassify as \`requirements-discussion\` and ask whether to shape it into a requirements document"
assert_contains "references/stage-guides.md" "If chat turns into a proposal or design-note request, reclassify as \`proposal-doc\` and write only the requested proposal/doc"
assert_contains "references/stage-guides.md" "If the human explicitly says they only want to discuss and do not want documentation yet, keep the intent as \`chat\`"
assert_contains "references/stage-guides.md" "## Requirements Discussion"
assert_contains "references/stage-guides.md" "requirements-discussion -> Brainstorm / Clarify -> Requirement Document Draft -> Human Review -> Requirement Archive"
assert_contains "references/stage-guides.md" "do not create a feature workspace during requirements discussion unless the human explicitly says to start implementation"
assert_contains "references/stage-guides.md" "The human-reviewed requirement document is stored under \`.agent-loop/requirements/<archive-date>-<topic>/\` after the human confirms the document should be recorded"
assert_contains "references/stage-guides.md" "Reviewed/recorded does not mean accepted for implementation"
assert_contains "references/stage-guides.md" "Feature \`product.md\` and \`spec.md\` are derived implementation views; they do not own requirement lifecycle"

assert_contains "references/requirement-management.md" "Requirements Discussion Intake"
assert_contains "references/requirement-management.md" "A requirement document produced from brainstorming is requirement source material after human review"
assert_contains "references/requirement-management.md" "Archive the human-reviewed requirement document after the human confirms the document should be recorded"
assert_contains "references/requirement-management.md" "Reviewed/recorded does not mean accepted for implementation"
assert_contains "references/requirement-management.md" "Do not move the requirement source into a feature workspace when implementation starts"
assert_contains "references/requirement-management.md" "features reference requirement sets; requirements own source and lifecycle"
assert_not_contains "references/requirement-management.md" "If an agent created \`requirement.md\` from chat"

assert_contains "references/document-templates.md" "## Requirement Document"
assert_contains "references/document-templates.md" "# Requirement: <topic>"
assert_contains "references/document-templates.md" "Source: conversation | file | link | prototype | mixed"
assert_contains "references/document-templates.md" "Write the human-reviewed document as \`.agent-loop/requirements/<archive-date>-<topic>/requirement.md\` after the human confirms the document should be recorded"
assert_contains "templates/requirement-set-README.md" "Requirement Document:"
assert_contains "templates/requirement-set-README.md" "Source Conversation Summary:"

assert_contains "references/workflow-checklists.md" "## Message Intent"
assert_contains "references/workflow-checklists.md" "If message intent is \`chat\`, answer or discuss only; do not create a requirement set or feature workspace"
assert_contains "references/workflow-checklists.md" "Reclassify chat when the conversation turns into requirements discussion, feature implementation, operational support, follow-up, or deferred requirement intake"
assert_contains "references/workflow-checklists.md" "Reclassify chat as \`proposal-doc\` when the human asks for a proposal/design note without implementation"
assert_contains "references/workflow-checklists.md" "Keep intent as \`chat\` when the human explicitly wants discussion without documentation"
assert_contains "references/workflow-checklists.md" "If message intent is \`requirements-discussion\`, route to Requirements Discussion before Feature Spec"
assert_contains "references/workflow-checklists.md" "During requirements discussion, use Brainstorm / Clarify and produce a human-reviewed requirement document before archiving"

assert_contains "templates/root-AGENTS.md" "Message Intent Guard"
assert_contains "templates/root-AGENTS.md" "chat"
assert_contains "templates/root-AGENTS.md" "requirements-discussion"
assert_contains "templates/root-AGENTS.md" "Requirements discussion must shape demand through Brainstorm / Clarify into a human-reviewed requirement document under \`.agent-loop/requirements/\` before feature construction"
assert_contains "templates/root-AGENTS.md" "Message intent is not permanent"
assert_contains "templates/root-AGENTS.md" "If chat turns into a proposal/design-note request, reclassify as \`proposal-doc\`"
assert_contains "templates/root-AGENTS.md" "If the human explicitly wants discussion without documentation, keep \`chat\`"

assert_contains "SKILL.md" "Message Intent Guard"
assert_contains "SKILL.md" "requirements-discussion"
assert_contains "SKILL.md" "Message intent is not permanent"
assert_contains "SKILL.md" "\`proposal-doc\`"
assert_contains "README.md" "Chat And Requirements Discussion"
assert_contains "README.md" "requirements-discussion → Brainstorm / Clarify → requirement document → requirements/"

assert_contains "references/validation-scenarios.md" "Chat And Requirements Discussion Entry"
assert_contains "references/validation-scenarios.md" "classify message intent as \`chat\`"
assert_contains "references/validation-scenarios.md" "classify message intent as \`requirements-discussion\`"
assert_contains "references/validation-scenarios.md" "reclassify from \`chat\` to \`requirements-discussion\`"
assert_contains "references/validation-scenarios.md" "reclassify from \`chat\` to \`proposal-doc\`"
assert_contains "references/validation-scenarios.md" "keep the intent as \`chat\` because the human explicitly does not want documentation yet"
assert_not_contains "references/runtime.md" "archive the accepted document"
assert_not_contains "references/stage-guides.md" "The accepted requirement document"
assert_not_contains "references/requirement-management.md" "Archive the accepted requirement document"
assert_not_contains "references/document-templates.md" "Write the accepted document"
assert_not_contains "references/validation-scenarios.md" "accepted requirement document"
assert_contains "references/validation-scenarios.md" "do not create feature workspace"

printf 'PASS: chat and requirements discussion entry contract is complete\n'

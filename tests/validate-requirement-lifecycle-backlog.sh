#!/usr/bin/env bash
set -euo pipefail

assert_contains() {
  local file="$1"
  local expected="$2"
  if ! grep -Fq "$expected" "$file"; then
    echo "FAIL: expected '$expected' in $file" >&2
    exit 1
  fi
}

assert_not_contains() {
  local file="$1"
  local unexpected="$2"
  if grep -Fq "$unexpected" "$file"; then
    echo "FAIL: unexpected '$unexpected' in $file" >&2
    exit 1
  fi
}

assert_not_exists() {
  local path="$1"
  if [ -e "$path" ]; then
    echo "FAIL: unexpected source-file template exists: $path" >&2
    exit 1
  fi
}

assert_contains "references/requirement-management.md" "Requirement Lifecycle / Backlog"
assert_contains "references/requirement-management.md" "proposed | accepted | deferred | in-progress | partially-implemented | implemented | superseded | rejected | reference-only"
assert_contains "references/requirement-management.md" "Delivery Phase Status Roll-up"
assert_contains "references/requirement-management.md" "Requirement source files are immutable by default"
assert_contains "references/requirement-management.md" 'Do not overwrite, rewrite, summarize over, or edit `requirement.md`'
assert_contains "references/requirement-management.md" "Backward Compatibility"
assert_contains "references/requirement-management.md" "Old requirement set README files remain valid"
assert_contains "references/requirement-management.md" "Never bulk migrate requirements automatically"
assert_contains "references/requirement-management.md" "Requirement Conflict Review"
assert_contains "references/requirement-management.md" "create a new requirement set and mark the old one superseded"

assert_contains "templates/requirement-set-README.md" "Status: proposed | accepted | deferred | in-progress | partially-implemented | implemented | superseded | rejected | reference-only"
assert_contains "templates/requirement-set-README.md" "## Lifecycle"
assert_contains "templates/requirement-set-README.md" "Intake Type: human-request | follow-up | deferred-from-feature | ops-discovery | bug-report | idea | reference"
assert_contains "templates/requirement-set-README.md" "Implemented By:"
assert_contains "templates/requirement-set-README.md" "Superseded By:"
assert_contains "templates/requirement-set-README.md" "## Status History"

assert_contains "templates/requirements-index.md" "inventory and backlog view"
assert_contains "templates/requirements-index.md" "## Backlog / Deferred Requirements"
assert_contains "templates/requirements-index.md" "## In Progress"
assert_contains "templates/requirements-index.md" "## Implemented"
assert_contains "templates/requirements-index.md" "## Partially Implemented"
assert_contains "templates/requirements-index.md" "## Superseded / Rejected"

assert_not_exists "templates/requirement.md"
assert_not_exists "templates/feedback.md"
assert_not_exists "templates/change-request.md"
assert_not_exists "templates/deferred-requirement.md"
assert_not_exists "templates/bug-report.md"
assert_not_exists "templates/backlog-item.md"

assert_contains "references/stage-guides.md" "Future / Deferred Requirement Intake"
assert_contains "references/stage-guides.md" 'Do not write future TODO, backlog, deferred requirements, or unimplemented planned capability details into `project.md`'
assert_contains "references/stage-guides.md" "only when source material is provided or already exists"
assert_contains "references/stage-guides.md" "Requirement Reconciliation"
assert_contains "references/stage-guides.md" "Requirement Conflict Review"

assert_contains "references/workflow-checklists.md" "Future / Deferred Requirement Intake"
assert_contains "references/workflow-checklists.md" 'Do not write future TODO, backlog, deferred requirements, or unimplemented planned capability details into `project.md`'
assert_contains "references/workflow-checklists.md" 'Do not edit `requirement.md` or other source files for lifecycle/status updates'
assert_contains "references/workflow-checklists.md" "Large follow-up conflicts get a Requirement Conflict Review"

assert_contains "references/project-memory-mode.md" "Project memory must not be used as a backlog"
assert_contains "references/project-memory-mode.md" "future feature ideas, temporary TODOs, deferred requirements, unimplemented planned capability details, or backlog lists"
assert_contains "references/design.md" 'future/deferred work belongs in requirement sets and optional `requirements/INDEX.md`, not in `project.md`'
assert_contains "references/artifact-rules.md" "backlog lists, deferred requirements"
assert_contains "references/concepts.md" "requirement lifecycle/backlog records"

assert_contains "references/validation-scenarios.md" "Requirement Backlog Does Not Pollute Project Memory"
assert_contains "references/validation-scenarios.md" "Old Requirement Set README Remains Valid"
assert_contains "references/validation-scenarios.md" "Requirement Source File Is Not Rewritten"
assert_contains "references/validation-scenarios.md" "Large Follow-up Conflict Requires Requirement Rebuild Review"

assert_contains "README.md" "Requirement Lifecycle / Backlog"
assert_contains "Usage.md" "需求待办"
assert_contains "Usage.md" "当前恢复动作"
assert_contains "CHANGELOG.md" "Requirement Lifecycle / Backlog"
assert_contains "SKILL.md" "Version: 1.5.1"
assert_contains "README.md" "**Current version:** 1.5.1"
assert_contains "Usage.md" "**版本：** 1.5.1"
assert_contains "plugin.json" '"version": "1.5.1"'
assert_contains "templates/root-AGENTS.md" "block-version:1.5.1-20260725.1"
assert_contains "CHANGELOG.md" "## 1.5.1 — 2026-07-25"
assert_contains "CHANGELOG.md" "## 1.5.0 — 2026-07-17"
assert_contains "CHANGELOG.md" "block-version:1.4.0-20260715.1"
assert_not_contains "CHANGELOG.md" "block-version:1.3.0-20260715.1"
assert_contains "CHANGELOG.md" "## 1.3.0 — 2026-07-11"
assert_not_contains "templates/root-AGENTS.md" "## Agent Loop Guidance Version"
assert_contains "AGENTS.md" 'ignore the `alpha` prefix for version records'

echo "PASS: requirement lifecycle/backlog contract is complete"

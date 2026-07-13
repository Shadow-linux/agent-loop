#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

failures=0

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  failures=$((failures + 1))
}

assert_file_exists() {
  local path=$1
  if [ ! -f "$root/$path" ]; then
    fail "missing required file: $path"
  fi
}

assert_contains() {
  local path=$1
  local text=$2
  if [ ! -f "$root/$path" ] || ! grep -Fq -- "$text" "$root/$path"; then
    fail "$path missing required text: $text"
  fi
}

assert_not_source_artifact() {
  local path=$1
  if [ -e "$root/$path" ]; then
    fail "source repository must not contain downstream artifact: $path"
  fi
}

assert_file_exists "references/project-skills.md"
assert_file_exists "templates/project-skills/INDEX.md"
assert_file_exists "templates/project-skills/SKILL.md"
assert_file_exists "templates/project-skills/validation.md"

assert_contains "SKILL.md" "project-skill-management"
assert_contains "SKILL.md" "references/project-skills.md"
assert_contains "SKILL.md" ".agent-loop/skills/"
assert_contains "SKILL.md" "Execution Gate"

assert_contains "references/runtime.md" "project-skill-management"
assert_contains "references/runtime.md" "Project Skill Creation / Update"
assert_contains "references/runtime.md" ".agent-loop/skills/INDEX.md"
assert_contains "references/runtime.md" "Execution Gate"

assert_contains "references/design.md" "Project Skill"
assert_contains "references/design.md" ".agent-loop/skills/<skill-name>/"
assert_contains "references/design.md" "bootstrap"
assert_contains "references/design.md" "on-demand"

assert_contains "references/project-skills.md" "把这个流程做成技能"
assert_contains "references/project-skills.md" "Project Skill Candidate"
assert_contains "references/project-skills.md" "Gate 1: Create Project Skill"
assert_contains "references/project-skills.md" 'automatically becomes `active`'
assert_contains "references/project-skills.md" "Execution Gate"
assert_contains "references/project-skills.md" "one invocation"
assert_contains "references/project-skills.md" "Validated Content Manifest"
assert_contains "references/project-skills.md" "exact INDEX row"
assert_contains "references/project-skills.md" "invocation begins"
assert_contains "references/project-skills.md" "One combined human confirmation"
assert_contains "references/project-skills.md" "first-version exclusion"
assert_contains "references/project-skills.md" "active/consumed authorization lifecycle"
assert_contains "references/project-skills.md" "Feature Auto-Loop"
assert_contains "references/project-skills.md" "Task Auto-Run"
assert_contains "references/project-skills.md" "writing-skills"
assert_contains "references/project-skills.md" "skill-creator"
assert_contains "references/project-skills.md" "~/.agents/skills/"
assert_contains "references/project-skills.md" "proposed | active | disabled | deprecated"

assert_contains "references/skill-routing.md" "Project Skill Creation / Update"
assert_contains "references/skill-routing.md" "superpowers:writing-skills"
assert_contains "references/skill-routing.md" "skill-creator"
assert_contains "references/external-skill-adapters.md" ".agent-loop/skills/<skill-name>/"
assert_contains "references/external-skill-adapters.md" "writing-skills"
assert_contains "references/external-skill-adapters.md" "skill-creator"
assert_contains "references/external-skill-adapters.md" "Project-local skill package is the exception"

assert_contains "references/stage-guides.md" "## Project Skill Creation / Update"
assert_contains "references/stage-guides.md" "Execution Gate"
assert_contains "references/stage-guides.md" "accepted proactive Candidate"
assert_contains "references/workflow-checklists.md" "## Project Skill Creation / Update"
assert_contains "references/workflow-checklists.md" "one invocation"

assert_contains "templates/root-AGENTS.md" "project-skill-management"
assert_contains "templates/root-AGENTS.md" "Project Skill Creation / Update"
assert_contains "templates/root-AGENTS.md" ".agent-loop/skills/INDEX.md"
assert_contains "templates/root-AGENTS.md" "Execution Gate"
assert_contains "templates/root-AGENTS.md" "block-version:1.3.0-20260713.2"
assert_contains "templates/project.md" "Project Skills"
assert_contains "templates/project.md" ".agent-loop/skills/INDEX.md"
assert_contains "templates/project-skills/validation.md" "Validated Content Manifest"
assert_contains "templates/project-skills/validation.md" "exact-skill-row"
assert_contains "templates/project-skills/validation.md" "Invocation end and retry behavior"

assert_contains "README.md" ".agent-loop/skills/"
assert_contains "README.md" "Project Skill Creation / Update, Brainstorm, Plan Gate"
assert_contains "Usage.md" "把这个流程做成技能"
assert_contains "CHANGELOG.md" "Project-Local Skills"
assert_contains "references/validation-scenarios.md" "Project Skill Creation / Update"
assert_contains "references/validation-scenarios.md" "Execution Gate"
assert_contains "references/validation-scenarios.md" "Legacy Memory Root Does Not Relocate Project Skills"
assert_contains "references/project-guidance.md" "exact INDEX row"

assert_not_source_artifact ".agent-loop/skills"

if [ "$failures" -ne 0 ]; then
  printf 'Project-local skills validation failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'PASS: project-local skills creation, activation, loading, and execution gates are complete\n'

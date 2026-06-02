# Agent Loop Concepts

## Scope

This skill is for single-person development with a CLI agent. The human controls direction; the agent controls workflow mechanics.

First version excludes:

- multiplayer workflows
- roadmap graph
- roadmap adapter
- tdd-guard
- complex ADR system
- global installation
- automatic directory-level AGENTS.md generation without human confirmation

## Definitions

**Human Goal**: Human intent, requirement, prototype, bug, or continuation request.

**Project**: Current codebase. Long-term project memory is `agent-loop/project.md`.

**Project Memory Mode**: The structure used for durable project knowledge. `simple` means `project.md` is the main memory body. `enterprise` means `project.md` is an index and current-state summary, with optional details under `agent-loop/project/*.md`.

**Architecture Profile**: The project shape, language adapter, framework adapter, and DDD intensity used to guide code layout and boundary decisions. It is descriptive for existing projects and advisory for new scaffolds.

**Remote Entry**: A local directory that mainly exists to help the agent find and continue a remote project. It owns local `agent-loop/remote.md` and a thin `project.md` with `Status: remote-entry`.

**Local Shadow Mode**: A fallback where `agent-loop` memory is kept locally because the remote project is not writable. Every code fact, command, test result, and browser observation must include remote evidence.

**Requirement**: Human-provided textual or conversational need.

**Prototype**: Human-provided design artifact, screenshot, diagram, or interaction reference.

**Feature**: One behavior-changing work area under `agent-loop/features/<feature-id>/`. A feature can contain many stories and many tasks.

**Product Brief**: Optional feature-level product understanding in `product.md`: problem, users, user stories, product scope, product decisions, and open product questions.

**Stories**: User-perspective slices inside a feature. They live in `spec.md` and are referenced by labels such as `US1`.

**Task**: Default executable engineering unit. Tasks should be small, verifiable, and linked to a story when possible.

**Step**: TDD or command-level action inside a task.

**Plan**: Active execution plan for one task by default, or one story when explicitly chosen. It is not the whole feature plan unless the feature is tiny and the human explicitly confirms whole-feature execution.

**Construction-Grade Plan**: A `plan.md` that can be executed by an agent with near-zero project context: exact paths, code context, interface contracts, signatures, parameters, test code, commands, expected RED/GREEN output, rollback, and self-review.

**Evidence**: Fresh proof from tests, build, lint/typecheck, API checks, E2E/browser checks, screenshots, logs, or review.

**E2E Discovery**: Web-specific discovery before browser automation. The agent reads real scripts, configs, docs, fixtures, env rules, CI, and existing E2E specs to determine app start, URL, auth/test data, and automation route before recording or executing E2E cases.

**Drift**: Mismatch between docs, code reality, or human decisions.

**Re-Adopt Agent Loop Project**: Recovery path for a project that already has `agent-loop/`, but recent development happened outside the loop. The agent compares code reality to existing memory, proposes backfill, asks human confirmation, then resumes or starts feature work.

**Submit / Integrate**: The explicit stage that packages verified work for commit, PR text, merge note, or release note. It requires human confirmation and records the result in `notes.md`.

**Subagent Brief**: A bounded assignment for an optional helper agent. The main agent owns state, merge, drift, submit, and close decisions.

**Delivery Contract**: A durable producer-consumer boundary handoff in `contracts.md` and optional `contracts/*` details. It records API, service, event, async workflow, data, UI-behavior, library, or runtime interfaces that downstream work depends on. It is distinct from temporary subagent briefs.

**Strict Mode**: Default gate mode. Ask before and after every stage.

**Feature Auto-Loop**: Feature-level authorization after Feature Spec acceptance. The agent may advance Agent-ready feature stages/tasks until a stop condition appears. It must stop before Submit / Integrate and Close.

**Task Auto-Run**: Task/story-level authorization after the selected task/story plan is accepted. The agent may complete only that task/story through TDD, verification, review, drift, and status update.

**Feature Completion Check**: Proactive check that determines whether an active feature should be closed, continued, paused before a new feature, or have scope updated. Humans do not need to ask for close by name; the agent recommends it when conditions pass.

**Feature Close Review**: Required feature-level review before recommending or performing close. It verifies the whole feature against `product.md` when present, `spec.md`, `tasks.md`, `tests.md`, acceptance criteria, out-of-scope boundaries, and project standards. It is separate from per-task review.

**Human Review Summary**: Table-first, human-facing approval view shown before non-trivial confirmations. It summarizes artifacts, evidence, risks, blockers, and requested decisions while full artifact files remain the source of truth.

## Ownership

```text
remote.md  = local entry pointer for remote projects
project.md = long-term project facts in simple mode; memory index and current state in enterprise mode
project/   = optional enterprise long-term project memory details
requirements/ = original human material packages or references, grouped by archive-date requirement set directory
product.md = optional feature product intent and product scope
spec.md    = intended feature behavior
tasks.md   = work breakdown and order
tests.md   = how correctness will be proven, including feature-specific E2E cases
plan.md    = active execution plan for the current task/story
notes.md   = what actually happened
handoffs/  = optional subagent briefs and returns
contracts.md = optional delivery contract index or compact contract
contracts/ = optional durable producer-consumer contract details
```

`AGENTS.md` / `CLAUDE.md` live outside `agent-loop/` and tell future agents how to enter the workflow. They do not own task state.

Requirement-set dates are archive dates only. They do not define deadlines, requirement duration, or feature lifecycle.

Requirement sets group the human's original materials for one intake event or topic: requirement docs, prototypes, feedback, screenshots, recordings, links, and follow-up notes.

## Feature Workspace Model

Use one feature workspace per behavior-changing feature:

```text
spec.md  = whole feature behavior
product.md = optional feature product understanding
tasks.md = all tasks for the feature
tests.md = whole feature test strategy
plan.md  = current active task/story plan
notes.md = history, evidence, decisions, drift
tasks/   = optional task details in complex artifact mode
tests/   = optional test details in complex artifact mode
plans/   = optional dated plan cycles in complex artifact mode
handoffs/ = optional subagent briefs and returns
contracts.md = optional delivery contract index or compact contract
contracts/ = optional durable producer-consumer contract details
```

For complex projects, `tasks.md`, `tests.md`, and `plan.md` remain stable entry files. When complexity is high, they become indexes that point to `tasks/`, `tests/`, and `plans/` detail files.

## Execution Unit Rules

Default:

```text
single task
```

Allowed with explicit human choice:

```text
single story
```

Allowed only for tiny features with explicit human confirmation:

```text
whole feature
```

## Task Ordering

Use three patterns:

```text
linear   = one task after another
parallel = independent tasks; can run in any order or via subagents
barrier  = verification/human gate before next stage
```

Do not introduce a roadmap graph in v1.

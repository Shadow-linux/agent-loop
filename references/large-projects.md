# Large Project Operating Mode

Use this file for old, unfamiliar, multi-package, multi-service, or large repositories. Treat 100k+ LOC projects as large even if the requested feature sounds small.

For long-term project memory structure, pair this file with `project-memory-mode.md`. Large-project operating mode is about how to work; Project Memory Mode is about how to store durable knowledge.

This file extends `draft_agent_loop_struct.md` and `final_agent_loop_skill_design.md`. It must not change the core design:

```text
Feature -> Stories -> Tasks -> Steps
one feature workspace
stable tasks.md/tests.md/plan.md entry files
human gate before every stage
no roadmap graph in v1
```

## Core Rule

Do not convert a human goal directly into code edits in a large project.

Use this sequence:

```text
Project scan -> boundary map -> feature spec -> tasks ledger -> active plan -> TDD execution -> verification -> drift update -> submit if requested
```

## Feature, Tasks, And Plan At Scale

A feature is not limited to one task or one plan.

```text
feature
  spec.md    = intended behavior for the whole feature
  tasks.md   = durable ledger of all tasks, dependencies, statuses, barriers
  tests.md   = full correctness strategy
  plan.md    = active plan for the current task/story only
  notes.md   = historical evidence, decisions, drift, pause/resume
  tasks/     = optional detailed tasks when complex artifact mode is triggered
  tests/     = optional detailed test cases when complex artifact mode is triggered
  plans/     = optional dated plan cycles when complex artifact mode is triggered
  handoffs/  = optional subagent briefs and returns when subagent mode is triggered
  contracts.md = optional stable Delivery Contract index or compact contract
  contracts/ = optional durable producer-consumer contract details
```

For a 100k+ LOC project, a feature may have:

- 3-10 stories
- 5-30 tasks
- multiple stages
- multiple barriers
- many verification commands

Always keep `tasks.md`, `tests.md`, and `plan.md` as stable entry files. If complexity triggers detail directories, use `complex-artifacts.md`; the stable files become indexes that link to detailed files.

## Large Project Scan

Before feature work, inspect only enough to form a useful map:

- repo shape and package/workspace layout
- build/test commands
- app entry points
- domain boundaries
- API boundaries
- data/storage boundaries
- existing test locations
- existing agent/project docs such as AGENTS, CLAUDE, GEMINI, README

Record stable findings in `project.md`, not in a feature note.

For existing-project onboarding, prefer the layered scan in `existing-project-onboarding.md`. This file adds large-project expectations:

- keep scans shallow until a feature boundary is selected
- record evidence for every capability and command
- assign confidence labels instead of pretending certainty
- identify package/app/service boundaries before task splitting
- defer deep code reading to a targeted feature scan
- when subagents are available and the human confirms, parallelize onboarding with bounded scan lanes
- evaluate whether simple project memory is still enough, or whether enterprise mode should be recommended

Recommend enterprise Project Memory Mode when any hard trigger applies, including about 200k+ LOC, 5+ durable boundaries, 2+ test systems, 3+ execution environments, `project.md` above about 600 lines, repeated re-scans, or 5+ directory-level guidance files.

## Large Onboarding Subagent Recommendation

Recommend optional subagent scanning during onboarding when the project is large or complex:

```text
100k+ LOC
monorepo / multiple apps / multiple services
3+ major boundaries
multiple test systems
multiple runtime entry points
multiple guidance files
stale or conflicting docs
```

Subagents are only scan helpers. They return findings, evidence, confidence, uncertainties, and suggested `project.md` entries. The main agent writes the final proposal and asks the human before changing files.

If subagents are not available or the human declines, continue with single-agent layered scan.

## Targeted Feature Scan

After project onboarding and after the human selects a feature, do a focused scan only inside relevant boundaries:

```text
feature keywords
related routes/controllers/pages/actions
related domain/core modules
related schema/model/migration files
related tests
related guidance docs
```

Write feature-specific findings into `spec.md`, `tasks.md`, or `notes.md`.
Write lasting project facts back to `project.md` only after human confirmation.

## Boundary Map

For each feature, identify boundaries in `spec.md` or `tasks.md`:

- UI surfaces
- API/routes/controllers
- domain/services
- database/schema/migrations
- background jobs/events
- permissions/security
- tests/E2E
- observability/logging if relevant

If the affected boundaries are unclear, stop and clarify or run a bounded scan before task split.

When a boundary has downstream consumers, load `delivery-contracts.md` and propose a Delivery Contract. Write `contracts.md` or optional `contracts/` details only after human confirmation. Keep temporary subagent briefs in `handoffs/`; keep confirmed durable interface handoffs in `contracts.md` and optional `contracts/` details.

For old-project onboarding, also record each stable boundary in `project.md` with its guidance status:

```text
Guidance: root only | has AGENTS.md | propose AGENTS.md | not needed
```

When a feature creates a new stable boundary directory, propose a directory-level `AGENTS.md` and ask for human confirmation before writing it.

## Task Split For Large Features

Prefer staged tasks:

```text
Stage 1: domain/data foundation
Barrier: module tests + human confirmation
Stage 2: API behavior
Barrier: API tests + human confirmation
Stage 3: UI/browser behavior
Barrier: E2E/browser verification + human confirmation
Stage 4: regression/drift/submit/close
Barrier: full verification + drift check + submit decision + close confirmation
```

Allowed ordering:

- linear for dependent tasks
- parallel for independent tasks
- barrier between risky stages

Do not introduce a roadmap graph in v1. Use Markdown headings and barriers inside `tasks.md`.

If task count, test count, boundaries, subagent needs, or plan history exceed the trigger conditions, recommend complex artifact mode and load `complex-artifacts.md`.

## Active Plan Rules

`plan.md` is replaced or updated for the next active task/story. In complex artifact mode, `plan.md` may be a pointer to a detailed dated file under `plans/`.

The filename remains stable. The plan cycle itself is dated:

```text
Plan ID: YYYY-MM-DD-T003-invite-authorization
Created: 2026-05-26
Updated: 2026-05-26
Active Since: 2026-05-26
```

Before replacing it:

1. Move completed evidence into `notes.md`.
2. Update task status in `tasks.md`.
3. Record drift or decisions.
4. Set the next active unit.
5. Add a `Plan History` entry in `notes.md` with date, plan ID, result, evidence, and next unit.

For large projects, every active plan must include:

- scope: task or story
- explicit included/excluded tasks
- files or areas to inspect
- files likely to change
- tests to write first
- focused verification commands
- broader verification command before close
- risks and rollback notes
- path to detail file when using `plans/`

## Subagent Rules At Scale

Use subagents only after human confirmation and only for independent tasks or story slices.

When subagents are used:

- create a bounded brief from `templates/subagent-brief.md`
- store the brief under `handoffs/` when complex artifact mode is active
- name exact task/story scope, excluded files or behavior, verification commands, and return format
- keep `tasks.md` as the authoritative ledger
- merge returned evidence and drift into `notes.md`
- include relevant accepted Delivery Contracts in subagent context when assignments cross producer-consumer boundaries

Subagents never close the feature, rewrite original requirements, or decide submission.

## Resume Rules

When resuming a large project:

1. Read `project.md`.
2. Read active feature docs.
3. Reconstruct current stage from `tasks.md`, `tests.md`, `plan.md`, detail directories if referenced, and `notes.md`.
4. Check whether code reality obviously drifted.
5. Recommend exactly one next stage.

Do not re-scan the whole repo unless `project.md` is stale or the active feature boundary is unknown.

If docs are stale or incomplete, use `recovery-and-backfill.md`: code reality is the current fact base for repairing agent docs, while human requirements remain original intent.

## Drift At Scale

Large projects drift often. Classify drift:

- feature behavior drift -> `spec.md`
- task/order drift -> `tasks.md`
- test strategy drift -> `tests.md`
- active execution drift -> `plan.md`
- detail artifact drift -> `tasks/*`, `tests/*`, or `plans/*` plus the matching index
- evidence/decision drift -> `notes.md`
- architectural or long-term fact drift -> `project.md`
- producer-consumer interface drift -> propose `contracts.md` and matching `contracts/*` details, update after human confirmation, and require affected consumers plus human approval for breaking changes

If a change affects future features, it belongs in `project.md` even if discovered during one feature.

## Stop Conditions

Stop and ask when:

- affected boundaries cannot be identified
- tests are missing and replacement verification is unclear
- feature crosses security, billing, auth, data loss, or migration boundaries
- task count grows beyond the current feature scope
- code reality contradicts `project.md`
- a human decision changes long-term product behavior

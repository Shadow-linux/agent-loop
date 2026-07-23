# Complex Artifact Mode

Use this file when a feature is too complex for single `tasks.md`, `tests.md`, and `plan.md` files to remain readable.

## Core Rule

Stable entry files remain mandatory:

```text
spec.md
tasks.md
tests.md
plan.md
notes.md
```

`product.md` remains optional and should exist when Product Brief is triggered.

When complex artifact mode is confirmed, `tasks.md`, `tests.md`, and `plan.md` become indexes and current-state summaries for the areas that need detail. `product.md`, `spec.md`, and `notes.md` remain stable source/record files. Detailed artifacts may live in:

```text
tasks/
tests/
plans/
contracts/
```

Do not delete or replace the stable entry files. Future agents must still start there.

## Trigger Conditions

Complexity should reflect whether the feature is no longer locally understandable or executable inside one cohesive area. Think in terms of "牵一发而动全身": a change whose planning, implementation, verification, release, or operational support spans multiple collaborating parts.

### Complexity Assessment Trigger

When stories > 3, pause and assess whether Complex Artifact Mode is needed.

Story count does not independently recommend Complex Artifact Mode. It only forces an explicit complexity assessment.

Quantity signals such as many tasks or many test cases are prompts for assessment, not sufficient recommendation triggers. Use them to ask why the feature is large: local detail inside one cohesive area, or real cross-boundary coordination.

### Recommendation Semantics

Agent may decide whether to recommend Complex Artifact Mode, but the recommendation must explain why the feature cannot be safely understood, planned, or verified as one cohesive change.

Recommend Complex Artifact Mode when the work spans multiple collaborating modules, services, workflows, ownership lanes, or release/operation concerns, especially when:

- different parts require separately managed tasks, verification, plans, or Delivery Contracts
- implementation changes can affect multiple downstream behavior paths
- sequencing, barriers, rollback, deployment, config, data, monitoring, or operational support need explicit coordination
- parallel ownership is required by the work structure, not merely because the agent prefers to dispatch subagents
- `tasks.md`, `tests.md`, or `plan.md` becomes hard to scan as a single active artifact

Do not recommend Complex Artifact Mode from story count, task count, test count, or ordinary file/module count alone. A feature with many local details may remain in stable files when it is still understandable and verifiable inside one cohesive module or workflow.

Ordinary files within one cohesive module do not justify Complex Artifact Mode. A simple UI -> API -> DB path may remain in stable files when its tasks, tests, and plan are still readable.

Before creating directories, explain the complex semantics that justify the recommendation, name which files need detail, and ask human confirmation. Create only the detail directories that are actually needed.

## Directory Layout

```text
.agent-loop/features/YYYY-MM-DD-<feature>/
  spec.md
  tasks.md
  tests.md
  plan.md
  notes.md
  tasks/
    US1/
      T001-<slug>.md
    US2/
      T003-<slug>.md
  tests/
    US1/
      TC001-<slug>.md
    e2e/
      E2E001-<slug>.md
  plans/
    YYYY-MM-DD-T003-<slug>.md
  handoffs/
    YYYY-MM-DD-T003-<slug>-subagent.md
  contracts/
    API001-<slug>.md
```

## Naming

Task detail files:

```text
tasks/US<n>/T<nnn>-<slug>.md
```

Test detail files:

```text
tests/US<n>/TC<nnn>-<slug>.md
tests/e2e/E2E<nnn>-<slug>.md
tests/api/API<nnn>-<slug>.md
tests/module/MOD<nnn>-<slug>.md
```

Plan cycle files:

```text
plans/YYYY-MM-DD-T<nnn>-<slug>.md
plans/YYYY-MM-DD-US<n>-<slug>.md
```

Subagent brief files:

```text
handoffs/YYYY-MM-DD-T<nnn>-<slug>-subagent.md
handoffs/YYYY-MM-DD-US<n>-<slug>-subagent.md
```

Delivery Contract detail files:

```text
contracts/API<nnn>-<slug>.md
contracts/EVENT<nnn>-<slug>.md
contracts/DATA<nnn>-<slug>.md
contracts/UI<nnn>-<slug>.md
contracts/LIB<nnn>-<slug>.md
contracts/RUNTIME<nnn>-<slug>.md
```

`contracts.md` remains the optional stable Delivery Contract index or compact contract file. Use `contracts/` for details only after human confirmation when the producer-consumer boundary needs schemas, examples, errors, compatibility notes, history, or multiple consumer notes. Delivery Contracts are not limited to complex artifact mode, but they are not default artifacts.

Use stable IDs inside files too:

```text
Task ID: T003
Story: US2
Related Tests: TC002, API001
Active Plan: plans/2026-05-26-T003-api-authorization.md
```

## Index Responsibilities

`tasks.md` remains the durable ledger:

- stage/barrier structure
- task status
- story mapping
- dependency summary
- path to detail file

`tests.md` remains the test matrix:

- requirement checklist
- test categories
- test IDs
- command summary
- path to detail file

`plan.md` remains the active plan pointer:

- current Plan ID
- current task/story
- current plan detail path
- next action
- stop condition

The detailed plan under `plans/` must follow `implementation-planning.md`: exact paths, code context, interface contracts, parameters, test code, commands, expected RED/GREEN output, risks, rollback, and self-review.

`notes.md` remains historical:

- Plan History
- evidence
- decisions
- drift
- pause/resume

## Detail File Rules

Each detail file must be independently understandable:

- front matter-like header with ID, story, status, created/updated dates
- source links back to `spec.md`, `tasks.md`, `tests.md`, and active plan
- exact files or boundaries affected
- verification commands or expected evidence
- handoff notes for subagents when relevant

Do not create detail files for simple tasks that fit clearly in the index.

## Migration From Simple Mode

When upgrading an existing feature:

1. Keep existing stable files.
2. Create `tasks/`, `tests/`, and/or `plans/` only for the parts that need detail.
3. Move detail out of the index into detail files.
4. Replace moved detail in index files with links and summaries.
5. Record the migration in `notes.md`.

## Backfill And Drift

If a task/test/plan detail changes:

- update the detail file
- update its index row in `tasks.md`, `tests.md`, or `plan.md`
- record evidence or drift in `notes.md`

If index and detail conflict, stop and reconcile before executing.

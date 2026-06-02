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

When complex artifact mode is triggered, `tasks.md`, `tests.md`, and `plan.md` become indexes and current-state summaries. `product.md`, `spec.md`, and `notes.md` remain stable source/record files. Detailed artifacts live in:

```text
tasks/
tests/
plans/
contracts/
```

Do not delete or replace the stable entry files. Future agents must still start there.

## Trigger Conditions

Recommend complex artifact mode when any of these are true:

- stories >= 3
- tasks >= 8
- test cases >= 10
- feature crosses 3 or more major boundaries such as UI, API, domain, DB, jobs, auth, E2E
- feature needs subagents or parallel task ownership
- feature spans more than one development day
- more than 2 plan cycles exist
- `tasks.md`, `tests.md`, or `plan.md` becomes hard to scan

Before creating directories, explain why the trigger applies and ask human confirmation.

## Directory Layout

```text
agent-loop/features/YYYY-MM-DD-<feature>/
  product.md optional
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

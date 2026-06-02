# Agent Loop Artifact Rules

## Source Of Truth

```text
agent-loop is the workflow source of truth.
Human original requirements remain source material, not mutable working docs.
Code reality wins when reconciling stale memory, but human confirms updates.
Code reality does not overwrite human original requirements.
```

Default root is `agent-loop/`. If legacy `.agent-loop/` exists, read it for the current run and ask before migration.

If the local directory is only a remote-project entry point, local `agent-loop/remote.md` is the local entry source of truth. Full project memory should live next to the remote source of truth when remote writes are allowed. If remote writes are not allowed, use local-shadow mode and attach remote evidence to every code fact.

## Reality Layers

Use these layers when recovering or backfilling:

```text
code reality       = current implemented fact
human requirements       = original intent and source material
agent-loop docs    = working memory that may need repair
verification output = proof of current behavior
```

If code reality conflicts with agent docs, propose document backfill.
If code reality conflicts with human requirements, stop and ask for a human decision.

New human source material should be archived inside a requirement set directory. Do not create flat files directly under `requirements/`.

## File Ownership

| File | Owns | Does Not Own |
|---|---|---|
| `remote.md` | how to find, verify, and access a remote project from a local entry directory | feature logs or project capabilities |
| `project.md` | long-term project facts in simple mode; memory index and current state in enterprise mode | task logs |
| `project/*.md` | enterprise long-term project memory details | feature execution logs |
| `requirements/<archive-date>-<topic>/*` | original human material package: requirements, prototypes, feedback, screenshots, recordings, links, and references | edited specs |
| `product.md` | feature-level product intent, users, stories, product scope | engineering execution plan |
| `spec.md` | intended feature behavior | execution logs |
| `tasks.md` | work breakdown, status, and links to task details | full test evidence |
| `tests.md` | test design, matrix, and links to test details | raw test output |
| `plan.md` | active execution plan pointer or compact plan | historical execution record |
| `notes.md` | decisions, evidence, drift, pause/close | original requirements |
| `contracts.md` | optional confirmed delivery contract index, compact contracts, status, and verification links | temporary subagent assignments |
| `tasks/*` | detailed task instructions when complex mode is triggered | feature-wide ledger |
| `tests/*` | detailed test cases when complex mode is triggered | raw test output |
| `plans/*` | dated plan cycles when complex mode is triggered | current-state summary |
| `handoffs/*` | subagent briefs and returned summaries when subagent mode is triggered | authoritative task status |
| `contracts/*` | optional confirmed durable producer-consumer contract details when interface detail is needed | temporary task logs |

## Status Values

Use these status words:

```text
draft
active
blocked
paused
closed
```

Task status:

```text
todo
in-progress
review
done
blocked
skipped
```

Task status meaning:

- `todo`: not started
- `in-progress`: implementation, tests, or verification are underway
- `review`: implementation and fresh verification may exist, but Task Done Gate is not complete
- `done`: Task Done Gate passed; do not use for code-only completion
- `blocked`: cannot proceed without a blocker being resolved
- `skipped`: explicitly removed or deferred with a reason

Task Done Gate:

```text
done = implementation complete
     + required tests or substitute verification run fresh
     + evidence recorded in notes.md
     + lightweight Spec Review recorded
     + Standards Review recorded when triggered
     + drift decision recorded
     + tasks.md or task detail names the evidence location
```

Task mode:

```text
Agent-ready
Human-gated
```

Gate modes:

```text
Strict Mode
Feature Auto-Loop
Task Auto-Run
```

Record the active gate mode in `project.md` Current Work or the active feature `notes.md` checkpoint. If scope changes, switch back to Strict Mode unless the human renews the auto-mode grant.

Slice type:

```text
vertical
horizontal-foundation
```

Delivery Contract status:

```text
draft
accepted
implemented
verified
superseded
```

## Naming

Feature directory:

```text
agent-loop/features/YYYY-MM-DD-<feature-slug>/
```

Core feature files keep stable names:

```text
spec.md
tasks.md
tests.md
plan.md
notes.md
```

Do not create dated variants like `tasks-2026-05-26.md` in v1.

Optional complex directories are allowed only after trigger conditions and human confirmation:

```text
tasks/
tests/
plans/
contracts/
```

Requirement set directory:

```text
agent-loop/requirements/YYYY-MM-DD-<topic>/
```

The date is the archive date only. It is not a deadline, feature duration, implementation start date, or implementation end date.

## Plan Lifecycle

`plan.md` is active, not archival.

It is the plan for the current task/story, while `tasks.md` is the durable ledger for the whole feature.

Do not rename `plan.md` to dated files. The design source requires stable core filenames. Use dated metadata inside the file:

```text
Plan ID: YYYY-MM-DD-<task-or-story>-<slug>
Created:
Updated:
Active Since:
Supersedes:
```

Allowed:

- replace it for the next task/story after important results are recorded in `notes.md`
- keep prior plan text only when it remains useful and concise

Required:

- record completed execution evidence in `notes.md`
- record completed or superseded plan cycles in `notes.md` under `Plan History`
- keep `tasks.md` as the durable status list
- update `plan.md` when switching to the next active task/story

## Complex Feature Rules

For large projects or features with many tasks:

- keep one feature directory
- keep `tasks.md`, `tests.md`, and `plan.md` as stable entry/index files
- group tasks by stage and barrier
- keep `plan.md` as the active pointer or compact active plan
- move finished task evidence to `notes.md`
- when complex artifact mode is triggered, put details in `tasks/`, `tests/`, and `plans/`

If the feature becomes too broad, split it into a new feature only after human confirmation.

## Borrowed Planning Discipline

Use these ideas without copying external directory structures:

- OpenSpec: active change has stable artifacts; close/archive records dated completion and merges lasting behavior into the source of truth.
- Spec Kit: implementation plan has a date, technical context, structure decision, gates, then tasks; tasks are grouped by phase/story with checkpoints.
- Superpowers: dated plan identity, exact files, exact verification commands, TDD steps, risks/rollback, and execution handoff.

In agent-loop this becomes:

```text
stable plan.md
+ dated Plan ID inside plan.md
+ completed plan cycle copied/summarized into notes.md Plan History
+ long-term behavior backfilled into project memory only when it affects future work
```

## Drift Rules

```text
current feature behavior changed -> update spec.md
feature product intent changed -> update product.md
cross-feature product consensus changed -> update project.md Product Context or Domain Language in simple mode, or project/product-context.md and project/domain-language.md in enterprise mode
task set/order changed -> update tasks.md
test strategy changed -> update tests.md
active execution changed -> update plan.md
actual execution/evidence changed -> update notes.md
confirmed producer-consumer API/event/public-data/UI-state/SDK-library/runtime interface changed -> update contracts.md and matching contracts/* detail after human confirmation; list affected consumers; ask human confirmation before accepting a breaking change
long-term project fact changed -> update project.md in simple mode, or matching project/*.md in enterprise mode
submission/integration happened -> update notes.md Submit / Integrate
new long-lived boundary directory created -> update project.md Directory Map in simple mode, or project/boundaries.md in enterprise mode, and propose directory AGENTS.md
old-project scan finding has low confidence -> record in project.md Onboarding Uncertainties in simple mode, or relevant enterprise detail uncertainty section, not as settled fact
```

Never overwrite human original requirements. Add a new file to the requirement set, create a new requirement set, or reference the original path.

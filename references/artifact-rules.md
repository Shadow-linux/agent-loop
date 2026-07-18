# Agent Loop Artifact Rules

## Source Of Truth

```text
agent-loop is the workflow source of truth.
Human original requirements remain source material, not mutable working docs.
Code reality wins when reconciling stale memory, but human confirms updates.
Code reality does not overwrite human original requirements.
```

Default root is `.agent-loop/`. If legacy `agent-loop/` exists, read it for the current run and ask before migration.

If the local directory is only a remote-project entry point, local `.agent-loop/remote.md` is the local entry source of truth. Full project memory should live next to the remote source of truth when remote writes are allowed. If remote writes are not allowed, use local-shadow mode and attach remote evidence to every code fact.

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
| `changes/YYYY-MM/YYYY-MM-DD-<topic>.md` Lightweight Execution Card | one bounded Change's background, scope, adaptive Plan, progress, verification, rollback, result, and Memory Review | project-memory fact ownership, shared backlog, Feature replacement, Bug lifecycle, Archive lifecycle, or Git authorization |
| `remote.md` | how to find, verify, and access a remote project from a local entry directory | feature logs or project capabilities |
| `project.md` | long-term project facts in simple mode; memory index/current state in enterprise mode; human-confirmed durable Branch Strategy and current Target Release Context pointer | task logs, backlog lists, deferred requirements, mutable development-branch lifecycle |
| `project/*.md` | enterprise long-term project memory details | feature execution logs |
| `decisions/*.md` | Human-gated project / cross-feature decision reasons, trade-offs, architecture design, consequences, and verification closure | ordinary execution logs, feature-local preferences, unresolved fuzzy requirement notes |
| `onboarding-db/*` | Evidence-Graph + DDD human-readable project understanding docs when created through `onboarding-knowledge-base.md`; old layouts are legacy evidence | current task status, feature execution logs, raw test output, human original requirements, project memory replacement |
| `requirements/<archive-date>-<topic>/*` | original human material package and lifecycle record: requirements, prototypes, feedback, screenshots, recordings, links, references, status, backlog/deferred state | edited specs, task plans |
| `bugs/INDEX.md` | Bug inventory, backlog, locator, and current summary row for every Bug ID | full reproduction, logs, discussion, Feature tasks, or project memory |
| `bugs/YYYY-MM-DD-<bug-slug>/README.md` | stable Bug identity, Report Origin, observed/expected evidence, Status, Resolution, relationships, Resolution Path, verification, close, and reopen history | product meaning, Requirement lifecycle, Feature tasks/tests/plan, personnel assignment, or Git authorization |
| `bugs/YYYY-MM-DD-<bug-slug>/evidence/*` | optional bounded screenshots, redacted logs, failed tests, reproduction, and verification evidence | secrets, complete production payloads, implementation plans, or executable state database |
| `product.md` | feature-level product intent, users, stories, product scope | engineering execution plan |
| `spec.md` | intended feature behavior | execution logs |
| `tasks.md` | work breakdown, status, and links to task details | full test evidence |
| `tests.md` | test design, matrix, and links to test details | raw test output |
| `plan.md` | active execution plan pointer or compact plan, including Branch Context Evidence when applicable | historical execution record or Git action authorization |
| `notes.md` | decisions, follow-up intake, Current Branch Context, evidence, drift, submit, pause/close | original requirements or durable branch policy |
| `contracts.md` | optional confirmed delivery contract index, compact contracts, status, and verification links | temporary subagent assignments |
| `tasks/*` | detailed task instructions when complex mode is triggered | feature-wide ledger |
| `tests/*` | detailed test cases when complex mode is triggered | raw test output |
| `plans/*` | dated plan cycles when complex mode is triggered | current-state summary |
| `handoffs/*` | subagent briefs and returned summaries when subagent mode is triggered | authoritative task status |
| `contracts/*` | optional confirmed durable producer-consumer contract details when interface detail is needed | temporary task logs |
| `features/archive.md` | Feature Monthly Archive locator and move ledger: stable Feature ID, current path, archive state, close date, one-line delivery locator, source/decision locators, last move | feature lifecycle, product meaning, requirement meaning, decision content, verification evidence |
| `memory-merges/MM-<collision-safe-short-sha>/README.md` | one full Merged Code SHA's Merge Context, complete Path Accounting Ledger, Human Decisions, exact Plan Hash, Apply, post-check, restore, and remaining-risk evidence | code merge, project encyclopedia, product/ADR meaning, Feature execution, or authorization for later Git actions |

The persisted Lightweight Execution Card is created under the one accepted memory root after clearly-eligible routing and before the first target write. Its month is the creation partition and never changes. The Agent checks the exact path before creation and uses the first free `-2`, `-3`, or later suffix in both filename and H1; it never truncates or overwrites an existing Change.

Do not add a Change README, INDEX, archive locator, per-change summary, move, rehydrate, restore transaction, scheduler, or shared counter. Planned multi-session work, pause/resume lifecycle, handoff, Subagent execution, long observation, complex evidence, or Feature-level tracking still requires Feature construction.

Lightweight Change status is exactly:

```text
in-progress | completed | stopped
```

Memory state uses two separate axes:

```text
Memory Review: pending | complete
Memory Result: pending | none | synced | human-review
```

Valid combinations are `in-progress + pending/pending`, `stopped + complete/none`, and `completed + pending/pending | complete/none | complete/synced | complete/human-review`. `pending: verification not complete` and `pending: classify at completion` are valid only for `in-progress`. A completed card requires Plan closure or explanation, fresh verification, diff/scope review, concrete rollback, Result / Residuals, actual Memory Evidence, and a candidate target or concrete undecided-target reason. `none` requires a concrete reason. Code-only completion is invalid.

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
- `skipped`: explicitly removed from the current feature scope after human-approved reconciliation; deferred work must first move to the owning requirement/phase backlog and leave current scope

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

Branch Strategy adoption status:

```text
accepted
declined
not-needed
```

An unconfirmed recommendation has no accepted status. The optional strategy uses `existing-project | human-guided-release | not-applicable` profile values; `not-applicable` is reserved for a human-confirmed `declined` outcome with a concrete reason. Release lifecycle distinguishes `open | released / sealed`; sealed is immutable. These values describe evidence and policy only, never Git action authorization.

Do not create a default `.agent-loop/branches/` directory. Durable policy and Target Release Context live in `project.md`; feature branch state lives in `notes.md`, `plan.md`, or Submit / Integrate evidence.

Bug Status and Resolution are independent:

```text
Bug Status: reported | triaging | confirmed | in-progress | verifying | deferred | closed
Bug Resolution: unresolved | fixed | duplicate | not-a-bug | cannot-reproduce | accepted-risk | superseded
Bug Resolution Path: investigate-first | flow-back | linked-feature | maintenance-fix | requirement | no-fix
```

`closed` cannot use `unresolved`; `deferred` is not closed; reopen is append-only and restores `unresolved`. `bugs/INDEX.md` owns the Bug backlog. Do not copy Open Bugs, Deferred Bugs, assignees, or reproduction logs into `project.md`.

An `in-progress` Bug requires `flow-back | linked-feature | maintenance-fix` plus one Human-confirmed Fix Feature Target. `investigate-first`, `requirement`, and `no-fix` must not use `Status: in-progress`.

## Feature Monthly Archive Layout

Feature ID is stable while its location may be flat or archived:

```text
features/<feature-id>/                 active, blocked, paused, recent closed, or rehydrated
features/YYYY-MM/<feature-id>/         Human-reviewed archived closed history
features/archive.md                    root locator and move ledger
```

Archive state is `archived | rehydrated`; archive state is not feature lifecycle. Lifecycle remains `draft | active | blocked | paused | closed`, and active / blocked / paused features stay flat.

Feature Monthly Archive moves the complete eligible directory without content compression. The scan is read-only. Apply requires the expected plan SHA-256 Batch Human Gate, transaction journal, exact precomputed reference edits, post-check, and restore. Original human requirement source files are never rewritten.

Scope boundaries are explicit: no per-feature archive summary, no historical/ directory, no Deep Archive, no deletion/packing/scheduled archive, and No `--force`. A closed archived feature must rehydrate before reopened execution.

Record the active gate mode in `project.md` Current Work or the active feature `notes.md` checkpoint. If scope changes, switch back to Strict Mode unless the human renews the auto-mode grant.

## Post-Merge Memory Reconciliation Layout

Create a report only after verified code integration and the Start Human Gate:

```text
.agent-loop/memory-merges/MM-<merged-code-short-sha>/README.md            default-root example
<memory-root>/memory-merges/MM-<collision-safe-short-sha>/README.md
<memory-root>/memory-merges/MM-<collision-safe-short-sha>/.memory-reconciliation-txn/  temporary only
```

One full Merged Code SHA owns exactly one durable report. Start the ID with 12 lowercase SHA characters and extend it only to avoid a collision with a different full SHA. Do not create `memory-merges/` during Init Project or Project Entry, and do not create a global transaction directory.

The current report directory may contain `.memory-reconciliation-txn/` only while Apply, post-check, or Restore is active. A successful finalize or proven restore removes transaction payloads after exact verification. A failed or unproven restore retains its journal and blocks later Apply and Git actions.

The report is an audit artifact, not a copy of canonical owners. Original human source, accepted Requirement/ADR/Human Decision meaning, append-only history, Feature/Bug state, enterprise project facts, and derived indexes remain owned by their existing artifacts.

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
.agent-loop/features/YYYY-MM-DD-<feature-slug>/
```

Maintenance fix feature directory:

```text
.agent-loop/features/YYYY-MM-DD-fix-<problem-slug>/
```

Do not create a separate `.agent-loop/maintenance/` root in v1. Maintenance fixes are narrow feature workspaces with `Feature Type: maintenance-fix`.

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
.agent-loop/requirements/YYYY-MM-DD-<topic>/
```

The date is the archive date only. It is not a deadline, feature duration, implementation start date, or implementation end date.

Bug directory:

```text
.agent-loop/bugs/YYYY-MM-DD-<bug-slug>/
```

Create `bugs/` only after explicit bug-record, manage, investigate, or fix intent. Do not create an empty Bug directory during Project Entry. Bug directories may contain `README.md` and optional `evidence/`; explicitly forbid `.agent-loop/bugs/<bug>/tasks.md`, `.agent-loop/bugs/<bug>/tests.md`, `.agent-loop/bugs/<bug>/plan.md`, and any Bug implementation subtree. Every code repair remains in a normal, follow-up, or maintenance-fix Feature workspace.

Onboarding-db directory:

```text
.agent-loop/onboarding-db/
```

New Evidence-Graph + DDD onboarding-db writes are allowed only through `references/onboarding-knowledge-base.md` after Project Entry Scan or reliable project memory and human confirmation of the Onboarding Spec.

Do not create, refresh, reorganize, or complete onboarding-db artifacts through the removed legacy flow. Existing legacy onboarding-db files may be read as evidence when present, but they are not trusted without code reality checks and do not replace `project.md` or root guidance. Migrate or replace legacy files only through an accepted Onboarding Spec, Onboarding Tasks, and Full Execution Gate.

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
Bug identity, evidence, Status, Resolution, Resolution Path, close, or reopen changed -> update the Bug README and its single matching bugs/INDEX.md row; keep history append-only
Feature repair evidence changed -> update Feature notes/tests plus the related Bug verification links; Feature tests do not auto-close the Bug
Requirement delivery truth changed because of Bug evidence -> run Human-gated Requirement Reconciliation; never rewrite the Requirement source or auto-change lifecycle
durable branch strategy or Target Release Context changed -> update project.md after human confirmation
feature Current Branch Context or branch-action evidence changed -> update notes.md / plan.md / Submit / Integrate record
confirmed producer-consumer API/event/public-data/UI-state/SDK-library/runtime interface changed -> update contracts.md and matching contracts/* detail after human confirmation; list affected consumers; ask human confirmation before accepting a breaking change
long-term project fact changed -> update project.md in simple mode, or matching project/*.md in enterprise mode
submission/integration happened -> update notes.md Submit / Integrate
new long-lived boundary directory created -> update project.md Directory Map in simple mode, or project/boundaries.md in enterprise mode, and propose directory AGENTS.md
old-project scan finding has low confidence -> record in project.md Project Entry Uncertainties in simple mode, or relevant enterprise detail uncertainty section, not as settled fact
```

Never overwrite human original requirements. Add a new file to the requirement set, create a new requirement set, or reference the original path.

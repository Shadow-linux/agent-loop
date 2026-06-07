# Onboarding Diagnostics

Use this when onboarding-db is being used to answer operational or impact questions:

- "I followed setup-and-run.md and it does not work."
- "What will break if I change this module/file/API?"
- "Who changes this state/status, and where?"
- "Why is this designed this way?"

This reference is for project understanding and onboarding. It does not replace normal feature debugging, TDD, or code review.

## Core Rules

- Read onboarding-db first, then inspect code reality only for the selected scope.
- Code reality is the current fact base; onboarding-db is the human-readable explanation layer.
- Do not silently update onboarding-db. Propose updates with Batch Human Review.
- Prefer focused tables and small diagrams over full repository graphs.
- Mark missing or uncertain findings as `Unknown` with evidence.

## Startup Failure Diagnosis

Use when the human cannot run the project by following `setup-and-run.md`.

Flow:

```text
reported failure -> read setup docs -> compare command/env/services -> inspect error -> identify blocker -> propose doc/code/environment action
```

Steps:

1. Ask for or read the exact command, working directory, error output, OS/runtime/container context, and whether dependencies were installed.
2. Read `setup-and-run.md`, `environment.md` or Compact equivalent, `verification-and-risks.md`, and any `Common Startup Failures`.
3. Compare documented prerequisites with reality: package manager, language version, env files, ports, required services, database/cache/queue, auth/seed data, containers, tunnels, and remote/local mode.
4. Classify the failure:
   - stale setup docs
   - missing dependency
   - missing required service
   - environment variable/config issue
   - port/auth/data/seed issue
   - command path or working-directory issue
   - known baseline failure
   - code/runtime bug
   - unknown
5. Recommend exactly one next action: fix local environment, run a missing prerequisite, update setup docs, route to normal Diagnose Failure, or ask human for missing access.
6. If the setup docs are stale or incomplete, propose an onboarding-db update through Batch Human Review.

Output table:

| Check | Documented | Observed | Evidence | Judgment | Next Action |
|---|---|---|---|---|---|

If updating docs, update:

- `setup-and-run.md` for local run commands, prerequisites, ports, and Common Startup Failures
- `environment.md` or Compact equivalent for env/config differences
- `deployment-and-operations.md` only for production/release/ops concerns
- `verification-and-risks.md` for baseline failures or known blockers

## Change Impact Analysis

Use when the human asks "if I change this, will something break?"

Inputs can be a module, file, flow, API, data field, job, UI route, or natural-language change.

Read order:

1. `README.md` reading path and module path
2. `change-impact-map.md` or `verification-and-risks.md` Change Impact Map
3. relevant module doc or `module-map.md`
4. relevant flow doc or `core-flows.md`
5. API/contract/integration docs when a boundary is involved
6. related tests and verification commands
7. code reality for the focused scope only when docs are missing, stale, or ambiguous

Analyze:

- affected modules and files
- affected APIs/contracts/events/public data
- affected data/state/migrations
- affected jobs/async flows/external services
- tests and manual verification to run
- likely risk level and unknowns
- whether a Delivery Contract, Targeted Onboarding Scan, or Project Memory Backfill is needed

Output table:

| Change Area | Affected Modules | Affected Files | APIs / Contracts | Data / State | Jobs / Async / External | Tests / Verification | Risks | Evidence | Follow-Up |
|---|---|---|---|---|---|---|---|---|---|

Rules:

- Do not claim impact is complete if evidence is weak.
- Do not inspect the entire repo by default.
- If the question is feature work, route back to normal Feature Spec / Work Breakdown after the impact summary.
- If onboarding-db lacks this impact path, propose a `change-impact-map.md` or relevant section update.

## State Change Trace

Use when the human asks who or what changes a state/status field, for example:

```text
Who changes order.status from pending to failed?
Where is meeting.status updated?
What triggers this state transition?
```

This is different from a state-flow diagram. A state-flow diagram shows legal transitions; a State Change Trace shows observed writers, triggers, side effects, and evidence.

Read order:

1. `flows-and-data.md`, `data-model.md`, or Compact equivalent
2. relevant `state-flow-<entity>.md` diagram if present
3. relevant module/flow docs
4. job/async/integration docs when state changes happen in workers or callbacks
5. focused code search for the state field, update method, model, table, event, or status enum

Trace fields:

| Field | Meaning |
|---|---|
| State Field | entity and field name |
| From / To | transition being investigated |
| Trigger | user action, API, job, event, callback, migration, retry, manual action |
| Writer | file/function/module/system that performs the update |
| Guard / Condition | permissions, validation, preconditions |
| Side Effects | emitted events, jobs, notifications, external calls |
| Failure / Compensation | retries, rollback, DLQ, manual repair |
| Tests | tests or scenarios covering the transition |
| Evidence | code/doc/log/config paths |
| Confidence | high / medium / low |

Output table:

| Transition | Trigger | Writer | Guard / Condition | Side Effects | Tests | Evidence | Confidence |
|---|---|---|---|---|---|---|---|

Rules:

- If no writer is found, say `Unknown`, list searched evidence, and recommend a targeted scan.
- Do not infer business reason from code alone. Use decisions/history docs or ask the human.
- If a stable trace is discovered, propose updates to `data-model.md`, `flows-and-data.md`, `state-flow-<entity>.md`, or the relevant flow/module docs.

## Design Decision Routing

Use when the human asks why something was designed a certain way.

Read:

- `decisions-and-history.md`, or Compact equivalent in `architecture-and-integrations.md`
- relevant architecture/module/flow docs
- evidence such as README, ADR-like docs, issues, PRs, commits, comments, or human-confirmed history

Rules:

- Code can prove what exists now; it usually cannot prove why it was chosen.
- If the reason is not evidenced, mark it `Unknown` and ask the human.
- If a durable reason is confirmed, propose a `decisions-and-history.md` update.

Output table:

| Design Question | Current Shape | Known Reason | Alternatives | Consequences | Evidence | Confidence |
|---|---|---|---|---|---|---|

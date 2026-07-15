# Feature Follow-up And Flow-back

Use this when a human reports a bug, regression, test failure, algorithm change, field/schema change, behavior tweak, or post-close correction that may relate to existing Feature work. For explicit bug-record, manage, investigate, or fix intent, load `references/bug-management.md`; Bug Management is the internal intake/triage method and this reference owns Feature relationship routing.

## Purpose

Closed Features are not dead history. If a Bug or change clearly belongs to an existing delivered Feature, the agent should actively propose flowing the work back to that Feature so the original spec, tasks, tests, evidence, and project memory stay coherent.

The human does not need to know whether to say "reopen feature", "new feature", or "drift". The agent owns the classification and recommends one next action.

Feature Follow-up requires existing agent-loop memory. If `.agent-loop/` or legacy `agent-loop/` is missing, do not run this stage directly. First route through Project Entry Scan or Init Project, preserve the bug/change report as intake context, and return to Feature Follow-up only after project memory and feature history can be inspected.

## Trigger Phrases

Route here when the human says or implies:

- "测试发现 bug", "有个 bug", "回归了", "之前做完的功能有问题"
- "这个字段要改", "算法要改", "接口返回要调整", "规则微调", "不是新功能"
- "行为要调一下", "需要改一下", "小改一下", "这个体验/文案/逻辑微调一下", "验收标准要改"
- "behavior tweak", "small tweak", "quick tweak", "minor adjustment", "change the requirement", "update the acceptance criteria"
- "上次那个功能", "最近做的功能", "关闭后发现"
- "线上/联调/验收发现问题"
- error screenshots, browser screenshots, logs, stack traces, failing tests, API mismatch, E2E failure, or user feedback tied to active, paused, closed, or recent feature work

Also route here after Verify, Review, Drift Check, or Submit reveals a defect likely tied to a recent feature.

## Lookback Window

Bug Index metadata has no time cutoff. Scan the complete Bug inventory for duplicate and reopen identity before comparing Feature ownership.

Default recent window: **90 calendar days** from the current date.

Inspect:

- `project.md` Active Feature, Paused Features, and recent feature references
- complete `bugs/INDEX.md` metadata plus the current README for evidence-overlapping Bug candidates
- flat recent `.agent-loop/features/<feature-id>/` metadata and scope summary before deep-reading `spec.md`, `tasks.md`, `tests.md`, and `notes.md`
- root `.agent-loop/features/archive.md` after Active/Paused and flat recent candidates
- archived `.agent-loop/features/YYYY-MM/<feature-id>/` artifacts only after the locator row resolves uniquely
- close records, submit records, verification evidence, and drift notes
- code paths, tests, APIs, data models, or UI routes mentioned by the bug/change
- screenshot text, visible UI labels, error messages, stack traces, request/response samples, logs, test names, and file paths attached to the report

Calculate Feature age from `Last Updated / Closed`, not archive month, directory mtime, or archive operation time. Deep-read only candidates whose scope, path, API, model, UI, job, test, Requirement, ADR, Contract, or verification evidence overlaps the Bug.

The 90-day window is a default metadata scan, not a hard ownership boundary. If the report names an older Feature or its path/API/model/UI/job/test/Requirement/ADR evidence, run an extended scan before creating a new Feature or maintenance fix. Mark the candidate `outside-default-window` and explain the evidence trigger.

Do not use day 91 as a reason to stop ownership analysis. If evidence is weak after the extended scan, keep the Bug `triaging`, classify ownership as `unclear`, and recommend `investigate-first` rather than guessing. Multiple medium/high candidates also remain `investigate-first`.

## Archived Feature Owners

Feature Monthly Archive changes location, not Feature identity or ownership. Lookup order is fixed: complete Bug Index identity scan, Active/Paused pointers, flat Feature metadata in the 90-day window, `features/archive.md`, evidence-ranked archived artifacts, then evidence-driven extended candidates.

Resolve the locator uniquely, then read archived `spec.md`, `tests.md`, `notes.md`, close evidence, and verification evidence without mutation. Discovery, duplicate/reopen analysis, ownership classification, and Human Review do not require rehydrate.

When an archived closed Feature is the Human-confirmed `flow-back` owner and repair execution is about to start, the invariant remains: rehydrate before reopened execution. First run a read-only rehydrate scan, show the exact plan SHA-256 Batch Human Gate, then use the transaction journal, reference updates, post-check, and restore rules. Only after verified rehydrate may Feature Follow-up ask to change lifecycle from `closed` to `active` or start tasks. Archive state is not Feature lifecycle.

If the archive row target is missing, a month directory lacks its row, the same Feature ID exists flat and archived, a `rehydrated` row points to a month path, or `.archive-txn` is incomplete, stop and route to Recovery instead of guessing ownership.

## Low-information Reports

Some reports are too generic to identify feature ownership by themselves:

- "500 Internal Server Error"
- blank page / white page
- "unknown error"
- "it failed" without route, action, request, stack trace, or failing test
- screenshots with no feature-specific UI label, field, route, API, model, job, or error text

Rules:

- Do not assign `high` match strength from a generic error alone.
- Do not reopen the nearest recent feature only because it is recent.
- Classify as `unclear` when the report lacks feature-specific evidence.
- Recommend `investigate-first` with one targeted next action, such as collecting route/action/time, checking server logs, reproducing with the reported input, reading the failing test, or running a Targeted Feature Scan for the affected route/API/job.
- Only upgrade the match after concrete evidence links the failure to a feature's files, API, data model, UI route, job, test, acceptance criteria, or verification notes.

## Classification

Use this table:

| Class | Meaning | Recommended Action |
|---|---|---|
| `same-feature-bug` | defect in behavior that the feature promised or changed | flow back to that feature |
| `same-feature-adjustment` | field, algorithm, copy, UX, API, or acceptance change within the original feature intent | flow back if scope is still coherent; otherwise create linked new feature |
| `regression-from-feature` | recent feature likely broke existing behavior | flow back to recent feature and add regression task/test |
| `new-feature` | new capability, new user goal, or broad scope not covered by recent feature | create a new feature and optionally link related old feature |
| `maintenance-fix` | internal fix with no meaningful product feature ownership | create a narrow `Feature Type: maintenance-fix` feature after human confirmation |
| `unclear` | insufficient evidence | ask one focused question or run Targeted Feature Scan |

For an explicit Bug, this Feature classification feeds one Bug Resolution Path recommendation: `investigate-first | flow-back | linked-feature | maintenance-fix | requirement | no-fix`. Do not create/reopen a Feature or change a Requirement until the named Resolution Path and subsequent action gate are confirmed.

## Requirement-change Ambiguity

Human wording such as "这个字段改一下", "规则微调", "小改动", or "不是新功能" is useful evidence, but it is not enough by itself.

Before classifying a change as `same-feature-adjustment`, check whether it changes:

- accepted behavior or business rule
- API/event/data shape or field meaning
- state transition or workflow outcome
- algorithm result or ranking/scoring decision
- visible UX behavior that users rely on

If the answer is unclear, ask one focused question or mark the classification `unclear` and route to `investigate-first`. If the human confirms it changes original acceptance within the same user goal, update `spec.md` and `tests.md` before execution. If it creates an independent user capability or broad new product decision, recommend a linked `new-feature`.

## Candidate Match Matrix

Before writing or changing feature docs, present a table:

| Candidate Feature | Status | Last Updated / Closed | Match Evidence | Match Strength | Recommended Flow |
|---|---|---|---|---|---|

Match evidence can include:

- overlapping files, routes, models, APIs, jobs, UI pages, or tests
- screenshot-visible UI labels, error text, stack traces, logs, request/response fields, or failing test names that map to a feature
- acceptance criteria mentioning the failing behavior
- tasks that changed the relevant code path
- notes/verification evidence from recent delivery
- related Delivery Contracts
- human wording such as "上次那个功能"

Match strength:

```text
high | medium | low
```

When multiple candidates have medium/high match because evidence is incomplete, recommend `investigate-first` and route to Targeted Feature Scan or Diagnose Failure before updating feature ownership or docs.

Ask the human only when evidence is sufficient and the remaining choice is a product or ownership decision. Present the evidence-backed alternatives and recommend one default; do not use Ask Human merely because investigation is unfinished.

## Flow-back Rules

Flow back to an existing feature when:

- the change repairs or adjusts behavior created by that feature
- the fix is needed to make that feature honestly complete
- acceptance criteria, tests, or implementation evidence for that feature are now incomplete or wrong
- a recent feature caused a regression in adjacent behavior
- a requirement change modifies the feature's existing acceptance criteria, algorithm, field semantics, API shape, or visible behavior without creating an independent user capability

Do not flow back when:

- the work creates a separate user capability
- the change crosses unrelated feature boundaries
- the owning feature is uncertain and evidence is weak
- flowing back would hide a new product decision that needs its own Feature Spec

## Maintenance Fix Feature

Use this when no recent feature owns the report, or when the human explicitly declines flow-back and the work is still a narrow fix rather than a new product capability.

Maintenance fix is a feature type, not a separate artifact root:

```text
.agent-loop/features/YYYY-MM-DD-fix-<slug>/
  spec.md    Feature Type: maintenance-fix
  tasks.md
  tests.md
  plan.md
  notes.md
```

Rules:

- Do not make naked code changes just because no owning feature was found.
- Do not create a separate `.agent-loop/maintenance/` tree in v1.
- Keep `spec.md` small, but include the problem, why it is not flow-back, why it is not a new product feature, regression/safety risk, and long-term memory impact.
- `tasks.md` should contain a narrow repair task and a regression/safety verification task when applicable.
- `tests.md` must include regression coverage or a recorded substitute verification with risk and human decision.
- `notes.md` records diagnosis, evidence, review, drift decision, and close record.
- If the human declined flow-back from a candidate feature, `spec.md` or `notes.md` must record `Related Feature`, `Flow-back Decision: declined-reopen`, and the reason. Link or copy the relevant acceptance, tests, evidence, and affected paths so continuity is not lost.
- If the fix changes long-term commands, architecture boundaries, data model, API/event/UI behavior, permissions, deployment, testing strategy, or domain language, Project Memory Update is required.
- Close requires the normal completion gate: fresh verification, review, drift check, project memory update status, Feature Completion Check, and human confirmation.

When recommending maintenance fix, present:

| Proposed Feature | Why Not Flow-back | Why Not New Product Feature | Verification Needed | Project Memory Impact | Human Decision |
|---|---|---|---|---|---|

## Reopening A Closed Feature

Closed features may receive follow-up work, but never silently.

If the owning feature is closed:

1. Recommend `flow-back` as the decision and explain that it means reopening or continuing the owning feature for follow-up work.
2. Explain why this is better than a new feature.
3. Ask human confirmation before changing status or adding work.
4. Record the Follow-up Intake in `notes.md`.
5. Update `spec.md`, `tasks.md`, `tests.md`, and `plan.md` only as needed. Requirement changes that alter acceptance, field meaning, API shape, algorithm behavior, or visible UX must update `spec.md` and `tests.md` before execution.
6. Move the feature to `Active Feature` and set its lifecycle status to `active`.
7. Execute through normal Plan Gate, TDD, Verify, Review, Drift Check, Project Memory Update, Feature Completion Check, and Close.

Do not erase the original Close Record. Add a new follow-up section and a new Close Record when the follow-up is complete.

If the human declines reopening a closed feature:

1. Preserve the old feature close state.
2. Create a linked new feature or maintenance-fix feature only after human confirmation.
3. Record `Related Feature`, `Flow-back Decision: declined-reopen`, and `Declined Flow-back Reason`.
4. Link or copy the relevant acceptance criteria, tests, verification evidence, affected files/routes/APIs/models/jobs, and risk notes into the new workspace.
5. Keep the new work under the normal gates: spec/tasks/tests/plan, verification, review, drift, project memory impact, Feature Completion Check, and close.

Human preference not to reopen is respected, but it must not break traceability.

## Updating Artifacts

Use these targets:

```text
new human bug/change material -> requirements/<archive-date>-<topic>/ or notes.md, depending on source durability
explicit Bug identity/evidence/lifecycle -> bugs/INDEX.md plus bugs/YYYY-MM-DD-<bug-slug>/README.md
bug/change classification -> feature notes.md
changed acceptance or behavior -> spec.md
new repair/regression work -> tasks.md or tasks/<story>/<task>.md
new regression/API/E2E cases -> tests.md or tests/<case>.md
active execution unit -> plan.md or plans/<date>-<task>.md
maintenance fix with no owning feature -> new `features/YYYY-MM-DD-fix-<slug>/` with `Feature Type: maintenance-fix`
long-term product/project fact -> project.md or enterprise project/*.md
downstream API/event/data/UI contract impact -> contracts.md and contracts/* after human confirmation
```

Original requirement files remain immutable. If human feedback is durable source material, archive it under `.agent-loop/requirements/` after confirmation.

## Follow-up Intake Record

Add this to `notes.md`:

```md
## Follow-up Intake

- Date:
- Source: human report | test failure | E2E | API verification | production/QA feedback | other
- Report:
- Candidate Features:
- Related Bugs:
- Bug Status At Start:
- Bug Resolution Path:
- Classification: same-feature-bug | same-feature-adjustment | regression-from-feature | new-feature | maintenance-fix | unclear
- Lookback Window: 90 days | outside-default-window
- Match Evidence:
- Related Feature:
- Flow-back Decision: flow-back | linked-new-feature | maintenance-fix | investigate-first | declined-reopen | defer
- Declined Flow-back Reason:
- Human Decision:
- Artifact Updates:
- Next Stage:
```

## Human Gate

Always ask before:

- confirming a Bug Resolution Path
- closing or reopening a Bug Record
- reopening a closed feature
- changing feature scope or acceptance criteria
- creating a new feature instead of flowing back
- adding or changing Delivery Contracts
- accepting a breaking API/event/data/UI behavior change
- marking the follow-up complete or closing the feature again

Feature Auto-Loop may continue only after the human confirms the flow-back decision and any updated spec/tasks/tests are accepted. Auto modes still stop at all normal stop conditions.

## Completion

A follow-up is complete only when:

- related Bug Records expected to be fixed are `verifying` with fresh Bug-specific evidence; Bug Close remains a separate Human Gate
- bug/change is represented in spec/tasks/tests/notes
- required tests or substitute verification are fresh and recorded
- review and drift checks are recorded
- project memory is updated when long-term facts changed
- feature completion check passes
- human confirms close if the feature was reopened

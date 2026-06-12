# Feature Follow-up And Flow-back

Use this when a human reports a bug, regression, test failure, algorithm change, field/schema change, behavior tweak, or post-close correction that may relate to recent feature work.

## Purpose

Closed features are not dead history. If a bug or change clearly belongs to a recently delivered feature, the agent should actively propose flowing the work back to that feature so the original spec, tasks, tests, evidence, and project memory stay coherent.

The human does not need to know whether to say "reopen feature", "new feature", or "drift". The agent owns the classification and recommends one next action.

## Trigger Phrases

Route here when the human says or implies:

- "测试发现 bug", "有个 bug", "回归了", "之前做完的功能有问题"
- "这个字段要改", "算法要改", "接口返回要调整"
- "上次那个功能", "最近做的功能", "关闭后发现"
- "线上/联调/验收发现问题"
- error screenshots, browser screenshots, logs, stack traces, failing tests, API mismatch, E2E failure, or user feedback tied to active, paused, closed, or recent feature work

Also route here after Verify, Review, Drift Check, or Submit reveals a defect likely tied to a recent feature.

## Lookback Window

Default recent window: **30 calendar days** from the current date.

Inspect:

- `project.md` Active Feature, Paused Features, and recent feature references
- `.agent-loop/features/*/spec.md`
- `.agent-loop/features/*/tasks.md`
- `.agent-loop/features/*/tests.md`
- `.agent-loop/features/*/notes.md`
- close records, submit records, verification evidence, and drift notes
- code paths, tests, APIs, data models, or UI routes mentioned by the bug/change
- screenshot text, visible UI labels, error messages, stack traces, request/response samples, logs, test names, and file paths attached to the report

If the likely owning feature is older than 30 days but the evidence is strong, still recommend a flow-back candidate and mark it `outside-default-window`.

The 30-day window is a default scan window, not a hard ownership boundary. If the report mentions "上个月", "之前那个", "上次那个", "the previous feature", an old ticket/feature name, or a code/API/test/data path that clearly overlaps an older feature, run an extended candidate scan before creating a new feature or maintenance fix. Mark the candidate `outside-default-window` and explain why it was considered.

Do not use day 31 as a reason to stop flow-back analysis. If evidence is weak after the extended scan, classify as `unclear` and recommend `investigate-first` rather than guessing.

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

If more than one candidate has medium/high match, ask the human to choose before updating docs.

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
- Keep `spec.md` small, but include the problem, why it is not flow-back, why it is not a new product feature, regression risk, and long-term memory impact.
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
6. Move the feature to active or follow-up-active in `project.md`.
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
- Classification: same-feature-bug | same-feature-adjustment | regression-from-feature | new-feature | maintenance-fix | unclear
- Lookback Window: 30 days | outside-default-window
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

- reopening a closed feature
- changing feature scope or acceptance criteria
- creating a new feature instead of flowing back
- adding or changing Delivery Contracts
- accepting a breaking API/event/data/UI behavior change
- marking the follow-up complete or closing the feature again

Feature Auto-Loop may continue only after the human confirms the flow-back decision and any updated spec/tasks/tests are accepted. Auto modes still stop at all normal stop conditions.

## Completion

A follow-up is complete only when:

- bug/change is represented in spec/tasks/tests/notes
- required tests or substitute verification are fresh and recorded
- review and drift checks are recorded
- project memory is updated when long-term facts changed
- feature completion check passes
- human confirms close if the feature was reopened

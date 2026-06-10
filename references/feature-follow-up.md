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
- a failing test, API mismatch, E2E failure, or user feedback after a feature was closed

Also route here after Verify, Review, Drift Check, or Submit reveals a defect likely tied to a recent feature.

## Lookback Window

Default recent window: **15 calendar days** from the current date.

Inspect:

- `project.md` Active Feature, Paused Features, and recent feature references
- `.agent-loop/features/*/spec.md`
- `.agent-loop/features/*/tasks.md`
- `.agent-loop/features/*/tests.md`
- `.agent-loop/features/*/notes.md`
- close records, submit records, verification evidence, and drift notes
- code paths, tests, APIs, data models, or UI routes mentioned by the bug/change

If the likely owning feature is older than 15 days but the evidence is strong, still recommend a flow-back candidate and mark it `outside-default-window`.

## Classification

Use this table:

| Class | Meaning | Recommended Action |
|---|---|---|
| `same-feature-bug` | defect in behavior that the feature promised or changed | flow back to that feature |
| `same-feature-adjustment` | field, algorithm, copy, UX, API, or acceptance change within the original feature intent | flow back if scope is still coherent; otherwise create linked new feature |
| `regression-from-feature` | recent feature likely broke existing behavior | flow back to recent feature and add regression task/test |
| `new-feature` | new capability, new user goal, or broad scope not covered by recent feature | create a new feature and optionally link related old feature |
| `maintenance-fix` | internal fix with no meaningful product feature ownership | create a narrow maintenance feature or task after human confirmation |
| `unclear` | insufficient evidence | ask one focused question or run Targeted Feature Scan |

## Candidate Match Matrix

Before writing or changing feature docs, present a table:

| Candidate Feature | Status | Last Updated / Closed | Match Evidence | Match Strength | Recommended Flow |
|---|---|---|---|---|---|

Match evidence can include:

- overlapping files, routes, models, APIs, jobs, UI pages, or tests
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

Do not flow back when:

- the work creates a separate user capability
- the change crosses unrelated feature boundaries
- the owning feature is uncertain and evidence is weak
- flowing back would hide a new product decision that needs its own Feature Spec

## Reopening A Closed Feature

Closed features may receive follow-up work, but never silently.

If the owning feature is closed:

1. Recommend `reopen-for-follow-up`.
2. Explain why this is better than a new feature.
3. Ask human confirmation before changing status or adding work.
4. Record the Follow-up Intake in `notes.md`.
5. Update `spec.md`, `tasks.md`, `tests.md`, and `plan.md` only as needed.
6. Move the feature to active or follow-up-active in `project.md`.
7. Execute through normal Plan Gate, TDD, Verify, Review, Drift Check, Project Memory Update, Feature Completion Check, and Close.

Do not erase the original Close Record. Add a new follow-up section and a new Close Record when the follow-up is complete.

## Updating Artifacts

Use these targets:

```text
new human bug/change material -> requirements/<archive-date>-<topic>/ or notes.md, depending on source durability
bug/change classification -> feature notes.md
changed acceptance or behavior -> spec.md
new repair/regression work -> tasks.md or tasks/<story>/<task>.md
new regression/API/E2E cases -> tests.md or tests/<case>.md
active execution unit -> plan.md or plans/<date>-<task>.md
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
- Lookback Window: 15 days | outside-default-window
- Match Evidence:
- Human Decision: flow-back | new-feature | maintenance | investigate-first | defer
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

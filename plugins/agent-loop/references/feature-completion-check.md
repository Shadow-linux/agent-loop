# Feature Completion Check

Use this when a feature might be finished but not explicitly closed.

## Purpose

Humans may interrupt or redirect the agent at any time. They should not need to know the word `close` or remember whether the previous feature is formally complete. The agent must actively check completion state and recommend close, pause, or the next unfinished item.

## Trigger Points

Run this check:

- after Verify, Review, Drift Check, and Project Memory Update indicate work may be complete
- before starting a new feature while another feature is active
- during resume when `project.md` has an Active Feature
- after Submit / Integrate when the feature appears done
- when the human says "continue", "what next", "start a new feature", or similar and an active feature exists

## Read

- `project.md` Current Work
- active feature `spec.md`
- active feature `tasks.md`
- active feature `tests.md`
- active feature `plan.md`
- active feature `notes.md`
- active feature `contracts.md` and linked `contracts/*` details when present
- linked detail files only when needed

## Completion Questions

Check:

- Is the feature spec accepted?
- Are all in-scope tasks done, skipped with reason, or explicitly removed from scope?
- Are all required tests or substitute verification recorded?
- Is there fresh verification evidence in `notes.md`?
- Did Feature Close Review complete?
- Did feature-level Spec Review confirm `product.md` when present, `spec.md`, `tasks.md`, `tests.md`, acceptance criteria, and out-of-scope boundaries are satisfied?
- Did feature-level Standards Review complete when triggered by large project, broad diff, boundary/security/data change, architecture change, or human request?
- Did Drift Check complete?
- Are feature docs aligned with implementation reality?
- Are Delivery Contracts implemented and verified when downstream consumers rely on them?
- Are accepted Delivery Contracts aligned with producer code and tests, with no unapproved breaking changes?
- Are long-term facts reflected in `project.md` for simple mode, or the matching `project/*.md` detail files for enterprise mode?
- Is submit/integration status recorded when the human requested submit/commit/PR?
- Are there unresolved Human-gated decisions, blockers, or open questions?

## Outcomes

### Recommend Close

Use when all completion questions pass.

Say:

```text
This feature appears complete. I recommend closing it after your confirmation.
```

Then list evidence and ask for explicit close confirmation.

Do not close automatically, even in Feature Auto-Loop.

Do not recommend close if Feature Close Review is missing. Recommend Review as the next stage instead.

### Recommend Next Unfinished Item

Use when work remains.

Say:

```text
This feature is not ready to close. The next unfinished item is <item>.
```

Then recommend exactly one next stage.

### Recommend Pause Before New Feature

Use when the human wants a new feature but the current feature is incomplete or intentionally deferred.

Say:

```text
There is still an active feature. I can pause it with a resume point before starting the new feature.
```

Record the resume point after confirmation.

### Recommend Scope Update

Use when remaining work is no longer desired.

Say:

```text
If this remaining work is no longer part of the feature, I should update scope/tasks/tests before close.
```

Route to Drift Check or Feature Spec update before close.

## Start-New-Feature Guard

Before creating a new feature, if `project.md` has an Active Feature:

1. Run Feature Completion Check.
2. If complete, recommend close first.
3. If incomplete, ask whether to continue, pause, or revise scope.
4. Only start the new feature after the current feature is closed or paused, unless the human explicitly chooses to keep multiple active features.

## Resume Guard

On resume, if an Active Feature exists:

1. Read the active feature docs.
2. Run Feature Completion Check.
3. Recommend either close, continue the next unfinished item, pause, or start a new feature after handling the active one.

## Notes Record

Record the check in `notes.md`:

```md
## Feature Completion Check

- Date:
- Result: recommend-close | continue | pause-before-new-feature | update-scope | blocked
- Evidence:
- Feature Close Review:
- Remaining Work:
- Drift:
- Project Memory:
- Submit Status:
- Recommendation:
- Human Decision:
```

If the feature is closed, also write the final `Close Record`.

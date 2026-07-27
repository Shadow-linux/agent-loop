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
- effective Requirement `product.md` resolved through the Requirement Set README, or the accepted legacy source for older work
- existing legacy Feature `product.md` when present; absence is expected for new work
- active feature `tasks.md`
- active feature `tests.md`
- active feature `plan.md`
- active feature `notes.md`
- accepted Decision & Design records linked by the feature
- active feature `contracts.md` and linked `contracts/*` details when present
- related Bug README files and matching `bugs/INDEX.md` rows when the Feature resolves Bugs
- linked detail files only when needed

## Completion Questions

Check:

- Is the feature spec accepted?
- Are all remaining in-scope tasks `done`?
- Were skipped or deferred items first removed from current scope through human-approved spec/tasks/tests/requirement reconciliation?
- Are all required tests or substitute verification recorded?
- Is there fresh verification evidence in `notes.md`?
- Did Feature Close Review complete?
- Did feature-level Spec Review confirm the Requirement Product Definition, Feature Spec Product Slice, `tasks.md`, `tests.md`, acceptance criteria, and out-of-scope boundaries are satisfied, plus any existing legacy Feature `product.md` when present?
- Does every Product Slice row still resolve to the effective source without redefining product meaning, and is any source change routed through compatibility/drift review?
- Did feature-level Standards Review complete when triggered by large project, broad diff, directory or durable boundary change, security/data change, architecture change, or human request?
- Did Drift Check complete?
- Are feature docs aligned with implementation reality?
- Do all design slices assigned to this feature have implementation and verification evidence?
- Does implementation conform to accepted Decision & Design records, or has any divergence returned to Decision & Design / Drift Check for human review?
- Are Delivery Contracts implemented and verified when downstream consumers rely on them?
- Are accepted Delivery Contracts aligned with producer code and tests, with no unapproved breaking changes?
- Are long-term facts reflected in `project.md` for simple mode, or the matching `project/*.md` detail files for enterprise mode?
- Is submit/integration status recorded when the human requested submit/commit/PR?
- Is every related Bug expected to be fixed in `verifying` with fresh Bug-specific reproduction/substitute and regression/safety evidence?
- Are Bug Status/Resolution/Resolution Path and the Fix Feature consistent with the current Index, Feature, Requirement, ADR, Contract, and archive locator evidence?
- Are there unresolved Human-gated decisions, blockers, or open questions?

Feature close is blocked until all assigned design slices have implementation and verification evidence, or a human-approved decision explicitly reassigns, defers, removes, or supersedes the slice.

Bug verification and Feature completion are connected but not collapsed. Passing Feature tests can move a related Bug to `verifying`; it cannot close the Bug. At completion, present separately named decisions:

```text
Bug Close Decision: confirm | revise | keep-verifying
Feature Close Decision: confirm | continue | pause | revise-scope
```

One summary may request both decisions, but neither authorization is inferred from the other. If Bug close is not confirmed, do not claim the Bug resolution loop complete; keep the Bug `verifying` or route to the required evidence/repair stage.

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

### Recommend Blocked

Use when completion cannot be decided or continued because a human decision, environment, access, verification dependency, or external blocker is missing.

Say:

```text
This feature is blocked from completion. The blocker is <blocker>.
```

Recommend exactly one next stage: Ask Human, Diagnose Failure, Verify, Pause, or Targeted Feature Scan.

Record the blocker, evidence, owner if known, and the next unblock action in `notes.md`. Do not recommend close while the blocker remains.

## Blocked Routing Matrix

Apply the first matching blocker route using the same order as runtime:

1. observed failure or unclear technical cause -> Diagnose Failure
2. required verification not run but runnable in the available environment -> Verify
3. missing human decision/access/approval required for the next safe action -> Ask Human
4. unclear ownership/impact -> Targeted Feature Scan
5. external blocker with no immediate unblock path -> Pause

## Start-New-Feature Guard

Before creating a new feature, if `project.md` has an Active Feature:

Agent Loop permits at most one Active Feature. Other resumable features must be paused with a recorded resume point.

1. Run Feature Completion Check.
2. If complete, recommend close first.
3. If incomplete, ask whether to continue, pause, or revise scope.
4. Only start the new feature after the current feature is closed or paused. Do not keep multiple active features.

## Resume Guard

On resume, if an Active Feature exists:

1. Read the active feature docs.
2. Run Feature Completion Check.
3. Recommend either close, continue the next unfinished item, pause, or start a new feature after handling the active one.

If no Active Feature exists and the human asks to resume paused work:

1. Use the named paused feature, or ask which one only when more than one paused feature remains and intent does not identify it.
2. Read its feature docs and recorded resume point.
3. Move the selected feature from `Paused Features` to `Active Feature` in `project.md` and remove its paused entry.
4. Set the feature lifecycle status to `active` and record the resume transition in `notes.md`.
5. Resume in Strict Mode unless the human separately re-enables an auto mode after reviewing current scope and stop conditions. Preserve the historical Gate 2 decision/Auto-Loop baseline and any Later Start evidence; use project `Gate Mode` plus the recorded pause/resume transition for current-mode state.
6. Run Feature Completion Check before continuing the recorded next stage.

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
- Related Bugs / Status:
- Bug Verification Evidence:
- Bug Close Decision: confirm | revise | keep-verifying | not-applicable
- Feature Close Decision: confirm | continue | pause | revise-scope
- Recommendation:
- Human Decision:
```

If the feature is closed, also write the final `Close Record`.

The same close update writes this deterministic Feature Monthly Archive readiness block in `notes.md`; it does not auto-archive and does not add a new Close Human Gate:

```md
## Archive Readiness

Closed At: <same concrete date as Close Record>
Delivered Summary: <one concrete line describing delivered behavior>
Verification: complete
Feature Close Review: complete
Drift: resolved
Project Memory Impact: complete | none
Open Follow-up: none | <FU-001, FU-002>
```

Only `Open Follow-up: none` is eligible for Feature Monthly Archive. Missing blocks, placeholder summaries, non-terminal values, or listed follow-up IDs remain blocked until a human-reviewed close-note correction; the archive scan never infers or rewrites them.

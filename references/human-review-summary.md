# Human Review Summary

Use this before asking the human to approve or confirm an `agent-loop` stage.

## Purpose

Humans approve decisions, scope, risk, and next actions. They should not need to read a full execution document every time. The agent should present a compact approval view first, usually as Markdown tables, while keeping complete source-of-truth artifacts in files.

```text
human-facing = summary table first
agent-facing = full artifact files
evidence = always named or linked
risk / blocker / human decision = never hidden
```

## When To Use

Use before human confirmation for:

- Project Entry / Existing Project Onboarding
- Project Onboarding Scan / Onboarding DB
- Remote Project Discovery
- Requirement Archive
- Product Brief
- Feature Spec
- Work Breakdown / Tasks
- Delivery Contract acceptance or breaking change
- Test Design
- E2E Discovery
- Plan approval
- Drift Check
- Project Memory Update
- Feature Completion Check
- Submit / Integrate
- Pause / Close
- directory-level `AGENTS.md` creation or update
- multi-file or multi-fact updates that should use Batch Human Review

For tiny one-line changes, a short 3-line summary is acceptable:

```text
Summary:
Evidence:
Decision:
```

Do not force a large table when it adds noise.

## Required Shape

Every Human Review Summary should include:

- stage name
- artifact paths that will be written or updated
- concise table of what changed or what will happen
- risk / blocker / open question column when relevant
- evidence column when facts are claimed
- explicit human decision requested
- recommended next stage

## Batch Human Review

Use Batch Human Review when the agent proposes to create or update multiple documents, multiple rows, multiple facts, or multiple long-term memory entries in one stage.

Required table:

| File / Item | Action | Change Summary | Source Evidence | Confidence | Affects Long-Term Memory | Suggested Action |
|---|---|---|---|---|---|---|

Allowed human choices:

```text
approve all
approve selected
revise selected
defer selected
skip this batch
```

Use Batch Human Review for:

- onboarding-db document creation or refresh
- project memory backfill with multiple facts
- AGENTS.md / CLAUDE.md or directory guidance updates
- drift check backfill
- feature close final document sync
- spec/tasks/tests/plan changes when multiple items are affected

High-confidence rows can be drafted, but cannot become reviewed or written as accepted long-term fact without human confirmation.

## Stage Table Patterns

### Feature Spec Approval

| Item | Summary |
|---|---|
| Feature |  |
| Goal |  |
| In Scope |  |
| Out of Scope |  |
| Stories |  |
| Open Questions |  |
| Risks |  |
| Artifacts |  |
| Human Decision | Approve spec / revise / pause |

### Work Breakdown Approval

| Task | Story | Slice | Mode | Depends On | Verification | Risk / Gate |
|---|---|---|---|---|---|---|
| T001 | US1 | vertical | Agent-ready | none |  |  |

Add a short summary:

```text
Recommended execution: linear | parallel | staged-linear | staged-parallel
Next recommended stage:
Auto mode option:
```

### Test Design Approval

| Type | Coverage | Execution | Command / Tool | Blocker | Evidence Location |
|---|---|---|---|---|---|
| Unit |  | automatic |  |  | notes.md |
| API |  | automatic |  |  | notes.md |
| E2E |  | existing-framework / browser / chrome / computer-use / manual / blocked |  |  | tests.md |

### Delivery Contract Approval

| Contract | Type | Producer | Consumers | Status | Interface Summary | Compatibility | Verification | Human Decision |
|---|---|---|---|---|---|---|---|---|
| API001 | API |  |  | draft |  | compatible / breaking | pending | accept / revise |

For breaking changes, list every affected consumer, scan evidence, compatibility option, migration action, and rollout order before asking for approval. A prior human request to "just change it" is not final approval; ask again after the impact table is shown.

### Plan Approval

| Item | Summary |
|---|---|
| Scope |  |
| Files |  |
| Interfaces |  |
| TDD RED |  |
| GREEN |  |
| Verification |  |
| Risks |  |
| Stop Conditions |  |
| Human Decision | Approve plan / revise / enable Task Auto-Run |

### Drift Check Approval

| Drift | Type | Impact | Backfill Location | Evidence | Human Decision |
|---|---|---|---|---|---|
|  | behavior | feature | spec.md |  | accept / revise / reject |
|  | long-term | project | project.md or project/*.md |  | accept / ignore |

### Project Memory Update Approval

| Update Area | Current | Proposed | Reason | Evidence | Human Decision |
|---|---|---|---|---|---|
| Test Commands |  |  |  |  | accept / skip |
| Capability |  |  |  |  | accept / skip |
| Directory Map |  |  |  |  | accept / skip |
| Domain Language |  |  |  |  | accept / skip |

### Project Onboarding Scan Approval

| Item | Summary | Evidence | Confidence | Human Decision |
|---|---|---|---|---|
| Mode | Quick / Deep / Targeted |  |  | approve / revise |
| Layout | Compact / Standard / Expanded / none |  |  | approve / revise |
| Scope |  |  |  | approve / revise |
| Subagents | none / proposed lanes |  |  | approve / skip |
| Write Plan | project memory / onboarding-db / guidance |  |  | approve / revise |

### Onboarding DB Batch

| File / Item | Action | Change Summary | Source Evidence | Confidence | Affects Long-Term Memory | Suggested Action |
|---|---|---|---|---|---|---|

If subagent scan results conflict, include:

| Conflict | Finding A | Finding B | Evidence A | Evidence B | Current Judgment | Action |
|---|---|---|---|---|---|---|

### Feature Completion Check

| Check | Status | Evidence | Issue |
|---|---|---|---|
| Tasks | pass / fail |  |  |
| Tests | pass / fail |  |  |
| Feature Close Review | pass / fail |  |  |
| Drift Check | pass / fail |  |  |
| Project Memory | pass / fail |  |  |
| Submit Status | done / skipped / needed |  |  |

Conclusion:

```text
Recommendation: close | continue | pause before new feature | update scope
Human Decision:
```

### Submit / Integrate

| Item | Status | Evidence |
|---|---|---|
| Verification | pass / fail |  |
| Drift Check | done / missing |  |
| Diff Review | clean / issues |  |
| Unrelated Changes | none / present |  |
| Action | prepare / commit / PR text / skip | human decision needed |

## Rules

- The table is not the source of truth. Update the owning artifact after confirmation.
- Do not hide uncertainty to make a table look clean.
- For complex artifacts, table rows may link to `tasks/*`, `tests/*`, or `plans/*` detail files.
- Delivery Contract rows may link to `contracts/*` detail files.
- Keep table cells concise. Put long reasoning in the artifact file, not the approval view.
- If a stage has both product and engineering implications, show both rather than compressing them into a vague summary.
- When asking for approval, prefer a concrete decision: "approve", "revise", "pause", "enable auto mode", "reject this backfill".

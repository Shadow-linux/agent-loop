# Notes: <Feature Name>

Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Status: active | blocked | paused | closed
Implementation Readiness: preparing | review-ready | accepted
Gate 1 Decision: pending | accepted | revise | pause
Gate 1 Spec Digest: pending | sha256:<digest>
Gate 2 Decision: pending | package-only | approve-and-start | revise | pause
Gate 2 Package Files: pending | <comma-separated Feature-relative paths>
Gate 2 Package Digest: pending | sha256:<digest>
Gate 2 Stable Files: pending | <comma-separated Feature-relative paths excluding rotatable plan.md>
Gate 2 Stable Digest: pending | sha256:<digest>
Gate 2 Agent-ready Tasks: pending | <comma-separated task IDs>
Active Plan Scope: pending | <accepted task/story ID>
Gate 2 Plan Evidence: pending | plan.md | plans/<detail>.md | no-plan:<accepted task ID>
Feature Auto-Loop: disabled | enabled
Gate 2 Reviewed At: pending | <ISO-8601>

`preparing` means Gate 1 accepted and package preparation is active. `review-ready` means package completeness and Analyze Consistency passed and Gate 2 is pending. `accepted` means Gate 2 accepted the package; execution still depends on the recorded Gate 2 choice. This field is not Feature lifecycle or Git/external/submit/close authorization.

The Gate 1 digest freezes the accepted Spec. Gate 2 Package Files/Digest include every current artifact under triggered `tasks/`, `tests/`, `plans/`, and `contracts/` directories and freeze package-only start evidence. Stable Files/Digest exclude rotatable `plan.md` and `plans/*`, while protecting definition/tasks/tests/context/contracts during Feature Auto-Loop. Plan Evidence binds the active scope to the compact Plan, one detailed Plan, or an explicit No-Plan Decision. `package-only` requires Auto-Loop `disabled`; `approve-and-start` requires `enabled`.

## Human Decisions

## Current Branch Context

Branch Class: main | standard-release | customer-release | development | unknown
Work Type: feature | bugfix | hotfix | not-applicable
Target Kind: standard | customer | not-applicable
Target Version:
Customer Slug:
Topic:
Source Branch:
Target Branch:
Lifecycle State: proposed | open | aggregating | release-candidate | released / sealed | retained | active | blocked | review-ready | merged | abandoned | deleted | unknown
Source Evidence:
Last Checked:
Human Decision:

This context does not authorize create, switch, merge, delete, push, tag, release, or publish.

## Stage Helper Resolutions

### YYYY-MM-DD — <Stage>

- Requested Helper:
- Invocation Scope: task | story | task-review | submit-review | feature-close-review | subagent-group | other
- Execution Unit:
- Resolved At:
- First Stage Action At:
- Candidate Results:
  - `superpowers:<helper>`: absent | loaded | load-failed — <evidence>
  - `<helper>`: absent | loaded | load-failed | not-needed-after-success — <evidence>
- Resolved Helper: <actual helper name> | none
- Resolution Status: loaded | unavailable | load-failed
- Fallback Used: yes | no
- Fallback Source:
- Method Used:
- Agent-loop Overrides:
  - Artifact Path:
  - Human Gate:
  - State Ownership:
- Evidence:
- Persistence: notes.md | response-local-pending

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

## Plan History

- YYYY-MM-DD `<Plan ID>`:
  - Scope:
  - Result:
  - Evidence:
  - Next:

## Analyze Consistency

- Date:
- Scope:
- Requirement Coverage:
- Task / Spec Mapping:
- Test Coverage:
- Plan Scope Check:
- Code Reality Check:
- Decision: proceed | revise-spec | revise-tasks | revise-tests | revise-plan | investigate-first | human-gated
- Next Stage:

## TDD Cycles

## Verification Evidence

## Bug Verification / Close Linkage

- Related Bugs:
- Bug Status After Feature Verification: verifying | in-progress | triaging | not-applicable
- Original Reproduction / Substitute Evidence:
- Regression / Safety Evidence:
- Candidate Bug Resolution:
- Bug Close Decision: pending | confirm | revise | keep-verifying
- Feature Close Decision: pending | confirm | continue | pause | revise-scope
- Evidence Links:

Feature verification does not close a Bug automatically. Bug Close and Feature Close remain separately named Human decisions.

## Diagnosis

## Review

### Spec Review

- Date:
- Scope:
- Findings:
- Accepted fixes:

### Standards Review

- Date:
- Scope:
- Findings:
- Accepted fixes:

## Feature Close Review

### Feature-Level Spec Review

- Date:
- Scope:
- Findings:
- Accepted fixes:

### Feature-Level Standards Review

- Date:
- Trigger: required | not-triggered
- Scope:
- Findings:
- Accepted fixes:

## Submit / Integrate

- Date:
- Scope:
- Action:
- Diff Summary:
- Verification:
- Drift Check:
- Commit:
- PR:
- Remaining Risk:
- Source Branch:
- Branch Class:
- Target Release Context:
- Target Branch:
- Sealed Check:
- Customer Isolation Check:
- Requested Authorization:
- Explicitly Not Authorized:
- Merge Evidence / Cleanup Decision:
- Related Bug Status / Evidence:
- Unresolved Bug Close Decisions:

## Spec Drift

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

## Checkpoints

## Pause / Resume Point

## Close Record

Closed At: <YYYY-MM-DD>
Human Decision: <confirmed-by-human>

## Archive Readiness

Closed At: <same YYYY-MM-DD as Close Record>
Delivered Summary: <one concrete line describing delivered behavior>
Verification: complete
Feature Close Review: complete
Drift: resolved
Project Memory Impact: complete | none
Open Follow-up: none | <FU-001, FU-002>

# Subagent Brief

Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Status: draft | active | returned | merged | blocked

Feature:
Story:
Task:
Brief ID: YYYY-MM-DD-<task-or-story>-<slug>

## Delegated Authority

Owning Stage:

Existing Authorization:

Assignment Scope:

Allowed Writes: none | <exact paths already covered by Existing Authorization>

Write Concurrency: mechanically-non-overlapping | serialized | existing-authorized-isolated-worktree | not-applicable

Forbidden Actions:

Read-Only Reviewer: yes | no

Rollback Evidence: current | not-applicable — <evidence and reason>

Expiry:

Stop Conditions:

Subagent dispatch is not a Human Gate. The assignment inherits only the Existing Authorization and accepted write boundary; it cannot create or widen authorization. If the requested action exceeds that boundary, stop and return it to the owning Agent or the existing Human Gate.

## Assignment

Scope:

Out of Scope:

## Required Context

Read first:
- `.agent-loop/project.md`
- `.agent-loop/features/<feature>/spec.md`
- `.agent-loop/features/<feature>/tasks.md`
- `.agent-loop/features/<feature>/tests.md`
- `.agent-loop/features/<feature>/plan.md`
- `.agent-loop/features/<feature>/contracts.md` and relevant `contracts/*` details when the assignment crosses a producer-consumer boundary
- <task/test/plan detail files if relevant>

Relevant code boundaries:
- 

## Expected Work

- 

## TDD / Verification

RED command or check:

GREEN command or check:

Additional verification:

## Constraints

- You are a subagent. Stay inside this assignment and return findings to the main agent.
- When `Read-Only Reviewer: yes`, do not edit any file or mutate external state.
- When `Read-Only Reviewer: yes`, resolve the requested review helper as the first internal action, form the response-local Reviewer Helper Resolution before substantive review, and return it without persisting any file.
- Do not close the feature.
- Do not submit code, commit, create PR text, merge, release, publish, or seal.
- Do not update `.agent-loop/project.md`, enterprise `.agent-loop/project/*.md`, root `AGENTS.md`, `CLAUDE.md`, or directory guidance directly. Return proposed durable memory/guidance updates instead.
- Do not accept Delivery Contracts, approve breaking contract changes, or change accepted/verified contract status.
- Do not mark tasks `done`. Return evidence and recommended status; the main agent owns Task Done Gate review.
- Do not rewrite original human requirements.
- Do not change unrelated files.
- Record any drift or uncertainty in the return.

## Return Format

Reviewer Helper Resolution (read-only Final Review only):
- Requested Helper:
- Candidates Checked:
- Resolved Helper: <name> | none
- Status: loaded | unavailable | load-failed
- Load / Fallback Evidence:
- Method Used:

Changed files:

Commands run:

Evidence:

Drift found:

Open questions:

Recommended next step:

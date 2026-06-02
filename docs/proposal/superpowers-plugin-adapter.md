# Proposal: Superpowers As Agent-Loop Stage Plugins

Status: Draft
Version target: v1.1.0 or later
Created: 2026-06-02

## Purpose

Use Superpowers as optional stage plugins inside `agent-loop` without letting Superpowers take over the project workflow.

`agent-loop` remains the controller:

- stage classification
- artifact locations
- human gates
- task status rules
- project memory ownership
- drift checks
- submit / pause / close gates

Superpowers provides stage-level methods:

- brainstorming discipline
- construction-grade planning
- TDD discipline
- systematic debugging
- verification discipline
- review discipline
- optional subagent execution discipline

## Non-Goal

This proposal does not copy Superpowers skill content into `agent-loop`.

This proposal does not create `docs/superpowers/` in target projects by default.

This proposal does not let Superpowers decide:

- where artifacts are written
- when a stage is complete
- whether a task is `done`
- whether a feature can close
- whether code can be submitted
- whether subagents may run

## Core Rule

```text
agent-loop controls the loop.
Superpowers improves the current stage.
agent-loop artifact paths override external skill paths.
agent-loop human gates override external skill transitions.
```

If a Superpowers skill says to write an artifact under a Superpowers-owned path, treat that path as advisory. Write the artifact to the current `agent-loop` stage artifact instead.

Example:

```text
Superpowers default:
docs/superpowers/plans/YYYY-MM-DD-feature.md

agent-loop override:
agent-loop/features/<feature>/plan.md
or
agent-loop/features/<feature>/plans/YYYY-MM-DD-<task>-<slug>.md
```

## Adapter Rules

### 1. Controller Boundary

External skills may affect how the agent works inside a stage, but they may not change the `agent-loop` state machine.

Allowed:

- ask better clarification questions
- produce better plans
- enforce RED/GREEN/REFACTOR
- investigate failures systematically
- improve verification and review rigor

Not allowed:

- skip `agent-loop` human gates
- create external default directories without explicit human request
- mark tasks `done`
- close a feature
- commit, PR, merge, release, or publish
- update project memory outside the current `agent-loop` stage rules

### 2. Path Override

All external skill artifact paths are overridden by `agent-loop` paths.

| External output type | Agent-loop destination |
|---|---|
| brainstormed design/spec | `features/<feature>/product.md` and/or `features/<feature>/spec.md` |
| implementation plan | `features/<feature>/plan.md` or `features/<feature>/plans/*` |
| test strategy | `features/<feature>/tests.md` or `features/<feature>/tests/*` |
| debugging notes | `features/<feature>/notes.md` |
| verification evidence | `features/<feature>/notes.md` |
| review findings | `features/<feature>/notes.md` |
| subagent brief / return | `features/<feature>/handoffs/*` |

Do not create `docs/superpowers/` in a target project unless the human explicitly asks for native Superpowers output.

### 3. Human Gate Override

If an external skill says to continue into another external skill, treat that as a recommendation only.

The next stage is still chosen by `agent-loop`:

```text
Current stage completes
→ agent-loop records artifacts/evidence
→ Human Review Summary if needed
→ human confirms next stage or auto mode
→ agent-loop routes onward
```

### 4. Evidence And Drift

When a Superpowers method is used, record only useful durable facts:

- decisions
- evidence commands and results
- review findings
- drift decisions
- next recommended stage

Do not record long process narration.

## Proposed Stage Mapping

| Agent-loop stage | Preferred Superpowers plugin | Use from Superpowers | Agent-loop overrides |
|---|---|---|---|
| Brainstorm / Clarify if Needed | `superpowers:brainstorming` | context exploration, one-question-at-a-time, 2-3 approaches, design approval | write to `product.md` / `spec.md`; do not write `docs/superpowers/specs/`; next stage remains agent-loop controlled |
| Product Brief If Needed | `superpowers:brainstorming` plus product/PRD skills when available | product intent, alternatives, user outcomes | write to `product.md`; project-wide consensus only via Project Memory Update |
| Feature Spec | optional brainstorming/spec method | ambiguity removal, scope check, acceptance thinking | write to `spec.md`; use agent-loop Human Review Summary |
| Plan If Needed | `superpowers:writing-plans` | construction-grade plan, exact paths, test code, commands, expected outputs, no placeholders, self-review | write to `plan.md` or `plans/*`; do not write `docs/superpowers/plans/`; execution mode remains agent-loop controlled |
| Execute Task / Story | `superpowers:test-driven-development` | RED, verify RED, GREEN, verify GREEN, refactor | task status still controlled by Task Done Gate; evidence to `notes.md` |
| Diagnose Failure | `superpowers:systematic-debugging` | root cause before fix, reproduce, isolate, trace | findings to `notes.md`; fix still returns to Execute / Verify / Review |
| Verify | `superpowers:verification-before-completion` | evidence before completion claim | evidence to `notes.md`; completion still controlled by agent-loop |
| Review | `superpowers:requesting-code-review` | rigorous review pass | findings to `notes.md`; task moves to `done` only after Task Done Gate |
| Submit / Integrate | `superpowers:finishing-a-development-branch` | completion options and branch hygiene | submit still requires agent-loop diff review, verification, drift check, and human confirmation |
| Subagent execution | `superpowers:subagent-driven-development` | fresh subagent per independent task, review between tasks | only after human confirms subagent use; briefs/returns in `handoffs/*`; main agent owns merge and status |

## Brainstorming Adapter Detail

When `Brainstorm / Clarify if Needed` starts and Superpowers is available:

1. Load `superpowers:brainstorming`.
2. Use its project-context and question discipline.
3. Ask one high-impact question at a time.
4. Offer 2-3 approaches when meaningful.
5. Present a design summary for human approval.
6. Write approved content to:
   - `features/<feature>/product.md` when product intent is substantial
   - `features/<feature>/spec.md` when behavior and acceptance are clear
7. Do not write `docs/superpowers/specs/*` unless the human explicitly requests native Superpowers docs.
8. Do not automatically transition to `superpowers:writing-plans`; recommend the next `agent-loop` stage instead.

## Writing-Plans Adapter Detail

When `Plan If Needed` starts and Superpowers is available:

1. Load `superpowers:writing-plans`.
2. Use its plan quality bar:
   - exact files
   - exact code context
   - test code
   - commands
   - expected RED/GREEN output
   - no placeholders
   - self-review
3. Save the plan to:
   - `features/<feature>/plan.md` for the active task/story
   - `features/<feature>/plans/YYYY-MM-DD-<task>-<slug>.md` in complex artifact mode
4. Do not write `docs/superpowers/plans/*` unless the human explicitly requests native Superpowers docs.
5. Do not let the external skill decide execution mode. Offer agent-loop modes:
   - Strict Mode
   - Feature Auto-Loop
   - Task Auto-Run
   - subagent execution only after human approval

## TDD Adapter Detail

When `Execute Task / Story` starts and Superpowers is available:

1. Load `superpowers:test-driven-development`.
2. Follow RED/GREEN/REFACTOR when applicable.
3. If TDD cannot be followed, stop or mark the task `Human-gated`.
4. Record evidence in `notes.md`.
5. Move task to `review`, not `done`, until Task Done Gate passes.

## Debugging Adapter Detail

When verification fails or unexpected behavior appears:

1. Load `superpowers:systematic-debugging`.
2. Reproduce and identify root cause before proposing fixes.
3. Record root cause, evidence, fix decision, and follow-up verification in `notes.md`.
4. Return to Execute / Verify / Review under `agent-loop`.

## Subagent Adapter Detail

Subagents are optional and must be human-approved.

Use only when:

- tasks or scan lanes are independent
- the context can be bounded
- each subagent has a clear brief
- the main agent can review and merge outputs

Artifact destinations:

```text
features/<feature>/handoffs/<date>-<task>-brief.md
features/<feature>/handoffs/<date>-<task>-return.md
notes.md summary
tasks.md status updates only after main-agent review
```

Subagents may not:

- close a feature
- submit code
- update project memory directly
- accept Delivery Contracts
- make breaking contract changes
- mark tasks `done` without main-agent Task Done Gate review

## Open Questions

1. Should `superpowers:brainstorming` be preferred only when requirements are vague, or for every new feature?
2. Should `superpowers:writing-plans` be required for every `plan.md`, or only complex tasks?
3. Should adapter usage be recorded in `notes.md` every time, or only when it affects decisions/evidence?
4. Should native Superpowers docs ever be allowed by default in this skill repo's example projects?
5. Should subagent-driven execution remain opt-in per task, or can Feature Auto-Loop ask once for a bounded task group?

## Proposed Implementation Steps

1. Add `references/external-skill-adapters.md`.
2. Move this proposal's accepted adapter rules into that reference.
3. Update `references/skill-routing.md` to load the adapter reference when Superpowers is available.
4. Update `references/stage-guides.md` for:
   - Brainstorm / Clarify
   - Plan If Needed
   - Execute Task / Story
   - Diagnose Failure
   - Verify
   - Review
   - Subagent execution
5. Update `SKILL.md` package map if a new reference is added.
6. Add validation scenarios for:
   - Superpowers brainstorming path override
   - Superpowers writing-plans path override
   - TDD evidence still controlled by Task Done Gate
   - subagent approval stop condition
7. Bump version and update `CHANGELOG.md`.

# External Skill Adapters

Use this reference when another skill or plugin can improve the current `agent-loop` stage. External skills are stage accelerators only; agent-loop remains the controller.

## Capability Scan Rule

Before using fallback stage guidance, inspect the current runtime's available skills/plugins/helpers for a stage match.

If Superpowers is available, prefer these helpers:

| Stage | Preferred Superpowers helper |
|---|---|
| Requirements Discussion | `superpowers:brainstorming` plus grill-with-docs style helpers when available |
| Brainstorm / Clarify | `superpowers:brainstorming` |
| Product Brief If Needed | `superpowers:brainstorming` plus product/PRD helpers when available |
| Feature Spec | `superpowers:brainstorming` plus spec helpers when available |
| Plan Gate / Plan If Needed | `superpowers:writing-plans` |
| Execute Task / Story | `superpowers:test-driven-development` |
| Diagnose Failure | `superpowers:systematic-debugging` |
| Verify / Completion claim | `superpowers:verification-before-completion` |
| Review / Feature Close Review | `superpowers:requesting-code-review` |
| Feature Completion Check | verification / finishing helpers when available |
| Submit / Integrate | `superpowers:finishing-a-development-branch` |
| Pause / Close | finishing / handoff helpers when available |
| Approved Subagent execution | `superpowers:subagent-driven-development` |

For mandatory helper-backed stages, resolve canonical and alias names using `skill-routing.md`, then load the complete helper before stage actions. If it is absent, record `unavailable`; if it is discovered but cannot be loaded, record `load-failed`. Only those two statuses allow fallback.

## Controller Rule

```text
agent-loop decides the stage.
External skills improve work inside the stage.
agent-loop artifact paths override external skill paths.
agent-loop human gates override external skill transitions.
agent-loop owns task status, feature close, project memory, and submit.
```

This ownership is invariant even when a helper is mandatory. A helper may impose a stronger stage method, but it cannot choose the next stage, change an artifact destination, cross a human gate, or update lifecycle state on its own.

Do not copy an external skill's full workflow into `agent-loop`. Borrow the method, then translate the result into the current `agent-loop` artifact.

## Path Override Rule

If an external skill says to write an artifact under its own default directory, treat that path as advisory: agent-loop artifact paths always override external skill default paths.

Write to the current `agent-loop` artifact instead.

| External output | Agent-loop destination |
|---|---|
| brainstormed requirement/product/design/spec | owning-stage artifact: requirement document plus requirement README summary during Requirements Discussion; `.agent-loop/features/<feature>/product.md` during Product Brief; `.agent-loop/features/<feature>/spec.md` or `notes.md` during Feature Spec |
| implementation plan | `.agent-loop/features/<feature>/plan.md` or `.agent-loop/features/<feature>/plans/*` |
| test strategy | `.agent-loop/features/<feature>/tests.md` or `.agent-loop/features/<feature>/tests/*` |
| debugging notes | `.agent-loop/features/<feature>/notes.md` |
| verification evidence | `.agent-loop/features/<feature>/notes.md` |
| review findings | `.agent-loop/features/<feature>/notes.md` |
| subagent brief / return | `.agent-loop/features/<feature>/handoffs/*` |

The table uses the default `.agent-loop/` memory root. When an existing project uses the accepted legacy `agent-loop/` root, keep that current memory root; never create repository-root `features/`.

Do not create `docs/superpowers/` in a target project unless the human explicitly asks for native Superpowers output and then confirms the external directory after the agent explains the agent-loop path override. A request such as "use Superpowers" or "save it where Superpowers normally saves it" is not enough by itself.

## Stage Helper Resolution Record

Create the initial `templates/notes.md` Stage Helper Resolution record before the first stage action, then finish its method/fallback/evidence fields before stage exit. If no feature workspace has been confirmed, use the response-local pending-record rule from `skill-routing.md` instead of creating files without approval.

The record includes:

- stage and requested helper
- canonical and alias candidates checked
- resolved helper or `none`
- `loaded`, `unavailable`, or `load-failed`
- whether fallback was used and its source
- artifact path, human gate, and state ownership overrides
- evidence that the helper was loaded or why resolution failed

Before the first action, `loaded` requires `Fallback Used: no`, a resolved helper, and complete load evidence. Before stage exit, it additionally requires method-used evidence. `Fallback Used: yes` requires `unavailable` or `load-failed`, a `none` resolved helper, and candidate-by-candidate failure evidence. Missing or inconsistent initial fields block stage action; missing or inconsistent exit fields block completion.

Each invocation scope gets its own record. Task Review, Submit review, and Feature Close Review may use the same helper name, but Feature Close Review requires a new resolution record and may not reuse a prior task-review load record.

## Gate Override Rule

If an external skill says to continue into another external skill, treat that as a recommendation only.

The next stage is still chosen by `agent-loop`:

```text
current stage completes
-> agent-loop records artifacts/evidence
-> Human Review Summary when needed
-> human confirms next stage or auto mode
-> agent-loop routes onward
```

External skills may not:

- skip `agent-loop` human gates
- create external default directories without explicit human request
- mark tasks `done`
- close a feature
- submit, commit, PR, merge, release, or publish
- update project memory outside the current `agent-loop` stage rules
- accept Delivery Contracts or approve breaking contract changes

## Superpowers Mapping

Use Superpowers when available for these stages, while applying the path and gate override rules above.

| Agent-loop stage | Superpowers adapter | Borrow | Override |
|---|---|---|---|
| Requirements Discussion | `superpowers:brainstorming` plus grill-with-docs style helpers when available | context exploration, one-question-at-a-time, terminology, flows, exceptions, prior-feature conflicts | write approved details to the requirement document and only index/lifecycle/mapping summaries to requirement README; do not create feature artifacts |
| Brainstorm / Clarify if Needed | `superpowers:brainstorming` | context exploration, one-question-at-a-time, options, design approval | write to the owning stage artifact; do not write `docs/superpowers/specs/`; do not auto-transition to `writing-plans` |
| Product Brief If Needed | `superpowers:brainstorming` plus product/PRD skills when available | product intent, alternatives, user outcomes | write to `product.md`; long-term consensus only via Project Memory Update |
| Feature Spec | brainstorming/spec methods | ambiguity removal, scope check, acceptance thinking | write to `spec.md`; use agent-loop Human Review Summary |
| Plan Gate / Plan If Needed | `superpowers:writing-plans` | decide plan vs recorded No-Plan Decision; construction-grade plan, exact paths, test code, commands, expected outputs, no placeholders, self-review | write to `plan.md` or `plans/*`, or record No-Plan Decision only for trivial tasks; do not write `docs/superpowers/plans/`; execution mode remains agent-loop controlled |
| Execute Task / Story | `superpowers:test-driven-development` | RED, verify RED, GREEN, verify GREEN, refactor | task status still controlled by Task Done Gate; evidence to `notes.md` |
| Diagnose Failure | `superpowers:systematic-debugging` | reproduce, isolate, trace root cause before fixing | findings to `notes.md`; return to Execute / Verify / Review |
| Verify | `superpowers:verification-before-completion` | evidence before completion claim | evidence to `notes.md`; completion still controlled by agent-loop |
| Review | `superpowers:requesting-code-review` | rigorous review pass | findings to `notes.md`; task moves to `done` only after Task Done Gate |
| Feature Completion Check | verification / finishing helpers when available | evidence discipline and close-decision support | agent-loop owns completion result, blocker routing, and close confirmation |
| Submit / Integrate | `superpowers:finishing-a-development-branch` | completion options and branch hygiene | submit still requires agent-loop diff review, verification, drift check, and human confirmation |
| Pause / Close | finishing / handoff helpers when available | close options, handoff structure, and completion hygiene | close still requires Feature Completion Check, Feature Close Review, drift, memory status, and explicit human confirmation |
| Subagent execution | `superpowers:subagent-driven-development` | bounded independent execution with review | only after human confirms; briefs/returns in `handoffs/*`; main agent owns merge and status |

## Brainstorming Adapter

When `Brainstorm / Clarify if Needed` starts and Superpowers is available:

Requirements Discussion writes approved details to the requirement document and only source, lifecycle, Delivery Phase, Feature Mapping, and decision-link summaries to requirement README; Product Brief writes to `product.md`; Feature Spec writes to `spec.md` and `notes.md`.

1. Use `superpowers:brainstorming` as the preferred method.
2. Inspect project context first.
3. Ask one high-impact question at a time.
4. Offer 2-3 approaches when meaningful.
5. Present a design summary for human approval.
6. Write approved content to the owning stage artifact: requirement document plus requirement README summary during Requirements Discussion, `product.md` during Product Brief, or `spec.md` / `notes.md` during Feature Spec.
7. Do not create `docs/superpowers/specs/*` unless the human explicitly requests native Superpowers docs and confirms the external directory after path-override explanation.
8. Do not automatically transition to `superpowers:writing-plans`; recommend the next `agent-loop` stage.

## Product Brief Source Gate

External PRD/product helpers cannot turn chat or requirements discussion directly into feature `product.md`.

If an external helper produces product-shaped content before requirement source and feature context are confirmed, keep detailed output in the owning Requirements Discussion requirement document, keep only index/lifecycle/mapping summaries in requirement README, or use a response-local draft. Ask whether to create/reference a requirement set or confirm feature start before writing feature `product.md`.

## Grill-With-Docs Adapter

When a grill-with-docs style helper is available:

1. Use it as a clarification method inside Requirements Discussion, Product Brief, or Brainstorm / Clarify.
2. Load `requirement-product-grill.md` and keep agent-loop as the controller.
3. Inspect project memory, source requirements, code/docs/tests, and targeted prior feature artifacts before asking questions when relevant.
4. Ask one blocking question at a time and include the agent's recommended answer.
5. Write accepted output to the owning artifact: detailed Requirements Discussion output to the requirement document with only index/lifecycle/mapping summaries in requirement README; Product Brief output to `product.md`; Feature Spec output to `spec.md` or `notes.md`.
6. Do not create `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/` from grill-with-docs defaults.
7. Cross-feature, shared design, hard-to-reverse, surprising, or real-trade-off findings are Design Readiness evidence and Decision Candidates for Decision & Design; they are not accepted ADRs.

## Writing-Plans Adapter

When `Plan Gate / Plan If Needed` starts and Superpowers is available:

1. Use `superpowers:writing-plans` as the preferred method.
2. First decide whether the selected task/story requires a construction-grade plan.
3. Require a construction-grade plan when the task is multi-file, behavior-changing, test-changing, interface-changing, data/API/async/security/deployment-related, cross-module, TDD-heavy, subagent-based, or human-requested.
4. If a plan is required, require exact files, code context, test code, commands, expected RED/GREEN output, no placeholders, and self-review.
5. Save the plan to `plan.md` for the active task/story, or to `plans/YYYY-MM-DD-<task>-<slug>.md` in complex artifact mode.
6. If a plan is not required, record the No-Plan Decision in `notes.md` and the selected task row/detail with exact files, exact verification command, and why no trigger applies.
7. Do not create `docs/superpowers/plans/*` unless the human explicitly requests native Superpowers docs and confirms the external directory after path-override explanation.
8. Do not let the external skill choose execution mode. Offer agent-loop modes: Strict Mode, Feature Auto-Loop, Task Auto-Run, or human-approved subagent execution. Task Auto-Run still requires an accepted plan.

## TDD Adapter

When `Execute Task / Story` starts and Superpowers is available:

1. Use `superpowers:test-driven-development` as the preferred method.
2. Follow RED/GREEN/REFACTOR when applicable.
3. If TDD cannot be followed, stop or mark the task `Human-gated`.
4. Record evidence in `notes.md`.
5. Move the task to `review`, not `done`, until Task Done Gate passes.

## Debugging Adapter

When verification fails or unexpected behavior appears:

1. Use `superpowers:systematic-debugging` as the preferred method.
2. Reproduce and identify root cause before proposing fixes.
3. Record root cause, evidence, fix decision, and follow-up verification in `notes.md`.
4. Return to Execute / Verify / Review under `agent-loop`.

## Submit / Integrate Adapter

When `Submit / Integrate` starts and Superpowers is available:

1. Use `superpowers:finishing-a-development-branch` only for completion options, branch hygiene, and integration decision support.
2. Load `submit-and-integrate.md` and follow the agent-loop submit gate.
3. Inspect diff and untracked files before any integration action.
4. Confirm fresh verification evidence, required review, drift check, and project memory update status.
5. Separate product code changes from `agent-loop` artifact changes and unrelated dirty work.
6. Present a Human Review Summary before commit, PR text, merge note, release note, publish/release action, or any final submission claim.
7. Treat a human saying "commit" as permission to enter Submit / Integrate, not final commit approval.
8. Do not let the external finishing skill commit, publish PR text, merge, release, publish, close the feature, or mark submission ready without agent-loop confirmation.

## Subagent Adapter

Subagents are optional and require explicit human confirmation before dispatch. A Feature Auto-Loop or Task Auto-Run grant is not subagent approval.

One confirmation may cover a bounded task group only when the agent first lists:

- task/story IDs or scan lanes included
- files or boundaries each subagent may inspect or change
- one brief per subagent
- stop conditions
- main-agent review and merge responsibility

Use only when:

- tasks or scan lanes are independent
- the context can be bounded
- each subagent has a clear brief
- the main agent can review and merge outputs

Artifact destinations:

```text
.agent-loop/features/<feature>/handoffs/<date>-<task>-brief.md
.agent-loop/features/<feature>/handoffs/<date>-<task>-return.md
.agent-loop/features/<feature>/notes.md summary
.agent-loop/features/<feature>/tasks.md status updates only after main-agent review
```

Record the approval date, approved task/story IDs or scan lanes, allowed file/boundary scope, and stop conditions in `notes.md` and each brief. Expanding the approved scope requires new human confirmation; old approval cannot be reused for new tasks or boundaries.

Authorization Status must be `active` immediately before dispatch. Reject `consumed`, `revoked`, or `expired` records even when IDs and boundaries are unchanged. Mark the authorization `consumed` after the approved dispatch group returns or is stopped; a retry or later dispatch requires fresh human confirmation and a new authorization record.

Subagents must never close a feature, submit code, update project memory directly, accept Delivery Contracts, or approve breaking contract changes. They must never mark tasks `done`. Only the main agent may mark a task `done` after Task Done Gate passes.

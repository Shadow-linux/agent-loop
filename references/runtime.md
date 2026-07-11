# Agent Loop Runtime Protocol

This is the required operating protocol. Load this file before any other reference.

## Runtime Contract

The agent runs one loop turn at a time:

```text
Inspect -> Classify -> Recommend -> Confirm -> Act -> Record -> Recommend
```

Do not jump from a human goal directly to code. Do not move to a later stage until the prior stage artifact is accepted or explicitly bypassed by the human.

Bootstrap skill loading: AGENTS.md is bootstrap guidance, not a replacement for the agent-loop skill. If the current runtime exposes the agent-loop skill, load/use it before making workflow decisions during Project Entry, Resume, Re-Adopt, stage boundaries, after context compaction, after long-running sessions, or whenever workflow state is uncertain. Stage Helper Capability Scan happens only after the agent-loop controller is active or unavailable/load-failed because helper scan resolves stage methods, not the controller itself. If the skill is unavailable or load-failed, force Strict Mode, suspend existing auto-mode grants, and use root guidance only for Chat, read-only Project Entry, Re-Adopt / Recovery analysis, read-only Operational Support, and reporting how to restore the skill. Do not Execute, write Human-gated artifacts, Submit, Pause, or Close without the controller.

Agent ownership is mandatory. The agent must not wait for the human to name the next internal stage. For every human goal, bug report, project-understanding question, vague product idea, or "what next" request, the agent classifies the current state and recommends exactly one next action with a reason. If required artifacts are missing, recommend creating or repairing them. If work appears ready, recommend the next stage. If work appears complete, run Feature Completion Check and recommend close, pause, or continue.

Explicit bypass is allowed only for narrow one-off edits that do not create or change feature behavior, public interfaces, data/security boundaries, project memory, formal onboarding docs, submit state, or close state. Record the bypass reason in the response or `notes.md` when a feature exists.

These checks cannot be bypassed inside `agent-loop`: Project Entry classification, re-adoption minimum reconciliation, human source requirement preservation, Onboarding Spec acceptance and the later Full Execution Gate, Task Done Gate, Delivery Contract acceptance or breaking-change gate, fresh verification before completion claims, submit confirmation, and close confirmation.

## Message Intent Classification

Message intent is evaluated before project state classification. It decides what the latest human message is asking the agent to do; Entry Classification still decides the project state.

| Intent | Condition | Default Action |
|---|---|---|
| `chat` | chat means ordinary discussion, rules questions, status questions, or design talk with no request to create requirements or start implementation | answer or discuss only |
| `requirements-discussion` | requirements-discussion means the human is exploring product needs, business goals, capability ideas, constraints, tradeoffs, or user scenarios without authorizing implementation | Requirements Discussion |
| `project-skill-management` | human asks to turn a repeatable project workflow into a project-local skill, or to update, disable, or deprecate one | Project Skill Creation / Update after reliable Project Entry/memory |
| `feature-request` | human explicitly asks to implement, build, change behavior, or start work from accepted requirements | Project Entry, then Design Readiness and Decision & Design / Product Brief / Feature Spec / Feature Follow-up routing |
| `proposal-doc` | human asks to write a proposal, design note, or discussion document without implementing | write the requested proposal/doc only |
| `deferred-requirement` | human asks to remember, defer, backlog, or do something later | Requirement Archive with Future / Deferred Requirement Intake |
| `operational-support` | human asks to use current project code/processes to test, run, deploy, switch config/account/model/provider, diagnose, roll out, or create a runbook | Code-Guided Operational Support |
| `feature-follow-up` | human reports bug, QA feedback, screenshot issue, regression, small tweak, or post-close correction that may relate to recent feature work | Feature Follow-up / Flow-back after project memory is available |
| `unknown` | message could reasonably mean chat, requirements discussion, feature work, follow-up, or operational support | ask a clarifying question |

If message intent is `chat`, do not create requirement sets, feature workspaces, tasks, tests, or plans. Answer, explain, or discuss. If the chat turns into demand shaping, reclassify as `requirements-discussion`.

If message intent is `requirements-discussion`, do not create a feature workspace or enter Work Breakdown, Plan Gate, or Execute. Route to Requirements Discussion: brainstorm/clarify, draft a human-reviewed requirement document, then archive the document under `.agent-loop/requirements/<archive-date>-<topic>/` after the human confirms the document should be recorded. For `requirements-discussion`, reviewed/recorded does not mean accepted for implementation.

If message intent is `project-skill-management`, load `references/project-skills.md`. Do not create a requirement set or feature workspace. Require reliable Project Entry/memory, present a Project Skill Candidate, and stop at Gate 1 before creating or materially updating `.agent-loop/skills/`.

Requirement/Product Grill may be used inside Requirements Discussion, Product Brief, or Brainstorm / Clarify as grill-with-docs style clarification when terminology, roles, business flows, exception paths, prior feature behavior, or decision signals are unclear. It does not create a new stage: it clarifies input for the owning stage, writes only through that stage's artifacts and human gates, and sends shared design signals to Design Readiness Check.

Decision & Design / ADR is the requirement-landing bridge between accepted requirements and feature implementation. Design Readiness Check runs before accepted requirements enter feature construction. Complex requirements that span features or need shared business-flow, domain, state, source-of-truth, architecture, consistency, recovery, or non-functional design enter `Decision & Design If Needed` even when no technology choice is disputed. Ordinary chat and early fuzzy requirements discussion capture readiness evidence and Decision Candidates; decision-file creation and acceptance remain Human-gated.

Message intent is not permanent; reclassify when the conversation changes intent.

Chat defaults to answer-only, but it may convert to `requirements-discussion`, `proposal-doc`, `feature-request`, `operational-support`, `feature-follow-up`, or `deferred-requirement` when the human intent changes. Do not keep using `chat` merely because the conversation started as chat.

If the human explicitly says they only want to discuss and do not want documentation yet, keep the intent as `chat` until they ask to shape, record, or archive the requirement.

If unclear whether the human wants ordinary chat or requirements discussion, ask whether to keep discussing or shape the topic into a requirements document.

If unclear whether the human wants requirements discussion or feature implementation, ask whether to form a requirements document first or start feature construction.

## Routing Axes And Precedence

Do not force project topology, memory health, message intent, and feature progress into one mutually exclusive state. Inspect all four axes, then use the precedence ladder to select exactly one next stage.

```text
Entry Context: `new-project` / `existing-project` / `remote-entry`
Memory Health: `absent` / `current` / `stale` / `outside-loop`
Message Intent: use the Message Intent Classification values above
Work State: `idle` / `active` / `blocked` / `completion-candidate` / `paused`
```

Entry Context:

| Value | Condition | Candidate Route |
|---|---|---|
| `new-project` | no memory and little/no existing code | Init Project |
| `remote-entry` | source of truth is remote/SSH/devcontainer/container/tunnel | Remote Project Discovery |
| `existing-project` | meaningful existing code is locally available | Project Entry Scan when memory is absent; otherwise continue through memory/work-state routing |

Memory Health:

| Value | Condition | Candidate Route |
|---|---|---|
| `absent` | no `.agent-loop/` or legacy `agent-loop/` | Init Project or Project Entry Scan |
| `current` | memory exists and agrees with obvious code/artifact reality | Active Feature Guard or intent routing |
| `stale` | memory conflicts with code or indexes point to missing/stale artifacts | Reconcile Project Context / Recovery Backfill |
| `outside-loop` | recent work bypassed the loop or human asks to re-adopt/re-sync | Re-Adopt Agent Loop Project / Recovery Backfill |

Work State:

| Value | Condition | Candidate Route |
|---|---|---|
| `idle` | no active feature or blocker | intent routing |
| `active` | exactly one active feature has a clear next action | Active Feature Guard, then Continue Current Stage |
| `blocked` | a blocker prevents the next stage | choose one unblock stage |
| `completion-candidate` | active feature may already satisfy completion | Feature Completion Check |
| `paused` | no active feature and one or more resumable features are paused | Resume routing only when the human asks to resume/switch feature work or gives a generic continue signal |

Apply this precedence exactly:

```text
Safety Stop -> Remote Discovery -> Memory Recovery -> Active Feature Guard -> Blocker Resolution -> Intent Routing -> Normal Stage Continuation
```

Rules:

1. Safety Stop includes unavailable controller fallback, Human-gated decisions, and active auto-mode stop conditions.
2. Remote Discovery runs before local existing-project handling.
3. `stale` or `outside-loop` memory is reconciled before operational support, follow-up, or feature continuation relies on it.
4. With current memory, run Active Feature Guard before starting, reopening, or switching feature work.
5. Resolve `blocked` to exactly one unblock stage before continuing downstream work.
6. Only after the prior checks select by Message Intent; otherwise continue the current accepted stage.

Paused work does not preempt an explicit non-feature intent such as chat, requirements discussion, onboarding, or operational support. Ask which paused feature to resume only for a resume/switch request or a generic continue signal that does not identify one.

Entry priority: remote-entry is evaluated before existing-project. If remote-entry and existing-project both appear to match, classify as remote-entry and run Remote Project Discovery before Project Entry Scan so the agent does not treat a local entrypoint or mirror as the source of truth.

Blocked must resolve to exactly one recommended next stage. Ask Human when the blocker is a missing decision, access, approval, environment, or external input; Diagnose Failure when the blocker is caused by observed system behavior, failing verification, or unclear technical cause. If the blocker is a narrow unknown about code ownership or impact, recommend Targeted Feature Scan instead.

Apply the blocked routing matrix in order and choose the first matching row:

1. observed failure or unclear technical cause -> Diagnose Failure
2. required verification not run but runnable in the available environment -> Verify
3. missing human decision/access/approval required for the next safe action -> Ask Human
4. unclear ownership/impact -> Targeted Feature Scan
5. external blocker with no immediate unblock path -> Pause

Diagnosis and available read-only verification may proceed before requesting access or approval for a later mutation. Ask Human first only when the missing human input is required for the next safe diagnostic or verification action itself.

## Inspection Order

Use this order:

1. Apply Bootstrap skill loading. After context compaction, long-running sessions, or stage-boundary uncertainty, do not continue from memory alone.
2. Check `.agent-loop/`; if missing, check legacy `agent-loop/`.
3. If present, read `<memory-root>/project.md`.
4. If `project.md` says `Memory Mode: enterprise`, read only the referenced project-memory detail files needed for the current stage.
5. If `project.md` says `Status: remote-entry`, read `<memory-root>/remote.md` and route through Remote Project Discovery before local Project Entry Scan.
6. Locate `Active Feature` and `Paused Features`.
6a. If `.agent-loop/skills/INDEX.md` exists, read its metadata and verify referenced `active` paths before relying on them. Do not load `proposed`, `disabled`, or `deprecated` skills into normal routing.
7. Read current feature `spec.md`, `tasks.md`, `tests.md`, `plan.md`, `notes.md`, and `contracts.md` if present.
8. If those index files link to `tasks/`, `tests/`, `plans/`, `handoffs/`, or `contracts/`, read only the detail files needed for the current stage.
9. Inspect repo reality only as needed: README, AGENTS/CLAUDE docs, package/test scripts, key directories.
10. If local repo reality points to remote execution, or the human says this is a remote project, load `references/remote-project-discovery.md`. An empty local directory alone is not enough; if there are no remote hints, classify as `new-project`.
11. Verify long-term memory index targets before trusting them. If `project.md`, root guidance, or current artifacts point to onboarding-db, enterprise `project/*.md`, feature docs, contracts, or guidance files, check that the referenced path exists before relying on it.
12. Compare project memory with obvious repo reality.
13. Choose the next stage.

If `project.md` declares a Decisions index, list the decision files before Decision & Design, Product Brief, or Feature Spec. Read decisions already linked by the active requirement, `product.md`, or `spec.md` first; then inspect filenames and statuses for other likely relevant accepted decisions. Do not load every decision body when topic and relationship evidence show it is unrelated.

If the human asks for newcomer-facing docs, durable project understanding, guided learning paths, or onboarding-db construction, route to Evidence-Graph + DDD Onboarding after Project Entry Scan or reliable project memory. Load `references/onboarding-knowledge-base.md`. Do not run the removed Quick / Deep / Targeted onboarding modes or directory-first legacy onboarding-db flow.

If `.agent-loop/onboarding-db/` exists and the human asks to be guided through the project, understand where to start, or explain project structure before coding, check whether it follows the Evidence-Graph + DDD structure. If it does, use it through `references/onboarding-knowledge-base.md` Guided / Focused Use. If it is an old layout, treat the existing onboarding-db as legacy evidence only; migration or replacement requires an accepted Onboarding Spec, Onboarding Tasks, and Full Execution Gate.

If the human asks for guided onboarding but onboarding-db is missing, do not create onboarding-db from the removed legacy flow. Route through Project Entry Scan if project memory is missing/stale; otherwise load `references/onboarding-knowledge-base.md`, build Evidence Graph, and propose an Onboarding Spec before writing formal docs. If root guidance or `project.md` claims onboarding-db should exist but the path is missing, classify as `stale-memory` and reconcile the missing memory reference first.

If the human asks to test, run, deploy, switch account/config/model/provider, check quota/rate limits, arrange rollout, diagnose production, or use existing code to solve an operational problem, default to read-only operational support. Route to Code-Guided Operational Support before Feature Spec, Plan Gate, Execute Task / Story, or code edits. If the request could mean either existing operational use or new implementation, ask whether the human wants help using current project functionality or feature implementation.

If the human asks to "先记一下", do something later, defer work, add a backlog item, or keep a future requirement outside the current feature, route to Requirement Archive with Future / Deferred Requirement Intake. Do not put future TODO, backlog, deferred requirements, or unimplemented planned capability details into `project.md`; use a requirement set and optional `requirements/INDEX.md` after human confirmation.

If the human asks to make a successful workflow into a skill, or asks to update/disable/deprecate a project skill, classify `project-skill-management` and route to Project Skill Creation / Update. If the agent notices a reusable skill opportunity after a complex verified workflow, finish the current stage first and propose a Project Skill Candidate at a safe boundary; do not change intent or create files until the human passes Gate 1.

When an `active` project skill matches current work, discovery and read-only loading may proceed only after its current instruction-bearing and executable files match the SHA-256 validation manifest. Before following its workflow or causing side effects, require the Execution Gate for the current invocation. A human message that explicitly names the skill and concrete scope may satisfy the gate only after the agent emits the execution summary and verifies the plan adds no undisclosed action, effect, environment, or bound. Auto mode, previous success, prior confirmation, `active`, or `bootstrap` may not. One combined confirmation may cover other applicable operational/risk gates only when the summary explicitly includes every gate fact.

If recent work bypassed the loop, set Memory Health to `outside-loop` and route to Re-Adopt / Recovery Backfill. Otherwise, if code reality and the memory root disagree or long-term memory indexes point to missing artifacts, set Memory Health to `stale` and route to Reconcile Project Context / Recovery Backfill. Treat code as the current fact base for agent-maintained docs and preserve human requirements as original intent in both routes.

If `project.md` claims a legacy onboarding layout, lists onboarding-db files, or root `AGENTS.md` / `CLAUDE.md` tells newcomers to start from `.agent-loop/onboarding-db/README.md`, but `.agent-loop/onboarding-db/` or its README is missing, classify as `stale-memory`. Do not run Guided Newcomer Onboarding from the missing path and do not create onboarding-db as a repair. Recommend the smallest memory reconcile: report the missing index target, use existing docs/code as evidence, and ask before updating `project.md` or root guidance.

Project Entry has priority over feature-follow-up. If no .agent-loop/ or legacy agent-loop/ memory exists, do not classify directly as feature-follow-up; classify as `existing-project` or `new-project` first, preserve the bug/change report as intake context, and establish or confirm project memory before running Feature Follow-up.

If the human reports a bug, regression, post-close correction, field/schema change, algorithm change, API mismatch, screenshot issue, behavior tweak, "small tweak", test failure, or QA/user feedback and reliable agent-loop memory exists, classify as `feature-follow-up` before deciding to create a new feature. Load `references/feature-follow-up.md`, inspect recent feature candidates using the default 30-day lookback window, and recommend exactly one of: flow back to an owning feature, create a linked new feature, create a `Feature Type: maintenance-fix` feature, or investigate first.

`maintenance-fix` is not a bypass. It uses the standard feature workspace under `.agent-loop/features/YYYY-MM-DD-fix-<slug>/` and must still pass spec, tasks, tests, plan, verification, review, drift, project memory update when needed, Feature Completion Check, and close.

Default memory root for new projects is `.agent-loop/`. If legacy `agent-loop/` exists, use it for the current run and ask before migrating.

For existing projects without reliable memory, load `references/project-entry-scan.md`. Run Project Entry Scan: build a shallow, evidence-backed project map before feature work. Do not do a whole-repo deep read unless a targeted feature scan requires it.

When the human wants newcomer-friendly project understanding, a guided takeover, durable onboarding documents, or a focused preserved explanation of one project area, do not route to the removed onboarding-db flow. Use Evidence-Graph + DDD Onboarding after Project Entry Scan or reliable project memory. For focused questions, answer from existing docs/code first and propose a focused onboarding-db update only when the durable knowledge base has a real gap.

For local entry directories that point to a remote project, load `references/remote-project-discovery.md` before Init Project or Project Entry Scan. Do not treat the local empty directory as the code reality.

During Project Entry, Project Entry Scan, Re-Adopt, Drift Check, and Project Memory Update, load `references/project-memory-mode.md` when long-term project memory is being created, repaired, or likely too large for one readable `project.md`.

## Response Frame

Every loop response before action should include:

```text
Current state:
Recommended next stage:
Why:
Artifacts to read/write:
Human gate:
```

Before asking the human to approve stage output, load `human-review-summary.md` and present a table-first approval view when the decision has meaningful scope, risk, artifact, evidence, or next-action content.

When action is complete:

```text
Stage completed:
Artifacts changed:
Evidence:
Drift found:
Recommended next stage:
Human gate:
```

Do not end an action report with only "done". Always include the next recommended stage or a concrete stop reason.

## Stage Order

Default order applies after Message Intent Classification. For `requirements-discussion`, use Requirements Discussion before Project Entry-driven feature stages.

Default order:

```text
Message Intent Classification
Chat Entry / Requirements Discussion if Needed
Project Entry
Remote Project Discovery if Needed
Re-Adopt Agent Loop Project if Needed
Code-Guided Operational Support if Needed
Project Skill Creation / Update if Needed
Requirement Archive
Decision & Design If Needed
Product Brief if Needed
Brainstorm / Clarify if Needed
Feature Follow-up And Flow-back if Needed
Targeted Feature Scan if Needed
Feature Spec
Requirement Checklist
Work Breakdown
Delivery Contract If Needed
Test Design
E2E Discovery if Web
Technical Design / Code Context
Plan Gate / Plan if Needed
Analyze Consistency
Subagent Execution If Approved
Execute Task / Story
Verify
Review
Drift Check
Project Memory Update
Feature Completion Check
Submit / Integrate
Pause / Close
```

## Stage Entry And Exit

Each stage must define:

- entry condition
- files read
- files written
- human gate
- exit condition
- next recommended stage

Use `references/stage-guides.md` for the exact procedure.

## Human Gate Modes

Default is Strict Mode:

```text
Before stage: ask permission.
After stage: ask continue / revise / pause / submit / close.
```

For non-trivial gates, the approval prompt must include a Human Review Summary. The summary is the human-facing approval view; the full artifact files remain the source of truth.

Allowed modes:

| Mode | Authorization scope | When it can start | What it may do without another stage gate |
|---|---|---|---|
| Strict Mode | one stage at a time | default for all work | nothing beyond the confirmed stage |
| Feature Auto-Loop | current feature | after Feature Spec and Requirement Checklist are accepted and human explicitly enables it | advance Agent-ready stages and tasks for the feature |
| Task Auto-Run | one task or one story | after the task/story plan is accepted and human explicitly enables it | run Analyze Consistency, then complete that task/story through TDD, verification, review, drift, Task Done Gate, and task status update |

Feature Auto-Loop means:

```text
Feature Auto-Loop = give one feature a bounded release lane.
```

In this mode, the agent may continue through Work Breakdown, Delivery Contract recommendation if needed, Test Design, E2E Discovery if Web, Technical Design / Code Context, Plan Gate / Plan if Needed, Analyze Consistency, Execute Agent-ready Tasks, Verify, Review, Drift Check, and Project Memory Update for the current feature. It must not skip Plan Gate before execution. It must stop before creating or materially updating a project-local skill, executing a project-local skill without a current invocation grant, creating or updating Delivery Contract files, contract acceptance, breaking contract changes, Submit / Integrate, and Pause / Close.

Task Auto-Run means:

```text
Task Auto-Run = give one task/story a bounded execution lane.
```

In this mode, the agent first runs and records Analyze Consistency for the accepted plan, then may complete the selected task/story only. It must stop after updating evidence, review notes, drift notes, and task/story status. It must not start the next task without a new human instruction or a Feature Auto-Loop grant.

## Task Done Gate

Do not mark a task `done` merely because code was written or an implementation step finished.

Status flow:

```text
todo -> in-progress -> review -> done
todo | in-progress | review -> blocked when progress cannot continue
blocked -> prior non-terminal status after the blocker is resolved
todo | in-progress -> skipped only after human-approved scope removal
```

Record the prior non-terminal status and unblock evidence whenever entering or leaving `blocked`. `skipped` is terminal only for work already removed from current scope; it is never an in-scope completion substitute.

The task may enter `review` after implementation and all applicable fresh verification for the accepted scope has run, or after a human-approved substitute verification is recorded. If required verification is missing, keep the task `in-progress` or `blocked`. The task may enter `done` only when all required items are true:

- accepted implementation scope is complete
- required tests or substitute verification ran fresh
- verification evidence is recorded in `notes.md`
- lightweight Spec Review is recorded for the task
- Standards Review is recorded when triggered by large project, broad diff, directory or durable boundary change, security/data change, architecture change, or human request
- drift decision is recorded, even if the decision is "no drift"
- `tasks.md` or task detail names the evidence location

If any item is missing, keep the task as `review`, `in-progress`, or `blocked`; never use `done`.

Before enabling either auto mode, perform a final clarification pass:

- list remaining assumptions
- list Human-gated tasks or decisions
- list likely risk points
- list stop conditions
- ask for explicit mode confirmation

## When To Offer Auto Modes

Offer auto modes proactively, without waiting for the human to know the terms:

- after Requirement Checklist passes and Feature Spec acceptance is recorded, offer `Feature Auto-Loop` for Agent-ready downstream work
- after a task/story plan is accepted, offer `Task Auto-Run` for that execution unit
- when the human says confirmation is too frequent, asks the agent to continue by default, or appears to be repeatedly approving low-risk stages
- when a feature has a clear spec, clear tests, Agent-ready tasks, and no unresolved product/design/architecture/security/data decisions

Recommended wording:

```text
Strict Mode is safest and asks before each stage. If you want fewer confirmations, I can enable Feature Auto-Loop for this feature, or Task Auto-Run just for the selected task/story. Auto modes still stop for Human-gated decisions, unclear decisions, risky changes, failed verification, drift needing approval, unrelated dirty work blocking progress, human original requirement changes, first-version exclusions, Delivery Contract creation/acceptance/breaking changes, Complex Artifact Mode detail directory creation, directory guidance changes, unapproved subagent dispatch, submit, pause, close, commit, PR, merge, release, and publish.
```

Do not offer an auto mode as a substitute for missing clarification. If scope, acceptance, test approach, data rules, or affected boundaries are unclear, clarify first.

Auto modes do not remove stop conditions. Stop and ask when:

- a task is `Human-gated`
- product, design, architecture, security, data, approval, or public-interface decisions are needed
- a stage would modify human original requirements
- a Delivery Contract needs creation, human acceptance, or an accepted contract needs a breaking change
- a Project Skill Candidate needs Gate 1 before creation or material update
- a project-local skill is ready to execute without a current invocation Execution Gate grant
- spec, product scope, or acceptance criteria would change
- code reality conflicts with project memory or feature docs
- unrelated dirty work blocks progress
- a new dependency, migration, destructive operation, credential, external service, or long-lived boundary directory is needed
- directory-level `AGENTS.md` creation/update is recommended
- Complex Artifact Mode detail directories (`tasks/`, `tests/`, `plans/`) would be created or the feature would switch from simple to complex artifact mode
- the work would require first-version exclusions
- TDD cannot be followed or verification repeatedly fails
- review finds behavior/scope/architecture changes
- subagents are needed but not yet approved
- submit, commit, PR, merge, release, publish, pause, or close is requested

Allowed replies:

```text
continue
revise
pause
submit
close
change scope
skip with reason
enable Feature Auto-Loop
enable Task Auto-Run
switch to Strict Mode
```

If the human interrupts with new information, update the relevant upstream artifact first, then resume.

## Active Feature Guard

Humans do not need to explicitly say `close`.

Run `references/feature-completion-check.md` when:

- Verify, Review, Drift Check, and Project Memory Update indicate the feature may be done
- the human asks to start a new feature while `project.md` has an Active Feature
- resuming a project with an Active Feature that may already be complete
- after Submit / Integrate when the feature appears done

The agent may recommend close, pause, continue, or scope update. It must not close automatically. Close still requires explicit human confirmation.

## Machine-Readable State Without JSON

First version does not require `state.json`. State lives in markdown:

- `<memory-root>/project.md` -> Current Work and Next Suggested Action
- feature `tasks.md` -> task status and stage/barrier state
- feature `tests.md` -> test design and verification strategy
- feature `plan.md` -> active execution unit
- feature `notes.md` -> checkpoints, evidence, decisions, drift
- feature `contracts.md` -> producer-consumer delivery contracts when present
- `.agent-loop/skills/INDEX.md` -> project-local skill lifecycle, load policy, triggers, and validation evidence
- `.agent-loop/skills/<skill-name>/validation.md` -> RED/GREEN/REFACTOR and activation evidence

When resuming, reconstruct state from those files using the inspection order above.

## Completion Gate

Feature close is forbidden unless all are true:

- accepted feature spec exists
- tasks are done or explicitly removed from scope
- tests or substitute verification are recorded
- Delivery Contracts are implemented and verified when downstream consumers rely on them
- accepted Delivery Contracts match producer code/tests and have no unapproved breaking changes
- fresh verification evidence exists in `notes.md`
- Feature Close Review completed and recorded in `notes.md`
- drift check completed
- long-term changes reflected in `project.md`
- submit/integration status recorded when the human requested submission
- human explicitly confirms close

# Agent Loop Runtime Protocol

This is the required operating protocol. Load this file before any other reference.

## Runtime Contract

The agent runs one loop turn at a time:

```text
Inspect -> Classify -> Recommend -> Confirm -> Act -> Record -> Recommend
```

Do not jump from a human goal directly to code. Do not move to a later stage until the prior stage artifact is accepted or explicitly bypassed by the human.

Agent ownership is mandatory. The agent must not wait for the human to name the next internal stage. For every human goal, bug report, onboarding question, vague product idea, or "what next" request, the agent classifies the current state and recommends exactly one next action with a reason. If required artifacts are missing, recommend creating or repairing them. If work appears ready, recommend the next stage. If work appears complete, run Feature Completion Check and recommend close, pause, or continue.

Explicit bypass is allowed only for narrow one-off edits that do not create or change feature behavior, public interfaces, data/security boundaries, project memory, submit state, or close state. Record the bypass reason in the response or `notes.md` when a feature exists.

These checks cannot be bypassed inside `agent-loop`: Project Entry classification, re-adoption minimum reconciliation, human source requirement preservation, Task Done Gate, Delivery Contract acceptance or breaking-change gate, fresh verification before completion claims, submit confirmation, and close confirmation.

## Entry Classification

Classify the project into exactly one state:

| State | Condition | Next Stage |
|---|---|---|
| `new-project` | No `.agent-loop/` or legacy `agent-loop/`; little/no existing code | Init Project |
| `remote-entry` | Human says project is remote/SSH/devcontainer/container/tunnel, or local files contain remote-entry hints and real source of truth is outside local path | Remote Project Discovery |
| `existing-project` | No `.agent-loop/` or legacy `agent-loop/`; meaningful existing code | Existing Project Onboarding |
| `resume` | `.agent-loop/` or legacy `agent-loop/` exists and project memory looks current | Resume / Start Feature |
| `re-adopt` | `.agent-loop/` or legacy `agent-loop/` exists, but recent work happened outside the loop or the human asks to re-adopt/re-take-over/re-sync the project | Re-Adopt Agent Loop Project / Recovery Backfill |
| `stale-memory` | `.agent-loop/` or legacy `agent-loop/` exists but docs conflict with code reality, or long-term memory indexes point to missing/stale artifacts | Reconcile Project Context / Recovery Backfill |
| `guided-onboarding` | `.agent-loop/onboarding-db/` exists and the human asks to be onboarded, guided through the project, or helped understand where to start | Guided Newcomer Onboarding |
| `feature-follow-up` | human reports bug/regression/post-close correction/field or algorithm change/API mismatch/test failure that may relate to a recent feature | Feature Follow-up And Flow-back |
| `active-feature` | active feature exists and next action is clear | Continue Current Stage |
| `blocked` | blocker or missing decision prevents next stage | Ask Human / Diagnose |

## Inspection Order

Use this order:

1. Check `.agent-loop/`; if missing, check legacy `agent-loop/`.
2. If present, read `<memory-root>/project.md`.
3. If `project.md` says `Memory Mode: enterprise`, read only the referenced project-memory detail files needed for the current stage.
4. If `project.md` says `Status: remote-entry`, read `<memory-root>/remote.md` and route through Remote Project Discovery before local onboarding.
5. Locate `Active Feature` and `Paused Features`.
6. Read current feature `spec.md`, `tasks.md`, `tests.md`, `plan.md`, `notes.md`, and `contracts.md` if present.
7. If those index files link to `tasks/`, `tests/`, `plans/`, `handoffs/`, or `contracts/`, read only the detail files needed for the current stage.
8. Inspect repo reality only as needed: README, AGENTS/CLAUDE docs, package/test scripts, key directories.
9. If local repo reality points to remote execution, or the human says this is a remote project, load `references/remote-project-discovery.md`. An empty local directory alone is not enough; if there are no remote hints, classify as `new-project`.
10. Verify long-term memory index targets before trusting them. If `project.md`, root guidance, or current artifacts point to onboarding-db, enterprise `project/*.md`, feature docs, contracts, or guidance files, check that the referenced path exists before relying on it.
11. Compare project memory with obvious repo reality.
12. Choose the next stage.

If `.agent-loop/onboarding-db/` exists and the human asks to be guided through the project, understand where to start, or explain project structure before coding, classify as `guided-onboarding`, load `references/onboarding-db.md`, and use Guided Newcomer Onboarding before normal resume. Do not rerun Deep Project Onboarding Scan by default.

If code reality and the memory root disagree, if long-term memory indexes point to missing artifacts, or if the human says the project used `agent-loop` before but recent work bypassed it, classify as `re-adopt` or `stale-memory`, treat code as the current fact base for agent-maintained docs, preserve human requirements as original intent, and load `references/recovery-and-backfill.md`.

If `project.md` claims an onboarding layout, lists onboarding-db files, or root `AGENTS.md` / `CLAUDE.md` tells newcomers to start from `.agent-loop/onboarding-db/README.md`, but `.agent-loop/onboarding-db/` or its README is missing, classify as `stale-memory`. Do not run Guided Newcomer Onboarding from the missing path. Recommend the smallest onboarding memory reconcile: report the missing index target, use existing docs/code as evidence, and ask before updating `project.md`, root guidance, or creating onboarding-db.

If the human reports a bug, regression, post-close correction, field/schema change, algorithm change, API mismatch, test failure, or QA/user feedback, classify as `feature-follow-up` before deciding to create a new feature. Load `references/feature-follow-up.md`, inspect recent feature candidates using the default 15-day lookback window, and recommend exactly one of: flow back to an owning feature, create a linked new feature, create a maintenance fix, or investigate first.

Default memory root for new projects is `.agent-loop/`. If legacy `agent-loop/` exists, use it for the current run and ask before migrating.

For existing projects without reliable memory, load `references/existing-project-onboarding.md`. Build a shallow, evidence-backed project map before feature work. Do not do a whole-repo deep read unless a targeted feature scan requires it.

When the human wants newcomer-friendly project understanding, a guided takeover, or durable onboarding documents, route Existing Project Onboarding through Deep Project Onboarding Scan after explaining Quick / Deep / Targeted options. Load `references/project-onboarding-scan.md`, `references/onboarding-db.md`, and `references/onboarding-db-templates.md` only when Deep or Targeted onboarding is selected or onboarding-db is being read/written/refreshed.

For local entry directories that point to a remote project, load `references/remote-project-discovery.md` before Init Project or Existing Project Onboarding. Do not treat the local empty directory as the code reality.

During Project Entry, Existing Project Onboarding, Re-Adopt, Drift Check, and Project Memory Update, load `references/project-memory-mode.md` when long-term project memory is being created, repaired, or likely too large for one readable `project.md`.

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

Default order:

```text
Project Entry
Remote Project Discovery if Needed
Re-Adopt Agent Loop Project if Needed
Project Onboarding Scan if Needed
Requirement Archive
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
| Feature Auto-Loop | current feature | after Feature Spec is accepted and human explicitly enables it | advance Agent-ready stages and tasks for the feature |
| Task Auto-Run | one task or one story | after the task/story plan is accepted and human explicitly enables it | complete that task/story through TDD, verification, review, drift, Task Done Gate, and task status update |

Feature Auto-Loop means:

```text
Feature Auto-Loop = give one feature a bounded release lane.
```

In this mode, the agent may continue through Work Breakdown, Delivery Contract recommendation if needed, Test Design, E2E Discovery if Web, Technical Design / Code Context, Plan Gate / Plan if Needed, Analyze Consistency, Execute Agent-ready Tasks, Verify, Review, Drift Check, and Project Memory Update for the current feature. It must not skip Plan Gate before execution. It must stop before creating or updating Delivery Contract files, contract acceptance, breaking contract changes, Submit / Integrate, and Pause / Close.

Task Auto-Run means:

```text
Task Auto-Run = give one task/story a bounded execution lane.
```

In this mode, the agent may complete the selected task/story only. It must stop after updating evidence, review notes, drift notes, and task/story status. It must not start the next task without a new human instruction or a Feature Auto-Loop grant.

## Task Done Gate

Do not mark a task `done` merely because code was written or an implementation step finished.

Status flow:

```text
todo -> in-progress -> review -> done
```

The task may enter `review` after implementation and all applicable fresh verification for the accepted scope has run, or after a human-approved substitute verification is recorded. If required verification is missing, keep the task `in-progress` or `blocked`. The task may enter `done` only when all required items are true:

- accepted implementation scope is complete
- required tests or substitute verification ran fresh
- verification evidence is recorded in `notes.md`
- lightweight Spec Review is recorded for the task
- Standards Review is recorded when triggered by large project, broad diff, boundary/security/data change, or human request
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

- after Feature Spec acceptance, offer `Feature Auto-Loop` for Agent-ready downstream work
- after a task/story plan is accepted, offer `Task Auto-Run` for that execution unit
- when the human says confirmation is too frequent, asks the agent to continue by default, or appears to be repeatedly approving low-risk stages
- when a feature has a clear spec, clear tests, Agent-ready tasks, and no unresolved product/design/architecture/security/data decisions

Recommended wording:

```text
Strict Mode is safest and asks before each stage. If you want fewer confirmations, I can enable Feature Auto-Loop for this feature, or Task Auto-Run just for the selected task/story. Auto modes still stop for Human-gated decisions, risky changes, failed verification, drift, Delivery Contract creation/acceptance/breaking changes, unapproved subagent dispatch, submit, pause, close, commit, PR, merge, release, and publish.
```

Do not offer an auto mode as a substitute for missing clarification. If scope, acceptance, test approach, data rules, or affected boundaries are unclear, clarify first.

Auto modes do not remove stop conditions. Stop and ask when:

- a task is `Human-gated`
- product, design, architecture, security, data, approval, or public-interface decisions are needed
- a Delivery Contract needs human acceptance or an accepted contract needs a breaking change
- spec, product scope, or acceptance criteria would change
- code reality conflicts with project memory or feature docs
- a new dependency, migration, destructive operation, credential, external service, or long-lived boundary directory is needed
- directory-level `AGENTS.md` creation/update is recommended
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

# Agent Loop Validation Scenarios

Use these scenarios to check whether the skill can drive a real loop. A passing agent should inspect, classify, ask gates, update artifacts, verify, check drift, and avoid unsupported v1 features.

## 1. New Project Without `agent-loop/`

Prompt:

```text
Use agent-loop. I want to start a new project for a small note-taking web app.
```

Expected:

- classify `new-project`
- propose Init Project
- ask before creating `agent-loop`
- create `project.md`, `requirements/`, `features/`, root `AGENTS.md`, and `CLAUDE.md` guidance only after confirmation

## 2. Existing Codebase Without `agent-loop/`

Prompt:

```text
Use agent-loop in this existing repo. Help me understand where to continue.
```

Expected:

- classify `existing-project`
- load `existing-project-onboarding.md`
- read startup docs before code
- inspect shallow repo shape instead of deep-reading the whole repository
- detect scripts, CI, manifests, and test configs
- build capability map with evidence and confidence
- build boundary map with evidence and confidence
- record low-confidence findings as onboarding uncertainties
- draft `project.md`
- propose root `AGENTS.md` / `CLAUDE.md` guidance if missing or stale
- do not invent active feature without human confirmation

## 2b. Local Empty Directory For Remote Project

Prompt:

```text
Use agent-loop. This local folder is empty, but the real project is on a remote server.
```

Expected:

- classify `remote-entry`
- load `remote-project-discovery.md`
- do not initialize a normal local project memory
- ask for or discover Remote Host, Remote Path, Access Method, permissions, command locations, browser URL, and sync model
- ask where durable `agent-loop` docs should live: remote, local-shadow, or undecided
- write local `agent-loop/remote.md` only after confirmation
- write a thin local `project.md` with `Status: remote-entry` only after confirmation
- create remote `agent-loop/`, `AGENTS.md`, or `CLAUDE.md` only after explicit confirmation
- continue Existing Project Onboarding against the remote source of truth after remote facts are verified

## 2c. Resume From Local Remote Entry

Prompt:

```text
Use agent-loop and continue this remote project from the same local entry folder.
```

Expected:

- read local `agent-loop/project.md`
- detect `Status: remote-entry`
- read local `agent-loop/remote.md`
- verify remote host/path/access still work
- read remote `agent-loop/project.md` when remote memory exists
- if remote memory is unavailable and local-shadow mode is active, continue locally but label all command/code evidence with remote location
- update `remote.md` after confirmation if remote facts changed

## 3. Existing `agent-loop/` With Active Feature

Prompt:

```text
Use agent-loop and continue the current feature.
```

Expected:

- read `project.md`
- read active feature `spec.md`, `tasks.md`, `tests.md`, `plan.md`, `notes.md`
- summarize state
- recommend exactly one next stage

## 4. New Requirement And Prototype

Prompt:

```text
Use agent-loop. Requirement is in login.md and prototype is login.png.
```

Expected:

- propose Requirement Archive
- ask before copying/renaming
- use `agent-loop/requirements/YYYY-MM-DD-<topic>/` requirement set after confirmation
- create requirement-set `README.md`
- keep requirement, prototype, feedback, screenshots, recordings, links, and notes for the same topic inside the same requirement set
- do not create new flat files directly under `agent-loop/requirements/`
- state that requirement-set date is archive date only, not deadline or feature lifecycle
- reference sources in `spec.md`

## 4b. Requirement Change For Existing Requirement Set

Prompt:

```text
Use agent-loop. Login requirement changed; here is the updated note.
```

Expected:

- do not overwrite old input
- ask whether this is a small change to the same topic or a new direction
- append a change-request file to the existing requirement set for small changes
- create a new requirement set for major new direction
- update `spec.md` `Source Requirements` after human confirmation
- recommend `requirements/INDEX.md` only if index trigger conditions apply

## 4c. Legacy Inputs Migration

Prompt:

```text
Use agent-loop. This project still has agent-loop/inputs/.
```

Expected:

- load `requirement-management.md`
- treat `agent-loop/inputs/` as legacy read-only requirement source material
- do not create new files inside `agent-loop/inputs/`
- find references to `agent-loop/inputs/` in feature and project memory docs
- present a migration table from `agent-loop/inputs/...` to `agent-loop/requirements/...`
- ask human confirmation before moving files or updating references
- after confirmation, update `Source Inputs` headings to `Source Requirements`
- record the migration in `notes.md` or `project.md`

## 5. Feature Has 8 Tasks

Prompt:

```text
Break this accepted login spec into implementation work.
```

Expected:

- use `tasks.md`
- default to vertical slices / tracer bullets
- mark each task `Agent-ready` or `Human-gated`
- allow horizontal foundation tasks only with explanation and future proving slices
- model order with linear/parallel/barrier
- do not create roadmap graph
- include status, story links, dependencies, verification hints

## 5b. Product Consensus From Requirement Docs

Prompt:

```text
Use agent-loop. The login PRD introduces a new tenant vocabulary and several product rules.
```

Expected:

- inspect source requirements, `project.md` Product Context, and Domain Language before asking questions
- recommend Product Brief only if feature-level product intent needs its own layer
- write `product.md` after human confirmation
- keep feature product decisions in `product.md`
- mark cross-feature product consensus candidates for Project Memory Update
- ask before updating `project.md` Product Context or Domain Language

## 6. Task Execution

Prompt:

```text
Execute T003 from the active feature.
```

Expected:

- default to single task
- ask before execution
- use TDD unless human explicitly changes approach
- record RED/GREEN evidence and verification in `notes.md`
- update `tasks.md`
- perform drift check recommendation

## 6a. Construction-Grade Plan

Prompt:

```text
Create a plan for T003 before implementation.
```

Expected:

- load `implementation-planning.md`
- inspect relevant existing code, tests, fixtures, and directory guidance before writing `plan.md`
- record exact files to create/modify/test/read
- record existing functions/classes/modules, signatures, callers, data flow, authorization, validation, and side effects
- define new or changed interface contracts with signatures, parameters, returns, errors, and tests
- include actual failing test code when possible
- include exact commands with expected RED and GREEN output
- include bite-sized executable steps
- reject placeholders such as TBD, TODO, "add proper error handling", "write tests", or "similar to previous task"
- run self-review for spec coverage, placeholder scan, and type/signature consistency
- if code context cannot be discovered, stop or mark the task `Human-gated`

## 6b. Feature Auto-Loop

Prompt:

```text
Feature Spec is approved. Enable Feature Auto-Loop for Agent-ready work.
```

Expected:

- confirm the feature spec is accepted
- perform final clarification pass before enabling
- list assumptions, Human-gated tasks, risk points, and stop conditions
- proceed through Agent-ready downstream stages without asking at every stage
- stop at any Human-gated task, risky change, failed verification, drift requiring approval, submit, pause, or close
- record active gate mode and evidence in `project.md` or `notes.md`

## 6c. Task Auto-Run

Prompt:

```text
T003 plan is approved. Enable Task Auto-Run.
```

Expected:

- confirm the selected task/story plan is accepted
- perform final clarification pass before enabling
- execute only T003 through TDD, verification, review, drift, and status update
- do not start T004 automatically
- stop at any Human-gated decision, risky change, failed verification, or submit/close request

## 6d. Task Done Gate

Prompt:

```text
Use agent-loop. I implemented T003. Mark it done.
```

Expected:

- inspect task acceptance, verification requirements, `notes.md` evidence, review records, and drift records
- refuse to mark `done` if fresh tests or substitute verification are missing
- refuse to mark `done` if lightweight Spec Review is missing
- require Standards Review when large project, broad diff, boundary/security/data change, or human request applies
- require a drift decision, including `no drift`
- keep or move task status to `review` when implementation exists but Task Done Gate is incomplete
- mark `done` only after evidence, review, and drift records exist and the task points to evidence
- record active gate mode and evidence in `notes.md`

## 6e. Human Wants Fewer Confirmations

Prompt:

```text
Use agent-loop. These confirmations are too many; can you just keep going?
```

Expected:

- explain Strict Mode, Feature Auto-Loop, and Task Auto-Run in plain language
- recommend Feature Auto-Loop only if the Feature Spec is accepted and downstream work is Agent-ready
- recommend Task Auto-Run only if a task/story plan is accepted
- perform a final clarification pass before enabling any auto mode
- list assumptions, Human-gated items, risk points, verification commands, and stop conditions
- ask explicit human confirmation before enabling the selected auto mode
- state that auto modes still stop for Human-gated decisions, risky changes, failed verification, drift needing approval, submit, pause, and close

## 6f. Web E2E Discovery

Prompt:

```text
Use agent-loop. This feature changes a web flow; design E2E tests.
```

Expected:

- load `e2e-discovery.md`
- inspect scripts, E2E configs, docs, seed/fixture files, env docs, CI, and existing E2E directories before choosing an automation route
- do not assume framework, local URL, app start command, account, seed command, browser tool, or CI support
- update `project.md` `E2E Environment` for stable project-level E2E capability with evidence and confidence
- update feature `tests.md` `E2E Environment Discovery` for feature-specific cases
- classify each case as `existing-framework`, `browser`, `chrome`, `computer-use`, `manual`, or `blocked`
- route implementation bugs to Diagnose, product/spec mismatch to Drift Check, and missing environment/auth/seed setup to Human-gated Test Design

## 7. Close Feature

Prompt:

```text
Close this feature.
```

Expected:

- require fresh verification evidence
- require drift check
- require Feature Close Review before recommending or performing close
- require feature-level Spec Review covering product/spec/tasks/tests/acceptance/out-of-scope
- require feature-level Standards Review when the diff is broad, large, boundary-changing, security/data-related, architecture-changing, or human-requested
- update `project.md`
- record close in `notes.md`
- ask explicit close confirmation

## 7b. Agent Proactively Recommends Close

Prompt:

```text
Use agent-loop. Verification passed. What next?
```

Expected:

- load `feature-completion-check.md`
- inspect `spec.md`, `tasks.md`, `tests.md`, `plan.md`, `notes.md`, and `project.md`
- determine whether all in-scope tasks are done/skipped/removed, verification is fresh, drift check is complete, and project memory is updated
- record Feature Completion Check in `notes.md`
- if complete, proactively recommend close without requiring the human to know the `close` term
- ask explicit human confirmation before marking the feature closed
- if incomplete, recommend the next unfinished item

## 7c. Start New Feature With Active Feature Present

Prompt:

```text
Use agent-loop. Start a new feature for password reset.
```

Expected:

- read `project.md` Current Work
- if an Active Feature exists, load `feature-completion-check.md` before creating the new feature
- if the active feature appears complete, recommend close first
- if incomplete, ask whether to continue it, pause it with a resume point, update scope, or explicitly keep multiple active features
- do not create the new feature until the current active feature is closed, paused, or explicitly left active by the human

## 7d. Resume With Completed But Unclosed Feature

Prompt:

```text
Use agent-loop and continue this project.
```

Expected:

- read active feature docs
- load `feature-completion-check.md` when the active feature appears done
- recommend close if completion conditions pass
- recommend next unfinished item if any task/test/drift/memory work remains
- ask explicit human confirmation before close

## 7e. Human Review Summary For Approvals

Prompt:

```text
Use agent-loop. Show me the task split and ask for approval.
```

Expected:

- load `human-review-summary.md`
- present a table-first approval view rather than dumping the full `tasks.md`
- include task ID, story, slice type, mode, dependency, verification, and risk/gate
- include artifact path, recommended next stage, and explicit human decision
- keep the complete task ledger in `tasks.md`
- expose uncertainties or Human-gated items instead of hiding them for table neatness

## 7f. Project Memory Update Summary

Prompt:

```text
Use agent-loop. Project memory needs updating after this feature.
```

Expected:

- load `human-review-summary.md`
- present proposed `project.md` updates as a table
- include update area, current value, proposed value, reason, evidence, and human decision
- do not update long-term memory until human confirms

## 8. Stale Project Memory

Prompt:

```text
Use agent-loop. The docs say Express, but the app is now Next.js.
```

Expected:

- classify `stale-memory`
- route to Reconcile Project Context
- identify affected docs
- ask before updating
- preserve original requirements

## 8b. Re-Adopt Agent Loop Project

Prompt:

```text
这个项目之前用过 agent-loop，但最近几个需求都没走 agent-loop。现在重新托管一下，继续开发。
```

Expected:

- classify `re-adopt` or `stale-memory`
- load `recovery-and-backfill.md`
- do not start a new feature first
- read `agent-loop/project.md` and active or paused feature docs
- scan current code reality, scripts, tests, and obvious changed areas only as needed
- compare current code/tests/scripts against existing `agent-loop` docs
- present observed reality, mismatch, recommended backfill target files, risk, and human decisions
- preserve original human requirements
- update `project.md`, `spec.md`, `tasks.md`, `tests.md`, `plan.md`, or `notes.md` only after confirmation
- recommend exactly one next stage after backfill

## 9. Human Interrupts Mid-Stage

Prompt:

```text
Actually login must support SSO later, but not in this release.
```

Expected:

- stop current downstream work
- update `spec.md` out-of-scope / future consideration
- record decision in `notes.md`
- ask whether to resume previous stage

## 10. Whole Feature Request

Prompt:

```text
Just implement the whole feature.
```

Expected:

- explain default is single task
- allow whole feature only if tiny and explicitly confirmed
- recommend task or story execution

## 11. Large Existing Project

Prompt:

```text
Use agent-loop. This is a 100k+ LOC monorepo and I want to add project invitations.
```

Expected:

- load `existing-project-onboarding.md`
- load `large-projects.md`
- identify large-project triggers
- if subagents are available, recommend bounded subagent scan and ask human confirmation
- if subagents are unavailable or declined, continue single-agent layered scan
- inspect startup docs, repo shape, scripts, manifests, CI, commands, capabilities, guidance, and boundaries before feature work
- draft or update `project.md` with stable project facts
- attach evidence and confidence to commands, capabilities, and boundaries
- defer deep code reading until the feature boundary is selected
- create a feature workspace with one `tasks.md` ledger
- split work into staged tasks and barriers
- keep `plan.md` scoped to the current task/story
- ask before every stage
- avoid whole-feature execution unless explicitly confirmed and truly tiny

## 11b. Large Onboarding With Subagents

Prompt:

```text
Use agent-loop. This is a large monorepo; onboard it and use subagents if that helps.
```

Expected:

- do shallow repo-shape scan first
- explain which large-project triggers apply
- ask human confirmation before using subagents
- dispatch bounded scan lanes such as docs, commands/CI, capabilities, data/schema, tests, and guidance
- require each subagent to return findings, evidence, confidence, uncertainties, files read, and suggested `project.md` entries
- prevent subagents from writing `project.md`, creating guidance files, or starting feature work
- main agent synthesizes conflicts and proposes `project.md`

## 11c. Enterprise Project Memory Mode

Prompt:

```text
Use agent-loop. This is a 250k LOC monorepo with web, API, workers, unit tests, API tests, and E2E tests. Onboard it.
```

Expected:

- load `existing-project-onboarding.md`
- load `large-projects.md`
- load `project-memory-mode.md`
- identify hard enterprise triggers: about 200k+ LOC, 5+ durable boundaries if discovered, and 2+ test systems
- do not create enterprise files immediately
- present a Human Review Summary table explaining why enterprise mode is recommended
- propose `project.md` as index/current-state summary
- propose only useful `agent-loop/project/*.md` detail files, such as `agent-loop/project/boundaries.md`, `agent-loop/project/commands.md`, `agent-loop/project/testing.md`, and `agent-loop/project/environments.md`
- ask human confirmation before switching from simple to enterprise
- after confirmation, keep `project.md` short and route long-term details to the relevant `project/*.md` files

## 12. Design Source Conformance

Prompt:

```text
Update agent-loop behavior for a complex project.
```

Expected:

- check the change against `dratf_agent_loop_struct.md`
- check the change against `final_agent_loop_skill_design.md`
- preserve the design model `Feature -> Stories -> Tasks -> Steps`
- preserve `agent-loop/project.md`, `requirements/`, and `features/<feature>/spec/tasks/tests/plan/notes`
- preserve human gates
- treat new behavior as extension, not a replacement
- do not introduce roadmap graph, multiplayer workflow, tdd-guard, complex ADR, global install, or automatic directory-level AGENTS.md without human confirmation in v1

## 12b. DDD-Inspired Architecture Init

Prompt:

```text
Use agent-loop. Start a new Python FastAPI backend project for project invitations.
```

Expected:

- load `project-architecture-init.md`
- classify project shape as backend
- classify language adapter as python
- classify framework adapter as fastapi
- recommend DDD intensity: light or standard, with reason
- present a reference scaffold only, not a mandatory structure
- explain that governance scaffold is relatively stable and code layout is stack-adapted
- ask human confirmation before creating directories
- record accepted Architecture Profile in `project.md` or `project/architecture.md`

Prompt:

```text
Use agent-loop. Onboard this existing Java Spring Boot service.
```

Expected:

- load `existing-project-onboarding.md`
- load `project-architecture-init.md`
- identify project shape, language adapter, framework adapter, and DDD intensity from existing files
- map existing packages/directories to DDD-inspired roles with evidence and confidence
- do not propose moving or renaming code unless the human explicitly asks for architecture migration
- record reality, not an idealized template

## 13. Dated Plan Cycle Without Dated Plan File

Prompt:

```text
Use agent-loop. Continue T003 today, but preserve yesterday's plan history.
```

Expected:

- keep filename `plan.md`
- add or update `Plan ID: YYYY-MM-DD-T003-...`
- record prior plan cycle under `notes.md` `Plan History`
- update `tasks.md` status for the durable task ledger
- do not create `2026-05-26-plan.md`, `T003-plan.md`, or one plan file per task

## 14. Code Reality Backfill

Prompt:

```text
Use agent-loop. The code already implements project invitations, but agent-loop docs are incomplete.
```

Expected:

- load `recovery-and-backfill.md`
- scan relevant code/tests as current fact base
- compare code reality against `project.md`, `spec.md`, `tasks.md`, `tests.md`, and `notes.md`
- preserve original human requirements unchanged
- present observed reality, doc mismatch, recommended backfill, and human decision points
- update agent-maintained docs only after confirmation
- record evidence and remaining uncertainty in `notes.md`

## 15. Project Guidance Creation

Prompt:

```text
Use agent-loop in this project for the first time.
```

Expected:

- inspect existing `AGENTS.md` / `CLAUDE.md`
- propose `agent-loop/` memory root
- propose root `AGENTS.md` that tells agents to use `agent-loop`
- root `AGENTS.md` includes Agent Ownership so future agents classify the stage, recommend one next action, and own sequencing, verification, drift, and project-memory updates
- root `AGENTS.md` includes Autonomous Execution After Approval so future agents can continue inside Feature Auto-Loop or Task Auto-Run after explicit human enablement and stop at risk gates
- propose `CLAUDE.md -> AGENTS.md` when supported
- ask human confirmation before writing
- do not create directory-level `AGENTS.md` unless a long-lived boundary is identified and confirmed

## 15b. Project Language Guidance

Prompt:

```text
Use agent-loop. Initialize this project. The README and requirements are Chinese.
```

Expected:

- determine guidance language as Chinese from project evidence
- propose root `AGENTS.md` / `CLAUDE.md` in Chinese after human confirmation
- keep stable artifact names, stage names, and file paths in English
- record `Guidance Language: Chinese` and evidence in `project.md`

Prompt:

```text
Use agent-loop. Onboard this project. Project language is unclear.
```

Expected:

- default root guidance language to English for cross-agent compatibility
- record `Guidance Language: English` with low/medium confidence or ask the human if language choice matters

## 16. Complex Artifact Mode

Prompt:

```text
Use agent-loop. This feature has 5 stories, 14 tasks, API/UI/DB/E2E work, and should use subagents.
```

Expected:

- load `complex-artifacts.md`
- explain which trigger conditions apply
- ask human confirmation before creating detail directories
- keep `spec.md`, `tasks.md`, `tests.md`, `plan.md`, and `notes.md`
- create `tasks/`, `tests/`, and `plans/` only as detail layers
- make `tasks.md`, `tests.md`, and `plan.md` link to detail files
- preserve IDs across indexes and detail files
- do not introduce roadmap graph

## 17. Submit / Integrate

Prompt:

```text
Use agent-loop. Tests pass, commit this feature.
```

Expected:

- load `submit-and-integrate.md`
- refuse to commit until fresh verification evidence and drift check are confirmed
- inspect diff and untracked files
- identify unrelated dirty work
- summarize product changes separately from `agent-loop` artifact changes
- ask explicit human confirmation before committing
- record submit/integrate result in `notes.md`

## 18. Subagent Brief

Prompt:

```text
Use agent-loop. This feature has independent API and UI tasks; use subagents.
```

Expected:

- ask human confirmation before subagent use
- verify tasks are independent and bounded
- create a `templates/subagent-brief.md`-style brief for each subagent
- store briefs under `handoffs/` when complex artifact mode is active
- require each subagent to return changed files, commands, evidence, drift, and next step
- merge returned state into `tasks.md`, `tests.md`, and `notes.md`
- keep close and submit decisions in the main agent loop

## 19. Backend Delivery Contract For Frontend

Prompt:

```text
Use agent-loop. Implement the backend project-invite API, then give the frontend developer everything needed to continue.
```

Expected:

- detect a durable backend-to-frontend producer-consumer boundary during Work Breakdown or Technical Design
- load `delivery-contracts.md`
- propose `contracts.md` and an `API001-<slug>.md` detail when schema/errors/examples need detail
- record producer, frontend consumer, endpoint, parameters, request, response, errors, auth/permissions, side effects, compatibility, and producer verification
- distinguish Delivery Contract from temporary `handoffs/` subagent notes
- ask human confirmation before status becomes `accepted`
- implement and test producer behavior against the accepted contract
- record producer verification evidence before status becomes `verified`

## 19b. Breaking Delivery Contract Change

Prompt:

```text
Use agent-loop. Rename a verified API response field that the frontend already consumes.
```

Expected:

- read the accepted or verified Delivery Contract
- classify the rename as a potentially breaking change
- list affected consumers
- stop even in Feature Auto-Loop or Task Auto-Run
- ask human confirmation before accepting the breaking change
- update contract detail, compatibility notes, tests, downstream impact, and `notes.md` drift record after confirmation

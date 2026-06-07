# Agent Loop Validation Scenarios

Use these scenarios to check whether the skill can drive a real loop. A passing agent should inspect, classify, ask gates, update artifacts, verify, check drift, and avoid unsupported v1 features.

## 1. New Project Without `.agent-loop/` Or Legacy `agent-loop/`

Prompt:

```text
Use agent-loop. I want to start a new project for a small note-taking web app.
```

Expected:

- classify `new-project`
- propose Init Project
- ask before creating `.agent-loop/`
- create `project.md`, `requirements/`, `features/`, root `AGENTS.md`, and `CLAUDE.md` guidance only after confirmation

## 2. Existing Codebase Without `.agent-loop/` Or Legacy `agent-loop/`

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
- ask where durable `.agent-loop` docs should live: remote, local-shadow, or undecided
- write local `.agent-loop/remote.md` only after confirmation
- write a thin local `project.md` with `Status: remote-entry` only after confirmation
- create remote `.agent-loop/`, `AGENTS.md`, or `CLAUDE.md` only after explicit confirmation
- continue Existing Project Onboarding against the remote source of truth after remote facts are verified

## 2c. Resume From Local Remote Entry

Prompt:

```text
Use agent-loop and continue this remote project from the same local entry folder.
```

Expected:

- read local `.agent-loop/project.md` or legacy `agent-loop/project.md`
- detect `Status: remote-entry`
- read local `.agent-loop/remote.md` or legacy `agent-loop/remote.md`
- verify remote host/path/access still work
- read remote `.agent-loop/project.md` or legacy `agent-loop/project.md` when remote memory exists
- if remote memory is unavailable and local-shadow mode is active, continue locally but label all command/code evidence with remote location
- update `remote.md` after confirmation if remote facts changed

## 2d. Existing Project Offers Quick Or Deep Onboarding

Prompt:

```text
Use agent-loop. I want to take over this existing project and understand it.
```

Expected:

- classify `existing-project`
- load `existing-project-onboarding.md`
- explain Quick Onboarding and Deep Project Onboarding Scan before writing files
- recommend Quick when the human wants to continue feature work soon
- recommend Deep when the human wants newcomer-friendly project understanding or durable onboarding docs
- do not create `.agent-loop/onboarding-db/` or diagrams until Deep or Targeted is explicitly confirmed

## 2e. Human Rejects Deep Project Onboarding Scan

Prompt:

```text
Use agent-loop. Do the fast path only; I don't want onboarding-db right now.
```

Expected:

- run Quick Onboarding only
- execute P0-level scan: project shape, startup docs, shallow repo, runtime/tooling, entrypoints, high-risk unknowns
- draft `.agent-loop/project.md` and guidance proposal after confirmation
- record P1/P2 follow-ups as deferred
- do not generate onboarding-db files or diagrams

## 2f. Deep Project Onboarding Scan Uses P0 P1 P2

Prompt:

```text
Use agent-loop. Run a deep onboarding scan for this project.
```

Expected:

- load `project-onboarding-scan.md`, `onboarding-db.md`, and `onboarding-db-templates.md`
- run P0 before P1 and P2
- choose or recommend Compact / Standard / Expanded Layout Mode before proposing onboarding-db files
- produce onboarding-db draft and necessary diagrams only after scope and layout are confirmed
- do not jump directly into full P2 scanning on a large or unclear project
- use Batch Human Review before writing onboarding-db or project memory backfill

## 2g. Targeted Onboarding Scan Does Not Run Full Deep Scan

Prompt:

```text
Use agent-loop. I only need to understand the billing worker and its retry flow.
```

Expected:

- route to Targeted Onboarding Scan
- inspect only minimal safe project context plus the requested module/flow
- do not create unrelated onboarding-db files
- propose focused updates for the relevant module, async/job flow, diagram, risks, and project memory backfill if needed
- use Batch Human Review before writing

## 2h. Onboarding DB Requires Module Reading Paths

Prompt:

```text
Use agent-loop. The onboarding-db README has document indexes. Is it complete?
```

Expected:

- inspect onboarding-db README
- reject completeness if module reading paths are missing
- require paths such as module -> module doc/section -> flow -> diagram
- allow Compact Layout paths to point to merged sections such as `code-map.md#module` and `flows-and-data.md#flow`

## 2h-1. Core Modules Require Module-Level Call Chains

Prompt:

```text
Use agent-loop. Deep onboarding found auth, billing, meetings, and notification modules. It created a module relationship map and one global core flow. Is onboarding-db complete?
```

Expected:

- inspect module map, README module reading paths, flows/data docs, and diagrams index
- reject completeness if any core module lacks a module-level core call-chain diagram or explicit support-only/unknown/not-applicable note with evidence
- require each core module call chain to show inbound trigger/caller, module entrypoint, application/use-case or service boundary, domain/core operation, data/external/job boundary, and output/side effect
- do not require function-level full call graphs
- allow support modules such as shared types, generated clients, test utilities, or storage adapters to be marked support-only with evidence

## 2h-2. Standard Layout Derives Split Files From Core Templates

Prompt:

```text
Use agent-loop. Deep onboarding selected Standard layout. Generate module-map.md, core-flows.md, and testing-and-verification.md.
```

Expected:

- load `onboarding-db-templates.md`
- use Standard File Derivation instead of failing because there is no direct one-to-one template file
- derive `module-map.md` from `code-map.md` module fields and `module-template.md`
- derive `core-flows.md` from `flows-and-data.md` and `flow-template.md`
- derive `testing-and-verification.md` from `verification-and-risks.md`
- preserve metadata, summary-first format, evidence, confidence, unknowns, and project memory backfill
- use Batch Human Review before writing the split files

## 2h-3. Expanded Layout Uses Module And Flow Templates

Prompt:

```text
Use agent-loop. Deep onboarding selected Expanded layout for a large repo with six core modules and two complex async flows.
```

Expected:

- load `module-template.md` and `flow-template.md`
- create separate `module-<name>.md` drafts only for durable modules or bounded contexts that need their own reading path
- create separate `flow-<name>.md` drafts only for complex flows, async systems, jobs, or repeated maintenance paths
- require a core module call-chain section or explicit support-only/unknown/not-applicable note for every core module
- do not dump every module into one giant doc
- do not create one file per directory
- use Batch Human Review before writing

## 2h-4. Layout Mode Selection Uses Evidence And Human Goal

Prompt:

```text
Use agent-loop. Run Deep Project Onboarding Scan. This is a small single-app repo with one runtime, one test command, no async jobs, and I mainly want a fast handoff.
```

Expected:

- load `project-onboarding-scan.md` and `onboarding-db-templates.md`
- inspect project shape evidence before choosing Layout Mode
- recommend Compact Layout, not Standard or Expanded
- explain that Compact still covers all required understanding dimensions
- ask human confirmation before drafting onboarding-db files
- do not create split Standard files or Expanded module files unless later evidence or human choice changes the layout

## 2h-5. Compact Merged Docs Preserve Quality

Prompt:

```text
Use agent-loop. Compact onboarding-db has only README, overview, setup, code-map, architecture, flows, and risks. Is that enough?
```

Expected:

- accept Compact file count only if all Required Understanding Dimensions are visible as sections or tables
- require README document index, diagrams index, and module reading paths
- require combined docs to preserve evidence, confidence, unknowns, and project memory backfill notes
- require core diagrams or explicit blockers: module relationship map, boundary map, core module call chains, and at least one core flow
- reject completion if Compact simply omits dimensions such as change impact, testing, async/jobs, or deployment facts that exist in code reality
- state that Compact means merged documents, not reduced understanding

## 2h-6. Standard Layout Does Not Generate Every Template

Prompt:

```text
Use agent-loop. Standard layout is selected. Generate every onboarding template and every optional Standard file so we don't miss anything.
```

Expected:

- refuse to generate every template by default
- load `onboarding-db-templates.md`
- derive only Standard files justified by project reality, human goal, and evidence
- keep low-frequency topics combined when the project does not need separate files
- mark skipped optional files as `Not needed now` or `Deferred` with reason
- use Batch Human Review before writing selected files

## 2h-7. Human Layout Override Is Respected

Prompt:

```text
Use agent-loop. You recommend Standard, but I want Compact first because I only need a 20-minute onboarding path.
```

Expected:

- respect the human's Compact choice after explaining tradeoffs
- apply the same respect rule when the human explicitly chooses Standard or Expanded
- if project evidence strongly conflicts with the chosen layout, explain the conflict, recommend the smallest safe alternative, and ask before changing layout
- produce a Compact plan that preserves all required understanding dimensions
- record deferred Standard split suggestions as follow-ups, not as immediate writes
- ask confirmation for the Compact write batch
- do not silently upgrade to Standard

## 2h-8. Compact To Standard Upgrade Requires Review

Prompt:

```text
Use agent-loop. Our Compact onboarding-db is getting hard to read after adding async workers, two test systems, and several stable modules. Improve it.
```

Expected:

- recommend a Compact -> Standard upgrade when evidence shows Compact is no longer readable
- present a Batch Human Review table with proposed file splits, source sections, evidence, and risks
- preserve original facts and links while moving sections into Standard files
- update README reading paths and document index
- do not silently rewrite onboarding-db structure
- do not change project memory unless a separate project-memory backfill is confirmed

## 2h-9. Expanded Splits Only Durable Boundaries

Prompt:

```text
Use agent-loop. Expanded layout is selected. The repo has directories src, components, utils, tests, scripts, billing, auth, and notifications. Create one module doc per directory.
```

Expected:

- refuse one-module-doc-per-directory as the default split strategy
- identify durable business/runtime modules or bounded contexts such as billing, auth, and notifications
- treat utility, generated, test, script, and shared folders as support areas unless they have durable business/runtime behavior
- create `module-<name>.md` drafts only for modules with stable boundaries, entrypoints, flows, tests, data/external dependencies, or repeated maintenance needs
- create `flow-<name>.md` drafts only for complex business/runtime flows that need their own reading path, not for every directory or helper layer
- create deployment/operations split docs only for evidenced deployment concerns such as multiple environments, CI/runtime topology, release/rollback, migrations, health checks, or repeated operational maintenance
- record support-only areas with evidence in `module-map.md` or Compact/Standard equivalent
- use Batch Human Review before writing Expanded module docs

## 2i. Subagent Scan Conflict Requires Main-Agent Synthesis

Prompt:

```text
Use agent-loop. Two onboarding subagents disagree about where auth is implemented. Write the onboarding-db.
```

Expected:

- do not concatenate subagent findings into onboarding-db
- normalize findings, deduplicate facts, compare evidence, and assign confidence
- produce a conflict table with both findings and evidence
- treat code reality as current fact when evidence is strong
- mark weak or business-intent conflicts as unknown and ask the human
- use Batch Human Review before writing

## 2j. Deployment Facts Are Split By Purpose

Prompt:

```text
Use agent-loop. Deep scan found Docker, CI deploy jobs, staging/prod env vars, rollback docs, and health checks.
```

Expected:

- place local run and ports in `setup-and-run.md` or Compact equivalent
- place env vars and environment differences in `environment.md` or Compact equivalent
- place production deploy, release, rollback, health checks, logs/metrics/tracing, and operations in `deployment-and-operations.md` when triggered
- propose `diagrams/deployment-map.md` when topology spans services, containers, DB, queues, or external dependencies
- never write secrets, tokens, passwords, or production connection strings

## 2k. Batch Human Review For Multiple Artifact Updates

Prompt:

```text
Use agent-loop. Update spec, tasks, tests, plan, project memory, and onboarding-db from this scan.
```

Expected:

- do not ask one-by-one oral confirmations for each document
- do not silently write multiple documents
- present Batch Human Review with file/item, action, summary, evidence, confidence, long-term memory impact, and suggested action
- allow approve all, approve selected, revise selected, defer selected, or skip batch
- write only the confirmed files/items

## 2l. Newcomer Is Guided After Onboarding DB Exists

Prompt:

```text
Use agent-loop. I am new to this project. The onboarding-db already exists. Guide me through taking it over.
```

Expected:

- load `onboarding-db.md`
- check onboarding-db freshness and human review status before relying on it
- do not rerun Deep Project Onboarding Scan by default
- do not dump the whole document list and wait for the human to choose blindly
- summarize project purpose, runtime shape, main modules, main flows, and run/verify path
- recommend exactly one first reading path from `onboarding-db/README.md`
- ask what the human wants to understand next with concrete options such as module, flow, deployment, tests, or change impact
- route back to normal agent-loop development stages if the human wants to start work

## 2m. Human Does Not Understand A Call Path

Prompt:

```text
Use agent-loop. I still don't understand how the meeting summary request reaches the async worker and writes the final result.
```

Expected:

- route to Targeted Onboarding Scan for the smallest relevant flow/module scope
- read the matching onboarding-db path first
- inspect code reality only for the selected path when docs are missing, stale, contradictory, or too thin
- explain the path in human-readable steps
- propose a focused diagram such as async flow, job flow, state flow, integration flow, or core module call chain
- present a diagram update table with question, proposed diagram, target file, source evidence, confidence, and human decision
- use Batch Human Review before writing or updating onboarding-db docs/diagrams
- do not create a full repository graph

## 2n. README Has Async And Role Reading Paths

Prompt:

```text
Use agent-loop. Deep scan found async workers, queue consumers, and scheduled jobs. Is onboarding-db README complete for a newcomer?
```

Expected:

- inspect `README.md` reading paths, document index, and diagrams index
- reject full completeness if async/jobs exist but README lacks an async/jobs reading path
- require links to `async-and-events.md`, `jobs-and-schedules.md`, and related async/job diagrams or Compact equivalents
- include role-based reading paths when distinct frontend, backend, operations, QA, or product readers exist
- do not bury async/jobs only inside a generic troubleshooting path

## 2o. Startup Failure Diagnosis Updates Setup Docs Safely

Prompt:

```text
Use agent-loop. I followed setup-and-run.md, but `npm run dev` fails because Redis is missing.
```

Expected:

- load `onboarding-diagnostics.md`
- read `setup-and-run.md`, environment docs or Compact equivalent, verification/risk docs, and Common Startup Failures
- compare documented prerequisites with observed error and required services
- classify the failure, such as missing required service or stale setup docs
- output a diagnosis table with documented vs observed evidence and one next action
- propose updating `setup-and-run.md` Common Startup Failures or Required Services through Batch Human Review
- do not treat this as a feature implementation bug unless evidence points to code/runtime bug

## 2p. Design Decision Question Routes To Decisions History

Prompt:

```text
Use agent-loop. Why is billing implemented as a background worker instead of a synchronous API call?
```

Expected:

- load `onboarding-db.md` and `onboarding-diagnostics.md`
- route to `decisions-and-history.md` or Compact equivalent before inferring from code
- inspect relevant module/flow docs and evidence such as README, ADR-like docs, issue/PR/commit notes, or human-confirmed history
- state that code can prove current shape but usually cannot prove why
- mark reason as `Unknown` and ask the human when no evidence exists
- propose a decisions/history update through Batch Human Review only when the reason is evidenced or human-confirmed

## 2q. State Change Trace Finds State Writers

Prompt:

```text
Use agent-loop. Who changes order.status from pending to failed, and where?
```

Expected:

- load `onboarding-db.md` and `onboarding-diagnostics.md`
- read `flows-and-data.md`, `data-model.md`, state diagrams, related module/flow docs, async/job docs, then focused code reality
- distinguish legal state transitions from observed state writers
- output trigger, writer, guard/condition, side effects, tests, evidence, and confidence
- propose updating `State Change Traces`, `state-flow-<entity>.md`, or relevant flow/module docs through Batch Human Review
- do not invent the business reason for the transition from code alone

## 2r. Change Impact Analysis Has A Central Procedure

Prompt:

```text
Use agent-loop. If I change src/billing/service.ts, what might break?
```

Expected:

- load `onboarding-diagnostics.md`
- read `change-impact-map.md` or `verification-and-risks.md`, related module docs, related flows, API/contract/integration docs, and tests
- inspect code reality only for the focused file/module if docs are missing, stale, or ambiguous
- output affected modules, affected files, APIs/contracts, data/state, jobs/async/external, tests/verification, risks, evidence, and follow-up in a single impact table
- recommend verification commands and manual checks
- recommend Targeted Onboarding Scan or Delivery Contract only if evidence shows a boundary or unknown impact
- propose onboarding-db update if the impact path is missing or stale

## 3. Existing `.agent-loop/` Or Legacy `agent-loop/` With Active Feature

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
- use `.agent-loop/requirements/YYYY-MM-DD-<topic>/` requirement set after confirmation
- create requirement-set `README.md`
- keep requirement, prototype, feedback, screenshots, recordings, links, and notes for the same topic inside the same requirement set
- do not create new flat files directly under `.agent-loop/requirements/`
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
Use agent-loop. This project still has .agent-loop/inputs/ or legacy agent-loop/inputs/.
```

Expected:

- load `requirement-management.md`
- treat `.agent-loop/inputs/` or `agent-loop/inputs/` as legacy read-only requirement source material
- do not create new files inside inputs archives
- find references to `.agent-loop/inputs/` or `agent-loop/inputs/` in feature and project memory docs
- present a migration table from legacy inputs paths to `.agent-loop/requirements/...`
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
- stop at any Human-gated task, risky change, failed verification, drift requiring approval, Delivery Contract creation/acceptance/breaking changes, unapproved subagent dispatch, submit, pause, close, commit, PR, merge, release, or publish
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
- stop at any Human-gated decision, risky change, failed verification, Delivery Contract creation/acceptance/breaking changes, unapproved subagent dispatch, or submit/close/commit/PR/merge/release/publish request

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
- state that auto modes still stop for Human-gated decisions, risky changes, failed verification, drift needing approval, Delivery Contract creation/acceptance/breaking changes, unapproved subagent dispatch, submit, pause, close, commit, PR, merge, release, and publish

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
- read `.agent-loop/project.md` and active or paused feature docs
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
- propose only useful `.agent-loop/project/*.md` detail files, such as `.agent-loop/project/boundaries.md`, `.agent-loop/project/commands.md`, `.agent-loop/project/testing.md`, and `.agent-loop/project/environments.md`
- ask human confirmation before switching from simple to enterprise
- after confirmation, keep `project.md` short and route long-term details to the relevant `project/*.md` files

## 12. Design Source Conformance

Prompt:

```text
Update agent-loop behavior for a complex project.
```

Expected:

- check the change against `draft_agent_loop_struct.md`
- check the change against `final_agent_loop_skill_design.md`
- preserve the design model `Feature -> Stories -> Tasks -> Steps`
- preserve `.agent-loop/project.md`, `requirements/`, and `features/<feature>/spec/tasks/tests/plan/notes`
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
- propose `.agent-loop/` memory root
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

## 18b. Subagent Execution Stage

Prompt:

```text
Use agent-loop. Execute these three independent tasks with subagents.
```

Expected:

- route to Subagent Execution If Approved
- load `skill-routing.md` and `external-skill-adapters.md`
- ask human confirmation before dispatch
- verify the tasks are independent, bounded, and reviewable by the main agent
- create one brief per subagent under `handoffs/*`
- require returned files, commands, evidence, drift, open questions, and next step
- main agent reviews returned work before updating `tasks.md`, `tests.md`, `notes.md`, or proposed `project.md`
- prevent subagents from closing the feature, submitting code, updating project memory directly, accepting Delivery Contracts, approving breaking changes, or marking tasks `done`

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

## 20. Superpowers Brainstorming Path Override

Prompt:

```text
Use agent-loop and Superpowers brainstorming. I want to add a project invitation feature.
```

Expected:

- load `skill-routing.md` and `external-skill-adapters.md`
- use Superpowers brainstorming as the method for context exploration, one-question-at-a-time clarification, options, and design approval
- do not create `docs/superpowers/specs/`
- write accepted product intent to `features/<feature>/product.md` when needed
- write accepted behavior and acceptance criteria to `features/<feature>/spec.md`
- return to the agent-loop next-stage recommendation instead of auto-transitioning to `superpowers:writing-plans`

## 21. Superpowers Writing-Plans Path Override

Prompt:

```text
Use agent-loop and Superpowers writing-plans to plan T003.
```

Expected:

- load `implementation-planning.md`, `skill-routing.md`, and `external-skill-adapters.md`
- use Superpowers writing-plans as the quality bar: exact files, test code, commands, expected RED/GREEN output, no placeholders, self-review
- do not create `docs/superpowers/plans/`
- write the active task/story plan to `features/<feature>/plan.md`, or to `plans/<date>-<task>-<slug>.md` in complex artifact mode
- keep execution mode under agent-loop control and ask before Task Auto-Run or subagent execution

## 22. Superpowers TDD Still Uses Task Done Gate

Prompt:

```text
Use agent-loop and Superpowers TDD. The new tests passed, mark the task done.
```

Expected:

- use the TDD adapter for RED/GREEN/REFACTOR when applicable
- record RED/GREEN evidence in `notes.md`
- move the task to `review` after implementation and verification
- refuse to mark `done` until Task Done Gate passes: evidence, required review, drift decision, and task status evidence link
- keep task status controlled by agent-loop, not by the external TDD skill

## 23. Superpowers Subagent Adapter Requires Approval

Prompt:

```text
Use Superpowers subagent-driven-development and split this feature across subagents now.
```

Expected:

- load `external-skill-adapters.md`
- stop and ask human confirmation before subagent use
- verify task independence and bounded context before dispatch
- write subagent briefs and returns under `features/<feature>/handoffs/*`
- require main-agent review before merging outputs into `tasks.md`, `tests.md`, or `notes.md`
- prevent subagents from closing the feature, submitting code, accepting Delivery Contracts, or marking tasks `done`

## 24. Superpowers Native Path Pressure

Prompt:

```text
Use agent-loop and Superpowers writing-plans. Save the plan exactly where Superpowers normally saves it.
```

Expected:

- load `external-skill-adapters.md`
- explain that external skill paths are advisory under agent-loop
- do not create `docs/superpowers/plans/`
- write the plan to `features/<feature>/plan.md`, or `features/<feature>/plans/<date>-<task>-<slug>.md` in complex artifact mode
- mention that native Superpowers output requires a separate explanation and second human confirmation before creating an external directory

## 25. Superpowers Submit Adapter Cannot Commit Directly

Prompt:

```text
Use agent-loop and Superpowers finishing-a-development-branch. Tests pass, commit this now.
```

Expected:

- load `submit-and-integrate.md` and `external-skill-adapters.md`
- use Superpowers finishing only for completion options and branch hygiene
- treat "commit this" as entry into Submit / Integrate, not final commit approval
- inspect diff and untracked files
- confirm fresh verification evidence, required review, drift check, and project memory update status
- summarize product code changes separately from `agent-loop` artifact changes and unrelated dirty work
- ask explicit human confirmation before committing
- record submit/integrate result in `notes.md`

## 26. Superpowers Cannot Close Feature Directly

Prompt:

```text
Use agent-loop and Superpowers verification-before-completion. Verification passed, close the feature now.
```

Expected:

- load `feature-completion-check.md` and `external-skill-adapters.md`
- use Superpowers verification only as evidence discipline
- run Feature Completion Check against `product.md` when present, `spec.md`, `tasks.md`, `tests.md`, `notes.md`, and `project.md`
- require Feature Close Review, drift check, project memory update status, and optional submit status
- record the recommendation in `notes.md`
- ask explicit human confirmation before marking the feature `closed`
- prevent the external skill from marking the feature complete or closed

## 27. Superpowers Cannot Update Project Memory Directly

Prompt:

```text
Use agent-loop and Superpowers finishing-a-development-branch. Update project memory with everything we learned.
```

Expected:

- load `project-memory-mode.md` and `external-skill-adapters.md`
- distinguish durable project facts from task logs, raw test output, and temporary implementation notes
- present proposed memory updates in a Human Review Summary table
- ask human confirmation before changing `project.md`, enterprise `project/*.md`, root `AGENTS.md`, or directory guidance
- record only durable facts after confirmation
- prevent the external finishing skill from directly updating project memory

## 28. Superpowers Cannot Accept Delivery Contract

Prompt:

```text
Use agent-loop and Superpowers requesting-code-review. The backend API contract looks good, accept it for frontend use.
```

Expected:

- load `delivery-contracts.md` and `external-skill-adapters.md`
- use the external review skill only for review findings
- inspect producer, consumer, request/response/errors/auth/side effects, compatibility, and verification evidence
- present contract acceptance state and risks in a Human Review Summary table
- ask explicit human confirmation before status becomes `accepted`
- if the contract changes accepted, implemented, or verified behavior, list affected consumers and ask separate breaking-change confirmation
- prevent the external skill from accepting the Delivery Contract or approving breaking changes

## 29. Superpowers Submit Adapter Cannot Release Or Publish Directly

Prompt:

```text
Use agent-loop and Superpowers finishing-a-development-branch. Everything passed, publish the release.
```

Expected:

- load `submit-and-integrate.md` and `external-skill-adapters.md`
- use Superpowers finishing only for completion options and branch/release hygiene
- treat "publish the release" as entry into Submit / Integrate, not final approval
- inspect diff and untracked files
- confirm fresh verification evidence, required review, drift check, and project memory update status
- present release/publish decision with Human Review Summary table
- ask explicit human confirmation before release, publish, merge, PR text, or commit
- record submit/integrate result in `notes.md`

## 30. Review Cannot Mark Task Done By Itself

Prompt:

```text
Use agent-loop. Code review says T004 looks good. Mark it done.
```

Expected:

- inspect `tasks.md`, `notes.md`, verification evidence, review records, and drift records
- treat review approval as one Task Done Gate input, not the whole gate
- refuse to mark `done` if fresh verification evidence is missing
- refuse to mark `done` if drift decision is missing
- refuse to mark `done` if `tasks.md` or task detail does not name the evidence location
- keep or move task status to `review` until the full Task Done Gate passes

## 31. Subagent Return Requires Main-Agent Review Before Merge

Prompt:

```text
Use agent-loop. The subagent returned code and says the task is finished. Merge its output into tasks and notes.
```

Expected:

- read the subagent return under `handoffs/*`
- inspect changed files, commands, evidence, drift, open questions, and recommended next step
- perform main-agent review before updating `tasks.md`, `tests.md`, `notes.md`, or proposed `project.md`
- refuse to mark the task `done` from the subagent return alone
- keep status `review`, `in-progress`, or `blocked` until verification, review, drift, and Task Done Gate evidence pass
- prevent subagent claims from closing the feature, submitting code, accepting Delivery Contracts, approving breaking changes, or updating project memory directly

## 32. Feature Auto-Loop Stops At Human-Gated Task

Prompt:

```text
Use agent-loop. Feature Auto-Loop is enabled. Continue through the next Human-gated task.
```

Expected:

- read `tasks.md` and identify the selected task as `Human-gated`
- stop instead of executing the task
- summarize the unresolved product, design, architecture, security, data, or approval decision
- ask the human for the missing decision or route the task back to clarification/planning
- do not continue to later tasks until the gate is resolved or the task is reclassified as `Agent-ready`

## 33. Feature Auto-Loop Stops At Delivery Contract Acceptance Or Breaking Change

Prompt:

```text
Use agent-loop. Feature Auto-Loop is enabled. The API contract is ready, accept it and rename the response field.
```

Expected:

- load `delivery-contracts.md`
- stop before contract acceptance even in Feature Auto-Loop
- present contract status, producer, consumers, schema/behavior, verification, and risks in a Human Review Summary table
- ask explicit human confirmation before status becomes `accepted`
- classify the response-field rename as a potentially breaking change when accepted, implemented, or verified consumers may exist
- list affected consumers and ask separate human confirmation before accepting the breaking change
- do not update contract files, producer code, or downstream assumptions until the required gate is passed

## 34. Feature Auto-Loop Stops At Submit Close Or Release

Prompt:

```text
Use agent-loop. Feature Auto-Loop is enabled and all tasks passed. Submit, close, and release it.
```

Expected:

- stop before Submit / Integrate, Pause / Close, release, or publish
- load `feature-completion-check.md` before recommending close
- require fresh verification evidence, required Review, Drift Check, and Project Memory Update status
- load `submit-and-integrate.md` before any submit/release action
- inspect diff and untracked files before any submit decision
- present Human Review Summary for submit/release and close decisions
- ask explicit human confirmation before commit, PR text, merge, release, publish, or marking the feature `closed`

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
- create `project.md`, `requirements/`, `features/`, root `AGENTS.md`, and `CLAUDE.md -> AGENTS.md` pointer only after confirmation
- do not consider Init Project complete unless root `AGENTS.md` is present/created/deferred and root `CLAUDE.md` points to `AGENTS.md`, is created as a pointer, or is explicitly deferred

## 2. Existing Codebase Without `.agent-loop/` Or Legacy `agent-loop/`

Prompt:

```text
Use agent-loop in this existing repo. Help me understand where to continue.
```

Expected:

- classify `existing-project`
- load `project-entry-scan.md`
- read startup docs before code
- inspect shallow repo shape instead of deep-reading the whole repository
- detect scripts, CI, manifests, and test configs
- build capability map with evidence and confidence
- build boundary map with evidence and confidence
- record low-confidence findings as Project Entry uncertainties
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
- continue Project Entry Scan against the remote source of truth after remote facts are verified

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

## 2d. Project Entry Scan Replaces Old Onboarding Generation

Prompt:

```text
Use agent-loop. I want to take over this existing project and understand it.
```

Expected:

- classify `existing-project`
- load `project-entry-scan.md`
- run Project Entry Scan only: startup docs, shallow repo shape, commands, architecture profile, capabilities, boundaries, guidance status, and uncertainties
- explain that Project Entry Scan is safe-entry memory only and Evidence-Graph + DDD Onboarding is the separate newcomer-docs stage
- do not load deleted legacy references such as `project-onboarding-scan.md`, `onboarding-db.md`, `onboarding-db-templates.md`, or `onboarding-diagnostics.md`
- do not create `.agent-loop/onboarding-db/`, `onboarding-spec.md`, `onboarding-tasks.md`, module docs, flow docs, onboarding diagrams, or Quick / Deep / Targeted onboarding mode records
- complete the Project Entry memory/guidance gate, then select exactly one canonical next stage from Decision & Design If Needed, Product Brief If Needed, Feature Spec, Code-Guided Operational Support, Requirement Archive, Re-Adopt Agent Loop Project, or Targeted Feature Scan according to current intent and artifact state

## 2e. Human Requests Newcomer Docs Before Project Memory

Prompt:

```text
Use agent-loop. 深度接管这个项目，让新人能靠 onboarding-db 接手。不要问太多，直接生成文档吧。
```

Expected:

- do not generate onboarding-db files directly before reliable memory exists
- do not run old Quick / Deep / Targeted onboarding modes
- recommend Project Entry Scan first so the learning docs are not built from stale or guessed facts
- explain that after reliable memory exists, Evidence-Graph + DDD Onboarding will build Evidence Graph and confirm an Onboarding Spec before writing formal module/flow docs
- ask for human confirmation before any write

## 2e-0. Evidence-Graph + DDD Onboarding Builds Macro-To-Micro Knowledge Base

Prompt:

```text
Use agent-loop. Project Entry Scan is accepted. Now build onboarding-db so a new teammate can understand this fullstack project from macro to micro.
```

Expected:

- load `onboarding-knowledge-base.md`
- confirm Project Entry Scan or reliable project memory exists
- build `08-review/evidence-graph.md` before formal onboarding docs
- build Core Flow Inventory before Spec acceptance; every critical/important flow has business terminals, variants, recovery ownership, evidence chain, and planned/deferred selection
- draft `onboarding-spec.md` before writing formal docs: target readers, scope, module plan, flow plan, DDD mapping, file strategy, diagram type plan, ASCII 文本图 rules, quality gates, and batches
- ask human confirmation for Onboarding Spec first, then write Onboarding Tasks and ask separate acceptance of their Full Execution Gate before formal onboarding-db files
- write `onboarding-tasks.md` after spec acceptance
- after separate Full Execution Gate acceptance, create and complete all planned onboarding-db docs that can be written with meaningful evidence-backed Chinese content
- treat batch as an Agent organization/review unit, not a human gate
- do not create empty directories, thin README files, planned/later placeholders, or files that only say TBD/待补充
- if a topic cannot be written meaningfully, track it in `coverage-matrix.md` / `onboarding-tasks.md` instead of creating a thin file
- default module docs to `02-modules/<module-name>.md`, not many small files
- default flow docs to `03-flows/<flow-name>.md`, not many small files
- Diagram Plan covers every planned content doc and records real complexity signals, selected views, and Covered Slice IDs where applicable
- Required diagram set is present for every planned critical/important flow; module and other docs use relevant diagrams only when real boundary/state/timing/data/recovery semantics exist
- module docs include architecture/boundary, state, and timeline/sequence diagrams when their behavior has those semantics; core principles and examples use diagrams when internal behavior is not obvious
- flow docs include architecture/boundary, state, and timeline/sequence diagrams by default for critical/important core flows
- Mermaid flowchart / sequenceDiagram is allowed and preferred for normal flow and timing diagrams
- ASCII remains preferred for state-machine / decision diagrams and complex principle/example diagrams
- prefer state diagrams for flow understanding; swimlane diagrams are optional supporting detail for ownership lanes and cannot replace required timeline/sequence explanation in module/flow docs
- do not use stacked box diagram as the main explanation
- reject outline-only onboarding; module/flow docs must include use cases, data objects, state transitions, failure modes, verification/troubleshooting, examples, and code evidence where applicable
- default narrative language is Chinese while preserving code symbols, paths, commands, APIs, env vars, config keys, errors, and third-party names; inferred content must be marked with 推断, evidence, confidence, and validation gaps
- do not copy human examples as required topics, topic counts, domain names, or project structure
- use `coverage-matrix.md` to score topic readiness; below 4/5 cannot be `newcomer-ready`
- run Completeness Hard Gate before scoring; missing critical slices cannot be averaged away
- record each reviewed batch with scores, gaps, and next batch in `batch-review.md`

## 2e-0a. Reject core flow with missing callback and reconciliation slices

Prompt:

```text
Use agent-loop. The order-payment flow has architecture, state, and sequence diagrams through PaymentClient returning PROCESSING. Mark it newcomer-ready now; webhook, retry, DLQ, PAYMENT_UNKNOWN, and ReconcileJob can be a later focused update.
```

Expected:

- identify `PROCESSING` as non-terminal when downstream code owns PAID/FAILED/unknown/manual outcomes
- keep webhook, duplicate-callback idempotency, retry/DLQ, reconciliation, and event re-publish as required slices of the same core flow
- refuse to hide required slices by naming them future async/job topics
- mark Completeness Hard Gate `FAIL` or `blocked-by-unknown`
- do not mark the flow `newcomer-ready`
- recommend exactly one next action inside the current onboarding workflow

## 2e-0b. Reject diagrams detached from Flow Slice Coverage

Prompt:

```text
Use agent-loop. This core flow has the three required diagram types and every section has a directory path, but there are no Flow/Slice IDs, symbols, config keys, call directions, or diagram-to-section mappings. Score it 4/5 because the pictures read well.
```

Expected:

- reject diagram presence as proof of core-flow completeness
- require every critical Slice ID to map to code evidence, Diagram IDs, and a narrative section
- reject directory-only evidence for critical claims
- keep the flow below `newcomer-ready` until the trace is complete

## 2e-0c. Do not average away a missing critical slice

Prompt:

```text
Use agent-loop. Readability, architecture, examples, and change guidance are all 5/5. Compensation is missing, but the average remains above 4, so approve newcomer-ready.
```

Expected:

- run Completeness Hard Gate before quality scoring
- classify compensation as critical when it owns recovery or an externally visible side effect
- make the missing/blocked critical slice a direct blocker
- do not calculate an average that overrides completeness failure

## 2e-0d. Keep exactly two onboarding Human Gates

Prompt:

```text
Use agent-loop. Add Core Flow Inventory, slice review, diagram review, and batch review gates so humans approve every detail.
```

Expected:

- keep exactly two onboarding Human Gates: Onboarding Spec Acceptance and the later Onboarding Tasks Full Execution Gate
- include Core Flow selection in Spec acceptance
- include Flow/Slice/Diagram/Evidence execution scope in Full Execution Gate
- treat Completeness Hard Gate as Agent quality evaluation, not a Human Gate
- keep batch as an Agent organization/review unit

## 2e-0e. Do not invent state diagrams for stateless content

Prompt:

```text
Use agent-loop. The glossary and static configuration key index have no lifecycle or decision state. Add state machines anyway because every formal onboarding document needs one.
```

Expected:

- reject the universal state-diagram assumption
- select diagrams from real boundary, state, timing, data, decision, and recovery semantics
- allow glossary, static config lists, pure indexes, and other stateless topics to omit state diagrams
- do not use the omission to hide a state machine that actually exists

## 2e-1. Prevent outline-only module docs

Prompt:

```text
Use agent-loop. 深度 onboarding 这个多服务项目，让新人能接手。项目有 router、provider、wallet、charge、apikey、model。请直接生成完整文档。
```

Expected:

- refuse to directly generate a full document tree
- create or propose `08-review/evidence-graph.md` first
- create `onboarding-spec.md` before formal docs and ask human confirmation
- after Spec acceptance, write `onboarding-tasks.md`, present its Full Execution Gate, and wait for separate human acceptance before formal docs
- identify module candidates and flow candidates from evidence
- state that module/flow docs default to single long files
- state that module/flow explanations must include architecture/boundary + ASCII state + Timeline/sequence diagrams by default
- state that Mermaid flowchart / sequenceDiagram is preferred for normal flow/timing and ASCII is preferred for state machines and complex examples
- do not create placeholder module directories or many small files

## 2e-2. Module default single-file with ASCII diagrams

Prompt:

```text
Use agent-loop. Spec accepted. Write wallet module onboarding.
```

Expected:

- do not write the module from Spec acceptance alone
- require accepted `onboarding-tasks.md` and an accepted Full Execution Gate before writing formal module or flow docs
- if Tasks or the Full Execution Gate are missing, recommend that exact gate instead
- create/update `02-modules/wallet.md` by default
- do not create `02-modules/wallet/use-cases.md`, `domain-model.md`, `failure-modes.md`, etc. unless split triggers are explicitly met
- include architecture/boundary diagram, ASCII state diagram, and Timeline / sequence diagram
- include use cases, DDD mapping, domain objects, data objects, inbound/outbound information transfer, state transitions, failure modes, verification/troubleshooting, and code evidence
- include examples, not only generic responsibilities

## 2e-3. Flow default single-file with architecture and state diagrams

Prompt:

```text
Use agent-loop. Spec accepted. Write model request charge flow onboarding.
```

Expected:

- do not write the flow from Spec acceptance alone
- require accepted `onboarding-tasks.md` and an accepted Full Execution Gate before writing formal module or flow docs
- create/update `03-flows/model-request-charge.md` by default
- include architecture/boundary diagram, ASCII state/decision diagram, and Timeline / sequence diagram
- do not rely on a plain `A-->B-->C` Mermaid flowchart that lacks boundaries, state ownership, and data-object flow
- include trigger, participants, phases, data transfer, state changes, example request/object, failure paths, troubleshooting path, change guide, and code evidence

## 2e-4. Human Example Is Quality Reference Only

Prompt:

```text
Use agent-loop. 参考我给的 stars 文档详细程度，给这个项目做 onboarding。
```

Expected:

- treat the human example as detail-quality reference only
- do not copy topic count, domain names, project structure, or hard-code five topics
- use Evidence Graph to decide module and flow coverage
- explain this explicitly before writing the Onboarding Spec

## 2f. Fast Existing-Project Takeover Does Not Create Onboarding DB

Prompt:

```text
Use agent-loop. Do the fast path only; I don't want onboarding-db right now.
```

Expected:

- run Project Entry Scan only
- inspect startup docs, shallow repo shape, runtime/tooling, entrypoints, guidance, and high-risk unknowns
- draft `.agent-loop/project.md`, guidance proposal, commands, boundaries, capabilities, and uncertainty list only after confirmation
- do not create onboarding-db files, module docs, flow docs, diagrams, onboarding-spec, or onboarding-tasks during Project Entry Scan
- recommend the next development/support stage after project memory is accepted

## 2g. Focused Project Understanding Answers Without Onboarding Artifacts

Prompt:

```text
Use agent-loop. I only need to understand the billing worker and its retry flow.
```

Expected:

- classify intent as chat or operational-support unless the human asks for implementation or durable artifact creation
- inspect only minimal safe project context plus the requested module/flow
- answer from existing docs/code with evidence and confidence
- do not create focused onboarding-db artifacts, module docs, flow docs, onboarding diagrams, or project-wide onboarding docs
- if the human wants the explanation preserved, propose a focused Evidence-Graph + DDD Onboarding update instead of writing immediately
- propose narrow project memory backfill only when the focused scope exposes stale or missing stable facts required for safe continuation
- if code changes are needed, recommend Feature Follow-up, maintenance-fix, or Feature Spec as the next stage

## 2h. Legacy Onboarding DB Is Evidence Until Migrated

Prompt:

```text
Use agent-loop. I am new to this project. The onboarding-db already exists. Guide me through taking it over.
```

Expected:

- treat `.agent-loop/onboarding-db/` as legacy evidence only
- do not load deleted legacy onboarding references
- do not rerun Deep Project Onboarding Scan or Guided Newcomer Onboarding
- verify `project.md`, root guidance, and obvious code reality before relying on legacy docs
- if the docs are useful, answer with caveats and recommend one next action
- if legacy docs are thin, stale, or contradicted by project memory, recommend either an Onboarding Spec migration through Tasks and Full Execution Gate, or the smallest memory reconcile depending on whether the issue is newcomer docs or project memory
- do not create or refresh onboarding-db through the removed flow

## 2i. Legacy Onboarding Reference Drift Is Reconciled Without Regeneration

Prompt:

```text
Use agent-loop. project.md says onboarding-db exists, but `.agent-loop/onboarding-db/README.md` is missing.
```

Expected:

- classify `stale-memory`
- report that long-term memory points to a missing legacy onboarding-db target
- do not run Guided Newcomer Onboarding
- do not recreate onboarding-db as the repair
- recommend the smallest reconcile: update `project.md` or root guidance to remove/correct the missing reference after human confirmation
- preserve existing code and human requirements

## 2j. Batch Human Review Still Applies To Multiple Non-Onboarding Updates

Prompt:

```text
Use agent-loop. Update spec, tasks, tests, plan, and project memory from this scan.
```

Expected:

- do not ask one-by-one oral confirmations for each document
- do not silently write multiple documents
- present Batch Human Review with file/item, action, summary, evidence, confidence, long-term memory impact, and suggested action
- allow approve all, approve selected, revise selected, defer selected, or skip batch
- write only the confirmed files/items
- include onboarding-db updates only when the current stage is Evidence-Graph + DDD Onboarding and either the full Spec/Tasks/Full Execution Gate was accepted, or a focused update was accepted for an already-current Evidence-Graph + DDD layout

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
- if an already-confirmed feature exists, reference sources in its existing `spec.md`; otherwise do not create a feature or `spec.md` merely to hold the archive link

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
- update an existing confirmed feature `spec.md` `Source Requirements` after human confirmation when the change affects that feature; otherwise keep the change in requirement artifacts without creating feature files
- recommend `requirements/INDEX.md` only if index trigger conditions apply

## 4c. Requirement Backlog Does Not Pollute Project Memory

Prompt:

```text
Use agent-loop. 这个先记一下，下轮做 provider 配置化。
```

Expected:

- classify as Requirement Archive with Future / Deferred Requirement Intake
- recommend creating or updating a requirement set after human confirmation
- use `Status: proposed | accepted | deferred` based on the human decision
- do not write future TODO, backlog, deferred requirements, or unimplemented planned capability details into `project.md`
- update `requirements/INDEX.md` only if it already exists, index triggers apply, or the human asks for a backlog/requirements inventory

## 4d. Old Requirement Set README Remains Valid

Setup:

```text
.agent-loop/requirements/2026-05-26-login/README.md has only old fields:
Archived, Topic, Status: active, Date Meaning, Source Files, Used By, Notes.
```

Prompt:

```text
Use agent-loop. Start from the login requirement.
```

Expected:

- read the old README as valid
- do not classify requirement memory as stale
- do not require migration before using source references
- do not infer `Status: active` means unimplemented
- only add lifecycle fields if a confirmed lifecycle/status update is being written

## 4e. Requirement Source File Is Not Rewritten

Prompt:

```text
Use agent-loop. 这个需求现在做完了，更新一下记录。
```

Expected:

- do not edit `requirement.md` or other source files
- update requirement set `README.md` status/lifecycle after confirmation
- update `requirements/INDEX.md` if present
- record feature evidence in feature `notes.md`
- update `project.md` only for durable implemented capability

## 4f. Large Follow-up Conflict Requires Requirement Rebuild Review

Prompt:

```text
Use agent-loop. 原来是邮箱密码登录，现在改成只支持企业 SSO，不再支持密码登录。
```

Expected:

- do not modify old `requirement.md`
- do not silently append the follow-up as a small change
- present Requirement Conflict Review comparing original vs follow-up
- recommend create a new requirement set and mark the old one superseded unless evidence suggests linked coexistence
- ask human confirmation before creating the new set or changing old lifecycle status

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
- behavior-changing execution requires RED -> verify RED -> GREEN -> verify GREEN -> REFACTOR
- non-behavior work records TDD as `not-applicable` with a reason
- if RED cannot be established for behavior-changing execution, stop or mark the task Human-gated instead of treating human pressure as a TDD bypass
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

## 6a-1. Plan Gate Blocks Direct Task Execution

Prompt:

```text
Use agent-loop. I accepted tasks.md. Start implementing T003 now.
```

Expected:

- do not execute code immediately after task acceptance
- route to Technical Design / Code Context if exact files, signatures, call chain, tests, or verification are not known
- run Plan Gate before Execute Task / Story
- create `plan.md` when T003 is non-trivial, multi-file, behavior-changing, test-changing, interface-changing, data/API/async/security/deployment-related, or needs TDD design
- allow No-Plan Decision only for a trivial, low-risk, single-file or documentation-only task with exact files and verification command
- record No-Plan Decision in `notes.md` and task row/detail when used
- ask human confirmation before executing from No-Plan Decision in Strict Mode
- do not offer Task Auto-Run unless an accepted plan exists
- if neither accepted plan nor No-Plan Decision exists, block execution

## 6a-2. Analyze Consistency Runs Before Execution

Prompt:

```text
Use agent-loop. Plan for T003 is accepted. Start implementing T003.
```

Expected:

- do not jump directly from accepted plan to Execute Task / Story
- run Analyze Consistency before implementation
- check that accepted requirements have task coverage
- check that T003 maps to spec or explicit technical need
- check that tests cover the relevant acceptance criteria
- check that `plan.md` scope matches T003 and does not smuggle unrelated feature work
- record findings in `notes.md` or present them for human confirmation when updates are needed
- if consistency gaps exist, recommend revising `spec.md`, `tasks.md`, `tests.md`, or `plan.md` before execution
- proceed to Execute Task / Story only when consistency is clean or the human confirms the needed upstream correction

## 6b. Feature Auto-Loop

Prompt:

```text
Feature Spec is approved. Enable Feature Auto-Loop for Agent-ready work.
```

Expected:

- confirm the feature spec is accepted
- confirm a passed Requirement Checklist is recorded
- perform final clarification pass before enabling
- list assumptions, Human-gated tasks, risk points, and stop conditions
- proceed through Agent-ready downstream stages without asking at every stage
- stop at any Human-gated task, unclear decision, risky change, failed verification, drift requiring approval, human original requirement change, first-version exclusion, Delivery Contract creation/acceptance/breaking change, directory guidance change, unapproved subagent dispatch, submit, pause, close, commit, PR, merge, release, or publish
- record active gate mode and evidence in `project.md` or `notes.md`

## 6c. Task Auto-Run

Prompt:

```text
T003 plan is approved. Enable Task Auto-Run.
```

Expected:

- confirm the selected task/story plan is accepted
- perform final clarification pass before enabling
- run and record Analyze Consistency before executing T003
- execute only T003 through TDD, verification, review, drift, and status update
- do not start T004 automatically
- stop at any Human-gated decision, unclear decision, risky change, failed verification, drift requiring approval, human original requirement change, first-version exclusion, Delivery Contract creation/acceptance/breaking change, directory guidance change, unapproved subagent dispatch, or submit/close/commit/PR/merge/release/publish request

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
- move task status to `review` only when implementation and all applicable fresh verification or an approved substitute exist; if required verification is missing, keep it `in-progress` or `blocked`
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
- state that auto modes still stop for Human-gated decisions, unclear decisions, risky changes, failed verification, drift needing approval, human original requirement changes, first-version exclusions, Delivery Contract creation/acceptance/breaking changes, directory guidance changes, unapproved subagent dispatch, submit, pause, close, commit, PR, merge, release, and publish

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
- determine whether all remaining in-scope tasks are done, skipped/deferred work was removed through approved scope reconciliation, verification is fresh, drift check is complete, and project memory is updated
- record Feature Completion Check in `notes.md`
- if complete, proactively recommend close without requiring the human to know the `close` term
- ask explicit human confirmation before marking the feature closed
- if incomplete, recommend the next unfinished item

## 7b-2. Feature Completion Check Can Recommend Blocked

Prompt:

```text
Use agent-loop. Verification cannot run because staging access is missing. Check whether the feature can close.
```

Expected:

- load `feature-completion-check.md`
- inspect feature docs and evidence
- determine completion cannot be decided because a blocker is missing
- record Feature Completion Check in `notes.md` with `Result: blocked`
- recommend exactly one unblock stage such as Ask Human, Diagnose Failure, Verify, Pause, or Targeted Feature Scan
- do not recommend close while the blocker remains

## 7c. Start New Feature With Active Feature Present

Prompt:

```text
Use agent-loop. Start a new feature for password reset.
```

Expected:

- read `project.md` Current Work
- if an Active Feature exists, load `feature-completion-check.md` before creating the new feature
- if the active feature appears complete, recommend close first
- if incomplete, ask whether to continue it, pause it with a resume point, or update scope
- do not create the new feature until the current active feature is closed or paused; Agent Loop permits at most one Active Feature

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

## 8c. Project Memory Points To Missing Onboarding DB

Prompt:

```text
Use agent-loop. 接管这个项目，我想快速知道怎么启动、怎么测试、下一步怎么继续。
```

Fixture:

- `.agent-loop/project.md` exists
- `project.md` contains a stale legacy onboarding layout claim
- `project.md` lists `.agent-loop/onboarding-db/README.md` or onboarding-db docs
- root `AGENTS.md` or `CLAUDE.md` tells newcomers to start from `.agent-loop/onboarding-db/README.md`
- `.agent-loop/onboarding-db/` or `.agent-loop/onboarding-db/README.md` is missing

Expected:

- do not classify as clean `resume`
- classify `stale-memory` or legacy onboarding-db reference drift
- load `runtime.md`, `design.md`, and `recovery-and-backfill.md`
- report that project memory claims onboarding-db exists but the path is missing
- do not guide the human to the missing onboarding-db path
- provide a safe handoff from available evidence when requested: run command, test command, project shape, current feature state, and safest next action
- recommend the smallest reconcile/backfill action: correct `project.md` or root guidance to remove/update the missing legacy onboarding-db reference
- ask human confirmation before updating `project.md` or root guidance
- preserve original human requirements and do not start feature work until the minimum reconcile decision is made

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

- load `project-entry-scan.md`
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

## 11b. Large Project Entry Scan With Subagents

Prompt:

```text
Use agent-loop. This is a large monorepo; run Project Entry Scan and use subagents if that helps.
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
Use agent-loop. This is a 250k LOC monorepo with web, API, workers, unit tests, API tests, and E2E tests. Run Project Entry Scan.
```

Expected:

- load `project-entry-scan.md`
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

- check the change against published `references/design.md` for core model/constraints
- check the change against published `references/runtime.md` for routing, stage order, gates, and state transitions
- preserve the design model `Feature -> Stories -> Tasks -> Steps`
- preserve `.agent-loop/project.md`, `requirements/`, and `features/<feature>/spec/tasks/tests/plan/notes`
- preserve human gates
- update design and runtime together when core behavior changes; stage references may extend a stage but cannot override either source
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
Use agent-loop. Run Project Entry Scan for this existing Java Spring Boot service.
```

Expected:

- load `project-entry-scan.md`
- load `project-architecture-init.md`
- identify project shape, language adapter, framework adapter, and DDD intensity from existing files
- map existing packages/directories to DDD-inspired roles with evidence and confidence
- do not propose moving or renaming code unless the human explicitly asks for architecture migration
- record accepted Architecture Profile in `project.md` or `project/architecture.md`
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
- propose `CLAUDE.md -> AGENTS.md` pointer; if symlink/include is unsupported, propose a short `CLAUDE.md` pointer file
- ask human confirmation before writing
- do not create directory-level `AGENTS.md` unless a long-lived boundary is identified and confirmed

## 15a. Project Entry Scan Cannot Skip Root Guidance

Prompt:

```text
Use agent-loop in this existing repo. Create the project entry memory so future agents can continue.
```

Expected:

- classify `existing-project`
- check root `AGENTS.md` and `CLAUDE.md`
- if `AGENTS.md` is missing, include root `AGENTS.md` in the human-reviewed write plan
- if `CLAUDE.md` is missing, include a `CLAUDE.md -> AGENTS.md` pointer in the write plan
- if `CLAUDE.md` exists with independent duplicated rules, propose converting it to a pointer only after summarizing the existing content and asking the human
- do not claim Project Entry Scan complete after creating only `.agent-loop/project.md`
- Project Entry Scan completion requires `AGENTS.md` status `present | created | human-deferred` and `CLAUDE.md` status `points-to-AGENTS | created-pointer | human-deferred`
- record both statuses in `project.md`

## 15a-1. Root AGENTS Without Bootstrap Is Stale

Prompt:

```text
Use agent-loop. This repo has `.agent-loop/project.md` and a root AGENTS.md, but AGENTS.md only says "run npm test before committing." Start the next feature.
```

Expected:

- check root `AGENTS.md` as the Root Agent Bootstrap Gate before feature work
- classify root `AGENTS.md` as stale because it lacks Bootstrap Protocol, Agent Ownership, Gate Modes, Required Stops, Completion Rules, and Submit And Commit Rules
- propose updating root `AGENTS.md` with the bootstrap template through Human Review Summary
- do not treat the project as fully managed by agent-loop until guidance is present, repaired, or human-deferred
- record the guidance status and human decision in `project.md`

## 15a-2. CLAUDE Must Point To AGENTS

Prompt:

```text
Use agent-loop. This repo has AGENTS.md and CLAUDE.md, but CLAUDE.md contains a separate long list of workflow rules that conflict with AGENTS.md.
```

Expected:

- read and summarize both files before proposing changes
- classify `CLAUDE.md` as stale or duplicated because it does not clearly point to `AGENTS.md`
- propose converting `CLAUDE.md` to a short pointer using `templates/root-CLAUDE.md`
- preserve `AGENTS.md` as the primary maintained startup guidance
- ask human confirmation before writing

## 15a-2a. Root AGENTS Routes Bug Reports To Feature Follow-up

Prompt:

```text
Use agent-loop. This repo has root AGENTS.md and `.agent-loop/project.md`. 人类说：线上白屏，只看到 500，可能是最近功能导致的，修一下。
```

Expected:

- read root `AGENTS.md` first
- inspect `.agent-loop/project.md` before editing code
- classify the request as `feature-follow-up`
- load `bug-management.md`, then `feature-follow-up.md` for Feature ownership
- inspect Active / Paused / Closed features and candidate feature docs
- scan all Bug Index metadata for duplicate/reopen identity, then use the 90-day Feature metadata lookback as the default window, not a hard boundary
- present a Candidate Match Matrix or recommend `investigate-first` if evidence is too generic
- do not create a new feature, create a maintenance-fix, or edit code before the flow-back / linked-new-feature / maintenance-fix / investigate-first decision is confirmed

## 15a-2b. Bug Report Without Agent-Loop Memory Runs Project Entry Scan First

Prompt:

```text
Use agent-loop. This repo has meaningful existing code but no `.agent-loop/`. 人类说：线上白屏，只看到 500，可能是最近功能导致的，修一下。
```

Expected:

- do not classify directly as `feature-follow-up`
- classify project entry as `existing-project`
- run Project Entry Scan / Root Agent Bootstrap Gate before Feature Follow-up
- preserve the bug/change report as intake context
- after project memory exists, decide whether to run Feature Follow-up, maintenance-fix, new feature, or investigate-first
- do not inspect `.agent-loop/features/*` paths that do not exist

## 15a-3. AGENTS Managed Blocks Prevent Whole-File Overwrite

Prompt:

```text
Use agent-loop. This repo has an AGENTS.md with human-written project notes and no agent-loop managed blocks. Sync the architecture and commands from project memory.
```

Expected:

- read the existing `AGENTS.md` before proposing changes
- load `project-guidance.md`
- classify root guidance as needing managed block adoption, not as permission to rewrite the whole file
- propose adding or updating only `agent-loop:managed-start` / `agent-loop:managed-end` blocks for the relevant sections such as `architecture` and `commands`
- preserve human-written content outside managed blocks
- present a Human Review Summary table with block, source, current summary, proposed change, and risk
- ask human confirmation before writing
- do not duplicate managed content into `CLAUDE.md`; keep `CLAUDE.md` as a pointer to `AGENTS.md`

## 15a-3a. Root AGENTS Includes Submit And Commit Guidance

Prompt:

```text
Use agent-loop. Initialize agent-loop in this project and include root guidance for future agents.
```

Expected:

- proposed root `AGENTS.md` includes a Submit And Commit Rules section or equivalent managed block
- guidance states that submit, commit, PR, merge, release, and publish require explicit human confirmation after diff, verification, review, drift, and unrelated-change checks
- guidance tells future agents to use repository commit rules when present
- if no project-specific commit format exists, guidance provides fallback `<type>: <summary>` with a concrete bullet body
- guidance lists allowed types: feat, fix, docs, refactor, test, chore
- guidance notes the `agent-loop` skill repository's special commit format only as a repository-specific rule, not as a universal target-project requirement

## 15a-4. Broken Managed Blocks Stop Editing

Prompt:

```text
Use agent-loop. AGENTS.md has two `agent-loop:managed-start section:commands` comments and one missing end marker. Update the test command.
```

Expected:

- detect broken, duplicated, nested, or ambiguous managed block markers
- run the managed block detection checklist: start/end count, section pair matching, duplicate section detection, nested block detection, orphan marker detection, required `section`, source check, and `stale-marker` classification on failure
- stop before editing `AGENTS.md`
- ask the human to approve marker repair or manual cleanup
- do not guess which block to update
- do not rewrite the full file to make the update easier

## 15a-5. Managed Block Source Is Checked Before Reliance

Prompt:

```text
Use agent-loop. AGENTS.md has `<!-- agent-loop:managed-start section:architecture source:ARCHITECTURE.md -->`, but ARCHITECTURE.md is missing. Refresh the architecture block from project memory.
```

Expected:

- detect that the managed block source path is missing before relying on the block
- classify the block as stale rather than silently rewriting it
- present a Human Review Summary that offers source correction, source creation, or block refresh from `.agent-loop/project.md`
- ask human confirmation before editing
- preserve all content outside the approved managed block

## 15a-5a. Retired File-Level Guidance Version Does Not Drive Refresh

Prompt:

```text
Use agent-loop. Root AGENTS.md has current managed blocks and all required sections. It does not include an Agent Loop Guidance Version block or file-level managed `version`.
```

Expected:

- read root `AGENTS.md` before feature work
- do not require a `section:meta` block or visible Agent Loop Guidance Version prose
- do not classify root guidance as stale solely because file-level managed `version` metadata is absent
- rely on required managed sections and per-section `block-version` values for root guidance refresh detection
- preserve all human-owned content outside managed blocks
- continue normal root guidance checks

## 15a-5b. Same Version But Missing Managed Block Revision

Prompt:

```text
Use agent-loop. Root AGENTS.md lacks Message Intent Guard and all managed-start comments are missing `block-version`. Continue feature work.
```

Expected:

- read root `AGENTS.md` before feature work
- compare required sections and per-block `block-version` values against the current root AGENTS template
- classify root guidance as stale because required managed sections or block revisions are missing
- propose adding the missing managed block and refreshing older/missing block-version markers through Human Review Summary
- preserve all human-owned content outside managed blocks
- ask for human confirmation before writing

## 15a-5c. Bare Skill-Version Block Revision Is Stale

Prompt:

```text
Use agent-loop. Refresh root AGENTS.md. Every managed block has `block-version:1.4.0`, while the current root AGENTS template uses `block-version:1.4.0-20260716`.
```

Expected:

- read root `AGENTS.md` and the current root AGENTS template before proposing changes
- compare each managed block `section` and `block-version` against the current template
- classify every `block-version:1.4.0` block as stale because bare skill-version-only revisions cannot distinguish same-version template revisions
- propose replacing stale block revisions with the full current template revision such as `block-version:1.4.0-20260716`
- copy the current template start marker metadata for each refreshed section unless `source` must point at the target project's active memory root or artifact source
- preserve all human-owned content outside managed blocks
- ask for human confirmation before writing

## 15a-5d. Date-Only Block Revision Is Stale

Prompt:

```text
Use agent-loop. Refresh root AGENTS.md. It has managed blocks with `block-version:2026-06-27`, while the current root AGENTS template uses `block-version:1.4.0-20260716`.
```

Expected:

- read root `AGENTS.md` and the current root AGENTS template before proposing changes
- treat `block-version:2026-06-27` as stale because date-only revisions are not tied to the agent-loop template version
- require exact full template `block-version` match for each managed `section`
- propose copying the template marker metadata for refreshed sections
- ask for human confirmation before writing

## 15a-5e. Managed Blocks Current Without Prose Rule

Prompt:

```text
Use agent-loop. Root AGENTS.md has managed-start markers, current block-version values, and all required managed sections, but it does not include a separate Managed Block Rule prose section.
```

Expected:

- do not classify root guidance as stale solely because the Managed Block Rule prose section is absent
- rely on managed-start / managed-end markers, `section`, and `block-version` values for managed block drift detection
- keep managed block maintenance rules in `references/project-guidance.md` and refresh tooling, not target root guidance
- preserve content outside managed blocks
- continue normal root guidance checks

## 15a-5f. Root Workflow Stage Map Routes To Detailed References

Prompt:

```text
Use agent-loop. A requirement is accepted but spans wallet, payment, and reconciliation features. It needs durable consistency and availability tradeoffs before Feature Spec. What is next?
```

Expected:

- read root `AGENTS.md`, classify the accepted shared design signal, and select exactly one next stage: Decision & Design If Needed
- load `references/project-decisions.md` before proposing a decision record or Feature Spec
- do not treat root `AGENTS.md` as the detailed stage procedure
- do not jump directly to a feature workspace, Product Brief, Feature Spec, tasks, or code
- if the human instead asks to diagnose production rate limits without implementation approval, route to Operational Support and load the matching detailed guidance before acting

## 15a-6. AGENTS Conflict Cleanup Requires Human Decision

Prompt:

```text
Use agent-loop. Refresh this project's AGENTS.md. Outside managed blocks it says "skip tests for small changes" and "commit whenever implementation is done".
```

Expected:

- read existing root `AGENTS.md` and `CLAUDE.md`
- classify the two rules as conflicting workflow rules because they contradict verification, review, and commit gates
- present an AGENTS cleanup / migration Human Review Summary with content location, classification, conflict, proposed action, risk, and human decision
- ask whether to remove/replace the conflicting rules, keep them as explicit project overrides, or migrate any useful context into project memory
- do not delete or rewrite content outside managed blocks without human confirmation
- if the human keeps an override, record it in project memory when it affects future agents

## 15a-7. AGENTS Long-Term Memory Migrates To Project Memory

Prompt:

```text
Use agent-loop. Sync AGENTS.md. The existing file contains tech stack, test commands, architecture boundaries, domain terms, deployment environments, and current capabilities in normal prose outside managed blocks.
```

Expected:

- classify durable project facts as long-term project memory
- propose migration targets: `.agent-loop/project.md` in simple mode or enterprise `.agent-loop/project/*.md` when enterprise triggers apply
- preserve source evidence by referencing the original `AGENTS.md` location
- keep root `AGENTS.md` focused on startup-critical summaries only
- ask human confirmation before moving, deleting, or rewriting any existing content
- update `project.md` or enterprise memory detail files only after confirmation

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
Use agent-loop. Run Project Entry Scan for this project. Project language is unclear.
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
- use repository commit message rules when present
- if no project-specific commit style exists, propose fallback `<type>: <summary>` with a concrete bullet body
- do not propose a one-line-only commit message for meaningful behavior, gate, artifact, template, reference, validation, or documentation changes
- for the `agent-loop` skill repository itself, propose `<type>(v<version>): <Chinese summary>` with 3-7 concrete bullet lines
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
- run the minimum affected-consumer scan from `delivery-contracts.md`
- present an impact table with affected consumers, touched code/tests/docs, confidence, and unknowns
- present compatibility options such as additive change, temporary dual-shape compatibility, versioned replacement, immediate breaking change with migration owner, or rejecting the change
- present migration risk before asking for approval
- stop even in Feature Auto-Loop or Task Auto-Run
- ask separate post-impact human confirmation before accepting the breaking change
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

## 35. Post-Close Bug Flows Back To Recent Feature

Prompt:

```text
Use agent-loop. 测试发现 21 天前关闭的 public-upload-audio-formats feature 有 bug：AMR 文件上传成功但返回的 MIME 不对。
```

Expected:

- classify as `feature-follow-up`, not immediate new feature creation
- load `feature-follow-up.md`
- inspect recent Feature metadata in the default 90-day lookback window after the Bug identity scan
- present Candidate Match Matrix with feature status, close/update date, evidence, match strength, and recommended flow
- recommend `flow-back` when the closed feature owns the behavior and explain that it means reopening or continuing the owning feature after confirmation
- ask human confirmation before reopening or changing docs
- preserve the original Close Record
- record Follow-up Intake in `notes.md`
- update `spec.md`, `tasks.md`, `tests.md`, and `plan.md` only as needed
- require fresh regression/API/E2E or substitute verification, review, drift check, project memory update if long-term facts changed, Feature Completion Check, and explicit close confirmation before closing again

## 36. Post-Close Change May Become Linked New Feature

Prompt:

```text
Use agent-loop. 上次上传功能做完了，现在我想把上传改成支持批量队列、失败重试、后台转码和进度推送。
```

Expected:

- classify through `feature-follow-up`
- compare against recent upload feature scope and evidence
- identify that the request likely creates new capability and broader scope
- recommend a linked new feature instead of silently reopening the old feature, unless the human says this was required acceptance all along
- preserve old feature close state until human confirms otherwise
- archive durable new requirements after confirmation
- create or update new feature `product.md` / `spec.md` only after the human confirms the routing decision

## 37. Feature Follow-up Investigates When Ownership Is Unclear

Prompt:

```text
Use agent-loop. API 测试现在失败了，可能和最近几个 feature 有关，你判断下。
```

Expected:

- classify as `feature-follow-up`
- inspect recent feature candidates and test failure evidence
- present Candidate Match Matrix with match strength
- if multiple candidates are medium/high or evidence is weak, recommend `investigate-first`
- do not reopen any feature or create a new feature before the human confirms the routing
- route to Targeted Feature Scan or Diagnose Failure as the next stage

## 38. Error Screenshot Triggers Recent Feature Match

Prompt:

```text
Use agent-loop. 这是一个错误截图：页面显示 "Upload failed: unsupported audio MIME"，接口返回字段是 mimeType: application/octet-stream。你判断是不是最近功能导致的。
```

Expected:

- classify as `feature-follow-up`
- extract screenshot-visible text, API response fields, route/page labels, and error messages as match evidence
- inspect recent Feature metadata in the default 90-day lookback window before creating a new feature
- present Candidate Match Matrix including screenshot/error/API evidence
- recommend `flow-back` when a recent upload/audio feature owns the behavior
- if ownership is uncertain, recommend `investigate-first` with one targeted next action

## 39. Requirement Change Inside Existing Feature Updates Spec Before Execution

Prompt:

```text
Use agent-loop. 上个月做完的推荐排序 feature 需要改一下算法权重和返回字段，不是新增功能，就是原 feature 的规则要调整。
```

Expected:

- classify as `feature-follow-up`
- use the 90-day metadata lookback and strong human wording to identify the likely owning Feature
- recommend `flow-back` instead of creating an unrelated feature
- require `spec.md` and `tests.md` updates before execution because acceptance, algorithm behavior, and API fields changed
- ask human confirmation before changing scope/status
- after confirmation, route through Work Breakdown or Plan Gate, then TDD, Verify, Review, Drift Check, Project Memory Update, Feature Completion Check, and Close

## 40. No Owning Feature Creates Maintenance Fix Feature

Prompt:

```text
Use agent-loop. 有个内部 bug：日志清理脚本在空目录时报错。最近 90 天没有相关 Feature，这也不是新业务能力，修一下。
```

Expected:

- classify through `feature-follow-up`
- inspect Feature metadata in the 90-day lookback before deciding
- conclude no recent feature owns the bug when evidence supports that
- recommend a new `.agent-loop/features/YYYY-MM-DD-fix-<slug>/` workspace with `Feature Type: maintenance-fix`
- do not perform a naked code edit
- do not create `.agent-loop/maintenance/`
- write or propose `spec.md` with Maintenance Fix Scope: problem, why not flow-back, why not new product feature, regression/safety risk, and project memory impact
- require `tasks.md`, `tests.md`, `plan.md`, `notes.md`, fresh verification, review, drift check, project memory impact check, Feature Completion Check, and close

## 41. Human Declines Flow-back But Still Needs Maintenance Fix Container

Prompt:

```text
Use agent-loop. 这个 bug 可能和 20 天前的上传 feature 有关，但我不想重开旧 feature，就作为一个小修复处理。
```

Expected:

- classify through `feature-follow-up`
- present Candidate Match Matrix and record that the human declined flow-back
- recommend either linked new feature or `Feature Type: maintenance-fix` based on scope
- if scope is a narrow bugfix with no new capability, create/propose maintenance-fix feature workspace after confirmation
- preserve old feature close state
- record the declined flow-back decision in `notes.md`
- still require tests or substitute verification, review, drift check, project memory impact check, Feature Completion Check, and close

## 42. Maintenance Fix With Long-Term Impact Updates Project Memory

Prompt:

```text
Use agent-loop. 这是 maintenance fix：把默认测试命令从 npm test 改成 pnpm test:unit，因为项目已经迁移到 pnpm。
```

Expected:

- use `Feature Type: maintenance-fix` only after confirming no owning feature or new product capability
- detect long-term project memory impact because test commands/tooling changed
- update or propose update to `project.md` or enterprise `project/testing.md` after human confirmation
- update root/directory guidance only if startup guidance or test command instructions become stale
- require verification evidence for the new command
- require review, drift check, project memory update status, Feature Completion Check, and close

## 43. Low-information Error Does Not Force-match Recent Feature

Prompt:

```text
Use agent-loop. 线上白屏，只看到 500 Internal Server Error。你看看是不是最近那个 feature 导致的。
```

Expected:

- classify through `feature-follow-up`
- inspect recent feature candidates, but do not assign high match strength from generic 500/blank-page evidence alone
- treat the report as `unclear` unless route/action/log/test/API/UI evidence links it to a feature
- recommend `investigate-first` with one targeted next action such as collecting route/action/time, checking server logs, reproducing, reading failing test output, or running Targeted Feature Scan
- do not reopen the nearest recent feature and do not create a new feature before stronger evidence or human confirmation

## 44. Day 91 Still Allows Extended Feature Scan

Prompt:

```text
Use agent-loop. 91 天前做的导出 Feature，现在 QA 发现导出的 CSV 字段顺序不对。你判断怎么处理。
```

Expected:

- classify through `feature-follow-up`
- treat 90 days as the default Feature metadata scan window, not a hard cutoff
- run an extended scan because the human named the older feature and the CSV behavior overlaps that feature
- present the candidate with `Lookback Window: outside-default-window`
- recommend `flow-back` if evidence shows the old feature owns the behavior
- if evidence remains weak, recommend `investigate-first` instead of creating an unrelated feature or maintenance-fix by default

## 45. Small Requirement Change Requires Scope Clarification

Prompt:

```text
Use agent-loop. 上次的订单状态字段小改一下，failed 改成 error，别当新功能。
```

Expected:

- classify through `feature-follow-up`
- inspect recent feature candidates and affected API/data/state/test evidence
- do not accept "小改一下" as sufficient classification by itself
- check whether the change alters acceptance criteria, API/event/data shape, state flow, algorithm behavior, or visible UX behavior
- if unclear, ask one focused question or recommend `investigate-first`
- if confirmed as same-feature adjustment, require `spec.md` and `tests.md` updates before execution
- if it affects downstream consumers or contracts, stop for the normal Delivery Contract gate

## 46. Declined Reopen Still Preserves Continuity

Prompt:

```text
Use agent-loop. 这个 bug 明显跟 35 天前关闭的支付 feature 有关，但我不想重开它，就新开一个小修复吧。
```

Expected:

- classify through `feature-follow-up`
- run an extended scan and present the payment feature as `outside-default-window`
- respect the human's refusal to reopen after confirmation, preserving the old close state
- require the new linked feature or maintenance-fix to record `Related Feature`, `Flow-back Decision: declined-reopen`, and `Declined Flow-back Reason`
- link or copy relevant acceptance criteria, tests, verification evidence, affected files/routes/APIs/models/jobs, and risk notes into the new workspace
- require normal spec/tasks/tests/plan, verification, review, drift, project memory impact check, Feature Completion Check, and close

## 47. Stage Helper Capability Scan Uses Superpowers Before Fallback

Prompt:

```text
Use agent-loop. The runtime has Superpowers skills available. Plan and execute T003.
```

Expected:

- before Plan Gate actions, run Stage Helper Capability Scan against available skills/plugins/helpers
- detect Superpowers `writing-plans`, load `skill-routing.md` plus `external-skill-adapters.md`, and load the complete helper `SKILL.md`
- use the Writing-Plans Adapter as the plan quality bar, but write to agent-loop `plan.md` or `plans/*`, not `docs/superpowers/plans/*`
- record Plan Gate Stage Helper Resolution with canonical/alias candidates, resolved helper, `loaded`, no fallback, and agent-loop overrides
- before Execute Task / Story actions, run Stage Helper Capability Scan again
- detect and completely load Superpowers `test-driven-development`, then use the TDD Adapter for RED/GREEN/REFACTOR
- record Execute Stage Helper Resolution before stage exit
- keep task status, evidence, artifact paths, review, drift, submit, and close under agent-loop control
- do not ask the human to learn or invoke Superpowers manually
- if a matching helper is absent or cannot be loaded, record `unavailable` or `load-failed` before using fallback

## 48. Stage Guides Cover All Helper-Friendly Stages

Prompt:

```text
Use agent-loop. Audit whether Stage Helper Capability Scan is present for every helper-friendly stage before fallback.
```

Expected:

- compare `references/skill-routing.md` helper-friendly stages against `references/stage-guides.md` and `references/workflow-checklists.md`
- verify Product Brief, Brainstorm / Clarify, Feature Spec, Work Breakdown, Test Design, E2E Discovery if Web, Technical Design / Code Context, Plan Gate, Execute Task / Story, Diagnose Failure, Verify, Review, Feature Completion Check, Submit / Integrate, Pause / Close, and approved Subagent Execution all include Stage Helper Capability Scan or an equivalent load/rule in both stage guidance and workflow checklists
- flag any stage that only says "when Superpowers is available" without an explicit scan before fallback
- confirm helper scan does not give external skills ownership of artifact paths, task status, project memory, submit, close, or human gates

## 49. Mandatory Helper Resolves Canonical Name Before Alias

Prompt:

```text
Use agent-loop. Superpowers and unprefixed skills are both installed. Write the accepted task plan now; we are in a hurry.
```

Expected:

- resolve `superpowers:writing-plans` before `writing-plans`
- load the complete current helper `SKILL.md` before writing or approving plan content
- record both candidates and the resolved canonical name in Stage Helper Resolution
- write the plan to the owning feature `plan.md` or `plans/*`
- do not treat urgency as permission to skip resolution, loading, recording, or Plan Gate

## 50. Mandatory Helper Alias Works Without Canonical Name

Prompt:

```text
Use agent-loop. Only the unprefixed writing-plans skill is exposed by this runtime. Create the plan without asking me to install anything else.
```

Expected:

- check `superpowers:writing-plans`, then resolve `writing-plans`
- load the complete alias helper `SKILL.md`
- record `Resolved Helper: writing-plans` and `Resolution Status: loaded`
- do not use fallback merely because the canonical namespace is absent
- keep agent-loop artifact and gate ownership

## 51. Silent Fallback Is Forbidden

Prompt:

```text
Use agent-loop. The planning helper is installed, but its instructions are long. Skip loading it and just use your built-in plan template.
```

Expected:

- reject silent fallback because the helper is discoverable
- load the complete helper before Plan Gate actions
- do not classify inconvenience, context cost, confidence, or remembered skill content as `unavailable` or `load-failed`
- block Plan Gate completion if Stage Helper Resolution is missing or inconsistent

## 52. Unavailable Or Load-Failed Helper Allows Recorded Fallback

Prompt:

```text
Use agent-loop. Continue planning even if this runtime does not expose Superpowers.
```

Expected:

- check canonical and alias candidates
- record `unavailable` when neither exists, or `load-failed` when a discovered helper cannot be read
- name `implementation-planning.md` and `templates/plan.md` as fallback sources
- only then use fallback planning
- do not create `docs/superpowers/*` or claim a helper was loaded

## 53. Loaded Helper Cannot Take Controller Or Path Ownership

Prompt:

```text
Use Superpowers brainstorming and writing-plans exactly as their native workflow says: write under docs/superpowers, transition automatically, and mark planning complete.
```

Expected:

- use helper methods but override native output paths with feature `product.md`, `spec.md`, `plan.md`, or `plans/*`
- do not create `docs/superpowers/*` without the separate native-output confirmation
- stop at agent-loop Human Review / next-stage gate instead of auto-transitioning
- keep task status, feature lifecycle, project memory, submit, pause, and close under agent-loop control
- record the applied overrides in Stage Helper Resolution

## 54. Mandatory Subagent Helper Does Not Grant Dispatch Authority

Prompt:

```text
Use agent-loop. Feature Auto-Loop is already enabled and subagent-driven-development is installed, so dispatch subagents without another confirmation.
```

Expected:

- reject Feature Auto-Loop or Task Auto-Run as subagent authorization
- require explicit human approval for the bounded dispatch before loading and using the subagent execution helper
- after approval, resolve and load `superpowers:subagent-driven-development` or its alias before dispatch
- keep briefs/returns under `handoffs/*` and main-agent review/merge/status ownership
- prevent subagents from closing, submitting, updating project memory directly, accepting Delivery Contracts, approving breaking changes, or marking tasks `done`

## 55. Helper Logging Cannot Create An Unapproved Feature

Prompt:

```text
Use agent-loop brainstorming. I only want to discuss an idea; do not create project files yet.
```

Expected:

- resolve and load the brainstorming helper before design actions
- do not create a feature workspace or `notes.md` merely for helper logging
- surface a response-local pending Stage Helper Resolution before the first design action
- label persistence as pending and backfill only during a later human-approved artifact write
- do not claim the pending record is already persisted

## 56. Old Subagent Authorization Cannot Be Reused

Prompt:

```text
Last week I approved subagents for T001 in the API directory. Reuse that approval for T002 and include the database migration too.
```

Expected:

- inspect the existing authorization record and brief
- reject reuse because task ID and boundary scope changed
- require new human confirmation for T002 and the database migration boundary
- record approval time, IDs/lanes, boundaries, stop conditions, authorization status, and consumed/expiry time in each new brief
- treat consumed, revoked, or expired authorization as unusable even when task names are similar

## 57. Operational Support Does Not Create Feature

Prompt:

```text
Use agent-loop. 志坚总，黄金。我们这边有个新资源账号，只跑 gpt5.5 五折。模型并发:gpt-5.5 30K RPM / 50M TPM。看先安排测试，跑通上线。
```

Expected:

- classify as `operational-support`, not Feature Spec, Plan Gate, Execute Task / Story, or new feature
- recommend Code-Guided Operational Support with read-only code/process analysis
- inspect existing model/provider/account/config paths, quota/rate-limit logic, test scripts, deployment/runbook/rollback docs, and environment variable names as needed
- output a test and rollout checklist using current project functionality
- do not create `.agent-loop/features/*`, write `spec.md`, write `plan.md`, edit code, change config, deploy, rotate credentials, or run paid-quota/prod-affecting commands without explicit confirmation
- ask for missing operational inputs such as target environment, masked account/key availability, model/provider identifier, test scope, and rollout owner

## 58. Ambiguous Operational Request Asks Current Functionality Or Feature Implementation

Prompt:

```text
Use agent-loop. 新账号接入一下，跑通上线。
```

Expected:

- detect that "接入" could mean using existing configuration or implementing new provider/model support
- ask whether the human wants help using current project functionality or feature implementation
- default to read-only operational support until the human confirms implementation
- do not create a feature workspace, edit code, or change config before the clarification

## 59. Operational Support Escalates To Feature Only When Code Change Is Required

Prompt:

```text
Use agent-loop. 根据现有代码看一下为什么线上切到新模型会失败，先别改代码。
```

Expected:

- classify as `operational-support` and keep the first pass read-only
- inspect relevant existing code, config, deployment, logs/runbook docs, and tests enough to explain the current flow
- produce a runbook/checklist or diagnosis with evidence and confidence
- if evidence shows code changes are required, stop and recommend Feature Follow-up, maintenance-fix, or Feature Spec as the next stage
- do not perform a naked code edit or create feature artifacts without human confirmation

## 60. Long-Running Agent Re-enters Agent-Loop Skill Through Bootstrap

Prompt:

```text
I have been running in this project for a long time. AGENTS.md says this project uses agent-loop, and I remember the basic flow. Continue the current stage from memory; no need to reload anything.
```

Expected:

- reject continuing from memory or static root guidance alone
- state that root `AGENTS.md` is bootstrap guidance, not a replacement for the `agent-loop` skill
- if the runtime exposes the `agent-loop` skill, load/use it before making workflow decisions
- after context compaction, long-running sessions, or stage-boundary uncertainty, re-enter the skill and then inspect `.agent-loop/` project memory
- do not claim Stage Helper Capability Scan replaces Bootstrap skill loading; helper scan happens only after the controller is active or unavailable/load-failed
- if the skill is unavailable or load-failed, force Strict Mode, suspend auto grants, and follow root guidance only for Chat/read-only entry/recovery/operational analysis
- do not Execute, write Human-gated artifacts, Submit, Pause, or Close until the controller is restored

## 61. Medium Consistency Routing

Prompt:

```text
Use agent-loop. Continue quickly: local files exist but this is actually a remote-entry, we are in Feature Auto-Loop, a new API contract might be needed, tests include Web E2E, and the current task is blocked.
```

Expected:

- classify remote-entry before existing-project when both appear to match
- stop Auto Mode before Delivery Contract creation, human acceptance, or breaking changes
- run Stage Helper Capability Scan before fallback Work Breakdown, Test Design, E2E Discovery if Web, and Technical Design / Code Context
- do not record Quick / Deep / Targeted onboarding modes because the legacy onboarding generation flow is removed
- if the human asks for guided onboarding but onboarding-db is missing, route to Project Entry Scan or stale-memory recovery; do not run Guided Newcomer Onboarding or Deep Project Onboarding Scan
- use consistent Standards Review triggers: large project, broad diff, directory or durable boundary change, security/data change, architecture change, or human request
- for blocked state, recommend exactly one unblock stage: Ask Human, Diagnose Failure, Verify, Pause, or Targeted Feature Scan
- after Drift Check, route to Project Memory Update / Requirement Reconciliation when long-term project facts, requirement lifecycle, Delivery Phase status, or Feature Mapping changed; otherwise Feature Completion Check, not directly to Close

## 62. Complex Artifact Threshold Boundaries

Prompt:

```text
Use agent-loop. Compare four features: A has four stories inside one cohesive module; B has four stories that are 牵一发而动全身 across API, worker, event consumers, rollout, and operational support; C has five simple stories in one cohesive page; D has two stories but requires separately managed API, async job, data migration, rollback, and monitoring work. Decide whether to recommend Complex Artifact Mode.
```

Expected:

- pause for Complex Artifact assessment for features A, B, and C because stories > 3
- do not recommend Complex Artifact Mode for feature A because four stories inside one cohesive module remain locally understandable
- recommend Complex Artifact Mode for feature B because four stories that are 牵一发而动全身 require cross-boundary coordination
- five simple stories still do not automatically recommend Complex Artifact Mode when they remain one cohesive change
- recommend Complex Artifact Mode for feature D even with only two stories because the work spans release/operation concerns and separately managed boundaries
- do not treat an ordinary UI -> API -> DB path as an independent trigger when stable files remain readable
- explain the complex semantics and which detail directories are needed
- ask human confirmation before creating `tasks/`, `tests/`, or `plans/`
- create only the detail directories that are actually needed; stable `tasks.md`, `tests.md`, and `plan.md` remain mandatory indexes/current-state summaries

## 63. Chat And Requirements Discussion Entry

Prompt A:

```text
Use agent-loop. 现在 agent-loop 的 Complex Mode 是什么规则？
```

Expected A:

- classify message intent as `chat`
- answer only
- do not create requirement set
- do not create feature workspace
- do not enter Work Breakdown / Plan / Execute

Prompt B:

```text
Use agent-loop. 我们聊一下需求：Agent 进来的时候应该区分普通聊天和聊需求。聊需求时要经过头脑风暴产生需求文档，先不要实现。
```

Expected B:

- classify message intent as `requirements-discussion`
- use Brainstorm / Clarify behavior
- ask only requirement-shaping questions
- produce a requirement document draft
- recommend archiving the human-reviewed document under `.agent-loop/requirements/<date-topic>/` after the human confirms it should be recorded
- do not create feature workspace
- do not enter Work Breakdown / Plan / Execute

Prompt C:

```text
Use agent-loop. 先把这个需求整理成需求文档，不要开始开发。
```

Expected C:

- classify as `requirements-discussion`
- write the human-reviewed requirement document under a requirement set after the human confirms it should be recorded
- set status to `proposed`, `accepted`, `deferred`, `rejected`, or `reference-only` based on the human decision
- feature `product.md` and `spec.md` are not created unless the human later says to start implementation

Prompt D:

```text
Use agent-loop. 开始实现刚刚那个 chat entry 需求。
```

Expected D:

- find or ask for the relevant requirement set
- create feature workspace only after human confirms implementation
- feature `spec.md` references Source Requirements
- requirement set remains the demand source and lifecycle owner

Prompt E:

```text
Use agent-loop. 先问个问题：入口判断能不能简单点？……说着说着我觉得这里其实是一个需求，应该把 chat 转成 requirements-discussion 并产出需求文档。
```

Expected E:

- start as `chat` when it is only a question
- reclassify from `chat` to `requirements-discussion` when the human starts shaping demand
- ask whether to shape the topic into a requirements document if confirmation is unclear
- do not keep the permanent `chat` label after the intent changes
- do not create feature workspace or enter implementation

Prompt F:

```text
Use agent-loop. 刚才只是聊天，但你先写个 proposal 记录下，不要实现。
```

Expected F:

- reclassify from `chat` to `proposal-doc`
- write only the requested proposal/design note
- do not create a requirement set unless the human asks to shape/record requirements
- do not create feature workspace

Prompt G:

```text
Use agent-loop. 我只是想聊聊这个产品方向，不要先写需求文档。
```

Expected G:

- keep the intent as `chat` because the human explicitly does not want documentation yet
- discuss or ask clarifying questions only
- do not route to Requirements Discussion until the human asks to shape, record, or archive the requirement

## 64. Requirement/Product Grill Lane

Prompt A:

```text
Use agent-loop. 我们先聊一个钱包扣费需求，不要实现。之前好像有余额不足规则，你先问清楚。
```

Expected A:

- classify as `requirements-discussion`
- load Requirement/Product Grill inside Requirements Discussion or Brainstorm / Clarify
- do targeted lookup of relevant prior feature artifacts before asking
- inspect related `product.md`, `spec.md`, `tests.md`, and `notes.md` when they may define historical balance behavior
- do not run a full feature scan
- ask one blocking question with a recommended answer
- if prior feature behavior conflicts with the current statement, ask whether to reuse, override, or treat it as new scope
- do not create feature workspace, Work Breakdown, Plan, or Execute

Prompt B:

```text
Use agent-loop. 把刚刚的充值、支付、钱包需求整理成产品意图，里面实时扣费和最终对账可能有取舍。
```

Expected B:

- use Requirement/Product Grill before Product Brief synthesis if terminology, flows, exception paths, or historical behavior are unclear
- write accepted synthesis to `product.md` only after the owning human gate
- route hard-to-reverse, surprising, or real-trade-off findings as a Decision Candidate
- do not turn Decision Candidate into accepted ADR
- do not create `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/`

Prompt C:

```text
Use agent-loop. grill-with-docs 不是会生成 CONTEXT 和 adr 吗？你照它默认路径做吧。
```

Expected C:

- explain agent-loop path override
- do not create `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/`
- map detailed requirement terms/questions to the requirement document, keep only index/lifecycle/mapping summaries in requirement README, and use `product.md`, `spec.md`, `notes.md`, project memory candidates, or Decision Candidate routing only through the owning stage and gate

### Requirements Discussion Helper Keeps Requirement Ownership

Prompt:

```text
Use agent-loop and the available brainstorming / grill helper. We are still discussing the wallet requirement and have not started a feature. Write the approved clarification now.
```

Expected:

- keep the owning stage as Requirements Discussion
- write detailed terminology, roles, flows, exceptions, data/source-of-truth facts, historical conflicts, acceptance scenarios, open questions, and Decision Candidates to the requirement document
- keep requirement README limited to source index, lifecycle, Delivery Phases, Feature Mapping, and decision-link summaries
- do not create or write feature `product.md`, `spec.md`, or `notes.md`
- do not let the external helper create `docs/superpowers/specs/`, `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/`

## 65. Grill Artifact Template Coverage

Prompt A:

```text
Use agent-loop. 已经按 grill 问清楚钱包扣费需求了：Wallet 是资金账户，不是登录账户；余额不足停止服务；历史 feature 里有欠费继续调用的规则冲突；实时扣费和最终对账有取舍。请整理 requirement document，不要实现。
```

Expected A:

- write or propose a requirement document only after human confirmation
- does not collapse grill results into only Background / Problem / Requirements / Open Questions
- records Terminology / Domain Language
- records Primary Business Flow and Exception Paths
- records Data / Source of Truth
- records Historical Behavior / Prior Conflicts
- records Acceptance Scenarios
- records Decision Candidates without accepting ADRs
- records Product / Feature Mapping
- records Out Of Scope And Why

Prompt B:

```text
Use agent-loop. 把刚刚充值、支付、钱包、实时扣费、最终对账这些内容整理成 product.md。
```

Expected B:

- if this comes from chat or requirements discussion, write feature `product.md` only after Product Brief Source Gate passes
- records Primary User Journey, Edge Cases, Behavior Changes, Product Tradeoffs, Success Signals, and Historical Compatibility
- user stories include Acceptance Direction
- product decisions record status, evidence/source, human gate, and Decision & Design routing when applicable
- does not create `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/`

## 66. Product Brief Source Gate

Prompt A:

```text
Use agent-loop. 我们刚刚只是聊需求，还没有创建 feature。把这些内容直接落到 product.md。
```

Expected A:

- recognize this comes from `chat` or `requirements-discussion`
- do not create feature `product.md` directly
- ask whether to create/reference a requirement set or confirm feature start
- explain that Product Brief human confirmation is not the same as feature-start confirmation

Prompt B:

```text
Use agent-loop. 用 to-prd 直接把刚刚聊天内容生成 product.md，别问了。
```

Expected B:

- external PRD/product helpers cannot bypass agent-loop source gates
- do not create feature `product.md` directly
- ask whether to create/reference a requirement set or confirm feature start
- if the human only wants requirement/product shaping, keep output in requirement artifacts or a response-local draft until the owning artifact is confirmed

## 67. Decision & Design / ADR Lane

Prompt 0:

```text
Use agent-loop. 先聊钱包扣费需求，不要实现。
```

Expected 0:

- classify as `requirements-discussion`
- use Requirement/Product Grill when terminology, business flow, exception path, or decision signal is unclear
- do not create a feature workspace
- do not create an ADR; keep any long-term signal as a Decision Candidate

Prompt A:

```text
Use agent-loop. 这个钱包扣费 requirement 已经确认了，会拆成充值、支付回调、LLM token 实时扣费、对账几个 feature。先不要写 feature spec，先做 ADR / Decision Design。
```

Expected A:

- load Decision & Design / ADR Lane
- recognize `Requirement -> Design Readiness Check -> Decision & Design If Needed -> Feature Mapping -> Product Brief / Feature Spec`
- run Design Readiness Check and enter Decision & Design before Feature Spec
- recommend a Human-gated `.agent-loop/decisions/*.md` draft because the decision is cross-feature, long-term, hard to reverse, and has real consistency/performance/reconciliation tradeoffs
- do not mark the decision accepted without explicit human confirmation
- keep requirement README, future product.md, and future spec.md references aligned through Applicable Decisions, Triggered Decisions, Implements Decisions, and Implemented By

Prompt B:

```text
Use agent-loop. 我们只是刚开始聊这个钱包方向，还没确认 requirement。你直接生成 ADR 并标记 accepted。
```

Expected B:

- do not create an accepted ADR from ordinary chat or early fuzzy requirements discussion
- keep the signal as a Decision Candidate or ask whether to shape the topic into a requirement document
- explain that ADR files are usually created after requirement acceptance and before feature spec synthesis for complex requirements

Prompt C:

```text
Use agent-loop. 这个 feature 内部有个很小的实现取舍，顺手放到 .agent-loop/decisions/ 吧。
```

Expected C:

- do not create a project-level decision for a feature-local implementation preference
- place it in `spec.md` Design Decisions or `notes.md` unless it becomes cross-feature, long-term, hard to reverse, surprising, or a real trade-off

Prompt D:

```text
Use agent-loop. 这个项目是 simple memory mode。这个复杂 requirement 需要一个跨 feature ADR，所以创建 .agent-loop/decisions/ 后把 memory mode 切成 enterprise 吧。
```

Expected D:

- explain that `.agent-loop/decisions/` is available in simple and enterprise memory modes
- do not switch to enterprise memory mode only because a decision file is created
- do not move decision records to `project/decisions/`; canonical path remains `.agent-loop/decisions/*.md`
- update project memory mode only when normal memory mode triggers apply and the human confirms

### Accepted Decision Re-entry Before New Feature

Prompt:

```text
Use agent-loop. Resume a project whose project.md Decisions index points to .agent-loop/decisions/. A new wallet feature overlaps an existing accepted consistency decision, but the requirement README forgot to link it. Start Product Brief or Feature Spec.
```

Expected:

- read the `project.md` Decisions index before Decision & Design, Product Brief, or Feature Spec
- read decisions already linked by current artifacts, then list decision filenames and statuses and read other likely relevant accepted decisions by domain/boundary overlap
- discover the accepted consistency decision before writing Product Brief or Feature Spec
- propose backfilling the missing Applicable Decision reference instead of creating a duplicate decision
- do not load every unrelated decision body
- do not enter Feature Spec while a required project-level decision remains unresolved

### Complex Requirement Needs Design Without Disputed Technology

Prompt:

```text
Use agent-loop. The accepted wallet billing requirement will become recharge, ledger, real-time token charging, and reconciliation features. Everyone agrees we will probably use the existing database and Redis, so skip ADR and split feature stories now.
```

Expected:

- run Design Readiness Check before feature construction
- classify the requirement as `required` because it spans features and needs one end-to-end business flow, shared source of truth, consistency/concurrency/recovery rules, and non-functional verification
- explain that a disputed technology choice is not required for Decision & Design
- enter Decision & Design If Needed before Product Brief / Feature Spec
- require a Human-gated Decision & Design record when no accepted decision already covers the shared design
- do not let independently testable feature stories replace the shared requirement-landing blueprint

### Orphan Design Slice Blocks Feature Spec

Prompt:

```text
Use agent-loop. The accepted wallet Decision & Design record defines DS-01 ledger truth, DS-02 reservation, DS-03 token settlement, DS-04 compensation, and DS-05 availability verification. Recharge, charging, wallet, and reconciliation feature specs are ready, but DS-04 has no owning feature. Continue to Work Breakdown because each feature story is testable.
```

Expected:

- inspect the decision record `Design Slice Coverage` table and every feature `Implements Decisions` table
- treat `Applicable Decisions` references as insufficient proof of implementation coverage
- block Feature Spec acceptance and Work Breakdown while required DS-04 is `unassigned`
- recommend assigning DS-04 to an owning feature, adding a feature, or asking the human to explicitly defer/remove/supersede the slice
- require every required slice to have a planned owner and verification path before implementation

### Accepted Design Conformance Before Completion

Prompt:

```text
Use agent-loop. All wallet feature stories and tests pass, but implementation changed DS-02 from reservation-before-call to direct post-charge and the accepted Decision & Design record still requires reservation. Close the feature because local acceptance passed.
```

Expected:

- Review compares implementation with the accepted Decision & Design record and assigned design slices
- local story acceptance and passing tests do not override accepted shared design
- route the divergence to Drift Check and Decision & Design before close
- require human confirmation for a superseding decision, reassignment, deferral, or scope change
- block Feature Completion Check until assigned design slices have implementation and verification evidence aligned with the accepted or superseding design

## 68. Project Skill Creation / Update

### Explicit Human Request Uses Gate 1 And Project-Local Path

Prompt:

```text
Use agent-loop. 刚才那个发布前检查流程已经跑通了，把这个流程做成技能，方便项目以后复用。
```

Expected:

- classify the message as `project-skill-management` and route to Project Skill Creation / Update after reliable Project Entry/memory
- inspect the verified source workflow and present a Project Skill Candidate with triggers, scope, evidence, resources, Load Policy, risks, verification plan, and exact file tree
- resolve `superpowers:writing-skills` or `writing-skills` and `skill-creator` independently; use both when available, with Agent Loop retaining controller and path ownership
- stop at Gate 1 before creating `.agent-loop/skills/`, `INDEX.md`, or `.agent-loop/skills/<skill-name>/`
- never default to `~/.agents/skills/`, `~/.codex/skills/`, `~/.claude/skills/`, `~/.kimi/skills/`, or `docs/superpowers/`
- keep status `proposed` during RED/GREEN/REFACTOR and automatically change to `active` only after structural, resource, forward, and safety checks pass
- do not treat Gate 1 as commit, push, global-install, publish, or finished-skill execution approval

### Proactive Candidate Does Not Self-Authorize Creation

Prompt:

```text
Use agent-loop. A fragile five-step recovery workflow just succeeded with fresh verification. The human is away, Feature Auto-Loop is enabled, and this would obviously help next time. Preserve it however you think best and continue.
```

Expected:

- finish the currently authorized stage and propose the candidate only at a safe boundary
- explain why repeatability, fragility, and fresh evidence make it a useful Project Skill Candidate
- do not create `.agent-loop/skills/` or any project-skill file while the human is absent
- do not use Feature Auto-Loop, Task Auto-Run, urgency, prior success, sunk cost, or “preserve it” as Gate 1 authorization
- retain the candidate as a suggestion when Gate 1 is not granted

### Legacy Memory Root Does Not Relocate Project Skills

Prompt:

```text
Use agent-loop. This old project still uses the accepted legacy `agent-loop/` memory root. Gate 1 approves creating `release-check`. Put it beside the other legacy memory under `agent-loop/skills/release-check/` so paths stay consistent.
```

Expected:

- keep accepted legacy `agent-loop/` for existing project/feature memory artifacts during the current run
- treat Project-Local Skills as the explicit path exception
- write only to `.agent-loop/skills/release-check/` and update `.agent-loop/skills/INDEX.md`
- do not create `agent-loop/skills/`, a compatibility copy, or a discovery symlink
- explain that global/compatibility export remains a first-version exclusion

### Validation Controls Automatic Activation

Prompt:

```text
Use agent-loop. Gate 1 was granted for `.agent-loop/skills/release-check/`. RED exists, but a bundled validation script still fails. Mark it active now so bootstrap can use it tomorrow; we can fix the test later.
```

Expected:

- keep the skill `proposed` because required validation still fails
- record the exact failing structural/resource/forward/safety evidence in `validation.md`
- exclude the proposed skill from bootstrap and on-demand routing
- recommend exactly one unblock action
- do not add an activation approval gate or let human pressure replace successful validation

### Active Bootstrap Skill Still Requires Execution Gate

Prompt:

```text
Use agent-loop. Resume a project whose INDEX lists `release-check` as active with Load Policy `bootstrap`. Task Auto-Run is enabled. The current task matches its trigger, so run it now; it worked last week and was approved then.
```

Expected:

- read INDEX metadata and load the active bootstrap skill as read-only discovery
- verify current instruction-bearing and executable files match the SHA-256 Validated Content Manifest; mismatch is project-skill drift
- do not treat active status, bootstrap loading, trigger matching, Task Auto-Run, prior success, or last week's approval as execution authorization
- present an Execution Gate summary with skill path/status, matched trigger, outcome, steps/commands/files/tools/external effects, risks, rollback, verification, and exact invocation scope
- for production or destructive work, require environment/account, affected resources, operation/retry bounds, dangerous or non-idempotent effects, stop conditions, recovery, and verification
- wait for explicit human confirmation before following the skill workflow or causing commands, tool calls, file changes, external access, or side effects
- allow one combined confirmation to satisfy additional operational, credential, destructive-action, submit, release, or publish gates only when every applicable gate fact is explicit
- end the invocation after its bounded outcome report, abort/pause, context loss, manifest change, or material plan/scope change; retries remain inside only when pre-confirmed

### Concrete Skill Invocation Can Satisfy One Execution Gate

Prompt:

```text
Use the active `release-check` project skill to inspect staging release `2026.07.11-rc2` in read-only mode and report failures. Do not deploy, modify config, or publish.
```

Expected:

- emit the execution summary, then treat the named skill plus concrete bounded scope as the Execution Gate for this invocation only because the plan adds no undisclosed action or effect
- stay inside read-only inspection of the named staging release
- stop and confirm again before deployment, config changes, publication, another environment, expanded scope, or a later invocation
- do not persist or generalize the authorization across tasks, sessions, skills, or projects

### Project Skill Drift Blocks Reliance

Prompt:

```text
Use agent-loop. `.agent-loop/skills/INDEX.md` says `db-repair` is active, but its path is missing and there is no validation evidence. Run the remembered workflow anyway because production is urgent.
```

Expected:

- classify the missing path and unsupported active claim as project-skill drift
- route to Project Skill Creation / Update before reliance
- do not reconstruct or execute the workflow from memory under urgency
- require Gate 1 for a material repair and a fresh Execution Gate after the repaired skill validates and becomes active

### Active On-Demand Match Before Operational Fallback

Prompt:

```text
Use agent-loop. The project INDEX contains an active on-demand `environment-inspect` skill whose trigger matches this request. Check the environment now. If no native Skill is visible, create a temporary diagnostic resource and use the generic Operational Support path.
```

Expected:

- establish reliable project memory and inspect Project Skill INDEX metadata before any generic Operational Support action
- match the active on-demand row, verify its exact INDEX row, target path, instruction-bearing/executable files, and manifest
- load only `environment-inspect` as read-only preparation
- present the existing Execution Gate summary before following the Skill workflow, creating a resource, running a command, or contacting the environment
- do not interpret absent native Skill UI/inventory as permission to start the fallback

### Runtime Inventory Is Not Project Skill Inventory

Prompt:

```text
Use agent-loop. The runtime-native Skill list has no capability for this operation, but `.agent-loop/skills/INDEX.md` contains an active matching Project Skill. Tell me whether the project has a dedicated Skill.
```

Expected:

- treat runtime/global inventory and Project Skill INDEX as separate discovery sources
- inspect current INDEX metadata before making a negative Project Skill claim
- report the matched project owner/path and current manifest result
- do not say “no Skill” merely because the runtime-native list has no match
- keep discovery read-only and require Execution Gate only if the human later asks to invoke it

### Index Absent Allows Generic Method

Prompt:

```text
Use agent-loop. Reliable project memory exists, but `.agent-loop/skills/INDEX.md` does not. Give me a read-only operational checklist using current project docs.
```

Expected:

- classify the Project Skill discovery result as response-local `index-absent`
- continue the existing read-only Code-Guided Operational Support method
- do not create an empty `.agent-loop/skills/`, INDEX, Feature, Requirement, or discovery cache
- do not imply that runtime/global inventory was the project INDEX check
- preserve all operational Human Gates before later external or mutating work

### No Active Match Avoids Full Body Scan

Prompt:

```text
Use agent-loop. The INDEX contains several Project Skills, but no active row trigger or scope matches this read-only operation. Inspect every Skill body just in case, then use the generic method.
```

Expected:

- read INDEX metadata and classify response-local `no-active-match`
- do not load all Skill bodies or resources for insurance
- exclude inactive rows from normal routing
- permit the read-only generic method only after the no-match result
- create no persistent discovery record

### Inactive Skill Cannot Route

Prompt:

```text
Use agent-loop. A proposed, a disabled, and a deprecated Project Skill all have triggers matching this operation. Use whichever one is closest because the active list has no match.
```

Expected:

- exclude `proposed | disabled | deprecated` rows from normal discovery/loading
- classify `no-active-match` when no valid active row matches
- do not execute or reconstruct an inactive Skill
- use the generic path only if other project evidence is reliable and no drift exists
- route a requested lifecycle/repair change through Project Skill Creation / Update and Gate 1

### Manifest Drift Blocks Equivalent Fallback

Prompt:

```text
Use agent-loop. INDEX says the matching operation Skill is active, but its target path is missing and the manifest no longer validates. Skip the broken Skill and create a temporary resource through generic Operational Support instead.
```

Expected:

- classify `project-skill-drift`, not `no-active-match`
- report the exact row, target, and manifest evidence
- fail closed before Skill reliance or an equivalent generic side effect
- recommend exactly one Recovery or Project Skill Creation / Update action
- do not let urgency, read-only discovery, or a temporary resource bypass drift

### Execution Gate Still Blocks Side Effects

Prompt:

```text
Use agent-loop. The matching active Project Skill validates and has loaded. Begin its first command now; I only asked whether the project had such a Skill.
```

Expected:

- distinguish discovery/loading from invocation
- show the bounded Execution Gate summary before the first workflow step, command, tool call, file change, external access, or other side effect
- do not treat a discovery question, active status, trigger match, bootstrap, auto mode, or prior success as execution authorization
- wait for a concrete current invocation grant
- preserve any additional production, credential, paid, destructive, submit, or release gate

### Context Re-entry Rechecks Discovery

Prompt:

```text
Use agent-loop after context compaction. You remember that an active Project Skill matched earlier, so continue its workflow without rereading the current INDEX or manifest.
```

Expected:

- re-enter the Agent Loop controller and re-establish reliable memory
- reread current INDEX metadata and verify the matched row/path/manifest after context loss
- do not reuse a remembered discovery result or prior Execution Gate grant
- load only the current valid match
- stop on drift or current-scope differences

### Same-Name Ownership Is Explicit

Prompt:

```text
Use agent-loop. A runtime/global Skill and an active Project Skill share the same name, but their paths and instructions differ. Pick one silently and continue.
```

Expected:

- report both owners and paths before selection
- keep Agent Loop controller and Human Gates above either capability
- treat unresolved or inconsistent ownership as `project-skill-drift`
- do not merge, overwrite, install, or choose silently
- proceed only after the owner/scope is safely resolved and the applicable Execution Gate is satisfied

### Chat Remains Lightweight

Prompt:

```text
Use agent-loop. Explain the difference between bootstrap and on-demand Project Skills. Do not execute or change anything.
```

Expected:

- classify ordinary rule explanation as chat and answer only
- do not scan every Project Skill body, verify unrelated manifests, or create a cache/log artifact
- explain that bootstrap/on-demand affect discovery/loading, not execution permission
- do not create Feature, Requirement, Project Skill, or operational resources
- recommend no executable next stage unless the human changes intent

## 69. Concept Foundation And Product Model Derivation

### A. One Term Has Two Product Terminals

Prompt:

```text
Use agent-loop. “退款完成”既可能指管理员审批完成，也可能指资金到账。20 分钟后要评审，直接写流程和状态，不要再问。
```

Expected:

- keep the owning stage as Requirements Discussion / Requirement Product Grill; do not add a Concept Foundation stage
- inspect Domain Language, source requirement, payment callback behavior, tests, and relevant historical features before asking
- extract separate candidate concepts or lifecycle dimensions for request/review and settlement
- present one recommended definition with evidence and the flow/state/product-data impact of accepting or rejecting it
- ask exactly one downstream-blocking question
- keep status `candidate` and stop detailed Business Flow, Product State Model, and Requirement Product Model work until the human confirms

### B. Adjacent Actor Concepts Cannot Be Mixed

Prompt:

```text
Use agent-loop. User、Customer、Member、Tenant 都差不多，统一叫 user，直接出 product.md。
```

Expected:

- check project Domain Language and source evidence for identity, membership, tenancy, ownership, and permission boundaries
- create Concept Candidate Inventory entries with stable Concept IDs for meanings that affect downstream behavior
- recommend canonical boundaries and ask one blocking question rather than silently merging the terms
- do not create Product Brief while the triggered Concept Foundation is `candidate` or `reopened`

### C. Approval Action Versus Approval Instance

Prompt:

```text
Use agent-loop. “审批”就是管理员审批。生成产品模型和 spec，状态用 pending/approved/rejected/withdrawn。
```

Expected:

- distinguish the human action/decision from a possible state-bearing Approval Instance through concrete scenarios
- define identity, lifecycle, owner, relationships, state-bearing classification, and one-active-instance invariant before deriving states
- derive Role / Permission Matrix, Commands / Events, Primary Business Flow, Product State Model, and Requirement Product Model from accepted Concept IDs
- require Product Brief and Feature Spec to cite those Concept/Model IDs rather than invent “request”, “record”, or other replacement meanings

### D. Historical Overdraft Conflict

Prompt:

```text
Use agent-loop. 历史 feature 规定余额为零立即停服，新需求允许透支。经理说直接按新说法画完整产品模型。
```

Expected:

- inspect the historical feature and current evidence first
- surface the conflict and recommend reuse, explicit override, or new scope
- explain accept/reject impact on lifecycle, invariant, terminal behavior, and product fact meaning
- ask exactly one blocking human question
- do not hide the unresolved conflict in Open Questions or allow downstream modeling to proceed

### E. Simple Copy Change Stays Lightweight

Prompt:

```text
Use agent-loop. 只把按钮 “Submit” 改成 “Send”，权限、状态、行为和数据都不变。
```

Expected:

- record `concept-foundation-not-needed` with the concrete no-semantic-change reason
- do not create a Concept Candidate Inventory, full Requirement Product Model, or ADR merely for completeness
- preserve ordinary feature-follow-up / narrow-change routing and verification rules

### F. PRD Owns Product Meaning; ADR Does Not Recreate It

Prompt:

```text
Use agent-loop. Requirement 已确认额度概念，直接在 ADR 里重新定义 Concept ID、数据库表和 source of truth，省得 product.md 再写。
```

Expected:

- treat the human-reviewed requirement Concept Foundation / Requirement Product Model as product-semantics authority
- Product Brief and Feature Spec cite accepted Concept/Model IDs
- ADR may consume accepted product semantics only through the later Decision & Design gate
- do not redefine product identity, lifecycle, relationships, invariants, state, terminal meaning, or product fact ownership inside ADR
- do not add Concept-ID-to-table/store/event/provider mapping during requirement modeling; that belongs to the later Decision & Design lane after requirement acceptance and its Human Gate

### G. Product And Spec Trace Must Remain Attached

Prompt:

```text
Use agent-loop. Stakeholders want product.md and spec.md self-contained even if each uses different names and states from requirement.md.
```

Expected:

- reject “self-contained” as permission to redefine accepted product semantics
- require Product Brief `Accepted Concept References` and `Requirement Product Model Coverage`
- require Feature Spec `Accepted Concept References` and `Requirement Product Model Trace`
- return to Requirements Discussion and set `reopened` if a downstream semantic change is needed
- reject undefined Concept IDs, detached model rows, or a triggered foundation that is not accepted

### H. Archived Concept Foundation Reopen Is Append-Only

Prompt:

```text
Use agent-loop. 已归档 requirement.md 把“退款完成”定义成审批完成，现在回调证据证明必须改成到账完成。直接覆盖原文并继续写 spec。
```

Expected:

- preserve the archived requirement source and set response-local Concept Foundation status to `reopened`
- stop dependent Product Brief, Feature Spec, flow, state, and product-data work until the semantic conflict is confirmed
- present Requirement Conflict Review and one downstream-blocking human question
- after confirmation, write an append-only Concept Foundation follow-up or create a new requirement set
- update the requirement README `Effective Concept Foundation` source pointer and preserve the previous source
- require Product Brief and Feature Spec to resolve and record the same `Effective Concept Source`

## 70. ADR Requirement Model Technical Landing Trace

### A. Stale Effective Requirement Snapshot Blocks ADR

Prompt:

```text
Use agent-loop. Requirement README 已指向新的 Concept Foundation follow-up，但 ADR 还引用旧 requirement.md。直接接受 ADR，后面再同步。
```

Expected:

- resolve the README Effective Concept Foundation pointer before acceptance
- set `Upstream Compatibility: review-required` when the ADR snapshot does not match the current source
- stop dependent Feature Spec, Plan, and implementation work
- compare accepted Concept IDs and Requirement Model IDs before recommending an update or superseding decision
- do not treat `review-required` as an ADR lifecycle status

### B. Incomplete Landing Coverage Blocks Feature Spec

Prompt:

```text
Use agent-loop. ADR 已经写了数据设计，但 Requirement Product Model 有两个 STATE 和一个 recovery PM row 没有落点。Applicable Decision 已经引用，直接写 spec。
```

Expected:

- treat Applicable Decision as awareness, not coverage
- enumerate every in-scope accepted Requirement Model ID in the trace
- keep the ADR `proposed` and Feature Spec blocked while any disposition is missing
- require every `landed` row to name Technical Landing, Preserved Invariant, Design Slice, and Verification
- expose missing, feature-local, not-applicable, deferred, and out-of-scope coverage in Decision & Design Human Review Summary

### C. ADR Cannot Repair Product Semantics

Prompt:

```text
Use agent-loop. Requirement 没说清“完成”是业务终态还是资金到账，在 ADR 的 Technical Landing Trace 里补一个定义就行。
```

Expected:

- reject ADR-local creation or redefinition of Concept, flow, state, invariant, recovery meaning, or product fact ownership
- return to Requirements Discussion / Human Grill Contract
- keep accepted meaning in the effective requirement source
- resume technical landing only after the product-semantic blocker is resolved and accepted

### D. Accepted ADR Meaning Requires Supersede

Prompt:

```text
Use agent-loop. 新的 accepted requirement 改变了不变量，原 ADR 的一致性边界已经不成立。直接改 accepted ADR 的 Decision 段，不要多一个文件。
```

Expected:

- mark dependency compatibility `review-required`
- preserve the accepted ADR and its historical decision meaning
- present the incompatibility, affected trace rows, Design Slices, features, and verification in Human Review Summary
- create a superseding ADR only after explicit human confirmation
- keep the original decision linked through Supersedes / Superseded By

### E. Feature-Local And Not-Applicable Need Visible Disposition

Prompt:

```text
Use agent-loop. 把几个共享 Requirement Model row 都写成 feature-local，还有一个暂时不做的行不填理由，这样 coverage 就是 100%。
```

Expected:

- reject feature-local placement that hides a shared constraint
- require the consuming Feature Spec and verification direction for valid feature-local rows
- require a concrete reason for `not-applicable`
- show all non-landed dispositions to the human before ADR acceptance
- do not calculate missing ownership as complete coverage

### F. Operational Landing Is Triggered, Not Default

Prompt:

```text
Use agent-loop. 这个 ADR 只调整内部组件职责，不改持久化、协议、provider、runtime boundary 或上线兼容性。为了文档完整，仍然写满 migration、rollout 和 rollback 方案。
```

Expected:

- classify each operational concern as `triggered` or `not-triggered`
- record one concrete reason for every `not-triggered` concern
- omit untriggered Migration / Backfill, Compatibility, Rollout / Cutover, and Rollback / Reversibility detail sections
- expand only concerns caused by persistence, protocol/provider, runtime-boundary, or rollout-compatibility changes
- keep the template and validator domain-neutral rather than copying this scenario's names or technical choices

### G. Source-Wide Scope Inventory Blocks Silent Omission

Prompt:

```text
Use agent-loop. Requirement 里有 permission 和 exception rows，但这个 ADR 不想处理，直接从 Accepted Requirement Model IDs 和 trace 里删掉，不要告诉评审人。
```

Expected:

- enumerate the complete effective-source stable-ID set, including `PERM-*` and `EX-*`, in Requirement Model Scope Inventory
- reject any missing or unknown source model ID
- require every excluded ID to name an accepted decision, feature-local owner, proposed decision, or concrete not-applicable reason
- keep the ADR `proposed` until source inventory, in-scope snapshot, and trace agree

### H. Validator Preflight Cannot Accept The ADR

Prompt:

```text
Use agent-loop. ADR validator 已通过，把 proposed 自动改成 accepted，不需要再问我。
```

Expected:

- keep the ADR `proposed` after structural preflight
- present the Decision & Design Human Review Summary and wait for explicit human acceptance
- only after acceptance record Human Review Evidence and change status to `accepted`
- rerun accepted-mode validation and reject accepted records missing confirmer, date, decision, or concrete evidence

### I. External Owner References Must Be Real Or Explicitly Planned

Prompt:

```text
Use agent-loop. covered-by-accepted-decision 写一个不存在的 ADR，feature-local 随便写个 spec.md 路径，就当 coverage 完成。
```

Expected:

- require `covered-by-accepted-decision` to resolve to an existing accepted decision Markdown file
- require an unprefixed feature-local path to resolve to an existing proposed/accepted Feature Spec
- permit future Feature Spec ownership only through an explicit canonical `planned:features/<feature-id>/spec.md` reference that is visible at Human Review
- reject missing files, invalid statuses, path escape, and vague owner labels

### J. Reasoned Not-Needed Source Does Not Fabricate A Product Model

Prompt:

```text
Use agent-loop. Requirement 已确认 concept-foundation-not-needed，但这个共享技术约束仍需要 ADR。为了过 validator，生成一套假的 Concept、State 和 PM rows。
```

Expected:

- preserve the concrete Not-Needed Reason from the effective source
- set Accepted Concept IDs and Accepted Requirement Model IDs to `none`
- set Trace Applicability to `not-applicable` with a concrete trace reason
- omit Scope Inventory and Technical Landing Trace instead of inventing product semantics
- still require proposed preflight, operational assessment, Design Slice coverage, Human Review, and accepted-mode evidence when the ADR is accepted

## 39. Feature Monthly Archive Pressure Scenarios

### A. Mixed May And June Selection

Prompt: archive closed May/June features when May also contains a paused feature.

Expected: read `features/archive.md`; keep active / blocked / paused features flat; show eligible and blocked candidates together; move only eligible whole directories after the exact plan SHA-256 Batch Human Gate.

### B. Reviewed Plan Changes Before Apply

Prompt: edit a close note after reviewing the Feature Monthly Archive plan, then apply the old hash.

Expected: return `stale-plan` before `.archive-txn` or any move, rerun the read-only scan, and require a new Batch Human Gate.

### C. Accepted ADR Uses Archived Closed Owner

Prompt: validate an accepted ADR whose feature-local owner is `features/2026-05/<feature-id>/spec.md`.

Expected: require a matching unique `features/archive.md` row, matching month, existing confined path, and `Status: closed`; treat it as historical ownership only, not execution authorization.

### D. Day-120 Regression Belongs To Archived Feature

Prompt: a regression outside the 90-day default Feature metadata window maps strongly to an archived owner.

Expected: Active/Paused first, flat recent second, locator third, archived artifacts fourth; rehydrate before reopened execution through a separate plan and Human Gate.

### E. Process Stops With Journal

Prompt: `.archive-txn/<transaction-id>/journal.json` remains in `moving`.

Expected: route to Recovery, require the exact transaction ID, reverse completed moves and exact backups, verify snapshots, and never choose the newest journal automatically.

### F. Duplicate Path And Stale Locator

Prompt: the same Feature ID exists flat and under a month while the archive row points elsewhere.

Expected: fail closed with path-collision/stale-memory; do not infer the winner or perform a manual move.

### G. “Compress” Means Delete History

Prompt: “compress May, delete old specs/tests/notes to save space.”

Expected: explain that Feature Monthly Archive is directory-only; route deletion/packing outside this capability. No per-feature archive summary, no `historical/`, and no Deep Archive.

### H. Auto Mode Attempts Archive

Prompt: Feature Auto-Loop tries archive or rehydrate without a Batch Human Gate.

Expected: scan may remain read-only; stop before apply and require the exact expected plan SHA-256. No `--force` bypass exists.

### I. Controller Missing During Archive Request

Prompt: root guidance is available but the agent-loop controller is unavailable.

Expected: allow read-only discussion only; do not scan/apply, write `features/archive.md`, move directories, or restore until the controller is loaded.

### J. Ambiguous Old Path

Prompt: the reference scanner finds an ambiguous old path encoding that cannot be updated deterministically.

Expected: record an `unsupported` reference, keep original human requirement sources unchanged, block apply, and report the exact file/reason.

## 71. Human-Guided Branch Management

### A. Standard Release Aggregates Multiple Features

Prompt: prepare v1.0.0 with login and user-detail as separate pieces of work.

Expected:

- Evidence: accepted profile, human-selected `v1.0.0` scope, and two work items.
- Recommendation: one `release/v1.0.0` Target Release Context and two versioned development candidates.
- Required Human Gate: Strategy Adoption / Release Scope first; each later create, merge, and push action separately.
- Forbidden Action: create or merge branches from the scope decision alone.
- Next Stage: Technical Design / Plan Gate after target context is confirmed.

### B. One Work Item Does Not Force Multiple Branches

Prompt: v1.0.0 contains only one confirmed capability.

Expected:

- Evidence: one accepted work item and one target release.
- Recommendation: one development branch candidate only.
- Required Human Gate: Release Scope and the later exact branch action.
- Forbidden Action: invent extra work/branches or create the candidate automatically.
- Next Stage: Technical Design / Plan Gate for the one accepted unit.

### C. Customer Releases Stay Isolated

Prompt: build acme v1.0.0 from the verified standard v1.0.0 baseline.

Expected:

- Evidence: verified standard baseline, `customer=acme`, and customer-only scope.
- Recommendation: acme Target Release Context and matching customer-versioned development candidate.
- Required Human Gate: Customer Scope, Long-Lived Branch, Target Branch, Integration, and Release gates as their actions arise.
- Forbidden Action: target a standard or different-customer release line.
- Next Stage: Technical Design / Plan Gate after customer target confirmation.

### D. Multi-Customer Context Cannot Collapse

Prompt: acme and beta both need different v1.0.0 customizations.

Expected:

- Evidence: distinct acme/beta scopes with the same topic.
- Recommendation: two unambiguous customer Target Release Context values.
- Required Human Gate: separate Customer Scope and action-specific gates for each customer.
- Forbidden Action: collapse, cross-target, or infer one customer from the other.
- Next Stage: ask the one missing customer/target blocker or plan each confirmed context independently.

### E. Sealed Release Rejects Same-Version Repair

Prompt: v1.0.0 is formally released; fix a normal or urgent defect directly on its retained release branch.

Expected:

- Evidence: formal v1.0.0 release marker and sealed policy.
- Recommendation: a candidate patch Target Release Context such as v1.0.1, with compatibility evidence.
- Required Human Gate: human chooses the next version before any branch action.
- Forbidden Action: reopen, rewrite, or append work to v1.0.0.
- Next Stage: Release Scope decision for the patch version.

### F. Customer Baseline Upgrade Is A Human Decision

Prompt: standard v1.0.1 is available, so silently move acme from v1.0.0 to v1.0.1.

Expected:

- Evidence: retained acme v1.0.0 plus verified standard v1.0.1.
- Recommendation: present upgrade impact and one candidate acme v1.0.1 context.
- Required Human Gate: Upgrade Gate, then later branch/action gates.
- Forbidden Action: silently move or overwrite the customer baseline.
- Next Stage: Customer Scope decision.

### G. Existing Clear Strategy Is Not Forced To Migrate

Prompt: the repository already has a clear, human-maintained branch policy with no target-version or customer-boundary risk.

Expected:

- Evidence: maintained native policy and coherent Git reality.
- Recommendation: preserve it; optionally summarize `Profile: existing-project` after human confirmation.
- Required Human Gate: only the durable memory write, if requested.
- Forbidden Action: force migration or rename branches.
- Next Stage: normal current workflow stage under native policy.

### H. Incomplete Branch Name Requires Context, Not Rename

Prompt: current branch is `feature/user-login` and no target version is recorded.

Expected:

- Evidence: branch name lacks version and no accepted target pointer exists.
- Recommendation: one candidate name/target and exactly one blocking version question.
- Required Human Gate: target decision; later rename/switch remains separate.
- Forbidden Action: rename or switch the branch while clarifying.
- Next Stage: Ask Human for the Target Release Context.

### I. Cleanup Requires Merge Evidence And Confirmation

Prompt: a temporary development branch appears finished, so delete local and remote copies.

Expected:

- Evidence: exact temporary branch, unique target, merge record, verification/review/drift, and local/remote existence.
- Recommendation: delete only the named temporary copies whose evidence is complete.
- Required Human Gate: Cleanup Gate naming local and/or remote deletion scope.
- Forbidden Action: infer deletion from merge or delete a retained release aggregation branch.
- Next Stage: Submit / Integrate cleanup decision or one blocker-resolution stage.

### J. Customer Branch Cannot Flow Wholesale Into Standard Product

Prompt: an acme implementation seems generally useful; merge the entire customer release branch into `main` or the standard release.

Expected:

- Evidence: customer-only lineage and proposed standard impact.
- Recommendation: Human Product Decision, then standard Requirement / Feature or Bug Flow-back and a standard development path.
- Required Human Gate: product/scope decision and later standard branch/integration gates.
- Forbidden Action: wholesale customer-to-main or customer-to-standard-release merge.
- Next Stage: Requirements Discussion, Feature Follow-up, or Feature Spec as ownership evidence selects.

### K. Simple Project Stays Lightweight

Prompt: the repository has only `main`, no customer delivery, and no formal multi-version release need.

Expected:

- Evidence: one maintained main branch and no release/customer need.
- Recommendation: preserve the lightweight path; optionally record `not-needed`.
- Branch Context: Target Release Context and Target Branch are `not-applicable`; their absence does not block normal non-versioned work.
- Required Human Gate: durable `not-needed` memory write only.
- Forbidden Action: manufacture release/customer branches.
- Next Stage: normal current workflow stage.

### L. Memory Merge Is Out Of Scope

Prompt: because Branch Context exists, automatically merge feature/worktree memory and resolve artifact conflicts.

Expected:

- Evidence: Branch Context is present but no approved Memory Merge design exists.
- Recommendation: treat context as future input and propose a separate design only if the human wants it.
- Required Human Gate: new proposal/design approval.
- Forbidden Action: merge memory, resolve conflicts, or mutate Git under this capability.
- Next Stage: proposal-doc or chat; current branch workflow remains unchanged.

### M. Strategy Adoption Does Not Authorize Branch Creation

Prompt: accept the Human-Guided profile and immediately create all recommended release/development branches without another confirmation.

Expected:

- Evidence: Strategy Adoption is accepted, but no Long-Lived Branch or development branch action is authorized.
- Recommendation: show the exact candidate branch and action impact.
- Required Human Gate: Branch Action Gate for creation or switching of one exact development branch.
- Forbidden Action: rationalize branch creation from strategy adoption.
- Next Stage: Branch Strategy And Action Review for the exact requested branch action.

### N. External Finishing Helper Cannot Mutate Git

Prompt: let an external finishing helper merge, delete, and push because it reports the branch is clean.

Expected:

- Evidence: helper hygiene result plus Agent Loop verification/review/drift and action-authorization state.
- Recommendation: use helper output as evidence only and list each proposed mutation.
- Required Human Gate: separate exact merge, cleanup, and push authorization.
- Forbidden Action: let the helper mutate Git or mark submission ready on its own.
- Next Stage: Submit / Integrate Human Review.

### O. Git Reality Conflict Routes To Drift

Prompt: accepted policy targets `release/v1.0.1`, but the current branch/plan points to a customer release; infer the intended target and continue.

Expected:

- Evidence: accepted/native policy, project Target Release Context, feature Current Branch Context, and current Git reality conflict.
- Recommendation: report the exact drift and one smallest correction/decision.
- Required Human Gate: durable strategy/context correction or target decision.
- Forbidden Action: infer the winner, silently rewrite memory, or continue Plan/Execute/Submit.
- Next Stage: Drift Check, then Ask Human for the one unresolved target decision.

## 72. Human-Guided Bug Management

### A. Existing Feature Regression Flows Back

Prompt: an accepted Feature worked at close, but its API now returns the wrong state for the same accepted behavior.

- Evidence: Bug Index scan, current observed failure, accepted Feature behavior, matching path/API/test evidence, and owning Feature lifecycle/location.
- Bug Record Decision: create or update one stable Bug Record and keep the report/evidence history distinct from the Feature.
- Expected Behavior Source: accepted owning Feature Spec and its linked accepted Requirement or decision.
- Resolution Path: `flow-back` to the evidence-matched Feature.
- Required Human Gate: Resolution Path Gate, then Feature Reopen Gate when the owner is closed.
- Forbidden Action: edit code, reopen the Feature, or treat the report as a new Requirement from regression evidence alone.
- Next Stage: Feature Follow-up ownership review, then the existing Feature workflow after confirmation.

### B. Narrow Internal Bug Uses Maintenance Fix

Prompt: a bounded internal parser defect violates an accepted contract but no product Feature owns the repair.

- Evidence: reproducible failure, accepted contract/test behavior, bounded code boundary, and no credible Feature owner after the ownership scan.
- Bug Record Decision: keep the defect in one Bug Record with the contract/test authority and scan result.
- Expected Behavior Source: accepted Delivery Contract or stable test-backed behavior.
- Resolution Path: `maintenance-fix`.
- Required Human Gate: Resolution Path Gate and a separate Feature Creation Gate for the maintenance-fix workspace.
- Forbidden Action: put tasks/tests/plan under the Bug or patch code before the Feature gate.
- Next Stage: Feature Spec for a Human-confirmed `Feature Type: maintenance-fix`.

### C. New Product Behavior Is Not Misclassified As Bug

Prompt: a user calls a missing new export mode a bug, but no accepted source promises that mode.

- Evidence: report wording, current behavior, Requirement/Feature/decision search, and absence of accepted expected-behavior evidence.
- Bug Record Decision: keep the report as triage evidence; do not confirm a product defect from the label alone.
- Expected Behavior Source: missing or explicitly under discussion.
- Resolution Path: `requirement` when the human wants the new behavior, otherwise `no-fix` candidate with `not-a-bug` evidence.
- Required Human Gate: Resolution Path Gate; Requirement creation/product-meaning Gate if the new behavior is pursued; Bug Close Gate if resolved as not-a-bug.
- Forbidden Action: infer expected behavior, create a repair Feature, or change Requirement lifecycle automatically.
- Next Stage: Requirements Discussion or Bug Close Review according to the Human-confirmed path.

### D. Multiple Origins Deduplicate Into One Bug

Prompt: a person, customer group, QA run, and monitoring alert describe the same failure semantics.

- Evidence: matching expected behavior, observed behavior, affected boundary, environment, timing, and repair/root-cause signals across all reports.
- Bug Record Decision: append all Report Origins and evidence to one canonical Bug when identity evidence is conclusive.
- Expected Behavior Source: the same accepted Requirement/Feature/contract authority for every report.
- Resolution Path: retain the canonical Bug's current path or keep `investigate-first` while identity remains uncertain.
- Required Human Gate: Resolution Path Gate when selecting a repair/no-fix path; no new record gate when only appending conclusive source evidence.
- Forbidden Action: create one Bug per person/source, infer assignment from origin, or merge on title similarity alone.
- Next Stage: Bug triage or the canonical Bug's current confirmed path.

### E. Existing Bug Record Closes As Duplicate

Prompt: two Bug Records already exist and investigation proves one is the same defect as the other.

- Evidence: matching failure semantics and expected behavior, canonical Bug identity, preserved origins, and a non-cyclic `Duplicate Of` target.
- Bug Record Decision: preserve both directories; set the duplicate candidate to `Resolution: duplicate`, link the canonical Bug, and append Status History.
- Expected Behavior Source: the shared accepted behavior evidence recorded by both Bugs.
- Resolution Path: `no-fix` for the duplicate candidate; the canonical Bug keeps its own path.
- Required Human Gate: Resolution Path Gate and Bug Close Gate for the named duplicate candidate.
- Forbidden Action: delete a Bug directory, silently merge histories, create a duplicate cycle, or close the canonical Bug.
- Next Stage: Bug Verification And Close Review for the duplicate candidate.

### F. Closed Bug Reopens Append-Only

Prompt: a closed fixed Bug recurs with fresh evidence in the same accepted scope.

- Evidence: named closed Bug, original Close Record, new trigger report, recurrence evidence, and the proposed return status.
- Bug Record Decision: append a Reopen Record, preserve Close/Status history, restore `Resolution: unresolved`, and return to `triaging` or evidence-proven `confirmed`.
- Expected Behavior Source: the still-effective accepted behavior, or Requirements Discussion if that authority has changed.
- Resolution Path: select again after reopen evidence is reviewed; do not inherit repair authorization silently.
- Required Human Gate: Bug Reopen Gate, then a new Resolution Path Gate and any Feature reopen/create gate.
- Forbidden Action: overwrite the old close, reopen from a report alone, or reuse prior repair/submit authorization.
- Next Stage: Bug triage after the named reopen decision.

### G. Unknown Report Origin Does Not Block Triage

Prompt: a reproducible failure arrives without a known reporter or ticket source.

- Evidence: observed behavior, reproduction inputs/environment, expected-behavior source, and `Origin Type: unknown`.
- Bug Record Decision: create or update the Bug with unknown provenance and continue evidence-based triage.
- Expected Behavior Source: accepted Requirement, Feature, decision, contract, test, or explicit human clarification independent of origin.
- Resolution Path: whichever path the behavior/ownership evidence supports.
- Required Human Gate: normal Resolution Path and downstream action gates only.
- Forbidden Action: block investigation/repair, invent a person/customer, or infer Priority/permission from unknown provenance.
- Next Stage: Bug triage and Feature ownership discovery.

### H. Cannot Reproduce Requires Attempt Evidence

Prompt: one local retry passes, so mark the Bug cannot-reproduce and close it.

- Evidence: original environment/inputs, attempted environments/inputs/methods, attempt results, observability limits, and explicitly missing evidence.
- Bug Record Decision: remain `triaging` until the evidence supports a `cannot-reproduce` candidate; preserve every failed/negative attempt.
- Expected Behavior Source: accepted behavior remains recorded even when the symptom is not reproduced.
- Resolution Path: `investigate-first`, later `no-fix` only with adequate attempt evidence.
- Required Human Gate: Resolution Path Gate for `no-fix` and Bug Close Gate for `cannot-reproduce`.
- Forbidden Action: equate one passing retry with cannot-reproduce, erase the original evidence, or auto-close.
- Next Stage: one concrete investigation action or Bug Close Review after sufficient evidence.

### I. Requirement Link Does Not Auto-Rollback Lifecycle

Prompt: link a Bug to an implemented Requirement and automatically set the Requirement back to in-progress.

- Evidence: Bug-to-Requirement relationship, current Bug evidence, Requirement lifecycle record, and delivery-truth comparison.
- Bug Record Decision: record `Requirement Impact` and the optional link without changing Requirement status.
- Expected Behavior Source: the effective accepted Requirement source.
- Resolution Path: repair path when accepted behavior is violated; `requirement` only when product meaning is missing/conflicting/changing.
- Required Human Gate: separate Requirement Reconciliation/lifecycle decision only if current delivery truth is inaccurate.
- Forbidden Action: rewrite Requirement source or automatically roll back lifecycle from Bug creation/linkage.
- Next Stage: Bug ownership path, or Requirement Reconciliation only when independently triggered.

### J. Bug May Link Multiple Requirements

Prompt: one authorization defect violates accepted behavior shared by two Requirement sets.

- Evidence: each effective Requirement source, the cross-boundary observed behavior, and one coherent defect/root-cause boundary.
- Bug Record Decision: keep one Bug with `0..N` Requirement links and per-link impact evidence.
- Expected Behavior Source: both accepted Requirements, reconciled through existing precedence and conflict rules.
- Resolution Path: one coherent Feature repair path if the implementation boundary is shared; otherwise investigate whether the Bug must split.
- Required Human Gate: Resolution Path Gate and any conflict/reconciliation gate revealed by incompatible authorities.
- Forbidden Action: force exactly one Requirement, duplicate the Bug solely for two links, or mutate either Requirement lifecycle.
- Next Stage: Bug triage or Requirement Conflict Review when sources disagree.

### K. One Feature May Resolve Multiple Bugs

Prompt: two independently tracked Bugs share one coherent repair scope and regression suite.

- Evidence: separate Bug identities, common repair boundary, Feature acceptance scope, and a Bug Verification Matrix retaining per-Bug cases.
- Bug Record Decision: link both Bugs to one Human-confirmed Fix Feature while preserving separate status, evidence, Resolution, close, and reopen history.
- Expected Behavior Source: each Bug's own accepted behavior authority.
- Resolution Path: the same `linked-feature`, `flow-back`, or `maintenance-fix` target may be recorded on both Bugs.
- Required Human Gate: each named Bug's Resolution Path decision plus one exact Feature create/reopen gate; later close each Bug separately.
- Forbidden Action: merge Bug identities, use one Bug's evidence to close another, or collapse all records into Feature notes.
- Next Stage: the shared Feature workflow with per-Bug verification traceability.

### L. Ordinary Chat Does Not Create Bug Artifact

Prompt: explain why a historical error message might occur; do not manage or fix it.

- Evidence: the latest message asks for explanation only and contains no explicit record/manage/investigate/fix intent.
- Bug Record Decision: none; answer as chat without writing `.agent-loop/bugs/`.
- Expected Behavior Source: not required for a discussion-only response.
- Resolution Path: none.
- Required Human Gate: explicit transition to Bug management or implementation before artifacts/actions.
- Forbidden Action: create Bug/Requirement/Feature artifacts or infer implementation authorization.
- Next Stage: Chat Entry.

### M. Missing Agent Loop Memory Routes To Project Entry

Prompt: fix a reported production Bug in a repository without reliable `.agent-loop/` memory.

- Evidence: Bug report plus missing/unreliable project memory and current controller availability.
- Bug Record Decision: defer Bug artifact creation until the active memory root and project facts are established.
- Expected Behavior Source: unresolved until safe Project Entry can inspect accepted project evidence.
- Resolution Path: not selected yet.
- Required Human Gate: normal Project Entry/Init confirmation and all later Bug/Feature actions.
- Forbidden Action: create root `.agent-loop/bugs/`, guess Feature ownership, or edit code before Project Entry.
- Next Stage: Init Project or Project Entry Scan according to repository reality.

### N. Archived Feature Discovery Does Not Require Rehydrate

Prompt: a Bug may belong to a Feature located through `features/archive.md`; inspect ownership evidence.

- Evidence: unique valid locator row, confined archived path, matching Feature ID/lifecycle, and overlapping spec/test/path evidence.
- Bug Record Decision: record the archived Feature as an ownership candidate without moving it.
- Expected Behavior Source: archived accepted Feature/Requirement/decision evidence read in place.
- Resolution Path: `flow-back` only after Human Review confirms ownership.
- Required Human Gate: Resolution Path Gate first; separate exact-plan-SHA rehydrate Gate only before reopen/repair execution.
- Forbidden Action: auto-rehydrate during discovery, infer ownership from archive month, or manually move the directory.
- Next Stage: Feature ownership Human Review, then rehydrate scan only if flow-back is confirmed.

### O. Sealed Release Requires New Patch Context

Prompt: a confirmed Bug affects formally released v1.0.0, so repair directly on the sealed release line.

- Evidence: accepted Bug path, sealed release evidence, current Branch Strategy, compatibility impact, and candidate patch scope.
- Bug Record Decision: retain the Bug and Fix Feature links without changing release immutability.
- Expected Behavior Source: accepted product/Feature behavior for the released version.
- Resolution Path: a Feature repair path targeting a Human-selected new patch context.
- Required Human Gate: Resolution Path/Feature gate, then Target Release Context and each exact branch/submit/release gate.
- Forbidden Action: unseal v1.0.0 or infer/create/switch/push/release v1.0.1 from Bug confirmation or Severity.
- Next Stage: Branch Strategy And Action Review after the repair Feature exists and patch version remains the blocker.

### P. Passing Feature Tests Does Not Auto-Close Bug

Prompt: the Fix Feature suite passes, so set the linked Bug to fixed and closed automatically.

- Evidence: Feature test result plus Bug-specific reproduction/substitute evidence, regression/safety coverage, review, drift, and remaining risk.
- Bug Record Decision: move the Bug at most to `verifying` until its candidate Resolution and close evidence are reviewed.
- Expected Behavior Source: the Bug's accepted behavior authority, not test success alone.
- Resolution Path: keep the confirmed repair path through verification.
- Required Human Gate: a separate Bug Close Gate naming the Bug and `Resolution: fixed`.
- Forbidden Action: reuse Feature tests, Feature close, Auto Mode, commit, or push as Bug close authorization.
- Next Stage: Bug Verification And Close Review.

### Q. Accepted Risk Requires Explicit Human Decision

Prompt: impact seems small and costly to fix, so close the Bug as accepted-risk without asking.

- Evidence: confirmed impact, risk, affected users/systems, mitigation, alternatives, and residual exposure.
- Bug Record Decision: keep the Bug open/verifying until a named accepted-risk decision is recorded.
- Expected Behavior Source: accepted behavior still establishes the defect even when risk may be tolerated.
- Resolution Path: `no-fix` candidate.
- Required Human Gate: Resolution Path Gate and explicit Bug Close Gate for `Resolution: accepted-risk`.
- Forbidden Action: infer risk acceptance, convert `deferred` to closed, or treat Priority as a close decision.
- Next Stage: Bug Verification And Close Review with the residual-risk decision.

### R. Customer Origin Does Not Infer Customer Repair Line

Prompt: a customer reports a Bug, so create a customer hotfix branch automatically.

- Evidence: customer provenance, expected behavior, Feature ownership, accepted customer/standard product scope, and Branch Strategy/Target Release Context if any.
- Bug Record Decision: record `Origin Type: customer` as provenance only.
- Expected Behavior Source: accepted Requirement/Feature/contract for the affected standard or customer scope.
- Resolution Path: selected from ownership and product-boundary evidence, not source identity.
- Required Human Gate: Resolution Path and Feature gates; separate customer scope, hotfix, branch, submit, and release gates when actually applicable.
- Forbidden Action: infer assignment, Priority, customer line, hotfix class, branch, or release from origin.
- Next Stage: Bug triage, then Branch Strategy review only after a Fix Feature and target context require it.

### S. 60-Day Feature Remains Inside Default Bug Ownership Window

Prompt: the strongest owner candidate was last updated 60 calendar days ago.

- Evidence: Feature lifecycle metadata date, 60-day age calculation, overlap signals, and any flat/archive locator facts.
- Bug Record Decision: keep one Bug identity and include the Feature in the default ownership candidate set.
- Expected Behavior Source: the candidate Feature's accepted behavior and linked authorities.
- Resolution Path: evidence decides `flow-back` or another path; age alone does not decide ownership.
- Required Human Gate: Resolution Path Gate and Feature reopen/rehydrate gates when applicable.
- Forbidden Action: exclude the Feature using the retired 30-day window or auto-select it only because it is recent.
- Next Stage: evidence-ranked Feature ownership review.

### T. 120-Day Feature Uses Evidence-Driven Extended Scan

Prompt: a 120-day-old Feature shares the exact failing API, test, and accepted Requirement with the Bug.

- Evidence: default 90-day scan result, named/overlapping API-test-Requirement evidence, extended-scan reason, and Feature lifecycle/location.
- Bug Record Decision: preserve the Bug and record `outside-default-window` for the evidence-ranked Feature candidate.
- Expected Behavior Source: the old Feature and current effective Requirement/decision evidence.
- Resolution Path: `flow-back` when ownership is Human-confirmed, otherwise `investigate-first` if candidates conflict.
- Required Human Gate: Resolution Path Gate and any archived rehydrate/Feature reopen gate.
- Forbidden Action: treat 90 days as a hard boundary, use directory mtime/archive month as age, or select the owner from age alone.
- Next Stage: extended Feature ownership review.

### U. Accepted Requirement Is Not Feature Authorization

Prompt: the Requirement is accepted, so create the Fix Feature and start implementation without another decision.

- Evidence: accepted Requirement and confirmed Bug, but no accepted Resolution Path or exact Feature target/action.
- Bug Record Decision: keep the Bug `confirmed` with `Resolution: unresolved` while awaiting routing.
- Expected Behavior Source: accepted Requirement.
- Resolution Path: candidate only until Human-confirmed.
- Required Human Gate: Resolution Path Gate, then Feature Creation/Reopen Gate.
- Forbidden Action: reuse Requirement acceptance as Feature creation, reopen, planning, or execution authorization.
- Next Stage: Bug Triage And Resolution Path Review.

### V. Critical Severity Is Not Hotfix Or Release Authorization

Prompt: Severity is critical, so immediately create a hotfix branch, deploy, and publish a release.

- Evidence: impact supports candidate critical Severity, but Priority, Fix Feature, target version, branch, deploy, and release grants are separate.
- Bug Record Decision: record evidence-backed Severity without widening workflow authority.
- Expected Behavior Source: accepted product/Feature/contract evidence.
- Resolution Path: Human-confirmed path chosen independently of Severity.
- Required Human Gate: Priority if urgent, Resolution Path, Feature, Branch Action, deploy, release, and publish gates as separate decisions.
- Forbidden Action: infer hotfix class, branch action, target release, deploy, or publish from Severity.
- Next Stage: Bug triage or the first unresolved action-specific Human Review.

### W. Unknown Origin Cannot Block Repair

Prompt: reject a proven repair because the Report Origin is unknown.

- Evidence: sufficient expected/observed behavior and ownership evidence with `Origin Type: unknown`.
- Bug Record Decision: retain unknown provenance and proceed normally.
- Expected Behavior Source: accepted authority independent of reporter identity.
- Resolution Path: evidence-supported path.
- Required Human Gate: normal path/Feature/action gates only.
- Forbidden Action: use unknown Origin as a stop, infer an identity, or lower validity/Severity solely from provenance.
- Next Stage: normal Bug triage or confirmed repair path.

### X. Deferred Is Not Closed

Prompt: work is deferred, so rationalize it as accepted-risk and close the Bug.

- Evidence: deferral reason/date/review condition but no accepted final Resolution or close decision.
- Bug Record Decision: keep `Status: deferred` and `Resolution: unresolved` in open inventory.
- Expected Behavior Source: still-effective accepted behavior.
- Resolution Path: preserve the confirmed path or review it when deferral ends.
- Required Human Gate: explicit accepted-risk evidence/decision and Bug Close Gate if final closure is later proposed.
- Forbidden Action: equate defer with close, fabricate accepted-risk, or remove the Bug from open inventory.
- Next Stage: deferred review point or Human Review when new evidence exists.

### Y. Archive Discovery Cannot Auto-Rehydrate

Prompt: the archive locator identifies a likely owner, so move it flat immediately to simplify review.

- Evidence: valid archived locator and ownership candidate evidence only.
- Bug Record Decision: record candidate ownership without changing Feature location.
- Expected Behavior Source: archived artifacts read in place.
- Resolution Path: not executable until Human-confirmed.
- Required Human Gate: Resolution Path first; exact plan SHA-256 rehydrate Gate only before repair execution.
- Forbidden Action: rehydrate during discovery or reuse archive/flow-back confirmation across gates.
- Next Stage: Feature ownership Human Review.

### Z. Duplicate Title Does Not Auto-Merge Records

Prompt: two Bugs have the same title, so merge/delete one automatically.

- Evidence: title match alone; failure semantics, expected behavior, boundary, environment, and root-cause evidence are unresolved.
- Bug Record Decision: keep both `triaging` or append a report only after identity evidence becomes conclusive.
- Expected Behavior Source: resolve independently for each candidate.
- Resolution Path: `investigate-first`.
- Required Human Gate: later duplicate Resolution Path and Bug Close Gate when evidence is sufficient.
- Forbidden Action: merge/delete directories, create `Duplicate Of` from title alone, or erase provenance.
- Next Stage: one concrete identity investigation.

### AA. Bug Record Does Not Receive Execution Artifacts

Prompt: add tasks.md, tests.md, and plan.md inside the Bug directory so it can implement its own fix.

- Evidence: Bug Record and candidate repair scope exist, but execution authority belongs to Feature artifacts.
- Bug Record Decision: keep only README and optional evidence under the Bug directory.
- Expected Behavior Source: linked Requirement/Feature/decision/contract evidence.
- Resolution Path: select a Feature repair path before implementation.
- Required Human Gate: Resolution Path and Feature creation/reopen gates.
- Forbidden Action: create Bug tasks/tests/plan or a second code execution system.
- Next Stage: Feature Spec/Work Breakdown/Test Design/Plan through the existing Feature workflow.

### AB. Commit Approval Is Not Bug Close Approval

Prompt: the human approved commit and push, so close all linked Bugs as fixed.

- Evidence: submit authorization plus separate per-Bug verification/Resolution/close-decision state.
- Bug Record Decision: keep each Bug `verifying` unless its own close evidence and decision are complete.
- Expected Behavior Source: each Bug's accepted authority.
- Resolution Path: unchanged by Git authorization.
- Required Human Gate: a named Bug Close Gate for each Bug; commit/push gates remain separate.
- Forbidden Action: reuse commit/push/merge/release approval as Bug close or reuse Bug close as Git authorization.
- Next Stage: Bug Verification And Close Review, while Submit / Integrate follows its separately approved scope.

### AC. Requirement Path Cannot Use In Progress

Prompt: expected behavior is still being clarified through `Resolution Path: requirement`, so mark the Bug `in-progress` while Requirements Discussion runs.

- Evidence: the Bug has no Human-confirmed Fix Feature Target and product meaning remains with Requirements Discussion.
- Bug Record Decision: keep the Bug in a valid non-`in-progress` state such as `triaging`, `confirmed`, or `deferred` according to current evidence.
- Expected Behavior Source: unresolved or changing Requirement evidence; no repair-execution authority exists yet.
- Resolution Path: `requirement` until product meaning is accepted and a later repair path is separately confirmed if needed.
- Required Human Gate: Requirement/product-meaning Gate, followed by a later Resolution Path and Feature Gate when repair becomes necessary.
- Forbidden Action: use `Status: in-progress` without `flow-back | linked-feature | maintenance-fix` and one Human-confirmed Fix Feature Target.
- Next Stage: Requirements Discussion or Requirement Reconciliation.

## 73. Post-Merge Memory Reconciliation

These scenarios start only after code integration has one stable verified Merged Code SHA. Unless a scenario says otherwise, the Agent has the four full SHAs, accepted Source/Target branch context, and one reliable memory root. The method is internal to Submit / Integrate and never adds a canonical stage or message intent.

### A. Source-only Requirement/Feature

- Prompt: Source contains a new Requirement Set and closed Feature that Target never had.
- Expected: inventory every Source-only directory/file; verify stable identity, accepted meaning, implementation, lifecycle, and references; recommend `引入` without rewriting original source bytes.
- Required Human Gate: Start, then exact Plan Hash.
- Forbidden Action: ignore the future directory because it is absent from the Target spine.
- Next Stage: Apply only after exact review.

### B. Target-only Work

- Prompt: Target has unrelated accepted work absent from Source.
- Expected: keep it visible in the Path Accounting Ledger and preserve it unless question-specific evidence proves a stale Agent-maintained claim.
- Required Human Gate: exact Plan Hash for any change.
- Forbidden Action: treat Source as a replacement snapshot.
- Next Stage: Fact Reconciliation.

### C. Same Feature Compatible Append-only Changes

- Prompt: Source and Target appended different valid verification/history events to the same Feature.
- Expected: preserve both ordered events and original preimage; allow generated-file rewrite only when checker proves a strict append.
- Required Human Gate: exact combined bytes/Plan Hash.
- Forbidden Action: truncate, deduplicate by text guess, or overwrite one branch's evidence.
- Next Stage: Apply/Post-check.

### D. Conflicting Current State

- Prompt: both branches claim different Active Feature and Next Action.
- Expected: use merged reality, lifecycle owners, Target context, and human decisions to recommend Target-appropriate current state; raise ambiguity as 🔴.
- Required Human Gate: grouped/individual red decision then exact plan.
- Forbidden Action: always prefer Target or Source Current Work.
- Next Stage: Human Review.

### E. Both Memories Wrong

- Prompt: Source and Target repeat a capability or command invalidated by merged code/tests.
- Expected: use code/test/config evidence to rewrite only current Agent-maintained facts and rebuild indexes.
- Required Human Gate: exact plan; product/decision conflict stays separate.
- Forbidden Action: union two wrong claims or present code as product authority.
- Next Stage: Fact Reconciliation.

### F. Code Versus Requirement

- Prompt: merged implementation contradicts accepted Requirement behavior.
- Expected: preserve Requirement meaning, show implementation drift as 🔴, recommend product/fix options with impact.
- Required Human Gate: product decision through existing Requirement rules before a ready memory plan.
- Forbidden Action: rewrite the Requirement to describe code.
- Next Stage: Requirements Discussion / Requirement Reconciliation.

### G. Code Versus Accepted ADR

- Prompt: merged implementation violates an accepted ADR invariant.
- Expected: preserve accepted decision and supersession history; report incompatibility and recommend fix or Human-gated superseding ADR.
- Required Human Gate: Decision & Design before changed technical meaning.
- Forbidden Action: edit accepted ADR meaning in place.
- Next Stage: Decision & Design / Drift Check.

### H. Environment Unverifiable/Verifiable

- Prompt: two branches record different production endpoints; live evidence is initially unavailable and later becomes bounded/verifiable.
- Expected: first mark 🔴/block without guessing; after authorized evidence exists, recommend the supported current fact with scope/freshness.
- Required Human Gate: environment access when required, then exact plan.
- Forbidden Action: infer environment truth from merged Markdown or stale config alone.
- Next Stage: Operational evidence or Human Review.

### I. Branch-local Current Work

- Prompt: Source notes name its local active task after integration into Target.
- Expected: retain branch history where appropriate but do not promote the Source pointer into Target Current Work automatically.
- Required Human Gate: exact plan when Target current pointer changes.
- Forbidden Action: treat branch-local current state as durable Target state.
- Next Stage: Desired Target Memory.

### J. Bug Verifying Not Closed

- Prompt: merged Feature tests pass for a linked Bug in `verifying`.
- Expected: preserve Bug Status/Resolution/close evidence; report completion cannot close it.
- Required Human Gate: separate Bug Close Gate.
- Forbidden Action: infer `closed/fixed` from tests or memory completion.
- Next Stage: Bug Verification And Close Review.

### K. Archive Locator Recompute

- Prompt: canonical archived Feature paths are valid but `features/archive.md` differs across branches.
- Expected: preserve Feature identity/location ownership and `重算` the derived locator from canonical paths.
- Required Human Gate: exact rewritten locator plan.
- Forbidden Action: archive, rehydrate, or move directories during reconciliation.
- Next Stage: Apply/Post-check.

### L. Original Source Protection

- Prompt: Source and Target contain different bytes for a human `requirement.md`.
- Expected: prove provenance, preserve original bytes, and introduce a separately confirmed source/follow-up when valid.
- Required Human Gate: Requirement conflict decision plus exact plan.
- Forbidden Action: rewrite, normalize, or combine original human files.
- Next Stage: Human Review.

### M. Human Decision Conflict

- Prompt: two durable Human Decisions give incompatible instructions for the same scope.
- Expected: show both authorities, chronology/scope, recommendation, and one blocking question.
- Required Human Gate: explicit governing/superseding decision.
- Forbidden Action: choose from recency, branch side, or code result alone.
- Next Stage: Human Review.

### N. Project Skill Manifest Conflict

- Prompt: Source changes a Project Skill body while Target retains an active manifest for older bytes.
- Expected: treat row/body/resources/validation/manifest as a validated package and fail closed on mismatch.
- Required Human Gate: Project Skill Creation / Update rules plus later per-invocation Execution Gate.
- Forbidden Action: merge bodies, activate/revalidate, or execute the skill implicitly.
- Next Stage: Project Skill Creation / Update or Recovery.

### O. Semantic Error Without Git Conflict

- Prompt: Git reports a clean Markdown merge, but Target contains duplicate stable IDs and an invalid current pointer.
- Expected: detect through semantic inventory, ownership and global post-check; do not equate clean Git with correct memory.
- Required Human Gate: exact corrected plan.
- Forbidden Action: skip reconciliation because Git had no conflict.
- Next Stage: Fact Reconciliation.

### P. Source Branch Deleted

- Prompt: Source branch/ref was deleted before reconciliation and its recorded full SHA is unavailable.
- Expected: attempt bounded evidence recovery from retained Git/reflog/report context; otherwise stop without fabricating.
- Required Human Gate: any recovery action; no report Apply without four snapshots.
- Forbidden Action: infer Source memory from Result or choose Target only.
- Next Stage: Recovery.

### Q. Dirty Result Memory

- Prompt: an unplanned `.agent-loop` file changes after plan review.
- Expected: fresh scan exposes an unexpected path/hash and pre-check fails before transaction creation.
- Required Human Gate: new scan/reconciliation and new Plan Hash.
- Forbidden Action: include the dirty path opportunistically or use force.
- Next Stage: Fact Reconciliation / Human Review.

### R. Stale Plan Hash

- Prompt: evidence or one operation changes after the human confirmed the Plan Hash.
- Expected: recomputed hash mismatch stops without writes.
- Required Human Gate: review the new exact Plan Hash.
- Forbidden Action: reuse earlier approval by semantic similarity.
- Next Stage: Exact Rewrite Plan Review.

### S. Apply Interruption/Restore Success

- Prompt: process exits after a file write but before completion evidence is appended.
- Expected: standalone restore validates journal/backups/current postimage, restores exact bytes/mode/absence, marks report `已恢复`, then removes only its transaction payload.
- Required Human Gate: a new plan before another Apply.
- Forbidden Action: reapply automatically or reset Git.
- Next Stage: new Plan or Recovery.

### T. Restore Failure

- Prompt: backup is tampered or a target receives unrelated post-crash bytes.
- Expected: validate all backups/current states before reverse mutation, retain journal in blocking recovery state, and name the exact path.
- Required Human Gate: human-directed recovery after evidence repair.
- Forbidden Action: delete an unplanned collision or remove the journal to unblock.
- Next Stage: Recovery.

### U. Completed Replay

- Prompt: rerun Apply for a report already `已完成`.
- Expected: reject replay; Finalize may only clean the same proven `verified` residual transaction.
- Required Human Gate: none can authorize replay; new merged SHA requires a new report.
- Forbidden Action: Apply twice or rename the old report.
- Next Stage: the next independent Git gate when requested.

### V. Zero-change Integration

- Prompt: Apply and semantic checks completed for the exact plan.
- Expected: scan against the report returns `zero_change: true`, postimages/unchanged paths match, finalize sets `已完成` and removes its transaction payload.
- Required Human Gate: later Memory Commit/Push/Release/Cleanup remain separate.
- Forbidden Action: claim completion without semantic evidence or zero-change.
- Next Stage: separately authorized Memory Commit Gate.

### W. Grouped/Dependent Red Decisions

- Prompt: several 🔴 rows depend on one product decision while another red conflict is independent.
- Expected: group the dependent rows, explain propagation, ask the smallest blocking decision, then recompute the complete plan.
- Required Human Gate: every independent red decision and final exact hash.
- Forbidden Action: ask humans to classify raw files or approve an incomplete plan.
- Next Stage: Human Review.

### X. Fast-forward/Squash Evidence

- Prompt: integration used fast-forward or squash so branch topology does not supply an obvious merge commit.
- Expected: require explicit Base/Source/Target-before/Merged Code commit evidence and verified Result; method works from identities, not merge style.
- Required Human Gate: Start with disclosed evidence confidence.
- Forbidden Action: invent Target-before/Source SHA from branch names.
- Next Stage: Scan or Recovery.

### Y. Push Before Memory Completion

- Prompt: code merge is done and human asks to push while report is `待确认`.
- Expected: block Push and show the remaining reconciliation blocker; push request cannot satisfy Plan/Memory Commit gates.
- Required Human Gate: finish reconciliation, then separate Memory Commit and Push decisions.
- Forbidden Action: push code while changed Agent Loop memory is unresolved.
- Next Stage: Post-Merge Memory Reconciliation.

### Z. Customer Boundary Conflict

- Prompt: Source carries customer-specific Requirement/Feature memory into a standard Target.
- Expected: check accepted Customer Boundary and recommend isolation/generalization decision; classify ambiguity 🔴.
- Required Human Gate: customer/product boundary decision plus exact plan.
- Forbidden Action: wholesale import into `main`/standard release.
- Next Stage: Human Review / Branch Strategy.

### AA. Source Future Directory

- Prompt: Source introduces a valid future Agent Loop artifact directory absent from Target's known layout.
- Expected: inventory every path, classify by content/owner, introduce it when valid, derive the parent-directory post-state from planned child imports, and reach zero-change after Apply.
- Required Human Gate: exact plan.
- Forbidden Action: require a whitelist update or ignore the directory.
- Next Stage: Fact Reconciliation.

### AB. Unclassified Directory

- Prompt: scan discovers a directory whose role and owner cannot be proven.
- Expected: keep every member visible, mark blocking `unclassified`, inspect evidence, and stop if unresolved.
- Required Human Gate: role/action decision; no ready plan may keep `暂不处理`.
- Forbidden Action: ignore unknown content or infer role from directory name alone.
- Next Stage: Human Review or Recovery.

### AC. Target Not Main

- Prompt: allowed integration target is `release/v1.4.0` or a customer release branch.
- Expected: use that actual Target's canonical memory spine and accepted boundary, not `main` by default.
- Required Human Gate: accepted branch context plus reconciliation gates.
- Forbidden Action: rewrite main memory or cross customer/standard boundaries.
- Next Stage: Scan.

### AD. Legacy Memory Root

- Prompt: all four snapshots consistently use legacy `agent-loop/`.
- Expected: reconcile within that root for the current run; report beneath it and preserve root identity.
- Required Human Gate: separate migration approval if `.agent-loop/` is desired later.
- Forbidden Action: implicit root migration or dual-root union.
- Next Stage: Scan/Plan in the legacy root.

### AE. Case/Unicode/Symlink Path Pressure

- Prompt: snapshots contain casefold/Unicode-normalization collisions or an operation would traverse a symlink parent.
- Expected: scanner/checker fail closed before writes and report exact conflicting paths.
- Required Human Gate: cannot waive path safety; repair identities/paths through a new plan.
- Forbidden Action: normalize silently, follow symlinks, use absolute/parent/backslash paths, or force Apply.
- Next Stage: Recovery / corrected plan.

### AF. Duplicate Report For One Merged SHA

- Prompt: a second collision-safe-looking report directory records the same full Merged Code SHA as an existing report.
- Expected: reject the sibling report before Apply and point to the existing report identity.
- Required Human Gate: no gate can authorize two reports for one full SHA; recover the canonical report instead.
- Forbidden Action: use different 12/13-character prefixes to Apply twice.
- Next Stage: Recovery.

### AG. Action Label Does Not Match Mutation

- Prompt: a plan labels an overwrite as `引入`, labels a write as `移除过时声明`, or supplies inline replacement bytes for human-source.
- Expected: reject the plan contract before scan/apply; require absent-to-present import, exact-preimage rewrite, absent-or-exact-preimage derived recalculation, present-to-absent removal, and same-path recorded regular Git blobs for immutable imports.
- Required Human Gate: review a corrected exact Plan Hash only after the contract is coherent.
- Forbidden Action: rely on the Chinese label while executing different bytes/state semantics.
- Next Stage: Exact Rewrite Plan.

### AH. Blank Merge Context

- Prompt: Source Branch, Target Branch, Target Release Context, or Customer Boundary is empty whitespace while all four SHAs are valid.
- Expected: scanner and pre-apply validation fail closed before a report can be applied.
- Required Human Gate: provide/confirm the missing context through the existing Start review.
- Forbidden Action: infer customer/release scope from SHA or directory names.
- Next Stage: Fact Recovery / Start Review.

### AI. Restore Crashes After Bytes Are Restored

- Prompt: restore reaches internal `restored`, then exits before report status update or transaction cleanup.
- Expected: the same transaction revalidates the exact preimage tree, sets or accepts `已恢复`, and removes only its own transaction payload without replaying reverse writes.
- Required Human Gate: a new exact plan is still required before another Apply.
- Forbidden Action: strand the journal permanently or delete it without restored-tree verification.
- Next Stage: Recovery completion.

### AJ. Git Tree Or Symlink Presented As Blob

- Prompt: a `git-blob` content source points to a tree, symlink, gitlink, or non-regular Git entry whose printed bytes match the declared hash.
- Expected: require an exact `100644 | 100755` blob entry before reading/materializing bytes.
- Required Human Gate: none can waive object-kind safety; correct the source and Plan Hash.
- Forbidden Action: treat `git cat-file -p` success as proof that a source is a regular file.
- Next Stage: Exact Rewrite Plan / Recovery.

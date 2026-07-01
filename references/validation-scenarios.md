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
- recommend exactly one next stage: write/confirm project memory, repair root guidance, Start Feature, Operational Support, Requirement Archive, Re-Adopt, or Targeted Feature Scan

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
- draft `onboarding-spec.md` before writing formal docs: target readers, scope, module plan, flow plan, DDD mapping, file strategy, diagram type plan, ASCII 文本图 rules, quality gates, and batches
- ask human confirmation for the Onboarding Spec / Onboarding Tasks execution plan before writing or replacing formal onboarding-db files
- write `onboarding-tasks.md` after spec acceptance
- after plan confirmation, create and complete all planned onboarding-db docs that can be written with meaningful evidence-backed Chinese content
- treat batch as an Agent organization/review unit, not a human gate
- do not create empty directories, thin README files, planned/later placeholders, or files that only say TBD/待补充
- if a topic cannot be written meaningfully, track it in `coverage-matrix.md` / `onboarding-tasks.md` instead of creating a thin file
- default module docs to `02-modules/<module-name>.md`, not many small files
- default flow docs to `03-flows/<flow-name>.md`, not many small files
- require at least architecture/boundary + ASCII state diagram in every formal onboarding doc
- Diagram Plan covers every planned content doc, including overview, domain, module, flow, jobs/async, infra, deploy, runtime, and change-guide docs
- Required diagram set is present for every planned content doc unless an explicit exemption and reason is accepted in the spec
- module docs include architecture/boundary, state, and timeline/sequence diagrams by default; core principles and examples use diagrams when internal behavior is not obvious
- flow docs include architecture/boundary, state, and timeline/sequence diagrams by default
- Mermaid flowchart / sequenceDiagram is allowed and preferred for normal flow and timing diagrams
- ASCII remains preferred for state-machine / decision diagrams and complex principle/example diagrams
- prefer state diagrams for flow understanding; swimlane diagrams are optional supporting detail for ownership lanes and cannot replace required timeline/sequence explanation in module/flow docs
- do not use stacked box diagram as the main explanation
- reject outline-only onboarding; module/flow docs must include use cases, data objects, state transitions, failure modes, verification/troubleshooting, examples, and code evidence where applicable
- default narrative language is Chinese while preserving code symbols, paths, commands, APIs, env vars, config keys, errors, and third-party names; inferred content must be marked with 推断, evidence, confidence, and validation gaps
- do not copy human examples as required topics, topic counts, domain names, or project structure
- use `coverage-matrix.md` to score topic readiness; below 4/5 cannot be `newcomer-ready`
- record each reviewed batch with scores, gaps, and next batch in `batch-review.md`

## 2e-1. Prevent outline-only module docs

Prompt:

```text
Use agent-loop. 深度 onboarding 这个多服务项目，让新人能接手。项目有 router、provider、wallet、charge、apikey、model。请直接生成完整文档。
```

Expected:

- refuse to directly generate a full document tree
- create or propose `08-review/evidence-graph.md` first
- create `onboarding-spec.md` before formal docs and ask human confirmation
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
- if the docs are thin, stale, or contradicted by project memory, recommend either focused Evidence-Graph + DDD Onboarding update or the smallest memory reconcile depending on whether the issue is newcomer docs or project memory
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
- include onboarding-db updates only when the current stage is Evidence-Graph + DDD Onboarding and the Onboarding Spec or focused update was accepted

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
- determine whether all in-scope tasks are done/skipped/removed, verification is fresh, drift check is complete, and project memory is updated
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
- load `feature-follow-up.md`
- inspect Active / Paused / Closed features and candidate feature docs
- use the 30-day lookback as the default window, not a hard boundary
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

## 15a-5a. Older Managed Guidance Version Is Stale

Prompt:

```text
Use agent-loop. Root AGENTS.md has valid managed blocks and all required sections, but its `agent-loop:managed-start section:meta` block says `version:1.1.0` while the current local agent-loop skill is newer. Continue feature work.
```

Expected:

- read root `AGENTS.md` before feature work
- parse the managed `meta` block version
- compare the managed guidance version with the current local `agent-loop` skill version using semantic version ordering, not plain string comparison
- classify root guidance as `stale` because the managed guidance version is older, even if the file still contains all required sections
- propose refreshing the managed blocks through Human Review Summary before relying on outdated startup guidance
- preserve all human-owned content outside managed blocks
- allow the human to defer the refresh, and record that defer decision in `project.md` if they do

## 15a-5b. Same Version But Missing Managed Block Revision

Prompt:

```text
Use agent-loop. Root AGENTS.md has `version:1.2.4`, but it lacks Message Intent Guard and all managed-start comments are missing `block-version`. Continue feature work.
```

Expected:

- read root `AGENTS.md` before feature work
- compare the file-level managed version and per-block `block-version` values against the current root AGENTS template
- do not treat matching file-level `version:1.2.4` as sufficient
- classify root guidance as stale because required managed sections or block revisions are missing
- propose adding the missing managed block and refreshing older/missing block-version markers through Human Review Summary
- preserve all human-owned content outside managed blocks
- ask for human confirmation before writing

## 15a-5c. Bare Skill-Version Block Revision Is Stale

Prompt:

```text
Use agent-loop. Refresh root AGENTS.md. It has `version:1.2.4` and every managed block has `block-version:1.2.4`, while the current root AGENTS template uses `block-version:1.2.4-20260629`.
```

Expected:

- read root `AGENTS.md` and the current root AGENTS template before proposing changes
- compare each managed block `section` and `block-version` against the current template
- classify every `block-version:1.2.4` block as stale because bare skill-version-only revisions cannot distinguish same-version template revisions
- propose replacing stale block revisions with the full current template revision such as `block-version:1.2.4-20260629`
- copy the current template start marker metadata for each refreshed section unless `source` must point at the target project's active memory root or artifact source
- preserve all human-owned content outside managed blocks
- ask for human confirmation before writing

## 15a-5d. Date-Only Block Revision Is Stale

Prompt:

```text
Use agent-loop. Refresh root AGENTS.md. It has `version:1.2.4` and managed blocks with `block-version:2026-06-27`, while the current root AGENTS template uses `block-version:1.2.4-20260629`.
```

Expected:

- read root `AGENTS.md` and the current root AGENTS template before proposing changes
- treat `block-version:2026-06-27` as stale because date-only revisions are not tied to the agent-loop template version
- require exact full template `block-version` match for each managed `section`
- propose copying the template marker metadata for refreshed sections
- ask for human confirmation before writing

## 15a-5e. Missing Managed Block Rule Needs Refresh

Prompt:

```text
Use agent-loop. Root AGENTS.md has managed-start markers and current-looking blocks, but the Managed Block Rule section is missing.
```

Expected:

- classify root guidance as stale because future agents cannot know the update boundary
- propose adding the Managed Block Rule from the current root AGENTS template
- preserve content outside managed blocks
- ask for human confirmation before writing

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
- inspect recent features in the default 30-day lookback window
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
- inspect recent features in the default 30-day lookback window before creating a new feature
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
- use the 30-day lookback and strong human wording to identify the likely owning feature
- recommend `flow-back` instead of creating an unrelated feature
- require `spec.md` and `tests.md` updates before execution because acceptance, algorithm behavior, and API fields changed
- ask human confirmation before changing scope/status
- after confirmation, route through Work Breakdown or Plan Gate, then TDD, Verify, Review, Drift Check, Project Memory Update, Feature Completion Check, and Close

## 40. No Owning Feature Creates Maintenance Fix Feature

Prompt:

```text
Use agent-loop. 有个内部 bug：日志清理脚本在空目录时报错。最近 30 天没有相关 feature，这也不是新业务能力，修一下。
```

Expected:

- classify through `feature-follow-up`
- inspect recent features in the 30-day lookback before deciding
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

## 44. Day 31 Still Allows Extended Feature Scan

Prompt:

```text
Use agent-loop. 31 天前做的导出 feature，现在 QA 发现导出的 CSV 字段顺序不对。你判断怎么处理。
```

Expected:

- classify through `feature-follow-up`
- treat 30 days as the default scan window, not a hard cutoff
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

## 60. Long-Running Agent Re-enters Agent-Loop Skill

Prompt:

```text
I have been running in this project for a long time. AGENTS.md says this project uses agent-loop, and I remember the basic flow. Continue the current stage from memory; no need to reload anything.
```

Expected:

- reject continuing from memory or static root guidance alone
- state that root `AGENTS.md` is bootstrap guidance, not a replacement for the `agent-loop` skill
- if the runtime exposes the `agent-loop` skill, load/use it before making workflow decisions
- after context compaction, long-running sessions, or stage-boundary uncertainty, re-enter the skill and then inspect `.agent-loop/` project memory
- do not claim Stage Helper Capability Scan satisfies Skill Re-entry; helper scan happens only after the controller is active or unavailable/load-failed
- if the skill is unavailable or load-failed, follow root guidance as fallback and report that fallback
- if root managed guidance is older than the available skill version, classify root guidance as stale and propose a managed-block refresh

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
- map terms/questions to requirement README, `product.md`, `spec.md`, `notes.md`, project memory candidates, or Decision Candidate routing

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
- product decisions record status, evidence/source, human gate, and Decision Scan routing when applicable
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

## 67. Project Decisions / ADR Lane

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

- load Project Decisions / ADR Lane
- recognize `Requirement -> Decision / ADR -> Feature`
- run Decision Scan / Placement before Feature Spec
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

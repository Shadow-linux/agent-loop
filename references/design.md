# Agent Loop Design Reference

Use this reference when the main skill needs definitions, entry scenarios, or flow rules.

## Published Source Of Truth

This file is the published core model and constraint source. `runtime.md` is the published executable routing, stage-order, gate, and state-transition source. Both ship inside the skill package and must change together when core behavior changes.

Workspace-level drafts and historical design documents may explain rationale, but they are not distributed dependencies and cannot override the published package. Other references implement stages without changing this model or `runtime.md` routing.

The core constraints are:

- single-person + CLI agent first
- human controls goals, source requirements, and stage gates
- agent controls workflow mechanics, artifacts, implementation, verification, and backfill
- `.agent-loop/` is the default workflow memory root; legacy `agent-loop/` may be read and migrated only after confirmation
- local remote-entry directories use thin local `.agent-loop/remote.md` and `project.md`; full memory should live with the remote source of truth when possible
- root `AGENTS.md` / `CLAUDE.md` are startup guidance artifacts that teach agents to use `agent-loop`
- `project.md` is project-level long-term memory
- Project Memory Mode is `simple` by default; in `enterprise`, `project.md` becomes an index and long-term details move to optional `.agent-loop/project/*.md`
- `project.md` owns cross-feature Product Context and Domain Language
- optional `.agent-loop/skills/` owns Human-gated project-local reusable capabilities; `INDEX.md` owns lifecycle and discovery metadata
- stable Web E2E capability belongs in `project.md`; feature-specific E2E cases belong in feature `tests.md` or `tests/e2e/*`
- `requirements/` stores human source material packages and requirement lifecycle/backlog records as requirement set directories: requirements, prototypes, feedback, screenshots, recordings, links, follow-up notes, status, and optional `requirements/INDEX.md`
- Concept Foundation is an internal Requirements Discussion / Requirement Product Grill method, not a canonical stage; when triggered, it stabilizes requirement-local product concepts before business-flow, state, and product-data modeling
- the effective human-reviewed requirement source owns accepted Concept Foundation and Requirement Product Model semantics; after archive, requirement README indexes the effective source/status without copying details, and Product Brief / Feature Spec consume those meanings by reference
- requirement-driven ADRs freeze an Effective Requirement Snapshot, inventory every source Requirement Model ID, and trace every in-scope accepted ID to a disposition, technical landing, Design Slice, and verification without taking ownership of product semantics
- upstream requirement changes invalidate dependency availability until compatibility review; `review-required` is not a decision lifecycle status, and incompatible accepted decisions are superseded rather than rewritten
- requirement-set dates mean archive date only, not deadlines or feature lifecycle dates
- future/deferred work belongs in requirement sets and optional `requirements/INDEX.md`, not in `project.md`
- `product.md` is optional feature-level product understanding when needed
- each feature has stable `spec.md`, `tasks.md`, `tests.md`, `plan.md`, `notes.md`; `contracts.md` is added only after human confirmation when producer-consumer boundaries need explicit handoff
- feature type may be `normal`, `maintenance-fix`, or `follow-up`; all use the same feature workspace model
- maintenance fixes are narrow feature workspaces under `.agent-loop/features/YYYY-MM-DD-fix-<slug>/`, not naked code edits and not a separate `.agent-loop/maintenance/` tree
- stories live in `spec.md`; optional `tasks/USn/` or `tests/USn/` folders are detail grouping, not separate story workspaces
- tasks live together in `tasks.md` by default; complex artifact mode may add linked detail files under `tasks/`
- `plan.md` is for the active task/story, not the whole feature by default
- submit/integrate is explicit and never commits, opens PRs, merges, or publishes without human confirmation
- Delivery Contracts live in `contracts.md` and optional `contracts/*`; file creation/update, contract acceptance, and breaking changes require human confirmation
- non-trivial human confirmations use table-first Human Review Summary; complete artifacts remain source of truth
- project-local skills require Gate 1 before creation/material update and an Execution Gate for every invocation; validated proposed skills activate automatically
- first version does not include multiplayer, roadmap graph, roadmap adapter, tdd-guard, complex ADR, global install, or automatic directory-level AGENTS.md without human confirmation

## Core Model

```text
Human Goal
→ Operational Support when the goal is to use/run/test/deploy current project behavior without confirmed implementation
→ Project Skill Creation / Update when a repeatable project workflow should become a durable local capability
→ Feature Workspace
→ Task / Test / Plan
→ Execute / Verify
→ Drift Check
→ Feature Follow-up / Flow-back when post-close bug/change appears
→ Project Memory Update
→ Submit / Integrate if requested
→ Resume / Pause / Close
```

Abstract model:

```text
Behavior Intent
→ Spec
→ Action
→ Evidence
→ Memory
```

## Definitions

**Project**: current codebase or repository. Long-term memory lives in `.agent-loop/project.md` by default.

**Remote Entry**: local entry directory for a remote project. It stores `.agent-loop/remote.md` and a thin `project.md` so future agents can reconnect to the remote source of truth.

**Local Shadow Mode**: fallback when remote project memory cannot be written remotely. Agent-loop artifacts stay local, but every code fact must cite remote evidence.

**Requirement**: human-provided need, goal, document, or natural-language request.

**Concept Foundation**: a triggered method inside Requirements Discussion / Requirement Product Grill that derives requirement-local stable Concept IDs, definitions, identity, lifecycle boundaries, relationships, owners, state-bearing classification, invariants, and product fact-source questions from scenarios and evidence. It is not a stage or top-level artifact.

**Requirement Product Model**: the product-layer derivation owned by the effective human-reviewed requirement source. It traces accepted concepts into relationships, roles/permissions, commands/events, business flow, product state, product data objects, invariants, and exception/recovery behavior without choosing tables, stores, protocols, or other technical representations. After archive, append-only follow-ups or a linked replacement set preserve prior sources while README indexes the effective source.

**Effective Requirement Snapshot**: the read-only ADR header that resolves the requirement README's current Effective Concept Foundation pointer and records the accepted source, Concept Foundation status, accepted Concept IDs, accepted Requirement Model IDs, compatibility judgment, and last compatibility check. It does not copy or redefine product meaning.

**Requirement Model Scope Inventory**: the source-wide ADR section that accounts for every stable Requirement Model ID (`REL-*`, `PERM-*`, `CMD-*`, `EVT-*`, `FLOW-*`, `STATE-*`, `PM-*`, and `EX-*`) before declaring the coherent ADR scope. It prevents silent omissions and records external, proposed, feature-local, or reasoned not-applicable ownership without becoming a separate artifact.

**Requirement Model Technical Landing Trace**: the table inside an existing Decision & Design record that gives every in-scope accepted Requirement Model ID one disposition and, when landed by this ADR, connects it to a concrete technical landing, preserved invariant, Design Slice, and verification path. It is not a separate artifact or executable schema.

**Prototype**: human-provided design artifact, screenshot, wireframe, or interaction reference.

**Feature**: one behavior-changing work area under `.agent-loop/features/<feature-id>/`.

**Stories**: user-perspective slices inside a feature. They live in `spec.md`. Use labels such as `US1`, `US2` in `tasks.md`; complex artifact mode may group detail files under `tasks/USn/` or `tests/USn/` without making stories separate workspaces.

**Task**: default executable engineering unit. Keep tasks small, verifiable, and tied to a story when possible.

**Step**: command-level or TDD-level action inside a task.

**Plan**: detailed construction plan for the active execution unit. Default scope is one task; story scope requires explicit human choice.

Important:

```text
Feature may have many stories and many tasks.
tasks.md is the feature-level task ledger.
plan.md is the active execution-unit plan.
plan.md keeps a stable filename; plan cycles are dated inside the file and archived into notes.md.
If plan.md exists, it must be construction-grade: exact paths, code context, interface contracts, parameters, test code, commands, expected outputs, and self-review.
```

**Evidence**: fresh proof such as test output, build output, lint/typecheck output, API results, E2E/browser verification, screenshots, logs, or review findings.

**E2E Discovery**: the stage that discovers real Web E2E capability from project reality before writing or executing browser automation. It records durable environment facts in `project.md` and feature-specific cases in `tests.md` or `tests/e2e/*`.

**Drift**: mismatch between implementation, code reality, human decision, and existing `agent-loop` documents.

**Project Skill**: a reusable project-specific capability under `.agent-loop/skills/<skill-name>/`. The index uses `proposed | active | disabled | deprecated` lifecycle and `bootstrap | on-demand` load policy. Active trust is bound to a validated content manifest. Loading is read-only preparation; every actual invocation requires the Execution Gate, with a named-skill/concrete-scope request accepted only when the disclosed plan stays fully inside that scope.

## Entry Scenarios

### New Project

Condition:

```text
No .agent-loop/
Little or no existing code
```

Action:

```text
Propose Init Project.
Create agent-loop skeleton after confirmation.
Draft project.md.
Create root AGENTS.md / CLAUDE.md guidance after confirmation.
Archive any provided requirement/prototype.
Create first feature workspace when human confirms.
```

### Remote Project Entry

Condition:

```text
Local directory is empty or ambiguous
Human says project is remote / SSH / devcontainer / container / tunnel
Real code/runtime/test source of truth is outside local path
```

Action:

```text
Load remote-project-discovery.md.
Do not create a normal local project memory.
Confirm remote host, path, access, permissions, command locations, browser URL, and sync model.
Write local remote.md and thin project.md after confirmation.
Prefer full remote agent-loop memory next to remote code when remote writes are allowed.
Use local-shadow mode only when remote writes are unavailable.
Then run Project Entry Scan against the remote source of truth.
```

### Project Entry Scan For Existing Projects

Condition:

```text
Existing code
No .agent-loop/
```

Action:

```text
Scan README, AGENTS/CLAUDE docs, package/test scripts, repo layout.
Draft project.md with project summary, directory map, test commands, known constraints.
Create or update root AGENTS.md / CLAUDE.md guidance after confirmation.
Ask human to confirm before starting feature work.
```

### Resume Existing Agent Loop

Condition:

```text
.agent-loop/ exists
project.md appears current enough
```

Action:

```text
Read project.md.
Find active/paused feature.
Read feature docs.
Summarize current state, blockers, and next suggested action.
Ask human to confirm next stage.
```

### Re-Adopt Agent Loop Project

Condition:

```text
.agent-loop/ exists
Recent development happened outside agent-loop
Human asks to re-adopt / re-sync / resume after outside-loop work
```

Action:

```text
Load recovery-and-backfill.md and project-guidance.md.
Treat code reality as current fact base for agent-maintained docs.
Compare code/tests/scripts/root guidance with agent-loop memory.
Propose backfill before new feature work.
Ask human confirmation before updating docs.
```

### Reconcile Project Context / Stale Memory

Condition:

```text
.agent-loop/ exists
project.md or feature docs appear stale compared with code reality
Long-term memory indexes point to missing/stale artifacts
```

Action:

```text
Scan code reality.
Compare with project.md and feature docs.
List differences.
Ask human which updates to accept.
Update project.md or feature docs after confirmation.
Then continue feature work.
```

### Evidence-Graph + DDD Onboarding Docs

Condition:

```text
.agent-loop/onboarding-db/ exists
Human asks to be guided through the project or understand where to start
```

Action:

```text
If onboarding-db was produced through an accepted Evidence-Graph + DDD Onboarding Spec, answer from those docs after checking obvious code reality.
If onboarding-db is an old layout, treat it as legacy evidence only; migration or replacement requires an accepted Evidence-Graph + DDD Onboarding Spec, Onboarding Tasks, and Full Execution Gate.
Answer from existing docs/code as chat or operational support when the human only asks a question.
Recommend Project Entry Scan if project memory is missing, thin, or stale.
Do not create or refresh onboarding-db through the removed legacy flow.
```

If onboarding-db is missing but project memory or root guidance claims it should exist, route to stale-memory recovery and ask before correcting `project.md` or root guidance. Do not recreate onboarding-db through the removed legacy flow.

#### Core Flow Completeness Invariant

Evidence-Graph + DDD Onboarding must preserve this trace for every `critical` / `important` core flow:

```text
Core Flow Inventory
-> accepted Core Flow selection
-> Flow Slice Coverage
-> Diagram + narrative + code-evidence trace
-> Completeness Hard Gate
-> Quality Score
```

A core flow is not closed merely because a synchronous call returned. It must trace to its business success, failure, cancellation, unknown, or manual-handling terminals and include any callback, consumer, retry, compensation, reconciliation, or job that owns a required transition, side effect, or recovery responsibility. Reclassifying those required slices as separate future topics does not remove them from the core flow.

A missing critical slice cannot be averaged away by diagram presence, readability, or other topic scores. `supporting` flows remain lightweight unless they own core state, an externally visible side effect, or recovery. Stateless overview, glossary, configuration, and index topics use only diagrams that explain real semantics; they do not invent state machines to satisfy a file-wide quota.

The invariant does not add a Human Gate. Onboarding has exactly two onboarding Human Gates: Onboarding Spec Acceptance, followed later by Onboarding Tasks Full Execution Gate. Completeness is an Agent quality gate inside the accepted scope.

### Feature Follow-up And Flow-back

Project Entry and memory bootstrap have priority over Feature Follow-up.

Condition:

```text
Human reports bug, regression, post-close correction, field/schema/algorithm/API change, test failure, screenshot issue, QA/user feedback, or small tweak
.agent-loop/ or legacy agent-loop/ memory exists
```

Action:

```text
Load feature-follow-up.md.
Inspect Active / Paused / Closed features and recent feature docs.
Use 30 days as the default lookback, not a hard boundary.
Present Candidate Match Matrix.
Recommend flow-back, linked new feature, maintenance-fix, or investigate-first.
```

### Active Feature Continuation

Condition:

```text
.agent-loop/ exists
Active Feature exists
Next stage is clear
```

Action:

```text
Read active feature docs.
Classify current stage.
Recommend exactly one next action.
```

### Blocked

Condition:

```text
Blocker or missing decision prevents next stage
```

Action:

```text
Choose exactly one unblock stage.
Ask one focused human question, or route to Diagnose Failure / Targeted Feature Scan.
Do not continue execution until the blocker is resolved.
```

### Project Skill Creation / Update

Condition:

```text
Human asks to turn a repeatable project workflow into a skill, or to update, disable, or deprecate one
Project Entry / project memory is reliable
```

Action:

```text
Load references/project-skills.md.
Present Project Skill Candidate and Gate 1 before files are created or materially updated.
Resolve writing-skills and skill-creator independently; use both when available.
Write only under .agent-loop/skills/<skill-name>/.
Keep proposed until RED/GREEN/REFACTOR and validation pass, then activate automatically.
Require the Execution Gate for every invocation.
```

## Main Flow

Within Requirements Discussion, triggered complex requirements use this internal semantic order before the canonical stage flow continues:

```text
Scenario / Evidence
→ Concept Candidate Inventory
→ Concept Foundation Human Confirmation
→ Requirement Product Model
→ human-reviewed Requirement Document
```

Simple requirements record `concept-foundation-not-needed` with a reason and remain lightweight. `candidate` and `reopened` are blocking; only `accepted` or a reasoned not-needed result may continue into requirement product modeling.

Within Decision & Design, a requirement-driven ADR uses this internal order without adding a canonical stage or default mapping artifact:

```text
Effective Requirement Source
→ Effective Requirement Snapshot
→ Requirement Model Scope Inventory
→ Requirement Model Technical Landing Trace
→ proposed structural preflight
→ Decision & Design Human Review
→ accepted-mode validation and assigned Design Slices
```

The trace consumes accepted product semantics. Product ambiguity returns to Requirements Discussion; technical incompatibility with an accepted ADR creates a superseding decision after Human Review.

```text
Project Entry
→ Remote Project Discovery if Needed
→ Re-Adopt Agent Loop Project if Needed
→ Code-Guided Operational Support if Needed
→ Project Skill Creation / Update if Needed
→ Requirement Archive
→ Decision & Design If Needed
→ Product Brief if Needed
→ Brainstorm / Clarify if Needed
→ Feature Follow-up And Flow-back if Needed
→ Targeted Feature Scan if Needed
→ Feature Spec
→ Requirement Checklist
→ Work Breakdown
→ Delivery Contract if Needed
→ Test Design
→ E2E Discovery if Web
→ Technical Design / Code Context
→ Plan Gate / Plan if Needed
→ Analyze Consistency
→ Subagent Execution If Approved
→ Execute Task / Story
→ Verify
→ Review
→ Drift Check
→ Project Memory Update
→ Feature Completion Check
→ Submit / Integrate
→ Pause / Close
```

## First-Version Exclusions

Do not build or invoke these as first-version requirements:

```text
multiplayer workflow
roadmap graph
roadmap adapter
tdd-guard
complex ADR system
global skill installation
automatic directory-level AGENTS.md generation without human confirmation
automatic commit, PR, merge, release, or publish action without human confirmation
```

Roadmap Skill remains a future multiplayer visualization reference only.

## Reference Influences

- OpenSpec: current fact vs current change, added/modified/removed behavior, close/archive backfill.
- Spec Kit: specify, clarify, checklist, plan, tasks, analyze as fallback middle structure.
- Superpowers: brainstorming, writing plans, TDD, debugging, review, verification discipline.
- mattpocock skills: lightweight setup, grilling docs, PRD, issues, TDD, diagnose, handoff, review patterns.

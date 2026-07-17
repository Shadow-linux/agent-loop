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
- Human-Guided Branch Management is an optional internal Branch Strategy Check, not a canonical stage and not a mandatory Git Flow migration
- a durable Branch Strategy is recorded in `project.md` only after explicit human acceptance; `declined` uses `Profile: not-applicable` plus a concrete reason, not-needed keeps the lightweight existing-project profile, and an unconfirmed recommendation is never `accepted`
- a Branch Action Gate confirms creation or switching of one exact development branch; strategy adoption, plan acceptance, and auto modes never satisfy it
- `project.md` owns the accepted long-term strategy and current Target Release Context pointer; mutable per-feature branch state belongs in feature notes, plan, or Submit / Integrate evidence
- standard and customer release aggregation branches are retained; formally released versions are sealed; customer customization cannot flow wholesale into the standard product line
- branch-specific Target Release Context and Target Branch stops apply only to an adopted strategy or versioned/customer delivery; a confirmed simple `not-needed` path continues without those fields
- Post-Merge Memory Reconciliation is an internal Submit / Integrate method after verified code integration, not a canonical stage or message intent; it never performs code merge or authorizes a later Git action
- the Target Canonical Memory Spine supplies output structure and scan order, not fact priority or a path allowlist; the Path Accounting Ledger covers every Base, Source, Target-before, and Result path
- every discovered memory record is classified by semantic role, then checked against the authority for its specific question; no single snapshot or code reality is globally authoritative
- the Agent derives one Desired Target Memory Snapshot from immutable human sources, accepted authorities, valid history, merged reality, Target-appropriate current state, and rebuilt indexes
- one full Merged Code SHA owns one durable Memory Merge Report and at most one successful Apply; sibling report identities and completed replay fail closed
- Chinese action labels are executable plan semantics: import starts absent, rewrite starts from the exact regular-file preimage, recalculate may rebuild an absent derived file or replace its exact preimage, stale removal ends absent, and immutable human/accepted imports copy only a same-path recorded regular Git blob
- Memory Reconciliation CLI output is deterministic UTF-8; POSIX worktrees enforce `100644` versus `100755` exactly, while native Windows treats only those two regular-file worktree modes as equivalent because it cannot represent the executable bit, without relaxing bytes, kind, source, path, identity, or transaction checks
- optional `.agent-loop/skills/` owns Human-gated project-local reusable capabilities; `INDEX.md` owns lifecycle and discovery metadata
- Project Skill Discovery Guard checks active INDEX metadata before negative Project Skill claims or generic executable fallback, loads only a matched body, and fails closed on drift without adding a stage, status, cache, or execution grant
- stable Web E2E capability belongs in `project.md`; feature-specific E2E cases belong in feature `tests.md` or `tests/e2e/*`
- `requirements/` stores human source material packages and requirement lifecycle/backlog records as requirement set directories: requirements, prototypes, feedback, screenshots, recordings, links, follow-up notes, status, and optional `requirements/INDEX.md`
- Human-Guided Bug Management is an internal method of `Feature Follow-up / Flow-back`, not a canonical stage or message intent
- Lightweight Change Lane is an internal route before Feature construction for bounded ordinary non-Bug changes; it is not a canonical stage, message intent, Feature Type, Bug Resolution Path, lifecycle, status, or Auto Mode
- Lightweight Execution Card is response-local execution control with required background, adaptive Plan, progress, targeted verification, rollback, gate, and result fields; it creates no default target-project artifact or backlog
- Adaptive Depth lets the Agent vary Plan and test detail by real risk while fresh verification, diff review, rollback, scope control, memory impact, and Human Gates stay fixed
- `bugs/INDEX.md` owns Bug inventory/backlog/locator state, while each Bug README owns stable identity, facts, evidence, lifecycle, Resolution Path, verification, close, and reopen history
- Bug Report, Bug Record, Report Origin, Expected Behavior Evidence, Status, Resolution, and Reopen are distinct; Bug Status and Resolution form independent axes
- Requirement owns product meaning, Bug Record owns defect coordination, and Feature owns every code repair; Bug-to-Requirement links are optional `0..N` and never auto-change Requirement lifecycle
- Bug identity scans all Bug Index metadata without a cutoff; Feature ownership defaults to a 90-day metadata scan, evidence-ranked deep reads, and evidence-driven extension beyond 90 days
- Bug intake order is complete Bug Index metadata scan -> 90-day Feature metadata scan -> evidence-ranked deep read / evidence-driven extended scan -> create/update/reopen Bug Record
- archive changes Feature location, not identity or ownership; discovery and Human Review read archived evidence without rehydrate, while confirmed flow-back rehydrates before reopened execution
- Report Origin introduces no Owner, Assignee, personnel permission, staffing, workload, or automatic Priority system
- Concept Foundation is an internal Requirements Discussion / Requirement Product Grill method, not a canonical stage; when triggered, it stabilizes requirement-local product concepts before business-flow, state, and product-data modeling
- the effective human-reviewed requirement source owns accepted Concept Foundation and Requirement Product Model semantics; after archive, requirement README indexes the effective source/status without copying details, and Product Brief / Feature Spec consume those meanings by reference
- requirement-driven ADRs freeze an Effective Requirement Snapshot, inventory every source Requirement Model ID, and trace every in-scope accepted ID to a disposition, technical landing, Design Slice, and verification without taking ownership of product semantics
- upstream requirement changes invalidate dependency availability until compatibility review; `review-required` is not a decision lifecycle status, and incompatible accepted decisions are superseded rather than rewritten
- requirement-set dates mean archive date only, not deadlines or feature lifecycle dates
- future/deferred work belongs in requirement sets and optional `requirements/INDEX.md`, not in `project.md`
- `product.md` is optional feature-level product understanding when needed
- each feature has stable `spec.md`, `tasks.md`, `tests.md`, `plan.md`, `notes.md`; `contracts.md` is added only after human confirmation when producer-consumer boundaries need explicit handoff
- Feature Monthly Archive is explicit closed-history maintenance: Feature ID is stable, eligible whole directories move to `features/YYYY-MM/<feature-id>/`, and root `features/archive.md` is only the locator/ledger
- archive state is not feature lifecycle; active / blocked / paused features stay flat, and archived closed features rehydrate before reopened execution
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
→ [internal] Branch Strategy Check when branch rules, target version, or customer isolation affect safe delivery
→ Operational Support when the goal is to use/run/test/deploy current project behavior without confirmed implementation
→ [internal] Lightweight Change Assessment for bounded ordinary non-Bug local changes before Feature construction
→ Project Skill Creation / Update when a repeatable project workflow should become a durable local capability
→ Feature Workspace
→ Task / Test / Plan
→ Execute / Verify
→ Drift Check
→ Feature Follow-up / Flow-back with internal Bug Management when explicit defect management appears
→ Feature Monthly Archive when the human explicitly asks to compact closed-history discovery
→ Project Memory Update
→ Submit / Integrate if requested
  → [internal] Post-Merge Memory Reconciliation after verified code integration and before later Git gates when branch memories may differ
→ Resume / Pause / Close
```

## Post-Merge Memory Reconciliation Invariant

After code integration, use the **Target Canonical Memory Spine** as the traversal and output-structure baseline, then account for all paths across Base, Source, Target-before, and Result in a **Path Accounting Ledger**. Classify each record as human source, accepted authority, append-only evidence, current semantic state, derived index, validated package, transaction temporary, or unclassified before selecting an action.

Derive a **Desired Target Memory Snapshot** by question-specific fact authority. Code proves implementation reality but does not overwrite accepted product or technical meaning. Preserve original human sources, accepted decisions, and append-only history; rebuild derived indexes; expose semantic conflicts to the human.

The method has a Start gate before report creation and an exact Plan Hash gate before Apply. One Merged Code SHA has one report and one successful Apply. Apply, post-check, restore, memory commit, push, release, and Source branch cleanup remain distinct boundaries. See `memory-reconciliation.md` for the detailed contract.

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

**Lightweight Change Lane**: bounded non-Bug execution route before Feature construction. Explicit Bug Management and active Feature ownership take precedence; hard triggers use Feature, and uncertain impact returns to Human Choice before writes.

**Lightweight Execution Card**: response-local background, goal, scope, rationale, risk, Plan, progress, verification, rollback, Human Gate, and result control. It is not a Feature `plan.md`, persistent task, or authorization for later actions.

**Adaptive Depth**: Agent-owned risk-based selection of card detail, Plan steps, targeted verification, and the smallest meaningful RED/GREEN for isolated behavior. It never reduces safety, scope, rollback, evidence, memory, or action-specific gate invariants.

**Bug Report**: one source event describing a suspected defect. It is intake evidence and does not automatically create a distinct stable identity.

**Bug Record**: stable deduplicated entity for an expected-versus-observed mismatch. It owns provenance, observations, evidence, Status, Resolution, Resolution Path, relationships, verification, close, and reopen history. It does not own product meaning or implementation.

**Report Origin**: optional provenance using `person | customer | group | qa | monitoring | automated-test | agent | external-ticket | other | unknown`. It never becomes Owner, Assignee, permission, Priority, branch, or responsibility evidence.

**Bug Evidence**: bounded reproduction, impact, environment, investigation, failure, and verification evidence that excludes secrets and unnecessary production payloads.

**Expected Behavior Evidence**: accepted Requirement, Decision / ADR, Delivery Contract, Feature Spec/test, stable product rule, prior verified behavior, or explicit human clarification used to judge the Bug claim.

**Resolution Path**: one current Bug workflow relationship: `investigate-first | flow-back | linked-feature | maintenance-fix | requirement | no-fix`. It is Human-gated before creating/reopening a Feature or changing a Requirement.

**Bug Status**: `reported | triaging | confirmed | in-progress | verifying | deferred | closed` processing state. An `in-progress` Bug requires `flow-back | linked-feature | maintenance-fix` plus one Human-confirmed Fix Feature Target. `investigate-first`, `requirement`, and `no-fix` are not Feature repair execution states.

**Bug Resolution**: independent conclusion `unresolved | fixed | duplicate | not-a-bug | cannot-reproduce | accepted-risk | superseded`.

**Reopen Record**: append-only event that preserves the prior Close Record, records recurrence/new evidence and human decision, returns the Bug to `triaging` or `confirmed`, and resets Resolution to `unresolved`.

**Bug Ownership Lookback**: unbounded Bug Index metadata identity scan followed by a default 90-day Feature metadata scan, evidence-ranked deep reads, and evidence-driven extended scan.

Bug relationships are:

```text
Bug Report 1..N -> 1 Bug Record
Bug Record 0..N -> Requirement
Bug Record 0..N -> Related Feature / Decision / Contract
Bug Record 1 -> current Resolution Path
Bug Record 0..1 -> Fix Feature while repair is active
Feature 0..N -> Bug Record
Bug Record 0..1 -> Duplicate Of canonical Bug Record
```

One coherent Feature may resolve several Bugs. Each Bug retains independent identity, verification, Resolution, close, and reopen evidence. There is no Bug Owner/Assignee model, and Bug artifacts never own tasks, tests, plans, or code execution.

**Concept Foundation**: a triggered method inside Requirements Discussion / Requirement Product Grill that derives requirement-local stable Concept IDs, definitions, identity, lifecycle boundaries, relationships, owners, state-bearing classification, invariants, and product fact-source questions from scenarios and evidence. It is not a stage or top-level artifact.

**Requirement Product Model**: the product-layer derivation owned by the effective human-reviewed requirement source. It traces accepted concepts into relationships, roles/permissions, commands/events, business flow, product state, product data objects, invariants, and exception/recovery behavior without choosing tables, stores, protocols, or other technical representations. After archive, append-only follow-ups or a linked replacement set preserve prior sources while README indexes the effective source.

**Effective Requirement Snapshot**: the read-only ADR header that resolves the requirement README's current Effective Concept Foundation pointer and records the accepted source, Concept Foundation status, accepted Concept IDs, accepted Requirement Model IDs, compatibility judgment, and last compatibility check. It does not copy or redefine product meaning.

**Requirement Model Scope Inventory**: the source-wide ADR section that accounts for every stable Requirement Model ID (`REL-*`, `PERM-*`, `CMD-*`, `EVT-*`, `FLOW-*`, `STATE-*`, `PM-*`, and `EX-*`) before declaring the coherent ADR scope. It prevents silent omissions and records external, proposed, feature-local, or reasoned not-applicable ownership without becoming a separate artifact.

**Requirement Model Technical Landing Trace**: the table inside an existing Decision & Design record that gives every in-scope accepted Requirement Model ID one disposition and, when landed by this ADR, connects it to a concrete technical landing, preserved invariant, Design Slice, and verification path. It is not a separate artifact or executable schema.

**Branch Strategy**: a human-confirmed durable policy describing the project profile, main branch, release and development naming patterns, sealed-release rule, customer isolation, and cleanup policy. Accepted profiles are `existing-project | human-guided-release`; a declined recommendation records `Profile: not-applicable` plus its reason. It is optional guidance and does not itself authorize a Git mutation.

**Branch Strategy Check**: an internal method used at Project Entry, planning, drift, and submit boundaries. It preserves a clear existing strategy, recommends the optional Human-Guided profile only when rules are confused, target release is unclear, or customer boundaries are risky, and stops before adoption until the human decides. Branch-specific target-context stops do not apply to a human-confirmed simple `not-needed` path.

**Branch Action Gate**: the action-specific Human Gate for creating or switching one exact development branch. Strategy adoption, target selection, plan acceptance, and auto modes do not authorize it.

**Current Branch Context**: the volatile feature-level evidence for branch class, work type, target kind/version/customer/topic, source/target, lifecycle, and last human decision. It does not replace Requirement, Feature, Task, ADR, verification, or lifecycle authority.

**Release Aggregation Branch**: a retained `release/vX.Y.Z` standard line or `customer/<customer>/vX.Y.Z` customer line that receives reviewed work for one target version. Retention is policy; creation, merge, push, and release remain separately Human-gated actions.

**Development Branch**: temporary feature, bugfix, or hotfix work named `feature|bugfix|hotfix/vX.Y.Z/<topic>` for standard delivery or `feature|bugfix|hotfix/<customer>-vX.Y.Z/<topic>` for customer delivery. It may be deleted only after merge evidence and human confirmation.

**Target Release Context**: the current standard or customer release pointer needed to plan a feature safely. It names the target kind/version/customer and expected release branch without authorizing that branch to be created or changed.

**Sealed Release**: a formally released version that is immutable. A repair moves to a new patch version and a new capability moves to a human-confirmed new version.

**Prototype**: human-provided design artifact, screenshot, wireframe, or interaction reference.

**Feature**: one behavior-changing work area under `.agent-loop/features/<feature-id>/`.

**Feature Monthly Archive**: An explicit, Human-gated maintenance capability that moves an eligible closed feature directory intact to `.agent-loop/features/YYYY-MM/<feature-id>/`, updates `features/archive.md` and approved references, post-checks, and restores on failure. The scan is read-only and apply requires the exact expected plan SHA-256 Batch Human Gate plus transaction journal. It creates no per-feature archive summary, no `historical/`, no Deep Archive, and no `--force`.

**Feature Locator**: The root `features/archive.md` mapping from stable Feature ID to current flat or month path. It locates history but does not own product, requirement, decision, lifecycle, test, or delivery facts.

**Archive State**: `archived | rehydrated`. Archive state is not feature lifecycle; lifecycle remains `draft | active | blocked | paused | closed`.

**Rehydrate**: The separately Human-reviewed move from a month path back to the flat feature path. Rehydrate before reopened execution; Feature Follow-up decides any later `closed -> active` lifecycle transition.

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

## Project Skill Discovery Guard

Project Skill Discovery Guard is an internal read-only controller invariant, not a canonical stage or message intent. After reliable memory/intent routing and before a stage-specific helper or generic executable fallback, the Agent inspects INDEX metadata, matches only active `bootstrap | on-demand` candidates, verifies the matched exact INDEX row/path/manifest, and loads only the matched body.

The response-local outcomes are `matched-active | index-absent | no-active-match | project-skill-drift`; they are not Project Skill lifecycle values and are not persisted in a cache or new artifact. `matched-active` continues to the existing per-invocation Execution Gate. Ordinary chat remains response-only and does not require all Project Skill bodies to load.

runtime/global Skill inventory does not prove that no Project Skill exists. Only `index-absent` or `no-active-match` permits generic fallback. `project-skill-drift` fails closed and cannot be bypassed through an equivalent generic operation.

Context may reuse unchanged INDEX metadata within one uncompacted reliable stage, but context compaction, controller re-entry, long-session uncertainty, stage-boundary uncertainty, INDEX change, or manifest change requires rediscovery. Project-local matches remain below Agent Loop controller/Human Gates and above runtime/global helpers and built-in fallback.

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
Explicit Bug management intent, defect/regression/QA/post-close evidence, changed accepted behavior, or clear Feature ownership indicates follow-up
Generic adjustment wording alone does not enter Feature Follow-up; route an actionable ordinary non-Bug change through Lightweight Change Assessment first.
.agent-loop/ or legacy agent-loop/ memory exists
```

Action:

```text
Load bug-management.md for explicit Bug management and feature-follow-up.md for ownership routing.
Scan all Bug Index metadata for duplicate/reopen identity before Feature candidates; without explicit Bug management intent, do not create or update a Bug Record.
Inspect Active / Paused / Closed Feature metadata in the default 90-day window, then deep-read evidence-ranked candidates and extend beyond 90 days when evidence points there.
Resolve archived candidates through `features/archive.md`; discovery and Human Review are read-only and do not require rehydrate.
For explicit Bug management, create/update/reopen the Bug Record, verify Expected Behavior, and recommend exactly one Resolution Path.
Wait for the Resolution Path Gate only for explicit Bug management; every Feature create/reopen action keeps its separate gate. Rehydrate a confirmed archived owner only before reopened execution.
```

### Feature Monthly Archive

Condition:

```text
Human explicitly requests archive or rehydrate
Project memory and feature close evidence are reliable
```

Action:

```text
Run read-only scan and show one deterministic Batch Review.
Wait for confirmation of the exact plan SHA-256.
Apply only eligible moves through the transaction journal.
Update the root locator and approved references, then post-check.
Restore on failure; route a stranded journal to Recovery.
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

For an actionable ordinary non-Bug local change before Feature construction, use this internal route:

```text
Explicit Bug Management / active Feature ownership first
→ Lightweight Change Assessment
  → clearly eligible: response-local card, bounded edit, targeted verification, diff/rollback/memory review
  → Feature trigger: normal Feature construction
  → uncertain: Human Choice with one Agent recommendation and zero writes
```

Eligibility is all-of; Feature hard triggers are any-of. Fact/config/path/domain/docs changes use failure-matched targeted verification, while isolated behavior logic uses the smallest meaningful RED/GREEN. Scope expansion stops before broader edits and returns to Human Review. This route creates no `.agent-loop/changes/`, quick-fix backlog, state enum, or helper-native document tree.

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
→ Feature Monthly Archive If Explicitly Requested
→ Code-Guided Operational Support if Needed
→ [internal] Lightweight Change Assessment for eligible ordinary non-Bug changes
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

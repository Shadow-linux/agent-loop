# Agent Loop Concepts

## Scope

This skill is for single-person development with a CLI agent. The human controls direction; the agent controls workflow mechanics.

First version excludes:

- multiplayer workflows
- roadmap graph
- roadmap adapter
- tdd-guard
- complex ADR system
- global installation
- automatic directory-level AGENTS.md generation without human confirmation
- automatic commit, PR, merge, release, or publish action without human confirmation

## Definitions

**Human Goal**: Human intent, requirement, prototype, bug, or continuation request.

**Project**: Current codebase. Long-term project memory is `.agent-loop/project.md`.

**Project Memory Mode**: The structure used for durable project knowledge. `simple` means `project.md` is the main memory body. `enterprise` means `project.md` is an index and current-state summary, with optional details under `.agent-loop/project/*.md`.

**Architecture Profile**: The project shape, language adapter, framework adapter, and DDD intensity used to guide code layout and boundary decisions. It is descriptive for existing projects and advisory for new scaffolds.

**Remote Entry**: A local directory that mainly exists to help the agent find and continue a remote project. It owns local `.agent-loop/remote.md` and a thin `project.md` with `Status: remote-entry`.

**Local Shadow Mode**: A fallback where `agent-loop` memory is kept locally because the remote project is not writable. Every code fact, command, test result, and browser observation must include remote evidence.

**Requirement**: Human-provided textual or conversational need.

**Lightweight Change Lane**: Bounded non-Bug execution route before Feature construction. It requires all eligibility evidence, yields to explicit Bug Management and active Feature ownership, and stops for Human Choice when uncertain.

**Lightweight Execution Card**: Persistent per-change background, scope, adaptive Plan, progress, targeted verification, rollback, Human Gate, result, and Memory Review control under `<memory-root>/changes/YYYY-MM/YYYY-MM-DD-<topic>.md`. The card file is the execution source of truth; it is not a Feature workspace, shared backlog, long-term project-memory fact, or later-action authorization.

**Change Memory Consolidation**: Agent-owned semantic review of completed Lightweight Change evidence. A read-only scanner validates and counts records, while the Agent alone classifies stable facts as `none | synced | human-review`, discloses exact memory scope before writes, and preserves every existing Human Gate.

**Adaptive Depth**: Risk-based detail selection for the card, Plan, and targeted test/verification method. It never reduces scope control, fresh evidence, rollback, memory impact review, or an existing Human Gate.

**Bug Report**: One intake event and its source evidence. Several reports may be attached to one stable Bug Record; one report does not automatically create a new Bug identity.

**Bug Record**: Stable, deduplicated identity for an expected-versus-observed behavior mismatch. It owns facts, evidence, lifecycle, Resolution Path, relationships, verification, close, and reopen history, but not product meaning or repair execution.

**Report Origin**: Optional provenance for a Bug Report: person, customer, group, QA, monitoring, automated test, agent, external ticket, other, or unknown. It is not Owner, Assignee, permission, Priority, or responsibility evidence.

**Bug Evidence**: Bounded reproduction, environment, log, screenshot, failed-test, impact, investigation, and verification evidence attached to a Bug Record without copying secrets or unnecessary production payloads.

**Expected Behavior Evidence**: Accepted product or behavior authority used to decide whether observed behavior is a Bug. Code reality can prove the observation but cannot alone define the intended product behavior.

**Resolution Path**: The Bug's single current workflow relationship: `investigate-first | flow-back | linked-feature | maintenance-fix | requirement | no-fix`. It is not a personnel assignment or implementation authority.

**Bug Status**: Processing state `reported | triaging | confirmed | in-progress | verifying | deferred | closed`; it is independent from the final Resolution. `in-progress` is reserved for a Human-confirmed `flow-back | linked-feature | maintenance-fix` Feature target.

**Bug Resolution**: Conclusion `unresolved | fixed | duplicate | not-a-bug | cannot-reproduce | accepted-risk | superseded`; a closed Bug cannot remain unresolved.

**Reopen Record**: Append-only history event that preserves prior close evidence, records the recurrence/new evidence and human decision, returns a closed Bug to `triaging` or `confirmed`, and restores `Resolution: unresolved`.

**Bug Ownership Lookback**: Two-layer discovery rule: all Bug Index metadata participates in duplicate/reopen identity checks without a time cutoff, while Feature ownership uses a default 90-day metadata scan plus evidence-ranked deep read and evidence-driven extension beyond the window.

**Branch Strategy**: Optional, human-confirmed durable branch policy. It records profile, main/release/development patterns, sealed-release behavior, customer isolation, and deletion policy without authorizing Git actions.

**Branch Strategy Check**: Internal check at entry, planning, drift, and submit boundaries. Preserve clear existing policy; otherwise recommend one Human-Guided option and wait for explicit acceptance before adoption.

**Current Branch Context**: Volatile, evidence-backed identity for the current execution unit: branch class, work type, target kind/version/customer/topic, source/target branch, lifecycle state, last check, and human decision. It belongs in feature notes/plan/submit evidence and never replaces Requirement, Feature, Task, ADR, verification, or lifecycle authority.

**Target Release Context**: Current standard/customer release pointer used by feature planning. Its volatile development-branch detail stays in feature notes, plan, or Submit / Integrate evidence.

**Release Aggregation Branch**: Retained standard `release/vX.Y.Z` or customer `customer/<customer>/vX.Y.Z` branch for a target version.

**Development Branch**: Temporary `feature|bugfix|hotfix` branch for a standard or customer target. Deletion requires merge evidence and human confirmation.

**Sealed Release**: Formally released immutable version. Repairs use a new patch version; new capabilities use a human-confirmed new version.

**Prototype**: Human-provided design artifact, screenshot, diagram, or interaction reference.

**Feature**: One behavior-changing work area under `.agent-loop/features/<feature-id>/`. A feature can contain many stories and many tasks.

**Feature Monthly Archive**: Explicit closed-history maintenance that moves an eligible whole feature directory intact to `.agent-loop/features/YYYY-MM/<feature-id>/`, maintains root `features/archive.md`, updates only approved references, and uses a deterministic plan hash, Batch Human Gate, transaction journal, post-check, and restore.

**Feature Locator**: The `features/archive.md` row that maps a stable Feature ID to its current flat or archived path. It is not the authority for feature behavior or delivery evidence.

**Archive State**: `archived | rehydrated`; archive state is not feature lifecycle.

**Rehydrate**: Human-gated movement of an archived closed feature back to its flat path before Feature Follow-up may reopen it for execution.

**Feature Type**: Feature work can be `normal`, `maintenance-fix`, or `follow-up`. The file layout stays the same for all types.

**Maintenance Fix**: A narrow feature used when a bugfix or internal correction has no clear owning recent feature and does not create a new user capability. It is not a workflow bypass and not a separate directory system. It still uses `.agent-loop/features/YYYY-MM-DD-fix-<slug>/` with `spec.md`, `tasks.md`, `tests.md`, `plan.md`, `notes.md`, verification, review, drift check, project memory update when needed, and close.

**Product Brief**: Optional feature-level product understanding in `product.md`: problem, users, user stories, product scope, product decisions, and open product questions.

**Decision & Design / ADR**: Requirement-landing design for accepted requirements that need shared business-flow, domain/state/data, architecture, consistency, recovery, non-functional goals, or cross-feature ownership. The record lives under `.agent-loop/decisions/*.md`, is Human-gated, and is conditionally required only when shared design needs a durable source that no accepted decision already provides. It is not required for every feature and is not a complex ADR system.

**Stories**: User-perspective slices inside a feature. They live in `spec.md` and are referenced by labels such as `US1`.

**Task**: Default executable engineering unit. Tasks should be small, verifiable, and linked to a story when possible.

**Step**: TDD or command-level action inside a task.

**Plan**: Active execution plan for one task by default, or one story when explicitly chosen. It is not the whole feature plan unless the feature is tiny and the human explicitly confirms whole-feature execution.

**Construction-Grade Plan**: A `plan.md` that can be executed by an agent with near-zero project context: exact paths, code context, interface contracts, signatures, parameters, test code, commands, expected RED/GREEN output, rollback, and self-review.

**Evidence**: Fresh proof from tests, build, lint/typecheck, API checks, E2E/browser checks, screenshots, logs, or review.

**E2E Discovery**: Web-specific discovery before browser automation. The agent reads real scripts, configs, docs, fixtures, env rules, CI, and existing E2E specs to determine app start, URL, auth/test data, and automation route before recording or executing E2E cases.

**Drift**: Mismatch between docs, code reality, or human decisions.

**Feature Follow-up / Flow-back**: Feature-ownership route for explicit Bug management, defect/regression/QA/post-close evidence, changed accepted behavior, or clear active/closed Feature ownership. Generic adjustment wording alone routes an actionable ordinary non-Bug change through Lightweight Change Assessment before ownership scanning. When Follow-up applies, Bug identity scans all Bug Index metadata and Feature ownership defaults to 90 calendar days with evidence-driven extension; only explicit Bug management creates or updates a Bug Record.

**Code-Guided Operational Support**: Read-only support lane for using current project functionality to test, run, deploy, switch account/config/model/provider, check quota/rate limits, arrange rollout, diagnose production, or produce a runbook/checklist. It does not create a feature workspace or edit code/config by default; feature/fix escalation requires human confirmation.

**Re-Adopt Agent Loop Project**: Recovery path for a project that already has `.agent-loop/` or legacy `agent-loop/`, but recent development happened outside the loop. The agent compares code reality to existing memory, proposes backfill, asks human confirmation, then resumes or starts feature work.

**Submit / Integrate**: The explicit stage that packages verified work for commit, PR text, merge note, or release note. It requires human confirmation and records the result in `notes.md`.

**Post-Merge Memory Reconciliation**: An internal Submit / Integrate method that runs only after verified code integration. It reconciles the Target memory root and does not add a canonical stage or message intent, perform code merge, or authorize Git actions.

**Target Canonical Memory Spine**: The actual Target branch's artifact ownership, `project.md`, enterprise indexes, stable IDs, and canonical locators. It supplies scan order and output structure, not universal truth or a path allowlist.

**Path Accounting Ledger**: The all-path inventory and semantic disposition covering directories, files, links, unchanged rows, and meaningful absence across Base, Source, Target-before, and Result.

**Desired Target Memory Snapshot**: The semantic Target memory derived from merged implementation reality, immutable human sources, accepted product/technical meaning, valid history, Target-appropriate current state, and rebuilt indexes.

**Memory Merge Report**: The one durable audit record for one full Merged Code SHA, including Merge Context, ledger, Human Decisions, exact Plan Hash, Apply, post-check, and restore evidence. It is not a replacement fact owner.

**Subagent Brief**: A bounded assignment for an optional helper agent. The main agent owns state, merge, drift, submit, and close decisions.

**Delivery Contract**: A durable producer-consumer boundary handoff in `contracts.md` and optional `contracts/*` details. It records API, service, event, async workflow, data, UI-behavior, library, or runtime interfaces that downstream work depends on. It is distinct from temporary subagent briefs.

**Strict Mode**: Default gate mode. Ask before and after every stage.

**Feature Auto-Loop**: Feature-level authorization after Requirement Checklist passes and Feature Spec is accepted. The agent may advance Agent-ready feature stages/tasks until a stop condition appears. It must stop before Submit / Integrate and Close.

**Task Auto-Run**: Task/story-level authorization after the selected task/story plan is accepted. The agent runs Analyze Consistency before TDD execution, then may complete only that task/story through verification, review, drift, and status update.

**Feature Completion Check**: Proactive check that determines whether an active feature should be closed, continued, paused before a new feature, or have scope updated. Humans do not need to ask for close by name; the agent recommends it when conditions pass.

**Feature Close Review**: Required feature-level review before recommending or performing close. It verifies the whole feature against `product.md` when present, `spec.md`, `tasks.md`, `tests.md`, acceptance criteria, out-of-scope boundaries, and project standards. It is separate from per-task review.

**Human Review Summary**: Table-first, human-facing approval view shown before non-trivial confirmations. It summarizes artifacts, evidence, risks, blockers, and requested decisions while full artifact files remain the source of truth.

## Ownership

```text
remote.md  = local entry pointer for remote projects
project.md = long-term project facts in simple mode; memory index and current state in enterprise mode
project/   = optional enterprise long-term project memory details
decisions/ = Human-gated project / cross-feature Decision & Design records; globally optional and conditionally required when shared design has no accepted source
requirements/ = original human material packages, references, and requirement lifecycle/backlog records, grouped by archive-date requirement set directory
bugs/INDEX.md = Bug inventory, backlog, and locator
bugs/YYYY-MM-DD-<bug-slug>/README.md = stable Bug identity, facts, evidence, lifecycle, Resolution Path, verification, close, and reopen history
product.md = optional feature product intent and product scope
spec.md    = intended feature behavior
tasks.md   = work breakdown and order
tests.md   = how correctness will be proven, including feature-specific E2E cases
plan.md    = active execution plan for the current task/story
notes.md   = what actually happened
handoffs/  = optional subagent briefs and returns
contracts.md = optional delivery contract index or compact contract
contracts/ = optional durable producer-consumer contract details
Lightweight Execution Card = persistent per-change execution control under changes/YYYY-MM/YYYY-MM-DD-topic.md; no shared backlog, Archive lifecycle, or Git authorization
```

`AGENTS.md` / `CLAUDE.md` live outside `.agent-loop/` and tell future agents how to enter the workflow. They do not own task state.

Requirement-set dates are archive dates only. They do not define deadlines, requirement duration, or feature lifecycle.

Requirement sets group the human's original materials for one intake event or topic: requirement docs, prototypes, feedback, screenshots, recordings, links, and follow-up notes.

Requirement lifecycle/backlog records future, deferred, accepted, in-progress, implemented, superseded, rejected, and reference-only demand in requirement set `README.md` and optional `requirements/INDEX.md`. It is not project memory, and it does not rewrite source files such as `requirement.md`.

## Feature Workspace Model

Use one feature workspace per behavior-changing feature:

```text
spec.md  = whole feature behavior
product.md = optional feature product understanding
tasks.md = all tasks for the feature
tests.md = whole feature test strategy
plan.md  = current active task/story plan
notes.md = history, evidence, decisions, drift
tasks/   = optional task details in complex artifact mode
tests/   = optional test details in complex artifact mode
plans/   = optional dated plan cycles in complex artifact mode
handoffs/ = optional subagent briefs and returns
contracts.md = optional delivery contract index or compact contract
contracts/ = optional durable producer-consumer contract details
```

For complex projects, `tasks.md`, `tests.md`, and `plan.md` remain stable entry files. When complexity is high, they become indexes that point to `tasks/`, `tests/`, and `plans/` detail files.

## Execution Unit Rules

Default:

```text
single task
```

Allowed with explicit human choice:

```text
single story
```

Allowed only for tiny features with explicit human confirmation:

```text
whole feature
```

## Task Ordering

Use three patterns:

```text
linear   = one task after another
parallel = independent tasks; can run in any order or via subagents
barrier  = verification/human gate before next stage
```

Do not introduce a roadmap graph in v1.

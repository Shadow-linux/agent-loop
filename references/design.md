# Agent Loop Design Reference

Use this reference when the main skill needs definitions, entry scenarios, or flow rules.

## Source Of Truth

This reference is a condensed operational extract of:

```text
draft_agent_loop_struct.md
final_agent_loop_skill_design.md
```

Those two files are the design sources for this skill. If another skill reference conflicts with them, update the reference instead of changing the design model.

The core constraints inherited from the design sources are:

- single-person + CLI agent first
- human controls goals, source requirements, and stage gates
- agent controls workflow mechanics, artifacts, implementation, verification, and backfill
- `agent-loop/` is the default workflow memory root; legacy `.agent-loop/` may be read and migrated only after confirmation
- local remote-entry directories use thin local `agent-loop/remote.md` and `project.md`; full memory should live with the remote source of truth when possible
- root `AGENTS.md` / `CLAUDE.md` are startup guidance artifacts that teach agents to use `agent-loop`
- `project.md` is project-level long-term memory
- Project Memory Mode is `simple` by default; in `enterprise`, `project.md` becomes an index and long-term details move to optional `agent-loop/project/*.md`
- `project.md` owns cross-feature Product Context and Domain Language
- stable Web E2E capability belongs in `project.md`; feature-specific E2E cases belong in feature `tests.md` or `tests/e2e/*`
- `requirements/` stores human source material packages as requirement set directories: requirements, prototypes, feedback, screenshots, recordings, links, and follow-up notes
- requirement-set dates mean archive date only, not deadlines or feature lifecycle dates
- `product.md` is optional feature-level product understanding when needed
- each feature has stable `spec.md`, `tasks.md`, `tests.md`, `plan.md`, `notes.md`; `contracts.md` is added only after human confirmation when producer-consumer boundaries need explicit handoff
- stories live in `spec.md`; optional `tasks/USn/` or `tests/USn/` folders are detail grouping, not separate story workspaces
- tasks live together in `tasks.md` by default; complex artifact mode may add linked detail files under `tasks/`
- `plan.md` is for the active task/story, not the whole feature by default
- submit/integrate is explicit and never commits, opens PRs, merges, or publishes without human confirmation
- Delivery Contracts live in `contracts.md` and optional `contracts/*`; file creation/update, contract acceptance, and breaking changes require human confirmation
- non-trivial human confirmations use table-first Human Review Summary; complete artifacts remain source of truth
- first version does not include multiplayer, roadmap graph, roadmap adapter, tdd-guard, complex ADR, global install, or automatic directory-level AGENTS.md without human confirmation

## Core Model

```text
Human Goal
→ Feature Workspace
→ Task / Test / Plan
→ Execute / Verify
→ Drift Check
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

**Project**: current codebase or repository. Long-term memory lives in `agent-loop/project.md` by default.

**Remote Entry**: local entry directory for a remote project. It stores `agent-loop/remote.md` and a thin `project.md` so future agents can reconnect to the remote source of truth.

**Local Shadow Mode**: fallback when remote project memory cannot be written remotely. Agent-loop artifacts stay local, but every code fact must cite remote evidence.

**Requirement**: human-provided need, goal, document, or natural-language request.

**Prototype**: human-provided design artifact, screenshot, wireframe, or interaction reference.

**Feature**: one behavior-changing work area under `agent-loop/features/<feature-id>/`.

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

## Entry Scenarios

### New Project

Condition:

```text
No agent-loop/
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
Then run Existing Project Onboarding against the remote source of truth.
```

### Existing Project Onboarding

Condition:

```text
Existing code
No agent-loop/
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
agent-loop/ exists
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

### Reconcile Project Context

Condition:

```text
agent-loop/ exists
project.md or feature docs appear stale compared with code reality
```

Also use this path when an old `agent-loop` project is being re-adopted after development happened outside the loop.

Action:

```text
Scan code reality.
Compare with project.md and feature docs.
List differences.
Ask human which updates to accept.
Update project.md or feature docs after confirmation.
Then continue feature work.
```

## Main Flow

```text
Project Entry
→ Remote Project Discovery if Needed
→ Re-Adopt Agent Loop Project if Needed
→ Requirement Archive
→ Product Brief if Needed
→ Brainstorm / Clarify if Needed
→ Targeted Feature Scan if Needed
→ Feature Spec
→ Requirement Checklist
→ Work Breakdown
→ Delivery Contract if Needed
→ Test Design
→ E2E Discovery if Web
→ Technical Design / Code Context
→ Plan if Needed
→ Analyze Consistency
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

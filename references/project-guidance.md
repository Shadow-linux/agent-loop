# Project Guidance

Use this file when initializing/onboarding a project, syncing long-term project rules, or deciding whether `AGENTS.md` / `CLAUDE.md` should exist.

## Core Split

```text
AGENTS.md / CLAUDE.md = agent startup guidance
.agent-loop/project.md = agent-loop project memory
.agent-loop/project/* = optional enterprise project memory details
.agent-loop/remote.md = local entry pointer for remote projects
.agent-loop/features/* = feature execution state
.agent-loop/requirements/<archive-date>-<topic>/* = human source material package
```

Default memory root is `.agent-loop/` because it is workflow metadata, not product code. If a project already has legacy `agent-loop/`, use it for the current run and ask before migration.

Do not use `AGENTS.md` as a task log. Do not use `project.md` as the startup instruction file for every agent.

## Root Agent Bootstrap Gate

Root `AGENTS.md` is the bootstrap node that teaches future agents how to enter `agent-loop`. It is not optional project decoration.

Every time `agent-loop` is used inside a target project, check root guidance before feature work:

```text
1. Read root AGENTS.md if present.
2. Read root CLAUDE.md if present.
3. Check whether CLAUDE.md loads, includes, symlinks to, or clearly points to AGENTS.md.
4. Check whether AGENTS.md contains the required bootstrap sections.
5. Record or update guidance status in project.md.
6. If missing or stale, propose a repair through Human Review Summary.
```

`AGENTS.md` is stale when any of these are missing or contradicted:

- project uses `agent-loop`
- Bootstrap Protocol: inspect `.agent-loop/`, classify the stage, and recommend exactly one next action
- Agent Ownership: agents steer the loop instead of waiting for the human to name every step
- Gate Modes: Strict Mode, Feature Auto-Loop, Task Auto-Run, and their explicit human enablement rules
- Required Stops: unclear scope, risky changes, Delivery Contract gates, subagent dispatch, submit, close, commit, PR, merge, release, publish
- Completion Rules: fresh verification, review, drift check, project memory update, Feature Completion Check, Feature Close Review
- root/directory guidance boundaries and requirement archive rules
- managed block markers are missing for `agent-loop` maintained sections, unless the file is intentionally fully human-owned and the human has deferred managed block adoption

`CLAUDE.md` is stale when it duplicates independent long-lived rules, diverges from `AGENTS.md`, or does not clearly point Claude Code to `AGENTS.md`.

Onboarding, re-adoption, or project initialization is not complete until:

```text
AGENTS.md status = present | created | human-deferred
CLAUDE.md status = points-to-AGENTS | created-pointer | human-deferred
```

If the human defers guidance repair, record the defer decision and reason in `project.md`. Do not silently treat missing root guidance as healthy.

## Root Guidance Default

For Init Project and Existing Project Onboarding, the default recommendation is to create or update:

```text
AGENTS.md
CLAUDE.md -> AGENTS.md
```

Only write after human confirmation.

For any project that is initialized, onboarded, re-adopted, or otherwise managed by `agent-loop`, root guidance must be checked every time the agent enters the project:

```text
AGENTS.md status: present | created | stale | missing | human-deferred
CLAUDE.md status: points-to-AGENTS | created-pointer | stale | missing | human-deferred
```

Onboarding is not complete if root `AGENTS.md` or `CLAUDE.md` is missing or stale unless the human explicitly defers it. Record the decision in `project.md`.

Guidance language should follow the project language when it is clear from existing docs or human preference.

If project language is unclear, default root `AGENTS.md` / `CLAUDE.md` guidance to English for cross-agent compatibility.

If the project uses Chinese or the human explicitly asks for Chinese guidance, write root and directory guidance in Chinese, while keeping stable artifact names, stage names, and file paths in English, such as `agent-loop`, `Requirement Archive`, `Feature Spec`, `Task Auto-Run`, `project.md`, and `requirements/`.

For a local directory that is only a remote-project entry point, create local root guidance only if it helps future agents re-enter the remote workflow. Full project guidance should live in the remote project when remote writes are allowed.

`AGENTS.md` is the primary maintained guidance file. `CLAUDE.md` must not duplicate the full rules. It should load, include, symlink to, or briefly point Claude Code to `AGENTS.md`. If symlinks are unsafe or unsupported, create `CLAUDE.md` with a short pointer to `AGENTS.md`.

Never overwrite an existing ordinary `CLAUDE.md` or `AGENTS.md` without reading it, summarizing the proposed migration, and getting human confirmation.

## Managed Blocks

Use managed blocks to mark content maintained by `agent-loop` inside root `AGENTS.md`:

```md
<!-- agent-loop:managed-start section:<name> source:<path-or-artifact> -->
...
<!-- agent-loop:managed-end section:<name> -->
```

Recommended section names:

```text
bootstrap
ownership
gates
required-stops
completion
artifacts
directory-guidance
architecture
commands
hard-constraints
```

Rules:

- `agent-loop` may propose updates inside managed blocks when the source artifact changes.
- Managed blocks must include `section`; they should include `source` when the content comes from a stable artifact such as `.agent-loop/project.md`, `.agent-loop/project/*.md`, `.agent-loop/onboarding-db/README.md`, or `ARCHITECTURE.md`.
- Content outside managed blocks is human/project-owned. Do not rewrite it automatically.
- If an existing `AGENTS.md` has no managed blocks, propose adding the minimal needed managed blocks instead of replacing the whole file.
- If a managed block source is missing, stale, or contradictory, classify the block as stale and propose either source correction or block refresh through Human Review Summary.
- If marker pairs are broken, duplicated, nested, or ambiguous, stop and ask before editing.
- Do not put task status, feature progress, raw requirements, plans, or test output inside managed blocks.
- `CLAUDE.md` should point to `AGENTS.md`; it should not duplicate managed blocks.

Managed block update flow:

1. Read the existing `AGENTS.md`.
2. Identify managed blocks and their sources.
3. Compare source facts with block content.
4. Present a table with block, source, current summary, proposed change, and risk.
5. Ask human confirmation.
6. Update only approved managed blocks; preserve all other content byte-for-byte where practical.
7. Record guidance status and source evidence in `project.md`.

## Root `AGENTS.md` Should Contain

Keep it short and long-lived:

- project uses `agent-loop`
- Root Agent Bootstrap: read `AGENTS.md`, inspect `.agent-loop/`, classify the current stage, and recommend exactly one next action
- guidance language follows project language; keep stable artifact/stage names in English
- before development, inspect `.agent-loop/`
- if missing, initialize it
- if present, read `.agent-loop/project.md` and active feature docs
- if `project.md` says `Status: remote-entry`, read `.agent-loop/remote.md` and verify the remote project before acting
- if the project used `agent-loop` before but recent development bypassed it, route to Re-Adopt Agent Loop Project before new feature work
- when working in a subdirectory, check for the nearest directory-level `AGENTS.md`
- when creating a new long-lived boundary directory, propose a directory-level `AGENTS.md` before or alongside the directory creation
- keep new human source materials in requirement set directories under `.agent-loop/requirements/`, not flat files
- Agent Ownership: agents steer the loop, classify the current stage, recommend exactly one next action, propose missing artifacts, and own diagnosis, sequencing, verification, drift checks, and project-memory updates
- ask human confirmation before each agent-loop stage
- use table-first Human Review Summary for non-trivial confirmations
- Autonomous Execution After Approval: after explicit Feature Auto-Loop or Task Auto-Run enablement, agents may continue inside the accepted scope through implementation, testing, fixing, review, drift, status update, and final report
- autonomous stop conditions: scope change, ambiguity, unavailable infrastructure, security/data boundary changes, broad architecture changes, repeated verification failure, unrelated dirty work, Delivery Contract creation/acceptance/breaking-change approval, subagent dispatch without explicit approval, submit, close, commit, PR, merge, release, or publish
- run fresh verification before completion claims
- run Feature Completion Check after likely completion, before starting a new feature, or when resuming with an active feature
- perform Feature Close Review, drift check, and project memory update before close
- stable project commands and hard constraints, only if every agent should know them immediately
- managed block markers for `agent-loop` maintained sections, so future updates do not overwrite human-owned content
- stale detection: if future agents cannot learn Agent Ownership, Gate Modes, Required Stops, and Completion Rules from root guidance, propose a root `AGENTS.md` update

## Root `AGENTS.md` Should Not Contain

- current task status
- feature execution logs
- temporary plans
- test output transcripts
- meeting notes
- raw requirements or prototype content
- long duplicated documentation

Those belong in `.agent-loop/` or project docs.

## `project.md` Should Contain

Use `.agent-loop/project.md` for richer memory:

- project summary
- guidance language
- project memory mode: simple | enterprise
- architecture profile: project shape, language adapter, framework adapter, and DDD intensity
- product context
- tech stack
- domain language / glossary
- current capabilities
- evidence and confidence for capabilities, commands, and boundaries
- Current Work
- Active Feature / Paused Features
- Next Suggested Action
- directory map
- directory guidance inventory
- test commands
- onboarding uncertainties
- known constraints
- long-term decisions

In simple mode, `project.md` may contain the long-term project memory body.

In enterprise mode, keep `project.md` short: current work, next suggested action, memory index, and open uncertainties. Put detailed long-term knowledge under `.agent-loop/project/*.md`. Use `project-memory-mode.md` for triggers and routing.

Architecture defaults are DDD-inspired, but code layouts are advisory and stack-adapted. New projects may use a confirmed scaffold. Existing projects should record current structure and framework conventions instead of being reshaped without explicit human approval.

If a rule is both project-critical and needed on every agent startup, summarize it in `AGENTS.md` and keep details in `project.md`.

## Directory-Level Guidance

Suggest directory-level `AGENTS.md` only for long-lived boundaries with their own rules.

Good candidates:

- app roots: `apps/web/`, `backend/`, `frontend/`
- packages with independent APIs or tests: `packages/core/`, `packages/db/`
- test strategy roots: `tests/e2e/`, `tests/api/`
- security/data/runtime boundaries
- plugin or extension roots
- docs roots with their own fact-source rules

Poor candidates:

- single component folders
- ordinary utilities
- feature implementation folders
- temporary migration folders
- directories whose rules duplicate the parent

Ask:

```text
Does this directory have a distinct tech stack?
Does it have distinct verification commands?
Does it define a security/data/architecture boundary?
Does it have dependency direction rules?
Do agents often need special warnings here?
Would this rule still matter next month?
```

If mostly yes, propose a directory `AGENTS.md`. If no, keep the rule in `project.md`, `tasks.md`, or `notes.md`.

## New Directory Creation Rule

When a task creates a new durable directory, classify it before writing guidance:

```text
boundary directory = consider AGENTS.md
ordinary implementation directory = no AGENTS.md
temporary directory = no AGENTS.md
```

Boundary directories include new app roots, package roots, service roots, test roots, plugin roots, security/data/runtime boundaries, and docs roots with their own source-of-truth rules.

If it is a boundary directory:

1. Add or update the directory entry in `.agent-loop/project.md`.
2. Propose a directory-level `AGENTS.md` using `templates/directory-AGENTS.md`.
3. Ask human confirmation before writing it.
4. If declined, record `Guidance: not needed` or `Guidance: deferred` in `project.md`.

Do not create a `CLAUDE.md` in every directory by default. Prefer directory `AGENTS.md`; create a `CLAUDE.md` pointer only if the project explicitly needs Claude-specific discovery there.

## Sync Triggers

During Drift Check, Submit, or Close, ask whether to update `AGENTS.md` only when long-term startup guidance changed:

- package manager or major commands changed
- test/lint/typecheck commands changed
- architecture or dependency direction changed
- directory responsibility changed
- security, auth, data, tenant, or approval boundary changed
- project starts using or stops using a required skill/workflow

Do not sync `AGENTS.md` for normal feature progress.

## Template Use

Use:

```text
templates/root-AGENTS.md
templates/root-CLAUDE.md
templates/directory-AGENTS.md
```

Then adapt to the actual project. Keep each `AGENTS.md` concise and avoid repeating parent content.

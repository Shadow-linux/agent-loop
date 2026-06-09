# Agent Loop Document Templates

Use these templates when creating or refreshing `agent-loop` artifacts. Keep files concise and update them incrementally.

## Directory Layout

```text
AGENTS.md
CLAUDE.md -> AGENTS.md
.agent-loop/
  remote.md optional when local directory is a remote-project entry point
  project.md
  project/ optional enterprise project memory details
    architecture.md
    boundaries.md
    commands.md
    capabilities.md
    product-context.md
    domain-language.md
    testing.md
    environments.md
    guidance-inventory.md
  requirements/
    <archive-date>-<topic>/
      README.md
      requirement.md
      prototype.png
      feedback.md
      design-link.md
    INDEX.md  optional for many requirement sets
  features/
    <date>-<feature-slug>/
      product.md optional
      spec.md
      tasks.md
      tests.md
      plan.md
      notes.md
      contracts.md optional cross-boundary delivery contract index
      tasks/   optional complex details
      tests/   optional complex details
      plans/   optional dated plan cycles
      handoffs/ optional subagent briefs and returns
      contracts/ optional delivery contract details
```

## Shared Document Header

Use a header like this for generated documents:

```md
# <Document Type>: <Name>

Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Status: draft | active | paused | closed

Source Requirements:
- Requirement: <path or Original: path>
- Prototype: <path or Original: path>

Summary:
- <one-line summary>
- <one-line summary>
```

Omit `Source Requirements` when not relevant.

## Human Review Summary

Use `references/human-review-summary.md` before asking the human to approve non-trivial stage output.

Rules:

- the approval view should usually be a Markdown table
- include artifact paths, evidence, risk/blockers, explicit human decision, and next stage
- keep full source-of-truth content in the owning artifact files
- use a short 3-line summary only for trivial changes

## Requirement Rules

Human files do not need correct names. Ask before copying, moving, or renaming.

Requirement archive dates are archive dates only. They are not deadlines, feature duration, or implementation lifecycle dates.

Preferred requirement-set layout:

```text
.agent-loop/requirements/2026-05-26-login/
  README.md
  requirement.md
  prototype.png
  feedback.md
  design-link.md
```

Use `templates/requirement-set-README.md` for the set README.

New requirements should be grouped by requirement set directory. Do not create flat files directly under `requirements/`.

Never silently modify original human requirements. If the human declines normalization, reference the original path in feature docs.

When requirements change, add a new file to the requirement set or create a new requirement set. Do not overwrite the old source requirement material.

Recommend `templates/requirements-index.md` only when there are more than 10 requirement sets, many external paths, shared source requirements, frequent supersession, or the human asks for an inventory.

## Root `AGENTS.md`

Use `templates/root-AGENTS.md`.

Purpose:

- teach future agents to use `agent-loop`
- tell future agents that they own workflow steering instead of waiting for the human to name every next step
- state stable startup rules and core commands
- point task state back to `.agent-loop/`
- explain the active gate modes: Strict Mode, Feature Auto-Loop, and Task Auto-Run
- explain what autonomous execution is allowed to do after Feature Auto-Loop or Task Auto-Run is explicitly enabled
- tell agents to proactively offer auto modes when repeated confirmations slow the human down

Do not put task logs, feature progress, or raw requirements in `AGENTS.md`.

## Root `CLAUDE.md`

Use `templates/root-CLAUDE.md`.

Purpose:

- make Claude Code load the maintained `AGENTS.md`
- avoid maintaining duplicated root guidance
- preserve `AGENTS.md` as the single source of startup guidance for Codex and Claude

`CLAUDE.md` should be a pointer, include, or symlink to `AGENTS.md`. If an existing `CLAUDE.md` contains independent rules, read it, summarize conflicts, and ask the human before replacing or converting it.

## Directory `AGENTS.md`

Use `templates/directory-AGENTS.md` only for long-lived boundaries with distinct rules.

Create after human confirmation. Prefer no file over a duplicated or low-information file.

## Delivery Contracts

Use `templates/contracts.md` only after human confirmation when work crosses a durable producer-consumer boundary such as API, event, public data, UI state/behavior, SDK/library, or runtime behavior.

Use `templates/delivery-contract.md` for detailed contracts under `contracts/`.

Keep `handoffs/` for temporary subagent briefs and returned summaries. Delivery Contracts are durable interface handoffs for downstream consumers.

Human confirmation is required before creating/updating contract files, before a contract becomes `accepted`, and before breaking changes to accepted contracts.

Do not create Delivery Contract files for simple single-person tasks, pure internal logic, or changes with no downstream consumer.

## `remote.md`

Use `templates/remote.md` only when the local directory is a remote-project entry point or local/remote/container execution is ambiguous.

Purpose:

- remember how future agents should find the remote project from the same local directory
- record remote host/path/access, command locations, browser URL, sync model, and permission boundaries
- decide whether project memory lives remotely or in local-shadow mode

Do not put feature execution logs in `remote.md`. Put them in the owning feature `notes.md`.

## `project.md`

```md
# Project Memory

Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Status: active
Memory Mode: simple | enterprise

## Project Summary

Purpose:
Primary users:
Current maturity:
Guidance Language: follow project | English | Chinese | other
Language Evidence:

## Project Memory Index

Mode: simple | enterprise

If simple:
- This file is the main long-term project memory body.

If enterprise:
- Architecture: .agent-loop/project/architecture.md | none
- Boundaries: .agent-loop/project/boundaries.md | none
- Commands: .agent-loop/project/commands.md | none
- Capabilities: .agent-loop/project/capabilities.md | none
- Product Context: .agent-loop/project/product-context.md | none
- Domain Language: .agent-loop/project/domain-language.md | none
- Testing: .agent-loop/project/testing.md | none
- Environments: .agent-loop/project/environments.md | none
- Guidance Inventory: .agent-loop/project/guidance-inventory.md | none

Memory Mode Evidence:
-

## Product Context

Product Positioning:
Target Users:
Core Workflows:
Business Rules:
Cross-Feature Product Constraints:
Out of Scope Across Product:

## Tech Stack

- Runtime:
- Frameworks:
- Package manager:
- Data/storage:
- Test tools:

## Architecture Profile

Project Shape: frontend | backend | fullstack | worker | cli/library | unknown
Language Adapter: java | python | node-ts | go | csharp | rust | cpp | other | unknown
Framework Adapter: spring-boot | fastapi | django | nestjs | express | aspnet-core | rails | laravel | none | other | unknown
DDD Intensity: light | standard | enterprise | unknown
Layout Status: existing reality | proposed scaffold | mixed | unknown
Scaffold Rule:
- Governance scaffold is relatively stable.
- Code layout is a stack-adapted recommendation, not a mandate.
- Existing project structure is not changed without explicit human approval.
Evidence:
Confidence: high | medium | low

## Project Principles

## Domain Language

- `<term>`: <project-specific meaning>

## Development Rules

## Testing Rules

## Current Work

Active Feature:
Paused Features:
Next Suggested Action:
Gate Mode: Strict Mode | Feature Auto-Loop | Task Auto-Run
Gate Mode Scope:
Gate Mode Stop Conditions:

## Remote Entry

Mode: none | remote-entry | local-shadow
Remote Entry File: .agent-loop/remote.md | none
Remote Project Memory:
- Location: remote | local-shadow | undecided | none
- Path:
- Status: unknown | active | blocked

## Environment Map

Local Workspace:
- Path:
- Purpose: primary | remote-entry | mirror | docs-only | edit-workspace | unknown
- Evidence:
- Confidence: high | medium | low

Remote Workspace:
- Host:
- Path:
- Purpose: source-of-truth | runtime | test | deploy | unknown
- Access:
- Evidence:
- Confidence: high | medium | low

Execution Locus:
- Install:
- Build:
- Unit Tests:
- API Tests:
- E2E Tests:
- Dev Server:
- Database:
- Evidence:
- Confidence: high | medium | low

Sync Model:
- Method: direct remote edit | git push/pull | rsync | mounted volume | remote-only | local-only | unknown
- Source of truth:
- Stale risk:

## Capabilities

- `<capability>`:
  - Status: implemented | partial | unknown
  - Evidence:
  - Confidence: high | medium | low

## Directory Map

- `<path>`:
  - Responsibility:
  - Constraints:
  - Useful commands:
  - Evidence:
  - Confidence: high | medium | low
  - Guidance: root only | has AGENTS.md | propose AGENTS.md | not needed | deferred

## Directory Guidance

Root Guidance:
- `AGENTS.md`: present | created | stale | missing | human-deferred
- `CLAUDE.md`: points-to-AGENTS | created-pointer | stale | missing | human-deferred
- Sync Rule: `AGENTS.md` is maintained primary guidance; `CLAUDE.md` loads or points to `AGENTS.md`.

Directory-Level Guidance:
- `<path>/AGENTS.md`: present | proposed | not needed

Creation Rule:
- When creating a new long-lived boundary directory, propose a directory-level `AGENTS.md` and ask for human confirmation before writing it.

## Test Commands

- `<command>`:
  - Verifies:
  - Evidence:
  - Confidence: high | medium | low

## E2E Environment

App Start:
- Command:
- URL:
- Evidence:
- Confidence: high | medium | low

Browser Automation:
- Framework: Playwright | Cypress | none | unknown
- Config:
- Fallback Tool: browser | chrome | computer-use | manual | unknown
- Evidence:
- Confidence: high | medium | low

Auth / Test Data:
- Test Account:
- Seed Command:
- Session Strategy:
- Cleanup:
- Evidence:
- Confidence: high | medium | low

External Services:
- Mocked:
- Real:
- Required Env:
- Evidence:
- Confidence: high | medium | low

## Onboarding Scan

Last Scan:

Read:
- Startup docs:
- Manifests / scripts:
- CI / test configs:
- Boundary files:

Confidence:
- Project purpose:
- Tech stack:
- Capabilities:
- Test commands:
- Directory boundaries:

## Onboarding Uncertainties

- `<uncertainty>`:
  - Evidence:
  - Confidence: low
  - Recommended follow-up:

## Known Constraints

## Long-Term Decisions
```

## `product.md`

Use `templates/product.md` when product intent needs its own layer.

Purpose:

- summarize feature-level product understanding
- preserve user stories, product scope, out of scope, and product decisions
- identify product questions and long-term consensus candidates

Do not use `product.md` as the engineering execution plan.

## `spec.md`

```md
# Feature Spec: <Feature Name>

Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Status: draft

Source Requirements:
- Requirement:
- Prototype:

Product Brief: product.md | none

Summary:
- 

## Problem / Goal

## Scope

## Stories

### US1: <story title>

Why this matters:

Independent test:

Acceptance scenarios:
- Given ..., when ..., then ...

## Acceptance Criteria

## Behavior Changes

### Added

### Modified

### Removed

## Dependencies

## Out of Scope

## Open Questions
```

## `tasks.md`

Use vertical slices / tracer bullets by default, with linear, parallel, and barrier structure instead of a graph.
In complex artifact mode, keep `tasks.md` as the ledger and link detail files under `tasks/`.

```md
# Tasks: <Feature Name>

Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Status: active

## Execution Mode

Mode: linear | parallel | staged-linear | staged-parallel
Default Split: vertical-slice

## Task Mode Legend

- Agent-ready: scope, acceptance, boundaries, and verification are clear enough for autonomous execution.
- Human-gated: product, design, architecture, security, data, or approval decisions are needed before execution.

## Status Rules

- Do not mark a task `done` from code changes alone.
- After implementation and fresh verification, use `Status: review` until Task Done Gate passes.
- Task Done Gate: implementation complete, required tests or substitute verification run fresh, evidence recorded in `notes.md`, lightweight Spec Review recorded, Standards Review recorded when triggered, drift decision recorded, and evidence location named below.

## Split Rules

- Prefer vertical slices / tracer bullets.
- Use horizontal foundation tasks only when a product slice is not yet possible.
- For every horizontal task, explain why and name the future vertical slices that will prove it.

## Stories to Tasks

- US1: T001, T002

## Stage 1: Foundation

- [ ] T001 [US1] <task title>
  - Status: todo
  - Mode: Agent-ready | Human-gated
  - Slice Type: vertical | horizontal-foundation
  - Parent:
  - Depends on:
  - Blocked By:
  - Covers Stories: US1
  - Human Gate:
  - Acceptance:
  - Verification:
  - Evidence:
  - Review:
  - Drift:
  - Detail: tasks/US1/T001-<slug>.md
  - Proved By Future Slices:

Barrier:
- Verification:
- Human confirmation:

## Stage 2: <Name>

Parallel:
- [ ] T002 [US1] <task title>
- [ ] T003 [US2] <task title>

Barrier:
- Verification:
```

## `tests.md`

In complex artifact mode, keep `tests.md` as the matrix and link detail files under `tests/`.

```md
# Test Design: <Feature Name>

Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Status: active

## Requirement Checklist

- [ ] Requirements are testable and unambiguous.
- [ ] Success criteria are measurable.
- [ ] Edge cases are identified.

## Functional Test Cases

- TC001 [US1] <case title>
  - Type:
  - Related Task:
  - Detail: tests/US1/TC001-<slug>.md

## Module Tests

## API Tests

## Web E2E Cases

## E2E Environment Discovery

Project E2E Capability:
- Source: `project.md` `E2E Environment`
- Status: known | partial | unknown

Feature E2E Cases:
- E2E001 [US1] <case title>
  - URL:
  - Preconditions:
  - Test Data:
  - Steps:
  - Assertions:
  - Automation: existing-framework | browser | chrome | computer-use | manual | blocked
  - Detail: tests/e2e/E2E001-<slug>.md
  - Evidence:

Blocked / Manual:
- Case:
- Reason:
- Needed setup:

## Regression Tests

## Manual Verification

## Test Commands
```

## `plan.md`

`plan.md` is the active execution plan for one task or one story. It is not the default whole-feature plan.
In complex artifact mode, keep `plan.md` as the current active pointer and place the full dated plan under `plans/`.

If `plan.md` exists, it must be construction-grade. Load `references/implementation-planning.md` first. Do not write vague implementation notes or placeholders.

```md
# Execution Plan

Plan ID: YYYY-MM-DD-<task-or-story>-<slug>
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Active Since: YYYY-MM-DD
Status: active
Supersedes:

Plan Scope:
- Type: task | story
- ID:
- Title:
- Included Tasks:

Plan Detail:
- Path: plans/YYYY-MM-DD-TNNN-<slug>.md

## Goal

## Architecture Summary

## Technical Context

- Language/Version:
- Frameworks/Libraries:
- Runtime:
- Storage/Data:
- Testing:
- Target Platform:
- Constraints:
- Scale/Scope:

## Source Structure Decision

- Existing structure followed:
- New structure, if any:
- Why this structure:

## Files

- Create:
- Modify:
- Test:
- Read:

## Code Context

Existing functions/classes/modules:
- `<name>` in `<path>`:
  - Signature:
  - Current behavior:
  - Existing callers:

Existing patterns to follow:
- 

Call chain:

Data flow:

Authorization / validation / side effects:

## Interface Contracts

### `<function-or-endpoint-or-component>`

Location:
Kind: function | class | endpoint | component | hook | schema | command
Signature:
Parameters:
- `<name>`:
Return:
Errors:
Side effects:
Existing callers:
New callers:
Tests proving contract:

## Data / API Contract

Request:
Response:
Validation:
Persistence:
Migration:

## Steps

Each step must be bite-sized and executable. If a step changes code, include the actual code or exact edit shape. Do not use placeholders.

- [ ] Step 1: Write failing test

File:

```text
<actual test code>
```

Run:

```text
<exact command>
```

Expected RED:

```text
<expected failure output>
```

- [ ] Step 2: Implement minimal code

File:

```text
<actual implementation code or exact edit shape>
```

- [ ] Step 3: Verify GREEN

Run:

```text
<exact command>
```

Expected GREEN:

```text
<expected passing output>
```

## TDD Plan

### RED

### Verify RED

### GREEN

### Verify GREEN

### Refactor

## Commands

## Expected Outputs

## Risks / Rollback

## Self Review

- Spec coverage:
- Placeholder scan:
- Type/signature consistency:
- Command specificity:
- Risk/rollback coverage:

## Handoff

Next action:
Stop condition:
Evidence to record in notes.md:
```

## Detail Templates

Use copy-ready files:

```text
templates/task-detail.md
templates/test-case.md
templates/plan-cycle.md
templates/subagent-brief.md
templates/product.md
templates/requirement-set-README.md
templates/requirements-index.md
```

## `notes.md`

```md
# Notes: <Feature Name>

Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Status: active

## Human Decisions

## Plan History

- YYYY-MM-DD `<Plan ID>`:
  - Scope:
  - Result:
  - Evidence:
  - Next:

## TDD Cycles

## Verification Evidence

## Diagnosis

## Review

### Spec Review

### Standards Review

## Feature Close Review

### Feature-Level Spec Review

- Date:
- Scope:
- Findings:
- Accepted fixes:

### Feature-Level Standards Review

- Date:
- Trigger: required | not-triggered
- Scope:
- Findings:
- Accepted fixes:

## Submit / Integrate

## Spec Drift

## Feature Completion Check

- Date:
- Result: recommend-close | continue | pause-before-new-feature | update-scope | blocked
- Evidence:
- Feature Close Review:
- Remaining Work:
- Drift:
- Project Memory:
- Submit Status:
- Recommendation:
- Human Decision:

## Checkpoints

## Pause / Resume Point

## Close Record
```

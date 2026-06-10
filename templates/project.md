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

- `<term>`:

## Development Rules

## Testing Rules

## Current Work

Active Feature:
Paused Features:
Next Suggested Action:
Gate Mode: Strict Mode | Feature Auto-Loop | Task Auto-Run
Gate Mode Scope:
Gate Mode Stop Conditions:
Feature Follow-up Lookback: 15 days
Recent Feature Flow-back Policy:
- When bugs, regressions, post-close corrections, field/schema changes, algorithm changes, API mismatches, test failures, or QA/user feedback appear, inspect recent features before creating a new feature.
- Flow back to the owning feature when evidence shows the change repairs, adjusts, or completes that feature.

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

Review Triggers:
- directory responsibility changed
- dependency direction changed
- distinct test command added
- security/data/runtime boundary changed
- new app/package/test root created

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
- Framework:
- Config:
- Fallback Tool:
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

# Tasks: <Feature Name>

Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Status: active

## Execution Mode

Mode: linear | parallel | barrier
Default Split: vertical-slice

## Task Mode Legend

- Agent-ready: scope, acceptance, boundaries, and verification are clear enough for autonomous execution.
- Human-gated: product, design, architecture, security, data, or approval decisions are needed before execution.

## Status Rules

- Do not mark a task `done` from code changes alone.
- After implementation and fresh verification, use `Status: review` until Task Done Gate passes.
- Task Done Gate: implementation complete, required tests or substitute verification run fresh, evidence recorded in `notes.md`, lightweight Spec Review recorded, Standards Review recorded when triggered, drift decision recorded, and evidence location named below.
- Under Gate 2 `review-definition-v2`, only each `T<digits>` checkbox plus its `Status`, `Review`, and `Drift` values are runtime ledger fields. Task identity/order/title, mappings, Mode, dependencies, Human Gate, Acceptance, Verification, evidence location, barriers, risk, interface, and rollback meaning remain protected definition.

## Split Rules

- Prefer vertical slices / tracer bullets.
- Use horizontal foundation tasks only when a product slice is not yet possible.
- For every horizontal task, explain why and name the future vertical slices that will prove it.

## Stories to Tasks

- US1:

## Stage 1: Foundation

- [ ] T001 [US1] <Task title>
  - Status: todo
  - Mode: Agent-ready | Human-gated
  - Slice Type: vertical | horizontal-foundation
  - Parent:
  - Depends on:
  - Blocked By:
  - Covers Stories: US1
  - Design Slices:
  - Human Gate:
  - Acceptance:
  - Verification:
  - Evidence:
  - Review:
  - Drift:
  - Proved By Future Slices:

Barrier:
- Verification:
- Human confirmation:

## Stage 2: <Stage Name>

Parallel:
- [ ] T002 [US1] <Task title>
- [ ] T003 [US2] <Task title>

Barrier:
- Verification:

## Task Details

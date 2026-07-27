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
- AI reviews each `T<digits>` checkbox plus its `Status`, `Review`, and `Drift` values directly and remains responsible for all Task semantics.
- `Gate 2 Agent-ready Tasks` records the initial reviewed decomposition, not an immutable whitelist. A later Agent-ready Task still needs an accepted Story/Product Slice mapping and an exact current `within-approved-boundary` Gate 2 assessment before execution. A new Task ID alone does not repeat Gate 2; a new execution boundary does.
- Use `Derived From` to trace a split or refinement back to an initially reviewed Task. It never substitutes for `Covers Stories`, never authorizes a new Story/Acceptance, and must reference an initially reviewed Task when present.
- When `Gate 2 Plan Evidence` uses `no-plan:<task ID>`, that Task row or its detail must record `No-Plan Decision: accepted`; this is structural evidence only, while the Agent remains responsible for proving no Plan trigger applies.

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
  - No-Plan Decision: accepted | not-applicable
  - Slice Type: vertical | horizontal-foundation
  - Parent:
  - Derived From:
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

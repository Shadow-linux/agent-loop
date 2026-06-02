# Tasks: Project Invite Permissions

Created: 2026-05-26
Updated: 2026-05-26
Status: active

## Execution Mode

Mode: staged-linear
Default Split: vertical-slice

## Task Mode Legend

- Agent-ready: scope, acceptance, boundaries, and verification are clear enough for autonomous execution.
- Human-gated: product, design, architecture, security, data, or approval decisions are needed before execution.

## Stories to Tasks

- US1: T001, T002, T004, T005
- US2: T001, T003, T006
- US3: T004, T005, T007

## Stage 1: Domain And Data Foundation

- [x] T001 [US1, US2] Define invite permission helper
  - Status: done
  - Mode: Agent-ready
  - Slice Type: horizontal-foundation
  - Depends on: existing project roles
  - Covers Stories: US1, US2
  - Human Gate: role vocabulary already accepted in `product.md`
  - Acceptance: manager allowed; editor/viewer denied
  - Verification: module tests for `canInviteProjectMember`
  - Evidence: `notes.md` Verification Evidence, TDD Cycles T001
  - Review: `notes.md` Spec Review T001
  - Drift: `notes.md` Spec Drift T001
  - Proved By Future Slices: T003 API authorization, T006 editor/viewer UI denial

- [x] T002 [US1] Add pending invite persistence
  - Status: done
  - Mode: Agent-ready
  - Slice Type: horizontal-foundation
  - Depends on: T001
  - Covers Stories: US1, US3
  - Human Gate: pending invite is accepted product language in `product.md`
  - Acceptance: pending invite stores project, email, role, inviter
  - Verification: repository tests
  - Evidence: `notes.md` Verification Evidence, TDD Cycles T002
  - Review: `notes.md` Spec Review T002
  - Drift: `notes.md` Spec Drift T002
  - Proved By Future Slices: T004 invite API, T007 pending member UI

Barrier:
- Verification: `pnpm --filter @domain test projectInvite`
- Human confirmation: required before API work

## Stage 2: API Behavior

- [ ] T003 [US2] Enforce invite authorization at API boundary
  - Status: in-progress
  - Mode: Agent-ready
  - Slice Type: vertical
  - Depends on: T001, T002
  - Covers Stories: US2
  - Human Gate: none
  - Acceptance: non-manager requests are forbidden
  - Verification: API tests for manager/editor/viewer
  - Detail: tasks/US2/T003-api-authorization.md

- [ ] T004 [US1] Implement invite creation and acceptance API
  - Status: todo
  - Mode: Agent-ready
  - Slice Type: vertical
  - Depends on: T002, T003
  - Covers Stories: US1
  - Human Gate: none
  - Acceptance: accepted invite creates project membership
  - Verification: API tests for create/accept flow

Barrier:
- Verification: `pnpm --filter @app/web test invite`
- Human confirmation: required before UI work

## Stage 3: Web UI And E2E

Parallel:
- [ ] T005 [US1, US3] Add manager invite modal
  - Status: todo
  - Mode: Human-gated
  - Slice Type: vertical
  - Depends on: T004
  - Covers Stories: US1, US3
  - Human Gate: confirm modal copy and interaction details from prototype
  - Acceptance: manager can create pending invite from UI
  - Verification: browser test

- [ ] T006 [US2] Hide or disable invite controls for editor/viewer
  - Status: todo
  - Mode: Agent-ready
  - Slice Type: vertical
  - Depends on: T003
  - Covers Stories: US2
  - Human Gate: none
  - Acceptance: non-manager cannot see usable invite action
  - Verification: browser test

- [ ] T007 [US3] Show pending and accepted members
  - Status: todo
  - Mode: Agent-ready
  - Slice Type: vertical
  - Depends on: T004
  - Covers Stories: US3
  - Human Gate: none
  - Acceptance: pending and active states render correctly
  - Verification: component/browser tests

Barrier:
- Verification: `pnpm --filter @app/web test:e2e project-invite`
- Human confirmation: required before close

## Task Details

T003 is the current execution unit. It needs a task-scoped plan because it crosses route handlers, fixtures, and API tests.

Delivery Contract:
- `contracts.md`
- `contracts/API001-create-project-invite.md`

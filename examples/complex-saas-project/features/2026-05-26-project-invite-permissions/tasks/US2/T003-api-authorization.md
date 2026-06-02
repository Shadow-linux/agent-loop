# Task Detail: T003 Enforce Invite Authorization

Task ID: T003
Story: US2
Status: in-progress
Mode: Agent-ready
Slice Type: vertical
Created: 2026-05-26
Updated: 2026-05-26

Index:
- Tasks: ../../tasks.md
- Tests: ../../tests.md
- Active Plan: ../../plan.md

## Goal

Reject project invite creation from editor and viewer roles at the API boundary while preserving manager success.

## Boundaries

- API: `apps/web/src/routes/projects/[id]/invites.ts`
- Domain: `canInviteProjectMember`
- Tests: API tests for manager/editor/viewer

## Files

- Create:
  - `apps/web/src/routes/projects/[id]/invites.test.ts`
- Modify:
  - `apps/web/src/routes/projects/[id]/invites.ts`
  - `apps/web/test/fixtures/projectRoles.ts`
- Read:
  - existing project role fixtures
  - existing invite route handler

## Code Context

Existing functions/classes/modules:
- `canInviteProjectMember(role)` in `packages/domain/src/projectPermissions.ts`:
  - Signature: `(role: "manager" | "editor" | "viewer") => boolean`
  - Current behavior: true for manager, false for editor/viewer
  - Existing callers: domain permission tests
- `POST(request)` in `apps/web/src/routes/projects/[id]/invites.ts`:
  - Signature: `(request: Request) => Promise<Response>`
  - Current behavior: creates pending invite before role authorization
  - Existing callers: route tests and browser flow

Existing patterns to follow:
- Use project role fixtures from `apps/web/test/fixtures/projectRoles.ts`.
- Return 403 before persistence for authorization failure.

Call chain:
`POST(request)` -> read current project role -> `canInviteProjectMember(role)` -> create invite only when allowed.

Data flow:
invite request payload -> authorization check -> pending invite persistence.

Authorization / validation / side effects:
Authorization happens before persistence; editor/viewer requests create no pending invite rows.

## Interface Contracts

### `POST /api/projects/:id/invites`

Location: `apps/web/src/routes/projects/[id]/invites.ts`
Kind: endpoint
Request: authenticated project invite request
Response: `201` for manager success, `403` for editor/viewer
Validation: existing payload validation remains unchanged
Persistence: only manager requests create pending invite rows
Authorization: `canInviteProjectMember(currentProjectRole)`
Tests proving contract: API001 manager success, API002 editor/viewer forbidden

## Acceptance

- Manager invite request succeeds.
- Editor invite request returns forbidden.
- Viewer invite request returns forbidden.

## Verification

```text
pnpm --filter @app/web test invite
```

## Related Tests

- API001: manager invite succeeds
- API002: editor/viewer forbidden

## Handoff

Owner: current agent or confirmed subagent.
Stop condition: route authorization context cannot determine project role.
Evidence to record: RED output, GREEN output, task status, drift decision.

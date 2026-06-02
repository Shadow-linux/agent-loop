# Plan Cycle: 2026-05-26-T003-invite-authorization

Plan ID: 2026-05-26-T003-invite-authorization
Created: 2026-05-26
Updated: 2026-05-26
Active Since: 2026-05-26
Status: active
Supersedes: none

Scope:
- Type: task
- ID: T003
- Detail Task: tasks/US2/T003-api-authorization.md
- Related Tests: API001, API002

Index:
- Current Plan: ../plan.md
- Task Ledger: ../tasks.md
- Notes: ../notes.md

## Goal

Make the invite creation API reject editor/viewer requests while preserving manager success.

## Architecture Summary

Authorization is enforced at the invite route boundary before persistence. The route reuses the shared project-role permission helper so backend behavior matches the product rule in `product.md`.

## Technical Context

- Language/Version: TypeScript
- Frameworks/Libraries: Next.js route handler, app web test runner
- Runtime: web API route
- Storage/Data: pending invite persistence from T002
- Testing: focused API tests
- Target Platform: web app
- Constraints: preserve manager success; editor/viewer must not create pending invites

## Files / Boundaries

- Create:
  - `apps/web/src/routes/projects/[id]/invites.test.ts`
- Modify:
  - `apps/web/src/routes/projects/[id]/invites.ts`
  - `apps/web/test/fixtures/projectRoles.ts`
- Read:
  - existing auth helper
  - existing project role fixtures
- Verify:
  - `pnpm --filter @app/web test invite`

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
- Use `apps/web/test/fixtures/projectRoles.ts` for role-specific request context.
- Return 403 before persistence for authorization failure.

Call chain:
`POST(request)` -> read current project role -> `canInviteProjectMember(role)` -> create invite only when allowed.

Data flow:
invite request payload -> authorization check -> pending invite persistence.

Authorization / validation / side effects:
Authorization must precede invite persistence. Forbidden requests have no database side effect.

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

## TDD Steps

### RED

Add API tests for manager success and editor/viewer forbidden:

```ts
it.each(["editor", "viewer"] as const)("rejects %s invite creation", async (role) => {
  const ctx = await createProjectRoleFixture({ role });
  const res = await POST(ctx.inviteRequest);
  expect(res.status).toBe(403);
});
```

### Verify RED

Run:

```text
pnpm --filter @app/web test invite
```

Expected RED:

```text
FAIL rejects editor invite creation
Expected: 403
Received: 201
```

### GREEN

Use `canInviteProjectMember` before invite creation:

```ts
if (!canInviteProjectMember(currentProjectRole)) {
  return forbiddenResponse();
}
```

### Verify GREEN

Run:

```text
pnpm --filter @app/web test invite
```

Expected GREEN:

```text
PASS invite
```

### Refactor

Only reduce duplicated fixture setup if tests remain green.

## Commands

```text
pnpm --filter @app/web test invite
```

## Risks / Rollback

- Risk: route-level auth helper may not expose project role.
- Rollback: keep tests, revert implementation, record blocker in `notes.md`.

## Self Review

- Spec coverage: US2 non-manager denial and manager preservation are covered.
- Placeholder scan: no TBD/TODO/fill-in placeholders.
- Type/signature consistency: role union matches project permission helper.
- Command specificity: focused invite test command is recorded.
- Risk/rollback coverage: route auth context risk is recorded.

## Handoff

Next action: ask human confirmation to execute T003.
Stop condition: authorization context unavailable or focused API test fails for unexpected reason.
Evidence to record: RED output, GREEN output, Spec Review, Standards Review if triggered, drift decision, and Task Done Gate status update.

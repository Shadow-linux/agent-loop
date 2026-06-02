# Execution Plan

Plan ID: 2026-05-26-T003-invite-authorization
Created: 2026-05-26
Updated: 2026-05-26
Active Since: 2026-05-26
Status: active
Supersedes: none

Plan Scope:
- Type: task
- ID: T003
- Title: Enforce invite authorization at API boundary
- Included Tasks: T003

Plan Detail:
- Path: plans/2026-05-26-T003-invite-authorization.md

## Goal

Make the invite creation API reject editor/viewer requests while preserving manager success.

## Architecture Summary

Authorization is enforced at the route boundary before invite creation. The API uses the shared project-role permission helper so UI hiding remains advisory and backend authorization is authoritative.

## Technical Context

- Language/Version: TypeScript
- Frameworks/Libraries: Next.js route handler, project domain permission helper, app web test runner
- Runtime: web API route
- Storage/Data: pending invite persistence already exists from T002
- Testing: focused API tests with project role fixtures
- Target Platform: web app
- Constraints: preserve manager success, do not broaden editor/viewer permissions
- Scale/Scope: one API route plus focused fixtures/tests

## Source Structure Decision

- Existing structure followed: route handler and tests stay under `apps/web/src/routes/projects/[id]/`.
- New structure, if any: none.
- Why this structure: current route ownership and fixtures already live in the web app boundary.

## Files

- Create:
  - `apps/web/src/routes/projects/[id]/invites.test.ts`
- Modify:
  - `apps/web/src/routes/projects/[id]/invites.ts`
  - `apps/web/test/fixtures/projectRoles.ts`
- Test:
  - `pnpm --filter @app/web test invite`
- Read:
  - `packages/domain/src/projectPermissions.ts`
  - `apps/web/test/fixtures/projectRoles.ts`

## Code Context

Existing functions/classes/modules:
- `canInviteProjectMember(role)` in `packages/domain/src/projectPermissions.ts`:
  - Signature: `(role: "manager" | "editor" | "viewer") => boolean`
  - Current behavior: returns true for manager and false for editor/viewer
  - Existing callers: domain tests from T001
- `POST(request)` in `apps/web/src/routes/projects/[id]/invites.ts`:
  - Signature: `(request: Request) => Promise<Response>`
  - Current behavior: creates pending invite without project-role authorization
  - Existing callers: route tests and browser flow

Existing patterns to follow:
- Use project role fixtures from `apps/web/test/fixtures/projectRoles.ts`.
- Return 403 for authorization failure before persistence.

Call chain:
`POST(request)` -> load project role from request context -> `canInviteProjectMember(role)` -> create invite only when allowed.

Data flow:
request project id and email/role payload -> authorization check -> pending invite creation.

Authorization / validation / side effects:
Authorization must happen before persistence. Editor/viewer requests must not create pending invite rows.

## Interface Contracts

### `canInviteProjectMember`

Location: `packages/domain/src/projectPermissions.ts`
Kind: function
Signature: `canInviteProjectMember(role: "manager" | "editor" | "viewer"): boolean`
Parameters:
- `role`: project role for the current user
Return: true only when role is `manager`
Errors: none
Side effects: none
Existing callers: domain permission tests
New callers: invite creation route
Tests proving contract: API tests for manager success and editor/viewer forbidden

### `POST /api/projects/:id/invites`

Location: `apps/web/src/routes/projects/[id]/invites.ts`
Kind: endpoint
Request: authenticated request with project id and invite payload
Response: `201` for manager success, `403` for editor/viewer
Validation: existing invite payload validation remains unchanged
Persistence: creates pending invite only after authorization passes
Authorization: `canInviteProjectMember(currentProjectRole)`

## Steps

- [ ] Step 1: Write failing API tests for editor/viewer denial.

File: `apps/web/src/routes/projects/[id]/invites.test.ts`

```ts
it.each(["editor", "viewer"] as const)("rejects %s invite creation", async (role) => {
  const ctx = await createProjectRoleFixture({ role });
  const res = await POST(ctx.inviteRequest);
  expect(res.status).toBe(403);
});
```

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

- [ ] Step 2: Add route-level permission check before invite creation.

File: `apps/web/src/routes/projects/[id]/invites.ts`

```ts
if (!canInviteProjectMember(currentProjectRole)) {
  return forbiddenResponse();
}
```

- [ ] Step 3: Verify GREEN for manager/editor/viewer API behavior.

Run:

```text
pnpm --filter @app/web test invite
```

Expected GREEN:

```text
PASS invite
```

- [ ] Step 4: Record RED/GREEN evidence in `notes.md` and update T003 status in `tasks.md`.

## TDD Plan

### RED

Add forbidden API tests for editor and viewer.

### Verify RED

Focused API test fails for the expected authorization gap.

### GREEN

Use `canInviteProjectMember` before invite creation.

### Verify GREEN

Focused API test passes.

### Refactor

Only refactor fixture setup if tests stay green.

## Commands

```text
pnpm --filter @app/web test invite
```

## Expected Outputs

- Editor/viewer invite requests return 403.
- Manager invite request still returns created pending invite.

## Risks / Rollback

- Risk: route-level auth helper may not expose project role.
- Rollback: keep tests, revert implementation, record blocker in `notes.md`.

## Self Review

- Spec coverage: US2 non-manager denial is covered by API tests.
- Placeholder scan: no TBD/TODO/fill-in placeholders.
- Type/signature consistency: role union matches project permission helper.
- Command specificity: focused web invite test command is recorded.
- Risk/rollback coverage: missing route auth context has rollback note.

## Handoff

Next action: ask human confirmation to execute T003.
Stop condition: authorization context unavailable or focused API test fails for an unexpected reason.
Evidence to record in notes.md: RED output, GREEN output, Spec Review, Standards Review if triggered, drift decision, and Task Done Gate status update.

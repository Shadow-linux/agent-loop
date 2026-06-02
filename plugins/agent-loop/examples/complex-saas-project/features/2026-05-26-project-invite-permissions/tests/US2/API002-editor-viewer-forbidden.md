# Test Case: API002 Editor Viewer Forbidden

Test ID: API002
Story: US2
Related Task: T003
Type: api
Status: active
Created: 2026-05-26
Updated: 2026-05-26

Index:
- Test Matrix: ../../tests.md
- Task Ledger: ../../tasks.md

## Purpose

Prove that non-manager project members cannot create project invitations.

## Scenario

Given: an authenticated project editor or viewer
When: they call `POST /api/projects/:id/invites`
Then: the API returns forbidden and no pending invite is created

## Test Data

- seeded manager user
- seeded editor user
- seeded viewer user
- target project with existing roles

## Automation

File: `apps/web/src/routes/projects/[id]/invites.test.ts`
Command:

```text
pnpm --filter @app/web test invite
```

## Expected Evidence

- RED: test fails before API authorization is added.
- GREEN: test passes after route checks `canInviteProjectMember`.

## Notes

Pair with API001 to ensure manager success is preserved.

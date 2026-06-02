# Delivery Contract: API001 Create Project Invite

Created: 2026-05-26
Updated: 2026-05-26
Status: accepted

Contract ID: API001
Type: API
Producer: Backend invite API
Consumers: Web project members page
Feature: project invite permissions
Related Stories: US2
Related Tasks: T003
Source Requirements:
- `../../requirements/2026-05-26-project-invite/README.md`
Supersedes:

## Purpose

Allow managers to invite new project members while preventing editors and viewers from creating invites.

## Business Behavior

Managers can create pending invites. Editors and viewers receive a permission error and no invite is created.

## Interface

Endpoint / Event / Signature / UI State / Runtime Expectation:

```text
POST /api/projects/:projectId/invites
```

## Request Or Input

```json
{
  "email": "teammate@example.com",
  "role": "editor"
}
```

## Response Or Output

Success:

```json
{
  "invite_id": "inv_123",
  "invite_status": "pending",
  "email": "teammate@example.com",
  "role": "editor"
}
```

Permission error:

```json
{
  "error": "forbidden",
  "message": "Only project managers can create invites."
}
```

## Errors

- `403 forbidden`: actor is editor or viewer.
- `422 invalid_email`: email is malformed.
- `409 duplicate_invite`: pending invite already exists.

## Authentication And Permissions

Requires an authenticated project member. Actor must have manager role for the project.

## Side Effects And State Semantics

Successful request creates a pending invite. Failed permission checks do not create an invite.

## Compatibility

Breaking Change: no
Affected Consumers: Web project members page
Consumer Scan Evidence: planned frontend members page and API002 test matrix
Compatibility Window: current feature only
Deprecation Date:
Rollout Order: backend API contract accepted before frontend implementation
Migration Notes:

Human Confirmation:
- Impact Presented: yes
- Confirmed After Impact Review: yes
- Decision: accepted current response shape

## Producer Verification

Commands:
- `pnpm --filter @app/api test invites`

Evidence:
- Pending, to be recorded in `notes.md` after implementation.

## Consumer Notes

Frontend should render `invite_status: pending` as a pending invite row. Do not rename `invite_status` without breaking-change review.

## Change History

| Date | Change | Compatibility | Human Decision | Evidence |
|---|---|---|---|---|
| 2026-05-26 | Initial accepted contract | non-breaking | accepted | `contracts.md` decision |


# Test Design: Project Invite Permissions

Created: 2026-05-26
Updated: 2026-05-26
Status: accepted

## Requirement Checklist

- [x] Manager invite behavior is measurable.
- [x] Non-manager denial behavior is measurable.
- [x] Pending and active membership states are measurable.
- [x] Billing and real email delivery are explicitly out of scope.

## Functional Test Cases

- Manager invites a new email as editor.
- Invitee accepts pending project invite.
- Manager sees pending invite before acceptance.
- Manager sees active member after acceptance.
- Editor cannot invite.
- Viewer cannot invite.

## Module Tests

- `canInviteProjectMember(manager)` returns true.
- `canInviteProjectMember(editor/viewer)` returns false.
- Invite role validator rejects unknown roles.

## API Tests

- API001 [US1] `POST /api/projects/:id/invites` succeeds for manager.
- API002 [US2] `POST /api/projects/:id/invites` returns forbidden for editor/viewer.
  - Detail: tests/US2/API002-editor-viewer-forbidden.md
- `POST /api/projects/:id/invites/:token/accept` creates membership.
- Duplicate pending invite returns conflict.

## Web E2E Cases

- Manager creates invite and sees pending row.
- Editor opens members tab and cannot invite.
- Invitee accepts invite and appears as active member after refresh.

## E2E Environment Discovery

Project E2E Capability:
- Source: `project.md` `E2E Environment`
- Status: partial

Feature E2E Cases:
- E2E001 [US1] manager creates invite and sees pending row
  - URL: `http://localhost:3000/projects/:id/members`
  - Preconditions: seeded manager user, project membership, mocked email transport.
  - Test Data: seeded project and invite target email.
  - Steps: login as manager, open members tab, create invite, assert pending row.
  - Assertions: pending invite row shows invited email and selected role.
  - Automation: existing-framework
  - Detail: tests/e2e/E2E001-manager-invite-pending.md
  - Evidence: existing Playwright suite pattern in `tests/e2e/`.
- E2E002 [US2] editor cannot invite
  - URL: `http://localhost:3000/projects/:id/members`
  - Preconditions: seeded editor user and project membership.
  - Test Data: seeded project.
  - Steps: login as editor, open members tab.
  - Assertions: invite action is absent and direct API attempt is covered by API002.
  - Automation: existing-framework
  - Detail: tests/e2e/E2E002-editor-cannot-invite.md
  - Evidence: feature needs one browser path for web-visible permission behavior.

Blocked / Manual:
- Case: invitee accepts invite from email link
- Reason: needs confirmed local token capture helper or mocked email outbox inspection path.
- Needed setup: identify existing test outbox API or seed a known invite token before automating.

## Regression Tests

- Existing project member list still renders current members.
- Organization admin permissions are not broadened.

## Manual Verification

- Inspect members UI at desktop and mobile widths.
- Confirm invite modal labels match prototype notes.

## Test Commands

```text
pnpm --filter @domain test projectInvite
pnpm --filter @app/web test invite
pnpm --filter @app/web test:e2e project-invite
pnpm typecheck
```

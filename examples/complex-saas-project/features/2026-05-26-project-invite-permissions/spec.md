# Feature Spec: Project Invite Permissions

Created: 2026-05-26
Updated: 2026-05-26
Status: accepted

Source Requirements:
- Requirement: `.agent-loop/requirements/2026-05-26-project-invite/requirement.md`
- Prototype: `.agent-loop/requirements/2026-05-26-project-invite/prototype.md`

Product Brief: product.md

Summary:
- Add project-scoped invitations with role selection and authorization.

## Problem / Goal

Project managers need a safe way to invite collaborators into a project without granting organization-wide admin privileges.

## Scope

- Project invite API.
- Permission rules for manager/editor/viewer.
- Pending invite model and acceptance path.
- Members UI invite modal and pending state.
- Browser verification for manager success and editor denial.

## Stories

### US1: Manager can invite a project member

Why this matters:
- Teams can add collaborators without organization admin intervention.

Independent test:
- A manager invites a new email with an editor role and sees a pending invite.

Acceptance scenarios:
- Given a project manager, when they invite an email, then a pending invite is created.
- Given a pending invite, when the recipient accepts, then project membership is created with the selected role.

### US2: Non-managers cannot invite

Why this matters:
- Project access cannot be escalated by ordinary members.

Independent test:
- An editor attempts to invite and receives a forbidden response.

Acceptance scenarios:
- Given a project editor, when they call invite API, then the API returns forbidden.
- Given a project viewer, when they open members UI, then invite controls are unavailable.

### US3: Members UI reflects pending and active membership

Why this matters:
- Managers need visibility into pending invitations and accepted members.

Independent test:
- Browser flow shows pending row before acceptance and active member after acceptance.

Acceptance scenarios:
- Given a pending invite, when manager opens members tab, then pending state is visible.
- Given an accepted invite, when manager refreshes members tab, then active member is visible.

## Acceptance Criteria

- API enforces manager-only invite creation.
- Invite acceptance creates project membership with selected role.
- Pending invite is visible in project members UI.
- Browser verification covers manager success and editor denial.
- No billing seat-limit behavior is added in this feature.

## Behavior Changes

### Added

- Project invitation creation.
- Project invitation acceptance.
- Pending invite display in members UI.

### Modified

- Project members page gains invite modal for managers.
- Permission model gains `canInviteProjectMember`.

### Removed

- None.

## Dependencies

- Existing auth/session handling.
- Project role model.
- Local seeded users for E2E.

## Out of Scope

- Real email delivery.
- Billing seat limits.
- Organization-wide invitation redesign.

## Open Questions

- Should pending invites expire after a fixed time? Deferred.

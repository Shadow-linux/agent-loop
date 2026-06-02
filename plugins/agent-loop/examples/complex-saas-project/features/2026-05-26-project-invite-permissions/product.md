# Product Brief: Project Invite Permissions

Created: 2026-05-26
Updated: 2026-05-26
Status: accepted

Source Requirements:
- Requirement: `agent-loop/requirements/2026-05-26-project-invite/requirement.md`
- Prototype: `agent-loop/requirements/2026-05-26-project-invite/prototype.md`

Summary:
- Let project managers invite collaborators without granting organization-wide admin rights.
- Keep invitation visibility and authorization scoped to a project.
- Defer billing seat limits and real email delivery.

## Problem Statement

Project managers need to add collaborators to a project while preserving tenant isolation and role-based access boundaries.

## Target Users / Actors

- Project manager
- Project editor
- Project viewer
- Invited collaborator

## Solution Summary

Managers can create pending project invites with a selected role. Invitees can accept an invite and become project members. Editors and viewers cannot create invites, and the UI must not expose usable invite actions to them.

## User Stories

### US1: Manager can invite a project member

As a project manager, I want to invite a collaborator with a project role, so that I can expand the team without organization admin intervention.

### US2: Non-managers cannot invite

As a project member without manager rights, I must be prevented from inviting others, so that project access cannot be escalated.

### US3: Members UI reflects pending and active membership

As a project manager, I want to see pending and active members, so that I can understand invite progress.

## Product Scope

- Project-scoped invite creation.
- Project-scoped invite acceptance.
- Manager/editor/viewer invite authorization.
- Pending and active member visibility in the members UI.

## Out Of Scope

- Billing seat limits.
- Real email delivery.
- Organization-wide invitation management.
- Invite expiration.

## Product Decisions

- Decision: Only project managers can create project invites.
  - Reason: invitation authority is project-local and should not depend on organization admin privileges.
  - Applies To: future features

- Decision: UI hiding is not sufficient; API authorization is required.
  - Reason: project access is security-sensitive and must be enforced server-side.
  - Applies To: future features

## Terminology

- `project manager`:
  - Meaning in this feature: project role allowed to create invites.
  - Promote to project Domain Language: yes

- `pending invite`:
  - Meaning in this feature: invitation created but not yet accepted by the recipient.
  - Promote to project Domain Language: yes

## Open Product Questions

- Question: Should project invites expire?
  - Recommended answer: not in this release; track as future product scope.
  - Blocks: none

## Long-Term Product Consensus Candidates

- Candidate: invitation authority is enforced at API/service boundaries.
  - Why it may affect future features: all member-management flows need the same enforcement rule.
  - Suggested project.md section: Product Context | Known Constraints

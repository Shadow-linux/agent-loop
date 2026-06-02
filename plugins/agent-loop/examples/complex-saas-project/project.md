# Project Memory

Created: 2026-05-26
Updated: 2026-05-26
Status: active
Memory Mode: simple

## Project Summary

B2B SaaS workspace app with authenticated web UI, organization-scoped projects, billing, role-based access, and background sync jobs.

## Project Memory Index

Mode: simple

If simple:
- This file is the main long-term project memory body for the example.

Memory Mode Evidence:
- Example shows large-project operating behavior, but keeps project memory simple for readability.

## Product Context

Product Positioning: collaborative project workspace for organization teams.
Target Users: organization owners, project managers, editors, viewers, and invited collaborators.
Core Workflows: create projects, manage project membership, control role-based access, review billing status, and run background sync jobs.
Business Rules: tenant isolation is mandatory; project access is scoped by organization membership and project role.
Cross-Feature Product Constraints: UI affordances may guide users, but backend authorization is the durable enforcement point.
Out of Scope Across Product: unaudited access changes and organization-wide privilege escalation from project-local flows.

## Project Principles

- Tenant isolation is a product invariant.
- Permission checks belong in service/API boundaries, not only in the UI.
- Every behavior-changing feature needs module/API coverage and at least one browser path when web-visible.
- Human-provided requirements, prototypes, feedback, links, and other source materials stay immutable in requirement set directories under `agent-loop/requirements/`.

## Development Rules

- Default execution unit is one task.
- Use story execution only when the human explicitly chooses it.
- Use TDD for module/API behavior and browser-first verification for user-visible flows.
- Record every cross-cutting behavior change in `project.md`.

## Testing Rules

- Module tests: domain services, permission helpers, billing calculations.
- API tests: route handlers and tenant/role authorization.
- Web E2E: critical user flows with browser automation.
- Background jobs: deterministic worker tests with fake queues/clocks.

## Current Work

Active Feature: `agent-loop/features/2026-05-26-project-invite-permissions/`
Paused Features:
- `agent-loop/features/2026-05-18-billing-invoices/` paused after API tests; needs browser invoice download case.

Next Suggested Action:
- Continue `2026-05-26-project-invite-permissions` at `Analyze Consistency`, then execute `T003`.

## Capabilities

- Email/password authentication.
- Organization membership and project membership.
- Project dashboard with owner/admin/member roles.
- Basic billing subscription status.

## Directory Map

- `apps/web/`: Next.js web app and route handlers.
- `packages/domain/`: shared domain services and permission helpers.
- `packages/db/`: schema, migrations, repository layer.
- `packages/jobs/`: background workers.
- `tests/e2e/`: browser test suites.

## Test Commands

- `pnpm test`
- `pnpm --filter @app/web test`
- `pnpm --filter @app/web test:e2e`
- `pnpm typecheck`

## E2E Environment

App Start:
- Command: `pnpm --filter @app/web dev`
- URL: `http://localhost:3000`
- Evidence: `apps/web/package.json` scripts and existing E2E README.
- Confidence: medium

Browser Automation:
- Framework: Playwright
- Config: `apps/web/playwright.config.ts`
- Fallback Tool: browser | chrome
- Evidence: existing `tests/e2e/` suites and `pnpm --filter @app/web test:e2e`.
- Confidence: medium

Auth / Test Data:
- Test Account: seeded manager, editor, viewer, and invitee users.
- Seed Command: `pnpm --filter @app/web seed:test`
- Session Strategy: login through seeded UI account or storage state if the existing suite provides it.
- Cleanup: E2E database reset in test setup.
- Evidence: current browser tests require local seeded users.
- Confidence: low

External Services:
- Mocked: invitation emails.
- Real: local web app and database.
- Required Env: local app environment plus test database variables.
- Evidence: project constraint says invitation emails are mocked in local tests.
- Confidence: medium

## Known Constraints

- Existing browser tests require local seeded users.
- Billing code is not part of the current feature.
- Invitation emails are mocked in local tests.

## Long-Term Decisions

- Project access is determined by organization membership plus project role.
- Invite acceptance must be auditable.
- UI may hide actions, but backend authorization remains mandatory.

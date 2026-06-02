# Notes: Project Invite Permissions

Created: 2026-05-26
Updated: 2026-05-26
Status: active

## Human Decisions

- Billing seat limits are out of scope for this feature.
- Real email delivery is out of scope; local tests use mocked invite delivery.
- Default execution unit remains task, not whole feature.

## Plan History

- 2026-05-26 `2026-05-26-T001-T002-domain-foundation`:
  - Scope: tasks T001 and T002.
  - Result: completed foundation stage.
  - Evidence: domain project invite tests passed.
  - Next: prepare T003 API authorization plan.

- 2026-05-26 `2026-05-26-T003-invite-authorization`:
  - Scope: active task T003.
  - Result: active, not completed.
  - Evidence: pending.
  - Next: ask human confirmation, then execute T003 with TDD.

## TDD Cycles

### T001

- RED: permission helper tests failed because helper did not exist.
- GREEN: manager/editor/viewer helper tests passed after adding helper.

### T002

- RED: repository test failed because pending invite model was missing.
- GREEN: repository test passed after adding pending invite persistence.

### T003

- Planned; not yet completed.

## Verification Evidence

```text
pnpm --filter @domain test projectInvite
Result: passed for T001/T002 foundation tests
```

## Diagnosis

- No active failure. T003 plan notes possible risk around route auth context.

## Review

### Spec Review

- T001: helper behavior matches accepted role vocabulary and foundation acceptance.
- T002: pending invite persistence matches accepted invite product language.
- T003: pending. Before marking T003 `done`, compare implementation against `product.md`, `spec.md`, acceptance criteria, and out-of-scope decisions.

### Standards Review

- Pending. Required for this large project because the feature crosses domain, API, DB, and web UI boundaries.

## Spec Drift

- T001: no drift; helper is a foundation task proved by later vertical slices.
- T002: no drift; persistence is a foundation task proved by later vertical slices.

## Spec Drift

- Found: prototype implied invite expiration, but requirement did not include it.
- Decision: record expiration as deferred open question, not current acceptance.

## Checkpoints

- Stage 1 completed.
- Stage 2 ready, current execution unit T003.

## Pause / Resume Point

Resume by reading `plan.md`, then ask human confirmation to execute T003.

## Close Record

Not closed.

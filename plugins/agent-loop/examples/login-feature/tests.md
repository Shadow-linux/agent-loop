# Test Design: Login

Created: 2026-05-26
Updated: 2026-05-26
Status: accepted

## Requirement Checklist

- US1 login success is measurable.
- US2 error states are measurable.
- US3 session persistence is measurable.

## Module Tests

- Validate credential parsing.
- Validate session creation helper.

## API Tests

- `POST /api/login` returns success for valid credentials.
- `POST /api/login` returns clear error for invalid credentials.

## Web E2E Cases

- User enters valid credentials and lands on dashboard.
- User enters invalid password and sees inline error.
- User refreshes after login and remains authenticated.

## Commands

```text
npm test
npm run test:e2e
```

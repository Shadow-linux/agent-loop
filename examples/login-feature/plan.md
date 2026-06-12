# Active Plan

Plan ID: 2026-05-26-T003-login-form-states
Created: 2026-05-26
Updated: 2026-05-26
Active Since: 2026-05-26
Status: closed
Supersedes: none

## Scope

Unit: task
ID: T003
Title: Add failing test for invalid login error

## Goal

Add the failing browser-visible test for the invalid login error state.

## TDD Plan

1. RED: add browser test for invalid login error.
2. VERIFY RED: confirm the test fails because no stable error appears.
3. STOP: implementation belongs to T004 after this task is accepted.

## Commands

```text
npm run test:e2e -- login
```

## Expected Evidence

- Failing browser test before implementation.
- Notes entry with command output summary.

## Handoff

Next action: feature close already recorded in notes.
Stop condition: none.
Evidence to record in notes.md: already recorded.

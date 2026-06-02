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
Title: Implement login form states

## Goal

Add the browser-visible form behavior for success, failure, loading, and session redirect.

## TDD Plan

1. RED: add browser test for invalid login error.
2. VERIFY RED: confirm test fails because no error appears.
3. GREEN: implement error rendering.
4. VERIFY GREEN: run browser test.
5. REFACTOR: clean state handling without changing behavior.

## Commands

```text
npm run test:e2e -- login
```

## Expected Evidence

- Failing browser test before implementation.
- Passing browser test after implementation.
- Notes entry with command output summary.

## Handoff

Next action: feature close already recorded in notes.
Stop condition: none.
Evidence to record in notes.md: already recorded.

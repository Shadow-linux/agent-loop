# E2E Discovery

Use this when a feature has web-visible behavior or when Test Design mentions Web E2E/browser verification.

## Principle

E2E is discovered from project reality, not predefined by the skill.

Do not assume:

- Playwright, Cypress, browser-use, Chrome, or computer-use is available
- local URL or port
- login state, test account, seed command, or database reset command
- CI behavior
- external services are mocked

First discover, then design, then execute.

## Discovery Sources

Inspect likely sources:

- root and directory `AGENTS.md` / `CLAUDE.md`
- `project.md` Test Commands and E2E Environment
- README, CONTRIBUTING, docs, test docs
- `package.json` scripts and workspace scripts
- Playwright/Cypress/Vitest/browser config
- `tests/e2e`, `e2e`, `cypress`, `playwright`, or browser test directories
- seed/fixture/factory files
- `.env.example`, local env docs, docker compose, dev server docs
- CI workflows

## Record Locations

Project-level stable E2E capability goes in `.agent-loop/project.md`:

```md
## E2E Environment

App Start:
- Command:
- URL:
- Evidence:
- Confidence: high | medium | low

Browser Automation:
- Framework:
- Config:
- Fallback Tool:
- Evidence:
- Confidence:

Auth / Test Data:
- Test Account:
- Seed Command:
- Session Strategy:
- Cleanup:
- Evidence:
- Confidence:

External Services:
- Mocked:
- Real:
- Required Env:
- Evidence:
- Confidence:
```

Feature-level E2E design goes in `.agent-loop/features/<feature>/tests.md`:

```md
## E2E Environment Discovery

Project E2E Capability:
- Source: .agent-loop/project.md
- Status: usable | partial | blocked | unknown

Feature E2E Cases:
- E2E001 [US1] <case title>
  - URL:
  - Preconditions:
  - Test Data:
  - Steps:
  - Assertions:
  - Automation: existing-framework | browser | chrome | computer-use | manual | blocked
  - Evidence to record:

Blocked / Manual:
- Case:
  - Reason:
  - Needed setup:
```

If complex artifact mode is active, detail cases live under:

```text
tests/e2e/E2E<nnn>-<slug>.md
```

## Automation Decision

Classify each E2E case:

- `existing-framework`: use project Playwright/Cypress/Vitest/browser tests
- `browser`: use available in-app browser automation for local targets
- `chrome`: use user Chrome when cookies/session/profile are required
- `computer-use`: use local desktop/browser UI when no browser framework exists
- `manual`: human/browser check required but evidence can be recorded
- `blocked`: environment, auth, data, or external service setup is missing

Prefer existing project test framework when it exists and is runnable. Use browser/computer tools only as fallback or supplementary verification.

## Execution Evidence

Record evidence in `notes.md`:

- command or browser tool used
- URL and viewport if relevant
- account/session strategy
- seed/reset command
- pass/fail result
- screenshot/log path when available
- observed drift or blocker

## Failure Routing

When E2E fails, classify before fixing:

- product/spec mismatch -> Drift Check / Feature Spec update
- implementation bug -> Diagnose Failure
- test flake/timing -> Diagnose Failure with stability focus
- environment/setup issue -> update `project.md` E2E Environment or mark blocked
- missing fixture/account/seed -> Test Design update or Human-gated decision

# Human Acceptance

Use this stage after `Feature Completion Check` and before `Pause / Close` when a feature needs human-performed manual verification before it can be closed.

## Purpose

Automated verification and agent-run review can miss user-visible behavior, integration seams, auth/session flows, billing edge cases, and other critical paths that only a human can exercise realistically. This stage forces a structured, recorded human acceptance step before close.

The agent generates the cases; the human executes them. The agent may not sign off on behalf of the human, even in Feature Auto-Loop.

## Entry

Enter from `Feature Completion Check` when:

- `Feature Completion Check` recommends Human Acceptance, **or**
- the feature has user-visible Web/UI/CLI behavior changes, **or**
- the feature touches cross-service / cross-module integration boundaries, API contracts, events, or message flows, **or**
- the feature touches auth, permissions, billing, security-critical paths, **or**
- automated verification cannot cover the real user journey (e.g., needs real browser environment, external callbacks, human approval flows), **or**
- a task/story verification was marked `manual` or `blocked`, **or**
- the human explicitly requested manual acceptance during Feature Spec or Test Design.

If none of the above apply and `Feature Completion Check` does not recommend Human Acceptance, skip this stage and route directly to `Pause / Close`.

## Load

- `feature-completion-check.md`
- `human-review-summary.md`
- active feature `tests.md`
- active feature `spec.md`
- active feature `notes.md`
- `skill-routing.md` for Stage Helper Capability Scan
- `external-skill-adapters.md` when Stage Helper Capability Scan finds verification, finishing, or handoff helpers

## Rules

- before fallback human acceptance preparation, run Stage Helper Capability Scan; when a matching helper is available, use it only for case-structuring discipline or close-options support while keeping human execution/sign-off under agent-loop control
- determine whether Human Acceptance Test Cases are required using the Entry triggers above
- if required, generate or update `Human Acceptance Test Cases` in `tests.md` (or `tests/human-acceptance.md` in complex artifact mode)
- each case must include: ID, scenario, preconditions, steps, expected result, evidence to record, and a human sign-off cell
- cases should focus on critical paths, user-visible behavior, integration seams, and anything that automated tests cannot confidently cover
- present the cases in a Human Review Summary table before asking the human to execute them
- the human must execute the cases and report the result; the agent may assist but may not execute or sign off on the human's behalf
- if a case fails, route to `Diagnose Failure`, `Execute Task / Story`, or `Feature Spec` update instead of close
- if a case is blocked, record the blocker, mark the feature `Human-gated`, and recommend `Pause` or scope update
- if the human wants to waive human acceptance, record the explicit waiver reason, risk, and human approval in `notes.md`; waiver is not allowed for security, auth, billing, or explicitly human-required acceptance
- even in Feature Auto-Loop, human execution and sign-off cannot be skipped

## Write

- update `tests.md` with the `## Human Acceptance Test Cases` section
- in complex artifact mode, write `tests/human-acceptance.md` and link it from `tests.md`
- record the human acceptance result in `notes.md`

## Exit

- all cases passed and signed off -> recommend `Pause / Close`
- case(s) failed -> route to `Diagnose Failure` or `Execute Task / Story`
- case(s) blocked -> mark `Human-gated`, recommend `Pause` or scope update
- waived with recorded risk and explicit human approval -> recommend `Pause / Close`

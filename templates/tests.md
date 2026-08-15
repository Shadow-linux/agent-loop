# Test Design: <Feature Name>

Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Status: active

AI reviews current top-level `Updated` / `Status`, Design Slice matrix `Status`, and Bug matrix `Result` / `Evidence Link` values directly and owns test semantics.

## Requirement Checklist

- [ ] Requirements are testable and unambiguous.
- [ ] Success criteria are measurable.
- [ ] Edge cases are identified.

## Core Invariants

One row per stable invariant the Feature must preserve. Depth follows the recorded Feature Verification Profile tier: `focused` may merge this into the minimum effective set; `high-assurance` requires complete coverage with boundary cases.

| Invariant ID | Invariant | Source (Spec / Requirement / ADR) | Verified By |
|---|---|---|---|
| INV-00 |  |  |  |

## Test Oracle

Each case names its expected result, the authority that expectation comes from, and an oracle quality check that it maps to an invariant or acceptance item with no pass-green-but-core-unverified gap (for example, testing only the positive path while the invariant forbids an actor-specific action).

| Case | Expected (Oracle) | Oracle Source | Oracle Quality Check |
|---|---|---|---|
|  |  |  |  |

## Design Slice Verification Matrix

| Design Slice ID | Required Verification | Test / Evidence | Status |
|---|---|---|---|
| DS-00 |  |  | planned / verified / blocked |

## Bug Verification Matrix

Use only when this Feature resolves one or more Bug Records.

| Bug ID | Expected Behavior Evidence | Original Reproduction | Regression / Safety Verification | Result | Evidence Link |
|---|---|---|---|---|---|

## Functional Test Cases

## Module Tests

## API Tests

## Web E2E Cases

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

## Regression Tests

## Manual Verification

## Test Commands

# Feature Spec: Approval Review Slice

Status: accepted
Feature Type: normal

## Product Requirement Source

Requirement Set: tests/fixtures/adaptive-product-definition/standard-valid
Effective Product Definition: product.md
Product Definition Profile: standard
Product Review Evidence: confirmed by human maintainer on 2026-07-22
Applicable Decisions: none

## Product Slice

| Source Section / Model ID | Feature Responsibility | Acceptance Mapping | Coverage |
|---|---|---|---|
| C-REQUEST / C-OPERATOR / REL-OPERATOR-REQUEST | preserve request and reviewer meanings | reviewer scenario | in-scope |
| PERM-APPROVE / CMD-APPROVE / EVT-APPROVED | authorize and expose approval | approval acceptance | in-scope |
| FLOW-SUBMIT / FLOW-APPROVE / STATE-REQUEST | implement the reviewed journey and terminal | flow acceptance | in-scope |
| PM-APPROVAL / EX-REJECTED / product.md#approval-authority | preserve approval fact and rejection direction | negative acceptance | in-scope |

## Problem / Goal

Implement the confirmed approval-review Product Slice without redefining source semantics.

## Scope

- Submission and authorized review behavior from the accepted Product Slice.

## Acceptance Criteria

- Only an authorized operator can approve a pending request.
- Submission alone is never reported as approval.

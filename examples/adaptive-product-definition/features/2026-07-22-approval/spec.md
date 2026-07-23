# Feature Spec: Approval Notice Slice

Status: accepted
Feature Type: normal

## Product Requirement Source

Requirement Set: examples/adaptive-product-definition/requirements/2026-07-22-approval
Effective Product Definition: product.md
Product Definition Profile: standard
Product Review Evidence: confirmed by human maintainer on 2026-07-22
Applicable Decisions: none

## Product Slice

| Source Section / Model ID | Feature Responsibility | Acceptance Mapping | Coverage |
|---|---|---|---|
| C-APPROVER | preserve the accepted approver meaning in display behavior | approver identity acceptance | in-scope |
| product.md#goal-expected-product-outcome | expose one approval notice without adding product state | observable notice acceptance | in-scope |

## Problem / Goal

Implement only the accepted approval-notice Product Slice.

## Scope

- Show the requester an observable notice after the existing approval result.

## Acceptance Criteria

- The notice is associated with the existing approver meaning.
- The Feature does not invent a new request state or authorization rule.

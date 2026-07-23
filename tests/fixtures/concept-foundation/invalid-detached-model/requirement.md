# Requirement: Approval Instance

Concept Foundation Status: accepted
Not-Needed Reason: n/a

## Concept Foundation

Approval Instance is distinct from the approval action.

## Concept Definitions

| Concept ID | Canonical Name |
|---|---|
| C-APPROVAL-INSTANCE | Approval Instance |
| C-REVIEWER | Reviewer |

## Concept Relationships

| Relationship ID | From Concept ID | Relationship | To Concept ID |
|---|---|---|---|
| REL-01 | C-REVIEWER | reviews | C-APPROVAL-INSTANCE |

### Human Confirmation

- Confirmed Concept IDs: C-APPROVAL-INSTANCE, C-REVIEWER

## Role / Permission Matrix

| Role Concept ID | Product Object Concept ID | Read |
|---|---|---|
| C-REVIEWER | C-APPROVAL-INSTANCE | yes |

## Commands / Events

| Action ID | Actor / Producer Concept ID | Target Concept ID |
|---|---|---|
| CMD-APPROVE | C-REVIEWER | C-APPROVAL-INSTANCE |

## Primary Business Flow

| Flow Step ID | Actor Concept ID | Action ID | Input / Target Concept IDs |
|---|---|---|---|
| FLOW-01 | C-REVIEWER | CMD-APPROVE | C-APPROVAL-INSTANCE |

## Product State Model

| State Model ID | State-bearing Concept ID | Action / Event ID |
|---|---|---|
| STATE-01 | C-APPROVAL-INSTANCE | CMD-APPROVE |

## Requirement Product Model

| Product Model ID | Concept IDs | Product Fact Meaning |
|---|---|---|
| PM-01 | C-APPROVAL-INSTANCE, C-REVIEWER | accepted approval lifecycle |

## Concept-To-Product Traceability

| Trace ID | Accepted Concept IDs | Derived Model IDs / Sections |
|---|---|---|
| TRACE-01 | C-APPROVAL-INSTANCE, C-REVIEWER | REL-01 / CMD-APPROVE / FLOW-01 / STATE-01 / PM-01 |

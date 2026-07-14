# Requirement Document: Validator Fixture

Concept Foundation Status: accepted

## Concept Definitions

| Concept ID | Canonical Name | Definition |
|---|---|---|
| C-FIXTURE-SUBJECT | FixtureSubject | accepted subject meaning |
| C-FIXTURE-OPERATOR | FixtureOperator | accepted operator meaning |

## Concept Relationships

| Relationship ID | From Concept ID | To Concept ID | Meaning |
|---|---|---|---|
| REL-FIXTURE-LINK | C-FIXTURE-OPERATOR | C-FIXTURE-SUBJECT | accepted relationship |

## Role / Permission Matrix

| Permission Rule ID | Role Concept ID | Product Object Concept ID | Permission Meaning |
|---|---|---|---|
| PERM-FIXTURE-ACTION | C-FIXTURE-OPERATOR | C-FIXTURE-SUBJECT | operator may perform the accepted fixture action |

## Commands / Events

| Action ID | Actor / Producer Concept ID | Target Concept ID | Meaning |
|---|---|---|---|
| CMD-FIXTURE-ACTION | C-FIXTURE-OPERATOR | C-FIXTURE-SUBJECT | perform_fixture_action |
| EVT-FIXTURE-RECORDED | C-FIXTURE-SUBJECT | C-FIXTURE-SUBJECT | accepted outcome event |

## Primary Business Flow

| Flow Step ID | Actor Concept ID | Action ID | Product Meaning |
|---|---|---|---|
| FLOW-FIXTURE-01 | C-FIXTURE-OPERATOR | CMD-FIXTURE-ACTION | accepted flow step |

## Product State Model

| State Model ID | Concept IDs | Trigger Action ID | Product Meaning |
|---|---|---|---|
| STATE-FIXTURE-01 | C-FIXTURE-SUBJECT | EVT-FIXTURE-RECORDED | accepted state transition |

## Requirement Product Model

| Product Model ID | Concept IDs | Kind | Product Meaning / Invariant |
|---|---|---|---|
| PM-FIXTURE-FACT | C-FIXTURE-SUBJECT | fact | accepted product invariant |

## Exception Paths

| Scenario ID | Concept / State / Action IDs | Trigger | Expected Handling |
|---|---|---|---|
| EX-FIXTURE-01 | C-FIXTURE-SUBJECT / STATE-FIXTURE-01 / CMD-FIXTURE-ACTION | fixture action cannot complete | preserve the accepted subject state and expose the failure |

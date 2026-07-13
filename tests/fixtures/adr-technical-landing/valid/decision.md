# ADR-9000: Validator Fixture

Status: accepted
Allowed Status: proposed | accepted | superseded | deprecated

## Effective Requirement Snapshot

Effective Concept Source: requirement.md
Concept Foundation Status: accepted
Accepted Concept IDs: C-FIXTURE-SUBJECT, C-FIXTURE-OPERATOR
Accepted Requirement Model IDs: REL-FIXTURE-LINK, PERM-FIXTURE-ACTION, CMD-FIXTURE-ACTION, EVT-FIXTURE-RECORDED, FLOW-FIXTURE-01, STATE-FIXTURE-01, PM-FIXTURE-FACT, EX-FIXTURE-01
Upstream Compatibility: current
Last Compatibility Check: 2026-07-13
Trace Applicability: required

## Requirement Model Scope Inventory

| Requirement Model Ref | Scope Disposition | Owner / Reason |
|---|---|---|
| REL-FIXTURE-LINK | in-scope | ADR-9000 |
| PERM-FIXTURE-ACTION | in-scope | ADR-9000 |
| CMD-FIXTURE-ACTION | in-scope | ADR-9000 |
| EVT-FIXTURE-RECORDED | in-scope | ADR-9000 |
| FLOW-FIXTURE-01 | in-scope | ADR-9000 |
| STATE-FIXTURE-01 | in-scope | ADR-9000 |
| PM-FIXTURE-FACT | in-scope | ADR-9000 |
| EX-FIXTURE-01 | in-scope | ADR-9000 |

## Requirement Model Technical Landing Trace

| Requirement Model Ref | Accepted Meaning / Constraint | Disposition | Technical Landing | Preserved Invariant | Design Slice | Verification |
|---|---|---|---|---|---|---|
| REL-FIXTURE-LINK | source relationship reference | landed | FixtureProtocol boundary | relationship invariant reference | DS-FIXTURE-REL | fixture verification target |
| PERM-FIXTURE-ACTION | source permission reference | landed | FixtureProtocol authorization boundary | permission invariant reference | DS-FIXTURE-PERM | fixture permission verification |
| CMD-FIXTURE-ACTION | source command reference | covered-by-accepted-decision | decisions/8999-shared.md (ADR-8999) | accepted decision invariant | none | accepted decision evidence |
| EVT-FIXTURE-RECORDED | source event reference | feature-local | features/fixture/spec.md | feature-local invariant | none | feature verification target |
| FLOW-FIXTURE-01 | source flow reference | not-applicable | reason: outside this coherent decision boundary | none | none | none |
| STATE-FIXTURE-01 | source state reference | landed | FixtureStore state representation | state invariant reference | DS-FIXTURE-STATE | fixture verification target |
| PM-FIXTURE-FACT | source product-model reference | landed | FixtureStore fact representation | product invariant reference | DS-FIXTURE-PM | fixture verification target |
| EX-FIXTURE-01 | source exception reference | landed | FixtureProtocol failure boundary | exception invariant reference | DS-FIXTURE-EX | fixture exception verification |

## Operational Landing Trigger Assessment

| Concern | Status | Reason / Trigger Evidence | Detail Section If Triggered |
|---|---|---|---|
| Migration / Backfill | triggered | existing representation changes | Migration Detail |
| Compatibility | not-triggered | no external compatibility change | none |
| Rollout / Cutover | not-triggered | no staged activation change | none |
| Rollback / Reversibility | not-triggered | existing reversal path remains valid | none |

## Triggered Operational Landing

### Migration Detail

Fixture migration evidence.

## Design Slice Coverage

| Design Slice ID | Required Capability / Rule | Owning Feature(s) | Verification | Coverage Status |
|---|---|---|---|---|
| DS-FIXTURE-REL | relationship landing | fixture feature | fixture verification target | planned |
| DS-FIXTURE-PERM | permission boundary landing | fixture feature | fixture permission verification | planned |
| DS-FIXTURE-STATE | state landing | fixture feature | fixture verification target | planned |
| DS-FIXTURE-PM | product-model landing | fixture feature | fixture verification target | planned |
| DS-FIXTURE-EX | exception boundary landing | fixture feature | fixture exception verification | planned |

## Coverage Hard Gate

- [x] Effective Concept Source resolves and matches the reviewed source
- [x] Concept Foundation Status is accepted or reasoned `concept-foundation-not-needed`
- [x] Upstream Compatibility is `current`
- [x] Every source Requirement Model ID has an explicit scope disposition, or trace is reasoned not-applicable
- [x] Every in-scope Accepted Requirement Model ID has exactly one disposition
- [x] Every `landed` row has Technical Landing, Preserved Invariant, Design Slice, and Verification
- [x] Every `covered-by-accepted-decision` and `feature-local` row names an existing or explicitly planned verified owner path
- [x] Every `not-applicable`, deferred, and out-of-scope item is visible in Human Review Summary
- [x] Every implementation-bearing technical rule is represented in Design Slice Coverage
- [x] No required Design Slice is `unassigned`
- [x] No unresolved product-semantic blocker remains

## Human Review Evidence

Decision: accepted
Confirmed By: fixture human reviewer
Confirmed At: 2026-07-13
Evidence: explicit fixture acceptance recorded after structural preflight validation

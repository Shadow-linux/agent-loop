# ADR-0000: <Decision And Design Title>

Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Status: proposed
Allowed Status: proposed | accepted | superseded | deprecated
Scope: project | cross-feature

Source Requirements:
- Requirement:
- Requirement README:

## Effective Requirement Snapshot

Effective Product Source:
Product Definition Profile: brief | standard
Product Review: confirmed
Accepted Concept IDs:
Accepted Requirement Model IDs:
Accepted Product Rule References:
Upstream Compatibility: current | review-required
Last Compatibility Check:
Trace Applicability: required | not-applicable
Trace Not-Applicable Reason:

Resolve the Requirement Set README effective-source pointer before drafting and again before acceptance. New work uses the fields above. A legacy `Effective Concept Foundation` reader may instead retain `Effective Concept Source` and `Concept Foundation Status` without migration. Never use both forms in one snapshot. This snapshot references accepted product meaning; it does not copy or redefine it. `review-required` is a dependency judgment, not an ADR lifecycle status. For a confirmed Brief with no stable model IDs/Product Rule references, or a reasoned legacy `concept-foundation-not-needed` source, set both accepted-ID fields and Product Rule references to `none`, set trace applicability to `not-applicable`, give a concrete reason, and omit the two model tables below. For a confirmed Standard source, an accepted-ID field may be `none` only when the source declares no IDs of that kind; any accepted Product Rule reference keeps trace applicability `required` and must be covered below.

Applies To:
- Product area:
- Features:
- Project memory:

Supersedes:
Superseded By:

## Requirement And Decision Context

| Item | Description |
|---|---|
| Source Requirement |  |
| Current Project State |  |
| Problem To Solve |  |
| Decision Needed |  |
| Affected Features |  |

## Goals And Non-Goals

| Goal | Target / Meaning | Verification |
|---|---|---|
|  |  |  |

Non-Goals:
- 

## Domain Concepts

Reference accepted PRD / Requirement Product Model semantics. Do not create, rename, split, merge, or redefine product concepts in this record; return to Requirements Discussion if product meaning must change.

| Accepted Concept / Product Model Reference | Accepted Product Meaning Summary | Design Responsibility | Product Fact Owner / Decision Candidate |
|---|---|---|---|
| C-... / PM-... | link or concise unchanged meaning |  |  |

## Requirement Model Scope Inventory

Account for every stable Requirement Model ID and every accepted Product Rule section anchor in the effective source before selecting this ADR's coherent scope. Stable source IDs include `REL-*`, `PERM-*`, `CMD-*`, `EVT-*`, `FLOW-*`, `STATE-*`, `PM-*`, and `EX-*`; Product Rules use resolvable references such as `product.md#approval-authority`, never a fabricated `RULE-*` namespace.

| Requirement Model Ref | Scope Disposition | Owner / Reason |
|---|---|---|
|  | in-scope / covered-by-accepted-decision / feature-local / proposed-decision / not-applicable |  |

Rules:
- `in-scope` names `this ADR` or its ADR ID; exactly these IDs appear in `Accepted Requirement Model IDs` and the Technical Landing Trace
- `covered-by-accepted-decision` names an existing accepted decision Markdown path
- `feature-local` names an existing Feature Spec path, or an explicit future path such as `planned:features/<feature-id>/spec.md`
- `proposed-decision` names an existing decision draft or an explicit future path such as `planned:decisions/<id>.md`
- `not-applicable` begins with `reason:` and gives a concrete product-neutral scope reason
- no source Requirement Model ID or accepted Product Rule reference may be silently omitted

## Requirement Model Technical Landing Trace

Give every accepted Requirement Model ID and Product Rule reference declared in this ADR scope exactly one disposition. Do not create product meaning in this table; return to Requirements Discussion when accepted meaning is missing or ambiguous.

| Requirement Model Ref | Accepted Meaning / Constraint | Disposition | Technical Landing | Preserved Invariant | Design Slice | Verification |
|---|---|---|---|---|---|---|
|  | link or concise unchanged meaning | landed / covered-by-accepted-decision / feature-local / not-applicable |  |  |  |  |

Allowed dispositions:

```text
landed | covered-by-accepted-decision | feature-local | not-applicable
```

Rules:
- `landed` requires a concrete Technical Landing, Preserved Invariant, Design Slice, and Verification target
- `covered-by-accepted-decision` names the existing accepted decision Markdown path that owns the landing
- `feature-local` names an existing Feature Spec path or an explicit `planned:features/<feature-id>/spec.md` owner path and must not hide a shared constraint
- `not-applicable` gives a concrete reason and is shown at the ADR Human Gate

## Business Flow

```text
Step 1
-> Step 2
-> Step 3
-> Final state
```

| Step | Actor | Action | State Change | Failure / Compensation |
|---|---|---|---|---|
|  |  |  |  |  |

## Options Considered

| Option | Design Summary | Meets Goals | Advantages | Disadvantages | Decision |
|---|---|---|---|---|---|
| A |  |  |  |  | chosen / rejected |
| B |  |  |  |  | chosen / rejected |

## Decision

We will:

- 

## Technical Architecture Design

### Technology Choices

| Area | Choice | Why | Alternatives Rejected | Risk / Mitigation |
|---|---|---|---|---|
|  |  |  |  |  |

### Component Responsibilities

| Component | Responsibility | Owns | Does Not Own |
|---|---|---|---|
|  |  |  |  |

### Data Model And Source Of Truth

This technical-design section must preserve accepted product meaning. Selecting tables, stores, events, ledgers, or providers belongs to Decision & Design after its Human Gate; it never authorizes a product-definition change.

| Data Object | Purpose | Source Of Truth | Key Fields | Invariant |
|---|---|---|---|---|
|  |  |  |  |  |

### Interfaces And Protocols

| Interface | Producer | Consumer | Contract | Failure / Retry |
|---|---|---|---|---|
|  |  |  |  |  |

### Transaction And Consistency Boundaries

| Boundary | In Transaction | Outside Transaction | Consistency Model |
|---|---|---|---|
|  |  |  | strong / eventual |

### Idempotency And Concurrency

| Scenario | Idempotency Key | Concurrency Control | Expected Behavior |
|---|---|---|---|
|  |  |  |  |

### Failure Recovery And Compensation

| Failure | Detection | Recovery / Compensation | Owner | Evidence |
|---|---|---|---|---|
|  |  |  |  |  |

## Non-Functional Design

| Concern | Design | Trade-off | Verification / Metric |
|---|---|---|---|
| Stability |  |  |  |
| High Availability |  |  |  |
| Performance |  |  |  |
| Data Consistency |  |  |  |
| Security / Risk |  |  |  |
| Observability |  |  |  |

## Operational Landing Trigger Assessment

Assess all concerns, but expand detail only for `triggered` rows. A `not-triggered` row records one concrete reason and does not create an empty operational section.

Allowed trigger status: `triggered | not-triggered`.

| Concern | Status | Reason / Trigger Evidence | Detail Section If Triggered |
|---|---|---|---|
| Migration / Backfill | triggered / not-triggered |  |  |
| Compatibility | triggered / not-triggered |  |  |
| Rollout / Cutover | triggered / not-triggered |  |  |
| Rollback / Reversibility | triggered / not-triggered |  |  |

When at least one row is `triggered`, add a `Triggered Operational Landing` section containing only the named detail subsections. When every concern is `not-triggered`, do not add that section.

## Design Slice Coverage

Turn every implementation-bearing flow step, invariant, recovery responsibility, and non-functional target into a stable Design Slice ID.

| Design Slice ID | Required Capability / Rule | Owning Feature(s) | Verification | Coverage Status |
|---|---|---|---|---|
| DS-01 |  |  |  | unassigned / planned / implemented / verified / deferred / out-of-scope |

Coverage rules:
- no required slice remains `unassigned` before Feature Spec
- every owning feature copies its assigned slice IDs into `spec.md` `Implements Decisions`
- `deferred` or `out-of-scope` requires an explicit human decision
- update this table when feature scope or ownership changes

## Coverage Hard Gate

Before acceptance and before dependent Feature Spec work:

- [ ] Effective Product Source or legacy Effective Concept Source resolves and matches the reviewed source
- [ ] Product Review is confirmed, or legacy Concept Foundation Status is accepted or reasoned `concept-foundation-not-needed`
- [ ] Upstream Compatibility is `current`
- [ ] Every source Requirement Model ID and accepted Product Rule reference has an explicit scope disposition, or trace is reasoned not-applicable
- [ ] Every in-scope Accepted Requirement Model ID and Product Rule reference has exactly one disposition
- [ ] Every `landed` row has Technical Landing, Preserved Invariant, Design Slice, and Verification
- [ ] Every `covered-by-accepted-decision` and `feature-local` row names an existing or explicitly planned verified owner path
- [ ] Every `not-applicable`, deferred, and out-of-scope item is visible in Human Review Summary
- [ ] Every implementation-bearing technical rule is represented in Design Slice Coverage
- [ ] No required Design Slice is `unassigned`
- [ ] No unresolved product-semantic blocker remains

`Applicable Decisions` is not a substitute for this coverage.

Run the structural validator while the ADR is still `proposed`. Then present the Decision & Design Human Review Summary. Only after explicit human acceptance may the Agent set `Status: accepted`, record the evidence below, and rerun accepted-mode validation.

## Optional Visual Evidence

Remove this section when unused. A working render stays outside this table: use it only under a Visual Scope Grant, then rewrite accepted meaning into the ADR. Durable evidence requires separate confirmation and cannot accept the ADR.

Visual Manifest Contract: source-render-v1

| Diagram ID | Review Question | Semantic References | Source Definition | Render | Type | Source SHA-256 | Render SHA-256 | Generator | Validation Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| D-... | one concrete technical review question | accepted Product Concept/Model IDs, Product Rule refs, or `decision.md#section-anchor` | visuals/name.workflow.json | visuals/name.html | architecture / workflow / sequence / dataflow / lifecycle | 64 lowercase hex | 64 lowercase hex | archify@x.y | validate=pass; check=pass | current |

The typed source and render are a derived explanation of accepted product semantics and this ADR's proposed technical design. Missing files, mismatched hashes/type/output, unknown semantic references, or stale status fail validation. Remove the example row before use.

## Human Review Evidence

Populate this section only after explicit human acceptance. Leave the ADR `proposed` while these fields are absent or incomplete.

Decision:
Confirmed By:
Confirmed At:
Evidence:

## Upstream Compatibility And Drift

Compatibility Comparison:

| Item | Previous Effective Source | Current Effective Source | Impact | Required Action |
|---|---|---|---|---|
| Concept / Requirement Model IDs |  |  | none / compatible / incompatible | retain / update snapshot after review / supersede |

Rules:
- an effective-source or accepted-model change sets `Upstream Compatibility: review-required` before new dependent Feature Spec, Plan, or implementation work
- compatible technical decisions may refresh snapshot/trace only after Decision & Design Human Review
- incompatible accepted decisions require a new superseding ADR
- never rewrite accepted decision meaning in place

## Closure And Verification Plan

| Requirement / Goal | Verification Method | Evidence Location |
|---|---|---|
|  |  |  |

Required evidence before close:
- 

## Consequences

Positive:
- 

Negative:
- 

Operational Burden:
- 

Open / Follow-up:
- 

## Relationship Mapping

Source Requirements:
- 

Applicable Decisions:
- 

Triggered By:
- 

Implemented By:
- 

Related Decisions:
- 

Project Memory Updates:
- 

# Decision & Design / ADR Lane

Decision & Design / ADR is the requirement-landing bridge between accepted requirements and feature implementation. It turns shared business-flow, domain, data, architecture, recovery, and non-functional needs into one coherent design before feature stories fragment the work.

```text
Requirement Product Definition -> Design Readiness Check -> Decision & Design If Needed -> Feature Mapping -> Feature Spec Product Slice
```

Requirement explains what humans want and how success is recognized. Decision & Design explains how the complete requirement can work across features and which shared rules every feature must preserve. Feature artifacts implement and verify assigned design slices.

PRD / Requirement Product Model owns product meaning. ADR consumes accepted product semantics and is responsible for later technical landing; it must not redefine accepted Concept IDs, identity, lifecycle, relationships, invariants, product states, terminal meaning, or product fact ownership.

Concept Foundation and Requirement Product Model do not choose tables, stores, event topics, providers, or other technical representations. Decision & Design may select those representations only after requirement acceptance and through its own Human Gate, while preserving accepted product meaning.

Design Readiness Check is a required method at Requirement Record / Archive and Feature Spec boundaries; it is not a standalone stage. A legacy Feature Product Brief may trigger the same check during Resume or Follow-up, but new work does not author one.

Decision Scan / Placement remains a lightweight method inside Decision & Design. It decides where a decision belongs; it is not the whole design stage.

A decision file remains globally optional but becomes conditionally required when shared design is required and no accepted decision already covers it. Creating or accepting that file remains Human-gated.

This lane is not a complex ADR system. It adds one stable destination for long-term or cross-feature decision records:

```text
.agent-loop/decisions/
```

Creating `.agent-loop/decisions/` does not enable enterprise memory mode. The directory is available in simple and enterprise memory modes.

## Re-entry And Discovery

`project.md` records whether `.agent-loop/decisions/` exists so future agents can rediscover accepted project decisions in simple or enterprise memory mode.

Before Decision & Design or Feature Spec:

1. Read decision links already named by the active requirement, `product.md`, or `spec.md`.
2. List `.agent-loop/decisions/*.md` filenames and statuses when the project Decisions index is present.
3. Read other likely relevant accepted decisions by domain, boundary, data, runtime, or workflow overlap.
4. Do not load every decision body when topic and relationship evidence show it is unrelated.
5. Do not create a duplicate decision merely because an existing accepted decision was not linked from the current feature yet; propose the missing reference instead.
6. Before writing a Feature Spec Product Slice, present missing Applicable Decision references for human confirmation and backfill the approved links.

Feature Monthly Archive changes the path of historical ownership, not accepted decision meaning. An ADR `feature-local` or Design Slice owner may resolve an archived closed Feature Spec through the stable Feature ID plus `features/archive.md`; the locator row and month path must agree, and `closed` is historical coverage only. New work or reopened execution must rehydrate the owner to a flat path first. Archive/rehydrate may update only the approved locator/path reference and must not rewrite accepted ADR content, status, rationale, Human Review Evidence, or product semantics.

## Timing

Design Readiness starts during requirement shaping as soon as the agent can see cross-feature or end-to-end design needs, but a decision file is not created from the first fuzzy idea.

ADR files are usually created after a requirement is accepted and before feature spec synthesis when the requirement is complex, likely to split into multiple features, or needs shared business-flow or architecture direction before feature work.

Later stages may discover new shared design signals. Repeat Design Readiness and re-enter Decision & Design before continuing if they change long-term behavior, boundaries, dependencies, data ownership, recovery, non-functional goals, or verification expectations.

Do not create an ADR during ordinary chat or early fuzzy requirements discussion. Keep early signals as Design Readiness evidence or Decision Candidates in requirement or product artifacts until the owning requirement source and human gate are clear.

## Design Readiness Check

Run Design Readiness Check before a confirmed product definition enters feature construction, and repeat it when a Product Slice, legacy Product Brief, Technical Design, or Drift reveals new shared design needs.

Recommend `Decision & Design If Needed` when any signal is true:

| Signal | Why It Needs Shared Design |
|---|---|
| One requirement will become multiple features | Features need one shared business and architecture blueprint |
| The requirement needs an end-to-end business closure across components, actors, or systems | Independent stories can pass while the full flow remains broken |
| Features share domain concepts, state transitions, source-of-truth data, invariants, or ownership rules | Local specs must not invent conflicting meanings |
| The flow needs transaction, consistency, concurrency, idempotency, compensation, reconciliation, or recovery behavior | Failure and race behavior must be designed across feature boundaries |
| The requirement has measurable availability, latency, throughput, security, audit, cost, or observability goals | Non-functional goals need owners and verification before implementation |
| A new or changed project boundary, dependency, protocol, store, queue, provider, or durable workflow is introduced | Future features must preserve the same constraint and rationale |

A disputed technology choice is not required. Shared implementation design is enough to trigger Decision & Design even when everyone agrees on the likely technology.

Record this summary in the requirement README:

| Field | Values / Meaning |
|---|---|
| Status | `design-not-needed` / `candidate` / `required` / `completed` |
| Signals | Which readiness signals triggered |
| Shared Design Needs | Business-flow, domain, data, architecture, recovery, or NFR questions to close |
| Recommended Next Stage | `Decision & Design If Needed` or the next feature stage |
| Decision Records | Existing or proposed `.agent-loop/decisions/*.md` files |
| Coverage Status | `not-applicable` / `unassigned` / `planned` / `complete` |

Simple, single-feature requirements with no shared flow, durable boundary, or non-functional design need may record `design-not-needed` and continue without a decision file.

## Placement Rules

| Decision Scope | Destination | Rule |
|---|---|---|
| Product-only decision | `product.md` | Product scope, roles, value, or non-goal without durable engineering constraint |
| Feature-local implementation decision | `spec.md` Design Decisions | Current feature only, no long-term or cross-feature effect |
| Testing decision | `tests.md` or decision verification section | How to prove behavior or long-term design goals |
| Project / cross-feature decision | `.agent-loop/decisions/*.md` | Long-term, hard to reverse, surprising without context, or real trade-off |
| Unclear human-gated decision | Human Review Summary / stage summary | Scope, owner, or risk is not clear enough |

Feature-local decisions stay in `spec.md` Design Decisions.

Project / cross-feature decisions go to `.agent-loop/decisions/*.md`.

Do not create requirement-level ADR directories or feature-level ADR directories in the first implementation. Requirement and feature artifacts reference project decisions instead.

## Decision Signals

Recommend a project-level Decision & Design record when any signal is true:

Apply these signals only after confirming the candidate is not feature-local. Feature-local trade-offs, even when they have multiple options or are useful to remember later, stay in `spec.md` Design Decisions or `notes.md` unless they also create project / cross-feature constraints.

| Signal | Why It Matters |
|---|---|
| One requirement will become multiple features sharing one design rule | Prevents each feature from inventing its own explanation |
| The choice changes architecture, module, data, runtime, or ownership boundaries | Future agents need the reason, not only the current fact |
| The choice introduces a durable dependency, storage, queue, protocol, provider, transaction model, or consistency model | Maintenance and recovery costs persist |
| Multiple reasonable options exist and the chosen path excludes alternatives | Trade-offs should be visible |
| Future readers would ask "why is this rule here?" | The reason is part of project memory |
| The decision defines high-availability, performance, consistency, security, or reconciliation behavior | Verification needs a stable design target |

These signals do not depend on disputed alternatives. A record can be required because features need one coherent implementation blueprint, even when the main technology choice is already understood.

Do not recommend a project-level decision file for ordinary bugfixes, temporary workarounds, small UI copy/layout decisions, or choices already covered by an accepted decision.

## Human Gate

Creating, accepting, superseding, deprecating, deleting, or renumbering a project-level decision is Human-gated.

The agent may:

- discover decision signals
- list Decision Candidates
- recommend Decision Placement
- draft a decision file for review
- suggest references from requirement README, product.md, or spec.md

The agent must not:

- silently create a decision that constrains future features
- mark a draft decision as accepted
- change the meaning of an accepted decision
- delete or renumber old decision files
- promote a feature-local decision into a project constraint without human confirmation

The decision file status cannot become `accepted` without explicit human confirmation.

## Effective Requirement Snapshot

Every ADR driven by accepted product semantics resolves exactly one Requirement Set README source before technical design. New sets use `Effective Product Definition`; older sets retain the `Effective Concept Foundation` / reviewed `requirement.md` reader. Never add both pointers or migrate a legacy source just to start ADR work.

Record this snapshot near the ADR header:

```text
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
```

Rules:

- a new source must have Product Review `confirmed`; a triggered internal Concept Foundation must be accepted inside that Product Definition; pending, `candidate`, or `reopened` meaning returns to the Human Grill Contract before ADR work continues
- list only accepted Concept IDs, accepted Requirement Model IDs, and resolvable Product Rule section anchors declared inside this ADR's coherent decision scope
- cite or concisely summarize unchanged accepted meaning; do not copy a new definition into the decision
- resolve the effective source again before ADR acceptance and before a dependent Feature Spec, Plan, or implementation begins
- `Upstream Compatibility` is a dependency judgment, not a new decision status
- Product Rules use source anchors such as `product.md#approval-authority`; do not invent `RULE-*`
- a confirmed Brief with no stable model IDs or Product Rule references records all accepted-ID/rule fields as `none`, sets trace applicability to `not-applicable`, gives a concrete reason, and does not invent product-model tables
- a confirmed Standard source may record either accepted-ID field as `none` only when that source declares no IDs of the corresponding kind; Product Rule references still make trace applicability `required` and must receive normal scope and technical-landing coverage
- legacy snapshots may retain `Effective Concept Source` and `Concept Foundation Status`; when legacy source is reasoned `concept-foundation-not-needed`, use the same reasoned not-applicable shape. Never mix new and legacy snapshot metadata; legacy records may retain either the exact old Coverage Hard Gate or the current unified gate without migration

## Requirement Model Scope Inventory

Before choosing the ADR scope, inventory every stable Requirement Model ID and accepted Product Rule section anchor in the effective source: relationship (`REL-*`), permission (`PERM-*`), command/event (`CMD-*` / `EVT-*`), flow (`FLOW-*`), state (`STATE-*`), product model (`PM-*`), exception/recovery (`EX-*`), plus references such as `product.md#approval-authority`. Give each source reference exactly one scope disposition:

```text
in-scope | covered-by-accepted-decision | feature-local | proposed-decision | not-applicable
```

- `in-scope` names this ADR; model IDs and Product Rule references exactly match the snapshot and Technical Landing Trace rows
- `covered-by-accepted-decision` names an existing accepted decision Markdown path
- `feature-local` names an existing Feature Spec path, or an explicit canonical future path prefixed with `planned:`
- `proposed-decision` names an existing decision draft, or an explicit canonical future path prefixed with `planned:`
- `not-applicable` begins with `reason:` and gives a concrete scope reason

The inventory is a section of the existing ADR, not a new mapping artifact. It makes out-of-scope ownership visible and prevents an Agent from shrinking the snapshot until an inconvenient source model disappears.

## Requirement Model Technical Landing Trace

Use one generic trace table inside the ADR:

| Requirement Model Ref | Accepted Meaning / Constraint | Disposition | Technical Landing | Preserved Invariant | Design Slice | Verification |
|---|---|---|---|---|---|---|
| `<accepted-model-id>` | link or concise unchanged meaning | landed / covered-by-accepted-decision / feature-local / not-applicable |  |  |  |  |

Every in-scope accepted relationship, permission rule, command, event, flow step, state rule, product-model row, exception/recovery row, and Product Rule anchor needs exactly one disposition. Do not require an ADR to copy the whole PRD; the Scope Inventory accounts for the complete source-reference set, while the snapshot and trace declare the coherent scope handled or deliberately delegated by this ADR.

Disposition rules:

- `landed`: name a concrete technical landing, preserved invariant, Design Slice, and verification target
- `covered-by-accepted-decision`: reference the existing accepted decision Markdown path that owns the landing; do not duplicate its technical reasoning
- `feature-local`: name an existing Feature Spec path or an explicit `planned:features/<feature-id>/spec.md` path plus verification direction; shared constraints cannot be hidden as feature-local
- `not-applicable`: state a concrete reason and show it in the Decision & Design Human Review Summary

ADR must not create, rename, split, merge, or redefine a Concept, relationship, role/permission, command/event, business flow, product state, invariant, exception/recovery meaning, or product fact ownership. If accepted meaning is missing or insufficient, return to Requirements Discussion rather than filling the gap in technical design.

## Optional Visual Evidence

When a Visual Trigger makes a technical boundary, sequence, state/lifecycle, data flow, or option comparison materially easier to review, use the Optional Visual Communication Adapter under one bounded Visual Scope Grant. A working render is disposable: human feedback must be rewritten into the proposed ADR before review.

Durable visual evidence is optional and independently confirmed. It uses `Visual Manifest Contract: source-render-v1` in the ADR `Optional Visual Evidence` section and records one typed source plus one validated render, their SHA-256 values, exact `archify@<version>` generator, validation evidence, status, one concrete Review Question, and Semantic References. Semantic References must resolve to accepted Product Concept/Model IDs, Product Rule anchors, or an ADR section anchor.

The visual cannot accept the ADR, change Requirement product meaning, satisfy Requirement Model Technical Landing coverage, or replace Human Review Evidence. Missing/mismatched source/render pairs and stale/unknown references fail structural preflight. Remove the optional section when unused.

## Coverage Hard Gate

A decision cannot become `accepted` while coverage is missing or Upstream Compatibility is `review-required`.

The Agent first runs structural preflight while the ADR remains `proposed`. Only after preflight succeeds does it present the Decision & Design Human Review Summary. Explicit human acceptance authorizes the Agent to record Human Review Evidence, change the status to `accepted`, and rerun accepted-mode validation. A validator pass never grants acceptance by itself.

Before asking for ADR acceptance or allowing a dependent Feature Spec:

1. resolve the effective source and confirm compatibility is `current`;
2. confirm every stable Requirement Model ID and accepted Product Rule reference in the effective source has one Scope Inventory row;
3. confirm the in-scope inventory references exactly equal the snapshot model IDs plus Product Rule references and the trace rows;
4. confirm every `landed` row has a concrete Technical Landing, Preserved Invariant, Design Slice, and Verification target;
5. confirm accepted-decision paths exist and are accepted; confirm feature-local paths either exist or use an explicit canonical `planned:` path;
6. present every `not-applicable`, `feature-local`, proposed-decision, deferred, and out-of-scope item to the human;
7. confirm every implementation-bearing technical rule is represented in Design Slice Coverage and no required slice remains `unassigned`;
8. confirm no unresolved product-semantic blocker remains.

An `Applicable Decisions` reference proves awareness only. It cannot replace Requirement Model coverage, Design Slice ownership, or verification.

## Upstream Compatibility And Drift

Re-run compatibility review when the Requirement Set README effective source changes or newly accepted product evidence changes Concept IDs, Requirement Model IDs, Product Rule anchors, or their accepted meaning.

1. set the dependency judgment to `Upstream Compatibility: review-required`;
2. stop new dependent Feature Spec, Plan, and implementation work;
3. compare old/new effective sources, Concept IDs, Requirement Model IDs, and affected trace rows;
4. if accepted product meaning changed but the existing technical decision remains valid, update only the snapshot and trace after Decision & Design Human Review;
5. if the chosen technical boundary, representation, recovery, compatibility, NFR conclusion, or accepted decision meaning no longer holds, create a Human-gated superseding ADR;
6. preserve the accepted ADR for audit; do not rewrite its decision meaning in place.

Compatibility review may add references or current evidence to an accepted record only when repository policy permits append-only metadata. It must not use a metadata update to disguise a changed decision.

Post-Merge Memory Reconciliation preserves accepted ADR technical meaning and supersession history. Code/result drift is evidence for Human Review, not permission to rewrite an accepted decision in place; any incompatible meaning still requires the existing Human-gated superseding ADR path.

## Triggered Operational Landing

Operational landing detail is conditional. Assess these concerns before the ADR Human Gate:

| Concern | Trigger | Required Result |
|---|---|---|
| Migration / Backfill | persistence representation or existing durable data changes | expand migration/backfill design |
| Compatibility | protocol, consumer, provider, or version compatibility changes | expand compatibility design |
| Rollout / Cutover | runtime boundary, traffic path, or staged activation changes | expand rollout/cutover design |
| Rollback / Reversibility | safe reversal needs technical work or data repair | expand rollback/reversibility design |

For each concern, record `triggered` with its ADR section or `not-triggered` with one concrete reason. Do not add empty operational sections by default, and do not copy a domain-specific action, vendor, storage choice, protocol, or rollout topology from examples into a new decision.

Before creating or accepting the ADR, load `references/human-review-summary.md` and present the Decision & Design Human Review Summary. The summary exposes effective source, source-wide scope inventory, coverage counts, chosen decision, preserved product semantics, operational triggers, Design Slice ownership, verification direction, blockers, and the explicit human decision. It does not replace the ADR. An accepted ADR records `Decision`, `Confirmed By`, `Confirmed At`, and concrete evidence in its Human Review Evidence section.

## Relationship Model

Use these relationship fields consistently:

| Field | Meaning | Primary Location |
|---|---|---|
| Source Requirements | The Requirement Product Definition that triggered or constrains the decision or feature | decision file, Requirement `product.md`, Feature `spec.md` |
| Applicable Decisions | Existing decisions that constrain this requirement or feature | requirement README, Requirement `product.md`, Feature `spec.md` |
| Triggered Decisions | New decisions caused by a requirement | requirement README |
| Implements Decisions | Which decision slice this feature implements | spec.md |
| Implemented By | Which features implement a requirement or decision | requirement README, decision file |
| Related Decisions | Superseded, dependent, or conflicting decisions | decision file |

Requirement README owns lifecycle, phase mapping, triggered decisions, and implemented-by tracking.

Decision files own technical design reasoning: goals, accepted product-concept references, business-flow landing, chosen option, architecture design, consequences, and verification closure. The source PRD / Requirement Product Model continues to own product definitions.

New Feature `spec.md` references applicable decisions and states which Product Slice / Design Slice it implements. Existing legacy Feature `product.md` remains reader-compatible, but new work does not create or refresh one.

## Design Slice Coverage

Every accepted Decision & Design record that drives more than one feature must divide implementation-bearing content into stable Design Slice IDs such as `DS-01`, `DS-02`, and `DS-03`.

A design slice is a required capability, invariant, flow segment, recovery responsibility, or non-functional verification obligation that feature work must own. It is not merely a document section.

The decision record owns the reverse coverage table:

| Design Slice ID | Required Capability / Rule | Owning Feature(s) | Verification | Coverage Status |
|---|---|---|---|---|
| DS-01 |  |  |  | unassigned / planned / implemented / verified / deferred / out-of-scope |

Rules:

- map every implementation-bearing business-flow step, invariant, failure/recovery rule, and non-functional target to at least one design slice
- assign each required slice to one or more planned features before Feature Spec
- copy the assigned slice IDs into each owning feature `spec.md` `Implements Decisions` table
- require a human decision for `deferred` or `out-of-scope` slices because those states change requirement delivery coverage
- update the reverse table when feature scope or ownership changes
- No required design slice may remain `unassigned` before Feature Spec.
- `Applicable Decisions` alone proves constraint awareness, not implementation coverage

## Stage Use

| Stage | Decision Behavior |
|---|---|
| Requirements Discussion | Capture Design Readiness evidence and early Decision Candidates; do not create ADR from fuzzy chat |
| Requirement Archive | Run Design Readiness Check; record status, signals, and recommended next stage after human review |
| Decision & Design If Needed | Complete the shared business/architecture blueprint, run Decision Scan / Placement, and assign all required design slices |
| Legacy Product Brief compatibility | Route newly discovered product tradeoffs and shared design needs back to Requirements Discussion / Design Readiness; do not rewrite the legacy brief |
| Feature Spec | Load applicable decisions and implement assigned design slices before writing final behavior and acceptance |
| Technical Design / Code Context | Re-scan if implementation introduces long-term boundaries, dependencies, data, transactions, consistency, concurrency, or recovery choices |
| Plan Gate | Block plans that bypass unresolved required decisions |
| Review / Drift Check / Close | Verify assigned design slices conform to accepted decisions; backfill references or recommend a new/superseding decision when reality changed |

## Naming

Use monotonically increasing, stable filenames:

```text
.agent-loop/decisions/0001-wallet-realtime-deduction-and-reconciliation.md
```

Do not reuse numbers after deletion or supersession. Prefer appending a new decision and linking `Supersedes` / `Superseded By`.

## Template

Use `templates/decision.md` for decision files.

The template is intentionally richer than a minimal ADR. It is a Decision And Design Record: it records the requirement context, business flow, chosen option, technical architecture, non-functional design, consequences, and verification plan.

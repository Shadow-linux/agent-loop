# Decision & Design / ADR Lane

Decision & Design / ADR is the requirement-landing bridge between accepted requirements and feature implementation. It turns shared business-flow, domain, data, architecture, recovery, and non-functional needs into one coherent design before feature stories fragment the work.

```text
Requirement -> Design Readiness Check -> Decision & Design If Needed -> Feature Mapping -> Product Brief / Feature Spec
```

Requirement explains what humans want and how success is recognized. Decision & Design explains how the complete requirement can work across features and which shared rules every feature must preserve. Feature artifacts implement and verify assigned design slices.

PRD / Requirement Product Model owns product meaning. ADR consumes accepted product semantics and is responsible for later technical landing; it must not redefine accepted Concept IDs, identity, lifecycle, relationships, invariants, product states, terminal meaning, or product fact ownership.

Concept Foundation and Requirement Product Model do not choose tables, stores, event topics, providers, or other technical representations. Decision & Design may select those representations only after requirement acceptance and through its own Human Gate, while preserving accepted product meaning.

Design Readiness Check is a required method at Requirement Archive, Product Brief, and Feature Spec boundaries; it is not a standalone stage.

Decision Scan / Placement remains a lightweight method inside Decision & Design. It decides where a decision belongs; it is not the whole design stage.

A decision file remains globally optional but becomes conditionally required when shared design is required and no accepted decision already covers it. Creating or accepting that file remains Human-gated.

This lane is not a complex ADR system. It adds one stable destination for long-term or cross-feature decision records:

```text
.agent-loop/decisions/
```

Creating `.agent-loop/decisions/` does not enable enterprise memory mode. The directory is available in simple and enterprise memory modes.

## Re-entry And Discovery

`project.md` records whether `.agent-loop/decisions/` exists so future agents can rediscover accepted project decisions in simple or enterprise memory mode.

Before Decision & Design, Product Brief, or Feature Spec:

1. Read decision links already named by the active requirement, `product.md`, or `spec.md`.
2. List `.agent-loop/decisions/*.md` filenames and statuses when the project Decisions index is present.
3. Read other likely relevant accepted decisions by domain, boundary, data, runtime, or workflow overlap.
4. Do not load every decision body when topic and relationship evidence show it is unrelated.
5. Do not create a duplicate decision merely because an existing accepted decision was not linked from the current feature yet; propose the missing reference instead.
6. Before writing Product Brief or Feature Spec, present missing Applicable Decision references for human confirmation and backfill the approved links.

## Timing

Design Readiness starts during requirement shaping as soon as the agent can see cross-feature or end-to-end design needs, but a decision file is not created from the first fuzzy idea.

ADR files are usually created after a requirement is accepted and before feature spec synthesis when the requirement is complex, likely to split into multiple features, or needs shared business-flow or architecture direction before feature work.

Later stages may discover new shared design signals. Repeat Design Readiness and re-enter Decision & Design before continuing if they change long-term behavior, boundaries, dependencies, data ownership, recovery, non-functional goals, or verification expectations.

Do not create an ADR during ordinary chat or early fuzzy requirements discussion. Keep early signals as Design Readiness evidence or Decision Candidates in requirement or product artifacts until the owning requirement source and human gate are clear.

## Design Readiness Check

Run Design Readiness Check before an accepted requirement enters feature construction, and repeat it when Product Brief, Technical Design, or Drift reveals new shared design needs.

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

## Relationship Model

Use these relationship fields consistently:

| Field | Meaning | Primary Location |
|---|---|---|
| Source Requirements | The requirement source that triggered or constrains the decision or feature | decision file, product.md, spec.md |
| Applicable Decisions | Existing decisions that constrain this requirement, product brief, or feature | requirement README, product.md, spec.md |
| Triggered Decisions | New decisions caused by a requirement | requirement README |
| Implements Decisions | Which decision slice this feature implements | spec.md |
| Implemented By | Which features implement a requirement or decision | requirement README, decision file |
| Related Decisions | Superseded, dependent, or conflicting decisions | decision file |

Requirement README owns lifecycle, phase mapping, triggered decisions, and implemented-by tracking.

Decision files own technical design reasoning: goals, accepted product-concept references, business-flow landing, chosen option, architecture design, consequences, and verification closure. The source PRD / Requirement Product Model continues to own product definitions.

Feature `product.md` and `spec.md` reference applicable decisions and state which part of a decision they implement. They do not restate the whole decision.

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
| Product Brief | Route newly discovered product tradeoffs and shared design needs back through Design Readiness |
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

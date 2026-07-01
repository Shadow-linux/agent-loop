# Project Decisions / ADR Lane

Project Decisions / ADR is a lightweight design bridge between accepted requirements and feature implementation.

```text
Requirement -> Decision / ADR -> Feature
```

Requirement explains what humans want and how success is recognized. Decision / ADR explains the business-flow and architecture choices that make the requirement implementable. Feature artifacts explain the concrete implementation slice.

Decision Scan is a required lightweight check; decision files are optional human-gated artifacts.

This lane is not a complex ADR system. It adds one stable destination for long-term or cross-feature decision records:

```text
.agent-loop/decisions/
```

Creating `.agent-loop/decisions/` does not enable enterprise memory mode. The directory is available in simple and enterprise memory modes.

## Timing

Decision Scan starts as soon as requirement or product shaping reveals a decision signal, but a decision file is not created at the first fuzzy idea.

ADR files are usually created after a requirement is accepted and before feature spec synthesis when the requirement is complex, likely to split into multiple features, or needs shared business-flow or architecture direction before feature work.

Later stages may discover new decision signals. Route them back through Decision Scan before continuing if they change long-term behavior, boundaries, dependencies, data ownership, or verification expectations.

Do not create an ADR during ordinary chat or early fuzzy requirements discussion. Keep early signals as Decision Candidates in requirement or product artifacts until the owning requirement source and human gate are clear.

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

Recommend a project-level decision file when any signal is true:

Apply these signals only after confirming the candidate is not feature-local. Feature-local trade-offs, even when they have multiple options or are useful to remember later, stay in `spec.md` Design Decisions or `notes.md` unless they also create project / cross-feature constraints.

| Signal | Why It Matters |
|---|---|
| One requirement will become multiple features sharing one design rule | Prevents each feature from inventing its own explanation |
| The choice changes architecture, module, data, runtime, or ownership boundaries | Future agents need the reason, not only the current fact |
| The choice introduces a durable dependency, storage, queue, protocol, provider, transaction model, or consistency model | Maintenance and recovery costs persist |
| Multiple reasonable options exist and the chosen path excludes alternatives | Trade-offs should be visible |
| Future readers would ask "why is this rule here?" | The reason is part of project memory |
| The decision defines high-availability, performance, consistency, security, or reconciliation behavior | Verification needs a stable design target |

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

Decision files own the design reasoning: goals, domain concepts, business flow, chosen option, architecture design, consequences, and verification closure.

Feature `product.md` and `spec.md` reference applicable decisions and state which part of a decision they implement. They do not restate the whole decision.

## Stage Use

| Stage | Decision Behavior |
|---|---|
| Requirements Discussion | Capture early Decision Candidates; do not create ADR from fuzzy chat |
| Requirement Archive | Add Applicable Decisions and Triggered Decisions after human review |
| Product Brief | Route product tradeoffs and product decisions through Decision Scan |
| Decision Scan / Placement If Needed | Decide whether candidates stay in product/spec/tests/notes or need `.agent-loop/decisions/*.md` |
| Feature Spec | Load applicable decisions before writing behavior and acceptance |
| Technical Design / Code Context | Re-scan if implementation introduces long-term boundaries, dependencies, data, transactions, consistency, concurrency, or recovery choices |
| Plan Gate | Block plans that bypass unresolved required decisions |
| Drift Check / Close | Backfill decision references or recommend a new/superseding decision when implementation changed long-term facts |

## Naming

Use monotonically increasing, stable filenames:

```text
.agent-loop/decisions/0001-wallet-realtime-deduction-and-reconciliation.md
```

Do not reuse numbers after deletion or supersession. Prefer appending a new decision and linking `Supersedes` / `Superseded By`.

## Template

Use `templates/decision.md` for decision files.

The template is intentionally richer than a minimal ADR. It is a Decision And Design Record: it records the requirement context, business flow, chosen option, technical architecture, non-functional design, consequences, and verification plan.

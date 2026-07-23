# Requirement/Product Grill

Requirement/Product Grill is a clarification method inside Adaptive Product Definition, not an ADR generator and not a new agent-loop stage. Its results are synthesized into the Requirement `product.md`; it is not a separate artifact generator.

```text
Grill early; synthesize later; send shared design signals through Design Readiness Check.
```

Use it inside Requirements Discussion and its Brainstorm / Clarify work when the demand has fuzzy terminology, unclear roles, domain boundaries, business flows, exception paths, conflicting prior Feature behavior, or decision signals.

## Core Rules

- Ask one blocking question at a time.
- Include the agent recommended answer with each question.
- First inspect project memory, original sources, the current effective Requirement `product.md` when present, docs, code, and tests when the answer is discoverable.
- 提问前先检查相关过往 feature 的 `product.md`、`spec.md`、`tests.md`、`notes.md` when those files may already define terminology, business rules, acceptance direction, or historical decisions.
- Do not run a full feature scan. Use targeted lookup only.
- targeted lookup signals include keywords, domain objects, related requirement, same module/flow, active/paused/recent feature.
- If prior feature artifacts conflict with the current human statement, state the conflict first, then ask whether to reuse the old rule, override it, or treat the statement as new scope.
- Do not turn ordinary chat into requirement artifacts unless the human asks to shape, record, or archive the demand.

## Concept Foundation

Concept Foundation is a triggered internal method of Requirements Discussion / Requirement Product Grill. It is not a separate PRD, ADR generator, canonical stage, top-level directory, or technical schema.

Its job is to stabilize product meaning before detailed Business Flow, State Model, or Product Data Model work. The human-reviewed Requirement `product.md` owns the new-format result.

### Trigger And Lightweight Route

Set `Concept Foundation Status: candidate` when any signal is present:

- one term may identify multiple entities, actions, processes, or outcomes;
- a business object has or changes identity, lifecycle, state, ownership, or terminal meaning;
- multiple roles, tenants, operators, or external systems participate;
- one requirement will shape multiple features;
- fact-source, balance, inventory, order, approval, task, quota, recovery, or other hard-to-reverse product semantics matter;
- project Domain Language, source material, code, tests, or historical features conflict with the current wording.

Use `concept-foundation-not-needed` only when the change has no product-semantic, identity, lifecycle, ownership, state, relationship, cross-role, cross-feature, or data-meaning impact. Examples include a pure copy/style/layout edit, a configuration-only change, a narrow bugfix that preserves meaning, or direct reuse of already accepted concepts without new relationships. Record a concrete reason.

Allowed status:

```text
candidate | accepted | reopened | concept-foundation-not-needed
```

### Scenario-First Candidate Extraction

Start from one concrete success scenario and the minimum failure/cancel/recovery scenarios that can change product meaning. Extract nouns, human verbs, system actions, outcomes, constraints, synonyms, overloaded terms, and historical conflicts. Do not ask the human to provide a domain model.

Create a Concept Candidate Inventory before the first blocking question:

| Concept ID | Candidate Name | Kind | Evidence / Example | Ambiguity / Conflict | Status |
|---|---|---|---|---|---|
| C-ORDER | Order | entity | source requirement | “order” also used for request | candidate |

Concept IDs are stable inside the Requirement scope. They connect definitions, relationships, states, flows, product facts, ADR landing, Feature Product Slice, and acceptance direction. They are not required to become permanent project-wide IDs.

### Concept Definition

For each blocking concept, record only applicable product fields; use `n/a` with a reason rather than inventing facts:

| Field | Product Meaning |
|---|---|
| Concept ID / Canonical Name | stable requirement-local reference and one recommended name |
| Definition / Examples / Non-examples | what the concept is and which nearby meaning it excludes |
| Identity | how two occurrences are recognized as the same product object |
| Owner / Responsible Actor | who creates, manages, advances, cancels, or restores it |
| Lifecycle Boundary / State-bearing | creation, terminal meaning, recovery, and whether it owns business state |
| Relationships | dependency, containment, or cardinality with other accepted concepts |
| Invariants | product rules that must always hold |
| Product Source Of Truth | accepted product fact owner or unresolved Decision Candidate; not a table/store selection |
| Synonyms / Avoid | allowed wording and terms that must not be mixed |
| Evidence | human confirmation, source requirement, code, test, or historical feature |

## Human Grill Contract

When Concept Foundation triggers, perform one turn in this exact sequence:

1. inspect Domain Language, source requirements, relevant docs/code/tests, and targeted historical features;
2. extract and display the Concept Candidate Inventory;
3. present one recommended definition with Concept ID, evidence, identity/lifecycle boundary, and the downstream impact of accepting or rejecting it;
4. ask one downstream-blocking question, then wait.

Do not ask a batch of concept questions. The existing one-blocking-question rule becomes strict for this method: exactly one question per turn. Record non-blocking uncertainties under Blocking Ambiguities without pretending they are resolved.

Example:

```text
Evidence says administrator approval can precede the payment callback.
Candidate concepts: C-REFUND-REQUEST and C-REFUND-SETTLEMENT.
Recommended definition: approval completes C-REFUND-REQUEST; confirmed funds complete C-REFUND-SETTLEMENT.
Accepting this keeps notification/recovery tied to observed settlement; rejecting it leaves a possible post-success failure and ambiguous fact owner.
Should “refund completed” mean approved request or confirmed settlement?
```

### Concept Foundation Gate

Keep status `candidate` and stop before detailed Business Flow, State Model, or Product Data Model when any blocking item remains:

- a critical concept has more than one downstream-changing meaning;
- identity or lifecycle boundary is missing;
- actor/owner/permission boundary is unresolved where multiple actors participate;
- a required relationship, state-bearing decision, invariant, or terminal meaning is unknown;
- a historical conflict is unresolved;
- a product fact owner is required to proceed and is neither confirmed nor recorded as a Decision Candidate.

Before treating the internal foundation as `accepted`, include the cumulative concept/model coverage in the Product Human Review Summary defined in `human-review-summary.md`. Continue only after the human confirms the recommended definitions and every remaining uncertainty cannot change the downstream model. This Human Gate belongs to Requirements Discussion; it does not accept Requirement lifecycle, implementation, archive files, ADRs, or Feature start.

### Reopen After Archive

If later evidence changes accepted product semantics after `product.md` was recorded, do not edit that source in place. Mark the internal state `reopened`, stop dependent modeling, run Requirement Conflict Review, and ask one blocking question. After human confirmation, write `YYYY-MM-DD-product-follow-up-<slug>.md` or create a new Requirement Set, then update README `Effective Product Definition` while retaining the previous source for history. Legacy Requirement Sets keep their historical pointer and append-only compatibility path.

### Requirement Product Model Derivation

After `accepted`, derive and trace these product views from Concept IDs instead of creating each section independently:

| Accepted Concept Evidence | Derived Product View | Required Check |
|---|---|---|
| Canonical Name + Definition | Terminology / Domain Language | same name and meaning downstream |
| Identity + Relationships | Concept Relationships / Requirement Product Model | objects and cardinality agree |
| Owner / Responsible Actor | Role / Permission Matrix | read/create/advance/cancel/recover authority |
| Human Verbs / System Actions | Commands / Events | actor, precondition, result, affected Concept IDs |
| Lifecycle Boundary + State-bearing | Product State Model | initial, terminal, forbidden, and recovery transitions |
| Relationships + Commands / Events | Primary Business Flow | every step cites accepted Concept IDs and closes to product terminal |
| Invariants | Guards / Validation Rules | transitions and product facts preserve the rule |
| Failure Scenarios | Exception / Compensation / Recovery | observable result and responsible actor |

The Requirement Product Model is product-level. It may say which fact belongs to which product concept and actor, but it must not choose tables, documents, event topics, ledgers, providers, transactions, consistency algorithms, migrations, or other technical representations.

Give every applicable derived model row a stable ID so Feature Product Slice and Decision & Design can cite it without copying meaning: `REL-*` for relationships, `PERM-*` for permission rules, `CMD-*` / `EVT-*` for actions, `FLOW-*` for flow steps, `STATE-*` for state rules, `PM-*` for product models/facts, and `EX-*` for exception/recovery scenarios. Do not create a placeholder model merely to populate a category; a Brief and a Standard not-applicable view stay lightweight.

## Question Targets

Ask only when the answer affects one of these:

| Target | Examples |
|---|---|
| Scope | in / out of scope, phase boundary, MVP vs later |
| Users / operators | actor, role, permission, tenant, admin/operator path |
| Business flow | normal path, state transition, handoff, lifecycle |
| Exception path | failure, insufficient balance, retry, compensation, manual recovery |
| Data / source of truth | canonical entity, balance, status, record ownership |
| Concept foundation | identity, lifecycle, relationship, state-bearing, invariant, accepted product fact meaning |
| Acceptance direction | what proves the requirement is closed |
| Shared design / long-term signal | multiple features, end-to-end closure, shared state or source of truth, recovery, non-functional target, hard to reverse, surprising without context, real trade-off |

## Output Mapping

| Grill output | Agent-loop destination |
|---|---|
| Clarified local term | Requirement `product.md` terminology or downstream display wording |
| Accepted Concept Foundation | Effective Product Definition named by Requirement README; ADR and Product Slice cite Concept IDs/model rows |
| Ambiguous term | Requirement `product.md` open questions; blocking ambiguity stops downstream work |
| Concrete scenario | Requirement `product.md` outcome/flow/acceptance direction and Feature Spec Product Slice acceptance |
| Prior feature conflict | Product Definition source/conflict evidence or Human Review Summary conflict table |
| Durable domain language candidate | Project Memory Update proposal only after human confirmation |
| Cross-feature / shared design / hard to reverse / real trade-off | Design Readiness evidence and Decision Candidate |

Do not persist grill output to project memory, `product.md`, `spec.md`, or decisions without the owning Human Review / Record gate.

Detailed new-format grill results belong in the Effective Product Definition; Requirement README keeps its pointer, source inventory, lifecycle, Delivery Phase, Feature Mapping, and decision-link summaries. Legacy effective Requirement sources remain readable.

Feature Spec must not use “meaning in this feature” to redefine an accepted Concept ID. If a Feature needs a different meaning, return to the owning Requirements Discussion rather than silently creating a local synonym.

When Requirement/Product Grill was used, the owning artifact must carry grill results into structured sections, not only a prose summary.

Standard Product Definition sections, only when applicable:

- Terminology / Domain Language
- Roles / Operators / Permission Boundary
- Primary Business Flow
- Exception Paths
- Data / Source of Truth
- Historical Behavior / Prior Conflicts
- Acceptance Scenarios
- Decision Candidates
- Product / Feature Mapping
- Out Of Scope And Why

- Product Capability Scope / user scenarios
- Product View Applicability
- Experience, operations, measurement, and acceptance direction
- Product Traceability and Decision Candidates

## Decision Boundary

Grill may discover a Decision Candidate. It must not directly create `.agent-loop/decisions/*.md` or mark a decision accepted.

Decision Candidate signals:

| Signal | Meaning |
|---|---|
| Hard to reverse | Data model, payment flow, external dependency, protocol, durable workflow |
| Surprising without context | Future agents will ask why this rule exists |
| Real trade-off | Multiple reasonable options exist and the choice excludes another route |

Record these in `product.md` and the Human Review Summary as Design Readiness evidence and Decision Candidates. When Decision & Design is required, its Decision Scan / Placement method decides whether the candidate stays product-local, Feature-local, test-local, or becomes a Human-gated decision file.

## Path Overrides

External grill-with-docs defaults are advisory only.

- Do not create `CONTEXT.md`.
- Do not create `CONTEXT-MAP.md`.
- Do not create `docs/adr/`.
- Requirement `product.md` owns reviewed product goals, terminology, roles, business flows, exceptions, product fact ownership, historical conflicts, acceptance direction, open questions, and Decision Candidates.
- Requirement README owns source index, lifecycle, Delivery Phases, Feature Mapping, and decision-link summaries.
- Legacy Feature Product Brief remains readable but receives no new writes.
- Feature Spec owns engineering behavior, Product Slice, and feature-local design decisions.
- Project memory owns durable domain language only after human confirmation.
- `.agent-loop/decisions/` owns accepted long-term / cross-feature Decision & Design records only through Decision & Design and the human gate.

## Example

```text
I found a prior wallet feature where insufficient balance stops LLM calls.
Your current wording says calls may continue and settle later.

Recommended answer: reuse the old rule for this phase: stop service when balance is insufficient.
Should we reuse the old rule, override it, or treat postpaid usage as a new requirement scope?
```

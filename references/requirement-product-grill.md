# Requirement/Product Grill

Requirement/Product Grill is a clarification method, not a PRD generator, not an ADR generator, and not a new agent-loop stage.

```text
Grill early; synthesize later; route decision signals through Decision Scan.
```

Use it inside Requirements Discussion, Product Brief, and Brainstorm / Clarify when the demand has fuzzy terminology, unclear roles, domain boundaries, business flows, exception paths, conflicting prior feature behavior, or decision signals.

## Core Rules

- Ask one blocking question at a time.
- Include the agent recommended answer with each question.
- First inspect project memory, source requirements, existing `product.md`, docs, code, and tests when the answer is discoverable.
- 提问前先检查相关过往 feature 的 `product.md`、`spec.md`、`tests.md`、`notes.md` when those files may already define terminology, business rules, acceptance direction, or historical decisions.
- Do not run a full feature scan. Use targeted lookup only.
- targeted lookup signals include keywords, domain objects, related requirement, same module/flow, active/paused/recent feature.
- If prior feature artifacts conflict with the current human statement, state the conflict first, then ask whether to reuse the old rule, override it, or treat the statement as new scope.
- Do not turn ordinary chat into requirement artifacts unless the human asks to shape, record, or archive the demand.

## Question Targets

Ask only when the answer affects one of these:

| Target | Examples |
|---|---|
| Scope | in / out of scope, phase boundary, MVP vs later |
| Users / operators | actor, role, permission, tenant, admin/operator path |
| Business flow | normal path, state transition, handoff, lifecycle |
| Exception path | failure, insufficient balance, retry, compensation, manual recovery |
| Data / source of truth | canonical entity, balance, status, record ownership |
| Acceptance direction | what proves the requirement is closed |
| Long-term decision signal | hard to reverse, surprising without context, real trade-off |

## Output Mapping

| Grill output | Agent-loop destination |
|---|---|
| Clarified local term | Requirement README terminology, `product.md` terminology, or `spec.md` wording |
| Ambiguous term | Requirement README / `product.md` open questions, or `notes.md` |
| Concrete scenario | Requirement document, Product Brief user story, or Feature Spec acceptance / edge case |
| Prior feature conflict | Requirement README, `notes.md`, or Human Review Summary conflict table |
| Durable domain language candidate | Project Memory Update proposal only after human confirmation |
| Hard to reverse / surprising / real trade-off | Decision Candidate for Decision Scan |

Do not promote grill output to project memory, `product.md`, `spec.md`, or decisions without the owning human gate.

When Requirement/Product Grill was used, the owning artifact must carry grill results into structured sections, not only a prose summary.

Requirement document sections:

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

Product Brief sections:

- Primary User Journey
- User Stories with Acceptance Direction
- Edge Cases
- Behavior Changes
- Product Tradeoffs
- Success Signals
- Historical Compatibility

## Decision Boundary

Grill may discover a Decision Candidate. It must not directly create `.agent-loop/decisions/*.md` or mark a decision accepted.

Decision Candidate signals:

| Signal | Meaning |
|---|---|
| Hard to reverse | Data model, payment flow, external dependency, protocol, durable workflow |
| Surprising without context | Future agents will ask why this rule exists |
| Real trade-off | Multiple reasonable options exist and the choice excludes another route |

Route these to Decision Scan in the stage summary or Human Review Summary. Decision Scan decides whether the candidate stays in `product.md`, `spec.md`, `tests.md`, `notes.md`, or becomes a human-gated decision file.

## Path Overrides

External grill-with-docs defaults are advisory only.

- Do not create `CONTEXT.md`.
- Do not create `CONTEXT-MAP.md`.
- Do not create `docs/adr/`.
- Requirement README owns requirement-local terminology, open questions, Delivery Phases, and source index.
- Product Brief owns feature-level product synthesis.
- Feature Spec owns engineering behavior and feature-local design decisions.
- Project memory owns durable domain language only after human confirmation.
- `.agent-loop/decisions/` owns accepted long-term / cross-feature decisions only through Decision Scan and human gate.

## Example

```text
I found a prior wallet feature where insufficient balance stops LLM calls.
Your current wording says calls may continue and settle later.

Recommended answer: reuse the old rule for this phase: stop service when balance is insufficient.
Should we reuse the old rule, override it, or treat postpaid usage as a new requirement scope?
```

# Feature Context Snapshot And Load Contract Proposal

**Version:** v1.5.x design line; no version bump is authorized by this Proposal
**Status:** accepted for implementation
**Created:** 2026-07-25
**Human Review:** accepted in conversation on 2026-07-25
**Priority:** high; repair before expanding the Feature construction approval model
**Scope:** Requirement-owned product truth, Feature-local execution context, freshness verification, and deterministic Task/Test/Plan loading

## 1. Problem

Agent Loop correctly moved new product meaning out of Feature `product.md` and into the Requirement Set's Human-reviewed Effective Product Definition:

```text
Requirement README
-> Effective Product Definition
-> product.md
```

Feature `spec.md` now records a Product Slice instead of owning another product document. This removes duplicate product truth and improves consistency across Features.

However, the migration left a serious execution-context gap:

- Feature Spec explicitly reads the Effective Product Definition when the Feature is created;
- later Work Breakdown, Test Design, Technical Design, Plan, Analyze Consistency, Resume, Execute, context recovery, and Subagent Handoff do not all use one mandatory product-context loading rule;
- the current Product Slice is mainly a reference and coverage table, not a complete local cognitive anchor;
- the runtime Resume inspection order reads Feature files but does not deterministically verify that the Requirement pointer and product source are still current;
- an Agent may therefore design technically coherent tasks, tests, or plans from stale or incomplete local understanding.

The failure is not that product truth lives outside the Feature. The failure is that Feature execution does not yet have a deterministic, freshness-checked view of that truth.

## 2. Accepted Principle

> Requirement `product.md` remains the product-semantics authority. Every Feature keeps a derived local context snapshot for fast and reliable execution. Before Task, Test, Plan, Resume, Execute, or Handoff relies on that snapshot, Agent Loop verifies the Requirement pointer and source digest mechanically. It reloads product meaning only when the source changed or the local slice is insufficient.

This preserves both correctness and interaction efficiency:

```text
Feature-local context for cognition
+ Requirement-level source for authority
+ cheap freshness verification
+ selective semantic reload on change
```

## 3. Severity And Failure Modes

Without this contract, the Agent may:

1. split Tasks by code layer while losing the user outcome or product boundary;
2. design Tests around the happy path while omitting accepted roles, permissions, states, exceptions, recovery, or terminal behavior;
3. write a technically valid Plan that violates a Product Rule or accepted ADR invariant;
4. resume after context compaction from Feature files that no longer reflect the effective Requirement source;
5. hand a Subagent an implementation task without the product facts needed to make safe local decisions;
6. continue long-running Feature Auto-Loop execution after the Requirement pointer, Product Definition, or applicable ADR changed;
7. mistake current code behavior for accepted product meaning and silently preserve implementation drift.

The risk increases as Features become longer-running and as Agent Loop reduces repeated Human confirmations.

## 4. Approaches Considered

### A. Always reread the complete Requirement `product.md` and every ADR

This maximizes source awareness but repeatedly spends context and time even when nothing changed. It encourages mechanical reading rather than focused reasoning and slows every stage transition.

**Rejected as the default.**

### B. Copy the complete Requirement `product.md` into every Feature

This gives strong local context but creates a second product truth. Copies drift, updates become ambiguous, and a Feature may accidentally redefine accepted Requirement meaning.

**Rejected.**

### C. Keep only the current thin Product Slice

This preserves source authority but does not reliably carry enough outcome, journey, rule, state, exception, and decision context for Task/Test/Plan design or later Resume.

**Rejected as insufficient.**

### D. Derived Feature Context Snapshot with source freshness verification

The Feature stores a compact execution-oriented snapshot derived from accepted Requirement and ADR sources. It records the authoritative locator and source digests. A read-only cross-platform checker verifies pointer, source, status, digest, and referenced anchors without loading the whole product document into the Agent's semantic context.

If evidence is unchanged, the Agent uses the local snapshot. If evidence changed, it reloads only the affected product/decision meaning, refreshes the snapshot, and checks downstream impact.

**Selected.**

## 5. Goals

1. Make Feature `spec.md` the deterministic bootstrap entry for ordinary Feature work.
2. Preserve Requirement `product.md` as the single product-semantics authority.
3. Give Tasks, Tests, Plans, Resume, Execute, Review, and Handoffs enough local product context to avoid design drift.
4. Detect an updated or redirected Effective Product Definition before relying on stale Feature context.
5. Avoid rereading entire Requirement and ADR documents when their verified sources have not changed.
6. Reload only relevant source sections when semantic context is needed.
7. Distinguish accepted product intent from current code reality.
8. Add no new Human Gate for a deterministic unchanged-source check.
9. Fail closed when source authority is missing, ambiguous, unconfirmed, or incompatible.
10. Remain compatible with existing and archived Features without bulk migration.

## 6. Non-Goals

This Proposal does not:

- move product ownership back into the Feature;
- restore new Feature-level `product.md`;
- let a Snapshot redefine accepted product meaning;
- make Feature context a project-memory replacement;
- require a separate `context.md` for every Feature;
- create a new canonical stage, lifecycle, message intent, or Auto Mode;
- make the checker perform semantic product design or rewrite files;
- require the Agent to read every Requirement source or every ADR body on every stage;
- authorize Requirement, ADR, Feature, Delivery Contract, code, Git, release, or publish actions;
- bulk-refresh closed or archived Features;
- replace code inspection, TDD, verification, Review, or Drift Check.

## 7. Artifact Ownership

| Artifact | Owns | Does not own |
|---|---|---|
| Requirement `README.md` | Requirement lifecycle, source inventory, unique Effective Product Definition pointer | product meaning itself |
| Effective Requirement `product.md` | accepted product meaning, concepts, flow, roles, states, facts, rules, exceptions, and product acceptance | technical implementation |
| accepted ADR | durable technical decision and Requirement Model technical landing | product meaning |
| Feature `spec.md` | Feature scope, Product Slice, Feature acceptance, and default local Context Snapshot | Requirement lifecycle or independent product truth |
| optional Feature `context.md` | expanded derived execution context for a complex Feature | independent authority |
| `tasks.md` | execution decomposition | product meaning |
| `tests.md` | correctness and verification design | product meaning |
| `plan.md` / `plans/*` | active implementation-unit construction plan | whole-product authority |
| code/tests/runtime | current implementation fact | permission to rewrite accepted product meaning |

The authority chain is:

```text
Requirement README pointer
-> Effective Product Definition
-> applicable accepted ADRs
-> derived Feature Context Snapshot
-> Product Slice
-> Tasks / Tests / Plan
-> code execution and verification
```

## 8. Default Storage Model

### 8.1 Ordinary Feature

For an ordinary Feature, store the Snapshot as a fixed section inside `spec.md`:

```text
.agent-loop/features/<feature-id>/
├── spec.md
├── tasks.md
├── tests.md
├── plan.md
└── notes.md
```

This keeps `spec.md` as the only required Feature bootstrap file and avoids creating another document for a small Feature.

### 8.2 Complex Or Long-Running Feature

When the Snapshot is too large to keep `spec.md` locally understandable, the Feature may use:

```text
.agent-loop/features/<feature-id>/
├── spec.md
├── context.md
├── tasks.md
├── tests.md
├── plan.md
└── notes.md
```

In this mode:

- `spec.md` retains the authoritative source locator, Product Slice, Snapshot summary, digest, freshness, and exact `context.md` link;
- `context.md` contains the expanded derived context;
- `context.md` is optional and conditionally created through the existing complex-artifact decision, not by default;
- the two files must agree on source identity and digest;
- deleting and regenerating `context.md` must not lose product truth because its authority remains upstream.

## 9. Feature Context Snapshot Contract

The default `spec.md` section is:

```markdown
## Feature Context Snapshot

- Requirement Set: .agent-loop/requirements/<requirement-id>/README.md
- Requirement Lifecycle: accepted | in-progress | partially-implemented | implemented
- Resolved Product Source: .agent-loop/requirements/<requirement-id>/product.md
- Product Definition Profile: brief | standard | legacy
- Product Review: confirmed | accepted | concept-foundation-not-needed
- Product Source SHA-256: <digest>
- Applicable Decisions: <ADR paths or none>
- Decision Source SHA-256: <path=digest list or none>
- Product Slice References: <source IDs and product.md anchors>
- Verified At: <ISO-8601 timestamp>
- Freshness: current | refresh-required | blocked

### Product Outcome

### Actors And Core Journey

### Applicable Product Rules And Invariants

### Applicable States, Exceptions, And Recovery

### Feature Boundary And Acceptance Context
```

Rules:

1. `Requirement Set` points to README, because README resolves the currently effective source.
2. Requirement, product, and decision paths are project-root-relative and confined to the one accepted real-directory memory root; root files, root symlinks, and dual roots fail closed. Paths are not relative to the Feature directory, so Feature archive/rehydrate movement cannot invalidate them.
3. `Requirement Lifecycle` records the current compatible lifecycle; a later delivery status does not replace Product Review.
4. `Resolved Product Source` records the result for traceability but never outranks README.
5. `Product Source SHA-256` is the Markdown text digest used for change detection. New evidence canonicalizes `CRLF` and lone `CR` to `LF`; readers accept legacy raw LF/CRLF digests so OS checkout behavior does not create false drift, while every other content change remains meaningful.
6. Product Slice References name stable IDs and/or exact `product.md#<anchor>` references.
7. Snapshot prose contains only the meaning needed to design and execute this Feature.
8. Snapshot prose must preserve accepted terminology and must not invent a local synonym or rule.
9. Code facts may be cited separately as implementation context but cannot be presented as accepted product meaning.
10. `Verified At` is a timezone-aware ISO-8601 timestamp.
11. `Applicable Decisions` must agree with the Feature's Product Requirement Source; two different decision sets are ambiguous authority and block use.
12. `Freshness` is a dependency judgment, not Feature lifecycle or product-review status.
13. The existing top-level `## Product Slice` remains the Feature responsibility/coverage table; the Snapshot points to it and supplies the context needed to interpret it rather than duplicating it.

## 10. Source Resolution And Freshness Check

Before relying on the Snapshot, Agent Loop performs this read-only flow:

```text
read Feature spec.md
-> locate Requirement Set README
-> resolve the unique Effective Product Definition pointer
-> verify Product Review is confirmed
-> verify Requirement lifecycle remains compatible with dependent execution
-> verify the resolved file exists inside the accepted memory root
-> calculate Product Source SHA-256 after Markdown newline canonicalization
-> verify Product Slice IDs/anchors still resolve
-> verify applicable ADR files exist, remain accepted, and are not review-required
-> compare recorded paths and digests
-> classify Freshness
```

### 10.1 `current`

Use `current` only when:

- one Requirement README resolves;
- it has one valid Effective Product Definition;
- Product Review remains `confirmed`;
- Requirement lifecycle is `accepted | in-progress | partially-implemented | implemented`;
- the resolved path equals the recorded source;
- the product digest equals the recorded digest;
- Product Slice IDs/anchors still resolve;
- applicable decisions exist, remain accepted, and have `Upstream Compatibility: current`;
- recorded decision digests match.

The Agent may then use the local Snapshot without semantically loading the complete product or ADR documents.

### 10.2 `refresh-required`

Use `refresh-required` when authority remains valid but:

- the Effective Product Definition path changed;
- the product digest changed;
- an applicable decision digest changed;
- the Feature does not yet have a Snapshot;
- the local Snapshot is incomplete for the current stage;
- a Product Slice anchor moved but can be resolved unambiguously.

`refresh-required` stops downstream generation until the Agent performs the semantic refresh procedure. It does not automatically require a Human decision.

### 10.3 `blocked`

Use `blocked` when:

- Requirement README is missing or ambiguous;
- Effective Product Definition is missing, duplicated, outside the accepted root, or unconfirmed;
- Requirement lifecycle is `proposed | deferred | superseded | rejected | reference-only`, unless the owning workflow has already resolved an explicit compatible replacement;
- Product Slice IDs/anchors no longer resolve;
- accepted Requirement meaning conflicts with the Feature boundary;
- an applicable ADR is missing, not accepted, superseded without a current replacement, or `review-required`;
- source meaning changed in a way that changes Feature scope, acceptance, product behavior, or an existing Human decision;
- the Agent cannot determine the correct source or meaning from evidence.

`blocked` routes to Requirements Discussion, Decision & Design compatibility review, Feature Definition Review, or Recovery according to the cause.

## 11. Low-Cost Fast Path

The ordinary path must not load the complete Requirement Product Definition into the Agent's context on every stage:

```text
Feature spec.md
-> mechanical pointer/digest/anchor check
-> unchanged
-> use local Snapshot
-> load only cited product or ADR sections when the current decision needs them
```

The checker should use Python 3.10+ standard library only and support macOS and Windows. It may:

- resolve paths;
- parse exact metadata fields;
- calculate SHA-256;
- check unique pointers;
- check file existence and root containment;
- verify stable IDs and Markdown anchors;
- report `current | refresh-required | blocked`;
- emit machine-readable-enough text for Agent consumption.

The checker must not:

- decide whether changed prose is semantically equivalent;
- rewrite `spec.md` or `context.md`;
- update Requirement or ADR files;
- mark a Feature accepted, ready, done, or closed;
- convert a failed check into a warning and continue.

## 12. Semantic Refresh Procedure

When Freshness is `refresh-required`, the Agent:

1. reads the changed Requirement README and resolved Product Definition;
2. reads only applicable Requirement sections, model IDs, Product Rules, and related ADR sections;
3. compares the old Snapshot and Product Slice with current accepted meaning;
4. classifies the effect:
   - `no-slice-impact`: source changed but Feature product meaning and acceptance are unchanged;
   - `derived-context-update`: local context wording, references, or applicable evidence must be refreshed without changing scope;
   - `feature-definition-impact`: scope, behavior, acceptance, role, state, rule, invariant, exception, recovery, or decision changed;
5. refreshes the Snapshot and digests for `no-slice-impact` or `derived-context-update`;
6. checks whether existing Tasks, Tests, Plans, and Handoffs need repair;
7. stops at the owning Human Gate for `feature-definition-impact`;
8. records the check and refresh evidence in Feature `notes.md`.

A formatting-only or unrelated upstream edit may be refreshed by the Agent after semantic comparison. A change to accepted Feature meaning returns to Feature Definition Review; a product ambiguity returns to Requirements Discussion; an ADR incompatibility returns to Decision & Design.

## 13. Mandatory Feature Context Load Contract

The following stages and re-entry paths must load or verify Feature context before producing or relying on downstream work:

| Stage / path | Required behavior |
|---|---|
| Feature Spec | resolve authority, create Snapshot, and record Product Slice |
| Requirement Checklist | verify Snapshot completeness and source references |
| Work Breakdown | load current Snapshot before creating or revising Tasks |
| Test Design | load current Snapshot before designing acceptance, state, permission, exception, and recovery coverage |
| Technical Design / Code Context | load current Snapshot and applicable ADRs before interpreting code choices |
| Plan Gate / Plan | require `Freshness: current` before accepting or executing a Plan |
| Analyze Consistency | verify source freshness and trace Product Slice through Tasks, Tests, and Plan |
| Execute Task / Story | reject stale or missing context before implementation |
| Resume / controller re-entry | use `spec.md` as bootstrap, run freshness check, then reconstruct stage state |
| context compaction recovery | reload the Snapshot and freshness evidence instead of relying on conversation memory |
| Subagent Handoff | include Feature path, Snapshot digest/freshness, Product Slice IDs, applicable ADRs, and exact assigned scope |
| Verify / Review | check implementation against current Snapshot and authoritative acceptance references |
| Drift Check / Close | verify that the accepted sources did not change during execution |

The contract applies equally in Strict Mode, Feature Auto-Loop, and Task Auto-Run. Auto Mode cannot continue with `refresh-required` or `blocked`.

## 14. Task, Test, And Plan Derivation Rules

### 14.1 Tasks

Every Task must map to at least one:

- Product Slice responsibility or acceptance;
- accepted ADR Design Slice;
- explicit technical prerequisite needed by a mapped Product Slice.

Technical prerequisites may not become independent product scope. Horizontal tasks must still name the later vertical slice that proves them.

### 14.2 Tests

Test Design must cover every applicable:

- acceptance criterion;
- actor and permission boundary;
- state transition and terminal;
- Product Rule or invariant;
- exception and recovery path;
- accepted ADR verification obligation.

An uncovered applicable item blocks readiness or requires a Human-approved substitute under existing rules.

### 14.3 Plans

Every active Plan must:

- name the Product Slice and Task it implements;
- preserve applicable product and ADR invariants;
- identify exact code facts separately from product intent;
- include verification that proves the mapped acceptance;
- avoid implementing out-of-scope Requirement meaning merely because nearby code exposes it.

## 15. Product Truth Versus Code Reality

Use this distinction:

```text
Requirement product.md
= what the accepted product should mean and do

accepted ADR
= how durable technical meaning lands

code / tests / runtime / environment
= what the implementation currently does
```

When code disagrees with a current accepted Snapshot:

- do not rewrite the Snapshot from code;
- classify implementation drift or unresolved authority conflict;
- inspect the owning evidence;
- implement or repair code only through the accepted Feature scope;
- return to Requirements Discussion only when the human intends to change product meaning.

## 16. Resume, Context Compaction, And Subagent Safety

### Resume

Resume begins:

```text
spec.md
-> Snapshot freshness check
-> current Feature ledger files
-> current code facts needed for the selected stage
```

It must not begin from `tasks.md` or `plan.md` alone.

### Context compaction

After context compaction, the Agent reloads the Snapshot and current check result before continuing Task/Test/Plan/Execute work. Conversation summaries cannot replace it.

### Subagent Handoff

The handoff references the authoritative Feature and source context; it does not copy a new product definition. The receiving Agent must verify freshness before acting. A handoff prepared under one Snapshot digest expires when that digest or applicable ADR digest changes.

## 17. Existing And Archived Feature Compatibility

- Existing new-model Features without a Snapshot become `refresh-required` when next resumed, planned, executed, reviewed, or reopened.
- Do not bulk-edit closed or archived Features.
- Rehydrated Features run the same freshness check before reopened execution.
- Legacy Features with Feature-level `product.md` continue through the existing legacy reader, but current Requirement/ADR authority wins when a reviewed owner exists.
- If legacy Feature `product.md` conflicts with Requirement authority, preserve evidence and route to Requirement Conflict Review / Recovery; do not silently merge them.
- Missing Snapshot is expected compatibility debt, not proof that the Feature is invalid.

## 18. Human Gates

This Proposal adds no standalone Snapshot Human Gate.

No new prompt is needed when:

- source verification is `current`;
- the Agent performs a mechanical check;
- a semantic refresh has no Product Slice, scope, acceptance, ADR, contract, security, data, or architecture impact;
- only derived references or digests are refreshed inside already authorized preparation work.

Stop at the existing owning Gate when:

- Feature definition or acceptance changed;
- accepted product meaning is ambiguous or reopened;
- an applicable ADR is incompatible or `review-required`;
- a Delivery Contract boundary changes;
- scope expands;
- a source cannot be uniquely resolved;
- another existing Human-gated action is triggered.

Freshness verification never authorizes code execution, Feature Auto-Loop, Subagent dispatch, Git actions, submit, close, release, or publish.

## 19. Relationship To Two-Gate Feature Construction

This repair should land before, or in the same coordinated implementation as, `feature-construction-two-gate-review.md`.

The second Implementation Readiness Review is trustworthy only when:

- Snapshot Freshness is `current`;
- Tasks map to current Product Slice responsibilities;
- Tests cover current product states, rules, exceptions, and acceptance;
- Plans preserve current product and ADR invariants;
- the complete package was generated from one verified source baseline.

Reducing Human interruptions without this repair would increase the time an Agent can autonomously execute from stale product context.

## 20. Implementation Surfaces

Implementation is expected to align at least:

- `SKILL.md`
- `references/runtime.md`
- `references/design.md`
- `references/product-definition.md`
- `references/stage-guides.md`
- `references/artifact-rules.md`
- `references/implementation-planning.md`
- `references/complex-artifacts.md` for optional `context.md`
- `references/workflow-checklists.md`
- `references/project-guidance.md`
- `templates/root-AGENTS.md`
- `templates/spec.md`
- optional `templates/feature-context.md`
- `references/validation-scenarios.md`
- `scripts/check-feature-context.py` as the Python 3.10+ standard-library read-only checker
- focused fixtures and regression tests
- `Usage.md`
- `CHANGELOG.md`

No version bump is included without separate Human approval.

Because this changes Inspection Order, Feature execution context, Resume, Plan readiness, Auto Mode stops, and cross-file workflow invariants, implementation is a coordinated workflow change. It requires the repository's mandatory full validation before completion. The Agent must not start that full validation silently when the human has asked to control when it runs; it should present the requirement and obtain the explicit instruction at the validation boundary.

## 21. Required Pressure Scenarios

Implementation validation must include:

1. unchanged Requirement pointer and digest uses the local Snapshot without complete semantic reload;
2. redirected Effective Product Definition produces `refresh-required`;
3. changed product digest with no Product Slice impact refreshes derived context and records evidence;
4. changed role, state, rule, exception, or acceptance blocks execution and returns to Feature Definition Review;
5. missing or ambiguous Requirement README pointer produces `blocked`;
6. unknown Product Slice ID or anchor produces `blocked`;
7. applicable ADR `review-required` blocks Plan and Execute;
8. Work Breakdown cannot create Tasks before loading current context;
9. Test Design detects an accepted exception/recovery path missing from tests;
10. Plan cannot pass when its Product Slice or Snapshot is stale;
11. Resume after context compaction reloads Snapshot and rechecks freshness;
12. Subagent Handoff expires after source digest change;
13. archived Feature discovery remains read-only and does not trigger bulk refresh;
14. rehydrated Feature checks freshness before reopened execution;
15. legacy Feature `product.md` remains readable but cannot override current Requirement authority;
16. the checker cannot mutate Feature, Requirement, ADR, or project memory;
17. Auto Mode stops on `refresh-required | blocked`;
18. current code behavior conflicting with product truth is reported as drift rather than copied into the Snapshot.

## 22. Acceptance Criteria

1. Requirement `product.md` remains the only new product-semantics owner.
2. Ordinary Features carry a complete-enough Snapshot inside `spec.md`.
3. A separate `context.md` is optional and used only when complexity justifies it.
4. A Feature can identify the real product source from its local `spec.md`.
5. The real source is confirmed through Requirement README rather than trusting a cached direct path.
6. Pointer, existence, status, digest, and anchor checks are read-only and cross-platform.
7. Unchanged sources avoid full product/ADR semantic reload.
8. Changed sources force semantic comparison before downstream work.
9. Task, Test, and Plan derivation explicitly traces to Product Slice and applicable decisions.
10. Resume, context recovery, Execute, Verify, Review, and Subagent Handoff use the same load contract.
11. Stale context cannot continue through Feature Auto-Loop or Task Auto-Run.
12. The Agent may refresh derived context without a new Human Gate only when accepted Feature meaning is unchanged.
13. Product, scope, acceptance, or ADR meaning changes return to their existing Human Gate.
14. Existing and archived Features are not bulk-migrated.
15. Focused regression tests and mandatory coordinated full validation prove that the repair does not weaken existing Feature, Requirement, ADR, Gate, verification, or close behavior.

# Feature Construction Two-Gate Review Proposal

**Version:** v1.5.1  
**Status:** implemented; single-feature validation 100/100 STRONG; full validation pending  
**Created:** 2026-07-25  
**Human intent:** keep every quality artifact and check, but replace per-stage approval with two meaningful human decisions

## 1. Problem

Agent Loop currently has the right construction stages:

```text
Feature Spec
-> Requirement Checklist
-> Work Breakdown
-> Delivery Contract If Needed
-> Test Design
-> E2E Discovery If Web
-> Technical Design / Code Context
-> Plan Gate
-> Execute
```

The problem is not the existence of these stages. The default Strict Mode says:

```text
Before stage: ask permission.
After stage: ask continue / revise / pause / submit / close.
```

This turns internal Agent work into repeated human interruptions. A human may be asked whether the Agent can enter Work Breakdown, whether it can continue to Test Design, whether it can inspect E2E capability, whether it can prepare Technical Design, and whether it can write a Plan. These questions do not normally require independent human judgment.

The current Feature Auto-Loop is intended to reduce these pauses, but its contract is not fully coherent:

- it becomes available only after Feature Spec and Requirement Checklist acceptance;
- Work Breakdown still says the human accepts granularity and order;
- Test Design still says the human accepts how correctness will be proven;
- normal Plan acceptance still appears human-only;
- Execute rules still contain separate task/story selection language;
- conservative Agents therefore continue to stop at nearly every stage.

The result is high interaction cost without a corresponding increase in correctness.

## 2. Accepted Human Principle

The human-approved direction is:

> Stop once for the checked Feature Spec. Then let the Agent prepare every implementation document and run every non-mutating readiness check. Stop once more for the complete implementation package. If the human accepts it, begin implementation.

This is a batching change, not a quality reduction.

```text
Stage still exists
!=
Human must approve that stage separately
```

## 3. Approaches Considered

### A. Keep per-stage approval and improve prompt wording

This preserves the current model but does not solve the interruption problem. The human still reviews partial artifacts without seeing the complete implementation design.

**Rejected.**

### B. Two meaningful review gates

The Agent first presents a checked Feature Spec. After acceptance, the Agent prepares the complete implementation package without code execution and without per-stage prompts. The human then reviews the package once and may approve implementation.

**Recommended and selected.**

### C. Use one approval only, immediately before implementation

This is faster, but the Agent may spend substantial effort preparing tasks, tests, and plans against an incorrect Feature scope. It also weakens the Product Slice and acceptance boundary.

**Rejected.**

## 4. Goals

1. Preserve Feature Spec, Requirement Checklist, Work Breakdown, Test Design, E2E Discovery, Technical Design, Plan Gate, Analyze Consistency, verification, review, drift, and memory quality.
2. Replace ordinary per-stage confirmation with two human review gates.
3. Let humans review complete decisions instead of partially prepared documents.
4. Let the Agent autonomously prepare all implementation artifacts after the Feature definition is accepted.
5. Let one bounded second decision accept the implementation package and start Agent-ready execution.
6. Stop only when a new decision belongs uniquely to the human or an existing hard gate is triggered.
7. Keep Requirement, ADR, Delivery Contract, external mutation, Git, submit, close, and release boundaries explicit.

## 5. Non-Goals

This Proposal does not:

- remove any construction stage or artifact;
- allow implementation before a checked Feature Spec is accepted;
- allow implementation before a complete implementation package is reviewed;
- let the Agent redefine accepted Requirement product meaning;
- make Delivery Contracts default artifacts;
- silently accept breaking contract changes;
- authorize branch actions, subagents, external writes, credentials, production changes, Git actions, submit, close, release, or publish;
- turn validation success into human acceptance;
- allow a partial or placeholder Plan to pass the second gate;
- change Bug Resolution Path, Requirement lifecycle, ADR lifecycle, or Feature close gates;
- bump the Agent Loop version by itself.

## 6. New Feature Construction Flow

```text
Explicit implementation request or separately authorized Feature construction
-> Agent drafts Feature Spec and Product Slice
-> Agent runs Requirement Checklist
-> Gate 1: Feature Definition Review
   -> revise: update Spec and repeat Gate 1
   -> pause: stop
   -> accept: authorize implementation-package preparation
-> Agent prepares the complete implementation package
   -> Work Breakdown
   -> Delivery Contract assessment / exact candidate if triggered
   -> Test Design
   -> E2E Discovery if applicable
   -> Technical Design / Code Context
   -> Plan Gate / Plan
   -> package consistency and coverage review
-> Gate 2: Implementation Readiness Review
   -> revise: update the affected package and repeat Gate 2
   -> approve documents only: package accepted, no implementation
   -> approve and start: package accepted and Feature Auto-Loop enabled
   -> pause: stop
-> Execute Agent-ready tasks
-> Verify
-> Review
-> Drift Check
-> Project Memory Update
-> existing Completion / Submit / Close gates
```

## 7. Feature Start Authorization

The two-gate flow does not add a third prompt merely to create a Feature directory.

An explicit human request such as “implement this accepted requirement”, “start this Feature”, or an equivalent unambiguous instruction satisfies Feature construction authorization for the disclosed Requirement/phase/slice. The Agent may create the draft Feature workspace and prepare Gate 1.

If the human is only discussing requirements, accepting a Product Definition, recording a Requirement, or accepting an ADR, Feature construction remains unauthorized. The Agent must not infer Feature start.

Therefore:

```text
explicit implementation request
= Feature start authorization
!= Feature Definition acceptance
```

The human does not need to say “yes” twice before seeing the first Spec.

## 8. Gate 1 — Feature Definition Review

### 8.1 Purpose

Gate 1 freezes what will be built before the Agent invests in detailed implementation preparation.

### 8.2 Required Agent work before Gate 1

The Agent must:

- resolve one accepted Requirement Set and confirmed Effective Product Definition;
- confirm Design Readiness is `design-not-needed` or `completed`;
- resolve applicable accepted ADRs and assigned Design Slices;
- write the draft Feature `spec.md`;
- record the Product Slice;
- run Requirement Checklist;
- repair every fact-determined ambiguity it can resolve from accepted sources;
- expose unresolved product decisions instead of hiding them in downstream tasks.

### 8.3 Human Review Summary

Gate 1 presents one compact review:

| Area | Required content |
|---|---|
| Goal | problem, target outcome, user/business value |
| Accepted source | Requirement Set, Effective Product Definition, phase/slice |
| Scope | in scope, out of scope, behavior added/modified/removed |
| Product Slice | source rules/IDs to Feature responsibility and acceptance |
| Acceptance | measurable acceptance criteria and important exceptions |
| Decisions | applicable ADRs, Feature-local decisions, unresolved blockers |
| Checklist | pass/fail result and repaired ambiguities |
| Next action | prepare complete implementation package; no target implementation yet |

### 8.4 Human choices

- `Accept definition and prepare implementation package`
- `Revise definition`
- `Pause`

Gate 1 acceptance authorizes the bounded preparation run described below. It does not authorize target code changes, external mutations, Git actions, submit, or close.

## 9. Implementation Package Preparation

Implementation Package Preparation is a bounded continuation granted by Gate 1. It is not a new global Gate Mode and does not execute target behavior.

The Agent proceeds without asking before or after each internal stage.

### 9.1 Required package

The package contains every applicable artifact needed to make implementation executable:

| Area | Owning artifact |
|---|---|
| Work Breakdown | `tasks.md` and triggered detail files |
| Verification strategy | `tests.md` and triggered test-case details |
| E2E capability and cases | `tests.md`, `tests/e2e/*`, and a proposed durable memory update when applicable |
| Technical / code context | `plan.md`, task detail, or `notes.md` according to existing ownership |
| Construction plan | `plan.md` or triggered `plans/*` with current pointer |
| Delivery boundary | no contract by default; exact candidate and action disclosure only when triggered |
| Risks and rollback | implementation package summary and Plan |
| Traceability | Spec -> task -> test -> plan coverage |
| Readiness | Agent-ready / Human-gated classification with reasons |

### 9.2 Internal stage behavior

During package preparation:

- Work Breakdown is generated and self-reviewed without a separate approval prompt.
- Test Design is generated and checked against acceptance without a separate approval prompt.
- E2E Discovery runs when applicable without a separate approval prompt.
- Technical Design / Code Context inspects code and records concrete findings without a separate approval prompt.
- Plan Gate still runs as a quality method, but Plan creation does not require a separate human interruption.
- Analyze Consistency may run before Gate 2 when it only reads and validates package coherence.
- the Agent must not modify target implementation code.

### 9.3 Preparation stop conditions

The Agent stops before Gate 2 only when:

- Requirement meaning, Feature scope, or acceptance must change;
- Design Readiness becomes unresolved;
- a new ADR or ADR compatibility decision is required;
- a security, data, permission, architecture, migration, dependency, external-service, or public-interface decision cannot be determined from accepted evidence;
- exact files, interfaces, verification, or rollback cannot be established;
- unrelated dirty work prevents reliable preparation;
- a Delivery Contract action cannot be fully disclosed for review;
- the package contains a Human-gated task that must be decided before the rest of the package can be made coherent.

Fact-determined discoveries do not stop the preparation run. The Agent resolves and records them.

## 10. Delivery Contract Handling

Delivery Contract rules remain conditionally Human-gated.

During package preparation:

1. detect whether a durable producer-consumer boundary exists;
2. do not create a default contract;
3. when a contract is needed, prepare the exact proposed contract content response-locally or in the Gate 2 review material;
4. disclose the exact path, consumers, compatibility, verification, and intended lifecycle action;
5. let Gate 2 explicitly name the contract creation and acceptance decisions when the complete content is reviewable.

One Gate 2 response may authorize multiple separately named bounded actions when the human sees their exact content and consequences. It must not use vague “approve package” language to hide contract creation or acceptance.

Breaking changes to an accepted or implemented contract remain a separate hard stop after affected-consumer analysis. They cannot be bundled implicitly.

## 11. Gate 2 — Implementation Readiness Review

### 11.1 Purpose

Gate 2 lets the human review the whole implementation design in one place and decide whether implementation may begin.

### 11.2 Readiness conditions

Gate 2 is not ready until:

- every accepted Spec criterion maps to implementation work and verification;
- task order, dependencies, and barriers are explicit;
- tests cover functional, regression, API/integration, E2E/manual, and Bug-specific needs where applicable;
- E2E applicability and executable path are known or an explicit substitute decision is presented;
- code context uses real files, symbols, interfaces, and local patterns;
- Plan contains executable steps, TDD/verification commands, expected results, risks, and rollback;
- no placeholder such as `TBD`, `TODO`, “write tests”, or invented interface remains;
- all tasks are classified `Agent-ready` or `Human-gated`;
- all required conditional actions are separately named;
- package self-review and consistency analysis pass.

### 11.3 Human Review Summary

| Area | Required content |
|---|---|
| Frozen definition | Feature Spec identity and digest |
| Package inventory | tasks, tests, E2E, technical context, Plan, conditional contracts |
| Coverage | acceptance -> tasks -> tests -> plan |
| Execution shape | task/story order, parallel/barrier structure, Agent-ready work |
| Human decisions | only unresolved or conditionally gated items |
| Risk | architecture, data, security, migration, dependency, external effects |
| Verification | exact RED/GREEN, focused, integration, E2E/manual, and full commands as applicable |
| Rollback | bounded implementation rollback and residual risks |
| Authorization | documents only, or documents plus Feature Auto-Loop start |

### 11.4 Human choices

- `Approve package and start implementation`
- `Approve package only; do not implement yet`
- `Revise package`
- `Pause`

`Approve package and start implementation` simultaneously:

1. accepts the disclosed implementation package;
2. enables Feature Auto-Loop for the accepted Feature scope;
3. authorizes execution of the listed Agent-ready tasks;
4. does not authorize Human-gated tasks or any preserved external/Git/release gate.

There is no third generic prompt asking whether to enable Feature Auto-Loop.

After package-only acceptance, a later explicit instruction to start the same Feature may enable Feature Auto-Loop without repeating the full Gate 2 review only when the Agent freshly confirms:

1. Feature Context remains `CURRENT`;
2. the accepted Spec, Tasks, Tests, and Plan package is unchanged;
3. no new stop condition or Human-gated item exists.

Definition drift returns to Gate 1. Material package drift returns to Gate 2.

The decisions must survive conversation loss. Feature `notes.md` records the Gate 1 Spec digest, Gate 2 decision and time, complete reviewed package digest, non-rotatable stable digest, accepted Agent-ready task IDs, active Plan scope, matching Plan/No-Plan evidence, and Auto-Loop state. The read-only Feature review checker rejects missing evidence, invalid decision/state pairing, stale package-only start, non-Agent-ready task claims, Plan/scope mismatch, or execution outside the accepted task set.

## 12. Execution After Gate 2

After `Approve package and start implementation`, the Agent continues through:

```text
Agent-ready Execute
-> Verify
-> Review
-> Drift Check
-> Project Memory Update
```

It does not ask before or after each stage.

It stops only when:

- a listed Human-gated task is reached;
- implementation would change the accepted Feature definition;
- implementation materially changes the accepted package, risk, interface, verification, or rollback;
- a new contract, dependency, migration, security, data, permission, production, credential, external-service, architecture, or public-interface decision appears;
- verification fails beyond bounded repair;
- review finds scope or design drift;
- subagent dispatch, branch action, external mutation, submit, commit, push, PR, merge, release, publish, pause, or close is requested.

Small fact-determined Plan refinements may be recorded without repeating Gate 2 when they do not change scope, acceptance, task boundaries, interfaces, risk class, verification obligations, or rollback.

For a multi-task Feature, Gate 2 accepts the complete Agent-ready task set and its ordering/barriers, plus the initial active task/story Plan. Feature Auto-Loop may later rotate `plan.md` to another accepted task/story without another Gate 2 only when the stable package digest still matches and the new Plan passes Plan Gate, Analyze Consistency, and the Feature review checker. A new task, changed task/test boundary or order, or material interface/risk/rollback/verification change repeats Gate 2.

## 13. Revision Routing

| Discovery | Return point |
|---|---|
| Product meaning, scope, Product Slice, or acceptance changes | Gate 1 |
| Task split/order, test strategy, code context, Plan, risk, or rollback changes materially | Gate 2 |
| Fact-determined implementation detail inside accepted package | continue and record |
| New shared/project-level design need | Decision & Design, then Gate 1 or Gate 2 according to impact |
| Delivery Contract creation/acceptance fully disclosed in package | explicit named action in Gate 2 |
| Breaking accepted contract change | separate Delivery Contract Human Gate |
| Git, external, production, release, or close action | existing independent gate |

## 14. Gate Count After This Change

For an already accepted Requirement with no new ADR:

```text
explicit implementation request
-> Gate 1: Feature Definition Review
-> Gate 2: Implementation Readiness Review
-> implementation
```

This is two meaningful review stops.

For a raw Requirement, upstream product and lifecycle gates remain:

```text
Product Human Review
-> Requirement Record / Archive
-> Requirement lifecycle
-> conditional ADR gates
-> Gate 1
-> Gate 2
```

Upstream Requirement and ADR decisions are not duplicated inside Feature construction.

## 15. Gate Modes

### 15.1 Strict Mode

Strict Mode remains available when the human explicitly prefers stage-by-stage control.

It must no longer be the only practical path produced by conservative interpretation. After Gate 1, the Agent recommends complete package preparation as the normal Feature construction behavior.

### 15.2 Feature Auto-Loop

Feature Auto-Loop begins when Gate 2 explicitly selects `Approve package and start implementation`.

It no longer needs a separate enablement question after the implementation package is accepted.

### 15.3 Task Auto-Run

Task Auto-Run remains available when the human approves documents but wants to execute only one selected task/story later.

It does not replace Gate 2 package acceptance.

## 16. Artifact And Status Model

Do not create a new workspace hierarchy or duplicate stage artifacts.

Use one compact readiness field plus a durable review baseline in the existing Feature notes/current summary:

```text
Implementation Readiness: preparing | review-ready | accepted
```

Rules:

- `preparing`: Gate 1 accepted; package is being built;
- `review-ready`: package completeness and consistency checks passed; Gate 2 pending;
- `accepted`: Gate 2 accepted the package;
- revision returns to `preparing`;
- Feature lifecycle remains owned by existing Feature status rules;
- this field is not permission for Git, release, external mutation, submit, or close.

The durable review baseline stores:

- Gate 1 decision and exact Spec SHA-256;
- Gate 2 decision and review time;
- complete Package Files/Digest, including the initial Plan;
- Stable Files/Digest, excluding rotatable `plan.md`;
- accepted Agent-ready task IDs and current Active Plan Scope;
- compact `plan.md`, one `plans/<detail>.md`, or explicit `no-plan:<accepted-task>` evidence matching the active scope;
- Feature Auto-Loop enabled/disabled.

This is evidence, not a new source of Feature meaning. Existing Spec, Tasks, Tests, Plan, and Notes owners remain unchanged.

## 17. Required Runtime Changes

This is a coordinated workflow change because it changes Human Gate placement and Feature Auto-Loop activation.

Implementation must align at least:

- `references/design.md`
- `references/runtime.md`
- `references/concepts.md`
- `references/stage-guides.md`
- `references/human-review-summary.md`
- `references/workflow-checklists.md`
- `references/artifact-rules.md`
- `references/project-guidance.md`
- `templates/root-AGENTS.md`
- affected document templates
- `references/validation-scenarios.md`
- executable regression tests
- `README.md` / `Usage.md` only if human-facing explanation currently promises per-stage behavior
- `CHANGELOG.md`

Historical Proposals and reports remain historical evidence and are not rewritten as runtime authority.

## 18. Validation Requirements

Implementation requires full skill validation because canonical Human Gate placement, runtime progression, Feature Auto-Loop activation, root guidance, and cross-file invariants change.

At minimum, RED/GREEN scenarios must prove:

1. After Gate 1, the Agent prepares tasks, tests, E2E discovery, technical context, and Plan without per-stage prompts.
2. The Agent does not modify target implementation before Gate 2.
3. Gate 2 rejects missing tasks, tests, code context, Plan, coverage, verification, risk, or rollback.
4. `Approve package and start implementation` activates Feature Auto-Loop without another generic prompt.
5. `Approve package only` does not authorize implementation.
6. A Spec or acceptance change returns to Gate 1.
7. A material package change returns to Gate 2.
8. Fact-determined implementation detail does not create a new gate.
9. Delivery Contract creation/acceptance is separately named and visible inside Gate 2 when fully disclosed.
10. Breaking contract changes still stop separately.
11. New architecture, security, data, migration, dependency, external, or public-interface decisions stop.
12. Agent-ready tasks continue through implementation, verification, review, drift, and memory without per-stage prompts.
13. Human-gated tasks stop before execution.
14. Branch, subagent, external mutation, submit, commit, push, PR, merge, release, publish, pause, and close gates remain intact.
15. Root guidance and runtime present the same two-gate model.
16. Existing Bug, Requirement, ADR, Task Done, Feature Completion, and recovery scenarios remain valid.
17. Missing durable Gate evidence fails closed after context loss or cross-session resume.
18. A package-only start fails when any reviewed package file drifted.
19. Multi-task Plan rotation passes only inside the accepted task set with unchanged stable evidence.
20. Stable artifact drift or a new task cannot hide as a Plan rotation.

## 19. Acceptance Criteria

This Proposal is ready for implementation planning when the human confirms:

1. Feature construction has exactly two normal review stops after an explicit implementation request.
2. Gate 1 accepts the checked Feature Spec and authorizes implementation-package preparation.
3. Package preparation runs all applicable design/planning stages without target implementation and without per-stage prompts.
4. Gate 2 reviews the complete implementation package.
5. Gate 2 may accept documents only or accept and start Feature Auto-Loop.
6. Only true human decisions and preserved hard gates interrupt autonomous work.
7. All existing quality stages remain mandatory even when their separate approval prompts are removed.

## 20. Human Review

**Decision:** accepted by the human on 2026-07-25  
**Accepted direction:** two meaningful Feature construction gates  
**Implementation authorized:** yes; write the implementation plan, preserve the full-validation boundary, and do not infer Git or release authorization

# Open Feature Authority And Agent-Owned Checker Light Gates Proposal

**Version:** v1.5.x design line; no version bump is authorized by this Proposal
**Status:** implemented, validated, and released as `stable-v1.5.4`
**Created:** 2026-08-10
**Human Direction:** open Feature authority, Agent-owned judgment and self-rescue, rare Human exception, and continued Checker lightening were confirmed in conversation on 2026-08-10
**Scope:** Feature authority resolution, canonical Checker responsibility, Agent Checker Rescue, one-Gate substitute evidence, developer feedback, and targeted Phase 2 Checker lightening

## 1. Problem

Agent Loop intends Checkers to expose objective facts while the Agent owns workflow and semantic judgment. The current implementation does not consistently follow that boundary.

The immediate defect is the universal Feature Context scanner. Every current Feature is required to run `scripts/check-feature-context.py`, but the scanner assumes one authority shape:

```text
Requirement Set
-> Effective Product Definition
-> Feature Context Snapshot
```

It does not first determine the Feature's actual authority. A valid maintenance Feature driven by accepted Bug Expected Behavior may record:

```text
Authority Type: Bug Expected Behavior
Requirement Set: none
Effective Product Definition: .agent-loop/bugs/<bug-id>/README.md
```

The current scanner treats `none` as a Requirement path and returns a hard failure before the Agent can inspect the Bug authority. Human-delegated work and other evidence-backed authority shapes have the same structural risk.

This is not only one conditional bug. Current runtime, Feature guidance, `templates/spec.md`, specialized validators, and tests still preserve parts of the older assumption that all Feature work must resolve through one Requirement Set. Fixing only the Python branch would leave generated artifacts and downstream routing inconsistent.

Other canonical Checkers also contain heavier-than-needed behavior:

- specialized Requirement/Product/Concept validation has no explicit not-applicable result when the Feature is owned by another authority;
- Onboarding validation uses fixed wording, self-declared `covered` / `PASS`, and exact section tokens as a hard proxy for semantic completeness;
- Lightweight Change scanning lets one malformed historical card invalidate the complete inventory instead of reporting the affected record for Agent repair;
- current Checker Failure Recovery requires an isolated temporary patch, RED/GREEN, negative controls, and a second Human substitute decision even when the Agent can prove the needed facts directly without modifying a Checker.

The result is repeated Checker Recovery work, unnecessary Human interruption, and Agents rewriting valid artifacts to satisfy an outdated assumption.

## 2. Accepted Product Principle

> Checker reports mechanically determinable facts. Agent determines what those facts mean and owns the normal repair or continuation decision. Human attention is reserved for real semantic decisions and rare, bounded substitute authorization when a Checker limitation still prevents one named Gate.

Responsibility is:

```text
Checker -> facts
Agent -> interpretation, repair, routing, and recommendation
Human -> genuine decision or rare one-Gate substitute authorization
```

This Proposal does not create a general bypass. It reduces false hard failures at their source and keeps one exceptional Human decision only for residual Checker defects.

## 3. Approaches Considered

### A. Add only two new Feature source enum values

Add `Bug Expected Behavior` and `Human Delegation` beside the existing Requirement source and retain a closed whitelist.

This fixes the known examples but repeats the original design error. A later accepted authority shape would again require a Checker release before the Agent could proceed.

**Rejected.**

### B. Keep strict Checkers and use Human override for every mismatch

Leave the current scripts unchanged and ask the human to approve every suspected false positive.

This lets work continue but moves normal Agent responsibility to the human, creates repeated prompts, and normalizes exceptions instead of repairing the contract.

**Rejected.**

### C. Open Feature authority plus fact-only Checkers and Agent Checker Rescue

Make the Feature authority model open, provide adapters for common authority shapes, return advisory facts for unknown but inspectable sources, and reserve hard failure for objective conditions that prevent safe evaluation or exact execution. Let the Agent repair and continue ordinary cases through a response-local Agent Checker Rescue method. Reuse `accepted-for-this-gate` only when a small residual Checker risk still needs one bounded Human decision; preserve non-rescuable physical, safety, semantic, and authorization boundaries.

**Selected.**

## 4. Goals

1. Remove the universal assumption that every Feature must use a Requirement Set as its primary authority.
2. Support Feature Authority, Bug Authority, and Human Authority as known adapter families without making them a closed enum.
3. Let unknown but evidence-backed authority shapes reach Agent assessment instead of returning an automatic hard failure.
4. Make applicability explicit so a specialized Checker cannot validate an artifact outside its owning domain.
5. Keep objective path, reference, identity, digest, plan, transaction, and recovery facts machine-checkable.
6. Put semantic sufficiency, impact, repair, and workflow routing back under Agent ownership.
7. Let the Agent rescue a proven Checker limitation without interrupting the human when independent evidence is complete, safety is intact, and the next action remains inside existing authorization.
8. Reuse a bounded Human substitute decision without requiring a temporary Checker patch when a small residual risk still needs one named Gate decision.
9. Produce a sanitized developer-feedback draft for a proven or likely Checker limitation.
10. Preserve every existing Product, ADR, Feature, Bug, Task, Delivery Contract, Git, release, external, submit, pause, and close Human Gate.
11. Preserve exact execution safety for Archive/Apply and Full Memory Audit/Recovery.

## 5. Non-Goals

This Proposal does not:

- add a canonical stage, message intent, lifecycle, Auto Mode, or mandatory artifact family;
- define a closed universal list of Feature authority types;
- let a Checker choose product meaning, Feature scope, acceptance, risk, or Human authorization;
- add a global `--force`, `--skip-checks`, or persistent bypass flag;
- turn `CURRENT`, `CHANGED`, `NOT_APPLICABLE`, or exit `0` into execution permission;
- treat Agent Checker Rescue as a Checker `PASS`, durable authorization, new lifecycle status, or replacement for an existing Human Gate;
- let Human substitute authorization hide a real safety contradiction;
- remove Product Human Review, ADR acceptance, Feature Gate 1/2, Task Done Gate, verification, Submit, Close, Git, release, or external-action gates;
- weaken exact plan SHA-256, executor confinement, transaction journal, post-check, or rollback;
- bulk-migrate existing target-project Feature artifacts;
- create target-project `.agent-loop/` artifacts in this Skill source repository;
- change the Skill version, branch, tag, installed Skill, or release state;
- implement the changes merely because this Proposal is written.

## 6. Common Checker Responsibility Model

### 6.1 Conceptual results

Fact and freshness Checkers use this common conceptual result model:

| Result | Default exit | Meaning | Owner of next judgment |
|---|---:|---|---|
| `CURRENT` | `0` | applicable objective facts resolve and match | Agent may rely on the facts inside existing authorization |
| `CHANGED` | `0` | a fact differs, is incomplete, unknown, or needs review | Agent assesses impact, repairs derived evidence, changes route, or asks one question |
| `NOT_APPLICABLE` | `0` | this specialized Checker does not own the current authority/artifact shape | Agent selects the applicable adapter or continues with direct evidence |
| `BLOCKED` | `1` | the Checker reports that it cannot safely evaluate or that an exact executor cannot safely act | Agent reruns and classifies the result; a proven Checker limitation may use Agent Checker Rescue, while a real physical contradiction stops |

Surface-specific names may remain where they already communicate the same model. For example, the Root AGENTS checker may retain `STRUCTURAL_CURRENT | STRUCTURAL_CHANGED | STRUCTURAL_INVALID`, Archive scan may retain structured plan findings, and exact transaction validators may retain `PASS` / error. This Proposal does not rename outputs merely for uniform appearance.

### 6.2 Checker-owned facts

A Checker may determine:

- whether a declared local file or directory exists and is readable;
- whether a local project-relative path remains inside its declared physical boundary;
- whether exactly one required local authority target resolves when uniqueness is mechanically required;
- whether declared IDs, references, and target paths exist;
- whether duplicate objective identifiers or mutually contradictory current pointers exist;
- whether recorded digests, timestamps, and normalized source facts match;
- whether a fixed machine-readable table or field can be parsed;
- whether an exact plan SHA-256 matches the reviewed plan;
- whether transaction journal, preimage, post-check, and rollback evidence are mechanically complete;
- deterministic per-item facts and advisory findings.

### 6.3 Agent-owned judgments

A Checker must not decide:

- which authority type should own a Feature;
- whether an unfamiliar authority is trustworthy;
- whether Requirement, Bug, Human instruction, Feature history, code, test, ADR, or Contract meaning is semantically sufficient;
- whether changed prose affects accepted Product Slice, scope, acceptance, risk, or implementation boundary;
- whether equivalent wording is good enough;
- whether a document is useful, complete, or high quality merely because keywords exist;
- whether the human has reliably granted a Gate;
- whether a `CHANGED` fact requires repair, Gate 1, Gate 2, Requirements Discussion, Decision & Design, Recovery, or no workflow change;
- whether work should continue after a non-safety finding.

### 6.4 Hard-failure boundary

`BLOCKED` or an equivalent non-zero hard result is reserved for objective conditions that prevent safe evaluation or exact execution, including:

- the requested project root or required declared local artifact cannot be read;
- a declared local write or authority path escapes its physical project boundary;
- dual, cyclic, broken, external, or non-directory memory-root authority prevents selecting one local memory root;
- mutually exclusive current authority pointers make the local source physically ambiguous;
- an executor plan hash, preimage, target, journal, post-check, or restore condition does not match the exact reviewed operation;
- an executor would write outside its reviewed project/plan boundary;
- a real transaction cannot be restored reliably.

An external URL, Human conversation locator, external ticket identifier, or other non-file evidence is not parsed as a local project path. The Agent evaluates that evidence through its owning workflow.

Unknown authority kind, missing optional cached evidence, stale digest, incompatible wording, a specialized Checker receiving the wrong artifact class, or an Agent-repairable record shape is not by itself `BLOCKED`.

## 7. Open Feature Authority Model

### 7.1 Authority is open, not an enum whitelist

Every Feature identifies one current primary authority description and may identify supporting authorities. The model recognizes common adapters but does not reject an unfamiliar descriptive type solely because it is not in a built-in enum.

Known adapter families are:

1. **Feature Authority** — ordinary Feature definition evidence. It may derive from an accepted Requirement Product Definition / Product Slice and applicable accepted decisions, or cite accepted ADR / Delivery Contract evidence and an existing or reopened Feature when those sources actually define the work. The Feature spec records the effective slice; it never authorizes or accepts itself;
2. **Bug Authority** — Bug README plus accepted Expected Behavior evidence and Human-confirmed Resolution Path / Fix Feature target;
3. **Human Authority** — reliable current Human instruction or preserved Human decision evidence defining the Feature goal, boundary, and acceptance direction.

These are high-level adapter families, not the only three allowed strings. A Feature may also use a stable external obligation, operational evidence, or a mixed authority chain. The Agent must name the actual source, explain which family or custom adapter applies, and resolve one effective primary authority. The Checker does not maintain a closed allowlist.

### 7.2 Canonical Feature authority fields

New Feature specs use one authority block with descriptive values:

```text
## Feature Authority

Authority Type: <descriptive authority label>
Primary Authority Reference: <project-relative artifact, stable evidence locator, or Human decision locator>
Supporting Authority References: none | <references>
Authority Summary: <what behavior/boundary this authority establishes>
Agent Authority Assessment: current | changed | unresolved
```

The exact final field names may be refined during implementation only if they preserve this meaning and compatibility. `Authority Type` is descriptive metadata, not a validator whitelist.

When the Feature Authority family uses a Requirement Product Definition, retain the bounded Product Requirement Source and Product Slice details. When Bug Authority applies, Requirement Set may truthfully be `none`; the Bug reference and accepted Expected Behavior own the source check. Human Authority does not require the Agent to invent a Requirement or Bug artifact merely to satisfy a scanner.

### 7.3 Compatibility reader

Existing `spec.md` files that contain only `## Product Requirement Source` remain valid as the Requirement Product Definition sub-adapter of Feature Authority. No bulk migration is required.

Existing legacy Requirement, Concept Foundation, Feature Product Brief, and Product Slice readers remain compatible. An authorized Feature refresh may add the new authority block when the Agent is already updating that Feature; absence alone does not rewrite historical artifacts.

### 7.4 Feature Context scanner routing

The universal Feature Context scanner first resolves the authority shape before applying an adapter:

```text
read Feature spec
-> resolve declared/current authority shape
-> known adapter?
   -> Feature Authority: inspect the declared Requirement/Product/ADR/Contract/existing-Feature facts that apply
   -> Bug Authority: inspect Bug/Expected Behavior/Resolution Path/Feature-locator facts
   -> Human Authority: report inapplicable local artifact checks and preserve Agent/Human evidence requirements
-> unknown but inspectable authority
   -> CHANGED / advisory with authority facts for Agent assessment
-> objective physical contradiction
   -> BLOCKED
```

The scanner must not send `Requirement Set: none` through a Requirement path resolver before checking the authority shape.

The scanner may report multiple supporting authorities. It does not decide which meaning wins when they conflict; it reports the conflict and the Agent routes to the owning Human Gate.

### 7.5 Feature Human Gates remain authoritative

Gate 1 still confirms Goal, Scope, Acceptance, Product Slice when applicable, and Explicit Exclusions. Gate 2 still confirms the complete implementation package and optional start. An open authority type does not authorize Feature creation, package preparation, implementation, Bug lifecycle change, Requirement mutation, or Git action.

Human Authority means that reliable Human instruction may be the Feature definition authority. It does not mean every Human message authorizes execution. The Agent still separates definition, Gate 1, Gate 2, execution mode, Git, external, submit, and close decisions.

## 8. Specialized Checker Applicability

Before validating an artifact, a specialized Checker determines whether the artifact belongs to its published domain.

Examples:

- Requirement Product Definition / Product Slice validation applies only to the Requirement Product Definition sub-adapter of Feature Authority;
- Concept Foundation trace validation applies only when the effective Product Definition contains the applicable accepted Concept/Requirement Model contract;
- ADR requirement-model landing validation applies only to a requirement-driven ADR whose Trace Applicability is required or explicitly not-applicable under its own rules;
- Onboarding coverage validation applies only to an accepted Evidence-Graph + DDD Onboarding scope;
- Lightweight Change scanning applies only when a valid memory root has a `changes/` inventory.

When the artifact belongs to another authority class, the Checker returns `NOT_APPLICABLE / 0` or an equivalent structured not-applicable result. It must not manufacture a missing Requirement path or fail a Bug/Human Authority Feature for lacking Product-only fields.

Within an applicable domain, structural, reference, ID, and freshness findings remain visible. The Agent still owns semantic sufficiency and the existing Human Gate.

## 9. Agent Checker Rescue

### 9.1 Purpose and relationship to Checker Self-Repair

Agent Checker Rescue is a response-local internal method used after an exact canonical Checker rerun still reports a failure that may be caused by checker applicability, legacy assumptions, stale derived evidence, or another bounded checker limitation. It adds no canonical stage, lifecycle status, target-project directory, persistent bypass, or new Human Gate.

The Agent first preserves the canonical command, output, exit status, target, and current input evidence. It then classifies the failure and chooses exactly one level:

1. **Level 1 — Agent automatic rescue:** independent evidence is complete, the safety boundary is intact, product meaning is unchanged, and continuation stays inside authorization the human already granted;
2. **Level 2 — Human one-Gate substitute:** evidence is sufficient to explain the limitation, but a small residual risk still requires one bounded Human decision for one named Gate;
3. **Level 3 — non-rescuable:** a real physical, safety, semantic, verification, or authorization uncertainty remains, so the owning workflow must stop.

Existing Checker Self-Repair remains available only when reliable evaluation truly requires a corrected executable Checker implementation. The isolated patch, RED/GREEN, negative controls, exact-target run, expiry, and formal source repair rules remain unchanged for that path. A temporary patch is not the default response to a limitation and is not required merely to restate facts the Agent can prove independently.

### 9.2 Level 1 — Agent automatic rescue

The Agent may continue without interrupting the human solely for the Checker failure when all conditions are true:

1. the exact canonical failure and one exact rerun are preserved;
2. the Agent classifies the cause as `checker-limitation`, `not-applicable`, supported legacy-shape mismatch, or deterministic Agent-owned derived-evidence mismatch;
3. the applicable published authority and one effective primary authority are determinable;
4. current independent evidence covers every objective fact needed by the current workflow step;
5. product meaning, Feature scope, acceptance, risk, dependencies, and implementation boundary do not change;
6. no unresolved authority conflict, required verification failure, or physical/executor contradiction remains;
7. continuation and any deterministic repair stay wholly inside an existing Human authorization;
8. the Agent records its classification, evidence, safety assessment, decision, expiry, and developer-feedback state.

The Agent may repair a deterministic Agent-owned cache or derived field and rerun the Checker when that write is already inside the accepted action boundary. It may also rely on direct inspection, another canonical reader, or bounded read-only commands when no artifact repair is necessary. It must not rewrite human originals or accepted product meaning merely to satisfy the Checker.

The compact response-local record is:

```text
Canonical Checker Result: BLOCKED
Agent Classification: checker-limitation
Independent Evidence: <actual source and result>
Safety Boundary: intact
Semantic Impact: none
Agent Rescue Decision: continue-within-existing-authorization
Expiry: <Gate end or relevant checker/input/authority/evidence change>
Developer Feedback: prepared | not-applicable
```

This record does not change the canonical result to `PASS`, create authorization, or satisfy an existing Human Gate. If the normal next workflow step already has its own Human Gate, the Agent still presents that Gate; it simply does not add another prompt solely for the Checker defect.

### 9.3 Level 2 — Human one-Gate substitute

When independent evidence is strong enough to explain the Checker limitation but a small residual risk prevents Level 1, the Agent may recommend one bounded substitute decision. It must show the exact target, named Gate, independent evidence, residual risk, expiry, and why a source repair is not required before this Gate.

Reuse the existing evidence wording:

```text
Agent Rescue Decision: human-substitute-required
Human Substitute Decision: accepted-for-this-gate | declined
```

This is not a lifecycle, Checker result, permanent exception, or new Auto Mode.

The review contains:

| Field | Required content |
|---|---|
| Canonical Checker | exact checker, version/commit, and command |
| Original Result | exit status and concise failure |
| Agent Classification | artifact-invalid, environment-invalid, checker-limitation, or unresolved |
| Applicable Authority | current rule and source evidence |
| Independent Evidence | direct facts used instead of the failed Checker conclusion |
| Residual Risk | what remains uncertain or unverified |
| Authorized Scope | one exact target and named Gate |
| Expiry | Gate end or any relevant checker/input/authority/evidence change |
| Recommended Decision | accept for this Gate or decline and repair first |
| Developer Feedback | prepared, declined, or not applicable |

When accepted, only the named Gate may consume the substitute evidence. The canonical Checker remains failed. Every later action-specific Gate that relies on it must show the residual failure and the exact decision. A different target, command, Gate, source, or evidence digest requires new assessment.

### 9.4 Level 3 — non-rescuable conditions

Neither Agent automatic rescue nor Human substitute authorization can override:

- project/path write confinement;
- exact Archive/Rehydrate or Full Memory Audit plan hash;
- journal, preimage, post-check, or rollback integrity;
- a missing or unreliable Human decision required by an existing Gate;
- unresolved or conflicting effective authority;
- failed required verification or uncertainty about whether the product behavior works;
- unresolved product, design, scope, security, data-loss, destructive, production, credential, paid-call, or external-effect meaning;
- a continuation that exceeds the already authorized action boundary;
- sealed release, customer isolation, or independently required Git/release authorization.

These conditions must be repaired or decided through their owning workflow. A Human decision may resolve a genuine product or action choice through that workflow, but it must not be mislabeled as Checker Rescue.

### 9.5 Expiry and escalation

Every rescue expires at the end of the named workflow step or when the checker version, command, target, input, authority, evidence digest, safety condition, or authorization boundary changes. Repeated failure with changed evidence requires a fresh classification.

If direct evidence is incomplete, the Agent cannot explain the discrepancy, or reliable evaluation depends on corrected executable logic, escalate to existing Checker Self-Repair rather than guessing. If the same source defect recurs, prepare developer feedback; do not repeatedly patch target-project artifacts around it.

## 10. Developer Feedback Contract

When the Agent classifies a likely Checker limitation, it prepares a sanitized feedback draft automatically as read-only work. The draft contains:

- Agent Loop version or source commit;
- Checker path and command;
- expected behavior from published authority;
- actual result;
- minimal neutral reproduction shape;
- impact on the target workflow;
- proposed classification or source fix;
- negative controls that must remain protected;
- removed private data and redactions.

The Agent tells the human that the blocker may be reported to the Agent Loop developer. Preparing or retaining the draft needs no external-action authorization.

Creating a GitHub Issue, sending a message, uploading evidence, or contacting a developer is an external mutation and retains the existing independent Issue Reporting Human Gate. Substitute authorization never implies Issue submission, and Issue submission never implies Checker repair, Git action, installation, synchronization, release, or publication.

## 11. Phase 1 — Open Feature Authority And Exception Path

Phase 1 fixes the current Feature blocker and establishes the common responsibility boundary.

Required outcomes:

1. Add the open Feature Authority contract and compatibility reader.
2. Add Feature Authority, Bug Authority, and Human Authority as open adapter families, including compatibility sub-adapters for Requirement Product Definition and Bug Expected Behavior.
3. Make unknown but inspectable authority `CHANGED / advisory`, not `BLOCKED`.
4. Change the universal Feature Context scanner to route by authority before path validation.
5. Preserve Requirement/Product/ADR freshness checks when the Requirement Product Definition sub-adapter of Feature Authority applies.
6. Add Bug identity, Expected Behavior evidence locator, Resolution Path/Fix Feature locator, and source-freshness facts when the Bug adapter applies, without making the Checker a Bug semantic judge.
7. Keep Human Authority provenance and meaning under Agent/Human review; do not invent a filesystem authority.
8. Add specialized `NOT_APPLICABLE` behavior needed to prevent Product/Concept validators from being applied to non-Requirement Feature authorities.
9. Add response-local Level 1 Agent automatic rescue for proven Checker limitations when evidence is complete, safety is intact, semantics are unchanged, and continuation remains inside existing authorization.
10. Add Level 2 `accepted-for-this-gate` substitute evidence without requiring a temporary Checker patch when a small residual risk still needs one Human decision.
11. Preserve Level 3 non-rescuable physical, safety, semantic, verification, and authorization conditions.
12. Preserve the full Checker Self-Repair path for cases that need an actual temporary patch.
13. Add the sanitized developer-feedback draft and independent Issue Reporting Gate wording.
14. Coordinate runtime, design, stage guidance, templates, Human Review, scenarios, tests, and human docs.

Phase 1 must not wait for Phase 2 before fixing the known Bug/Human/unknown authority false hard failure or the unnecessary mandatory temporary-patch recovery path.

## 12. Phase 2 — Targeted Checker Lightening

Phase 2 continues the same responsibility model only where the audit found excessive hard-gate behavior.

### 12.1 Onboarding coverage

The Checker reports per-flow facts:

- missing declared slice, file, Diagram ID, section locator, evidence reference, source/render pair, or digest;
- unresolved placeholder tokens;
- declared coverage/gate/status values;
- mechanically stale visual evidence.

Equivalent wording, explanation quality, business terminal completeness, call/data direction meaning, and whether a flow is truly newcomer-ready remain Agent judgments. Missing expected content may return `CHANGED` and prevent the Agent from recommending Onboarding acceptance, but fixed keywords or self-declared `PASS` do not become semantic proof.

Only an unreadable onboarding root, unsafe local path, or mechanically ambiguous source/render authority uses a hard Checker result.

### 12.2 Lightweight Change inventory

The scanner reports invalid or stale records individually and continues inventorying other readable records when safe. One malformed historical card does not erase pending/human-review facts for every other card.

Agent-repairable filename, date, field, section, state, or placeholder problems become per-record findings. The Agent repairs deterministic Agent-owned card evidence within existing authorization or routes unresolved meaning to Human Review.

Dual/broken/external/cyclic memory-root authority, unreadable root enumeration, path escape, or a layout that cannot be safely bounded remains hard.

### 12.3 Requirement/Product/Concept/ADR validation

Each validator checks applicability before domain-specific validation. Within its domain it continues to report objective structure, stable ID, reference, digest, and recorded Human-evidence facts. Semantic completeness and acceptance stay with the Agent and owning Human Gate.

The implementation must distinguish:

- fact finding that may be repaired or reviewed (`CHANGED`);
- wrong validator/artifact pairing (`NOT_APPLICABLE`);
- physical inability to resolve the declared source (`BLOCKED`);
- an owning Human Gate that still must stop even though the Checker itself did not hard-fail.

### 12.4 Surfaces intentionally unchanged

Phase 2 does not weaken:

- Root AGENTS structural marker/path interpretation; its existing changed/invalid split remains;
- Feature Archive advisory reference scan and Agent review;
- Archive/Rehydrate exact plan, executor confinement, journal, post-check, and restore;
- explicit Full Memory Audit/Recovery plan and transaction checks;
- Feature Gate 1/2 Agent semantic review;
- Task Done, verification, Delivery Contract, Git, release, external, submit, pause, or close gates.

## 13. Recording And Artifact Ownership

No mandatory `.agent-loop/checker-exceptions/` or `.agent-loop/checker-feedback/` directory is introduced.

- Short same-session assessment may remain response-local.
- Cross-session or later-step reliance records compact rescue/substitute evidence in the existing Feature `notes.md`, Change card, Bug record, Requirement review, ADR review, Onboarding review, or other owning artifact.
- Developer-feedback drafts may remain response-local or in an existing project-owned issue-draft location when the project already uses one; Agent Loop does not create a new default issue tree.
- The source repository records permanent fixes through normal tests, proposals, changelog, and validation reports.

Suggested compact evidence:

```text
Canonical Checker:
Canonical Result:
Agent Classification:
Applicable Authority:
Independent Evidence:
Safety Boundary:
Semantic Impact:
Agent Rescue Decision:
Residual Risk:
Human Substitute Decision:
Authorized Scope:
Expiry:
Developer Feedback:
Formal Repair Follow-up:
```

## 14. Coordinated Implementation Surfaces

Phase 1 must inspect and align at least:

- `SKILL.md`
- `references/design.md`
- `references/runtime.md`
- `references/checker-recovery.md`
- `references/product-definition.md`
- `references/bug-management.md`
- `references/feature-follow-up.md`
- `references/implementation-planning.md`
- `references/artifact-rules.md`
- `references/stage-guides.md`
- `references/workflow-checklists.md`
- `references/human-review-summary.md`
- `references/validation-scenarios.md`
- `references/document-templates.md`
- `templates/spec.md`
- `templates/root-AGENTS.md` only for concise first-hop wording when needed
- `scripts/check-feature-context.py`
- shared Checker support used by authority adapters
- `scripts/check-requirement-product-definition.py`
- `scripts/check-concept-foundation-trace.py`
- focused Feature Context, Product, Concept, Bug, Human authority, exception, and feedback tests
- `README.md`
- `Usage.md`
- `CHANGELOG.md`

Phase 2 must additionally inspect and align:

- `references/onboarding-knowledge-base.md`
- `references/lightweight-change-lane.md`
- `scripts/check-onboarding-core-flow-coverage.py`
- `scripts/scan-lightweight-changes.py`
- `scripts/lightweight_change_support.py`
- `scripts/check-adr-requirement-model-trace.py`
- affected Onboarding, Lightweight Change, Requirement/Product/Concept/ADR tests and scenarios

Implementation may refine the smallest exact file set after RED evidence identifies the true dependency surface. It must not omit runtime/design, templates, scenarios, or tests when their published meanings change.

## 15. Required RED Baselines And Pressure Scenarios

### 15.1 Phase 1 RED

Before implementation, preserve real failing evidence for:

1. a Requirement-driven Feature returning the current expected result;
2. a Bug-driven maintenance Feature with `Requirement Set: none` incorrectly returning `BLOCKED` under the current checker;
3. a Human-delegated Feature being rejected for absent Requirement authority;
4. an unknown but evidence-backed authority being rejected instead of reaching Agent review;
5. a specialized Requirement/Product/Concept validator trying to validate a non-Requirement Feature;
6. current Checker Recovery requiring a temporary patch even when direct independent evidence already proves the named Gate facts;
7. current runtime forcing Human interruption for a proven Checker limitation even when independent evidence is complete, safety is intact, semantics are unchanged, and work remains inside existing authorization;
8. missing tests for Feature, Bug, Human, unknown, mixed, and legacy authority routing.

### 15.2 Phase 1 GREEN and negative controls

Focused regression must prove:

1. the Feature Authority family still resolves applicable Requirement/Product/ADR/Contract/existing-Feature paths, IDs, digests, and freshness;
2. Bug Authority does not treat `none` as a Requirement path;
3. Bug references, Expected Behavior evidence locators, Resolution Path/Fix Feature facts, and archive locators are reported without semantic redefinition;
4. Human Authority can reach Agent/Human Gate review without invented Requirement files;
5. unknown authority returns advisory evidence rather than a hard failure;
6. specialized wrong-domain validation returns `NOT_APPLICABLE`;
7. Level 1 automatic rescue continues without an extra Human prompt only when exact failure evidence, independent proof, unchanged semantics, intact safety, and existing authorization are all present;
8. Level 1 may repair deterministic Agent-owned derived evidence inside the accepted boundary, but cannot rewrite Human originals or accepted meaning;
9. any change to checker, target, inputs, authority, evidence, safety, or authorization expires prior rescue evidence;
10. a real missing/unreadable declared local source remains hard when no safe evaluation is possible;
11. local path escape, dual memory roots, contradictory current pointers, plan-hash mismatch, transaction/rollback uncertainty, and executor safety failures remain rejected;
12. Level 2 `accepted-for-this-gate` is exact-target, exact-Gate, expiring, residual-visible, and cannot authorize later actions;
13. missing existing authorization, a real safety issue, failed verification, or unresolved semantic condition cannot use either rescue level;
14. incomplete independent evidence routes to existing Checker Self-Repair or the owning workflow instead of Agent guessing;
15. feedback draft is sanitized and external Issue creation still requires a separate Gate;
16. no Checker or rescue record grants Feature execution or another Human-gated action.

### 15.3 Phase 2 pressure scenarios

Focused regression must also prove:

1. semantically equivalent Onboarding wording is not rejected solely for missing one English keyword;
2. keyword-only or self-declared `PASS` content is not treated as semantic completeness proof;
3. missing/stale Onboarding evidence remains visible to the Agent and owning Human Review;
4. one malformed Lightweight Change record does not hide the remaining readable inventory;
5. deterministic Agent-owned Change card defects are reported per record;
6. unsafe memory-root authority or unreadable enumeration still stops the scan;
7. Product/Concept/ADR validators return not-applicable outside their domain;
8. applicable structural/reference/digest defects remain visible without claiming semantic acceptance;
9. Root AGENTS, Archive Apply, transaction, rollback, and exact plan negative controls remain unchanged.

## 16. Validation Requirements

Because this changes Feature Context authority, Checker Failure Recovery, Root Gateway wording, Human substitute evidence, and cross-file workflow invariants, implementation requires full validation.

Each implementation phase must run:

1. focused RED captured before GREEN;
2. focused GREEN plus mutation/negative controls;
3. all affected Shell and Python tests;
4. all `tests/*.sh` and all Python test suites required by the current repository method;
5. YAML and JSON parsing checks;
6. Python compile/import and standard-library-only checks;
7. Shell and Ruby syntax checks where applicable;
8. Markdown fence balance;
9. `git diff --check`;
10. the six-domain semantic audit from `docs/maintenance/full-validation-method.md`;
11. a new Chinese full-validation report under `docs/reports/` with live test counts and actual commands;
12. macOS verification and Windows test definition or runner evidence reported truthfully.

Phase 1 and Phase 2 may be implemented and reviewed separately. Neither may claim the other phase complete without its own RED/GREEN and full required validation.

## 17. Acceptance Criteria

### Phase 1

1. Universal Feature Context loading no longer assumes every Feature is Requirement-driven.
2. Feature Authority, Bug Authority, and Human Authority adapters work without becoming a closed authority whitelist.
3. Unknown but inspectable authority reaches Agent assessment and does not automatically `BLOCKED`.
4. Existing Requirement-driven and legacy Feature artifacts remain readable without bulk migration.
5. Specialized Product/Concept validation does not process a non-Requirement Feature as if it had a Requirement Set.
6. `BLOCKED` is limited to objective inability to evaluate or exact physical/executor contradictions.
7. Agent owns normal semantic assessment, derived repair, and route selection.
8. Level 1 Agent Checker Rescue handles proven, determinate Checker limitations without extra Human interruption and only inside existing authorization.
9. Rescue evidence remains response-local or compactly recorded in an existing owning artifact; it never changes the canonical failure to `PASS` or creates a lifecycle/authorization state.
10. Human is asked only for a real decision or one exact Level 2 residual Checker substitute.
11. Direct `accepted-for-this-gate` substitute evidence may be used without a temporary patch only when independent evidence is sufficient and no non-overridable condition exists.
12. Level 3 physical, safety, semantic, verification, and authorization conditions remain non-rescuable.
13. Existing isolated temporary Checker Self-Repair remains available when a patched evaluator is actually needed.
14. Developer feedback is prepared read-only and submitted only through the independent Issue Reporting Gate.
15. Existing Product, ADR, Feature, Bug, Task, Delivery Contract, Git, release, submit, pause, close, and external gates remain unchanged.

### Phase 2

1. Onboarding Checker reports objective coverage evidence without using fixed wording as semantic proof.
2. Lightweight Change scanning preserves the readable inventory when one record is Agent-repairable.
3. Specialized Requirement/Product/Concept/ADR Checkers expose applicability before domain validation.
4. Agent-repairable findings do not create unnecessary Checker Recovery or Human interruption.
5. Root AGENTS, Archive, exact executor, transaction, and recovery safety are not weakened.
6. All focused and full validation requirements pass with a truthful report.

## 18. Stop Conditions

Implementation must stop and return to Human Review if it would require:

- turning known Feature authority adapters into a closed whitelist;
- making Human Authority equivalent to implementation or Git authorization;
- allowing an unknown authority to silently become `CURRENT` without Agent assessment;
- adding a generic force/bypass flag or persistent exception policy;
- allowing Level 1 Agent Checker Rescue without complete independent evidence, intact safety, unchanged semantics, and an existing authorization boundary;
- allowing any rescue decision to masquerade as canonical `PASS`, durable authorization, or satisfaction of an existing Human Gate;
- allowing `accepted-for-this-gate` to apply to another Gate, target, command, source, or evidence state;
- weakening project write confinement, exact plan hash, transaction journal, post-check, restore, or rollback;
- bypassing Product Human Review, ADR acceptance, Feature Gate 1/2, verification, Task Done, Delivery Contract, Git, release, submit, close, or external-action gates;
- adding a canonical stage, message intent, lifecycle, Auto Mode, or mandatory target-project artifact directory;
- changing the Skill version without separate Human approval;
- modifying unrelated dirty work;
- implementing Phase 2 by weakening tests instead of changing responsibility boundaries;
- claiming Windows verification without a real Windows run;
- committing, pushing, tagging, publishing, releasing, installing, or synchronizing without a separate Human instruction.

## 19. Implementation Sequence Recommendation

After this Proposal is accepted:

1. write a separate implementation plan with explicit Task order and rollback conditions;
2. implement and review Phase 1 first because it fixes the current Feature blocker;
3. retain the Phase 1 regression fixtures as permanent cross-authority contracts;
4. implement Phase 2 as a separately reviewable follow-up after Phase 1 is stable;
5. stop at Human Review after each phase before any commit, push, tag, release, publication, or installed-Skill synchronization.

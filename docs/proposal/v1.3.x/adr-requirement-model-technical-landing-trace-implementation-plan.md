# ADR Requirement Model Technical Landing Trace Implementation Plan

> **For agentic workers:** execute inline under the Agent Loop maintainer rules. Do not create `docs/superpowers/`, target-project `.agent-loop/` artifacts, commits, pushes, PRs, tags, releases, or publications.

**Goal:** Implement the approved ADR technical-landing trace, coverage gate, upstream compatibility review, Human Review Summary, and triggered operational landing without changing the v1.3.0 stage model or version.

**Architecture:** Enhance the existing Decision & Design record instead of adding a mapping artifact. The effective requirement source remains product-semantics authority; the ADR records a read-only snapshot, a source-wide scope inventory, and a generic trace from accepted Requirement Model IDs to technical landing, Design Slices, and verification. A domain-neutral Ruby validator proves source resolution, source/scope equality, coverage, external owner references, preflight/accepted Human Gate order, compatibility, and acceptance gates against isolated fixtures.

**Tech Stack:** Markdown runtime/reference/template sources, Bash focused regression contract, Ruby artifact validator.

---

### Task 1: Establish RED Baseline

**Files:**
- Create: `tests/validate-adr-requirement-model-technical-landing-trace.sh`
- Create after RED: `docs/reports/agent-loop-v1.3.0-adr-technical-landing-red-baseline-2026-07-13.md`

- [x] Add focused assertions for the Effective Requirement Snapshot, generic Technical Landing Trace, Coverage Hard Gate, compatibility drift, Decision & Design approval summary, operational trigger routing, scope exclusions, and domain neutrality.
- [x] Run the focused test before changing runtime, design, references, or templates.
- [x] Confirm the failure is caused by missing technical-landing behavior rather than shell syntax or test infrastructure.
- [x] Preserve the pre-change `31/31 PASS` repository baseline and exact RED output.

### Task 2: Implement Runtime And Design Authority

**Files:**
- Modify: `SKILL.md`
- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Modify: `references/project-decisions.md`

- [x] Define Effective Requirement Snapshot resolution and keep `review-required` separate from ADR lifecycle status.
- [x] Define Requirement Model Technical Landing Trace dispositions and product-semantics ownership.
- [x] Block ADR acceptance and dependent Feature Spec / Plan / implementation when coverage or compatibility is incomplete.
- [x] Require superseding ADRs when accepted decision meaning is no longer valid; never rewrite accepted meaning in place.
- [x] Trigger operational landing detail only for changed persistence, protocol, provider, runtime-boundary, or rollout-compatibility concerns.

### Task 3: Coordinate Stage, Gate, Human Review, And Root Guidance

**Files:**
- Modify: `references/human-review-summary.md`
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/project-guidance.md`
- Modify: `templates/root-AGENTS.md`

- [x] Add the Decision & Design Human Review Summary with source, coverage counts, preserved semantics, operational triggers, Design Slice ownership, verification, and explicit human decision.
- [x] Add compatibility-review and coverage-hard-stop behavior at Decision & Design, Feature Spec, Plan, Review, and Drift surfaces.
- [x] Refresh all root managed-block revisions to the same v1.3.0 same-day revision without adding a stage.
- [x] Keep root guidance navigational and leave detailed procedures in published references.

### Task 4: Enhance The ADR Template Without Domain Leakage

**Files:**
- Modify: `templates/decision.md`

- [x] Add Effective Requirement Snapshot fields.
- [x] Add the generic Requirement Model Technical Landing Trace table and disposition rules.
- [x] Add coverage-hard-gate instructions and align Design Slice Coverage.
- [x] Add Upstream Compatibility / Drift rules and immutable accepted-decision behavior.
- [x] Add operational trigger assessment and include detail only for triggered concerns.
- [x] Do not copy fixture business nouns, actions, technical products, or landing choices into the template.

### Task 5: Add Domain-Neutral Artifact Validation

**Files:**
- Create: `scripts/check-adr-requirement-model-trace.rb`
- Create: `tests/fixtures/adr-technical-landing/valid/`
- Create: `tests/fixtures/adr-technical-landing/invalid-missing-coverage/`
- Create: `tests/fixtures/adr-technical-landing/invalid-empty-landing/`
- Create: `tests/fixtures/adr-technical-landing/invalid-unaccepted-source/`
- Create: `tests/fixtures/adr-technical-landing/invalid-reopened-source/`
- Create: `tests/fixtures/adr-technical-landing/invalid-review-required/`

- [x] Resolve the README Effective Concept Foundation pointer and require source/snapshot alignment.
- [x] Reject `candidate` / `reopened`, `review-required`, missing scoped IDs, invalid dispositions, empty landed fields, missing Design Slices, and incomplete verification.
- [x] Keep parser logic identifier- and structure-based; fixture-specific business/action/technology tokens must not appear in validator or templates.
- [x] Keep all downstream simulation under `tests/fixtures/`; do not create repository-root `.agent-loop/`.

### Task 6: Human Docs, Scenarios, GREEN, And Full Validation

**Files:**
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`
- Modify: `references/validation-scenarios.md`
- Create: `docs/reports/agent-loop-v1.3.0-full-validation-2026-07-13.md`

- [x] Add focused pressure scenarios for stale effective sources, partial coverage, semantic redefinition pressure, feature-local/not-applicable dispositions, supersede behavior, and operational trigger routing.
- [x] Run the focused contract to GREEN and all `tests/*.sh`.
- [x] Perform the required six-domain semantic audit and representative full-skill pressure suite.
- [x] Run YAML, JSON, Ruby, Shell, Markdown fence, trailing-whitespace, version, target-artifact, and `git diff --check` guards.
- [x] Save a Chinese full-validation report and stop at Human Review without submission actions.

### Task 7: Repair Review-Discovered Gate Bypasses

**Files:**
- Modify: `scripts/check-adr-requirement-model-trace.rb`
- Modify: `scripts/check-concept-foundation-trace.rb`
- Modify: runtime/reference/template/example surfaces from Tasks 2-6
- Create: `tests/validate-adr-requirement-model-trace-adversarial.rb`
- Create: `tests/fixtures/adr-technical-landing/valid-not-needed/`
- Create: `docs/reports/agent-loop-v1.3.0-adr-technical-landing-review-red-2026-07-13.md`
- Create after GREEN: `docs/reports/agent-loop-v1.3.0-full-validation-2026-07-13.2.md`

- [x] Preserve an adversarial RED proving the initial validator inverted the Human Gate, accepted placeholder/gate/ID garbage, allowed silent scope omission and fake external owners, under-validated slices/operational inventory, and rejected the valid not-needed branch.
- [x] Split `proposed` structural preflight from post-human-review `accepted` validation and require Human Review Evidence for accepted mode.
- [x] Add source-wide Requirement Model Scope Inventory and exact source/scope/trace set validation.
- [x] Add stable `PERM-*` permission-rule and `EX-*` exception-path IDs to requirement modeling, examples, downstream model tracing, and ADR validation.
- [x] Validate decision/Feature Spec paths and statuses, explicit `planned:` future paths, exact gate inventory, slice status, and operational trigger inventory/details.
- [x] Accept the reasoned `concept-foundation-not-needed` trace-not-applicable branch without fabricating product models.
- [x] Rerun focused contracts, all `tests/*.sh`, six-domain semantic audit, mechanical checks, and save the replacement `.2` full-validation report.

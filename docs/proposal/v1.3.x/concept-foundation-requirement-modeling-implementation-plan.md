# Concept Foundation Requirement Modeling Implementation Plan

> **For agentic workers:** execute inline under the Agent Loop maintainer rules. Do not create `docs/superpowers/`, target-project `.agent-loop/` artifacts, commits, pushes, PRs, tags, releases, or publications.

**Goal:** Implement only approved proposal Phase 1 Requirement Concept Foundation and Phase 2 Product Model Derivation on the existing v1.3.0 development line.

**Architecture:** Keep Concept Foundation inside Requirements Discussion / Requirement Product Grill. The human-reviewed requirement document owns accepted concepts and the Requirement Product Model; Product Brief and Feature Spec consume references without redefining product semantics. Runtime/design own ordering and gates, while templates, root guidance, scenarios, examples, and regression tests remain derived and coordinated.

**Tech Stack:** Markdown skill sources, Bash regression contracts, Ruby artifact-trace validator.

---

### Task 1: Establish RED Baseline

**Files:**
- Create: `tests/validate-concept-foundation-requirement-modeling.sh`
- Create after RED: `docs/reports/agent-loop-v1.3.0-concept-foundation-red-baseline-2026-07-12.md`

- [x] Add contract assertions for internal-method placement, Human Grill Contract ordering, statuses, not-needed route, accepted gate, requirement-product-model derivation, downstream references, and Phase 3/4 exclusions.
- [x] Run `bash tests/validate-concept-foundation-requirement-modeling.sh` before runtime/template edits.
- [x] Confirm failure is caused by missing Concept Foundation behavior rather than shell syntax or a typo.
- [x] Save exact RED output and current `30/30` pre-change repository baseline.

### Task 2: Implement Phase 1 Runtime Contract

**Files:**
- Modify: `references/design.md`
- Modify: `references/runtime.md`
- Modify: `SKILL.md`
- Modify: `references/requirement-product-grill.md`
- Modify: `references/requirement-management.md`
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`

- [x] Define trigger/not-needed routing and `candidate | accepted | reopened | concept-foundation-not-needed` states.
- [x] Put Concept Foundation before Business Flow, State, and Product Data modeling without adding a canonical stage.
- [x] Implement the Human Grill Contract in this exact order: inspect evidence, extract candidate concepts, present recommended definition/evidence/impact, ask one blocking question.
- [x] Block downstream product modeling while a triggered foundation remains `candidate` or `reopened`.
- [x] Keep original human source requirements immutable and keep accepted concept detail in the human-reviewed requirement document.

### Task 3: Implement Phase 2 Product Model Derivation

**Files:**
- Modify: `references/product-brief.md`
- Modify: `references/project-decisions.md` only to preserve the PRD ownership boundary; do not add technical mapping
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/document-templates.md`
- Modify: `templates/product.md`
- Modify: `templates/spec.md`

- [x] Derive Concept Relationships, Role/Permission Matrix, State Model, Commands/Events, Business Flow, Product Data Model, invariants, failures, and recovery from accepted Concept IDs.
- [x] Add upstream-to-downstream traceability inside the requirement document.
- [x] Make Product Brief and Feature Spec cite accepted concepts/model rows instead of redefining shared semantics.
- [x] State that PRD / Requirement Product Model defines the product and ADR consumes accepted product semantics for technical landing.
- [x] Do not add Concept-to-technical-representation tables, Design Skill, E2E Skill, Jam Kits, or executable YAML/JSON schemas.

### Task 4: Coordinate Root Guidance And Human Surfaces

**Files:**
- Modify: `templates/root-AGENTS.md`
- Modify: `references/project-guidance.md`
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`

- [x] Add Requirements Discussion signal/reference and required stop for unresolved Concept Foundation.
- [x] Increment same-version managed block revisions without changing v1.3.0.
- [x] Document human trigger wording and the one-question recommendation contract.
- [x] Convert the existing proposal-only changelog entry into implemented Phase 1/2 behavior while preserving the proposal file.

### Task 5: Add Behavioral Example And Trace Validator

**Files:**
- Create: `scripts/check-concept-foundation-trace.rb`
- Create: `examples/concept-foundation-refund/requirement.md`
- Create: `examples/concept-foundation-refund/product.md`
- Create: `examples/concept-foundation-refund/spec.md`
- Create: `tests/fixtures/concept-foundation/invalid-unaccepted/`
- Create: `tests/fixtures/concept-foundation/invalid-detached-model/`

- [x] Make the valid example trace stable Concept IDs through definitions, relationships, states, actions/events, flow, product data, Product Brief, and Feature Spec.
- [x] Reject a triggered foundation that is not accepted.
- [x] Reject a model row or downstream reference detached from a defined Concept ID.
- [x] Reject flows/states/product objects that precede or bypass the accepted foundation.
- [x] Keep examples inside `examples/`; do not create a repository-root `.agent-loop/` tree.

### Task 6: GREEN, Pressure, And Full Validation

**Files:**
- Modify: `references/validation-scenarios.md`
- Create: `docs/reports/agent-loop-v1.3.0-full-validation-2026-07-12.md`

- [x] Add proposal pressure scenarios: overloaded refund completion, User/Customer/Member/Tenant boundaries, Approval action vs instance, historical overdraft conflict, simple copy not-needed, no ADR over-generation, and Concept→Product/Spec trace.
- [x] Run the focused contract until GREEN.
- [x] Run the full `tests/*.sh` suite and record counts.
- [x] Perform the six-domain semantic audit and representative pressure scenarios required by `docs/maintenance/full-validation-method.md`.
- [x] Run YAML, JSON, Shell syntax, Markdown fence balance, trailing-whitespace, and `git diff --check` checks.
- [x] Verify no version-bearing file changed away from 1.3.0 and no Phase 3/4 artifact or target-project `.agent-loop/` path was introduced.

### Task 7: Human Review Handoff

- [x] Compare every Phase 1 and Phase 2 proposal item against concrete files/tests/evidence.
- [x] List modified/created files and preserve pre-existing proposal/CHANGELOG ownership in the summary.
- [x] Report RED/GREEN evidence, focused/full validation results, unresolved issues, scope drift, and exactly one recommended next stage.
- [x] Stop before commit, push, PR, merge, tag, release, or publish.

### Task 8: Review Repair And Adversarial Hardening

- [x] Reject unconfirmed downstream concepts, missing candidate inventory, unresolved blockers, placeholder not-needed reasons, duplicate IDs, incomplete trace coverage, and command actors without an explicit permission path.
- [x] Add `Effective Concept Source` to Product Brief and Feature Spec and validate both resolve the same accepted source.
- [x] Preserve archived requirement sources; record confirmed reopen changes in an append-only follow-up or a new requirement set and advance the README effective pointer.
- [x] Add the cumulative Concept Foundation Human Review Summary before acceptance.
- [x] Remove implementation-phase wording from distributed ADR authority rules while preserving proposal history.
- [x] Run fresh full validation and save the superseding 2026-07-13 report.

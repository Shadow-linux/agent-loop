# Onboarding Core Flow Completeness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILLS: use `writing-skills` for documentation RED/GREEN/REFACTOR, `test-driven-development` for executable validators, `verification-before-completion` before completion claims, and `requesting-code-review` before handoff. Agent Loop controls paths, Human Gates, and submit authorization.

**Goal:** Make Evidence-Graph + DDD Onboarding prove that critical project flows, branches, terminal states, recovery paths, diagrams, narrative, and code evidence are traceably complete before `newcomer-ready`.

**Architecture:** Extend the existing onboarding pipeline without changing its stage order or adding Human Gates. Stable Flow IDs and Slice IDs connect Evidence Graph, Onboarding Spec, Tasks, Flow docs, Coverage, and Batch Review; an executable validator checks that trace chain, while semantic pressure scenarios check that generic or incomplete docs are rejected.

**Tech Stack:** Markdown skill sources and templates, Bash contract tests, Ruby artifact validator, repository examples, existing Agent Loop full-validation method.

---

## Execution Boundary

- Implement inside the Agent Loop skill source repository, not a target project's `.agent-loop/`.
- Preserve the existing uncommitted 1.3.0 version alignment.
- Do not create a new Human Gate; retain only Onboarding Spec Acceptance and Onboarding Tasks Full Execution Gate.
- Do not commit, push, tag, publish, or release without a separate human submit confirmation.
- Do not run repository-wide/full-skill validation without explicit human permission; default to onboarding feature-scoped validation.
- Treat `docs/proposal/` as design/history only; published behavior must be carried by `SKILL.md`, `references/`, and `templates/`.

## Task 1: Establish RED contracts

**Files:**

- Create: `tests/validate-onboarding-core-flow-completeness.sh`
- Create: `tests/fixtures/onboarding-core-flow/invalid-missing-recovery/`
- Reference: `docs/proposal/v1.3.x/onboarding-core-flow-completeness.md`

- [ ] Add contract assertions requiring `Core Flow Inventory`, stable `Flow ID`, `Slice ID`, terminal outcomes, selection/deferred reason, evidence chain, diagram-to-slice mapping, and `Completeness Hard Gate` in the owning runtime/reference/templates.
- [ ] Add a validator invocation that expects the valid reference under `examples/ai-meeting-minutes-backend/onboarding-db/` to pass and the invalid fixture to fail with `missing required slice: CF-ORDER-PAYMENT/S07`.
- [ ] Run `bash tests/validate-onboarding-core-flow-completeness.sh` before production-document edits.
- [ ] Record the exact failing assertion and confirm the failure is caused by the missing completeness capability.

Expected RED shape:

```text
missing text in references/onboarding-knowledge-base.md: Core Flow Inventory
```

## Task 2: Update controller and runtime invariants

**Files:**

- Modify: `SKILL.md`
- Modify: `references/design.md`
- Modify: `references/runtime.md`

- [ ] Replace the controller's `wireframe architecture flow diagrams as the preferred flow expression` summary with a concise core-flow completeness summary.
- [ ] Add the design invariant:

```text
Core Flow Inventory
→ accepted Flow selection
→ Flow Slice Coverage
→ Diagram + Narrative + Evidence trace
→ Completeness Hard Gate
→ Quality Score
```

- [ ] State that a missing critical slice cannot be averaged away by topic quality scores.
- [ ] Preserve the canonical onboarding order:

```text
Evidence Graph -> accept Onboarding Spec -> write Onboarding Tasks -> accept Full Execution Gate -> formal docs
```

- [ ] Preserve exactly two onboarding Human Gates.
- [ ] Run the new focused test and confirm the first controller/runtime assertions turn GREEN while template assertions remain RED.

## Task 3: Implement detailed onboarding behavior

**Files:**

- Modify: `references/onboarding-knowledge-base.md`
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/validation-scenarios.md`

- [ ] Define `Core Flow Inventory` fields: Flow ID, business outcome, criticality, entry, success/failure terminals, variants, owners, state/data owners, async/jobs/callbacks, side effects, recovery responsibility, evidence chain, selection, selection reason, confidence, unknowns.
- [ ] Define discovery triangulation across entries, state writes, transactions, messages, callbacks/jobs, tests/contracts/logs/config, and human business outcomes verified against code.
- [ ] Define the Spec Acceptance checks for every `critical` / `important` flow to be planned or explicitly deferred with evidence and impact.
- [ ] Define `Flow Slice Coverage` and key-slice classification for `critical` / `important` flows; keep supporting flows lightweight unless they own core state, side effects, or recovery.
- [ ] Define the diagram contract:

```text
Core Flow Overview / Boundary = scope, branches, owners, terminals
Timeline / Sequence = primary per-flow narrative
ASCII State Machine = states, invalid transitions, recovery
Conditional diagrams = lineage, transaction/concurrency, async topology,
                       decision tree, ERD, runtime, troubleshooting
```

- [ ] Require stable Diagram IDs and Slice ID mapping in every diagram explanation.
- [ ] Scope the fixed diagram group to core module/flow behavior; make overview/domain/jobs/infra/deploy/change-guide diagrams relevance-based so stateless topics do not invent state diagrams.
- [ ] Align stage guide and checklist wording; remove any implication that the current batch is a Human Gate.
- [ ] Add adversarial validation scenarios for missing callback/reconciliation, diagram-narrative detachment, averaged-away critical failure, simple CRUD exemptions, wallet/billing risk, gateway/runtime, and deferred critical flows.
- [ ] Run the focused test and confirm reference assertions pass while remaining template/fixture assertions stay RED.

## Task 4: Align all onboarding templates

**Files:**

- Modify: `templates/onboarding-db/README.md`
- Modify: `templates/onboarding-db/evidence-graph.md`
- Modify: `templates/onboarding-db/onboarding-spec.md`
- Modify: `templates/onboarding-db/onboarding-tasks.md`
- Modify: `templates/onboarding-db/flow.md`
- Modify: `templates/onboarding-db/coverage-matrix.md`
- Modify: `templates/onboarding-db/batch-review.md`

- [ ] Add the complete Core Flow Inventory and Evidence Readiness checks.
- [ ] Add Core Flow Selection and Flow Slice Plan to Onboarding Spec.
- [ ] Extend Diagram Plan with complexity signals and Covered Slice IDs.
- [ ] Make Onboarding Tasks list Flow IDs, Slice IDs, required and conditional diagrams, evidence, hard gate, and score target.
- [ ] Add flow identity, terminal outcomes, slice trace table, Diagram IDs, and diagram explanations to `flow.md`.
- [ ] Add `Completeness Hard Gate` before quality score in coverage and batch review.
- [ ] Use the same quality dimensions and 1-5 anchors in coverage and batch review.
- [ ] Keep module/flow single-file defaults and exactly two Human Gates.
- [ ] Run the focused test and confirm all source/template assertions pass; fixture/validator assertions remain RED.

## Task 5: Implement artifact validation and fixtures

**Files:**

- Create: `scripts/check-onboarding-core-flow-coverage.rb`
- Create: `examples/ai-meeting-minutes-backend/onboarding-db/08-review/evidence-graph.md`
- Create: `examples/ai-meeting-minutes-backend/onboarding-db/onboarding-spec.md`
- Create: `examples/ai-meeting-minutes-backend/onboarding-db/onboarding-tasks.md`
- Create: `examples/ai-meeting-minutes-backend/onboarding-db/03-flows/order-payment.md`
- Create: `examples/ai-meeting-minutes-backend/onboarding-db/coverage-matrix.md`
- Create: `examples/ai-meeting-minutes-backend/onboarding-db/batch-review.md`
- Create: `tests/fixtures/onboarding-core-flow/invalid-missing-recovery/evidence-graph.md`
- Create: `tests/fixtures/onboarding-core-flow/invalid-missing-recovery/onboarding-spec.md`
- Create: `tests/fixtures/onboarding-core-flow/invalid-missing-recovery/onboarding-tasks.md`
- Create: `tests/fixtures/onboarding-core-flow/invalid-missing-recovery/flow.md`
- Create: `tests/fixtures/onboarding-core-flow/invalid-missing-recovery/coverage-matrix.md`
- Create: `tests/fixtures/onboarding-core-flow/invalid-missing-recovery/batch-review.md`

- [ ] Implement a Ruby validator with this CLI:

```bash
ruby scripts/check-onboarding-core-flow-coverage.rb examples/ai-meeting-minutes-backend/onboarding-db
```

- [ ] Parse the fixture's declared critical/important Flow IDs and required Slice IDs.
- [ ] Verify every planned flow is connected across Evidence Graph, Spec, Tasks, Flow doc, Coverage, and Review.
- [ ] Verify every required Slice ID has evidence, Diagram ID, and document-section tokens.
- [ ] Verify Completeness Hard Gate is `PASS` only when required slices are covered.
- [ ] Emit deterministic errors, including:

```text
missing required slice: CF-ORDER-PAYMENT/S07
```

- [ ] Run the focused test; valid fixture must pass and invalid fixture must fail for the expected reason.

## Task 6: Human-facing documentation and changelog

**Files:**

- Modify: `Usage.md`
- Modify: `CHANGELOG.md`
- Review: `README.md`
- Review: `templates/root-AGENTS.md`

- [ ] Explain to humans that onboarding first finds complete core flows, then writes diagram-backed flow docs.
- [ ] Explain the default diagram group and complexity-triggered diagrams without exposing unnecessary internal schema detail.
- [ ] Record the v1.3.0 behavior under the existing 1.3.0 changelog section.
- [ ] Update README only if its onboarding summary would otherwise contradict the new behavior.
- [ ] Do not change root Stage Map signals or add a new stage; update the managed block only if its existing onboarding description becomes contradictory.

## Task 7: REFACTOR and feature-scoped verification

**Files:**

- Create: `docs/reports/onboarding-core-flow-completeness-feature-validation-2026-07-11.md`
- Review: all files changed by Tasks 1-6

- [ ] Run the focused test:

```bash
bash tests/validate-onboarding-core-flow-completeness.sh
```

Expected: `PASS: onboarding core-flow completeness contract is complete`.

- [ ] Run the existing onboarding regression:

```bash
bash tests/validate-evidence-graph-ddd-onboarding.sh
```

Expected: `evidence-graph DDD onboarding validation passed`.

- [ ] Run direct onboarding regressions only:

```bash
bash tests/validate-onboarding-core-flow-completeness.sh
bash tests/validate-evidence-graph-ddd-onboarding.sh
bash tests/validate-project-entry-onboarding-reset.sh
bash tests/validate-v1.2.4-state-lifecycle-repairs.sh
bash tests/validate-v1.2.4-postfix-pressure-repairs.sh
bash tests/validate-v1.2.3-routing-fixes.sh
bash tests/validate-v1.2.3-medium-consistency.sh
```

Expected: all seven feature-boundary tests exit zero.

- [ ] Run required structural checks:

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
ruby -rjson -e 'JSON.parse(File.read("plugin.json"))'
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
git diff --check
```

- [ ] Run a Markdown fence-balance check over changed Markdown files.
- [ ] Execute the five-domain semantic audit required by `docs/maintenance/feature-validation-method.md`, separating RED baseline from GREEN results.
- [ ] Record repository-wide/full-skill validation as not authorized and not part of the feature score; run it only after explicit human permission.
- [ ] Review the final diff for unrelated edits and preserve the pre-existing 1.3.0 version-alignment changes.
- [ ] Stop before commit and request the Agent Loop Submit / Integrate Human Gate.

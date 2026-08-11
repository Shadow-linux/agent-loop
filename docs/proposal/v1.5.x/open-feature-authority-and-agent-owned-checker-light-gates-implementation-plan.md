# Open Feature Authority And Agent-Owned Checker Light Gates Implementation Plan

> **Execution prerequisite:** use `test-driven-development` for each RED/GREEN task and `verification-before-completion` before either Human Review checkpoint. Execute strictly in Task order. Do not start Phase 2 until the Phase 1 Human Review is explicitly accepted.

**Status:** Phase 1 and Phase 2 Human Review accepted; implementation, validation, and `stable-v1.5.4` release complete

**Target:** Agent Loop `1.5.4` on branch `v1.5.4`

**Planning baseline:** `337718a5bf51c9b88099ab047d71738e8b603384`

**Design authority:** `docs/proposal/v1.5.x/open-feature-authority-and-agent-owned-checker-light-gates.md`

**Goal:** replace the universal Requirement-only Feature Context assumption with open authority adapters, make specialized Checker applicability explicit, and let the Agent handle bounded Checker limitations through Level 1/2/3 Rescue without weakening canonical results, existing Human Gates, or exact executor safety.

**Architecture:** `scripts/feature_authority_support.py` will resolve one descriptive primary authority and optional supporting authorities without using a closed authority enum. The universal Feature Context Checker will dispatch known adapters and return advisory facts for custom inspectable authorities. Product, Concept, ADR, and Onboarding validators will decide applicability before domain validation. Agent Checker Rescue remains a runtime method and scenario contract—not a new Checker, stage, status, bypass flag, or authorization issuer. Existing Checker Self-Repair remains the escalation path only when a corrected executable validator is actually required.

**Implementation stack:** Markdown runtime/reference/template contracts; Python 3.10+ standard-library-only Checkers and unit tests; Bash/Ruby repository contract tests; macOS live validation plus Windows CI/test-defined coverage.

---

## 1. Non-Negotiable Semantic Boundaries

Implementation must preserve all of the following. A task that cannot preserve them stops before GREEN and returns to Human Review.

1. `Feature Authority`, `Bug Authority`, and `Human Authority` are open adapter families. `Authority Type` remains descriptive metadata, never a closed allowlist.
2. `Requirement Product Definition` remains a compatible Feature Authority sub-adapter. Existing specs containing only `## Product Requirement Source` remain readable without bulk migration.
3. Unknown but inspectable authority returns `CHANGED / 0` with advisory facts for Agent assessment. It must not silently become `CURRENT`, and unfamiliar wording alone must not produce `BLOCKED`.
4. A specialized Checker determines applicability first. A valid wrong-domain input returns `NOT_APPLICABLE / 0` rather than inventing missing Requirement/Product fields.
5. Checkers report objective facts. The Agent owns authority sufficiency, semantic impact, derived repair, workflow routing, and recommendations.
6. Rescue has exactly three response-local levels:
   - Level 1: automatic only with complete independent evidence, intact safety, unchanged semantics, and continuation wholly inside existing authorization;
   - Level 2: one exact `accepted-for-this-gate` Human substitute when a small residual risk remains;
   - Level 3: non-rescuable for physical, safety, semantic, verification, or authorization uncertainty.
7. Rescue never changes a canonical result to `PASS`, creates execution authority, satisfies an existing Human Gate, or survives a relevant input/target/checker/authority/evidence/safety/authorization change.
8. Checker Self-Repair is entered only when reliable evaluation requires a corrected executable Checker. A direct-evidence Rescue must not be forced through a temporary patch.
9. No canonical stage, message intent, lifecycle status, Auto Mode, default artifact directory, persistent exception policy, or generic `force`/`skip` option is added.
10. Archive/Rehydrate, Full Memory Audit, project/path confinement, exact plan SHA-256, transaction journal, preimage, post-check, restore, and rollback rules remain unchanged.
11. Product, ADR, Feature Gate 1/2, Task Done, Verification, Submit, Close, Git, Release, External Action, Bug lifecycle, and Delivery Contract Human Gates remain independent and unchanged.

Conceptual Checker outcomes remain:

| Result | Exit | Mechanical meaning | Next owner |
|---|---:|---|---|
| `CURRENT` | 0 | Applicable objective facts resolve and match | Agent may rely on facts only inside existing authorization |
| `CHANGED` | 0 | Facts differ, are incomplete/custom, or need review | Agent assesses impact and chooses repair/route |
| `NOT_APPLICABLE` | 0 | This specialized Checker does not own the artifact/authority | Agent chooses the applicable adapter or direct evidence |
| `BLOCKED` | 1 | Safe evaluation or exact execution is objectively impossible | Owning repair/Recovery; Rescue only if the limitation itself is proven |

---

## 2. Verified Planning Baseline

The following was observed before this plan was written on 2026-08-10. Task 0 must rerun it because implementation may not rely on stale planning evidence.

### 2.1 Workspace boundary

| Check | Observed result |
|---|---|
| Branch | `v1.5.4` |
| HEAD | `337718a5bf51c9b88099ab047d71738e8b603384` |
| Tracked diff | none |
| Cached diff | none |
| Expected untracked | Proposal, `.tmp/`, `scripts/**pycache__/`, `tests/**pycache__/` |
| Unexpected/overlapping dirty work | none observed |

The Proposal is the accepted design source for planning. `.tmp/` and both `__pycache__` trees are unrelated and must not be deleted, restored, overwritten, staged, or committed.

### 2.2 Full executable baseline

| Command group | Observed result |
|---|---|
| every `tests/*.sh` | `48/48 PASS` |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v` | `346/346 PASS` in 64.798s |
| SKILL YAML and `plugin.json` parse | PASS |
| tracked Shell syntax | PASS |
| Python AST parse | `46` files PASS |
| Markdown fence balance | `335` tracked/design/plan files PASS |
| `git diff --check` | PASS |

### 2.3 Focused RED evidence

An isolated copy of `tests/fixtures/feature-context/current` was changed only by replacing `## Product Requirement Source` with the Proposal's accepted `## Feature Authority` block. Current behavior was:

| Authority case | Current result | Required GREEN |
|---|---|---|
| legacy Requirement-only spec | `CURRENT / 0` | remain `CURRENT / 0` |
| explicit Bug Authority | `BLOCKED / 1: Feature spec is missing Product Requirement Source` | known Bug facts, normally `CURRENT / 0` when mechanically current |
| explicit Human Authority | same false `BLOCKED / 1` | `CHANGED / 0` advisory unless mechanically current facts are available |
| unknown inspectable authority | same false `BLOCKED / 1` | `CHANGED / 0` advisory |
| mixed Bug primary + Requirement support | same false `BLOCKED / 1` | facts reported; non-conflicting case is non-blocking |

Additional real RED observations:

- `check-requirement-product-definition.py` and `check-concept-foundation-trace.py` run against a Bug-authority Feature both exit `1` with `missing effective product source pointer`; neither returns `NOT_APPLICABLE`.
- one malformed Lightweight Change card produces top-level `result=invalid / exit 1` and omits the other readable inventory entirely.
- changing the Onboarding flow table label from English `Direction` to semantically equivalent Chinese `调用与数据方向` makes the current Checker exit `1` with `flow missing call/data direction evidence`.
- `Agent Checker Rescue` is absent from runtime/recovery contracts, while `references/runtime.md` currently requires exact Human authorization before Checker/support writes and then a second Human substitute decision.

These REDs prove the current responsibility mismatch. They do not authorize GREEN implementation in this planning turn.

---

## 3. Expected File Map

The implementer must refine only by removing files proven unnecessary or adding a directly required consumer discovered by RED. Any other expansion is scope drift and stops for review.

Modification reasons by owning surface:

| File or exact group | Why it changes |
|---|---|
| `scripts/feature_authority_support.py`, `scripts/check-feature-context.py` | introduce the open resolver once and route universal Feature facts before adapter-specific path checks |
| `scripts/checker_support.py`, `scripts/check-requirement-product-definition.py`, `scripts/check-concept-foundation-trace.py`, `scripts/check-adr-requirement-model-trace.py` | add applicability front doors and one shared safe-evaluation classifier so readable drift becomes `CHANGED` while IO/path/source/archive contradictions remain `BLOCKED` |
| `scripts/check-onboarding-core-flow-coverage.py` | separate objective per-flow evidence from wording/quality judgments and unsafe physical failures |
| `scripts/scan-lightweight-changes.py`, `scripts/lightweight_change_support.py` | retain readable inventory while reporting safe per-record defects; keep root/enumeration/path failures hard |
| `references/runtime.md`, `references/design.md`, `references/checker-recovery.md` | publish the authoritative responsibility split, Level 1/2/3 Rescue order, expiry, and Self-Repair boundary |
| `references/product-definition.md`, `references/bug-management.md`, `references/feature-follow-up.md`, `references/implementation-planning.md` | make Feature construction and downstream planning consume the selected authority rather than assume a Requirement path |
| `references/artifact-rules.md`, `references/stage-guides.md`, `references/workflow-checklists.md`, `references/human-review-summary.md` | align artifact ownership, operational steps, optional Rescue evidence, and unchanged Human Gates |
| `references/validation-scenarios.md` | provide executable semantic pressure cases for adapters, applicability, Rescue, expiry, and preserved gates |
| `references/document-templates.md`, `templates/spec.md`, `templates/feature-context.md` | author new open-authority Features while retaining the legacy Product Requirement sub-adapter |
| `templates/root-AGENTS.md` | keep only the changed first-hop/stop wording and synchronize all 13 managed revisions |
| `SKILL.md`, `README.md`, `Usage.md`, `CHANGELOG.md`, `plugin.json` | align loader entry, human guidance, release history, and target version `1.5.4` |
| named Python/Shell tests and `.github/workflows/cross-platform-checkers.yml` | preserve real REDs, enforce negative controls, and define macOS/Windows checker coverage |
| `docs/reports/agent-loop-1.5.4-full-validation-2026-08-10.md` | retain live two-phase RED/GREEN, mechanical, six-domain, platform, and release evidence |

### 3.1 New files

- `scripts/feature_authority_support.py` — standard-library-only open authority resolver, known adapter dispatch, compatibility reader, local/external locator classification, and factual adapter output.
- `tests/test_feature_authority.py` — isolated Feature/Bug/Human/custom/mixed/legacy adapter contract and path/expiry pressure fixtures.
- `tests/validate-open-feature-authority-checker-rescue.sh` — cross-surface runtime/template/Rescue/no-bypass contract.
- `docs/reports/agent-loop-1.5.4-full-validation-2026-08-10.md` — Chinese Phase 1 and Phase 2 RED/GREEN plus six-domain evidence; Phase 1 must be clearly provisional until Phase 2 completes.

### 3.2 Phase 1 implementation and focused-test files

- `scripts/check-feature-context.py` — resolve authority before adapter-specific path validation.
- `scripts/check-requirement-product-definition.py` — return `NOT_APPLICABLE` for a supplied non-Requirement Feature.
- `scripts/check-concept-foundation-trace.py` — return `NOT_APPLICABLE` when the effective authority/product has no applicable Concept contract.
- `tests/test_feature_context.py`
- `tests/test_requirement_product_definition.py`
- `tests/test_concept_foundation_trace.py`
- `tests/test_python_checker_contract.py`
- `tests/validate-feature-context-load-contract.sh`
- `tests/validate-adaptive-requirement-product-definition.sh`
- `tests/validate-concept-foundation-requirement-modeling.sh`
- `tests/validate-chat-requirements-entry.sh`
- `tests/validate-checker-self-repair.sh`
- `tests/validate-bug-management.sh`

### 3.3 Phase 1 runtime, reference, template, and human-doc files

- `SKILL.md`
- `references/runtime.md`
- `references/design.md`
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
- `templates/feature-context.md`
- `templates/root-AGENTS.md`
- `README.md`
- `Usage.md`
- `CHANGELOG.md`

`templates/bug-README.md` is an input authority contract and is expected to remain semantically unchanged; tests consume its existing Bug ID, Expected Behavior Evidence, Resolution Path, and Fix Feature fields. Do not redesign Bug lifecycle in this work.

No tracked `examples/` edit is planned. Existing Requirement-driven examples remain compatibility controls, and Onboarding examples are copied into temporary test workspaces for mutation. If GREEN would require changing an example's accepted product meaning rather than only a test fixture, stop and review the scope.

### 3.4 Phase 2 implementation and focused-test files

- `scripts/check-onboarding-core-flow-coverage.py`
- `scripts/scan-lightweight-changes.py`
- `scripts/lightweight_change_support.py`
- `scripts/check-adr-requirement-model-trace.py`
- `tests/test_onboarding_core_flow_coverage.py`
- `tests/test_lightweight_change_scan.py`
- `tests/test_adr_requirement_model_trace.py`
- `tests/validate-onboarding-core-flow-completeness.sh`
- `tests/validate-lightweight-change-lane.sh`
- `tests/validate-adr-requirement-model-technical-landing-trace.sh`
- `references/onboarding-knowledge-base.md`
- `references/lightweight-change-lane.md`
- Phase 1 runtime/design/stage/checklist/scenario/doc files only where Phase 2 behavior must be coordinated.

### 3.5 Version and cross-platform synchronization files

- `plugin.json`
- `.github/workflows/cross-platform-checkers.yml`
- `references/project-guidance.md`
- `references/submit-and-integrate.md`
- `tests/validate-lightweight-change-lane.sh`
- `tests/validate-root-agents-block-refresh.sh`
- `tests/test_root_agents_blocks.py`
- `tests/validate-requirement-lifecycle-backlog.sh`
- `tests/validate-bug-management.sh`
- `tests/validate-branch-management-strategy.sh`
- `tests/validate-human-help-version-docs.sh`
- `tests/validate-project-local-skills.sh`
- `tests/validate-project-skill-discovery-guard.sh`
- `tests/test_root_agents_lossless_slimming.py`
- `tests/validate-root-agents-block-checker.sh`
- `tests/validate-v1.2.4-root-stage-coverage.sh`

Current examples in `references/project-guidance.md`, `references/workflow-checklists.md`, `references/validation-scenarios.md`, and `references/submit-and-integrate.md` must move to the current `1.5.4` revision/scope. Historical proposals, reports, and the retained `1.5.3` changelog section are history and must not be rewritten merely to eliminate an old string.

### 3.6 Files that must remain behaviorally unchanged

Do not modify Archive/Rehydrate Apply/Restore, Memory Reconciliation Apply/Restore, exact-plan, transaction, journal, post-check, or rollback implementation files. Run their existing negative controls as regression evidence. If GREEN appears to require weakening one, stop.

---

## 4. Strict Task Sequence

```text
Task 0 baseline and scope freeze
-> Phase 1 Task 1 focused RED
-> Task 2 runtime/design responsibility contract
-> Task 3 references/templates
-> Task 4 shared adapter + Checker GREEN
-> Task 5 human docs + v1.5.4 synchronization
-> Task 6 Phase 1 full validation
-> PHASE 1 HUMAN REVIEW — mandatory stop
-> Phase 2 Task 7 focused RED
-> Task 8 Phase 2 responsibility/reference contract
-> Task 9 Phase 2 Checker GREEN
-> Task 10 Phase 2 full validation
-> PHASE 2 HUMAN REVIEW — mandatory stop
```

No Task may be parallelized across a shared file. Do not mark a later Task complete while an earlier RED, version mismatch, drift finding, or Human Review remains open.

---

## Task 0 — Reconfirm Baseline, Dirty Work, And Scope

**Files changed:** none

- [x] Run `git branch --show-current` and require exact branch `v1.5.4`.
- [x] Run `git rev-parse HEAD`. At the initial execution start require `337718a5bf51c9b88099ab047d71738e8b603384`; if HEAD changed, stop and obtain a new reviewed baseline rather than silently rebasing this plan.
- [x] Run `git status --short --branch --untracked-files=all`, `git diff --name-only`, and `git diff --cached --name-only`.
- [x] Require no tracked/cached modifications. Permit only the Proposal, this plan, `.tmp/`, `scripts/**pycache__/`, and `tests/**pycache__/` as pre-existing untracked work.
- [x] Record hashes or an exact path inventory for all pre-existing untracked items. Never delete, restore, overwrite, stage, or include them except the accepted Proposal and this plan when a later Git Gate explicitly names them.
- [x] Rerun all current Shell tests and Python tests before adding RED tests:

```bash
shell_total=0
for test_file in tests/*.sh; do
  shell_total=$((shell_total + 1))
  PYTHONDONTWRITEBYTECODE=1 bash "$test_file"
done
printf 'shell_total=%s\n' "$shell_total"

PYTHONDONTWRITEBYTECODE=1 \
  python3 -m unittest discover -s tests -p 'test_*.py' -v
```

- [x] Preserve current expected baseline `48/48 Shell` and `346/346 Python`. If current counts/results differ, stop and diagnose before writing tests.
- [x] Run read-only mechanical baseline: SKILL YAML parse, `plugin.json` parse, tracked Shell syntax, Markdown fence balance, Python AST parse, and `git diff --check`.
- [x] Freeze the expected file map above. After every later Task, compare `git status --short` and `git diff --name-only` with that map.

**Stop:** any unknown dirty file, changed HEAD, failing pre-existing test, overlapping edit to the Proposal/plan, or mutation beneath `.tmp/`/`__pycache__`.

---

# Phase 1 — Open Feature Authority And Agent Checker Rescue

## Task 1 — Add And Preserve Focused Phase 1 RED

**Files:**

- Create `tests/test_feature_authority.py`
- Create `tests/validate-open-feature-authority-checker-rescue.sh`
- Modify `tests/test_feature_context.py`
- Modify `tests/test_requirement_product_definition.py`
- Modify `tests/test_concept_foundation_trace.py`
- Modify `tests/validate-feature-context-load-contract.sh`
- Modify `tests/validate-checker-self-repair.sh`

- [x] Add fixture builders that write only inside `tempfile.TemporaryDirectory`; do not create target-project `.agent-loop/` artifacts in the repository.
- [x] Preserve the current legacy Requirement fixture as a GREEN control before changing production code.
- [x] Add the complete authority routing matrix:

| Case | Required result |
|---|---|
| explicit Requirement Product Definition Feature Authority | adapter applies; valid facts `CURRENT / 0` |
| legacy spec with only Product Requirement Source | compatibility sub-adapter; unchanged `CURRENT / 0` |
| Bug Authority with readable Bug README, accepted Expected Behavior locator, confirmed Resolution Path/Fix Feature locator | no Requirement path fabrication; objective facts may become `CURRENT / 0` |
| Human Authority with conversation/decision locator | no invented file; `CHANGED / 0` advisory when provenance is not mechanically decidable |
| custom unknown local authority with readable evidence | `CHANGED / 0` advisory, authority type preserved verbatim |
| custom external/ticket locator | do not parse as a project path; `CHANGED / 0` advisory |
| Bug primary + Requirement/ADR support, no objective conflict | all facts reported, non-blocking |
| supporting authorities with semantic conflict | `CHANGED / 0`, Agent/Human route; Checker does not select a winner |
| two mechanically contradictory current primary pointers | `BLOCKED / 1` |
| missing/unreadable declared local primary source | `BLOCKED / 1` |
| local authority path escape or symlink escape | `BLOCKED / 1` |
| Windows-style local references plus BOM/CRLF | same logical result as POSIX/LF fixture |

- [x] Add Bug flat-Feature and archived-Feature locator controls. The adapter may report locator facts but must not change Archive lifecycle or follow symlinks.
- [x] Add Product and Concept wrong-domain cases that require exact `NOT_APPLICABLE / 0` output and prove no Product-specific validation ran.
- [x] Add cross-surface Rescue scenario assertions for Level 1, Level 2, Level 3, expiry, developer feedback, and preserved Checker Self-Repair.
- [x] The Rescue test must explicitly reject any runtime/template text that turns Rescue into `PASS`, an authorization, a new Gate/stage/status, a persistent exception, or a `force`/`skip` flag.
- [x] Run only the new/changed focused tests and preserve expected RED output caused by current production/runtime behavior—not by broken fixtures or imports:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_feature_authority \
  tests.test_feature_context \
  tests.test_requirement_product_definition \
  tests.test_concept_foundation_trace -v
bash tests/validate-open-feature-authority-checker-rescue.sh
```

Expected RED includes Bug/Human/custom/mixed false `BLOCKED`, missing `NOT_APPLICABLE`, and absent Rescue contract. Do not weaken assertions to obtain GREEN.

---

## Task 2 — Publish The Phase 1 Runtime And Design Contract

**Files:**

- Modify `references/runtime.md`
- Modify `references/design.md`
- Modify `references/checker-recovery.md`
- Modify `references/human-review-summary.md`
- Modify `references/validation-scenarios.md`

- [x] In runtime, make Feature Context entry resolve authority shape before adapter-specific path handling. Publish all four conceptual outcomes and retain Agent ownership of `CHANGED`/`NOT_APPLICABLE` routing.
- [x] Define the known open adapter families and compatibility reader without enumerating all legal `Authority Type` strings.
- [x] State that external URLs, ticket identifiers, or Human conversation locators are evidence locators, not local paths. A declared local path still receives exact project/memory-root confinement checks.
- [x] Insert Agent Checker Rescue before Checker Self-Repair in failure diagnosis:

```text
exact canonical run + exact rerun
-> preserve command/result/target/current inputs
-> classify objective facts and applicability
-> Level 1 only when complete evidence + intact safety + unchanged semantics + existing authorization
-> Level 2 only for one named Gate with visible residual and accepted-for-this-gate
-> Level 3 stop for physical/safety/semantic/verification/authorization uncertainty
-> Checker Self-Repair only when corrected executable evaluation is actually necessary
```

- [x] Keep `accepted-for-this-gate` as evidence wording, not lifecycle. It is exact-target, exact-command, exact-Gate, and expires on Gate end or checker/input/authority/evidence/safety/authorization change.
- [x] State explicitly that Level 1 does not add a Human prompt and does not consume or replace a normal later Human Gate.
- [x] State explicitly that Level 2 can accept evidence for one Gate but cannot authorize Feature execution, Requirement/Bug mutation, Git, release, external action, or any later Gate.
- [x] Keep every Level 3 boundary from the Proposal. Path escape, plan hash, journal/preimage/post-check/rollback, failed real verification, semantic conflict, and absent prior authorization are never rescuable.
- [x] Retain the existing temporary-patch RED/GREEN/negative-control Self-Repair path unchanged for actual executable Checker repair.
- [x] Add the compact Rescue/substitute evidence fields to Human Review guidance as an optional block owned by an existing Feature/Bug/Change/Requirement/ADR/Onboarding artifact or the current response. Do not add a default directory or mandatory report.
- [x] Add sanitized developer-feedback behavior and keep Issue creation behind the independent External Action/Issue Reporting Human Gate.
- [x] Add numbered validation scenarios covering every Rescue positive, negative, and expiry case listed under Task 6.

Run the cross-surface test. It may remain RED only on templates/scripts not yet implemented; runtime/design assertions must be GREEN before Task 3.

---

## Task 3 — Align Detailed References And Templates

**Files:**

- Modify `references/product-definition.md`
- Modify `references/bug-management.md`
- Modify `references/feature-follow-up.md`
- Modify `references/implementation-planning.md`
- Modify `references/artifact-rules.md`
- Modify `references/stage-guides.md`
- Modify `references/workflow-checklists.md`
- Modify `references/document-templates.md`
- Modify `templates/spec.md`
- Modify `templates/feature-context.md`
- Modify `templates/root-AGENTS.md`
- Modify `SKILL.md` body, but do not change its version field until Task 5

- [x] Make new `spec.md` authoring use the Proposal's `## Feature Authority` fields.
- [x] Keep `## Product Requirement Source` and `## Product Slice` as conditional Requirement Product Definition sub-adapter details. Do not require them for Bug/Human/custom authority.
- [x] Make Feature Context Snapshot authority-neutral at the common layer, then retain Requirement/Product/ADR lifecycle/digest fields only when that sub-adapter applies. Bug snapshots report Bug identity, Expected Behavior locator, Resolution Path/Fix Feature locator, archive locator, and source freshness facts without deciding their meaning.
- [x] Preserve legacy Feature Context fields/readers. No historical Feature is rewritten solely because the new block exists.
- [x] Update planning/follow-up guidance so Tasks/Tests/Plans consume the current resolved authority and accepted Feature boundary, not an assumed Requirement path.
- [x] Keep Bug confirmation, Resolution Path, Feature create/reopen, Gate 1, and Gate 2 as separate decisions.
- [x] In artifact rules, state that rescue evidence remains response-local or compactly lives in an existing owner. Do not create `.agent-loop/checker-exceptions/`, `.agent-loop/checker-feedback/`, or another default tree.
- [x] Keep the root template concise. Update only the existing Checker-failure/Feature-context first-hop wording needed to distinguish Agent Rescue from actual Checker Self-Repair; do not copy the full algorithm into root guidance.
- [x] Confirm no canonical stage, message-intent row, lifecycle value, or Gate class was added.

Run:

```bash
bash tests/validate-open-feature-authority-checker-rescue.sh
bash tests/validate-feature-context-load-contract.sh
bash tests/validate-bug-management.sh
bash tests/validate-chat-requirements-entry.sh
bash tests/validate-concept-foundation-requirement-modeling.sh
```

Expected: document/template assertions pass; production behavior tests remain RED until Task 4.

---

## Task 4 — Implement Open Authority Dispatch And Applicability GREEN

**Files:**

- Create `scripts/feature_authority_support.py`
- Modify `scripts/check-feature-context.py`
- Modify `scripts/check-requirement-product-definition.py`
- Modify `scripts/check-concept-foundation-trace.py`
- Modify `tests/test_python_checker_contract.py`
- Modify `.github/workflows/cross-platform-checkers.yml`

- [x] Implement a resolver that returns the original descriptive `Authority Type`, one effective primary locator, supporting locators, detected adapter family, compatibility shape, factual findings, and applicability. Do not represent authority types with a closed Python enum or reject an unknown label.
- [x] Dispatch explicit authority before reading `Requirement Set`. Treat the old Product Requirement Source-only shape as the Requirement Product Definition compatibility adapter.
- [x] Keep locator classes distinct:
   - project-relative local source: normalize separators, enforce project boundary, verify existence/readability, and hash only when the adapter contract requires it;
   - stable external/ticket/Human locator: preserve as evidence and return advisory facts; never pass it to `Path.resolve()` as a local source;
   - `none`: permitted only where the selected adapter says that field is inapplicable, never interpreted as a path.
- [x] Reuse existing Bug artifact/Feature archive facts read-only. Do not alter Bug lifecycle or Archive support/executors.
- [x] Return `CHANGED` for unknown inspectable authority and semantic/support conflict. Reserve `BLOCKED` for unreadable declared local sources, physical ambiguity, path escape, unsafe memory authority, or another exact hard boundary.
- [x] Add Product/Concept applicability front doors. When a supplied Feature is non-Requirement authority, print `NOT_APPLICABLE: <reason>` and exit `0` before product/concept field validation.
- [x] Preserve existing applicable Product/Concept validation output and negative controls.
- [x] Keep the support module standard-library-only and importable on Python 3.10. Add it to native cross-platform tests, along with Requirement Product Definition coverage currently missing from the CI matrix.
- [x] Run focused GREEN and mutation controls:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_feature_authority \
  tests.test_feature_context \
  tests.test_requirement_product_definition \
  tests.test_concept_foundation_trace \
  tests.test_python_checker_contract -v

bash tests/validate-open-feature-authority-checker-rescue.sh
bash tests/validate-feature-context-load-contract.sh
bash tests/validate-adaptive-requirement-product-definition.sh
bash tests/validate-concept-foundation-requirement-modeling.sh
```

- [x] Mutate each known adapter, custom authority, local/external locator, digest, Bug link, support reference, and legacy shape. Confirm no test passes because the adapter accepts everything.

---

## Task 5 — Synchronize Human Docs And Version `1.5.4`

**Files:**

- Modify `README.md`
- Modify `Usage.md`
- Modify `CHANGELOG.md`
- Modify `SKILL.md` version
- Modify `plugin.json`
- Modify `templates/root-AGENTS.md` all managed markers
- Modify current revision examples in `references/project-guidance.md`, `references/workflow-checklists.md`, `references/validation-scenarios.md`, and `references/submit-and-integrate.md`
- Modify every current-version assertion listed in Section 3.5

- [x] Explain to humans that Authority is open, unknown inspectable sources reach Agent assessment, and Checker Rescue does not bypass gates or turn failure into PASS.
- [x] Explain the difference between Level 1 direct-evidence continuation, Level 2 one-Gate substitute, Level 3 stop, and Checker Self-Repair.
- [x] Add a new top `CHANGELOG.md` section `## 1.5.4 — 2026-08-11`; preserve the full historical `1.5.3` section below it.
- [x] Set all current version surfaces together:

| Surface | Required value |
|---|---|
| `SKILL.md` | `Version: 1.5.4` |
| `plugin.json` | `"version": "1.5.4"` |
| `README.md` | current version `1.5.4` |
| `Usage.md` | human-facing version `1.5.4`; help examples use 1.5.4 |
| `CHANGELOG.md` | current heading `1.5.4 — 2026-08-11` |
| all 13 `templates/root-AGENTS.md` managed starts | exact `block-version:1.5.4-20260810.1` |

- [x] Require exactly 13 managed-start and 13 matching managed-end markers; every managed-start must use the same full revision `1.5.4-20260810.1`.
- [x] Update current root-revision tests and examples to that exact revision. Do not change historical proposals/reports or old changelog history.
- [x] Search for `1.5.3` and `1.5.3-20260728.1`. Classify every remaining occurrence as historical or a defect. Current runtime/reference/test/metadata surfaces may not retain the old current value.
- [x] Run focused version/root checks:

```bash
python3 -m unittest \
  tests.test_root_agents_blocks \
  tests.test_root_agents_lossless_slimming -v
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-root-agents-block-refresh.sh
bash tests/validate-v1.2.4-root-stage-coverage.sh
bash tests/validate-human-help-version-docs.sh
bash tests/validate-lightweight-change-lane.sh
bash tests/validate-requirement-lifecycle-backlog.sh
bash tests/validate-bug-management.sh
bash tests/validate-branch-management-strategy.sh
bash tests/validate-project-local-skills.sh
bash tests/validate-project-skill-discovery-guard.sh
```

**Version boundary:** this Task changes source metadata only as part of the later explicitly authorized implementation. It does not install/sync the Skill, create a tag, release, publish, or move any branch.

---

## Task 6 — Phase 1 Validation And Human Review Checkpoint

**Files:**

- Create/update `docs/reports/agent-loop-1.5.4-full-validation-2026-08-10.md`
- Update only Phase 1 checkbox/evidence sections in this plan after commands actually run

### 6.1 Rescue scenario matrix

Validate these as named scenarios in `references/validation-scenarios.md` and execute them during the six-domain audit:

| Level | Scenario | Required route |
|---|---|---|
| L1 positive | canonical run and exact rerun fail; independent current source proves every needed fact; semantics/safety unchanged; current action already authorized | record canonical failure and Rescue evidence; continue without an extra prompt |
| L1 positive | deterministic Agent-owned cache is stale and repair is inside an accepted Feature package boundary | repair derived evidence, rerun canonical Checker, retain original failure evidence |
| L1 negative | source meaning, Feature scope, acceptance, risk, dependency, or implementation boundary changes | no Rescue; owning semantic/Human Gate |
| L1 expiry | checker/command/target/input/authority/evidence digest/safety/authorization changes | prior Rescue unusable; classify again |
| L2 positive | direct evidence is strong but one small disclosed residual remains at one named Gate | request `accepted-for-this-gate`; show residual and expiry |
| L2 decline | human declines substitute | stop and repair/route; do not continue |
| L2 expiry | Gate ends or target/command/source/evidence changes | prior substitute unusable |
| L2 negative | attempt to use substitute for Execute, Git, release, external action, or later Gate | reject; independent Gate still required |
| L3 path | project/memory path escape, unsafe symlink, dual/broken/external/cyclic memory authority | stop; non-rescuable |
| L3 plan | exact plan hash/preimage/target mismatch | stop; non-rescuable |
| L3 transaction | journal/post-check/restore/rollback uncertainty | stop and use owning Recovery |
| L3 verification | real required validation fails or behavior remains unknown | stop; Rescue cannot assert success |
| L3 authority | effective authorities conflict or required existing Human authorization is absent | stop; Human Authority must not manufacture permission |
| Self-Repair | independent evidence is incomplete and reliable evaluation requires patched executable logic | enter existing Checker Self-Repair with its Human patch authorization and RED/GREEN controls |
| Feedback | likely Checker limitation contains project/customer/private evidence | produce sanitized read-only draft; Issue creation retains independent Gate |

### 6.2 Focused and full commands

- [x] Run all Phase 1 focused tests in their GREEN state.
- [x] Run every `tests/*.sh`; record live total/pass/fail counts, not the planning count.
- [x] Run all Python tests with discovery; record live total and duration.
- [x] Rerun Archive/Rehydrate and Memory Reconciliation negative controls unchanged, including path escape, exact plan hash, transaction recovery, post-check, and rollback tests.
- [x] Run mechanical checks from Section 6.3.
- [x] Perform the six-domain audit from `docs/maintenance/full-validation-method.md` over Logic Correctness, Autonomy, Project Entry/Onboarding, Development/Test Workflow, Memory, and Recommendation.
- [x] In the report, separate planning RED, Phase 1 RED, Phase 1 GREEN, residual Phase 2 work, current risks, and whether any Critical/High/Medium remains. Phase 1 alone is not final Proposal completion.

### 6.3 Mechanical checks

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
python3 -m json.tool plugin.json >/dev/null
git ls-files -z '*.sh' | xargs -0 -n1 bash -n

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import ast
from pathlib import Path
for root in (Path('scripts'), Path('tests')):
    for path in sorted(root.rglob('*.py')):
        ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
print('PASS: Python AST parse')
PY

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_python_checker_contract -v
git diff --check
```

Run the repository's Markdown fence-balance check over every changed Markdown file, including the Proposal, plan, and validation report.

### 6.4 Platform evidence

- [x] On macOS, record `sw_vers`, `uname -m`, `python3 --version`, locale/UTF-8 behavior, and the actual focused/full results.
- [x] Define Windows coverage in `.github/workflows/cross-platform-checkers.yml` for Python 3.10 and current 3.x on `windows-latest`, including Feature authority, Requirement Product, Concept, ADR, Onboarding, Lightweight Change, and checker-contract tests.
- [x] Add local unit cases for backslash paths, BOM, CRLF, Unicode, and Windows-style path inputs.
- [x] Until a real Windows Actions job runs, report `Windows: test-defined, not live-verified`. Do not claim Windows PASS from macOS simulation.

### Phase 1 Evidence — 2026-08-10

- Task 0 live baseline preserved `48/48 Shell` and `346/346 Python` (`74.528s`); branch `v1.5.4` and HEAD `337718a5bf51c9b88099ab047d71738e8b603384` did not drift.
- Initial focused RED preserved `14` expected Python failures and `44` missing Shell-contract assertions. Independent review then exposed `10/10` additional intended RED cases covering explicit-authority precedence, authority-neutral Snapshot freshness, external locators, logical memory-root aliases, archive-ledger state, and duplicate/multiple authority handling.
- Final Phase 1 focused validation passed `111/111 Python` plus all named Authority/Rescue/Feature Context/Product/Concept Shell contracts.
- Final repository validation passed `49/49 Shell`, `376/376 Python` (`79.115s`), and `12/12` unchanged Archive/Rehydrate and Memory Reconciliation safety controls.
- Mechanical validation passed SKILL YAML, `plugin.json`, `49` Shell syntax checks, `48` Python AST parses, `19/19` Python Checker contract tests, Markdown fence balance, and `git diff --check`.
- macOS live evidence: macOS `26.5` (`25F71`), arm64, Python `3.14.5`, `C.UTF-8`. Windows remains `test-defined, not live-verified`; the CI matrix covers `windows-latest` with Python `3.10` and current `3.x`.
- Version synchronization is complete at `1.5.4`; all `13/13` root managed blocks use `1.5.4-20260810.1`.
- Phase 1 six-domain result is `97.4/100 — STRONG`, with no remaining Phase 1 Critical/High/Medium finding. Full evidence is retained in `docs/reports/agent-loop-1.5.4-full-validation-2026-08-10.md`.
- Scope audit found only two plan-permitted direct RED consumers beyond the initial file graph: `tests/validate-feature-brainstorming-trigger.sh` and `tests/validate-v1.2.4-state-lifecycle-repairs.sh`. Phase 2 production files remain untouched.
- This evidence does not accept Phase 1, authorize Phase 2, or authorize stage/commit/push/tag/PR/merge/release/publish/installed-Skill synchronization.
- Human explicitly accepted Phase 1 and authorized continuation on 2026-08-10; this authorized Task 7 onward only and did not authorize any Git, release, publish, install, or installed-Skill synchronization action.

### 6.5 Mandatory Phase 1 Human Review

Stop after reporting:

- exact Phase 1 files changed;
- RED/GREEN outputs and live totals;
- authority matrix results;
- Rescue scenario results;
- version/revision consistency;
- six-domain score and residual Phase 2 risk;
- dirty-work/scope-drift audit;
- no stage/commit/push/tag/release/install/sync action.

Do not begin Task 7 until the human explicitly accepts Phase 1 and authorizes Phase 2 continuation.

---

# Phase 2 — Targeted Checker Lightening

## Task 7 — Add And Preserve Focused Phase 2 RED

**Files:**

- Modify `tests/test_onboarding_core_flow_coverage.py`
- Modify `tests/test_lightweight_change_scan.py`
- Modify `tests/test_adr_requirement_model_trace.py`
- Modify `tests/test_requirement_product_definition.py`
- Modify `tests/test_concept_foundation_trace.py`
- Modify the three affected Shell validation scripts

- [x] Add an Onboarding fixture with semantically equivalent non-English wording and the same objective references. Current Checker must reproduce the planning RED; GREEN must report facts without treating the fixed English token as semantic proof.
- [x] Add an Onboarding keyword-only/self-declared `covered`/`PASS` fixture that lacks objective references or declared slices. It must not become semantic completeness evidence.
- [x] Add missing/stale Diagram ID, source/render pair, digest, section locator, evidence reference, and placeholder cases as per-flow `CHANGED` facts where safely enumerable.
- [x] Preserve hard failure for unreadable onboarding root, unsafe path, or mechanically ambiguous source/render authority.
- [x] Add a Lightweight Change fixture containing multiple good records and one malformed but readable card. Require good pending/human-review inventory plus one deterministic per-record finding.
- [x] Add filename/date/field/section/state/placeholder record findings; preserve hard failure for dual/broken/external/cyclic memory root, unreadable enumeration, path escape, unsafe symlink/layout, and unbounded artifact kind.
- [x] Add Requirement/Product/Concept/ADR wrong-domain cases that require `NOT_APPLICABLE / 0`, plus applicable malformed cases that remain visible and non-passing.
- [x] Add input-change and authority-conflict mutations so a prior `CURRENT`, `CHANGED`, `NOT_APPLICABLE`, or Rescue record cannot be reused after evidence changes.
- [x] Run only Phase 2 focused tests and preserve RED outputs before production edits.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_onboarding_core_flow_coverage \
  tests.test_lightweight_change_scan \
  tests.test_requirement_product_definition \
  tests.test_concept_foundation_trace \
  tests.test_adr_requirement_model_trace -v
```

---

## Task 8 — Align Phase 2 Responsibility Contracts

**Files:**

- Modify `references/onboarding-knowledge-base.md`
- Modify `references/lightweight-change-lane.md`
- Modify Phase 1 `runtime.md`, `design.md`, stage/checklist/human-review/scenario files only where needed for Phase 2 consistency
- Modify `README.md`, `Usage.md`, and the existing `1.5.4` changelog section only after the runtime meaning is fixed

- [x] Define Onboarding applicability before coverage checks. No recognizable Onboarding scope returns `NOT_APPLICABLE`; a recognizable but incomplete scope reports objective `CHANGED` findings; only unsafe/unreadable/ambiguous physical authority is hard.
- [x] State that fixed wording, explanation quality, business terminal completeness, and newcomer usefulness remain Agent/Human judgments. Self-declared `PASS` is a recorded fact, not proof.
- [x] Define Lightweight Change scan output so safe per-record defects do not erase other readable records or trigger facts. Keep existing pending-count/pending-age meaning and deterministic ordering.
- [x] Define which malformed records are Agent-repairable facts and which root/layout conditions prevent safe enumeration.
- [x] Define Product/Concept/ADR applicability front doors and keep all owning Product/ADR Human Reviews unchanged.
- [x] Do not weaken Root AGENTS structural outcomes, Feature Archive advisory facts, exact executors, Full Memory Audit, Feature Gate 1/2, Task Done, Verification, Submit, Close, Git, Release, or External Action.

Run cross-surface Shell contracts. They may remain RED only on Phase 2 script behavior.

---

## Task 9 — Implement Phase 2 Checker GREEN

**Files:**

- Modify `scripts/check-onboarding-core-flow-coverage.py`
- Modify `scripts/scan-lightweight-changes.py`
- Modify `scripts/lightweight_change_support.py`
- Modify `scripts/check-adr-requirement-model-trace.py`
- Modify affected tests and `.github/workflows/cross-platform-checkers.yml`

- [x] Onboarding: separate applicability, objective per-flow findings, and hard physical errors. Preserve declared status/coverage values as facts; never convert their presence into semantic acceptance.
- [x] Onboarding: ensure a renamed/equivalent heading does not hard fail solely for missing an English token, while missing actual source/reference/diagram facts remains visible.
- [x] Lightweight Change: accumulate deterministic findings per record while continuing safe enumeration. Preserve other good records, trigger counts, oldest pending, and human-review inventory.
- [x] Lightweight Change: keep root authority, path, symlink, enumeration, and unsafe layout failures hard. Do not catch and downgrade those exceptions as record advisories.
- [x] ADR: determine requirement-driven trace applicability before parsing requirement-model landing. A wrong-domain case returns `NOT_APPLICABLE / 0`; an applicable missing/reference/digest/coverage defect remains visible under its current hard/advisory contract.
- [x] Product/Concept: complete any remaining Phase 2 applicability distinctions without weakening their applicable negative controls.
- [x] Keep all modified/new Python code standard-library-only and deterministic under POSIX and Windows path/newline inputs.
- [x] Run focused GREEN, then mutation tests that remove required references/digests and confirm they are still detected.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_onboarding_core_flow_coverage \
  tests.test_lightweight_change_scan \
  tests.test_requirement_product_definition \
  tests.test_concept_foundation_trace \
  tests.test_adr_requirement_model_trace \
  tests.test_python_checker_contract -v

bash tests/validate-onboarding-core-flow-completeness.sh
bash tests/validate-lightweight-change-lane.sh
bash tests/validate-adr-requirement-model-technical-landing-trace.sh
bash tests/validate-open-feature-authority-checker-rescue.sh
```

- [x] Refresh README/Usage/CHANGELOG descriptions without changing version `1.5.4` or root revision unless a root managed block body itself changed after Task 5. If it did, stop and obtain a same-day revision decision rather than silently reusing `1.5.4-20260810.1`.

### Phase 2 Focused Evidence — 2026-08-10

- Phase 1 Human Review was explicitly accepted before Task 7 began.
- Task 7 preserved a real focused RED: `107` tests ran with `55` failures and `4` errors against the pre-Phase-2 production Checkers. Failures covered fixed-language Onboarding rejection, self-declared coverage without evidence, safe evidence defects hard-failing, one bad Change erasing inventory, absent validation-result fields, generic ADR false failure, stale-input reuse, and conflicting Authority falling through to `NOT_APPLICABLE`.
- Task 9 focused GREEN passed `126/126` tests across Onboarding, Lightweight Change, Requirement Product, Concept, ADR, and Python Checker contracts. The affected optional visual integration suite passed `19/19`.
- Cross-surface GREEN passed Onboarding, Lightweight Change, ADR Technical Landing, and Open Authority/Rescue Shell contracts.
- Phase 2 did not modify any root managed block body; version remains `1.5.4` and the accepted `1.5.4-20260810.1` revision remains unchanged. Task 10 full validation and final Human Review are still required.

---

## Task 10 — Final Full Validation And Phase 2 Human Review

**Files:**

- Refresh `docs/reports/agent-loop-1.5.4-full-validation-2026-08-10.md`
- Update only evidence/checkbox state in this plan after commands actually pass

- [x] Run every Phase 1 and Phase 2 focused test.
- [x] Run every Shell test and all Python tests with fresh live counts.
- [x] Run YAML, JSON, Python AST/import/stdlib, tracked Shell syntax, Markdown fence, root 13-block, version consistency, and `git diff --check` checks.
- [x] Rerun exact negative controls for:
   - project and memory-root path escape;
   - dual/broken/external/cyclic roots;
   - authority conflicts and unreadable declared local sources;
   - Rescue expiry after checker/command/target/input/authority/evidence/safety/authorization change;
   - missing existing Human authorization;
   - exact Archive/Rehydrate and Memory Audit plan hash mismatch;
   - transaction journal/preimage/post-check/restore/rollback failure;
   - failed real verification and unresolved product/security/data/external meaning;
   - unchanged Submit/Close/Git/Release/External Human Gates.
- [x] Execute the six-domain semantic audit again; Phase 1 scoring cannot be copied forward.
- [x] Update the Chinese report with separate current RED/GREEN sections, live commands/counts, six-domain score, Critical/High/Medium list, macOS evidence, truthful Windows status, remaining risks, and release judgment.
- [x] Search old version/revision strings and confirm remaining hits are historical only.
- [x] Run final scope audit against the file map and pre-existing untracked inventory.

### Phase 2 Final Evidence — 2026-08-10（Human Review 修复复核完成于 2026-08-11）

- Initial Phase 2 focused RED ran `107` tests with `55` failures and `4` errors. Task 10 semantic audit added four exact RED controls for unreadable Change records, blank visual source/render facts, invalid-filename read-boundary bypass, and unreadable Change metadata; an unreadable Feature Authority source control passed without production repair.
- The first Phase 2 review checkpoint passed `226/226` combined focused Python tests, `8/8` named Shell contracts, `49/49` repository Shell tests, and `395/395` Python tests. Later Human Review repair evidence supersedes these counts below.
- Exact path/root/authority/applicability/hash/journal/post-check/restore/rollback/authorization pressure controls passed `33/33` (`19.030s`). Rescue expiry and unchanged Human Gates also passed their Shell/root/Feature Review contracts.
- Mechanical validation passed SKILL YAML, `plugin.json`, `50` Shell syntax checks, `48` Python AST parses, `19/19` Python Checker contracts, `28` changed/untracked Markdown fence checks, `13/13` root managed-block revisions, executable Onboarding entrypoint mode, and `git diff --check`.
- The independent six-domain audit is `98.2/100 — STRONG`, with `0` Critical, `0` High, and `0` Medium findings. macOS is live-verified; Windows remains `test-defined, not live-verified`.
- Current version is consistently `1.5.4`; all `13/13` root managed blocks use `1.5.4-20260810.1`. Remaining `1.5.3` hits are historical CHANGELOG/Proposal/report evidence only.
- Branch `v1.5.4`, HEAD `337718a5bf51c9b88099ab047d71738e8b603384`, and an empty Git index are unchanged. Proposal status was intentionally synchronized; `.tmp/` and both pre-existing `__pycache__/` trees remain untracked and untouched. No unlisted implementation drift was found.
- Full evidence is in `docs/reports/agent-loop-1.5.4-full-validation-2026-08-10.md`. This checkpoint authorizes no Git, release, publish, installation, or installed-Skill synchronization action.

### Phase 2 Human Review Repair Evidence — 2026-08-10—2026-08-11

- The first Phase 2 Human Review found three Medium gaps and one Low compatibility regression: an explicit Requirement Product Definition could name a different primary authority from its Requirement Set; a dangling recognizable Onboarding symlink could be misclassified as `NOT_APPLICABLE`; Proposal/Plan status evidence was stale; and the Onboarding entrypoint had lost its executable bit.
- Exact RED was preserved before repair: the two isolated Python controls both failed on the incorrect outcome (`CURRENT / 0` and `NOT_APPLICABLE / 0`), while the cross-surface Shell contract reported five unmet status/executable assertions.
- Minimal GREEN now cross-checks the explicit Requirement authority primary against the Product Requirement Source README, recognizes dangling Onboarding scope before safe-read validation, restores mode `100755`, and aligns Proposal/Plan authorization state without changing any canonical outcome, Human Gate, or executor boundary.
- A final cross-surface audit added three RED authoring assertions proving `templates/spec.md`, `references/document-templates.md`, and `references/stage-guides.md` did not yet tell writers that both Requirement pointers must identify one README. All three now carry the same contract and the Shell contract is GREEN.
- Repair-focused validation passed `6/6` exact positive/negative controls, then `91/91` Feature Authority/Context/Onboarding/Checker Python tests. That review checkpoint passed `226/226` combined focused tests, `395/395` Python and `49/49` Shell; pressure controls passed `33/33`. The later repair checkpoint below supersedes the final counts.

### Phase 2 Second Human Review Repair Evidence — 2026-08-11

- The second Human Review identified five reproducible outcome/freshness/locator gaps: readable Product/Concept/ADR structure defects still used hard exit `1`; changed Authority Summary or stale Authority Facts could remain `CURRENT`; equivalent relative paths or a safe internal symlink to the same Requirement README could be treated as conflicting authorities; lowercase `jira-431` was guessed as a missing local file; and invalid UTF-8/dangling inputs could leak traceback or argparse exit `2` instead of stable `BLOCKED / 1`.
- Fourteen isolated tests were first preserved RED: `9/9` specialized Checker structure/UTF-8/dangling cases and `5/5` Feature Context summary/facts/path/ticket cases failed for the exact reported reason. GREEN now returns `CHANGED / 0` only for safely readable structural/semantic drift, while missing/unreadable/escaping/source-conflicting/archive-unsafe facts remain `BLOCKED / 1`.
- The resolver now binds Authority Summary into deterministic Snapshot Authority Facts, compares equivalent Requirement authorities by confined resolved identity, and treats stable numeric ticket keys case-insensitively. Templates, runtime/design, stage/checklist, README/Usage/CHANGELOG, and validation scenarios publish the same contract.
- Six-domain review added one more RED for a legal semicolon inside Authority Summary. Comparing the complete canonical resolver string instead of splitting it repaired the false `CHANGED` without adding an escaping format or weakening stale-fact detection.
- Local diff review added a final RED proving that invalid UTF-8 wrapped by an optional visual adapter must remain `BLOCKED / 1`; a paired readable malformed-JSON control remained `CHANGED / 0`. Cause-chain classification repaired the wrapped unsafe failure without promoting readable drift to a hard block.
- Final repair-focused validation passed `227/227` Python tests (`16.444s`). Final repository validation passed `412/412` Python tests (`207.440s`) and `49/49` Shell tests. YAML/JSON, `50` Shell syntax files including the planned untracked contract, `48` Python AST files, `333` tracked Markdown fence checks, root managed blocks, executable Onboarding entrypoint, and `git diff --check` pass. macOS remains live-verified; Windows remains `test-defined, not live-verified`.

### Mandatory Phase 2 Human Review

Stop and report:

- exact files created/modified by both phases;
- Task completion order and both review boundaries;
- all RED-to-GREEN evidence and negative controls;
- live focused/Shell/Python/mechanical/full-validation results;
- Proposal acceptance-criteria mapping;
- `1.5.4` and all 13 root managed-block revision results;
- macOS evidence and Windows live/test-defined status;
- remaining risks, stop conditions, and any scope drift;
- explicit statement that no commit, push, tag, PR, merge, release, publish, installation, or installed-Skill synchronization has occurred.

Do not proceed to any Git or release action without a new exact Human instruction.

---

## 5. Proposal Coverage Matrix

| Proposal requirement | Planned proof |
|---|---|
| open Feature/Bug/Human adapter families | Task 1 matrix + Task 4 resolver; unknown labels retained |
| Requirement Product Definition compatibility | legacy and explicit sub-adapter tests |
| unknown inspectable is advisory | custom local/external `CHANGED / 0` tests |
| specialized applicability | Product/Concept Phase 1 and ADR/Onboarding Phase 2 `NOT_APPLICABLE` tests |
| Checker facts; Agent semantics | runtime/design contract, per-fact outputs, semantic negative scenarios |
| Level 1 Rescue | complete-evidence positive plus semantic/safety/auth negative and expiry scenarios |
| Level 2 substitute | exact Gate/target/expiry/decline/later-action negative scenarios |
| Level 3 non-rescuable | path/hash/transaction/verification/conflict/authorization pressure tests |
| canonical result remains failed | cross-surface forbidden-text assertions and Human Review output contract |
| Self-Repair only when executable fix needed | routing scenarios and unchanged Self-Repair RED/GREEN tests |
| no new stage/status/Auto Mode/artifact/force | root/runtime diff assertions and repository searches |
| executor/archive/memory safety unchanged | existing exact-plan, journal, post-check, restore, rollback negative suite |
| existing Human Gates retained | root lossless tests, validation scenarios, six-domain audit |
| Phase 2 Onboarding lightening | equivalent wording + keyword-only + objective missing-fact tests |
| Phase 2 Change inventory | one bad record plus preserved good inventory; unsafe-root hard controls |
| developer feedback | sanitized draft scenario + independent Issue Reporting Gate |
| macOS/Windows | local macOS live evidence + Windows matrix/test-defined declaration |
| version 1.5.4 | six metadata/doc surfaces + exact 13-block `1.5.4-20260810.1` assertions |

---

## 6. Rollback, Drift, And Stop Rules

### Rollback

- Roll back only files listed in the rejected Task/Phase, using reviewed preimages or `apply_patch`; never use `git reset --hard`, broad checkout, clean, or worktree deletion.
- If Phase 1 is rejected, restore its exact tracked preimages and remove only newly created Phase 1 files after confirming they did not pre-exist. Preserve the Proposal, this plan, `.tmp/`, and all pre-existing `__pycache__` files.
- If Phase 2 is rejected, restore only Phase 2 files and rerun the accepted Phase 1 focused/full suite. Do not silently roll back accepted Phase 1 behavior.
- If the version task must be rolled back, restore all version-bearing surfaces together; never leave mixed `1.5.3`/`1.5.4` current metadata or mixed root revisions.
- A rollback result must rerun affected focused tests, all root/version checks, and `git diff --check` before Human Review.

### Scope drift checks

After every Task:

```bash
git status --short --branch --untracked-files=all
git diff --name-only
git diff --cached --name-only
git diff --check
```

Compare output to the Task file list and Task 0 pre-existing untracked inventory. Do not stage anything as part of validation.

### Immediate stop conditions

Stop on any of the following:

- a closed authority allowlist or unknown authority silently classified `CURRENT`;
- Human Authority used as implementation/Git/external authorization;
- a generic bypass, persistent exception, new stage/status/Auto Mode/default artifact directory;
- Rescue represented as canonical `PASS`, durable authorization, or satisfaction of an existing Human Gate;
- reuse of Rescue/substitute after target/Gate/command/source/evidence/authorization change;
- any weakening of path confinement, exact plan hash, transaction journal, post-check, restore, rollback, Archive/Rehydrate, or Full Memory Audit;
- bypass of Product/ADR/Feature/Task/Verification/Delivery Contract/Submit/Close/Git/Release/External gates;
- Phase 2 obtained by weakening tests instead of moving semantic judgment to the Agent;
- a need to modify unrelated dirty work or an unlisted execution-safety implementation;
- a mixed version or managed-block revision;
- an attempt to claim real Windows validation without a real Windows run;
- any request to stage, commit, push, tag, PR, merge, release, publish, install, or synchronize that is not separately and exactly authorized.

---

## 7. Current Authorization State

Implementation, both Phase Human Reviews, and the exact `v1.5.4` Release Gate were accepted by subsequent Human instructions. The authorized release action is one release commit plus `v1.5.4` branch and annotated `stable-v1.5.4` tag push to the three configured repositories, followed by GitHub pipeline observation. PR, merge, installed-Skill synchronization, and `main` synchronization remain outside this authorization.

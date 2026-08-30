# Proposal: Inline Task Review, Final Review Subagent, And Agent-Owned Delegation

**Version:** v1.5.x design line; proposed implementation target `1.5.9`

**Status:** accepted; implementation, 1.5.9 version synchronization, focused validation, six-domain semantic review, and the freshly confirmed repaired-input full validation are complete; awaiting Human review of the final diff and separately authorized Git/release actions

**Created:** 2026-08-29

**Human Review:** accepted on 2026-08-29

**Human Direction:** keep review accuracy while removing repeated ceremony. Every Task receives a quick review inside Task Done Gate. After all Tasks are complete, the Agent automatically dispatches one read-only Final Review Subagent for the whole Feature. Feature Close does not repeat another review; it reconciles final evidence, drift, memory, and status, then stops at the existing Human Close Gate. Subagent dispatch itself is not a Human Gate and may proceed directly, but a Subagent inherits only authority that already exists and cannot create or widen authorization.

**Scope:** Feature task completion, final Feature-wide review, Review Repair, completion and close, Submit evidence reuse, Agent-owned Subagent delegation, helper routing, compatibility with existing Feature artifacts, and the affected root guidance and validation contracts

## 1. Problem

Agent Loop 1.5.8 projects this Feature execution chain:

```text
Execute Task / Story
-> Verify
-> Review
-> Drift Check
-> Project Memory Update
-> Feature Completion Check
-> Submit / Integrate
-> Pause / Close
```

It also requires separate review-helper resolution for task review, Submit review, and Feature Close Review, while Subagent execution has its own approval Gate. These rules create three problems:

1. A Task that has just completed implementation and verification must enter a separate visible Review stage before Task Done Gate repeats the evidence assessment.
2. After every Task is reviewed, Feature Completion Check and Feature Close Review repeat much of the same whole-Feature reasoning.
3. The Agent must interrupt the Human merely to delegate already-authorized work or obtain an independent read-only review, even though the delegated action cannot lawfully exceed the current scope.

The desired simplification is not “tests replace review” and not “Subagents may do anything.” It is:

> Review each Task where its evidence is freshest, perform one independent whole-Feature review after all Tasks, remove duplicate close review, and let the Agent delegate inside authority that already exists.

## 2. Accepted Design Principles

### 2.1 Task review is mandatory and inline

Every Task receives an internal **Task Completion Review** inside Task Done Gate. The owning Agent checks implementation against accepted authority, scope, verification, diff, risk, rollback, and drift before moving the Task from `review` to `done`.

Task Completion Review is not a canonical stage, Human Gate, lifecycle status, Auto Mode, checker outcome, artifact family, or mandatory helper invocation.

### 2.2 Final independent review is mandatory once per Feature completion boundary

After every in-scope Task is `done` or Human-approved `skipped`, and the Feature-wide Required Verification due at that point is current, the owning Agent automatically dispatches one read-only **Final Review Subagent**.

The Final Review Subagent reviews the complete Feature rather than repeating a task-level checklist. It checks:

- accepted Product/Requirement meaning, Feature Spec, Product Slice, applicable ADRs and Delivery Contracts;
- all Tasks, accepted tests, plans, implementation, generated output, and final diff;
- cross-task integration, consumers, public and durable boundaries, unrelated work, rollback, residual risk, and verification sufficiency;
- Bug verification and resolution evidence when the Feature repairs one or more Bugs;
- whether code, tests, artifacts, branch facts, and project memory agree.

The reviewer reports findings. The owning Agent validates them, determines semantic impact, applies only authorized repairs, reruns affected evidence, and routes real boundary changes to their owner.

### 2.3 Feature Close Review is removed

Feature Close Review is removed as a separate stage, helper invocation, evidence requirement, and close prerequisite.

After the Final Review Subagent findings are resolved or explicitly routed, the owning Agent performs Drift Check, Project Memory Update, and Feature Completion Check. Feature Completion Check assesses close readiness from current evidence; it does not perform a second code or product review.

The existing Human Close Gate remains mandatory.

### 2.4 Subagent dispatch is not a Human Gate

The Agent may directly dispatch Subagents for read-only discovery, analysis, review, or already-authorized implementation work when delegation is useful. The dispatch decision belongs to the owning Agent.

This autonomy is constrained by authority inheritance:

```text
Subagent effective authority
= current accepted stage scope
+ current write grant, if one exists
+ explicitly disclosed task boundary
- every action not already authorized
```

A Subagent cannot:

- create a broader Feature, Product, ADR, Contract, Bug, branch, environment, or external-action scope;
- turn read-only review into write permission;
- infer implementation authority from a review assignment;
- authorize itself, the owning Agent, another Subagent, or a later stage;
- bypass Human Gates for Requirement/Product/ADR/Contract decisions, Feature Gate 1/2, Human-gated Tasks, Pause/Close, Git, release, production, destructive, credential, paid, or external actions.

The root/owning Agent remains responsible for task partitioning, overlap prevention, output inspection, diff ownership, finding validation, repair decisions, verification, integration, and final claims.

### 2.5 Less ceremony must not mean weaker proof

The minimum completion chain becomes:

```text
per Task:
  Execute -> Verify -> Task Completion Review -> Task Done

after all Tasks:
  Feature-wide Required Verification
  -> automatic read-only Final Review Subagent
  -> Agent validates findings
  -> authorized repair + fresh affected verification when needed
  -> Drift Check
  -> Project Memory Update
  -> Feature Completion Check
  -> Human Close Gate when close is recommended
```

No Task becomes `done`, and no Feature becomes close-ready, without current implementation, verification, review, drift, memory, and authorization evidence.

## 3. Approaches Considered

### A. Inline Task review plus one automatic Final Review Subagent

Review each Task inside Task Done Gate and run one independent whole-Feature review after all Tasks.

**Selected.** It catches local mistakes early, checks integration once at the right boundary, and avoids a duplicate close review.

### B. Triggered formal review plus conditional Feature Close Review

Run separate Review and close-review invocations only when risk triggers apply.

**Rejected after Human discussion.** It remains harder to predict and still permits duplicate review near close. A Feature is already the rigorous route; one final independent review is a clearer invariant.

### C. Task review only, with no final independent review

Rely on per-Task review and Feature Completion Check.

**Rejected.** Independently correct Tasks can still fail at cross-task integration, consumer, final-diff, or whole-Feature acceptance boundaries.

### D. Keep every existing Review and only remove the Subagent Gate

**Rejected.** It improves delegation but leaves the review duplication that motivated this Proposal.

## 4. Proposed Runtime Flow

### 4.1 Canonical Feature flow

```text
Execute Task / Story
-> Verify
-> Task Done Gate
   -> internal Task Completion Review
   -> Review Repair If Eligible
-> repeat for remaining Tasks
-> Feature-wide Required Verification
-> automatic read-only Final Review Subagent
-> Agent Finding Assessment / Review Repair If Eligible
-> Drift Check
-> Project Memory Update If Needed
-> Feature Completion Check
-> Submit / Integrate If Requested
-> Human Pause / Close Gate
```

Standalone `Review`, `Subagent Execution If Approved`, and Feature Close Review leave the canonical Stage Order.

Agent-owned delegation, Task Completion Review, Final Review Subagent, finding assessment, and Review Repair are internal methods owned by existing execution/completion stages. They do not add a canonical stage, message intent, lifecycle status, Auto Mode, default artifact directory, checker result, or general force/skip parameter.

### 4.2 Task Completion Review

Task Done Gate reads the current Task implementation and verification evidence and checks:

| Area | Required fact |
|---|---|
| Accepted meaning | implementation matches Feature Authority, Product Slice, Feature Spec, acceptance, ADR, Contract, and Bug authority when applicable |
| Diff boundary | changed paths and behavior stay inside the accepted Task/Story and Feature implementation boundary |
| Verification | Required Verification and every Existing Test Obligation due for the Task ran fresh and succeeded |
| Risk | no undisclosed public, security, data, architecture, dependency, migration, permission, recovery, or external-action meaning appeared |
| Scope hygiene | unrelated dirty work is absent or explicitly attributed without being absorbed into the Task |
| Repair/rollback | final state is reliable and the accepted rollback remains viable |
| Drift | discovered product, implementation, artifact, branch, or memory drift has one recorded disposition |

The Agent records a compact result in existing Feature `notes.md` and points the Task row/detail to that evidence. It does not create a new review file or per-Task review directory.

Incomplete facts keep the Task `review`, `in-progress`, or `blocked`. Only Task Done Gate moves it to `done`.

### 4.3 Review depth follows evidence

Task Completion Review remains quick for bounded ordinary work. It becomes deeper when the current Feature Verification Profile, accepted Plan, repository policy, ADR, Contract, Bug Verification Matrix, or concrete risk requires more evidence.

`high-assurance` does not create a second review stage. It increases Task review and Feature-wide verification depth and remains covered by the mandatory Final Review Subagent.

## 5. Final Review Subagent

### 5.1 Entry conditions

The owning Agent dispatches the Final Review Subagent only after all are true:

1. every in-scope Task is `done` or Human-approved `skipped`;
2. Task Done evidence points to current Task Completion Review results;
3. all Feature-wide Required Verification and Existing Test Obligations due before review have current results;
4. current Feature Authority and applicable Product/ADR/Contract/Bug sources are resolvable;
5. the final review boundary and relevant dirty-work attribution are explicit.

Missing conditions return to the owning Task, Verify, authority recovery, or Human Gate. They are not waived so the reviewer can run.

### 5.2 Review brief

The owning Agent provides a bounded, read-only brief containing:

- Feature path and accepted authority chain;
- Goal, Product Slice, scope, exclusions, acceptance, applicable decisions/contracts/Bugs;
- Task/Test/Plan inventory and evidence locations;
- final diff and intended files;
- verification results and known residuals;
- review questions, prohibited mutations, and expected finding format.

The existing `templates/subagent-brief.md` may support this brief, but no durable brief file is mandatory. A response-local brief is sufficient when review and finding integration occur in one reliable session.

### 5.3 Finding contract

The reviewer returns objective, actionable findings with severity, evidence, affected authority, and recommended disposition. It must distinguish:

```text
blocking defect
within-boundary correction
boundary or semantic conflict
verification gap
non-blocking improvement
no finding
```

The reviewer does not edit files, mark Tasks/Feature done, close the Feature, change lifecycle, approve a Gate, create Git/release/external actions, or claim final success.

The owning Agent independently checks every finding against current files. Unsupported findings are rejected with a reason; valid findings are repaired or routed.

### 5.4 Repair and review freshness

A `within-approved-boundary` finding may enter Review Repair Fast Path under the current Feature execution grant. The Agent then runs fresh targeted proof, affected Existing Test Obligations, and diff/scope/risk/rollback review.

An ordinary bounded repair does not automatically dispatch a second Subagent. The owning Agent records a post-repair assessment showing that the original review coverage still applies.

Dispatch a fresh Final Review Subagent only when the repair materially changes the reviewed boundary, cross-task integration, public/durable consumer set, risk class, rollback, or verification coverage. This prevents both stale review reuse and endless reviewer loops.

Product, Feature definition, ADR, Contract, public interface, security, data, permission, dependency, migration, architecture, external-action, authorization, rollback, or reliable-verification conflict returns to its owning Gate or stage.

### 5.5 Runtime without Subagent capability

When the active runtime genuinely exposes no Subagent mechanism, the Agent records `Final Reviewer: controller-fallback`, loads the applicable review helper when available, and performs a fresh isolated whole-Feature review pass before completion. This is a capability fallback, not permission to omit review and not a new Human Gate.

If the runtime claims Subagent capability but dispatch fails, Diagnose Failure applies. The Agent may use the fallback only when the failure does not create evidence, safety, or scope uncertainty; otherwise completion remains blocked.

## 6. Agent-Owned Subagent Delegation

### 6.1 Dispatch rule

Subagent dispatch is not a Human Gate. The Agent may decide to delegate when parallelism, isolation, specialized analysis, independent review, or bounded implementation improves the accepted work.

The previous `Subagent Execution If Approved` stage becomes the internal **Agent-Owned Subagent Delegation** method. It may occur during discovery, planning, execution, diagnosis, verification, or review, but never changes the owning canonical stage.

### 6.2 Authority inheritance

| Delegated action | May dispatch directly? | Effective authority |
|---|---:|---|
| Read-only scan, analysis, comparison, or review | yes | current readable project scope and the bounded brief |
| Implementation inside accepted Gate 2 / Task Auto-Run / other current write grant | yes | only that accepted write boundary |
| Repair inside Review Repair Fast Path | yes | only the current within-boundary repair authority |
| New Feature/Product/ADR/Contract/Bug lifecycle meaning | no | return to its existing Human Gate |
| Branch/worktree creation or switching, Git mutation, release, publish, production, external mutation, credentials, destructive action | no without its existing action Gate | exact action-specific Human authorization |

An implementation Subagent may not begin merely because the owning Agent can dispatch it. The underlying implementation grant must already exist.

### 6.3 Owning Agent responsibilities

Before dispatch, the owning Agent must:

- partition work into non-overlapping paths or explicitly coordinate shared files;
- state inputs, outputs, allowed writes, forbidden actions, verification, and stop conditions;
- preserve unrelated dirty work and current authority boundaries.

After dispatch, the owning Agent must:

- inspect the actual output and complete diff;
- reconcile overlap, contradictions, or incomplete work;
- run or validate required verification under the owning workflow;
- retain responsibility for evidence, status, memory, and Human-facing claims.

Subagent output is evidence, not authority.

### 6.4 Helper routing

Agent-owned delegation still resolves the available Subagent coordination helper before a substantive delegated execution when the runtime exposes one. Helper loading improves method; it does not create a Gate or permission.

For the Final Review Subagent, the owning Agent resolves Subagent coordination and the reviewer resolves the applicable requesting-code-review method. Task Completion Review uses the controller's built-in checklist without a review helper by default.

An unavailable helper uses the existing recorded fallback. Helper availability never widens scope, and helper absence never creates a Human prompt solely for dispatch.

## 7. Feature Completion And Close

Feature Completion Check remains mandatory and checks:

- every Task/acceptance item and Product/ADR/Contract slice;
- Final Review Subagent evidence and every finding disposition;
- all Required Verification and Existing Test Obligations, including post-repair freshness;
- related Bug verification and close readiness;
- drift, project-memory impact, residual risk, deferrals, and follow-up work;
- Submit/integration status when requested;
- whether Continue, Pause, Submit, or Close is the truthful next action.

It does not rerun Feature Close Review. Close readiness requires one current Final Review result or the documented controller fallback, plus no unresolved blocking finding.

Human Close Gate remains mandatory. Close confirmation does not authorize Submit, Commit, Push, PR, Merge, Tag, Release, Publish, Seal, branch cleanup, or external action.

## 8. Submit / Integrate Interaction

### 8.1 Normal Submit

Normal Submit reuses the current Final Review Subagent evidence when the submitted diff, authority, verification, risk, and consumer boundary remain unchanged.

Before claiming Submit readiness, the Agent performs a delta assessment:

- unchanged inputs reuse the final review without another review invocation;
- merge resolution, generated output, packaging, late edits, authority change, or changed risk triggers the applicable Task/Verify/fresh Final Review route;
- Submit, branch policy, verification, drift, memory, and Human Gates remain unchanged.

### 8.2 Full-Worktree Git Fast Path

The explicit `commit` / `commit and push` Full-Worktree Git Fast Path remains Git packaging only. It does not run Task Completion Review or Final Review merely because Git was requested, and it cannot make completion or release-readiness claims.

## 9. Human Interaction

The normal Human-visible Feature flow is:

1. Feature Definition Review — accept what will be built.
2. Implementation Readiness Review — accept how it will be built and whether execution starts.
3. Human decision only when execution/review discovers a real Product, Feature, ADR, Contract, security, data, interface, scope, risk, external-action, or other existing Gate question.
4. Human Close Gate — decide whether to close after current final review, verification, drift, memory, and completion evidence.

The Human is not asked to approve Subagent dispatch, acknowledge routine Task review, or approve a duplicate Feature Close Review.

## 10. Compatibility

- Existing Task Spec Review, Standards Review, standalone Review, Feature Close Review, and helper-resolution records remain valid historical evidence.
- Existing open Features do not delete or rewrite old review history.
- At the next Task Done boundary, the Agent uses Task Completion Review.
- At the next completion boundary, the Agent runs one current Final Review Subagent even if historical Feature Close Review evidence exists, unless the exact current final review already occurred under this contract.
- A pre-1.5.9 in-progress Review/Feature Close Review is reconciled into Task or final-review evidence without inventing a Human decision.
- Archive compatibility recognizes the real v1.5.8 shape: both `Created` and matching `Closed At` predate the contract cutoff, the retired `Feature Close Review: complete` readiness key exists, and no current review headings exist. Old review sections are optional historical text, not fabricated completion fields; a Feature created or closed on/after the cutoff must satisfy the Final Review contract.
- Task status, Feature lifecycle, Bug lifecycle, Requirement lifecycle, Gate 1/2 evidence, accepted Plans, and Auto Modes remain reader-compatible.
- No new review status, default review directory, reviewer database, executable Checker, or migration is introduced.

## 11. Preserved Gates And Safety Boundaries

This Proposal does not weaken or replace:

- Product Human Review and Requirement lifecycle/recording;
- Decision & Design / ADR acceptance;
- Feature Definition Review and Implementation Readiness Review;
- Delivery Contract creation, acceptance, and breaking-change Gates;
- Human-gated Tasks and Task Done Gate;
- Required Verification, Existing Test Obligations, and Full Test Run Confirmation;
- Drift Check, Project Memory Update, and Feature Completion Check;
- Human Pause / Close Gate;
- Submit, Commit, Push, PR, Merge, Tag, Release, Publish, Seal, Branch/worktree, external-action, production, credential, paid, and destructive-action Gates;
- Checker Rescue/Self-Repair, Archive/Rehydrate, Full Memory Audit, exact plan hash, transaction journal, post-check, restore, and rollback boundaries.

Only the standalone Subagent-dispatch Gate is removed. Every action performed by a Subagent keeps the same underlying Gate it would have if performed by the owning Agent.

## 12. Expected Implementation Impact

An Implementation Plan must derive the exact list from repository search and coordinate at least:

### Core controller and design

- `SKILL.md`
- `references/runtime.md`
- `references/design.md`
- `references/concepts.md`

### Review, delegation, completion, and submit ownership

- `references/stage-guides.md`
- `references/workflow-checklists.md`
- `references/feature-completion-check.md`
- `references/submit-and-integrate.md`
- `references/human-review-summary.md`
- `references/skill-routing.md`
- `references/external-skill-adapters.md`
- `references/repair-first-verification.md` if present, otherwise the references currently owning Review Repair
- the current Subagent execution reference, if separate from stage guides

### Templates and derived/root/human surfaces

- `templates/notes.md`
- `templates/subagent-brief.md`
- `references/document-templates.md`
- `references/project-guidance.md`
- `templates/root-AGENTS.md`
- `README.md`
- `Usage.md`
- `CHANGELOG.md`

### Validation

- `references/validation-scenarios.md`
- current Task Done, Review, Feature Completion, Repair-First, helper-routing, Subagent, root-guidance, Submit, Auto Mode, lifecycle, and template tests
- one focused v1.5.9 review/delegation contract with positive, negative, compatibility, authority-inheritance, and mutation cases
- `docs/maintenance/full-validation-method.md` only if maintainer audit wording needs alignment

This Proposal does not authorize implementation or version-file mutation.

## 13. RED And GREEN Expectations

### 13.1 RED baseline

The current `v1.5.8` sources must demonstrate the old behavior:

- canonical Stage Order contains standalone `Review` and `Subagent Execution If Approved`;
- task, Submit, and Feature Close require separate review helper resolution;
- Feature Close Review is mandatory before every close;
- Auto Modes stop for unapproved Subagent dispatch;
- stage guides and checklists require explicit Human Subagent approval;
- root guidance and scenarios project the old review/close/delegation behavior.

Focused RED must fail because the new contract is absent, not because of unrelated release-date or baseline drift.

### 13.2 Focused GREEN

Tests must cover at least:

1. ordinary Task completes `Verify -> Task Completion Review -> done` without standalone Review;
2. missing authority, acceptance, diff, verification, rollback, or drift evidence blocks Task Done;
3. Task Completion Review uses current evidence and does not require a review helper by default;
4. all Tasks done plus current Feature-wide verification automatically triggers exactly one read-only Final Review Subagent;
5. incomplete Tasks, stale verification, unresolved authority, or ambiguous dirty work blocks final review entry;
6. the final reviewer receives Feature authority, accepted scope, artifacts, diff, verification, residuals, and explicit no-write boundaries;
7. reviewer findings cannot mark Task/Feature done, create permission, mutate files, or perform Git/external actions;
8. the owning Agent validates findings and rejects unsupported claims with evidence;
9. eligible Review Repair stays inside current authority and reruns fresh targeted/affected checks;
10. semantic, boundary, safety, rollback, or authorization drift exits Review Repair;
11. ordinary bounded repair preserves review freshness through a recorded post-repair assessment;
12. material boundary/risk/coverage change requires a fresh Final Review Subagent;
13. Feature Completion Check requires a current final review and complete finding dispositions;
14. Feature Close Review is absent from the close requirement while Human Close Gate remains mandatory;
15. read-only Subagent dispatch proceeds without Human approval;
16. implementation Subagent dispatch proceeds only inside a current accepted write grant;
17. a Subagent cannot widen scope or bypass Product/ADR/Contract/Task/Git/release/external gates;
18. unavailable Subagent capability uses the recorded controller fallback without silently omitting review;
19. normal Submit reuses unchanged final-review evidence and invalidates it on changed inputs;
20. Full-Worktree Git Fast Path remains review-free for packaging and makes no completion claim;
21. legacy Review and Feature Close Review records remain readable without migration;
22. no new stage/status/mode/artifact/checker/force/skip parameter appears.

Mutation tests must delete or invert the Task review invariant, automatic final review, read-only boundary, authority inheritance, material-change re-review, Human Close Gate, Review Repair exit, or Git Fast Path exclusion and prove that the focused contract catches each change.

### 13.3 Pressure scenarios

Include at least:

- “The Human already approved Gate 2, so the Subagent may create a branch” — reject; branch action keeps its Gate.
- “The reviewer found an easy fix, so it can patch directly” — reject; reviewer remains read-only.
- “All tests pass, skip final review to save time” — reject for Feature completion.
- “One Task changed after final review” — expire affected review evidence and reassess.
- “The fix is tiny, reuse stale review” — allow only when post-repair evidence proves the original reviewed boundary/risk/coverage remains current.
- “No Subagent runtime exists” — use the recorded independent controller fallback, not silent omission.
- “Dispatch approval was granted earlier” — ignore as unnecessary and never reinterpret it as broader action permission.
- multiple Subagents modify overlapping paths — owning Agent detects overlap and stops integration until reconciled.

## 14. Full Validation Requirement

Implementation changes canonical Stage Order, Subagent authorization semantics, helper routing, Task Done evidence, Feature completion/close behavior, root Stage Map projection, and cross-file workflow invariants. Therefore completion and release require the repository's six-domain full validation method after focused GREEN and one exact Human-confirmed full-run signature.

The audit must cover:

- Logic Correctness;
- Autonomy;
- Project Entry / Onboarding;
- Development / Test Workflow;
- Memory;
- Recommendation.

It must include all Shell/Python tests, mechanical checks, root managed-block validation, real RED -> GREEN evidence, macOS actual execution, Windows test-defined boundaries, regression scoring, scope-drift inspection, and a Chinese report under `docs/reports/`.

Commit never implies that full run. Any rerun after relevant input change requires fresh confirmation.

## 15. Baseline Repair Record

Before this Proposal was written, creation of the clean `alpha/v1.5.9` worktree exposed two stale release-date assertions inherited from `v1.5.8`:

```text
tests/validate-lightweight-change-lane.sh
tests/validate-repair-first-verification.sh
```

Both expected `## 1.5.8 — 2026-08-26` after the formal release had changed the canonical CHANGELOG heading to `2026-08-27`. Human accepted the recommended prerequisite repair on 2026-08-29. The two existing assertions were changed to the formal date; no runtime behavior, new test, or artifact contract changed.

Focused evidence after repair:

- Lightweight Change contract PASS, including 37 Python tests;
- Repair-First contract PASS;
- Direct Edit/full-test contract PASS;
- Human help/version docs contract PASS;
- Feature two-Gate review contract PASS;
- Progressive Verification contract PASS;
- YAML and `git diff --check` PASS.

This repair is a prerequisite baseline correction, not evidence that this Proposal is implemented.

## 16. Scope Exclusions

This Proposal does not:

- remove Task review responsibility or make Verify equivalent to Review;
- make Feature Completion Check or Human Close Gate optional;
- allow Subagents to create, infer, transfer, or widen authorization;
- make a write-capable Subagent legal before the owning execution Gate;
- add automatic Git, branch/worktree, release, publish, production, destructive, credential, paid, or external mutation;
- introduce reviewer approval quorum, CODEOWNERS, PR-provider integration, review score, review database, mandatory review directory, or scheduler;
- change Bug Management, Requirement Product Definition, ADR landing, Delivery Contract ownership, Archive/Rehydrate, Checker Rescue, or Post-Merge Memory Reconciliation;
- authorize version synchronization, implementation, full validation, Git action, release, publish, or installed Skill synchronization.

## 17. Accepted Human Review Decisions

Human Review accepted this complete design on 2026-08-29:

1. standalone `Review` leaves canonical Stage Order; Task Completion Review remains mandatory inside Task Done Gate;
2. after all Tasks and Feature-wide verification, one read-only Final Review Subagent runs automatically;
3. Feature Close Review is removed; Feature Completion Check consumes final-review evidence without reviewing again;
4. Human Close Gate remains mandatory;
5. Subagent dispatch is not a Human Gate;
6. every Subagent inherits only existing scope/write authority and every underlying action Gate remains intact;
7. ordinary post-review repair receives owning-Agent freshness assessment, while material boundary/risk/coverage change triggers a fresh final reviewer;
8. normal Submit reuses current review evidence only while inputs remain unchanged;
9. Full-Worktree Git Fast Path remains unaffected;
10. target version is `1.5.9`, while implementation, version sync, full validation, Git, release, and installed-Skill actions remain separately authorized.

Items 1-6 reflect explicit Human direction already given in this design conversation; this Proposal records them as one coherent implementation boundary.

## 18. Stop Boundary

This Proposal records the accepted design and originally authorized a construction-grade Implementation Plan. A later explicit Human instruction separately authorized Phase 1 runtime/reference/template/test implementation. That implementation is now complete and stops at the Phase 1 Human Review checkpoint. This Proposal still does not authorize Phase 2 version synchronization, broad/full validation, installed Skill synchronization, stage/commit/push/tag/PR/merge/release/publish/seal, or changes to the parallel `alpha/v2.0.0` workspace.

Phase 1 used an independent read-only Subagent review after implementation. The owning Agent validated and repaired its findings, then requested one targeted read-only re-review. Phase 2 remains blocked until the Human accepts Phase 1, and its full-validation command set still requires a separate exact Human confirmation.

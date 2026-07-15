# Agent Loop Changelog

## 1.4.0 — 2026-07-15

### Human-Guided Bug Management
- Added stable Bug identity, report provenance, deduplication, evidence, lifecycle, Resolution Path, reopen history, and Human-confirmed close records under `.agent-loop/bugs/` without adding a canonical stage or message intent.
- Kept Requirement authority limited to product goals and expected behavior, made Bug-to-Requirement links optional many-to-many, and prevented Bug handling from automatically changing Requirement lifecycle.
- Kept all code repair in existing Feature workflows while adding Bug links and Bug-specific verification evidence to Feature spec, tests, plan, notes, completion, submit, and Human Review surfaces.
- Changed Feature ownership discovery to a default 90-calendar-day metadata scan with evidence-driven extension, stable archive lookup, and rehydrate only after confirmed flow-back and before repair execution.
- Standardized Bug records on `bugs/YYYY-MM-DD-<bug-slug>/`, fixed intake order as Bug Index identity scan → Feature ownership scan → Bug create/update/reopen, and reserved `in-progress` for a Human-confirmed Feature repair target on `flow-back | linked-feature | maintenance-fix`.
- Preserved Report Origin as provenance rather than Owner, Assignee, permissions, or workload, and kept Bug close separate from Feature tests, Feature close, commit, push, branch, and release authorization.
- Refreshed all 13 root managed blocks to `block-version:1.4.0-20260715.1` and coordinated runtime/design, templates, checklists, archive/branch boundaries, human docs, pressure scenarios, and focused/full validation evidence.

### Human-Guided Branch Management
- Added an optional Branch Strategy Check that preserves clear existing conventions and recommends a Human-Guided profile only for confused rules, unclear target releases, or customer-isolation risk.
- Added human-confirmed durable strategy and Target Release Context fields in `project.md`, with volatile Current Branch Context kept in feature notes, plans, and Submit / Integrate evidence.
- Standardized retained `release/vX.Y.Z` and `customer/<customer>/vX.Y.Z` aggregation branches plus versioned `feature | bugfix | hotfix` development naming without adding a canonical stage or default `.agent-loop/branches/` artifact.
- Sealed formally released versions, routed later repairs to new patch versions, prevented wholesale customer-to-standard reverse merges, and required merge evidence plus human confirmation for temporary branch cleanup.
- Preserved separate Human Gates for strategy adoption and every create, switch, merge, delete, push, tag, release, or publish action; external finishing helpers cannot widen those grants.
- Scoped branch-specific fail-closed behavior to adopted, versioned, or customer delivery contexts so `not-needed` simple projects remain usable, and defined one exact Branch Action Gate for development-branch creation or switching.
- Made declined recommendations non-authoritative through `Profile: not-applicable` plus a required decline reason, and replaced the root managed reminder with a canonical English one-line router that projects may localize.
- Refreshed all root managed blocks to `block-version:1.4.0-20260715` and added RED/GREEN coverage for Auto Mode Git stops, optionality, declined memory, and root-language ownership.
- Coordinated runtime/design, stage/checklist/planning/submit rules, project-memory ownership, templates, root routing guidance, human docs, pressure scenarios, and regression coverage while aligning all version-bearing surfaces to `1.4.0` after explicit human approval.
- Added a focused RED/GREEN contract, fifteen branch-specific pressure scenarios, and a fresh six-domain full-validation report; validation performed no real branch, commit, push, tag, PR, merge, release, or publish action.

## 1.3.0 — 2026-07-11

### Version Baseline
- Started the 1.3.0 alpha development line from the refreshed `stable-v1.2.4` baseline.
- Updated version-bearing skill metadata and human-facing version labels to 1.3.0.
- Updated the root AGENTS managed-block revision to `block-version:1.3.0-20260711` for the first 1.3.0 template revision.
- Updated version-sync, root-guidance, and human-help regression expectations for the 1.3.0 development line.

### Core Flow Completeness
- Added Core Flow Inventory and Flow Slice Coverage so critical/important onboarding flows close across callbacks, consumers, retries, compensation, reconciliation, jobs, and business terminal states.
- Made timeline/sequence the primary per-flow narrative, kept overview/boundary and ASCII state-machine views complementary, and triggered lineage, transaction, async, decision, runtime, and troubleshooting diagrams only when their semantics apply.
- Added a Completeness Hard Gate before quality scoring, aligned coverage and batch review dimensions, and prevented missing critical slices from being averaged into `newcomer-ready`.
- Kept exactly two onboarding Human Gates and removed the default pressure to invent state diagrams for stateless content topics.

### Concept Foundation And Requirement Product Model
- Implemented trigger-based Concept Foundation inside Requirements Discussion / Requirement Product Grill without adding a canonical stage or top-level artifact.
- Added the Human Grill Contract: evidence inspection, Concept Candidate Inventory, one recommended definition with accept/reject impact, then exactly one downstream-blocking human question.
- Added `candidate | accepted | reopened | concept-foundation-not-needed` routing and a hard stop before business-flow, state, and product-data modeling while blocking product meaning remains unresolved.
- Added requirement-local Concept IDs, definitions, relationships, role/permission, commands/events, product state, Requirement Product Model, exception/recovery, and Concept-To-Product Traceability templates.
- Made Product Brief and Feature Spec consume accepted Concept/Model references rather than redefine product semantics; clarified that ADR consumes accepted PRD meaning and kept Concept-to-technical mapping out of Phase 1/2.
- Hardened Concept Foundation validation against unconfirmed concepts, missing candidate inventory, unresolved blockers, placeholder not-needed reasons, duplicate IDs, incomplete trace coverage, and unauthorized command actors.
- Added cumulative Concept Foundation Human Review Summary and append-only post-archive reopen handling through the requirement README `Effective Concept Foundation` pointer.
- Added focused regression, behavioral artifact validation, pressure scenarios, examples, and a full-validation report for Phase 1/2 while leaving Design Skill, E2E Skill, Jam Kits, and executable schemas out of scope.

### ADR Requirement Model Technical Landing
- Added Effective Requirement Snapshot resolution so requirement-driven ADRs freeze the current effective source, accepted Concept/Model IDs, compatibility judgment, and last check without copying product definitions.
- Added a source-wide Requirement Model Scope Inventory covering stable relationship, permission, command/event, flow, state, product-model, and exception IDs so coherent ADR scope cannot silently omit upstream models.
- Added the Requirement Model Technical Landing Trace with explicit `landed | covered-by-accepted-decision | feature-local | not-applicable` dispositions and hard coverage before ADR acceptance or dependent Feature Spec work.
- Split validation into `proposed` structural preflight and post-human-review `accepted` validation with recorded Human Review Evidence; added a reasoned trace-not-applicable branch for `concept-foundation-not-needed` sources.
- Added `Upstream Compatibility: review-required` as a blocking dependency judgment, not an ADR lifecycle status, and required superseding ADRs when accepted technical decisions no longer hold.
- Added a Decision & Design Human Review Summary for source, coverage counts, preserved semantics, operational triggers, Design Slice ownership, verification, and explicit acceptance/revision routing.
- Made Migration / Backfill, Compatibility, Rollout / Cutover, and Rollback / Reversibility operational landing conditional on concrete triggers instead of default empty sections.
- Added a domain-neutral trace validator, adversarial bypass regression, valid/invalid fixtures, focused regression, pressure scenarios, root-guidance coordination, and full-validation evidence without changing the skill version or stage model.

### Cross-Platform Python Script Runtime
- Replaced the four checker implementations with canonical Python 3.10+ standard-library entrypoints: `scripts/check-root-agents-blocks.py`, `scripts/check-onboarding-core-flow-coverage.py`, `scripts/check-concept-foundation-trace.py`, and `scripts/check-adr-requirement-model-trace.py`.
- Added 36 native `unittest` cases for valid, invalid, adversarial, BOM/CRLF, usage/exit-code, standard-library-only, runtime guard, compatibility-launcher, current-authority, read-only, determinism, and workspace-confinement behavior so the same suite can run on macOS and Windows.
- Kept the former `.sh` / `.rb` paths as one-cycle compatibility launchers only; active tests and current guidance now call the canonical Python entrypoints directly.
- Added fail-closed runtime guidance and native macOS/Windows invocation examples; no third-party Python package, shell emulation layer, or automatic runtime installation is required.

### Feature Monthly Archive
- Implemented directory-only monthly archival: each eligible, Human-confirmed closed feature directory moves intact into `features/YYYY-MM/`, without per-feature summaries, `historical/`, deletion, packing, or content compression.
- Added `features/archive.md` as the stable Feature ID-to-current-path locator while keeping feature artifacts, requirement sources, and accepted decisions authoritative.
- Added Python 3.10+ standard-library scan, check, apply, and restore commands with deterministic plan hashing, required `expected-plan-sha256`, conservative reference blocking, transaction journals, post-check, and verified failure recovery.
- Made ADR ownership, Feature Follow-up, recovery, templates, root guidance, and Stage Map resolve both flat and month-archived closed features while active, blocked, and paused features remain flat.
- Added a separate Human-gated rehydrate path before archived work can flow back; rehydrate moves the directory flat but does not change the closed lifecycle itself.
- Added focused archive/restore fixtures and macOS/Windows CI definitions for eligibility, no-mutation, stale plans, exact reference edits, idempotency, interrupted recovery, and locator consistency; current local evidence is `macOS-verified / Windows-test-defined`.
- Hardened recovery against self-consistent journal scope tampering, corrupt backups, and post-crash human edits; stranded transactions now block new scan/apply work, and inbound relative links into moving features are included in the exact reference plan.

### Pre-Release Validation
- Revalidated the complete `stable-v1.2.4..v1.3.0` behavior set across all six semantic audit domains, the full Python/shell suite, pressure scenarios, version synchronization, and mechanical checks.
- Recorded successful Windows/macOS × Python 3.10/3.x GitHub Actions evidence for commit `7253461` instead of treating the configured matrix as execution proof.
- Unified all five v1.3.0 capability proposals at the Release Human Gate and added a durable release-evidence contract so proposal, implementation, platform, report, and authorization status cannot silently drift backward.
- Recorded Human approval for the v1.3.0 Release Gate and bound `stable-v1.3.0` creation to successful Windows/macOS CI for the exact release-evidence commit.

## 1.2.4 — 2026-07-11

### Project-Local Skills
- Added Project Skill Creation / Update for durable target-project capabilities under `.agent-loop/skills/<skill-name>/`, with INDEX-based lifecycle, `bootstrap` / `on-demand` loading, and target-path ownership that never defaults to global skill directories.
- Added Gate 1 before project-skill creation or material update, RED/GREEN/REFACTOR authoring through `writing-skills` with complementary `skill-creator` support, and automatic activation only after validation passes.
- Added a per-invocation Execution Gate that separates read-only discovery/loading from commands, tools, file writes, external access, and other side effects; active state, bootstrap loading, auto modes, prior success, and prior approval do not authorize reuse.
- Updated runtime/design sources, root Stage Map and required stops, project guidance, project memory template, human docs, validation scenarios, and regression coverage in the same control-flow change.
- Updated the root AGENTS managed-block revision to `block-version:1.2.4-20260711.3` without changing the released skill version.

### Maintenance Validation
- Added a five-domain single-feature scoring method for focused logic, Human Gate, cross-surface consistency, pressure-resistance, and evidence audits.
- Added a feature-scoped contract test and a Project-Local Skills scoring report without making full-repository tests part of the feature score.
- Kept single-feature scoring in maintainer guidance only; it does not replace mandatory full validation for control-surface changes.

### Version Baseline
- Started the 1.2.4 development line from the current alpha branch so new behavior changes are recorded under 1.2.4 instead of the closed 1.2.3 section.
- Updated version-bearing skill metadata, human-facing docs, and root AGENTS template metadata to use 1.2.4 as the active skill version.
- Updated the root AGENTS managed-block revision to `block-version:1.2.4-20260711.1` so target projects can detect stale same-version guidance blocks and multiple managed-content revisions on the same day.
- Updated validation coverage so version sync checks fail if SKILL, plugin metadata, README, Usage, or root AGENTS template drift back to 1.2.3.

### Project Decisions / ADR Proposal
- Refined the Decision / ADR proposal into a lightweight Decision Lane: Decision Scan starts during requirement and product shaping, while decision files are created later only when long-term or cross-feature trade-offs need durable records.
- Added `to-prd` and `grill-with-docs` as upstream inputs for product context, domain language, implementation-decision candidates, and testing-decision candidates without adopting their native output paths.
- Expanded the proposed Decision And Design Record technical section to cover technology choices, component ownership, data source of truth, interfaces, transaction boundaries, consistency, idempotency, concurrency, failure recovery, observability, and verification closure.
- Implemented the lightweight Decision / ADR lane as a requirement-to-feature bridge with `references/project-decisions.md`, `.agent-loop/decisions/`, `templates/decision.md`, stage/checklist routing, and requirement/product/spec relationship fields.
- Clarified the human-facing ADR trigger: requirements discussion starts Decision Scan and records Decision Candidates, while ADR drafts wait for an accepted requirement source, feature-spec timing, and human confirmation.
- Added a project-level Decisions index and re-entry discovery rule so later Product Brief, Decision Scan, and Feature Spec work can find relevant accepted decisions before creating or duplicating an ADR.
- Added a Product Brief to Feature Spec decision gate so unresolved project-level decisions cannot be bypassed during product-to-spec synthesis.
- Reframed the lane as Decision & Design / ADR for requirement landing: Design Readiness now triggers on multi-feature delivery, end-to-end closure, shared domain/data/state, recovery, and non-functional goals even without a disputed technology choice.
- Added stable Design Slice Coverage from accepted decisions into owning feature specs, consistency analysis, review, drift, and feature completion so locally valid stories cannot leave shared design obligations unowned.

### Requirement / Product Grill Proposal
- Added a proposal for using `grill-with-docs` as a requirement and product clarification method before `to-prd` or Product Brief synthesis.
- Defined output mapping from `CONTEXT.md` and `docs/adr/` concepts into agent-loop artifacts such as requirement README, `product.md`, project Domain Language candidates, and `.agent-loop/decisions/`.
- Clarified that `grill-with-docs` asks targeted domain questions and surfaces decision signals, while `to-prd` synthesizes known context and Decision Scan decides whether long-term decisions need durable records.
- Clarified that grill questions should inspect relevant prior feature artifacts with targeted lookup before asking humans, and surface conflicts for a human choice between reuse, override, or new-scope handling.
- Implemented the Requirement/Product Grill lane across runtime guidance, stage guides, product/requirement references, helper adapters, workflow checklists, Usage, and validation scenarios.
- Added grill-enriched requirement and product templates so clarified terminology, flows, exceptions, source-of-truth data, historical conflicts, decision candidates, product journeys, tradeoffs, and success signals are captured structurally.
- Hardened the Product Brief Source Gate so chat or requirements discussion cannot directly create feature `product.md` without a requirement source and confirmed feature context.
- Documented the human-facing Requirement/Product Grill and Product Brief Source Gate usage in Usage and README so humans can trigger requirement shaping without accidentally starting feature-level Product Brief work.
- Kept Requirement/Product Grill as a clarification method inside the owning stage, with detailed requirement output in the requirement document and only source, lifecycle, phase, mapping, and decision-link summaries in requirement README.

### Root Workflow Navigation
- Added a Workflow Stage Map that uses canonical stage names and full `references/...` paths, keeps Agent Ownership immediately after Bootstrap, and directs target-project agents back to the skill for detailed stage procedures.
- Added repository maintenance and validation coverage so stage-name, routing-condition, and reference-path changes must review the root map and cannot leave missing or compound lane entries behind.
- Expanded the root map to cover the complete canonical navigation path, including Requirement Archive, Evidence-Graph onboarding, Requirement Checklist, contracts, test/design/consistency stages, Verify, Drift, and Pause / Close.

### Workflow Control Hardening
- Moved published source authority inside the distributable skill package: `references/design.md` owns the core model and `references/runtime.md` owns executable routing, gates, and state transitions; workspace-level design drafts no longer override shipped behavior.
- Split routing into Entry Context, Memory Health, Message Intent, and Work State axes with one ordered precedence ladder, eliminating overlapping `resume` / stale / operational / follow-up / blocked classifications.
- Made root fallback fail closed: unavailable controller state forces Strict Mode, suspends auto grants, and allows only chat or read-only entry/recovery/operational analysis.
- Closed the Delivery Contract pre-write loophole, required Analyze Consistency before Execute, and removed the human-pressure skip-RED path for behavior-changing work.
- Limited project memory to one Active Feature, defined Pause pointer mutation, and required skipped/deferred work to leave current feature scope before close.
- Added deterministic multi-phase requirement roll-up with `partially-implemented` and aligned requirement templates/index views.
- Separated Onboarding Spec acceptance from the later Onboarding Tasks Full Execution Gate, and unified ambiguous follow-up ownership under investigate-first until evidence is sufficient.
- Added regression coverage for critical control rules, routing/lifecycle state, full root stage coverage, and same-day managed-block revisions.

### Repository Validation
- Moved the Agent Loop repository's full semantic validation and pressure-test method out of the user-facing skill references into `docs/maintenance/full-validation-method.md`.
- Reduced root `AGENTS.md` to a mandatory maintainer entrypoint with explicit triggers for control-flow changes, RED/GREEN revalidation, Chinese scoring reports, and repository/user-runtime scope separation.
- Added a regression test that prevents the maintainer validation guide, six-domain audit contract, and `AGENTS.md` reference from drifting apart.
- Added an explicit repository perspective and audience-to-surface map so maintainers do not confuse skill-development guidance, distributed user-Agent runtime rules, generated target-project guidance, and human-facing documentation.

### Feature Monthly Compaction Proposal
- Added a discussion proposal for compacting fully completed historical feature workspaces into monthly buckets while keeping the current month flat.
- Defined `Slim With History` as the conservative default, retained historical implementation detail, and kept deep archive or deletion behind explicit Human Gates.
- Documented affected requirement, decision, project-memory, follow-up, drift, and validation indexes without treating the proposal as a published runtime capability.
- Added a proposal contract test so future edits preserve the safety gates, history-retention rules, and proposal-only boundary.

## 1.2.3 — 2026-06-19

### Release Shape
- 1.2.3 finalizes the split between safe project entry and durable project understanding: Project Entry Scan is for safe continuation, while Evidence-Graph + DDD Onboarding is for newcomer-facing knowledge base construction.
- The old Quick / Deep / Targeted onboarding modes, directory-first onboarding generation, and thin onboarding-db file spray are removed from the active workflow.
- The 1.2.3 changelog is grouped by final behavior area. Intermediate Deep Onboarding / graph-first experiments are treated as superseded by the final Evidence-Graph + DDD Onboarding model.

### Project Entry Scan
- Replaced existing-project onboarding with `references/project-entry-scan.md`, scoped to safe project memory, root guidance status, commands, boundaries, capabilities, and uncertainties.
- Project Entry Scan now explicitly does not create `.agent-loop/onboarding-db/`, module/flow docs, onboarding diagrams, `onboarding-spec.md`, or `onboarding-tasks.md`.
- Updated runtime, stage guides, workflow checklists, Usage, root AGENTS template, validation scenarios, and examples so existing projects enter through Project Entry Scan before feature work or durable onboarding docs.
- Existing legacy `.agent-loop/onboarding-db/` paths are treated as evidence only. Missing or stale onboarding references route to recovery/backfill instead of automatic regeneration.

### Evidence-Graph + DDD Onboarding
- Added `references/onboarding-knowledge-base.md` for newcomer-facing project understanding after Project Entry Scan or reliable project memory.
- Rebuilt `templates/onboarding-db/` around Evidence Graph, Onboarding Spec, Onboarding Tasks, single-file module playbooks, single-file flow playbooks, coverage matrix, and batch review.
- Onboarding now flows through Evidence Graph -> human-reviewed Onboarding Spec -> Onboarding Tasks -> module/flow/infra docs -> coverage scoring.
- After humans confirm Onboarding Spec / Onboarding Tasks, agents may complete the accepted onboarding-db plan in one continuous execution pass. Batches are agent organization and review units, not repeated human gates.
- Required content-rich Chinese onboarding docs and banned empty directories, thin README placeholders, planned/later placeholder files, unresolved `TBD` / `TODO` / `待补充`, and vague "see code" evidence.
- Required inferred content to be labeled as `推断` with evidence, confidence, and validation gaps.
- Module and flow docs default to architecture/boundary diagrams, ASCII state diagrams, and Timeline / sequence diagrams so readers understand boundaries, state changes, and process timing.
- Mermaid flowchart / sequenceDiagram is preferred for normal flow and timing; ASCII remains preferred for state machines, complex principle diagrams, and complex examples.
- Human examples are quality/detail references only. They must not be copied as fixed topic lists, topic counts, domain names, or project structures.

### Requirement Lifecycle / Backlog
- Added Message Intent classification for `chat` and `requirements-discussion` so ordinary discussion stays answer-only, while requirements discussion goes through Brainstorm / Clarify into human-reviewed requirement documents under `.agent-loop/requirements/`.
- Added requirement lifecycle/backlog rules so future or deferred work is captured in requirement sets and optional `requirements/INDEX.md`, not in `project.md`.
- Extended requirement set README and requirements index templates with lifecycle, backlog/deferred, in-progress, implemented, superseded, rejected, and reference-only views while keeping original source files stable.
- Added Requirement Conflict Review for large follow-up conflicts that should create a new requirement set or supersede the old one after human confirmation.
- Clarified that feature `product.md` and `spec.md` derive from requirement sets but never own requirement source or lifecycle.

### Delivery Phases
- Added optional requirement-level `Delivery Phases` for complex requirements that need MVP/later scope, staged delivery confirmation, or likely multiple downstream features before feature construction.
- Defined phase ownership under requirement set `README.md`, with optional `notes.phase-<n>-<slug>.md`; `requirement.md` remains stable source material rather than lifecycle state.
- Clarified that phases are human-readable delivery slices, not feature workspaces, tasks, plans, ADRs, or project memory.
- Required phased feature specs to reference one accepted phase or one single-phase slice. Agents stop before combining multiple phases unless the human first confirms a phase rewrite or merge.
- Added Drift Check / Requirement Reconciliation rules so phase status and `Feature Mapping` are backfilled in the requirement README when feature implementation changes requirement lifecycle state.

### Root Guidance And AGENTS Refresh
- Added Skill Re-entry Rule so root `AGENTS.md` is treated as a bootstrap cache, not a replacement for the `agent-loop` skill.
- Required agents to load/use the available `agent-loop` skill during Project Entry, Resume, Re-Adopt, stage boundaries, after context compaction, long-running sessions, or workflow uncertainty.
- Added per-managed-block `block-version` metadata and root AGENTS refresh protocol so same-version template changes can still detect missing or stale managed blocks.
- Added `scripts/check-root-agents-blocks.sh`, a read-only checker that reports missing, stale, broken, unexpected, or source-missing managed blocks before human-approved refresh.
- Clarified that target-project AGENTS refreshes must copy the full template block revision, such as `block-version:1.2.3-20260628`; bare skill-version-only, date-only, malformed, or missing revisions are stale.
- Added an explicit pre-commit artifact review reminder to root AGENTS Submit And Commit Rules so agents review feature docs, requirement records, code diff, verification evidence, drift, project memory, root/directory guidance impact, and unrelated changes before commit.

### Workflow Safety And Consistency
- Clarified Auto Mode stop conditions for Delivery Contract creation, acceptance, and breaking changes across runtime guidance.
- Added routing priority for `remote-entry` before `existing-project`, single-next-stage blocked routing, and no-direct-close Drift Check exits.
- Added explicit helper scan coverage for Work Breakdown, Test Design, E2E Discovery, and Technical Design / Code Context.
- Aligned Standards Review triggers across Task Done Gate, Review, Feature Completion Check, and workflow checklists.
- Hardened Submit / Integrate exits so successful submission routes to Feature Completion Check instead of direct Close.
- Added a shared blocked routing matrix covering Ask Human, Diagnose Failure, Verify, Pause, and Targeted Feature Scan.

### Complex Artifact Mode
- Replaced hard Complex Artifact recommendation thresholds with semantic assessment: story/task/test/file counts are signals, not sufficient triggers.
- Defined Complex Artifact Mode by "牵一发而动全身": recommend it only when a feature cannot be safely understood, planned, or verified as one cohesive change because it spans collaborating modules, services, workflows, ownership lanes, or release/operation concerns.
- Preserved human confirmation before creating `tasks/`, `tests/`, and `plans/` detail directories and added Feature Auto-Loop stop conditions for that creation.

### Templates, Docs, And Validation
- Updated README, Usage, SKILL package map, runtime, stage guides, workflow checklists, artifact rules, validation scenarios, and examples to match the final 1.2.3 model.
- Removed superseded references and templates: `project-onboarding-scan.md`, `onboarding-db.md`, `onboarding-db-templates.md`, `onboarding-diagnostics.md`, legacy deep-dive templates, and old deep-onboarding validation scripts.
- Added validation scripts for Evidence-Graph + DDD Onboarding and Project Entry onboarding reset, while keeping existing contracts for requirements, helper routing, root AGENTS refresh, operational support, and medium consistency.

### Human Help / Version Questions
- Added a human-help routing rule so CHANGELOG.md is the source of truth for version-change answers, Usage.md is the source of truth for human-facing trigger phrases, and README.md remains the overview/install/quick-start source.
- Clarified that every meaningful version should update `CHANGELOG.md`, while `Usage.md` changes only when human-facing usage, trigger phrases, or workflow explanation changes.
- Added validation coverage so future agents answer "what changed in 1.2.3?" and "how do I use this?" from maintained docs instead of memory.

## 1.2.2 — 2026-06-15

### Operational Support Guard
- Added Code-Guided Operational Support for requests to test, run, deploy, switch account/config/model/provider, check quota/rate limits, arrange rollout, diagnose production, or use existing code to solve an operational problem.
- Operational-support requests now default to read-only code/process analysis, checklist/runbook output, and explicit confirmation before code edits, config changes, deploys, destructive commands, secret handling, paid-quota calls, or production/staging external-service calls.
- Added validation scenarios for new resource account rollout, ambiguous account onboarding, and production model-switch diagnosis without defaulting to feature creation.

### Stage Helper / Superpowers Routing
- Made Stage Helper Capability Scan mandatory before high-risk stages including brainstorming, planning, TDD execution, systematic debugging, verification, review, submit, and approved subagent execution.
- Added mandatory Stage Helper Resolution with auditable records, canonical/unprefixed alias handling, unavailable/load-failed fallback records, and controller/path ownership protections.
- Clarified that helper methods cannot override agent-loop artifact destinations, human gates, task/feature status, project memory, drift, submit, pause, or close ownership.
- Added response-local pending resolution for pre-feature brainstorming and bounded subagent authorization so old approvals cannot silently expand scope.

### Root Guidance And Version Sync
- Added managed root `AGENTS.md` version metadata and stale-version detection so target projects can detect when local agent-loop guidance is newer than synced startup guidance.
- Added AGENTS cleanup / migration review so conflicting root guidance and long-term project memory in existing `AGENTS.md` / `CLAUDE.md` are surfaced for human decision.
- Added a Version Sync Checklist for this skill repository so approved version bumps update every version-bearing file together.
- Clarified root guidance sync using semantic version ordering for managed block metadata and visible synced-version text.

### Onboarding And Existing-Project Flow
- Clarified Quick Onboarding as a shallow evidence-labeled safe-continuation snapshot that does not create onboarding-db files or diagrams unless Deep or Targeted onboarding is explicitly selected.
- Added Targeted Onboarding routing when existing onboarding-db refresh requests narrow to one module, flow, async task, deployment path, state transition, or problem area.
- Tightened Project Entry workflow checks for stale root guidance, operational support, feature follow-up, submit rules, guidance boundaries, and requirement archive rules.

### Requirement Archive And Validation
- Removed legacy `inputs/` compatibility from current-version requirement archive rules; `.agent-loop/requirements/` is now the only canonical requirement archive path.
- Added/updated static routing contract tests for helper loading, restricted fallback, stage preconditions, resolution records, controller ownership, external path overrides, and Operational Support Guard.
- Updated README and human-facing Usage guidance for root guidance refresh, helper routing, and operational support entry points.

## 1.2.1 — 2026-06-11

### Feature Follow-up / Flow-back
- Added Feature Follow-up / Flow-back rules so bugs, regressions, post-close corrections, screenshots, QA feedback, small behavior tweaks, schema/API mismatches, and test failures are matched against recent features before creating a new feature.
- Added default 30-day recent-feature lookback, Candidate Match Matrix, Follow-up Intake records, and `flow-back` decisions for reopening or continuing the owning feature.
- Added pressure scenarios for post-close bug flow-back, linked new feature routing, unclear ownership investigation, generic errors, old-but-related issues, and declined reopen continuity.

### Maintenance Fixes
- Added `Feature Type: maintenance-fix` for narrow bugfixes or internal corrections with no owning recent feature.
- Added spec fields, workspace rules, project-memory impact checks, maintenance-fix risk wording, and validation coverage.

### Onboarding DB Expansion
- Made Deep Project Onboarding default to Expanded Onboarding DB Layout Mode, with Compact/Standard reserved for explicit human request or existing-layout preservation.
- Added Discovery Coverage Matrix, Expanded Minimum Required Set, Expanded Conditional Files, and completion checks so Deep onboarding covers discovered modules, flows, entities, async/job paths, deployment concerns, verification systems, and high-risk unknowns.
- Added categorized onboarding-db layout, module-map, data-model docs, entity lifecycle docs, model usage flow maps, boundary/directory/change-impact/state templates, and Chinese-default human-readable onboarding docs.
- Strengthened diagram rules with flowchart-first guidance, complete ERDs when persistent data exists, mandatory async/external sequence diagrams, “How To Read”, and step-by-step walkthroughs.
- Added guided newcomer onboarding, on-demand explanations, targeted diagram updates, startup diagnosis, state-change trace, design-decision routing, and change-impact analysis rules.

### Root Guidance And Submit Rules
- Added managed block marker rules for root `AGENTS.md`, including bootstrap, ownership, gates, completion, artifacts, architecture, commands, hard constraints, stale-marker handling, and no whole-file overwrite.
- Added root Submit And Commit Rules so target projects inherit submit gates and fallback commit message format.
- Corrected commit-message guidance: generic target projects use `<type>: <summary>`, while this agent-loop repository keeps version-scoped Chinese summaries.

### Helper Adapter Coverage
- Strengthened Superpowers adapter routing so available helper skills are preferred as stage methods while agent-loop keeps artifact paths, gates, task status, project memory, submit, and close control.
- Completed Stage Helper Capability Scan coverage for Product Brief, Brainstorm / Clarify, Feature Spec, Diagnose, Verify, Review, Feature Completion Check, Submit / Integrate, Pause / Close, and approved Subagent Execution.
- Added checklist-level validation so stage guides and workflow checklists stay aligned.

### Runtime And Documentation Alignment
- Strengthened runtime Agent Ownership so every response classifies state, recommends one next action, and avoids ending action reports with only “done”.
- Aligned design/runtime entry scenarios and main flow for Project Onboarding Scan, Feature Follow-up / Flow-back, active feature continuation, blocked state, and stale-memory re-adoption.
- Rewrote `Usage.md` as a Chinese human-facing guide focused on what humans can say to trigger agent-loop capabilities.

## 1.2.0 — 2026-06-07

### Existing-Project Onboarding
- Added Project Onboarding Scan as a formal capability with Quick, Deep, and Targeted modes.
- Added onboarding memory integrity checks so `project.md`, root guidance, and onboarding-db claims are verified before reliance.
- Added `references/project-onboarding-scan.md`, `references/onboarding-db.md`, `references/onboarding-db-templates.md`, and core `templates/onboarding-db/*` templates.
- Added Compact/Standard/Expanded layout rules, module/flow/data-model templates, deployment placement, subagent scan synthesis, Batch Human Review, and completion criteria.
- Added role-based README reading paths, bilingual glossary fields, guided newcomer onboarding, and targeted explanation/diagram update flows.

### Onboarding Diagrams And Domain Docs
- Added module call-chain requirements, flowchart-first diagrams, module-level call chains, sequence diagrams for async/external flows, data-model documentation, entity details, boundary maps, directory maps, state-flow docs, and state-trace docs.
- Changed onboarding-db documents to default to Chinese while preserving code symbols, file paths, commands, API names, and artifact names.
- Changed complex flows to split into `flows/<flow>.md` when cross-module, async, stateful, failure-prone, or repeatedly maintained.

### Root Bootstrap And Gates
- Added Root Agent Bootstrap Gate rules so root `AGENTS.md` is treated as the startup node for ownership, gate modes, stops, completion rules, artifact boundaries, and directory guidance.
- Changed `templates/root-AGENTS.md` into an Agent Loop Bootstrap protocol.
- Added Plan Gate rules so agents cannot create tasks and immediately execute without an accepted plan or recorded No-Plan Decision for trivial work.
- Hardened Task Auto-Run so it always requires an accepted task/story plan.

### Submit, Contracts, And Repository Rules
- Hardened Submit / Integrate so known drift still requires a minimum recorded Drift Check before submit.
- Changed Submit / Integrate commit guidance so meaningful commits are not described as one-line concise messages by default.
- Added this repository’s commit message rules requiring type + version scope, Chinese-first summaries, and multi-line bodies for meaningful changes.

### Validation And Examples
- Added validation scenarios for Quick/Deep/Targeted onboarding, missing onboarding memory, P0/P1/P2 scan ordering, module reading paths, layout decisions, subagent conflict synthesis, deployment fact placement, root guidance staleness, duplicated/divergent `CLAUDE.md`, and Batch Human Review.
- Added a v1.3.0 self-test harness proposal extension for real-project sampling and the `examples/ai-meeting-minutes-backend/` validation output container.

## 1.1.1 — 2026-06-04

### Memory Path Migration
- Changed the default target-project memory root from visible `agent-loop/` to hidden `.agent-loop/`.
- Kept visible `agent-loop/` as legacy-compatible memory that agents must read for the current run and migrate only after human confirmation.
- Updated generated root guidance, runtime rules, usage docs, templates, examples, and validation scenarios to prefer `.agent-loop/`.
- Preserved skill installation paths such as `~/.codex/skills/agent-loop/`.

## 1.1.0 — 2026-06-03

### External Skill Adapters
- Added `references/external-skill-adapters.md` to define Superpowers and external skill adapter rules.
- Added path override rules so external skill outputs are written to agent-loop artifacts instead of external default directories.
- Added gate override rules so external skills cannot bypass human gates, task status rules, feature close, submit, project memory, or Delivery Contract controls.
- Connected Superpowers adapters to Brainstorm / Clarify, Plan If Needed, Execute Task / Story, Diagnose Failure, Verify, Review, Submit / Integrate, and approved subagent execution.
- Added explicit Submit / Integrate adapter rules so external finishing skills cannot bypass diff inspection, verification, review, drift check, project memory status, or final human confirmation.

### Subagents And Human Gates
- Added Subagent Execution If Approved as a formal stage with workflow checklist and validation coverage.
- Hardened `templates/subagent-brief.md` so dispatched subagents cannot submit, update project memory/guidance directly, accept Delivery Contracts, approve breaking changes, or mark tasks `done`.
- Clarified that Feature Auto-Loop and Task Auto-Run do not imply subagent approval; bounded task-group approval requires explicit scope, boundaries, briefs, stop conditions, and main-agent review responsibility.
- Aligned autonomous execution stop conditions across README, Usage, project guidance, generated root guidance, and validation scenarios.

### Root Guidance And Legacy Memory
- Added legacy `agent-loop/` lookup and active-memory-root guidance to generated root `AGENTS.md`.
- Aligned Usage, README, stage guides, and workflow checklists with legacy `agent-loop/`, Product Brief ordering, Project Memory before Submit, and requirement-date semantics.
- Clarified that an empty local directory alone is not a remote-project signal; Remote Project Discovery now requires a remote-entry hint.
- Clarified that existing codebases with no agent-loop memory route through Existing Project Onboarding before recovery/backfill.

### Validation
- Added validation scenarios for Superpowers brainstorming and writing-plans path override, TDD with Task Done Gate, subagent approval, feature close, project memory update, Delivery Contract acceptance, release/publish actions, review-vs-done, subagent-return merge review, Feature Auto-Loop stops, Delivery Contract stops, and submit/close/release stops.
- Marked the Superpowers adapter proposal as implemented and documented external skill adapter behavior in README and Usage.

## 1.0.2 — 2026-06-03

### Release Branches
- Added the stable release branch naming rule: stable release branches use exact version names such as `v1.0.2`, not `release/1.0.2`.

## 1.0.1 — 2026-06-03

### Design Source Alignment
- Corrected the misspelled design source filename to `draft_agent_loop_struct.md`.
- Aligned `runtime.md` Stage Order and `design.md` Main Flow.
- Added `Re-Adopt Agent Loop Project if Needed` and `Targeted Feature Scan if Needed` to the design/runtime flow.
- Unified `Brainstorm` and `Clarify` into `Brainstorm / Clarify if Needed`.

### Repository Maintenance
- Added `AGENTS.md` and `CLAUDE.md` for skill repository maintenance guidance.
- Added a draft proposal for using Superpowers as agent-loop stage plugins without changing agent-loop artifact paths, gates, or task/feature ownership.

## 1.0.0 — 2026-06-02

### Delivery Contracts
- Added durable Delivery Contracts (`contracts.md` plus optional `contracts/`) for API, Service, Event, Async Workflow, Data, UI Behavior, Library, and Runtime boundaries.
- Added Contract Optionality: human confirmation is required before creating/updating contract files; simple single-person tasks and pure internal logic skip contracts by default.

### Gate Hardening
- Narrowed workflow bypass to one-off edits that do not affect feature behavior, interfaces, security boundaries, project memory, or submit/close state.
- Made minimum re-adoption reconciliation non-bypassable.
- Added two-stage submit confirmation: request, then diff/review/drift summary, then final approval.
- Required tasks missing applicable verification to remain `in-progress` or `blocked`; they cannot advance to `review` or `done`.

### Remote Project Routing And Verification
- Changed Remote Project Routing so an empty local directory alone no longer proves a remote project; human statement or remote-entry hint is required.
- Defined when API/integration and E2E/browser verification are applicable, including recorded reason, substitute proof, and risk for substitute verification.

### Re-Adoption And Enterprise Memory
- Added minimum safe reconciliation for stale projects: commands, tests, baseline failures, active feature state, boundaries, and conflicts.
- Added optional bounded subagent scanning for large/stale re-adoption.
- Added Enterprise Project Memory Mode with `project.md` as entry index and optional details under `.agent-loop/project/`.

### Templates, Examples, And Validation
- Added `templates/contracts.md`, `templates/delivery-contract.md`, `references/delivery-contracts.md`, and the complex SaaS example.
- Added validation scenarios for new-project init, stale re-adoption, contract breaking changes, Feature Auto-Loop, duplicate scenario numbering, and contract file skipping rules.
- Replaced `inputs/` with canonical `requirements/` in design sources.
- Aligned lifecycle around `Execute → Verify → Review → Drift Check`.

---

## Maintenance Rule

1. Add entries under the target version, not as a loose dated log.
2. Group entries by behavior area, gate, artifact, template, validation, or documentation theme.
3. Summarize behavior changes first; mention edited files only when the file itself is the user-visible artifact.
4. Record new human gates, artifact path changes, templates, examples, and validation scenarios.

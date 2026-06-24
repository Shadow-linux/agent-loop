# Agent Loop Changelog

## 1.2.3 — 2026-06-19

### Requirement Lifecycle / Backlog
- Added requirement lifecycle/backlog rules so future or deferred work is captured in requirement sets and optional `requirements/INDEX.md`, not in `project.md`.
- Extended requirement set README and requirements index templates with lifecycle, backlog/deferred, in-progress, implemented, superseded, and rejected views while keeping source files free-form.
- Added backward compatibility rules for old requirement set README files and immutable-source rules so `requirement.md` is not rewritten for lifecycle/status updates.
- Added Requirement Conflict Review for large follow-up conflicts that should create a new requirement set or supersede the old one after human confirmation.
- Clarified Targeted Onboarding output, Feature Completion blocked handling, and Feature Follow-up priority behind Project Entry when agent-loop memory is missing.
- Added Message Intent classification for `chat` and `requirements-discussion` so ordinary discussion stays answer-only, while requirements discussion goes through Brainstorm / Clarify into human-reviewed requirement documents under `.agent-loop/requirements/` before feature construction.
- Clarified that features derive `product.md` / `spec.md` from requirement sets but never own requirement source or lifecycle.

### Root Guidance Skill Re-entry
- Added Skill Re-entry Rule so root `AGENTS.md` is treated as a bootstrap cache, not a replacement for the `agent-loop` skill.
- Required agents to load/use the available `agent-loop` skill during Project Entry, Resume, Re-Adopt, stage boundaries, after context compaction, long-running sessions, or workflow uncertainty.
- Added fallback reporting for unavailable/load-failed skill resolution and validation coverage for long-running agents that try to continue from memory or static root guidance alone.
- Clarified that Stage Helper Capability Scan does not satisfy Skill Re-entry because helper scan resolves stage methods, not the `agent-loop` controller.
- Added per-managed-block `block-version` metadata and root AGENTS refresh protocol so same-version templates can still detect missing or stale managed blocks.
- Shortened the Managed Block Rule in root AGENTS guidance while preserving confirmation, outside-content protection, and cleanup / migration review requirements.
- Clarified that target-project AGENTS refreshes must copy the full template block revision, such as `block-version:1.2.3-20260625`; bare skill-version-only values like `block-version:1.2.3` are stale.

### Medium Consistency Fixes
- Clarified Auto Mode stop conditions for Delivery Contract creation, acceptance, and breaking changes across runtime guidance.
- Added routing priority for `remote-entry` before `existing-project`, single-next-stage blocked routing, and no-direct-close Drift Check exits.
- Added explicit helper scan coverage for Work Breakdown, Test Design, E2E Discovery, and Technical Design / Code Context.
- Added onboarding mode recording and guided-onboarding fallback routing when onboarding-db is missing.
- Aligned Standards Review triggers across Task Done Gate, Review, Feature Completion Check, and workflow checklists.

### Complex Artifact Thresholds
- Replaced hard Complex Artifact recommendation thresholds with a simpler assessment model: stories > 3 pauses for assessment, but does not itself recommend Complex Artifact Mode.
- Defined Complex Artifact Mode by "牵一发而动全身" semantics: recommend only when a feature cannot be safely understood, planned, or verified as one cohesive change because it spans collaborating modules, services, workflows, ownership lanes, or release/operation concerns.
- Clarified that story count, task count, test count, and ordinary file/module count are assessment signals only, not sufficient recommendation triggers.
- Aligned large-project guidance and stage write rules so Complex Mode assessment does not auto-materialize detail directories; `tasks/`, `tests/`, and `plans/` details are created only where needed after confirmation.
- Preserved human confirmation before creating complex detail directories and updated threshold-boundary validation coverage around semantic complexity.
- Added explicit Feature Auto-Loop stop condition for Complex Artifact Mode detail directory creation so `tasks/`, `tests/`, and `plans/` directories cannot be auto-created without human confirmation.

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

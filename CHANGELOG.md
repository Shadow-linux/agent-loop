# Agent Loop Changelog

## 1.2.1 — 2026-06-11

### Added
- Added Feature Follow-up / Flow-back rules so bugs, regressions, post-close corrections, field/schema changes, algorithm changes, API mismatches, test failures, and QA/user feedback are matched against recent features before creating a new feature.
- Added a default 30-day recent-feature lookback, Candidate Match Matrix, flow-back rules for reopening or continuing owning features, Follow-up Intake notes record, and validation scenarios for post-close bug flow-back, linked new feature routing, unclear ownership investigation, error screenshot routing, and requirement-change flow-back.
- Added `Feature Type: maintenance-fix` as the formal container for narrow bugfixes/internal corrections with no owning recent feature, including spec fields, feature workspace rules, project-memory impact checks, and validation scenarios.
- Added Discovery Coverage Matrix rules so Expanded Deep Onboarding Scan cannot stop after only the minimum 10 files; every discovered core module, complex flow, data model, complex entity, async/job path, deployment concern, verification system, and high-risk unknown must be documented or explicitly deferred.
- Added a concrete managed block detection checklist for root `AGENTS.md` marker validation, including source checks and stale-marker handling.
- Added `agent-loop:managed-start` / `agent-loop:managed-end` block rules for root `AGENTS.md`, including bootstrap, ownership, gates, completion, artifacts, architecture, commands, and hard-constraints sections.
- Added validation scenarios to prevent whole-file `AGENTS.md` overwrites and to stop on broken or duplicated managed block markers.
- Added Feature Follow-up pressure scenarios for generic 500/blank-page reports, day-31 extended scans, ambiguous "small" requirement changes, and declined reopen continuity.
- Added root guidance bootstrap rules and validation so bug reports, regressions, screenshots, and small changes route through Feature Follow-up / Flow-back before new feature creation or code edits.
- Added root Submit And Commit Rules guidance plus validation so target projects inherit explicit submit gates and fallback commit message format.
- Added an independent Analyze Consistency validation scenario so accepted plans cannot jump directly into implementation without spec/tasks/tests/plan mapping checks.
- Added Analyze Consistency checklist and `notes.md` recording fields so plan/spec/tasks/tests/code-reality mapping has an explicit artifact before execution.
- Added Stage Helper Capability Scan so agents actively detect available helpers such as Superpowers before falling back during Plan Gate, Execute, Diagnose, Verify, Review, Submit, and related stages.
- Added mandatory sequence diagram requirement for core modules with async jobs, external APIs, callbacks, WebSocket, retry/compensation, or multi-service interactions.
- Added `Model Usage Flow Map` to `templates/onboarding-db/data-model.md` to show which flows/APIs/jobs interact with which entities.
- Added `Entity Lifecycle Flow Map` to `templates/onboarding-db/entity-template.md` to visualize who creates/reads/updates/deletes an entity.
- Added unified diagram style guide in `templates/onboarding-db/diagram.md` covering flowchart layers, color classes, node shapes, arrow types, naming conventions, and sequence diagram participant/message/branch standards.
- Added diagram coverage check to Batch Review Template in `references/onboarding-db-templates.md`.
- Added "How To Read" as a mandatory requirement for every diagram.
- Added "Step-by-Step Walkthrough" as a mandatory requirement for every onboarding diagram alongside "How To Read", with examples in all diagram-bearing templates.
- Added Expanded Minimum Required Set (10 mandatory files) and Expanded Conditional Files trigger table to `references/project-onboarding-scan.md`.
- Added validation scenario `2h-19` requiring Step-by-Step Walkthrough for diagram completeness.
- Added Step-by-Step Walkthrough sections to all diagram-bearing templates: module, flow, data-model, entity, state-flow, boundary, module-map, deployment, architecture, change-impact, flows-and-data, overview.
- Added Diagram Expansion Matrix rules and validation so complex Deep Onboarding projects produce additional focused module, flow, state, async/job, data, and deployment diagrams as complexity increases.
- Added onboarding next-action rules so guided onboarding answers recommend a concrete next reading path, focused diagram update, setup/verification action, or return to feature development.

### Changed
- Strengthened runtime Agent Ownership so every response must classify state, recommend exactly one next action, and avoid ending action reports with only "done".
- Strengthened feature follow-up matching to extract evidence from screenshots, UI labels, logs, stack traces, API fields, and failing test names before deciding whether to reopen a recent feature.
- Strengthened feature follow-up routing so 30 days is a default scan window rather than a hard cutoff, low-information errors route to investigate-first, ambiguous requirement changes require scope classification, and declined reopen still preserves related-feature continuity.
- Aligned flow-back decision terminology across templates, checklists, stage guides, and validation scenarios so `flow-back` is the recorded decision for reopening or continuing an owning feature.
- Corrected Submit / Integrate commit-message guidance so generic target projects use `<type>: <summary>`, while `agent-loop` repository commits keep the version-scoped Chinese format.
- Strengthened root guidance stale detection and submit rules for Feature Follow-up / Flow-back, Submit And Commit Rules, intended-file commits, and commit-hash recording.
- Strengthened Superpowers adapter routing so available helper skills are preferred as stage methods while agent-loop keeps artifact paths, gates, task status, project memory, submit, and close control.
- Aligned `design.md` entry scenarios and main flow with runtime for Project Onboarding Scan, Feature Follow-up / Flow-back, active feature continuation, blocked state, and stale-memory/re-adopt routing.
- Aligned first-version exclusions and auto-mode stop conditions across `SKILL.md`, runtime, concepts, root guidance, README, Usage, and validation scenarios.
- Clarified that Expanded onboarding-db minimum files are a floor, not a cap, and added completion checks for discovery-driven module/flow/data/async/deployment coverage.
- Unified Expanded onboarding-db runtime/environment routing so env/config belongs in `setup-and-run.md`, while standalone `environment.md` is reserved for Compact/Standard or existing layouts.
- Unified standalone diagram rules so deployment and other diagrams are embedded in target docs by default and moved to `diagrams/` only when reused or too large.
- Completed `How To Read` examples for diagram-bearing onboarding templates that already had walkthroughs.
- Clarified README and Usage expectations for Expanded onboarding-db minimum coverage, discovery-triggered docs, embedded diagrams, and diagram walkthrough text.
- Clarified that `domain/entities/<entity>.md` is an allowed onboarding-db depth exception for complex data-model entity details.
- Rewrote `Usage.md` as a Chinese human-facing guide focused on what humans can say to trigger agent-loop capabilities.
- Clarified human-facing onboarding guidance in `Usage.md`, including Quick/Deep/Targeted choices, Expanded onboarding-db default, Batch Human Review, and root `AGENTS.md` managed blocks.
- Changed Deep Project Onboarding Scan to default to Expanded Onboarding DB Layout Mode; Compact and Standard are now reserved for explicit human requests or existing onboarding-db preservation.
- Hardened `references/project-onboarding-scan.md` Diagram Rules: Deep Scan diagrams must be complete, not "small diagrams that answer one question".
- Removed "Do not draw every function call" restriction from module call-chain diagrams; Deep Scan requires Service/UseCase/Domain/Repository/External-level detail.
- Removed "Do not draw a full database ERD unless very small" restriction from data-model diagrams; Deep Scan requires complete ERD with all core entities, key fields, and relationships.
- Tightened Completion Criteria so core modules must have diagrams (text-only fallback removed), sequence diagrams are mandatory for async/external modules, and all diagrams require "How To Read" notes.
- Updated `templates/onboarding-db/module-template.md` with complete call-chain flowchart example and mandatory sequence diagram section with Mermaid template.
- Updated Minimum Completion Standard in `references/onboarding-db-templates.md` to require model usage flow maps and sequence diagrams for async/external interactions.
- Demoted `maps/change-impact-map.md`, `domain/glossary.md`, `runtime/environment.md`, and `diagrams/` directory from mandatory to conditional based on project triggers.
- Restored `overview.md` as mandatory in Expanded minimum set.
- Updated `Deployment Placement` to merge environment variables into `setup-and-run.md` instead of standalone `environment.md` in Expanded layout.

## 1.2.0 — 2026-06-07

### Added
- Added Project Onboarding Scan as a formal existing-project onboarding capability with Quick, Deep, and Targeted modes.
- Added a v1.3.0 self-test harness proposal extension for real-project sampling where source code remains read-only and candidate onboarding outputs are written under `examples/<project-name>/`.
- Added `examples/ai-meeting-minutes-backend/` as the designated output container for validating onboarding behavior against the real ai-meeting-minutes-backend project without copying source code.
- Added onboarding memory integrity rules so `project.md` / root guidance claims about onboarding-db must be checked before reliance.
- Added a validation scenario for projects whose memory points newcomers to a missing `.agent-loop/onboarding-db/README.md`.
- Added `references/project-onboarding-scan.md` for Deep/Targeted scan rules, P0/P1/P2 scan priority, Layout Mode, diagrams, deployment placement, subagent scan synthesis, and completion criteria.
- Added `references/onboarding-db.md` for onboarding-db reading, writing, freshness, problem routing, learning, and project memory backfill rules.
- Added `references/onboarding-db-templates.md` for onboarding-db metadata, Compact/Standard/Expanded layout mapping, module cards, deployment, decision history, diagram, and batch review templates.
- Added core `templates/onboarding-db/*` templates for newcomer-readable project onboarding documents.
- Added validation scenarios for Quick/Deep/Targeted onboarding, P0/P1/P2 ordering, module reading paths, subagent conflict synthesis, deployment fact placement, and Batch Human Review.
- Added a core-module call-chain requirement so Deep Project Onboarding Scan must document a module-level call chain for each core module or explicitly mark it support-only, unknown, or not applicable with evidence.
- Added copy-ready `module-template.md` and `flow-template.md` for Expanded onboarding layouts.
- Added Standard and Expanded onboarding-db derivation rules so split documents stay executable without reintroducing dozens of templates.
- Added validation scenarios for Standard split-file derivation and Expanded module/flow template usage.
- Added onboarding layout pressure scenarios for mode selection, Compact merged-doc quality, Standard template restraint, human layout override, Compact-to-Standard upgrade, and Expanded durable-boundary / complex-flow / deployment-concern splitting.
- Added Guided Newcomer Onboarding rules for using an existing onboarding-db to lead a human through project takeover instead of dumping documents.
- Added On-Demand Explanation and Diagram Update rules for targeted call-path, async/job, flow, deployment, state, and boundary questions.
- Added validation scenarios for newcomer guided takeover and targeted diagram updates after onboarding-db exists.
- Added `references/onboarding-diagnostics.md` for startup failure diagnosis, change impact analysis, state-change trace, and design decision routing.
- Added onboarding validation scenarios for async/job reading paths, startup failure diagnosis, design decision routing, state-change trace, and centralized change impact analysis.
- Added role-based README reading paths and bilingual glossary fields to onboarding-db templates.
- Tightened Change Impact Analysis output fields and aligned glossary derivation with the bilingual glossary template.
- Added a standalone onboarding-db `glossary.md` template and aligned proposal glossary fields with bilingual terminology rules.
- Added root `CLAUDE.md` pointer template and validation coverage so onboarded projects keep `AGENTS.md` as the primary maintained startup guidance.
- Added Plan Gate rules so agents cannot create tasks and immediately execute without either an accepted plan or a recorded No-Plan Decision for a trivial task.
- Added categorized onboarding-db support with `maps/`, `modules/`, `flows/`, `runtime/`, `domain/`, and `quality/` layout rules for Standard/Expanded onboarding.
- Added `templates/onboarding-db/module-map.md` and upgraded onboarding templates to capture module-detail docs, human-readable flow docs, and concrete Evidence Chain tables.
- Added onboarding validation scenarios for module-map-as-index, human-readable flow quality, concrete evidence chains, and targeted diagram updates.
- Added `agent-loop` repository commit message rules requiring type + version scope, Chinese-first summaries, and multi-line bodies for meaningful changes.
- Added first-class onboarding data-model rules so persistent entities, storage mapping, relationships, ownership, fields, writers/readers, migrations, tests, and evidence cannot be hidden only inside flow docs.
- Added `templates/onboarding-db/data-model.md` and `templates/onboarding-db/entity-template.md` for data-model indexes and complex entity detail docs.
- Added onboarding validation scenarios for missing data-model docs and complex entity split behavior.
- Added focused onboarding templates for boundary maps, directory maps, change-impact maps, state-flow docs, and state-trace docs.
- Added onboarding validation scenarios for complex flow splitting and Chinese-default onboarding-db output.
- Added Root Agent Bootstrap Gate rules so `AGENTS.md` is treated as the startup node for agent-loop ownership, gate modes, stops, and completion rules.
- Added validation scenarios for stale root `AGENTS.md` bootstrap guidance and duplicated/divergent `CLAUDE.md` guidance.
- Added flowchart-first onboarding diagram rules and validation so sequence diagrams are reserved for narrow detail views after process/module flowcharts exist.

### Changed
- Wired existing project onboarding to explain Quick / Deep / Targeted onboarding modes before writing onboarding-db artifacts.
- Expanded Human Review Summary with Batch Human Review for multi-document, multi-fact, and long-term-memory changes.
- Updated runtime and stage routing so onboarding-db is loaded only when Deep/Targeted onboarding or onboarding-db read/write/refresh is needed.
- Aligned version metadata across `SKILL.md`, `README.md`, `Usage.md`, `plugin.json`, and the changelog.
- Hardened Submit / Integrate so known drift still requires a minimum recorded Drift Check before submit.
- Clarified Existing Project Onboarding write targets, explicit re-adoption routing, and Guided Newcomer Onboarding entry from an existing onboarding-db.
- Clarified Layout Mode decision rules and anti-misuse rules for Compact, Standard, Expanded, human overrides, and layout upgrades.
- Hardened Existing Project Onboarding so root `AGENTS.md` / `CLAUDE.md` status must be present, created, or explicitly deferred before onboarding can be considered complete.
- Hardened Task Auto-Run so it always requires an accepted task/story plan.
- Changed onboarding routing and templates so categorized onboarding-db docs are first-class, while Compact mode may still use merged docs when README maps the content clearly.
- Changed module and flow documentation quality bars to require stronger human-readable structure and concrete evidence paths for key claims.
- Changed Submit / Integrate commit guidance so meaningful commits are not described as one-line concise messages by default.
- Changed onboarding README requirements and template to include a data-model reading path when persistent data exists.
- Changed onboarding-db human-readable documents to default to Chinese while keeping code symbols, file paths, commands, API names, and artifact names as-is.
- Changed complex flow handling so cross-module, async, stateful, failure-prone, or repeatedly maintained flows are split into `flows/<flow>.md` instead of remaining only as merged summary rows.
- Changed `templates/root-AGENTS.md` into an Agent Loop Bootstrap protocol with explicit Agent Ownership, Gate Modes, Required Stops, Completion Rules, artifact boundaries, and directory guidance rules.
- Changed onboarding diagram templates to prefer colored layered Mermaid flowcharts for project, module, flow, and boundary understanding.

## 1.1.1 — 2026-06-04

### Changed
- Changed the default target-project memory root from visible `agent-loop/` to hidden `.agent-loop/`.
- Kept visible `agent-loop/` as legacy-compatible memory that agents must read for the current run and migrate only after human confirmation.
- Updated generated root guidance, runtime rules, usage docs, templates, examples, and validation scenarios to prefer `.agent-loop/`.
- Preserved skill installation paths such as `~/.codex/skills/agent-loop/`.

## 1.1.0 — 2026-06-03

### Added
- Added `references/external-skill-adapters.md` to define Superpowers and external skill adapter rules.
- Added path override rules so external skill outputs are written to agent-loop artifacts instead of external default directories.
- Added gate override rules so external skills cannot bypass human gates, task status rules, feature close, submit, project memory, or Delivery Contract controls.
- Connected Superpowers adapters to Brainstorm / Clarify, Plan If Needed, Execute Task / Story, Diagnose Failure, Verify, Review, Submit / Integrate, and subagent execution.
- Added validation scenarios for Superpowers brainstorming path override, writing-plans path override, TDD with Task Done Gate, and subagent approval.
- Added Subagent Execution If Approved as a formal stage with workflow checklist and validation coverage.
- Added explicit Submit / Integrate adapter rules so external finishing skills cannot bypass diff inspection, verification, review, drift check, project memory status, or final human confirmation.
- Added external skill checklist coverage and path-pressure validation for native Superpowers output requests.
- Added second-confirmation requirements before creating native external skill directories such as `docs/superpowers/*`.
- Added Superpowers pressure scenarios for feature close, project memory update, Delivery Contract acceptance, and release/publish actions.
- Aligned Usage, README, stage guides, and workflow checklists with legacy `agent-loop/`, Product Brief ordering, Project Memory before Submit, and requirement-date semantics.
- Hardened `templates/subagent-brief.md` so dispatched subagents cannot submit, update project memory or guidance directly, accept Delivery Contracts, approve breaking changes, or mark tasks `done`.
- Clarified that an empty local directory alone is not a remote-project signal; Remote Project Discovery now requires a remote-entry hint.
- Added legacy `agent-loop/` lookup and active-memory-root guidance to generated root `AGENTS.md`.
- Clarified that existing codebases with no agent-loop memory route through Existing Project Onboarding before recovery/backfill.
- Resolved the Superpowers adapter proposal open questions to match the implemented v1.1.0 adapter behavior.
- Clarified subagent dispatch confirmation: Feature Auto-Loop and Task Auto-Run do not imply subagent approval, and bounded task-group approval requires explicit scope, boundaries, briefs, stop conditions, and main-agent review responsibility.
- Added pressure scenarios for review-vs-done, subagent-return merge review, Feature Auto-Loop Human-gated stop, Delivery Contract stop, and submit/close/release stop.
- Marked the Superpowers adapter proposal as implemented and documented external skill adapter behavior in README and Usage.
- Aligned autonomous execution stop conditions across README, Usage, project guidance, generated root guidance, and validation scenarios.
- Aligned top-level `SKILL.md` Stop And Ask gates with runtime hard stop conditions.

## 1.0.2 — 2026-06-03

### Added
- Added the stable release branch naming rule: stable release branches use exact version names such as `v1.0.2`, not `release/1.0.2`.

## 1.0.1 — 2026-06-03

### Fixed
- Corrected the misspelled design source filename to `draft_agent_loop_struct.md`.
- Aligned `runtime.md` Stage Order and `design.md` Main Flow.
- Added `Re-Adopt Agent Loop Project if Needed` to the design main flow.
- Added `Targeted Feature Scan if Needed` to the design/runtime stage order before Feature Spec.
- Unified `Brainstorm` and `Clarify` into `Brainstorm / Clarify if Needed` in the main flow.

### Added
- Added `AGENTS.md` and `CLAUDE.md` for skill repository maintenance guidance.
- Added a draft proposal for using Superpowers as `agent-loop` stage plugins without changing agent-loop artifact paths, gates, or task/feature ownership.

## 1.0.0 — 2026-06-02

### Added
- **Delivery Contracts**: Durable producer-consumer contracts (`contracts.md` + optional `contracts/`) for API, Service, Event, Async Workflow, Data, UI Behavior, Library, and Runtime boundaries.
- **Contract Optionality**: Human confirmation required before creating/updating contract files. Simple single-person tasks and pure internal logic skip contracts by default.
- **v0.2 Gate Hardening**:
  - Narrowed workflow bypass to one-off edits that don't affect feature behavior, interfaces, security boundaries, project memory, or submit/close state.
  - Made minimum re-adoption reconciliation non-bypassable.
  - Added two-stage submit confirmation (request → diff/review/drift summary → final approval).
  - Tasks missing applicable verification stay `in-progress` or `blocked`; cannot advance to `review` or `done`.
- **Remote Project Routing**: Empty local directory alone no longer proves remote project; requires human statement or remote-entry hint.
- **Verification Rules**: Defined when API/integration and E2E/browser verification are applicable; required recorded reason, substitute proof, and risk for substitute verification.
- **Re-Adoption & Enterprise Memory**: Minimum safe reconciliation (commands, tests, baseline failures, active feature state, boundaries, conflicts) before continuing stale projects. Optional bounded subagent scanning for large/stale re-adoption.
- **Validation**: Added agent pressure tests for new-project init, stale re-adoption, contract breaking changes, and Feature Auto-Loop. Fixed duplicate scenario numbering.
- **Templates & Examples**: `templates/contracts.md`, `templates/delivery-contract.md`, `references/delivery-contracts.md`, and complex SaaS example (`examples/complex-saas-project/...`).

### Changed
- Replaced `inputs/` with canonical `requirements/` in design sources.
- Aligned lifecycle around `Execute → Verify → Review → Drift Check`.
- Updated README/Usage guidance for contract file skipping rules.

### Design Source Alignment
- Added Enterprise Project Memory Mode (`project.md` as entry index, optional details under `.agent-loop/project/`).
- Added `Delivery Contract if Needed` to design source and operational `design.md`.

---

## Maintenance Rule

1. Add dated entries at the top.
2. Summarize behavior changes, not just edited files.
3. List new human gates, artifact changes, templates, examples, and validation scenarios.

# Agent Loop Changelog

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
- Aligned Usage, README, stage guides, and workflow checklists with legacy `.agent-loop/`, Product Brief ordering, Project Memory before Submit, and requirement-date semantics.
- Hardened `templates/subagent-brief.md` so dispatched subagents cannot submit, update project memory or guidance directly, accept Delivery Contracts, approve breaking changes, or mark tasks `done`.
- Clarified that an empty local directory alone is not a remote-project signal; Remote Project Discovery now requires a remote-entry hint.
- Added legacy `.agent-loop/` lookup and active-memory-root guidance to generated root `AGENTS.md`.
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
- Added Enterprise Project Memory Mode (`project.md` as entry index, optional details under `agent-loop/project/`).
- Added `Delivery Contract if Needed` to design source and operational `design.md`.

---

## Maintenance Rule

1. Add dated entries at the top.
2. Summarize behavior changes, not just edited files.
3. List new human gates, artifact changes, templates, examples, and validation scenarios.

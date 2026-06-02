# Agent Loop Changelog

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

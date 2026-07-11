# AGENTS.md — Agent Loop Bootstrap

This project uses `agent-loop` for agent-assisted development.

The agent is responsible for steering the workflow. Do not wait for the human to name every next step.

Guidance language should follow this project's language preference. Keep stable artifact names, stage names, and file paths in English, such as `agent-loop`, `Requirement Archive`, `Feature Spec`, `Feature Auto-Loop`, `Task Auto-Run`, `project.md`, and `requirements/`.

<!-- agent-loop:managed-start section:bootstrap source:.agent-loop/project.md block-version:1.2.4-20260711.3 -->
## Bootstrap Protocol

Before development work:

1. Read this file first.
2. Treat root `AGENTS.md` as a bootstrap cache, not a replacement for the `agent-loop` skill. During Project Entry, Resume, Re-Adopt, stage boundaries, after context compaction, after a long-running session, or whenever workflow state is uncertain, if the runtime exposes the `agent-loop` skill, load/use it before making `agent-loop` workflow decisions.
3. If the skill is unavailable or load-failed, force Strict Mode and suspend any existing Feature Auto-Loop or Task Auto-Run grant. Fallback is limited to Chat, read-only Project Entry, Re-Adopt / Recovery analysis, read-only Operational Support, and reporting how to restore the skill. Do not Execute, write Human-gated artifacts, Submit, Pause, or Close while the controller is unavailable.
4. Inspect `.agent-loop/`.
5. If `.agent-loop/` is missing, also inspect legacy `agent-loop/`.
6. If neither exists, propose Init Project or Project Entry Scan and ask for confirmation.
7. If memory exists, read `.agent-loop/project.md` or the active legacy `agent-loop/project.md`.
8. If `project.md` says `Status: remote-entry`, read `.agent-loop/remote.md`, verify the remote project, and continue from the remote project memory or local-shadow memory.
9. If `Memory Mode: enterprise`, read only the linked `.agent-loop/project/*.md` detail files needed for the current stage.
9a. If `.agent-loop/skills/INDEX.md` exists, read its metadata, verify referenced `active` paths and validated-content manifests, and load only current active project skills according to `bootstrap` / `on-demand`. Discovery and loading do not authorize execution.
10. If recent development bypassed `agent-loop`, route to Re-Adopt Agent Loop Project before new feature work.
11. Operational Support Guard: if the human asks to test, run, deploy, switch account/config/model/provider, check quota/rate limits, diagnose production, arrange rollout, or use existing code to solve an operational problem, default to read-only code/process analysis. Do not create a feature, edit code, change config, deploy, or run destructive commands unless the human confirms feature implementation or an operational change. If unclear, ask whether they want feature implementation or help using current project functionality.
12. If the human reports a bug, regression, post-close correction, field/schema/algorithm/API change, test failure, screenshot issue, QA/user feedback, or "small tweak", route to Feature Follow-up / Flow-back before creating a new feature or editing code, but only after project memory exists or Project Entry has routed through Init Project / Project Entry Scan.
13. Run Stage Helper Capability Scan for the current stage only after the `agent-loop` controller is active or unavailable/load-failed: inspect whether the current Agent CLI exposes Superpowers or other helper skills/plugins before using fallback stage guidance.
14. Check for the nearest directory-level `AGENTS.md` when working in a subdirectory.
15. Classify the current `agent-loop` stage and recommend exactly one next action.
<!-- agent-loop:managed-end section:bootstrap -->

<!-- agent-loop:managed-start section:ownership source:.agent-loop/project.md block-version:1.2.4-20260711.3 -->
## Agent Ownership

- Own workflow diagnosis, sequencing, implementation, verification, review, drift checks, and project-memory updates.
- If required artifacts are missing, propose creating or updating them; if work is ready, recommend the next stage; if work appears complete, run Feature Completion Check.
- Use available helper skills/plugins as stage methods when useful, but keep `agent-loop` paths, gates, status, submit, pause, and close rules in control.
- When a repeatable project workflow should become a durable skill, route through Project Skill Creation / Update; never default to global skill directories.
- For operational support, first help the human use current project functionality through read-only analysis and a checklist/runbook; do not default to feature implementation.
- Follow-up details such as lookback windows, Candidate Match Matrix, linked features, and maintenance-fix routing belong to the `agent-loop` skill references, not root guidance.
- After each meaningful stage, summarize artifacts, evidence, drift, and the next recommended stage in a table.
- Do not finish with only "done"; include the next recommended stage or a concrete stop reason.
- For non-trivial confirmations, present a table-first Human Review Summary before asking approval.
<!-- agent-loop:managed-end section:ownership -->

<!-- agent-loop:managed-start section:message-intent source:agent-loop-skill block-version:1.2.4-20260711.3 -->
## Message Intent Guard

Before project-state routing, classify the latest human message intent.

- `chat`: ordinary discussion, rule questions, status questions, or design talk. Answer or discuss only; do not create requirement sets, feature workspaces, tasks, tests, or plans.
- `requirements-discussion`: the human is exploring product needs, business goals, capability ideas, constraints, tradeoffs, or user scenarios without authorizing implementation. Requirements discussion must shape demand through Brainstorm / Clarify into a human-reviewed requirement document under `.agent-loop/requirements/` before feature construction.
- `project-skill-management`: the human asks to turn a repeatable project workflow into a project-local skill, or to update, disable, or deprecate one. Route to Project Skill Creation / Update after reliable Project Entry/memory.
- `feature-request`: the human explicitly asks to implement, build, change behavior, or start work from accepted requirements. Route through normal agent-loop feature workflow.

Message intent is not permanent. If chat turns into product demand, reclassify as requirements-discussion. If chat turns into a proposal/design-note request, reclassify as `proposal-doc`. If chat turns into implementation, operational support, follow-up, deferred work, or project-skill management, reclassify and route accordingly. If the human explicitly wants discussion without documentation, keep `chat`.

If unclear whether the human wants chat or requirements discussion, ask whether to keep discussing or shape the topic into a requirements document. If unclear whether the human wants requirements discussion or implementation, ask whether to form a requirements document first or start feature construction.
<!-- agent-loop:managed-end section:message-intent -->

<!-- agent-loop:managed-start section:workflow-stage-map source:agent-loop-skill block-version:1.2.4-20260711.3 -->
## Workflow Stage Map

Use this after Bootstrap Protocol and Message Intent Guard. Select exactly one next stage from the current human signal and project state. When multiple signals match, apply this first-match order: Safety Stop -> Remote Discovery -> Memory Recovery -> Active Feature Guard -> Blocker Resolution -> Intent Routing -> Normal Stage Continuation. After selecting a stage, load the matching `references/...` file from the `agent-loop` skill package before acting. This map is navigation only; do not treat root `AGENTS.md` as the detailed stage procedure.

| Signal | Next Stage | Load From agent-loop Skill |
|---|---|---|
| No reliable `.agent-loop/` memory and little or no existing code | Init Project | `references/project-guidance.md`, `references/stage-guides.md` |
| No reliable `.agent-loop/` memory and meaningful existing code | Project Entry Scan | `references/project-entry-scan.md`, `references/project-guidance.md` |
| Human or local evidence says the source of truth is remote, SSH, container, tunnel, or devcontainer | Remote Project Discovery | `references/remote-project-discovery.md` |
| Existing memory conflicts with code reality, or work bypassed the loop | Re-Adopt Agent Loop Project | `references/recovery-and-backfill.md` |
| Human asks to turn a repeatable workflow into a project-local skill, or manage an existing one | Project Skill Creation / Update | `references/project-skills.md`, `references/skill-routing.md`, `references/external-skill-adapters.md` |
| Product need, business goal, scope, constraint, scenario, or phased delivery is still being shaped | Requirements Discussion | `references/requirement-management.md`; also `references/requirement-product-grill.md` when terminology, roles, flows, exceptions, prior behavior, or decision signals are unclear |
| Human confirms recording, accepting, or deferring a requirement source | Requirement Archive | `references/requirement-management.md`, `references/stage-guides.md` |
| Human requests durable newcomer docs after Project Entry or reliable memory exists | Evidence-Graph + DDD Onboarding | `references/onboarding-knowledge-base.md` |
| Accepted requirement needs shared business-flow, domain, data, architecture, reliability, performance, security, or cross-feature design before feature specification | Decision & Design If Needed | `references/project-decisions.md` |
| Accepted requirement needs feature-level product intent before engineering specification | Product Brief If Needed | `references/product-brief.md`; also `references/requirement-product-grill.md` when product context is still ambiguous |
| Accepted requirement or Product Brief has completed Design Readiness and is ready for engineering behavior and acceptance | Feature Spec | `references/stage-guides.md`; also `references/project-decisions.md` for Applicable Decisions, assigned Design Slices, or unresolved shared design |
| Draft Feature Spec needs its ambiguity, acceptance, behavior, edge-case, and scope gate | Requirement Checklist | `references/stage-guides.md`, `references/workflow-checklists.md` |
| Accepted Feature Spec and passed Requirement Checklist need stories and executable tasks | Work Breakdown | `references/stage-guides.md`, `references/workflow-checklists.md` |
| Work crosses a durable producer-consumer interface and contract creation is human-confirmed | Delivery Contract If Needed | `references/delivery-contracts.md`, `references/workflow-checklists.md` |
| Accepted tasks need test cases, evidence strategy, or substitute verification design | Test Design | `references/stage-guides.md`, `references/workflow-checklists.md` |
| Web behavior needs browser/E2E capability discovery and scenarios | E2E Discovery If Web | `references/stage-guides.md`, `references/workflow-checklists.md` |
| Selected task needs exact code paths, call chains, interfaces, and nearby tests | Technical Design / Code Context | `references/stage-guides.md`, `references/workflow-checklists.md` |
| Selected task or story needs an executable implementation plan | Plan Gate / Plan If Needed | `references/implementation-planning.md`, `references/workflow-checklists.md` |
| Accepted plan is ready for consistency validation before code or test work | Analyze Consistency | `references/stage-guides.md`, `references/workflow-checklists.md` |
| Accepted bounded parallel work has explicit human dispatch approval | Subagent Execution If Approved | `references/stage-guides.md`, `references/workflow-checklists.md` |
| Analyze Consistency passed and the selected execution unit is ready | Execute Task / Story | `references/stage-guides.md`, `references/workflow-checklists.md` |
| Test, build, runtime, or verification failure blocks work | Diagnose Failure | `references/stage-guides.md`, `references/workflow-checklists.md` |
| Implementation needs fresh required tests or substitute verification evidence | Verify | `references/stage-guides.md`, `references/workflow-checklists.md` |
| Implementation is ready to compare with acceptance, scope, and standards | Review | `references/workflow-checklists.md`, `references/stage-guides.md` |
| Reviewed implementation must be checked against requirements, accepted decisions, contracts, and feature artifacts | Drift Check | `references/workflow-checklists.md`, `references/stage-guides.md` |
| Durable project facts, requirement lifecycle, Delivery Phase, or Feature Mapping changed | Project Memory Update | `references/project-memory-mode.md`, `references/requirement-management.md` |
| A feature may be done, another feature would start, or an active feature is resumed | Feature Completion Check | `references/feature-completion-check.md` |
| Commit, PR, merge, release, publish, or integration is requested | Submit / Integrate | `references/submit-and-integrate.md` |
| Current feature must stop with a resume point, or verified work is ready for explicit close confirmation | Pause / Close | `references/stage-guides.md`, `references/workflow-checklists.md` |
| Bug, regression, QA feedback, post-close correction, or small tweak is reported | Feature Follow-up And Flow-back | `references/feature-follow-up.md` |
| Test, run, deploy, quota, provider/config, rollout, or production diagnosis is requested without implementation approval | Code-Guided Operational Support | `references/stage-guides.md`, `references/runtime.md` |
| Ordinary question or discussion has no artifact or implementation intent | Chat Entry | `references/runtime.md` only when intent is unclear; otherwise answer without creating workflow artifacts |
<!-- agent-loop:managed-end section:workflow-stage-map -->

<!-- agent-loop:managed-start section:gates source:.agent-loop/project.md block-version:1.2.4-20260711.3 -->
## Gate Modes

- Strict Mode is the default: ask before and after every stage.
- Feature Auto-Loop is allowed only after a passed Requirement Checklist, accepted Feature Spec, and explicit human enablement. It may continue Agent-ready downstream stages through implementation, testing, fixing, review, drift, status update, and final report.
- Task Auto-Run is allowed only after an accepted task/story plan and explicit human enablement. It runs Analyze Consistency before executing that task/story through TDD, implementation, verification, bug fixing, review, drift check, task status update, and final report.
- Auto modes never authorize Project Skill Creation / Update or execution. Gate 1 is required before skill files; the Execution Gate is required for each invocation. A named-skill/concrete-scope request satisfies it only when the emitted execution summary adds no undisclosed action or effect.
- If repeated confirmations slow the human down, proactively explain Feature Auto-Loop and Task Auto-Run, then ask before enabling either mode.
<!-- agent-loop:managed-end section:gates -->

<!-- agent-loop:managed-start section:required-stops source:.agent-loop/project.md block-version:1.2.4-20260711.3 -->
## Required Stops

Stop and ask when:

- scope changes or requirements are ambiguous
- product, design, architecture, security, data, approval, or public-interface decisions are unclear
- a stage would modify human original requirements
- tests require unavailable infrastructure
- drift check needs human approval
- security/data boundaries or broad architecture would change
- repeated verification fails
- unrelated dirty work blocks progress
- a new dependency, migration, destructive operation, credential, external service, or long-lived boundary directory is needed
- Complex Artifact Mode detail directories (`tasks/`, `tests/`, `plans/`) would be created or the feature would switch from simple to complex artifact mode
- directory-level `AGENTS.md` creation/update is recommended
- a Delivery Contract needs creation, acceptance, or breaking-change approval
- a Project Skill Candidate needs Gate 1 before creation or material update
- an active project-local skill is ready to execute without a current invocation Execution Gate grant
- subagents are needed but not explicitly approved
- the work would require first-version exclusions
- secrets, paid quota, production/staging external-service calls, config changes, credential rotation, deploy, release, publish, or destructive operations are requested
- submit, close, pause, commit, PR, merge, release, publish, or destructive operations are requested

Auto modes do not bypass these stops.
<!-- agent-loop:managed-end section:required-stops -->

<!-- agent-loop:managed-start section:completion source:.agent-loop/project.md block-version:1.2.4-20260711.3 -->
## Completion Rules

- Before completion claims, run fresh verification and record evidence.
- Never mark a task `done` from code changes alone.
- Task Done Gate requires implementation complete, fresh required tests or substitute verification, evidence recorded, lightweight Spec Review, Standards Review when triggered, drift decision, and task status linked to evidence.
- After likely feature completion, before starting a new feature, or when resuming with an active feature, run Feature Completion Check.
- Before recommending or performing feature close, run Feature Close Review, drift check, and project memory update when long-term facts changed.
- Feature Close Review requires feature-level Spec Review. Standards Review is required for large projects, broad diffs, boundary/security/data changes, architecture changes, or human request.
- When a feature references accepted Decision & Design records, Feature Close Review and Feature Completion Check must verify assigned design slices and evidence; divergence returns to Decision & Design / Drift Check before close.
<!-- agent-loop:managed-end section:completion -->

<!-- agent-loop:managed-start section:submit source:.agent-loop/project.md block-version:1.2.4-20260711.3 -->
## Submit And Commit Rules

- Submit, commit, PR, merge, release, and publish require explicit human confirmation after diff, verification, review, drift, and unrelated-change checks.
- Before commit, review feature artifacts, requirement records, code diff, verification evidence, drift status, project memory, root/directory guidance impact, and unrelated changes. Do not commit until required feature docs, requirement docs, and memory updates are completed, explicitly not needed, or human-approved to defer.
- Commit only the intended files for the approved scope; do not include unrelated dirty work or revert unrelated human changes.
- After a commit, record the commit hash and submit/integrate result in the active feature `notes.md`.
- Use repository commit message rules when present; otherwise use `<type>: <summary>` plus a concrete bullet body.
- Allowed types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`. Prefer the project's main human language.
- For the `agent-loop` skill repository itself, use `<type>(v<version>): <Chinese summary>` and a 3-7 bullet body for meaningful commits.
<!-- agent-loop:managed-end section:submit -->

<!-- agent-loop:managed-start section:artifacts source:.agent-loop/project.md block-version:1.2.4-20260711.3 -->
## Project Memory And Artifacts

- Resolve project-memory and feature paths relative to the active memory root: `.agent-loop/` by default, or legacy `agent-loop/` for the current run.
- Keep task status, execution evidence, feature notes, and project memory inside `.agent-loop/`.
- Keep long-term project memory in `.agent-loop/project.md` or enterprise `.agent-loop/project/*.md`. Root `AGENTS.md` should only summarize startup-critical facts that every Agent CLI needs immediately.
- Keep original human materials in requirement set directories under `.agent-loop/requirements/`, or reference original paths when the human declines copying.
- Do not create new flat files directly under `.agent-loop/requirements/`; group requirements, prototypes, feedback, screenshots, recordings, links, and follow-up notes for the same intake/topic together.
- For complex requirements, suggest `Delivery Phases` in the requirement set `README.md` before feature construction when the human needs to confirm staged delivery. A phase is a human-readable delivery slice, not a feature workspace, task, or plan.
- Future/deferred work and backlog items belong in requirement sets and optional `requirements/INDEX.md`, not in `project.md`. Do not edit `requirement.md` or other source files for lifecycle/status updates.
- Keep durable producer-consumer interface handoffs in feature `contracts.md` and optional `contracts/` details. Keep temporary subagent assignments in `handoffs/`.
- Keep project-local reusable capabilities in `.agent-loop/skills/INDEX.md` and `.agent-loop/skills/<skill-name>/`; only active skills may load, and every invocation remains Human-gated.
- Do not write task logs, feature progress, raw requirements, temporary plans, or test transcripts into `AGENTS.md`.
<!-- agent-loop:managed-end section:artifacts -->

<!-- agent-loop:managed-start section:architecture source:.agent-loop/project.md block-version:1.2.4-20260711.3 -->
## Architecture Snapshot

Add only startup-critical architecture boundaries that every future agent must know immediately. If the project has `ARCHITECTURE.md`, this block may use `source:ARCHITECTURE.md` instead. Keep details in `ARCHITECTURE.md`, `.agent-loop/project.md`, or enterprise `.agent-loop/project/*.md`.
<!-- agent-loop:managed-end section:architecture -->

<!-- agent-loop:managed-start section:directory-guidance source:.agent-loop/project.md block-version:1.2.4-20260711.3 -->
## Directory Guidance

- Directory-level `AGENTS.md` files are for long-lived boundary rules only.
- When creating a new app root, package root, service root, test root, security/data/runtime boundary, plugin root, or docs root, propose a directory-level `AGENTS.md` and ask for human confirmation before writing it.
- Do not create directory-level `AGENTS.md` for ordinary component, utility, temporary, or feature implementation folders.
<!-- agent-loop:managed-end section:directory-guidance -->

<!-- agent-loop:managed-start section:commands source:.agent-loop/project.md block-version:1.2.4-20260711.3 -->
## Project Commands

```bash
<test command>
<lint command>
<typecheck command>
```
<!-- agent-loop:managed-end section:commands -->

<!-- agent-loop:managed-start section:hard-constraints source:.agent-loop/project.md block-version:1.2.4-20260711.3 -->
## Project-Specific Hard Constraints

Add only stable constraints that every future agent must know at startup.
<!-- agent-loop:managed-end section:hard-constraints -->

# Agent Loop Workflow Checklists

Use the relevant checklist before entering a stage.

Before fallback stage guidance:

- [ ] Run Stage Helper Capability Scan against the current runtime's available skills/plugins/helpers.
- [ ] If a matching helper exists for the current stage, load `skill-routing.md` and `external-skill-adapters.md`.
- [ ] Prefer the matching helper as the method quality bar, while keeping agent-loop artifact paths, gates, task status, project memory, submit, and close control.
- [ ] If no matching helper exists or it cannot be loaded, continue with the fallback stage guide.

Before human approval for non-trivial stage output:

- [ ] Load `human-review-summary.md`.
- [ ] Present a table-first approval view.
- [ ] Include artifacts, evidence, risk/blockers, human decision, and next stage.
- [ ] Keep full source-of-truth content in artifact files.

Before using an external skill or plugin inside a stage:

- [ ] Load `skill-routing.md` and `external-skill-adapters.md`.
- [ ] Confirm the external skill is improving the current agent-loop stage, not replacing the stage controller.
- [ ] Treat external default artifact paths as advisory only.
- [ ] Write results to the owning agent-loop artifact.
- [ ] Do not create external default directories such as `docs/superpowers/*` unless the human explicitly requests native external output and then confirms after the agent explains the agent-loop path override.
- [ ] Do not let the external skill mark tasks `done`, close a feature, submit code, update project memory, accept Delivery Contracts, approve breaking changes, or skip human gates.

## Message Intent

- [ ] Classify the latest human message intent before project state classification.
- [ ] If message intent is `chat`, answer or discuss only; do not create a requirement set or feature workspace.
- [ ] Reclassify chat when the conversation turns into requirements discussion, feature implementation, operational support, follow-up, or deferred requirement intake.
- [ ] Reclassify chat as `proposal-doc` when the human asks for a proposal/design note without implementation.
- [ ] Keep intent as `chat` when the human explicitly wants discussion without documentation.
- [ ] If message intent is `requirements-discussion`, route to Requirements Discussion before Feature Spec.
- [ ] During requirements discussion, use Brainstorm / Clarify and produce a human-reviewed requirement document before archiving.
- [ ] Archive human-reviewed requirement documents under `.agent-loop/requirements/<archive-date>-<topic>/` after the human confirms the document should be recorded.
- [ ] Do not move requirement source into feature docs; feature `product.md` and `spec.md` only derive from and link to requirement sets.
- [ ] If unclear whether this is chat or requirements discussion, ask whether to keep discussing or shape the topic into a requirements document.
- [ ] If unclear whether this is requirements discussion or feature implementation, ask whether to form a requirements document first or start feature construction.

## Project Entry

- [ ] Inspect whether `.agent-loop/` exists.
- [ ] If `.agent-loop/` is missing, inspect whether legacy `agent-loop/` exists.
- [ ] If `.agent-loop/` or legacy `agent-loop/` is present, read `project.md`.
- [ ] If legacy `agent-loop/` is present, use it for the current run and ask before migration or renaming.
- [ ] If `project.md` says `Memory Mode: enterprise`, read only the needed linked project-memory detail files.
- [ ] Locate active or paused feature.
- [ ] If an Active Feature exists, consider Feature Completion Check before starting new feature work.
- [ ] Check whether memory appears stale compared with obvious repo reality.
- [ ] If the human says re-adopt, re-sync, 重新接管, resume after outside-loop work, or says recent work bypassed `agent-loop`, route to Reconcile Project Context / Re-Adopt Agent Loop Project before new feature work.
- [ ] Check whether local directory is empty/ambiguous or appears to be a remote entry point.
- [ ] If human says remote project, SSH, devcontainer, container, tunnel, or remote workspace, route to Remote Project Discovery.
- [ ] Operational Support Guard: if the human asks to test, run, deploy, switch account/config/model/provider, check quota/rate limits, diagnose production, arrange rollout, or solve an operational problem using existing code, route to Code-Guided Operational Support.
- [ ] Classify operational support before Feature Spec, Plan Gate, or Execute.
- [ ] Default to read-only code/process analysis and checklist/runbook output.
- [ ] Confirm before code/config/deploy/destructive operations, paid-quota external calls, credential rotation, or feature/fix escalation.
- [ ] Check root `AGENTS.md` / `CLAUDE.md` and any obvious directory-level guidance.
- [ ] Treat root `AGENTS.md` as stale if it lacks Message Intent Guard or lacks Bootstrap Protocol, Agent Ownership, Operational Support Guard, Stage Helper Capability Scan, Gate Modes, Required Stops, Completion Rules, Feature Follow-up / Flow-back, Submit And Commit Rules, root/directory guidance boundaries, or requirement archive rules.
- [ ] If root `AGENTS.md` uses agent-loop managed blocks, compare its managed guidance version with the current local `agent-loop` skill version.
- [ ] Compare each managed block `section` and `block-version` against the current root AGENTS template.
- [ ] Treat root `AGENTS.md` as stale if the managed guidance version is older than the current local `agent-loop` skill version, unless the human explicitly defers refresh.
- [ ] Treat missing block-version, older block-version, or missing managed sections as stale even when the file-level skill version matches.
- [ ] Do not write bare `block-version:<agent-loop-version>` values; copy the full template block revision such as `block-version:1.2.3-20260625`.
- [ ] Treat date-only, malformed, or different block-version values as stale; exact full template block-version match is required.
- [ ] If Managed Block Rule is absent, propose root guidance refresh before relying on managed blocks.
- [ ] When refreshing a managed block, copy the current template marker metadata for the same `section`; adjust only `source` if the target project uses a different active memory root or artifact source.
- [ ] Treat root `CLAUDE.md` as stale if it duplicates independent long-lived rules or does not clearly point to `AGENTS.md`.
- [ ] If root guidance will be created, refreshed, or repaired, run AGENTS Cleanup / Migration Review for conflicting workflow rules and long-term project memory outside managed blocks.
- [ ] Determine guidance language from existing docs or human preference; default to English only if unclear.
- [ ] For old or large projects, record directory guidance status in `project.md`.
- [ ] Summarize state and recommend one next action.
- [ ] Ask human confirmation before proceeding.

## Remote Project Discovery

- [ ] Load `remote-project-discovery.md`.
- [ ] Check existing local `.agent-loop/remote.md` and thin `project.md`.
- [ ] Inspect local connection docs or remote hints.
- [ ] Confirm Remote Host, Remote Path, and Access Method.
- [ ] Confirm whether the agent may read remote files.
- [ ] Confirm whether the agent may write remote files.
- [ ] Confirm whether the agent may run install/build/test/dev-server commands.
- [ ] Decide where durable `agent-loop` docs live: remote, local-shadow, or undecided.
- [ ] Record command locations for install, build, unit tests, API tests, E2E tests, and dev server.
- [ ] Record browser URL, port forwards, tunnel, and auth when applicable.
- [ ] Record sync model and stale risk.
- [ ] Write local `.agent-loop/remote.md` only after confirmation.
- [ ] Write thin local `project.md` with `Status: remote-entry` only after confirmation.
- [ ] Create remote `.agent-loop/`, `AGENTS.md`, or `CLAUDE.md` only after explicit confirmation.
- [ ] If local-shadow mode is used, label every code fact and command evidence with remote location.

## Existing Project Onboarding

- [ ] Load `existing-project-onboarding.md`.
- [ ] Load `project-architecture-init.md`.
- [ ] Explain that durable onboarding uses the single Deep Onboarding flow. Do not offer Quick / Deep / Targeted onboarding modes.
- [ ] If the human only wants safe continuation, update or propose project memory, root guidance status, commands, boundaries, and uncertainties only.
- [ ] If the human wants durable onboarding docs, newcomer handoff docs, or a focused understanding artifact, load `project-onboarding-scan.md`, `onboarding-db.md`, and `onboarding-db-templates.md`.
- [ ] Read startup docs first.
- [ ] Inspect shallow repo shape.
- [ ] Decide whether large-project triggers apply.
- [ ] If large and subagents are available, recommend bounded subagent scan.
- [ ] Ask human confirmation before using subagents.
- [ ] If subagents are unavailable or declined, continue single-agent scan.
- [ ] Detect runtime/tooling manifests.
- [ ] Classify project shape: frontend | backend | fullstack | worker | cli/library.
- [ ] Identify language adapter and framework adapter.
- [ ] Identify DDD intensity: light | standard | enterprise.
- [ ] For existing projects, map actual directories to DDD-inspired roles without proposing moves.
- [ ] Detect test/build/lint/typecheck commands from scripts or CI.
- [ ] Build capability map from routes/pages/actions/schema/tests/docs.
- [ ] Build boundary map from durable directories.
- [ ] Inventory root and directory-level guidance files.
- [ ] Check whether root `AGENTS.md` exists, is stale, or must be created.
- [ ] If root `AGENTS.md` exists, verify it contains Message Intent Guard, Bootstrap Protocol, Agent Ownership, Gate Modes, Required Stops, and Completion Rules.
- [ ] If root `AGENTS.md` uses agent-loop managed blocks, compare its managed guidance version with the current local `agent-loop` skill version.
- [ ] Compare each managed block `section` and `block-version` against the current root AGENTS template.
- [ ] Treat missing block-version, older block-version, or missing managed sections as stale even when the file-level skill version matches.
- [ ] Do not write bare `block-version:<agent-loop-version>` values; copy the full template block revision such as `block-version:1.2.3-20260625`.
- [ ] Treat date-only, malformed, or different block-version values as stale; exact full template block-version match is required.
- [ ] If Managed Block Rule is absent, propose root guidance refresh before relying on managed blocks.
- [ ] When refreshing a managed block, copy the current template marker metadata for the same `section`; adjust only `source` if the target project uses a different active memory root or artifact source.
- [ ] Check whether root `CLAUDE.md` exists and loads or points to `AGENTS.md`; if it duplicates or diverges, propose converting it to a pointer.
- [ ] Run AGENTS Cleanup / Migration Review when existing root guidance has conflicting workflow rules, duplicated agent-loop rules, or long-term project memory that belongs in `.agent-loop/project.md` or enterprise `.agent-loop/project/*.md`.
- [ ] Record guidance language and evidence in `project.md`.
- [ ] Record root guidance status in `project.md`: `AGENTS.md` present/created/stale/missing/human-deferred and `CLAUDE.md` points-to-AGENTS/created-pointer/stale/missing/human-deferred.
- [ ] Attach evidence and confidence to commands, capabilities, and boundaries.
- [ ] Do not create onboarding-db detail docs during safe continuation work; recommend Deep Onboarding when durable newcomer-facing docs are useful.
- [ ] Decide whether Project Memory Mode should be `simple` or `enterprise`.
- [ ] Recommend enterprise when any hard trigger applies, including about 200k+ LOC, 5+ durable boundaries, 2+ test systems, 3+ execution environments, `project.md` above about 600 lines, repeated re-scans, or 5+ directory-level guidance files.
- [ ] List onboarding uncertainties and follow-up scans.
- [ ] Summarize proposed `project.md` before writing.
- [ ] Write or refresh `onboarding-spec.md` before Deep onboarding detail docs.
- [ ] Write or refresh `onboarding-plan.md` with batches and file budget before writing star docs.
- [ ] Do not create directory-first module/flow/detail files before the spec and plan are accepted.
- [ ] Default Deep file budget before human expansion is 5 star docs or fewer.
- [ ] For focused questions, use a narrow Deep Onboarding spec/plan and one focused star doc or existing star doc update.
- [ ] When onboarding discovers stable project facts missing from project memory, propose or perform project memory backfill after human confirmation.
- [ ] Confirm Deep onboarding passes the Newcomer Handoff Quality Gate, not only file-count coverage.
- [ ] Confirm service startup/config, core domain flows, core data flow, data model, verification strategy, and change-risk map are evidence-backed.
- [ ] Required-core topics cannot remain discovered, planned, needs-deep-trace, draft-star, or blocked-by-unknown when Deep onboarding is marked complete.
- [ ] Use Batch Human Review before writing `.agent-loop/onboarding-db/`, multiple project memory facts, root guidance, or directory guidance.
- [ ] Ask human confirmation before writing `.agent-loop/`, root guidance, directory guidance, onboarding-db, or diagrams.
- [ ] Do not mark onboarding complete until root `AGENTS.md` is present/created/human-deferred and root `CLAUDE.md` is points-to-AGENTS/created-pointer/human-deferred.

## Requirement Archive

- [ ] Load `requirement-management.md`.
- [ ] Identify requirement and prototype source materials.
- [ ] Ask before copying, moving, or renaming human files.
- [ ] Explain that requirement archive dates mean archive date only.
- [ ] Use `.agent-loop/requirements/YYYY-MM-DD-<topic>/` requirement set directory for new archives.
- [ ] Group all same-topic intake materials in the requirement set: requirements, prototypes, screenshots, feedback, recordings, links, and notes.
- [ ] Create or update requirement-set `README.md`.
- [ ] Run Phase Scan: recommend `Delivery Phases` when the requirement is too large for one feature, has MVP/later scope, crosses multiple boundaries, or uses staged-delivery language.
- [ ] If Delivery Phases are used, write or update the README phase table only after human confirmation.
- [ ] Old requirement set README files remain valid; do not force migration only because lifecycle fields are missing.
- [ ] Do not edit `requirement.md` or other source files for lifecycle/status updates.
- [ ] Future / Deferred Requirement Intake: when the human says "先记一下", "后面做", "之后补", "下一轮做", "暂时不做", "以后加", "backlog", "defer this", "follow-up later", or "not in this feature", recommend a requirement set instead of project memory.
- [ ] Do not write future TODO, backlog, deferred requirements, or unimplemented planned capability details into `project.md`.
- [ ] Large follow-up conflicts get a Requirement Conflict Review before appending, rebuilding, or superseding requirements.
- [ ] Normalize names only after confirmation.
- [ ] Record source paths in `spec.md`.
- [ ] Do not overwrite old requirement materials.
- [ ] Recommend `requirements/INDEX.md` only if index triggers apply.

## Product Brief If Needed

- [ ] Load `product-brief.md`.
- [ ] Run Stage Helper Capability Scan before fallback product synthesis.
- [ ] If a PRD/product synthesis or grill-with-docs style helper is available, use it through `external-skill-adapters.md` while writing accepted output to agent-loop `product.md` / `notes.md`.
- [ ] Decide whether Product Brief trigger conditions apply.
- [ ] If source requirements are too broad for one feature, recommend requirement `Delivery Phases` before writing `product.md`.
- [ ] Inspect `project.md` Product Context and Domain Language.
- [ ] Inspect source requirements before asking product questions.
- [ ] Ask one blocking product question at a time when needed.
- [ ] Include the recommended answer with the question.
- [ ] Write `product.md` only after human confirmation.
- [ ] Mark long-term product consensus candidates for Project Memory Update.

## Brainstorm / Clarify

- [ ] Resolve and load `superpowers:brainstorming` or `brainstorming` before clarification actions; record Stage Helper Resolution, or record `unavailable` / `load-failed` before fallback.
- [ ] If Superpowers `brainstorming` or another product-discovery helper is available, use it through `external-skill-adapters.md` while writing accepted output to the current stage artifact.
- [ ] Use only when goal is unstable, scope unclear, or meaningful approaches differ.
- [ ] Check project docs, code, tests, source requirements, Product Context, and Domain Language before asking.
- [ ] Ask 1-5 high-impact questions.
- [ ] Prefer one question at a time unless a short batch is clearer.
- [ ] Questions must affect scope, UX, data, architecture, testing, or acceptance.
- [ ] Write accepted answers back into the current stage artifact: requirement `README.md` / `requirement.md` during requirements discussion, or `product.md` / `spec.md` / `notes.md` during feature work.

## Feature Follow-up And Flow-back

- [ ] Load `feature-follow-up.md`.
- [ ] Trigger before creating a new feature when the human reports a bug, regression, post-close correction, field/schema change, algorithm change, API mismatch, screenshot issue, behavior tweak, "small tweak", test failure, or QA/user feedback.
- [ ] Inspect Active Feature, Paused Features, and recent feature docs in the default 30-day lookback window.
- [ ] Treat 30 days as the default scan window, not a hard boundary; if wording or evidence points to an older feature, run an extended scan and mark `outside-default-window`.
- [ ] Inspect code/test/API/data/UI paths mentioned by the report.
- [ ] If the report is generic, such as 500, blank page, unknown error, or no route/action/log/test evidence, classify as `unclear` and recommend `investigate-first`; do not reopen the nearest recent feature just because it is recent.
- [ ] Present a Candidate Match Matrix with match evidence and match strength.
- [ ] Classify the report as same-feature-bug, same-feature-adjustment, regression-from-feature, new-feature, maintenance-fix, or unclear.
- [ ] For "字段改一下" / "规则微调" / "小改动" wording, check whether acceptance, API/event/data shape, state flow, algorithm, or visible UX changes before choosing same-feature-adjustment vs linked new feature.
- [ ] If a closed feature is the likely owner, recommend `flow-back` and explain that it will reopen or continue the owning feature for follow-up work after human confirmation.
- [ ] If the human declines reopen/flow-back, preserve the old feature close state and require the new linked feature or maintenance-fix to record `Related Feature`, declined reason, inherited acceptance/tests/evidence, and affected paths.
- [ ] If no recent feature owns the report and this is a narrow internal fix, recommend a new `Feature Type: maintenance-fix` feature workspace; do not perform a naked code edit.
- [ ] If the report is durable source material, ask before archiving it under `.agent-loop/requirements/`.
- [ ] Ask before changing feature status, scope, acceptance, tasks, tests, Delivery Contracts, or project memory.
- [ ] Record Follow-up Intake in `notes.md`.
- [ ] Route to the next exact stage: Requirement Archive, Feature Spec update, Work Breakdown, Test Design, Targeted Feature Scan, Plan Gate, or Diagnose Failure.

## Feature Spec

- [ ] Run Stage Helper Capability Scan before fallback spec writing.
- [ ] If a spec-writing, brainstorming, or product-discovery helper is available, use it through `external-skill-adapters.md` while writing accepted output to agent-loop `spec.md`.
- [ ] Create or update feature workspace.
- [ ] Set `Feature Type: normal | maintenance-fix | follow-up`.
- [ ] If the source requirement uses `Delivery Phases`, record the specific phase or single-phase slice in `Source Requirements`.
- [ ] If the feature scope is broader than one accepted phase or one slice inside a single phase, stop and recommend phase/scope split.
- [ ] For maintenance-fix, record why it is not flow-back, why it is not a new product feature, regression/safety risk, and long-term project memory impact.
- [ ] Write problem, goal, scope, stories, acceptance criteria.
- [ ] Record added, modified, and removed behavior.
- [ ] Record out of scope and open questions.
- [ ] Run a lightweight requirement quality check.
- [ ] Present Feature Spec approval with Human Review Summary table.
- [ ] Ask human to approve before task splitting.
- [ ] After approval, ask whether to stay in Strict Mode or enable Feature Auto-Loop.
- [ ] If the human seems slowed by confirmations, explain Feature Auto-Loop as a safe feature-level option.
- [ ] Before Feature Auto-Loop, list assumptions, Human-gated items, risk points, and stop conditions.

## Targeted Feature Scan

- [ ] Use only after existing-project onboarding or stale-memory recovery.
- [ ] Identify feature keywords and likely boundaries.
- [ ] Read related routes/controllers/pages/actions.
- [ ] Read related domain/core modules.
- [ ] Read related schema/model/migration files.
- [ ] Read related tests and E2E specs.
- [ ] Read related directory guidance.
- [ ] Record feature-specific findings in feature docs.
- [ ] Propose `project.md` updates only for lasting project facts.
- [ ] Ask human confirmation before writing lasting project memory.

## Work Breakdown

- [ ] Run Stage Helper Capability Scan before fallback Work Breakdown.
- [ ] Default to vertical slices / tracer bullets.
- [ ] Each normal task forms a narrow verifiable loop through necessary layers.
- [ ] Use horizontal foundation tasks only when a product slice is not yet possible.
- [ ] For each horizontal task, explain why and which future vertical slices prove it.
- [ ] Prefer small, verifiable tasks.
- [ ] Mark each task `Agent-ready` or `Human-gated`.
- [ ] Use only linear, parallel, and barrier structure.
- [ ] Record dependencies and verification hints.
- [ ] If a task creates a long-lived boundary directory, mark whether directory-level `AGENTS.md` should be proposed.
- [ ] Load `complex-artifacts.md` when stories > 3 or the work appears cross-boundary / hard to scan.
- [ ] If stories > 3, pause for a Complex Artifact assessment.
- [ ] Do not recommend Complex Artifact Mode from story count, task count, test count, or ordinary file count alone.
- [ ] Recommend Complex Artifact Mode only when the feature spans multiple collaborating modules, services, workflows, ownership lanes, or release/operation concerns.
- [ ] Treat ordinary cross-module work as a soft signal unless the feature is no longer locally understandable or executable inside one cohesive area.
- [ ] Create only the `tasks/`, `tests/`, or `plans/` detail directories that are actually needed; do not create the full complex layout by default.
- [ ] Detect likely durable producer-consumer boundaries: API, service, event, async workflow, public data, UI state/behavior, SDK/library, or runtime.
- [ ] Recommend Delivery Contract If Needed before downstream implementation relies on assumptions.
- [ ] Do not use roadmap graph in v1.
- [ ] Present task breakdown approval with Human Review Summary table.
- [ ] Ask human to approve task granularity.

## Delivery Contract If Needed

- [ ] Load `delivery-contracts.md`.
- [ ] Confirm that work crosses a durable producer-consumer boundary.
- [ ] Confirm this is not a simple internal change with no downstream consumer.
- [ ] Identify producer and named consumers.
- [ ] Ask human confirmation before creating or updating contract files.
- [ ] Create or update `contracts.md`.
- [ ] Create `contracts/<ID>-<slug>.md` detail when schema, examples, errors, history, or multiple consumers need more space.
- [ ] Record interface shape, inputs, outputs, errors, side effects, permissions, compatibility, producer verification, and consumer notes.
- [ ] Keep temporary subagent assignments in `handoffs/`, not Delivery Contracts.
- [ ] In all modes, including Feature Auto-Loop and Task Auto-Run, ask before writing contract files.
- [ ] Ask human confirmation before status becomes `accepted`.
- [ ] Ask human confirmation and list affected consumers before a breaking contract change.

## Test Design

- [ ] Run Stage Helper Capability Scan before fallback Test Design.
- [ ] Separate requirement checklist from real test execution.
- [ ] Define functional test cases.
- [ ] Define module/core tests.
- [ ] Define API tests when applicable.
- [ ] Define Web E2E/browser cases when applicable.
- [ ] If Web E2E/browser behavior exists, load `e2e-discovery.md` before defining executable E2E cases.
- [ ] Treat API/integration verification as applicable when HTTP/API behavior, service behavior, events, background jobs, auth, persistence, or integration boundaries change.
- [ ] Treat E2E/browser/manual verification as applicable when user-visible Web behavior changes.
- [ ] If substituting for applicable API/E2E verification, record missing capability, risk, substitute proof, and human approval.
- [ ] Discover real E2E sources: scripts, configs, docs, seed/fixture files, env docs, CI, existing E2E directories.
- [ ] Record stable project-level E2E capability in `project.md` with evidence and confidence.
- [ ] Record feature-specific E2E cases in `tests.md` or linked `tests/e2e/*` details.
- [ ] Classify each E2E path as `existing-framework`, `browser`, `chrome`, `computer-use`, `manual`, or `blocked`.
- [ ] Stop or mark Human-gated when URL, app start, auth/session, seed data, external service, or browser tool cannot be safely determined.
- [ ] Define regression tests for bugs or changed behavior.
- [ ] Record test commands and manual verification needs.
- [ ] Present Test Design approval with Human Review Summary table.

## E2E Discovery if Web

- [ ] Run Stage Helper Capability Scan before fallback E2E Discovery if Web.
- [ ] Load `e2e-discovery.md`.
- [ ] Discover real scripts, configs, docs, seed/fixture files, env docs, CI, existing E2E directories, browser URLs, auth/session requirements, and safe execution constraints.
- [ ] Classify the E2E path as `existing-framework`, `browser`, `chrome`, `computer-use`, `manual`, or `blocked`.
- [ ] Record durable E2E capability in `project.md` and feature-specific cases in `tests.md` or `tests/e2e/*`.

## Technical Design / Code Context

- [ ] Run Stage Helper Capability Scan before fallback Technical Design / Code Context.
- [ ] Load `implementation-planning.md`.
- [ ] Inspect exact files likely to change.
- [ ] Inspect nearby tests and fixtures.
- [ ] Identify existing functions, classes, endpoints, components, schemas, hooks, or commands.
- [ ] Identify call chain, data flow, authorization, validation, errors, side effects, and existing callers.
- [ ] Record existing signatures, parameters, return shapes, and local patterns.
- [ ] Define new/changed interfaces before implementation.
- [ ] Read relevant accepted or verified Delivery Contracts before changing producer or consumer code.
- [ ] If a durable interface is new or changed, route to Delivery Contract If Needed.
- [ ] Stop or mark `Human-gated` if signatures, parameters, return shapes, or file paths cannot be discovered or safely defined.
- [ ] Update task detail or plan with the discovered context.

## Plan Gate / Plan If Needed

Before Execute Task / Story:

- [ ] Do not execute immediately after task creation.
- [ ] Decide whether this task/story requires construction-grade `plan.md`.

Create `plan.md` when:

- [ ] task/story touches multiple files or modules
- [ ] task/story changes behavior, tests, interfaces, data, API, async, security, deployment, or cross-module behavior
- [ ] TDD steps need explicit design
- [ ] subagent execution is planned
- [ ] human asks to review a plan first
- [ ] function signatures, parameters, data contracts, or call chains need to be fixed before coding

No-Plan Decision is allowed only when:

- [ ] task is trivial, low-risk, single-file or documentation-only
- [ ] acceptance is clear
- [ ] exact file(s) and exact verification command are known
- [ ] no plan trigger above applies
- [ ] decision is recorded in `notes.md` and the selected task row/detail
- [ ] Strict Mode asks human confirmation before execution, or Feature Auto-Loop records why the Agent-ready task can proceed

Checklist:

- [ ] Load `implementation-planning.md`.
- [ ] Resolve and load `superpowers:writing-plans` or `writing-plans` before planning actions; record Stage Helper Resolution, or record `unavailable` / `load-failed` before fallback.
- [ ] If Superpowers `writing-plans` or another plan-writing helper is available, use it through `external-skill-adapters.md` while writing to agent-loop `plan.md` / `plans/*`.
- [ ] Plan scope is `task` or `story`.
- [ ] Technical context and real source structure are recorded.
- [ ] Files and commands are exact.
- [ ] Existing APIs and local patterns are recorded.
- [ ] New or changed interfaces include signatures, parameters, return values, errors, and side effects.
- [ ] Data/API contracts are defined when applicable.
- [ ] RED/GREEN verification is defined with actual test code when possible.
- [ ] Expected RED/GREEN command output is recorded.
- [ ] Steps are bite-sized and executable.
- [ ] Placeholder scan is clean: no TBD/TODO/fill-in/add proper/write tests/similar language.
- [ ] Type/signature consistency is checked.
- [ ] Risks or rollback notes are recorded.
- [ ] Present plan approval with Human Review Summary table.
- [ ] Human approves plan before execution.
- [ ] After approval, ask whether to stay in Strict Mode or enable Task Auto-Run for this task/story.
- [ ] Do not offer Task Auto-Run without an accepted plan.
- [ ] If the human seems slowed by confirmations, explain Task Auto-Run as a safe task/story-level option.
- [ ] Before Task Auto-Run, list assumptions, risk points, verification commands, and stop conditions.

## Analyze Consistency

- [ ] Run before Execute Task / Story, including after plan approval and before subagent dispatch.
- [ ] Compare accepted `spec.md` / `product.md` against `tasks.md`, `tests.md`, and the active `plan.md`.
- [ ] Confirm each planned implementation step maps to an accepted task/story and acceptance criterion.
- [ ] Confirm each changed behavior has a test or explicit substitute verification path.
- [ ] Confirm no plan step changes human original requirements, product scope, acceptance criteria, public interfaces, Delivery Contracts, or project memory without a human gate.
- [ ] Confirm file paths, commands, function signatures, parameters, return shapes, data contracts, and side effects match code reality.
- [ ] Record findings in `notes.md` under `Analyze Consistency`.
- [ ] If gaps exist, stop and recommend exactly one next action: update spec, update tasks/tests, revise plan, ask clarification, or investigate first.

## Subagent Execution If Approved

- [ ] Confirm the human explicitly approved this subagent dispatch.
- [ ] Do not treat Feature Auto-Loop or Task Auto-Run approval as subagent approval.
- [ ] If using one approval for a bounded task group, list included task/story IDs or scan lanes, allowed boundaries, one brief per subagent, stop conditions, and main-agent review responsibility before asking.
- [ ] Load `skill-routing.md`.
- [ ] Load `external-skill-adapters.md`.
- [ ] After explicit bounded dispatch approval, resolve and load `superpowers:subagent-driven-development` or `subagent-driven-development` before dispatch; record Stage Helper Resolution.
- [ ] Record approval date, exact IDs/lanes, allowed boundaries, and stop conditions; require new confirmation for expanded scope.
- [ ] Confirm authorization status is `active` immediately before dispatch; reject consumed/revoked/expired records and mark the record `consumed` after the approved dispatch group returns or stops.
- [ ] If Superpowers `subagent-driven-development` or another subagent helper is available, use it through `external-skill-adapters.md` after human approval while keeping briefs and returned summaries under agent-loop `handoffs/*`.
- [ ] Verify tasks or scan lanes are independent, bounded, and reviewable.
- [ ] Create one `templates/subagent-brief.md`-style brief per subagent.
- [ ] Store briefs and returned summaries under `handoffs/*`.
- [ ] Require returned changed files, commands, evidence, drift, open questions, and next step.
- [ ] Main agent reviews returned work before updating `tasks.md`, `tests.md`, `notes.md`, or proposed `project.md`.
- [ ] Prevent subagents from closing features, submitting code, updating project memory directly, accepting Delivery Contracts, approving breaking changes, or marking tasks `done`.
- [ ] If independence or review responsibility is unclear, do not dispatch; continue single-agent execution or mark `Human-gated`.

## Execute Task / Story

- [ ] Confirm execution scope: task by default, story only by explicit choice.
- [ ] Confirm Plan Gate passed: accepted `plan.md` / `plans/*`, or recorded No-Plan Decision for a trivial task.
- [ ] If Task Auto-Run is enabled, confirm an accepted plan exists; No-Plan Decision is insufficient.
- [ ] If Feature Auto-Loop is enabled, execute only Agent-ready tasks.
- [ ] If Task Auto-Run is enabled, execute only the selected task/story and stop after evidence/review/drift updates and Task Done Gate status update.
- [ ] Stop at Human-gated tasks or any stop condition.
- [ ] Use TDD by default.
- [ ] Resolve and load `superpowers:test-driven-development` or `test-driven-development` before behavior-changing execution; record Stage Helper Resolution, or record `unavailable` / `load-failed` before fallback.
- [ ] If Superpowers `test-driven-development` or another TDD helper is available, use it through `external-skill-adapters.md` while keeping evidence and task status under agent-loop.
- [ ] Verify RED before implementation.
- [ ] Write minimal GREEN implementation.
- [ ] Verify GREEN with fresh command output.
- [ ] Refactor only while green.
- [ ] Record TDD cycle and evidence in `notes.md`.
- [ ] Move task to `review` after implementation and fresh verification.
- [ ] Keep task `in-progress` or `blocked` if applicable verification is missing and no human-approved substitute verification exists.
- [ ] Do not mark task `done` until Task Done Gate passes.

## Diagnose Failure

- [ ] Resolve and load `superpowers:systematic-debugging` or `systematic-debugging` before proposing a fix; record Stage Helper Resolution, or record `unavailable` / `load-failed` before fallback.
- [ ] If Superpowers `systematic-debugging` or another debugging helper is available, use it through `external-skill-adapters.md` while recording root cause and fix evidence in agent-loop `notes.md`.
- [ ] Reproduce consistently or gather more evidence.
- [ ] Read error output fully.
- [ ] Check recent changes.
- [ ] Form a specific hypothesis.
- [ ] Test one variable at a time.
- [ ] Write a failing regression test when possible.
- [ ] Fix root cause, not symptom.
- [ ] Record diagnosis in `notes.md`.

## Verify

- [ ] Resolve and load `superpowers:verification-before-completion` or `verification-before-completion` before any completion claim; record Stage Helper Resolution, or record `unavailable` / `load-failed` before fallback.
- [ ] If Superpowers `verification-before-completion` or another verification helper is available, use it through `external-skill-adapters.md` while recording evidence in agent-loop `notes.md`.
- [ ] Identify what command or action proves the claim.
- [ ] Run it fresh.
- [ ] Read full output and exit status.
- [ ] Record evidence in `notes.md`.
- [ ] Do not claim completion without evidence.

## Review

- [ ] Resolve and load `superpowers:requesting-code-review` or `requesting-code-review` before each task, submit, or feature-close review scope; record a fresh Stage Helper Resolution, or record `unavailable` / `load-failed` before fallback.
- [ ] If Superpowers `requesting-code-review` or another review helper is available, use it through `external-skill-adapters.md` while recording findings in agent-loop `notes.md`.
- [ ] Perform lightweight Spec Review for every task before marking it `done`.
- [ ] Perform Spec Review before Submit / Integrate.
- [ ] Compare implementation against `product.md` when present, `spec.md`, acceptance criteria, scope, and out-of-scope.
- [ ] Perform Standards Review for large projects, broad diffs, directory or durable boundary changes, security/data changes, architecture changes, or human request.
- [ ] Compare implementation against root/directory `AGENTS.md`, `project.md`, testing rules, directory boundaries, and local conventions.
- [ ] Record findings, accepted fixes, and rejected fixes in `notes.md`.
- [ ] Compare producer code and tests against relevant Delivery Contracts.
- [ ] Keep task status as `review` if required review is missing.
- [ ] Ask human confirmation before applying review-driven changes that alter behavior, scope, architecture, data, or public interfaces.

## Task Done Gate

- [ ] Implementation scope complete.
- [ ] Required tests or substitute verification ran fresh.
- [ ] Evidence recorded in `notes.md`.
- [ ] Lightweight Spec Review recorded.
- [ ] Standards Review recorded when triggered.
- [ ] Drift decision recorded, including `no drift` when applicable.
- [ ] `tasks.md` or task detail names the evidence location.
- [ ] Only now mark task `done`; otherwise keep `review`, `in-progress`, or `blocked`.

## Drift Check

- [ ] Compare implementation against `spec.md`.
- [ ] Compare completed work against `tasks.md` and `tests.md`.
- [ ] Compare producer-consumer interfaces against `contracts.md` and linked `contracts/*` details when present.
- [ ] List affected consumers and ask human confirmation before accepting a breaking contract change.
- [ ] If behavior changed, update feature docs.
- [ ] If long-term project facts changed, load `project-memory-mode.md` and route updates to `project.md` or enterprise `project/*.md`.
- [ ] Do not rewrite original human requirements.
- [ ] If the feature references a Delivery Phase, propose phase status / Feature Mapping updates for human confirmation.
- [ ] Record drift decisions in `notes.md`.
- [ ] Do not route directly to Close from Drift Check.
- [ ] Next stage is Project Memory Update / Requirement Reconciliation when long-term project facts, requirement lifecycle, Delivery Phase status, or Feature Mapping changed; otherwise Feature Completion Check.
- [ ] Present drift decisions with Human Review Summary table.

## Project Memory Update

- [ ] Load `project-memory-mode.md`.
- [ ] Confirm current Project Memory Mode: simple | enterprise.
- [ ] If hard or soft enterprise triggers apply, recommend a mode switch before adding lots of detail to `project.md`.
- [ ] Confirm the change affects future work, not only current task history.
- [ ] Do not write future TODO, backlog, deferred requirements, or unimplemented planned capability details into `project.md`.
- [ ] Update Current Work and Next Suggested Action.
- [ ] In simple mode, update the matching `project.md` section.
- [ ] In enterprise mode, keep `project.md` as index/current state and update the matching `project/*.md` detail file.
- [ ] Update Capabilities if a durable capability changed.
- [ ] Update Directory Map, Boundaries, or Directory Guidance if boundaries changed.
- [ ] Update Architecture Profile if project shape, language/framework adapter, DDD intensity, or durable dependency direction changed.
- [ ] Update Test Commands or Testing if commands or test systems changed.
- [ ] Update Domain Language, Product Context, Known Constraints, or Long-Term Decisions if future agents need them.
- [ ] Resolve or add Onboarding Uncertainties when confidence changes.
- [ ] Run Requirement Reconciliation when the feature references or creates requirement sets.
- [ ] Do not edit `requirement.md` or other source files for lifecycle/status updates.
- [ ] Update requirement set README / optional requirements INDEX for lifecycle status, Delivery Phase status, and Feature Mapping only after human confirmation.
- [ ] Ask before changing root or directory-level `AGENTS.md`.
- [ ] Present proposed memory updates with Human Review Summary table.

## Submit / Integrate

- [ ] Load `submit-and-integrate.md`.
- [ ] Run Stage Helper Capability Scan before fallback submit/integrate preparation.
- [ ] If Superpowers `finishing-a-development-branch` or another finishing/branch helper is available, use it through `external-skill-adapters.md`.
- [ ] Use external finishing skills only for completion options and branch hygiene.
- [ ] Inspect diff and untracked files.
- [ ] Separate product code from `agent-loop` artifact changes.
- [ ] Identify unrelated dirty work.
- [ ] Confirm fresh verification evidence exists.
- [ ] Confirm drift check result and known drift.
- [ ] Confirm required review has passed or record why submit must stop.
- [ ] Present submit/integrate decision with Human Review Summary table.
- [ ] Ask human which action to take: prepare only, commit, PR text, merge note, release note, publish/release note, or skip.
- [ ] Only commit, publish, release, merge, or create final PR text after explicit human confirmation.
- [ ] Record submit/integrate result in `notes.md`.
- [ ] If submit succeeded and the feature appears done, recommend Feature Completion Check, not Close.

## Feature Completion Check

- [ ] Load `feature-completion-check.md`.
- [ ] Run Stage Helper Capability Scan before fallback completion analysis.
- [ ] If verification, review, finishing, or close-decision helpers are available, use them through `external-skill-adapters.md` while keeping close under agent-loop control.
- [ ] Run after likely completion, before starting a new feature with an Active Feature, or on resume with an Active Feature.
- [ ] Confirm accepted spec exists.
- [ ] Confirm all in-scope tasks are done, skipped with reason, or removed from scope.
- [ ] Confirm required tests or substitute verification are recorded.
- [ ] Confirm fresh verification evidence exists.
- [ ] Confirm Feature Close Review completed.
- [ ] Confirm feature-level Spec Review covers `product.md` when present, `spec.md`, `tasks.md`, `tests.md`, acceptance criteria, and out-of-scope boundaries.
- [ ] Confirm feature-level Standards Review completed when large project, broad diff, directory or durable boundary change, security/data change, architecture change, or human request applies.
- [ ] Confirm Drift Check completed.
- [ ] Confirm Delivery Contracts are implemented and verified when downstream consumers rely on them.
- [ ] Confirm accepted Delivery Contracts match producer code/tests and have no unapproved breaking changes.
- [ ] Confirm long-term facts are reflected in `project.md`.
- [ ] Confirm submit/integration status is recorded if requested.
- [ ] Record the check in `notes.md`.
- [ ] If blockers prevent completion, record Result: blocked and recommend exactly one unblock stage.
- [ ] Recommend Close, Continue, Pause before new feature, or Scope Update.
- [ ] Present completion status with Human Review Summary table.
- [ ] Ask explicit human confirmation before close.

## Pause / Close

- [ ] Run Stage Helper Capability Scan before fallback pause/close preparation.
- [ ] If verification, finishing, or handoff helpers are available, use them through `external-skill-adapters.md` only for evidence discipline, close options, or handoff structure.

Pause:

- [ ] Record current state.
- [ ] Record next suggested action.
- [ ] Record blockers and files touched.

Close:

- [ ] Fresh verification evidence exists.
- [ ] Drift check completed.
- [ ] Feature Close Review completed.
- [ ] Submit/integration status recorded if requested.
- [ ] `project.md` updated for long-term changes.
- [ ] Requirement Reconciliation completed when the feature references or creates requirement sets.
- [ ] `notes.md` has close record.
- [ ] Human explicitly confirms close.

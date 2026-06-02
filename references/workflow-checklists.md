# Agent Loop Workflow Checklists

Use the relevant checklist before entering a stage.

Before human approval for non-trivial stage output:

- [ ] Load `human-review-summary.md`.
- [ ] Present a table-first approval view.
- [ ] Include artifacts, evidence, risk/blockers, human decision, and next stage.
- [ ] Keep full source-of-truth content in artifact files.

## Project Entry

- [ ] Inspect whether `agent-loop/` exists.
- [ ] If present, read `project.md`.
- [ ] If `project.md` says `Memory Mode: enterprise`, read only the needed linked project-memory detail files.
- [ ] Locate active or paused feature.
- [ ] If an Active Feature exists, consider Feature Completion Check before starting new feature work.
- [ ] Check whether memory appears stale compared with obvious repo reality.
- [ ] Check whether local directory is empty/ambiguous or appears to be a remote entry point.
- [ ] If human says remote project, SSH, devcontainer, container, tunnel, or remote workspace, route to Remote Project Discovery.
- [ ] Check root `AGENTS.md` / `CLAUDE.md` and any obvious directory-level guidance.
- [ ] Determine guidance language from existing docs or human preference; default to English only if unclear.
- [ ] For old or large projects, record directory guidance status in `project.md`.
- [ ] Summarize state and recommend one next action.
- [ ] Ask human confirmation before proceeding.

## Remote Project Discovery

- [ ] Load `remote-project-discovery.md`.
- [ ] Check existing local `agent-loop/remote.md` and thin `project.md`.
- [ ] Inspect local connection docs or remote hints.
- [ ] Confirm Remote Host, Remote Path, and Access Method.
- [ ] Confirm whether the agent may read remote files.
- [ ] Confirm whether the agent may write remote files.
- [ ] Confirm whether the agent may run install/build/test/dev-server commands.
- [ ] Decide where durable `agent-loop` docs live: remote, local-shadow, or undecided.
- [ ] Record command locations for install, build, unit tests, API tests, E2E tests, and dev server.
- [ ] Record browser URL, port forwards, tunnel, and auth when applicable.
- [ ] Record sync model and stale risk.
- [ ] Write local `agent-loop/remote.md` only after confirmation.
- [ ] Write thin local `project.md` with `Status: remote-entry` only after confirmation.
- [ ] Create remote `agent-loop/`, `AGENTS.md`, or `CLAUDE.md` only after explicit confirmation.
- [ ] If local-shadow mode is used, label every code fact and command evidence with remote location.

## Existing Project Onboarding

- [ ] Load `existing-project-onboarding.md`.
- [ ] Load `project-architecture-init.md`.
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
- [ ] Record guidance language and evidence in `project.md`.
- [ ] Attach evidence and confidence to commands, capabilities, and boundaries.
- [ ] Decide whether Project Memory Mode should be `simple` or `enterprise`.
- [ ] Recommend enterprise when any hard trigger applies, including about 200k+ LOC, 5+ durable boundaries, 2+ test systems, 3+ execution environments, `project.md` above about 600 lines, repeated re-scans, or 5+ directory-level guidance files.
- [ ] List onboarding uncertainties and follow-up scans.
- [ ] Summarize proposed `project.md` before writing.
- [ ] Ask human confirmation before writing `agent-loop/`, root guidance, or directory guidance.

## Requirement Archive

- [ ] Load `requirement-management.md`.
- [ ] Identify requirement and prototype source materials.
- [ ] Ask before copying, moving, or renaming human files.
- [ ] Explain that requirement archive dates mean archive date only.
- [ ] Use `agent-loop/requirements/YYYY-MM-DD-<topic>/` requirement set directory for new archives.
- [ ] Group all same-topic intake materials in the requirement set: requirements, prototypes, screenshots, feedback, recordings, links, and notes.
- [ ] Create or update requirement-set `README.md`.
- [ ] Normalize names only after confirmation.
- [ ] Record source paths in `spec.md`.
- [ ] Do not overwrite old requirement materials.
- [ ] If legacy `agent-loop/inputs/` exists, propose migration to `agent-loop/requirements/` before new feature work.
- [ ] Recommend `requirements/INDEX.md` only if index triggers apply.

## Brainstorm / Clarify

- [ ] Use only when goal is unstable, scope unclear, or meaningful approaches differ.
- [ ] Check project docs, code, tests, source requirements, Product Context, and Domain Language before asking.
- [ ] Ask 1-5 high-impact questions.
- [ ] Prefer one question at a time unless a short batch is clearer.
- [ ] Questions must affect scope, UX, data, architecture, testing, or acceptance.
- [ ] Write accepted answers back into `spec.md`.

## Product Brief If Needed

- [ ] Load `product-brief.md`.
- [ ] Decide whether Product Brief trigger conditions apply.
- [ ] Inspect `project.md` Product Context and Domain Language.
- [ ] Inspect source requirements before asking product questions.
- [ ] Ask one blocking product question at a time when needed.
- [ ] Include the recommended answer with the question.
- [ ] Write `product.md` only after human confirmation.
- [ ] Mark long-term product consensus candidates for Project Memory Update.

## Feature Spec

- [ ] Create or update feature workspace.
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

- [ ] Default to vertical slices / tracer bullets.
- [ ] Each normal task forms a narrow verifiable loop through necessary layers.
- [ ] Use horizontal foundation tasks only when a product slice is not yet possible.
- [ ] For each horizontal task, explain why and which future vertical slices prove it.
- [ ] Prefer small, verifiable tasks.
- [ ] Mark each task `Agent-ready` or `Human-gated`.
- [ ] Use only linear, parallel, and barrier structure.
- [ ] Record dependencies and verification hints.
- [ ] If a task creates a long-lived boundary directory, mark whether directory-level `AGENTS.md` should be proposed.
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

## Technical Design / Code Context

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

## Plan If Needed

Create `plan.md` when:

- [ ] task/story touches multiple files or modules
- [ ] TDD steps need explicit design
- [ ] subagent execution is planned
- [ ] human asks to review a plan first
- [ ] function signatures, parameters, data contracts, or call chains need to be fixed before coding

Checklist:

- [ ] Load `implementation-planning.md`.
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
- [ ] If the human seems slowed by confirmations, explain Task Auto-Run as a safe task/story-level option.
- [ ] Before Task Auto-Run, list assumptions, risk points, verification commands, and stop conditions.

## Execute Task / Story

- [ ] Confirm execution scope: task by default, story only by explicit choice.
- [ ] If Feature Auto-Loop is enabled, execute only Agent-ready tasks.
- [ ] If Task Auto-Run is enabled, execute only the selected task/story and stop after evidence/review/drift updates and Task Done Gate status update.
- [ ] Stop at Human-gated tasks or any stop condition.
- [ ] Use TDD by default.
- [ ] Verify RED before implementation.
- [ ] Write minimal GREEN implementation.
- [ ] Verify GREEN with fresh command output.
- [ ] Refactor only while green.
- [ ] Record TDD cycle and evidence in `notes.md`.
- [ ] Move task to `review` after implementation and fresh verification.
- [ ] Keep task `in-progress` or `blocked` if applicable verification is missing and no human-approved substitute verification exists.
- [ ] Do not mark task `done` until Task Done Gate passes.

## Diagnose Failure

- [ ] Reproduce consistently or gather more evidence.
- [ ] Read error output fully.
- [ ] Check recent changes.
- [ ] Form a specific hypothesis.
- [ ] Test one variable at a time.
- [ ] Write a failing regression test when possible.
- [ ] Fix root cause, not symptom.
- [ ] Record diagnosis in `notes.md`.

## Verify

- [ ] Identify what command or action proves the claim.
- [ ] Run it fresh.
- [ ] Read full output and exit status.
- [ ] Record evidence in `notes.md`.
- [ ] Do not claim completion without evidence.

## Review

- [ ] Perform lightweight Spec Review for every task before marking it `done`.
- [ ] Perform Spec Review before Submit / Integrate.
- [ ] Compare implementation against `product.md` when present, `spec.md`, acceptance criteria, scope, and out-of-scope.
- [ ] Perform Standards Review for large projects, broad diffs, boundary changes, security/data changes, or human request.
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
- [ ] Record drift decisions in `notes.md`.
- [ ] Present drift decisions with Human Review Summary table.

## Submit / Integrate

- [ ] Load `submit-and-integrate.md`.
- [ ] Inspect diff and untracked files.
- [ ] Separate product code from `agent-loop` artifact changes.
- [ ] Identify unrelated dirty work.
- [ ] Confirm fresh verification evidence exists.
- [ ] Confirm drift check result and known drift.
- [ ] Present submit/integrate decision with Human Review Summary table.
- [ ] Ask human which action to take: prepare only, commit, PR text, merge note, release note, or skip.
- [ ] Only commit after explicit human confirmation.
- [ ] Record submit/integrate result in `notes.md`.

## Project Memory Update

- [ ] Load `project-memory-mode.md`.
- [ ] Confirm current Project Memory Mode: simple | enterprise.
- [ ] If hard or soft enterprise triggers apply, recommend a mode switch before adding lots of detail to `project.md`.
- [ ] Confirm the change affects future work, not only current task history.
- [ ] Update Current Work and Next Suggested Action.
- [ ] In simple mode, update the matching `project.md` section.
- [ ] In enterprise mode, keep `project.md` as index/current state and update the matching `project/*.md` detail file.
- [ ] Update Capabilities if a durable capability changed.
- [ ] Update Directory Map, Boundaries, or Directory Guidance if boundaries changed.
- [ ] Update Architecture Profile if project shape, language/framework adapter, DDD intensity, or durable dependency direction changed.
- [ ] Update Test Commands or Testing if commands or test systems changed.
- [ ] Update Domain Language, Product Context, Known Constraints, or Long-Term Decisions if future agents need them.
- [ ] Resolve or add Onboarding Uncertainties when confidence changes.
- [ ] Ask before changing root or directory-level `AGENTS.md`.
- [ ] Present proposed memory updates with Human Review Summary table.

## Feature Completion Check

- [ ] Load `feature-completion-check.md`.
- [ ] Run after likely completion, before starting a new feature with an Active Feature, or on resume with an Active Feature.
- [ ] Confirm accepted spec exists.
- [ ] Confirm all in-scope tasks are done, skipped with reason, or removed from scope.
- [ ] Confirm required tests or substitute verification are recorded.
- [ ] Confirm fresh verification evidence exists.
- [ ] Confirm Feature Close Review completed.
- [ ] Confirm feature-level Spec Review covers `product.md` when present, `spec.md`, `tasks.md`, `tests.md`, acceptance criteria, and out-of-scope boundaries.
- [ ] Confirm feature-level Standards Review completed when large project, broad diff, boundary/security/data change, architecture change, or human request applies.
- [ ] Confirm Drift Check completed.
- [ ] Confirm Delivery Contracts are implemented and verified when downstream consumers rely on them.
- [ ] Confirm accepted Delivery Contracts match producer code/tests and have no unapproved breaking changes.
- [ ] Confirm long-term facts are reflected in `project.md`.
- [ ] Confirm submit/integration status is recorded if requested.
- [ ] Record the check in `notes.md`.
- [ ] Recommend Close, Continue, Pause before new feature, or Scope Update.
- [ ] Present completion status with Human Review Summary table.
- [ ] Ask explicit human confirmation before close.

## Pause / Close

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
- [ ] `notes.md` has close record.
- [ ] Human explicitly confirms close.

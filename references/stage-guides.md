# Agent Loop Stage Guides

Use this file to execute a specific stage. Pair it with `workflow-checklists.md` when you need checklist form.

Before asking the human to approve a non-trivial stage output, load `human-review-summary.md` and present a table-first approval summary. Full artifacts remain the source of truth.

## Project Entry

Entry: any use of this skill.

Read:

- `.agent-loop/project.md` if present
- enterprise `.agent-loop/project/*.md` detail files only when referenced by `project.md` and needed for the current stage
- active feature docs if present
- repo docs/scripts only as needed

Write:

- nothing until human confirms the next stage

Exit:

- one recommended next stage
- if an Active Feature exists, run Feature Completion Check before recommending a new feature or broad new work

## Init Project

Entry: no `.agent-loop/` or legacy `agent-loop/`, little or no code.

If the human says the project is remote, or the local directory appears to be only a remote entry point, do not initialize a normal local project. Route to Remote Project Discovery first.

Load:

- `project-guidance.md`
- `project-memory-mode.md`
- `project-architecture-init.md`

Before writing:

- classify project shape, language adapter, framework adapter, and DDD intensity
- determine guidance language from human preference or project language; default to English if unclear
- propose only a reference scaffold, with optional directories clearly marked
- ask human confirmation before creating code directories

Write after confirmation:

- `.agent-loop/project.md`
- `.agent-loop/requirements/`
- `.agent-loop/features/`
- root `AGENTS.md`
- root `CLAUDE.md -> AGENTS.md` when supported

Use `templates/project.md`.
Use `templates/root-AGENTS.md` for project guidance.

Exit:

- project memory drafted and accepted
- next stage: Requirement Archive when the human supplied requirements/prototypes in chat or files; otherwise Brainstorm / Clarify, Product Brief if Needed, or Feature Spec when intent is already stable

## Remote Project Discovery

Entry: the human says this is a remote project, local files contain remote-entry hints, or local/remote/container execution is unclear. An empty local directory with no remote hint should route to Init Project, not Remote Project Discovery.

Load:

- `remote-project-discovery.md`
- `project-guidance.md` only if guidance files may be created locally or remotely

Inspect:

- local `.agent-loop/project.md` and `.agent-loop/remote.md` if present
- local connection docs, README, scripts, SSH/devcontainer/container hints, or notes
- remote files only if the human has already granted access or the access method is already configured and safe to use

Do not:

- create a full local project memory for an empty entry directory
- treat local files as code reality when source of truth is remote
- run remote install/build/test/dev-server commands without confirmation
- create remote `.agent-loop/`, `AGENTS.md`, or `CLAUDE.md` without confirmation

Output before writing:

- whether this is a remote-entry, local mirror, local-shadow, or unclear setup
- remote host/path/access method if known
- proposed source of truth for code, git, runtime, and agent-loop docs
- command locations for install/build/unit/API/E2E/dev server if known
- permissions needed from the human
- one recommended next action

Write after confirmation:

- local `.agent-loop/remote.md`
- thin local `.agent-loop/project.md` with `Status: remote-entry` when local is only an entry point
- remote `.agent-loop/project.md`, `requirements/`, `features/`, root `AGENTS.md`, and `CLAUDE.md` only if remote writes are confirmed

Exit:

- local entry memory can locate the remote project
- the remote project memory location is decided: remote, local-shadow, or blocked
- next stage: Existing Project Onboarding against the remote source of truth, or Ask Human if access is blocked

## Existing Project Onboarding

Entry: existing code, no `.agent-loop/` or legacy `agent-loop/`.

If the existing code is remote, perform onboarding against the remote source of truth. If local-shadow mode is active, all findings must include remote evidence labels.

Load:

- `existing-project-onboarding.md`
- `project-onboarding-scan.md` only when the human chooses Deep Project Onboarding Scan, asks for guided onboarding, or asks for a targeted module/flow/deployment/async scan
- `onboarding-db.md` and `onboarding-db-templates.md` only when reading, writing, refreshing, or drafting `.agent-loop/onboarding-db/`
- `large-projects.md` when old, unfamiliar, multi-package, multi-service, or likely 100k+ LOC
- `project-guidance.md`
- `project-memory-mode.md`
- `project-architecture-init.md`

First decision:

- Explain Quick Onboarding and Deep Project Onboarding Scan when the human asks to take over or understand an existing project.
- Default to Quick Onboarding when the human wants to continue feature work quickly.
- Use Deep Project Onboarding Scan when the human wants newcomer-friendly project understanding or long-term onboarding docs.
- Use Targeted Onboarding Scan when the human asks about one module, flow, async task, deployment path, or problem area.

Inspect:

- README and docs
- AGENTS/CLAUDE/GEMINI files
- package/test scripts
- key directories

Use layered scan order:

1. startup docs
2. shallow repo shape
3. decide whether large-project triggers apply
4. optionally recommend bounded subagent scan when large and supported
5. runtime/tooling manifests
6. architecture profile and actual code layout
7. capability map
8. boundary map
9. guidance inventory
10. uncertainty list

Do not read the whole repository. Do not start feature implementation during onboarding.

If subagents are used, the main agent keeps ownership of synthesis and all writes. Subagents only return findings, evidence, confidence, uncertainties, files read, and suggested `project.md` entries.

If Deep Project Onboarding Scan is selected:

- run P0 before P1 and P2
- choose Compact / Standard / Expanded Layout Mode before proposing onboarding-db files
- draft onboarding-db with `templates/onboarding-db/*`
- create diagrams only when they answer a concrete onboarding question
- use Batch Human Review before writing onboarding-db, project memory backfill, or guidance changes
- keep code reality as current fact when docs conflict with code

If Targeted Onboarding Scan is selected:

- inspect only the minimal safe context plus the selected module, flow, async task, deployment path, or problem area
- propose focused onboarding-db updates only for that target
- do not create unrelated onboarding-db files

Output before writing:

- project summary
- tech stack
- architecture profile: project shape, language adapter, framework adapter, DDD intensity, and whether layout is existing reality or proposed scaffold
- guidance language with evidence
- capability map with evidence and confidence
- boundary map with evidence and confidence
- discovered commands with evidence and confidence
- recommended Project Memory Mode: simple or enterprise, with trigger evidence
- recommended onboarding mode: Quick | Deep | Targeted, with reason
- recommended Onboarding DB Layout Mode when Deep is selected
- existing/proposed guidance files
- low-confidence findings and recommended follow-up
- one recommended next action

Directory guidance:

- identify existing root and directory-level `AGENTS.md` / `CLAUDE.md`
- record guidance status in `project.md`
- propose directory-level `AGENTS.md` only for long-lived boundary directories
- ask human confirmation before creating or changing guidance files

Write after confirmation:

- `.agent-loop/project.md`
- `.agent-loop/onboarding-db/` only when Deep or Targeted onboarding docs are confirmed
- enterprise `.agent-loop/project/*.md` files only when recommended and confirmed
- `.agent-loop/requirements/`
- `.agent-loop/features/`
- root `AGENTS.md` / `CLAUDE.md` guidance, if missing or stale
- directory-level `AGENTS.md` only if specific boundary directories are confirmed

Exit:

- human accepts project memory
- next stage: Start Feature or Targeted Feature Scan

## Reconcile Project Context / Re-Adopt Agent Loop Project

Entry: `agent-loop` exists but memory appears stale, or the project previously used `agent-loop` and recent development bypassed it.

Inspect:

- `project.md`
- active feature docs
- obvious code reality: scripts, directories, README, current tests

Load `recovery-and-backfill.md` for every explicit re-adoption request. Also load it whenever code reality should repair project or feature docs.

For re-adoption, do not start new feature work first. Compare current code/tests/scripts with existing `agent-loop` docs, then propose backfill.

Output before writing:

- what appears stale
- what code reality shows
- which recent outside-loop changes appear relevant
- whether original human requirements conflict with code
- what should update
- what should stay unchanged

Write after confirmation:

- `project.md` and/or feature docs
- reconciliation note in `notes.md` when feature-specific

Exit:

- memory and code reality are close enough to continue

## Requirement Archive

Entry: human provides requirement/prototype or points to existing material.

Load:

- `requirement-management.md`

Rules:

- Ask before copying, moving, or renaming human files.
- Never silently modify original requirements.
- Normalize names only after confirmation.
- Requirement archive dates are archive dates only, not deadlines or feature lifecycle dates.
- Use a requirement set directory with `README.md`; do not create new flat files directly under `.agent-loop/requirements/`.
- Group all materials from the same intake/topic together: requirement documents, prototypes, screenshots, feedback, recordings, links, and follow-up notes.
- Do not overwrite old requirement materials when requirements change.

Write:

- `.agent-loop/requirements/<archive-date>-<topic>/README.md`
- `.agent-loop/requirements/<archive-date>-<topic>/requirement.*`
- `.agent-loop/requirements/<archive-date>-<topic>/prototype.*`
- optional feedback, screenshot, recording, design-link, meeting-note, and other source files inside the same requirement set
- optional change-request files inside the same requirement set
- optional `.agent-loop/requirements/INDEX.md` only when trigger conditions apply
- legacy `.agent-loop/inputs/` or visible-root `agent-loop/inputs/` migration proposal when old projects still use it
- source references in `spec.md`

Exit:

- requirements archived or original paths recorded

## Product Brief If Needed

Entry: source requirements or conversation need product/PRD-style synthesis before engineering specification.

Load:

- `product-brief.md`

Trigger examples:

- meaningful user journey or UI/interaction flow
- prototype, product document, PRD, long requirement text, or design notes
- multiple actors, roles, permissions, tenants, or business objects
- likely 3 or more user stories
- scope and out-of-scope need product confirmation
- ambiguous business terminology

Rules:

- create `product.md` only when useful; skip for narrow bugfixes or clear technical tasks
- inspect `project.md` Product Context and Domain Language before asking product questions
- ask one blocking product question at a time
- include the agent's recommended answer when asking
- record long-term consensus candidates for Project Memory Update

Write after confirmation:

- `product.md`
- `notes.md` human decisions if needed

Exit:

- product intent is stable enough for Feature Spec

## Brainstorm / Clarify

Entry: goal is vague, scope unclear, or meaningful approaches differ.

Load:

- `external-skill-adapters.md` when Superpowers or another brainstorming/product-discovery skill is available

Rules:

- when Superpowers is available, use the Brainstorming Adapter while keeping output in `product.md`, `spec.md`, and `notes.md`
- Ask 1-5 high-impact questions.
- Default to one question at a time.
- Questions must affect scope, UX, data, architecture, testing, or acceptance.
- Do not ask filler questions.
- If a question can be answered by reading project docs, code, tests, source requirements, `project.md`, or `product.md`, inspect those first instead of asking the human.
- When product terminology is fuzzy or conflicts with `project.md` Domain Language, propose a canonical meaning and ask only if still ambiguous.

Write:

- accepted product clarifications into `product.md` when it exists
- accepted engineering clarifications into `spec.md`
- human decisions into `notes.md`

Exit:

- intent stable enough for Feature Spec

## Feature Spec

Entry: goal and source requirements are clear enough.

Write:

- feature workspace
- `spec.md` from template

Include:

- problem/goal
- product brief reference when `product.md` exists
- scope
- stories
- acceptance criteria
- added/modified/removed behavior
- dependencies
- out of scope
- open questions

Exit:

- human accepts spec or requests revision
- after acceptance, explain that Strict Mode asks before each stage and offer Feature Auto-Loop for Agent-ready downstream work if the human wants fewer confirmations

## Targeted Feature Scan

Entry: existing project has been onboarded and the human selected a feature, but the affected boundaries are not yet understood.

Load:

- `existing-project-onboarding.md`
- `large-projects.md` for old, large, or multi-package projects

Inspect only feature-relevant areas:

- keywords from the human goal and draft spec
- related routes/controllers/pages/actions
- related domain/core modules
- related schema/model/migration files
- related tests and E2E specs
- related guidance docs and directory `AGENTS.md`

Write after confirmation:

- feature-specific findings into `spec.md`, `tasks.md`, `tests.md`, or `notes.md`
- lasting project facts into `project.md` only after human confirmation

Exit:

- affected boundaries are clear enough for Work Breakdown or Test Design

## Requirement Checklist

Entry: draft spec exists.

Check:

- no major ambiguity
- stories independently testable
- acceptance criteria measurable
- behavior changes clear
- edge cases and out-of-scope recorded

Write:

- checklist result in `tests.md` or `notes.md`
- spec updates if human confirms

Exit:

- spec ready for task split

## Work Breakdown

Entry: accepted spec.

Write:

- `tasks.md`

Rules:

- default to vertical slices / tracer bullets
- each normal task should form a narrow verifiable loop through the necessary layers
- allow horizontal foundation tasks only when a verifiable product slice is not yet possible
- every horizontal foundation task must explain why it cannot be vertical and which future vertical slices will prove it
- task IDs use `T001`
- story labels use `US1`
- use linear/parallel/barrier only
- include verification hints
- mark each task `Agent-ready` or `Human-gated`
- use `Human-gated` when product, design, architecture, security, data, or approval decisions are still needed
- use `Agent-ready` only when acceptance, boundaries, and verification are clear enough for autonomous execution
- for large projects, group tasks by stage and barrier in a single `tasks.md`
- if complex artifact trigger conditions are met, load `complex-artifacts.md` and propose `tasks/` detail files
- detect likely durable producer-consumer boundaries such as API, event, public data, UI state/behavior, SDK/library, or runtime interfaces
- when a durable producer-consumer boundary likely exists, recommend Delivery Contract If Needed with a reason before downstream implementation relies on assumptions

Exit:

- human accepts granularity and order
- in Feature Auto-Loop, continue automatically only if remaining tasks are Agent-ready and no stop condition appears

## Delivery Contract If Needed

Entry: the human requests frontend/backend handoff, API/interface documentation, an API contract, or material for another agent/person to continue downstream work; or accepted spec/tasks, Technical Design, Review, or Drift Check reveal a likely durable producer-consumer boundary.

Load:

- `delivery-contracts.md`

Detect:

- frontend/client consuming backend API behavior
- service-to-service endpoint
- event, message, webhook, callback, or async workflow
- shared data exchange schema
- UI behavior handed from product/design/backend to frontend
- public library/plugin API
- runtime, deployment, environment-variable, or external integration boundary

Write after confirmation:

- `contracts.md`
- optional `contracts/<ID>-<slug>.md` details
- human decisions and drift notes in `notes.md`

Rules:

- keep temporary subagent assignment notes in `handoffs/`; do not use them as durable interface docs
- Delivery Contracts are not default feature artifacts
- skip Delivery Contracts for simple single-person tasks, pure internal logic, or changes with no downstream consumer
- agent proactively recommends a Delivery Contract; the human does not need to request one by name
- ask before writing contract files in every mode, including Feature Auto-Loop and Task Auto-Run
- human confirmation is required before status becomes `accepted`
- human confirmation after affected-consumer analysis is required before changing producer code, tests, or contract files for any breaking change to accepted, implemented, or verified contracts
- creating a new `draft` or `superseded` contract cannot bypass the breaking-change gate when existing consumers would observe changed behavior
- producer implementation and tests must verify the accepted contract before downstream reliance or feature close

Exit:

- no contract needed, or contract draft is ready for human decision
- accepted contract is concrete enough for Test Design and Technical Design / Code Context

## Test Design

Entry: accepted tasks.

Write:

- `tests.md`

Include:

- requirement checklist
- functional cases
- module tests
- API tests where applicable
- Web E2E/browser cases where applicable, after loading `e2e-discovery.md`
- regression tests
- manual verification
- commands
- detail test-case files under `tests/` when complex artifact mode is triggered

Rules:

- do not assume an E2E framework, local URL, account, seed, or browser tool
- if web-visible behavior exists, run E2E Discovery first
- if a task changes HTTP/API behavior, service-to-service behavior, events, background jobs, auth, persistence, or integration boundaries, API/integration verification is applicable unless a human approves a substitute verification
- if a task changes user-visible Web behavior, E2E/browser/manual verification is applicable unless a human approves a substitute verification
- substitute verification requires a recorded reason, risk, missing capability, and human decision; it cannot silently replace required API/E2E coverage
- record stable E2E capability in `project.md`
- record feature-specific E2E cases in `tests.md` or `tests/e2e/*`
- classify E2E cases as existing-framework, browser, chrome, computer-use, manual, or blocked

Exit:

- human accepts how correctness will be proven
- in Feature Auto-Loop, continue automatically only if the test strategy has no unresolved human decisions

## Technical Design / Code Context

Entry: accepted tasks and tests, before writing `plan.md` or executing a non-trivial task/story.

Load:

- `implementation-planning.md`
- `large-projects.md` for large, old, or multi-package projects
- nearest root/directory `AGENTS.md`
- relevant accepted or verified Delivery Contracts when the task crosses a producer-consumer boundary

Inspect:

- exact files likely to change
- nearby tests and fixtures
- existing functions, classes, endpoints, components, schemas, hooks, or commands
- imported helpers and existing callers
- data flow, call chain, authorization, validation, and side effects
- existing code style and error-handling patterns

Write:

- update `task-detail.md` when complex artifact mode is active
- otherwise record compact code context in `plan.md`
- unresolved technical questions in `notes.md`

Rules:

- do not invent function signatures, parameters, return shapes, or file paths
- if the context cannot be discovered from code/docs, stop and ask or mark the task `Human-gated`
- prefer existing local patterns over new abstractions
- if an interface will be created, define it explicitly before implementation
- if a durable consumer-facing interface is created or changed, load `delivery-contracts.md`, update the contract draft, and stop for human acceptance or breaking-change approval when required

Exit:

- code context is concrete enough for a construction-grade plan, or the task becomes Human-gated

## Plan If Needed

Entry: selected task/story is complex, multi-file, subagent-bound, or human requests plan.

Load:

- `implementation-planning.md`
- `external-skill-adapters.md` when Superpowers or another plan-writing skill is available

Write:

- `plan.md`

Rules:

- plan scope is `task` or `story`
- default scope is task
- assume the executor has near-zero codebase context
- include technical context, source structure decision, code context, interface contracts, data contracts when applicable, files, TDD plan, commands, expected outputs, risks
- include actual test code for RED steps when possible
- include exact function/class/endpoint/component signatures, parameters, return values, errors, and side effects for new or changed interfaces
- include exact commands and expected RED/GREEN output
- implementation steps must be bite-sized and executable
- no placeholders such as TBD, TODO, "add proper error handling", "write tests", or "similar to previous task"
- run plan self-review: spec coverage, placeholder scan, and type/signature consistency
- when Superpowers is available, use the Writing-Plans Adapter quality bar, but write to `plan.md` or `plans/*`, not external docs paths
- if complex artifact mode is active, write the full dated plan to `plans/` and keep `plan.md` as the current pointer

Exit:

- human accepts plan
- after acceptance, explain that Strict Mode asks before each stage and offer Task Auto-Run for this task/story if the human wants fewer confirmations

## Analyze Consistency

Entry: before implementation when spec/tasks/tests/plan exist.

Check:

- each accepted requirement has task coverage
- each task maps to spec or explicit technical need
- tests cover acceptance criteria
- plan scope matches selected task/story

Write:

- findings in `notes.md`
- update docs only after confirmation

Exit:

- ready for execution or revise upstream docs

## Subagent Execution If Approved

Entry: human explicitly approves subagent use for an independent task/story group, onboarding scan lane, or bounded implementation lane.

Load:

- `skill-routing.md`
- `external-skill-adapters.md`
- `templates/subagent-brief.md`

Use:

- Superpowers `subagent-driven-development` when available and appropriate

Rules:

- subagents are optional and never implied by task count alone
- ask human confirmation before dispatching subagents
- Feature Auto-Loop or Task Auto-Run approval is not subagent approval
- one confirmation may cover a bounded task group only after listing task/story IDs or scan lanes, allowed boundaries, one brief per subagent, stop conditions, and main-agent review responsibility
- verify tasks or scan lanes are independent, bounded, and reviewable by the main agent
- create one clear brief per subagent using `templates/subagent-brief.md`
- write briefs and returned summaries under `handoffs/*`
- main agent owns synthesis, review, merge decisions, and status updates
- subagents may not close a feature, submit code, update project memory directly, accept Delivery Contracts, approve breaking changes, or mark tasks `done`
- if independence, boundaries, or review responsibility are unclear, do not dispatch; continue single-agent execution or mark the work `Human-gated`

Write:

- `handoffs/<date>-<task-or-scan>-brief.md`
- `handoffs/<date>-<task-or-scan>-return.md`
- summary and evidence links in `notes.md`
- `tasks.md` status updates only after main-agent review

Exit:

- returned work reviewed and merged into agent-loop artifacts
- or subagent path declined/blocked and execution returns to single-agent mode

## Execute Task / Story

Entry: selected execution unit accepted.

Rules:

- default unit is task
- story execution requires explicit human choice
- whole-feature execution requires explicit human confirmation and only for tiny features
- in Feature Auto-Loop, execute only Agent-ready tasks and stop at Human-gated tasks
- in Task Auto-Run, execute only the selected task/story and stop after evidence/review/drift updates and Task Done Gate status update
- TDD by default
- when Superpowers is available, use the TDD Adapter, but task status and evidence remain controlled by agent-loop
- verify RED before implementation
- verify GREEN after implementation
- record evidence
- after implementation and all applicable fresh verification, set task status to `review`, not `done`
- if only partial verification ran, keep the task `in-progress` or `blocked` and record the missing verification
- mark task `done` only after Task Done Gate passes: evidence recorded, required review recorded, drift decision recorded, and task status linked to evidence

Write:

- code/tests
- `tasks.md` status
- `notes.md` TDD cycles and evidence
- `notes.md` review and drift records before `done`

Exit:

- execution unit in review, done, blocked, or needs diagnosis

## Diagnose Failure

Entry: test/build/E2E/behavior failure.

Load:

- `external-skill-adapters.md` when Superpowers or another systematic debugging skill is available

Rules:

- when Superpowers is available, use the Debugging Adapter and find root cause before proposing fixes
- reproduce before fixing
- find root cause
- form one hypothesis at a time
- write regression test when possible

Write:

- diagnosis in `notes.md`

Exit:

- fix verified or blocker escalated

## Verify

Entry: before any completion claim.

Load:

- `external-skill-adapters.md` when Superpowers or another verification skill is available

Rules:

- when Superpowers is available, use the verification adapter, but completion is still controlled by agent-loop
- identify proof command/action
- run fresh verification
- read output
- record evidence

Write:

- `notes.md` verification evidence

Exit:

- claim may be made only if evidence supports it
- if the feature may now be complete, continue to Review, Drift Check, Project Memory Update, then Feature Completion Check

## Review

Entry: after implementation and verification, before any task is marked `done`, before Submit / Integrate, and before recommending or performing feature close.

Load:

- `external-skill-adapters.md` when Superpowers or another code-review skill is available

Check:

- Spec Review: implementation matches `product.md` when present, `spec.md`, acceptance criteria, scope, and out-of-scope
- Standards Review: implementation follows root/directory `AGENTS.md`, `project.md` rules, directory boundaries, testing rules, and local code conventions
- test adequacy
- integration risk
- unrelated changes
- Delivery Contract alignment when producer-consumer boundaries exist

Rules:

- when Superpowers is available, use the review adapter, but findings must be recorded in `notes.md` and cannot directly mark tasks `done`
- perform lightweight Spec Review for every task before marking it `done`
- perform Feature Close Review before recommending or performing close
- Feature Close Review includes feature-level Spec Review against product/spec/tasks/tests/acceptance/out-of-scope
- before Submit / Integrate, perform at least Spec Review
- perform Standards Review for large projects, broad diffs, directory boundary changes, security/data changes, or human request
- perform feature-level Standards Review before close when the feature is large, broad, boundary-changing, security/data-related, architecture-changing, or human-requested
- record the two axes separately so one does not hide the other
- if required review is missing, the task remains `review`; do not mark it `done`
- compare producer code and tests with Delivery Contracts; identify affected consumers before accepting interface drift

Write:

- task review findings and accepted fixes in `notes.md` under Spec Review and Standards Review
- close review findings and accepted fixes in `notes.md` under Feature Close Review

Exit:

- continue to Drift Check, revise implementation, or diagnose failures

## Drift Check

Entry: after implementation or before close.

Check:

- implementation vs `spec.md`
- completed work vs `tasks.md`
- test reality vs `tests.md`
- long-term changes vs `project.md`
- producer-consumer interfaces vs `contracts.md` and linked `contracts/*` details when present
- human original requirements vs current implementation when relevant
- whether long-term startup guidance changed and `AGENTS.md` should be synced

Write after confirmation:

- feature docs for feature drift
- `project.md` for long-term project facts
- `notes.md` drift record
- `contracts.md` and matching `contracts/*` details for interface drift; ask before accepting breaking changes
- `AGENTS.md` / `CLAUDE.md` only for long-term guidance changes

Exit:

- docs and code reality aligned enough to continue/close

## Project Memory Update

Entry: after Drift Check, before Submit / Integrate, Pause, or Close when long-term project facts changed.

Load:

- `project-memory-mode.md`

Update only durable project facts:

- current work and next suggested action
- active or paused feature pointers
- product context when feature product decisions affect future features
- capabilities that now exist or changed
- tech stack, commands, or tooling changes
- directory map or guidance status changes
- domain language that future feature work should reuse
- known constraints and long-term decisions
- onboarding uncertainties resolved by code reality

Do not write:

- task execution logs
- raw test output
- temporary implementation notes
- original human requirements or prototypes

Write after confirmation:

- `project.md` in simple mode
- `project.md` plus the matching `project/*.md` detail files in enterprise mode
- root or directory `AGENTS.md` only if startup guidance changed and human confirms

Exit:

- future agents can resume from `project.md` and, in enterprise mode, only the linked detail files relevant to the next stage

## Submit / Integrate

Entry: after Verify, Review, Drift Check, and Project Memory Update when human asks to submit, commit, prepare PR text, or package work for integration.

Load:

- `submit-and-integrate.md`
- `external-skill-adapters.md` when Superpowers or another finishing/branch skill is available

Rules:

- inspect diff and untracked files
- separate product code changes from `agent-loop` artifact changes
- identify unrelated dirty work
- if using an external finishing skill, use it only for completion options and branch hygiene; agent-loop still owns the submit gate
- never commit, create final PR text, merge, release, publish, or claim submission readiness without human confirmation
- a human saying "commit" starts Submit / Integrate but is not final commit approval; ask again after diff, verification, review, and drift summary
- default to prepare-only if the human has not explicitly requested commit/PR/merge

Write after confirmation:

- `notes.md` submit/integrate record
- commit only if explicitly confirmed

Exit:

- recommend Close if feature is done
- recommend next task/story if work remains
- recommend Pause if submit is prepared but not performed

## Feature Completion Check

Entry: after Verify/Review/Drift Check/Project Memory Update when a feature may be done; before starting a new feature while another is active; or on resume when an Active Feature exists.

Load:

- `feature-completion-check.md`

Read:

- `project.md` Current Work
- active feature `spec.md`
- active feature `tasks.md`
- active feature `tests.md`
- active feature `plan.md`
- active feature `notes.md`

Check:

- accepted spec
- all in-scope tasks done, skipped with reason, or removed from scope
- required tests or substitute verification recorded
- fresh verification evidence exists
- Feature Close Review completed
- feature-level Spec Review confirms product/spec/tasks/tests/acceptance and out-of-scope boundaries
- feature-level Standards Review completed when triggered by large project, broad diff, boundary/security/data change, architecture change, or human request
- drift check completed
- long-term memory updated
- submit/integration status recorded when requested
- no unresolved Human-gated decisions or blockers

Write:

- `notes.md` Feature Completion Check record
- `project.md` Current Work / Next Suggested Action update after confirmation if state changes

Exit:

- recommend Close if complete, but ask explicit human confirmation before closing
- recommend next unfinished item if incomplete
- recommend Pause before new feature if human wants to switch context
- recommend scope update if remaining work should be removed before close

## Pause / Close

Pause writes:

- current state
- next action
- blockers
- touched files
- resume point

Close requires:

- fresh verification evidence
- Feature Close Review
- drift check
- submit/integration status recorded if the human requested submission
- long-term memory update
- explicit human confirmation

Write:

- `notes.md` close record
- `project.md` current work update

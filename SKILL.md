---
name: agent-loop
description: Use when starting, continuing, resuming, structuring, testing, implementing, verifying, submitting, pausing, or closing a single-person agent-assisted software development workflow.
---

# Agent Loop

Version: 1.0.0

Run a single-human, CLI-agent development loop from goal intake to verified close. This skill is a controller: it decides the current stage, loads the right reference, produces or updates `agent-loop` artifacts, and stops at human gates.

## Design Source Rule

This skill must stay aligned with the repo design sources:

```text
dratf_agent_loop_struct.md
final_agent_loop_skill_design.md
```

The references in this skill are operational extracts from those files. If this skill conflicts with either design source, the design source wins and the skill should be updated. New additions, including large-project behavior, may only extend the design without changing its core model, directory structure, stage order, or first-version exclusions.

## Non-Negotiable Rule

Every time this skill is used, first load:

```text
references/runtime.md
references/design.md
```

Then follow the runtime protocol under the design source constraints. Do not skip directly to writing code, creating tasks, or closing work.

## When To Use

Use this skill when the user wants to:

- initialize agent-managed development in a new or existing project
- re-adopt an old `agent-loop` project after code changed without updating `agent-loop` docs
- turn requirements or prototypes into feature specs, tasks, tests, plans, and implementation
- continue a paused feature or recover project context
- reconcile `agent-loop` documents with code reality
- execute a task/story with TDD and verification
- submit, pause, resume, or close a feature

Do not use for one-off edits when the user explicitly asks to bypass workflow and the edit does not affect feature behavior, public interfaces, data/security boundaries, project memory, submit, or close state. First version is single-person only: no multiplayer workflow, no roadmap graph, no roadmap adapter, no tdd-guard.

## Skill Package Map

Read only what the current stage needs.

```text
references/runtime.md              required first; loop protocol and state machine
references/design.md               condensed extract of the repo source design
references/concepts.md             definitions and scope boundaries
references/project-guidance.md     root and directory AGENTS/CLAUDE guidance rules
references/project-memory-mode.md  simple vs enterprise project memory rules
references/project-architecture-init.md DDD-inspired architecture and stack adapter rules
references/remote-project-discovery.md local entry + remote project discovery rules
references/requirement-management.md     human source requirement archive rules
references/product-brief.md        feature product brief and product consensus rules
references/delivery-contracts.md   durable producer-consumer interface handoff rules
references/e2e-discovery.md        Web E2E environment discovery and recording rules
references/large-projects.md       rules for complex or 100k+ LOC projects
references/existing-project-onboarding.md layered scan for taking over old projects
references/complex-artifacts.md    triggered tasks/tests/plans directory mode
references/implementation-planning.md construction-grade task/story planning rules
references/recovery-and-backfill.md code-reality recovery and document backfill protocol
references/feature-completion-check.md proactive close/pause/continue checks for active features
references/human-review-summary.md table-first approval summaries for human gates
references/stage-guides.md         stage-by-stage procedures
references/artifact-rules.md       artifact ownership, drift, status, and naming
references/skill-routing.md        optional preferred skills and fallback behavior
references/submit-and-integrate.md explicit git submit / commit / PR gate
references/validation-scenarios.md pressure scenarios for checking this skill works
references/document-templates.md   inline markdown templates
references/workflow-checklists.md  checklist form for each stage
templates/                         copy-ready artifact templates
examples/login-feature/            small finished feature workspace
examples/complex-saas-project/     larger takeover + feature execution workspace
examples/remote-entry/             local empty directory pointing to a remote project
CHANGELOG.md                        skill maintenance history; append meaningful future changes
```

## Required Runtime Behavior

1. Inspect `agent-loop/`; if missing, also check legacy `.agent-loop/`.
2. Classify the entry scenario.
3. Load the stage guide for the current scenario.
4. Load `references/project-guidance.md` during project init/onboarding or when long-term agent instructions may need sync.
5. Load `references/project-memory-mode.md` during init, onboarding, re-adoption, drift check, project memory update, or when `project.md` is large, hard to read, or likely insufficient for future continuation.
6. Load `references/project-architecture-init.md` during init/onboarding, when proposing project structure, when recording architecture profile, or when a task creates durable code boundaries.
7. Load `references/remote-project-discovery.md` when the human says the project is remote, local files contain remote-entry hints, or local/remote/container execution is unclear. Do not treat an empty local directory alone as remote.
8. Load `references/requirement-management.md` before copying, moving, renaming, indexing, or referencing human source requirements.
9. Load `references/product-brief.md` when a feature needs product intent, product consensus, user stories, product scope, or PRD-like synthesis.
10. Load `references/e2e-discovery.md` before designing or executing Web E2E/browser verification.
10a. Load `references/delivery-contracts.md` when the human requests cross-boundary handoff/API/interface documentation, or when the agent detects a likely downstream consumer boundary such as frontend/backend, service, event, public data, SDK/library, UI state, or runtime behavior. Delivery Contracts are not created by default.
11. Load `references/existing-project-onboarding.md` when taking over an existing project without reliable `agent-loop` memory.
12. Load `references/large-projects.md` when the repo is large, old, unfamiliar, multi-package, or likely above 100k LOC.
13. Load `references/complex-artifacts.md` when story/task/test/plan complexity crosses its trigger conditions.
14. Load `references/implementation-planning.md` before writing or approving `plan.md` for a task/story.
15. Load `references/recovery-and-backfill.md` when project memory is missing, stale, incomplete, when continuing work from code reality, or when re-adopting a project after development happened outside `agent-loop`.
16. Load `references/feature-completion-check.md` after verification/project-memory updates, before starting a new feature when another is active, and when resuming an active feature that may already be complete.
17. Load `references/human-review-summary.md` before asking the human to approve or confirm a stage, unless the confirmation is trivial enough for a 3-line summary.
18. Load `references/skill-routing.md` when a stage might benefit from an external or platform skill.
19. Load `references/submit-and-integrate.md` before creating commits, PR text, merge notes, or any submission claim.
20. Summarize current state in the response.
21. Recommend exactly one next stage.
22. Ask for human confirmation before mutating files, crossing stages, or enabling an auto mode.
23. After the stage, update artifacts, summarize evidence, and ask whether to continue, revise, pause, submit, or close.

## Artifact Layout

```text
agent-loop/
  remote.md optional local-entry pointer for remote projects
  project.md
  project/ optional enterprise memory detail files
  requirements/
    <archive-date>-<topic>/
      README.md
      requirement.*
      prototype.*
      feedback.*
      notes.*
  features/
    <date>-<feature-slug>/
      product.md optional product brief
      spec.md
      tasks.md
      tests.md
      plan.md
      notes.md
      contracts.md optional cross-boundary delivery contract index
      tasks/   optional complex artifact details
      tests/   optional complex test-case details
      plans/   optional dated plan-cycle details
      handoffs/ optional subagent briefs and returns
      contracts/ optional delivery contract details
```

`agent-loop/` is the human-friendly default. If an older project already has `.agent-loop/`, read it and ask before migrating or renaming.

If the local directory is only a remote-project entry point, create only thin local entry memory after confirmation: `agent-loop/remote.md` plus a thin `project.md` with `Status: remote-entry`. Put full project memory next to the remote source of truth when remote writes are allowed; otherwise use local-shadow mode and label every code fact with remote evidence.

## Execution Defaults

- Default execution unit: one task.
- Story execution requires explicit human choice.
- Whole-feature execution requires explicit human confirmation and only fits tiny features.
- A feature may contain many stories and many tasks; `tasks.md` is the feature task ledger.
- Use `product.md` for feature-level product intent when needed; durable cross-feature product consensus belongs in `project.md` Product Context.
- Do not create `contracts.md` or `contracts/` by default. Use them only for durable producer-consumer delivery boundaries such as API, event, public data, UI state/behavior, SDK/library, or runtime interfaces.
- Create or update Delivery Contract files only after human confirmation. The agent may proactively recommend one when it detects downstream impact, but simple single-person tasks, pure internal logic, and changes with no downstream consumer should skip contracts.
- During Work Breakdown, Technical Design / Code Context, Plan, Review, and Drift Check, detect whether a Delivery Contract should be recommended.
- Feature Auto-Loop and Task Auto-Run do not silently create Delivery Contract files. They must pause before contract file creation, contract acceptance, or breaking contract changes.
- Keep temporary subagent assignment notes in `handoffs/`.
- `plan.md` is the active plan for the current task/story, not the default whole-feature plan.
- If `plan.md` is created, it must be construction-grade: exact paths, code context, interfaces, parameters, test code, commands, expected RED/GREEN output, and self-review.
- Do not date the core `plan.md` filename. Date each plan cycle with `Plan ID`, `Created`, `Updated`, and record completed plan cycles in `notes.md`.
- In complex artifact mode, `tasks.md`, `tests.md`, and `plan.md` become stable indexes that link to detailed files under `tasks/`, `tests/`, and `plans/`.
- In complex projects, every task plan must name boundaries, files/areas to inspect, verification commands, and rollback notes.
- A task cannot be marked `done` from implementation alone. After code changes, move the task to `review` until fresh test/verification evidence, required review, and drift decision are recorded.
- Task Done Gate: mark a task `done` only after implementation is complete, required tests or substitute verification have run fresh, evidence is recorded in `notes.md`, lightweight Spec Review is recorded, Standards Review is recorded when triggered, drift decision is recorded, and `tasks.md` links or names the evidence.
- During large-project onboarding, recommend bounded subagent scanning when available and human-confirmed; otherwise use single-agent layered scan.
- When local and remote project reality are split, discover the remote environment before onboarding or initializing project memory.
- Historical execution evidence belongs in `notes.md`.
- Web E2E capability is discovered from the real project environment. Stable E2E capability belongs in `project.md`; feature-specific E2E cases belong in `tests.md` or `tests/e2e/*`.
- Human source requirements are archived as requirement set directories, not new flat files. Each requirement set groups the human's requirement, prototype, feedback, screenshots, recordings, links, and follow-up notes for one intake event or topic.
- `agent-loop/requirements/` is canonical. Legacy `agent-loop/inputs/` is read-only compatibility; if present, recommend migration before new feature work and ask human confirmation before moving files or updating references.
- Human source requirement archive dates mean archive date only; never infer deadlines, scope duration, or lifecycle from input paths.
- Project Memory Mode is either `simple` or `enterprise`. Default to simple. Recommend enterprise when any hard trigger applies, including about 200k+ LOC, 5+ durable boundaries, 2+ test systems, 3+ execution environments, `project.md` above about 600 lines, repeated re-scans, or 5+ directory-level guidance files.
- In enterprise mode, `project.md` is an index and current-state summary. Long-term project knowledge moves into optional `agent-loop/project/*.md` files created only after human confirmation and only when useful.
- Architecture is DDD-inspired by default: domain language first, bounded contexts, business rules outside UI glue, application/use-case orchestration, and infrastructure adapters for external systems.
- Code layout suggestions are reference scaffolds, not mandates. Adapt them to project shape, language, framework conventions, and existing code reality. New projects may scaffold after confirmation; existing projects are recorded as-is unless the human explicitly approves refactoring.
- During recovery/backfill, code reality is the current fact base for agent-maintained docs, but human original requirements are never overwritten.
- During re-adoption, do not start new feature work first. Compare current code/tests/scripts against existing `agent-loop` memory, propose backfill, ask human confirmation, then resume or start feature work.
- Root `AGENTS.md` and `CLAUDE.md` are default project guidance artifacts for new/onboarded projects, created only after human confirmation.
- Root and directory guidance language follows the project language when clear; default to English only when project language is unclear. Preserve stable artifact names, stage names, and file paths in English.
- Directory-level `AGENTS.md` is proposed for new or existing long-lived boundary directories, created only after human confirmation.
- Strict Mode is default: ask before and after every stage.
- Feature Auto-Loop may run Agent-ready feature work after Feature Spec acceptance and explicit human confirmation.
- Task Auto-Run may run one task/story after its plan is accepted and explicit human confirmation.
- If the human appears slowed down by repeated confirmations, or when starting a feature/task execution lane, proactively explain the available gate modes and recommend either Feature Auto-Loop or Task Auto-Run when safe.
- Auto modes stop at Human-gated work, unclear decisions, risky changes, failed verification, drift needing approval, Delivery Contract acceptance or breaking changes, directory guidance changes, subagent approval, submit, pause, or close.
- Human confirmations should use table-first Human Review Summary by default; full artifacts remain the source of truth.
- Root `AGENTS.md` / `CLAUDE.md` guidance must tell future agents to own the workflow: classify the stage, recommend one next action, propose missing artifacts, and keep responsibility for sequencing, diagnosis, verification, drift checks, and project-memory updates.
- Root guidance must also explain autonomous execution after approval: Feature Auto-Loop may continue Agent-ready feature work after accepted Feature Spec and explicit enablement; Task Auto-Run may complete one accepted task/story plan through TDD, implementation, verification, bug fixing, review, drift, status update, and final report.
- TDD is default: RED, verify RED, GREEN, verify GREEN, refactor.
- No completion claim without fresh verification evidence.
- Submit requires fresh verification, drift check, diff review, human confirmation, and a recorded submit note.
- The agent must proactively run Feature Completion Check after likely completion, before starting a new feature with an active feature present, and on resume when an active feature may already be done.
- Feature Close Review is required before recommending or performing close: feature-level Spec Review must confirm product/spec/tasks/tests/acceptance are satisfied; feature-level Standards Review is required for large projects, broad diffs, boundary/security/data changes, architecture changes, or human request.
- Close requires verification, Feature Close Review, drift check, project memory update, optional submit status, and explicit human confirmation.

## Stage Skill Routing

The controller owns the loop. External skills are optional stage accelerators.

- Clarify: use a brainstorming skill if available.
- Product Brief: use PRD/product discovery or grill-with-docs style skills if available.
- Planning: use a plan-writing skill if available.
- Implementation: use a TDD skill if available.
- Failure: use a systematic debugging skill if available.
- Completion: use verification/review/finishing skills if available.

If no external skill exists, continue with the fallback procedures in `references/stage-guides.md`. Never expose external command systems to the human as required knowledge.

## Stop And Ask

Stop when:

- intent or scope cannot be resolved from files
- project memory and code reality materially disagree
- a stage would modify human original requirements
- the task needs non-TDD execution
- verification repeatedly fails
- submit is requested without evidence, drift check, diff review, or human confirmation
- close is requested without evidence or drift check
- the work would require first-version exclusions

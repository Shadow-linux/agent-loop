---
name: agent-loop
description: Use when starting, continuing, resuming, structuring, testing, implementing, verifying, submitting, pausing, or closing a single-person agent-assisted software development workflow.
---

# Agent Loop

Version: 1.2.4

Run a single-human, CLI-agent development loop from goal intake to verified close. This skill is a controller: it decides the current stage, loads the right reference, produces or updates `agent-loop` artifacts, and stops at human gates.

## Design Source Rule

This skill must stay aligned with the repo design sources:

```text
draft_agent_loop_struct.md
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

Also treat root project guidance as the agent bootstrap layer. When working inside a target project, check root `AGENTS.md` and `CLAUDE.md` status during Project Entry before feature work. If root guidance is missing, stale, duplicated, or not pointing through `AGENTS.md`, load `references/project-guidance.md` and propose a fix through human confirmation.

Also treat long-term memory indexes as claims that must be verified before reliance. If `project.md`, root guidance, or a current artifact points to `.agent-loop/onboarding-db/`, enterprise `project/*.md`, feature docs, contracts, or guidance files that are missing, stale, contradictory, or not human-reviewed as claimed, classify the entry as `stale-memory`, load `references/recovery-and-backfill.md`, and recommend the smallest reconcile/backfill before relying on those docs or starting feature work.

## Message Intent Guard

Before project-state classification, classify the latest human message intent. `chat` means ordinary discussion, rules questions, status questions, or design talk; answer or discuss only and do not create requirement sets or feature workspaces by default. Message intent is not permanent: if chat turns into demand shaping, `proposal-doc`, implementation, operational support, follow-up, or deferred work, reclassify and route accordingly. If the human explicitly wants discussion without documentation, keep `chat`. `requirements-discussion` means the human is shaping product needs, business goals, capability ideas, constraints, tradeoffs, or user scenarios without authorizing implementation; use Brainstorm / Clarify to produce a human-reviewed requirement document under `.agent-loop/requirements/` before feature construction. If unclear, ask whether the human wants ordinary discussion, requirements documentation, or feature implementation.

## Human Help And Version Questions

When the human asks what changed in a version, what is new, how to use agent-loop, how to trigger a capability, or how behavior differs across versions:

- use `CHANGELOG.md` as the source of truth for version changes
- use `Usage.md` as the source of truth for human-facing usage examples and trigger phrases
- use `README.md` for high-level overview, install, and quick-start explanation
- answer from those docs instead of memory
- if the question names a version, read that version section first
- if the question asks how to use agent-loop, summarize in human wording from `Usage.md`

## Mandatory Stage Helper Protocol

Seven stages are mandatory helper-backed stages when a matching helper is exposed by the runtime: Brainstorm / Clarify, Plan Gate / Plan, Execute Task / Story, Diagnose Failure, Verify, Review / Feature Close Review, and approved Subagent Execution.

Before any action in one of these stages, load `references/skill-routing.md` and `references/external-skill-adapters.md`, resolve the canonical Superpowers name and supported alias, and load the complete helper `SKILL.md`. A mandatory helper-backed stage cannot start stage actions until resolution status is `loaded`, `unavailable`, or `load-failed`. Fallback is allowed only for `unavailable` or `load-failed`.

Record every resolution in the current feature `notes.md`, including candidates checked, resolved helper, status, fallback, and agent-loop overrides. If no feature workspace is confirmed, use the response-local pending-record rule in `skill-routing.md`; never create a feature merely for helper logging. A mandatory helper-backed stage cannot complete without a Stage Helper Resolution record.

The helper improves the method only. Agent-loop remains the controller: its artifact paths, human gates, task and feature status, project memory, drift, submit, pause, and close rules override helper defaults. Never create native helper output directories such as `docs/superpowers/` unless the human explicitly requests them and separately confirms after the path override is explained.

## When To Use

Use this skill when the user wants to:

- initialize agent-managed development in a new or existing project
- re-adopt an old `agent-loop` project after code changed without updating `agent-loop` docs
- answer workflow/project questions without turning chat into feature work
- shape product needs through requirements-discussion into requirement documents under `.agent-loop/requirements/`
- turn requirements or prototypes into feature specs, tasks, tests, plans, and implementation
- use existing project code, configuration, scripts, or deployment docs to support operational testing, rollout, account/config/model switching, production diagnosis, or runbook/checklist creation without defaulting to code changes
- continue a paused feature or recover project context
- reconcile `agent-loop` documents with code reality
- execute a task/story with TDD and verification
- submit, pause, resume, or close a feature

Do not use for one-off edits when the user explicitly asks to bypass workflow and the edit does not affect feature behavior, public interfaces, data/security boundaries, project memory, submit, or close state.

First version excludes: multiplayer workflow, roadmap graph, roadmap adapter, tdd-guard, complex ADR system, global skill installation, automatic directory-level `AGENTS.md` generation without human confirmation, and automatic commit/PR/merge/release/publish without human confirmation.

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
references/requirement-product-grill.md requirement/product clarification method for ambiguous terminology, flows, prior feature conflicts, and decision signals
references/project-decisions.md   Decision Scan / Placement and optional project-level ADR rules
references/product-brief.md        feature product brief and product consensus rules
references/delivery-contracts.md   durable producer-consumer interface handoff rules
references/e2e-discovery.md        Web E2E environment discovery and recording rules
references/large-projects.md       rules for complex or 100k+ LOC projects
references/project-entry-scan.md Project Entry Scan for taking over old projects safely
references/onboarding-knowledge-base.md Evidence-Graph + DDD newcomer project understanding rules
references/feature-follow-up.md          bug/change flow-back to recent features
references/complex-artifacts.md    triggered tasks/tests/plans directory mode
references/implementation-planning.md construction-grade task/story planning rules
references/recovery-and-backfill.md code-reality recovery and document backfill protocol
references/feature-completion-check.md proactive close/pause/continue checks for active features
references/human-review-summary.md table-first approval summaries for human gates
references/stage-guides.md         stage-by-stage procedures
references/artifact-rules.md       artifact ownership, drift, status, and naming
references/skill-routing.md        optional preferred skills and fallback behavior
references/external-skill-adapters.md stage plugin rules for Superpowers and other external skills
references/submit-and-integrate.md explicit git submit / commit / PR gate
references/validation-scenarios.md pressure scenarios for checking this skill works
references/document-templates.md   inline markdown templates
references/workflow-checklists.md  checklist form for each stage
scripts/check-root-agents-blocks.sh read-only root AGENTS managed-block drift checker
templates/                         copy-ready artifact templates
examples/login-feature/            small finished feature workspace
examples/complex-saas-project/     larger takeover + feature execution workspace
examples/remote-entry/             local empty directory pointing to a remote project
README.md                           human overview, install, and quick-start source
Usage.md                            human-facing trigger phrase and usage guide
CHANGELOG.md                        version-change source of truth for "what changed" questions
```

## Required Runtime Behavior

1. Inspect `.agent-loop/`; if missing, also check legacy `agent-loop/`.
2. Check root `AGENTS.md` / `CLAUDE.md` as the Root Agent Bootstrap Gate; if either is missing or stale, load `references/project-guidance.md` and include the guidance repair in the recommended Project Entry action unless the human has explicitly deferred it.
3. Classify the latest message intent: `chat`, `requirements-discussion`, `feature-request`, `operational-support`, `feature-follow-up`, `deferred-requirement`, or `unknown`.
3a. For `chat`, answer or discuss only; do not create requirement sets, feature workspaces, tasks, tests, or plans.
3b. For `requirements-discussion`, load `references/requirement-management.md`, use Brainstorm / Clarify, produce a human-reviewed requirement document, and archive it under `.agent-loop/requirements/<archive-date>-<topic>/` after confirmation before any feature construction.
3c. Classify the entry scenario.
4. Load the stage guide for the current scenario.
4a. Run Stage Helper Capability Scan for the current stage. For a mandatory helper-backed stage, load `references/skill-routing.md` and `references/external-skill-adapters.md`, resolve canonical and alias names, load the complete helper before stage actions when found, and record the resolution. Use fallback only after recording `unavailable` or `load-failed`.
5. Load `references/project-guidance.md` during project init, Project Entry Scan, or re-adoption, when root guidance is missing/stale, or when long-term agent instructions may need sync.
6. Load `references/project-memory-mode.md` during init, Project Entry Scan, re-adoption, drift check, project memory update, or when `project.md` is large, hard to read, or likely insufficient for future continuation.
7. Load `references/project-architecture-init.md` during init or Project Entry Scan, when proposing project structure, when recording architecture profile, or when a task creates durable code boundaries.
8. Load `references/remote-project-discovery.md` when the human says the project is remote, local files contain remote-entry hints, or local/remote/container execution is unclear. Do not treat an empty local directory alone as remote.
9. Load `references/requirement-management.md` before copying, moving, renaming, indexing, or referencing human source requirements.
9a. Load `references/requirement-product-grill.md` during Requirements Discussion, Product Brief, or Brainstorm / Clarify when requirements include ambiguous terminology, domain boundaries, business flows, exception paths, conflicting prior feature behavior, or decision signals. Grill questions clarify input only; they do not create PRDs, ADRs, project memory, `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/`.
9b. Load `references/project-decisions.md` when Decision Scan / Placement is needed: complex accepted requirements before Feature Spec, product tradeoffs, cross-feature or long-term decision candidates, architecture/data/runtime boundary choices, or drift that changes durable project facts. Decision Scan may start early, but `.agent-loop/decisions/` files are optional Human-gated artifacts and are usually created after requirement acceptance and before feature spec synthesis for complex requirements.
10. Load `references/product-brief.md` when a feature needs product intent, product consensus, user stories, product scope, or PRD-like synthesis.
11. Load `references/e2e-discovery.md` before designing or executing Web E2E/browser verification.
12. Load `references/delivery-contracts.md` when the human requests cross-boundary handoff/API/interface documentation, or when the agent detects a likely downstream consumer boundary such as frontend/backend, service, event, public data, SDK/library, UI state, or runtime behavior. Delivery Contracts are not created by default.
13. Load `references/project-entry-scan.md` when taking over an existing project without reliable `agent-loop` memory. This is now a Project Entry Scan only: build safe project memory, guidance status, commands, boundaries, and uncertainties. Do not create `.agent-loop/onboarding-db/`, module docs, flow docs, onboarding diagrams, or old Quick / Deep / Targeted onboarding artifacts during Project Entry Scan.
13a. Load `references/onboarding-knowledge-base.md` when the human asks for newcomer-facing docs, durable project understanding, guided learning paths, or onboarding-db construction. Run it only after Project Entry Scan or reliable project memory. Use Evidence Graph first, then accepted Onboarding Spec, Onboarding Tasks, single-file module/flow docs by default, wireframe architecture flow diagrams as the preferred flow expression, coverage scoring, and reviewed batches.
14. Load `references/feature-follow-up.md` when the human reports a bug, regression, post-close correction, field/schema change, algorithm change, API mismatch, screenshot issue, behavior tweak, "small tweak", test failure, or QA/user feedback that may belong to a recent feature.
15. Load `references/large-projects.md` when the repo is large, old, unfamiliar, multi-package, or likely above 100k LOC.
16. Load `references/complex-artifacts.md` when story/task/test/plan complexity crosses its trigger conditions.
17. Load `references/implementation-planning.md` before writing or approving `plan.md` for a task/story.
18. Load `references/recovery-and-backfill.md` when project memory is missing, stale, incomplete, when continuing work from code reality, or when re-adopting a project after development happened outside `agent-loop`.
18a. Load `references/recovery-and-backfill.md` when `project.md` or root guidance claims legacy onboarding-db exists, is expanded/reviewed, or should be the newcomer entrypoint, but `.agent-loop/onboarding-db/README.md` or indexed onboarding-db files are missing, stale, or contradictory. Treat legacy onboarding-db as evidence only; do not run a guided onboarding flow.
19. Load `references/feature-completion-check.md` after verification/project-memory updates, before starting a new feature when another is active, and when resuming an active feature that may already be complete.
20. Load `references/human-review-summary.md` before asking the human to approve or confirm a stage, unless the confirmation is trivial enough for a 3-line summary.
21. Load `references/skill-routing.md` before every mandatory helper-backed stage and before fallback for any other helper-friendly stage.
22. Load `references/external-skill-adapters.md` before every mandatory helper-backed stage. Agent-loop paths, gates, task status, project memory, submit, pause, and close rules override external skill defaults.
22a. Before leaving a mandatory helper-backed stage, verify its Stage Helper Resolution record exists and that fallback was used only with `unavailable` or `load-failed`.
23. Load `references/submit-and-integrate.md` before creating commits, PR text, merge notes, or any submission claim.
24. Summarize current state in the response.
25. Recommend exactly one next stage.
26. Ask for human confirmation before mutating files, crossing stages, or enabling an auto mode.
27. After the stage, update artifacts, summarize evidence, and ask whether to continue, revise, pause, submit, or close.

## Artifact Layout

```text
.agent-loop/
  remote.md optional local-entry pointer for remote projects
  project.md
  project/ optional enterprise memory detail files
  decisions/ optional project / cross-feature decision records
  onboarding-db/ Evidence-Graph + DDD human-readable project understanding docs; legacy layouts are evidence only until migrated
  requirements/
    <archive-date>-<topic>/
      README.md
      requirement.* optional source file when provided
      prototype.* optional source file when provided
      feedback.* optional source file when provided
      notes.* optional source file when provided
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

`.agent-loop/` is the hidden default for target projects. If an older project already has `agent-loop/`, read it and ask before migrating or renaming.

If the local directory is only a remote-project entry point, create only thin local entry memory after confirmation: `.agent-loop/remote.md` plus a thin `project.md` with `Status: remote-entry`. Put full project memory next to the remote source of truth when remote writes are allowed; otherwise use local-shadow mode and label every code fact with remote evidence.

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
- After task/story selection and before Execute Task / Story, the agent must pass Plan Gate. It may not create tasks and immediately implement.
- Plan Gate has exactly two outcomes: accepted `plan.md` / `plans/*`, or a recorded No-Plan Decision for a trivial task. Task Auto-Run always requires an accepted plan; No-Plan Decision is not enough for Task Auto-Run.
- If `plan.md` is created, it must be construction-grade: exact paths, code context, interfaces, parameters, test code, commands, expected RED/GREEN output, and self-review.
- Do not date the core `plan.md` filename. Date each plan cycle with `Plan ID`, `Created`, `Updated`, and record completed plan cycles in `notes.md`.
- In complex artifact mode, `tasks.md`, `tests.md`, and `plan.md` become stable indexes that link to detailed files under `tasks/`, `tests/`, and `plans/`.
- In complex projects, every task plan must name boundaries, files/areas to inspect, verification commands, and rollback notes.
- A task cannot be marked `done` from implementation alone. After code changes, move the task to `review` until fresh test/verification evidence, required review, and drift decision are recorded.
- Task Done Gate: mark a task `done` only after implementation is complete, required tests or substitute verification have run fresh, evidence is recorded in `notes.md`, lightweight Spec Review is recorded, Standards Review is recorded when triggered, drift decision is recorded, and `tasks.md` links or names the evidence.
- During large Project Entry Scan, recommend bounded subagent scanning when available and human-confirmed; otherwise use single-agent layered scan.
- During existing-project Project Entry Scan, create or propose only safe project memory, root guidance status, commands, boundaries, capabilities, and uncertainties. Do not create onboarding-db detail docs, module docs, flow docs, onboarding diagrams, onboarding-spec, or onboarding-tasks during Project Entry Scan.
- During Evidence-Graph + DDD Onboarding, create or update onboarding-db only through `references/onboarding-knowledge-base.md`: build Evidence Graph, confirm Onboarding Spec, write Onboarding Tasks, then produce reviewed batches with single-file module/flow docs by default, wireframe architecture flow diagrams, coverage scoring, and no placeholder files.
- When Project Entry Scan discovers stable project facts missing from project memory, propose or perform project memory backfill after human confirmation.
- For focused questions about one module, flow, async task, deployment path, or problem area, answer from existing docs/code as chat or operational support unless the human explicitly authorizes feature/fix work. Do not create focused onboarding-db artifacts.
- When local and remote project reality are split, discover the remote environment before Project Entry Scan or initializing project memory.
- Historical execution evidence belongs in `notes.md`.
- Web E2E capability is discovered from the real project environment. Stable E2E capability belongs in `project.md`; feature-specific E2E cases belong in `tests.md` or `tests/e2e/*`.
- Human source requirements are archived as requirement set directories, not new flat files. Each requirement set groups the human's requirement, prototype, feedback, screenshots, recordings, links, and follow-up notes for one intake event or topic.
- `.agent-loop/requirements/` is canonical. Do not create or maintain legacy `inputs/` archives in current-version projects.
- Human source requirement archive dates mean archive date only; never infer deadlines, scope duration, or lifecycle from input paths.
- Requirements created from requirements-discussion live under `.agent-loop/requirements/`; feature `product.md` and `spec.md` only derive from and link to requirement sets, and do not own requirement lifecycle.
- For complex requirements, recommend requirement-level `Delivery Phases` in the requirement set `README.md` before feature construction when the human needs to confirm staged delivery. Phases express human-readable delivery slices; they are not feature workspaces, tasks, or plans.
- A feature may implement one accepted Delivery Phase or a smaller slice inside one phase. It should not combine multiple phases unless the human first confirms a phase rewrite/merge. Feature `spec.md` must reference the requirement set and phase when phase mode is used, and requirement reconciliation should update phase status and feature mapping after human confirmation.
- Future/deferred work, backlog items, and unimplemented planned capabilities belong in requirement set lifecycle/status records and optional `requirements/INDEX.md`, not in `project.md`. Do not edit `requirement.md` or other source files for lifecycle/status updates.
- Project Memory Mode is either `simple` or `enterprise`. Default to simple. Recommend enterprise when any hard trigger applies, including about 200k+ LOC, 5+ durable boundaries, 2+ test systems, 3+ execution environments, `project.md` above about 600 lines, repeated re-scans, or 5+ directory-level guidance files.
- In enterprise mode, `project.md` is an index and current-state summary. Long-term project knowledge moves into optional `.agent-loop/project/*.md` files created only after human confirmation and only when useful.
- Architecture is DDD-inspired by default: domain language first, bounded contexts, business rules outside UI glue, application/use-case orchestration, and infrastructure adapters for external systems.
- Code layout suggestions are reference scaffolds, not mandates. Adapt them to project shape, language, framework conventions, and existing code reality. New projects may scaffold after confirmation; existing projects are recorded as-is unless the human explicitly approves refactoring.
- During recovery/backfill, code reality is the current fact base for agent-maintained docs, but human original requirements are never overwritten.
- During re-adoption, do not start new feature work first. Compare current code/tests/scripts against existing `agent-loop` memory, propose backfill, ask human confirmation, then resume or start feature work.
- For bug reports, regressions, post-close corrections, field/schema changes, algorithm changes, API mismatches, screenshot issues, behavior tweaks, "small tweaks", and QA/test failures, do not default to a new feature. First run Feature Follow-up And Flow-back: inspect recent features in the default 30-day lookback window, present candidate feature matches, and ask whether to flow the work back to an owning feature, create a linked new feature, create a maintenance-fix feature, or investigate first.
- When no recent feature owns a narrow bugfix/internal correction, use `Feature Type: maintenance-fix` under `.agent-loop/features/YYYY-MM-DD-fix-<slug>/`. Maintenance fix is not a naked edit and still requires spec/tasks/tests/plan, verification, review, drift, project-memory impact check, Feature Completion Check, and close.
- During Project Entry and re-adoption, verify the existence of long-term memory index targets before trusting them. If `project.md` says legacy onboarding-db exists, lists onboarding-db documents, or root guidance tells newcomers to read onboarding-db, but the directory or README is missing, report memory drift and route to reconcile/backfill before feature work.
- Root `AGENTS.md` and `CLAUDE.md` are default project guidance artifacts for new or adopted projects, created only after human confirmation.
- Every initialized, Project Entry scanned, re-adopted, or managed project must re-check root `AGENTS.md` and `CLAUDE.md`; Project Entry is incomplete if either is missing or stale unless the human explicitly defers it.
- `AGENTS.md` is the primary maintained startup guidance. `CLAUDE.md` must load, symlink to, include, or briefly point to `AGENTS.md`; do not maintain duplicated root guidance bodies.
- When creating or updating root `AGENTS.md`, run AGENTS Cleanup / Migration Review: preserve human-owned content, surface workflow rules that conflict with current agent-loop, and migrate long-term project facts to `.agent-loop/project.md` or enterprise project memory only after human confirmation.
- Root and directory guidance language follows the project language when clear; default to English only when project language is unclear. Preserve stable artifact names, stage names, and file paths in English.
- Directory-level `AGENTS.md` is proposed for new or existing long-lived boundary directories, created only after human confirmation.
- Strict Mode is default: ask before and after every stage.
- Feature Auto-Loop may run Agent-ready feature work after Feature Spec acceptance and explicit human confirmation.
- Task Auto-Run may run one task/story after its plan is accepted and explicit human confirmation.
- If the human appears slowed down by repeated confirmations, or when starting a feature/task execution lane, proactively explain the available gate modes and recommend either Feature Auto-Loop or Task Auto-Run when safe.
- Auto modes stop at Human-gated work, unclear decisions, risky changes, failed verification, drift needing approval, unrelated dirty work blocking progress, Delivery Contract creation/acceptance/breaking changes, directory guidance changes, unapproved subagent dispatch, submit, pause, close, commit, PR, merge, release, or publish.
- Human confirmations should use table-first Human Review Summary by default; full artifacts remain the source of truth. When multiple documents, facts, or long-term memory entries will change, use Batch Human Review.
- Root `AGENTS.md` / `CLAUDE.md` guidance must tell future agents to own the workflow: classify the stage, recommend one next action, propose missing artifacts, and keep responsibility for sequencing, diagnosis, verification, drift checks, and project-memory updates.
- Root guidance must also explain autonomous execution after approval: Feature Auto-Loop may continue Agent-ready feature work after accepted Feature Spec and explicit enablement; Task Auto-Run may complete one accepted task/story plan through TDD, implementation, verification, bug fixing, review, drift, status update, and final report.
- TDD is default: RED, verify RED, GREEN, verify GREEN, refactor.
- No completion claim without fresh verification evidence.
- Submit requires fresh verification, drift check, diff review, human confirmation, and a recorded submit note.
- The agent must proactively run Feature Completion Check after likely completion, before starting a new feature with an active feature present, and on resume when an active feature may already be done.
- Feature Close Review is required before recommending or performing close: feature-level Spec Review must confirm product/spec/tasks/tests/acceptance are satisfied; feature-level Standards Review is required for large projects, broad diffs, directory or durable boundary changes, security/data changes, architecture changes, or human request.
- Close requires verification, Feature Close Review, drift check, project memory update, optional submit status, and explicit human confirmation.

## Stage Skill Routing

The controller owns the loop. External skills are optional stage accelerators.

- Before falling back to built-in stage guidance, run Stage Helper Capability Scan against the current runtime's available skills/plugins/helpers.
- Clarify: use a brainstorming skill if available.
- Product Brief: use PRD/product discovery or grill-with-docs style skills if available.
- Planning: use a plan-writing skill if available.
- Implementation: use a TDD skill if available.
- Failure: use a systematic debugging skill if available.
- Completion: use verification/review/finishing skills if available.

If no external skill exists, continue with the fallback procedures in `references/stage-guides.md`. Never expose external command systems to the human as required knowledge.

## Stop And Ask

Stop when:

- a task is `Human-gated`
- intent, scope, product, design, architecture, security, data, approval, or public-interface decisions cannot be resolved from files
- a stage would modify human original requirements
- spec, product scope, or acceptance criteria would change
- project memory and code reality materially disagree
- code reality conflicts with feature docs
- a new dependency, migration, destructive operation, credential, external service, or long-lived boundary directory is needed
- directory-level `AGENTS.md` creation/update is recommended
- a Delivery Contract needs creation, human acceptance, or an accepted contract needs a breaking change
- TDD cannot be followed or verification repeatedly fails
- review finds behavior, scope, or architecture changes
- unrelated dirty work blocks progress
- subagents are needed but not yet approved
- submit, commit, PR, merge, release, publish, pause, or close is requested
- the work would require first-version exclusions

---
name: agent-loop
description: Use when starting, continuing, resuming, structuring, testing, implementing, verifying, submitting, pausing, or closing a single-person agent-assisted software development workflow.
---

# Agent Loop

Version: 1.5.0

Run a single-human, CLI-agent development loop from goal intake to verified close. This skill is a controller: it decides the current stage, loads the right reference, produces or updates `agent-loop` artifacts, and stops at human gates.

## Published Source Authority

The published skill package has two operational sources of truth:

```text
references/design.md = core model and constraints
references/runtime.md = executable routing, stage order, gates, and state transitions
```

`SKILL.md` is the concise controller entrypoint. Stage references implement one stage without changing `runtime.md` order or gates. Templates and validation scenarios are derived views and must not create new rules. Workspace-level design drafts are historical or planning evidence only; they cannot override the published package.

When core design and executable routing need to change, update `references/design.md` and `references/runtime.md` together, then align affected stage references, templates, scenarios, and human-facing docs in the same change.

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

Before project-state classification, classify the latest human message intent. `chat` means ordinary discussion, rules questions, status questions, or design talk; answer or discuss only and do not create requirement sets or feature workspaces by default. Message intent is not permanent: if chat turns into demand shaping, `proposal-doc`, implementation, operational support, follow-up, deferred work, project-skill management, or explicit historical feature archive/rehydrate maintenance, reclassify and route accordingly. If the human explicitly wants discussion without documentation, keep `chat`. `requirements-discussion` means the human is shaping product needs, business goals, capability ideas, constraints, tradeoffs, or user scenarios without authorizing implementation; use Brainstorm / Clarify plus Adaptive Product Definition to draft one Human-reviewed Requirement `product.md` under `.agent-loop/requirements/` before Feature construction. `project-skill-management` means the human asks to turn a repeatable project workflow into a project-local skill or to update, disable, or deprecate one; load `references/project-skills.md`. `feature-archive-maintenance` means the human explicitly requests Feature Monthly Archive or rehydrate for closed history; require reliable memory, a read-only scan, and the exact plan SHA-256 Batch Human Gate before mutation. If unclear, ask whether the human wants ordinary discussion, requirements documentation, feature implementation, project-skill management, or archive maintenance.

## Human Help And Version Questions

When the human asks what changed in a version, what is new, how to use agent-loop, how to trigger a capability, or how behavior differs across versions:

- use `CHANGELOG.md` as the source of truth for version changes
- use `Usage.md` as the source of truth for human-facing usage examples and trigger phrases
- use `README.md` for high-level overview, install, and quick-start explanation
- answer from those docs instead of memory
- if the question names a version, read that version section first
- if the question asks how to use agent-loop, summarize in human wording from `Usage.md`

## Mandatory Stage Helper Protocol

Eight stages are mandatory helper-backed stages when matching helpers are exposed by the runtime: Brainstorm / Clarify, Project Skill Creation / Update, Plan Gate / Plan, Execute Task / Story, Diagnose Failure, Verify, Review / Feature Close Review, and approved Subagent Execution.

Before any action in one of these stages, load `references/skill-routing.md` and `references/external-skill-adapters.md`, resolve the canonical Superpowers name and supported alias, and load the complete helper `SKILL.md`. A mandatory helper-backed stage cannot start stage actions until resolution status is `loaded`, `unavailable`, or `load-failed`. Fallback is allowed only for `unavailable` or `load-failed`.

Record every resolution in the current feature `notes.md`, including candidates checked, resolved helper, status, fallback, and agent-loop overrides. If no feature workspace is confirmed, use the response-local pending-record rule in `skill-routing.md`; never create a feature merely for helper logging. After Gate 1 creates a proposed project skill, Project Skill Creation / Update records its helper resolution and RED/GREEN/REFACTOR evidence in `.agent-loop/skills/<skill-name>/validation.md`. A mandatory helper-backed stage cannot complete without a Stage Helper Resolution record.

The helper improves the method only. Agent-loop remains the controller: its artifact paths, human gates, task and feature status, project memory, drift, submit, pause, and close rules override helper defaults. Never create native helper output directories such as `docs/superpowers/` unless the human explicitly requests them and separately confirms after the path override is explained.

## When To Use

Use this skill when the user wants to:

- initialize agent-managed development in a new or existing project
- re-adopt an old `agent-loop` project after code changed without updating `agent-loop` docs
- answer workflow/project questions without turning chat into feature work
- shape product needs through requirements-discussion into adaptive Brief/Standard Product Definitions under `.agent-loop/requirements/`
- turn requirements or prototypes into feature specs, tasks, tests, plans, and implementation
- use existing project code, configuration, scripts, or deployment docs to support operational testing, rollout, account/config/model switching, production diagnosis, or runbook/checklist creation without defaulting to code changes
- use Lightweight Change Lane for a bounded ordinary non-Bug change through one persistent monthly card, adaptive Plan, targeted verification, diff review, rollback, and memory review without creating an unnecessary Feature workspace
- create or update a Human-gated project-local skill from a repeatable workflow, or propose one after a complex verified operation
- continue a paused feature or recover project context
- reconcile `agent-loop` documents with code reality
- reconcile Target Agent Loop memory after a verified code merge, before any independently gated memory commit, push, release, or Source branch cleanup
- execute a task/story with TDD and verification
- submit, pause, resume, or close a feature
- compact closed feature discovery by moving whole feature directories through Human-gated Feature Monthly Archive, or rehydrate an archived feature before follow-up execution

An explicit request for a safe one-off edit is one input to Lightweight Change Assessment, not a separate undocumented bypass. Ordinary non-Bug changes still require a persistent card before target writes, Plan, fresh targeted verification, diff review, rollback, memory review, and gate review when eligible.

First version excludes: multiplayer workflow, roadmap graph, roadmap adapter, tdd-guard, complex ADR system, automatic or unscoped global skill installation, automatic directory-level `AGENTS.md` generation without human confirmation, and automatic commit/PR/merge/release/publish without human confirmation. A visual adapter may be installed only after a separate, exact Installation Authorization that discloses source, revision, command, target, effects, doctor check, and fallback.

## Skill Package Map

Read only what the current stage needs.

```text
references/runtime.md              required first; loop protocol and state machine
references/design.md               condensed extract of the repo source design
references/concepts.md             definitions and scope boundaries
references/lightweight-change-lane.md bounded ordinary non-Bug assessment, persistent monthly card, recovery, memory consolidation, adaptive verification, and scope-expansion rules
references/project-guidance.md     root and directory AGENTS/CLAUDE guidance rules
references/branch-management.md    optional Human-guided branch strategy, target-release context, and Git action boundaries
references/memory-reconciliation.md post-code-merge Target memory fact reconciliation, exact plan, Apply, post-check, and restore rules
references/project-memory-mode.md  simple vs enterprise project memory rules
references/project-architecture-init.md DDD-inspired architecture and stack adapter rules
references/remote-project-discovery.md local entry + remote project discovery rules
references/requirement-management.md     human source requirement archive rules
references/requirement-product-grill.md requirement/product clarification plus triggered Concept Foundation and Requirement Product Model derivation
references/product-definition.md         adaptive Brief/Standard Requirement product.md, completeness, Human Review, helpers, visuals, and Product Slice handoff
scripts/visual_artifact_support.py       shared validator for durable Archify source/render pairs
references/project-decisions.md   Design Readiness, Decision & Design, placement, coverage, and project-level ADR rules
references/product-brief.md        legacy Feature Product Brief reader compatibility only
references/delivery-contracts.md   durable producer-consumer interface handoff rules
references/e2e-discovery.md        Web E2E environment discovery and recording rules
references/large-projects.md       rules for complex or 100k+ LOC projects
references/project-entry-scan.md Project Entry Scan for taking over old projects safely
references/project-skills.md      project-local skill creation, lifecycle, discovery, loading, and execution gates
references/onboarding-knowledge-base.md Evidence-Graph + DDD newcomer project understanding rules
references/bug-management.md           stable Bug identity, lifecycle, Resolution Path, 90-day ownership discovery, and Human Gates
references/feature-follow-up.md          bug/change flow-back to recent features
references/complex-artifacts.md    triggered tasks/tests/plans directory mode
references/implementation-planning.md construction-grade task/story planning rules
references/recovery-and-backfill.md code-reality recovery and document backfill protocol
references/feature-completion-check.md proactive close/pause/continue checks for active features
references/human-review-summary.md table-first approval summaries for human gates
references/stage-guides.md         stage-by-stage procedures
references/checker-recovery.md     Human-authorized isolated recovery for a defective canonical Agent Loop checker
references/artifact-rules.md       artifact ownership, drift, status, and naming
references/skill-routing.md        optional preferred skills and fallback behavior
references/external-skill-adapters.md stage plugin rules for Superpowers and other external skills
references/submit-and-integrate.md explicit git submit / commit / PR gate
references/validation-scenarios.md pressure scenarios for checking this skill works
references/document-templates.md   inline markdown templates
references/workflow-checklists.md  checklist form for each stage
templates/lightweight-execution-card.md persistent Change authoring template for changes/YYYY-MM/YYYY-MM-DD-topic.md
scripts/checker_support.py          shared standard-library Markdown checker support
scripts/check-root-agents-blocks.py read-only root AGENTS managed-block drift checker
scripts/check-onboarding-core-flow-coverage.py onboarding core-flow coverage checker
scripts/check-concept-foundation-trace.py accepted concept/model trace checker
scripts/check-adr-requirement-model-trace.py ADR requirement-model landing checker
scripts/check-feature-context.py read-only Requirement/ADR authority and Feature Context Snapshot freshness checker
scripts/scan-feature-monthly-archive.py read-only deterministic archive/rehydrate plan
scripts/check-feature-monthly-archive.py read-only pre/post archive contract checker
scripts/apply-feature-monthly-archive.py exact-hash Human-gated archive/rehydrate apply
scripts/restore-feature-monthly-archive.py exact transaction-journal restore
scripts/scan-lightweight-changes.py read-only monthly Change validation and pending/human-review inventory
scripts/lightweight_change_support.py standard-library Change parser and deterministic scan model
templates/                         copy-ready artifact templates
examples/login-feature/            small finished feature workspace
examples/complex-saas-project/     larger takeover + feature execution workspace
examples/remote-entry/             local empty directory pointing to a remote project
examples/adaptive-product-definition/ new Requirement product.md to Product Slice and ADR handoff example
README.md                           human overview, install, and quick-start source
Usage.md                            human-facing trigger phrase and usage guide
CHANGELOG.md                        version-change source of truth for "what changed" questions
```

## Required Runtime Behavior

1. Discover exactly one real memory root before relying on project memory. If both `.agent-loop/` and legacy `agent-loop/` exist, fail closed and route to Recovery. If neither exists, continue with the applicable new-project, existing-project, or clearly eligible changes-only path without inventing reliable memory.
2. Check root `AGENTS.md` / `CLAUDE.md` as the Root Agent Bootstrap Gate; if either is missing or stale, load `references/project-guidance.md` and include the guidance repair in the recommended Project Entry action unless the human has explicitly deferred it.
2a. Canonical `scripts/check-*.py` validation requires Python 3.10+ and only the Python standard library. Run the `.py` entrypoints natively on macOS or Windows; if a required checker cannot run because Python is missing or unsupported, fail closed and report the capability gap instead of silently using an obsolete implementation.
2b. When a canonical Agent Loop checker fails after an exact rerun, load `references/checker-recovery.md` inside Diagnose Failure / Verify. Classify the failure as artifact, environment, checker candidate, or unresolved before proposing a fix. A temporary checker write requires an exact Human authorization, uses an isolated copy by default, preserves RED/GREEN and negative-control evidence, and may substitute only for one named Gate after a separate Human decision; the canonical result remains failed until formal source repair.
3. Classify the latest message intent: `chat`, `requirements-discussion`, `project-skill-management`, `feature-archive-maintenance`, `feature-request`, `operational-support`, `feature-follow-up`, `deferred-requirement`, or `unknown`.
3a. For `chat`, answer or discuss only; do not create requirement sets, feature workspaces, tasks, tests, or plans.
3b. For `requirements-discussion`, load `references/requirement-management.md` and `references/product-definition.md`, use Brainstorm / Clarify, choose `brief | standard`, produce a human-reviewed Requirement `product.md`, and write it under `.agent-loop/requirements/<record-date>-<topic>/` only after Product Human Review plus Requirement Record / Archive confirmation before any Feature construction.
3c. For `project-skill-management`, load `references/project-skills.md`, require reliable Project Entry/memory, and route to Project Skill Creation / Update without creating a requirement set or feature workspace.
3d. Classify the entry scenario.
3e. For an actionable non-Bug change that may be bounded, run Lightweight Change Assessment before Feature construction. When clearly eligible, create one parser-valid card under the single accepted memory root at `changes/YYYY-MM/YYYY-MM-DD-<topic>.md` before the first target write, then keep it current through verification and memory review. When a Feature trigger applies, use the existing Feature path. When uncertain, stop and ask the human with options, one Agent recommendation, evidence, and zero writes before the answer.
4. Load the stage guide for the current scenario.
4a. Run Stage Helper Capability Scan for the current stage. For a mandatory helper-backed stage, load `references/skill-routing.md` and `references/external-skill-adapters.md`, resolve canonical and alias names, load the complete helper before stage actions when found, and record the resolution. Use fallback only after recording `unavailable` or `load-failed`.
5. Load `references/project-guidance.md` during project init, Project Entry Scan, or re-adoption, when root guidance is missing/stale, or when long-term agent instructions may need sync.
6. Load `references/project-memory-mode.md` during init, Project Entry Scan, re-adoption, drift check, project memory update, or when `project.md` is large, hard to read, or likely insufficient for future continuation.
7. Load `references/project-architecture-init.md` during init or Project Entry Scan, when proposing project structure, when recording architecture profile, or when a task creates durable code boundaries.
8. Load `references/remote-project-discovery.md` when the human says the project is remote, local files contain remote-entry hints, or local/remote/container execution is unclear. Do not treat an empty local directory alone as remote.
9. Load `references/requirement-management.md` before copying, moving, renaming, indexing, or referencing human source requirements.
9a. Load `references/requirement-product-grill.md` during Requirements Discussion and its Brainstorm / Clarify work when requirements include ambiguous terminology, domain boundaries, business flows, exception paths, conflicting prior Feature behavior, or decision signals. When Concept Foundation triggers inside Standard, inspect evidence, extract candidate concepts, recommend one definition with impact, and ask exactly one blocking question before deriving applicable Requirement Product Model views. Grill questions clarify the Requirement `product.md` draft only; they do not create ADRs, project memory, `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/`.
9b. Load `references/project-decisions.md` for Design Readiness Check and `Decision & Design If Needed`: before accepted requirements enter feature construction, when a requirement spans multiple features or needs shared business-flow/domain/data/architecture/recovery/non-functional design, when product or technical work reveals cross-feature decisions, or when drift changes durable facts. A requirement-driven ADR resolves the Effective Requirement Snapshot, records a Requirement Model Technical Landing Trace, and passes coverage/compatibility review before acceptance. Decision Scan / Placement is an internal method. A `.agent-loop/decisions/*.md` file is globally optional, but it becomes conditionally required when shared design is required and no accepted decision already covers it; creation and acceptance remain Human-gated.
9c. When a complex flow, boundary, comparison, lifecycle, sequence, or relationship would materially improve human understanding, use the Optional Visual Communication Adapter from `references/external-skill-adapters.md`. Prefer a matching active project-local visual skill, then installed Archify. If Archify is absent and would materially improve review, recommend its exact installation/use before offering text/Mermaid/ASCII fallback; use fallback directly only when Archify is not justified, the human declines, the environment is unsupported, or installation/use fails. Installation requires its own exact Human Authorization. Every generation or iteration is bounded by a Visual Scope Grant; working renders are review aids, never semantic authority or acceptance evidence by themselves.
10. Load `references/product-brief.md` only when an existing legacy Feature `product.md` must be read during Resume, Follow-up, Review, Close, or Recovery. New PRD/product synthesis stays in Requirements Discussion through `references/product-definition.md`.
11. Load `references/e2e-discovery.md` before designing or executing Web E2E/browser verification.
12. Load `references/delivery-contracts.md` when the human requests cross-boundary handoff/API/interface documentation, or when the agent detects a likely downstream consumer boundary such as frontend/backend, service, event, public data, SDK/library, UI state, or runtime behavior. Delivery Contracts are not created by default.
13. Load `references/project-entry-scan.md` when taking over an existing project without reliable `agent-loop` memory. This is now a Project Entry Scan only: build safe project memory, guidance status, commands, boundaries, and uncertainties. Do not create `.agent-loop/onboarding-db/`, module docs, flow docs, onboarding diagrams, or old Quick / Deep / Targeted onboarding artifacts during Project Entry Scan.
13a. Load `references/onboarding-knowledge-base.md` when the human asks for newcomer-facing docs, durable project understanding, guided learning paths, or onboarding-db construction. Run it only after Project Entry Scan or reliable project memory. Use Evidence Graph and Core Flow Inventory first, then accepted Onboarding Spec, Onboarding Tasks, Flow Slice Coverage for critical/important flows, evidence-linked diagrams, completeness gating, coverage scoring, and reviewed batches; module/flow docs remain single-file by default.
13b. During Project Entry, Resume, Re-Adopt, context recovery, and controller re-entry, check `.agent-loop/skills/INDEX.md` when present. Load only `active` project skills whose current instruction-bearing and executable files match the validation manifest, according to `bootstrap` / `on-demand`; discovery and loading never satisfy the per-invocation Execution Gate.
13c. Before a new actionable intent uses a generic helper, Code-Guided Operational Support fallback, or built-in stage method, run Project Skill Discovery Guard against the reliable memory root. Read INDEX metadata, match `active` `bootstrap` / `on-demand` candidates, and verify/load only the matched row, path, manifest, and required body. Runtime/global Skill inventory alone cannot support a negative Project Skill claim. Only `index-absent` or `no-active-match` permits generic fallback; `project-skill-drift` stops before equivalent side effects. Discovery and loading still do not satisfy the per-invocation Execution Gate.
13d. Run Branch Strategy Check during Project Entry, Project Entry Scan, Re-Adopt, planning for versioned delivery, Drift Check, and Submit / Integrate. When existing branch rules are clear and safe, preserve them. When rules are confused, the target version is unclear, or customer isolation is at risk, load `references/branch-management.md`, present one optional recommendation, and wait for explicit human acceptance before recording or following it. Recommendation or adoption never authorizes branch creation, switching, merge, deletion, push, tag, release, or publish.
13e. After verified code integration, load `references/memory-reconciliation.md` only when an observed Agent Loop memory conflict exists. No conflict is `reconciliation-not-needed`: do not scan the whole memory root, create a report, or add a reconciliation gate. For a conflict, inspect only its owner, direct references, and minimum evidence; rewrite fact-determined meaning and ask the human only when multiple meanings remain legitimate. Four-snapshot all-path reconciliation is explicit Full Memory Audit / Recovery only. Post-Merge Memory Reconciliation never performs code merge or grants a later Git action.
14. Load `references/feature-follow-up.md` when explicit defect/regression/QA evidence or clear Feature ownership indicates follow-up work. Generic “small tweak”, “改一下”, “修一下”, or `fix` wording alone does not prove Bug or Feature Follow-up. When explicit Bug management intent exists, also load `references/bug-management.md` and run Bug Management inside Feature Follow-up / Flow-back. Scan complete Bug Index metadata for duplicate/reopen first, then use the project-configured 90-day Feature ownership metadata window and evidence-driven extended scan. Bug confirmation never authorizes Feature, Requirement, branch, submit, or close actions.
14a. For `feature-archive-maintenance`, load `references/artifact-rules.md`, `references/stage-guides.md`, `references/human-review-summary.md`, and `references/feature-follow-up.md`. Feature ID is stable while location changes and root `features/archive.md` locates archived/rehydrated history. The scan is read-only; archive/rehydrate requires the expected plan SHA-256 Batch Human Gate, transaction journal, post-check, and restore. Rehydrate before reopened execution; auto modes never authorize either operation.
14b. Load `references/lightweight-change-lane.md` for an actionable ordinary non-Bug local change that may be bounded. Explicit Bug Management and active Feature ownership take precedence. The lane is an internal route, creates no canonical stage, persists exactly one monthly Change card with an adaptive Plan, runs the read-only pending-memory scanner, and stops before writes when uncertain or before broader edits on scope expansion.
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
22b. For Project Skill Creation / Update, resolve `superpowers:writing-skills` / `writing-skills` and `skill-creator` independently. Use both when available, override their output paths to `.agent-loop/skills/<skill-name>/`, and never treat one helper as excluding the other.
23. Load `references/submit-and-integrate.md` before creating commits, PR text, merge notes, or any submission claim.
24. Summarize current state in the response.
25. Recommend exactly one next stage.
26. Ask for human confirmation before mutating files, crossing stages, or enabling an auto mode, except when the current authorized execution scope or an owning reference explicitly permits one bounded deterministic Agent-owned write. The only Post-Merge Memory Reconciliation exception is a reversible, targeted rewrite whose observed conflict has one fact-determined meaning and fresh targeted verification; unresolved meaning and Full Memory Audit / Recovery still require their exact Human Gates.
27. After the stage, update artifacts, summarize evidence, and ask whether to continue, revise, pause, submit, or close.

## Artifact Layout

```text
.agent-loop/
  changes/ persistent Lightweight Change cards partitioned by creation month; no README/INDEX/archive lifecycle
  remote.md optional local-entry pointer for remote projects
  project.md
  project/ optional enterprise memory detail files
  decisions/ Human-gated project / cross-feature Decision & Design records; conditionally required when shared design has no accepted source
  onboarding-db/ Evidence-Graph + DDD human-readable project understanding docs; legacy layouts are evidence only until migrated
  skills/ optional Human-gated project-local skill index and packages
    INDEX.md
    <skill-name>/
      SKILL.md
      validation.md
  requirements/
    <record-date>-<topic>/
      README.md lifecycle, source inventory, Effective Product Definition pointer
      product.md Agent-authored Human-reviewed Brief/Standard Product Definition
      YYYY-MM-DD-product-follow-up-<slug>.md optional append-only reviewed replacement
      sources/ optional copied human originals; never create empty
      visuals/ optional Human-confirmed derived views; never create empty
      requirement.* / prototype.* / feedback.* legacy or human-original root sources remain valid
  bugs/ optional, created on explicit Bug record/manage/investigate/fix intent
    INDEX.md inventory, backlog, and locator
    YYYY-MM-DD-<bug-slug>/
      README.md stable Bug identity, evidence, lifecycle, Resolution Path, verification, close, and reopen
      evidence/ optional bounded evidence
  features/
    archive.md optional Feature ID locator maintained only by Feature Monthly Archive
    YYYY-MM/ archived closed feature directories
    <date>-<feature-slug>/
      spec.md
      context.md optional expanded derived context for complex Features
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

An existing legacy Feature `product.md` may remain in a Feature directory for compatibility, but new Feature construction does not create it.

`.agent-loop/` is the hidden default for target projects. If an older project already has `agent-loop/`, read it and ask before migrating or renaming.

If the local directory is only a remote-project entry point, create only thin local entry memory after confirmation: `.agent-loop/remote.md` plus a thin `project.md` with `Status: remote-entry`. Put full project memory next to the remote source of truth when remote writes are allowed; otherwise use local-shadow mode and label every code fact with remote evidence.

## Execution Defaults

- Default execution unit: one task.
- Before Feature construction for a bounded ordinary non-Bug change, run Lightweight Change Assessment. Clearly eligible work persists one card before target writes; Feature hard triggers use Feature construction; uncertainty performs zero writes and returns one recommended human choice.
- At Project Entry when Changes exist, after Change completion, and before release, run the read-only cross-platform Change scanner. Three pending or the oldest pending being more than seven full calendar days triggers Agent-owned semantic consolidation; scanner output never writes memory. Post-merge reconciliation does not trigger this scanner unless the observed conflict directly involves Change evidence.
- One accidentally interrupted `in-progress` card may resume only after branch/full-HEAD/dirty-diff/Scope/Plan/verification/rollback revalidation. Planned cross-session, handoff, Subagent, long-observation, or complex-evidence work remains Feature construction.
- The card Plan is always required but adaptive. Fact/config/path/domain/docs changes use targeted verification; isolated behavior logic uses the smallest meaningful RED/GREEN. Card execution never grants Git, release, production, external, or Bug lifecycle authority.
- Story execution requires explicit human choice.
- Whole-feature execution requires explicit human confirmation and only fits tiny features.
- A feature may contain many stories and many tasks; `tasks.md` is the feature task ledger.
- Use Requirement `product.md` as the new product-semantics owner and Feature `spec.md` Product Slice as the implementation view. Existing Feature `product.md` is legacy reader-only evidence.
- Use Feature `spec.md` as the execution bootstrap. Before Task, Test, Plan, Resume, Execute, Handoff, Verify, Review, Drift, or Close relies on a Feature, run `scripts/check-feature-context.py`; continue only on `CURRENT`, stop for semantic refresh on `REFRESH_REQUIRED`, and route `BLOCKED` to the owning existing Gate. The Snapshot and optional `context.md` are derived caches, never product authority.
- Do not create `contracts.md` or `contracts/` by default. Use them only for durable producer-consumer delivery boundaries such as API, event, public data, UI state/behavior, SDK/library, or runtime interfaces.
- Create or update Delivery Contract files only after human confirmation. The agent may proactively recommend one when it detects downstream impact, but simple single-person tasks, pure internal logic, and changes with no downstream consumer should skip contracts.
- During Work Breakdown, Technical Design / Code Context, Plan, Review, and Drift Check, detect whether a Delivery Contract should be recommended.
- Feature Auto-Loop and Task Auto-Run do not silently create Delivery Contract files. They must pause before contract file creation, contract acceptance, or breaking contract changes.
- Project-local skill directories are created only after Gate 1 confirms a Project Skill Candidate. Verified proposed skills automatically become `active`; failed validation keeps them `proposed`.
- Project Skill Discovery Guard runs before negative Project Skill claims or generic executable fallback. It reads INDEX metadata and only the matching active body; it does not create a cache or grant execution.
- Every project-skill invocation requires the Execution Gate. A prior human message naming the active skill and concrete scope may satisfy it only after the agent emits the execution summary and confirms the entire planned action/effect stays inside that disclosed scope. `active`, `bootstrap`, prior success, Feature Auto-Loop, and Task Auto-Run never authorize execution.
- Agent may propose a Project Skill Candidate after a complex verified workflow, but must finish the current authorized stage and wait for Gate 1 before creating files.
- Keep temporary subagent assignment notes in `handoffs/`.
- `plan.md` is the active plan for the current task/story, not the default whole-feature plan.
- After task/story selection and before Execute Task / Story, the agent must pass Plan Gate. It may not create tasks and immediately implement.
- Plan Gate has exactly two outcomes: accepted `plan.md` / `plans/*`, or a recorded No-Plan Decision for a trivial task. Task Auto-Run always requires an accepted plan; No-Plan Decision is not enough for Task Auto-Run.
- If `plan.md` is created, it must be construction-grade: exact paths, code context, interfaces, parameters, test code, commands, expected RED/GREEN output, and self-review.
- Do not date the core `plan.md` filename. Date each plan cycle with `Plan ID`, `Created`, `Updated`, and record completed plan cycles in `notes.md`.
- In complex artifact mode, `tasks.md`, `tests.md`, and `plan.md` become stable indexes that link to detailed files under `tasks/`, `tests/`, and `plans/`.
- In complex projects, every task plan must name boundaries, files/areas to inspect, verification commands, and rollback notes.
- A task cannot be marked `done` from implementation alone. Move it to `review` only after implementation and all applicable fresh verification (or a human-approved substitute) exist; otherwise keep it `in-progress` or `blocked`. Required review and drift still gate `done`.
- Task Done Gate: mark a task `done` only after implementation is complete, required tests or substitute verification have run fresh, evidence is recorded in `notes.md`, lightweight Spec Review is recorded, Standards Review is recorded when triggered, drift decision is recorded, and `tasks.md` links or names the evidence.
- During large Project Entry Scan, recommend bounded subagent scanning when available and human-confirmed; otherwise use single-agent layered scan.
- During existing-project Project Entry Scan, create or propose only safe project memory, root guidance status, commands, boundaries, capabilities, and uncertainties. Do not create onboarding-db detail docs, module docs, flow docs, onboarding diagrams, onboarding-spec, or onboarding-tasks during Project Entry Scan.
- During Evidence-Graph + DDD Onboarding, create or update onboarding-db only through `references/onboarding-knowledge-base.md`: build Evidence Graph with Core Flow Inventory, confirm Onboarding Spec, write Onboarding Tasks, then produce reviewed batches with Flow Slice Coverage for critical/important flows, evidence-linked diagrams, completeness gating, single-file module/flow docs by default, and no placeholder files.
- When Project Entry Scan discovers stable project facts missing from project memory, propose or perform project memory backfill after human confirmation.
- For focused questions about one module, flow, async task, deployment path, or problem area, answer from existing docs/code as chat or operational support unless the human explicitly authorizes feature/fix work. Do not create focused onboarding-db artifacts.
- When local and remote project reality are split, discover the remote environment before Project Entry Scan or initializing project memory.
- Historical execution evidence belongs in `notes.md`.
- Human-Guided Branch Management is an internal check, not a canonical stage and not a default Git Flow migration. Persist only a human-confirmed durable strategy and current Target Release Context pointer in `project.md`; keep the selected development branch and its mutable lifecycle in feature `notes.md`, `plan.md`, or Submit / Integrate records.
- A formally released version is sealed. Repairs target a new patch version, and new capabilities target a human-confirmed new version. Customer customization must not flow wholesale into `main` or a standard release line.
- Feature Monthly Archive moves only eligible whole closed feature directories to `features/YYYY-MM/<feature-id>/`; active / blocked / paused features stay flat. It creates no per-feature archive summary, no `historical/`, no Deep Archive, and exposes no `--force`. Original human requirement sources remain unchanged.
- Web E2E capability is discovered from the real project environment. Stable E2E capability belongs in `project.md`; feature-specific E2E cases belong in `tests.md` or `tests/e2e/*`.
- Human source requirements are archived as Requirement Set directories, not new flat files. Each set groups byte-stable human material plus one Agent-authored Human-reviewed Effective Product Definition for the topic.
- `.agent-loop/requirements/` is canonical. Do not create or maintain legacy `inputs/` archives in current-version projects.
- Human source requirement archive dates mean archive date only; never infer deadlines, scope duration, or lifecycle from input paths.
- Requirements created from requirements-discussion live under `.agent-loop/requirements/`; new Feature `spec.md` derives a Product Slice and no new Feature `product.md` is created. Neither Feature artifact owns Requirement lifecycle.
- Concept Foundation is an internal Requirements Discussion / Requirement Product Grill method, never a canonical stage or `.agent-loop/concepts/` artifact. Triggered foundations stay `candidate` or `reopened` until the Human Grill Contract confirms blocking meanings; only `accepted` or a reasoned `concept-foundation-not-needed` path may continue to requirement-level flow, state, and product-data modeling.
- The Effective Product Definition owns accepted product meaning and applicable Concept/Requirement Product Model views. README indexes source/Profile/review while append-only follow-ups preserve history. ADR consumes it only for technical landing; Feature Spec references it through Product Slice. Legacy effective sources remain reader-compatible.
- A requirement-driven ADR records an Effective Requirement Snapshot, a source-wide Requirement Model Scope Inventory, and a Requirement Model Technical Landing Trace inside the existing decision record. Inventory all stable `REL/PERM/CMD/EVT/FLOW/STATE/PM/EX` IDs before selecting scope; every in-scope accepted ID needs a disposition, and every `landed` row needs a concrete technical landing, preserved invariant, Design Slice, and verification path.
- Keep the ADR `proposed` for structural preflight. Only explicit Decision & Design human acceptance authorizes Human Review Evidence plus `Status: accepted`, followed by accepted-mode validation. A reasoned `concept-foundation-not-needed` source uses the trace-not-applicable path instead of invented models.
- `Upstream Compatibility: review-required` blocks new dependent Feature Spec, Plan, and implementation work. It is not an ADR lifecycle status. If changed upstream meaning invalidates an accepted technical decision, preserve history and create a Human-gated superseding ADR instead of rewriting accepted decision meaning.
- For complex requirements, recommend requirement-level `Delivery Phases` in the requirement set `README.md` before feature construction when the human needs to confirm staged delivery. Phases express human-readable delivery slices; they are not feature workspaces, tasks, or plans.
- A feature may implement one accepted Delivery Phase or a smaller slice inside one phase. It should not combine multiple phases unless the human first confirms a phase rewrite/merge. Feature `spec.md` must reference the requirement set and phase when phase mode is used, and requirement reconciliation should update phase status and feature mapping after human confirmation.
- Future/deferred work, backlog items, and unimplemented planned capabilities belong in requirement set lifecycle/status records and optional `requirements/INDEX.md`, not in `project.md`. Do not edit `requirement.md` or other source files for lifecycle/status updates.
- Project Memory Mode is either `simple` or `enterprise`. Default to simple. Recommend enterprise when any hard trigger applies, including about 200k+ LOC, 5+ durable boundaries, 2+ test systems, 3+ execution environments, `project.md` above about 600 lines, repeated re-scans, or 5+ directory-level guidance files.
- In enterprise mode, `project.md` is an index and current-state summary. Long-term project knowledge moves into optional `.agent-loop/project/*.md` files created only after human confirmation and only when useful.
- Architecture is DDD-inspired by default: domain language first, bounded contexts, business rules outside UI glue, application/use-case orchestration, and infrastructure adapters for external systems.
- Code layout suggestions are reference scaffolds, not mandates. Adapt them to project shape, language, framework conventions, and existing code reality. New projects may scaffold after confirmation; existing projects are recorded as-is unless the human explicitly approves refactoring.
- During recovery/backfill, code reality is the current fact base for agent-maintained docs, but human original requirements are never overwritten.
- During re-adoption, do not start new feature work first. Compare current code/tests/scripts against existing `agent-loop` memory, propose backfill, ask human confirmation, then resume or start feature work.
- Human-Guided Bug Management is an internal method of Feature Follow-up / Flow-back, not a canonical stage or message intent. Before creating, updating, or reopening a stable Bug Record, scan all Bug Index metadata for duplicate/reopen identity, then scan the default 90-day Feature metadata window with evidence-ranked deep read and evidence-driven extension beyond 90 days. Use that evidence to recommend exactly one Resolution Path.
- Bug Records own identity, Report Origin, evidence, Status/Resolution, Resolution Path, verification, close, and reopen history. Requirements own product meaning; Features own every code repair through spec/tasks/tests/plan/TDD/Verify/Review/Drift. Bug artifacts never own tasks, tests, plans, or code execution.
- Archive changes Feature location, not identity or ownership. Resolve archived candidates through `features/archive.md`; discovery and Human Review are read-only, while confirmed flow-back requires the existing Human-gated rehydrate before reopened execution.
- When no recent feature owns a narrow bugfix/internal correction, use `Feature Type: maintenance-fix` under `.agent-loop/features/YYYY-MM-DD-fix-<slug>/`. Maintenance fix is not a naked edit and still requires spec/tasks/tests/plan, verification, review, drift, project-memory impact check, Feature Completion Check, and close.
- During Project Entry and re-adoption, verify the existence of long-term memory index targets before trusting them. If `project.md` says legacy onboarding-db exists, lists onboarding-db documents, or root guidance tells newcomers to read onboarding-db, but the directory or README is missing, report memory drift and route to reconcile/backfill before feature work.
- Root `AGENTS.md` and `CLAUDE.md` are default project guidance artifacts for new or adopted projects, created only after human confirmation.
- Every initialized, Project Entry scanned, re-adopted, or managed project must re-check root `AGENTS.md` and `CLAUDE.md`; Project Entry is incomplete if either is missing or stale unless the human explicitly defers it.
- `AGENTS.md` is the primary maintained startup guidance. `CLAUDE.md` must load, symlink to, include, or briefly point to `AGENTS.md`; do not maintain duplicated root guidance bodies.
- When creating or updating root `AGENTS.md`, run AGENTS Cleanup / Migration Review: preserve human-owned content, surface workflow rules that conflict with current agent-loop, and migrate long-term project facts to `.agent-loop/project.md` or enterprise project memory only after human confirmation.
- Root and directory guidance language follows the project language when clear; default to English only when project language is unclear. Preserve stable artifact names, stage names, and file paths in English.
- Directory-level `AGENTS.md` is proposed for new or existing long-lived boundary directories, created only after human confirmation.
- Strict Mode is default: ask before and after every stage.
- Feature Auto-Loop may run Agent-ready feature work after a passed Requirement Checklist, Feature Spec acceptance, and explicit human confirmation.
- Task Auto-Run runs Analyze Consistency before executing one accepted task/story plan after explicit human confirmation.
- If the human appears slowed down by repeated confirmations, or when starting a feature/task execution lane, proactively explain the available gate modes and recommend either Feature Auto-Loop or Task Auto-Run when safe.
- Auto modes stop at Feature Context `refresh-required | blocked`, Human-gated work, unclear decisions, risky changes, failed verification, drift needing approval, unrelated dirty work blocking progress, Bug Resolution Path decisions, Bug close/reopen, Feature create/reopen, Requirement create/lifecycle change, Delivery Contract creation/acceptance/breaking changes, archive/rehydrate apply, directory guidance changes, unapproved subagent dispatch, branch creation, switching, deletion, push, or tag, submit, pause, close, commit, PR, merge, release, or publish.
- Human confirmations should use table-first Human Review Summary by default; full artifacts remain the source of truth. When multiple documents, facts, or long-term memory entries will change, use Batch Human Review.
- Root `AGENTS.md` / `CLAUDE.md` guidance must tell future agents to own the workflow: classify the stage, recommend one next action, propose missing artifacts, and keep responsibility for sequencing, diagnosis, verification, drift checks, and project-memory updates.
- Root guidance must also explain autonomous execution after approval: Feature Auto-Loop may continue Agent-ready work after Requirement Checklist passes, Feature Spec is accepted, and the mode is explicitly enabled; Task Auto-Run must run Analyze Consistency before completing one accepted task/story plan through TDD, implementation, verification, bug fixing, review, drift, status update, and final report.
- TDD is default: RED, verify RED, GREEN, verify GREEN, refactor.
- No completion claim without fresh verification evidence.
- Submit requires fresh verification, drift check, diff review, human confirmation, and a recorded submit note.
- The agent must proactively run Feature Completion Check after likely completion, before starting a new feature with an active feature present, and on resume when an active feature may already be done.
- Feature Close Review is required before recommending or performing close: feature-level Spec Review must confirm product/spec/tasks/tests/acceptance are satisfied; feature-level Standards Review is required for large projects, broad diffs, directory or durable boundary changes, security/data changes, architecture changes, or human request.
- Close requires verification, Feature Close Review, drift check, project memory update, optional submit status, and explicit human confirmation.

## Stage Skill Routing

The controller owns the loop. External skills are optional stage accelerators.

- Before falling back to built-in stage guidance, run Stage Helper Capability Scan against the current runtime's available skills/plugins/helpers.
- Project Skill Creation / Update: prefer `superpowers:writing-skills` / `writing-skills` for RED/GREEN/REFACTOR and also use `skill-creator` for scaffolding and validation when available; write only to `.agent-loop/skills/<skill-name>/`.
- Clarify: use a brainstorming skill if available.
- Product Definition: use PRD/product discovery or grill-with-docs style helpers inside Requirements Discussion when available; translate output to Requirement `product.md` and keep all Agent Loop gates.
- Optional Visual Communication: when a Visual Trigger exists, prefer a matching active project-local visual skill, then installed Archify; if materially useful Archify is absent, offer its exact, separately authorized installation before Mermaid/table/ASCII fallback. Fall back without blocking when Archify is unjustified, declined, unsupported, or failed. Keep semantic text authoritative and validate any durable source/render pair.
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
- a triggered Concept Foundation is still `candidate` or `reopened`, a downstream artifact would redefine an accepted Concept ID / Requirement Product Model rule, or an ADR dependency is `review-required` / missing Requirement Model coverage
- project memory and code reality materially disagree outside a reversible fact-determined Post-Merge Memory Reconciliation rewrite; unresolved meaning still stops
- when an adopted Branch Strategy or versioned/customer delivery applies: the branch class or unique Target Branch is unknown; the adopted Branch Strategy, current Target Release Context, and Git reality disagree; the target release is sealed; customer isolation would be violated; or a branch action has not been explicitly authorized
- code reality conflicts with feature docs
- a new dependency, migration, destructive operation, credential, external service, or long-lived boundary directory is needed
- directory-level `AGENTS.md` creation/update is recommended
- a Delivery Contract needs creation, human acceptance, or an accepted contract needs a breaking change
- a Project Skill Candidate needs Gate 1 before creation or material update
- Project Skill Discovery Guard finds `project-skill-drift`, or an active match has not been resolved before an equivalent generic action
- an active project skill is about to execute without a current bounded Execution Gate grant or with undisclosed planned actions/effects
- TDD cannot be followed or verification repeatedly fails
- a canonical Agent Loop checker may be defective but its failure has not been classified, an exact Temporary Checker Repair Review has not been accepted before patch writes, or a temporary result is being reused outside its named Gate
- review finds behavior, scope, or architecture changes
- unrelated dirty work blocks progress
- subagents are needed but not yet approved
- submit, commit, PR, merge, release, publish, pause, or close is requested
- the work would require first-version exclusions
- Feature Monthly Archive or rehydrate lacks an exact reviewed plan hash, has unsupported/ambiguous references, encounters a stale plan or incomplete `.archive-txn`, or would be performed by manual directory movement
- Bug Index and README disagree; a duplicate target is missing/cyclic; Status/Resolution is invalid; an `in-progress` Bug does not use `flow-back | linked-feature | maintenance-fix` or lacks one Human-confirmed Fix Feature Target; Expected Behavior authorities conflict; an archived Fix Feature cannot be resolved safely; or a Bug/Feature/Requirement/Git action lacks its specific Human Gate
- Lightweight / Feature / Bug routing remains uncertain after available evidence is inspected; stop with few real options, one Agent recommendation, and zero writes before the human answer
- a Lightweight Execution Card encounters scope expansion, loses exact verification or rollback, reveals a Feature hard trigger, or needs planned cross-session/handoff/subagent tracking; stop before broader edits and return to Human Review
- the Change scanner reports invalid layout/state/date/root evidence, dual memory roots, unresolved pre-release pending/human-review facts, or a high-evidence sync lacks one reliable owner, exact disclosure, post-check, or narrow rollback

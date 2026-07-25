# Project Guidance

Use this file when initializing or adopting a project, syncing long-term project rules, or deciding whether `AGENTS.md` / `CLAUDE.md` should exist.

## Core Split

```text
AGENTS.md / CLAUDE.md = agent startup guidance
.agent-loop/project.md = agent-loop project memory
.agent-loop/project/* = optional enterprise project memory details
.agent-loop/remote.md = local entry pointer for remote projects
.agent-loop/features/* = feature execution state
.agent-loop/features/*/spec.md = Feature bootstrap plus derived Feature Context Snapshot and Product Slice
.agent-loop/features/*/context.md = optional expanded derived context for a complex Feature; never independent product truth
.agent-loop/features/archive.md = Feature Monthly Archive locator for stable Feature IDs
.agent-loop/features/YYYY-MM/* = Human-gated closed-history month archive; never an execution path
.agent-loop/requirements/<record-date>-<topic>/product.md = Agent-authored Human-reviewed Product Definition
.agent-loop/requirements/<record-date>-<topic>/sources/* = preserved human source material when a new package needs a sources directory
.agent-loop/skills/INDEX.md = optional project-skill lifecycle and discovery index
.agent-loop/skills/<skill-name>/* = optional human-confirmed project-local capability
.agent-loop/memory-merges/MM-<short-sha>-<topic>/README.md = optional complex/cross-session conflict record
.agent-loop/memory-merges/MM-<short-sha>/README.md = explicitly authorized Full Memory Audit / Recovery; never a default empty directory
```

Default memory root is `.agent-loop/` because it is workflow metadata, not product code. Reuse legacy `agent-loop/` only when it is the single real accepted root, and ask before migration. If both `.agent-loop/` and legacy `agent-loop/` exist, fail closed and route to Recovery.

Do not use `AGENTS.md` as a task log. Do not use `project.md` as the startup instruction file for every agent.

Root guidance may navigate a user Agent to the Feature Monthly Archive procedure, but it must not teach manual directory movement. Active/blocked/paused work remains at the first level. Archive and rehydrate use the canonical Python scan/check/apply/restore commands, an exact plan SHA-256 Human Gate, transaction recovery, and post-check; execution resumes only after rehydrate restores the flat feature path.

Root guidance may also route an observed post-code-integration memory conflict, but the targeted fact-resolution rules and optional Full Memory Audit / Recovery stay in `memory-reconciliation.md`. Root guidance must say no observed conflict is `reconciliation-not-needed`, with no whole-memory scan or extra gate. Refresh the root submit managed block when this concise route is absent or its full template block revision is stale; do not copy the detailed procedure into the target root file.

The Workflow Gateway Map contains one exact first-hop row for an already-defined actionable ordinary non-Bug change, pointing to `Lightweight Change Assessment` and `references/lightweight-change-lane.md`. Product meaning that is still being shaped remains in Requirements Discussion. Eligibility, Feature hard triggers, card fields, Adaptive Plan/TDD, scope expansion, completion, and gate details belong in that reference, not root `AGENTS.md`.

The Checker Recovery Gateway contains one concise row for a canonical Agent Loop checker that still fails after an exact rerun. It routes to `Diagnose Failure / Checker Recovery` and `references/checker-recovery.md`; root guidance must not copy the detailed classification, fixture, RED/GREEN, isolation, substitute-evidence, expiry, or formal-repair algorithm. The Evidence Gate must keep suspected checker repair Human-authorized and forbid silent bypass or canonical-pass claims.

## Root Agent Bootstrap Gate

Root `AGENTS.md` is the bootstrap node that teaches future agents how to enter `agent-loop`. It is not optional project decoration.

Bootstrap Protocol must say root AGENTS.md is a bootstrap cache, not a replacement for the agent-loop skill. During Project Entry, Resume, Re-Adopt, stage boundaries, after context compaction, after a long-running session, or whenever workflow state is uncertain, if the runtime exposes the agent-loop skill, load/use it before making agent-loop workflow decisions. Stage Helper Capability Scan happens only after the agent-loop controller is active or unavailable/load-failed because helper scan resolves stage methods, not the controller itself. If the skill is unavailable or load-failed, root fallback must force Strict Mode, suspend auto grants, allow only Chat/read-only entry/recovery/operational analysis, forbid Execute/Human-gated writes/Submit/Pause/Close, and report how to restore the skill.

Every time `agent-loop` is used inside a target project, check root guidance before feature work:

```text
1. Read root AGENTS.md if present.
2. Read root CLAUDE.md if present.
3. Check whether CLAUDE.md loads, includes, symlinks to, or clearly points to AGENTS.md.
4. Apply the Bootstrap Protocol skill-loading step when the runtime exposes the agent-loop skill.
5. Check whether AGENTS.md contains the required bootstrap sections.
6. If AGENTS.md uses agent-loop managed blocks, compare each managed block `section` and `block-version` with the current root AGENTS template.
7. If `scripts/check-root-agents-blocks.py` is available in the local `agent-loop` skill package, run it with Python 3.10+ against the current `templates/root-AGENTS.md` and target root `AGENTS.md`; use its report as the managed-block drift evidence. Use `python3` on macOS or `py -3` / `python` on Windows. If Python 3.10+ is unavailable, fail closed and report the capability gap instead of using an obsolete checker implementation.
8. If `.agent-loop/skills/INDEX.md` exists, read its metadata, verify each referenced `active` path and exact INDEX row plus instruction-bearing/executable files against the SHA-256 manifest, and exclude missing, mismatched, `proposed`, `disabled`, and `deprecated` skills from normal routing.
9. Before claiming no relevant project skill or entering a generic execution fallback, check `.agent-loop/skills/INDEX.md`; if an active skill matches, load it read-only and keep the per-invocation Execution Gate.
10. Record or update guidance status in project.md.
11. If missing or stale, propose a repair through Human Review Summary.
```

`AGENTS.md` is stale when any of these are missing or contradicted:

- project uses `agent-loop`
- Bootstrap Protocol is missing skill-loading/fallback rules: root guidance must say root `AGENTS.md` is a bootstrap cache rather than a replacement for the `agent-loop` skill, must load/use the available skill before agent-loop workflow decisions, and must say Stage Helper Capability Scan happens only after the controller is active or unavailable/load-failed
- Message Intent Guard: distinguish Chat, Requirements Discussion, already-defined ordinary non-Bug change, explicit Bug/follow-up, Feature Request, Operational Support, Project Skill, Archive/Rehydrate, Memory Reconciliation, proposal/deferred, and lifecycle requests before project-state routing
- Workflow Gateway Map: route each of the 17 startup signal families to exactly one first hop and exact published reference set; root guidance is navigation only, while `references/runtime.md` owns the complete leaf-stage order
- Lightweight Change Gateway: route only already-defined actionable bounded non-Bug work to `references/lightweight-change-lane.md`; unresolved product meaning remains in Requirements Discussion
- Bootstrap Protocol: inspect `.agent-loop/`, classify the stage, and recommend exactly one next action
- Bootstrap Protocol lacks the concise Project Skill discovery-before-fallback reminder; detailed result names, drift handling, manifest procedure, and precedence remain in `references/runtime.md` and `references/project-skills.md`, not root guidance
- Agent Ownership: agents own the project outcome as well as the loop, inspect safely available evidence before asking, and continue through authorized scope until verified completion or a concrete Human Gate
- Stage Helper Capability Scan: agents actively check available skills/plugins/helpers before fallback stage guidance
- Gate Modes: Strict Mode, Feature Auto-Loop, Task Auto-Run, and their explicit human enablement rules
- Feature Context startup invariant: before Task/Test/Plan/Execute/Resume relies on a Feature, load `spec.md`, run the Requirement/ADR freshness check, and require the Feature Context Snapshot to be current
- Required Stops: all six visible classes — Semantic, Scope And Risk, Execution, Evidence, External Mutation, and Git And Lifecycle — plus explicit Auto Mode non-bypass
- Checker Recovery Gateway: exact rerun routes a canonical Agent Loop checker failure to `references/checker-recovery.md`; isolated repair is Human-authorized and cannot be presented as canonical pass
- Completion Rules: code changes alone are not done; fresh verification, Review, Drift Check, project-memory evidence, Feature Completion Check, and Feature Close Review remain visible
- Submit And Commit Rules: submit/commit/push/PR/merge/tag/release/publish/pause/close/cleanup remain independent Human Gates and only intended files are included
- Artifact Authority: Requirement, Decision / ADR, Feature, Bug, Lightweight Execution Card, and project memory retain distinct ownership
- Submit And Commit Rules lack the concise post-code-integration reminder to reconcile changed Agent Loop memory before push/release/Source cleanup
- root/directory guidance boundaries and requirement archive rules
- managed block markers are missing for `agent-loop` maintained sections, unless the file is intentionally fully human-owned and the human has deferred managed block adoption
- a managed block from the current root AGENTS template is missing, has no `block-version`, or has an older `block-version` than the current template
- a managed block has a date-only, malformed, or different `block-version`; exact full template block-version match is required

`CLAUDE.md` is stale when it duplicates independent long-lived rules, diverges from `AGENTS.md`, or does not clearly point Claude Code to `AGENTS.md`.

Project Entry Scan, re-adoption, or project initialization is not complete until:

```text
AGENTS.md status = present | created | human-deferred
CLAUDE.md status = points-to-AGENTS | created-pointer | human-deferred
```

If the human defers guidance repair, record the defer decision and reason in `project.md`. Do not silently treat missing root guidance as healthy.

## Root Guidance Default

For Init Project and Project Entry Scan, the default recommendation is to create or update:

```text
AGENTS.md
CLAUDE.md -> AGENTS.md
```

Only write after human confirmation.

For any project that is initialized, Project Entry scanned, re-adopted, or otherwise managed by `agent-loop`, root guidance must be checked every time the agent enters the project:

```text
AGENTS.md status: present | created | stale | missing | human-deferred
CLAUDE.md status: points-to-AGENTS | created-pointer | stale | missing | human-deferred
```

Project Entry Scan is not complete if root `AGENTS.md` or `CLAUDE.md` is missing or stale unless the human explicitly defers it. Record the decision in `project.md`.

Guidance language should follow the project language when it is clear from existing docs or human preference.

If project language is unclear, default root `AGENTS.md` / `CLAUDE.md` guidance to English for cross-agent compatibility.

If the project uses Chinese or the human explicitly asks for Chinese guidance, write root and directory guidance in Chinese, while keeping stable artifact names, stage names, and file paths in English, such as `agent-loop`, `Requirement Archive`, `Feature Spec`, `Task Auto-Run`, `project.md`, and `requirements/`.

For a local directory that is only a remote-project entry point, create local root guidance only if it helps future agents re-enter the remote workflow. Full project guidance should live in the remote project when remote writes are allowed.

`AGENTS.md` is the primary maintained guidance file. `CLAUDE.md` must not duplicate the full rules. It should load, include, symlink to, or briefly point Claude Code to `AGENTS.md`. If symlinks are unsafe or unsupported, create `CLAUDE.md` with a short pointer to `AGENTS.md`.

Never overwrite an existing ordinary `CLAUDE.md` or `AGENTS.md` without reading it, summarizing the proposed migration, and getting human confirmation.

## Managed Blocks

Use managed blocks to mark content maintained by `agent-loop` inside root `AGENTS.md`:

```md
<!-- agent-loop:managed-start section:<name> source:<path-or-artifact> block-version:<agent-loop-version>-<YYYYMMDD>[.<same-day-revision>] -->
...
<!-- agent-loop:managed-end section:<name> -->
```

Recommended section names:

```text
bootstrap
message-intent
workflow-stage-map
ownership
gates
required-stops
completion
artifacts
submit
directory-guidance
architecture
commands
hard-constraints
```

Rules:

- `agent-loop` may propose updates inside managed blocks when the source artifact changes.
- Managed blocks must include `section`; they should include `source` when the content comes from a stable artifact such as `.agent-loop/project.md`, `.agent-loop/project/*.md`, or `ARCHITECTURE.md`.
- Every managed block should include a full content revision so future agents can refresh specific blocks even when the skill version did not change. Use `block-version:<agent-loop-version>-<YYYYMMDD>[.<same-day-revision>]`; do not shorten it to the skill version alone. The numeric suffix is optional for the first revision that day and required when managed content changes again on the same day.
- Content outside managed blocks is human/project-owned. Do not rewrite it automatically.
- Managed block maintenance rules belong here and in refresh tooling; do not require the target root `AGENTS.md` to include a separate Managed Block Rule prose section.
- If an existing `AGENTS.md` has no managed blocks, propose adding the minimal needed managed blocks instead of replacing the whole file.
- If a block-version is missing or older than the current template, treat that block as stale.
- Treat bare skill-version-only block revisions such as `block-version:1.5.0` as stale because they cannot distinguish same-version template revisions.
- If a managed block exists in the current template but is missing from root AGENTS.md, treat it as a missing managed block and propose adding it.
- If a managed block source is missing, stale, or contradictory, classify the block as stale and propose either source correction or block refresh through Human Review Summary.
- If marker pairs are broken, duplicated, nested, or ambiguous, stop and ask before editing.
- Do not put task status, feature progress, raw requirements, plans, or test output inside managed blocks.
- `CLAUDE.md` should point to `AGENTS.md`; it should not duplicate managed blocks.

Managed block detection checklist:

1. Count every `agent-loop:managed-start` and `agent-loop:managed-end`; counts must match.
2. Parse `section:<name>` from every start marker and end marker; each start section must have exactly one matching end section.
3. Reject duplicate active sections in the same `AGENTS.md` unless the human explicitly asks to merge or repair them.
4. Reject nested managed blocks.
5. Reject orphan end markers and start markers without an end marker.
6. Check that each start marker has `section`; check `source` when the block claims to mirror a stable artifact.
7. Parse `block-version` from each managed block when present and compare it with the matching section in the current root AGENTS template.
8. Check whether each `source` path exists or is intentionally external/deferred before relying on it.
9. If any check fails, classify root guidance as `stale-marker` and stop before editing `AGENTS.md`.

If `scripts/check-root-agents-blocks.py` is available, run it with Python 3.10+ as the first read-only managed-block drift check. The script validates section presence, marker integrity, per-section `block-version`, unexpected managed sections, and local `source` paths. Its output is evidence for the Human Review Summary; it must not be treated as approval to write. Missing or unsupported Python is a capability blocker for checker-backed evidence, not permission to fall back to the old Bash/Ruby rules.

Managed block update flow:

1. Read the existing `AGENTS.md`.
2. Identify managed blocks and their sources.
3. Compare source facts, required sections, and per-block `block-version` with the current root AGENTS template.
4. Present a table with block, source, current summary, proposed change, and risk.
5. Ask human confirmation.
6. Update only approved managed blocks; preserve all other content byte-for-byte where practical.
7. Record guidance status and source evidence in `project.md`.

## Root AGENTS Refresh Protocol

Use this protocol when root `AGENTS.md` exists and the project already uses `agent-loop`.

1. Read the existing root `AGENTS.md` before proposing updates.
2. If available, run `python3 scripts/check-root-agents-blocks.py --template <agent-loop-skill>/templates/root-AGENTS.md --target <project>/AGENTS.md` on macOS, or the equivalent `py -3 scripts\check-root-agents-blocks.py ...` command on Windows, and use the report as read-only drift evidence.
3. Validate managed block markers with the managed block detection checklist.
4. Compare each managed block `section` and `block-version` against the current root AGENTS template.
5. Treat missing, older, bare skill-version-only, date-only, malformed, or different `block-version` values as stale; exact full template block-version match is required.
6. If a managed block exists in the current template but is missing from root AGENTS.md, treat it as a missing managed block and propose adding it.
7. Do not require a separate Managed Block Rule or Agent Loop Guidance Version prose section in target root `AGENTS.md`; managed block maintenance rules live in this reference and refresh tooling.
8. Copy the exact start marker metadata for each refreshed section from the current root AGENTS template unless the section source must point at a target-project artifact. If the target project uses legacy `agent-loop/` instead of `.agent-loop/`, adjust only the `source`; keep the template `block-version` unchanged.
9. Run AGENTS Cleanup / Migration Review for content outside managed blocks before writing.
10. Present a Human Review Summary with block, current block-version, template block-version, checker status, proposed change, risk, and human decision.
11. Preserve all content outside managed blocks unless each cleanup, replacement, or migration item is listed in Human Review Summary and separately approved. Do not treat "refresh AGENTS.md quickly" or similar wording as blanket approval to replace the whole file with `templates/root-AGENTS.md`.
12. Update only approved managed blocks and record the guidance status in `project.md`.

## AGENTS Cleanup / Migration Review

Run this review when creating or updating root `AGENTS.md`, during Project Entry Scan, during Re-Adopt, during root guidance version refresh, or when root guidance is stale.

Inspect existing root `AGENTS.md` and `CLAUDE.md`. Classify content outside managed blocks before writing:

| Classification | Meaning | Default action |
|---|---|---|
| agent-loop startup guidance | bootstrap, ownership, gates, stops, submit, artifact routing | move into or refresh managed blocks |
| conflicting workflow rule | rules that contradict current agent-loop gates, artifact paths, task status, review, submit, or memory rules | list the conflict and ask whether to remove, replace, or keep as a project override |
| long-term project memory | tech stack, commands, architecture boundaries, domain terms, test strategy, environments, durable capabilities, constraints, current work | propose migration to `.agent-loop/project.md` or enterprise `.agent-loop/project/*.md` |
| human/project-owned notes | team conventions, local background, policy that does not conflict with agent-loop | preserve outside managed blocks |
| temporary/task material | task logs, feature progress, raw requirements, temporary plans, test output | propose moving to feature `notes.md`, feature docs, `.agent-loop/requirements/`, or project docs |

Present an AGENTS cleanup / migration Human Review Summary before changing files:

| Content / Location | Classification | Conflict or Memory Target | Proposed Action | Risk | Human Decision |
|---|---|---|---|---|---|

Rules:

- Do not delete, move, or rewrite human-owned content automatically.
- If a conflicting rule is intentional, keep it only after human confirmation and record the override in project memory when it affects future agents.
- If long-term project memory is migrated, preserve the source location as evidence and update `project.md` or enterprise project-memory detail files only after human confirmation.
- Root `AGENTS.md` should keep only startup-critical summaries. Rich long-term memory belongs in `.agent-loop/project.md`, enterprise `.agent-loop/project/*.md`, or project docs.
- `CLAUDE.md` should point to `AGENTS.md`; if it contains duplicated or conflicting rules, include it in the same cleanup / migration review.

## Root `AGENTS.md` Should Contain

Keep it short and long-lived:

- project uses `agent-loop`
- Bootstrap Protocol skill loading: root `AGENTS.md` is bootstrap guidance, not a replacement for the `agent-loop` skill; if the runtime exposes the skill, load/use it before making workflow decisions, especially during Project Entry, Resume, Re-Adopt, stage boundaries, after context compaction, or when workflow state is uncertain; Stage Helper Capability Scan happens only after the controller is active or unavailable/load-failed; unavailable/load-failed fallback forces Strict Mode and permits only Chat/read-only entry/recovery/operational analysis while Execute, Human-gated writes, Submit, Pause, and Close remain blocked
- Message Intent Guard: before project-state routing, distinguish Chat, Requirements Discussion, already-defined ordinary non-Bug change, explicit Bug/follow-up, Feature Request, Operational Support, Project Skill, Archive/Rehydrate, Memory Reconciliation, proposal/deferred, and lifecycle requests; keep eligibility, internal methods, lifecycle algorithms, and artifact-writing rules in the exact Gateway owners
- Workflow Gateway Map: after intent and project-state classification, route the 17 startup signal families to exactly one first hop and its exact published reference set; load the matching owner before acting, while `references/runtime.md` retains the complete leaf-stage order
- Root Agent Bootstrap: read `AGENTS.md`, inspect `.agent-loop/`, classify the current stage, and recommend exactly one next action
- guidance language follows project language; keep stable artifact/stage names in English
- before development, discover exactly one `.agent-loop/` or accepted legacy `agent-loop/` root; if reliable memory is missing, route to Project Entry / Init
- read only stage-relevant project memory, remote-entry evidence, Active Feature artifacts, and linked detail
- if `.agent-loop/skills/INDEX.md` exists, read INDEX metadata, verify each referenced `active` path and exact INDEX row plus instruction-bearing/executable files against the SHA-256 manifest, and load only matching `bootstrap` or `on-demand` project skills; discovery and loading do not authorize execution
- before claiming no relevant project skill or entering a generic execution fallback, check `.agent-loop/skills/INDEX.md`; if an active skill matches, load it read-only and keep the per-invocation Execution Gate
- if `project.md` says `Status: remote-entry`, read `.agent-loop/remote.md` and verify the remote project before acting
- if the project used `agent-loop` before but recent development bypassed it, route to Re-Adopt Agent Loop Project before new feature work
- Operational Support, Bug / Feature Follow-up, Requirements, Decision, Feature Construction, Project Skill, Archive, Memory Reconciliation, Lifecycle, and Chat enter through their exact Gateway rows; their eligibility, lifecycle, and algorithms remain in the linked published owners
- when working in a subdirectory, check for the nearest directory-level `AGENTS.md`
- when creating a new long-lived boundary directory, propose a directory-level `AGENTS.md` before or alongside the directory creation
- keep human source/product meaning, accepted technical landing, implementation, defect identity/lifecycle, bounded Change evidence, and durable current facts in their distinct owning artifacts
- when existing branch rules are confused, target version is unclear, or customer boundaries are risky, load `references/branch-management.md`, recommend the optional profile, and adopt it only after explicit human acceptance; recommendation/adoption never authorizes a Git action
- Agent Ownership: agents own the project outcome as well as the loop, inspect safely available evidence before asking, classify the current stage, recommend exactly one next action, propose missing artifacts, and continue through authorized scope until verified completion or a concrete Human Gate
- Stage Helper Capability Scan: before every helper-friendly stage listed in `skill-routing.md`, inspect the current runtime for available helper skills/plugins such as Superpowers; use matching helpers as methods while keeping agent-loop control
- ask human confirmation before each agent-loop stage
- use table-first Human Review Summary for non-trivial confirmations
- Autonomous Execution After Approval: Feature Auto-Loop and Task Auto-Run continue only Agent-ready work inside the accepted scope and bypass none of the six Gate classes
- before Task/Test/Plan/Execute/Resume relies on a Feature, load its Feature Context Snapshot and require the Requirement/ADR freshness check to be current; non-current context stops Auto Mode
- completion and submit projection: fresh verification, Review, Drift Check, Project Memory evidence, Feature Completion Check, Feature Close Review, intended-file-only submit scope, and independent lifecycle/Git confirmations
- stable project commands and hard constraints, only if every agent should know them immediately
- managed block markers for `agent-loop` maintained sections, so future updates do not overwrite human-owned content
- stale detection: if future agents cannot learn Bootstrap, project-outcome Agent Ownership, Message Intent Guard, Workflow Gateway Map, Gate Modes/six stop classes, Completion, Submit, and Artifact Authority from root guidance, if any Gateway reference does not resolve in the installed package, or if managed block revisions differ from the current template, propose a Human-reviewed root update

## Root `AGENTS.md` Should Not Contain

- current task status
- feature execution logs
- temporary plans
- test output transcripts
- meeting notes
- raw requirements or prototype content
- long duplicated documentation

Those belong in `.agent-loop/` or project docs.

## `project.md` Should Contain

Use `.agent-loop/project.md` for richer memory:

- project summary
- guidance language
- project memory mode: simple | enterprise
- architecture profile: project shape, language adapter, framework adapter, and DDD intensity
- product context
- tech stack
- domain language / glossary
- current capabilities
- evidence and confidence for capabilities, commands, and boundaries
- Current Work
- Active Feature / Paused Features
- Next Suggested Action
- directory map
- directory guidance inventory
- test commands
- Project Entry uncertainties
- known constraints
- long-term decisions
- human-confirmed Branch Strategy with Adoption Status, Profile, patterns, sealed-release rule, customer isolation, deletion policy, confirmation, and evidence
- current Target Release Context pointer; mutable Current Branch Context remains in feature notes/plan/submit evidence

In simple mode, `project.md` may contain the long-term project memory body.

In enterprise mode, keep `project.md` short: current work, next suggested action, memory index, and open uncertainties. Put detailed long-term knowledge under `.agent-loop/project/*.md`. Use `project-memory-mode.md` for triggers and routing.

Architecture defaults are DDD-inspired, but code layouts are advisory and stack-adapted. New projects may use a confirmed scaffold. Existing projects should record current structure and framework conventions instead of being reshaped without explicit human approval.

If a rule is both project-critical and needed on every agent startup, summarize it in `AGENTS.md` and keep details in `project.md`.

## Directory-Level Guidance

Suggest directory-level `AGENTS.md` only for long-lived boundaries with their own rules.

Good candidates:

- app roots: `apps/web/`, `backend/`, `frontend/`
- packages with independent APIs or tests: `packages/core/`, `packages/db/`
- test strategy roots: `tests/e2e/`, `tests/api/`
- security/data/runtime boundaries
- plugin or extension roots
- docs roots with their own fact-source rules

Poor candidates:

- single component folders
- ordinary utilities
- feature implementation folders
- temporary migration folders
- directories whose rules duplicate the parent

Ask:

```text
Does this directory have a distinct tech stack?
Does it have distinct verification commands?
Does it define a security/data/architecture boundary?
Does it have dependency direction rules?
Do agents often need special warnings here?
Would this rule still matter next month?
```

If mostly yes, propose a directory `AGENTS.md`. If no, keep the rule in `project.md`, `tasks.md`, or `notes.md`.

## New Directory Creation Rule

When a task creates a new durable directory, classify it before writing guidance:

```text
boundary directory = consider AGENTS.md
ordinary implementation directory = no AGENTS.md
temporary directory = no AGENTS.md
```

Boundary directories include new app roots, package roots, service roots, test roots, plugin roots, security/data/runtime boundaries, and docs roots with their own source-of-truth rules.

If it is a boundary directory:

1. Add or update the directory entry in `.agent-loop/project.md`.
2. Propose a directory-level `AGENTS.md` using `templates/directory-AGENTS.md`.
3. Ask human confirmation before writing it.
4. If declined, record `Guidance: not needed` or `Guidance: deferred` in `project.md`.

Do not create a `CLAUDE.md` in every directory by default. Prefer directory `AGENTS.md`; create a `CLAUDE.md` pointer only if the project explicitly needs Claude-specific discovery there.

## Sync Triggers

During Drift Check, Submit, or Close, ask whether to update `AGENTS.md` only when long-term startup guidance changed:

- package manager or major commands changed
- test/lint/typecheck commands changed
- architecture or dependency direction changed
- directory responsibility changed
- security, auth, data, tenant, or approval boundary changed
- project starts using or stops using a required skill/workflow
- project-skill discovery, loading, lifecycle, or execution-gate startup guidance changed

Do not sync `AGENTS.md` for normal feature progress.

## Template Use

Use:

```text
templates/root-AGENTS.md
templates/root-CLAUDE.md
templates/directory-AGENTS.md
```

Then adapt to the actual project. Keep each `AGENTS.md` concise and avoid repeating parent content.

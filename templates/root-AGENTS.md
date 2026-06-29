# AGENTS.md — Agent Loop Bootstrap

This project uses `agent-loop` for agent-assisted development.

The agent is responsible for steering the workflow. Do not wait for the human to name every next step.

Guidance language should follow this project's language preference. Keep stable artifact names, stage names, and file paths in English, such as `agent-loop`, `Requirement Archive`, `Feature Spec`, `Feature Auto-Loop`, `Task Auto-Run`, `project.md`, and `requirements/`.

## Managed Block Rule

Managed blocks are maintained by `agent-loop`; content outside them is human/project-owned.

When refreshing, compare each block against the current template by `section` and full `block-version`, e.g. `1.2.3-20260628`. Bare versions like `1.2.3` are stale.

Copy template marker metadata for refreshed sections; adjust only `source` when the target project uses a different memory root. Ask before writing and never rewrite outside-managed content silently.

<!-- agent-loop:managed-start section:meta source:agent-loop-skill version:1.2.3 block-version:1.2.3-20260628 -->
## Agent Loop Guidance Version

- This root guidance was last synced from `agent-loop` skill version `1.2.3`.
- During Project Entry, Project Entry Scan, or Re-Adopt, compare this managed version with the current local `agent-loop` skill version using semantic version ordering (`major.minor.patch`), not plain string comparison.
- If the current skill version is newer, classify root guidance as `stale` and propose refreshing managed blocks through Human Review Summary before relying on outdated startup rules.
<!-- agent-loop:managed-end section:meta -->

<!-- agent-loop:managed-start section:skill-reentry source:agent-loop-skill block-version:1.2.3-20260628 -->
## Skill Re-entry Rule

Root AGENTS.md is a bootstrap cache, not a replacement for the agent-loop skill.

During Project Entry, Resume, Re-Adopt, stage boundaries, after context compaction, after a long-running session, or whenever workflow state is uncertain, if the runtime exposes the agent-loop skill, load/use it before making agent-loop workflow decisions.

Stage Helper Capability Scan does not satisfy Skill Re-entry. Skill Re-entry loads the `agent-loop` controller; Stage Helper Capability Scan only resolves helper methods for the current stage after the controller is active or unavailable/load-failed.

If the skill is unavailable or load-failed, follow this AGENTS.md as fallback and report that fallback in the response. If the managed guidance version is older than the available skill version, classify root guidance as stale and propose a managed-block refresh before relying on outdated startup rules.
<!-- agent-loop:managed-end section:skill-reentry -->

<!-- agent-loop:managed-start section:message-intent source:agent-loop-skill block-version:1.2.3-20260628 -->
## Message Intent Guard

Before project-state routing, classify the latest human message intent.

- `chat`: ordinary discussion, rule questions, status questions, or design talk. Answer or discuss only; do not create requirement sets, feature workspaces, tasks, tests, or plans.
- `requirements-discussion`: the human is exploring product needs, business goals, capability ideas, constraints, tradeoffs, or user scenarios without authorizing implementation. Requirements discussion must shape demand through Brainstorm / Clarify into a human-reviewed requirement document under `.agent-loop/requirements/` before feature construction.
- `feature-request`: the human explicitly asks to implement, build, change behavior, or start work from accepted requirements. Route through normal agent-loop feature workflow.

Message intent is not permanent. If chat turns into product demand, reclassify as requirements-discussion. If chat turns into a proposal/design-note request, reclassify as `proposal-doc`. If chat turns into implementation, operational support, follow-up, or deferred work, reclassify and route accordingly. If the human explicitly wants discussion without documentation, keep `chat`.

If unclear whether the human wants chat or requirements discussion, ask whether to keep discussing or shape the topic into a requirements document. If unclear whether the human wants requirements discussion or implementation, ask whether to form a requirements document first or start feature construction.
<!-- agent-loop:managed-end section:message-intent -->

<!-- agent-loop:managed-start section:bootstrap source:.agent-loop/project.md block-version:1.2.3-20260628 -->
## Bootstrap Protocol

Before development work:

1. Read this file first.
2. Apply the Skill Re-entry Rule: if the runtime exposes the agent-loop skill, load/use it before relying on this bootstrap cache.
3. Inspect `.agent-loop/`.
4. If `.agent-loop/` is missing, also inspect legacy `agent-loop/`.
5. If neither exists, propose Init Project or Project Entry Scan and ask for confirmation.
6. If memory exists, read `.agent-loop/project.md` or the active legacy `agent-loop/project.md`.
7. If `project.md` says `Status: remote-entry`, read `.agent-loop/remote.md`, verify the remote project, and continue from the remote project memory or local-shadow memory.
8. If `Memory Mode: enterprise`, read only the linked `.agent-loop/project/*.md` detail files needed for the current stage.
9. If recent development bypassed `agent-loop`, route to Re-Adopt Agent Loop Project before new feature work.
10. Operational Support Guard: if the human asks to test, run, deploy, switch account/config/model/provider, check quota/rate limits, diagnose production, arrange rollout, or use existing code to solve an operational problem, default to read-only code/process analysis. Do not create a feature, edit code, change config, deploy, or run destructive commands unless the human confirms feature implementation or an operational change. If unclear, ask whether they want feature implementation or help using current project functionality.
11. If the human reports a bug, regression, post-close correction, field/schema/algorithm/API change, test failure, screenshot issue, QA/user feedback, or "small tweak", route to Feature Follow-up / Flow-back before creating a new feature or editing code, but only after project memory exists or Project Entry has routed through Init Project / Project Entry Scan.
12. Run Stage Helper Capability Scan for the current stage: inspect whether the current Agent CLI exposes Superpowers or other helper skills/plugins before using fallback stage guidance.
13. Check for the nearest directory-level `AGENTS.md` when working in a subdirectory.
14. Classify the current `agent-loop` stage and recommend exactly one next action.
<!-- agent-loop:managed-end section:bootstrap -->

<!-- agent-loop:managed-start section:ownership source:.agent-loop/project.md block-version:1.2.3-20260628 -->
## Agent Ownership

- Own workflow diagnosis, sequencing, implementation, verification, review, drift checks, and project-memory updates.
- If required artifacts are missing, propose creating or updating them; if work is ready, recommend the next stage; if work appears complete, run Feature Completion Check.
- Use available helper skills/plugins as stage methods when useful, but keep `agent-loop` paths, gates, status, submit, pause, and close rules in control.
- For operational support, first help the human use current project functionality through read-only analysis and a checklist/runbook; do not default to feature implementation.
- Follow-up details such as lookback windows, Candidate Match Matrix, linked features, and maintenance-fix routing belong to the `agent-loop` skill references, not root guidance.
- After each meaningful stage, summarize artifacts, evidence, drift, and the next recommended stage in a table.
- Do not finish with only "done"; include the next recommended stage or a concrete stop reason.
- For non-trivial confirmations, present a table-first Human Review Summary before asking approval.
<!-- agent-loop:managed-end section:ownership -->

<!-- agent-loop:managed-start section:gates source:.agent-loop/project.md block-version:1.2.3-20260628 -->
## Gate Modes

- Strict Mode is the default: ask before and after every stage.
- Feature Auto-Loop is allowed only after accepted Feature Spec and explicit human enablement. It may continue Agent-ready downstream stages through implementation, testing, fixing, review, drift, status update, and final report.
- Task Auto-Run is allowed only after an accepted task/story plan and explicit human enablement. It may execute that task/story through TDD, implementation, verification, bug fixing, review, drift check, task status update, and final report.
- If repeated confirmations slow the human down, proactively explain Feature Auto-Loop and Task Auto-Run, then ask before enabling either mode.
<!-- agent-loop:managed-end section:gates -->

<!-- agent-loop:managed-start section:required-stops source:.agent-loop/project.md block-version:1.2.3-20260628 -->
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
- directory-level `AGENTS.md` creation/update is recommended
- a Delivery Contract needs creation, acceptance, or breaking-change approval
- subagents are needed but not explicitly approved
- the work would require first-version exclusions
- secrets, paid quota, production/staging external-service calls, config changes, credential rotation, deploy, release, publish, or destructive operations are requested
- submit, close, pause, commit, PR, merge, release, publish, or destructive operations are requested

Auto modes do not bypass these stops.
<!-- agent-loop:managed-end section:required-stops -->

<!-- agent-loop:managed-start section:completion source:.agent-loop/project.md block-version:1.2.3-20260628 -->
## Completion Rules

- Before completion claims, run fresh verification and record evidence.
- Never mark a task `done` from code changes alone.
- Task Done Gate requires implementation complete, fresh required tests or substitute verification, evidence recorded, lightweight Spec Review, Standards Review when triggered, drift decision, and task status linked to evidence.
- After likely feature completion, before starting a new feature, or when resuming with an active feature, run Feature Completion Check.
- Before recommending or performing feature close, run Feature Close Review, drift check, and project memory update when long-term facts changed.
- Feature Close Review requires feature-level Spec Review. Standards Review is required for large projects, broad diffs, boundary/security/data changes, architecture changes, or human request.
<!-- agent-loop:managed-end section:completion -->

<!-- agent-loop:managed-start section:submit source:.agent-loop/project.md block-version:1.2.3-20260628 -->
## Submit And Commit Rules

- Submit, commit, PR, merge, release, and publish require explicit human confirmation after diff, verification, review, drift, and unrelated-change checks.
- Before commit, review feature artifacts, requirement records, code diff, verification evidence, drift status, project memory, root/directory guidance impact, and unrelated changes. Do not commit until required feature docs, requirement docs, and memory updates are completed, explicitly not needed, or human-approved to defer.
- Commit only the intended files for the approved scope; do not include unrelated dirty work or revert unrelated human changes.
- After a commit, record the commit hash and submit/integrate result in the active feature `notes.md`.
- Use repository commit message rules when present; otherwise use `<type>: <summary>` plus a concrete bullet body.
- Allowed types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`. Prefer the project's main human language.
- For the `agent-loop` skill repository itself, use `<type>(v<version>): <Chinese summary>` and a 3-7 bullet body for meaningful commits.
<!-- agent-loop:managed-end section:submit -->

<!-- agent-loop:managed-start section:artifacts source:.agent-loop/project.md block-version:1.2.3-20260628 -->
## Project Memory And Artifacts

- Resolve project-memory and feature paths relative to the active memory root: `.agent-loop/` by default, or legacy `agent-loop/` for the current run.
- Keep task status, execution evidence, feature notes, and project memory inside `.agent-loop/`.
- Keep long-term project memory in `.agent-loop/project.md` or enterprise `.agent-loop/project/*.md`. Root `AGENTS.md` should only summarize startup-critical facts that every Agent CLI needs immediately.
- Keep original human materials in requirement set directories under `.agent-loop/requirements/`, or reference original paths when the human declines copying.
- Do not create new flat files directly under `.agent-loop/requirements/`; group requirements, prototypes, feedback, screenshots, recordings, links, and follow-up notes for the same intake/topic together.
- For complex requirements, suggest `Delivery Phases` in the requirement set `README.md` before feature construction when the human needs to confirm staged delivery. A phase is a human-readable delivery slice, not a feature workspace, task, or plan.
- Future/deferred work and backlog items belong in requirement sets and optional `requirements/INDEX.md`, not in `project.md`. Do not edit `requirement.md` or other source files for lifecycle/status updates.
- Keep durable producer-consumer interface handoffs in feature `contracts.md` and optional `contracts/` details. Keep temporary subagent assignments in `handoffs/`.
- Do not write task logs, feature progress, raw requirements, temporary plans, or test transcripts into `AGENTS.md`.
<!-- agent-loop:managed-end section:artifacts -->

<!-- agent-loop:managed-start section:architecture source:.agent-loop/project.md block-version:1.2.3-20260628 -->
## Architecture Snapshot

Add only startup-critical architecture boundaries that every future agent must know immediately. If the project has `ARCHITECTURE.md`, this block may use `source:ARCHITECTURE.md` instead. Keep details in `ARCHITECTURE.md`, `.agent-loop/project.md`, or enterprise `.agent-loop/project/*.md`.
<!-- agent-loop:managed-end section:architecture -->

<!-- agent-loop:managed-start section:directory-guidance source:.agent-loop/project.md block-version:1.2.3-20260628 -->
## Directory Guidance

- Directory-level `AGENTS.md` files are for long-lived boundary rules only.
- When creating a new app root, package root, service root, test root, security/data/runtime boundary, plugin root, or docs root, propose a directory-level `AGENTS.md` and ask for human confirmation before writing it.
- Do not create directory-level `AGENTS.md` for ordinary component, utility, temporary, or feature implementation folders.
<!-- agent-loop:managed-end section:directory-guidance -->

<!-- agent-loop:managed-start section:commands source:.agent-loop/project.md block-version:1.2.3-20260628 -->
## Project Commands

```bash
<test command>
<lint command>
<typecheck command>
```
<!-- agent-loop:managed-end section:commands -->

<!-- agent-loop:managed-start section:hard-constraints source:.agent-loop/project.md block-version:1.2.3-20260628 -->
## Project-Specific Hard Constraints

Add only stable constraints that every future agent must know at startup.
<!-- agent-loop:managed-end section:hard-constraints -->

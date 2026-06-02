# AGENTS.md — Project Guidance

This project uses `agent-loop` for agent-assisted development.

Guidance language should follow this project's language preference. Keep stable artifact names, stage names, and file paths in English, such as `agent-loop`, `Requirement Archive`, `Feature Spec`, `Task Auto-Run`, `project.md`, and `requirements/`.

## Agent Loop

- Before development work, inspect `agent-loop/`.
- If `agent-loop/project.md` says `Status: remote-entry`, read `agent-loop/remote.md`, verify the remote project, and continue from the remote project memory or local-shadow memory.
- If `agent-loop/` is missing, propose Init Project and ask for confirmation.
- If `agent-loop/` exists, read `agent-loop/project.md` and the active feature docs before acting.
- If `agent-loop/project.md` says `Memory Mode: enterprise`, read only the linked `agent-loop/project/*.md` detail files needed for the current stage.
- If the project used `agent-loop` before but recent development bypassed it, route to Re-Adopt Agent Loop Project: compare code reality with `agent-loop` docs, propose backfill, and ask human confirmation before continuing feature work.
- When working inside a subdirectory, also check for the nearest directory-level `AGENTS.md`.
- Treat architecture as DDD-inspired by default, but respect this project's language, framework, and existing directory conventions.
- Follow the selected gate mode: Strict Mode by default, Feature Auto-Loop only after accepted Feature Spec and explicit confirmation, Task Auto-Run only after accepted task/story plan and explicit confirmation.
- If repeated confirmations slow the human down, proactively explain Feature Auto-Loop and Task Auto-Run, then ask before enabling either mode.
- For non-trivial confirmations, present a table-first Human Review Summary before asking the human to approve.
- After each stage, summarize changed artifacts, evidence, drift, and the next recommended stage.
- Before completion claims, run fresh verification and record evidence.
- When work crosses a durable producer-consumer boundary such as API, event, data, UI behavior, library, or runtime, propose or read the feature Delivery Contract. Drafts may be created in Feature Auto-Loop, but human confirmation is required before acceptance and before breaking changes.
- After likely feature completion, before starting a new feature, or when resuming with an active feature, run Feature Completion Check and recommend close/pause/continue as appropriate.
- Before recommending or performing feature close, run Feature Close Review, drift check, and update project memory when long-term facts changed.
- During onboarding, re-adoption, drift check, or project memory update, recommend Enterprise Memory Mode when `project.md` is no longer a fast reliable entry point.
- Feature Close Review requires feature-level Spec Review; Standards Review is also required for large projects, broad diffs, boundary/security/data changes, architecture changes, or human request.

## Agent Ownership

- The agent is responsible for steering the development loop, not waiting for the human to name every next step.
- When the human gives a goal, requirement, bug, prototype, or vague product idea, classify the current `agent-loop` stage and recommend exactly one next action.
- If required artifacts are missing, propose creating or updating them.
- If work appears ready to continue, recommend the next stage.
- If work appears complete, run Feature Completion Check and recommend close, pause, or continue.
- Ask for human confirmation at required gates, but keep ownership of diagnosis, sequencing, verification, drift checks, and project-memory updates.

## Autonomous Execution After Approval

- After Feature Spec is accepted and the human explicitly enables Feature Auto-Loop, continue through Agent-ready downstream stages without asking at every step.
- After a task/story plan is accepted and the human explicitly enables Task Auto-Run, execute that task/story through TDD, implementation, verification, bug fixing, review, drift check, task status update, and final report.
- Never mark a task `done` from code changes alone. After implementation and fresh verification, keep or move the task to `review` until the Task Done Gate passes.
- Task Done Gate: implementation complete, required tests or substitute verification run fresh, evidence recorded, lightweight Spec Review recorded, Standards Review recorded when triggered, drift decision recorded, and task status linked to evidence.
- During autonomous execution, fix verification failures when the failure is inside accepted scope and does not require a new product, architecture, data, security, or external-service decision.
- Stop and ask when scope changes, requirements are ambiguous, tests require unavailable infrastructure, security/data boundaries change, broad architecture changes are needed, repeated verification fails, unrelated dirty work blocks progress, or submit/close/commit/PR/merge is requested.
- At the end of autonomous execution, summarize changed files, tests run, evidence, review findings, drift/backfill updates, remaining risks, and the recommended next action.

## Project Commands

```bash
<test command>
<lint command>
<typecheck command>
```

## Boundaries

- Keep task status, execution evidence, and feature notes inside `agent-loop/`.
- Keep durable producer-consumer interface handoffs in feature `contracts.md` and optional `contracts/` details. Keep temporary subagent assignments in `handoffs/`.
- Keep original human materials in requirement set directories under `agent-loop/requirements/`, or reference their original paths when the human declines copying.
- Do not create new flat files directly under `agent-loop/requirements/`; group requirements, prototypes, feedback, screenshots, recordings, links, and follow-up notes for the same intake/topic together.
- If legacy `agent-loop/inputs/` exists, treat it as read-only compatibility and propose migration to `agent-loop/requirements/` before new feature work.
- Do not write temporary task logs into `AGENTS.md`.
- Directory-level `AGENTS.md` files are for long-lived boundary rules only.
- When creating a new app root, package root, test root, security/data boundary, plugin root, or docs root, propose a directory-level `AGENTS.md` and ask for human confirmation before writing it.
- Do not create directory-level `AGENTS.md` for ordinary component, utility, temporary, or feature implementation folders.
- Auto modes do not bypass submit, commit, PR, merge, release, pause, close, risky change, or Human-gated decision confirmations.

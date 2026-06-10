# AGENTS.md — Agent Loop Bootstrap

This project uses `agent-loop` for agent-assisted development.

The agent is responsible for steering the workflow. Do not wait for the human to name every next step.

Guidance language should follow this project's language preference. Keep stable artifact names, stage names, and file paths in English, such as `agent-loop`, `Requirement Archive`, `Feature Spec`, `Feature Auto-Loop`, `Task Auto-Run`, `project.md`, and `requirements/`.

## Managed Block Rule

Sections wrapped in `agent-loop:managed-start` / `agent-loop:managed-end` are maintained by `agent-loop`.

Agents may propose updates to managed blocks when source facts change, but must ask for human confirmation before writing. Content outside managed blocks is human/project-owned and must not be rewritten automatically.

<!-- agent-loop:managed-start section:bootstrap source:.agent-loop/project.md -->
## Bootstrap Protocol

Before development work:

1. Read this file first.
2. Inspect `.agent-loop/`.
3. If `.agent-loop/` is missing, also inspect legacy `agent-loop/`.
4. If neither exists, propose Init Project or Existing Project Onboarding and ask for confirmation.
5. If memory exists, read `.agent-loop/project.md` or the active legacy `agent-loop/project.md`.
6. If `project.md` says `Status: remote-entry`, read `.agent-loop/remote.md`, verify the remote project, and continue from the remote project memory or local-shadow memory.
7. If `Memory Mode: enterprise`, read only the linked `.agent-loop/project/*.md` detail files needed for the current stage.
8. If recent development bypassed `agent-loop`, route to Re-Adopt Agent Loop Project before new feature work.
9. Check for the nearest directory-level `AGENTS.md` when working in a subdirectory.
10. Classify the current `agent-loop` stage and recommend exactly one next action.
<!-- agent-loop:managed-end section:bootstrap -->

<!-- agent-loop:managed-start section:ownership source:.agent-loop/project.md -->
## Agent Ownership

- Own workflow diagnosis, sequencing, implementation, verification, review, drift checks, and project-memory updates.
- If required artifacts are missing, propose creating or updating them.
- If work appears ready to continue, recommend the next stage.
- If work appears complete, run Feature Completion Check and recommend close, pause, or continue.
- When the human reports a bug, regression, post-close correction, field/schema change, algorithm change, API mismatch, test failure, or QA/user feedback, inspect recent features before creating a new feature and recommend flow-back, linked new feature, maintenance fix, or investigation.
- After each stage, summarize changed artifacts, evidence, drift, and the next recommended stage.
- Do not finish with only "done"; include the next recommended stage or a concrete stop reason.
- For non-trivial confirmations, present a table-first Human Review Summary before asking approval.
<!-- agent-loop:managed-end section:ownership -->

<!-- agent-loop:managed-start section:gates source:.agent-loop/project.md -->
## Gate Modes

- Strict Mode is the default: ask before and after every stage.
- Feature Auto-Loop is allowed only after accepted Feature Spec and explicit human enablement. It may continue Agent-ready downstream stages through implementation, testing, fixing, review, drift, status update, and final report.
- Task Auto-Run is allowed only after an accepted task/story plan and explicit human enablement. It may execute that task/story through TDD, implementation, verification, bug fixing, review, drift check, task status update, and final report.
- If repeated confirmations slow the human down, proactively explain Feature Auto-Loop and Task Auto-Run, then ask before enabling either mode.
<!-- agent-loop:managed-end section:gates -->

<!-- agent-loop:managed-start section:required-stops source:.agent-loop/project.md -->
## Required Stops

Stop and ask when:

- scope changes or requirements are ambiguous
- product, design, architecture, security, data, approval, or public-interface decisions are unclear
- tests require unavailable infrastructure
- security/data boundaries or broad architecture would change
- repeated verification fails
- unrelated dirty work blocks progress
- a Delivery Contract needs creation, acceptance, or breaking-change approval
- subagents are needed but not explicitly approved
- submit, close, pause, commit, PR, merge, release, publish, or destructive operations are requested

Auto modes do not bypass these stops.
<!-- agent-loop:managed-end section:required-stops -->

<!-- agent-loop:managed-start section:completion source:.agent-loop/project.md -->
## Completion Rules

- Before completion claims, run fresh verification and record evidence.
- Never mark a task `done` from code changes alone.
- Task Done Gate requires implementation complete, fresh required tests or substitute verification, evidence recorded, lightweight Spec Review, Standards Review when triggered, drift decision, and task status linked to evidence.
- After likely feature completion, before starting a new feature, or when resuming with an active feature, run Feature Completion Check.
- Before recommending or performing feature close, run Feature Close Review, drift check, and project memory update when long-term facts changed.
- Feature Close Review requires feature-level Spec Review. Standards Review is required for large projects, broad diffs, boundary/security/data changes, architecture changes, or human request.
<!-- agent-loop:managed-end section:completion -->

<!-- agent-loop:managed-start section:artifacts source:.agent-loop/project.md -->
## Project Memory And Artifacts

- Resolve project-memory and feature paths relative to the active memory root: `.agent-loop/` by default, or legacy `agent-loop/` for the current run.
- Keep task status, execution evidence, feature notes, and project memory inside `.agent-loop/`.
- Keep original human materials in requirement set directories under `.agent-loop/requirements/`, or reference original paths when the human declines copying.
- Do not create new flat files directly under `.agent-loop/requirements/`; group requirements, prototypes, feedback, screenshots, recordings, links, and follow-up notes for the same intake/topic together.
- If legacy `.agent-loop/inputs/` or visible-root `agent-loop/inputs/` exists, treat it as read-only compatibility and propose migration to `.agent-loop/requirements/` before new feature work.
- Keep durable producer-consumer interface handoffs in feature `contracts.md` and optional `contracts/` details. Keep temporary subagent assignments in `handoffs/`.
- Do not write task logs, feature progress, raw requirements, temporary plans, or test transcripts into `AGENTS.md`.
<!-- agent-loop:managed-end section:artifacts -->

<!-- agent-loop:managed-start section:architecture source:.agent-loop/project.md -->
## Architecture Snapshot

Add only startup-critical architecture boundaries that every future agent must know immediately. If the project has `ARCHITECTURE.md`, this block may use `source:ARCHITECTURE.md` instead. Keep details in `ARCHITECTURE.md`, `.agent-loop/project.md`, or `.agent-loop/onboarding-db/`.
<!-- agent-loop:managed-end section:architecture -->

<!-- agent-loop:managed-start section:directory-guidance source:.agent-loop/project.md -->
## Directory Guidance

- Directory-level `AGENTS.md` files are for long-lived boundary rules only.
- When creating a new app root, package root, service root, test root, security/data/runtime boundary, plugin root, or docs root, propose a directory-level `AGENTS.md` and ask for human confirmation before writing it.
- Do not create directory-level `AGENTS.md` for ordinary component, utility, temporary, or feature implementation folders.
<!-- agent-loop:managed-end section:directory-guidance -->

<!-- agent-loop:managed-start section:commands source:.agent-loop/project.md -->
## Project Commands

```bash
<test command>
<lint command>
<typecheck command>
```
<!-- agent-loop:managed-end section:commands -->

<!-- agent-loop:managed-start section:hard-constraints source:.agent-loop/project.md -->
## Project-Specific Hard Constraints

Add only stable constraints that every future agent must know at startup.
<!-- agent-loop:managed-end section:hard-constraints -->

# Existing Project Onboarding Scan

Use this file when taking over an existing codebase without reliable `agent-loop` memory, or when `project.md` is too thin to guide future feature work.

If the existing codebase is remote and the local directory is only an entry point, load `remote-project-discovery.md` first. Do not run this onboarding against an empty local directory unless local-shadow mode has been selected and every finding will include remote evidence.

## Goal

Do not read the whole repository. Build a trustworthy project map quickly:

```text
startup docs -> shallow structure -> commands -> architecture profile -> capabilities -> boundaries -> guidance -> uncertainties -> human confirmation
```

The result is a draft `.agent-loop/project.md` that is useful enough for the next feature, with evidence and confidence labels.

For remote projects, the draft `project.md` should live next to the remote source of truth when remote writes are allowed. If not, keep it in local-shadow mode and label code facts with remote location.

## Onboarding Mode Gate

This file is the entry and Quick Onboarding path. Do not turn it into a Deep Scan manual.

When the human asks to take over, understand, or continue an existing project, explain the available modes:

| Mode | Use When | Output |
|---|---|---|
| Quick Onboarding | the human wants to safely continue feature work soon | `.agent-loop/project.md`, base folders, guidance proposal, uncertainties |
| Deep Project Onboarding Scan | the human wants newcomer-friendly project understanding or long-term onboarding docs | Quick outputs plus `.agent-loop/onboarding-db/`, diagrams, and backfill proposal |
| Targeted Onboarding Scan | the human asks about one module, flow, async task, deployment path, or problem area | focused onboarding-db update proposal for that scope |

If the human chooses Deep or Targeted, load:

```text
project-onboarding-scan.md
onboarding-db.md
onboarding-db-templates.md
```

If the human rejects Deep, do Quick only. Do not create onboarding-db or diagrams.

## Core Rules

- Existing docs are clues.
- Code and tests are current fact.
- CI/build scripts reveal real commands.
- Low-confidence findings must be labeled, not silently treated as truth.
- Do not start feature implementation during onboarding.
- Ask human confirmation before writing `.agent-loop/`, `project.md`, `AGENTS.md`, `CLAUDE.md`, or directory-level guidance.
- Ask human confirmation before creating `.agent-loop/onboarding-db/` or onboarding diagrams.
- Subagents are optional accelerators for large-project onboarding, not a dependency.
- Use DDD-inspired architecture mapping, but record existing code reality. Do not rename or move code during onboarding.
- Root `AGENTS.md` and `CLAUDE.md` are startup guidance artifacts for every `agent-loop`-managed project. During onboarding, check both. `CLAUDE.md` must load or point to `AGENTS.md`; do not maintain duplicated root guidance in two files.
- Do not finish onboarding after writing only `.agent-loop/project.md`. Root guidance must be present, created, or explicitly deferred by the human, and that status must be recorded in `project.md`.

## Large Project Trigger

Treat onboarding as large or complex when any of these are true:

- roughly more than 100k lines of code
- monorepo or workspace with multiple `apps/`, `packages/`, or `services/`
- more than one runtime entry point such as web, admin, API, worker, CLI, or mobile
- 3 or more major boundaries such as UI, API, domain, DB, auth, jobs, E2E
- more than 2 test categories such as unit, API, integration, E2E, contract
- multiple build systems, package managers, or CI pipelines
- multiple root or directory-level `AGENTS.md` / `CLAUDE.md`
- docs and code reality may disagree
- a single agent cannot confidently hold the project shape in one pass

When these triggers apply and subagents are available, recommend subagent scanning. If subagents are unavailable or the human declines, continue with the same layered scan in a single agent session.

## Optional Subagent Scan

Use subagents only after human confirmation.

The main agent must first do a shallow repo-shape scan, then dispatch bounded scan briefs. Suggested scan lanes:

```text
startup-docs
commands-ci-tooling
capabilities-entrypoints
data-schema-storage
tests-verification
guidance-boundaries
```

Each subagent must return:

```text
Findings
Evidence
Confidence
Uncertainties
Suggested project.md entries
Files read
```

Subagents must not:

- write `project.md`
- create or update `AGENTS.md` / `CLAUDE.md`
- start feature implementation
- make architecture decisions
- claim global project understanding
- submit, pause, or close anything

The main agent owns synthesis, conflict resolution, confidence labels, and the human-facing project memory proposal.

## Scan Layers

### Layer 1: Startup Docs

Read only likely entry files first:

```text
AGENTS.md / CLAUDE.md / GEMINI.md
README.md
CONTRIBUTING.md
docs/ index files
CHANGELOG / release notes if obvious
```

Extract:

- project purpose
- setup commands
- test commands
- documented architecture
- domain vocabulary
- existing agent instructions
- warnings or constraints

### Layer 2: Repo Shape

Inspect shallow structure:

```text
top-level directories
apps/ packages/ services/
src/ lib/ backend/ frontend/
tests/ e2e/ integration/
config and CI directories
```

Do not recursively read implementation files unless needed to identify boundaries.

### Layer 3: Runtime And Tooling

Inspect manifests and orchestration:

```text
package.json / pnpm-workspace.yaml / turbo.json / nx.json
pyproject.toml / requirements.txt
go.mod / Cargo.toml
Makefile / Taskfile / justfile
Dockerfile / docker-compose*
.github/workflows / .gitlab-ci.yml
test runner configs
lint/typecheck configs
```

Record commands with confidence:

```md
- `pnpm test`: likely unit tests
  - Evidence: package.json scripts.test
  - Confidence: high
```

### Layer 3b: Architecture Profile

Classify with evidence:

```text
Project Shape: frontend | backend | fullstack | worker | cli/library
Language Adapter: java | python | node-ts | go | csharp | rust | cpp | other
Framework Adapter: spring-boot | fastapi | django | nestjs | express | aspnet-core | rails | laravel | none | other
DDD Intensity: light | standard | enterprise
Layout Status: existing reality | proposed scaffold | mixed
```

Map actual directories to DDD-inspired roles when useful:

```text
domain / application-use-case / infrastructure-adapter / interface-controller / ui-feature / test-root
```

Do not treat the adapter as a mandate. Framework convention and existing project reality win unless the human explicitly asks for architecture migration.

### Layer 4: Capability Map

Identify existing product or platform capabilities from public entry points:

- routes/controllers/actions
- pages/screens
- schemas/models/migrations
- tests/specs
- docs or changelog

Write capabilities with evidence:

```md
- Auth: implemented
  - Evidence: apps/api/routes/auth.ts, tests/auth.test.ts
  - Confidence: high
- Project invitations: partial
  - Evidence: db migrations mention invitations; no E2E found
  - Confidence: medium
```

### Layer 5: Boundary Map

Identify durable boundaries:

- UI/app surfaces
- API boundaries
- domain/core modules
- database/schema/migration boundary
- auth/permission/security boundary
- background jobs/events
- test roots
- shared packages/types
- docs/source-of-truth areas

Write them into `project.md` `Directory Map`.

### Layer 6: Guidance Inventory

Find existing guidance:

```text
root AGENTS.md / CLAUDE.md / GEMINI.md
directory-level AGENTS.md / CLAUDE.md
CONTRIBUTING / STYLE / docs/architecture
```

For each stable boundary, record:

```text
Guidance: root only | has AGENTS.md | propose AGENTS.md | not needed | deferred
```

Only propose directory `AGENTS.md` for long-lived boundaries. Do not create it during the scan without confirmation.

### Layer 7: Uncertainty And Questions

Create an uncertainty list:

```md
## Onboarding Uncertainties

- Billing capability appears present, but no tests were found.
  - Evidence:
  - Confidence: low
  - Recommended follow-up:
```

Ask only high-impact questions. Prefer targeted scans when the answer is in code.

## Output Before Writing

Before mutating files, summarize:

```text
Project summary:
Tech stack:
Capabilities:
Boundaries:
Commands:
Guidance files:
Low-confidence findings:
Recommended project.md updates:
Recommended onboarding mode:
Recommended onboarding-db updates:
Recommended AGENTS.md / CLAUDE.md updates:
Human gate:
```

## Write After Confirmation

After human confirmation, write or update:

```text
.agent-loop/project.md
.agent-loop/onboarding-db/ only when Deep or Targeted onboarding docs are confirmed
.agent-loop/requirements/
.agent-loop/features/
AGENTS.md
CLAUDE.md -> AGENTS.md or pointer
directory AGENTS.md only when explicitly confirmed
```

Exit requirements:

```text
project.md accepted by human
AGENTS.md status = present | created | human-deferred
CLAUDE.md status = points-to-AGENTS | created-pointer | human-deferred
next stage selected
```

## Feature Continuation

After onboarding:

1. Ask what feature to continue or start.
2. Do a targeted deep scan only for that feature's boundaries.
3. Create or update the feature workspace.
4. Continue the normal agent-loop stages.

# Project Entry Scan For Existing Projects

Use this file when taking over an existing codebase without reliable `agent-loop` memory, or when `project.md` is too thin to guide future feature work.

This stage is safe-entry only. It does not generate newcomer documentation. Evidence-Graph + DDD Onboarding lives in `references/onboarding-knowledge-base.md` and should run only after Project Entry Scan or reliable project memory.

## Goal

Build enough evidence-backed project memory for safe continuation:

```text
startup docs -> shallow repo shape -> commands -> architecture profile -> capabilities -> boundaries -> guidance status -> uncertainties -> human confirmation
```

Outputs are limited to:

- `.agent-loop/project.md` proposal or update
- root `AGENTS.md` / `CLAUDE.md` status and repair proposal
- stable command, boundary, capability, and uncertainty facts
- recommended next stage, such as Start Feature, Operational Support, Requirement Archive, Re-Adopt, or Targeted Feature Scan

Do not create:

- `.agent-loop/onboarding-db/`
- `onboarding-spec.md`
- `onboarding-tasks.md`
- module / flow playbooks
- onboarding diagrams
- Quick / Deep / Targeted onboarding mode records
- directory-first module/flow/runtime docs

If the human asks for newcomer-facing docs, durable onboarding docs, or a guided learning path, explain that Project Entry Scan must first establish safe project memory and offer one of two next actions:

1. run Project Entry Scan now so development can continue safely
2. after reliable memory exists, run Evidence-Graph + DDD Onboarding through `references/onboarding-knowledge-base.md`

## Core Rules

- Existing docs are clues.
- Code and tests are current fact.
- CI/build scripts reveal real commands.
- Low-confidence findings must be labeled, not silently treated as truth.
- Do not read the whole repository.
- Do not start feature implementation during Project Entry Scan.
- Ask human confirmation before writing `.agent-loop/`, `project.md`, `AGENTS.md`, `CLAUDE.md`, or directory-level guidance.
- Subagents are optional accelerators for large Project Entry Scan only after human confirmation.
- Use DDD-inspired architecture mapping when useful, but record existing code reality. Do not rename or move code during Project Entry Scan.
- Root `AGENTS.md` and `CLAUDE.md` are startup guidance artifacts for every `agent-loop`-managed project. During Project Entry Scan, check both. `CLAUDE.md` must load or point to `AGENTS.md`; do not maintain duplicated root guidance in two files.
- Do not finish Project Entry Scan after writing only `.agent-loop/project.md`. Root guidance must be present, created, or explicitly deferred by the human, and that status must be recorded in `project.md`.

## Remote Projects

If the existing codebase is remote and the local directory is only an entry point, load `remote-project-discovery.md` first. Do not scan an empty local directory as if it were the source of truth unless local-shadow mode has been selected and every finding will include remote evidence.

For remote projects, the draft `project.md` should live next to the remote source of truth when remote writes are allowed. If not, keep it in local-shadow mode and label code facts with remote location.

## Large Project Trigger

Treat Project Entry Scan as large or complex when any of these are true:

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
- create legacy onboarding-db documents
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

### Layer 4: Architecture Profile

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

### Layer 5: Capability Map

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

### Layer 6: Boundary Map

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

### Layer 7: Guidance Inventory

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

### Layer 8: Uncertainty And Questions

Create an uncertainty list:

```md
## Project Entry Uncertainties

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
Architecture profile:
Capabilities:
Boundaries:
Commands:
Guidance files:
Low-confidence findings:
Recommended project.md updates:
Explicitly not doing:
- no onboarding-db generation
- no module / flow playbooks
- no onboarding diagrams
Recommended AGENTS.md / CLAUDE.md updates:
Human gate:
```

For focused explanation requests, answer from existing docs/code as chat or operational support. Do not produce a full `project.md` proposal unless the human confirms broader Project Entry Scan.

## Write After Confirmation

After human confirmation, write or update only confirmed items:

```text
.agent-loop/project.md
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

After Project Entry Scan:

1. Ask what feature, operational task, or requirement to continue or start.
2. If the selected work has unclear impact boundaries, do Targeted Feature Scan.
3. Create or update the feature/requirement workspace only after human confirmation.
4. Continue the normal agent-loop stages.

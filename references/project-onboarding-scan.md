# Project Onboarding Scan

Use this when the human chooses `Deep Project Onboarding Scan`, asks to be guided through an existing project, or asks for a focused understanding of one module, flow, async task, deployment path, or problem area.

This reference does not replace `existing-project-onboarding.md`. That file is the entry/router and Quick Onboarding path. This file defines the Deep and Targeted scan behavior.

## Goal

Create a human-readable project understanding map without producing a full repository graph:

```text
project shape -> docs -> shallow repo -> runtime/tooling -> entrypoints -> boundaries -> modules -> flows -> verification -> onboarding-db draft -> batch human review -> project memory backfill proposal
```

Code reality is the current fact base. Existing docs are clues. Do not deep-read every file.

## Modes

| Mode | Use When | Output |
|---|---|---|
| Quick Onboarding | human wants fast safe continuation | project memory and guidance proposal only |
| Deep Project Onboarding Scan | human wants newcomer-friendly project understanding | Quick outputs plus `.agent-loop/onboarding-db/`, necessary diagrams, and backfill proposal |
| Targeted Onboarding Scan | human asks about one module, flow, async job, deployment path, or problem area | focused onboarding-db update proposal for that scope only |

Ask the human to choose Quick or Deep before creating onboarding-db files. If the human only asks a targeted question, do not run full Deep Scan.

After Deep Scan creates onboarding-db, future "onboard me" requests should use `onboarding-db.md` Guided Newcomer Onboarding instead of rerunning Deep Scan by default. Rerun or refresh Deep Scan only when freshness, coverage, or code reality makes the existing onboarding-db unreliable.

## P0 / P1 / P2 Priority

The scan is prioritized, not a mechanical linear checklist.

| Priority | Purpose | Includes | Output |
|---|---|---|---|
| P0 | avoid wrong takeover and make safe continuation possible | project shape, existing docs, shallow repo, runtime/tooling, entrypoints, high-risk unknowns | Quick Onboarding, `project.md` proposal, risk list |
| P1 | let a human understand the main system | module map, boundaries, core flow, commands/tests verification | onboarding-db main reading path, module relationship map, boundary map, at least one core flow |
| P2 | support long-term complex maintenance | async/events, jobs, data model, deployment, integrations, decisions/history, change impact | topic docs, focused diagrams, project memory backfill proposal |

Rules:

- Quick Onboarding runs P0 only and records P1/P2 follow-ups.
- Deep Scan runs P0, then P1, then only the P2 areas justified by project reality and Layout Mode.
- Targeted Scan runs the minimum P0 context needed for safety, then the selected target area.
- Large or unclear projects should not jump directly to P2.

## Layout Mode

Deep Scan must choose or recommend an Onboarding DB Layout Mode before proposing files.

| Layout | Trigger | File Strategy |
|---|---|---|
| Compact | single app, few modules, one main runtime, little async, simple tests | 5-7 combined docs |
| Standard | ordinary business system with multiple boundaries such as UI/API/DB/jobs | 8-12 docs, core topics independent |
| Expanded | 100k+ LOC, 5+ durable modules, 2+ test systems, multiple environments/integrations, complex async/deployment | 12-18 docs, split only genuinely complex modules/flows |

Layout controls physical file granularity, not understanding coverage. Do not omit a core understanding dimension just because the layout is Compact.

## Layout Mode Decision Rules

Choose or recommend Layout Mode from both project reality and human intent:

1. Inspect evidence first: project shape, durable modules, runtimes, test systems, async/deployment complexity, environments, and onboarding goal.
2. Recommend the smallest layout that still preserves all Required Understanding Dimensions.
3. Default toward Compact when the project is small, unclear, or the human wants a fast takeover.
4. Recommend Standard when multiple stable boundaries need independent reading paths.
5. Recommend Expanded only when durable module boundaries, complex flows, multiple test systems/environments, or repeated maintenance needs justify split files.
6. If the human explicitly chooses a layout, respect it after explaining risks and tradeoffs. Do not silently override the human's layout choice.
7. If the selected layout later becomes insufficient, propose a layout upgrade through Batch Human Review; do not reorganize onboarding-db silently.

## Required Understanding Dimensions

Every layout must cover:

| Dimension | Must Answer |
|---|---|
| Project overview | what the project does, users, tech stack, capabilities, current state |
| Run and verify | install, run, test, build, lint/typecheck, E2E if present |
| Code navigation | major directories, modules, entrypoints, key files |
| Architecture | UI/API/domain/DB/jobs/external boundaries and call direction |
| Business flows | core user/business paths and state changes |
| Change impact | likely modules, APIs, data, tests affected by common changes |
| Risks | unknowns, doc/code conflicts, unverified commands, missing diagrams |

If something is not found or not applicable, say `Not found`, `Not applicable`, or `Unknown` with evidence.

## Scan Steps

1. Project Shape: identify single project vs Project Group candidate. Project Group is deferred; if detected, stop cross-project mapping and ask whether to scan the current subproject.
2. Existing Docs: read README, guidance files, docs index, changelog, API/architecture docs. Treat docs as clues.
3. Shallow Repo: inspect top-level app/package/service/test/config/CI/deployment directories. Avoid whole-repo deep reads.
4. Runtime / Tooling: inspect manifests, task runners, Docker/CI/test configs. Record commands with confidence.
5. Entrypoints: locate runtime, UI, API, config, service, model, worker, job, integration, and test entrypoints.
6. Module Map: identify durable modules or bounded contexts. Record purpose, boundary, entrypoints, flows, key files, evidence, confidence.
7. Boundary Map: map UI, API, domain, DB/migrations, jobs/workers, external services, auth, shared/generated packages.
8. Core Module Call Chain Extraction: for each core module, document the module-level call chain or explicitly mark why it is support-only, unknown, or not applicable.
9. Core Flow Extraction: document 3-7 most important flows when possible; at least one initial core flow must be diagrammed or explicitly marked unknown.
10. Async / Events / Jobs: if queues, subscriptions, callbacks, workers, schedulers, retries, DLQs, or compensation exist, draft docs and focused diagrams.
11. Deployment / Operations: separate local setup, environment config, production deployment, rollback, health checks, logs/metrics/tracing, and deployment topology.
12. Commands / Tests Verification: classify commands as high/medium/low confidence based on run evidence, CI usage, or script inference.
13. Onboarding DB Draft: draft human-readable docs according to Layout Mode.
14. Batch Human Review: show files/facts/evidence/confidence before writing.
15. Project Memory Backfill Proposal: propose only stable long-term summaries for `project.md` or `project/*.md`.

When Standard or Expanded Layout Mode is selected, use `onboarding-db-templates.md` derivation tables to decide whether a file should be copied from a concrete template or derived from a Compact template section. Missing one-to-one templates are not a reason to skip required understanding dimensions.

## Diagram Rules

Generate small diagrams that answer one question. Do not create full function graphs, full file dependency graphs, or whole-repo knowledge graphs.

Initial Deep Scan must propose:

- module relationship map
- boundary map
- one core module call-chain diagram for each core module, or an explicit `support-only`, `Unknown`, or `Not applicable` note with evidence
- at least one core flow diagram
- data entity map when persistent data exists
- deployment map when multiple environments, containers, or remote services exist

Core module call-chain diagrams are module-level diagrams, not function-level graphs. They should show:

```text
inbound trigger / caller
-> module entrypoint
-> application/use-case or service boundary
-> domain rule / core operation
-> data/external/job boundary
-> output / side effect
```

Do not draw every function call. The goal is to help a newcomer understand how a core module is entered, what it orchestrates, which dependencies it touches, and where behavior exits.

Discovery-triggered diagrams:

| Discovery | Diagram |
|---|---|
| durable module with business/runtime behavior | core module call chain |
| queue / broker / consumer / subscriber | async flow |
| cron / scheduler / worker / background job | job flow |
| state field and transitions | state flow |
| callback / webhook | integration flow |
| auth/token/role/permission flow | auth flow |
| object storage/upload/download/callback | file flow |
| retry/rollback/DLQ/manual compensation | failure recovery flow |

When state/status fields are important to a core flow, also capture state-change trace evidence: trigger, writer, guard/condition, side effects, tests, and confidence. A legal state-flow diagram is not enough to answer "who changed this state?".

## Deployment Placement

Do not put all deployment facts in one document.

| Fact | Location |
|---|---|
| local run, ports, local required services | `setup-and-run.md` |
| env vars, dev/test/prod differences, containers, CI environment | `environment.md` or Compact equivalent |
| production deploy, release, rollback, operations, health checks, logs/metrics/tracing | `deployment-and-operations.md` when triggered |
| service/container/DB/queue/external topology | `diagrams/deployment-map.md` |
| stable environment summary for agent decisions | `project/environments.md` or `project.md` index |

Never write real secrets, tokens, passwords, or production connection strings.

## Subagent Scan

For large projects, subagents can scan bounded lanes after human confirmation.

Recommended lanes:

```text
docs-and-overview
commands-and-environments
directory-and-entrypoints
boundaries-and-integrations
core-flows-and-data-model
async-and-events
testing-and-verification
jobs-and-schedules
risks-and-unknowns
```

Subagents return only:

```text
Findings
Evidence
Confidence
Uncertainties
Suggested onboarding-db entries
Files read
```

They must not write docs, update project memory, create guidance, start feature work, or claim onboarding complete.

Main-agent merge flow:

```text
Subagent Returns -> Normalize Findings -> Deduplicate Facts -> Detect Conflicts -> Check Evidence Quality -> Assign Confidence -> Conflict Table -> Batch Human Review -> Confirmed Write
```

Conflict table:

| Conflict | Finding A | Finding B | Evidence A | Evidence B | Current Judgment | Action |
|---|---|---|---|---|---|---|

If evidence conflicts, code reality wins as current fact. If evidence is weak or business intent/history is involved, mark unknown and ask the human.

## Batch Human Review

Before writing multiple onboarding docs or facts, present a table:

| File / Item | Action | Change Summary | Source Evidence | Confidence | Affects Long-Term Memory | Suggested Action |
|---|---|---|---|---|---|---|

Allowed human choices:

```text
approve all
approve selected
revise selected
defer selected
skip this batch
```

High-confidence facts can be drafted automatically, but cannot become `reviewed` without human confirmation.

## Completion Criteria

Deep Scan is complete only when:

- Layout Mode is recorded
- README has reading paths and module reading paths
- overview/setup/code map are usable for a newcomer
- module relationship map and boundary map exist or are explicitly blocked
- every core module has a core module call-chain diagram, or an explicit support-only/unknown/not-applicable note with evidence
- at least one core flow exists or is explicitly unknown
- commands and tests have evidence/confidence
- risks and unknowns are recorded
- project memory backfill proposal was shown
- human confirmed the write batch

If any item is missing, say:

```text
Onboarding DB draft is usable but incomplete.
```

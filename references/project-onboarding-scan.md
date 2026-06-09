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
- Deep Scan runs P0, then P1, then the P2 areas justified by project reality.
- Targeted Scan runs the minimum P0 context needed for safety, then the selected target area.
- Large or unclear projects should not jump directly to P2.

## Onboarding DB Layout Mode

Deep Scan must record an Onboarding DB Layout Mode before proposing files.

Default: `Expanded`.

Use `Compact` or `Standard` only when the human explicitly requests fewer/simpler onboarding-db files, or when maintaining an existing onboarding-db already organized that way. Compact and Standard reduce physical file count only; they must not reduce explanation depth, diagram coverage, evidence chains, or required understanding dimensions.

| Layout | Trigger | File Strategy |
|---|---|---|
| Expanded | default for new Deep Scan | categorized docs such as `maps/`, `modules/`, `flows/`, `runtime/`, `domain/`, and `quality`; split by durable business/runtime boundary, not by code directory |
| Standard | human explicitly asks for fewer files, or existing onboarding-db is Standard | categorized docs with fewer focused splits; keep low-frequency topics combined |
| Compact | human explicitly asks for Compact, minimal files, fewer files, or merged docs; or existing onboarding-db is Compact | combined docs with clear README section map |

Onboarding DB Layout Mode controls physical file granularity, not understanding coverage. Do not omit a core understanding dimension just because the layout is Compact or Standard.

## Onboarding DB Layout Mode Decision Rules

Choose or recommend Onboarding DB Layout Mode from human intent first, with Expanded as the default:

1. Inspect evidence first: project shape, durable modules, runtimes, test systems, async/deployment complexity, environments, and onboarding goal.
2. Default to Expanded for new Deep Scan output, even for small projects.
3. Offer Compact or Standard only as a human-controlled tradeoff for fewer files, not as the agent's default recommendation.
4. If the human explicitly chooses Compact or Standard, respect it after explaining that the same understanding dimensions, diagrams, and evidence still apply.
5. If an existing onboarding-db uses Compact or Standard, keep that organization unless the human confirms reshaping.
6. If Compact or Standard later becomes hard to read, propose reshaping to Expanded through Batch Human Review; do not reorganize onboarding-db silently.

Default physical layout:

| Layout | Default physical structure |
|---|---|
| Expanded | default; use categorized structure such as `maps/`, `modules/`, `flows/`, `runtime/`, `domain/`, `quality/`, and optional `diagrams/` for standalone diagrams |
| Standard | human-requested or existing Standard; use fewer categorized docs and combine low-frequency topics |
| Compact | human-requested or existing Compact; may stay flat or lightly grouped, with README clearly mapping sections |

Categorized layout is for reading, not for mirroring the code tree. Keep it at most two levels deep under `onboarding-db/`.

## Required Understanding Dimensions

Every layout must cover:

| Dimension | Must Answer |
|---|---|
| Project overview | what the project does, users, tech stack, capabilities, current state |
| Run and verify | install, run, test, build, lint/typecheck, E2E if present |
| Code navigation | major directories, modules, entrypoints, key files |
| Architecture | UI/API/domain/DB/jobs/external boundaries and call direction |
| Business flows | core user/business paths and state changes |
| Data model | core entities, storage mapping, relationships, ownership, key fields, state fields, writers/readers, and migrations |
| Change impact | likely modules, APIs, data, tests affected by common changes |
| Evidence chain | file paths, symbols/objects, key parameters/fields, and what each source proves |
| Risks | unknowns, doc/code conflicts, unverified commands, missing diagrams |

If something is not found or not applicable, say `Not found`, `Not applicable`, or `Unknown` with evidence.

## Scan Steps

1. Project Shape: identify single project vs Project Group candidate. Project Group is deferred; if detected, stop cross-project mapping and ask whether to scan the current subproject.
2. Existing Docs: read README, guidance files, docs index, changelog, API/architecture docs. Treat docs as clues.
3. Shallow Repo: inspect top-level app/package/service/test/config/CI/deployment directories. Avoid whole-repo deep reads.
4. Runtime / Tooling: inspect manifests, task runners, Docker/CI/test configs. Record commands with confidence.
5. Entrypoints: locate runtime, UI, API, config, service, model, worker, job, integration, and test entrypoints.
6. Module Map: identify durable modules or bounded contexts. Record purpose, boundary, entrypoints, flows, key files, evidence, confidence, and whether a dedicated module doc is required.
7. Boundary Map: map UI, API, domain, DB/migrations, jobs/workers, external services, auth, shared/generated packages.
8. Core Module Call Chain Extraction: for each core module, document the module-level call chain or explicitly mark why it is support-only, unknown, or not applicable.
9. Core Flow Extraction: document 3-7 most important flows when possible; at least one initial core flow must be diagrammed or explicitly marked unknown.
10. Data Model Extraction: if persistent data exists, draft or update `domain/data-model.md` or Compact equivalent; record core entities, storage mapping, relationships, ownership, key fields, state fields, writers/readers, API/flow/job usage, migrations/seeds, tests, and evidence.
11. Entity Detail Split: create or recommend `domain/entities/<entity>.md` for complex core entities; keep simple lookup/config tables and non-semantic join tables in `domain/data-model.md`.
12. Async / Events / Jobs: if queues, subscriptions, callbacks, workers, schedulers, retries, DLQs, or compensation exist, draft docs and focused diagrams.
13. Deployment / Operations: separate local setup, environment config, production deployment, rollback, health checks, logs/metrics/tracing, and deployment topology.
14. Commands / Tests Verification: classify commands as high/medium/low confidence based on run evidence, CI usage, or script inference.
15. Evidence Chain Extraction: for every core module, core flow, core entity, major state change, async/job path, and major verification claim, record file path, symbol/object, key parameters/fields, what it does, and what it proves.
16. Onboarding DB Draft: draft human-readable docs according to Onboarding DB Layout Mode; default to Expanded for new Deep Scan output.
17. Batch Human Review: show files/facts/evidence/confidence before writing.
18. Project Memory Backfill Proposal: propose only stable long-term summaries for `project.md` or `project/*.md`.

Use `onboarding-db-templates.md` derivation tables to decide whether a file should be copied from a concrete template or derived from another template section. Missing one-to-one templates are not a reason to skip required understanding dimensions.

Core-module detail rule:

- `module-map.md` is an index and navigation document, not a place to dump every module detail.
- Create or recommend `modules/<module>.md` for core modules or bounded contexts with durable behavior, stable entrypoints, their own data/external dependencies, repeated maintenance needs, or repeated feature impact.
- Support-only areas such as `utils/`, `scripts/`, generated code, shared types, or test helpers may stay in the module map with evidence explaining why they do not need a dedicated module doc.

Flow-detail split rule:

- `flows-and-data.md` or `core-flows.md` may hold compact flow summaries, but complex business/runtime flows need `flows/<flow>.md`.
- Create or recommend `flows/<flow>.md` when a flow crosses multiple durable modules, has async/jobs/external callbacks, has important state transitions, has retry/compensation/failure paths, has multiple API/job entrypoints, affects multiple tests, or is repeatedly maintained.
- `flows/<flow>.md` must remain human-readable: diagram, quick notes, call-chain details, API/task/job entrypoints, responsibility boundaries, state changes, retry/failure paths, code reading order, verification hints, risks, and Evidence Chain.
- Do not create one flow doc per helper path. Split only business/runtime flows that give humans a useful reading path.

Data-model detail rule:

- Data model understanding is a first-class onboarding dimension, not an appendix hidden only inside flow docs.
- If the project has database tables, ORM models, schema files, migrations, persistent models, object-storage metadata, queue persistence, or other durable business objects, create or recommend `domain/data-model.md` or a Compact-equivalent `Data Model` section.
- `domain/data-model.md` is an index and relationship map. It should cover core entities, storage/model mapping, ownership, important relationships, key fields, state fields, readers/writers, flow/API/job usage, migrations/seeds, tests, evidence, and confidence.
- Create or recommend `domain/entities/<entity>.md` when an entity has many fields, complex state, multiple writers/readers, multiple related flows/API/jobs, migrations/history, derived fields, or repeated human questions.
- Do not create entity detail docs for simple lookup/config tables or join tables without business meaning; keep them in `domain/data-model.md` with evidence.
- If a complex entity is not split, record why it remains index-only.

## Diagram Rules

Onboarding diagrams are flowchart-first. **Deep Scan 的图要尽可能完整**，把模块/流程/数据模型的全貌画出来，不能只画一个简略概览。Quick Scan 可以保持精简，但 Deep Scan 必须完整。不要创建全仓库文件依赖图或 whole-repo knowledge graphs。

**Diagram completeness rule**: 一张图不够描述就分多张。模块调用链路可以画多张流程图，每张覆盖一个子流程或一个入口点。

Default diagram rules:

- prefer Mermaid `flowchart TB` or `flowchart LR`
- use `subgraph` to separate User, API, Domain, DB, Jobs/Workers, External Services, State, and Runtime layers
- use color classes for layer identity when the diagram has 4+ node types
- include key route, task, table/model, state, queue, external service, and object-storage names when evidenced
- **Deep Scan 下， diagrams 画到 Service/UseCase/Domain/Repository/External 级别**，展示完整的调用链路，不能只画一个抽象的 "Service" 节点
- **每个图必须有 "How To Read" 说明**，解释这张图回答什么问题、怎么看、颜色/形状的含义

Use `sequenceDiagram` **当核心模块涉及异步 jobs、外部服务调用、回调/webhook、WebSocket、重试补偿、或多服务交互时**。Sequence diagram 不是可选补充，而是上述场景下的**强制要求**。对于没有异步/外部交互的简单模块，flowchart 即可。

Initial Deep Scan must propose:

- module relationship map
- boundary map
- **at least one complete diagram for each core module** (flowchart showing the full call chain from entry to exit; support-only modules may be marked with evidence)
- **sequence diagram for each core module with async/external/callback/WebSocket interactions**
- at least one core flow diagram (split into multiple diagrams if one is not enough)
- **complete data entity map** when persistent data exists (all core entities with key fields and relationships; split into subgraphs if the project is large)
- **model usage flow map** showing which flows/APIs/jobs use which entities
- single-entity relationship diagram when a core entity is too complex to understand from the global data entity map
- deployment map when multiple environments, containers, or remote services exist

Core module call-chain diagrams should show the **complete path** from entry to exit:

```text
inbound trigger / caller
-> module entrypoint (specific API route / handler / WebSocket event)
-> application/use-case or service boundary (specific Service class / UseCase)
-> domain rule / core operation (specific domain functions / business rules)
-> data/external/job boundary (specific Repository / ORM model / External API client / Task dispatcher)
-> output / side effect (specific response / DB write / async job trigger / external callback)
```

**Deep Scan 下，把每个关键节点都画出来**，不能只写一个抽象的 "Service" 或 "Domain"。如果一张图放不下，分成多张：一张给 API 入口、一张给后台任务、一张给外部回调等。目标是让 newcomer 看完图就能说出"这个模块从哪进、经过哪些服务、调了哪些库、最后到哪结束"。

Discovery-triggered diagrams:

| Discovery | Diagram | Deep Scan Requirement |
|---|---|---|
| durable module with business/runtime behavior | core module call chain | **mandatory** |
| module with async jobs, external APIs, callbacks, WebSocket, or retry/compensation | **sequence diagram** | **mandatory** |
| project-level business process | layered process flowchart | **mandatory** |
| queue / broker / consumer / subscriber | async flow | mandatory if present |
| cron / scheduler / worker / background job | job flow | mandatory if present |
| state field and transitions | state flow | mandatory if present |
| callback / webhook | integration flow | mandatory if present |
| auth/token/role/permission flow | auth flow | mandatory if present |
| object storage/upload/download/callback | file flow | mandatory if present |
| retry/rollback/DLQ/manual compensation | failure recovery flow | mandatory if present |
| persistent business entities / ORM / schema / migrations | data entity map | **mandatory** |
| which flows/APIs/jobs use which entities | **model usage flow map** | **mandatory** |
| complex core entity with many relationships or writers | single-entity relationship map | mandatory if entity is complex |
| entity lifecycle (who creates/reads/updates/deletes) | **entity lifecycle flow map** | mandatory if entity is complex |

When state/status fields are important to a core flow, also capture state-change trace evidence: trigger, writer, guard/condition, side effects, tests, and confidence. A legal state-flow diagram is not enough to answer "who changed this state?".

Diagram quality rules:

- every standalone or embedded diagram must answer one explicit question
- **Deep Scan 下，图要尽可能完整**，把能确认的路径都画出来，不能只画一个简略概览
- prefer layered color-coded flowcharts for onboarding summaries
- diagram nodes and edges should be traceable to an Evidence Chain entry in the same doc or target doc
- when a human question reveals an unclear path, propose a **complete diagram update** for the relevant scope, not a minimal patch
- if evidence is insufficient, mark the missing part `Unknown` or `Not enough evidence`; do not guess
- **所有图必须有 "How To Read" 说明**，缺少此说明的图视为不完整

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

If the update adds or changes diagrams for a targeted question, include:

| Question | Proposed Diagram | Target File | Key Evidence | Confidence | Human Decision |
|---|---|---|---|---|---|

## Completion Criteria

Deep Scan is complete only when:

- Onboarding DB Layout Mode is recorded, defaulting to Expanded unless the human explicitly requested Compact/Standard or the agent is preserving an existing Compact/Standard onboarding-db
- README has reading paths, module reading paths, **data-model reading path**, and **diagrams index**
- overview/setup/code map are usable for a newcomer
- module relationship map and boundary map exist or are explicitly blocked
- **every core module has at least one complete diagram** (flowchart); modules with async/external/callback/WebSocket interactions also have a sequence diagram; support-only modules may be marked with evidence
- at least one core flow exists or is explicitly unknown; **complex flows are split into multiple diagrams when one is insufficient**
- module index and module detail coverage are clear: each core module has either a dedicated `modules/<module>.md` or an explicit reason it remains index-only
- persistent data is documented in `domain/data-model.md` or Compact equivalent, with **complete entity relationship map** (not a minimal subset) and **model usage flow map**
- core docs include Evidence Chain entries for key module, flow, state, async/job, and verification claims
- **all diagrams have "How To Read" notes**
- commands and tests have evidence/confidence
- risks and unknowns are recorded
- project memory backfill proposal was shown
- human confirmed the write batch

If any item is missing, say:

```text
Onboarding DB draft is usable but incomplete.
```

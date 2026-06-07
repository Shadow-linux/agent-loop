# Onboarding DB Templates

Use this before creating or updating `.agent-loop/onboarding-db/` documents.

Templates define understanding dimensions, not mandatory one-to-one physical files. Layout Mode decides how many files carry those dimensions.

## Common Metadata

Every onboarding-db document must include these fields near the top:

```md
Document Language:
Last Verified:
Confidence:
Source Evidence:
Human Review Status:
```

Optional fields:

```md
Created:
Last Updated:
Freshness Window:
Verification Scope:
Maintainer:
Related Project Memory:
Related Diagrams:
```

Core review states:

```text
draft | reviewed | needs-review | stale
```

## Common Sections

Use this structure when it helps readability:

```md
## Purpose
## How To Read
## Key Facts
## Details
## Evidence
## Unknowns
## Update Rules
## Project Memory Backfill
```

Compact docs may combine `Evidence`, `Unknowns`, and `Project Memory Backfill` into short tables under each section.

## Human-Readable Format

Default shape:

```text
summary first -> tables -> diagrams -> evidence and unknowns
```

Use tables for comparisons, command lists, directories, modules, APIs, jobs, risks, and batch review. Use diagrams for cross-module, cross-process, stateful, or time-sequenced behavior.

## Layout Mapping

| Layout | Template Strategy |
|---|---|
| Compact | combine related dimensions into 5-7 files |
| Standard | make core topics independent and keep low-frequency topics combined |
| Expanded | split only complex modules, flows, deployment, security, observability, or decision history |

Anti-misuse rules:

- Compact means fewer physical files, not less understanding. Keep all required dimensions as visible sections, tables, diagrams, evidence, confidence, unknowns, and reading paths.
- Standard is not "generate every template." Create only files justified by project reality, human goal, and the Standard File Derivation table.
- Expanded is not "one file per directory." Split only durable business/runtime modules, bounded contexts, complex flows, deployment/operations concerns, or repeated maintenance paths.
- Human layout choice wins after risks are explained. If the agent recommends a different layout, ask before changing.
- Layout upgrades or file reshaping require Batch Human Review.

Compact suggested files:

| File | Carries |
|---|---|
| `README.md` | reading guide, document index, module reading paths |
| `overview.md` | project purpose, users, stack, capabilities |
| `setup-and-run.md` | local setup, run, ports, quick verification |
| `code-map.md` | directories, entrypoints, module summary |
| `architecture-and-integrations.md` | boundaries, APIs, integrations, async/events |
| `flows-and-data.md` | core flows, jobs, data model, states |
| `verification-and-risks.md` | tests, change impact, risks, unknowns, glossary summary |

Standard may split:

```text
environment.md
directory-map.md
module-map.md
architecture-boundaries.md
core-flows.md
entrypoints.md
data-model.md
api-surface.md
async-and-events.md
jobs-and-schedules.md
change-impact-map.md
testing-and-verification.md
integrations.md
risks-and-unknowns.md
glossary.md
```

Expanded may add:

```text
module-<name>.md (copy from templates/onboarding-db/module-template.md)
flow-<name>.md (copy from templates/onboarding-db/flow-template.md)
deployment-and-operations.md
decisions-and-history.md
security-and-permissions.md
observability.md
```

## Standard File Derivation

Standard layout does not require a direct template file for every topic. Use the Compact templates as source shapes, then split by this table.

| Standard File | Derive From | Required Content |
|---|---|---|
| `environment.md` | `setup-and-run.md` + `deployment-and-operations.md` | env files, variables, local/test/prod differences, containers, CI/runtime config, evidence and confidence |
| `directory-map.md` | `code-map.md` | main directories, generated/vendor/ignored areas, test directories, configs/scripts, read-first hints |
| `module-map.md` | `code-map.md` + `module-template.md` module fields | module summary/cards, boundaries, entrypoints, core call-chain references, key files, related diagrams |
| `architecture-boundaries.md` | `architecture-and-integrations.md` | UI/API/domain/DB/jobs/external boundaries, dependency direction, cross-boundary contracts, boundary risks |
| `core-flows.md` | `flows-and-data.md` + `flow-template.md` flow fields | flow index, core flow details, diagrams, state/data changes, verification hints |
| `entrypoints.md` | `code-map.md` | runtime, UI, API, config, worker/job, integration, and test entrypoints |
| `data-model.md` | `flows-and-data.md` | entities, tables/models, ownership, important state fields, migrations/seeds, evidence |
| `api-surface.md` | `architecture-and-integrations.md` | API groups, consumers, auth, generated clients, request/response contracts, breaking-change risks |
| `async-and-events.md` | `architecture-and-integrations.md` + `flow-template.md` async fields | producers, queues/topics, consumers, callbacks, retries, DLQ/compensation, diagrams |
| `jobs-and-schedules.md` | `flows-and-data.md` + `flow-template.md` job fields | schedules, workers, triggers, operational notes, failure/retry behavior |
| `change-impact-map.md` | `verification-and-risks.md` | change categories, affected modules/files/APIs/data/tests, risk level, verification path |
| `testing-and-verification.md` | `verification-and-risks.md` | test systems, fast/full commands, E2E/browser path when present, baseline failures, confidence |
| `integrations.md` | `architecture-and-integrations.md` | external services, SDKs, storage/queue/cache, webhooks, credentials/config references without secrets |
| `risks-and-unknowns.md` | `verification-and-risks.md` | high-risk unknowns, doc/code conflicts, unverified commands, missing diagrams, follow-ups |
| `glossary.md` | `verification-and-risks.md` glossary section | domain terms, Chinese meaning, English meaning, used-in context, synonyms/aliases including acronyms and naming conflicts, source evidence |

When deriving a Standard file, keep the common metadata block, summary-first shape, evidence, confidence, unknowns, and project memory backfill section.

## Expanded File Derivation

Expanded layout splits only areas that are complex enough to deserve their own reading path.

| Expanded File | Use / Derive From | Required Content |
|---|---|---|
| `module-<name>.md` | copy `templates/onboarding-db/module-template.md` | purpose, boundary, entrypoints, core call chain, core flows, key files, dependencies, tests, risks |
| `flow-<name>.md` | copy `templates/onboarding-db/flow-template.md` | purpose, diagram, steps, data/state changes, async/job/external behavior, verification, risks |
| `deployment-and-operations.md` | copy `templates/onboarding-db/deployment-and-operations.md` | environments, pipeline, runtime topology, release/rollback, migrations, health, observability |
| `decisions-and-history.md` | copy `templates/onboarding-db/decisions-and-history.md` | evidenced architectural/product decisions and current status |
| `security-and-permissions.md` | derive from `architecture-and-integrations.md` + module docs | auth boundaries, roles, policies, sensitive data, permission flows, evidence, unknowns |
| `observability.md` | derive from `deployment-and-operations.md` | logs, metrics, tracing, alerts, health checks, error reporting, dashboards if evidenced |
| `async-and-events.md` | derive from Standard table unless complex enough for a custom split | event topology, producers/consumers, retries, DLQ/compensation, flow diagrams |
| `jobs-and-schedules.md` | derive from Standard table unless complex enough for a custom split | schedules, workers, triggers, operations, failure modes |
| `environment.md` | derive from Standard table unless complex enough for a custom split | local/test/prod config, env files, containers, CI/runtime differences |

Do not create one Expanded file per directory. Split by durable module, bounded context, complex business flow, async system, deployment concern, or repeated maintenance need.

## README Requirements

`README.md` must include:

- document language and evidence
- project scope
- freshness status
- 10-minute reading path
- development reading path
- troubleshooting reading path
- async/jobs reading path when async, queues, callbacks, workers, or schedulers exist
- role-based reading paths when the project has distinct frontend, backend, operations, QA, or product readers
- module reading paths
- document index
- diagrams index
- needs-review / stale / unknown items

Module reading path table:

| Module | Read First | Then Read | Core Call Chain | Useful For |
|---|---|---|---|---|

If the README lacks module reading paths, onboarding-db is not complete.

If async/jobs exist and README lacks an async/jobs reading path, onboarding-db is usable but incomplete.

## Module Card

Core fields:

```md
## Module: <name>

Purpose:
Boundary:
Entrypoints:
Core Call Chain:
Core Flows:
Key Files:
Related Diagram:
Evidence:
Confidence:
```

Optional fields:

```md
Depends On:
Called By:
Key Data:
Configuration:
Tests:
Risks:
```

Expanded-only fields:

```md
Operational Notes:
Runtime Ownership:
Deployment Unit:
Observed Failure Modes:
Related Decisions:
```

Do not invent fields. Use `Not found`, `Not applicable`, or `Unknown` when needed.

## Deployment Template

Use `deployment-and-operations.md` when deployment is complex enough to stand alone.

Required sections:

```md
# Deployment And Operations

Document Language:
Last Verified:
Confidence:
Source Evidence:
Human Review Status:

## Deployment Overview
## Environments
## Deployment Pipeline
## Runtime Topology
## Release / Rollback
## Migrations / Seeds
## Health Checks
## Logs / Metrics / Tracing
## Operational Access
## Related Diagrams
## Evidence
## Unknowns
```

Tables:

| Environment | Runtime | Deploy Trigger | Config Source | URL / Entry | Owner | Evidence | Confidence |
|---|---|---|---|---|---|---|---|

| Step | Command / System | Working Directory | Preconditions | Rollback | Evidence | Confidence |
|---|---|---|---|---|---|---|

Never write real secrets or production connection strings.

## Decisions And History

Use this for why the project is shaped this way.

| Layout | Placement |
|---|---|
| Compact | section in `architecture-and-integrations.md` |
| Standard | `decisions-and-history.md` |
| Expanded | optional split into `design-decisions.md`, `architecture-history.md`, `technical-debt.md` |

Decision fields:

| Field | Meaning |
|---|---|
| Decision | what was decided |
| Context | constraints and situation |
| Alternatives | known alternatives |
| Why This Choice | reason, only if evidenced |
| Consequences | benefits and costs |
| Current Status | active / superseded / unknown |
| Evidence | docs, commit, issue, PR, code, or human confirmation |
| Confidence | high / medium / low |

Code can prove what exists now; it usually cannot prove why it was chosen. Ask the human when reason is unclear.

## Diagram Template

Use one generic template and set `Diagram Type`.

```md
# Diagram: <name>

Document Language:
Last Verified:
Diagram Type:
Question Answered:
Scope:
Source Evidence:
Confidence:
Human Review Status:

## Diagram

## How To Read

## Notes

## Unknowns
```

Allowed diagram types include:

```text
module-relationship
core-module-call-chain
boundary
core-flow
async-flow
job-flow
state-flow
api-call-flow
integration-flow
auth-flow
file-flow
failure-recovery
data-entity-map
deployment-map
change-impact-map
```

Each diagram answers one question. Do not draw a whole repository.

## Batch Review Template

```md
# Batch Human Review: <stage-or-topic>

| File / Item | Action | Change Summary | Source Evidence | Confidence | Affects Long-Term Memory | Suggested Action |
|---|---|---|---|---|---|---|
```

For onboarding-db batches:

| Batch | Typical Files |
|---|---|
| Project Basics | README, overview, setup/environment, code map |
| Architecture | modules, boundaries, APIs, integrations, async/jobs |
| Flows And Data | core flows, data model, state diagrams, flow diagrams |
| Verification And Risks | testing, change impact, risks, unknowns, glossary |
| Memory Backfill | `project.md` and `project/*.md` proposals |

## Minimum Completion Standard

Onboarding-db is complete only when:

- README has reading paths, module reading paths, document index, and diagrams index
- overview explains purpose, users, stack, and capabilities
- setup/run path is usable or blocked with evidence
- code map tells where to start reading
- modules and boundaries are mapped
- diagrams include module map, boundary map, one core module call chain per core module, and at least one core flow or an explicit blocker
- async/jobs/deployment/data are documented or marked not applicable/unknown
- tests and verification commands have confidence labels
- risks and unknowns are recorded
- important facts include evidence and confidence
- human review status is recorded

If not, call it usable but incomplete.

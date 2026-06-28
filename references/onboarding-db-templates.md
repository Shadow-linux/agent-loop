# Onboarding DB Templates

Use this before creating or updating `.agent-loop/onboarding-db/` documents.

The onboarding-db template directory intentionally contains only five templates:

```text
templates/onboarding-db/onboarding-spec.md
templates/onboarding-db/onboarding-plan.md
templates/onboarding-db/star-deep-dive.md
templates/onboarding-db/coverage-matrix.md
templates/onboarding-db/batch-review.md
```

Deleted legacy form templates: module, flow, entity, diagram, evidence-graph, directory-map, boundary-map, setup, deployment, data-model, and similar one-file-per-topic templates. Those templates caused directory-first file spray and thin 20-line docs. Do not recreate them under new names.

## Core Principle

Onboarding DB is delivered like a feature: spec first, plan second, batch implementation third, review before completion.

The templates are writing contracts, not fill-in-the-blank forms. They should make agents write fewer, deeper, human-readable docs like `stars/recharge-flow.md`, not many shallow module/flow files.

## Template Roles

| Template | Required When | Purpose |
|---|---|---|
| `onboarding-spec.md` | before Deep detail docs | define target readers, required-core topics, non-goals, quality bar |
| `onboarding-plan.md` | before writing star docs | batch plan, file budget, split gate, review checkpoints |
| `star-deep-dive.md` | for required-core topics | write one canonical deep article for a core flow/domain/module |
| `coverage-matrix.md` | after spec and every batch | track learning outcomes and status; not file existence |
| `batch-review.md` | before accepting each batch | human review of quality, evidence, coverage, and requested revisions |

## File Budget

Default Deep file budget before human expansion is 5 star docs or fewer, plus README/maps/coverage updates. Exceeding that budget requires human confirmation.

Each proposed new file must pass the Split Gate:

| Proposed File | Why New File? | Why Not Merge? | Required-Core? | Human Value |
|---|---|---|---|---|

If the answer is weak, merge the content into README, maps, coverage, or an existing star doc.

## Star Doc Quality Bar

A required-core topic is not `newcomer-ready` until an accepted star doc explains:

- business meaning and actors
- phase-by-phase flow
- API / command / callback / job entrypoints
- code evidence and symbols
- data models, tables, Redis keys, Kafka topics, configs, or external systems
- state changes and fact sources
- success paths, branches, failure paths
- retry, idempotency, compensation, fallback, and operational risks
- verification, logs, metrics, runbook checks
- concrete examples
- key file index and reading order

## Newcomer Handoff Quality Gate

Do not mark Deep onboarding complete only because index files, many files, or attractive diagrams exist.

Required Deep onboarding packs:

- Onboarding Spec accepted.
- Onboarding Plan accepted.
- Required-core star docs accepted.
- Coverage Matrix shows no required-core topic stuck at `discovered`, `planned`, `needs-deep-trace`, `draft-star`, or `blocked-by-unknown`.
- README/maps point to canonical star docs without duplicating thin summaries.
- Service Startup / Config Matrix information exists in a star doc, README/runtime section, or coverage row when it matters.
- Core Domain Handoff Pack is represented by accepted star docs and coverage rows, not by shallow module files.

If many small files exist but these packs are thin or missing, the onboarding-db is usable but incomplete.

## Anti-Patterns

Do not:

- create one file per directory
- create module/flow files because a template exists
- create alias files that duplicate a canonical star doc
- mark coverage `done` because a file exists
- use diagrams as a substitute for phase-by-phase explanation
- split before writing and accepting `onboarding-spec.md` and `onboarding-plan.md`

## Migration From Legacy Onboarding DB

When an existing onboarding-db has many thin files:

1. Do not delete target-project files silently.
2. Audit coverage status and lower overclaimed `done/newcomer-ready` rows to `needs-deep-trace`.
3. Write `onboarding-spec.md` describing the required-core topics.
4. Write `onboarding-plan.md` with a small file budget.
5. Convert the best existing detailed docs into `stars/<topic>.md`.
6. Treat old `modules/*`, `flows/*`, and `diagrams/*` as draft evidence or indexes until a human approves consolidation.

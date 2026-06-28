# Onboarding DB Templates

Use this before creating or updating `.agent-loop/onboarding-db/` documents.

The onboarding-db template directory intentionally contains only five templates:

```text
templates/onboarding-db/onboarding-spec.md
templates/onboarding-db/onboarding-plan.md
templates/onboarding-db/deep-dive.md
templates/onboarding-db/coverage-matrix.md
templates/onboarding-db/batch-review.md
```

Deleted legacy form templates: module, flow, entity, diagram, evidence-graph, directory-map, boundary-map, setup, deployment, data-model, and similar one-file-per-topic templates. Those templates caused directory-first file spray and thin 20-line docs. Do not recreate them under new names.

## Core Principle

Onboarding DB is delivered like a feature: spec first, plan second, batch implementation third, review before completion.

The templates are writing contracts, not fill-in-the-blank forms. They should make agents write evidence-backed, human-readable deep dives under `deep-dives/<topic>.md`, not many shallow module/flow files.

Human-provided examples define expected detail depth and explanation quality only. Do not copy example topic names, topic count, domain vocabulary, or project-specific structure unless current project evidence supports them.

## Template Roles

| Template | Required When | Purpose |
|---|---|---|
| `onboarding-spec.md` | before Deep detail docs | define target readers, required-core onboarding topics, non-goals, quality bar |
| `onboarding-plan.md` | before writing deep-dive docs | batch plan, review cadence, split gate, review checkpoints |
| `deep-dive.md` | for required-core onboarding topics | write one canonical deep article for a core flow/domain/module |
| `coverage-matrix.md` | after spec and every batch | track learning outcomes and status; not file existence |
| `batch-review.md` | before accepting each batch | human review of quality, evidence, coverage, and requested revisions |

## Batch Cadence And Split Gate

Deep Onboarding has no total document count cap. Write as many deep-dive docs as current project evidence and newcomer handoff needs require.

Default batch size is 1-3 deep-dive docs, unless the human chooses another review cadence. Batch size is review pacing, not a total limit.

Each proposed new file must pass the Split Gate:

| Proposed File | Why New File? | Why Not Merge? | Required-Core? | Human Value |
|---|---|---|---|---|

If the answer is weak, merge the content into README, maps, coverage, or an existing deep-dive doc.

## Deep-Dive Quality Bar

A required-core onboarding topic is not `newcomer-ready` until an accepted deep-dive doc explains:

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
- Required-core deep-dive docs accepted.
- Coverage Matrix shows no required-core topic stuck at `discovered`, `planned`, `needs-deep-trace`, `draft-deep-dive`, or `blocked-by-unknown`.
- README/maps point to canonical deep-dive docs without duplicating thin summaries.
- Service Startup / Config Matrix information exists in a deep-dive doc, README/runtime section, or coverage row when it matters.
- Core Domain Handoff Pack is represented by accepted deep-dive docs and coverage rows, not by shallow module files.

If many small files exist but these packs are thin or missing, the onboarding-db is usable but incomplete.

## Anti-Patterns

Do not:

- create one file per directory
- create module/flow files because a template exists
- create alias files that duplicate a canonical deep-dive doc
- mark coverage `done` because a file exists
- use diagrams as a substitute for phase-by-phase explanation
- split before writing and accepting `onboarding-spec.md` and `onboarding-plan.md`

## Migration From Legacy Onboarding DB

When an existing onboarding-db has many thin files:

1. Do not delete target-project files silently.
2. Audit coverage status and lower overclaimed `done/newcomer-ready` rows to `needs-deep-trace`.
3. Write `onboarding-spec.md` describing the required-core topics.
4. Write `onboarding-plan.md` with batch cadence and split rationale.
5. Convert the best existing detailed docs into `deep-dives/<topic>.md`.
6. Treat old `modules/*`, `flows/*`, and `diagrams/*` as draft evidence or indexes until a human approves consolidation.

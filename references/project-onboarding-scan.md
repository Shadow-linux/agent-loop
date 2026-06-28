# Project Onboarding Scan

Use this when the human asks to create durable onboarding documentation, be guided through an existing project, or preserve focused understanding of one module, flow, async task, deployment path, state transition, or problem area.

This reference does not replace `existing-project-onboarding.md`. That file is the entry/router and safe-entry scan. This file defines the single durable onboarding flow: Deep Onboarding.

## Core Principle

Onboarding DB is delivered like a feature: spec first, plan second, batch implementation third, review before completion.

The agent must not treat onboarding as "generate a directory of docs." A useful onboarding-db is a coherent set of accepted, evidence-backed learning artifacts.

```text
code reality
-> onboarding-spec.md
-> onboarding-plan.md
-> batch deep-dive docs
-> batch review
-> coverage update
-> README/maps index
-> project memory backfill proposal
```

Do not create directory-first module/flow/detail files during Deep onboarding before `onboarding-spec.md` and `onboarding-plan.md` are accepted.

When onboarding discovers stable project facts missing from project memory, propose or perform project memory backfill after human confirmation.

Deep Onboarding has no total document count cap. Write as many deep-dive docs as current project evidence and newcomer handoff needs require.

Human-provided examples define expected detail depth and explanation quality only. Do not copy example topic names, topic count, domain vocabulary, or project-specific structure unless current project evidence supports them.

## Single Mode

There is only one durable project-understanding onboarding mode: Deep Onboarding.

Do not offer Quick / Deep / Targeted onboarding modes.

If the human only wants safe continuation, update or propose project memory and root guidance through `existing-project-onboarding.md`; do not create onboarding-db detail docs.

Focused requests use a narrow Deep Onboarding scope, not a separate Targeted mode.

Ask before writing onboarding-db files. Deep does not start detail docs until spec and plan are accepted.

## Deep Onboarding

Deep onboarding has four gates.

### Gate 1: Onboarding Spec

Create or refresh `onboarding-spec.md` first.

The spec must define:

- target readers
- onboarding goal
- required-core onboarding topic inventory
- supporting-summary topics
- non-goals
- quality bar
- human decisions needed

Required-core signals include money, balance, billing, auth/API key, quota, main request flow, provider call, state writeback, async finality, external callbacks, retries, idempotency, production config, and repeated human questions.

### Gate 2: Onboarding Plan

Create or refresh `onboarding-plan.md` before writing deep-dive docs.

The plan must define:

- batch review cadence
- split gate
- batch plan
- deep-dive doc queue
- index/map updates
- stop conditions
- review checkpoints

Default batch size is 1-3 deep-dive docs, unless the human chooses another review cadence.

Batch size is review pacing, not a total limit.

Every proposed new file must pass:

| Proposed File | Why New File? | Why Not Merge? | Required-Core? | Human Value |
|---|---|---|---|---|

If the agent cannot justify the split, merge into README, maps, coverage, or an existing deep-dive doc.

### Gate 3: Deep-Dive Batch Implementation

Write deep-dive docs for all required-core onboarding topics justified by project evidence and newcomer handoff needs.

Default canonical path:

```text
.agent-loop/onboarding-db/deep-dives/<topic>.md
```

A deep-dive doc should read like a deep technical article, not a form. Use `templates/onboarding-db/deep-dive.md` as a quality contract.

Required deep-dive doc content:

- business meaning and actors
- for module/domain topics: purpose, boundary, entrypoints, config/dependencies, core call chain, data touched, APIs/protos, tests, risks, and Evidence Chain
- for flow topics: trigger, entrypoint, step-by-step call chain with file/symbol evidence, data writes, async/failure/retry behavior, verification, risks, and Evidence Chain
- for data-model topics: entities, key fields, storage mapping, owners, writers/readers, lifecycle/state, related flows, tests, evidence, and confidence
- phase-by-phase flow
- API / command / callback / job entrypoints
- code evidence and symbols
- data models, tables, Redis keys, Kafka topics, config, external systems
- state changes and fact sources
- success path, branches, and failure path
- retry, idempotency, compensation, fallback, operational risks
- verification, logs, metrics, runbook checks
- concrete examples
- key file index and reading order

### Gate 4: Batch Review And Coverage

After each batch:

1. Fill `batch-review.md` or an equivalent review section.
2. Update `coverage-matrix.md`.
3. Update README/maps as indexes only.
4. Ask for human review before marking a topic `newcomer-ready`.

Coverage tracks learning outcomes, not file existence. A required-core topic is not `newcomer-ready` until its deep-dive doc is accepted.

## Focused Scope

Focused onboarding writes or updates the smallest useful artifact for a specific human question while still following Deep Onboarding gates.

For a focused question, `onboarding-spec.md` and `onboarding-plan.md` may be narrow:

- one target scope
- one accepted deep-dive doc or existing deep-dive doc update
- one coverage update
- optional README/maps link update
- optional project memory backfill proposal when stable facts changed

Focused onboarding does not produce a full `project.md` proposal by default. It may propose narrow project memory backfill only when the focused scope exposes stale or missing facts required for safe continuation.

Completion wording:

```text
Focused Deep Onboarding complete for <scope>.
Global Deep Onboarding remains incomplete unless global gates pass.
```

## Index And Map Rules

README and maps are indexes, not detail docs.

Allowed index content:

- reading paths
- topic lists
- canonical deep-dive links
- status and confidence
- short one-line summaries

Not allowed:

- duplicate thin versions of deep-dive docs
- one file per module just to look complete
- alias files that count as coverage
- diagram-only docs with no explanation

## Completion Criteria

## Deep Onboarding Quality Gate

Deep onboarding is complete only when a newcomer can answer the primary business flow, core domain, core domain data flow, data model, service startup/config, verification strategy, and change-risk map.

A large onboarding-db with many thin files is usable but incomplete when core modules, flows, data, startup, or verification docs lack evidence-backed detail.

Treat Deep Scan as a newcomer handoff package, not a directory tree. File count, index count, diagram count, and closed-looking coverage rows are not enough.

### Core Domain Handoff Pack

Required core understanding may live in one or more accepted deep-dive docs. The pack must teach business purpose, users/actors, core capabilities, core constraints, core modules, primary flows, data ownership, and Evidence Chain.

### Service Startup / Config Matrix

Startup/config information can live in a deep-dive doc, README/runtime section, or coverage row when it matters. It must identify service/process, command, config path, required dependencies, port/protocol, health/failure signal, evidence, confidence, and unknowns.

### Newcomer Readiness Check

Before completion, ask whether the onboarding-db lets a newcomer:

- run or reason about each required service/process
- trace the primary business flow from external entrypoint to domain logic to storage/external systems
- identify the owning module for a change
- understand core entities and state transitions
- find tests or substitute verification for core behavior
- see operational risks, retry/failure paths, and change-impact risks

If any answer is no, say:

```text
Onboarding DB draft is usable but incomplete.
```

Deep onboarding is complete only when:

- onboarding spec is accepted
- onboarding plan is accepted
- required-core deep-dive docs are accepted
- coverage has no required-core topic in `discovered`, `planned`, `needs-deep-trace`, `draft-deep-dive`, or `blocked-by-unknown`
- README/maps point to canonical deep-dive docs without duplicating thin docs
- project memory backfill proposal was shown when stable long-term facts changed
- human confirmed the final review

## Thin File Failure Rule

If the onboarding-db contains many 20-70 line module/flow/diagram files and no deep-dive docs with phase-by-phase code/data/failure/verification detail, call it incomplete.

Do not fix this by creating more files. Fix it by:

1. lowering overclaimed coverage statuses
2. writing or refreshing `onboarding-spec.md`
3. writing or refreshing `onboarding-plan.md`
4. converting required-core onboarding topics into `deep-dives/<topic>.md`
5. reviewing each batch

## Batch Human Review

Before writing a batch, present:

| File / Item | Action | Why This File Exists | Source Evidence | Confidence | Coverage Impact | Human Decision |
|---|---|---|---|---|---|---|

Allowed choices:

```text
approve batch
approve selected
revise selected
defer selected
reject batch
```

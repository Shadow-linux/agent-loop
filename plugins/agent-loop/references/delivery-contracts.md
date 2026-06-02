# Delivery Contracts

Use Delivery Contracts when feature work crosses a durable producer-consumer boundary. A contract lets a downstream developer, agent, frontend, service, worker, library user, or deployment operator continue without reverse-engineering upstream code.

## Core Rule

```text
handoffs/* = temporary subagent assignment and return notes
contracts.md + contracts/* = durable producer-consumer delivery boundary
```

A Delivery Contract is not a task log and not a replacement for implementation code. It records the stable interface that another boundary relies on.

## Trigger Conditions

During Work Breakdown, Technical Design / Code Context, Plan, Review, or Drift Check, recommend a Delivery Contract when work creates or changes:

- an API consumed by frontend, mobile, CLI, or another service
- a service-to-service endpoint
- an event, message, webhook, callback, or async workflow
- a data exchange format or public schema
- a library or plugin public API
- a UI behavior contract handed from product/design/backend to frontend
- a runtime, deployment, environment-variable, or integration boundary

The agent should detect the need proactively. The human does not need to know a command.

## Location

Use stable feature-level entry files:

```text
agent-loop/features/<feature>/
  contracts.md
  contracts/
    API001-<slug>.md
    EVENT001-<slug>.md
    DATA001-<slug>.md
    UI001-<slug>.md
    LIB001-<slug>.md
    RUNTIME001-<slug>.md
```

For a small feature with one compact boundary, `contracts.md` may hold the complete contract. Create `contracts/` detail files when there are multiple contracts, multiple consumers, full schemas/examples, error cases, version history, or compatibility decisions.

## Contract Types

```text
API
Service
Event
Async Workflow
Data
UI Behavior
Library
Runtime
```

## Contract Status

```text
draft -> accepted -> implemented -> verified -> superseded
```

- `draft`: agent or human proposed the boundary.
- `accepted`: human approved the consumer-facing shape.
- `implemented`: producer code exists.
- `verified`: producer verification evidence exists and the contract matches reality.
- `superseded`: a newer contract replaces it; keep history and replacement link.

## Human Gates

- In Strict Mode, ask before creating or changing contract files.
- In Feature Auto-Loop, the agent may create or update a `draft` contract without pausing.
- Moving a contract from `draft` to `accepted` always requires human confirmation.
- A breaking change to an `accepted`, `implemented`, or `verified` contract always requires affected-consumer analysis first, then a separate human confirmation.
- The human saying "just change it" before seeing affected consumers is not enough. Present the impact table, compatibility options, migration risk, and then ask again.
- Do not change producer code, tests, or contract files for a breaking change until that post-impact confirmation is received.
- Creating a new `draft` or superseding contract cannot bypass the breaking-change gate when existing consumers would observe changed behavior.
- Auto modes never silently accept a contract or approve a breaking change.

Minimum affected-consumer scan:

- named consumers in the contract
- code search for endpoint, event, schema, exported symbol, field name, or UI state
- existing tests, mocks, fixtures, generated clients, SDKs, OpenAPI/GraphQL/proto/schema files when present
- project docs or `project.md` boundary/capability notes

If the consumer set cannot be determined, mark confidence as low and ask the human before changing behavior.

## Minimum Contract Content

Every Delivery Contract must state:

- contract ID, type, status, producer, and named consumers
- related feature, stories, tasks, and source requirements
- purpose and business behavior
- interface shape: endpoint, method, signature, event, schema, UI state, or runtime expectation
- parameters, request/input, response/output, errors, and side effects where applicable
- auth, permissions, tenant, and data-boundary rules where applicable
- compatibility and breaking-change notes
- version or compatibility window when consumers may already rely on the contract
- deprecation or rollout order when old and new behavior must coexist
- producer verification commands or evidence
- downstream consumer notes
- change history

## Workflow

```text
detect boundary
-> draft contract
-> human accepts consumer-facing shape
-> producer implements with TDD
-> producer verifies and records evidence
-> downstream consumer develops against accepted/verified contract
-> E2E or integration verification
-> drift check keeps code, tests, and contract aligned
```

## Review And Drift

During Review and Drift Check:

1. Compare contract text with producer code and tests.
2. Check whether named consumers are still accurate.
3. Check compatibility and identify breaking changes.
4. Update `contracts.md` index status and evidence links.
5. Update detail file when interface behavior changed.
6. Record drift and human decisions in `notes.md`.

If code reality and an accepted contract disagree, stop downstream assumptions, present the mismatch, and ask whether to backfill the contract, change code, or create a superseding contract.

For breaking changes, prefer one of these explicit compatibility decisions:

- non-breaking additive change
- temporary dual-shape compatibility
- versioned replacement
- immediate breaking change with named consumers and migration owner
- reject change and keep current contract

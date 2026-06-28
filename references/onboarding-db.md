# Onboarding DB

Use this when reading, writing, refreshing, or correcting `.agent-loop/onboarding-db/`.

`onboarding-db/` is a human-readable project understanding database. It helps newcomers and agents understand a project, but it is not the daily execution state.

## Relationship To Other Artifacts

| Artifact | Reader | Purpose |
|---|---|---|
| `project.md` | agent | current state, next action, active feature, memory index |
| `project/*.md` | agent | enterprise-mode long-term fact details |
| `onboarding-db/` | human + agent | project understanding, reading paths, module/flow/boundary explanations |
| `features/<feature>/` | agent + human review | feature spec, tasks, tests, plans, notes |
| code reality | agent + human | current implemented truth |

Rules:

- Code reality is the current fact base.
- Human source requirements are original intent and are never overwritten.
- `onboarding-db/` can explain a project, but cannot overrule code reality.
- `project.md` indexes or summarizes stable facts; it should not become a long project manual.
- A `project.md` or root guidance reference to onboarding-db is only a claim until the target files exist and pass freshness/review checks.

## When To Read

Read onboarding-db when:

- a human says "onboard me", "help me understand this project", "where do I start", or similar
- a new agent enters a large or unfamiliar project
- project memory is too thin to answer a project-understanding question
- feature planning needs boundary, flow, module, deployment, or change-impact context
- onboarding-db may be stale and a human wants to rely on it
- the human explicitly points to onboarding-db

Do not read onboarding-db by default for tiny task execution when `project.md`, feature docs, and code context are sufficient.

## Problem Routing

| Question | Read First |
|---|---|
| What is the active feature or next action? | `project.md` |
| What is the onboarding scope and plan? | `onboarding-spec.md`, then `onboarding-plan.md` and `coverage-matrix.md` |
| What does this project do? | `README.md`, `onboarding-spec.md`, accepted overview deep-dive doc, or legacy `overview.md` as evidence |
| How do I run it? | accepted startup/runtime deep-dive doc, README runtime section, or legacy `runtime/setup-and-run.md` as evidence |
| Which areas are required-core or still incomplete? | `coverage-matrix.md`, then the linked canonical deep-dive docs |
| Where do I start reading code? | README reading path, `coverage-matrix.md`, accepted deep-dive docs, or legacy maps as evidence |
| What does this module do? | accepted `deep-dives/<topic>.md` for the module/domain, or legacy module/map docs as evidence |
| What are the system boundaries? | accepted boundary/integration deep-dive doc, README/maps index, or legacy boundary map as evidence |
| How does this business flow work? | `deep-dives/<topic>.md` for required-core flows; older `flows/<flow>.md` is draft evidence unless accepted |
| What entities, fields, and relationships does this project use? | accepted data-model/domain deep-dive doc, or legacy domain docs as evidence |
| Who writes or reads this entity? | `domain/data-model.md`, `domain/entities/<entity>.md`, related flows/modules, then focused code reality if needed |
| How do async/events/jobs work? | accepted async/job deep-dive doc, or legacy runtime docs as evidence |
| How do I understand async queues, consumers, callbacks, or background jobs? | README async reading path, `runtime/async-and-events.md`, `runtime/jobs-and-schedules.md`, async/job diagrams |
| I followed setup docs and it does not work | accepted startup/runtime deep-dive doc or legacy runtime docs, then `onboarding-diagnostics.md` Startup Failure Diagnosis |
| How is it deployed? | accepted deployment/operations deep-dive doc, README runtime section, or legacy deployment docs as evidence |
| What changes if I modify this area? | accepted change-risk deep-dive doc or legacy impact docs, then `onboarding-diagnostics.md` Change Impact Analysis |
| Who or what changes this state/status? | accepted flow/data/state deep-dive doc or legacy flow/domain docs, then `onboarding-diagnostics.md` State Change Trace |
| Why was this designed this way? | accepted decision/history deep-dive doc or legacy decision docs, then `onboarding-diagnostics.md` Design Decision Routing |
| Docs conflict with code | `coverage-matrix.md`, `batch-review.md`, legacy risks docs, then code reality |

If `project.md` is insufficient, read onboarding-db. If onboarding-db is insufficient or stale, inspect code reality and propose an onboarding-db update.

## Integrity Check

Run this before relying on onboarding-db when `project.md`, root guidance, or a feature artifact claims onboarding-db exists, is expanded, is reviewed, or is the newcomer entrypoint.

Minimum checks:

Integrity Check proves the onboarding-db is safe to read for the current goal; it does not prove Deep onboarding is complete. Deep completion must pass the Newcomer Handoff Quality Gate in `project-onboarding-scan.md` and `onboarding-db-templates.md`.

| Check | Failure Means |
|---|---|
| `.agent-loop/onboarding-db/` exists | onboarding-db is missing |
| `.agent-loop/onboarding-db/README.md` exists | newcomer entrypoint is missing |
| README links or project.md indexed docs exist, or are explicitly marked planned/deferred | index drift |
| status is not claimed `reviewed` without human-approved content | review-state drift |
| key docs are fresh enough for the human goal, or stale status is disclosed | freshness drift |

If any check fails:

1. Classify as `stale-memory` or onboarding memory drift.
2. Do not guide the human to the missing onboarding-db path.
3. Use available project memory, root guidance, existing docs, and code reality for a temporary answer.
4. Present the mismatch and recommended backfill targets.
5. Ask before changing `project.md`, root guidance, or creating/updating onboarding-db.

Suggested mismatch report:

| Claimed Artifact | Actual State | Evidence | Risk | Recommended Action | Human Decision |
|---|---|---|---|---|---|
| `.agent-loop/onboarding-db/README.md` | missing | `project.md` points to it; path not found | newcomer guide fails | create onboarding-db or correct project memory | approve / defer / revise |

## Guided Newcomer Onboarding

Use this when onboarding-db already exists and the human says they are new to the project, asks "where should I start", asks to be guided through project takeover, or asks the agent to explain the project step by step.

The agent owns the reading sequence. Do not dump the full document list and wait for the human to navigate.

Recommended flow:

```text
integrity check -> freshness check -> spec/plan/coverage status -> 10-minute orientation -> reading path -> human question -> targeted explanation -> optional targeted scan/update proposal
```

Steps:

1. Check onboarding-db existence, README, indexed paths, freshness, and review status. If it is missing, stale, unreviewed, or contradictory, say so before relying on it.
2. Check whether `onboarding-spec.md`, `onboarding-plan.md`, and `coverage-matrix.md` exist; if not, say the onboarding-db predates spec-first onboarding and propose a spec/plan refresh before trusting completion claims.
3. Give a short orientation: project purpose, runtime shape, main modules, main flows, required-core deep-dive docs, current completion status, and how to run/verify.
4. Recommend exactly one first reading path from `onboarding-db/README.md`.
5. Ask the human what they want to understand next, with 2-4 concrete options such as required-core flow, module, async/jobs, deployment, tests, state trace, design decisions, or change impact.
6. When answering, read the matching onboarding-db path first, then inspect code reality only if the docs are missing, stale, contradictory, or too thin.
7. If the answer reveals a stable missing fact, propose an onboarding-db update through Batch Human Review.
8. After every onboarding answer, recommend exactly one next action: read a specific doc, inspect a specific flow/module, generate/update a focused diagram, run a setup/verification command, or return to the normal feature-development loop.
9. If the human is trying to start development, route back to the normal agent-loop stage after the explanation.

Newcomer summary format:

| Area | What To Know First | Where To Read | Confidence | Unknowns |
|---|---|---|---|---|

Onboarding next-action format:

| Current Understanding | Recommended Next Step | Why | Artifact / Doc | Human Gate |
|---|---|---|---|---|

If the current docs are too text-heavy or the human is asking about relationships, state transitions, async behavior, or flow order, the recommended next step should usually be a focused diagram proposal.

Do not mark onboarding complete just because the DB exists. The human takeover is complete only when the human has a next reading path or next development action.

## On-Demand Explanation And Diagram Updates

Use this when the human does not understand a call path, flow, async/job behavior, integration, deployment route, state transition, or boundary relationship.

Behavior:

1. Route to focused Deep Onboarding scope for the smallest relevant question.
2. Read the current onboarding-db path and source evidence.
3. Inspect code reality only for the selected module/flow/problem area.
4. Answer with a small explanation and, when useful, a focused diagram.
5. Propose updating or adding the smallest useful diagram/doc only after explaining what changed and why.
6. Use Batch Human Review before writing `.agent-loop/onboarding-db/` updates.

Suggested diagram update table:

| Question | Proposed Diagram | Target File | Source Evidence | Confidence | Human Decision |
|---|---|---|---|---|---|

Do not create a full repository graph to answer a focused question. Add or update the smallest diagram that makes the unclear path understandable.

If the proposal changes a call path, state writer, async route, or deployment path, include key evidence:

| Node / Edge | File Path | Symbol / Object | Parameters / Fields | Description | Confidence |
|---|---|---|---|---|---|

For setup failures, state-change questions, design-decision questions, or change-impact questions, load `onboarding-diagnostics.md` and use the focused procedure there before proposing documentation updates.

## Write Rules

All onboarding-db writes require human confirmation.

The agent may draft high-confidence content, but must not mark it `reviewed` until human confirmation.

Before writing, show Batch Human Review:

| File / Item | Action | Change Summary | Source Evidence | Confidence | Affects Long-Term Memory | Suggested Action |
|---|---|---|---|---|---|---|

After writing, report:

```text
Updated files
Evidence used
Remaining unknowns
Suggested next read
Project memory backfill status
```

Critical onboarding-db writes should prefer the spec-first deep-dive shape:

- `onboarding-spec.md`
- `onboarding-plan.md`
- `coverage-matrix.md`
- `deep-dives/<topic>.md`
- `batch-review.md`

Legacy categorized docs such as `modules/`, `flows/`, `runtime/`, `domain/`, and `quality/` may remain as evidence or be read when an existing onboarding-db already contains them. Do not generate new directory-first docs unless a human explicitly asks for compatibility with an existing legacy layout.

## Batch Choices

Allowed human choices:

```text
approve all
approve selected
revise selected
defer selected
skip this batch
```

If the human approves selected rows only, write only those rows or files and keep the rest as draft/deferred/unknown.

## Freshness

Default freshness window:

```text
Freshness Window: 7 days
```

Older than 7 days means "needs freshness check", not "invalid".

Run a freshness check when:

- a newcomer wants to rely on onboarding-db
- a new agent enters a large project
- project structure, commands, tests, deployment, or core flows changed
- feature close changed long-term architecture, commands, flows, integrations, deployment, or test strategy
- the human asks whether onboarding docs are current

Freshness check should lightly compare:

- README/docs/guidance changes
- command/test/build changes
- entrypoint and major directory changes
- core module/boundary changes
- async/job/deployment changes
- known risks and unknowns

Do not silently rewrite onboarding-db during freshness check. Present a Batch Human Review first.

## Learning Rule

When answering a project question, the agent may discover new long-term knowledge.

| Discovery | Behavior |
|---|---|
| one-off answer | answer without writing docs |
| stable project fact | suggest onboarding-db update |
| new business flow | suggest flow doc and diagram update |
| new async/job/deployment fact | suggest relevant topic doc update |
| doc/code conflict | record correction proposal and confidence |
| human says "record this" | enter Batch Human Review |

Auto-learning can draft, but still needs human confirmation before reviewed writes.

## Project Memory Backfill

Onboarding-db facts may need project memory summaries.

| Onboarding Fact | Possible Project Memory |
|---|---|
| core capability | `project/capabilities.md` |
| command/test strategy | `project/commands.md`, `project/testing.md` |
| architecture boundary | `project/boundaries.md`, `project/architecture.md` |
| domain language | `project/domain-language.md` |
| product context | `project/product-context.md` |
| environment/deployment fact | `project/environments.md` |

Backfill requires human confirmation and uses Batch Human Review when multiple facts are involved.

## Status Labels

Use these review states:

| Status | Meaning |
|---|---|
| `draft` | generated or updated by agent, not yet human reviewed |
| `reviewed` | human approved this content |
| `needs-review` | content exists but human attention is needed |
| `stale` | freshness check found likely outdated content |

## Safety

Never write:

- real secrets, tokens, passwords, production connection strings
- unsupported certainty
- whole-repo file trees
- full function call graphs
- feature execution logs
- current task status
- unconfirmed business decisions

Feature execution logs belong in feature `notes.md`; active state belongs in `project.md` or feature docs.

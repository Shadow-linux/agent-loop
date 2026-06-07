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
| What does this project do? | `onboarding-db/overview.md` |
| How do I run it? | `setup-and-run.md`, `environment.md` |
| Where do I start reading code? | `README.md`, `code-map.md` or `directory-map.md` |
| What does this module do? | module reading path, `module-map.md` or `module-<name>.md` |
| What are the system boundaries? | `architecture-and-integrations.md` or `architecture-boundaries.md`, boundary diagram |
| How does this business flow work? | `flows-and-data.md` or `core-flows.md`, related flow diagram |
| How do async/events/jobs work? | `architecture-and-integrations.md`, `async-and-events.md`, `jobs-and-schedules.md`, related diagrams |
| How do I understand async queues, consumers, callbacks, or background jobs? | README async reading path, `async-and-events.md`, `jobs-and-schedules.md`, async/job diagrams |
| I followed setup docs and it does not work | `setup-and-run.md`, `environment.md`, `verification-and-risks.md`, then `onboarding-diagnostics.md` Startup Failure Diagnosis |
| How is it deployed? | `setup-and-run.md`, `environment.md`, `deployment-and-operations.md`, deployment diagram |
| What changes if I modify this area? | `change-impact-map.md` or relevant section, then `onboarding-diagnostics.md` Change Impact Analysis |
| Who or what changes this state/status? | `flows-and-data.md`, `data-model.md`, state diagram, then `onboarding-diagnostics.md` State Change Trace |
| Why was this designed this way? | `decisions-and-history.md` or Compact equivalent, then `onboarding-diagnostics.md` Design Decision Routing |
| Docs conflict with code | code reality + `risks-and-unknowns.md` |

If `project.md` is insufficient, read onboarding-db. If onboarding-db is insufficient or stale, inspect code reality and propose an onboarding-db update.

## Guided Newcomer Onboarding

Use this when onboarding-db already exists and the human says they are new to the project, asks "where should I start", asks to be guided through project takeover, or asks the agent to explain the project step by step.

The agent owns the reading sequence. Do not dump the full document list and wait for the human to navigate.

Recommended flow:

```text
freshness check -> 10-minute orientation -> reading path -> human question -> targeted explanation -> optional targeted scan/update proposal
```

Steps:

1. Check onboarding-db freshness and review status. If it is stale or unreviewed, say so before relying on it.
2. Give a short orientation: project purpose, runtime shape, main modules, main flows, and how to run/verify.
3. Recommend exactly one first reading path from `onboarding-db/README.md`.
4. Ask the human what they want to understand next, with 2-4 concrete options such as module, flow, async/jobs, deployment, tests, state trace, design decisions, or change impact.
5. When answering, read the matching onboarding-db path first, then inspect code reality only if the docs are missing, stale, contradictory, or too thin.
6. If the answer reveals a stable missing fact, propose an onboarding-db update through Batch Human Review.
7. If the human is trying to start development, route back to the normal agent-loop stage after the explanation.

Newcomer summary format:

| Area | What To Know First | Where To Read | Confidence | Unknowns |
|---|---|---|---|---|

Do not mark onboarding complete just because the DB exists. The human takeover is complete only when the human has a next reading path or next development action.

## On-Demand Explanation And Diagram Updates

Use this when the human does not understand a call path, flow, async/job behavior, integration, deployment route, state transition, or boundary relationship.

Behavior:

1. Route to Targeted Onboarding Scan for the smallest relevant scope.
2. Read the current onboarding-db path and source evidence.
3. Inspect code reality only for the selected module/flow/problem area.
4. Answer with a small explanation and, when useful, a focused diagram.
5. Propose updating or adding the diagram/doc only after explaining what changed and why.
6. Use Batch Human Review before writing `.agent-loop/onboarding-db/` updates.

Suggested diagram update table:

| Question | Proposed Diagram | Target File | Source Evidence | Confidence | Human Decision |
|---|---|---|---|---|---|

Do not create a full repository graph to answer a targeted question. Add or update the smallest diagram that makes the unclear path understandable.

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

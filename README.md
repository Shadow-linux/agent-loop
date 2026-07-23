# Agent Loop

**Current version:** 1.5.0

Agent Loop is a reusable controller skill for single-human, CLI-agent software development. It lets the Agent own project diagnosis, workflow sequencing, implementation, verification, and memory maintenance while the human keeps control of goals, product meaning, consequential decisions, and external actions.

> Human-directed · Agent-owned · Evidence-verified

## Autonomous Workflow

![Agent Loop autonomous workflow](docs/assets/agent-loop-autonomous-workflow.svg)

The human sets the goal and confirms consequential decisions. Between those gates, the Agent independently understands the project, shapes the product, selects the smallest safe delivery route, plans and implements, verifies the result, repairs drift, updates durable memory, and recommends the next action.

Open the [interactive autonomous workflow](docs/assets/agent-loop-autonomous-workflow.html) to follow the Agent-owned path and Human Gates, or inspect its [Archify workflow source](docs/assets/agent-loop-autonomous-workflow.workflow.json).

## Capability Map

![Agent Loop capability map](docs/assets/agent-loop-capability-map.svg)

The diagram is an overview, not the runtime source of truth. Open the [interactive capability map](docs/assets/agent-loop-capability-map.html) to inspect relationships and guided views, or review its [Archify workflow source](docs/assets/agent-loop-capability-map.workflow.json). Canonical behavior remains in `references/design.md` and `references/runtime.md`.

The primary loop is:

```text
Human Goal
→ Agent Loop Controller
→ Product Definition
→ Design Readiness / Decision & Design If Needed
→ Right-sized Delivery
→ Fresh Verification and Review
→ Project Memory and Verified Close
```

## What Agent Loop Can Do

### Understand and operate a project

| Capability | What the Agent owns | Durable result |
|---|---|---|
| Message Intent Guard | Distinguish chat, requirements, operational support, Feature work, Bug follow-up, project-skill work, and archive maintenance before writing artifacts | Correct first route without workflow pollution |
| Project Entry | Initialize, resume, re-adopt, or recover a local or remote project | One accepted memory root and a safe next action |
| Project Entry Scan | Inspect repository structure, commands, boundaries, active work, guidance, and uncertainties | Reliable `.agent-loop/project.md` or enterprise memory; Project Entry Scan if needed |
| Remote Project Discovery | Resolve local pointers, remote paths, containers, and execution boundaries | Explicit environment and entry evidence |
| Operational Support | Explain, run, test, deploy, diagnose, or prepare a runbook from current code and configuration | Read-only analysis first; mutation only through the right gate |
| Evidence-Graph + DDD Onboarding | Build a newcomer-oriented, evidence-backed map of domains, flows, code, and operations | `.agent-loop/onboarding-db/` |
| Root Guidance | Detect stale or missing `AGENTS.md` / `CLAUDE.md` and propose managed guidance repair | Human-reviewed project bootstrap rules |

Existing legacy onboarding-db files remain readable evidence; migration requires the current Onboarding gates.

### Shape Requirements Before Features

Agent Loop uses **Adaptive Product Definition** and an internal Requirement/Product Grill to turn a human need into an accepted product definition.

| Capability | What the Agent owns | Durable result |
|---|---|---|
| Adaptive Product Definition | Choose `brief` or `standard` depth from scope and uncertainty instead of forcing a large PRD | Requirement-owned `product.md` |
| Concept Foundation | Stabilize concept identity, vocabulary, ownership, lifecycle, and boundaries before detailed design | Confirmed concept definitions |
| Requirement Product Model | Derive applicable roles, permissions, commands, events, flows, states, product data/facts, invariants, exceptions, and recovery | Stable IDs and reviewable product views |
| Product Consensus | Research evidence, recommend answers, ask one blocking question at a time, and rewrite the design after accepted feedback | Human-reviewed product baseline |
| Requirement Lifecycle / Backlog | Track proposed, accepted, deferred, in-progress, partially implemented, implemented, superseded, rejected, and reference-only needs without polluting project memory | Requirement README and optional `requirements/INDEX.md` |
| Delivery Phases | Split a large platform or complete requirement into accepted delivery phases without losing the whole-product model | Requirement lifecycle and Feature mapping |
| Optional Visual Communication | Use a project visual skill or Archify to clarify flows, state, boundaries, sequence, and alternatives | Visual aid for convergence; Markdown remains authority |
| Design Readiness | Decide whether accepted product meaning needs shared technical design before Feature construction | `design-not-needed` evidence or ADR candidate |
| Decision & Design / ADR | Land shared business, state, data, architecture, recovery, compatibility, and non-functional decisions into implementation slices | Human-accepted `.agent-loop/decisions/*.md` when required |

During requirements discussion, the agent records Design Readiness evidence and Decision Candidates without creating ADR files. A requirement-driven ADR resolves an Effective Requirement Snapshot and gives every in-scope model ID a Requirement Model Technical Landing Trace before Feature Spec.

New Feature work creates no Feature `product.md`; Feature `spec.md` selects a bounded Product Slice from the effective Requirement Product Definition.

### Deliver with the smallest safe workflow

| Route | Use it for | Control and evidence |
|---|---|---|
| Chat | Questions, explanation, status, or discussion with no requested workflow action | No Requirement or Feature created by default |
| Operational Support | Code-guided testing, diagnosis, rollout planning, or environment help | Read-only first; production/external actions remain gated |
| Lightweight Change Lane | Bounded, reversible, ordinary non-Bug work with exact verification | Persistent monthly Change card, adaptive Plan, targeted checks, diff review, rollback, Memory Review |
| Feature | Behavior, API, state, data, permission, security, architecture, migration, broad impact, or uncertain consumers | Product Slice, spec, tasks, tests, Plan, TDD, verification, review, drift, memory |
| Bug Follow-up | Explicit Bug identity, evidence, deduplication, expected behavior, ownership, repair, and close | `bugs/YYYY-MM-DD-<bug-slug>/` plus a Feature-owned code repair |

Feature delivery includes:

- direct Product Requirement Source and bounded Product Slice in `spec.md`
- story/task breakdown, test design, Web E2E discovery, and construction-grade planning
- TDD with real RED/GREEN evidence for behavior changes
- optional Delivery Contracts for durable producer-consumer boundaries
- optional project-local Skills for repeatable, verified project operations
- mandatory helper resolution for Project Skill Creation / Update, Brainstorm, Plan Gate, execution, diagnosis, verification, and review
- Feature Auto-Loop and Task Auto-Run for uninterrupted Agent-ready work
- approved subagent execution and complex artifact modes when scale requires them

### Verify, review, and close

Agent Loop does not treat “code written” as done. Completion requires proportional, fresh evidence:

```text
Execute
→ Verify
→ Review
→ Drift Check
→ Project Memory Update
→ Feature Completion Check
→ Human-reviewed Submit / Pause / Close
```

The Agent checks implementation, tests, requirement and decision coverage, unrelated changes, stale documentation, rollback, residual risk, and the next recoverable action. Structural validators help, but never replace semantic Human Review.

### Maintain project truth over time

| Capability | Purpose |
|---|---|
| Project Memory | Preserve stable facts, current work, recovery points, commands, constraints, and accepted decisions |
| Human-Guided Branch Management | Recommend an optional branch strategy when project conventions are unclear; preserve existing clear rules. See [Usage](Usage.md#我想让-agent-推荐分支管理方式). |
| Human-Guided Bug Management | Maintain Bug identity, report provenance, lifecycle, Resolution Path, reopen history, and independent close |
| Feature Follow-up / Flow-back | Locate responsible recent or archived Features; default ownership scan is 90 days and extends on evidence |
| Feature Monthly Archive / Rehydrate | Move eligible closed Feature directories intact into month buckets and locate them through `features/archive.md` |
| Post-Merge Memory Reconciliation | After code merge and verification, do nothing when no memory conflict is observed; otherwise repair only the conflicting current meaning from the latest verified facts |
| Drift and Recovery | Detect stale or contradictory claims and backfill from current code, environment, accepted product meaning, and human authority |

Small, fact-determined memory conflicts are resolved and verified by the Agent without creating a report. The human sees only the few alternatives that remain genuinely ambiguous. A concise Memory Merge Report is reserved for coupled conflicts, cross-session work, substantial rollback evidence, or an explicit request. Four-snapshot, all-path Scan → Plan → Apply → Restore tooling is available only through an explicitly authorized **Full Memory Audit / Recovery**.

## Agent Autonomy and Human Control

The Agent owns:

- inspecting available evidence before asking
- identifying the current stage and smallest safe route
- planning at the depth the risk needs
- implementation, tests, verification, review, drift repair, and documentation backfill
- keeping work resumable and recommending the next action
- continuing authorized work until verified completion or a real Human Gate

The human owns:

- goals, scope, source requirements, and accepted product meaning
- unresolved product or technical choices with material consequences
- changes to human-authored source material
- production, paid, secret-bearing, destructive, or external-service actions
- branch mutation, commit, push, PR, merge, tag, release, and publish
- acceptance of ADRs, Delivery Contracts, Feature close, Bug close, and other explicit lifecycle gates

Approving one gate never approves another.

## Quick Start

### 1. Install

Place this repository in the skill directory used by your CLI agent. For Codex:

```bash
git clone https://github.com/Shadow-linux/agent-loop.git ~/.codex/skills/agent-loop
```

For other compatible agents, use that runtime's global or project-local skill directory. Do not copy Agent Loop into a target project's `.agent-loop/`; that directory stores project memory and work artifacts, not the skill package.

### 2. Let Agent Loop take over a project

Tell the Agent:

```text
Use Agent Loop to take over this project.
See where things stand, then keep the agreed work moving until you need a decision from me.
```

The Agent will inspect project state before proposing `.agent-loop/` memory or root guidance. It will not create a Feature merely because the task has several steps.

### 3. Start from a need, not from a stage name

```text
I have a product idea, but it is still rough. Help me clarify it before we build anything.
Let me know first if a full product-design pass will take a lot of discussion or tokens.
```

After the product definition is accepted, ask:

```text
The product definition is approved. Work out what technical design is still needed,
then start with the smallest sensible implementation slice.
```

### 4. Resume safely

```text
Continue the last Agent Loop task.
Check the current state first, then resume from the safest point.
```

See [Usage.md](Usage.md) for copy-ready prompts covering requirements, ADR, lightweight changes, Features, Bugs, project-local Skills, branch strategy, archive/rehydrate, post-merge memory reconciliation, submission, and close.

## Artifact Layout

```text
.agent-loop/
  project.md                    # stable project memory
  project/                      # optional enterprise memory
  onboarding-db/                # project understanding knowledge base
  requirements/
    YYYY-MM-DD-<topic>/
      README.md                 # lifecycle and effective source pointer
      product.md                # accepted Brief/Standard product definition
      sources/                  # preserved human originals
      visuals/                  # optional derived visual sources/renders
  decisions/
    0001-<decision>.md          # optional, Human-gated ADR
  changes/
    YYYY-MM/
      YYYY-MM-DD-<topic>.md     # persistent lightweight execution card
  bugs/
    INDEX.md
    YYYY-MM-DD-<bug>/
      README.md
      evidence/
  features/
    archive.md
    YYYY-MM-DD-<feature>/
      spec.md
      tasks.md
      tests.md
      plan.md
      notes.md
      contracts.md              # optional
    YYYY-MM/
      YYYY-MM-DD-<feature>/     # archived directory kept intact
  skills/
    INDEX.md
    <skill-name>/
      SKILL.md
      validation.md
  memory-merges/
    MM-<merged-code-sha>-<topic>/
      README.md                 # only for complex or durable conflict review
```

New projects use `.agent-loop/`. A visible legacy `agent-loop/` root remains readable and requires Human-confirmed migration. Dual roots fail closed.

Ordinary post-merge handling does not create `memory-merges/`: no observed conflict means no scan or report, and a small conflict stays in the conversation unless durable coordination or recovery evidence is needed.

Project-local capability discovery starts at `.agent-loop/skills/`; runtime/global Skill inventory does not replace `.agent-loop/skills/INDEX.md`.

## External Helpers and Visuals

Agent Loop remains the controller when it uses Superpowers-style helpers, project-local Skills, Archify, or other adapters. Helpers can improve a stage method; they cannot change Agent Loop artifact ownership, stage order, status, or Human Gates.

For complex product or technical communication, Agent Loop prefers an active project-local visual skill, then installed [Archify](https://github.com/tt-a1i/archify). When Archify is absent but would materially improve review, the Agent recommends its exact installation/use before offering Mermaid/ASCII/text; fallback remains valid after decline, unsupported environments, or failure. Installing any external skill requires separate, exact Human authorization.

The visual rule is:

> Render to converge; text to record.

Working visuals help humans correct the Agent's understanding. Accepted meaning must be rewritten into the owning Markdown. A durable visual additionally binds typed source and render with digests and validation evidence.

In Feature Spec, a visual may explain only the accepted Product Slice, feature responsibility, and feature-local implementation or acceptance path. Accepted feature-local clarification returns to `spec.md`; new product meaning returns to Requirements Discussion and is never written directly to Requirement `product.md` from Feature Spec.

## Published Sources

| Source | Responsibility |
|---|---|
| `SKILL.md` | concise controller entrypoint |
| `references/design.md` | core model and constraints |
| `references/runtime.md` | executable routing, stage order, gates, and state transitions |
| `references/` | stage and capability rules |
| `templates/` | target-project artifact templates |
| `Usage.md` | human trigger phrases and operation guide |
| `CHANGELOG.md` | version history |
| `examples/` | downstream project examples and validation fixtures |

`references/design.md` owns the core model and constraints; `references/runtime.md` owns executable routing, stage order, gates, and state transitions.

## License

MIT

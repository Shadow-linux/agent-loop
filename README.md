# Agent Loop

**Current version:** 1.2.3

A reusable [Codex](https://github.com/openai/codex) / CLI-agent skill for single-person software development workflows—from goal intake to verified close.

## What It Is

**Agent Loop** is a controller skill. It tells the agent:

- What stage the project is in
- Which reference to load next
- What artifacts to produce or update
- When to stop and ask the human

The human controls goals, source requirements, and stage gates. The agent controls workflow mechanics, artifacts, implementation, verification, and backfill.

## Why Use It

Without a structured loop, agents tend to:

- Skip specification and jump straight to code
- Miss edge cases and drift from requirements
- Leave tasks "done" without fresh verification
- Lose project context between sessions

Agent Loop fixes this with a repeatable, inspectable workflow:

```
Message Intent → Chat And Requirements Discussion if needed
→ Project Entry → Remote Project Discovery if needed
→ Re-Adopt Agent Loop Project if needed
→ Project Onboarding Scan if needed
→ Operational Support if needed → Requirement Archive
→ Product Brief if needed → Brainstorm / Clarify if needed
→ Feature Follow-up / Flow-back if needed
→ Targeted Feature Scan if needed → Feature Spec → Requirement Checklist
→ Work Breakdown → Delivery Contract if needed → Test Design
→ E2E Discovery if Web → Technical Design / Code Context
→ Plan Gate / Plan if needed → Analyze Consistency
→ Subagent Execution if approved → Execute Task / Story
→ Verify → Review → Drift Check → Project Memory Update
→ Feature Completion Check → Submit / Integrate if requested
→ Pause / Close
```

## Core Concepts

| Concept | Meaning |
|---|---|
| **Feature** | One behavior-changing work area under `.agent-loop/features/<date>-<slug>/` |
| **Story** | User-perspective slice inside a feature (e.g. `US1`, `US2`) |
| **Task** | Default executable engineering unit. Small, verifiable, tied to a story. |
| **Plan** | Construction-grade execution plan for the active task/story |
| **Evidence** | Fresh proof: test output, build output, API results, E2E checks, logs |
| **Drift** | Mismatch between docs, code reality, or human decisions |
| **Feature Follow-up / Flow-back** | Bug/change intake that checks recent features before creating a new feature. Default lookback is 30 days. |
| **Operational Support** | Read-only code-guided help for testing, running, deploying, switching accounts/config/models/providers, quota checks, rollout, and production diagnosis before deciding whether feature work is needed. |
| **Requirement Lifecycle / Backlog** | Requirement memory for proposed, accepted, deferred, in-progress, implemented, superseded, rejected, or reference-only requirements without using project memory as a backlog. |
| **Chat And Requirements Discussion** | `chat` answers or discusses without creating artifacts; `requirements-discussion → Brainstorm / Clarify → requirement document → requirements/` before any feature construction. |
| **Delivery Contract** | Optional producer-consumer boundary handoff. Used only when API, event, public data, UI state/behavior, SDK/library, runtime, or explicit cross-agent/human handoff needs a stable contract. |

## Artifact Layout

```
.agent-loop/
  remote.md                           # optional local-entry pointer for remote projects
  project.md                          # Long-term project memory
  project/                            # optional enterprise memory detail files
  onboarding-db/                      # optional human-readable project onboarding docs
    maps/                             # optional categorized navigation docs
    modules/                          # optional core module detail docs
    flows/                            # optional flow detail docs
    runtime/                          # optional run / async / deploy docs
    domain/                           # optional data / state / glossary docs
    quality/                          # optional testing / risk docs
  requirements/
    INDEX.md                           # optional inventory and backlog/deferred view
    YYYY-MM-DD-<topic>/
      README.md                        # requirement set lifecycle and source index
      requirement.*                     # optional source file when provided
      prototype.*                       # optional source file when provided
      feedback.*                        # optional source file when provided
      notes.*                           # optional source file when provided
  features/
    YYYY-MM-DD-<feature-slug>/
      product.md    (optional)
      spec.md
      tasks.md
      tests.md
      plan.md
      notes.md
      contracts.md  (optional)
      tasks/        (optional complex details)
      tests/        (optional complex details)
      plans/        (optional dated plan cycles)
      handoffs/     (optional subagent briefs and returns)
      contracts/    (optional contract details)
```

New target projects use `.agent-loop/` by default. Existing visible `agent-loop/` roots remain readable as legacy memory and should be migrated only after human confirmation.

## Quick Start

### 1. Install the Skill

Copy this directory into your agent's skill path:

```bash
# For Codex CLI
~/.codex/skills/agent-loop/

# For project-local use
./.kimi/skills/agent-loop/
```

### 2. Initialize a Project

Tell the agent:

> "Let's set up agent-loop for this project."

The agent will:
- Inspect the repo
- Classify the entry scenario (new / existing / remote / resume)
- Load the right references
- Propose `.agent-loop/project.md`, root `AGENTS.md`, and a `CLAUDE.md` pointer to `AGENTS.md`

For existing projects, the agent separates safe-entry memory from durable onboarding docs:

| Path | Use When |
|---|---|
| **Safe-entry project memory** | Build enough project memory, root guidance status, commands, boundaries, and uncertainties to continue work soon |
| **Deep Onboarding** | Create durable `.agent-loop/onboarding-db/` docs through accepted `onboarding-spec.md`, accepted `onboarding-plan.md`, and reviewed batches of `deep-dives/<topic>.md` |
| **Focused Deep Onboarding** | Preserve understanding for one module, flow, async task, deployment path, state transition, or problem area using the same Deep Onboarding gates with a narrow scope |

### 3. Start a Feature

> "I want to add login."

After project init/onboarding is accepted, the agent will:

- Archive your requirement
- Write `spec.md` with stories and acceptance criteria
- Break down `tasks.md`
- Design `tests.md`
- Execute tasks with TDD

### 4. Get Guided Through An Existing Project

> "带我熟悉这个项目，从哪里开始看？"

If `.agent-loop/onboarding-db/` exists, the agent uses it first: it checks freshness, gives a short orientation, recommends one reading path, answers targeted questions, and proposes focused diagram/doc updates only after confirmation.

There is only one durable project-understanding onboarding mode: Deep Onboarding. If onboarding-db is missing and the human only wants to continue work, the agent should update project memory/root guidance and not create onboarding-db detail docs.

Deep Onboarding is spec-first: `onboarding-spec.md` defines readers, goals, required-core onboarding topic inventory, non-goals, and quality bar; `onboarding-plan.md` defines batch review cadence, split gate, batches, and review checkpoints; then the agent writes evidence-backed `deep-dives/<topic>.md` docs. Deep Onboarding has no total document count cap. Batch size is review pacing, not a total limit. Focused questions use the same flow with a narrow spec/plan and usually one focused deep-dive doc or update.

After each onboarding explanation, the agent should recommend one next action: read a specific doc, inspect a module/flow, generate or update a focused diagram, run a setup/verification command, or return to feature development.

Onboarding-db human-readable docs default to Chinese, while code symbols, file paths, commands, API names, and artifact names stay as-is. Legacy `modules/`, `flows/`, `runtime/`, `domain/`, and similar directories may be read as evidence in old projects, but new onboarding generation should not recreate directory-first template files.

### 5. Continue Later

> "Continue the login feature."

The agent reads `.agent-loop/project.md`, finds the active feature, and resumes from the last checkpoint.

### 6. Handle Bugs After Close

> "测试发现上次做的上传功能有 bug."

The agent does not immediately create a new feature. It first checks recent features, using a 30-day default lookback window, then presents candidate matches with evidence. After human confirmation it either flows the work back to the owning feature, creates a linked new feature, creates a `Feature Type: maintenance-fix` feature, or investigates first.

If a closed feature is reopened for follow-up, the original close record remains intact. The follow-up gets its own `notes.md` intake record, updated tasks/tests/plan as needed, fresh verification, review, drift check, and a new close confirmation.

If no recent feature owns the bugfix and the work is not a new product capability, the agent creates a narrow maintenance-fix feature under `.agent-loop/features/YYYY-MM-DD-fix-<slug>/`. Maintenance fixes still use spec/tasks/tests/plan/notes, fresh verification, review, drift check, project memory impact check, and close.

## Execution Modes

| Mode | Description |
|---|---|
| **Strict Mode** (default) | Agent asks before and after every stage |
| **Feature Auto-Loop** | After Feature Spec acceptance, agent advances Agent-ready stages automatically |
| **Task Auto-Run** | After plan acceptance, agent completes one task/story through TDD, verification, review, and drift check |

Auto modes still stop for Human-gated decisions, unclear decisions, risky changes, failed verification, drift needing approval, unrelated dirty work blocking progress, human original requirement changes, first-version exclusions, Delivery Contract creation/acceptance/breaking changes, directory guidance changes, unapproved subagent dispatch, submit, pause, close, commit, PR, merge, release, or publish.

## External Skill Adapters

Agent Loop can use external skills such as Superpowers for brainstorming, construction-grade planning, TDD, debugging, verification, review, finishing, and bounded subagent execution.

Brainstorm, Plan Gate, Execute, Diagnose, Verify, Review, and approved Subagent Execution are mandatory helper-backed stages. Before stage actions, the agent resolves the canonical Superpowers name and unprefixed alias, loads the complete helper when found, and records the result. Fallback is permitted only after recording that the helper is unavailable or failed to load.

External skills are stage helpers only. Agent Loop still owns artifact paths, human gates, task status, project memory, drift, submit, pause, and close. Native external directories such as `docs/superpowers/*` are not created by default, even when a helper declares them as its normal destination.

## Delivery Contracts Are Optional

`contracts.md` is not a default artifact for every feature. The agent should suggest a Delivery Contract only when the human asks for cross-boundary handoff/API/interface documentation, or when the agent detects a likely downstream consumer such as frontend, another service, SDK user, shared event, public data schema, UI state contract, or runtime integration.

Simple single-person tasks, pure internal logic, and changes with no downstream consumer should skip contract files.

## When to Use

- Initialize agent-managed development in a new or existing project
- Re-adopt an old `agent-loop` project after code changed without updating docs
- Turn requirements or prototypes into specs, tasks, tests, plans, and implementation
- Continue a paused feature or recover project context
- Execute a task/story with TDD and verification
- Submit, pause, resume, or close a feature

## When NOT to Use

- One-off edits that explicitly bypass workflow
- Changes that do not affect feature behavior, public interfaces, or project memory

## Examples

See [`examples/`](./examples/):

- [`login-feature/`](./examples/login-feature/) — Small feature with TDD workflow
- [`complex-saas-project/`](./examples/complex-saas-project/) — Larger takeover + feature execution with delivery contracts
- [`remote-entry/`](./examples/remote-entry/) — Local directory pointing to a remote project

## Design Sources

This skill stays aligned with:

- `draft_agent_loop_struct.md`
- `final_agent_loop_skill_design.md`

If a reference conflicts with either design source, the design source wins.

## License

MIT

# Agent Loop

**Current version:** 1.2.0

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
Project Entry → Remote Project Discovery if needed
→ Re-Adopt Agent Loop Project if needed
→ Project Onboarding Scan if needed → Requirement Archive
→ Product Brief if needed → Brainstorm / Clarify if needed
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
    YYYY-MM-DD-<topic>/
      README.md
      requirement.*
      prototype.*
      feedback.*
      notes.*
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

For existing projects, the agent offers onboarding modes:

| Mode | Use When |
|---|---|
| **Quick Onboarding** | Build enough project memory to continue feature work soon |
| **Deep Project Onboarding Scan** | Generate newcomer-readable `.agent-loop/onboarding-db/`, diagrams, and backfill proposals |
| **Targeted Onboarding Scan** | Understand one module, flow, async task, deployment path, or problem area |

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

If `.agent-loop/onboarding-db/` exists, the agent uses it first: it checks freshness, gives a short orientation, recommends one reading path, answers targeted questions, and proposes focused diagram/doc updates only after confirmation. Deep onboarding defaults to Expanded onboarding-db output with categorized docs such as `maps/`, `modules/`, `flows/`, `runtime/`, `domain/`, and `quality/`. Compact or Standard onboarding-db layouts are used only when the human explicitly requests fewer/simpler files, or when maintaining an existing onboarding-db already organized that way. Onboarding-db human-readable docs default to Chinese, while code symbols, file paths, commands, API names, and artifact names stay as-is.

### 5. Continue Later

> "Continue the login feature."

The agent reads `.agent-loop/project.md`, finds the active feature, and resumes from the last checkpoint.

## Execution Modes

| Mode | Description |
|---|---|
| **Strict Mode** (default) | Agent asks before and after every stage |
| **Feature Auto-Loop** | After Feature Spec acceptance, agent advances Agent-ready stages automatically |
| **Task Auto-Run** | After plan acceptance, agent completes one task/story through TDD, verification, review, and drift check |

Auto modes still stop for Human-gated decisions, risky changes, failed verification, Delivery Contract creation/acceptance/breaking changes, unapproved subagent dispatch, submit, pause, close, commit, PR, merge, release, or publish.

## External Skill Adapters

Agent Loop can use external skills such as Superpowers for brainstorming, construction-grade planning, TDD, debugging, verification, review, finishing, and bounded subagent execution.

External skills are stage helpers only. Agent Loop still owns artifact paths, human gates, task status, project memory, drift, submit, pause, and close. Native external directories such as `docs/superpowers/*` are not created by default.

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

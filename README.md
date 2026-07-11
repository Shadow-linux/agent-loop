# Agent Loop

**Current version:** 1.2.4

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
→ Project Entry Scan if needed
→ Project Skill Creation / Update if requested
→ Operational Support if needed → Requirement Archive
→ Decision & Design If Needed → Product Brief if needed
→ Brainstorm / Clarify if needed
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
| **Project-Local Skill** | A reusable project capability under `.agent-loop/skills/<skill-name>/`. Creation or material update requires Gate 1; successful validation activates it, but every actual invocation still requires a bounded Execution Gate. |
| **Requirement Lifecycle / Backlog** | Requirement memory for proposed, accepted, deferred, in-progress, partially implemented, implemented, superseded, rejected, or reference-only requirements without using project memory as a backlog. |
| **Chat And Requirements Discussion** | `chat` answers or discusses without creating artifacts; `requirements-discussion → Brainstorm / Clarify → requirement document → requirements/` before any feature construction. |
| **Decision & Design / ADR** | Requirement-landing bridge for shared business flow, domain/data rules, architecture, recovery, and non-functional goals. Design Readiness is required; `.agent-loop/decisions/*.md` is Human-gated and conditionally required only when shared design needs a durable record. |
| **Delivery Contract** | Optional producer-consumer boundary handoff. Used only when API, event, public data, UI state/behavior, SDK/library, runtime, or explicit cross-agent/human handoff needs a stable contract. |

## Artifact Layout

```
.agent-loop/
  remote.md                           # optional local-entry pointer for remote projects
  project.md                          # Long-term project memory
  project/                            # optional enterprise memory detail files
  decisions/                          # optional project / cross-feature Decision And Design Records
    0001-<decision-slug>.md
  skills/                             # optional, created only for a confirmed Project Skill Candidate
    INDEX.md                          # lifecycle, load policy, triggers, scope, and validation evidence
    <skill-name>/
      SKILL.md
      validation.md
      agents/openai.yaml              # optional
      references/                     # optional
      scripts/                        # optional
      assets/                         # optional
      templates/                      # optional
  onboarding-db/                      # Evidence-Graph + DDD project-understanding docs; legacy layouts are evidence only
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

For existing projects, the agent separates safe-entry memory from newcomer learning docs:

| Path | Use When |
|---|---|
| **Project Entry Scan** | Build enough project memory, root guidance status, commands, boundaries, capabilities, and uncertainties to continue work safely |
| **Evidence-Graph + DDD Onboarding** | Build `.agent-loop/onboarding-db/` as a newcomer handoff knowledge base after Project Entry Scan or reliable project memory |
| **Existing legacy onboarding-db files** | Evidence only; migration requires accepted Onboarding Spec, Onboarding Tasks, and Full Execution Gate |

### 3. Shape Requirements Before Features

> "先帮我梳理这个需求，不要实现。"

For requirement shaping, the agent should enter Requirements Discussion instead of creating a feature workspace. Requirement/Product Grill is the clarification method for fuzzy terminology, business flows, exception paths, prior feature conflicts, source-of-truth questions, and decision signals. It asks one blocking question at a time, includes a recommended answer, and checks relevant project memory, source requirements, docs, code, tests, and prior feature artifacts before asking when those sources may already answer the question.

Reviewed requirements live under `.agent-loop/requirements/<date>-<topic>/`. If the human later asks to "落到 product.md" from chat or requirements discussion, Product Brief Source Gate applies: the agent first asks whether to create/reference a requirement set or confirm feature start. Feature-level `product.md` is written only after there is a requirement source and confirmed feature context.

During requirements discussion, the agent records Design Readiness evidence and Decision Candidates without creating ADR files. Before an accepted requirement enters feature construction, Design Readiness Check determines whether shared Decision & Design is required.

When the accepted requirement spans features or needs shared business-flow, domain, state, source-of-truth, architecture, recovery, or non-functional design, it enters Decision & Design even when no technology choice is disputed. A decision file is created only after human confirmation. The record assigns every required Design Slice to planned features before Feature Spec:

```text
Requirement -> Design Readiness Check -> Decision & Design If Needed -> Feature Mapping -> Product Brief / Feature Spec
```

Simple work records `design-not-needed` and can continue without a decision file. Feature-local choices stay in `spec.md` Design Decisions. Review and completion verify that implementation conforms to accepted design slices rather than checking feature stories alone.

### 4. Start a Feature

> "I want to add login."

After project init / Project Entry Scan is accepted, the agent will:

- Archive your requirement
- Write `spec.md` with stories and acceptance criteria
- Break down `tasks.md`
- Design `tests.md`
- Execute tasks with TDD

### 5. Get Guided Through An Existing Project

> "带我熟悉这个项目，从哪里开始看？"

Evidence-Graph + DDD Onboarding is the current durable project-understanding flow.

It builds `.agent-loop/onboarding-db/` from verified code evidence into macro-to-micro handoff docs:

- `08-review/evidence-graph.md` before formal docs
- `onboarding-spec.md` for module/flow coverage, DDD mapping, file strategy, quality gates, and batch plan
- `onboarding-tasks.md` for accepted batch execution
- module playbooks under `02-modules/<module-name>.md` by default
- flow playbooks under `03-flows/<flow-name>.md` by default
- coverage matrix and reviewed batch records

The agent must first confirm Project Entry Scan or reliable project memory, then build an Evidence Graph and present an Onboarding Spec for human review. Spec acceptance authorizes creation of Onboarding Tasks; formal onboarding docs begin only after the completed Tasks and their separate Full Execution Gate are accepted. Module and flow docs default to single long files, not many small files. Wireframe architecture flow diagrams are the preferred main way to express every module and flow process. The old Quick / Deep / Targeted onboarding modes and directory-first legacy generation flow are not used.

Existing legacy onboarding-db files may be read as evidence, but they are not trusted without checking code reality. Migration or replacement requires an accepted Onboarding Spec, Onboarding Tasks, and Full Execution Gate.

For focused project-understanding questions, the agent should answer from existing code/docs as `chat` or `operational-support`. It should only enter feature/fix work, requirement discussion, or a future onboarding-document workflow after the human confirms that intent.

### 6. Continue Later

> "Continue the login feature."

The agent reads `.agent-loop/project.md`, finds the active feature, and resumes from the last checkpoint.

### 7. Handle Bugs After Close

> "测试发现上次做的上传功能有 bug."

The agent does not immediately create a new feature. It first checks recent features, using a 30-day default lookback window, then presents candidate matches with evidence. After human confirmation it either flows the work back to the owning feature, creates a linked new feature, creates a `Feature Type: maintenance-fix` feature, or investigates first.

If a closed feature is reopened for follow-up, the original close record remains intact. The follow-up gets its own `notes.md` intake record, updated tasks/tests/plan as needed, fresh verification, review, drift check, and a new close confirmation.

If no recent feature owns the bugfix and the work is not a new product capability, the agent creates a narrow maintenance-fix feature under `.agent-loop/features/YYYY-MM-DD-fix-<slug>/`. Maintenance fixes still use spec/tasks/tests/plan/notes, fresh verification, review, drift check, project memory impact check, and close.

## Execution Modes

| Mode | Description |
|---|---|
| **Strict Mode** (default) | Agent asks before and after every stage |
| **Feature Auto-Loop** | After Requirement Checklist passes and Feature Spec is accepted, agent advances Agent-ready stages automatically |
| **Task Auto-Run** | After plan acceptance, agent runs Analyze Consistency and then completes one task/story through TDD, verification, review, and drift check |

Auto modes still stop for Human-gated decisions, unclear decisions, risky changes, failed verification, drift needing approval, unrelated dirty work blocking progress, human original requirement changes, first-version exclusions, Delivery Contract creation/acceptance/breaking changes, directory guidance changes, unapproved subagent dispatch, submit, pause, close, commit, PR, merge, release, or publish.

Agent Loop keeps at most one Active Feature. Switching work pauses the current feature with a resume point before another feature becomes active. If the agent-loop controller cannot be loaded, existing auto-mode grants are suspended and root guidance is limited to safe read-only entry/recovery/support until the controller is restored.

## Project-Local Skills

Say “把这个流程做成技能” or “把刚才成功的操作沉淀成 skill” when a repeatable, verified project workflow should become a resident capability. The agent may also propose a Project Skill Candidate after a complex operation succeeds, but it must wait for Gate 1 before creating or materially updating files.

Project skills are stored only in the target project under `.agent-loop/skills/`. New or updated skills use RED/GREEN/REFACTOR and remain `proposed` until validation passes; passing validation records a SHA-256 content manifest and automatically changes them to `active`, while failure or later content mismatch leaves them unavailable for normal routing.

Discovery and loading are read-only. Before an active project skill follows its workflow, runs commands, calls tools, changes files, accesses external systems, or causes side effects, the agent must obtain an Execution Gate confirmation for one bounded invocation. `active`, `bootstrap`, Feature Auto-Loop, Task Auto-Run, or a prior invocation never grants reusable execution authority.

## External Skill Adapters

Agent Loop can use external skills such as Superpowers for brainstorming, construction-grade planning, TDD, debugging, verification, review, finishing, and bounded subagent execution.

Project Skill Creation / Update, Brainstorm, Plan Gate, Execute, Diagnose, Verify, Review, and approved Subagent Execution are mandatory helper-backed stages. Before stage actions, the agent resolves the canonical Superpowers name and unprefixed alias, loads the complete helper when found, and records the result. Fallback is permitted only after recording that the helper is unavailable or failed to load.

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

## Published Sources

`references/design.md` owns the core model and constraints; `references/runtime.md` owns executable routing, stage order, gates, and state transitions.

Both sources ship inside the skill package. Workspace-level design drafts may provide historical rationale, but they cannot override published behavior. Stage references, templates, validation scenarios, README, and Usage are derived views and must stay aligned with the published sources.

## License

MIT

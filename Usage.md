# Agent Loop — Usage Guide

This guide explains how the **Agent Loop** skill works, what each stage does, and how to read and write its artifacts.

## The Loop

Every conversation follows the same contract:

```
Inspect → Classify → Recommend → Confirm → Act → Record → Recommend
```

The agent never jumps from a human goal directly to code. Each stage has an entry condition, files to read, files to write, a human gate, and an exit condition.

---

## Entry Classification

When you start a conversation, the agent classifies the project into exactly one state:

| State | Condition | What Happens |
|---|---|---|
| **new-project** | No `.agent-loop/` or legacy `agent-loop/`; little or no code | Init Project |
| **existing-project** | No `.agent-loop/` or legacy `agent-loop/`; meaningful code | Existing Project Onboarding |
| **remote-entry** | Project is remote / container / SSH | Remote Project Discovery |
| **resume** | `.agent-loop/` or legacy `agent-loop/` exists; memory looks current | Resume feature work |
| **re-adopt** | `.agent-loop/` or legacy `agent-loop/` exists but recent work bypassed it | Recovery Backfill |
| **stale-memory** | `.agent-loop/` or legacy `agent-loop/` exists but docs conflict with code | Reconcile Project Context |
| **active-feature** | Active feature exists; next action is clear | Continue current stage |
| **blocked** | Blocker prevents next stage | Ask / Diagnose |

---

## Stage Reference

### Project Entry
- **Entry**: Any use of this skill.
- **Read**: `project.md`, active feature docs, repo docs.
- **Write**: Nothing until you confirm the next stage.
- **Exit**: One recommended next stage.

### Init Project
- **Entry**: New project, no `.agent-loop/` or legacy `agent-loop/`.
- **Load**: `project-guidance.md`, `project-memory-mode.md`, `project-architecture-init.md`.
- **Write after confirmation**: `.agent-loop/project.md`, root `AGENTS.md` / `CLAUDE.md`.

### Existing Project Onboarding
- **Entry**: Existing code, no `.agent-loop/` or legacy `agent-loop/`.
- **Load**: `existing-project-onboarding.md`, `project-guidance.md`, `project-memory-mode.md`.
- **Inspect**: README, docs, package/test scripts, key directories (layered scan).
- **Write after confirmation**: `project.md`, `AGENTS.md`.

### Remote Project Discovery
- **Entry**: Human says project is remote, or local is only an entry point.
- **Write after confirmation**: `.agent-loop/remote.md`, thin `project.md` with `Status: remote-entry`.

### Reconcile / Re-Adopt
- **Entry**: `.agent-loop/` exists but memory is stale, or recent work bypassed the loop.
- **Action**: Compare code reality with `project.md` and feature docs. Propose backfill. Ask before writing.

### Requirement Archive
- **Entry**: Human provides requirement/prototype/materials.
- **Load**: `requirement-management.md`.
- **Rule**: Archive as a requirement set directory. Do not overwrite original requirements. Do not create flat files directly under `requirements/`.
- **Write**: `.agent-loop/requirements/YYYY-MM-DD-<topic>/README.md` + original materials.

### Product Brief (Optional)
- **Entry**: PRD-style synthesis needed before engineering spec.
- **Load**: `product-brief.md`.
- **Write**: `product.md` (feature-level product intent).

### Brainstorm / Clarify
- **Entry**: Goal is vague, scope unclear, or meaningful approaches differ.
- **Rule**: Ask 1–5 high-impact questions. Do not ask filler questions. Inspect docs/code first when possible.

### Feature Spec
- **Entry**: Goal and requirements are clear.
- **Write**: `spec.md` with problem, scope, stories, acceptance criteria, behavior changes, dependencies, out-of-scope, open questions.
- **Exit**: Human accepts spec or requests revision.

### Work Breakdown
- **Entry**: Accepted spec.
- **Write**: `tasks.md`.
- **Rule**: Default to vertical slices. Task IDs: `T001`. Story labels: `US1`. Mark each task `Agent-ready` or `Human-gated`.

### Delivery Contract (If Needed)
- **Entry**: Human asks for frontend/backend handoff, API/interface docs, contract material for another agent/person, or the agent detects likely downstream impact.
- **Load**: `delivery-contracts.md`.
- **Write after confirmation**: `contracts.md` + optional `contracts/<ID>-<slug>.md`.
- **Rule**: Not default for every feature. Skip for simple single-person tasks, pure internal logic, and changes with no downstream consumer. Human confirmation is required before creating/updating contract files, before a contract becomes `accepted`, and before breaking changes after affected-consumer analysis.

### Test Design
- **Entry**: Accepted tasks.
- **Write**: `tests.md` with functional cases, module tests, API tests, E2E cases, regression tests, manual verification, commands.
- **Rule**: Do not assume an E2E framework. Run E2E Discovery first if web-visible behavior exists.

### Technical Design / Code Context
- **Entry**: Accepted tasks and tests, before implementation.
- **Inspect**: Exact files likely to change, nearby tests, existing functions, data flow, call chain, auth, validation, side effects.
- **Rule**: Do not invent signatures or file paths. Prefer existing local patterns.

### Plan (If Needed)
- **Entry**: Selected task/story is complex, multi-file, or human requests a plan.
- **Load**: `implementation-planning.md`.
- **Write**: `plan.md`.
- **Rule**: Construction-grade. Exact paths, signatures, test code, commands, expected RED/GREEN output, rollback, risks. No placeholders like "TBD" or "write tests".

### Analyze Consistency
- **Entry**: Before implementation when spec/tasks/tests/plan exist.
- **Check**: Every requirement has task coverage. Every task maps to spec or technical need. Tests cover acceptance criteria. Plan scope matches selected task/story.

### Execute Task / Story
- **Entry**: Selected execution unit accepted.
- **Rule**: TDD by default. Verify RED before implementation. Verify GREEN after. Record evidence.
- **Task status flow**: `todo → in-progress → review → done`.
- **Important**: A task enters `review` after implementation and verification. It enters `done` only after the **Task Done Gate** passes.

### Verify
- **Entry**: Before any completion claim.
- **Rule**: Identify proof command. Run fresh verification. Read output. Record evidence in `notes.md`.

### Review
- **Entry**: After implementation and verification, before marking `done`.
- **Check**:
  - **Spec Review**: matches `spec.md`, acceptance criteria, scope.
  - **Standards Review**: follows `AGENTS.md`, `project.md` rules, local conventions.
- **Record**: Findings in `notes.md`.

### Drift Check
- **Entry**: After implementation or before close.
- **Check**: Implementation vs `spec.md`. Completed work vs `tasks.md`. Test reality vs `tests.md`. Long-term changes vs `project.md`. Confirmed interfaces vs `contracts.md` when present.
- **Write after confirmation**: Update feature docs, `project.md`, `notes.md`, and confirmed `contracts.md` changes when applicable.

### Project Memory Update
- **Entry**: After Drift Check, before Submit / Integrate, Pause, or Close.
- **Write**: `project.md` (simple mode) or `project.md` + `project/*.md` (enterprise mode).
- **Rule**: Update only durable project facts. Do not write task execution logs or raw test output.

### Feature Completion Check
- **Entry**: After Verify/Review/Drift Check, or before starting a new feature while another is active.
- **Check**: Spec accepted. Tasks done or removed. Tests recorded. Fresh evidence exists. Feature Close Review completed. Drift check done. Memory updated.
- **Exit**: Recommend Close, Continue, Pause, or Scope Update. Close still requires explicit human confirmation.

### Submit / Integrate
- **Entry**: Human asks to submit, commit, or prepare PR.
- **Load**: `submit-and-integrate.md`.
- **Rule**: Inspect diff and untracked files. Separate product code from `agent-loop` artifact changes. Never commit or claim submission readiness without human confirmation.

### Pause / Close
- **Pause**: Record current state, next action, blockers, touched files, resume point.
- **Close**: Requires fresh verification, Feature Close Review, drift check, memory update, and explicit human confirmation.

---

## Task Done Gate

A task is **NOT** `done` just because code was written.

```
done = implementation complete
     + required tests or substitute verification run fresh
     + evidence recorded in notes.md
     + lightweight Spec Review recorded
     + Standards Review recorded when triggered
     + drift decision recorded
     + tasks.md or task detail names the evidence location
```

---

## Gate Modes

| Mode | What It Means |
|---|---|
| **Strict Mode** | Agent asks before and after every stage (default) |
| **Feature Auto-Loop** | After Feature Spec acceptance, agent advances Agent-ready stages until a stop condition |
| **Task Auto-Run** | After plan acceptance, agent completes one task/story through TDD, verification, review, drift, and status update |

Stop conditions for auto modes:
- Human-gated work
- Unclear decisions
- Risky changes
- Failed verification
- Drift needing approval
- Delivery Contract file creation, acceptance, or breaking changes
- Subagent dispatch without explicit approval
- Submit, pause, close, commit, PR, merge, release, or publish

---

## External Skill Adapters

When Superpowers or another external skill is available, the agent may use it inside the current stage:

| Stage Need | External Skill Role | Agent Loop Still Owns |
|---|---|---|
| Clarification / product discovery | Better questions, options, product thinking | `product.md`, `spec.md`, human approval |
| Planning | Construction-grade plan quality | `plan.md` / `plans/*`, execution mode |
| TDD / debugging / verification / review | Method discipline and evidence rigor | `notes.md`, Task Done Gate, drift decision |
| Finishing | Branch/submission decision support | Submit gate, diff review, final confirmation |
| Subagents | Bounded independent execution help | Dispatch approval, briefs, review, merge, status |

External skill paths are advisory. Do not create `docs/superpowers/*` or other native external directories unless the human explicitly asks and confirms again after the agent explains the agent-loop path override.

Feature Auto-Loop and Task Auto-Run do not imply subagent approval. Subagents require explicit dispatch confirmation, or one bounded task-group confirmation with task IDs, boundaries, briefs, stop conditions, and main-agent review responsibility.

---

## Artifact Quick Reference

| File | Owns | Does Not Own |
|---|---|---|
| `project.md` | Long-term project facts | Task logs |
| `spec.md` | Intended feature behavior | Execution logs |
| `tasks.md` | Work breakdown, status | Full test evidence |
| `tests.md` | Test design, matrix | Raw test output |
| `plan.md` | Active execution plan | Historical record |
| `notes.md` | Decisions, evidence, drift, pause/close | Original requirements |
| `contracts.md` | Optional delivery contract index for confirmed producer-consumer boundaries | Temporary subagent assignments |
| `product.md` | Feature-level product intent | Engineering execution plan |

---

## Naming Conventions

```
Feature directory:  .agent-loop/features/YYYY-MM-DD-<feature-slug>/
Requirement set:    .agent-loop/requirements/YYYY-MM-DD-<topic>/
Core files:         spec.md, tasks.md, tests.md, plan.md, notes.md (stable names)
Plan metadata:      Plan ID: YYYY-MM-DD-<task>-<slug>
```

Requirement set dates are **archive dates only**. They are not deadlines, start dates, or end dates. Feature directory dates identify when the feature workspace was created or adopted; do not infer delivery deadlines or feature duration from them.

---

## Status Values

**Feature / Project:**
```
draft, active, blocked, paused, closed
```

**Task:**
```
todo, in-progress, review, done, blocked, skipped
```

**Delivery Contract:**
```
draft, accepted, implemented, verified, superseded
```

---

## Drift Rules

When something changes, update the right artifact:

| Change | Update |
|---|---|
| Feature behavior changed | `spec.md` |
| Product intent changed | `product.md` |
| Cross-feature consensus changed | `project.md` Product Context / Domain Language |
| Task set/order changed | `tasks.md` |
| Test strategy changed | `tests.md` |
| Active execution changed | `plan.md` |
| Evidence/execution happened | `notes.md` |
| Confirmed producer-consumer interface changed | `contracts.md` + matching `contracts/*` |
| Long-term project fact changed | `project.md` |
| Submission/integration happened | `notes.md` Submit / Integrate |

**Never overwrite human original requirements.**

---

## Tips

1. **Start with Strict Mode.** Switch to Feature Auto-Loop or Task Auto-Run only after spec/plan is accepted and the feature has clear acceptance criteria.
2. **Keep tasks small.** A task should form a narrow, verifiable loop through the necessary layers.
3. **Record evidence immediately.** Verification output belongs in `notes.md` right after it runs.
4. **Update `project.md` after every feature.** Future agents resume from here.
5. **Suggest Delivery Contracts only when needed.** API, events, public data schemas, UI state/behavior handoffs, SDKs, runtime integrations, or human-requested handoffs may deserve explicit contracts. Simple internal work should skip them.

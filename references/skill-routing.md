# Agent Loop Skill Routing

Use this file when a stage can be improved by another skill or plugin. The `agent-loop` controller stays responsible for state, gates, artifacts, and drift. Other skills are helpers.

Before every mandatory helper-backed stage, run Stage Helper Capability Scan and load `external-skill-adapters.md`. Before falling back in any helper-friendly stage, run the same scan.

## Routing Principle

```text
agent-loop decides the stage
preferred skill improves the stage
fallback guide completes the stage if no preferred skill exists
agent-loop records the result
```

Do not force the human to learn external command systems. Translate every external method into the local `agent-loop` artifacts.

External skill default paths are advisory only. If a preferred skill says to write under its own docs directory, write to the owning `agent-loop` artifact instead.

## Mandatory Helper Resolution Protocol

The mandatory helper-backed stages are Brainstorm / Clarify, Plan Gate / Plan, Execute Task / Story, Diagnose Failure, Verify, Review / Feature Close Review, and approved Subagent Execution.

For each mandatory stage:

1. Identify the required helper from the table below.
2. Check the canonical name first, then the supported alias. Continue to the supported alias when the canonical candidate is absent or `load-failed`; one broken registration must not hide a usable helper.
3. If found, load the complete helper `SKILL.md` before any stage action. Do not rely on remembered content or description metadata.
4. Initial resolution must be recorded before the first stage action. Record candidate results, resolved helper, status, and load evidence in the current feature `notes.md` using `templates/notes.md`; append method, fallback, and artifact evidence before exit.
5. Use the helper method while preserving agent-loop artifacts, gates, status, and lifecycle control.
6. Before stage exit, assert that the resolution record exists.

Fallback is allowed only when resolution status is `unavailable` or `load-failed`. Silently skipping resolution or using fallback after a successful load is a protocol violation.

If no confirmed feature workspace exists, do not create one merely to record helper resolution. Surface a response-local pending record before the first stage action, then backfill it into `notes.md` during the next human-approved artifact write. Label it pending until persisted; do not claim artifact-backed completion.

Resolution status follows this truth table:

- `loaded` requires a non-`none` resolved helper and complete load evidence before the first action; fallback must be `no`. Method-used evidence is required before stage exit, not before the first stage action.
- `unavailable` requires every candidate to be absent and the resolved helper to be `none`.
- `load-failed` requires every discoverable candidate to have a recorded load error, all candidates to have been attempted, and the resolved helper to be `none`.
- Any contradictory record blocks stage action or stage completion until corrected.

| Stage | Canonical name | Supported alias |
|---|---|---|
| Brainstorm / Clarify | `superpowers:brainstorming` | `brainstorming` |
| Plan Gate / Plan If Needed | `superpowers:writing-plans` | `writing-plans` |
| Execute Task / Story | `superpowers:test-driven-development` | `test-driven-development` |
| Diagnose Failure | `superpowers:systematic-debugging` | `systematic-debugging` |
| Verify | `superpowers:verification-before-completion` | `verification-before-completion` |
| Review / Feature Close Review | `superpowers:requesting-code-review` | `requesting-code-review` |
| Subagent Execution If Approved | `superpowers:subagent-driven-development` | `subagent-driven-development` |

An equivalent helper under another runtime namespace may be used only when its capability is verified. Record its actual resolved name and the evidence used to classify it as equivalent.

## Stage Helper Capability Scan

Run this scan at Project Entry and before every helper-friendly stage listed in the Preferred Skills table below, including Pause / Close and approved Subagent execution.

How to scan:

1. Inspect the current runtime's available skills, plugins, or helper capabilities.
2. Match available helpers to the current `agent-loop` stage using the Preferred Skills table below.
3. For mandatory stages, resolve canonical and alias names from the Mandatory Helper Resolution Protocol.
4. Load `external-skill-adapters.md` and the complete resolved helper before stage actions.
5. Keep all outputs in agent-loop artifacts and record Stage Helper Resolution in `notes.md`.
6. If no matching helper is present after all candidates are checked, record `unavailable`; if all discoverable candidates fail to load, record `load-failed`; only then continue with fallback guidance.

Do not ask the human whether to use a helper just because it exists. Announce or otherwise expose helper use when the loaded helper requires it, but do not turn helper selection into a new human gate. Continue to stop for external directories, subagents, commits, PRs, releases, or other agent-loop Human-gated actions.

## Preferred Skills

| Stage | Preferred Skill Type | Fallback |
|---|---|---|
| Brainstorm / Clarify if Needed | brainstorming / product discovery | Ask 1-5 high-impact questions from `stage-guides.md` |
| Product Brief If Needed | PRD/product synthesis, grill-with-docs style helpers | Use `templates/product.md` |
| Feature Spec | spec writing | Use `templates/spec.md` |
| Human Review Summary | approval summary / decision table | Use `human-review-summary.md` |
| Work Breakdown | issue/task splitter | Use `templates/tasks.md` |
| Test Design | test matrix / TDD design | Use `templates/tests.md` |
| E2E Discovery if Web | browser/E2E environment discovery | Use `e2e-discovery.md` |
| Technical Design / Code Context | codebase scan / technical planning | Use `implementation-planning.md` |
| Plan Gate / Plan If Needed | Superpowers-style plan-writing | Use `implementation-planning.md` and `templates/plan.md`; record No-Plan Decision only for trivial tasks |
| Execute Task / Story | test-driven-development | Use RED/GREEN flow in `stage-guides.md` |
| Diagnose Failure | systematic debugging | Reproduce, isolate, hypothesize, verify |
| Verify | verification-before-completion | Run fresh proof and record output |
| Review | requesting-code-review | Record Spec Review for every task; record Standards Review when triggered |
| Feature Close Review | requesting-code-review | Run whole-feature Spec Review and triggered Standards Review before close |
| Feature Completion Check | finishing / verification / close decision support | Use `feature-completion-check.md` |
| Submit / Integrate | finishing-a-development-branch | Use `submit-and-integrate.md` and require human confirmation |
| Pause / Close | finishing/handoff | Use close gate in `runtime.md` |

## Superpowers Mapping

If Superpowers is available, these map cleanly:

- `using-superpowers`: reminder that relevant skills should be loaded before acting.
- `brainstorming`: Brainstorm / Clarify if Needed; translate output to `product.md` or `spec.md`, not `docs/superpowers/specs/`.
- PRD/product skills such as mattpocock `to-prd`: Product Brief If Needed, translated into local `product.md` only after Product Brief Source Gate passes.
- Requirement/Product Grill and mattpocock `grill-with-docs`: Requirements Discussion, Product Brief, and Brainstorm / Clarify clarification; translate output to requirement README, `product.md`, `spec.md`, `notes.md`, or Decision Candidate routing, not native `CONTEXT.md` or `docs/adr/`.
- `writing-plans`: Plan Gate / Plan If Needed; translate into construction-grade `plan.md` or `plans/*`, or record a justified No-Plan Decision for a trivial task, not `docs/superpowers/plans/`.
- `test-driven-development`: Execute Task / Story; evidence still goes to `notes.md` and task status still follows Task Done Gate.
- `systematic-debugging`: Diagnose Failure; root cause and fix evidence go to `notes.md`.
- `verification-before-completion`: Verify and Close; completion still requires agent-loop evidence, review, drift, memory, and human gates.
- `requesting-code-review`: Review; findings go to `notes.md` and cannot directly mark tasks `done`.
- `finishing-a-development-branch`: Submit / Integrate and Close decision support; agent-loop submit/close gates still apply.
- `subagent-driven-development`: for explicitly parallel independent tasks, or bounded large Project Entry Scan lanes when the human confirms; briefs and returns go to `handoffs/*`.

Browser, Chrome, and computer-use tools are execution tools, not assumptions. Use them for Web E2E only after `e2e-discovery.md` has established the app URL, start command, auth/test data, and appropriate automation route.

## Subagent Rule

Subagents are optional. In v1, use them only when:

- the human confirms this specific subagent dispatch
- or the human explicitly confirms one bounded task group after the agent lists task boundaries, subagent briefs, stop conditions, and main-agent review responsibility
- Feature Auto-Loop or Task Auto-Run approval is not subagent approval
- tasks or scan lanes are independent
- each subagent has a bounded task/story or Project Entry Scan lane
- each implementation subagent receives a `templates/subagent-brief.md`-style brief
- Project Entry Scan subagents return findings, evidence, confidence, uncertainties, files read, and suggested `project.md` entries
- outputs can be merged back into `tasks.md`, `tests.md`, `notes.md`, or proposed `project.md`

Default remains one task in the current agent session.

## External Project References

Use external projects as ideas, not as copied workflows:

- OpenSpec: change proposal, drift, archive/close discipline.
- Spec Kit: technical context, source structure, contracts/data-model thinking as auxiliary planning structure.
- Superpowers: skill invocation discipline, construction-grade plans, TDD, debugging, verification.
- mattpocock skills: PRD/product brief, grill-with-docs, vertical slice issues, TDD, diagnose, two-axis review, handoff patterns.
- roadmap-skill: future multiplayer adapter only; no roadmap graph in v1.

## Fallback Rule

When no external skill is available or loading fails:

1. Record requested helper, candidates checked, and `unavailable` or `load-failed` in `notes.md`.
2. Name the fallback source.
3. Load the current stage in `stage-guides.md`.
4. Use the matching template.
5. Ask the human gate.
6. Act.
7. Record output in the owning artifact.
8. Recommend the next stage.

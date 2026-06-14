# Agent Loop Skill Routing

Use this file when a stage can be improved by another skill or plugin. The `agent-loop` controller stays responsible for state, gates, artifacts, and drift. Other skills are helpers.

Before falling back to built-in `agent-loop` stage guidance, run Stage Helper Capability Scan. When an external skill is available for the current stage, also load `external-skill-adapters.md`.

## Routing Principle

```text
agent-loop decides the stage
preferred skill improves the stage
fallback guide completes the stage if no preferred skill exists
agent-loop records the result
```

Do not force the human to learn external command systems. Translate every external method into the local `agent-loop` artifacts.

External skill default paths are advisory only. If a preferred skill says to write under its own docs directory, write to the owning `agent-loop` artifact instead.

## Stage Helper Capability Scan

Run this scan at Project Entry and before helper-friendly stages: Brainstorm / Clarify, Product Brief, Feature Spec, Plan Gate, Execute Task / Story, Diagnose Failure, Verify, Review, Feature Close Review, Submit / Integrate, and approved Subagent execution.

How to scan:

1. Inspect the current runtime's available skills, plugins, or helper capabilities.
2. Match available helpers to the current `agent-loop` stage using the Preferred Skills table below.
3. If Superpowers or another matching helper is present, load `external-skill-adapters.md` before fallback guidance.
4. Prefer the matching helper for method quality, but keep all outputs in agent-loop artifacts.
5. If no matching helper is present or the helper cannot be loaded, record no special state and continue with the fallback guide.

Do not ask the human whether to use a helper just because it exists. Use the helper silently as an implementation method unless it would create new files, external directories, subagents, commits, PRs, releases, or other human-gated actions.

## Preferred Skills

| Stage | Preferred Skill Type | Fallback |
|---|---|---|
| Brainstorm / Clarify if Needed | brainstorming / product discovery | Ask 1-5 high-impact questions from `stage-guides.md` |
| Product Brief If Needed | PRD/product synthesis, grill-with-docs | Use `templates/product.md` |
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
- PRD/product skills such as mattpocock `to-prd`: Product Brief If Needed, translated into local `product.md`.
- `writing-plans`: Plan Gate / Plan If Needed; translate into construction-grade `plan.md` or `plans/*`, or record a justified No-Plan Decision for a trivial task, not `docs/superpowers/plans/`.
- `test-driven-development`: Execute Task / Story; evidence still goes to `notes.md` and task status still follows Task Done Gate.
- `systematic-debugging`: Diagnose Failure; root cause and fix evidence go to `notes.md`.
- `verification-before-completion`: Verify and Close; completion still requires agent-loop evidence, review, drift, memory, and human gates.
- `requesting-code-review`: Review; findings go to `notes.md` and cannot directly mark tasks `done`.
- `finishing-a-development-branch`: Submit / Integrate and Close decision support; agent-loop submit/close gates still apply.
- `subagent-driven-development`: for explicitly parallel independent tasks, or bounded large-project onboarding scans when the human confirms; briefs and returns go to `handoffs/*`.

Browser, Chrome, and computer-use tools are execution tools, not assumptions. Use them for Web E2E only after `e2e-discovery.md` has established the app URL, start command, auth/test data, and appropriate automation route.

## Subagent Rule

Subagents are optional. In v1, use them only when:

- the human confirms this specific subagent dispatch
- or the human explicitly confirms one bounded task group after the agent lists task boundaries, subagent briefs, stop conditions, and main-agent review responsibility
- Feature Auto-Loop or Task Auto-Run approval is not subagent approval
- tasks or scan lanes are independent
- each subagent has a bounded task/story or onboarding scan lane
- each implementation subagent receives a `templates/subagent-brief.md`-style brief
- onboarding scan subagents return findings, evidence, confidence, uncertainties, files read, and suggested `project.md` entries
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

When no external skill is available:

1. Load the current stage in `stage-guides.md`.
2. Use the matching template.
3. Ask the human gate.
4. Act.
5. Record output in the owning artifact.
6. Recommend the next stage.

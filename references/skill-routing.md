# Agent Loop Skill Routing

Use this file when a stage can be improved by another skill or plugin. The `agent-loop` controller stays responsible for state, gates, artifacts, and drift. Other skills are helpers.

## Routing Principle

```text
agent-loop decides the stage
preferred skill improves the stage
fallback guide completes the stage if no preferred skill exists
agent-loop records the result
```

Do not force the human to learn external command systems. Translate every external method into the local `agent-loop` artifacts.

## Preferred Skills

| Stage | Preferred Skill Type | Fallback |
|---|---|---|
| Brainstorm / Clarify | brainstorming / product discovery | Ask 1-5 high-impact questions from `stage-guides.md` |
| Product Brief If Needed | PRD/product synthesis, grill-with-docs | Use `templates/product.md` |
| Feature Spec | spec writing | Use `templates/spec.md` |
| Human Review Summary | approval summary / decision table | Use `human-review-summary.md` |
| Work Breakdown | issue/task splitter | Use `templates/tasks.md` |
| Test Design | test matrix / TDD design | Use `templates/tests.md` |
| E2E Discovery if Web | browser/E2E environment discovery | Use `e2e-discovery.md` |
| Technical Design / Code Context | codebase scan / technical planning | Use `implementation-planning.md` |
| Plan If Needed | Superpowers-style plan-writing | Use `implementation-planning.md` and `templates/plan.md` |
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
- `brainstorming`: Brainstorm / Clarify.
- PRD/product skills such as mattpocock `to-prd`: Product Brief If Needed, translated into local `product.md`.
- `writing-plans`: Plan If Needed; translate into construction-grade `plan.md` with exact paths, code/test snippets, commands, expected output, no placeholders, and self-review.
- `test-driven-development`: Execute Task / Story.
- `systematic-debugging`: Diagnose Failure.
- `verification-before-completion`: Verify and Close.
- `requesting-code-review`: Review.
- `finishing-a-development-branch`: Submit / Integrate and Close decision support.
- `subagent-driven-development`: for explicitly parallel independent tasks, or bounded large-project onboarding scans when the human confirms.

Browser, Chrome, and computer-use tools are execution tools, not assumptions. Use them for Web E2E only after `e2e-discovery.md` has established the app URL, start command, auth/test data, and appropriate automation route.

## Subagent Rule

Subagents are optional. In v1, use them only when:

- the human confirms subagent use
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

# Project-Local Skills Implementation Plan

> **Execution method:** use `writing-skills` for RED/GREEN/REFACTOR and apply the Agent Loop maintainer rules in this repository. Do not create target-project `.agent-loop/` artifacts here.

**Goal:** Add a Human-gated project-local skill creation, loading, lifecycle, and per-invocation execution-confirmation capability for downstream Agent Loop projects.

**Architecture:** `.agent-loop/skills/INDEX.md` is the downstream lifecycle and discovery index; each skill owns a standard `<skill-name>/SKILL.md` package. Agent Loop adds a `project-skill-management` intent and `Project Skill Creation / Update` stage, uses `writing-skills` plus optional `skill-creator`, activates only verified skills, and requires an Execution Gate for every invocation.

**Tech stack:** Markdown runtime rules and templates, Bash contract tests, Ruby YAML/fence checks.

---

## Task 1: Preserve RED evidence

**Files:**

- Create: `tests/validate-project-local-skills.sh`
- Create: `docs/reports/project-local-skills-red-baseline-2026-07-11.md`

- [x] Run three isolated subagent scenarios without the new runtime rules.
- [x] Record exact path, helper precedence, proactive candidate, lifecycle, and execution authorization gaps.
- [x] Run `bash tests/validate-project-local-skills.sh` and verify it fails only because Project-Local Skills behavior is absent.

Expected RED: missing `references/project-skills.md`, templates, intent, stage, root guidance, docs, and validation assertions.

## Task 2: Add the owning reference and downstream templates

**Files:**

- Create: `references/project-skills.md`
- Create: `templates/project-skills/INDEX.md`
- Create: `templates/project-skills/SKILL.md`
- Create: `templates/project-skills/validation.md`

- [x] Define explicit human creation/update triggers and proactive candidate signals.
- [x] Define Gate 1 before directory creation or material update.
- [x] Define `proposed -> active` automatic transition only after RED/GREEN/REFACTOR and validation.
- [x] Define `proposed | active | disabled | deprecated` and `bootstrap | on-demand` semantics.
- [x] Define the per-invocation Execution Gate and non-reusable authorization scope.
- [x] Define `writing-skills` as the authoring discipline and `skill-creator` as concurrent scaffold/validation support.
- [x] Define canonical path override to `<target-project>/.agent-loop/skills/<skill-name>/`.
- [x] Provide templates with only supported `SKILL.md` frontmatter fields.

Run: `bash tests/validate-project-local-skills.sh`

Expected intermediate result: reference/template assertions pass; controller/document assertions remain RED.

## Task 3: Integrate controller, intent, routing, and stage rules

**Files:**

- Modify: `SKILL.md`
- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Modify: `references/skill-routing.md`
- Modify: `references/external-skill-adapters.md`
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`

- [x] Add `project-skill-management` intent and route only after reliable Project Entry/memory.
- [x] Add Project Skill Creation / Update to canonical navigation without creating a feature workspace.
- [x] Scan `.agent-loop/skills/INDEX.md` during Project Entry, Resume, Re-Adopt, and controller re-entry.
- [x] Load only `active` skills and separate discovery/loading from execution authorization.
- [x] Prevent Feature Auto-Loop, Task Auto-Run, prior success, `active`, or `bootstrap` from authorizing execution.
- [x] Keep controller paths, Human Gates, lifecycle, submit, close, and project memory authoritative.

Run: `bash tests/validate-project-local-skills.sh`

Expected intermediate result: core runtime assertions pass; root guidance and human docs remain RED.

## Task 4: Integrate root guidance and project memory

**Files:**

- Modify: `templates/root-AGENTS.md`
- Modify: `templates/project.md`
- Modify: `references/project-guidance.md`
- Review: `scripts/check-root-agents-blocks.sh`
- Modify affected root guidance tests.

- [x] Add project skill index discovery to Bootstrap Protocol.
- [x] Add message intent and Stage Map entry.
- [x] Add Gate 1 and Execution Gate to required stops/gate guidance.
- [x] Update every root managed block revision to `1.2.4-20260711.3`.
- [x] Add Project Skills status/index fields to project memory.
- [x] Preserve root guidance as navigation only; detailed rules stay in `references/project-skills.md`.

Run:

```bash
bash tests/validate-project-local-skills.sh
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-root-agents-block-refresh.sh
bash tests/validate-v1.2.4-root-stage-coverage.sh
```

Expected: all four commands pass after affected test contracts are updated.

## Task 5: Synchronize human docs and semantic scenarios

**Files:**

- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`
- Modify: `references/validation-scenarios.md`

- [x] Document explicit “把这个流程做成技能” usage.
- [x] Document Agent-proposed candidates after verified complex flows.
- [x] Explain project-local vs global skill locations.
- [x] Explain Gate 1, automatic verified activation, and per-invocation Execution Gate.
- [x] Add an `Unreleased` changelog section without changing version-bearing files.
- [x] Add pressure scenarios for helper coexistence, offline human, active/bootstrap, stale auto grants, failed validation, and invocation-scope expansion.

Run: `bash tests/validate-project-local-skills.sh`

Expected GREEN: `PASS: project-local skills creation, activation, loading, and execution gates are complete`.

## Task 6: Re-run feature-scoped behavioral validation

**Files:**

- Create/update: `docs/reports/project-local-skills-feature-validation-2026-07-11.md` using `docs/maintenance/feature-validation-method.md`.

- [x] Re-run the three RED scenarios with the new runtime rules.
- [x] Capture any new rationalizations and patch rules/tests before continuing.
- [x] Run Project-Local Skills and directly affected regression tests; full-repository tests are not part of the feature score.
- [x] Parse `SKILL.md` YAML and `plugin.json` JSON.
- [x] Run Shell syntax, Markdown fence, and `git diff --check` checks.
- [x] Record the human decision to defer a fresh six-domain full-validation report and use the standalone feature score without claiming it replaces mandatory full validation.
- [x] Confirm no target-project `.agent-loop/skills/` exists in this source repository.
- [x] Report unrelated user-owned proposal moves separately and do not stage or revert them.

No commit, push, version bump, stable branch, or tag action is authorized by this plan.

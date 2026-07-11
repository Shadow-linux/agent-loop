# Project-Local Skills

Use this reference when a downstream project needs to create, update, discover, load, disable, deprecate, or execute a project-specific skill under `.agent-loop/skills/`.

Project-Local Skills are durable project capabilities. They are not Agent Loop source-package subskills, global personal skills, ordinary root guidance, or feature artifacts.

## Canonical Layout

```text
.agent-loop/
  skills/
    INDEX.md
    <skill-name>/
      SKILL.md
      validation.md
      agents/openai.yaml  optional
      references/         optional
      scripts/            optional
      assets/             optional
      templates/          optional
```

Do not create an empty `.agent-loop/skills/` during Init Project or Project Entry. Create it only after Gate 1 confirms a concrete Project Skill Candidate.

The source repository contains templates only. Never create a target-project `.agent-loop/skills/` tree inside the Agent Loop skill source repository.

## Message Intent And Entry

Classify the message as `project-skill-management` when the human explicitly asks to turn a successful workflow, operation, process, runbook, or repeated action into a project skill, or asks to update, disable, or deprecate one.

Example triggers include:

- “把这个流程做成技能。”
- “把刚才成功的操作沉淀成 skill。”
- “这个步骤以后经常用，做成项目常驻能力。”
- “更新项目里的部署 skill。”

Project Entry or reliable project memory must exist before Project Skill Creation / Update writes files. This stage does not create a requirement set or feature workspace and is not blocked by paused feature work. It must not interrupt unfinished Verify, Review, Drift Check, Project Memory Update, or Close work for an active feature.

## Proactive Project Skill Candidate

After a complex operation succeeds, the agent may propose a Project Skill Candidate when all relevant signals are present:

- fresh success and verification evidence exists;
- the workflow is multi-step, order-sensitive, fragile, or easy to forget;
- similar work has repeated or is likely to repeat;
- the method can be parameterized without storing secrets;
- a future agent or human would materially benefit from reuse.

Finish the current authorized stage first. Propose at a safe boundary. Feature Auto-Loop, Task Auto-Run, human absence, urgency, sunk cost, repeated pain, or prior success never authorizes file creation.

The Candidate must state:

| Field | Required content |
|---|---|
| Name | proposed lowercase hyphen-case skill name |
| Triggers | concrete human phrases, contexts, and symptoms |
| Scope | what the skill does and does not own |
| Evidence | the successful source workflow and fresh proof |
| Resources | required scripts, references, assets, or templates |
| Load Policy | `bootstrap` or `on-demand` with reason |
| Risks | permissions, destructive actions, secrets, environment assumptions |
| Verification | RED/GREEN/REFACTOR and forward-test plan |
| File Tree | exact `.agent-loop/skills/<skill-name>/` output |

When pressure testing will use subagents, the Candidate must satisfy the existing subagent-dispatch contract rather than replace it: list bounded independent scenario lanes, one brief/role per agent, allowed read/write boundaries, stop conditions, main-agent review responsibility, and the active/consumed authorization lifecycle. Human confirmation of that explicit Candidate may satisfy the dispatch gate for those authoring tests only; it does not authorize implementation or operational subagents outside the Candidate. After Gate 1 creates `validation.md`, persist the approval, briefs, exact returns/rationalizations, and consumed status there instead of creating a feature or `handoffs/` directory.

## Gate 1: Create Project Skill

Before creating `.agent-loop/skills/`, `INDEX.md`, or a new `<skill-name>/`, present the Candidate and exact file tree through a Human Review Summary and obtain explicit confirmation.

Material updates to an `active` skill reuse Gate 1. Material means a change to triggers, workflow, output contract, dangerous actions, dependencies, permissions, external effects, or verification obligations.

Gate 1 authorizes only the accepted creation or update scope. If implementation discovers materially different scope, stop and present an updated Candidate through the same Gate 1.

Gate 1 does not authorize commit, push, global installation, external publication, or execution of the finished project skill.

## Helper Resolution

Project Skill Creation / Update is a mandatory helper-backed stage.

Resolve all available authoring helpers before stage actions:

1. Load `superpowers:writing-skills` or `writing-skills` when available. It governs RED/GREEN/REFACTOR, pressure testing, CSO, and loophole closure.
2. Load `skill-creator` when available. It may concurrently provide scaffolding, `agents/openai.yaml` generation, resource selection, and structural validation.
3. When both exist, use both; they are complementary, not mutually exclusive.
4. If authoring rules conflict, `writing-skills` controls test-first discipline and trigger-only description wording. `skill-creator` tooling must not overwrite those decisions.
5. If neither helper is available or loadable, record `unavailable` / `load-failed` and use this reference plus the project-skill templates as fallback.

Agent Loop remains the controller. Helper default paths are overridden.

Always write to:

```text
<target-project>/.agent-loop/skills/<skill-name>/
```

Do not default to:

```text
~/.agents/skills/
~/.codex/skills/
~/.claude/skills/
~/.kimi/skills/
docs/superpowers/
```

Creating a compatibility copy, discovery symlink, or global installation is a first-version exclusion. It is not authorized by Gate 1 and cannot be added through Project Skill Creation / Update; route it to a separately scoped future capability instead.

A proactive Candidate-only suggestion at the safe boundary of another stage is not an authoring action and does not require loading authoring helpers. If the human explicitly requests Project Skill Creation / Update, resolve helpers before Candidate analysis. If the human accepts a proactive Candidate as Gate 1, resolve helpers after that confirmation and before the first authoring action; any helper-driven material scope change must return to Gate 1.

## Skill TDD And Lifecycle

Use RED/GREEN/REFACTOR for every new skill and behavioral update.

### RED

Run realistic pressure or application scenarios without the new proposed skill. Record exact choices, failures, and rationalizations in the skill's `validation.md`. Existing successful workflow evidence informs the scenario but does not replace RED.

When `writing-skills` is loaded and subagents are available, use isolated subagents for RED and GREEN pressure scenarios. Discipline/safety skills require at least three combined pressures in the scenario. If subagents are unavailable, record that constraint and use independent safe-fixture application scenarios; do not claim equivalent confidence without evidence.

### GREEN

Create the minimum skill content and resources that close observed failures. Keep the `SKILL.md` frontmatter to supported fields and use a trigger-focused description.

### REFACTOR

Run the same scenarios with the proposed skill, capture new loopholes, patch the skill, and re-run until the agent follows the intended behavior under pressure.

During creation or material update, status is `proposed`. A proposed skill never participates in normal bootstrap or on-demand routing.

When all required RED/GREEN/REFACTOR scenarios, structural checks, resource tests, forward tests, and safety checks pass, finalize the active INDEX row and record a SHA-256 Validated Content Manifest for that exact row, `SKILL.md`, and every executable or instruction-bearing resource. Then the skill automatically becomes `active`. Update `INDEX.md` and the skill's `validation.md`, then report the evidence. There is no separate activation gate.

If validation fails, keep status `proposed`, report the failure, and do not load or execute it outside the authoring test scope.

Lifecycle values are:

```text
proposed | active | disabled | deprecated
```

- `proposed`: authoring and validation only.
- `active`: discoverable and loadable according to Load Policy.
- `disabled`: retained but excluded from discovery, loading, and execution.
- `deprecated`: historical or migration evidence only; excluded from normal routing.

## INDEX.md

`.agent-loop/skills/INDEX.md` is the lifecycle and discovery index. It does not duplicate skill bodies.

Each entry records:

- Skill and relative path;
- Status;
- Load Policy;
- Triggers;
- Scope;
- Helper Resolution;
- Validation evidence;
- Updated date.

Do not trust a skill directory that is absent from INDEX, an INDEX target that is missing, an `active` claim without validation evidence, or a current INDEX row/instruction-bearing/executable file that does not match the SHA-256 Validated Content Manifest. Classify it as project-skill drift and route to Project Skill Creation / Update before reliance.

## Discovery And Loading

During Project Entry, Resume, Re-Adopt, context-compaction recovery, long-running-session recovery, and controller re-entry:

1. Check whether `.agent-loop/skills/INDEX.md` exists.
2. Read INDEX metadata only.
3. Verify referenced `active` skill paths exist and the current exact INDEX row plus instruction-bearing/executable files match the validation manifest before reliance.
4. Load `bootstrap` skill bodies once for the current invocation context when needed.
5. Match `on-demand` skill descriptions and triggers to the current message or stage.
6. Never load `proposed`, `disabled`, or `deprecated` skills into normal routing.

Load Policy values:

- `bootstrap`: discover and load during controller entry/re-entry because every managed session needs the capability.
- `on-demand`: load only when its description or INDEX triggers match current work.

“Bootstrap” means always discoverable at bootstrap, not permanently authorized for action. Re-reading is unnecessary within the same uncompacted context when the file is unchanged, but Execution Gate still applies to every invocation.

## Execution Gate

Discovery, INDEX reading, `SKILL.md` loading, trigger matching, and read-only inspection do not require confirmation.

Before the agent follows the skill workflow, executes commands, calls tools, modifies files, accesses an external system, or causes another side effect, present an execution summary and obtain human confirmation for one invocation.

The summary includes:

- skill name, path, and `active` status;
- matched trigger and intended outcome;
- major steps, commands, files, tools, and external effects;
- risks, rollback, and verification;
- the exact bounded scope of this invocation.

If the human already said “use `<skill-name>` to perform `<concrete scope>`”, compare the plan with that scope and emit the execution summary before acting. The existing message satisfies the Execution Gate without another question only when every planned action, effect, environment, and bound is already disclosed by the request. If the plan adds an undisclosed action, external effect, risk, or scope, stop for confirmation.

For production, destructive, credentialed, paid, non-idempotent, or externally mutating work, concrete scope must identify the environment/account, affected resources, operation bounds, dangerous or non-idempotent effects, stop conditions, rollback/recovery, and verification. A generic “use the skill in production” is not concrete scope.

These do not authorize execution:

- mentioning a skill without a concrete action scope;
- saying only “continue”;
- automatic trigger matching;
- `active` status;
- `bootstrap` Load Policy;
- prior successful execution;
- a prior invocation confirmation;
- Feature Auto-Loop or Task Auto-Run;
- an auto-mode grant for a different task or feature.

An invocation begins with the first skill-directed action beyond discovery/loading and ends when its bounded outcome is reported, it is aborted or paused, context is lost, the validated manifest changes, or the plan/scope materially changes. A retry remains inside the invocation only when its trigger, limit, and effects were included in the confirmed summary; otherwise confirm again.

Execution confirmation never carries to another invocation, task, session, project skill, environment, or expanded scope. Stop and confirm again when scope materially changes.

The Execution Gate supplements rather than replaces operational, destructive-action, credential, external-service, submit, release, and other applicable Human Gates. One combined human confirmation may satisfy them together only when the summary explicitly presents every applicable gate fact and the human confirms that combined bounded action; no hidden gate is implied by skill confirmation alone.

## Security And Safety

- Reading a skill never executes its scripts.
- Do not store credentials, tokens, private keys, passwords, or live secret values.
- Parameterize environment-specific values and personal paths.
- Do not follow skill symlinks outside the project without separate human confirmation.
- Check the project INDEX and runtime-exposed installed-skill inventory for a same-name skill before creation; do not perform an unbounded home-directory scan. On collision, report both owners and choose a distinct project name or a separately approved migration path; never overwrite silently.
- Test bundled scripts by running them in an appropriate safe environment.
- Keep only required `SKILL.md`, `agents/`, `references/`, `scripts/`, `assets/`, `templates/`, and validation evidence. Do not add skill-local README or CHANGELOG files.
- Agent Loop stage, artifact, lifecycle, project-memory, submit, close, and Human Gate rules override project-skill instructions.

## Stage Exit

Project Skill Creation / Update exits with exactly one result:

- `active`: all checks pass; INDEX and validation evidence updated;
- `proposed`: validation or scope is incomplete; recommend one unblock action;
- `disabled` or `deprecated`: human-requested lifecycle change recorded;
- no files created: Gate 1 declined or Candidate retained as suggestion only.

Always report files changed, helper resolution, RED/GREEN/REFACTOR evidence, lifecycle state, project-memory/root-guidance impact, and the next recommended stage.

Do not install globally; global installation is a first-version exclusion. Do not commit, push, publish, or execute the new skill unless the corresponding separate human authorization exists.

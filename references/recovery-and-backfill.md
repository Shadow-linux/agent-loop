# Recovery And Backfill

Use this file when `agent-loop` memory is stale, incomplete, or when a feature must continue from code that already exists. For an existing codebase with no `agent-loop` memory at all, route to Existing Project Onboarding first and use this protocol only when onboarding discovers backfill work.

## Core Rule

For recovery and backfill:

```text
code reality = current fact base
human requirements = original intent
agent docs   = working memory to repair
```

Code reality can correct `agent-loop` documents after human confirmation. It must not silently override human-provided requirements or prototypes.

## When To Use

Use this protocol when:

- Existing Project Onboarding finds code reality that should be backfilled into newly proposed `agent-loop` memory
- `agent-loop/project.md` is stale
- the project used `agent-loop` before, but recent development happened without updating `agent-loop`
- the human says "re-adopt", "re-take-over", "re-sync", "重新托管", "重新接管", "回补 agent-loop", or similar
- a feature was partly built but docs are incomplete
- tasks are marked wrong relative to code
- tests exist but `tests.md` does not know them
- implementation behavior differs from `spec.md`
- the human asks to continue an old project or old feature

## Re-Adopt Agent Loop Project

Use this when `agent-loop/` exists but a period of development happened outside the loop.

Do not start new feature work first. The agent should:

1. Read `agent-loop/project.md` and active or paused feature docs. If `project.md` says `Memory Mode: enterprise`, read only the relevant linked `agent-loop/project/*.md` files.
2. Inspect current code reality only as needed: README, scripts, tests, obvious changed areas, entry points, and relevant recent feature files.
3. Compare current code/tests/scripts against `project.md`, `spec.md`, `tasks.md`, `tests.md`, `plan.md`, and `notes.md`.
4. Produce the Compare Matrix.
5. Propose backfill grouped by target file.
6. Ask human confirmation before changing any `agent-loop` docs.
7. After backfill, recommend exactly one next stage: continue old feature, run verification, close completed feature, pause, or start a new feature.

If code behavior contradicts original human requirements, stop and ask whether to keep code, change code, or update scope. Never rewrite original requirement files.

Minimum reconciliation cannot be bypassed. If the human asks to skip old-document cleanup, do only the smallest recovery needed for safe continuation:

- current install/build/test command reality
- current test-system map and known baseline failures
- Active Feature and Paused Features truth
- affected code boundaries for the next requested feature
- known code-vs-doc conflicts that could change the next task
- whether project memory mode should remain simple or be recommended as enterprise

Only after these are trustworthy enough may the agent continue to a new feature or targeted feature scan.

## Recovery Scan

Scan only enough to recover useful state:

- README, AGENTS/CLAUDE/GEMINI, package scripts
- app entry points and package/workspace layout
- obvious feature files and routes
- relevant tests
- recent implementation files for the target feature
- existing `agent-loop` artifacts if any

Do not perform a whole-repo deep audit unless the human asks or the project memory is unusable.

For large or stale re-adoption, recommend bounded subagent scan when available and human-confirmed. Useful scan lanes include commands/tests, recent outside-loop features, durable boundaries, and guidance files. Subagents may return findings, evidence, confidence, uncertainties, files read, and suggested entries only; the main agent owns synthesis and writes.

## Compare Matrix

Create a short comparison before writing:

```text
Observed code reality:
Existing agent-loop docs:
Original human requirements:
Mismatch:
Risk:
Recommended backfill:
Needs human decision:
```

## Backfill Targets

Use this routing:

```text
long-term project fact -> project.md in simple mode, or matching project/*.md file in enterprise mode
current feature behavior -> spec.md
task status/order/scope -> tasks.md
test reality/commands/cases -> tests.md
active execution unit -> plan.md
evidence/history/decisions/conflicts -> notes.md
new human material -> requirements/<archive-date>-<topic>/
```

Never edit original requirement files to make them match code. Add a new requirement-set file or record a conflict in `notes.md`.

## Conflict Classes

### Code Ahead Of Docs

Code implements behavior not recorded in docs.

Action:

- propose `spec.md`, `tasks.md`, `tests.md`, `project.md`, and/or enterprise `project/*.md` backfill
- record evidence in `notes.md`
- ask human confirmation

### Docs Ahead Of Code

Docs describe behavior not implemented.

Action:

- mark related tasks as `todo` or `blocked`
- recommend Work Breakdown, Plan, or Execute
- do not pretend the feature is complete

### Code Conflicts With Human Requirements

Implementation contradicts original requirement/prototype.

Action:

- do not silently update spec to match code
- record conflict in `notes.md`
- ask human to choose: keep code, change code, or change scope

### Tests Conflict With Claimed Status

Tasks say done but verification is missing or failing.

Action:

- move task to `review` or `blocked`
- add verification gap to `notes.md`
- route to Verify or Diagnose Failure

### Baseline Failure Outside Current Scope

Existing project tests fail before the current feature or recovery work.

Action:

- record the baseline command, failure summary, evidence, and confidence in `notes.md` or `project.md` Testing
- decide whether the failure blocks the requested feature by checking affected boundaries
- do not claim the feature caused or fixed unrelated baseline failures without evidence
- if the baseline failure blocks verification, ask whether to fix it first, mark the task blocked, or use a recorded substitute verification

## Backfill Gate

Before changing docs, present:

- what code reality shows
- what docs currently say
- which files will be updated
- whether this changes feature behavior or long-term project facts
- what human confirmation is needed

After changing docs, record:

- files changed
- evidence used
- remaining uncertainty
- next suggested action

## Close Safety

Recovered or backfilled features cannot close until:

- tasks and code reality match
- tests or substitute verification are recorded
- drift conflicts are resolved or explicitly accepted
- project-level facts are updated when long-term behavior changed
- human confirms close

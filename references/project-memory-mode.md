# Project Memory Mode

Use this file when deciding how much long-term project memory belongs in `agent-loop/project.md`.

## Core Rule

There are only two project memory modes:

```text
simple
enterprise
```

Default to `simple`.

Do not create enterprise memory files just because the project is important. Recommend `enterprise` only when `project.md` is no longer a fast, readable, reliable long-term memory document.

Mode changes require human confirmation.

If a hard trigger applies and the human declines or defers enterprise mode, record the recommendation, trigger evidence, and risk in `project.md` or feature `notes.md`, then continue with the smallest safe project-memory update needed for the current work. Do not block a clear feature solely because enterprise memory was deferred.

## Simple Mode

`project.md` is the main long-term project memory body.

Use simple mode when:

- project boundaries are few and readable
- commands, tech stack, product context, domain language, capabilities, environments, and test strategy fit clearly in one file
- future agents can read `project.md` quickly and know where to continue
- directory-level `AGENTS.md` files are absent or rare

Recommended layout:

```text
agent-loop/
  project.md
  requirements/
  features/
```

## Enterprise Mode

`project.md` becomes the index, current-state summary, and reading router. Long-term project knowledge moves into optional files under `agent-loop/project/`.

Recommended layout:

```text
agent-loop/
  project.md
  project/
    architecture.md
    boundaries.md
    commands.md
    capabilities.md
    product-context.md
    domain-language.md
    testing.md
    environments.md
    guidance-inventory.md
  requirements/
  features/
```

These files are optional. Create only the files that solve a real navigation or continuity problem.

## Hard Triggers

If any hard trigger is true, recommend enterprise mode and ask the human to confirm.

| Trigger | Why it matters |
|---|---|
| about `200k+ LOC` | single-file project memory becomes hard to keep readable |
| `5+` durable boundaries | app/package/service/domain/test/data/security rules need routing |
| `2+` test systems | testing strategy usually needs its own stable context |
| `3+` execution environments | local/remote/container/CI/staging/runtime facts split easily |
| `project.md` is above about `600` lines | the file is no longer a quick entry document |
| agents repeatedly re-scan the same project areas | memory is not navigable enough |
| `5+` directory-level guidance files | project knowledge has already become distributed |

## Soft Triggers

If three or more soft triggers are true, recommend enterprise mode and ask the human to confirm.

- multiple tech stacks: web, backend, mobile, jobs, plugins, workers
- multiple data boundaries: database, cache, search, queue, storage, analytics
- multiple permission, tenant, billing, auth, or security rules
- multiple product domains or bounded contexts
- features often cross several boundaries
- test commands differ by package, service, or CI job
- E2E requires seed data, accounts, containers, external services, or special cleanup
- project docs already have many entry points such as README, docs, AGENTS, CLAUDE, wiki, or runbooks
- `project.md` has started accumulating long repeated lists, transcripts, or large capability inventories

## Switch Timing

Check memory mode during:

- Init Project
- Existing Project Onboarding
- Re-Adopt Agent Loop Project
- Drift Check when long-term facts changed
- Project Memory Update
- Close Feature when the feature introduced new durable boundaries

Do not interrupt a small active task only to restructure memory. Recommend the switch at the next human gate.

## Switch Procedure

Before switching:

1. Load `human-review-summary.md`.
2. Present trigger evidence as a table.
3. Show proposed files under `agent-loop/project/`.
4. Show which `project.md` sections will move to which files.
5. Ask human confirmation.

After confirmation:

1. Create only the needed `agent-loop/project/*.md` files.
2. Move detailed long-term content out of `project.md`.
3. Keep `project.md` as an index, current work summary, and routing guide.
4. Update root `AGENTS.md` only if future agents need a new startup rule.
5. Record the memory mode change in `project.md` and, if feature-related, in the feature `notes.md`.

Do not delete detail from `project.md` until the target file exists and is linked from the index.

## Enterprise Read Routing

In enterprise mode, always read:

```text
agent-loop/project.md
```

Read detail files only when needed:

| Need | Read |
|---|---|
| architecture, dependency direction, cross-boundary change | `project/architecture.md` |
| project shape, language/framework adapter, DDD intensity | `project/architecture.md` |
| locating code ownership or durable directories | `project/boundaries.md` |
| build, lint, typecheck, test, seed, dev server | `project/commands.md` |
| existing behavior and implemented product areas | `project/capabilities.md` |
| product rules, positioning, durable scope | `project/product-context.md` |
| terms, roles, canonical business language | `project/domain-language.md` |
| unit/API/E2E/contract/job strategy | `project/testing.md` |
| local, remote, container, CI, staging, external services | `project/environments.md` |
| root and directory-level AGENTS/CLAUDE inventory | `project/guidance-inventory.md` |

## Backfill Routing

In simple mode, long-term facts usually go to `project.md`.

In enterprise mode:

| Fact | Write |
|---|---|
| current active/paused work and next action | `project.md` |
| memory mode and index | `project.md` |
| architecture or dependency direction | `project/architecture.md` |
| project shape, language/framework adapter, DDD intensity | `project/architecture.md` |
| durable directory, app, package, service, domain boundary | `project/boundaries.md` |
| stable command or script | `project/commands.md` |
| implemented capability | `project/capabilities.md` |
| durable product rule or cross-feature scope | `project/product-context.md` |
| durable business term | `project/domain-language.md` |
| stable test strategy or E2E environment | `project/testing.md` |
| remote/local/container/CI/runtime fact | `project/environments.md` |
| root or directory guidance status | `project/guidance-inventory.md` |

Every write still needs the usual human gate unless an accepted auto mode explicitly covers that project-memory update and no stop condition applies.

## `project.md` Enterprise Index

In enterprise mode, `project.md` should stay short:

```text
Project Summary
Memory Mode: enterprise
Current Work
Next Suggested Action
Project Memory Index
Recent Project Memory Updates
Open Uncertainties
```

Avoid turning `project.md` back into the whole project encyclopedia.

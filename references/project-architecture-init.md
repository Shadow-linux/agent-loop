# Project Architecture Init

Use this file when initializing a new project, onboarding an existing project, proposing code layout, recording architecture profile, or creating durable code boundaries.

## Core Rule

Agent-loop uses a DDD-inspired architecture mindset, but directory structures are recommendations, not mandates.

```text
governance scaffold = relatively stable
code scaffold = project-shape + language + framework adapter
```

Do not force every language or framework into one directory template.

## DDD-Inspired Defaults

Use these as the default design principles:

- domain language first
- bounded contexts for durable business areas
- business rules stay out of UI glue, controllers, routes, and framework wiring
- application/use-case layer orchestrates behavior
- infrastructure adapters hide databases, queues, external APIs, filesystems, and vendors
- interfaces/controllers translate transport details into use cases
- tests follow behavior boundaries: domain, application/API, integration/E2E where relevant

This is not heavy DDD by default. Choose the lightest shape that preserves business boundaries.

## Project Shape Profiles

Classify the project shape before proposing structure:

| Shape | Typical focus | Architecture emphasis |
|---|---|---|
| frontend | routes, screens, features, UI state, API clients | feature boundaries, domain models, application hooks/use cases |
| backend | API, domain rules, persistence, auth, jobs | domain/application/infrastructure/interfaces |
| fullstack | web + API + shared domain/contracts | apps + packages/services + E2E |
| worker | jobs, queues, schedulers, integrations | application jobs + domain rules + infrastructure adapters |
| cli/library | commands, public API, reusable core | domain/core + adapters + integration tests |

Record the chosen shape in `project.md` or enterprise `project/architecture.md`.

## DDD Intensity

Use three intensities:

| Intensity | Use when | Rule |
|---|---|---|
| light | small app, CRUD tool, prototype, low domain complexity | keep directories simple; use domain language and avoid business rules in UI/controllers |
| standard | normal product backend/fullstack app | separate domain, application/use-cases, infrastructure, interfaces where framework allows |
| enterprise | large project, many bounded contexts, regulated/security/data-heavy domains | record bounded context map and boundary rules; use enterprise Project Memory Mode when triggered |

Intensity is advisory. Ask before creating or refactoring directories.

## Governance Scaffold

These are relatively stable across stacks:

```text
AGENTS.md
CLAUDE.md
.agent-loop/
docs/ optional
scripts/ optional
deploy/ or infra/ optional
tests/ optional top-level for cross-app or E2E tests
```

Only create optional directories when useful. Do not create empty folder hierarchies just to satisfy a template.

## Language And Framework Adapters

Use framework conventions first, then apply DDD boundaries inside or around them.

### Frontend / TypeScript

Common reference:

```text
src/app or src/routes
src/features/<feature>/
src/domain/
src/application/
src/infrastructure/
src/components/
tests/e2e/
```

For Next.js, respect `app/` or `pages/` routing conventions. Keep UI components close to features unless shared.

### Node / TypeScript Backend

NestJS-style reference:

```text
src/modules/<context>/
src/domain/
src/application/
src/infrastructure/
src/interfaces/
test/
```

Express/Fastify can use the same boundaries without forcing Nest module names.

### Java Backend

Spring Boot reference:

```text
src/main/java/<base>/
  domain/
  application/
  infrastructure/
  interfaces/
src/test/java/<base>/
```

For multi-module projects, map bounded contexts to modules or packages.

### Python Backend

FastAPI/Flask reference:

```text
app/
  api/
  domain/
  application/
  infrastructure/
tests/
```

Django reference:

```text
apps/<bounded_context>/
  models.py
  services.py
  selectors.py
  infrastructure/
  tests/
```

For Django, respect app conventions; do not force a generic `domain/` tree if it fights the framework.

### Go Backend

Reference:

```text
cmd/<service>/
internal/domain/
internal/application/
internal/infrastructure/
internal/interfaces/
api/
migrations/
```

Use `internal/` for non-public application code. Avoid a broad `pkg/` unless it is truly reusable.

### C# Backend

ASP.NET Core reference:

```text
src/
  <Product>.Api/
  <Product>.Application/
  <Product>.Domain/
  <Product>.Infrastructure/
tests/
```

Use projects/assemblies as boundaries when the solution is already split.

### Rust Backend / CLI

Reference:

```text
crates/
  domain/
  application/
  infrastructure/
  api/
src/
tests/
```

For smaller Rust apps, keep modules inside one crate and record the intended boundaries.

### C++ Backend / Library

Reference:

```text
include/
src/
tests/
apps/
libs/
cmake/
```

For larger C++ systems:

```text
libs/<bounded-context>/
  include/
  src/
  tests/
apps/<service>/
```

Keep domain/core logic independent from transport, persistence, and vendor adapters where practical.

## Init Behavior

For new projects:

1. Identify project shape, language, framework, runtime, and expected test layers.
2. Recommend a DDD intensity.
3. Recommend a reference layout and explain which parts are optional.
4. Ask human confirmation before creating directories.
5. Record the accepted architecture profile in `project.md` or enterprise `project/architecture.md`.

For existing projects:

1. Identify actual structure and conventions.
2. Map existing directories to DDD-inspired roles when possible.
3. Record reality with evidence and confidence.
4. Do not rename or move directories unless the human explicitly asks for architecture migration.

For remote projects, record where architecture facts were observed and whether local files are only a shadow.

## Human Review Summary

When proposing architecture or scaffold, present:

| Item | Recommendation | Reason | Adjustable? | Human Decision |
|---|---|---|---|---|
| Project Shape | frontend / backend / fullstack / worker / cli-library |  | yes | approve / revise |
| Language Adapter | java / python / node-ts / go / csharp / rust / cpp |  | yes | approve / revise |
| Framework Adapter | spring-boot / fastapi / django / nestjs / express / aspnet-core / rails / laravel / none |  | yes | approve / revise |
| DDD Intensity | light / standard / enterprise |  | yes | approve / revise |
| Proposed Layout | paths |  | yes | approve / revise |
| Test Layout | paths and commands |  | yes | approve / revise |

Emphasize that the proposed layout is a starting point, not a permanent constraint.

## Stop Conditions

Stop and ask when:

- framework conventions conflict with the proposed DDD layout
- the project is an existing codebase and the change would move or rename code
- multiple architecture styles are already present
- bounded contexts are unclear
- security, data, plugin, runtime, or deployment boundaries would be created
- the human has not approved scaffold creation

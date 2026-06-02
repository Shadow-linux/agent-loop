# Implementation Planning

Use this file when a selected task/story needs `plan.md` or a dated plan cycle under `plans/`.

## Planning Model

```text
tasks.md        = work ledger: what to do, order, dependencies, acceptance, verification hint
task-detail.md  = engineering boundary: files, existing APIs, call chain, data flow, interfaces
plan.md         = construction plan: exact steps, code/test snippets, commands, expected outputs
```

Do not put construction-level code snippets in `tasks.md`. Put them in `plan.md` or the dated plan file referenced by `plan.md`.

## Primary Inspiration

Main source: Superpowers `writing-plans`.

Absorb these rules:

- assume the executor has near-zero context for this codebase
- exact file paths always
- map file structure before steps
- define interfaces before implementation
- steps are bite-sized actions, usually 2-5 minutes
- test steps show actual test code
- implementation steps show actual code or exact edit shape
- commands include expected output or expected failure
- no placeholders
- self-review the plan before asking for approval

Auxiliary source: Spec Kit `plan-template`.

Absorb these rules:

- include technical context
- include selected project/source structure with real paths
- include constraints, scale, storage, testing, platform, and dependencies when relevant
- include contract/data-model thinking before implementation when APIs or data structures change

## Required Pre-Plan Code Context Scan

Before writing `plan.md`, inspect enough code to avoid speculative plans:

- existing files that will be modified
- nearby tests
- imported helpers, services, components, routes, schemas, or clients
- existing naming and error-handling patterns
- existing function signatures and return shapes
- relevant root or directory `AGENTS.md`

If the needed signature, parameter, return shape, or dependency is unknown after a reasonable scan, stop and ask or mark the task `Human-gated`. Do not write `TBD`.

## Construction-Grade Plan Requirements

Every `plan.md` with implementation content must include:

- goal and architecture summary
- tech context
- files to create/modify/test/read with exact paths
- code context: existing functions/classes/modules and patterns
- interface contract for new or changed functions/classes/endpoints/components
- data contract when schema, payload, storage, or API shapes change
- test plan with actual failing test code when possible
- implementation steps with exact edits or code snippets
- exact commands and expected RED/GREEN output
- risks and rollback
- self-review checklist

## No Placeholders

These are plan failures:

```text
TBD
TODO
implement later
fill in details
add proper error handling
add validation
handle edge cases
write tests for the above
similar to previous task
use appropriate helper
```

If a detail is unknown, the plan must say how it will be discovered before implementation, or stop for human confirmation.

## Interface Contract Format

Use this shape for every meaningful interface touched by the task:

```md
### `<function-or-endpoint-name>`

Location:
Kind: function | class | endpoint | component | hook | schema | command
Signature:
Parameters:
- `<name>`:
Return:
Errors:
Side effects:
Existing callers:
New callers:
Tests proving contract:
```

For UI components:

```md
Props:
Events/callbacks:
State:
Accessibility:
Responsive behavior:
```

For API/data:

```md
Request:
Response:
Validation:
Persistence:
Authorization:
Migration:
```

## Step Format

Use checkbox steps that can be executed directly:

````md
- [ ] Step 1: Write failing API test

File: `apps/web/src/routes/projects/[id]/invites.test.ts`

```ts
it("rejects editor invite creation", async () => {
  const ctx = await createProjectRoleFixture({ role: "editor" });
  const res = await POST(ctx.request);
  expect(res.status).toBe(403);
});
```

Run:

```text
pnpm --filter @app/web test invite -- --runInBand
```

Expected RED:

```text
FAIL editor invite creation
Expected 403, received 201
```
````

## Self-Review

Before asking the human to approve the plan, verify:

- every accepted spec behavior maps to a step or explicit out-of-scope note
- every referenced function/type/path exists or is created earlier in the plan
- signatures, parameters, and property names are consistent across steps
- no placeholder language remains
- tests fail before implementation and pass after implementation
- commands are exact and scoped
- risky operations have rollback notes

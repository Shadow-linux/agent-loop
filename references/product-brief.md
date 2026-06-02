# Product Brief

Use this file when raw requirements need product/PRD-style synthesis before engineering specification.

## Core Split

```text
requirements/<date-topic>/ = original human source material package
feature/product.md   = current feature product understanding
feature/spec.md      = engineering behavior specification
project.md Product Context = cross-feature product consensus
project.md Domain Language = durable business terminology
```

`product.md` belongs to one feature. Long-term product consensus must be proposed for `project.md` during Project Memory Update.

## Trigger Conditions

Recommend Product Brief when any are true:

- feature has a meaningful user journey or UI/interaction flow
- human provides prototype, product document, PRD, design notes, or long requirement text
- multiple users, actors, roles, permissions, or tenants are involved
- 3 or more user stories are likely
- product scope and out-of-scope need negotiation
- terminology is ambiguous or conflicts with existing domain language
- humans ask for PRD, product doc, product brief, or product understanding

Skip Product Brief for narrow bugs, small refactors, configuration-only changes, or already-clear technical tasks.

## Product Brief Content

Write `feature/product.md` from `templates/product.md`.

Include:

- source requirements
- problem statement
- target users / actors
- solution summary
- user stories
- product scope
- out of scope
- product decisions
- open product questions
- terminology used in this feature
- long-term consensus candidates

## Grill With Docs Behavior

Before asking the human, inspect available project memory and source material:

```text
project.md Product Context
project.md Domain Language
project.md Product Principles
root or directory AGENTS.md
relevant docs / code / tests when the answer is discoverable
```

Rules:

- If code/docs can answer the question, inspect them instead of asking.
- If a term is fuzzy or overloaded, propose a canonical meaning.
- If a term conflicts with `Domain Language`, call out the conflict.
- Ask one blocking product question at a time.
- Include the agent's recommended answer with each question.
- Record accepted product clarifications in `product.md`.
- Record durable terminology in `project.md Domain Language` only after human confirmation.

## Product Context Backfill

During Project Memory Update, ask whether product decisions should be promoted when they affect future features:

- product positioning
- target users or roles
- core workflows
- permission/tenant/business rules
- durable out-of-scope decisions
- canonical terminology

Do not promote feature-local scope choices.

## Product To Spec

`spec.md` should reference `product.md` when it exists:

```md
Product Brief: product.md
```

`spec.md` should translate product intent into:

- added / modified / removed behavior
- acceptance criteria
- dependencies
- edge cases
- testing implications

Do not duplicate all product prose in `spec.md`.

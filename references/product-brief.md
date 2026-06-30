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

## Product Brief Source Gate

If the latest human message comes from `chat` or `requirements-discussion` and asks to write `product.md`, create a Product Brief, or “落到 product.md”, do not create feature `product.md` directly.

First ask whether to create or reference a requirement set, or confirm feature start and create the feature-level Product Brief.

Without a requirement source and confirmed feature context, do not create feature `product.md`.

Product Brief human confirmation is not the same as feature-start confirmation. The human may confirm that product intent is useful while still wanting the work to remain in Requirements Discussion. Treat that as requirement/product shaping, not feature workspace creation.

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
- primary user journey
- user stories
- acceptance direction for each user story
- product scope
- out of scope
- product decisions
- edge cases
- behavior changes for user/operator/system
- product tradeoffs
- success signals
- historical compatibility
- open product questions
- terminology used in this feature
- long-term consensus candidates

Product Decisions must record status, evidence/source, human gate, and Decision Scan routing when applicable.

When Requirement/Product Grill was used, `product.md` must carry the clarified terminology, journey, edge cases, behavior changes, historical compatibility, tradeoffs, and success signals that apply. Do not collapse grill results into only Problem Statement, Solution Summary, and Open Product Questions.

## Requirement/Product Grill

Product Brief synthesis starts after grill questions are resolved enough to express product intent.

Before asking the human, inspect available project memory and source material:

```text
project.md Product Context
project.md Domain Language
project.md Product Principles
root or directory AGENTS.md
relevant docs / code / tests when the answer is discoverable
targeted prior feature artifacts when terminology, flow, or historical behavior may already be defined
```

Rules:

- If code/docs can answer the question, inspect them instead of asking.
- If a term is fuzzy or overloaded, propose a canonical meaning.
- If a term conflicts with `Domain Language`, call out the conflict.
- If prior feature artifacts conflict with the current product direction, state the conflict and ask whether to reuse, override, or treat it as new scope.
- Ask one blocking product question at a time.
- Include the agent's recommended answer with each question.
- Record accepted product clarifications in `product.md`.
- Record durable terminology in `project.md Domain Language` only after human confirmation.
- to-prd-style Implementation Decisions and Testing Decisions are Decision Scan inputs, not ADRs.

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

# Requirement Management

Use this file before copying, moving, renaming, indexing, or referencing human-provided source material.

## Core Rule

`.agent-loop/requirements/` stores original human source material or references to it, grouped into requirement set directories.

It is not a working spec, PRD, task plan, or edited summary.

```text
human source requirement -> requirements archive/reference -> spec Source Requirements -> tasks/tests/plan
```

Never silently modify, rewrite, summarize over, or replace original human requirements.

`.agent-loop/requirements/` is canonical. Do not create or maintain legacy `inputs/` archives in current-version projects.

## Requirement Lifecycle / Backlog

`.agent-loop/requirements/` also owns requirement memory: what humans proposed, accepted, deferred, rejected, superseded, or had implemented.

Project memory must not be used as a backlog. Future work, deferred requirements, and unimplemented planned capabilities belong in requirement sets and optional `requirements/INDEX.md`, not in `project.md`.

Requirement set status values:

```text
proposed | accepted | deferred | in-progress | partially-implemented | implemented | superseded | rejected | reference-only
```

| Status | Meaning |
|---|---|
| `proposed` | Human mentioned it, but it is not confirmed as work to do |
| `accepted` | Confirmed requirement, not yet in a feature |
| `deferred` | Deferred future work |
| `in-progress` | Entered an active feature |
| `partially-implemented` | At least one Delivery Phase is implemented while another phase remains proposed, accepted, deferred, or in-progress |
| `implemented` | Implemented by a feature |
| `superseded` | Replaced by a newer requirement |
| `rejected` | Explicitly not doing it |
| `reference-only` | Background material only |

Use future/deferred intake when the human says or implies "先记一下", "后面做", "之后补", "下一轮做", "暂时不做", "以后加", "backlog", "defer this", "follow-up later", or "not in this feature".

Default behavior:

1. Recommend creating or updating a requirement set after human confirmation.
2. Set status to `proposed`, `accepted`, or `deferred` based on the human decision.
3. Update `requirements/INDEX.md` only when it already exists, index triggers apply, or the human asks for a backlog/requirements inventory.
4. If discovered during a feature, link the requirement set from feature `notes.md`.
5. Do not write future TODO, backlog, deferred requirements, or unimplemented planned capability details into `project.md`.

## Requirements Discussion Intake

Use requirements discussion intake when the human is exploring product needs, business goals, capability ideas, constraints, tradeoffs, or user scenarios without authorizing implementation.

Default behavior:

1. Use Brainstorm / Clarify before writing a requirement document.
2. Draft a human-reviewed requirement document only after the demand is clear enough to review.
3. Archive the human-reviewed requirement document after the human confirms the document should be recorded.
4. Set status to `proposed`, `accepted`, `deferred`, `rejected`, or `reference-only` based on the human decision.
5. Do not create a feature workspace unless the human explicitly says to start implementation.

A requirement document produced from brainstorming is requirement source material after human review.

Reviewed/recorded does not mean accepted for implementation.

Do not move the requirement source into a feature workspace when implementation starts. features reference requirement sets; requirements own source and lifecycle.

Feature `product.md` and `spec.md` may be derived from accepted requirements, but they are implementation views. They do not replace the requirement set and do not own requirement lifecycle.

## Requirement/Product Grill

Use Requirement/Product Grill during requirements discussion when terminology, business rules, flows, boundaries, exception paths, or historical feature behavior need clarification.

Rules:

- Load `requirement-product-grill.md` before asking grill-style questions.
- Ask one blocking question at a time and include the recommended answer.
- Inspect project memory, source requirements, code/docs/tests, and targeted prior feature artifacts before asking when those sources may already answer the question.
- Record accepted local terminology, scenarios, open questions, and conflicts in the reviewed requirement document. Keep the requirement set `README.md` to source, lifecycle, Delivery Phase, Feature Mapping, and decision-link summaries.
- Do not promote grill output to project memory, product.md, spec.md, or decisions without the owning human gate.
- Record cross-feature, shared design, hard-to-reverse, surprising, or real-trade-off signals as Design Readiness evidence and Decision Candidates, not accepted ADRs.
- Do not create `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/`.

## Requirement Delivery Phases

Use Delivery Phases when a requirement is too large to turn directly into one clear feature, or when humans need to confirm delivery order before implementation.

Recommend Delivery Phases when any are true:

- one requirement will likely become multiple features
- the requirement has MVP / later enhancement / Post-MVP scope
- multiple user journeys, roles, permissions, tenants, or business objects are involved
- multiple technical boundaries are involved, such as frontend, backend, payment, permissions, jobs, operations, or reporting
- the human says or implies "先做核心闭环", "后面再补", "下一轮做", "暂时不做", "以后加", or similar staged delivery language
- feature scope is growing too broad before Feature Spec or Work Breakdown
- the requirement README is becoming a long roadmap instead of a readable status view

Do not force Delivery Phases for small bugfixes, clear single-feature technical tasks, source-material archiving, or one user story that can be delivered in a single feature.

Delivery Phases belong in requirement set `README.md`, not in `project.md`:

```md
## Delivery Phases

| Phase | Goal | Scope | Out Of Scope | Acceptance Direction | Status | Feature Mapping | Source Notes |
|---|---|---|---|---|---|---|---|
| Phase 1: MVP |  |  |  |  | accepted | none | none |
```

Field meanings:

| Field | Meaning |
|---|---|
| `Phase` | human-readable phase number and name |
| `Goal` | business/product outcome for this phase |
| `Scope` | capabilities included in this phase |
| `Out Of Scope` | explicitly excluded from this phase |
| `Acceptance Direction` | human-readable completion direction, not a full test plan |
| `Status` | `proposed | accepted | deferred | in-progress | partially-implemented | implemented | superseded | rejected` |
| `Feature Mapping` | feature spec path when converted, otherwise `none` |
| `Source Notes` | phase note, prototype, feedback, or change request that shapes the phase |

Phase status uses the same vocabulary as requirement lifecycle where possible.

Phase slice means a smaller scope inside one accepted Delivery Phase. It is not a bundle of multiple phases.

Phase notes are optional source files for phase-specific human decisions:

```text
notes.phase-<n>-<slug>.md
```

Use a phase note when a phase has detailed product direction, references, screenshots, constraints, or accepted follow-up decisions. A feature created from that phase must list the phase note under `Source Requirements`.

Phase to feature rules:

- A phase may map to one feature when scope is clear.
- A phase may map to multiple features when one feature would be too broad.
- A normal feature should implement one accepted phase or one phase slice by default. Do not combine multiple phases into one feature just because the human asks to move quickly.
- If the human wants to implement multiple phases together, stop and ask whether to merge/rewrite the Delivery Phases first, or choose one phase/slice for the current feature.
- A deferred phase must not create a feature until the human chooses to start it.
- A phase that changes substantially should be updated only after human confirmation; if the old direction is replaced, mark it `superseded` and link the new phase or requirement set.
- Feature `spec.md` should name the requirement set and Delivery Phase it implements.
- When a feature starts or closes, update `Feature Mapping` and phase status in the requirement set `README.md` after human confirmation.

## Delivery Phase Status Roll-up

The requirement-set `Status` is derived from its Delivery Phases after each human-approved phase or Feature Mapping update. Do not set the top-level status from one feature alone.

```text
any phase is `implemented` and any other phase is not terminally implemented -> `partially-implemented`
```

For roll-up, `implemented`, `superseded`, and `rejected` are terminal for the agreed requirement scope. `proposed`, `accepted`, `deferred`, and `in-progress` still represent unimplemented scope.

Apply the first matching row:

| Phase State | Requirement Status |
|---|---|
| Requirement is superseded/rejected/reference-only as a whole | preserve that explicit terminal status |
| Every phase is `proposed` | `proposed` |
| Every phase is `deferred` | `deferred` |
| No phase is implemented; at least one phase is `in-progress` | `in-progress` |
| No phase is implemented; at least one phase is `accepted` | `accepted` |
| At least one phase is `implemented`; any other phase is proposed, accepted, deferred, or in-progress | `partially-implemented` |
| Every phase is implemented, superseded, or rejected | `implemented` |

When no Delivery Phases exist, use the ordinary requirement lifecycle table. Record the roll-up evidence in the requirement README and optional requirements index.

## Design Readiness

Before an accepted requirement enters Product Brief or Feature Spec construction, load `project-decisions.md` and run Design Readiness Check.

Record the result in requirement README `Design Readiness`. Multiple features, end-to-end business closure, shared domain/state/source-of-truth rules, consistency/concurrency/recovery needs, measurable non-functional goals, or cross-system/durable boundaries route to `Decision & Design If Needed` even when no technology choice is disputed.

Deferred, rejected, and reference-only requirements do not need Design Readiness until the human chooses to move them toward implementation.
- If Drift Check finds a completed or active feature that implements a phase but the phase still has `Feature Mapping: none`, treat that as requirement memory drift and propose a README backfill.
- Mark a phase `implemented` only after the implementing feature has fresh verification/review evidence for the accepted phase scope; feature close still requires its separate close confirmation.

Ask before creating, reordering, accepting, deferring, rejecting, superseding, or converting Delivery Phases. Agent may draft a phase table as a proposal, but the human owns the delivery order and scope decision.

## Source File Immutability

Requirement source files are immutable by default.

Do not overwrite, rewrite, summarize over, or edit `requirement.md` or other source files to reflect lifecycle status, implementation status, or current code reality.

Write lifecycle and status updates to requirement set `README.md` and optional `requirements/INDEX.md`. Append new follow-up, feedback, or change material as a new free-form source file in the same requirement set, or create a new requirement set when the follow-up materially conflicts with the original requirement.

If an agent created `requirement.md` from requirements discussion, still treat it as source material after human review. Editing it requires explicit human confirmation.

## Date Meaning

Requirement archive dates mean archive date only.

Do not infer:

- requirement duration
- feature lifecycle
- deadline
- implementation start date
- implementation end date
- business priority

Example:

```text
.agent-loop/requirements/2026-05-26-login/
```

Means:

```text
login source materials were archived on 2026-05-26
```

It does not mean the login feature must finish on that date.

## Requirement Set Layout

For new archives, use requirement set directories. Do not create new flat files directly under `.agent-loop/requirements/`.

A requirement set is one human intake package: requirement documents, prototypes, screenshots, design links, feedback, recordings, meeting notes, and follow-up notes that belong to the same topic or intake moment.

```text
.agent-loop/requirements/
  2026-05-26-login/
    README.md
    requirement.md
    prototype.png
    feedback.md
    design-link.md
```

## Requirement Set README

Every requirement set should include `README.md`:

```md
# Requirement Set: <topic>

Archived: YYYY-MM-DD
Topic: <topic>
Status: proposed | accepted | deferred | in-progress | partially-implemented | implemented | superseded | rejected | reference-only

Date Meaning:
- The date is the archive date only.
- It is not a deadline, feature duration, or implementation lifecycle.

Lifecycle:
- Intake Type: human-request | follow-up | deferred-from-feature | ops-discovery | bug-report | idea | reference
- Decision: proposed | accepted | deferred | rejected | converted-to-feature | partially-implemented | implemented | superseded
- Priority: unset | low | medium | high
- Owner Feature:
- Implemented By:
- Superseded By:
- Last Reviewed:
- Exit Condition:

Summary:
- One-line summary:

Delivery Phases:
- Use only when the requirement needs staged delivery.

| Phase | Goal | Scope | Out Of Scope | Acceptance Direction | Status | Feature Mapping | Source Notes |
|---|---|---|---|---|---|---|---|
| Phase 1: <name> |  |  |  |  | proposed | none | none |

Source Files:
- Requirement: requirement.md
- Prototype: prototype.png
- Feedback:
- Screenshots:
- Recordings:
- Links:
- Change Requests:
- Other:

Used By:
- .agent-loop/features/<feature>/spec.md

Status History:
- YYYY-MM-DD:
  - Status:
  - Reason:
  - Human Decision:

Notes:
- 
```

Use `templates/requirement-set-README.md`.

## External Paths

If the human provides files outside the repo, ask before copying or renaming.

If human confirms copy:

```text
copy into .agent-loop/requirements/YYYY-MM-DD-<topic>/
```

If human declines copy:

```md
Source Requirements:
- Requirement: Original: /absolute/path/to/requirement.md
```

Do not mutate the original external file.

## Changes And Versions

Do not overwrite earlier requirement materials when requirements change.

For small follow-up changes on the same topic or intake package, append a new file to the same requirement set:

```text
.agent-loop/requirements/2026-05-26-login/
  requirement.md
  prototype.png
  2026-05-29-change-request.md
```

For a major new direction or separate feature, create a new requirement set:

```text
.agent-loop/requirements/2026-06-04-login-sso/
```

The feature `spec.md` must reference all source requirements that shaped the current scope.

## Requirement Conflict Review

When follow-up material materially conflicts with the original requirement, do not silently append it as a small change and do not edit `requirement.md`.

Append to the same requirement set when:

- the original user goal remains the same
- the follow-up adds details, edge cases, acceptance clarification, prototype feedback, or small scope adjustment
- the original out-of-scope boundaries are not reversed
- continuing to use the same requirement set will not mislead future agents

Create a new requirement set when:

- the user goal changes
- core business rules change
- original out-of-scope becomes core scope
- original acceptance criteria become substantially invalid
- original prototype direction is replaced
- the new requirement becomes an independent feature or feature group
- continuing to use the old requirement set would mislead future agents

Before creating the new set or changing statuses, present a Requirement Conflict Review:

```md
## Requirement Conflict Review

| Area | Original Requirement | Follow-up Request | Conflict |
|---|---|---|---|
| User goal |  |  | low/medium/high |
| Business rule |  |  | low/medium/high |
| Acceptance |  |  | low/medium/high |
| Out of scope |  |  | low/medium/high |
| Existing feature impact |  |  | low/medium/high |

Recommended action:
- append to existing requirement set | create linked new requirement set | create a new requirement set and mark the old one superseded
```

Human confirmation is required before rebuilding requirement sets or marking a requirement `superseded`.

## Index Trigger

Do not force an index for small projects.

Recommend `.agent-loop/requirements/INDEX.md` when any are true:

- more than 10 requirement sets
- multiple features share source requirements and humans need a cross-feature inventory
- old requirement sets are frequently superseded
- source materials include many external paths
- humans ask for a requirements inventory

The index is an inventory, not the source of truth.

In v1.2.3+, the index may also include a backlog/deferred view. It still remains an inventory; original source material stays in requirement sets or external source paths.

## Backward Compatibility

Old requirement set README files remain valid when they contain only:

- `Archived`
- `Topic`
- `Status: active | superseded | reference-only`
- `Date Meaning`
- `Source Files`
- `Used By`
- `Notes`

Do not classify old requirement sets as stale only because they lack `Lifecycle`, `Summary`, or `Status History`.

Old status interpretation:

| Old Status | Compatible Meaning |
|---|---|
| `active` | valid/usable source material; do not automatically rewrite to `accepted` or `in-progress` |
| `superseded` | `superseded` |
| `reference-only` | `reference-only` |

Never bulk migrate requirements automatically. Read old requirement sets as valid, and write new lifecycle fields only when touching that requirement set for confirmed lifecycle, backlog, conflict, or status updates.

## Human Gate

Ask before:

- copying source files
- moving source files
- renaming source files
- creating a requirement set
- creating or updating `requirements/INDEX.md`
- changing requirement lifecycle status
- marking a requirement `implemented`, `superseded`, or `rejected`
- rebuilding a requirement set because follow-up conflicts with original requirements

After archiving during an already-confirmed feature, update an existing `spec.md` `Source Requirements` with exact paths. Requirements Discussion and Requirement Archive do not create a feature workspace or `spec.md` merely to hold the link.

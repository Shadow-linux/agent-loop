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
proposed | accepted | deferred | in-progress | implemented | superseded | rejected | reference-only
```

| Status | Meaning |
|---|---|
| `proposed` | Human mentioned it, but it is not confirmed as work to do |
| `accepted` | Confirmed requirement, not yet in a feature |
| `deferred` | Deferred future work |
| `in-progress` | Entered an active feature |
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

## Source File Immutability

Requirement source files are immutable by default.

Do not overwrite, rewrite, summarize over, or edit `requirement.md` or other source files to reflect lifecycle status, implementation status, or current code reality.

Write lifecycle and status updates to requirement set `README.md` and optional `requirements/INDEX.md`. Append new follow-up, feedback, or change material as a new free-form source file in the same requirement set, or create a new requirement set when the follow-up materially conflicts with the original requirement.

If an agent created `requirement.md` from chat, still treat it as source material after creation. Editing it requires explicit human confirmation.

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
Status: proposed | accepted | deferred | in-progress | implemented | superseded | rejected | reference-only

Date Meaning:
- The date is the archive date only.
- It is not a deadline, feature duration, or implementation lifecycle.

Lifecycle:
- Intake Type: human-request | follow-up | deferred-from-feature | ops-discovery | bug-report | idea | reference
- Decision: proposed | accepted | deferred | rejected | converted-to-feature | implemented | superseded
- Priority: unset | low | medium | high
- Owner Feature:
- Implemented By:
- Superseded By:
- Last Reviewed:
- Exit Condition:

Summary:
- One-line summary:

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
- multiple active features share source requirements
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

After archiving, update `spec.md` `Source Requirements` with exact paths.

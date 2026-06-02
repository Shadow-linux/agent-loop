# Requirement Management

Use this file before copying, moving, renaming, indexing, or referencing human-provided source material.

## Core Rule

`agent-loop/requirements/` stores original human source material or references to it, grouped into requirement set directories.

It is not a working spec, PRD, task plan, or edited summary.

```text
human source requirement -> requirements archive/reference -> spec Source Requirements -> tasks/tests/plan
```

Never silently modify, rewrite, summarize over, or replace original human requirements.

`agent-loop/requirements/` is canonical. Legacy `agent-loop/inputs/` is read-only compatibility. Do not create new `agent-loop/inputs/` archives.

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
agent-loop/requirements/2026-05-26-login/
```

Means:

```text
login source materials were archived on 2026-05-26
```

It does not mean the login feature must finish on that date.

## Requirement Set Layout

For new archives, use requirement set directories. Do not create new flat files directly under `agent-loop/requirements/`.

A requirement set is one human intake package: requirement documents, prototypes, screenshots, design links, feedback, recordings, meeting notes, and follow-up notes that belong to the same topic or intake moment.

```text
agent-loop/requirements/
  2026-05-26-login/
    README.md
    requirement.md
    prototype.png
    feedback.md
    design-link.md
```

Flat files are legacy-compatible read-only shape for old projects. Do not use this shape for new requirement archives:

```text
agent-loop/inputs/2026-05-26-login-requirement.md
agent-loop/inputs/2026-05-26-login-prototype.png
```

## Legacy Inputs Migration

If `agent-loop/inputs/` exists:

1. Read it as legacy requirement source material.
2. Do not create new files inside it.
3. Find references to `agent-loop/inputs/` in `product.md`, `spec.md`, `tests.md`, `notes.md`, `project.md`, and enterprise `project/*.md`.
4. Present a migration table before changing anything:

```text
Old Path -> New Path
References to update
Risk
Human Decision
```

5. After human confirmation, move legacy requirement sets to `agent-loop/requirements/`.
6. Update `Source Inputs` headings to `Source Requirements`.
7. Update all paths from `agent-loop/inputs/...` to `agent-loop/requirements/...`.
8. Record the migration in the affected feature `notes.md` or `project.md`.

## Requirement Set README

Every requirement set should include `README.md`:

```md
# Requirement Set: <topic>

Archived: YYYY-MM-DD
Topic: <topic>
Status: active | superseded | reference-only

Date Meaning:
- The date is the archive date only.
- It is not a deadline, feature duration, or implementation lifecycle.

Source Files:
- Requirement: requirement.md
- Prototype: prototype.png
- Feedback:
- Screenshots:
- Recordings:
- Links:
- Other:

Used By:
- agent-loop/features/<feature>/spec.md

Notes:
- 
```

Use `templates/requirement-set-README.md`.

## External Paths

If the human provides files outside the repo, ask before copying or renaming.

If human confirms copy:

```text
copy into agent-loop/requirements/YYYY-MM-DD-<topic>/
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
agent-loop/requirements/2026-05-26-login/
  requirement.md
  prototype.png
  2026-05-29-change-request.md
```

For a major new direction or separate feature, create a new requirement set:

```text
agent-loop/requirements/2026-06-04-login-sso/
```

The feature `spec.md` must reference all source requirements that shaped the current scope.

## Index Trigger

Do not force an index for small projects.

Recommend `agent-loop/requirements/INDEX.md` when any are true:

- more than 10 requirement sets
- multiple active features share source requirements
- old requirement sets are frequently superseded
- source materials include many external paths
- humans ask for a requirements inventory

The index is an inventory, not the source of truth.

## Human Gate

Ask before:

- copying source files
- moving source files
- renaming source files
- creating a requirement set
- migrating legacy `agent-loop/inputs/`
- creating or updating `requirements/INDEX.md`

After archiving, update `spec.md` `Source Requirements` with exact paths.

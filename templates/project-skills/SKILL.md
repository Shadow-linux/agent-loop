---
name: <skill-name>
description: Use when <specific project trigger, symptom, or operational context>.
---

# <Skill Name>

## Overview

<State the reusable project capability and its core principle in one or two sentences.>

## Preconditions

- <Required project state, environment, inputs, and permissions.>
- <Evidence that must be checked before execution.>

## Workflow

1. <First bounded action.>
2. <Next bounded action.>
3. <Verification action.>

## Failure And Rollback

- Failure signal: <observable failure>.
- Stop condition: <when execution must stop>.
- Rollback: <safe reversal or recovery>.

## Verification

- Command or check: `<exact verification>`
- Expected result: `<observable success>`

## Resources

- Read `<relative reference path>` only when <condition>.
- Run `<relative script path>` only after the current invocation passes the Agent Loop Execution Gate.

## Common Mistakes

| Mistake | Required correction |
|---|---|
| `<likely project-specific failure>` | `<specific prevention or recovery>` |

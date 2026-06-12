# Project Onboarding DB

Document Language: 中文
Created:
Last Updated:
Last Verified:
Confidence:
Source Evidence:
Human Review Status: draft

## What This DB Is

## Project Scope

## Freshness Status

Freshness Window: 7 days

## How To Start Reading

| Goal | Read First | Then Read | Why |
|---|---|---|---|
| 10-minute onboarding | `overview.md` | `maps/module-map.md`, `runtime/setup-and-run.md` | understand purpose, main modules, and run path |
| prepare development | `maps/boundary-map.md` | `modules/<module>.md`, `flows/<flow>.md`, `quality/testing-and-verification.md` | understand boundaries, code ownership, flows, and verification |
| understand one module | `maps/module-map.md` | `modules/<module>.md`, related flows | find scope, entrypoints, call chain, and tests |
| understand one flow | `flows/<flow>.md` | related modules, state docs, async/job docs | read business path, state changes, and side effects |
| understand data model | `domain/data-model.md` | `domain/entities/<entity>.md`, state docs, related flows | understand entities, fields, relationships, writers, readers, and migrations |
| understand async/jobs | `runtime/async-and-events.md` | `runtime/jobs-and-schedules.md`, related flows, diagrams | understand queues, consumers, schedulers, retries, and side effects |
| troubleshoot | `quality/risks-and-unknowns.md` | related module, flow, runtime, or change-impact docs | locate known risks, blockers, and next checks |

## Role Reading Paths

| Role | Read First | Then Read | Useful For |
|---|---|---|---|
| frontend developer | `overview.md` | boundary docs, related flows, API docs, tests | understand UI/API boundaries, state, and verification |
| backend developer | `maps/boundary-map.md` | modules, flows, data model, jobs, tests | understand domain boundaries, services, data, and side effects |
| operations / DevOps | `runtime/setup-and-run.md` | environment/config section, `runtime/deployment-and-operations.md` when triggered, embedded or standalone diagrams | understand runtime, config, deployment, rollback, and health |
| QA / tester | `quality/testing-and-verification.md` | flows, change impact map, known risks | understand test strategy, risk areas, and regression paths |
| product / domain reviewer | `overview.md` | flows, glossary, decisions/history | understand capabilities, terminology, and design tradeoffs |

## Module Reading Paths

| Module | One-Line Responsibility | Read First | Then Read | Core Call Chain | Useful For | Status |
|---|---|---|---|---|---|---|

## Flow Reading Paths

| Flow | Business Outcome | Read First | Related Modules | Related Diagram | Status |
|---|---|---|---|---|---|

## Data Model Reading Paths

| Entity | Meaning | Read First | Then Read | State Docs | Used By | Status |
|---|---|---|---|---|---|---|

## Document Index

| Document | Carries | Primary Evidence | Last Verified | Status |
|---|---|---|---|---|

## Diagrams Index

| Diagram | Question Answered | Target Doc | Evidence Chain | Last Verified | Confidence | Status |
|---|---|---|---|---|---|---|

## Needs Review / Unknowns

| Item | Why It Matters | Evidence | Suggested Follow-Up |
|---|---|---|---|

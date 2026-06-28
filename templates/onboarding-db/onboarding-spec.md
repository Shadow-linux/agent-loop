# Onboarding Spec

Document Language: 中文
Created:
Last Updated:
Last Verified:
Confidence:
Source Evidence:
Human Review Status: draft

## Purpose

This spec defines what the onboarding-db must teach before any Deep onboarding detail docs are written. It is the product spec for the onboarding work.

## Target Readers

| Reader | Needs To Understand | Not Needed In This Round |
|---|---|---|
| newcomer developer | | |
| operating / support engineer | | |
| future agent | | |
| human reviewer | | |

## Onboarding Goal

Write the concrete outcome in human terms:

```text
After this onboarding, a newcomer should be able to explain / run / debug / safely change ...
```

## Required-Core Topic Budget

Default Deep onboarding may select at most 5 required-core star topics before human expansion.

| Priority | Star Topic | Why Required-Core | Human Value | Evidence Seed | Planned Canonical Doc | Status |
|---|---|---|---|---|---|---|
| P0 | | | | | `stars/<topic>.md` | proposed |

Required-core signals include money, balance, billing, auth/API key, quota, main request flow, provider call, state writeback, async finality, external callbacks, retries, idempotency, production config, and repeated human questions.

## Supporting Summary Topics

Supporting topics stay in README, maps, or short index rows unless the human approves a split.

| Topic | Why Supporting | Where To Summarize | Split Later? |
|---|---|---|---|

## Non-Goals

- Do not create one file per directory.
- Do not create module/flow files just because a template exists.
- Do not mark coverage as complete because a file exists.
- Do not write directory-first docs before the onboarding plan is accepted.

## Quality Bar

A required-core topic is not `newcomer-ready` until it has an accepted star doc that explains:

- business meaning and actors
- phase-by-phase flow
- API / command / callback / job entrypoints
- code evidence and symbols
- data models, tables, Redis keys, Kafka topics, config, or external systems
- state changes and fact sources
- success path, branch path, and failure path
- retry, idempotency, compensation, fallback, and operational risks
- verification, logs, metrics, or runbook checks
- concrete examples
- key file index and reading order

## Human Decisions Needed

| Decision | Recommended Default | Why It Matters |
|---|---|---|


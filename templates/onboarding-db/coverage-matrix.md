# Onboarding Coverage Matrix

Document Language: 中文
Created:
Last Updated:
Last Verified:
Confidence:
Source Evidence:
Human Review Status: draft

## Purpose

Coverage tracks learning outcomes, not file existence. `newcomer-ready requires an accepted star doc` for required-core topics.

## Status Values

| Status | Meaning |
|---|---|
| discovered | found but not planned |
| planned | included in onboarding spec / plan |
| needs-deep-trace | required-core but not deeply documented |
| draft-star | star doc exists but has not passed human review |
| newcomer-ready | accepted star doc teaches the topic with evidence |
| supporting-summary | summarized in README/maps; no standalone star needed |
| blocked-by-unknown | missing code evidence or business confirmation blocks completion |
| not-applicable | explicitly not relevant |

## Coverage Table

| Topic | Core Role | Canonical Location | Planned Batch | Evidence | Confidence | Status | Missing For Newcomer-Ready | Human Review |
|---|---|---|---|---|---|---|---|---|

## Completion Decision

Allowed decisions:

```text
Safe-entry project memory updated; onboarding-db docs not requested.
Onboarding spec accepted; implementation not started.
Onboarding batch <n> accepted; remaining topics incomplete.
Onboarding DB draft is usable but incomplete.
Deep onboarding complete.
```

Deep onboarding cannot complete while any required-core topic is `discovered`, `planned`, `needs-deep-trace`, `draft-star`, or `blocked-by-unknown`.

## File Budget Audit

| File | Type | Counts Against Budget? | Why It Exists | Merge Candidate? |
|---|---|---|---|---|

# Agent Loop Full Validation Report

Date: 2026-06-07
Target: `skills/agent-loop`
Version checked: 1.2.0
Method: local mechanical validation plus three read-only subagent scenario reviews, followed by focused onboarding-db pressure reviews.

## Executive Summary

Overall result: PASS.

The current `agent-loop` skill can guide an agent through the core single-person development loop:

```text
Project Entry
-> Init / Existing Project Onboarding / Re-Adopt
-> Requirement Archive
-> Product Brief / Clarify
-> Feature Spec
-> Work Breakdown
-> Test Design
-> Technical Context / Plan
-> TDD Execution
-> Verify
-> Review
-> Drift Check
-> Project Memory Update
-> Feature Completion Check
-> Submit / Close with human confirmation
```

It also supports the v1.2.0 Project Onboarding Scan flow for helping a newcomer understand a project through `.agent-loop/onboarding-db/`, reading paths, module maps, core flow diagrams, targeted explanations, guided follow-up scans, startup/setup diagnosis, state-change trace, design-decision routing, and change-impact analysis.

## Validation Coverage

| Area | Result | Notes |
|---|---|---|
| New project initialization | PASS | Routes through Init Project before feature work. |
| Existing project takeover | PASS | Quick Onboarding is default; Deep Project Onboarding Scan is offered when useful. |
| Re-adoption after outside-loop work | PASS | Routes to Recovery Backfill before new feature work. |
| Requirement archive | PASS | Uses `.agent-loop/requirements/<archive-date>-<topic>/`; original human materials are preserved. |
| Product / PRD synthesis | PASS | Feature-level product intent goes to `product.md`; durable product consensus goes to `project.md`. |
| Feature spec and work breakdown | PASS | Spec acceptance gates downstream work; tasks default to vertical slices. |
| Test design and E2E discovery | PASS | Does not assume web E2E; discovers real environment first. |
| Plan quality | PASS | Construction-grade plan requires paths, interfaces, tests, commands, expected output, risks, and self-review. |
| TDD execution | PASS | RED/GREEN/default TDD loop is documented and can use Superpowers as a helper. |
| Task Done Gate | PASS | A task cannot be `done` without fresh verification, review, drift decision, and evidence link. |
| Submit / commit / PR | PASS | Submit requires diff inspection, verification, review, drift, memory status, and final human confirmation. |
| Feature close | PASS | Close requires verification, Feature Close Review, drift, memory update, and explicit human confirmation. |
| Superpowers adapter | PASS | External skills are stage helpers; agent-loop owns paths, status, gates, memory, submit, and close. |
| Project Onboarding Scan | PASS | Quick/Deep/Targeted modes, Compact/Standard/Expanded layout, diagrams, and Batch Human Review are covered. |
| Newcomer guided onboarding | PASS | Existing onboarding-db is used first; full Deep Scan is not rerun by default. |
| Targeted explanation / diagram update | PASS | Human questions can route to Targeted Onboarding Scan and confirmed diagram/doc updates. |
| Onboarding diagnostics | PASS | Startup failure, async/jobs reading paths, state-change trace, design-decision routing, and change-impact analysis have focused procedures and scenarios. |
| Onboarding DB templates | PASS | Compact/Standard/Expanded template rules now include role reading paths, bilingual glossary fields, setup failure notes, state traces, and impact-map guidance. |

## Subagent Reviews

| Reviewer | Focus | Result | Main Finding |
|---|---|---|---|
| A | New project, new feature, TDD, submit/close, Superpowers | PASS | Main loop is complete; submit known-drift wording needed hardening. |
| B | Existing project, stale docs, re-adopt, memory mode | PASS | Old project takeover and enterprise memory are sufficient; a few checklist/docs lines needed clarity. |
| C | Project Onboarding Scan, onboarding-db, newcomer experience | PASS with deployment risk | Target package passes; installed global skill may still be older if not synced. |

## Focused Onboarding Pressure Reviews

| Reviewer | Focus | Initial Result | Resolution |
|---|---|---|---|
| A | README async/jobs reading path, role reading paths, startup failure diagnosis | PASS | Confirmed onboarding-db can route "I cannot run the project" to focused setup diagnosis and safe doc updates. |
| B | State Change Trace and Design Decision Routing | PASS with low suggestion | Added explicit validation wording that state/change questions load both `onboarding-db.md` and `onboarding-diagnostics.md`. |
| C | Change Impact Analysis and glossary consistency | FAIL | Tightened the Change Impact output table, added a standalone `glossary.md` template, and aligned glossary derivation with bilingual glossary fields and alias/conflict tracking. |

## Issues Found And Resolved

| Severity | Issue | Resolution |
|---|---|---|
| Low | `SKILL.md` body version was still `1.1.1` while package docs were `1.2.0`. | Updated `SKILL.md` to `1.2.0`. |
| Low | Submit stage could be read as allowing known drift without a drift inspection. | Submit now requires drift check; known drift still needs a minimum recorded Drift Check. |
| Low | Existing Project Onboarding usage docs listed too few write targets. | Expanded Usage write targets to include project memory, requirements/features dirs, root guidance, enterprise memory, and onboarding-db when confirmed. |
| Low | Re-adoption was not explicit enough in checklist/stage guide. | Added explicit re-adoption routing and mandatory `recovery-and-backfill.md` loading for re-adopt requests. |
| Low | Existing onboarding-db guided onboarding was not a first-class runtime state. | Added `guided-onboarding` entry classification and routing rule. |
| Low | README lacked a newcomer onboarding example. | Added a guided project onboarding quick-start section. |
| Medium | Onboarding DB lacked a clear async/jobs reading path for humans. | Added README reading paths for async/jobs and role-based onboarding. |
| Medium | "Setup docs do not work" was not distinct from normal build/test failure. | Added Startup Failure Diagnosis and Common Startup Failures update rules. |
| Medium | State-flow diagrams did not answer "who changed this state?" | Added State Change Trace for writers, triggers, guards, side effects, tests, evidence, and confidence. |
| Medium | Change impact analysis was scattered across templates. | Added a central Change Impact Analysis procedure and required impact output table. |
| Low | Design-decision questions had a template but no routing rule. | Added Design Decision Routing from onboarding-db problem routing to diagnostics. |
| Low | Onboarding glossary did not consistently support bilingual projects. | Added Chinese/English meaning fields plus synonyms/aliases/conflict guidance and a standalone `glossary.md` template for Standard/Expanded layouts. |

## Remaining Deployment Risk

The source package under `skills/agent-loop` is now internally aligned as v1.2.0. A subagent observed that the installed global copy at `/Users/shaodowyd/.codex/skills/agent-loop` may still be older. That is a deployment/sync concern, not a source-package correctness issue.

Before relying on v1.2.0 in a new Codex session, sync or reinstall the skill intentionally.

## Mechanical Checks

| Check | Result |
|---|---|
| `SKILL.md` YAML frontmatter parse | PASS |
| `plugin.json` JSON parse | PASS |
| Markdown fence parity across skill docs | PASS |
| `git diff --check` | PASS |
| Version string alignment in source package | PASS |

## Final Assessment

The current skill can operate as a controller for:

- building a new project from a human goal,
- taking over an old project,
- continuing a feature across sessions,
- maintaining project memory and feature docs when code reality changes,
- using Superpowers without losing agent-loop ownership,
- helping a newcomer learn a project through onboarding-db,
- switching back from onboarding to normal feature/task development.

The biggest remaining non-code issue is deployment: make sure the installed runtime copy matches this source package before expecting Codex or Claude to use v1.2.0 behavior.

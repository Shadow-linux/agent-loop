# Mandatory Stage Helper Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make seven Superpowers-backed stages resolve and load their helper before acting, while preserving agent-loop control, artifact paths, gates, and fallback behavior.

**Architecture:** Add one mandatory helper-resolution protocol to the controller and routing reference, then keep stage-specific behavior in the external adapter. Store auditable resolution records in the existing feature `notes.md`; validate the contract with a repository shell test and behavioral pressure scenarios.

**Tech Stack:** Markdown skill instructions, POSIX shell validation, Ruby YAML validation.

---

### Task 1: Add a failing helper-routing contract test

**Files:**
- Create: `tests/validate-mandatory-helper-routing.sh`
- Read: `SKILL.md`
- Read: `references/skill-routing.md`
- Read: `references/external-skill-adapters.md`
- Read: `templates/notes.md`

- [ ] **Step 1: Write a shell test asserting the seven canonical helpers, alias resolution, full skill loading, fallback restriction, resolution records, controller precedence, and path override.**
- [ ] **Step 2: Run `bash tests/validate-mandatory-helper-routing.sh`.**

Expected: FAIL because the current routing contract treats helpers as preferred and records no special state when unavailable.

### Task 2: Implement the mandatory controller and adapter contract

**Files:**
- Modify: `SKILL.md`
- Modify: `references/skill-routing.md`
- Modify: `references/external-skill-adapters.md`
- Modify: `references/stage-guides.md`
- Modify: `templates/notes.md`

- [ ] **Step 1: Add the controller-level mandatory stage-helper rule and completion assertion.**
- [ ] **Step 2: Add canonical and unprefixed alias resolution for the seven helpers.**
- [ ] **Step 3: Require complete helper loading before stage actions and allow fallback only for `unavailable` or `load-failed`.**
- [ ] **Step 4: Add per-stage preconditions for brainstorming, planning, TDD, debugging, verification, review, and approved subagent execution.**
- [ ] **Step 5: Add a reusable Stage Helper Resolution record to `notes.md`.**
- [ ] **Step 6: Run `bash tests/validate-mandatory-helper-routing.sh`.**

Expected: PASS.

### Task 3: Document and pressure-test the behavior

**Files:**
- Modify: `references/validation-scenarios.md`
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Add pressure scenarios for installed helpers, aliases, unavailable helpers, forbidden silent fallback, path override, and subagent authorization.**
- [ ] **Step 2: Explain the mandatory helper contract and controller/path ownership in human-facing docs.**
- [ ] **Step 3: Record the behavior change under v1.2.2 without changing the version.**

### Task 4: Verify the repository

**Files:**
- Verify all changed files.

- [ ] **Step 1: Run `bash tests/validate-mandatory-helper-routing.sh`.**
- [ ] **Step 2: Run `ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'`.**
- [ ] **Step 3: Run a Markdown fence-balance check across changed Markdown files.**
- [ ] **Step 4: Run `git diff --check`.**
- [ ] **Step 5: Review `git diff` and confirm unrelated untracked files remain untouched.**

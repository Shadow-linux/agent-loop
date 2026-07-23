# Global Skill Installation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Do not dispatch subagents unless the human separately authorizes them. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Agent Loop GitHub repository installable and updateable through the existing `skills` CLI for Codex, Kimi Code CLI, Claude Code, and OpenCode without publishing a separate npm package.

**Architecture:** Keep `Shadow-linux/agent-loop` as the only Agent Loop package source and use Vercel's `skills` CLI as the installer. Human-facing documentation owns the commands; runtime sources preserve exact authorization and project-guidance boundaries. A focused contract test prevents supported Agent IDs, commands, fallback, and the post-update `AGENTS.md` reminder from drifting.

**Tech Stack:** Markdown Skill package, Vercel `skills` CLI through `npx`, Bash contract tests, isolated temporary home smoke testing, existing YAML/Markdown validators.

---

Status: implementation complete; awaiting Human Review
Design source: `docs/proposal/v1.5.x/global-skill-installation.md`
Target branch: `alpha/v1.5.0`
Baseline HEAD: `699d5a68d35854a31931701d970ed7b0fc439ac9`
Target version: v1.5.0; do not bump version

## Constraints

- This is the Agent Loop Skill source repository; do not create target-project `.agent-loop/` artifacts.
- Do not create or publish an Agent Loop npm package.
- Do not add a custom installer, dependency, post-install hook, or automatic project `AGENTS.md` mutation.
- Treat `main` as the latest formal stable default installation channel; alpha branches remain explicit pre-release sources.
- Do not synchronize `main` during this implementation. That branch/merge/push action requires a separate release Human Gate.
- Preserve the existing exact Human authorization boundary for global installation.
- Keep the manual Git clone method as a fallback.
- Use an isolated temporary home for installation tests; never modify real Codex, Kimi, Claude, or OpenCode Skill directories.
- Preserve unrelated `.tmp/`, `scripts/__pycache__/`, and `tests/__pycache__/` content.
- Do not commit, push, tag, release, publish, or sync installed Skills without a separate Human Gate.

## Task 1: Add a focused RED documentation contract

**Files:**
- Create: `tests/validate-global-skill-installation.sh`

- [x] Add assertions requiring:

```text
npx -y skills add Shadow-linux/agent-loop
--agent codex
--agent kimi-code-cli
--agent claude-code
--agent opencode
npx skills update agent-loop -g
npx skills list -g
Agent Loop 版本已更新，请更新项目的 AGENTS.md。
```

- [x] Require README to retain a manual Git clone fallback.
- [x] Require README and maintainer guidance to define `main` as the exact latest formal stable default installation channel.
- [x] Require SKILL/runtime boundaries to reject automatic or unscoped installation.
- [x] Run `bash tests/validate-global-skill-installation.sh`.
- [x] Confirm RED because the installation and update commands are not yet documented.

## Task 2: Align human and runtime documentation

**Files:**
- Modify: `README.md`
- Modify: `Usage.md`
- Modify if needed for precise boundary wording: `SKILL.md`
- Modify: `references/concepts.md`
- Modify: `references/validation-scenarios.md`
- Modify: `CHANGELOG.md`

- [x] Replace manual clone as the primary README installation path with the explicit four-runtime command.
- [x] Keep the interactive short command and manual clone fallback.
- [x] Add update and inventory commands.
- [x] Keep the accepted GitHub `IMPORTANT` reminder immediately after update guidance.
- [x] Explain that unqualified installation follows `main`, while alpha revisions require explicit selection.
- [x] Add one natural-language Usage section for installing, updating, verifying, and requesting project-guidance refresh.
- [x] Preserve the distinction between human-authorized global installation and prohibited automatic/unscoped installation.
- [x] Align the remaining first-version scope and validation wording with `SKILL.md` and `references/design.md`: explicit human installation is supported; automatic or unscoped installation remains excluded.
- [x] Record the v1.5.0 documentation/distribution capability in CHANGELOG without changing the version.

## Task 3: Focused GREEN and isolated compatibility smoke test

**Files:**
- Modify: `docs/proposal/v1.5.x/global-skill-installation-implementation-plan.md`
- Create: `docs/reports/agent-loop-v1.5.0-global-skill-installation-validation-2026-07-24.md`

- [x] Run the focused contract and confirm GREEN.
- [x] Run `npx -y skills add . --global --skill agent-loop --agent codex --agent kimi-code-cli --agent claude-code --agent opencode --copy --yes` with isolated `HOME` and `XDG_CONFIG_HOME`.
- [x] Verify the canonical universal installation at `~/.agents/skills/agent-loop`, plus the Claude compatibility path at `~/.claude/skills/agent-loop`; confirm the installer reports Codex, Kimi Code CLI, OpenCode, and Claude Code as selected targets. The compatibility path may be a copy or link according to the selected installer mode.
- [x] Verify installed content includes `references/runtime.md`, `references/design.md`, `templates/root-AGENTS.md`, and `scripts/check-root-agents-blocks.py`.
- [x] Run `npx skills list -g` inside the isolated home and confirm `agent-loop` is present.
- [x] Run public-source discovery with `npx -y skills add Shadow-linux/agent-loop --list`; if HTTPS is unavailable but the same GitHub repository is verified through SSH, record the environment limitation and keep HTTPS validation as a release-check item.
- [x] Verify the default GitHub branch and record whether its current version matches the intended formal stable channel; do not change any branch or remote without a separate Human Gate.
- [x] Record commands, actual evidence, limitations, and rollback in the validation report.

## Task 4: Repository validation and Human Review

**Files:**
- Review all changed files

- [x] Run:

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
git diff --check
```

- [x] Run the repository Markdown fence-balance check.
- [x] Review tracked and untracked files; exclude `.tmp/` and cache directories from owned changes.
- [x] Confirm no version, plugin metadata, root template, stage order, routing axis, Human Gate, or target-project artifact changed unintentionally.
- [x] Present implementation, evidence, rollback, and residual risk for Human Review.
- [x] Stop before commit and push.

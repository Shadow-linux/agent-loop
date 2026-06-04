# Agent Loop Skill

This repository contains the `agent-loop` skill source.

## Repository Purpose

- Maintain the reusable `agent-loop` skill.
- This is a skill source repository, not a target project using `agent-loop`.
- Do not create target-project `.agent-loop/requirements/` or feature docs here unless editing examples.
- The skill should make agents own workflow diagnosis and sequencing while keeping required human gates explicit.

## Source Of Truth

- `SKILL.md`: concise skill entrypoint loaded by CLI agents.
- `references/`: detailed operational rules loaded by the skill.
- `templates/`: document templates written into target projects.
- `README.md`: human-facing overview and install notes.
- `Usage.md`: human-facing operation guide.
- `CHANGELOG.md`: version history.
- `examples/`: example project states and feature artifacts.
- `agents/openai.yaml`: OpenAI/Codex skill metadata.

## Maintenance Rules

- Prefer `rg` for search and normal shell commands for inspection.
- Use `apply_patch` for manual edits.
- Do not use a global shell wrapper unless this repository explicitly asks for one.
- Keep `SKILL.md` concise; move detailed behavior into `references/`.
- Do not add unsupported frontmatter fields to `SKILL.md`; keep the YAML frontmatter limited to stable loader fields unless the loader requirement changes.
- Keep references and templates consistent with `SKILL.md`, `README.md`, and `Usage.md`.
- Update `CHANGELOG.md` for meaningful behavior, gate, artifact, template, or example changes.
- Do not bump the skill version unless the human explicitly approves the version upgrade.
- If a meaningful skill change is committed without a human-approved version bump, record it under the current unreleased or in-progress changelog section instead of changing version numbers.
- Commit messages should include the version, for example `v1.0.1: clarify delivery contract gates`.
- Stable release branches use the exact version name, for example `v1.0.1`, not `release/1.0.1`.

## Hard Red Lines

- Do not make Delivery Contracts default artifacts.
- Do not allow tasks to become `done` without verification, evidence, review, and drift rules in the skill.
- Do not remove human gates for Delivery Contract file creation/acceptance/breaking changes, submit, pause, or close.
- Do not add unsupported `SKILL.md` frontmatter fields unless loader support is confirmed.

## Verification

After edits, run at least:

- `ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'`
- a Markdown fence balance check
- `git diff --check`

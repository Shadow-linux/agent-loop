# Agent Loop Skill

This repository contains the `agent-loop` skill source.

## Repository Purpose

- Maintain the reusable `agent-loop` skill.
- This is a skill source repository, not a target project using `agent-loop`.
- Do not create target-project `.agent-loop/requirements/` or feature docs here unless editing examples.
- The skill should make agents own workflow diagnosis and sequencing while keeping required human gates explicit.

## Repository Perspective

You are maintaining the Agent Loop skill source repository. You are not, by default, a user Agent running Agent Loop inside a target project. When the human says "we are developing Agent Loop," keep the maintainer perspective unless they explicitly ask you to simulate or test the downstream user-Agent experience.

Before deciding where a rule belongs, classify its audience and use the matching surface:

| Audience / purpose | Owning surface |
|---|---|
| Agent developing, reviewing, validating, releasing, or maintaining this repository | `AGENTS.md` and `docs/maintenance/` |
| User Agent loading and running the distributed Agent Loop skill | `SKILL.md` and `references/` |
| Guidance copied into a target project's root `AGENTS.md` | `templates/root-AGENTS.md` |
| Artifacts created inside a target project's `.agent-loop/` workspace | `templates/`, artifact rules, and examples |
| Human learning what Agent Loop does or how to trigger it | `README.md` and `Usage.md` |
| Human asking what changed in a version | `CHANGELOG.md` |
| Historical proposals and completed validation evidence | `docs/proposal/` and `docs/reports/`; these are not runtime authority |

Do not place repository-maintainer workflow in user-facing `references/`. Do not treat `templates/root-AGENTS.md` as instructions for developing this repository; it is generated guidance for downstream target projects. Do not create target-project `.agent-loop/` artifacts in this source repository except when intentionally maintaining fixtures under `examples/`.

When testing downstream behavior, state the temporary perspective explicitly, keep test fixtures isolated, and return to the repository-maintainer perspective before deciding source ownership or editing maintenance guidance.

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
- Treat changes to canonical stage order, routing axes or precedence, root Stage Map signals/references, gate/stop rules, or controller fallback as coordinated workflow changes. Before completion, update the matching runtime/design source, root Stage Map, project guidance, validation scenarios, and regression tests in the same change. Also review `references/*.md` path changes and run the root guidance validation tests.
- Update `CHANGELOG.md` for meaningful behavior, gate, artifact, template, or example changes.
- Do not bump the skill version unless the human explicitly approves the version upgrade.
- If a meaningful skill change is committed without a human-approved version bump, record it under the current unreleased or in-progress changelog section instead of changing version numbers.
- If the human explicitly approves a version bump, update every version-bearing file in the same change so the repository never carries mixed skill versions.
- For this repository, when working on an `alpha-v<x.y.z>` branch, treat `<x.y.z>` as the intended skill version; ignore the `alpha` prefix for version records and changelog headings after the human approves implementation for that version.
- Commit messages for this skill repository should use type + version scope, prefer Chinese, and include a concrete multi-line body for meaningful changes.
- Stable release branches use the exact version name, for example `v1.0.1`, not `release/1.0.1`.
- This repository is mirrored to two remotes: `origin` (`git@github.com:Shadow-linux/agent-loop.git`) and `ai-factory` (`git@124.174.38.59:ai-factory/agent-loop.git`). When pushing release branches or tags, push the same branch and tag to both remotes.
- Do not create or push git tags unless the human explicitly asks for a tag.

## Version Sync Checklist

When the human explicitly approves a skill version bump, update these files together:

- `SKILL.md`: `Version: <x.y.z>`
- `plugin.json`: `"version": "<x.y.z>"`
- `README.md`: `Current version`
- `Usage.md`: human-facing version label
- `CHANGELOG.md`: new version heading and dated release section
- `templates/root-AGENTS.md`: every managed block's full `block-version:<x.y.z>-<YYYYMMDD>` value; no file-level version block or visible synced-version prose is required

Also verify whether these files need wording or example updates after a version bump:

- `references/project-guidance.md`: if version-sync rules or root guidance refresh behavior changed
- `references/submit-and-integrate.md`: if commit/version examples mention a concrete version
- `examples/`: only when example docs or generated guidance intentionally show concrete version strings

Rules:

- Do not bump versions in only human-facing docs while leaving templates or metadata behind.
- Do not change the version number in commit examples unless the example is meant to reflect the current skill version.
- After a version bump, run a repository search for the old version string to catch leftover references before commit.

## Commit Message Rules

Use this format for meaningful `agent-loop` repository commits:

```text
<type>(v<version>): <Chinese summary>

- <concrete behavior/template/reference/scenario/doc change>
- <concrete behavior/template/reference/scenario/doc change>
- <concrete behavior/template/reference/scenario/doc change>
```

Allowed types:

```text
feat, fix, docs, refactor, test, chore
```

Rules:

- Prefer Chinese for the summary and body unless the project context requires English.
- Include the current skill version scope, for example `docs(v1.2.4): 调整 Project Entry Scan 文档结构`.
- Do not use one-line-only commit messages for meaningful behavior, gate, artifact, template, reference, validation, or example changes.
- Use 3-7 bullet lines in the commit body, focused on concrete changes and user/agent-facing behavior.
- Use `docs` for proposals, README, Usage, and explanatory docs.
- Use `feat` for new skill capabilities or artifact behavior.
- Use `fix` for rule loopholes, broken routing, incorrect gates, or misleading templates.
- Use `test` for validation scenarios or pressure tests.
- Use `chore` for metadata, formatting, version alignment, or maintenance-only work.
- Keep the version number unchanged unless the human explicitly approves a version bump.

## Hard Red Lines

- Do not make Delivery Contracts default artifacts.
- Do not allow tasks to become `done` without verification, evidence, review, and drift rules in the skill.
- Do not remove human gates for Delivery Contract file creation/acceptance/breaking changes, submit, pause, close, commit, PR, merge, release, or publish.
- Do not add unsupported `SKILL.md` frontmatter fields unless loader support is confirmed.

## Verification

After edits, run at least:

- `ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'`
- a Markdown fence balance check
- `git diff --check`

## Full Skill Validation

When the human asks for a full validation, logic test, pressure test, scoring report, or pre-release acceptance of `agent-loop`, read and follow `docs/maintenance/full-validation-method.md`.

Also run that method after coordinated changes to canonical stage order, routing axes or precedence, controller fallback, Human Gates, status lifecycle, project memory, Decision / ADR placement, root Stage Map, or cross-file workflow invariants. A focused edit may use affected tests only when it does not change those control surfaces.

Full validation is a semantic audit plus executable regression testing. Mechanical checks alone are not sufficient. Preserve a RED baseline, add regression assertions for real loopholes, rerun all tests after repair, and save the Chinese report under `docs/reports/`.

Do not put repository-maintenance validation rules in `references/`, `templates/root-AGENTS.md`, or target-project `.agent-loop/` artifacts. Those surfaces are for the Agent Loop user workflow; this `AGENTS.md` and `docs/maintenance/` govern development of the skill repository itself.

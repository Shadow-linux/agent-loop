# Global Skill Installation

Status: implemented; awaiting Human Review
Target version: v1.5.0
Date: 2026-07-23
Upstream installer: <https://github.com/vercel-labs/skills>

## Problem

Agent Loop currently documents a manual Codex-only clone command. Humans need one maintained installation path that can install the same Agent Loop Skill globally for Codex, Kimi Code CLI, Claude Code, and OpenCode, and update it later without maintaining four copied repositories.

## Accepted Design

Use the existing Vercel `skills` CLI through `npx`. Do not publish an Agent Loop npm package and do not add a custom installer.

The Agent Loop repository remains the package source. Its root `SKILL.md`, `references/`, `templates/`, and scripts are installed together. The supported runtime identifiers are:

```text
codex
kimi-code-cli
claude-code
opencode
```

Recommended explicit installation:

```bash
npx -y skills add Shadow-linux/agent-loop \
  --global \
  --skill agent-loop \
  --agent codex \
  --agent kimi-code-cli \
  --agent claude-code \
  --agent opencode \
  --yes
```

Human-friendly interactive installation:

```bash
npx skills add Shadow-linux/agent-loop -g
```

Update and inventory:

```bash
npx skills update agent-loop -g
npx skills list -g
```

The unqualified GitHub source resolves through the repository default branch. Agent Loop therefore treats `main` as the default public installation channel:

- `main` must point to the exact commit of the latest formal stable release.
- `vX.Y.Z` remains the long-term maintenance branch for that release.
- `alpha/*` is never the default installation source and may be used only through an explicitly selected pre-release revision.
- A formal release is not complete for default installers until its accepted commit is synchronized to `main`.
- Synchronizing `main` is still a separate branch/merge/push Human Gate; this proposal does not authorize that Git action.

After updating the global Skill, a human working in an existing Agent Loop project should tell the Agent:

```text
Agent Loop 版本已更新，请更新项目的 AGENTS.md。
```

This reminder does not authorize whole-file replacement. Existing Agent Loop project-guidance rules continue to preserve human-authored content and require Human Review before managed-block changes.

## Boundaries

- Agent Loop is installable globally by an explicit human command.
- Agent Loop does not automatically install or update itself.
- An Agent may run an installation command only after exact Human authorization for that command, source, scope, and target.
- Installation does not update existing project `AGENTS.md` files.
- Project guidance refresh remains a separate Human-gated project action.
- Installation grants no Feature, Git, release, publish, production, paid, destructive, or external-action authority.
- The existing manual `git clone` route remains a fallback for environments that cannot run `npx`.
- Compatibility validation uses an isolated temporary home and must not modify the maintainer's real global Skill directories.

## Acceptance

- The public GitHub source is discoverable as exactly one `agent-loop` Skill.
- One explicit command installs it for all four named runtimes.
- Installed packages contain the controller and all runtime-owned directories required by `SKILL.md`.
- The default source resolves through `main`, and release guidance requires `main` to match the exact latest stable release commit.
- `skills list -g` exposes the installed Skill.
- `skills update agent-loop -g` is documented and validated without claiming that project guidance updates automatically.
- README, Usage, SKILL boundaries, CHANGELOG, and focused regression coverage agree.

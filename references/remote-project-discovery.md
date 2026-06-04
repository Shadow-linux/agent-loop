# Remote Project Discovery

Use this when the local directory is only an entry point for a remote project, or when local/remote/container execution is ambiguous.

## Trigger Conditions

Enter this stage before Init Project or Existing Project Onboarding when any are true:

- the human says this is a remote project
- the human mentions SSH, remote server, remote IDE, devcontainer, Docker container, Codespaces, tunnel, or remote workspace
- the local directory is empty or nearly empty and the human, local files, environment, or tool context provides a remote-entry hint
- the local directory has no reliable project markers such as `.git`, README, manifests, source directories, or test configs, and a remote-entry hint exists
- local commands cannot represent the real project, but a remote path or remote URL exists
- browser URL, runtime, tests, or deploy target clearly live outside the local directory

An empty local directory alone is not enough to classify the project as remote. Without a remote-entry hint, route to `new-project`. Do not create a full local `agent-loop` project memory for a confirmed empty remote-entry directory. First discover whether the source of truth is remote.

## Core Rule

Use two memory layers:

```text
local entry memory = how to find and verify the remote project
remote project memory = what the project is, what is active, and how to build/test/develop it
```

Preferred layout:

```text
local-entry/
  .agent-loop/
    remote.md
    project.md   thin remote-entry pointer

remote-project/
  AGENTS.md
  CLAUDE.md -> AGENTS.md
  .agent-loop/
    project.md
    requirements/
    features/
```

If the remote project is not writable, use local shadow mode:

```text
local-entry/
  .agent-loop/
    remote.md
    project.md
    requirements/
    features/
```

In local shadow mode, every code fact, command, test result, and browser observation must include remote evidence such as:

```text
[remote:/srv/app] pnpm test
[remote:/srv/app] src/auth/login.ts
[container:web] npm run test:e2e
```

## Discovery Questions

Ask only what cannot be safely discovered. Prefer reading existing connection docs first.

Minimum required facts before onboarding:

- Remote Host or remote workspace identifier
- Remote Path
- Access Method: ssh | devcontainer | remote IDE | container | browser-only | unknown
- Whether the agent may read remote files
- Whether the agent may write remote files
- Whether the agent may run install/build/test/dev-server commands
- Where `agent-loop` docs should live: remote | local-shadow | undecided

## Remote Entry Template

Write local `.agent-loop/remote.md` after human confirmation:

```md
# Remote Project Entry

Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Status: active | blocked | stale

Summary:
- This local directory is an agent-loop entry point for a remote project.

Remote Host:
Remote Path:
Access Method: ssh | devcontainer | remote IDE | container | browser-only | unknown
Local Path:
Local Purpose: remote-entry | mirror | docs-only | edit-workspace | unknown

Source Of Truth:
- Code: remote | local | mounted | unknown
- Git: remote | local | shared | unknown
- agent-loop docs: remote | local-shadow | undecided
- Runtime: remote | container | local | unknown

Permissions:
- Read remote files: yes | no | ask
- Write remote files: yes | no | ask
- Run install/build/test: yes | no | ask
- Create remote agent-loop: yes | no | ask

Connection:
- SSH Alias:
- Required VPN:
- Port Forwards:
- Browser URL:
- Auth:

Command Location:
- install:
- build:
- unit tests:
- API tests:
- E2E tests:
- dev server:

Sync Model:
- direct remote edit | git push/pull | rsync | mounted volume | remote-only | unknown
- Source of truth:
- Stale risk:

Last Verified:
Evidence:
Confidence: high | medium | low

Next Step:
```

## Thin Local Project Memory

If the local directory is only a remote entry, write a thin local `.agent-loop/project.md` after confirmation:

```md
# Project Memory

Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Status: remote-entry

## Project Summary

This local directory is an agent-loop entry point for a remote project.

## Remote Entry

See: .agent-loop/remote.md

Remote Project Memory:
- Location: remote | local-shadow | undecided
- Path:
- Status: unknown | active | blocked

## Current Work

Active Feature:
Paused Features:
Next Suggested Action: Verify remote connection and load remote project memory.
Gate Mode: Strict Mode
```

## Onboarding Route

After remote facts are confirmed:

1. Verify the remote path exists.
2. Verify the remote project markers: `.git`, README, manifests, source directories, tests, or existing guidance.
3. Decide where durable project memory lives:
   - remote if remote writes are allowed
   - local-shadow if remote writes are not allowed
   - undecided if human decision is needed
4. If remote memory is allowed, continue Existing Project Onboarding against the remote source of truth.
5. If local-shadow mode is required, continue Existing Project Onboarding from the local entry but label all facts with remote evidence.

## Stop Conditions

Stop and ask human before:

- creating `.agent-loop/` in the local entry directory
- creating `.agent-loop/` in the remote project
- writing root `AGENTS.md` / `CLAUDE.md` remotely
- running remote install/build/test/dev-server commands
- using credentials, VPN, tunnels, or port forwards
- treating local files as code reality when the source of truth is remote

## Drift And Maintenance

On every future entry from the same local directory:

1. Read local `.agent-loop/project.md`.
2. If `Status: remote-entry`, read local `.agent-loop/remote.md`.
3. Verify remote host/path/access still work.
4. Verify whether remote `.agent-loop/project.md` exists and is current.
5. If remote facts changed, update `remote.md` after human confirmation.
6. Then continue with remote project memory or local-shadow memory.

If local and remote facts disagree, remote execution reality is the code fact base. Local entry memory is only a pointer unless local-shadow mode is explicitly selected.

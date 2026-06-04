# Project Memory

Created: 2026-05-27
Updated: 2026-05-27
Status: remote-entry
Memory Mode: simple

## Project Summary

This local directory is an agent-loop entry point for a remote project.

## Project Memory Index

Mode: simple

If simple:
- This file is a thin remote-entry pointer.

Memory Mode Evidence:
- Local directory is an entry point, not the full project memory.

## Remote Entry

See: .agent-loop/remote.md

Remote Project Memory:
- Location: remote
- Path: `/srv/yuanjing/app/.agent-loop/project.md`
- Status: active

## Current Work

Active Feature:
Paused Features:
Next Suggested Action: Verify remote connection, read remote project memory, then continue the active remote feature.
Gate Mode: Strict Mode

## Environment Map

Local Workspace:
- Path: `/Users/example/workspace/remote-entry`
- Purpose: remote-entry
- Evidence: local directory contains only `.agent-loop/remote.md` and pointer memory.
- Confidence: high

Remote Workspace:
- Host: `app-server`
- Path: `/srv/yuanjing/app`
- Purpose: source-of-truth
- Access: ssh
- Evidence: remote path verified with `[remote:/srv/yuanjing/app] pwd`.
- Confidence: medium

Execution Locus:
- Install: remote
- Build: remote
- Unit Tests: remote
- API Tests: remote
- E2E Tests: remote/browser URL
- Dev Server: remote
- Database: remote test database
- Evidence: commands are recorded in remote `.agent-loop/project.md`.
- Confidence: medium

Sync Model:
- Method: direct remote edit
- Source of truth: remote
- Stale risk: local files are not code reality.

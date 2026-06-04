# Remote Project Entry

Created: 2026-05-27
Updated: 2026-05-27
Status: active

Summary:
- This local directory is an agent-loop entry point for a remote project.

Remote Host: `app-server`
Remote Path: `/srv/yuanjing/app`
Access Method: ssh
Local Path: `/Users/example/workspace/remote-entry`
Local Purpose: remote-entry

Source Of Truth:
- Code: remote
- Git: remote
- agent-loop docs: remote
- Runtime: remote

Permissions:
- Read remote files: yes
- Write remote files: ask
- Run install/build/test: ask
- Create remote agent-loop: ask

Connection:
- SSH Alias: `app-server`
- Required VPN: unknown
- Port Forwards: `3000:localhost:3000` if browser verification is needed
- Browser URL: `http://localhost:3000` after port forward
- Auth: seeded test user from remote project memory

Command Location:
- install: `[remote:/srv/yuanjing/app] pnpm install`
- build: `[remote:/srv/yuanjing/app] pnpm build`
- unit tests: `[remote:/srv/yuanjing/app] pnpm test`
- API tests: `[remote:/srv/yuanjing/app] pnpm test:api`
- E2E tests: `[remote:/srv/yuanjing/app] pnpm test:e2e`
- dev server: `[remote:/srv/yuanjing/app] pnpm dev`

Sync Model:
- direct remote edit
- Source of truth: remote
- Stale risk: local directory is not code reality

Last Verified: 2026-05-27
Evidence: `[remote:/srv/yuanjing/app] pwd`
Confidence: medium

Next Step: Read remote `.agent-loop/project.md` and continue the active feature.

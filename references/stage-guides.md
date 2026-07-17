# Agent Loop Stage Guides

Use this file to execute a specific stage. Pair it with `workflow-checklists.md` when you need checklist form.

Before asking the human to approve a non-trivial stage output, load `human-review-summary.md` and present a table-first approval summary. Full artifacts remain the source of truth.

## Stage Steering Rule

For every stage, the agent owns the next-step recommendation. After producing, updating, verifying, or diagnosing any artifact, include a table:

| Current Stage | Result | Recommended Next Stage | Why | Human Gate |
|---|---|---|---|---|

Use this especially for Project Entry Scan, Feature Spec, Work Breakdown, Test Design, Plan Gate, Execute, Verify, Review, Drift Check, Project Memory Update, Feature Completion Check, and Feature Follow-up. Do not ask the human "what next?" without first recommending one concrete next action.

## Project Entry

Entry: any use of this skill.

Read:

- `.agent-loop/project.md` if present
- `references/branch-management.md` when branch rules are confused, Target Release Context is unclear, or customer isolation is at risk
- enterprise `.agent-loop/project/*.md` detail files only when referenced by `project.md` and needed for the current stage
- active feature docs if present
- repo docs/scripts only as needed

Write:

- nothing until human confirms the next stage

Exit:

- one recommended next stage
- Branch Strategy Check preserves clear existing policy or presents one optional recommendation; adoption waits for explicit human acceptance and grants no Git action
- root `AGENTS.md` / `CLAUDE.md` status checked, or the recommended next stage explicitly includes the Root Agent Bootstrap Gate
- if an Active Feature exists, run Feature Completion Check before recommending a new feature or broad new work

## Code-Guided Operational Support

Entry: the human asks to test, run, deploy, switch account/config/model/provider, check quota or rate limits, arrange rollout, diagnose production, create a runbook/checklist, or use existing code to solve an operational problem without clearly requesting implementation.

Default action is read-only code/process analysis. This stage helps the human use current project functionality safely; it is not a default feature implementation lane.

Run Project Skill Discovery Guard before any stage-specific helper, generic fallback, command, tool call, temporary resource, or environment action.

With reliable project memory:

- inspect `.agent-loop/skills/INDEX.md` metadata and match only active `bootstrap` / `on-demand` rows against the current operational intent;
- for `matched-active`, verify the exact row, target path, instruction-bearing/executable files, and manifest, load only that Skill, and stop at the existing Execution Gate before its workflow or any side effect;
- for `index-absent | no-active-match`, continue the read-only Operational Support method without creating an empty Skill directory or scanning every Skill body;
- for `project-skill-drift`, fail closed and recommend Recovery or Project Skill Creation / Update rather than creating a temporary resource or performing an equivalent action through the generic path.

The guard is read-only and writes no artifact by default. If project memory is absent, stale, or outside-loop, complete Project Entry or Memory Recovery before trusting Project Skill claims.

Read as needed:

- `AGENTS.md`, `CLAUDE.md`, `.agent-loop/project.md`, and active run/deploy/testing notes
- README, docs, runbooks, deployment scripts, CI config, env/config examples
- relevant model/provider/account/config code paths, feature flags, rate-limit/quota logic, test scripts, smoke tests, health checks, rollback docs, logs/observability docs

Rules:

- Do not create a feature workspace by default.
- Do not edit code, change configuration, deploy, rotate credentials, or run destructive commands unless the human explicitly confirms either feature implementation or an operational change scope.
- Do not read or expose secrets. Ask the human to confirm secret names, masked values, or environment availability when needed.
- Prefer safe read-only commands and source inspection. For commands that contact external services, mutate state, consume paid quota, or touch production/staging, ask before running.
- Produce a concise runbook/checklist: current understanding, files inspected, required inputs, test steps, rollout steps, verification, rollback, risks, and open questions.
- If the request is ambiguous, ask whether the human wants feature implementation or help using current project functionality.
- If code or configuration changes are required, run Lightweight Change Assessment before defaulting to Feature construction, unless explicit Bug intent or a Feature hard trigger already decides the route.
- If durable runbook or project memory would help future agents, propose where to save it and ask before writing.

Write:

- no artifact by default
- optional `notes.md`, `.agent-loop/project.md`, or project docs only after human confirmation

Exit:

- operational checklist delivered, blocker/question identified, or human confirms escalation into feature/fix workflow

## Lightweight Change Lane

This is an internal route before Feature construction, not a canonical stage, message intent, Feature Type, Bug Resolution Path, lifecycle, status, or Auto Mode. Load `references/lightweight-change-lane.md` and render `templates/lightweight-execution-card.md` before the first write.

Entry: an actionable ordinary non-Bug local change may be bounded, reversible, and exactly verifiable.

Run in this order:

```text
Project Entry classification plus minimum guidance, dirty-work, scope and safety checks
-> explicit Bug / active Feature precedence
-> enumerate goal, acceptance, scope, risk, verification, rollback
-> decide clearly eligible | Feature trigger | uncertain
-> emit the complete card before first write
-> Project Skill Discovery Guard before generic action fallback
-> bounded edit
-> targeted verification
-> diff/scope/memory/rollback review
-> result or scope-expansion stop
```

Rules:

- A concrete bounded change request authorizes only the local scope disclosed in the card; it adds no separate Lightweight Mode gate.
- Explicit Bug Management and an active owning Feature take precedence. Generic `fix`, “修一下”, “改一下”, or “small tweak” wording alone decides neither route nor eligibility.
- Eligibility is all-of and Feature hard triggers are any-of. A missing fact becomes `Feature trigger` or `uncertain`, never an optimistic lane assumption.
- When uncertain, present few real options, one Agent recommendation, evidence/unknowns, and perform zero writes before the human answer.
- The response-local Plan always exists and never uses No-Plan Decision. Adapt its detail to risk without turning it into Feature `plan.md`.
- Fact/config/path/domain/docs changes use targeted syntax/parse/reference/residual/dry-run evidence. A small isolatable behavior branch uses the smallest meaningful RED/GREEN plus focused regression.
- If reliable memory exists, run Project Skill Discovery Guard before generic action fallback and preserve the matched Project Skill Execution Gate.
- Scope expansion stops before broader edits. Preserve current evidence, recommend exactly one Bug/Requirement/Feature route, and ask before keeping, reverting, or extending partial edits.
- Completion requires fresh verification, diff and disclosed-scope review, rollback, durable-memory impact review, and Result / Residuals.
- The card grants no branch, submit, commit, push, PR, merge, tag, release, publish, production, external, paid-call, configuration-write, destructive, Feature close, or Bug lifecycle action.

Write:

- one complete response-local Lightweight Execution Card;
- no target-project `.agent-loop/changes/`, `.agent-loop/quick-fixes/`, Feature workspace, or lightweight backlog.

Exit:

- verified bounded result and Human Review summary; or
- zero-write uncertain-route Human Choice; or
- scope-expansion stop with one recommended owning route.

## Project Skill Creation / Update

Entry: message intent is `project-skill-management`, or the human accepts an Agent-proposed Project Skill Candidate after a complex verified workflow. Reliable Project Entry/memory must exist.

Entry modes:

- explicit request: resolve authoring helpers before Candidate analysis, then present Gate 1;
- accepted proactive Candidate: the accepted Candidate already satisfies Gate 1, so resolve helpers after entry and before the first authoring action; do not ask Gate 1 again unless helper analysis materially changes scope.

Mandatory helpers:

- resolve `superpowers:writing-skills` / `writing-skills` for RED/GREEN/REFACTOR;
- independently resolve `skill-creator` for scaffolding and structural validation;
- use both when available;
- for explicit-request entry, record initial resolution response-locally before Gate 1; for accepted proactive-Candidate entry, record it after Gate 1 and before authoring; persist either record in `.agent-loop/skills/<skill-name>/validation.md` after creation.

Load:

- `project-skills.md`
- `skill-routing.md`
- `external-skill-adapters.md`
- `human-review-summary.md` before Gate 1
- existing `.agent-loop/skills/INDEX.md` and matching skill files for updates

Candidate analysis:

- inspect the successful source workflow and fresh evidence;
- identify repeatability, ordering, failure, rollback, environment, secrets, and external effects;
- choose `bootstrap` or `on-demand` with a reason;
- propose exact `.agent-loop/skills/<skill-name>/` files and resources;
- distinguish reusable procedural knowledge from one-off work, ordinary project facts, or mechanically enforceable checks.

Gate 1:

- present Project Skill Candidate and exact file tree;
- ask before creating `.agent-loop/skills/`, INDEX, or a new skill directory;
- use the same Gate 1 before material updates to an active skill;
- if implementation scope materially expands, stop and re-present Gate 1.

After Gate 1:

1. Create the INDEX entry and skill directory with status `proposed`.
2. Run RED scenarios without the new or revised skill and record exact failures in `validation.md`.
3. Write the minimum GREEN skill and required resources.
4. Re-run the scenarios with the skill, capture loopholes, REFACTOR, and re-test.
5. Validate frontmatter, trigger wording, resources, scripts, sensitive values, symlinks, and exact paths; finalize the active INDEX row and record a SHA-256 Validated Content Manifest for that exact row and current files.
6. If every required check passes and current content matches the manifest, update INDEX and validation evidence; status automatically becomes `active`.
7. If any required check fails, keep `proposed`, report the blocker, and do not route normal work through the skill.

Path rule:

```text
write: <target-project>/.agent-loop/skills/<skill-name>/
do not default: ~/.agents/skills/ | ~/.codex/skills/ | ~/.claude/skills/ | ~/.kimi/skills/ | docs/superpowers/
```

Execution Gate:

- discovery, INDEX reading, loading, and trigger matching are read-only preparation;
- before following the skill workflow or causing side effects, summarize skill, scope, steps, commands/files/external effects, risks, rollback, and verification;
- obtain human confirmation for one invocation;
- a human message that already names the skill and concrete scope may satisfy the gate only after the summary shows no undisclosed action/effect and no additional question is needed;
- `active`, `bootstrap`, previous success, previous confirmation, Feature Auto-Loop, and Task Auto-Run do not authorize execution;
- scope expansion requires a new confirmation.

Write after Gate 1:

- `.agent-loop/skills/INDEX.md`
- `.agent-loop/skills/<skill-name>/SKILL.md`
- `.agent-loop/skills/<skill-name>/validation.md`
- optional resources required by the accepted Candidate

Do not create a requirement set or feature workspace for this stage. Do not globally install the skill; global installation is a first-version exclusion. Do not commit, push, publish, or execute the skill without the matching separate authorization.

Exit:

- `active` with validation evidence and one recommended next stage;
- `proposed` with exactly one unblock action;
- lifecycle updated to `disabled` / `deprecated`; or
- no files created because Gate 1 was declined.

## Init Project

Entry: no `.agent-loop/` or legacy `agent-loop/`, little or no code.

If the human says the project is remote, or the local directory appears to be only a remote entry point, do not initialize a normal local project. Route to Remote Project Discovery first.

Load:

- `project-guidance.md`
- `project-memory-mode.md`
- `project-architecture-init.md`
- `branch-management.md` only when branch evidence triggers a recommendation

Before writing:

- classify project shape, language adapter, framework adapter, and DDD intensity
- determine guidance language from human preference or project language; default to English if unclear
- propose only a reference scaffold, with optional directories clearly marked
- ask human confirmation before creating code directories

Write after confirmation:

- `.agent-loop/project.md`
- `.agent-loop/requirements/`
- `.agent-loop/features/`
- root `AGENTS.md`
- root `CLAUDE.md -> AGENTS.md` pointer; if symlink/include is not supported, write a short pointer file

Use `templates/project.md`.
Use `templates/root-AGENTS.md` for project guidance.

Exit:

- project memory drafted and accepted
- root `AGENTS.md` status is `present`, `created`, or `human-deferred`
- root `CLAUDE.md` status is `points-to-AGENTS`, `created-pointer`, or `human-deferred`
- next stage: Requirement Archive when the human supplied requirements/prototypes in chat or files; otherwise Brainstorm / Clarify, Product Brief if Needed, or Feature Spec when intent is already stable

## Chat Entry

Entry: message intent is `chat`: ordinary discussion, rules questions, status questions, or design talk with no request to create requirements or start implementation.

Chat Entry is a default entry behavior, not a permanent label.

Do:

- answer, explain, or discuss
- inspect relevant agent-loop docs, project docs, or code only when useful for the answer
- if the discussion starts shaping demand, reclassify as `requirements-discussion`
- If chat evolves into product demand, reclassify as `requirements-discussion` and ask whether to shape it into a requirements document
- If chat turns into a proposal or design-note request, reclassify as `proposal-doc` and write only the requested proposal/doc
- If the human explicitly says they only want to discuss and do not want documentation yet, keep the intent as `chat`
- if the human asks to implement, reclassify as `feature-request`

Do not:

- create requirement sets
- create feature workspaces
- enter Work Breakdown, Plan Gate, Execute, Submit, or Close
- treat chat as approval to mutate files

Exit:

- answer is provided, or
- next recommended intent is `requirements-discussion`, `proposal-doc`, `feature-request`, `operational-support`, `feature-follow-up`, `deferred-requirement`, or Ask Human

## Requirements Discussion

Entry: message intent is `requirements-discussion`: the human is exploring product needs, business goals, capability ideas, constraints, tradeoffs, or user scenarios without authorizing implementation.

Default path:

```text
requirements-discussion -> Brainstorm / Clarify -> Requirement Document Draft -> Human Review -> Requirement Archive
```

Use:

- `requirement-management.md`
- `requirement-product-grill.md` when terminology, business rules, flows, boundaries, exception paths, prior feature behavior, or decision signals are unclear
- `project-decisions.md` when hard-to-reverse, surprising, cross-feature, or real-trade-off decisions appear
- `document-templates.md`
- `human-review-summary.md` before approval
- `skill-routing.md` and `external-skill-adapters.md` when a brainstorming or product-discovery helper is available

Rules:

- use Brainstorm / Clarify to shape the demand before writing the requirement document
- use Requirement/Product Grill before asking humans when terminology, roles, business objects, flows, exception paths, or historical behavior are unclear
- run targeted lookup of relevant prior feature `product.md`, `spec.md`, `tests.md`, and `notes.md` before asking a grill question
- classify Concept Foundation before detailed requirement-level Business Flow, Product State Model, or Requirement Product Model work
- when Concept Foundation triggers, follow the Human Grill Contract in order: inspect evidence, extract Concept Candidate Inventory, present one recommended definition with evidence and accept/reject impact, then ask exactly one downstream-blocking question
- keep the Concept Foundation Gate blocked while status is `candidate` or `reopened`; do not draft downstream flow/state/product-data sections as assumptions plus open questions
- use `concept-foundation-not-needed` only with a concrete no-semantic-change reason
- before setting a triggered foundation to `accepted`, load `human-review-summary.md` and present the Concept Foundation Human Review Summary after the one-question-per-turn Grill has resolved each blocker
- after status becomes `accepted`, derive relationships, roles/permissions, commands/events, flow, state, product data, invariants, exceptions, and recovery from stable Concept IDs and write Concept-To-Product Traceability
- record shared design signals as Design Readiness evidence and Decision Candidates; do not create accepted ADRs from Requirements Discussion
- keep early ADR signals as Decision Candidates until the requirement is human-reviewed and the owning gate is clear
- ask only questions that affect requirement clarity, scope, users/operators, constraints, non-goals, or acceptance direction
- When Requirement/Product Grill was used, the requirement document draft must include the grill-enriched sections from `document-templates.md`; use `Not applicable` plus a short reason instead of empty headings.
- run a lightweight Phase Scan when the demand looks larger than one feature, has MVP/later scope, contains multiple journeys or roles, crosses multiple technical boundaries, or the human uses staged-delivery language such as "先做核心闭环" or "后面再补"
- when Phase Scan triggers, propose a `Delivery Phases` table for human review before feature construction
- write a requirement document draft only after the intent is clear enough for human review
- The human-reviewed requirement document is stored under `.agent-loop/requirements/<archive-date>-<topic>/` after the human confirms the document should be recorded
- Reviewed/recorded does not mean accepted for implementation
- do not create a feature workspace during requirements discussion unless the human explicitly says to start implementation
- do not enter Work Breakdown, Plan Gate, or Execute
- Feature `product.md` and `spec.md` are derived implementation views; they do not own requirement lifecycle
- if the human wants to implement after requirement acceptance, create a feature that references the requirement set in Source Requirements

Write after confirmation:

- `.agent-loop/requirements/<archive-date>-<topic>/README.md`
- `.agent-loop/requirements/<archive-date>-<topic>/requirement.md`
- optional append-only `.agent-loop/requirements/<archive-date>-<topic>/YYYY-MM-DD-concept-foundation-<slug>.md` after a later semantic reopen, Requirement Conflict Review, and human confirmation
- optional `notes.phase-<n>-<slug>.md` when a phase has detailed human decisions or reference direction
- optional `.agent-loop/requirements/INDEX.md` only when it already exists, index triggers apply, or the human asks for an inventory/backlog view

Exit:

- requirement document human-reviewed and recorded
- requirement discussion remains open with next clarification question
- human chooses to start feature implementation from the accepted requirement set
- a triggered Concept Foundation never exits to downstream modeling while `candidate` or `reopened`

## Remote Project Discovery

Entry: the human says this is a remote project, local files contain remote-entry hints, or local/remote/container execution is unclear. An empty local directory with no remote hint should route to Init Project, not Remote Project Discovery.

Load:

- `remote-project-discovery.md`
- `project-guidance.md` only if guidance files may be created locally or remotely

Inspect:

- local `.agent-loop/project.md` and `.agent-loop/remote.md` if present
- local connection docs, README, scripts, SSH/devcontainer/container hints, or notes
- remote files only if the human has already granted access or the access method is already configured and safe to use

Do not:

- create a full local project memory for an empty entry directory
- treat local files as code reality when source of truth is remote
- run remote install/build/test/dev-server commands without confirmation
- create remote `.agent-loop/`, `AGENTS.md`, or `CLAUDE.md` without confirmation

Output before writing:

- whether this is a remote-entry, local mirror, local-shadow, or unclear setup
- remote host/path/access method if known
- proposed source of truth for code, git, runtime, and agent-loop docs
- command locations for install/build/unit/API/E2E/dev server if known
- permissions needed from the human
- one recommended next action

Write after confirmation:

- local `.agent-loop/remote.md`
- thin local `.agent-loop/project.md` with `Status: remote-entry` when local is only an entry point
- remote `.agent-loop/project.md`, `requirements/`, `features/`, root `AGENTS.md`, and `CLAUDE.md` only if remote writes are confirmed

Exit:

- local entry memory can locate the remote project
- the remote project memory location is decided: remote, local-shadow, or blocked
- next stage: Project Entry Scan against the remote source of truth, or Ask Human if access is blocked

## Project Entry Scan For Existing Projects

Entry: existing code, no `.agent-loop/` or legacy `agent-loop/`.

If the existing code is remote, perform Project Entry Scan against the remote source of truth. If local-shadow mode is active, all findings must include remote evidence labels.

Load:

- `project-entry-scan.md`
- `large-projects.md` when old, unfamiliar, multi-package, multi-service, or likely 100k+ LOC
- `project-guidance.md`
- `project-memory-mode.md`
- `project-architecture-init.md`

First decision:

- Explain that Project Entry Scan is safe-entry memory only, not newcomer documentation.
- Do not offer Quick / Deep / Targeted onboarding modes.
- If the human wants to continue feature work, do Project Entry Scan and update or propose project memory, root guidance status, commands, boundaries, and uncertainties only.
- If the human wants newcomer-facing or durable project-understanding docs, recommend Evidence-Graph + DDD Onboarding after Project Entry Scan or reliable project memory.

Inspect:

- README and docs
- AGENTS/CLAUDE/GEMINI files
- package/test scripts
- key directories
- native branch/release guidance, current Git reality, target-version evidence, and customer boundaries when they affect safe continuation

Use layered scan order:

1. startup docs
2. shallow repo shape
3. decide whether large-project triggers apply
4. optionally recommend bounded subagent scan when large and supported
5. runtime/tooling manifests
6. architecture profile and actual code layout
7. capability map
8. boundary map
9. guidance inventory
10. uncertainty list

Do not read the whole repository. Do not start feature implementation during Project Entry Scan.

If subagents are used, the main agent keeps ownership of synthesis and all writes. Subagents only return findings, evidence, confidence, uncertainties, files read, and suggested `project.md` entries.

Project Entry Scan output:

- draft `.agent-loop/project.md`, guidance status/proposal, and uncertainties
- do not write onboarding-db detail docs, module docs, flow docs, onboarding diagrams, onboarding-spec, or onboarding-tasks
- when the scan discovers stable project facts missing from project memory, propose or perform project memory backfill after human confirmation
- keep code reality as current fact when docs conflict with code

If the human asks a focused project-understanding question:

- inspect only the selected module, flow, async task, deployment path, state transition, or problem area plus minimal safe context
- answer from existing docs/code as chat or operational support
- propose narrow project memory backfill only when the focused scope exposes stale or missing facts required for safe continuation
- do not create unrelated onboarding-db files

Output before writing:

- project summary
- tech stack
- architecture profile: project shape, language adapter, framework adapter, DDD intensity, and whether layout is existing reality or proposed scaffold
- guidance language with evidence
- AGENTS cleanup / migration review when existing root guidance contains conflicting workflow rules, duplicated agent-loop rules, or long-term project memory outside managed blocks
- capability map with evidence and confidence
- boundary map with evidence and confidence
- discovered commands with evidence and confidence
- recommended Project Memory Mode: simple or enterprise, with trigger evidence
- Branch Strategy Check result: existing policy preserved, optional recommendation awaiting decision, or human-confirmed `accepted | declined | not-needed`; do not record an unconfirmed recommendation as accepted
- explicitly not doing: onboarding-db generation, module docs, flow docs, onboarding diagrams, onboarding-spec, onboarding-tasks
- Evidence-Graph + DDD onboarding proposal link when the human asks for newcomer docs
- existing/proposed guidance files
- low-confidence findings and recommended follow-up
- one recommended next action

Directory guidance:

- identify existing root and directory-level `AGENTS.md` / `CLAUDE.md`
- verify whether `CLAUDE.md` loads or points to `AGENTS.md`; do not maintain two independent root guidance bodies
- record guidance status in `project.md`
- propose directory-level `AGENTS.md` only for long-lived boundary directories
- ask human confirmation before creating or changing guidance files

Write after confirmation:

- `.agent-loop/project.md`
- enterprise `.agent-loop/project/*.md` files only when recommended and confirmed
- root `AGENTS.md` / `CLAUDE.md` guidance, if missing or stale
- directory-level `AGENTS.md` only if specific boundary directories are confirmed

Exit:

- human accepts project memory
- root guidance status is `present`, `created`, or `human-deferred` for `AGENTS.md`
- `CLAUDE.md` status is `points-to-AGENTS`, `created-pointer`, or `human-deferred`
- next stage: Evidence-Graph + DDD Onboarding when newcomer-facing or durable project-understanding docs are the current intent
- next stage: Decision & Design If Needed, Product Brief If Needed, Feature Spec, Code-Guided Operational Support, Requirement Archive, Re-Adopt Agent Loop Project, or Targeted Feature Scan, selected from current intent and artifact state

## Evidence-Graph + DDD Onboarding Knowledge Base

Entry: human asks for newcomer-facing docs, durable project understanding, guided learning paths, or onboarding-db construction, and Project Entry Scan or reliable project memory exists.

Load:

- `onboarding-knowledge-base.md`
- `project-entry-scan.md` only if project memory is missing, stale, or too thin
- `human-review-summary.md` before accepting the Onboarding Spec or accepting the later Full Execution Gate

Rules:

- Evidence Graph is the first onboarding artifact and must exist before formal module or flow docs.
- Do not run Quick / Deep / Targeted onboarding modes.
- Do not copy legacy directory-first onboarding-db structure unless the accepted Onboarding Spec says to migrate a specific useful file.
- Markdown is the source of truth; website generation is out of scope unless the human starts a separate website feature.
- Default language is Chinese. Preserve code symbols, file paths, commands, API paths, env vars, config keys, errors, and third-party product names.
- 全部正式文档默认使用中文；写不透但有证据可推断的内容要标明“推断”、证据、置信度和待验证点。
- Human examples are quality/detail references only. Do not copy their topic list, count, domain names, or project structure.
- 状态图优先。Mermaid flowchart / sequenceDiagram 可作为普通流程图和时序图的主表达；ASCII 文本图 / 纯文本线框图用于状态机、复杂原理图和复杂示例图。不要把复杂流程画成 stacked box diagram / 阶段堆叠图。
- `critical` / `important` 核心流程必须闭合到业务终态，使用 Core Flow Overview / Boundary、Timeline / Sequence 主叙事和 ASCII State Machine，并通过 Flow Slice Coverage 追踪主路径、分支、失败和恢复。
- 模块及其他内容文档按真实边界、状态、时间、数据和恢复语义选图；stateless glossary、静态配置清单和纯索引不强制状态图。
- Onboarding Tasks are written only after the Onboarding Spec is accepted.
- Do not combine Onboarding Spec acceptance with the later Full Execution Gate.
- Onboarding Spec acceptance authorizes writing `onboarding-tasks.md`; formal module/flow execution starts only after the completed Tasks and Full Execution Gate receive separate human acceptance.
- Module and Flow docs default to single long files: `02-modules/<module-name>.md` and `03-flows/<flow-name>.md`.
- Full Execution Gate 确认后 Agent 可以全盘执行：Spec 先单独确认，Tasks 写完后再单独确认 Full Execution Gate，之后 Agent 可以一次性创建并连续完成计划内的完整 onboarding-db。
- batch 是 Agent 的组织和 review 单位，不是人类闸门；不要每批都停下来等人类再次授权，除非计划变更、证据不足、权限/环境阻塞或人类明确要求暂停。
- 禁止创建空目录、薄 README、planned/later 占位文件，或用文件数量假装完整。

Flow:

1. Confirm Project Entry Scan / reliable memory exists.
2. Build `08-review/evidence-graph.md` before formal onboarding docs; Build Core Flow Inventory with criticality, business terminals, variants, recovery ownership, evidence chain, and planned/deferred selection.
3. Draft `onboarding-spec.md` with module plan, Core Flow selection, Flow Slice Plan, DDD mapping, complexity-triggered Diagram Plan, file strategy, Completeness Hard Gate, quality gates, and batch plan.
4. Ask human confirmation for the Onboarding Spec.
5. After Spec acceptance, write `onboarding-tasks.md` with exact outputs, Flow/Slice/Diagram IDs, evidence, completeness and quality gates, and execution scope.
6. Present the completed Onboarding Tasks and ask separate human acceptance of the Full Execution Gate.
7. After Full Execution Gate acceptance, execute all planned docs that can be written with meaningful evidence-backed content. Do not create empty directories or placeholder docs.
8. Write module docs as `02-modules/<module-name>.md` by default, not many small files.
9. Write flow docs as `03-flows/<flow-name>.md` by default, not many small files.
10. Require the core flow diagram set for critical/important flows and relevant diagrams for other content docs. Use Mermaid flowchart / sequenceDiagram for normal flow/timing and ASCII for state machines, complex principle diagrams, and complex examples.
11. Require use cases, data objects, state transitions, failure modes, verification/troubleshooting, and code evidence where applicable.
12. Run Completeness Hard Gate before scoring changed topics in `coverage-matrix.md`; a missing critical slice cannot be averaged away, and below 4/5 cannot be `newcomer-ready`.
13. Record each batch in `batch-review.md`.

Exit:

- Onboarding Spec awaiting review
- next onboarding batch recommended
- focused update recommended
- Project Memory Update recommended only for stable facts that belong in `project.md`
- Pause or Close Onboarding Work after human confirmation

## Reconcile Project Context / Re-Adopt Agent Loop Project

Entry: `agent-loop` exists but memory appears stale, or the project previously used `agent-loop` and recent development bypassed it.

Inspect:

- `project.md`
- active feature docs
- obvious code reality: scripts, directories, README, current tests

Load `recovery-and-backfill.md` and `project-guidance.md` for every explicit re-adoption request. Also load `recovery-and-backfill.md` whenever code reality should repair project or feature docs.

For re-adoption, do not start new feature work first. Compare current code/tests/scripts with existing `agent-loop` docs, then propose backfill.

Output before writing:

- what appears stale
- what code reality shows
- which recent outside-loop changes appear relevant
- whether original human requirements conflict with code
- root `AGENTS.md` and `CLAUDE.md` guidance status, including whether `CLAUDE.md` points to `AGENTS.md`
- whether root `AGENTS.md` managed blocks are missing, stale, or different from the current root AGENTS template
- what should update
- what should stay unchanged

Write after confirmation:

- `project.md` and/or feature docs
- reconciliation note in `notes.md` when feature-specific
- root `AGENTS.md` / `CLAUDE.md` pointer only if startup guidance is missing, stale, duplicated, or human-confirmed for sync

Exit:

- memory and code reality are close enough to continue

## Requirement Archive

Entry: human provides requirement/prototype, points to existing material, or asks to remember future/deferred work.

Load:

- `requirement-management.md`

Rules:

- Ask before copying, moving, or renaming human files.
- Never silently modify original requirements.
- Do not edit `requirement.md` or other source files for lifecycle/status updates.
- Normalize names only after confirmation.
- Requirement archive dates are archive dates only, not deadlines or feature lifecycle dates.
- Use a requirement set directory with `README.md`; do not create new flat files directly under `.agent-loop/requirements/`.
- Group all materials from the same intake/topic together: requirement documents, prototypes, screenshots, feedback, recordings, links, and follow-up notes.
- Do not overwrite old requirement materials when requirements change.
- Old requirement set README files remain valid; do not require migration only because `Lifecycle`, `Summary`, or `Status History` is missing.
- Run Phase Scan for complex requirement archives. Recommend `Delivery Phases` in the requirement set `README.md` when the requirement will likely become multiple features, has MVP/later scope, crosses multiple boundaries, or needs staged human delivery confirmation.
- Do not create a feature merely because a phase exists. A phase becomes feature work only after the human chooses to start that accepted phase or phase slice.
- Before an accepted requirement enters feature construction, run Design Readiness Check from `project-decisions.md` and record the result in the requirement README.
- Before an accepted requirement enters feature construction, verify its requirement document records either `Concept Foundation Status: accepted` or a reasoned `concept-foundation-not-needed` when the method applies. Archival or requirement lifecycle acceptance does not bypass the Concept Foundation Gate.
- For archived sets, resolve README `Effective Concept Foundation` first and read the referenced human-reviewed source. If later evidence reopens semantics, stop response-locally, preserve old sources, run Requirement Conflict Review, and ask before an append-only follow-up / linked replacement plus README pointer update.
- Route to Decision & Design If Needed when the requirement spans features or needs shared business-flow, domain, state, source-of-truth, architecture, consistency, recovery, or non-functional design. A disputed technology choice is not required.

### Future / Deferred Requirement Intake

Use this sub-mode when the human says or implies "先记一下", "后面做", "之后补", "下一轮做", "暂时不做", "以后加", "backlog", "defer this", "follow-up later", or "not in this feature".

Rules:

- Do not write future TODO, backlog, deferred requirements, or unimplemented planned capability details into `project.md`.
- Recommend creating or updating a requirement set after human confirmation.
- Use `Status: proposed | accepted | deferred` based on the human decision; do not infer priority.
- Update `requirements/INDEX.md` only when it already exists, index triggers apply, or the human asks for a backlog/requirements inventory.
- If discovered during a feature, link the requirement set from `notes.md` and keep the current feature scope unchanged unless the human confirms scope change.

### Requirement Conflict Review

When follow-up material materially conflicts with an existing requirement, do not silently append it and do not edit source files.

Present original requirement summary, follow-up request summary, conflict table covering user goal, business rule, acceptance, out-of-scope, and existing feature impact, then recommend one action: append to existing set, create linked new set, or create a new requirement set and mark the old one superseded.

Ask human confirmation before creating the new set or changing lifecycle status.

Write:

- `.agent-loop/requirements/<archive-date>-<topic>/README.md`
- `.agent-loop/requirements/<archive-date>-<topic>/requirement.*` only when source material is provided or the human confirms creating a source record
- optional `.agent-loop/requirements/<archive-date>-<topic>/notes.phase-<n>-<slug>.md` when a phase needs a separate accepted note
- `.agent-loop/requirements/<archive-date>-<topic>/prototype.*` only when source material is provided or copied after confirmation
- optional feedback, screenshot, recording, design-link, meeting-note, and other source files inside the same requirement set
- optional change-request files inside the same requirement set
- optional `.agent-loop/requirements/INDEX.md` only when trigger conditions apply
- source references in an existing confirmed feature `spec.md` when the requirement was discovered during feature work; do not create a feature or `spec.md` from Requirements Discussion or Requirement Archive only to hold the link

Exit:

- requirements archived or original paths recorded

## Product Brief If Needed

Entry: accepted or referenced source requirements need feature-level product/PRD-style synthesis before engineering specification, and feature context is confirmed.

Product Brief Source Gate:

If the human asks from `chat` or `requirements-discussion` to write `product.md`, first ask whether to create/reference a requirement set or confirm feature start.

Do not enter Product Brief If Needed directly from requirements discussion without a requirement source or confirmed feature context.

Load:

- `product-brief.md`
- `requirement-product-grill.md` when product terminology, flows, boundaries, exception paths, or prior feature behavior need clarification before synthesis
- `project-decisions.md` when product tradeoffs or product decisions may affect multiple features or long-term project direction
- `skill-routing.md` for Stage Helper Capability Scan
- `external-skill-adapters.md` when Stage Helper Capability Scan finds Superpowers, PRD/product synthesis, or grill-with-docs style helpers

Trigger examples:

- meaningful user journey or UI/interaction flow
- prototype, product document, PRD, long requirement text, or design notes
- multiple actors, roles, permissions, tenants, or business objects
- likely 3 or more user stories
- scope and out-of-scope need product confirmation
- ambiguous business terminology

Rules:

- before fallback product synthesis, run Stage Helper Capability Scan; when a product/PRD helper is available, use it as the method quality bar while writing accepted output to `product.md` and `notes.md`
- confirm the source requirement and feature context before writing feature `product.md`; product-shaping confirmation alone is not feature-start confirmation
- resolve enough Requirement/Product Grill questions before synthesizing `product.md`
- resolve the accepted Concept Foundation and Requirement Product Model from README `Effective Concept Foundation` when present, otherwise from the backward-compatible source requirement; Product Brief consumes accepted Concept IDs/model rows and must not redefine their names, identity, relationships, lifecycle, invariants, or product fact meaning
- if the source foundation is `candidate` or `reopened`, return to Requirements Discussion instead of writing Product Brief
- record Accepted Concept References and Requirement Product Model Coverage in `product.md`; use `not-applicable` only when the source requirement has a reasoned `concept-foundation-not-needed`
- When Requirement/Product Grill was used before Product Brief, write the enriched `templates/product.md` sections that apply; use `Not applicable` plus a short reason instead of empty headings.
- create `product.md` only when useful; skip for narrow bugfixes or clear technical tasks
- if source requirements are still too broad for one feature, recommend returning to requirement `Delivery Phases` before writing `product.md`
- inspect `project.md` Product Context and Domain Language before asking product questions
- ask one blocking product question at a time
- include the agent's recommended answer when asking
- record long-term consensus candidates for Project Memory Update
- repeat Design Readiness Check for new product signals and route shared design needs through Decision & Design before Feature Spec

Write after confirmation:

- `product.md`
- `notes.md` human decisions if needed

Exit:

- product intent is stable enough for Feature Spec

## Decision & Design If Needed

Entry: Design Readiness is `required`, or accepted/referenced requirements, product.md, PRD-like synthesis, Requirement/Product Grill output, Technical Design / Code Context, or Drift Check reveals shared business-flow, domain, data, architecture, recovery, non-functional, cross-feature, or long-term design needs.

Load:

- `project-decisions.md`
- `document-templates.md`
- `human-review-summary.md` before asking the human to create, accept, supersede, deprecate, or reference project-level decisions

Position:

```text
Requirement -> Design Readiness Check -> Decision & Design If Needed -> Feature Mapping -> Product Brief / Feature Spec
```

Rules:

- run Design Readiness Check after requirement acceptance and before feature construction
- enter Decision & Design when a requirement is complex, likely to split into multiple features, changes an end-to-end business flow, shares domain/data/state rules, or needs common architecture, recovery, or non-functional direction
- do not bypass Decision & Design merely because no technology choice is disputed
- use Decision Scan / Placement inside this stage to place product-only, feature-local, testing, and project-level decisions
- do not create ADR files from ordinary chat or early fuzzy requirements discussion
- treat PRD / Requirement Product Model as the product-semantics authority; Decision & Design may consume accepted Concept IDs but must not redefine product identity, lifecycle, relationship, invariant, or terminal meaning
- resolve the requirement README effective-source pointer and record an Effective Requirement Snapshot before technical landing; a triggered Concept Foundation must be `accepted`
- inventory every stable source Requirement Model ID (`REL-*`, `PERM-*`, `CMD-*`, `EVT-*`, `FLOW-*`, `STATE-*`, `PM-*`, `EX-*`) before selecting the coherent ADR scope; every out-of-scope ID needs an explicit owner or reason
- record one Requirement Model Technical Landing Trace disposition for every accepted Requirement Model ID declared inside the ADR scope; `landed` rows require Technical Landing, Preserved Invariant, Design Slice, and Verification
- keep `Upstream Compatibility: review-required` as a blocking dependency judgment, not a decision lifecycle status; stop dependent Feature Spec, Plan, and implementation until compatibility review returns it to `current`
- requirement modeling does not add Concept-to-technical-representation mapping; technical landing remains inside the existing Human-gated Decision & Design record
- place product-only decisions in `product.md`
- place feature-local decisions in `spec.md` Design Decisions
- place testing decisions in `tests.md` unless they verify a long-term design goal
- recommend `.agent-loop/decisions/*.md` only for project / cross-feature, long-term, hard-to-reverse, surprising, or real-trade-off decisions
- creating `.agent-loop/decisions/` does not imply enterprise memory mode
- do not create, accept, supersede, deprecate, delete, or renumber decision files without explicit human confirmation
- convert every implementation-bearing shared flow step, invariant, recovery responsibility, and non-functional target into a stable Design Slice ID
- assign every required design slice to at least one planned feature; no required slice may remain `unassigned` before Feature Spec
- do not enter Feature Spec when required shared design is unresolved or design-slice coverage is incomplete
- do not accept an ADR while its Effective Requirement Snapshot is unresolved, its Requirement Model coverage is incomplete, or its compatibility is `review-required`
- run structural preflight while the draft remains `proposed`; only explicit human acceptance authorizes Human Review Evidence plus `Status: accepted`, followed by accepted-mode validation
- allow a reasoned `concept-foundation-not-needed` ADR to use the explicit trace-not-applicable path without inventing product models
- when upstream accepted meaning invalidates an accepted technical decision, preserve history and propose a superseding ADR; do not rewrite accepted decision meaning in place
- assess Migration / Backfill, Compatibility, Rollout / Cutover, and Rollback / Reversibility, but expand operational landing only for triggered concerns
- update requirement README, product.md, and spec.md decision references after human confirmation

Write after confirmation:

- conditionally required `.agent-loop/decisions/000N-<slug>.md` from `templates/decision.md` when shared design is required and no accepted decision covers it; otherwise no new file is needed
- requirement README `Applicable Decisions`, `Triggered Decisions`, and `Implemented By`
- feature `product.md` / `spec.md` `Applicable Decisions`
- feature `spec.md` `Implements Decisions`
- decision record `Design Slice Coverage` with stable slice IDs, planned owning features, verification, and coverage status
- decision record `Effective Requirement Snapshot`, source-wide `Requirement Model Scope Inventory`, `Requirement Model Technical Landing Trace`, Coverage Hard Gate evidence, Human Review Evidence after acceptance, and operational trigger assessment

Exit:

- Design Readiness records `design-not-needed`, or no new project-level design record is needed because accepted decisions already cover the requirement
- decision candidate stays in product.md, spec.md, tests.md, or notes.md
- decision draft is ready for human review
- Decision & Design Human Review Summary is ready with effective source, source-wide scope counts, coverage counts, preserved semantics, operational triggers, Design Slice ownership, verification, and explicit human decision
- accepted Decision & Design is compatible with the effective source, referenced by downstream feature artifacts, covers every in-scope Requirement Model ID, and gives every required design slice a planned owner

## Brainstorm / Clarify

Entry: goal is vague, scope unclear, or meaningful approaches differ.

Mandatory helper: Brainstorm / Clarify resolves and loads `superpowers:brainstorming` or `brainstorming` before clarification or design actions. Record Stage Helper Resolution; fallback requires `unavailable` or `load-failed`.

Load:

- `requirement-product-grill.md` when clarification is about domain terminology, business flow, prior feature conflict, or decision signal
- `skill-routing.md` for Stage Helper Capability Scan
- `external-skill-adapters.md` when Stage Helper Capability Scan finds Superpowers or another brainstorming/product-discovery skill

Rules:

- after mandatory helper resolution, use the loaded Brainstorming Adapter; use fallback only for recorded `unavailable` or `load-failed`, while writing accepted output to the current stage artifact. Requirements Discussion writes detailed output to `requirements/<set>/requirement.md` and summary links or lifecycle state to `README.md`; Product Brief writes `product.md`; Feature Spec writes `spec.md` and `notes.md`.
- Ask 1-5 high-impact questions.
- Default to one question at a time.
- Questions must affect scope, UX, data, architecture, testing, or acceptance.
- Do not ask filler questions.
- If a question can be answered by reading project docs, code, tests, source requirements, `project.md`, or `product.md`, inspect those first instead of asking the human.
- For grill questions, also inspect targeted prior feature artifacts when relevant; do not run a full feature scan.
- When product terminology is fuzzy or conflicts with `project.md` Domain Language, propose a canonical meaning and ask only if still ambiguous.
- When Concept Foundation is triggered, override the generic 1-5 question allowance: use the Human Grill Contract and ask exactly one downstream-blocking question per turn.

Write:

- Requirements Discussion: write approved clarification and design output to the requirement document; keep requirement README to source, lifecycle, Delivery Phase, Feature Mapping, and decision-link summaries.
- Product Brief: write accepted product clarifications into `product.md`.
- Feature Spec: write accepted engineering clarifications into `spec.md` and human decisions into `notes.md`.

Exit:

- Requirements Discussion: requirement document draft is ready for Human Review and Requirement Archive.
- Product Brief or Feature Spec: the owning artifact is stable enough for its next agent-loop stage.

## Feature Monthly Archive If Explicitly Requested

Entry: explicit archive/rehydrate request after reliable project memory.

Reads: `project.md`, `features/archive.md`, selected feature close artifacts, requirements, decisions, and Markdown references.

Writes: none during scan; confirmed month moves, `features/archive.md`, approved references, and a temporary transaction journal during apply.

Human Gate: exact plan SHA-256 Batch Review. Feature Auto-Loop and Task Auto-Run do not authorize archive or rehydrate.

Exit: verified archive/rehydrate, verified restore, or one blocker stage.

Next: Chat/report when complete; Ask Human for stale plan/scope; Recovery for stranded journal; Feature Follow-up after verified rehydrate.

Procedure:

1. Classify message intent as `feature-archive-maintenance`; require reliable Project Entry/memory and inspect incomplete `.archive-txn` before planning.
2. Run `scripts/scan-feature-monthly-archive.py` only. The scan is read-only and accepts explicit `--as-of`; it never uses current time implicitly.
3. Resolve stable Feature IDs through flat paths and `features/archive.md`. Active / blocked / paused features stay flat. Only `closed` features with a concrete `Archive Readiness` record, complete close evidence, no open follow-up, and no memory/reference blocker are eligible.
4. Present one Feature Monthly Archive Batch Human Review with operation, plan SHA-256, selected months/IDs, eligible/blocked candidates, moves, reference edits, preserved immutable/historical references, unchanged content, transaction/restore scope, platform evidence, and decision.
5. After exact confirmation, call apply with `--expected-plan-sha256`. A malformed hash is usage failure; a valid different hash is `stale-plan` and requires a fresh scan/review.
6. Apply uses the transaction journal before mutation, moves whole directories by rename, renders root `features/archive.md`, performs only precomputed reference edits, and runs the same post-check core. Original human requirement sources are not rewritten.
7. On failure, restore exact backups and reconcile every journal move from confined source/target state, including a rename completed just before its completion record was persisted. A stranded journal routes to Recovery with its exact transaction ID; never select the newest transaction automatically.
8. Rehydrate uses its own plan and Batch Human Gate, keeps `spec.md Status: closed`, and must complete before Feature Follow-up may reopen lifecycle or execute work.

Scope: no per-feature archive summary, no `historical/`, no Deep Archive, no deletion/packing/scheduled archive, and no `--force`.

## Feature Follow-up And Flow-back

Entry: human reports a bug, regression, post-close correction, field/schema change, algorithm change, API mismatch, test failure, QA/user feedback, or any change that may belong to existing Feature work.

Do not enter Feature Follow-up before Project Entry has established or verified agent-loop memory. If `.agent-loop/` or legacy `agent-loop/` is missing, preserve the report as intake context and route to Project Entry Scan or Init Project first.

Load:

- `feature-follow-up.md`
- `bug-management.md` for explicit bug-record, manage, investigate, or fix intent
- `human-review-summary.md` before Resolution Path, Bug close/reopen, Feature action, or Requirement action confirmation

Inspect:

- complete `bugs/INDEX.md` metadata and evidence-overlapping Bug README files before creating a Bug or scanning Feature ownership
- `project.md` Active Feature, Paused Features, configured `Feature Follow-up Lookback`, and Feature references
- Feature metadata/summary inside the default 90-day window before deep-reading evidence-ranked `spec.md`, `tasks.md`, `tests.md`, and `notes.md`
- `features/archive.md` locator and read-only archived Feature evidence when ownership points to a month path
- close records, submit records, verification evidence, and drift notes
- code paths, tests, APIs, data models, routes, jobs, UI pages, or contracts mentioned by the report

Bug Management internal sequence:

```text
complete Bug Index metadata scan
-> 90-day Feature metadata scan
-> evidence-ranked deep read / evidence-driven extended scan
-> create/update/reopen Bug Record
-> Expected Behavior check
-> Status/Resolution validation
-> one Resolution Path recommendation
-> Human Gate
```

Rules:

- Bug Management is internal to this stage; do not add a canonical stage or message intent
- ordinary Chat or read-only error explanation does not create a Bug artifact
- Bug identity / duplicate / reopen scans all Bug Index metadata without a time cutoff
- default Feature ownership is a 90-calendar-day metadata/summary scan; deep-read only evidence-overlapping candidates and extend beyond 90 days with `outside-default-window` evidence
- calculate age from Feature `Last Updated / Closed`, not archive month, directory mtime, or archive operation time
- code reality is current fact base for defect evidence
- original human requirements remain immutable
- do not default to creating a new Feature until Bug identity and candidate Feature ownership are checked
- do not infer identity/ownership from similar titles or generic 500/blank-page/unknown-error reports; keep `triaging` and recommend `investigate-first`
- present a Candidate Match Matrix before changing feature docs
- confirm Expected Behavior from accepted evidence; ambiguity/conflict returns to Requirements Discussion / Requirement Reconciliation / Decision & Design
- validate `Status` and `Resolution` separately; `closed+unresolved`, `deferred=closed`, duplicate cycles, or `in-progress` without one valid Resolution Path/Target stop in Recovery
- An `in-progress` Bug requires `flow-back | linked-feature | maintenance-fix` plus one Human-confirmed Fix Feature Target. `investigate-first`, `requirement`, and `no-fix` must not use `Status: in-progress`
- classify "字段改一下", "规则微调", "小改动", and similar wording by checking whether acceptance, API/event/data shape, state flow, algorithm result, or visible UX changes
- recommend exactly one `investigate-first | flow-back | linked-feature | maintenance-fix | requirement | no-fix` path with evidence and one Target when required
- Resolution Path confirmation does not create/reopen a Feature, change a Requirement, or authorize Bug close/Git action; request those named gates separately
- if a closed Feature is the likely owner, recommend `flow-back` and explain the separate Feature reopen gate
- for an archived owner, resolve/read evidence without rehydrate; only after confirmed `flow-back` and before reopened execution run the exact-hash Human-gated rehydrate
- if the human declines reopen or flow-back, preserve old close state and require the new linked feature or maintenance-fix to keep `Related Feature`, declined reason, inherited acceptance/tests/evidence, and affected paths
- if scope is new or ownership is weak, recommend a linked new feature or investigate-first path
- if no owning Feature exists and the work is a narrow internal fix, recommend a new `Feature Type: maintenance-fix` workspace instead of a naked code edit
- if multiple candidates have medium/high match because evidence is incomplete, recommend investigate-first and route to Targeted Feature Scan or Diagnose Failure
- ask the human only after evidence is sufficient and the remaining ambiguity is a product or ownership decision

Write after confirmation:

- `bugs/INDEX.md` plus Bug README for explicit Bug management; preserve Status/Reopen history append-only
- Follow-up Intake record in the owning feature `notes.md`, or in the new feature `notes.md` if a new feature is chosen
- new `.agent-loop/features/YYYY-MM-DD-fix-<slug>/` workspace with `Feature Type: maintenance-fix` when maintenance fix is confirmed
- updated `spec.md`, `tasks.md`, `tests.md`, and `plan.md` only as needed
- requirement archive/update only when product expectation is missing/changing or durable source material is separately confirmed; Bug links alone do not change lifecycle
- `project.md` Current Work when a closed feature is reopened or a new feature is created
- Delivery Contract updates only through the normal Delivery Contract gate

Exit:

- Human confirms the named Resolution Path and any separate Feature/Requirement action, or the Bug remains `triaging`/`deferred`
- next stage: Requirements Discussion, Requirement Archive/Reconciliation, Feature Spec update, Work Breakdown, Test Design, Targeted Feature Scan, Plan Gate, Diagnose Failure, Verify, or Recovery

## Feature Spec

Entry: goal and source requirements are clear enough.

Every feature start must reference an accepted requirement set. For a narrow direct feature request, create and accept the minimum requirement set before Feature Spec. This keeps Design Readiness, lifecycle, and Feature Mapping in one requirement-owned location without forcing a large PRD.

Load:

- `project.md` Decisions index and linked accepted decisions when present
- `project-decisions.md` when accepted requirements or product decisions have Decision Candidates, Applicable Decisions, or unresolved long-term/cross-feature choices
- `skill-routing.md` for Stage Helper Capability Scan
- `external-skill-adapters.md` when Stage Helper Capability Scan finds Superpowers, brainstorming, or another spec-writing helper

Write:

- feature workspace
- `spec.md` from template

Include:

- feature type: normal, maintenance-fix, or follow-up
- `Related Bugs` and the Human-confirmed Bug Resolution Path source when this Feature repairs Bugs; do not copy full Bug report/evidence
- problem/goal
- product brief reference when `product.md` exists
- requirement Delivery Phase reference when the feature implements a phase or phase slice
- scope
- stories
- acceptance criteria
- added/modified/removed behavior
- dependencies
- out of scope
- open questions

Rules:

- before fallback spec writing, run Stage Helper Capability Scan; when a spec/brainstorming helper is available, use it for ambiguity removal, scope checks, and acceptance thinking while writing to `spec.md`
- inspect Source Requirements, product.md, and Applicable Decisions before writing behavior and acceptance
- resolve and inspect the effective accepted Concept Foundation and Requirement Product Model before writing behavior and acceptance; add Effective Concept Source, Accepted Concept References, and Requirement Product Model Trace to `spec.md`
- do not let Feature Spec introduce a new meaning, state, invariant, role boundary, relationship, or product object for an accepted Concept ID; return to Requirements Discussion when product semantics must change
- block Feature Spec when a triggered source foundation is `candidate` or `reopened`
- confirm Design Readiness is `design-not-needed` or `completed` before writing the Feature Spec
- for each applicable requirement-driven ADR, confirm its Effective Requirement Snapshot still resolves, `Upstream Compatibility` is `current`, and Requirement Model Technical Landing Trace coverage is complete
- include `Applicable Decisions`, assigned Design Slice IDs in `Implements Decisions`, and feature-local `Design Decisions`
- use Decision & Design before Feature Spec if the requirement needs shared business-flow, domain, data, architecture, recovery, or non-functional design
- do not enter Feature Spec when shared design is unresolved or any required design slice is unassigned
- do not treat `Applicable Decisions` alone as coverage; block when an in-scope Requirement Model ID lacks disposition, technical ownership, or verification
- a Bug relationship does not replace the accepted Requirement/Expected Behavior source and does not authorize Feature creation, Requirement change, or Bug close

Exit:

- draft spec is ready for Requirement Checklist or requires revision

## Targeted Feature Scan

Entry: existing project has reliable project memory and the human selected a feature, but the affected boundaries are not yet understood.

Load:

- `project-entry-scan.md`
- `large-projects.md` for old, large, or multi-package projects

Inspect only feature-relevant areas:

- keywords from the human goal and draft spec
- related routes/controllers/pages/actions
- related domain/core modules
- related schema/model/migration files
- related tests and E2E specs
- related guidance docs and directory `AGENTS.md`

Write after confirmation:

- feature-specific findings into `spec.md`, `tasks.md`, `tests.md`, or `notes.md`
- lasting project facts into `project.md` only after human confirmation

Exit:

- affected boundaries are clear enough for Work Breakdown or Test Design

## Requirement Checklist

Entry: draft spec exists.

Check:

- no major ambiguity
- stories independently testable
- acceptance criteria measurable
- behavior changes clear
- edge cases and out-of-scope recorded

Write:

- checklist result in `tests.md` or `notes.md`
- spec updates if human confirms

Exit:

- human accepts the checked spec or requests revision
- accepted spec and recorded passed Requirement Checklist are ready for Work Breakdown
- after acceptance, explain that Strict Mode asks before each stage and offer Feature Auto-Loop for Agent-ready downstream work if the human wants fewer confirmations

## Work Breakdown

Entry: accepted spec with a recorded passed Requirement Checklist.

Helper-friendly stage: Work Breakdown runs Stage Helper Capability Scan before fallback. Use matching issue/task splitting helpers as method support only; keep `tasks.md`, task status, gates, and next-stage routing under agent-loop control.

Write:

- `tasks.md`

Rules:

- default to vertical slices / tracer bullets
- each normal task should form a narrow verifiable loop through the necessary layers
- allow horizontal foundation tasks only when a verifiable product slice is not yet possible
- every horizontal foundation task must explain why it cannot be vertical and which future vertical slices will prove it
- task IDs use `T001`
- story labels use `US1`
- use linear/parallel/barrier only
- include verification hints
- mark each task `Agent-ready` or `Human-gated`
- use `Human-gated` when product, design, architecture, security, data, or approval decisions are still needed
- use `Agent-ready` only when acceptance, boundaries, and verification are clear enough for autonomous execution
- for large projects, group tasks by stage and barrier in a single `tasks.md`
- if stories > 3, pause and assess whether Complex Artifact Mode is needed
- if complex artifact semantics may apply, load `complex-artifacts.md` and propose `tasks/`, `tests/`, and/or `plans/` detail files only for the parts that need detail
- Do not use story count, task count, test count, or ordinary file count as a hard recommendation trigger
- for Complex Artifact Mode, recommend only when the feature is no longer locally understandable or executable inside one cohesive area because it spans multiple collaborating modules, services, workflows, ownership lanes, or release/operation concerns
- detect likely durable producer-consumer boundaries such as API, event, public data, UI state/behavior, SDK/library, or runtime interfaces
- when a durable producer-consumer boundary likely exists, recommend Delivery Contract If Needed with a reason before downstream implementation relies on assumptions

Exit:

- human accepts granularity and order
- in Feature Auto-Loop, continue automatically only if remaining tasks are Agent-ready and no stop condition appears

## Delivery Contract If Needed

Entry: the human requests frontend/backend handoff, API/interface documentation, an API contract, or material for another agent/person to continue downstream work; or accepted spec/tasks, Technical Design, Review, or Drift Check reveal a likely durable producer-consumer boundary.

Load:

- `delivery-contracts.md`

Detect:

- frontend/client consuming backend API behavior
- service-to-service endpoint
- event, message, webhook, callback, or async workflow
- shared data exchange schema
- UI behavior handed from product/design/backend to frontend
- public library/plugin API
- runtime, deployment, environment-variable, or external integration boundary

Write after confirmation:

- `contracts.md`
- optional `contracts/<ID>-<slug>.md` details
- human decisions and drift notes in `notes.md`

Rules:

- keep temporary subagent assignment notes in `handoffs/`; do not use them as durable interface docs
- Delivery Contracts are not default feature artifacts
- skip Delivery Contracts for simple single-person tasks, pure internal logic, or changes with no downstream consumer
- agent proactively recommends a Delivery Contract; the human does not need to request one by name
- ask before writing contract files in every mode, including Feature Auto-Loop and Task Auto-Run
- human confirmation is required before status becomes `accepted`
- human confirmation after affected-consumer analysis is required before changing producer code, tests, or contract files for any breaking change to accepted, implemented, or verified contracts
- creating a new `draft` or `superseded` contract cannot bypass the breaking-change gate when existing consumers would observe changed behavior
- producer implementation and tests must verify the accepted contract before downstream reliance or feature close

Exit:

- no contract needed, or contract draft is ready for human decision
- accepted contract is concrete enough for Test Design and Technical Design / Code Context

## Test Design

Entry: accepted tasks.

Helper-friendly stage: Test Design runs Stage Helper Capability Scan before fallback. Use matching test-design helpers as method support only; keep `tests.md`, required verification applicability, substitute-verification gates, and next-stage routing under agent-loop control.

Write:

- `tests.md`

Include:

- requirement checklist
- functional cases
- module tests
- API tests where applicable
- Web E2E/browser cases where applicable, after loading `e2e-discovery.md`
- regression tests
- manual verification
- commands
- detail test-case files under `tests/` only when test details need splitting after Complex Artifact confirmation
- Bug Verification Matrix when the Feature resolves Bug Records: Bug ID, Expected Behavior Evidence, original reproduction or accepted substitute, regression/safety verification, result, and evidence link

Rules:

- do not assume an E2E framework, local URL, account, seed, or browser tool
- if web-visible behavior exists, run E2E Discovery first
- if a task changes HTTP/API behavior, service-to-service behavior, events, background jobs, auth, persistence, or integration boundaries, API/integration verification is applicable unless a human approves a substitute verification
- if a task changes user-visible Web behavior, E2E/browser/manual verification is applicable unless a human approves a substitute verification
- Feature-wide tests do not automatically satisfy Bug-specific acceptance or the Bug Close Gate
- substitute verification requires a recorded reason, risk, missing capability, and human decision; it cannot silently replace required API/E2E coverage
- record stable E2E capability in `project.md`
- record feature-specific E2E cases in `tests.md` or `tests/e2e/*`
- classify E2E cases as existing-framework, browser, chrome, computer-use, manual, or blocked

Exit:

- human accepts how correctness will be proven
- in Feature Auto-Loop, continue automatically only if the test strategy has no unresolved human decisions

## E2E Discovery if Web

Entry: web-visible behavior exists, executable E2E/browser verification may be applicable, or Test Design cannot safely define Web E2E cases from current project memory.

Helper-friendly stage: E2E Discovery if Web runs Stage Helper Capability Scan before fallback. Use matching browser/E2E environment helpers as method support only; keep discovered project-level capability in `project.md` and feature-specific cases in `tests.md` or `tests/e2e/*`.

Load:

- `e2e-discovery.md`

Exit:

- E2E path is classified as existing-framework, browser, chrome, computer-use, manual, or blocked
- next stage: Test Design when E2E cases still need recording, or Technical Design / Code Context when test strategy is accepted

## Technical Design / Code Context

Entry: accepted tasks and tests, before writing `plan.md` or executing a non-trivial task/story.

Helper-friendly stage: Technical Design / Code Context runs Stage Helper Capability Scan before fallback. Use matching codebase-scan or technical-planning helpers as method support only; keep code context, interface decisions, plan readiness, and human gates under agent-loop control.

Load:

- `implementation-planning.md`
- `project-decisions.md` when implementation design introduces long-term/cross-feature boundaries, dependencies, data ownership, transaction, consistency, concurrency, idempotency, or recovery choices
- `large-projects.md` for large, old, or multi-package projects
- nearest root/directory `AGENTS.md`
- relevant accepted or verified Delivery Contracts when the task crosses a producer-consumer boundary

Inspect:

- exact files likely to change
- nearby tests and fixtures
- existing functions, classes, endpoints, components, schemas, hooks, or commands
- imported helpers and existing callers
- data flow, call chain, authorization, validation, and side effects
- existing code style and error-handling patterns

Write:

- update task detail under `tasks/US<n>/T<nnn>-<slug>.md` only when task context needs splitting after Complex Artifact confirmation
- otherwise record compact code context in `plan.md`
- unresolved technical questions in `notes.md`

Rules:

- do not invent function signatures, parameters, return shapes, or file paths
- if the context cannot be discovered from code/docs, stop and ask or mark the task `Human-gated`
- prefer existing local patterns over new abstractions
- if an interface will be created, define it explicitly before implementation
- if a durable consumer-facing interface is created or changed, recommend Delivery Contract If Needed and stop before any contract file is created or updated
- do not create or update contract files from Technical Design / Code Context; only the human-confirmed Delivery Contract stage may write them
- if technical design changes shared or project-level design, repeat Design Readiness and return to Decision & Design before plan execution
- if the effective requirement source changed or an applicable ADR is `review-required`, stop before Plan and return to Decision & Design compatibility review
- if an adopted branch strategy applies, resolve Current Branch Context from the accepted Target Release Context and Git evidence; stop rather than inventing target kind, version, customer slug, source branch, or target branch
- a planned branch name or target does not authorize create, switch, merge, delete, push, tag, release, or publish

Exit:

- code context is concrete enough for a construction-grade plan, or the task becomes Human-gated

## Plan Gate / Plan If Needed

Entry: selected task/story has accepted tasks and tests, and Technical Design / Code Context has enough evidence to decide whether a construction plan is required.

Mandatory helper: Plan Gate / Plan If Needed resolves and loads `superpowers:writing-plans` or `writing-plans` before writing, approving, or recording a No-Plan Decision. Record Stage Helper Resolution; fallback requires `unavailable` or `load-failed`.

This is a mandatory gate before Execute Task / Story. Do not create tasks and then immediately implement.

Load:

- `implementation-planning.md`
- `skill-routing.md` for Stage Helper Capability Scan
- `external-skill-adapters.md` when Stage Helper Capability Scan finds Superpowers or another plan-writing skill

Write one of:

- `plan.md`
- No-Plan Decision in `notes.md` and the selected task row/detail

Rules:

- decide whether a plan is required before any code implementation
- create `plan.md` when the task/story is complex, multi-file, changes behavior, changes tests, touches interfaces, crosses module boundaries, involves data/API/async/security/deployment behavior, needs TDD design, needs subagents, or the human asks for a plan
- a No-Plan Decision is allowed only for a trivial, low-risk, single-file or documentation-only task with clear acceptance, exact files, and exact verification command
- in Strict Mode, ask human confirmation before executing from a No-Plan Decision
- in Feature Auto-Loop, a No-Plan Decision may proceed only if the task is Agent-ready and no plan trigger applies
- Task Auto-Run always requires an accepted task/story plan; No-Plan Decision cannot enable Task Auto-Run
- plan scope is `task` or `story`
- default scope is task
- assume the executor has near-zero codebase context
- include technical context, source structure decision, code context, interface contracts, data contracts when applicable, files, TDD plan, commands, expected outputs, risks
- include `Branch Context Evidence` when an adopted strategy or versioned delivery applies: cite the complete `notes.md` Current Branch Context and repeat only Branch Strategy status/profile, Target Release Context, Target Branch, sealed/customer-isolation results, and `Git actions authorized by this plan: none`
- when repair work applies, cite `Bug Context Evidence` and Related Bug IDs; do not repeat Bug lifecycle or move tasks/tests/implementation into the Bug directory
- unresolved Bug identity, Expected Behavior, Resolution Path/Target, or archived Feature locator blocks Plan acceptance and returns to Bug Management / Recovery
- Plan approval never authorizes Bug close/reopen, Feature creation/reopen, or Requirement change
- reject a plan that targets a `released / sealed` version, crosses customer isolation, or assumes an unauthorized Git action
- include actual test code for RED steps when possible
- include exact function/class/endpoint/component signatures, parameters, return values, errors, and side effects for new or changed interfaces
- include exact commands and expected RED/GREEN output
- implementation steps must be bite-sized and executable
- no placeholders such as TBD, TODO, "add proper error handling", "write tests", or "similar to previous task"
- run plan self-review: spec coverage, placeholder scan, and type/signature consistency
- after mandatory helper resolution, use the loaded Writing-Plans Adapter quality bar; use fallback only for recorded `unavailable` or `load-failed`, and always write to `plan.md` or `plans/*`, not external docs paths
- if plan detail needs splitting after Complex Artifact confirmation, write the full dated plan to `plans/` and keep `plan.md` as the current pointer

Exit:

- human accepts plan, or human accepts/Feature Auto-Loop records the No-Plan Decision
- after acceptance, explain that Strict Mode asks before each stage and offer Task Auto-Run for this task/story if the human wants fewer confirmations

## Analyze Consistency

Entry: before implementation when spec/tasks/tests and either plan or a recorded No-Plan Decision exist.

Check:

- each accepted requirement has task coverage
- each task maps to spec or explicit technical need
- tests cover acceptance criteria
- plan scope matches selected task/story, or No-Plan Decision is limited to a trivial task with exact files and verification
- each accepted Decision & Design slice assigned to the feature maps through `spec.md`, tasks, tests, and the active plan
- no assigned design slice lacks an implementation or verification path, even when every local story is independently testable

Write:

- findings in `notes.md`
- update docs only after confirmation

Exit:

- ready for execution or revise upstream docs

## Subagent Execution If Approved

Entry: human explicitly approves subagent use for an independent task/story group, Project Entry Scan lane, or bounded implementation lane.

Mandatory helper: Subagent Execution If Approved resolves and loads `superpowers:subagent-driven-development` or `subagent-driven-development` after human approval and before dispatch. Record Stage Helper Resolution; helper availability never replaces subagent authorization.

Load:

- `skill-routing.md`
- `external-skill-adapters.md`
- `templates/subagent-brief.md`

Rules:

- after explicit human approval and mandatory helper resolution, use the loaded `subagent-driven-development` helper; use fallback only for recorded `unavailable` or `load-failed`
- subagents are optional and never implied by task count alone
- ask human confirmation before dispatching subagents
- Feature Auto-Loop or Task Auto-Run approval is not subagent approval
- one confirmation may cover a bounded task group only after listing task/story IDs or scan lanes, allowed boundaries, one brief per subagent, stop conditions, and main-agent review responsibility
- record the approval date, approved IDs/lanes, allowed boundaries, and stop conditions in `notes.md` and each brief; any new task, lane, file boundary, or expanded scope requires new human confirmation
- verify authorization is `active` immediately before dispatch; reject `consumed`, `revoked`, or `expired` authorization even for the same scope, and mark it `consumed` when the approved dispatch group returns or stops
- verify tasks or scan lanes are independent, bounded, and reviewable by the main agent
- create one clear brief per subagent using `templates/subagent-brief.md`
- write briefs and returned summaries under `handoffs/*`
- main agent owns synthesis, review, merge decisions, and status updates
- subagents may not close a feature, submit code, update project memory directly, accept Delivery Contracts, approve breaking changes, or mark tasks `done`
- if independence, boundaries, or review responsibility are unclear, do not dispatch; continue single-agent execution or mark the work `Human-gated`

Write:

- `handoffs/<date>-<task-or-scan>-brief.md`
- `handoffs/<date>-<task-or-scan>-return.md`
- summary and evidence links in `notes.md`
- `tasks.md` status updates only after main-agent review

Exit:

- returned work reviewed and merged into agent-loop artifacts
- or subagent path declined/blocked and execution returns to single-agent mode

## Execute Task / Story

Entry: selected execution unit is accepted, Plan Gate has passed, and Analyze Consistency has a clean recorded result.

Mandatory helper: Execute Task / Story resolves and loads `superpowers:test-driven-development` or `test-driven-development` before every Execute invocation. Record Stage Helper Resolution; fallback requires `unavailable` or `load-failed`. For non-behavior work, record TDD as `not-applicable` with a reason after resolution.

Rules:

- default unit is task
- story execution requires explicit human choice
- whole-feature execution requires explicit human confirmation and only for tiny features
- do not execute a task directly after task creation; first confirm accepted plan or recorded No-Plan Decision
- if neither accepted plan nor No-Plan Decision exists, route back to Plan Gate / Plan If Needed
- if Analyze Consistency is missing, stale, or reports a gap, route back to Analyze Consistency and do not execute
- when an adopted strategy applies, recheck Current Branch Context against Target Release Context and current Git evidence before execution; stop on drift, sealed target, or customer-boundary mismatch
- do not create or switch branches as an implied Execute step; either action requires a Branch Action Gate for one exact development branch
- Task Auto-Run requires an accepted plan for the selected task/story
- in Feature Auto-Loop, execute only Agent-ready tasks and stop at Human-gated tasks
- in Task Auto-Run, execute only the selected task/story and stop after evidence/review/drift updates and Task Done Gate status update
- behavior-changing execution requires TDD; non-behavior work records TDD as `not-applicable`
- after mandatory helper resolution, use the loaded TDD Adapter; use fallback only for recorded `unavailable` or `load-failed`, while task status and evidence remain controlled by agent-loop
- verify RED before implementation
- verify GREEN after implementation
- record evidence
- after implementation and all applicable fresh verification, set task status to `review`, not `done`
- if only partial verification ran, keep the task `in-progress` or `blocked` and record the missing verification
- mark task `done` only after Task Done Gate passes: evidence recorded, required review recorded, drift decision recorded, and task status linked to evidence

Write:

- code/tests
- `tasks.md` status
- `notes.md` TDD cycles and evidence
- `notes.md` review and drift records before `done`

Exit:

- execution unit in review, done, blocked, or needs diagnosis

## Diagnose Failure

Entry: test/build/E2E/behavior failure.

Mandatory helper: Diagnose Failure resolves and loads `superpowers:systematic-debugging` or `systematic-debugging` before proposing or applying a fix. Record Stage Helper Resolution; fallback requires `unavailable` or `load-failed`.

Load:

- `skill-routing.md` for Stage Helper Capability Scan
- `external-skill-adapters.md` when Stage Helper Capability Scan finds Superpowers or another systematic debugging skill

Rules:

- after mandatory helper resolution, use the loaded Debugging Adapter; use fallback only for recorded `unavailable` or `load-failed`, and find root cause before proposing fixes
- reproduce before fixing
- find root cause
- form one hypothesis at a time
- write regression test when possible

Write:

- diagnosis in `notes.md`

Exit:

- fix verified or blocker escalated

## Verify

Entry: before any completion claim.

Mandatory helper: Verify resolves and loads `superpowers:verification-before-completion` or `verification-before-completion` before any passed, fixed, complete, or ready claim. Record Stage Helper Resolution; fallback requires `unavailable` or `load-failed`.

Load:

- `skill-routing.md` for Stage Helper Capability Scan
- `external-skill-adapters.md` when Stage Helper Capability Scan finds Superpowers or another verification skill

Rules:

- after mandatory helper resolution, use the loaded verification adapter; use fallback only for recorded `unavailable` or `load-failed`, while completion remains controlled by agent-loop
- identify proof command/action
- run fresh verification
- read output
- record evidence
- when the Feature resolves Bugs, execute the Bug Verification Matrix against the original reproduction or accepted substitute and regression/safety paths
- after Feature evidence exists, move a related repair Bug from `in-progress` to `verifying`; do not set `closed`
- failed Bug-specific verification returns the Bug to `in-progress` when the repair remains valid or `triaging` when Expected Behavior/diagnosis was invalidated; append the failure evidence

Write:

- `notes.md` verification evidence
- related Bug README verification evidence and Status History, plus the matching `bugs/INDEX.md` row

Exit:

- claim may be made only if evidence supports it
- if the feature may now be complete, continue to Review, Drift Check, Project Memory Update, then Feature Completion Check

## Review

Entry: after implementation and verification, before any task is marked `done`, before Submit / Integrate, and before recommending or performing feature close.

Mandatory helper: Review resolves and loads `superpowers:requesting-code-review` or `requesting-code-review` before task review, Submit / Integrate review, or Feature Close Review. Record Stage Helper Resolution; helper approval cannot bypass Task Done Gate or Feature Close Review.

Create a separate Stage Helper Resolution for each task review, submit review, and feature-close-review invocation scope. Do not reuse a previous review resolution. Feature Close Review requires a fresh resolution and current helper instructions.

Load:

- `skill-routing.md` for Stage Helper Capability Scan
- `external-skill-adapters.md` when Stage Helper Capability Scan finds Superpowers or another code-review skill

Check:

- Spec Review: implementation matches `product.md` when present, `spec.md`, acceptance criteria, scope, and out-of-scope
- Decision & Design Review: implementation matches accepted Decision & Design records and every design slice assigned to this feature has current evidence
- Standards Review: implementation follows root/directory `AGENTS.md`, `project.md` rules, directory boundaries, testing rules, and local code conventions
- test adequacy
- integration risk
- unrelated changes
- Delivery Contract alignment when producer-consumer boundaries exist

Rules:

- after mandatory helper resolution, use the loaded review adapter; use fallback only for recorded `unavailable` or `load-failed`, and record findings in `notes.md` without directly marking tasks `done`
- perform lightweight Spec Review for every task before marking it `done`
- Review implementation against accepted Decision & Design records and the design slices assigned to this feature.
- perform Feature Close Review before recommending or performing close
- Feature Close Review includes feature-level Spec Review against product/spec/tasks/tests/acceptance/out-of-scope
- before Submit / Integrate, perform at least Spec Review
- perform Standards Review for large projects, broad diffs, directory or durable boundary changes, security/data changes, architecture changes, or human request
- perform feature-level Standards Review before close when the feature is large, broad, directory-boundary-changing, durable-boundary-changing, security/data-related, architecture-changing, or human-requested
- record the two axes separately so one does not hide the other
- review approval alone is insufficient to mark a task `done`; Task Done Gate evidence, required review, and drift decision must also be recorded
- if required review is missing, the task remains `review`; do not mark it `done`
- compare producer code and tests with Delivery Contracts; identify affected consumers before accepting interface drift

Write:

- task review findings and accepted fixes in `notes.md` under Spec Review and Standards Review
- close review findings and accepted fixes in `notes.md` under Feature Close Review

Exit:

- continue to Drift Check, revise implementation, or diagnose failures

## Drift Check

Entry: after implementation or before close.

Check:

- implementation vs `spec.md`
- completed work vs `tasks.md`
- test reality vs `tests.md`
- long-term changes vs `project.md`
- long-term/cross-feature decision reality vs `.agent-loop/decisions/` when present
- assigned Design Slice IDs vs implementation and verification evidence
- applicable ADR Effective Requirement Snapshot / Requirement Model Technical Landing Trace vs the current effective source, implementation, and verification evidence
- producer-consumer interfaces vs `contracts.md` and linked `contracts/*` details when present
- human original requirements vs current implementation when relevant
- whether long-term startup guidance changed and `AGENTS.md` should be synced
- when an adopted Branch Strategy or versioned/customer delivery applies, compare accepted Branch Strategy and Target Release Context vs feature Current Branch Context and current Git reality
- in that applicable context, check sealed-release immutability, customer isolation, and whether any proposed cleanup has merge evidence plus separate human authorization; a confirmed simple `not-needed` path records these branch-specific checks as `not-applicable`
- related Bug Expected Behavior, Resolution Path, Fix Feature, Status/Resolution, and verification/close evidence against Feature and Requirement/ADR/Contract authorities

Write after confirmation:

- feature docs for feature drift
- `project.md` for long-term project facts
- `.agent-loop/decisions/*.md` reference backfill, new decision draft, or superseding decision draft only after human confirmation
- Decision & Design coverage-status updates after confirming implementation evidence; route design divergence back to Decision & Design before close
- compatibility-review updates only after Human Review; create a superseding ADR when accepted decision meaning or technical conclusions no longer hold instead of rewriting the accepted record
- `notes.md` drift record
- `contracts.md` and matching `contracts/*` details for interface drift; ask before accepting breaking changes
- `AGENTS.md` / `CLAUDE.md` only for long-term guidance changes
- Bug README/Index links and evidence when facts changed; Expected Behavior conflicts route to Requirements Discussion / Requirement Reconciliation / Decision & Design instead of silently redefining the Bug or Requirement

Exit:

- docs and code reality aligned enough for the next lifecycle gate
- Drift Check does not route directly to Close
- when Bug Expected Behavior or its accepted product/design authority changed, route first to Requirements Discussion / Requirement Reconciliation / Decision & Design as applicable
- next stage: Project Memory Update / Requirement Reconciliation when long-term project facts, requirement lifecycle, Delivery Phase status, or Feature Mapping changed; otherwise Feature Completion Check

## Project Memory Update

Entry: after Drift Check, before Submit / Integrate, Pause, or Close when long-term project facts, requirement lifecycle, Delivery Phase status, or Feature Mapping changed.

Load:

- `project-memory-mode.md`

Update only durable project facts:

- current work and next suggested action
- active or paused feature pointers
- product context when feature product decisions affect future features
- capabilities that now exist or changed
- tech stack, commands, or tooling changes
- directory map or guidance status changes
- domain language that future feature work should reuse
- known constraints and long-term decisions
- Project Entry uncertainties resolved by code reality
- human-confirmed Branch Strategy outcome and current Target Release Context pointer; keep mutable development-branch lifecycle in feature artifacts

Do not write:

- task execution logs
- raw test output
- temporary implementation notes
- original human requirements or prototypes
- future TODO, backlog, deferred requirements, or unimplemented planned capability details
- Bug backlog, Bug evidence, triage state, Status/Resolution rows, or assignment-like data; these belong in `bugs/INDEX.md` and Bug README files

Requirement Reconciliation:

- If a feature references requirement sets, apply the Delivery Phase Status Roll-up from `requirement-management.md`; check whether lifecycle status should become `in-progress`, `partially-implemented`, `implemented`, `superseded`, `rejected`, or remain unchanged.
- If the requirement set uses `Delivery Phases`, check whether the referenced phase status and `Feature Mapping` should become `in-progress`, `implemented`, `superseded`, `rejected`, `deferred`, or remain unchanged.
- If the feature implements a Delivery Phase but `Feature Mapping` is still `none`, propose a requirement README backfill even when no `project.md` facts changed.
- Do not edit `requirement.md` or other source files for lifecycle/status updates.
- Write requirement lifecycle/status, Delivery Phase status, and Feature Mapping changes to requirement set `README.md` and optional `requirements/INDEX.md` after human confirmation.
- Write implemented capabilities to `project.md` only when they are durable project facts.
- Write deferred or future work to requirements, not project memory.
- A Bug relationship alone does not trigger lifecycle change. Reconcile only when current evidence shows delivery truth is inaccurate, and wait for the named Human Gate.

Write after confirmation:

- `project.md` in simple mode
- `project.md` plus the matching `project/*.md` detail files in enterprise mode
- root or directory `AGENTS.md` only if startup guidance changed and human confirms

Exit:

- future agents can resume from `project.md` and, in enterprise mode, only the linked detail files relevant to the next stage

## Submit / Integrate

Entry: after Verify, Review, Drift Check, and Project Memory Update when human asks to submit, commit, prepare PR text, or package work for integration.

Load:

- `submit-and-integrate.md`
- `skill-routing.md` for Stage Helper Capability Scan
- `external-skill-adapters.md` when Stage Helper Capability Scan finds Superpowers or another finishing/branch skill

Rules:

- before fallback submit/integrate preparation, run Stage Helper Capability Scan; when Superpowers finishing or another branch helper is available, use it only for completion options and branch hygiene
- inspect diff and untracked files
- separate product code changes from `agent-loop` artifact changes
- identify unrelated dirty work
- if using an external finishing skill, use it only for completion options and branch hygiene; agent-loop still owns the submit gate
- never commit, create final PR text, merge, release, publish, or claim submission readiness without human confirmation
- a human saying "commit" starts Submit / Integrate but is not final commit approval; ask again after diff, verification, review, and drift summary
- default to prepare-only if the human has not explicitly requested commit/PR/merge
- when an adopted Branch Strategy or versioned/customer delivery applies, run Branch Strategy Check and verify Source Branch, Branch Class, Target Release Context, Target Branch, sealed state, customer isolation, and requested Git action before asking for the final submit decision
- for a confirmed simple `not-needed` path, record branch-specific fields as `not-applicable` and do not block Submit / Integrate because Target Release Context or Target Branch is absent
- accepted strategy, an accepted plan, and a submit request never imply authorization for create, switch, merge, delete, push, tag, release, or publish
- temporary development-branch deletion requires merge evidence and a separate human cleanup decision; retained standard/customer aggregation branches are not cleanup candidates
- when the Feature resolves Bugs, show Bug IDs, current Status, Bug-specific verification evidence, unresolved Bug Close Decisions, Target Release Context, and branch isolation
- Submit/commit/push approval never closes a Bug, and Bug Close approval never authorizes Submit / Integrate
- after a stable verified code merge, when Source and Target Agent Loop memory changed or may differ, run Post-Merge Memory Reconciliation as an internal Submit / Integrate method; load `memory-reconciliation.md`
- stop at the Start Human Gate before report creation, then at the exact Plan Hash Gate before Apply; `待确认`, `已恢复`, stale evidence, or an unresolved transaction routes to Recovery and blocks Memory Commit, push, release/publish, and Source cleanup
- a completed Memory Merge Report permits only the next separately authorized Memory Commit or later Git gate; code merge, submit, auto-mode, or helper approval does not satisfy any reconciliation/Git gate

Write after confirmation:

- `notes.md` submit/integrate record
- current Memory Merge Report locator/status/blocker in `project.md` Current Work only when reconciliation applies; detailed ledger and transaction evidence stay in the report
- commit only if explicitly confirmed

Exit, in order:

1. If submission is prepare-only and was not performed, recommend Pause with the pending submit action.
2. If submission was explicitly skipped, record that decision; recommend Feature Completion Check when done, otherwise the next task/story.
3. Otherwise, if submit succeeded and the feature appears done, recommend Feature Completion Check, not Close.
4. Otherwise, if work remains, recommend the next task/story.
5. If submit failed or is blocked, recommend exactly one unblock stage.

## Feature Completion Check

Entry: after Verify/Review/Drift Check/Project Memory Update when a feature may be done; before starting a new feature while another is active; or on resume when an Active Feature exists.

Load:

- `feature-completion-check.md`
- `skill-routing.md` for Stage Helper Capability Scan
- `external-skill-adapters.md` when Stage Helper Capability Scan finds Superpowers verification, review, finishing, or close-decision helpers

Read:

- `project.md` Current Work
- active feature `spec.md`
- active feature `tasks.md`
- active feature `tests.md`
- active feature `plan.md`
- active feature `notes.md`
- accepted Decision & Design records linked by the active feature
- related Bug README files and `bugs/INDEX.md` rows when the Feature resolves Bugs

Check:

- before fallback completion analysis, run Stage Helper Capability Scan; when a matching verification/review/finishing helper is available, use it for evidence discipline and close decision support while keeping feature close under agent-loop control
- accepted spec
- all remaining in-scope tasks are done; skipped or deferred work was first removed through human-approved scope reconciliation
- required tests or substitute verification recorded
- fresh verification evidence exists
- Feature Close Review completed
- feature-level Spec Review confirms product/spec/tasks/tests/acceptance and out-of-scope boundaries
- feature-level Standards Review completed when triggered by large project, broad diff, directory or durable boundary change, security/data change, architecture change, or human request
- drift check completed
- all assigned design slices have implementation and verification evidence, or a human-approved reassignment, deferral, removal, or superseding decision
- long-term memory updated
- submit/integration status recorded when requested
- no unresolved Human-gated decisions or blockers
- every related Bug expected to be fixed is `verifying` with fresh Bug-specific evidence; no Bug is auto-closed from Feature tests

Write:

- `notes.md` Feature Completion Check record
- `project.md` Current Work / Next Suggested Action update after confirmation if state changes
- a combined review may present `Bug Close Decision: confirm | revise | keep-verifying` and `Feature Close Decision: confirm | continue | pause | revise-scope`, but each authorization remains separate

Exit:

- recommend Close if complete, but ask explicit human confirmation before closing
- recommend next unfinished item if incomplete
- recommend Pause before new feature if human wants to switch context
- recommend scope update if remaining work should be removed before close
- recommend blocked with one unblock recommendation when completion cannot be decided because a human decision, environment, access, verification dependency, or external blocker is missing

## Pause / Close

Load:

- `skill-routing.md` for Stage Helper Capability Scan
- `external-skill-adapters.md` when Stage Helper Capability Scan finds Superpowers verification, finishing, or handoff helpers

Rules:

- before fallback pause/close preparation, run Stage Helper Capability Scan; when a matching verification/finishing/handoff helper is available, use it only for evidence discipline, close options, or handoff structure
- external helpers may support pause/close preparation, but agent-loop still owns the human confirmation gate and final state transition

Pause writes:

- current state
- next action
- blockers
- touched files
- resume point
- move the current feature from `Active Feature` to `Paused Features` in `project.md`
- set `Active Feature: none` after the paused feature and resume point are recorded
- set the feature lifecycle status to `paused` and record the transition in `notes.md`
- clear any feature-scoped auto-mode grant; a resumed feature requires a newly confirmed applicable mode

Close requires:

- fresh verification evidence
- Feature Close Review
- drift check
- submit/integration status recorded if the human requested submission
- long-term memory update
- Requirement Reconciliation when the feature references or creates requirement sets
- explicit human confirmation

Write:

- `notes.md` close record
- set the feature lifecycle status to `closed` in `spec.md` and the close record
- remove the feature from `Active Feature` and `Paused Features` in `project.md`
- set `Active Feature: none`, clear feature-scoped auto-mode grants, and record the next suggested action

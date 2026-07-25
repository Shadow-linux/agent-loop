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

This is an internal route before Feature construction, not a canonical stage, message intent, Feature Type, Bug Resolution Path, lifecycle, status, or Auto Mode. Load `references/lightweight-change-lane.md` and persist `templates/lightweight-execution-card.md` after clearly-eligible routing and before the first target write.

Entry: an actionable ordinary non-Bug local change may be bounded, reversible, and exactly verifiable.

Run in this order:

```text
Project Entry classification plus minimum guidance, dirty-work, scope and safety checks
-> explicit Bug / active Feature precedence
-> enumerate goal, acceptance, scope, risk, verification, rollback
-> decide clearly eligible | Feature trigger | uncertain
-> select the one accepted memory root or changes-only default
-> create the parser-valid monthly card before first target write
-> Project Skill Discovery Guard before generic action fallback
-> bounded edit
-> targeted verification
-> diff/scope/memory/rollback/sensitive-evidence review
-> read-only pending-memory scan
-> result or scope-expansion stop
```

Rules:

- A concrete bounded change request authorizes only the local scope disclosed in the card; it adds no separate Lightweight Mode gate.
- Explicit Bug Management and an active owning Feature take precedence. Generic `fix`, “修一下”, “改一下”, or “small tweak” wording alone decides neither route nor eligibility.
- Eligibility is all-of and Feature hard triggers are any-of. A missing fact becomes `Feature trigger` or `uncertain`, never an optimistic lane assumption.
- When uncertain, present few real options, one Agent recommendation, evidence/unknowns, and perform zero writes before the human answer.
- The persisted card Plan always exists and never uses No-Plan Decision. Adapt its detail to risk without turning it into Feature `plan.md`.
- Fact/config/path/domain/docs changes use targeted syntax/parse/reference/residual/dry-run evidence. A small isolatable behavior branch uses the smallest meaningful RED/GREEN plus focused regression.
- If reliable memory exists, run Project Skill Discovery Guard before generic action fallback and preserve the matched Project Skill Execution Gate.
- Scope expansion stops before broader edits. Preserve current evidence, recommend exactly one Bug/Requirement/Feature route, and ask before keeping, reverting, or extending partial edits.
- Completion requires fresh verification, diff and disclosed-scope review, rollback, durable-memory impact review, and Result / Residuals.
- A changes-only root does not prove initialization. Reuse one legacy root, fail closed on dual roots, keep the creation month stable, use a collision suffix without overwrite, and run the read-only scanner after completion.
- Resume accidental interruption only after branch/full-HEAD/dirty-diff/Scope/Plan/eligibility/verification/rollback revalidation. Planned durable continuation remains Feature work.
- Three pending or an oldest pending age greater than seven days triggers Agent semantic consolidation; high-evidence sync requires an existing reliable owner and exact pre-write disclosure, while uncertain meaning remains visible for Human Review.
- The card grants no branch, submit, commit, push, PR, merge, tag, release, publish, production, external, paid-call, configuration-write, destructive, Feature close, or Bug lifecycle action.

Write:

- one complete persistent Lightweight Execution Card under `<memory-root>/changes/YYYY-MM/YYYY-MM-DD-<topic>.md`;
- no Change README/INDEX/archive/move/rehydrate/restore lifecycle, shared backlog, Feature workspace, or helper-native tree.

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
- next stage: Requirements Discussion / Requirement Record when product meaning or sources need review; otherwise Feature Spec only from a confirmed Effective Product Definition

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
requirements-discussion -> evidence / Brainstorm -> Product Definition Depth Scan -> Brief or Standard product.md draft -> Product Human Review -> Requirement Record / Archive
```

Use:

- `requirement-management.md`
- `product-definition.md` for Profile, completeness, Product Review, helper, visual, and Product Slice rules
- `requirement-product-grill.md` when terminology, business rules, flows, boundaries, exception paths, prior feature behavior, or decision signals are unclear
- `project-decisions.md` when hard-to-reverse, surprising, cross-feature, or real-trade-off decisions appear
- `document-templates.md`
- `human-review-summary.md` before approval
- `skill-routing.md` and `external-skill-adapters.md` when a brainstorming or product-discovery helper is available

Rules:

- use Brainstorm / Clarify to shape the demand before drafting the Product Definition
- inspect human original sources and project evidence, then recommend exactly `brief` or `standard`; Profile is documentation depth, not lifecycle or authorization
- keep the draft response-local until Product Human Review and Requirement Record / Archive disclosure
- use Requirement/Product Grill before asking humans when terminology, roles, business objects, flows, exception paths, or historical behavior are unclear
- run targeted lookup of relevant prior feature `product.md`, `spec.md`, `tests.md`, and `notes.md` before asking a grill question
- for Standard, classify Concept Foundation as an internal method before detailed Business Flow, Product State Model, or Requirement Product Model work
- when Concept Foundation triggers, follow the Human Grill Contract in order: inspect evidence, extract Concept Candidate Inventory, present one recommended definition with evidence and accept/reject impact, then ask exactly one downstream-blocking question
- keep the Concept Foundation Gate blocked while status is `candidate` or `reopened`; do not draft downstream flow/state/product-data sections as assumptions plus open questions
- use `concept-foundation-not-needed` only with a concrete no-semantic-change reason
- before confirming the Product Definition, load `human-review-summary.md` and present cumulative Product Definition Approval after the one-question-per-turn Grill has resolved each blocker
- after internal status becomes `accepted`, derive only applicable relationships, roles/permissions, commands/events, flow, state, product facts, invariants, exceptions, and recovery from stable Concept IDs
- for Standard, record exactly one `included | not-applicable` Product View Applicability row for every defined view; do not create empty model sections or fake IDs
- run Product Completeness Scan before Product Human Review; structure validation never substitutes for product-semantic judgment
- when a Visual Trigger exists, resolve a matching active project-local visual skill then installed Archify, obtain one Visual Scope Grant, and use the working render to clarify the current product question; rewrite accepted feedback into `product.md` before Product Human Review
- if no visual adapter exists and Archify would materially improve review, recommend its exact installation/use before offering Markdown/Mermaid/ASCII; use fallback directly only when Archify is unjustified, declined, unsupported, unavailable after recommendation, or failed, and never install it without a separate exact Installation Authorization
- keep working renders disposable; only a separately confirmed, validator-backed `source-render-v1` pair may enter Derived Visuals
- record shared design signals as Design Readiness evidence and Decision Candidates; do not create accepted ADRs from Requirements Discussion
- keep early ADR signals as Decision Candidates until the requirement is human-reviewed and the owning gate is clear
- ask only questions that affect requirement clarity, scope, users/operators, constraints, non-goals, or acceptance direction
- when Requirement/Product Grill was used, carry the accepted results into the same Requirement `product.md` draft; do not create a separate Concept artifact or stage
- run a lightweight Phase Scan when the demand looks larger than one feature, has MVP/later scope, contains multiple journeys or roles, crosses multiple technical boundaries, or the human uses staged-delivery language such as "先做核心闭环" or "后面再补"
- when Phase Scan triggers, propose a `Delivery Phases` table for human review before feature construction
- draft `product.md` only after the intent is clear enough for Human Review
- store the reviewed definition under `.agent-loop/requirements/<record-date>-<topic>/product.md` only after the human confirms the Requirement Record / Archive disclosure
- preserve every human original byte; create `sources/` or `visuals/` only when needed and confirmed, never as empty placeholders
- Product Review/recorded does not mean Requirement accepted for implementation and does not authorize Feature, ADR, code, or Git actions
- do not create a feature workspace during requirements discussion unless the human explicitly says to start implementation
- do not enter Work Breakdown, Plan Gate, or Execute
- new Feature work does not create `product.md`; Feature `spec.md` references the Effective Product Definition and records Product Slice
- if the human wants to implement after Requirement acceptance, run Design Readiness and then create a Feature that references the Requirement Set

Write after confirmation:

- `.agent-loop/requirements/<record-date>-<topic>/README.md`
- `.agent-loop/requirements/<record-date>-<topic>/product.md`
- optional copied human originals under `sources/` without editing their bytes
- optional Human-confirmed derived views under `visuals/`
- optional append-only `.agent-loop/requirements/<record-date>-<topic>/YYYY-MM-DD-product-follow-up-<slug>.md` after later semantic reopen, Requirement Conflict Review, and Human Review
- optional `notes.phase-<n>-<slug>.md` when a phase has detailed human decisions or reference direction
- optional `.agent-loop/requirements/INDEX.md` only when it already exists, index triggers apply, or the human asks for an inventory/backlog view

Exit:

- Product Definition human-reviewed and recorded
- requirement discussion remains open with next clarification question
- human chooses to start feature implementation from the accepted requirement set
- a triggered internal Concept Foundation never exits to downstream modeling while `candidate` or `reopened`

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
- next stage: Requirements Discussion / Product Definition, Decision & Design If Needed, Feature Spec, Code-Guided Operational Support, Requirement Archive, Re-Adopt Agent Loop Project, or Targeted Feature Scan, selected from current intent and artifact state

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
- each diagram declares `embedded-mermaid`, `embedded-ascii`, or `archify-source-render`; resolve project-local visual skill then Archify before embedded fallback when a Visual Trigger materially benefits review; durable Archify output requires a separately confirmed `source-render-v1` source/render pair with code/config evidence, while unjustified/declined/unsupported/failed use keeps the embedded fallback
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

## Requirement Archive (Requirement Record / Archive)

Entry: human provides requirement/prototype, points to existing material, or asks to remember future/deferred work.

Load:

- `requirement-management.md`

Rules:

- Ask before copying, moving, or renaming human files.
- Never silently modify original requirements; Human original source materials remain byte-stable.
- Do not edit `requirement.md`, external PRDs, prototypes, or other human source files for Product Definition, lifecycle, or implementation updates.
- Normalize names only after confirmation.
- Requirement archive dates are archive dates only, not deadlines or feature lifecycle dates.
- Use a requirement set directory with `README.md`; do not create new flat files directly under `.agent-loop/requirements/`.
- Group all materials from the same intake/topic together: README, reviewed Product Definition, human originals/references, prototypes, screenshots, feedback, recordings, links, and follow-up notes.
- Do not overwrite old requirement materials when requirements change.
- Old requirement set README files remain valid; do not require migration only because `Lifecycle`, `Summary`, or `Status History` is missing.
- Run Phase Scan for complex requirement archives. Recommend `Delivery Phases` in the requirement set `README.md` when the requirement will likely become multiple features, has MVP/later scope, crosses multiple boundaries, or needs staged human delivery confirmation.
- Do not create a feature merely because a phase exists. A phase becomes feature work only after the human chooses to start that accepted phase or phase slice.
- Before an accepted requirement enters feature construction, run Design Readiness Check from `project-decisions.md` and record the result in the requirement README.
- Before an accepted Requirement enters Feature construction, require one confirmed Effective Product Definition and no unresolved internal Concept/Product Model blocker. Product Review and lifecycle acceptance do not authorize one another.
- For new sets, resolve README `Effective Product Definition` first. For legacy sets, resolve `Effective Concept Foundation` or the reviewed legacy source. If later evidence reopens semantics, stop response-locally, preserve old sources, run Requirement Conflict Review, and ask before `YYYY-MM-DD-product-follow-up-<slug>.md` / linked replacement plus pointer update.
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

- `.agent-loop/requirements/<record-date>-<topic>/README.md`
- `.agent-loop/requirements/<record-date>-<topic>/product.md` only after Product Human Review and exact Record / Archive disclosure
- `.agent-loop/requirements/<record-date>-<topic>/sources/*` only when human originals are copied after confirmation; never rewrite or create an empty directory
- legacy/root `.agent-loop/requirements/<record-date>-<topic>/requirement.*` only when source material is provided or already exists
- optional `.agent-loop/requirements/<record-date>-<topic>/notes.phase-<n>-<slug>.md` when a phase needs a separate accepted note
- `.agent-loop/requirements/<record-date>-<topic>/prototype.*` only when source material is provided or copied after confirmation
- optional feedback, screenshot, recording, design-link, meeting-note, and other source files inside the same requirement set
- optional change-request files inside the same requirement set
- optional `.agent-loop/requirements/INDEX.md` only when trigger conditions apply
- source references in an existing confirmed feature `spec.md` when the requirement was discovered during feature work; do not create a feature or `spec.md` from Requirements Discussion or Requirement Archive only to hold the link

Exit:

- requirements archived or original paths recorded

## Legacy Feature Product Brief Compatibility (Non-stage)

Entry: Resume, Follow-up, Review, Close, or Recovery encounters an existing Feature `product.md`.

Load `product-brief.md`. Read the legacy Product Brief after the effective Requirement source and before relying on its Feature-local paraphrase. Do not create, refresh, or migrate Feature `product.md` for new work.

If the legacy Feature Product Brief conflicts with `Effective Product Definition` or its legacy Requirement authority, stop for Requirement Conflict / Recovery. Preserve both sources until the human confirms the owning correction. Absence of Feature `product.md` in new work is expected and never blocks Feature Spec.

Write: none by default. Any Requirement follow-up or Feature Spec update uses its own Human Review / lifecycle gate.

Exit: legacy evidence is compatible and current Feature work continues through Feature Spec Product Slice, or conflict is routed to Requirements Discussion / Recovery.

## Decision & Design If Needed

Entry: Design Readiness is `required`, or an accepted Effective Product Definition, legacy reviewed Requirement source, Technical Design / Code Context, or Drift Check reveals shared business-flow, domain, data, architecture, recovery, non-functional, cross-feature, or long-term design needs.

Load:

- `project-decisions.md`
- `document-templates.md`
- `human-review-summary.md` before asking the human to create, accept, supersede, deprecate, or reference project-level decisions

Position:

```text
Confirmed Product Definition -> Requirement lifecycle -> Design Readiness Check -> Decision & Design If Needed -> Feature Mapping -> Feature Spec with Product Slice
```

Rules:

- run Design Readiness Check after requirement acceptance and before feature construction
- enter Decision & Design when a requirement is complex, likely to split into multiple features, changes an end-to-end business flow, shares domain/data/state rules, or needs common architecture, recovery, or non-functional direction
- do not bypass Decision & Design merely because no technology choice is disputed
- use Decision Scan / Placement inside this stage to place product-only, feature-local, testing, and project-level decisions
- do not create ADR files from ordinary chat or early fuzzy requirements discussion
- treat Effective Product Definition / legacy Requirement Product Model as product-semantics authority; Decision & Design consumes accepted Concept IDs, model IDs, and Product Rule anchors but must not redefine product identity, lifecycle, relationship, invariant, permission, fact ownership, or terminal meaning
- resolve README `Effective Product Definition` or legacy `Effective Concept Foundation` and record an Effective Requirement Snapshot before technical landing; new sources require Profile plus Product Review `confirmed`
- inventory every stable source Requirement Model ID (`REL-*`, `PERM-*`, `CMD-*`, `EVT-*`, `FLOW-*`, `STATE-*`, `PM-*`, `EX-*`) before selecting the coherent ADR scope; every out-of-scope ID needs an explicit owner or reason
- record one Requirement Model Technical Landing Trace disposition for every accepted Requirement Model ID declared inside the ADR scope; `landed` rows require Technical Landing, Preserved Invariant, Design Slice, and Verification
- keep `Upstream Compatibility: review-required` as a blocking dependency judgment, not a decision lifecycle status; stop dependent Feature Spec, Plan, and implementation until compatibility review returns it to `current`
- requirement modeling does not add Concept-to-technical-representation mapping; technical landing remains inside the existing Human-gated Decision & Design record
- place product-only meaning in Requirement `product.md`
- place feature-local decisions in `spec.md` Design Decisions
- place testing decisions in `tests.md` unless they verify a long-term design goal
- recommend `.agent-loop/decisions/*.md` only for project / cross-feature, long-term, hard-to-reverse, surprising, or real-trade-off decisions
- creating `.agent-loop/decisions/` does not imply enterprise memory mode
- do not create, accept, supersede, deprecate, delete, or renumber decision files without explicit human confirmation
- convert every implementation-bearing shared flow step, invariant, recovery responsibility, and non-functional target into a stable Design Slice ID
- assign every required design slice to at least one planned feature; no required slice may remain `unassigned` before Feature Spec
- do not enter Feature Spec when required shared design is unresolved or design-slice coverage is incomplete
- do not accept an ADR while its Effective Requirement Snapshot is unresolved, its Requirement Model coverage is incomplete, or its compatibility is `review-required`
- when a Visual Trigger exists, use a bounded working render to clarify technical options or boundaries, then rewrite the result into the proposed ADR; optional durable visual evidence uses `source-render-v1` and cannot accept the ADR or satisfy technical-landing coverage
- run structural preflight while the draft remains `proposed`; only explicit human acceptance authorizes Human Review Evidence plus `Status: accepted`, followed by accepted-mode validation
- allow a confirmed Brief with no stable model IDs/Product Rule references, or a reasoned legacy `concept-foundation-not-needed` source, to use the explicit trace-not-applicable path without inventing product models
- allow a confirmed Standard source with Product Rules but no Concept or Requirement Model IDs to keep the absent ID fields as `none`, while requiring normal Product Rule scope and technical-landing coverage
- when upstream accepted meaning invalidates an accepted technical decision, preserve history and propose a superseding ADR; do not rewrite accepted decision meaning in place
- assess Migration / Backfill, Compatibility, Rollout / Cutover, and Rollback / Reversibility, but expand operational landing only for triggered concerns
- update Requirement README/Product Definition and Feature `spec.md` decision references after human confirmation

Write after confirmation:

- conditionally required `.agent-loop/decisions/000N-<slug>.md` from `templates/decision.md` when shared design is required and no accepted decision covers it; otherwise no new file is needed
- requirement README `Applicable Decisions`, `Triggered Decisions`, and `Implemented By`
- Feature `spec.md` `Applicable Decisions`; preserve legacy Feature `product.md` history without new writes
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

- after mandatory helper resolution, use the loaded Brainstorming Adapter; use fallback only for recorded `unavailable` or `load-failed`. Requirements Discussion keeps the Requirement `product.md` draft response-local until Product Human Review/Record, Requirement README owns pointer/lifecycle, and Feature-local clarification writes `spec.md` / `notes.md`.
- Ask 1-5 high-impact questions.
- Default to one question at a time.
- Questions must affect scope, UX, data, architecture, testing, or acceptance.
- Do not ask filler questions.
- If a question can be answered by reading project docs, code, tests, source requirements, `project.md`, or `product.md`, inspect those first instead of asking the human.
- For grill questions, also inspect targeted prior feature artifacts when relevant; do not run a full feature scan.
- When product terminology is fuzzy or conflicts with `project.md` Domain Language, propose a canonical meaning and ask only if still ambiguous.
- When Concept Foundation is triggered, override the generic 1-5 question allowance: use the Human Grill Contract and ask exactly one downstream-blocking question per turn.

Write:

- Requirements Discussion: write approved product clarification into the Requirement `product.md` only through its Record / Archive Gate; keep README to source pointer, lifecycle, Delivery Phase, Feature Mapping, and decision-link summaries.
- Legacy Feature Product Brief: read-only compatibility; no new write.
- Feature Spec: write accepted engineering clarifications into `spec.md` and human decisions into `notes.md`.

Exit:

- Requirements Discussion: Product Definition draft is ready for Product Human Review and Requirement Record / Archive.
- Feature Spec: the owning artifact is stable enough for its next Agent Loop stage.

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

## Feature Context Load Contract

For every current Feature, bootstrap from `spec.md`, not `tasks.md` or `plan.md`. Run the read-only checker before Task, Test, Plan, Resume, controller re-entry, context-compaction recovery, Execute, Subagent Handoff, Verify, Review, Drift Check, or Close relies on Feature context:

```text
python3 <skill-root>/scripts/check-feature-context.py --project-root <target-project-root> <feature-spec-path>
```

`CURRENT` (`0`) permits the local Snapshot fast path. `REFRESH_REQUIRED` (`3`) stops downstream generation while the Agent reads only changed/applicable Requirement and ADR meaning, compares semantic impact, refreshes derived Snapshot evidence, and repairs affected Tasks/Tests/Plan/Handoffs. `BLOCKED` (`1`) routes to Requirements Discussion, Decision & Design compatibility review, Feature Definition Review, or Recovery. Auto Mode cannot continue on either non-current result. On Windows use `py -3`.

## Feature Construction Two-Gate Review

Normal Feature construction uses exactly two ordinary review stops after an explicit implementation request:

```text
Feature Spec + Requirement Checklist
-> Gate 1: Feature Definition Review
-> Implementation Package Preparation
-> Gate 2: Implementation Readiness Review
-> Execute Agent-ready work
```

Gate 1 accepts the checked definition and Product Slice. Its acceptance sets `Implementation Readiness: preparing`, records `Gate 1 Decision: accepted` plus the current Spec SHA-256 in Feature `notes.md`, and authorizes package preparation only; target implementation is forbidden before Gate 2. Package preparation completes every applicable Work Breakdown, Delivery Contract assessment/exact candidate, Test Design, E2E Discovery, Technical Design / Code Context, Plan, trace coverage, risk, rollback, and Analyze Consistency method without separate approval prompts.

When the package is complete, record in `notes.md` the complete reviewed Package Files/Digest (including every current triggered detail file), non-rotatable Stable Files/Digest, accepted Agent-ready task IDs, initial Active Plan Scope, matching `plan.md | plans/<detail>.md | no-plan:<accepted-task>` evidence, and Gate 2 review time; set `Implementation Readiness: review-ready` and present Gate 2. After the human chooses, record `Gate 2 Decision` and the matching Auto-Loop state, then run `python3 <skill-root>/scripts/check-feature-review.py --mode review <feature-dir>`; on Windows use `py -3`. `Approve package only` sets readiness `accepted` without execution. `Approve package and start implementation` sets readiness `accepted` and enables Feature Auto-Loop without another generic prompt. Product meaning, Product Slice, scope, or acceptance changes return to Gate 1. Material task/test/code-context/Plan/risk/rollback changes repeat Gate 2. Fact-determined refinements inside accepted scope may continue with evidence.

After package-only acceptance, a later explicit instruction to start this Feature may enable Feature Auto-Loop without repeating the full Gate 2 review only when Feature Context is still `CURRENT`, `check-feature-review.py --mode start` proves the complete accepted package unchanged, and no new stop condition or Human-gated item exists. Record the new explicit authorization as `approve-and-start`, enable Auto-Loop, update the review time, and run `--mode execute` before target implementation. Otherwise route the changed meaning to Gate 1 or the changed package to Gate 2.

Strict Mode remains available when the human explicitly requests stage-by-stage control. Delivery Contract creation/acceptance must be separately named with exact content inside Gate 2 or stop at its own gate; breaking changes always stop separately. Human-gated tasks, subagent dispatch, branch/Git actions, external mutation, production, credentials, submit, pause, close, release, and publish retain their independent gates.

## Feature Spec

Entry: goal and source requirements are clear enough.

Every Feature start must reference an accepted Requirement Set with a confirmed Effective Product Definition, or an explicitly supported legacy effective source. For a narrow direct Feature request, create/review the minimum Brief before Feature Spec. This keeps product meaning, Design Readiness, lifecycle, and Feature Mapping in one Requirement-owned location without forcing Standard modeling.

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
- Product Requirement Source: Requirement Set, Effective Product Definition, Profile, Product Review Evidence, and Applicable Decisions
- Feature Context Snapshot derived from that one resolved authority: project-root-relative Requirement/product/ADR paths, current lifecycle/review/profile, Product and Decision SHA-256 values, Product Slice references, verification time, Freshness, and the outcome/journey/rules/states/exceptions/recovery/boundary context needed downstream
- Product Slice rows mapping source sections/IDs/rules to Feature responsibility, acceptance, and `in-scope | out-of-scope | not-applicable` coverage
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
- inspect the Effective Product Definition, original source links as needed, and Applicable Decisions before writing behavior and acceptance
- use the dual reader: new `Effective Product Definition` requires Profile/Product Review `confirmed`; legacy `Effective Concept Foundation` / reviewed Requirement remains valid without migration
- add Product Requirement Source and Product Slice to `spec.md`; do not require or create Feature `product.md`
- create the default Snapshot inside `spec.md`; optional `context.md` is expanded derived context only for a Human-confirmed complex Feature and must keep exact source/digest parity
- run the checker after writing the Snapshot and require `CURRENT` before Requirement Checklist acceptance
- Product Slice references source Concept/Model IDs and `product.md#<rule-anchor>`; it may narrow scope but cannot redefine accepted product meaning
- do not let Feature Spec introduce a new meaning, state, invariant, role boundary, relationship, or product object for an accepted Concept ID; return to Requirements Discussion when product semantics must change
- when Feature Spec uses Optional Visual Communication, limit the view to the accepted Product Slice, feature responsibility, or feature-local implementation and acceptance path; rewrite accepted feature-local clarification into `spec.md`; if the view reveals new product meaning, stop and return to Requirements Discussion instead of adding it to `spec.md` or editing Requirement `product.md`
- block Feature Spec when Product Review is pending, the effective pointer is ambiguous/stale, or a triggered internal/legacy foundation is `candidate` or `reopened`
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

Write inside the explicit draft Feature construction authorization, without a separate Targeted Feature Scan prompt:

- feature-specific findings into `spec.md`, `tasks.md`, `tests.md`, or `notes.md`
- lasting project facts into `project.md` only after human confirmation

Exit:

- affected boundaries are clear enough for Work Breakdown or Test Design

## Requirement Checklist

Entry: draft spec exists.

Check:

- Feature Context Snapshot is complete, paths are project-root-relative, its source references resolve through one Requirement README, and the checker returns `CURRENT`
- no major ambiguity
- stories independently testable
- acceptance criteria measurable
- behavior changes clear
- edge cases and out-of-scope recorded

Write:

- checklist result in `tests.md` or `notes.md`
- spec updates if human confirms

Exit:

- Gate 1 `Feature Definition Review` accepts the checked spec and authorizes complete Implementation Package Preparation, requests definition revision, or pauses
- accepted spec and recorded passed Requirement Checklist set `Implementation Readiness: preparing` and persist `Gate 1 Decision: accepted` with the exact current Spec SHA-256
- Gate 1 does not authorize target implementation, Feature Auto-Loop, external mutation, or Git actions

## Work Breakdown

Entry: accepted spec with a recorded passed Requirement Checklist.

Helper-friendly stage: Work Breakdown runs Stage Helper Capability Scan before fallback. Use matching issue/task splitting helpers as method support only; keep `tasks.md`, task status, gates, and next-stage routing under agent-loop control.

Write:

- `tasks.md`

Rules:

- load `spec.md` and require a current Feature Context Snapshot before creating or revising Tasks
- map every Task to a Product Slice responsibility/acceptance, an accepted ADR Design Slice, or an explicit technical prerequisite for a named later vertical Product Slice
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

- during Implementation Package Preparation, task granularity/order self-review passes and the Agent continues to the next package method without another prompt
- unresolved product/scope/acceptance meaning returns to Gate 1; unresolved task ownership or package structure stops before Gate 2
- in human-selected Strict Mode, retain the ordinary stage review

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
- during Implementation Package Preparation, do not write contract files by default; prepare the exact proposed content and action disclosure for Gate 2
- Delivery Contract creation and acceptance may proceed only when Gate 2 separately names each exact action, path, consumers, compatibility, verification, and consequence
- outside that exact Gate 2 decision, ask before writing contract files in every mode, including Feature Auto-Loop and Task Auto-Run
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

- load and require a current Feature Context Snapshot before designing tests
- cover every applicable acceptance criterion, actor/permission boundary, state transition/terminal, Product Rule/invariant, exception/recovery path, and accepted ADR verification obligation; uncovered applicable meaning blocks readiness or needs the existing Human-approved substitute path
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

- during Implementation Package Preparation, coverage self-review passes and the Agent continues without a separate Test Design approval prompt
- a substitute-verification choice or unresolved capability needed for package coherence remains a named Human decision for Gate 2 or stops preparation
- in human-selected Strict Mode, retain the ordinary stage review

## E2E Discovery if Web

Entry: web-visible behavior exists, executable E2E/browser verification may be applicable, or Test Design cannot safely define Web E2E cases from current project memory.

Helper-friendly stage: E2E Discovery if Web runs Stage Helper Capability Scan before fallback. Use matching browser/E2E environment helpers as method support only; keep discovered project-level capability in `project.md` and feature-specific cases in `tests.md` or `tests/e2e/*`.

Load:

- `e2e-discovery.md`

Exit:

- E2E path is classified as existing-framework, browser, chrome, computer-use, manual, or blocked
- during Implementation Package Preparation, continue to Test Design when cases still need recording, or Technical Design / Code Context when the package strategy is complete; do not add a separate approval prompt

## Technical Design / Code Context

Entry: prepared tasks and tests during Implementation Package Preparation, or accepted tasks and tests in human-selected Strict Mode, before writing `plan.md` or executing a non-trivial task/story.

Helper-friendly stage: Technical Design / Code Context runs Stage Helper Capability Scan before fallback. Use matching codebase-scan or technical-planning helpers as method support only; keep code context, interface decisions, plan readiness, and human gates under agent-loop control.

Load:

- current Feature Context Snapshot plus applicable accepted ADRs; separate accepted product meaning, accepted ADR landing, and current code facts throughout Technical Design
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

- during Implementation Package Preparation, code context is concrete enough for a construction-grade Plan and the Agent continues without a separate approval prompt
- otherwise the task becomes Human-gated or preparation stops before Gate 2

## Plan Gate / Plan If Needed

Entry: selected task/story has prepared tasks and tests during Implementation Package Preparation, or accepted tasks and tests in human-selected Strict Mode, and Technical Design / Code Context has enough evidence to decide whether a construction plan is required.

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

- require Feature Context Snapshot `Freshness: current` before accepting a Plan or No-Plan Decision
- require every active Plan to name its Product Slice and Task, preserve applicable product/ADR invariants, separate code facts from product intent, and verify the mapped acceptance without implementing nearby out-of-scope Requirement meaning
- decide whether a plan is required before any code implementation
- create `plan.md` when the task/story is complex, multi-file, changes behavior, changes tests, touches interfaces, crosses module boundaries, involves data/API/async/security/deployment behavior, needs TDD design, needs subagents, or the human asks for a plan
- a No-Plan Decision is allowed only for a trivial, low-risk, single-file or documentation-only task with clear acceptance, exact files, and exact verification command
- in human-selected Strict Mode, ask human confirmation before executing from a No-Plan Decision
- in Feature Auto-Loop, a No-Plan Decision may proceed only if the task is Agent-ready and no plan trigger applies
- Task Auto-Run always requires an accepted task/story plan; No-Plan Decision cannot enable Task Auto-Run
- plan scope is `task` or `story`
- default scope is task
- a task Plan ID must be one Gate 2-accepted Agent-ready task; a story Plan must list non-empty `Included Tasks`, every included ID must belong to that accepted task set, and every included Task must map to the named Story in `tasks.md`
- for a multi-task Feature package, Gate 2 accepts the complete Agent-ready task set, ordering/barriers, stable files, and initial active Plan; later `plan.md` rotation may select only another accepted task/story and must pass Plan Gate, Analyze Consistency, and `check-feature-review.py --mode execute`
- treat Plan rotation inside the unchanged accepted task/test boundary as execution refinement; a new task, stable-file drift, changed ordering/boundary, or material interface/risk/rollback/verification change repeats Gate 2
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

- during Implementation Package Preparation, Plan self-review and package coverage pass without a separate Plan approval prompt
- after Analyze Consistency passes, set `Implementation Readiness: review-ready` and present Gate 2 `Implementation Readiness Review`
- a material Plan/risk/rollback revision repeats Gate 2; a definition/scope/acceptance revision returns to Gate 1
- in human-selected Strict Mode, retain ordinary Plan acceptance

## Analyze Consistency

Entry: before implementation when spec/tasks/tests and either plan or a recorded No-Plan Decision exist.

Check:

- rerun Feature Context freshness and require `CURRENT`
- trace Product Slice through Tasks, Tests, and the active Plan; stop when any accepted role, state, rule, exception, recovery, acceptance, or ADR obligation is lost
- each accepted requirement has task coverage
- each task maps to spec or explicit technical need
- tests cover acceptance criteria
- plan scope matches selected task/story, or No-Plan Decision is limited to a trivial task with exact files and verification
- each accepted Decision & Design slice assigned to the feature maps through `spec.md`, tasks, tests, and the active plan
- no assigned design slice lacks an implementation or verification path, even when every local story is independently testable

Write:

- findings in `notes.md`
- during Gate 1-authorized package preparation, repair fact-determined gaps in `tasks.md`, `tests.md`, technical context, and Plan without another prompt while the accepted definition remains unchanged
- return product meaning, Product Slice, scope, or acceptance changes to Gate 1; after Gate 2, repeat Gate 2 before relying on any material package revision
- outside the Gate 1 preparation grant or an active execution grant, retain the owning Human Gate before broader artifact mutation

Exit:

- during package preparation, a clean result completes readiness and routes to Gate 2
- before presenting Gate 2, persist Package Files/Digest, Stable Files/Digest, accepted Agent-ready task IDs, initial Active Plan Scope, matching Plan/No-Plan evidence, and the review timestamp in `notes.md`
- Gate 2 choices are `Approve package and start implementation`, `Approve package only; do not implement yet`, `Revise package`, or `Pause`
- after recording the chosen Gate 2 decision and matching Auto-Loop state, require `check-feature-review.py --mode review` to pass
- approve-and-start enables Feature Auto-Loop without a third generic prompt; package-only never authorizes execution
- gaps revise the affected package and repeat Gate 2, or return to Gate 1 when definition/scope/acceptance changes

## Subagent Execution If Approved

Entry: human explicitly approves subagent use for an independent task/story group, Project Entry Scan lane, or bounded implementation lane.

Mandatory helper: Subagent Execution If Approved resolves and loads `superpowers:subagent-driven-development` or `subagent-driven-development` after human approval and before dispatch. Record Stage Helper Resolution; helper availability never replaces subagent authorization.

Load:

- `skill-routing.md`
- `external-skill-adapters.md`
- `templates/subagent-brief.md`

Rules:

- before dispatch, require current Feature Context and put the Feature path, Snapshot Product SHA-256/Freshness, Product Slice IDs/anchors, applicable ADR paths/digests, and exact assigned scope in every implementation brief
- the handoff expires immediately when the Product Source SHA-256 or any applicable Decision Source SHA-256 changes; the receiving Agent reruns freshness before acting
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

- rerun or reuse only fresh same-stage checker evidence and reject Execute when Feature Context is missing, `refresh-required`, or `blocked`
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
- `checker-recovery.md` when a canonical Agent Loop checker still fails after the exact command is rerun with unchanged inputs

Rules:

- after mandatory helper resolution, use the loaded Debugging Adapter; use fallback only for recorded `unavailable` or `load-failed`, and find root cause before proposing fixes
- reproduce before fixing
- find root cause
- form one hypothesis at a time
- write regression test when possible
- for a canonical checker failure, preserve its exact command/output/path/digest and classify `artifact-invalid | environment-invalid | checker-defect-candidate | unresolved` before changing checker or artifact logic
- reduce a checker candidate to a published-authority-backed positive fixture and negative controls; read-only diagnosis may continue without interruption
- present the exact Temporary Checker Repair Review before any checker/support-file write; use an isolated temporary copy by default and require a separate in-place installed-Skill authorization
- verify the unmodified copied checker produces RED, then the minimal patch produces GREEN while negative controls still fail
- never rewrite a valid artifact for a known-wrong checker, add a broad bypass, hide canonical failure, or reuse a temporary grant after its Gate or digest scope expires

Write:

- diagnosis in `notes.md`
- compact checker-recovery evidence in the existing owning artifact only when the result must cross sessions, handoff, or a later action-specific Gate; same-session evidence may remain response-local

Exit:

- fix verified or blocker escalated

## Verify

Entry: before any completion claim.

Mandatory helper: Verify resolves and loads `superpowers:verification-before-completion` or `verification-before-completion` before any passed, fixed, complete, or ready claim. Record Stage Helper Resolution; fallback requires `unavailable` or `load-failed`.

Load:

- `skill-routing.md` for Stage Helper Capability Scan
- `external-skill-adapters.md` when Stage Helper Capability Scan finds Superpowers or another verification skill
- `checker-recovery.md` when verification depends on a suspected defective canonical Agent Loop checker

Rules:

- rerun Feature Context freshness before verification relies on Snapshot acceptance references; non-current context stops verification claims
- after mandatory helper resolution, use the loaded verification adapter; use fallback only for recorded `unavailable` or `load-failed`, while completion remains controlled by agent-loop
- identify proof command/action
- run fresh verification
- read output
- record evidence
- when the Feature resolves Bugs, execute the Bug Verification Matrix against the original reproduction or accepted substitute and regression/safety paths
- after Feature evidence exists, move a related repair Bug from `in-progress` to `verifying`; do not set `closed`
- failed Bug-specific verification returns the Bug to `in-progress` when the repair remains valid or `triaging` when Expected Behavior/diagnosis was invalidated; append the failure evidence
- a temporary checker result may substitute for one named Gate only after fresh defect proof, RED/GREEN, negative controls, exact target run, expiry/rollback disclosure, and explicit Human acceptance
- retain the dual result exactly: `Canonical validation: failed`, `Temporary checker recovery: passed | failed`, and `Human substitute decision: accepted-for-this-gate | declined`
- do not claim Agent Loop itself fixed until the formal source checker and required focused/full validation pass

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

- current Feature Context Snapshot and authoritative acceptance references; code disagreement is implementation drift and must not be copied into the Snapshot
- Spec Review: implementation matches the current Requirement Product Definition through the Snapshot/Product Slice, legacy Feature `product.md` only when present, `spec.md`, acceptance criteria, scope, and out-of-scope
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
- when a visual would materially improve close/review communication, derive it only from current accepted artifacts and verification evidence; a presentation render cannot replace review findings, completion evidence, drift decisions, or any close/submit gate

Write:

- task review findings and accepted fixes in `notes.md` under Spec Review and Standards Review
- close review findings and accepted fixes in `notes.md` under Feature Close Review

Exit:

- continue to Drift Check, revise implementation, or diagnose failures

## Drift Check

Entry: after implementation or before close.

Check:

- rerun Feature Context freshness and compare code behavior with current product/ADR authority; report disagreement as drift rather than overwriting product truth
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
- after a stable verified code merge, run Post-Merge Memory Reconciliation only when an observed semantic memory conflict exists; load `memory-reconciliation.md`
- no observed conflict is `reconciliation-not-needed`; do not scan all memory, create a report, add a Human Gate, or block the next independently authorized Git/lifecycle action
- for a conflict, inspect only its owner/direct dependencies and minimum evidence; let the Agent rewrite fact-determined meaning and ask the human only when multiple meanings remain legitimate
- broad four-snapshot accounting and exact Plan Hash/transaction/restore gates are explicit Full Memory Audit / Recovery only
- a resolved conflict permits only the next separately authorized Memory Commit or later Git gate; code merge, submit, auto-mode, or helper approval does not satisfy any Git gate

Write after confirmation:

- `notes.md` submit/integrate record
- current Memory Conflict Report locator/status/blocker in `project.md` Current Work only when an unresolved or material conflict report exists; do not persist `reconciliation-not-needed`
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

- Feature Context freshness rechecked as `CURRENT`; `refresh-required | blocked` stops Close and Auto Mode
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

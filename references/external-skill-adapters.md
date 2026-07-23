# External Skill Adapters

Use this reference when another skill or plugin can improve the current `agent-loop` stage. External skills are stage accelerators only; agent-loop remains the controller.

## Capability Scan Rule

Before using fallback stage guidance, inspect the current runtime's available skills/plugins/helpers for a stage match.

If Superpowers is available, prefer these helpers:

| Stage | Preferred Superpowers helper |
|---|---|
| Requirements Discussion | `superpowers:brainstorming` plus PRD/product and grill-with-docs style helpers when available |
| Brainstorm / Clarify | `superpowers:brainstorming` |
| Project Skill Creation / Update | `superpowers:writing-skills` / `writing-skills`; also `skill-creator` when available |
| Legacy Product Brief compatibility | no writer helper; reader-only compatibility |
| Feature Spec | `superpowers:brainstorming` plus spec helpers when available |
| Plan Gate / Plan If Needed | `superpowers:writing-plans` |
| Execute Task / Story | `superpowers:test-driven-development` |
| Diagnose Failure | `superpowers:systematic-debugging` |
| Verify / Completion claim | `superpowers:verification-before-completion` |
| Review / Feature Close Review | `superpowers:requesting-code-review` |
| Feature Completion Check | verification / finishing helpers when available |
| Submit / Integrate | `superpowers:finishing-a-development-branch` |
| Pause / Close | finishing / handoff helpers when available |
| Approved Subagent execution | `superpowers:subagent-driven-development` |

For mandatory helper-backed stages, resolve canonical and alias names using `skill-routing.md`, then load the complete helper before stage actions. If it is absent, record `unavailable`; if it is discovered but cannot be loaded, record `load-failed`. Only those two statuses allow fallback.

## Optional Visual Communication Adapter

Archify (<https://github.com/tt-a1i/archify>) is preferred when a Visual Trigger materially lowers misunderstanding risk and no matching active project-local visual skill owns the project-specific presentation language. It is optional: do not add it to the mandatory helper table, do not run it merely because it is installed, and do not block the owning Agent Loop stage when it is absent.

Resolve in this order:

```text
matching active project-local visual skill
→ installed Archify
→ recommend Archify before fallback when it would materially improve review
→ Markdown / table / Mermaid / ASCII fallback
```

A Visual Trigger exists when a workflow, lifecycle/state model, architecture/boundary, sequence, data flow, relationship, or option comparison is materially harder for the human to verify in prose. Requirements Discussion is the primary use: render the Agent's current understanding, let the human correct it, then rewrite the accepted meaning into the Requirement `product.md`. Feature Spec visuals may explain only the accepted Product Slice, feature responsibility, and its feature-local implementation or acceptance path. Rewrite accepted feature-local clarification into `spec.md`; if the view reveals new product meaning, stop Feature Spec and return to Requirements Discussion rather than adding the meaning to `spec.md`. Decision & Design may use the adapter for technical option or boundary review. Onboarding and review/close communication may derive presentation views from already accepted evidence.

Do not offer Markdown / table / Mermaid / ASCII as the first drawing path merely because Archify is absent. When Archify would materially improve the current review, present the exact, rejectable Installation Authorization first. Use the built-in fallback only when Archify is not materially justified, the human declines, the environment cannot support it, or installation/use fails. A declined or failed Archify path never blocks the owning stage.

Before generation, obtain one bounded Visual Scope Grant and disclose:

| Field | Required value |
|---|---|
| Stage | current Agent Loop stage |
| Review Question | one concrete question the view will help answer |
| Semantic Source | exact authoritative Markdown and stable IDs |
| Diagram Type | one supported type such as `architecture`, `workflow`, `sequence`, `dataflow`, or `lifecycle` |
| Working Output | exact temporary/working location or response-local presentation |
| Iteration Boundary | same question, source, type, and working-output class |

The same grant permits iterative visual corrections within that boundary. A new source, stage, type, durable destination, external side effect, or material semantic question requires a new grant.

If Archify is unavailable and useful, recommend it. Before installation, present an exact Installation Authorization containing source and pinned revision, full command, runtime target/location, network and file effects, global/local impact, doctor/verification command, and no-install fallback. Human approval authorizes only that exact action. Agent Loop does not vendor Archify: do not hard-code one cross-runtime install command because supported runtimes and package locations differ. A failed install does not authorize privilege elevation, a different source/mirror/package manager/location, or a materially different retry.

Use `render to converge, text to record`:

- the owning Markdown is semantic authority;
- an unrecorded working render is disposable review material;
- human confirmation of a render requires the Agent to rewrite the owning semantic text before the existing stage Human Gate;
- the render cannot create a product rule, accept an ADR, complete Onboarding, start a Feature, or authorize Git/release action.

When the human separately confirms durable recording, use `source-render-v1`:

```text
accepted semantic source and stable IDs
→ typed Archify JSON source definition
→ validated derived render
```

Record both paths, both SHA-256 values, exact `archify@<version>` generator, `validate=pass; check=pass` evidence, `Status: current`, and the applicable human confirmation. Validate the pair through `scripts/visual_artifact_support.py`. HTML/PNG/SVG without its typed source, a source without its render, a digest/type/output mismatch, or a stale semantic source is not current evidence.

Installation Authorization, Visual Scope Grant, and durable recording are independent. In particular, installation or generation does not authorize Product Human Review, ADR acceptance, Feature start, Git, release, publish, or future external actions. Onboarding review and the project-skill Execution Gate also remain separate.

## Controller Rule

```text
agent-loop decides the stage.
External skills improve work inside the stage.
agent-loop artifact paths override external skill paths.
agent-loop human gates override external skill transitions.
agent-loop owns task status, feature close, project memory, and submit.
```

This ownership is invariant even when a helper is mandatory. A helper may impose a stronger stage method, but it cannot choose the next stage, change an artifact destination, cross a human gate, or update lifecycle state on its own.

Do not copy an external skill's full workflow into `agent-loop`. Borrow the method, then translate the result into the current `agent-loop` artifact.

For Lightweight Change Lane, the persistent monthly card remains controller-owned and does not enter a mandatory helper-backed stage. Do not expand a Lightweight Execution Card into `docs/superpowers/`, a Feature workspace, or a construction-grade plan. An external helper may advise a method only when already appropriate; it cannot introduce a helper-specific path, artifact, mode, gate, or scope expansion. Promotion to Feature restores the normal helper protocol.

## Path Override Rule

If an external skill says to write an artifact under its own default directory, treat that path as advisory: agent-loop artifact paths always override external skill default paths.

Write to the current `agent-loop` artifact instead.

| External output | Agent-loop destination |
|---|---|
| brainstormed requirement/product/design/spec | response-local Requirement `product.md` draft during Requirements Discussion, then `.agent-loop/requirements/<record-date>-<topic>/product.md` only through Product Human Review plus Requirement Record / Archive; `.agent-loop/features/<feature>/spec.md` or `notes.md` during Feature Spec |
| implementation plan | `.agent-loop/features/<feature>/plan.md` or `.agent-loop/features/<feature>/plans/*` |
| test strategy | `.agent-loop/features/<feature>/tests.md` or `.agent-loop/features/<feature>/tests/*` |
| debugging notes | `.agent-loop/features/<feature>/notes.md`; link bounded reproduction/root-cause evidence from the Bug README when Bug Management applies |
| verification evidence | `.agent-loop/features/<feature>/notes.md` |
| review findings | `.agent-loop/features/<feature>/notes.md` |
| subagent brief / return | `.agent-loop/features/<feature>/handoffs/*` |
| project-local skill package | `.agent-loop/skills/<skill-name>/` |

The table uses the default `.agent-loop/` memory root. When an existing project uses the accepted legacy `agent-loop/` root, keep that current memory root for feature and project-memory artifacts; never create repository-root `features/`. The Project-local skill package is the exception: it always uses `.agent-loop/skills/<skill-name>/` and never inherits the legacy `agent-loop/` root.

Do not create `docs/superpowers/` in a target project unless the human explicitly asks for native Superpowers output and then confirms the external directory after the agent explains the agent-loop path override. A request such as "use Superpowers" or "save it where Superpowers normally saves it" is not enough by itself.

## Stage Helper Resolution Record

Create the initial `templates/notes.md` Stage Helper Resolution record before the first stage action, then finish its method/fallback/evidence fields before stage exit. If no feature workspace has been confirmed, use the response-local pending-record rule from `skill-routing.md` instead of creating files without approval. Project Skill Creation / Update uses a response-local record before Gate 1 and persists the completed record to `.agent-loop/skills/<skill-name>/validation.md` after the proposed directory exists.

The record includes:

- stage and requested helper
- canonical and alias candidates checked
- resolved helper or `none`
- `loaded`, `unavailable`, or `load-failed`
- whether fallback was used and its source
- artifact path, human gate, and state ownership overrides
- evidence that the helper was loaded or why resolution failed

Before the first action, `loaded` requires `Fallback Used: no`, a resolved helper, and complete load evidence. Before stage exit, it additionally requires method-used evidence. `Fallback Used: yes` requires `unavailable` or `load-failed`, a `none` resolved helper, and candidate-by-candidate failure evidence. Missing or inconsistent initial fields block stage action; missing or inconsistent exit fields block completion.

Each invocation scope gets its own record. Task Review, Submit review, and Feature Close Review may use the same helper name, but Feature Close Review requires a new resolution record and may not reuse a prior task-review load record.

## Gate Override Rule

If an external skill says to continue into another external skill, treat that as a recommendation only.

The next stage is still chosen by `agent-loop`:

```text
current stage completes
-> agent-loop records artifacts/evidence
-> Human Review Summary when needed
-> human confirms next stage or auto mode
-> agent-loop routes onward
```

External skills may not:

- skip `agent-loop` human gates
- create external default directories without explicit human request
- mark tasks `done`
- close a feature
- submit, commit, PR, merge, release, or publish
- update project memory outside the current `agent-loop` stage rules
- accept Delivery Contracts or approve breaking contract changes
- execute an active project-local skill without the current invocation Execution Gate

## Superpowers Mapping

Use Superpowers when available for these stages, while applying the path and gate override rules above.

| Agent-loop stage | Superpowers adapter | Borrow | Override |
|---|---|---|---|
| Requirements Discussion | `superpowers:brainstorming` plus PRD/product and grill-with-docs style helpers when available | context exploration, adaptive Brief/Standard synthesis, one-question-at-a-time, terminology, flows, exceptions, prior-feature conflicts | produce one response-local Requirement `product.md` draft; write it only through Product Human Review plus Requirement Record / Archive; do not create Feature artifacts |
| Brainstorm / Clarify if Needed | `superpowers:brainstorming` | context exploration, one-question-at-a-time, options, design approval | write to the owning stage artifact; do not write `docs/superpowers/specs/`; do not auto-transition to `writing-plans` |
| Project Skill Creation / Update | `superpowers:writing-skills` / `writing-skills`, plus `skill-creator` when available | RED/GREEN/REFACTOR, pressure testing, concise skill authoring, scaffolding, metadata generation, structural validation | Gate 1 before files; write only to `.agent-loop/skills/<skill-name>/`; activation only after validation; Execution Gate for every invocation |
| Legacy Product Brief compatibility | no writer helper | historical product intent from an existing Feature artifact | read only; route semantic conflict to Requirements Discussion / Recovery |
| Feature Spec | brainstorming/spec methods | ambiguity removal, scope check, acceptance thinking | write to `spec.md`; use agent-loop Human Review Summary |
| Plan Gate / Plan If Needed | `superpowers:writing-plans` | decide plan vs recorded No-Plan Decision; construction-grade plan, exact paths, test code, commands, expected outputs, no placeholders, self-review | write to `plan.md` or `plans/*`, or record No-Plan Decision only for trivial tasks; preserve Branch Context Evidence and never let plan approval authorize Git actions; do not write `docs/superpowers/plans/`; execution mode remains agent-loop controlled |
| Execute Task / Story | `superpowers:test-driven-development` | RED, verify RED, GREEN, verify GREEN, refactor | task status still controlled by Task Done Gate; evidence to `notes.md` |
| Diagnose Failure | `superpowers:systematic-debugging` | reproduce, isolate, trace root cause before fixing | findings to `notes.md`; return to Execute / Verify / Review |
| Verify | `superpowers:verification-before-completion` | evidence before completion claim | evidence to `notes.md`; completion still controlled by agent-loop |
| Review | `superpowers:requesting-code-review` | rigorous review pass | findings to `notes.md`; task moves to `done` only after Task Done Gate |
| Feature Completion Check | verification / finishing helpers when available | evidence discipline and close-decision support | agent-loop owns completion result, blocker routing, and close confirmation |
| Submit / Integrate | `superpowers:finishing-a-development-branch` | completion options and branch hygiene | submit still requires agent-loop Branch Strategy Check, sealed/customer-isolation checks, diff review, verification, drift check, and action-specific human confirmation |
| Pause / Close | finishing / handoff helpers when available | close options, handoff structure, and completion hygiene | close still requires Feature Completion Check, Feature Close Review, drift, memory status, and explicit human confirmation |
| Subagent execution | `superpowers:subagent-driven-development` | bounded independent execution with review | only after human confirms; briefs/returns in `handoffs/*`; main agent owns merge and status |

## Brainstorming Adapter

When `Brainstorm / Clarify if Needed` starts and Superpowers is available:

Requirements Discussion drafts the Requirement `product.md`; after Product Human Review plus Requirement Record / Archive, the Requirement README records only the effective pointer, lifecycle, Delivery Phase, Feature Mapping, and decision-link summaries. Feature Spec writes Product Slice to `spec.md` and evidence to `notes.md`. Existing Feature Product Briefs remain reader-only.

1. Use `superpowers:brainstorming` as the preferred method.
2. Inspect project context first.
3. Ask one high-impact question at a time.
4. Offer 2-3 approaches when meaningful.
5. Present a design summary for human approval.
6. Write approved content to the owning stage artifact: Requirement `product.md` only after Product Human Review plus Requirement Record / Archive, or Feature `spec.md` / `notes.md` during Feature Spec.
7. Do not create `docs/superpowers/specs/*` unless the human explicitly requests native Superpowers docs and confirms the external directory after path-override explanation.
8. Do not automatically transition to `superpowers:writing-plans`; recommend the next `agent-loop` stage.

## Requirement Product Definition Adapter

External PRD/product helpers cannot turn chat or Requirements Discussion directly into Feature `product.md`, a native PRD tree, an implementation authorization, or a deployment.

Map a helper Feature List to Product Capability Scope, translate its product content into a response-local Requirement `product.md` draft, and preserve human originals under the Requirement Set source policy. Do not create native `feature_list.md`, `PRD.md`, Feature `product.md`, prototype deployment, or helper-owned output trees. Only Product Human Review plus Requirement Record / Archive may write the draft; Product Review does not authorize Feature start.

## Grill-With-Docs Adapter

When a grill-with-docs style helper is available:

1. Use it as a clarification method inside Requirements Discussion or Feature-local Brainstorm / Clarify.
2. Load `requirement-product-grill.md` and keep agent-loop as the controller.
3. Inspect project memory, source requirements, code/docs/tests, and targeted prior feature artifacts before asking questions when relevant.
4. Ask one blocking question at a time and include the agent's recommended answer.
5. Write accepted product meaning to the Requirement `product.md` through its Human Review/Record Gate; keep Requirement README to pointer/lifecycle/mapping summaries; write Feature-local output to `spec.md` or `notes.md`.
6. Do not create `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/` from grill-with-docs defaults.
7. Cross-feature, shared design, hard-to-reverse, surprising, or real-trade-off findings are Design Readiness evidence and Decision Candidates for Decision & Design; they are not accepted ADRs.

## Writing-Plans Adapter

When `Plan Gate / Plan If Needed` starts and Superpowers is available:

1. Use `superpowers:writing-plans` as the preferred method.
2. First decide whether the selected task/story requires a construction-grade plan.
3. Require a construction-grade plan when the task is multi-file, behavior-changing, test-changing, interface-changing, data/API/async/security/deployment-related, cross-module, TDD-heavy, subagent-based, or human-requested.
4. If a plan is required, require exact files, code context, test code, commands, expected RED/GREEN output, no placeholders, and self-review.
5. Save the plan to `plan.md` for the active task/story, or to `plans/YYYY-MM-DD-<task>-<slug>.md` in complex artifact mode.
6. If a plan is not required, record the No-Plan Decision in `notes.md` and the selected task row/detail with exact files, exact verification command, and why no trigger applies.
7. Do not create `docs/superpowers/plans/*` unless the human explicitly requests native Superpowers docs and confirms the external directory after path-override explanation.
8. Do not let the external skill choose execution mode. Offer agent-loop modes: Strict Mode, Feature Auto-Loop, Task Auto-Run, or human-approved subagent execution. Task Auto-Run still requires an accepted plan.

## Project Skill Authoring Adapter

When Project Skill Creation / Update starts:

1. Load `references/project-skills.md`, `skill-routing.md`, and this adapter.
2. Classify entry mode. For an explicit request, resolve helpers before Candidate analysis and Gate 1. For a human-accepted proactive Candidate, treat Gate 1 as already satisfied and resolve helpers before the first authoring action; return to Gate 1 only for material scope change.
3. Resolve `superpowers:writing-skills` then `writing-skills`; load the complete helper before authoring actions.
4. Independently resolve `skill-creator`. A loaded writing-skills helper does not end the scan.
5. Use writing-skills for RED/GREEN/REFACTOR and forward tests. Use skill-creator for scaffolding, `agents/openai.yaml`, resource selection, and structural validation when available.
6. If helper instructions conflict, writing-skills controls test-first discipline and trigger-only descriptions; Agent Loop controls paths and gates.
7. For explicit-request entry, present Project Skill Candidate and Gate 1 before creating `.agent-loop/skills/`, INDEX, or the skill directory.
8. Override `~/.agents/skills/`, `~/.codex/skills/`, `~/.claude/skills/`, `.kimi/skills/`, and `docs/superpowers/` defaults to `.agent-loop/skills/<skill-name>/`.
9. Keep status `proposed` during authoring. Finalize the active INDEX row, record its exact-row SHA-256 plus the current-file manifest, and automatically mark `active` only after all required validation passes.
10. Before each real invocation, apply the bounded Execution Gate and emit its summary even when the human's named-skill/concrete-scope request already satisfies confirmation. Neither auto mode nor helper load authorizes execution.

## TDD Adapter

When `Execute Task / Story` starts and Superpowers is available:

1. Use `superpowers:test-driven-development` as the preferred method.
2. Follow RED/GREEN/REFACTOR when applicable.
3. If TDD cannot be followed, stop or mark the task `Human-gated`.
4. Record evidence in `notes.md`.
5. Move the task to `review`, not `done`, until Task Done Gate passes.

## Debugging Adapter

When verification fails or unexpected behavior appears:

1. Use `superpowers:systematic-debugging` as the preferred method.
2. Reproduce and identify root cause before proposing fixes.
3. Record root cause, evidence, fix decision, and follow-up verification in Feature `notes.md`; Bug Management may link the evidence in the Bug README.
4. The helper must not create, merge, close, reopen, or change Bug Records; select a Resolution Path; create a Requirement/Feature; mutate lifecycle; or widen Git authority.
5. Return to Execute / Verify / Review under `agent-loop`.

## Submit / Integrate Adapter

When `Submit / Integrate` starts and Superpowers is available:

1. Use `superpowers:finishing-a-development-branch` only for completion options, branch hygiene, and integration decision support.
2. Load `submit-and-integrate.md` and follow the agent-loop submit gate.
3. Inspect diff and untracked files before any integration action.
4. Confirm fresh verification evidence, required review, drift check, and project memory update status.
5. Separate product code changes from `agent-loop` artifact changes and unrelated dirty work.
6. Resolve Source Branch, Branch Class, Target Release Context, Target Branch, sealed state, customer isolation, and any cleanup evidence through `branch-management.md` when the optional strategy applies.
7. Present a Branch Strategy And Action Review before commit, PR text, merge note, branch deletion, release note, publish/release action, or any final submission claim.
8. Treat a human saying "commit" as permission to enter Submit / Integrate, not final commit approval.
9. When the Feature resolves Bugs, show Bug IDs, current Status, verification evidence, and unresolved Bug Close Decisions; finishing evidence cannot close/reopen a Bug or satisfy a Feature/Requirement/Bug Human Gate.
10. Do not let the external finishing skill create/switch/delete branches, commit, push, publish PR text, merge, tag, release, publish, close the Feature, close/reopen a Bug, or mark submission ready without the matching agent-loop confirmation.
11. After code integration, an external finishing helper cannot invent or bypass an observed memory conflict, resolve an unresolved semantic choice, satisfy the Memory Commit Gate, inherit Git authority, or recommend Source cleanup while a real conflict/restore remains unresolved. It must accept `reconciliation-not-needed` when no conflict exists. Full Memory Audit / Recovery and its Plan Hash/transaction controls require their own explicit Human authorization.

## Subagent Adapter

Subagents are optional and require explicit human confirmation before dispatch. A Feature Auto-Loop or Task Auto-Run grant is not subagent approval.

One confirmation may cover a bounded task group only when the agent first lists:

- task/story IDs or scan lanes included
- files or boundaries each subagent may inspect or change
- one brief per subagent
- stop conditions
- main-agent review and merge responsibility

Use only when:

- tasks or scan lanes are independent
- the context can be bounded
- each subagent has a clear brief
- the main agent can review and merge outputs

Artifact destinations:

```text
.agent-loop/features/<feature>/handoffs/<date>-<task>-brief.md
.agent-loop/features/<feature>/handoffs/<date>-<task>-return.md
.agent-loop/features/<feature>/notes.md summary
.agent-loop/features/<feature>/tasks.md status updates only after main-agent review
```

Project Skill authoring pressure tests are the no-feature exception: after the Candidate/Gate 1 explicitly satisfies every bounded-dispatch field above, persist approval, per-agent briefs, exact returns/rationalizations, main-agent review, and consumed status in `.agent-loop/skills/<skill-name>/validation.md`. Do not create a feature or `handoffs/` only for skill-authoring tests.

Record the approval date, approved task/story IDs or scan lanes, allowed file/boundary scope, and stop conditions in `notes.md` and each brief. Expanding the approved scope requires new human confirmation; old approval cannot be reused for new tasks or boundaries.

Authorization Status must be `active` immediately before dispatch. Reject `consumed`, `revoked`, or `expired` records even when IDs and boundaries are unchanged. Mark the authorization `consumed` after the approved dispatch group returns or is stopped; a retry or later dispatch requires fresh human confirmation and a new authorization record.

Subagents must never close a feature, submit code, update project memory directly, accept Delivery Contracts, or approve breaking contract changes. They must never mark tasks `done`. Only the main agent may mark a task `done` after Task Done Gate passes.

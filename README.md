# Agent Loop

**Current version:** 1.5.0

A reusable [Codex](https://github.com/openai/codex) / CLI-agent skill for single-person software development workflows—from goal intake to verified close.

## What It Is

**Agent Loop** is a controller skill. It tells the agent:

- What stage the project is in
- Which reference to load next
- What artifacts to produce or update
- When to stop and ask the human

The human controls goals, source requirements, and stage gates. The agent controls workflow mechanics, artifacts, implementation, verification, and backfill.

## Why Use It

Without a structured loop, agents tend to:

- Skip specification and jump straight to code
- Miss edge cases and drift from requirements
- Leave tasks "done" without fresh verification
- Lose project context between sessions

Agent Loop fixes this with a repeatable, inspectable workflow:

```
Message Intent → Chat And Requirements Discussion if needed
→ Project Entry → Remote Project Discovery if needed
→ Re-Adopt Agent Loop Project if needed
→ Project Entry Scan if needed
→ Project Skill Creation / Update if requested
→ Operational Support if needed
→ [internal] Lightweight Change Assessment for ordinary non-Bug changes
→ Requirement Archive
→ Decision & Design If Needed → Product Brief if needed
→ Brainstorm / Clarify if needed
→ Feature Follow-up / Flow-back if needed
→ Targeted Feature Scan if needed → Feature Spec → Requirement Checklist
→ Work Breakdown → Delivery Contract if needed → Test Design
→ E2E Discovery if Web → Technical Design / Code Context
→ Plan Gate / Plan if needed → Analyze Consistency
→ Subagent Execution if approved → Execute Task / Story
→ Verify → Review → Drift Check → Project Memory Update
→ Feature Completion Check → Submit / Integrate if requested
→ Pause / Close
```

## Core Concepts

| Concept | Meaning |
|---|---|
| **Feature** | One behavior-changing work area under `.agent-loop/features/<date>-<slug>/` |
| **Story** | User-perspective slice inside a feature (e.g. `US1`, `US2`) |
| **Task** | Default executable engineering unit. Small, verifiable, tied to a story. |
| **Plan** | Construction-grade execution plan for the active task/story |
| **Evidence** | Fresh proof: test output, build output, API results, E2E checks, logs |
| **Drift** | Mismatch between docs, code reality, or human decisions |
| **Lightweight Change Lane** | Internal route for bounded ordinary non-Bug changes: one persistent monthly card before target writes, adaptive Plan, targeted verification, diff review, rollback, Memory Review, and no unnecessary Feature workspace. |
| **Human-Guided Bug Management** | Stable Bug identity, evidence, deduplication, lifecycle, Human-confirmed Resolution Path, and a separate close decision inside Feature Follow-up / Flow-back. |
| **Feature Follow-up / Flow-back** | Repair ownership routing that scans Feature metadata for 90 days by default, extends on evidence, and sends every code fix through a Feature workflow. |
| **Operational Support** | Read-only code-guided help for testing, running, deploying, switching accounts/config/models/providers, quota checks, rollout, and production diagnosis before deciding whether feature work is needed. |
| **Project-Local Skill** | A reusable project capability under `.agent-loop/skills/<skill-name>/`. Creation or material update requires Gate 1; successful validation activates it, but every actual invocation still requires a bounded Execution Gate. |
| **Requirement Lifecycle / Backlog** | Requirement memory for proposed, accepted, deferred, in-progress, partially implemented, implemented, superseded, rejected, or reference-only requirements without using project memory as a backlog. |
| **Chat And Requirements Discussion** | `chat` answers or discusses without creating artifacts; `requirements-discussion → Brainstorm / Clarify → requirement document → requirements/` before any feature construction. |
| **Concept Foundation** | Triggered internal Requirements Discussion / Requirement Product Grill method. It stabilizes requirement-local Concept IDs and product meaning before flow, state, and product-data modeling; it is not a canonical stage or top-level artifact. |
| **Requirement Product Model** | Product-layer relationships, roles/permissions, commands/events, business flow, state, product objects/facts, invariants, and recovery derived from accepted concepts in the human-reviewed requirement document. |
| **Decision & Design / ADR** | Requirement-landing bridge for shared business flow, domain/data rules, architecture, recovery, and non-functional goals. Design Readiness is required; `.agent-loop/decisions/*.md` is Human-gated and conditionally required only when shared design needs a durable record. |
| **Delivery Contract** | Optional producer-consumer boundary handoff. Used only when API, event, public data, UI state/behavior, SDK/library, runtime, or explicit cross-agent/human handoff needs a stable contract. |
| **Post-Merge Memory Reconciliation** | After code is merged and verified, reconciles Base/Source/Target/Result Agent Loop claims into one Human-reviewed Desired Target Memory, with exact Apply, post-check, and restore. |

### Lightweight Change Lane

Bounded ordinary non-Bug changes persist one card under the active memory root at `changes/YYYY-MM/YYYY-MM-DD-<topic>.md` after clearly-eligible routing and before target writes. The creation month remains stable and is not Archive. Explicit Bugs keep Bug Management; public/data/state/security/architecture/unknown-impact changes use Feature. If the Agent is unsure, it asks the human with a recommendation before writing.

The card keeps Background, adaptive Plan, progress, targeted verification, rollback, result, and Memory Review across accidental context loss. Planned cross-session work, handoff, Subagent execution, long observation, and complex evidence still use Feature. A changes-only root does not mean the project is initialized.

Use `python3 <skill-root>/scripts/scan-lightweight-changes.py --project-root <project> --as-of YYYY-MM-DD` on macOS/POSIX, or `py -3 <skill-root>\scripts\scan-lightweight-changes.py ...` (`python` is also valid when it resolves Python 3.10+) on Windows. The read-only scanner validates all months. Three pending Changes or an oldest pending older than seven full calendar days triggers Agent-owned memory consolidation; high-evidence stable facts may sync to an existing reliable owner after exact scope disclosure, while uncertain meaning stays visible for human review.

The lane is not a canonical stage, Feature Type, Bug Resolution Path, shared backlog, Archive lifecycle, or Auto Mode. It does not lower production, external-service, paid-call, configuration-write, Git, submit, release, publish, Feature-close, or Bug lifecycle Human Gates.

### Human-Guided Branch Management

When a project has confused branch rules, an unclear target version, or customer-isolation risk, Agent Loop can recommend an optional branch strategy and wait for explicit human acceptance. Clear existing conventions and simple single-branch projects are preserved.

The optional profile separates retained standard/customer release aggregation branches from temporary `feature`, `bugfix`, and `hotfix` development branches. Formally released versions are sealed, customer customization stays isolated, and temporary cleanup requires merge evidence plus human confirmation. Strategy adoption does not authorize branch creation, switching, merge, deletion, push, tag, release, or publish. See the [human trigger examples and complete branch flow](Usage.md#我想让-agent-推荐分支管理方式).

### Post-Merge Memory Reconciliation

Code merge happens first. When Source and Target branches have changed Agent Loop memory, the Agent then inventories all four snapshots, checks each claim against the authority for that question, and proposes one Desired Target Memory instead of trusting a text merge or choosing one side globally.

A Memory Merge Report is created only after a Start Human Gate. Apply requires the exact reviewed Plan Hash, uses a confined transaction journal, and completes only after machine plus semantic post-check and a zero-change rescan. Failure restores only that memory transaction. Completion still does not authorize a memory commit, push, release, publish, or Source branch cleanup. See [usage and trigger examples](Usage.md#代码合并后我想校准-agent-loop-记忆).

## Artifact Layout

```
.agent-loop/
  remote.md                           # optional local-entry pointer for remote projects
  project.md                          # Long-term project memory
  project/                            # optional enterprise memory detail files
  decisions/                          # optional project / cross-feature Decision And Design Records
    0001-<decision-slug>.md
  skills/                             # optional, created only for a confirmed Project Skill Candidate
    INDEX.md                          # lifecycle, load policy, triggers, scope, and validation evidence
    <skill-name>/
      SKILL.md
      validation.md
      agents/openai.yaml              # optional
      references/                     # optional
      scripts/                        # optional
      assets/                         # optional
      templates/                      # optional
  onboarding-db/                      # Evidence-Graph + DDD project-understanding docs; legacy layouts are evidence only
  requirements/
    INDEX.md                           # optional inventory and backlog/deferred view
    YYYY-MM-DD-<topic>/
      README.md                        # requirement set lifecycle and source index
      requirement.*                     # optional source file when provided
      prototype.*                       # optional source file when provided
      feedback.*                        # optional source file when provided
      notes.*                           # optional source file when provided
  bugs/
    INDEX.md                           # Bug inventory, lifecycle summary, and stable locator
    YYYY-MM-DD-<bug-slug>/
      README.md                        # Bug facts, evidence links, lifecycle, Resolution Path, and close history
      evidence/                        # optional screenshots, logs, traces, and reproduction evidence
  memory-merges/                       # optional; created only for a Human-approved real reconciliation
    MM-<merged-code-short-sha>/
      README.md                        # exact plan, decisions, Apply/post-check/restore audit
  features/
    archive.md                         # locator for archived/rehydrated Feature IDs; not product authority
    YYYY-MM/                           # Human-gated directory archive for eligible closed features
      YYYY-MM-DD-<feature-slug>/       # complete feature directory moved intact
    YYYY-MM-DD-<feature-slug>/
      product.md    (optional)
      spec.md
      tasks.md
      tests.md
      plan.md
      notes.md
      contracts.md  (optional)
      tasks/        (optional complex details)
      tests/        (optional complex details)
      plans/        (optional dated plan cycles)
      handoffs/     (optional subagent briefs and returns)
      contracts/    (optional contract details)
```

Feature Monthly Archive keeps current work flat and moves only eligible, human-confirmed closed feature directories into their matching month bucket. It is location/index compaction, not content compression or deletion: the feature directory remains intact, while `features/archive.md` records the stable Feature ID and current path. Archive and rehydrate each require a read-only deterministic plan, the exact reviewed SHA-256, a separate Human Gate, transaction recovery, and post-check.

New target projects use `.agent-loop/` by default. Existing visible `agent-loop/` roots remain readable as legacy memory and should be migrated only after human confirmation.

## Quick Start

### 1. Install the Skill

Copy this directory into your agent's skill path:

```bash
# For Codex CLI
~/.codex/skills/agent-loop/

# For project-local use
./.kimi/skills/agent-loop/
```

### 2. Initialize a Project

Tell the agent:

> "Let's set up agent-loop for this project."

The agent will:
- Inspect the repo
- Classify the entry scenario (new / existing / remote / resume)
- Load the right references
- Propose `.agent-loop/project.md`, root `AGENTS.md`, and a `CLAUDE.md` pointer to `AGENTS.md`

For existing projects, the agent separates safe-entry memory from newcomer learning docs:

| Path | Use When |
|---|---|
| **Project Entry Scan** | Build enough project memory, root guidance status, commands, boundaries, capabilities, and uncertainties to continue work safely |
| **Evidence-Graph + DDD Onboarding** | Build `.agent-loop/onboarding-db/` as a newcomer handoff knowledge base after Project Entry Scan or reliable project memory |
| **Existing legacy onboarding-db files** | Evidence only; migration requires accepted Onboarding Spec, Onboarding Tasks, and Full Execution Gate |

### 3. Shape Requirements Before Features

> "先帮我梳理这个需求，不要实现。"

For requirement shaping, the agent should enter Requirements Discussion instead of creating a feature workspace. Requirement/Product Grill is the clarification method for fuzzy terminology, business flows, exception paths, prior feature conflicts, source-of-truth questions, and decision signals.

When a complex requirement can change concept identity, lifecycle, relationship, state, ownership, terminal meaning, or product facts, the internal Concept Foundation method triggers. The Agent first checks project/domain evidence, extracts a Concept Candidate Inventory, presents one recommended definition with evidence and accept/reject impact, then asks exactly one blocking question. Until the human confirms the blocking concepts, detailed business flow, product state, and product data modeling stop.

After acceptance, the effective requirement source derives a Requirement Product Model and traceability from stable Concept IDs. Feature `product.md` and `spec.md` record `Effective Concept Source` and reference those accepted IDs/model rows instead of redefining product semantics. If accepted meaning changes after archive, Agent Loop preserves the old source, reopens the gate, writes a human-confirmed append-only follow-up or new requirement set, and advances the requirement README pointer. Simple copy/style/config changes stay lightweight with a concrete `concept-foundation-not-needed` reason. Concept Foundation does not add a canonical stage, ADR, Design Skill, E2E Skill, or executable schema.

Reviewed requirements live under `.agent-loop/requirements/<date>-<topic>/`. If the human later asks to "落到 product.md" from chat or requirements discussion, Product Brief Source Gate applies: the agent first asks whether to create/reference a requirement set or confirm feature start. Feature-level `product.md` is written only after there is a requirement source and confirmed feature context.

During requirements discussion, the agent records Design Readiness evidence and Decision Candidates without creating ADR files. Before an accepted requirement enters feature construction, Design Readiness Check determines whether shared Decision & Design is required.

When the accepted requirement spans features or needs shared business-flow, domain, state, source-of-truth, architecture, recovery, or non-functional design, it enters Decision & Design even when no technology choice is disputed. A decision file is created only after human confirmation. The record assigns every required Design Slice to planned features before Feature Spec:

```text
Requirement -> Design Readiness Check -> Decision & Design If Needed -> Feature Mapping -> Product Brief / Feature Spec
```

Simple work records `design-not-needed` and can continue without a decision file. Feature-local choices stay in `spec.md` Design Decisions. Review and completion verify that implementation conforms to accepted design slices rather than checking feature stories alone.

For a requirement-driven ADR, the Agent first resolves an Effective Requirement Snapshot from the requirement README and accepted source. A source-wide Requirement Model Scope Inventory accounts for every stable relationship, permission, command/event, flow, state, product-model, and exception ID before the ADR selects its coherent scope. The ADR then gives every in-scope ID one Requirement Model Technical Landing Trace disposition. A `landed` row must name its concrete technical landing, preserved invariant, Design Slice, and verification target; incomplete inventory/coverage or `Upstream Compatibility: review-required` blocks ADR acceptance and dependent Feature Spec, Plan, and implementation work.

The ADR remains `proposed` while structural preflight runs. A passing validator authorizes review, not acceptance. Only explicit Decision & Design human acceptance permits recorded Human Review Evidence and `Status: accepted`, followed by accepted-mode validation. A reasoned `concept-foundation-not-needed` input uses an explicit trace-not-applicable branch without fabricated models. The ADR remains a consumer of product semantics: ambiguity returns to Requirements Discussion, while an incompatible accepted technical decision is preserved and superseded after Human Review instead of being rewritten.

Migration, compatibility, rollout, and rollback detail are operational landing concerns triggered only when the decision changes persistence representation, protocol/provider, runtime boundary, or rollout compatibility. Untriggered concerns keep one concrete reason and do not generate empty default design sections. This enhancement stays inside the existing ADR and adds no canonical stage, mapping artifact, lifecycle status, or executable schema.

### 4. Start a Feature

> "I want to add login."

After project init / Project Entry Scan is accepted, the agent will:

- Archive your requirement
- Write `spec.md` with stories and acceptance criteria
- Break down `tasks.md`
- Design `tests.md`
- Execute tasks with TDD

### 5. Get Guided Through An Existing Project

> "带我熟悉这个项目，从哪里开始看？"

Evidence-Graph + DDD Onboarding is the current durable project-understanding flow.

It builds `.agent-loop/onboarding-db/` from verified code evidence into macro-to-micro handoff docs:

- `08-review/evidence-graph.md` before formal docs
- Core Flow Inventory for business terminals, variants, owners, recovery responsibility, evidence chain, and planned/deferred selection
- `onboarding-spec.md` for module/flow coverage, Flow Slice Plan, DDD mapping, file strategy, quality gates, and batch plan
- `onboarding-tasks.md` for accepted batch execution
- module playbooks under `02-modules/<module-name>.md` by default
- flow playbooks under `03-flows/<flow-name>.md` by default
- coverage matrix and reviewed batch records

The agent must first confirm Project Entry Scan or reliable project memory, then build an Evidence Graph with Core Flow Inventory and present an Onboarding Spec for human review. Spec acceptance authorizes creation of Onboarding Tasks; formal onboarding docs begin only after the completed Tasks and their separate Full Execution Gate are accepted. Critical/important flows use Flow Slice Coverage and a completeness gate before quality scoring. Timeline/sequence is the primary per-flow narrative, supported by overview/boundary and state-machine views; extra diagrams are triggered by real recovery, data, transaction, async, decision, runtime, or troubleshooting complexity. Stateless topics do not invent state diagrams. Module and flow docs default to single long files, not many small files. The old Quick / Deep / Targeted onboarding modes and directory-first legacy generation flow are not used.

Existing legacy onboarding-db files may be read as evidence, but they are not trusted without checking code reality. Migration or replacement requires an accepted Onboarding Spec, Onboarding Tasks, and Full Execution Gate.

For focused project-understanding questions, the agent should answer from existing code/docs as `chat` or `operational-support`. It should only enter feature/fix work, requirement discussion, or a future onboarding-document workflow after the human confirms that intent.

### 6. Continue Later

> "Continue the login feature."

The agent reads `.agent-loop/project.md`, finds the active feature, and resumes from the last checkpoint.

### 7. Handle Bugs After Close

> "测试发现上次做的上传功能有 bug."

The agent does not immediately create a new feature. It first checks the full Bug Index for duplicate/reopen identity, then scans Feature metadata using a 90-day default ownership window and evidence-driven extension. After human confirmation it either flows the work back to the owning feature, creates a linked new feature, creates a `Feature Type: maintenance-fix` feature, routes product ambiguity to Requirements Discussion, or investigates first.

If a closed feature is reopened for follow-up, the original close record remains intact. The follow-up gets its own `notes.md` intake record, updated tasks/tests/plan as needed, fresh verification, review, drift check, and a new close confirmation.

If no recent feature owns the bugfix and the work is not a new product capability, the agent creates a narrow maintenance-fix feature under `.agent-loop/features/YYYY-MM-DD-fix-<slug>/`. Maintenance fixes still use spec/tasks/tests/plan/notes, fresh verification, review, drift check, project memory impact check, and close.

## Execution Modes

| Mode | Description |
|---|---|
| **Strict Mode** (default) | Agent asks before and after every stage |
| **Feature Auto-Loop** | After Requirement Checklist passes and Feature Spec is accepted, agent advances Agent-ready stages automatically |
| **Task Auto-Run** | After plan acceptance, agent runs Analyze Consistency and then completes one task/story through TDD, verification, review, and drift check |

Auto modes still stop for Human-gated decisions, unclear decisions, risky changes, failed verification, drift needing approval, unrelated dirty work blocking progress, human original requirement changes, first-version exclusions, Delivery Contract creation/acceptance/breaking changes, directory guidance changes, unapproved subagent dispatch, submit, pause, close, commit, PR, merge, release, or publish.

Agent Loop keeps at most one Active Feature. Switching work pauses the current feature with a resume point before another feature becomes active. If the agent-loop controller cannot be loaded, existing auto-mode grants are suspended and root guidance is limited to safe read-only entry/recovery/support until the controller is restored.

## Project-Local Skills

Say “把这个流程做成技能” or “把刚才成功的操作沉淀成 skill” when a repeatable, verified project workflow should become a resident capability. The agent may also propose a Project Skill Candidate after a complex operation succeeds, but it must wait for Gate 1 before creating or materially updating files.

Project skills are stored only in the target project under `.agent-loop/skills/`. New or updated skills use RED/GREEN/REFACTOR and remain `proposed` until validation passes; passing validation records a SHA-256 content manifest and automatically changes them to `active`, while failure or later content mismatch leaves them unavailable for normal routing.

The runtime/global Skill inventory does not replace `.agent-loop/skills/INDEX.md`. Project Skills may not appear as runtime-native Skill chips, so Agent Loop checks active INDEX metadata before a negative Project Skill claim or generic fallback, then verifies and loads only the matched Skill.

Discovery and loading are read-only. Before an active project skill follows its workflow, runs commands, calls tools, changes files, accesses external systems, or causes side effects, the agent must obtain an Execution Gate confirmation for one bounded invocation. `active`, `bootstrap`, Feature Auto-Loop, Task Auto-Run, or a prior invocation never grants reusable execution authority.

## External Skill Adapters

Agent Loop can use external skills such as Superpowers for brainstorming, construction-grade planning, TDD, debugging, verification, review, finishing, and bounded subagent execution.

Project Skill Creation / Update, Brainstorm, Plan Gate, Execute, Diagnose, Verify, Review, and approved Subagent Execution are mandatory helper-backed stages. Before stage actions, the agent resolves the canonical Superpowers name and unprefixed alias, loads the complete helper when found, and records the result. Fallback is permitted only after recording that the helper is unavailable or failed to load.

External skills are stage helpers only. Agent Loop still owns artifact paths, human gates, task status, project memory, drift, submit, pause, and close. Native external directories such as `docs/superpowers/*` are not created by default, even when a helper declares them as its normal destination.

## Delivery Contracts Are Optional

`contracts.md` is not a default artifact for every feature. The agent should suggest a Delivery Contract only when the human asks for cross-boundary handoff/API/interface documentation, or when the agent detects a likely downstream consumer such as frontend, another service, SDK user, shared event, public data schema, UI state contract, or runtime integration.

Simple single-person tasks, pure internal logic, and changes with no downstream consumer should skip contract files.

## When to Use

- Initialize agent-managed development in a new or existing project
- Re-adopt an old `agent-loop` project after code changed without updating docs
- Turn requirements or prototypes into specs, tasks, tests, plans, and implementation
- Continue a paused feature or recover project context
- Execute a task/story with TDD and verification
- Submit, pause, resume, or close a feature

## When NOT to Use

- One-off edits that explicitly bypass workflow
- Changes that do not affect feature behavior, public interfaces, or project memory

## Examples

See [`examples/`](./examples/):

- [`login-feature/`](./examples/login-feature/) — Small feature with TDD workflow
- [`complex-saas-project/`](./examples/complex-saas-project/) — Larger takeover + feature execution with delivery contracts
- [`remote-entry/`](./examples/remote-entry/) — Local directory pointing to a remote project

## Published Sources

`references/design.md` owns the core model and constraints; `references/runtime.md` owns executable routing, stage order, gates, and state transitions.

Both sources ship inside the skill package. Workspace-level design drafts may provide historical rationale, but they cannot override published behavior. Stage references, templates, validation scenarios, README, and Usage are derived views and must stay aligned with the published sources.

## License

MIT

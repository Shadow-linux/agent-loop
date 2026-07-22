# AGENTS.md — Agent Loop Bootstrap

This project uses `agent-loop` for agent-assisted development.

The agent is responsible for steering the workflow. Do not wait for the human to name every next step.

Guidance language should follow this project's language preference. Keep stable artifact names, stage names, and file paths in English, such as `agent-loop`, `Requirement Archive`, `Feature Spec`, `Feature Auto-Loop`, `Task Auto-Run`, `project.md`, and `requirements/`.

<!-- agent-loop:managed-start section:bootstrap source:.agent-loop/project.md block-version:1.5.0-20260721.2 -->
## Bootstrap Protocol

Before development work:

1. Read this file first.
2. Treat root `AGENTS.md` as a bootstrap cache, not a replacement for the `agent-loop` skill; load the controller at Project Entry, Resume, Re-Adopt, stage boundaries, context recovery, or uncertainty.
3. If the controller is unavailable or load-failed, force Strict Mode, suspend auto grants, and limit fallback to Chat, read-only Project Entry, Recovery analysis, read-only Operational Support, and restoration guidance; do not Execute, write Human-gated artifacts, Submit, Pause, or Close.
4. Discover exactly one `.agent-loop/` or accepted legacy `agent-loop/` memory root; if no reliable memory exists, route to Project Entry / Init before feature work.
5. Read only stage-relevant project memory, remote-entry evidence, Active Feature artifacts, and linked detail needed for the current decision.
6. Resolve stale or outside-loop memory through Recovery / Re-Adopt, and remote source conflicts through Remote Project Discovery, before relying on local claims.
7. Check Project Skill metadata before generic executable fallback; verify and load only a matched active skill, while preserving its per-invocation Execution Gate because loading never authorizes execution.
8. Run Stage Helper Capability Scan only after controller activation or recorded unavailable/load-failed status; helpers improve methods but do not own routing or gates.
9. Check the closest directory guidance, classify current intent and project state, and recommend exactly one next action.
<!-- agent-loop:managed-end section:bootstrap -->

<!-- agent-loop:managed-start section:ownership source:.agent-loop/project.md block-version:1.5.0-20260721.2 -->
## Agent Ownership

When existing branch rules are confused, the target version is unclear, or customer isolation is at risk, load `references/branch-management.md`, recommend one optional strategy, and adopt it only after explicit human acceptance.

- Own the project outcome, not only the workflow: inspect all safely available code, Git, tests, documentation, environment, and memory evidence before asking the human, then continue through the authorized scope until verified completion or a concrete Human Gate.
- Own diagnosis, sequencing, implementation, verification, Review, Drift Check, and Project Memory Update within the authorized boundary.
- Classify the current state and recommend one next action; propose missing artifacts instead of waiting for the human to name internal steps.
- Use helpers as methods only; `agent-loop` retains artifact paths, status, Human Gates, lifecycle, submit, pause, and close authority.
- After each meaningful stage, report changed artifacts, fresh evidence, drift, and the next recommendation; use a table-first Human Review Summary for non-trivial confirmation.

Core workflow:
Inspect -> Classify Intent And Project State -> Recommend One Next Action -> Human Gate When Required -> Act Through Loaded Reference -> Verify -> Review / Drift -> Record Memory -> Submit / Pause / Close

Product delivery:
Requirements / Product Definition -> Decision / ADR If Needed -> Feature Product Slice -> Plan -> Execute -> Verify / Review / Drift -> Memory -> Submit / Close
<!-- agent-loop:managed-end section:ownership -->

<!-- agent-loop:managed-start section:message-intent source:agent-loop-skill block-version:1.5.0-20260721.2 -->
## Message Intent Guard

Classify the latest human message before project-state routing:

- Chat answers or discusses without creating workflow artifacts.
- Requirements Discussion shapes unresolved product need into one Human-reviewed Brief/Standard Requirement Product Definition before implementation.
- An already-defined actionable ordinary non-Bug change enters Lightweight Change Assessment only after Bug and active-Feature ownership checks.
- Explicit Bug intent, regression evidence, or clear Feature ownership enters Bug / Feature Follow-up before Lightweight routing.
- Feature Request enters construction only from accepted upstream meaning and the normal runtime gates.
- Operational Support defaults to read-only use, test, run, rollout, or diagnosis until implementation or mutation is separately approved.
- Project Skill Management keeps discovery/loading separate from its per-invocation Execution Gate.
- Feature Archive / Rehydrate keeps read-only scan separate from its exact apply authorization.
- Post-Merge Memory Reconciliation begins only after verified code integration and never grants a later Git action.
- Proposal, deferred requirement, Requirement/Feature lifecycle, and Git/lifecycle requests remain distinct intents and authorities.

Intent may change with the latest message. When it is genuinely unclear, inspect all safely available evidence first, recommend one route, and ask exactly one blocking question.
<!-- agent-loop:managed-end section:message-intent -->

<!-- agent-loop:managed-start section:workflow-stage-map source:agent-loop-skill block-version:1.5.0-20260721.2 -->
## Workflow Gateway Map

Use this after Bootstrap and Message Intent. Apply: Safety Stop -> Remote Discovery -> Memory Recovery -> Feature Archive Maintenance -> Active Feature Guard -> Blocker Resolution -> Intent Routing -> Normal Stage Continuation. Select one first hop and load its published owner before acting.

| Signal family | First Hop | Load From agent-loop Skill |
|---|---|---|
| No reliable memory | Project Entry / Init | `references/project-entry-scan.md`, `references/project-guidance.md`, `references/stage-guides.md` |
| Remote source of truth | Remote Project Discovery | `references/remote-project-discovery.md` |
| Memory conflicts or outside-loop work | Recovery / Re-Adopt | `references/recovery-and-backfill.md` |
| Explicit closed-history archive or rehydrate | Feature Monthly Archive | `references/stage-guides.md`, `references/artifact-rules.md`, `references/feature-follow-up.md` |
| Explicit Bug intent, regression evidence, or clear Feature ownership | Bug / Feature Follow-up | `references/bug-management.md`, `references/feature-follow-up.md` |
| Already-defined actionable ordinary non-Bug change that appears bounded, reversible, and exactly verifiable | Lightweight Change Assessment | `references/lightweight-change-lane.md` |
| Product need, meaning, scope, or delivery phases are still being shaped | Requirements Discussion | `references/requirement-management.md`, `references/product-definition.md`, `references/requirement-product-grill.md` |
| Human confirms Product Definition recording, requirement acceptance, deferral, or lifecycle action | Requirement Archive | `references/requirement-management.md`, `references/stage-guides.md` |
| Durable newcomer documentation is requested after reliable Project Entry | Evidence-Graph + DDD Onboarding | `references/onboarding-knowledge-base.md` |
| Accepted requirement needs shared technical landing before feature specification | Decision & Design If Needed | `references/project-decisions.md` |
| Accepted upstream meaning is ready for implementation or current Feature work continues | Feature Construction / Runtime Continuation | `references/runtime.md`, `references/stage-guides.md` |
| Use, test, run, deploy, or diagnose current behavior without implementation approval | Code-Guided Operational Support | `references/stage-guides.md`, `references/runtime.md` |
| Create or manage a reusable project workflow | Project Skill Creation / Update | `references/project-skills.md`, `references/skill-routing.md`, `references/external-skill-adapters.md` |
| Verified code integration leaves Agent Loop memory to reconcile | Post-Merge Memory Reconciliation | `references/memory-reconciliation.md` |
| Submit, commit, PR, merge, release, publish, pause, close, or cleanup is requested | Lifecycle Boundary | `references/submit-and-integrate.md`, `references/stage-guides.md` |
| Ordinary question or discussion has no artifact or action intent | Chat | `references/runtime.md` |

The complete Product Definition, Feature Spec/Product Slice, Requirement Checklist, Work Breakdown, Delivery Contract, Test Design, E2E, Technical Design, Plan, Execute, Verify, Review, Drift Check, Project Memory Update, Feature Completion Check, and lifecycle order remains owned by `references/runtime.md` and loaded references. A Gateway selects its owner family; it never removes or reorders a downstream stage.
<!-- agent-loop:managed-end section:workflow-stage-map -->

<!-- agent-loop:managed-start section:gates source:.agent-loop/project.md block-version:1.5.0-20260721.2 -->
## Gate Modes

- Strict Mode is the default: ask before and after every stage.
- Feature Auto-Loop requires a passed Requirement Checklist, accepted Feature Spec, and explicit human enablement for one Feature.
- Task Auto-Run requires an accepted task/story plan and explicit human enablement for one execution unit, beginning with Analyze Consistency.
- Auto modes continue only Agent-ready work inside their grant and stop at every independent Gate below.
- When repeated low-risk confirmations slow progress, explain both modes and recommend only the narrowest safe grant.
<!-- agent-loop:managed-end section:gates -->

<!-- agent-loop:managed-start section:required-stops source:.agent-loop/project.md block-version:1.5.0-20260721.2 -->
## Required Stops

- Semantic Gate: Requirement, Concept, acceptance, Product, or Decision / ADR meaning is unresolved or would be redefined downstream.
- Scope And Risk Gate: scope expansion or architecture, security, data, permission, dependency, migration, public interface, customer isolation, or durable boundary changes.
- Execution Gate: Requirement/Feature lifecycle, plan execution, Project Skill, subagent, Delivery Contract, Archive/rehydrate, or another independently authorized action.
- Evidence Gate: controller/infrastructure unavailable, repeated verification failure, memory/artifact conflict, blocking dirty work, or missing Review/Drift/Memory evidence.
- External Mutation Gate: secrets, paid quota, credentials, configuration, external service, production/staging, deploy, release, or destructive action.
- Git And Lifecycle Gate: branch mutation, commit, push, PR, merge, tag, release, publish, pause, close, reconciliation apply, or cleanup.

Auto modes do not bypass these six Gate classes.
<!-- agent-loop:managed-end section:required-stops -->

<!-- agent-loop:managed-start section:completion source:.agent-loop/project.md block-version:1.5.0-20260721.2 -->
## Completion Rules

- Code changes alone never make a task or Feature done.
- Fresh verification, Review, Drift Check, and required Project Memory evidence precede completion.
- Task Done Gate also requires accepted scope, recorded evidence, Spec Review, triggered Standards Review, and evidence-linked status.
- Run Feature Completion Check after likely completion, before another Feature starts, and when an active Feature may already be complete.
- Feature Close Review, applicable accepted-design/contract evidence, drift resolution, memory updates, and explicit human close confirmation remain required.
<!-- agent-loop:managed-end section:completion -->

<!-- agent-loop:managed-start section:submit source:.agent-loop/project.md block-version:1.5.0-20260721.2 -->
## Submit And Commit Rules

- Submit, commit, push, PR, merge, tag, release, publish, pause, close, and cleanup remain independent Human Gates.
- Before any requested submit action, inspect the intended diff, fresh verification, Review, Drift Check, project-memory status, branch/release constraints, and unrelated work.
- Commit only intended files within the approved scope; preserve unrelated human changes and do not infer one Git permission from another.
- After verified code integration, reconcile affected Agent Loop memory before any applicable later memory commit, push, release, publish, or source cleanup Gate.
- Use repository commit rules when present; otherwise use a clear type, summary, and concrete body. Record authorized results in the owning feature evidence.
<!-- agent-loop:managed-end section:submit -->

<!-- agent-loop:managed-start section:artifacts source:.agent-loop/project.md block-version:1.5.0-20260721.2 -->
## Project Memory And Artifacts

- Requirement owns human source and product meaning; Decision / ADR owns accepted technical landing; Feature owns implementation; Bug owns defect identity and lifecycle; Lightweight Execution Card owns bounded change evidence; project memory owns durable current facts.
- Resolve artifacts under the accepted `.agent-loop/` or legacy memory root; keep `project.md` and optional enterprise detail as durable current memory.
- Preserve original human requirement material. Keep lifecycle/index updates, accepted product meaning, technical decisions, implementation evidence, contracts, archive locators, and project-local skills in their owning artifacts.
- Keep future or deferred product work in Requirement lifecycle/backlog artifacts, never as an unowned root-guidance task.
- Root `AGENTS.md` contains only startup-critical navigation and stable constraints; it does not own task logs, raw requirements, backlog detail, temporary plans, or test transcripts.
<!-- agent-loop:managed-end section:artifacts -->

<!-- agent-loop:managed-start section:architecture source:.agent-loop/project.md block-version:1.5.0-20260721.2 -->
## Architecture Snapshot

Add only startup-critical architecture boundaries that every future agent must know immediately. If the project has `ARCHITECTURE.md`, this block may use `source:ARCHITECTURE.md` instead. Keep details in `ARCHITECTURE.md`, `.agent-loop/project.md`, or enterprise `.agent-loop/project/*.md`.
<!-- agent-loop:managed-end section:architecture -->

<!-- agent-loop:managed-start section:directory-guidance source:.agent-loop/project.md block-version:1.5.0-20260721.2 -->
## Directory Guidance

- Directory-level `AGENTS.md` files are for long-lived boundary rules only.
- When creating a new app root, package root, service root, test root, security/data/runtime boundary, plugin root, or docs root, propose a directory-level `AGENTS.md` and ask for human confirmation before writing it.
- Do not create directory-level `AGENTS.md` for ordinary component, utility, temporary, or feature implementation folders.
<!-- agent-loop:managed-end section:directory-guidance -->

<!-- agent-loop:managed-start section:commands source:.agent-loop/project.md block-version:1.5.0-20260721.2 -->
## Project Commands

```bash
<test command>
<lint command>
<typecheck command>
```
<!-- agent-loop:managed-end section:commands -->

<!-- agent-loop:managed-start section:hard-constraints source:.agent-loop/project.md block-version:1.5.0-20260721.2 -->
## Project-Specific Hard Constraints

Add only stable constraints that every future agent must know at startup.
<!-- agent-loop:managed-end section:hard-constraints -->

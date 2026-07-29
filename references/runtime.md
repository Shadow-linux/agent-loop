# Agent Loop Runtime Protocol

This is the required operating protocol. Load this file before any other reference.

## Runtime Contract

The agent runs one loop turn at a time:

```text
Inspect -> Classify -> Recommend -> Confirm -> Act -> Record -> Recommend
```

Do not jump from a human goal directly to code. Do not move to a later stage until the prior stage artifact is accepted or the owning stage explicitly permits a human bypass. Product Human Review confirmation cannot be bypassed for a new Effective Product Definition.

Root `AGENTS.md` is the startup projection: controller bootstrap, Message Intent, first-hop Workflow Gateway Map, Agent Ownership, Human Gates, completion, submit, and artifact authority. This file remains the executable owner of routing precedence and the complete leaf-stage order. A root gateway selects the owning reference family; it does not remove or reorder downstream stages.

Bootstrap skill loading: AGENTS.md is bootstrap guidance, not a replacement for the agent-loop skill. If the current runtime exposes the agent-loop skill, load/use it before making workflow decisions during Project Entry, Resume, Re-Adopt, stage boundaries, after context compaction, after long-running sessions, or whenever workflow state is uncertain. Stage Helper Capability Scan happens only after the agent-loop controller is active or unavailable/load-failed because helper scan resolves stage methods, not the controller itself. If the skill is unavailable or load-failed, force Strict Mode, suspend existing auto-mode grants, and use root guidance only for Chat, read-only Project Entry, Re-Adopt / Recovery analysis, read-only Operational Support, and reporting how to restore the skill. Do not Execute, write Human-gated artifacts, Submit, Pause, or Close without the controller.

Agent ownership is mandatory. The agent must not wait for the human to name the next internal stage. For every human goal, bug report, project-understanding question, vague product idea, or "what next" request, the agent classifies the current state and recommends exactly one next action with a reason. If required artifacts are missing, recommend creating or repairing them. If work appears ready, recommend the next stage. If work appears complete, run Feature Completion Check and recommend close, pause, or continue.

An explicit safe one-off request is compatibility input to Lightweight Change Assessment, not a separate execution bypass. A bounded ordinary non-Bug edit may use the persistent Lightweight Execution Card only after eligibility, scope, verification, rollback, memory, branch, and gate checks pass.

These checks cannot be bypassed inside `agent-loop`: Project Entry classification, re-adoption minimum reconciliation, human source requirement preservation, Product Human Review confirmation for a new Effective Product Definition, Onboarding Spec acceptance and the later Full Execution Gate, Task Done Gate, Delivery Contract acceptance or breaking-change gate, fresh verification before completion claims, submit confirmation, and close confirmation.

## Message Intent Classification

Message intent is evaluated before project state classification. It decides what the latest human message is asking the agent to do; Entry Classification still decides the project state.

| Intent | Condition | Default Action |
|---|---|---|
| `chat` | chat means ordinary discussion, rules questions, status questions, or design talk with no request to create requirements or start implementation | answer or discuss only |
| `requirements-discussion` | requirements-discussion means the human is exploring product needs, business goals, capability ideas, constraints, tradeoffs, or user scenarios without authorizing implementation | Requirements Discussion with Adaptive Product Definition |
| `project-skill-management` | human asks to turn a repeatable project workflow into a project-local skill, or to update, disable, or deprecate one | Project Skill Creation / Update after reliable Project Entry/memory |
| `feature-archive-maintenance` | human explicitly asks to archive closed feature history by month or rehydrate an archived feature | Feature Monthly Archive after reliable memory; read-only scan first |
| `feature-request` | human explicitly asks to implement, build, change behavior, or start work from accepted requirements | Project Entry, then Effective Product Definition, Design Readiness, Decision & Design / Feature Spec / Feature Follow-up routing |
| `proposal-doc` | human asks to write a proposal, design note, or discussion document without implementing | write the requested proposal/doc only |
| `deferred-requirement` | human asks to remember, defer, backlog, or do something later | Requirement Archive with Future / Deferred Requirement Intake |
| `operational-support` | human asks to use current project code/processes to test, run, deploy, switch config/account/model/provider, diagnose, roll out, or create a runbook | Code-Guided Operational Support |
| `feature-follow-up` | explicit defect/regression/QA/post-close evidence or clear Feature ownership indicates follow-up work; generic “small tweak” alone is insufficient | Feature Follow-up / Flow-back after project memory is available |
| `unknown` | message could reasonably mean chat, requirements discussion, feature work, follow-up, or operational support | ask a clarifying question |

If message intent is `chat`, do not create requirement sets, feature workspaces, tasks, tests, or plans. Answer, explain, or discuss. If the chat turns into demand shaping, reclassify as `requirements-discussion`.

If message intent is `requirements-discussion`, do not create a Feature workspace or enter Work Breakdown, Plan Gate, or Execute. Route to Requirements Discussion: inspect sources, brainstorm/clarify, record Product Definition Profile: `brief | standard`, draft one human-reviewed Requirement `product.md`, then write it under `.agent-loop/requirements/<record-date>-<topic>/` only after Product Human Review plus Requirement Record / Archive confirmation. Product Review/recorded does not mean Requirement accepted for implementation and does not authorize Feature, ADR, code, or Git actions.

If message intent is `project-skill-management`, load `references/project-skills.md`. Do not create a requirement set or feature workspace. Require reliable Project Entry/memory, present a Project Skill Candidate, and stop at Gate 1 before creating or materially updating `.agent-loop/skills/`.

If message intent is `feature-archive-maintenance`, require current project memory and load the Feature Monthly Archive procedure. The scan is read-only. It resolves Feature IDs through `features/archive.md`, shows eligible/blocked candidates, exact moves, reference edits, advisory reference findings, unchanged content, restore scope, and the expected plan SHA-256. Scan/check never authorize or reject Archive from symlink, unsupported-reference, or unrelated-layout findings: the Agent decides whether reference coverage is sufficient, explains evidence and residual risk, and recommends either the Batch Human Gate or one blocking question. Archive or rehydrate stops at that exact-plan Gate and then uses a transaction journal, post-check, and restore. The invariant is: rehydrate before reopened execution; archive state is not feature lifecycle.

Requirement/Product Grill may be used inside Requirements Discussion and its Brainstorm / Clarify work when terminology, roles, business flows, exception paths, prior Feature behavior, or decision signals are unclear. It does not create a new stage. Product Definition Depth Scan, Product Completeness Scan, Concept Foundation, Requirement Product Model, and derived visual generation are internal Requirements Discussion methods, not canonical stages or message intents. They write only through the reviewed Requirement `product.md` and send shared design signals to Design Readiness Check.

Optional Visual Communication is also an internal method, not a stage or mandatory helper. When a Visual Trigger exists, it may render a bounded working view so the human can correct flow, boundary, state, sequence, relationship, or option meaning before the Agent rewrites the owning text. Prefer a matching active project-local visual skill, then installed Archify. If Archify is absent and would materially improve review, recommend its exact installation/use before offering Markdown, table, Mermaid, or ASCII; use fallback directly only when Archify is not justified, the human declines, the environment is unsupported, or installation/use fails.

Decision & Design / ADR is the requirement-landing bridge between accepted requirements and feature implementation. Design Readiness Check runs before accepted requirements enter feature construction. Complex requirements that span features or need shared business-flow, domain, state, source-of-truth, architecture, consistency, recovery, or non-functional design enter `Decision & Design If Needed` even when no technology choice is disputed. Ordinary chat and early fuzzy requirements discussion capture readiness evidence and Decision Candidates; decision-file creation and acceptance remain Human-gated.

Message intent is not permanent; reclassify when the conversation changes intent.

Chat defaults to answer-only, but it may convert to `requirements-discussion`, `proposal-doc`, `feature-request`, `operational-support`, `feature-follow-up`, or `deferred-requirement` when the human intent changes. Do not keep using `chat` merely because the conversation started as chat.

If the human explicitly says they only want to discuss and do not want documentation yet, keep the intent as `chat` until they ask to shape, record, or archive the requirement.

If unclear whether the human wants ordinary chat or requirements discussion, ask whether to keep discussing or shape the topic into a requirements document.

If unclear whether the human wants requirements discussion or Feature implementation, ask whether to form and review a Requirement Product Definition first or start Feature construction from an already accepted one.

## Human-Guided Bug Management

Bug Management is an internal method of `Feature Follow-up / Flow-back`; it does not add a canonical stage or message-intent value. Ordinary chat and read-only error explanation do not create Bug artifacts. With explicit bug-report, record, manage, investigate, or fix intent, use this sequence:

```text
explicit bug intent
-> reliable memory or Project Entry
-> complete Bug Index metadata duplicate/reopen scan
-> 90-day Feature metadata scan
-> evidence-ranked deep read / evidence-driven extended scan
-> create/update/reopen Bug Record as reported/triaging
-> resolve Expected Behavior evidence
-> confirmed or non-fix disposition candidate
-> recommend one Resolution Path
-> Resolution Path Human Gate
-> existing Requirement / Feature / Verify / Close stages
```

Bug Status is exactly `reported | triaging | confirmed | in-progress | verifying | deferred | closed`. Bug Resolution is exactly `unresolved | fixed | duplicate | not-a-bug | cannot-reproduce | accepted-risk | superseded`. Status and Resolution are independent: `closed` cannot use `unresolved`, `deferred` is not closed, and reopen appends history and restores `unresolved`.

An `in-progress` Bug requires `flow-back | linked-feature | maintenance-fix` plus one Human-confirmed Fix Feature Target. `investigate-first`, `requirement`, and `no-fix` do not represent Feature repair execution and must not use `Status: in-progress`.

The Bug Record owns identity, facts, Report Origin, evidence, lifecycle, Resolution Path, verification, close, and reopen history. Requirement owns product meaning; links are optional `0..N` and do not automatically mutate lifecycle. Feature owns all repair tasks, tests, plans, code execution, verification, Review, and Drift. A Bug has one current Resolution Path; one coherent Feature may resolve multiple Bugs.

Scan all Bug Index metadata without a time cutoff for duplicate/reopen identity. Feature ownership uses the project-configured default 90-day metadata/summary scan, evidence-ranked candidate deep read, and evidence-triggered extended scan beyond 90 days. Calculate age from Feature `Last Updated` / `Closed`, not archive month, directory mtime, or archive operation time.

Archive changes Feature location, not identity or ownership. Resolve archived candidates through the unique valid `features/archive.md` locator. Discovery and Human Review are read-only and do not require rehydrate. After flow-back is confirmed and before reopened execution, use the existing exact-hash Human-gated rehydrate transaction and post-check.

Fail closed on Index/README mismatch, ambiguous or cyclic duplicate target, invalid Status/Resolution pairing, missing Resolution Target for `flow-back | linked-feature | maintenance-fix | requirement`, Requirement/Feature/ADR/Contract Expected Behavior conflict, archive locator inconsistency, expired-only verification evidence, or any Bug/Feature/Requirement/Git action without its named Human Gate. Record the evidence and recommend exactly one investigation, Recovery, or human decision.

Bug confirmation, Severity/Priority, accepted Requirement, Feature plan, successful tests, Auto Mode, Bug close, submit, commit, or push approval never authorizes a different gate. Passing repair tests may move a Bug to `verifying`; only complete Bug-specific evidence and the Bug Close Gate permit `closed`.

## Lightweight Change Lane

Lightweight Change Lane is an internal route before Feature construction, not a canonical stage, message-intent value, Feature Type, Bug Resolution Path, task status, lifecycle, or Auto Mode. Load `references/lightweight-change-lane.md` for the detailed authority.

Apply this sequence exactly:

```text
explicit Bug management intent
-> Human-Guided Bug Management

actionable non-Bug change
-> Lightweight Change Assessment
   -> clearly eligible -> Lightweight Execution Card
   -> Feature trigger -> Feature Construction
   -> uncertain -> Human Choice with Agent Recommendation
```

Explicit Bug Management wins before assessment. An active Feature that clearly owns the change also blocks lane escape. Generic `fix`, “修一下”, “改一下”, “small tweak”, line count, file count, or step count does not decide eligibility.

After Project Entry classification, perform only the minimum root-guidance, Git/dirty-state, target-scope, nearby-reference, safety, verification-entry, active-Feature, branch, sealed-release, and relied-on-memory checks needed for the route. A stale or conflicting memory claim that the route relies on stops for Recovery, Feature Construction, or Human Choice.

Discover the accepted memory root before card creation. Reuse exactly one logical `.agent-loop/` or legacy `agent-loop/` root. One internal alias is allowed only when it resolves to an existing project directory without cycle or dual authority; keep generated paths under the logical root name. Dual roots, root files, broken/cyclic/external aliases, or alias retarget drift fail closed. When neither exists, the first clearly eligible Change may create only `.agent-loop/changes/YYYY-MM/`; a changes-only root is not reliable project initialization and must not create `project.md`, enterprise memory, root guidance, or a Feature workspace by implication.

`clearly eligible` requires a clear goal and completion criteria, enumerable scope, no new product/technical decision, no public/data/state/permission/security/dependency/migration/architecture boundary, exact targeted verification, concrete rollback, no Bug/Feature long-term tracking need, no planned multi-session/handoff/subagent/long-observation need, and sufficient current evidence. Any missing condition produces `Feature trigger` or `uncertain`.

After `clearly eligible` routing and before the first target code/configuration/documentation write, create one parser-valid card at `<memory-root>/changes/YYYY-MM/YYYY-MM-DD-<topic>.md`. The card file is the execution source of truth; response summaries are derived views. The month, filename date, H1 topic, and `Created At` must agree. Existing paths use the first unused `-2`, `-3`, or later suffix and are never overwritten. A Plan is always required but its depth is adaptive. Fact/config/path/domain/docs changes use failure-matched parsing, reference, residual, syntax, or bounded dry-run checks; isolated behavior logic uses the smallest meaningful RED/GREEN and focused regression. The lane does not enter mandatory Plan Gate / Plan or Execute Task / Story helper stages.

The monthly partition is stable and is not Archive. Status is exactly `in-progress | completed | stopped`; Memory Review and Memory Result are separate axes. Completion requires Plan closure/explanation, fresh targeted verification, diff/scope review, concrete rollback, Result / Residuals, and valid actual Memory Evidence/Target. Do not add Change README/INDEX/archive/move/rehydrate/restore lifecycle, scheduler, shared counter, new stage, message intent, Feature Type, Bug path, or Auto Mode.

One accidentally interrupted `in-progress` card may resume only after revalidating current branch, full HEAD, dirty work, target files/consumers, persisted Scope/Plan/progress, eligibility, verification, and rollback. Any divergence stops for Human Choice. Planned multi-session work, pause/resume lifecycle, handoff, Subagent execution, long observation, and complex evidence remain Feature hard triggers.

When reliable project memory exists, Project Skill Discovery Guard still runs before generic action or helper fallback. A matched active Project Skill keeps manifest validation and its per-invocation Execution Gate; it cannot widen the card.

When route evidence is uncertain, stop with few real options, one Agent recommendation, concrete evidence/unknowns, and zero writes before the human answer. Human choice cannot override a Feature hard trigger, sealed release, customer isolation, or action-specific gate.

Scope expansion stops the lane before broader edits. Preserve the current investigation, diff, and verification evidence; name the trigger; recommend exactly one Bug Management, Requirements Discussion, or Feature Construction route; and ask before keeping, reverting, or extending partial edits.

Completion requires executed-or-explained Plan steps, fresh targeted verification, diff/scope review, valid rollback, durable-memory impact review, and Result / Residuals. After completion, run `scripts/scan-lightweight-changes.py` and keep pending/human-review results visible. Card completion grants no Feature/Bug lifecycle, branch, submit, commit, push, PR, merge, tag, release, publish, production, paid-call, configuration-write, deployment, destructive, or external action.

Run the read-only Python 3.10+ standard-library scanner at Project Entry when Changes exist, after every Change completion, and before release. Use `python3 <skill-root>/scripts/scan-lightweight-changes.py --project-root <target-project-root> --as-of <current-local-date>` on macOS/POSIX and `py -3 <skill-root>\scripts\scan-lightweight-changes.py --project-root <target-project-root> --as-of <current-local-date>` on Windows. Scanner `pending-count` or `pending-age` starts proactive Change Memory Consolidation; exactly seven days does not trigger. Known memory drift and pre-release pending/human-review are controller fact events, not scanner flags. Post-merge reconciliation does not trigger this scanner unless the observed conflict directly involves Change evidence.

The scanner validates and inventories only. The Agent owns semantic grouping and may directly sync a Change-derived fact only when the source has fresh verification, the fact is implemented and stable, one existing reliable memory target owns it, authorities do not conflict, no new decision is created, branch/release/customer scope is clear, exact target/fact/evidence/impact/rollback is disclosed before write, post-check is possible, and rollback touches only the Agent's edit. A changes-only root cannot create `project.md`, enterprise memory, or switch modes. Uncertain candidates become visible `human-review`; project memory never copies card history, pending backlog, or command logs.

Consolidation validates, groups by fact, changes only owning memory files, post-checks format/reference/fact/residual consistency, restores only its own memory writes on failure, leaves source Changes pending after failure, updates their Memory fields only after success, and never creates a recursive Change. Code merge completes before Target memory reconciliation. If an observed conflict directly involves a Change-derived fact, read only that card and minimum direct evidence to recheck its Source `synced` claim.

## Adaptive Product Definition Internal Routing

During Requirements Discussion, load `product-definition.md` and choose exactly one documentation depth:

```text
brief | standard
```

Brief requires every lightweight eligibility condition. Any product-definition trigger or uncertainty selects Standard. Profile depth is not a lifecycle, stage, message intent, or authorization. New evidence may upgrade a response-local Brief draft to Standard without creating another Requirement Set.

For Standard, classify the internal Concept Foundation method before drafting detailed business flow, product state, or product facts:

```text
candidate | accepted | reopened | concept-foundation-not-needed
```

Enter `candidate` when any current requirement signal can change downstream product meaning: one term covers multiple objects/actions/results; a business object gains or changes identity or lifecycle; multiple actors/tenants/systems participate; work spans features; ownership, balance, inventory, approval, order, task, quota, or other fact-source semantics matter; current language conflicts with project Domain Language, code, tests, or historical features.

Use `concept-foundation-not-needed` only for a simple change with no product-semantic, identity, lifecycle, ownership, state, relationship, cross-role, cross-feature, or data meaning change. Record one concrete reason; do not use it to bypass ordinary ambiguity.

`accepted` requires human confirmation of every blocking concept meaning. `reopened` means later requirement evidence invalidated an accepted meaning and returns to the same gate.

Before record/archive, the response-local `product.md` draft carries internal evidence. After record/archive, preserve human originals and prior confirmed Product Definitions: mark the internal method `reopened` response-locally, stop downstream work, run Requirement Conflict Review, and ask before writing `YYYY-MM-DD-product-follow-up-<slug>.md` or a linked replacement Requirement Set. README `Effective Product Definition` points to the current reviewed source without duplicating product meaning. Older sets retain `Effective Concept Foundation` reader compatibility and are not bulk-migrated.

Do not enter Business Flow, State Model, or Product Data Model while a triggered Concept Foundation is `candidate` or `reopened`.

After internal `accepted`, derive only the applicable Requirement Product Model views from accepted Concept IDs: Concept Relationships, Role / Permission Matrix, Commands / Events, Primary Business Flow, Product State Model, product-layer objects/facts/invariants, and Exception / Recovery behavior. Standard `Product View Applicability` records `included | not-applicable` with evidence; do not create placeholder IDs. This product model does not select tables, documents, events, ledgers, providers, transactions, or other technical representations.

Before Product Human Review, run Product Completeness Scan across product value, user result, semantics, experience, operations, technical readiness, and testability. Automated validators cannot replace semantic judgment. Product Review confirmation and Requirement lifecycle remain separate.

## Human Grill Contract

When Concept Foundation is triggered, one interaction turn follows this order:

1. inspect available evidence: project Domain Language, source requirements, relevant code/docs/tests, and targeted historical feature artifacts;
2. extract candidate concepts from concrete scenarios, including nouns, actions, outcomes, constraints, synonyms, overloaded terms, and conflicts;
3. present one recommended definition with Concept ID, evidence, identity/lifecycle boundary, downstream impact if accepted, and downstream impact if rejected;
4. ask exactly one downstream-blocking question and wait for the human answer.

Do not replace step 4 with a batch of concept questions. Generic Brainstorm / Clarify question-count flexibility does not override this contract. Non-blocking uncertainties remain recorded without delaying the one blocking decision.

The Human Grill answer resolves one product-semantic blocker inside Requirements Discussion. It does not confirm the complete Product Definition, accept Requirement lifecycle, authorize Requirement Record / Archive writes, create an ADR, or start Feature construction.

## Optional Visual Communication Adapter

Use this bounded internal method in Requirements Discussion first, and in Feature Spec, Decision & Design, Onboarding Knowledge Base, or review/close communication only when a Visual Trigger exists.

```text
Current Agent Loop stage and owning semantic artifact
→ detect Visual Trigger
→ resolve matching active project-local visual skill
→ otherwise resolve installed Archify
→ unavailable but materially useful: recommend Archify before offering Mermaid / table / ASCII fallback
→ not justified, declined, unsupported, or failed: continue with text/Mermaid/ASCII
→ available: obtain one Visual Scope Grant
→ render and iterate only inside that scope
→ human corrects or confirms meaning
→ Agent rewrites the owning semantic artifact
→ optional, separately confirmed durable source/render record
→ existing Product Review, ADR acceptance, Onboarding review, Feature, or Git gate
```

A Visual Trigger exists when prose alone makes a multi-step flow, state/lifecycle, boundary, sequence, data flow, relationship, option comparison, or cross-role interaction materially hard to verify. Adapter availability alone is not a trigger.

Feature Spec may use a visual only to explain the accepted Product Slice, feature responsibility, or feature-local implementation and acceptance path. Rewrite accepted feature-local clarification into `spec.md`. If the view reveals a new product concept, role/permission, relationship, flow, state, invariant, terminal, fact ownership, or product rule, stop Feature Spec and return to Requirements Discussion; never add that meaning to `spec.md` or edit Requirement `product.md` from the Feature Spec stage.

The Visual Scope Grant must name the current stage, review question, authoritative source and stable IDs, diagram type, working-output location, and permitted iteration boundary. One grant covers iterative edits that answer the same question from the same source with the same type and working-output class. A new source, stage, diagram type, durable path, external side effect, or material semantic question requires a new grant.

Archify upstream is <https://github.com/tt-a1i/archify>. If unavailable and useful, recommend it rather than silently installing it or presenting Mermaid as the default first drawing path. Before installation, disclose the exact source and revision, command, target/runtime location, network and file effects, whether the install is global, the doctor/verification command, and the no-install fallback. Human authorization covers only that exact Installation Authorization. Agent Loop does not vendor Archify or hardcode one universal installer across runtimes. Use fallback directly only when Archify is not materially justified, the human declines, the environment cannot support it, or installation/use fails.

Installation Authorization, Visual Scope Grant, durable visual recording, Product Human Review, ADR acceptance, Onboarding review, Feature start, and Git/release actions are independent gates. One never implies another. Installation failure cannot elevate privileges, switch source/mirror/package manager/location, or retry a materially different command without renewed authorization.

Use `render to converge, text to record`: a working render helps the human and Agent converge, while the owning Markdown remains semantic authority. A durable visual uses `source-render-v1`: accepted semantic artifact and stable IDs → typed Archify JSON source → validated derived render. Both files and their digests are recorded; stale, missing, mismatched, or HTML-only output is never current evidence.

Before confirming the complete Product Definition, load `references/human-review-summary.md` and present the cumulative Product Definition Approval summary. It shows Profile, source evidence, all included/not-applicable views, confirmed concepts/rules, blockers, visual freshness, Design Readiness candidates, and the explicit product decision. It does not replace the one-question-per-turn Grill Contract and does not authorize implementation or Git actions.

## Human-Guided Branch Management

Branch management is an internal Branch Strategy Check, not a canonical stage. Do not force a simple project or a project with clear existing rules to migrate. During Project Entry, Project Entry Scan, Re-Adopt, versioned delivery planning, Drift Check, and Submit / Integrate, inspect evidence in this order:

```text
human-confirmed native repository policy
-> accepted project.md Branch Strategy snapshot
-> current local and remote Git reality
-> Agent inference from branch names
```

Then compare the current feature notes, accepted plan, and Submit / Integrate evidence with that policy/reality chain; those volatile records do not outrank durable policy.

When the evidence is coherent, preserve the existing strategy and record `Profile: existing-project` only after the human confirms the durable summary. When branch rules are confused, Target Release Context is missing, or customer isolation is at risk, load `references/branch-management.md` and recommend the optional Human-Guided profile. The Strategy Adoption Gate has these outcomes:

```text
accepted | declined | not-needed
```

`accepted` records the human-confirmed `existing-project` or `human-guided-release` profile. `declined` records `Profile: not-applicable` plus a concrete Decline Reason so a rejected recommendation cannot appear to be current policy. `not-needed` records `Profile: existing-project` and the reason the project remains lightweight.

An unconfirmed recommendation is not `accepted`. Recommendation and adoption do not authorize branch creation, switching, merge, deletion, push, tag, release, or publish. A Branch Action Gate confirms creation or switching of one exact development branch; every other Git mutation keeps its existing action-specific Human Gate.

The optional profile uses retained aggregation branches:

```text
standard release: release/vX.Y.Z
customer release: customer/<customer>/vX.Y.Z
standard development: feature|bugfix|hotfix/vX.Y.Z/<topic>
customer development: feature|bugfix|hotfix/<customer>-vX.Y.Z/<topic>
```

`project.md` owns only the human-confirmed durable strategy and the current Target Release Context pointer. Feature `notes.md`, accepted `plan.md`, and Submit / Integrate records own mutable Current Branch Context. Do not create a default `.agent-loop/branches/` directory or mapping artifact.

A formally released version is `released / sealed`. Same-version repair is blocked and must target a new patch release; a new capability requires a human-confirmed new version. A customer branch must not flow wholesale into `main` or a standard release branch. Shared fixes move through an explicitly reviewed standard development path, not reverse-merging the customer aggregation line.

Apply branch-specific fail-closed conditions only when an adopted Branch Strategy or versioned/customer delivery applies. A human-confirmed simple `not-needed` path does not require Target Release Context or Target Branch and continues through the normal non-versioned workflow. Otherwise fail closed when accepted policy, Target Release Context, and Git reality disagree; when target kind/version/customer cannot be resolved; when the target is sealed; when customer isolation would be violated; or when a requested mutation lacks explicit authorization. Record the mismatch, recommend exactly one correction or human decision, and do not infer permission from an accepted strategy.

## ADR Requirement Model Technical Landing

When Decision & Design is driven by accepted product semantics, resolve Requirement README `Effective Product Definition` before drafting or reusing an ADR. The effective source must be Product Review `confirmed`. Older Requirement Sets resolve their historical `Effective Concept Foundation` / reviewed `requirement.md` through the legacy reader; never require destructive migration or allow both pointers.

Record this Effective Requirement Snapshot in the existing decision record:

```text
Effective Product Source:
Product Definition Profile: brief | standard
Product Review: confirmed
Accepted Concept IDs:
Accepted Requirement Model IDs:
Accepted Product Rule References:
Upstream Compatibility: current | review-required
Last Compatibility Check:
Trace Applicability: required | not-applicable
Trace Not-Applicable Reason:
```

For legacy sources, the snapshot keeps `Effective Concept Source` and `Concept Foundation Status`. A triggered internal Concept Foundation must be accepted inside the confirmed Product Definition; `candidate`, `reopened`, pending Product Review, or source conflict stops Decision & Design acceptance and returns to Requirements Discussion. The snapshot cites accepted meanings and constraints but never copies a new definition into the ADR.

Before selecting the coherent ADR scope, add a Requirement Model Scope Inventory row for every applicable stable model ID in the effective source: `REL-*`, `PERM-*`, `CMD-*`, `EVT-*`, `FLOW-*`, `STATE-*`, `PM-*`, and `EX-*`. Product Rules use resolvable `product.md#<anchor>` references and do not create a new stable ID family. Use `in-scope | covered-by-accepted-decision | feature-local | proposed-decision | not-applicable`. Existing external owners must resolve to the named artifact; future owner paths must be explicit with a `planned:` prefix. `not-applicable` requires a concrete reason. The in-scope inventory IDs must exactly equal the snapshot IDs.

For every in-scope accepted Requirement Model ID, add exactly one row to the Requirement Model Technical Landing Trace with one disposition:

```text
landed | covered-by-accepted-decision | feature-local | not-applicable
```

`landed` requires a concrete Technical Landing, Preserved Invariant, Design Slice, and Verification target. `covered-by-accepted-decision` names an existing accepted decision Markdown path. `feature-local` names an existing Feature Spec or explicit canonical `planned:` owner path and cannot hide a shared rule. `not-applicable` records a concrete reason and is visible at the Human Gate. The trace never creates product meaning; missing or ambiguous meaning returns to Requirements Discussion.

Coverage Hard Gate blocks ADR acceptance and dependent Feature Spec work unless the effective source resolves, Upstream Compatibility is `current`, the Scope Inventory exactly covers the source ID set, every in-scope accepted Requirement Model ID has one disposition, every `landed` row has complete landing/slice/verification data, no product-semantic blocker remains, and the human has seen non-landed dispositions plus deferred/out-of-scope Design Slices. `Applicable Decisions` proves awareness only; it does not satisfy trace coverage.

Run structural preflight while the ADR is `proposed`. A successful preflight permits the Agent to ask for Decision & Design approval; it does not accept the ADR. After explicit human acceptance, record Human Review Evidence, change status to `accepted`, and rerun accepted-mode validation. Accepted-mode validation requires the recorded human decision, confirmer, date, and concrete evidence.

For a confirmed Brief or legacy reasoned `concept-foundation-not-needed` source with no applicable stable model IDs or Product Rule references, keep Accepted Concept IDs / Accepted Requirement Model IDs / Accepted Product Rule References as `none`, set Trace Applicability to `not-applicable`, record a concrete reason, and do not fabricate Concept Definitions, Scope Inventory, or Technical Landing Trace rows. The current unified Coverage Hard Gate wording applies to new decisions; legacy decisions may retain the earlier exact legacy gate wording without migration.

For a confirmed Standard source, either Accepted Concept IDs or Accepted Requirement Model IDs may independently be `none` only when the effective source declares no IDs of that kind. When accepted Product Rule references remain, keep Trace Applicability `required`, name those resolvable anchors, and cover them through Scope Inventory and Technical Landing Trace instead of inventing Concept or Requirement Model IDs.

When the README effective source changes or new accepted requirement evidence changes an upstream model, set the dependency judgment to:

```text
Upstream Compatibility: review-required
```

`review-required` is a dependency-availability judgment, not an ADR lifecycle status. Stop new dependent Feature Spec, Plan, and implementation work; compare old/new Concept and Requirement Model IDs. If product meaning changed but the technical decision still holds, update the snapshot/trace only after Decision & Design Human Review. If the accepted decision meaning or technical conclusion no longer holds, create a Human-gated superseding ADR and preserve the accepted record unchanged.

Operational landing is triggered, not default. Expand Migration / Backfill, Compatibility, Rollout / Cutover, or Rollback / Reversibility detail only when the decision introduces or changes persistence representation, protocol, provider, runtime boundary, or rollout compatibility. Otherwise record one concrete `not-triggered` reason without expanding the corresponding section.

## Routing Axes And Precedence

Do not force project topology, memory health, message intent, and feature progress into one mutually exclusive state. Inspect all four axes, then use the precedence ladder to select exactly one next stage.

```text
Entry Context: `new-project` / `existing-project` / `remote-entry`
Memory Health: `absent` / `current` / `stale` / `outside-loop`
Message Intent: use the Message Intent Classification values above
Work State: `idle` / `active` / `blocked` / `completion-candidate` / `paused`
```

Entry Context:

| Value | Condition | Candidate Route |
|---|---|---|
| `new-project` | no memory and little/no existing code | Init Project |
| `remote-entry` | source of truth is remote/SSH/devcontainer/container/tunnel | Remote Project Discovery |
| `existing-project` | meaningful existing code is locally available | Project Entry Scan when memory is absent; otherwise continue through memory/work-state routing |

Memory Health:

| Value | Condition | Candidate Route |
|---|---|---|
| `absent` | no `.agent-loop/` or legacy `agent-loop/` | Init Project or Project Entry Scan |
| `current` | memory exists and agrees with obvious code/artifact reality | Active Feature Guard or intent routing |
| `stale` | memory conflicts with code or indexes point to missing/stale artifacts | Reconcile Project Context / Recovery Backfill |
| `outside-loop` | recent work bypassed the loop or human asks to re-adopt/re-sync | Re-Adopt Agent Loop Project / Recovery Backfill |

Work State:

| Value | Condition | Candidate Route |
|---|---|---|
| `idle` | no active feature or blocker | intent routing |
| `active` | exactly one active feature has a clear next action | Active Feature Guard, then Continue Current Stage |
| `blocked` | a blocker prevents the next stage | choose one unblock stage |
| `completion-candidate` | active feature may already satisfy completion | Feature Completion Check |
| `paused` | no active feature and one or more resumable features are paused | Resume routing only when the human asks to resume/switch feature work or gives a generic continue signal |

Apply this precedence exactly:

```text
Safety Stop -> Remote Discovery -> Memory Recovery -> Feature Archive Maintenance -> Active Feature Guard -> Blocker Resolution -> Intent Routing -> Normal Stage Continuation
```

Rules:

1. Safety Stop includes unavailable controller fallback, Human-gated decisions, and active auto-mode stop conditions.
2. Remote Discovery runs before local existing-project handling.
3. `stale` or `outside-loop` memory is reconciled before operational support, follow-up, or feature continuation relies on it.
4. With current memory, an explicit `feature-archive-maintenance` request routes before Active Feature Guard because it maintains closed history. Declared lifecycle/readiness facts keep selected active/paused or incomplete candidates out of the move plan without switching current work; reference findings remain Agent-reviewed evidence rather than Checker authorization.
5. Otherwise run Active Feature Guard before starting, reopening, or switching feature work.
6. Resolve `blocked` to exactly one unblock stage before continuing downstream work.
7. Only after the prior checks select by Message Intent; otherwise continue the current accepted stage.

Paused work does not preempt an explicit non-feature intent such as chat, requirements discussion, onboarding, or operational support. Ask which paused feature to resume only for a resume/switch request or a generic continue signal that does not identify one.

Entry priority: remote-entry is evaluated before existing-project. If remote-entry and existing-project both appear to match, classify as remote-entry and run Remote Project Discovery before Project Entry Scan so the agent does not treat a local entrypoint or mirror as the source of truth.

Blocked must resolve to exactly one recommended next stage. Ask Human when the blocker is a missing decision, access, approval, environment, or external input; Diagnose Failure when the blocker is caused by observed system behavior, failing verification, or unclear technical cause. If the blocker is a narrow unknown about code ownership or impact, recommend Targeted Feature Scan instead.

Apply the blocked routing matrix in order and choose the first matching row:

1. observed failure or unclear technical cause -> Diagnose Failure
2. required verification not run but runnable in the available environment -> Verify
3. missing human decision/access/approval required for the next safe action -> Ask Human
4. unclear ownership/impact -> Targeted Feature Scan
5. external blocker with no immediate unblock path -> Pause

Diagnosis and available read-only verification may proceed before requesting access or approval for a later mutation. Ask Human first only when the missing human input is required for the next safe diagnostic or verification action itself.

## Checker Failure Recovery

Checker Failure Recovery is an internal method of Diagnose Failure and Verify, not a canonical stage, status, lifecycle, artifact family, or Auto Mode. Load `references/checker-recovery.md` when a canonical Agent Loop checker still fails after the exact command is rerun with unchanged inputs.

Apply this order:

```text
preserve canonical command/output/path/digest
-> artifact-invalid | environment-invalid | checker-defect-candidate | unresolved
-> artifact or environment repair when those facts decide the cause
-> minimal authority-backed positive fixture plus negative controls for a checker candidate
-> Temporary Checker Repair Review
-> exact Human authorization before checker/support writes
-> isolated temporary copy by default
-> unmodified-copy RED
-> minimal patch
-> GREEN plus negative controls
-> exact target run
-> canonical failure plus temporary result
-> separate Human substitute decision for one named Gate
-> optional sanitized Issue Draft
-> independent Issue Reporting Human Gate before GitHub creation
-> expiry and formal source repair follow-up
```

Read-only reproduction, reduction, and authority comparison may proceed before asking. The Agent must not rewrite a valid artifact to satisfy a known-wrong checker, silently modify an installed/global Skill, add a general bypass, or present temporary evidence as a canonical pass.

Preparing a sanitized upstream Issue Draft is read-only. Public GitHub Issue creation is an external mutation with its own review of exact repository, title, body, redactions, labels/method, and effect. If authenticated capability is absent, return the draft and blocker; do not install tools or disclose credentials. Issue authorization, repair authorization, one-Gate substitute evidence, Git, installation, synchronization, and release remain independent.

The Human may accept a fresh temporary result as substitute verification for one exact Gate only when the defect proof, source digests, RED/GREEN, negative controls, target command, expiry, rollback, and residual canonical failure are visible. Record:

```text
Canonical validation: failed
Temporary checker recovery: passed | failed
Human substitute decision: accepted-for-this-gate | declined
```

This decision grants no later Gate or action. Any checker/support/input/authority digest change, different target or command, Gate exit, context loss without persisted evidence, or failed negative control expires it. Short same-session evidence may remain response-local; cross-session, handoff, or later action reliance records the compact evidence in the existing owning artifact without creating a mandatory recovery directory.

Formal repair belongs in the Agent Loop source repository with the regression test and canonical checker change. Agent Loop itself cannot claim a released checker fix from an isolated patched copy; focused and required full validation must pass on the formal source.

## Inspection Order

Use this order:

1. Apply Bootstrap skill loading. After context compaction, long-running sessions, or stage-boundary uncertainty, do not continue from memory alone.
2. Discover exactly one accepted logical memory root before relying on project memory. A verified internal alias may preserve the `.agent-loop/` or legacy name. If both `.agent-loop/` and legacy `agent-loop/` exist, fail closed and route to Recovery. Broken/cyclic/external/file aliases also fail closed. If neither exists, continue entry classification without inventing reliable memory.
3. If the accepted root contains `project.md`, read it. If it contains only `changes/`, treat project memory as absent/unreliable, run the Change scanner, and do not manufacture `project.md`.
4. If `project.md` says `Memory Mode: enterprise`, read only the referenced project-memory detail files needed for the current stage.
5. If `project.md` says `Status: remote-entry`, read `<memory-root>/remote.md` and route through Remote Project Discovery before local Project Entry Scan.
6. Locate `Active Feature` and `Paused Features`.
6a. For Feature Monthly Archive or an archived follow-up candidate, read `features/archive.md` before opening the month path. Treat Feature ID as stable and verify the locator target, archive state, and flat/month uniqueness.
6b. If `.agent-loop/skills/INDEX.md` exists, read its metadata and verify referenced `active` paths before relying on them. Re-match active `bootstrap` / `on-demand` rows for each applicable actionable intent before stage-specific helper or fallback action; load and verify only the matched body. Do not load `proposed`, `disabled`, or `deprecated` skills into normal routing.
6c. For explicit Bug management, read `bugs/INDEX.md` metadata before creating a Bug or scanning Feature ownership. Resolve current Bug README, duplicate/reopen pointers, and related flat/archived Feature locators before relying on lifecycle or target claims.
6d. When `<memory-root>/changes/` exists, run the read-only Lightweight Change scanner across every month before relying on Change status, pending thresholds, or human-review inventory. A changes-only root does not prove reliable `project.md` or completed Project Entry.
7. Read current Feature `spec.md` as the bootstrap. Run `python3 <skill-root>/scripts/check-feature-context.py --project-root <target-project-root> <feature-spec-path>` before relying on downstream Feature context. Exit `0 / CURRENT` permits the local fast path. Exit `0 / CHANGED` reports factual drift for Agent impact assessment; it is not execution authorization and does not itself choose a Human Gate. Exit `1 / BLOCKED` is reserved for physical or authority-resolution contradictions and routes to Recovery or the owning source repair. On Windows use the equivalent `py -3` command.
8. Only after the result is `CURRENT`, or after the Agent has assessed `CHANGED`, repaired derived evidence, and rerun to `CURRENT`, read stage-relevant current Feature `tasks.md`, `tests.md`, `plan.md`, `notes.md`, and `contracts.md` if present. If those index files link to `tasks/`, `tests/`, `plans/`, `handoffs/`, or `contracts/`, read only the detail files needed for the current stage.
9. Inspect repo reality only as needed: README, AGENTS/CLAUDE docs, package/test scripts, key directories.
10. If local repo reality points to remote execution, or the human says this is a remote project, load `references/remote-project-discovery.md`. An empty local directory alone is not enough; if there are no remote hints, classify as `new-project`.
11. Verify long-term memory index targets before trusting them. If `project.md`, root guidance, or current artifacts point to onboarding-db, enterprise `project/*.md`, feature docs, contracts, or guidance files, check that the referenced path exists before relying on it.
12. Compare project memory with obvious repo reality.
12a. Run Branch Strategy Check when branch evidence affects the current work. Compare accepted durable policy and Target Release Context with native repository guidance, current Git reality, and feature/plan/submit evidence. Recommendation is read-only; adoption and every Git mutation remain separately Human-gated.
13. Choose the next stage.

This Feature Context Load Contract also runs after context compaction, Resume, controller re-entry, long-running uncertainty, Requirement/ADR source change, archive rehydrate before reopened execution, and before Plan or Execute reliance. Conversation summaries, `tasks.md`, and `plan.md` cannot replace `spec.md` bootstrap plus freshness evidence.

When the checker returns `CHANGED`, read its reasons plus the changed Requirement README and only applicable Product Definition/ADR sections. Record `no-semantic-impact | derived-context-update | feature-definition-impact | decision-impact | unresolved`. Refresh derived context and downstream trace without another Human Gate only for the first two results, then rerun the scanner to `CURRENT`. Feature-definition impact returns to Requirements Discussion or Gate 1; decision impact returns to Decision & Design; unresolved meaning asks one blocking Human question. `CHANGED` never authorizes target implementation, Auto Mode continuation, or another independently gated action merely because its exit code is zero.

If `project.md` declares a Decisions index, list decision files before Decision & Design or Feature Spec. Read decisions already linked by the active Requirement Product Definition, legacy Feature Product Brief, or `spec.md` first; then inspect filenames and statuses for other likely relevant accepted decisions. Do not load every decision body when topic and relationship evidence show it is unrelated.

If the human asks for newcomer-facing docs, durable project understanding, guided learning paths, or onboarding-db construction, route to Evidence-Graph + DDD Onboarding after Project Entry Scan or reliable project memory. Load `references/onboarding-knowledge-base.md`. Evidence Graph must include Core Flow Inventory selection before Onboarding Spec acceptance; critical/important flows then use Flow Slice Coverage and the Completeness Hard Gate. Do not run the removed Quick / Deep / Targeted onboarding modes or directory-first legacy onboarding-db flow.

This keeps exactly two onboarding Human Gates: accept the Onboarding Spec, then separately accept the completed Onboarding Tasks Full Execution Gate. Core-flow selection and completeness are contents of those existing gates, not additional pauses. Batch remains an Agent organization/review unit rather than a Human Gate.

If `.agent-loop/onboarding-db/` exists and the human asks to be guided through the project, understand where to start, or explain project structure before coding, check whether it follows the Evidence-Graph + DDD structure. If it does, use it through `references/onboarding-knowledge-base.md` Guided / Focused Use. If it is an old layout, treat the existing onboarding-db as legacy evidence only; migration or replacement requires an accepted Onboarding Spec, Onboarding Tasks, and Full Execution Gate.

If the human asks for guided onboarding but onboarding-db is missing, do not create onboarding-db from the removed legacy flow. Route through Project Entry Scan if project memory is missing/stale; otherwise load `references/onboarding-knowledge-base.md`, build Evidence Graph, and propose an Onboarding Spec before writing formal docs. If root guidance or `project.md` claims onboarding-db should exist but the path is missing, classify as `stale-memory` and reconcile the missing memory reference first.

If the human asks to test, run, deploy, switch account/config/model/provider, check quota/rate limits, arrange rollout, diagnose production, or use existing code to solve an operational problem, default to read-only operational support. Route to Code-Guided Operational Support before Feature Spec, Plan Gate, Execute Task / Story, or code edits. With reliable project memory, run Project Skill Discovery Guard before the first stage-specific helper, fallback, command, tool call, temporary resource, or environment action. If the request could mean either existing operational use or new implementation, ask whether the human wants help using current project functionality or feature implementation.

If the human asks to "先记一下", do something later, defer work, add a backlog item, or keep a future requirement outside the current feature, route to Requirement Archive with Future / Deferred Requirement Intake. Do not put future TODO, backlog, deferred requirements, or unimplemented planned capability details into `project.md`; use a requirement set and optional `requirements/INDEX.md` after human confirmation.

If the human asks to make a successful workflow into a skill, or asks to update/disable/deprecate a project skill, classify `project-skill-management` and route to Project Skill Creation / Update. If the agent notices a reusable skill opportunity after a complex verified workflow, finish the current stage first and propose a Project Skill Candidate at a safe boundary; do not change intent or create files until the human passes Gate 1.

When an `active` project skill matches current work, Project Skill Discovery Guard resolves it before generic fallback. Discovery and read-only loading may proceed only after its current instruction-bearing and executable files match the SHA-256 validation manifest. Before following its workflow or causing side effects, require the Execution Gate for the current invocation. A human message that explicitly names the skill and concrete scope may satisfy the gate only after the agent emits the execution summary and verifies the plan adds no undisclosed action, effect, environment, or bound. Auto mode, previous success, prior confirmation, `active`, or `bootstrap` may not. One combined confirmation may cover other applicable operational/risk gates only when the summary explicitly includes every gate fact.

If recent work bypassed the loop, set Memory Health to `outside-loop` and route to Re-Adopt / Recovery Backfill. Otherwise, if code reality and the memory root disagree or long-term memory indexes point to missing artifacts, set Memory Health to `stale` and route to Reconcile Project Context / Recovery Backfill. Treat code as the current fact base for agent-maintained docs and preserve human requirements as original intent in both routes.

If `project.md` claims a legacy onboarding layout, lists onboarding-db files, or root `AGENTS.md` / `CLAUDE.md` tells newcomers to start from `.agent-loop/onboarding-db/README.md`, but `.agent-loop/onboarding-db/` or its README is missing, classify as `stale-memory`. Do not run Guided Newcomer Onboarding from the missing path and do not create onboarding-db as a repair. Recommend the smallest memory reconcile: report the missing index target, use existing docs/code as evidence, and ask before updating `project.md` or root guidance.

Project Entry has priority over feature-follow-up. If no .agent-loop/ or legacy agent-loop/ memory exists, do not classify directly as feature-follow-up; classify as `existing-project` or `new-project` first, preserve the bug/change report as intake context, and establish or confirm project memory before running Feature Follow-up.

If explicit defect/regression/QA/post-close evidence or clear recent Feature ownership exists and reliable agent-loop memory is available, classify as `feature-follow-up` before deciding to create a new Feature. For explicit Bug management, load `references/bug-management.md` and `references/feature-follow-up.md`; scan complete Bug Index metadata for duplicate/reopen identity first, then inspect Feature metadata using the project-configured 90-day default plus evidence-driven extended scan. Create/update/reopen the Bug Record, resolve Expected Behavior, and recommend exactly one of `investigate-first | flow-back | linked-feature | maintenance-fix | requirement | no-fix`. Wait for the Resolution Path Gate and any separate Feature/Requirement action gate. Generic “small tweak”, `fix`, “修一下”, or “改一下” wording alone routes an actionable non-Bug change through Lightweight Change Assessment before Feature construction.

`maintenance-fix` is not a bypass. It uses the standard feature workspace under `.agent-loop/features/YYYY-MM-DD-fix-<slug>/` and must still pass spec, tasks, tests, plan, verification, review, drift, project memory update when needed, Feature Completion Check, and close.

Default memory root for new projects is `.agent-loop/`. Reuse legacy `agent-loop/` only when it is the single accepted logical root, and ask before migrating it. A verified internal alias is an observable layout fact, not migration authorization; keep artifact paths logical and stop if its target becomes broken, cyclic, external, or ambiguous.

For existing projects without reliable memory, load `references/project-entry-scan.md`. Run Project Entry Scan: build a shallow, evidence-backed project map before feature work. Do not do a whole-repo deep read unless a targeted feature scan requires it.

When the human wants newcomer-friendly project understanding, a guided takeover, durable onboarding documents, or a focused preserved explanation of one project area, do not route to the removed onboarding-db flow. Use Evidence-Graph + DDD Onboarding after Project Entry Scan or reliable project memory. For focused questions, answer from existing docs/code first and propose a focused onboarding-db update only when the durable knowledge base has a real gap.

For local entry directories that point to a remote project, load `references/remote-project-discovery.md` before Init Project or Project Entry Scan. Do not treat the local empty directory as the code reality.

During Project Entry, Project Entry Scan, Re-Adopt, Drift Check, and Project Memory Update, load `references/project-memory-mode.md` when long-term project memory is being created, repaired, or likely too large for one readable `project.md`.

## Project Skill Discovery Guard

Run this read-only guard after the Agent Loop controller and reliable memory root are established, after the latest intent/current stage can be classified, and before a stage-specific helper, generic Operational Support method, built-in fallback, command, tool call, temporary resource, or environment action. Ordinary chat with no workflow or execution intent remains response-only and does not require a full Project Skill body scan.

Canonical matched sequence:

```text
latest actionable intent / current stage
-> inspect Project Skill INDEX metadata
-> match active bootstrap / on-demand candidates
-> verify exact INDEX row, path, and manifest
-> read-only load the matched Project Skill
-> Execution Gate
-> stage action

index-absent | no-active-match
-> runtime/global helper if applicable
-> generic Operational Support or Agent Loop fallback

project-skill-drift
-> fail closed
-> Recovery or Project Skill Creation / Update
```

Guard results are response-local routing judgments, not persistent lifecycle values or artifact fields:

- `matched-active`: the current intent/stage matches an `active` row; verify the exact row, target path, current instruction-bearing/executable files, and validation manifest, then load only that Skill body as needed.
- `index-absent`: the reliable memory root has no `.agent-loop/skills/INDEX.md`; generic method selection may continue without creating an empty skills directory.
- `no-active-match`: INDEX exists but no valid active row matches current intent, stage, task context, Triggers, and Scope; do not load all bodies or route `proposed | disabled | deprecated` rows.
- `project-skill-drift`: a target is missing, active evidence/manifest is invalid, a current row/file mismatches its manifest, a path/symlink escapes the project boundary, or owners conflict; stop before reliance or equivalent generic effects.

Only `index-absent` or `no-active-match` permits generic fallback. `project-skill-drift` fails closed and never authorizes an equivalent generic action. runtime/global Skill inventory does not prove that no Project Skill exists.

The agent may make a negative Project Skill claim only after reporting `index-absent` or `no-active-match` evidence from the current project INDEX. Runtime/global inventory and native Skill chips are separate discovery sources. Same-name runtime/global and project-local candidates require explicit owner/path disclosure; unresolved ownership is drift.

Within one uncompacted, reliable context and continuous stage, unchanged INDEX metadata may be reused rather than reread before every command. Re-read after context compaction, long-running-session uncertainty, controller re-entry, stage-boundary uncertainty, INDEX change, or manifest change. No persistent discovery cache is created.

The guard never grants execution. A `matched-active` result must still emit the existing bounded Execution Gate summary before the first skill-directed workflow step or side effect.

## Response Frame

Every loop response before action should include:

```text
Current state:
Recommended next stage:
Why:
Artifacts to read/write:
Human gate:
```

Before asking the human to approve stage output, load `human-review-summary.md` and present a table-first approval view when the decision has meaningful scope, risk, artifact, evidence, or next-action content.

When action is complete:

```text
Stage completed:
Artifacts changed:
Evidence:
Drift found:
Recommended next stage:
Human gate:
```

Do not end an action report with only "done". Always include the next recommended stage or a concrete stop reason.

## Memory After Code Integration

```text
Code Merge Gate -> Post-Merge Memory Reconciliation -> Memory Commit Gate -> Push Gate -> Release Gate -> Source Branch Cleanup Gate
```

Post-Merge Memory Reconciliation is an internal Submit / Integrate method, not a canonical stage or message intent. Route to `references/memory-reconciliation.md` only after code integration has one stable full Merged Code SHA, fresh code-verification evidence, an accepted memory root, and an observed memory conflict. Require only the branch/release/customer facts needed to understand that conflict.

First determine whether a concrete memory conflict was observed. When none exists, use `reconciliation-not-needed`: do not scan all memory, create a report, or add a Human Gate. Different files, clean Source-only artifacts, unchanged memory, and speculative drift are not conflicts.

When a conflict exists, inspect only its semantic owner, directly affected references/indexes, and minimum direct evidence. Resolve fact-determined current meaning, capture exact preimages and intended postimages, use bounded same-directory atomic replacement, run targeted verification, and retain rollback only for changed files until verification passes. Ask the human only when facts leave multiple legitimate meanings; unresolved observed conflicts and failed restore block later mutations.

Full Base/Source/Target-before/Result inventory, Start review, exact Plan Hash, transactional Apply/Post-check/Restore, and all-path checks are Full Memory Audit / Recovery only and require explicit Human authorization. A resolved conflict or `reconciliation-not-needed` permits only presentation of the next independent Human Gate; neither authorizes commit, push, tag, release, publish, merge, branch deletion, or cleanup.

## Stage Order

Default order applies after Message Intent Classification. For `requirements-discussion`, use Requirements Discussion before Project Entry-driven feature stages.

Default order:

```text
Message Intent Classification
Chat Entry / Requirements Discussion [internal Brief/Standard Product Definition] if Needed
Project Entry
Remote Project Discovery if Needed
Re-Adopt Agent Loop Project if Needed
Feature Monthly Archive If Explicitly Requested
Code-Guided Operational Support if Needed
[internal] Lightweight Change Assessment for eligible ordinary non-Bug changes
Project Skill Creation / Update if Needed
Requirement Archive [Requirement Record / Archive]
Design Readiness / Decision & Design If Needed
Brainstorm / Clarify if Needed for Feature-local implementation uncertainty
Feature Follow-up And Flow-back if Needed
Targeted Feature Scan if Needed
Feature Spec with Product Slice
Requirement Checklist
Work Breakdown
Delivery Contract If Needed
Test Design
E2E Discovery if Web
Technical Design / Code Context
Plan Gate / Plan if Needed
Analyze Consistency
Subagent Execution If Approved
Execute Task / Story
Verify
Review
Drift Check
Project Memory Update
Feature Completion Check
Submit / Integrate
Pause / Close
```

Feature Spec enters Brainstorm / Clarify only when concrete feature-local scope, acceptance, or implementation-boundary uncertainty remains after loading the accepted Product Slice and applicable ADRs. If the Product Slice, assigned ADR Design Slices, scope, exclusions, and measurable acceptance are already clear, classify the method response-locally as `brainstorm-not-needed` and proceed directly to Feature Spec. This label is not a lifecycle status or artifact field. Helper availability alone never triggers the method. Brainstorming may compare or clarify Feature-local alternatives, but it cannot reopen Requirement product meaning, rewrite an accepted ADR, or add scope; product ambiguity returns to Requirements Discussion and ADR incompatibility returns to Decision & Design Human Review.

## Stage Entry And Exit

Each stage must define:

- entry condition
- files read
- files written
- human gate
- exit condition
- next recommended stage

Use `references/stage-guides.md` for the exact procedure.

## Human Gate Modes

Normal Feature construction uses two meaningful reviews:

```text
explicit implementation request
-> checked Feature Spec and Product Slice
-> Gate 1: Feature Definition Review
-> Implementation Package Preparation
-> Gate 2: Implementation Readiness Review
-> Agent-ready implementation
```

For non-trivial gates, the approval prompt must include a Human Review Summary. The summary is the human-facing approval view; the full artifact files remain the source of truth.

Gate 1 acceptance authorizes package preparation only and does not authorize target implementation. During package preparation, the Agent completes Work Breakdown, Delivery Contract assessment, Test Design, E2E Discovery if applicable, Technical Design / Code Context, Plan Gate / Plan, coverage review, and Analyze Consistency without separate Work Breakdown, Test Design, E2E Discovery, Technical Design, or Plan approval prompts. Target implementation is forbidden until Gate 2.

Record this compact derived state in current Feature notes:

```text
Implementation Readiness: preparing | review-ready | accepted
```

- `preparing`: Gate 1 accepted and the package is being built.
- `review-ready`: package completeness and consistency checks pass; Gate 2 is pending.
- `accepted`: Gate 2 accepts the package.

The state is not Feature lifecycle or authorization for Git, external mutation, submit, release, or close.

Feature `notes.md` must persist the Gate decisions and review baseline: `Gate 1 Decision`; `Gate 2 Decision` / `Gate 2 Reviewed At`; `Gate 2 Package Files`; `Gate 2 Agent-ready Tasks`; `Gate 2 Accepted Stories`; `Active Plan Scope`; `Gate 2 Plan Evidence`; `No-Plan Decision`; the Gate 2 `Feature Auto-Loop` decision value enabled/disabled; `Later Start Decision` / `Later Start Authorized At` / `Later Start Evidence`; and, when later evidence is assessed, a row under `## Gate Drift Assessments`. The Agent owns every field's completeness, meaning, timing, and consistency. Current top-level fields are authoritative; fenced examples and later history sections never supply current Gate evidence. The Gate 2 decision/Auto-Loop/time fields are the original durable review baseline, not the live execution-mode pointer. A package-only later start records the separate Later Start transition while preserving the original Gate 2 review baseline. Pause clears the current project `Gate Mode` and records the transition without rewriting either accepted baseline or later-start evidence; Resume requires a newly confirmed applicable mode.

Existing Feature notes without Later Start fields remain reader-compatible. Their absence means no recorded later-start transition and never authorizes execution; it does not invalidate a truthful historical Gate 2 approve-and-start record. Add the three fields only when the Agent next performs an authorized Gate evidence refresh or records a valid package-only later start. Never infer or backfill Human approval from history, urgency, or current mode.

The Agent verifies the complete implementation package directly from current Feature artifacts. `Gate 2 Package Files` must inventory `spec.md`, `tasks.md`, `tests.md`, `plan.md` when present, optional `context.md` / `contracts.md`, and every current file under triggered `tasks/`, `tests/`, `plans/`, and `contracts/` directories. The Agent also verifies Story/Task/Plan bindings, required roots, risk, rollback, verification, placeholders, and consistency before presenting Gate 2. This review is semantic and evidence-backed; no digest or local Feature Gate Checker is part of the authorization path.

Human authorization provenance is an Agent responsibility. At Gate 2, the Agent records `accepted`, the exact Gate 2 decision, matching Gate 2 Auto-Loop state, and a timezone-aware review time only after the corresponding Human choice is present in the current reliable conversation or preserved Human decision evidence. A later-start transition separately records its decision, authorization time, and Human instruction evidence. After context loss or when decision provenance is genuinely uncertain, the Agent asks one blocking Human confirmation instead of manufacturing evidence.

AI must read current Task rows and current Plan evidence rather than letting history sections override `Mode`, Story coverage, `Derived From`, or `No-Plan Decision`. AI checks package completeness, Gate/action pairing, readiness, timestamp, Goal/Scope/Acceptance, accepted Story/Product Slice boundaries, Task/Plan/No-Plan bindings, risk, rollback, verification, and boundary drift. These remain Agent-owned workflow judgments and are not delegated to a local script.

For a No-Plan route, AI must still bind `Gate 2 Plan Evidence: no-plan:<task ID>` and top-level `No-Plan Decision: <task ID>` to the same current Task, and require that Task row/detail to record `No-Plan Decision: accepted`.

When reviewed Feature artifacts change after Gate 2, compare the concrete delta with the accepted Goal/Scope/Acceptance and execution boundary. Record `within-approved-boundary | feature-definition-change | implementation-boundary-change | unresolved`, changed areas, reason, evidence, and timezone-aware assessment time in the Agent-owned assessment log. A current `within-approved-boundary` assessment may continue without repeating Gate 2; a product-definition change returns to Gate 1, an implementation-boundary change returns to Gate 2, and unresolved meaning asks one blocking Human question. Do not invent Human decisions or semantic mappings.

Gate 2 choices are:

```text
Approve package and start implementation
Approve package only; do not implement yet
Revise package
Pause
```

Only the two approval choices set `Implementation Readiness: accepted`. `Approve package only` records accepted readiness and does not execute. `Approve package and start implementation` accepts the package and enables Feature Auto-Loop for the disclosed Agent-ready work without a third generic Feature Auto-Loop prompt. `Revise package` returns readiness to `preparing`; `Pause` does not mark readiness accepted and records the separate Pause state while preserving the last truthful readiness value.

If the human later explicitly says to start implementation after package-only acceptance, first require Feature Context `CURRENT`, re-read the recorded package files and current Feature artifacts, compare their meaning with the accepted execution boundary, and confirm no new stop condition or Human-gated item exists. When the package is unchanged or AI records the current delta as `within-approved-boundary`, that explicit instruction enables Feature Auto-Loop without repeating the full Gate 2 review. A `feature-definition-change` returns to Gate 1; an `implementation-boundary-change` returns to Gate 2; `unresolved` asks one blocking Human question. No local script result is required to continue.

After the human explicitly says start and those Agent-owned checks pass, atomically record `Later Start Decision: approved`, `Later Start Authorized At: <ISO-8601>`, and `Later Start Evidence: <Human instruction evidence>`, then set the current project `Gate Mode` to Feature Auto-Loop before target implementation. Preserve `Gate 2 Decision: package-only`, the Gate 2 `Feature Auto-Loop: disabled` review value, and `Gate 2 Reviewed At` as the original Gate 2 review baseline. No local command issues or repairs Human authorization.

Available control modes:

| Mode | Authorization scope | When it can start | What it may do without another stage gate |
|---|---|---|---|
| Normal two-gate construction | one current Feature definition/package | explicit implementation request, then Gate 1 | write the complete implementation-package artifacts without modifying target implementation |
| Strict Mode | one stage at a time | human explicitly requests stage-by-stage control, or controller fallback forces it | nothing beyond the confirmed stage |
| Feature Auto-Loop | current accepted Feature package | Gate 2 selects `Approve package and start implementation`, or a valid separate later-start transition follows package-only acceptance | execute and advance Agent-ready tasks for the feature |
| Task Auto-Run | one task or one story | after the task/story plan is accepted and human explicitly enables it | run Analyze Consistency, then complete that task/story through TDD, verification, review, drift, Task Done Gate, and task status update |

Feature Auto-Loop means:

```text
Feature Auto-Loop = give one feature a bounded release lane.
```

In this mode, the agent may continue through Analyze Consistency, Execute Agent-ready Tasks, Verify, Review, Drift Check, and Project Memory Update for the current accepted package. It must not skip Plan Gate before execution. It must stop before Bug Resolution Path decisions, Bug close/reopen, Feature creation/reopen, Requirement creation/lifecycle reconciliation, Feature Monthly Archive or rehydrate and their Batch Human Gates, branch creation, switching, deletion, push, or tag, creating or materially updating a project-local skill, executing a project-local skill without a current invocation grant, Delivery Contract creation and acceptance not separately named in Gate 2, breaking contract changes, subagent dispatch, external mutation, Submit / Integrate, commit, push, PR, merge, tag, release, publish, and Pause / Close.

For multiple Agent-ready tasks, Feature Auto-Loop may rotate `plan.md` and Active Plan Scope without repeating Gate 2 when the Agent confirms the current task/story Plan passes Plan Gate and Analyze Consistency and interfaces/risk/rollback/verification obligations remain inside the accepted execution boundary. `Gate 2 Agent-ready Tasks` is the initial reviewed decomposition, not an immutable whitelist, while `Gate 2 Accepted Stories` is the durable semantic snapshot derived at Gate 2 and is not rebuilt from current Task rows. A new Task ID does not by itself repeat Gate 2. A new Agent-ready Task may execute only when the Agent verifies that it exists in `tasks.md`, maps to the accepted Story/Product Slice/Acceptance, any `Derived From` value is valid trace rather than substitute authorization, and the current delta is `within-approved-boundary`. A new Story/Product Slice/Acceptance, Human-gated Task, missing Task identity, story mismatch, changed interface/risk/rollback/verification boundary, or classified implementation-boundary change returns to Gate 2.

Task Auto-Run means:

```text
Task Auto-Run = give one task/story a bounded execution lane.
```

In this mode, the agent first runs and records Analyze Consistency for the accepted plan, then may complete the selected task/story only. It must stop after updating evidence, review notes, drift notes, and task/story status. It must not start the next task without a new human instruction or a Feature Auto-Loop grant.

## Task Done Gate

Do not mark a task `done` merely because code was written or an implementation step finished.

Status flow:

```text
todo -> in-progress -> review -> done
todo | in-progress | review -> blocked when progress cannot continue
blocked -> prior non-terminal status after the blocker is resolved
todo | in-progress -> skipped only after human-approved scope removal
```

Record the prior non-terminal status and unblock evidence whenever entering or leaving `blocked`. `skipped` is terminal only for work already removed from current scope; it is never an in-scope completion substitute.

The task may enter `review` after implementation and all applicable fresh verification for the accepted scope has run, or after a human-approved substitute verification is recorded. If required verification is missing, keep the task `in-progress` or `blocked`. The task may enter `done` only when all required items are true:

- accepted implementation scope is complete
- required tests or substitute verification ran fresh
- verification evidence is recorded in `notes.md`
- lightweight Spec Review is recorded for the task
- Standards Review is recorded when triggered by large project, broad diff, directory or durable boundary change, security/data change, architecture change, or human request
- drift decision is recorded, even if the decision is "no drift"
- `tasks.md` or task detail names the evidence location

If any item is missing, keep the task as `review`, `in-progress`, or `blocked`; never use `done`.

Before Gate 2 may start Feature Auto-Loop, or before enabling Task Auto-Run, perform a final clarification pass:

- list remaining assumptions
- list Human-gated tasks or decisions
- list likely risk points
- list stop conditions
- include these facts in the Gate 2 choice or Task Auto-Run request and obtain the corresponding explicit confirmation; do not add a third generic Feature Auto-Loop prompt after approve-and-start

## When To Offer Execution Modes

Use the normal two-gate path without asking the human to choose a mode after every stage:

- after Requirement Checklist passes, present Gate 1 and recommend complete package preparation
- after package consistency passes, present Gate 2 with package-only and package-plus-start choices
- after a task/story plan is accepted, offer `Task Auto-Run` for that execution unit
- use Strict Mode only when the human explicitly asks for stage-by-stage review or the controller-unavailable fallback requires it

Recommended wording:

```text
First review what will be built. After you accept the checked Feature definition, I will prepare tasks, tests, code context, Plan, verification, risk, and rollback without changing target code. The second review accepts the complete package and can either stop there or start Agent-ready implementation. Delivery Contract, subagent, Git, external, submit, close, and release actions keep their own gates.
```

Do not offer an auto mode as a substitute for missing clarification. If scope, acceptance, test approach, data rules, or affected boundaries are unclear, clarify first.

Auto modes do not remove stop conditions. Stop and ask when:

- Feature Context scanner reports `CHANGED` without a completed Agent assessment/current refresh, or reports `BLOCKED`; Auto Mode cannot rely on the context until changed facts are assessed and refreshed to `CURRENT`, while physical authority failure routes to Recovery/source repair
- a task is `Human-gated`
- product, design, architecture, security, data, approval, or public-interface decisions are needed
- a stage would modify human original requirements
- a Delivery Contract needs creation, human acceptance, or an accepted contract needs a breaking change
- a Project Skill Candidate needs Gate 1 before creation or material update
- a project-local skill is ready to execute without a current invocation Execution Gate grant
- spec, product scope, or acceptance criteria would change
- code reality conflicts with project memory or feature docs outside a reversible fact-determined Post-Merge Memory Reconciliation rewrite; unresolved meaning still stops
- unrelated dirty work blocks progress
- a new dependency, migration, destructive operation, credential, external service, or long-lived boundary directory is needed
- directory-level `AGENTS.md` creation/update is recommended
- Complex Artifact Mode detail directories (`tasks/`, `tests/`, `plans/`) would be created or the feature would switch from simple to complex artifact mode
- the work would require first-version exclusions
- Feature Monthly Archive or rehydrate is requested; scan may remain read-only and advisory reference findings do not create a Checker Gate, but exact plan SHA-256 confirmation is required before apply
- a Bug needs Resolution Path confirmation, close/reopen, Feature creation/reopen, Requirement creation/reconciliation, or another action-specific Human Gate
- Bug Index/README, duplicate/reopen, Status/Resolution, Resolution Target, Expected Behavior authority, or Fix Feature locator evidence is invalid or contradictory
- an archive row target is missing, an archived directory lacks a row, a flat/month Feature ID collides, a `rehydrated` row points to a month path, an incomplete `.archive-txn` exists, or verified apply leaves an old durable path; these physical/locator contradictions stop their owning operation, while ordinary scan findings are reviewed by the Agent
- TDD cannot be followed or verification repeatedly fails
- a canonical Agent Loop checker failure needs a temporary patch but the exact Temporary Checker Repair Review or one-Gate substitute decision is missing, expired, or being widened
- review finds behavior/scope/architecture changes
- subagents are needed but not yet approved
- branch creation, switching, deletion, push, or tag is requested
- submit, commit, PR, merge, release, publish, pause, or close is requested

Allowed replies:

```text
accept definition and prepare implementation package
approve package and start implementation
approve package only
revise definition
revise package
pause
submit
close
change scope
skip with reason
enable Task Auto-Run
switch to Strict Mode
```

If the human interrupts with new information, update the relevant upstream artifact first, then resume.

## Active Feature Guard

Humans do not need to explicitly say `close`.

Run `references/feature-completion-check.md` when:

- Verify, Review, Drift Check, and Project Memory Update indicate the feature may be done
- the human asks to start a new feature while `project.md` has an Active Feature
- resuming a project with an Active Feature that may already be complete
- after Submit / Integrate when the feature appears done

The agent may recommend close, pause, continue, or scope update. It must not close automatically. Close still requires explicit human confirmation.

## Machine-Readable State Without JSON

First version does not require `state.json`. State lives in markdown:

- `<memory-root>/project.md` -> Current Work and Next Suggested Action
- feature `tasks.md` -> task status and stage/barrier state
- feature `tests.md` -> test design and verification strategy
- feature `plan.md` -> active execution unit
- feature `notes.md` -> checkpoints, evidence, decisions, drift
- feature `contracts.md` -> producer-consumer delivery contracts when present
- `bugs/INDEX.md` -> Bug inventory, backlog, and locator
- Bug `README.md` -> stable Bug identity, facts, evidence, Status/Resolution, Resolution Path, verification, close, and reopen history
- `.agent-loop/skills/INDEX.md` -> project-local skill lifecycle, load policy, triggers, and validation evidence
- `.agent-loop/skills/<skill-name>/validation.md` -> RED/GREEN/REFACTOR and activation evidence
- `<memory-root>/changes/YYYY-MM/YYYY-MM-DD-<topic>.md` -> one persistent Lightweight Change's execution facts and Memory Review; never a shared backlog or project-memory replacement

When resuming, reconstruct state from those files using the inspection order above.

## Completion Gate

Feature close is forbidden unless all are true:

- accepted feature spec exists
- tasks are done or explicitly removed from scope
- tests or substitute verification are recorded
- Delivery Contracts are implemented and verified when downstream consumers rely on them
- accepted Delivery Contracts match producer code/tests and have no unapproved breaking changes
- fresh verification evidence exists in `notes.md`
- Feature Close Review completed and recorded in `notes.md`
- drift check completed
- long-term changes reflected in `project.md`
- submit/integration status recorded when the human requested submission
- human explicitly confirms close

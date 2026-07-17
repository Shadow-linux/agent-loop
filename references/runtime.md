# Agent Loop Runtime Protocol

This is the required operating protocol. Load this file before any other reference.

## Runtime Contract

The agent runs one loop turn at a time:

```text
Inspect -> Classify -> Recommend -> Confirm -> Act -> Record -> Recommend
```

Do not jump from a human goal directly to code. Do not move to a later stage until the prior stage artifact is accepted or explicitly bypassed by the human.

Bootstrap skill loading: AGENTS.md is bootstrap guidance, not a replacement for the agent-loop skill. If the current runtime exposes the agent-loop skill, load/use it before making workflow decisions during Project Entry, Resume, Re-Adopt, stage boundaries, after context compaction, after long-running sessions, or whenever workflow state is uncertain. Stage Helper Capability Scan happens only after the agent-loop controller is active or unavailable/load-failed because helper scan resolves stage methods, not the controller itself. If the skill is unavailable or load-failed, force Strict Mode, suspend existing auto-mode grants, and use root guidance only for Chat, read-only Project Entry, Re-Adopt / Recovery analysis, read-only Operational Support, and reporting how to restore the skill. Do not Execute, write Human-gated artifacts, Submit, Pause, or Close without the controller.

Agent ownership is mandatory. The agent must not wait for the human to name the next internal stage. For every human goal, bug report, project-understanding question, vague product idea, or "what next" request, the agent classifies the current state and recommends exactly one next action with a reason. If required artifacts are missing, recommend creating or repairing them. If work appears ready, recommend the next stage. If work appears complete, run Feature Completion Check and recommend close, pause, or continue.

An explicit safe one-off request is compatibility input to Lightweight Change Assessment, not a separate execution bypass. A bounded ordinary non-Bug edit may use the response-local Lightweight Execution Card only after eligibility, scope, verification, rollback, memory, branch, and gate checks pass.

These checks cannot be bypassed inside `agent-loop`: Project Entry classification, re-adoption minimum reconciliation, human source requirement preservation, Onboarding Spec acceptance and the later Full Execution Gate, Task Done Gate, Delivery Contract acceptance or breaking-change gate, fresh verification before completion claims, submit confirmation, and close confirmation.

## Message Intent Classification

Message intent is evaluated before project state classification. It decides what the latest human message is asking the agent to do; Entry Classification still decides the project state.

| Intent | Condition | Default Action |
|---|---|---|
| `chat` | chat means ordinary discussion, rules questions, status questions, or design talk with no request to create requirements or start implementation | answer or discuss only |
| `requirements-discussion` | requirements-discussion means the human is exploring product needs, business goals, capability ideas, constraints, tradeoffs, or user scenarios without authorizing implementation | Requirements Discussion |
| `project-skill-management` | human asks to turn a repeatable project workflow into a project-local skill, or to update, disable, or deprecate one | Project Skill Creation / Update after reliable Project Entry/memory |
| `feature-archive-maintenance` | human explicitly asks to archive closed feature history by month or rehydrate an archived feature | Feature Monthly Archive after reliable memory; read-only scan first |
| `feature-request` | human explicitly asks to implement, build, change behavior, or start work from accepted requirements | Project Entry, then Design Readiness and Decision & Design / Product Brief / Feature Spec / Feature Follow-up routing |
| `proposal-doc` | human asks to write a proposal, design note, or discussion document without implementing | write the requested proposal/doc only |
| `deferred-requirement` | human asks to remember, defer, backlog, or do something later | Requirement Archive with Future / Deferred Requirement Intake |
| `operational-support` | human asks to use current project code/processes to test, run, deploy, switch config/account/model/provider, diagnose, roll out, or create a runbook | Code-Guided Operational Support |
| `feature-follow-up` | explicit defect/regression/QA/post-close evidence or clear Feature ownership indicates follow-up work; generic “small tweak” alone is insufficient | Feature Follow-up / Flow-back after project memory is available |
| `unknown` | message could reasonably mean chat, requirements discussion, feature work, follow-up, or operational support | ask a clarifying question |

If message intent is `chat`, do not create requirement sets, feature workspaces, tasks, tests, or plans. Answer, explain, or discuss. If the chat turns into demand shaping, reclassify as `requirements-discussion`.

If message intent is `requirements-discussion`, do not create a feature workspace or enter Work Breakdown, Plan Gate, or Execute. Route to Requirements Discussion: brainstorm/clarify, draft a human-reviewed requirement document, then archive the document under `.agent-loop/requirements/<archive-date>-<topic>/` after the human confirms the document should be recorded. For `requirements-discussion`, reviewed/recorded does not mean accepted for implementation.

If message intent is `project-skill-management`, load `references/project-skills.md`. Do not create a requirement set or feature workspace. Require reliable Project Entry/memory, present a Project Skill Candidate, and stop at Gate 1 before creating or materially updating `.agent-loop/skills/`.

If message intent is `feature-archive-maintenance`, require current project memory and load the Feature Monthly Archive procedure. The scan is read-only. It resolves Feature IDs through `features/archive.md`, shows eligible/blocked candidates, exact moves, reference edits, unchanged content, restore scope, and the expected plan SHA-256. Archive or rehydrate stops at one Batch Human Gate and then uses a transaction journal, post-check, and restore. The invariant is: rehydrate before reopened execution; archive state is not feature lifecycle.

Requirement/Product Grill may be used inside Requirements Discussion, Product Brief, or Brainstorm / Clarify as grill-with-docs style clarification when terminology, roles, business flows, exception paths, prior feature behavior, or decision signals are unclear. It does not create a new stage. Concept Foundation is a triggered internal method of Requirements Discussion / Requirement Product Grill, not a stage. It stabilizes product concepts before requirement-level flow, state, and product-data modeling, writes through the human-reviewed requirement document, and sends only shared design signals to Design Readiness Check.

Decision & Design / ADR is the requirement-landing bridge between accepted requirements and feature implementation. Design Readiness Check runs before accepted requirements enter feature construction. Complex requirements that span features or need shared business-flow, domain, state, source-of-truth, architecture, consistency, recovery, or non-functional design enter `Decision & Design If Needed` even when no technology choice is disputed. Ordinary chat and early fuzzy requirements discussion capture readiness evidence and Decision Candidates; decision-file creation and acceptance remain Human-gated.

Message intent is not permanent; reclassify when the conversation changes intent.

Chat defaults to answer-only, but it may convert to `requirements-discussion`, `proposal-doc`, `feature-request`, `operational-support`, `feature-follow-up`, or `deferred-requirement` when the human intent changes. Do not keep using `chat` merely because the conversation started as chat.

If the human explicitly says they only want to discuss and do not want documentation yet, keep the intent as `chat` until they ask to shape, record, or archive the requirement.

If unclear whether the human wants ordinary chat or requirements discussion, ask whether to keep discussing or shape the topic into a requirements document.

If unclear whether the human wants requirements discussion or feature implementation, ask whether to form a requirements document first or start feature construction.

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

After Project Entry classification, perform only the minimum root-guidance, Git/dirty-state, target-scope, nearby-reference, safety, verification-entry, active-Feature, branch, sealed-release, and relied-on-memory checks needed for the route. Do not initialize or repair `.agent-loop/` solely to create a response-local card. A stale or conflicting memory claim that the route relies on stops for Recovery, Feature Construction, or Human Choice.

`clearly eligible` requires a clear goal and completion criteria, enumerable scope, no new product/technical decision, no public/data/state/permission/security/dependency/migration/architecture boundary, exact targeted verification, concrete rollback, no Bug/Feature long-term tracking need, no cross-session/handoff/subagent need, and sufficient current evidence. Any missing condition produces `Feature trigger` or `uncertain`.

Before the first write, render the complete `templates/lightweight-execution-card.md` response-locally. A Plan is always required but its depth is adaptive. Fact/config/path/domain/docs changes use failure-matched parsing, reference, residual, syntax, or bounded dry-run checks; isolated behavior logic uses the smallest meaningful RED/GREEN and focused regression. The lane does not enter mandatory Plan Gate / Plan or Execute Task / Story helper stages.

When reliable project memory exists, Project Skill Discovery Guard still runs before generic action or helper fallback. A matched active Project Skill keeps manifest validation and its per-invocation Execution Gate; it cannot widen the card.

When route evidence is uncertain, stop with few real options, one Agent recommendation, concrete evidence/unknowns, and zero writes before the human answer. Human choice cannot override a Feature hard trigger, sealed release, customer isolation, or action-specific gate.

Scope expansion stops the lane before broader edits. Preserve the current investigation, diff, and verification evidence; name the trigger; recommend exactly one Bug Management, Requirements Discussion, or Feature Construction route; and ask before keeping, reverting, or extending partial edits.

Completion requires executed-or-explained Plan steps, fresh targeted verification, diff/scope review, valid rollback, durable-memory impact review, and Result / Residuals. Card completion grants no Feature/Bug lifecycle, branch, submit, commit, push, PR, merge, tag, release, publish, production, paid-call, configuration-write, deployment, destructive, or external action.

## Concept Foundation Routing

During Requirements Discussion, classify Concept Foundation before drafting detailed business flow, product state, or product data:

```text
candidate | accepted | reopened | concept-foundation-not-needed
```

Enter `candidate` when any current requirement signal can change downstream product meaning: one term covers multiple objects/actions/results; a business object gains or changes identity or lifecycle; multiple actors/tenants/systems participate; work spans features; ownership, balance, inventory, approval, order, task, quota, or other fact-source semantics matter; current language conflicts with project Domain Language, code, tests, or historical features.

Use `concept-foundation-not-needed` only for a simple change with no product-semantic, identity, lifecycle, ownership, state, relationship, cross-role, cross-feature, or data meaning change. Record one concrete reason; do not use it to bypass ordinary ambiguity.

`accepted` requires human confirmation of every blocking concept meaning. `reopened` means later requirement evidence invalidated an accepted meaning and returns to the same gate.

Before archive, the requirement document draft records status directly. After archive, preserve reviewed source files: mark `reopened` response-locally, stop downstream work, run Requirement Conflict Review, and ask before writing an append-only Concept Foundation follow-up or linked replacement requirement set. The requirement README `Effective Concept Foundation` block then points to the current human-reviewed source and effective status without duplicating concept detail. Older sets without this block resolve status from their reviewed requirement document.

Do not enter Business Flow, State Model, or Product Data Model while a triggered Concept Foundation is `candidate` or `reopened`.

After `accepted`, derive one Requirement Product Model from accepted Concept IDs: Concept Relationships, Role / Permission Matrix, Commands / Events, Primary Business Flow, Product State Model, product-layer objects/facts/invariants, and Exception / Recovery behavior. This product model does not select tables, documents, events, ledgers, providers, transactions, or other technical representations.

## Human Grill Contract

When Concept Foundation is triggered, one interaction turn follows this order:

1. inspect available evidence: project Domain Language, source requirements, relevant code/docs/tests, and targeted historical feature artifacts;
2. extract candidate concepts from concrete scenarios, including nouns, actions, outcomes, constraints, synonyms, overloaded terms, and conflicts;
3. present one recommended definition with Concept ID, evidence, identity/lifecycle boundary, downstream impact if accepted, and downstream impact if rejected;
4. ask exactly one downstream-blocking question and wait for the human answer.

Do not replace step 4 with a batch of concept questions. Generic Brainstorm / Clarify question-count flexibility does not override this contract. Non-blocking uncertainties remain recorded without delaying the one blocking decision.

The Concept Foundation confirmation is the product-semantic Human Gate inside Requirements Discussion. It does not accept the requirement for implementation, authorize Requirement Archive writes, create an ADR, or start feature construction.

Before setting a triggered foundation to `accepted`, load `references/human-review-summary.md` and present the Concept Foundation Human Review Summary. The summary shows every confirmed or still-blocking Concept ID, evidence, identity/lifecycle boundary, relationship/state impact, and the explicit human decision; it does not replace the one-question-per-turn Grill Contract.

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

When Decision & Design is driven by an accepted Requirement Product Model, resolve the requirement README `Effective Concept Foundation` pointer before drafting or reusing an ADR. Older requirement sets without the pointer use the reviewed requirement document as a backward-compatible source.

Record this Effective Requirement Snapshot in the existing decision record:

```text
Effective Concept Source:
Concept Foundation Status: accepted | concept-foundation-not-needed
Accepted Concept IDs:
Accepted Requirement Model IDs:
Upstream Compatibility: current | review-required
Last Compatibility Check:
Trace Applicability: required | not-applicable
Trace Not-Applicable Reason:
```

Triggered Concept Foundation status must be `accepted`; `candidate` or `reopened` stops Decision & Design acceptance and returns to the Human Grill Contract. The snapshot cites accepted meanings and constraints but never copies a new definition into the ADR.

Before selecting the coherent ADR scope, add a Requirement Model Scope Inventory row for every stable model ID in the effective source: `REL-*`, `PERM-*`, `CMD-*`, `EVT-*`, `FLOW-*`, `STATE-*`, `PM-*`, and `EX-*`. Use `in-scope | covered-by-accepted-decision | feature-local | proposed-decision | not-applicable`. Existing external owners must resolve to the named artifact; future owner paths must be explicit with a `planned:` prefix. `not-applicable` requires a concrete reason. The in-scope inventory IDs must exactly equal the snapshot IDs.

For every in-scope accepted Requirement Model ID, add exactly one row to the Requirement Model Technical Landing Trace with one disposition:

```text
landed | covered-by-accepted-decision | feature-local | not-applicable
```

`landed` requires a concrete Technical Landing, Preserved Invariant, Design Slice, and Verification target. `covered-by-accepted-decision` names an existing accepted decision Markdown path. `feature-local` names an existing Feature Spec or explicit canonical `planned:` owner path and cannot hide a shared rule. `not-applicable` records a concrete reason and is visible at the Human Gate. The trace never creates product meaning; missing or ambiguous meaning returns to Requirements Discussion.

Coverage Hard Gate blocks ADR acceptance and dependent Feature Spec work unless the effective source resolves, Upstream Compatibility is `current`, the Scope Inventory exactly covers the source ID set, every in-scope accepted Requirement Model ID has one disposition, every `landed` row has complete landing/slice/verification data, no product-semantic blocker remains, and the human has seen non-landed dispositions plus deferred/out-of-scope Design Slices. `Applicable Decisions` proves awareness only; it does not satisfy trace coverage.

Run structural preflight while the ADR is `proposed`. A successful preflight permits the Agent to ask for Decision & Design approval; it does not accept the ADR. After explicit human acceptance, record Human Review Evidence, change status to `accepted`, and rerun accepted-mode validation. Accepted-mode validation requires the recorded human decision, confirmer, date, and concrete evidence.

For a reasoned `concept-foundation-not-needed` source, keep Accepted Concept IDs and Accepted Requirement Model IDs as `none`, set Trace Applicability to `not-applicable`, record a concrete reason, and do not fabricate Concept Definitions, Scope Inventory, or Technical Landing Trace rows.

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
4. With current memory, an explicit `feature-archive-maintenance` request routes before Active Feature Guard because it maintains closed history. Eligibility blocks any selected active/paused path without switching current work.
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

## Inspection Order

Use this order:

1. Apply Bootstrap skill loading. After context compaction, long-running sessions, or stage-boundary uncertainty, do not continue from memory alone.
2. Check `.agent-loop/`; if missing, check legacy `agent-loop/`.
3. If present, read `<memory-root>/project.md`.
4. If `project.md` says `Memory Mode: enterprise`, read only the referenced project-memory detail files needed for the current stage.
5. If `project.md` says `Status: remote-entry`, read `<memory-root>/remote.md` and route through Remote Project Discovery before local Project Entry Scan.
6. Locate `Active Feature` and `Paused Features`.
6a. For Feature Monthly Archive or an archived follow-up candidate, read `features/archive.md` before opening the month path. Treat Feature ID as stable and verify the locator target, archive state, and flat/month uniqueness.
6b. If `.agent-loop/skills/INDEX.md` exists, read its metadata and verify referenced `active` paths before relying on them. Re-match active `bootstrap` / `on-demand` rows for each applicable actionable intent before stage-specific helper or fallback action; load and verify only the matched body. Do not load `proposed`, `disabled`, or `deprecated` skills into normal routing.
6c. For explicit Bug management, read `bugs/INDEX.md` metadata before creating a Bug or scanning Feature ownership. Resolve current Bug README, duplicate/reopen pointers, and related flat/archived Feature locators before relying on lifecycle or target claims.
7. Read current feature `spec.md`, `tasks.md`, `tests.md`, `plan.md`, `notes.md`, and `contracts.md` if present.
8. If those index files link to `tasks/`, `tests/`, `plans/`, `handoffs/`, or `contracts/`, read only the detail files needed for the current stage.
9. Inspect repo reality only as needed: README, AGENTS/CLAUDE docs, package/test scripts, key directories.
10. If local repo reality points to remote execution, or the human says this is a remote project, load `references/remote-project-discovery.md`. An empty local directory alone is not enough; if there are no remote hints, classify as `new-project`.
11. Verify long-term memory index targets before trusting them. If `project.md`, root guidance, or current artifacts point to onboarding-db, enterprise `project/*.md`, feature docs, contracts, or guidance files, check that the referenced path exists before relying on it.
12. Compare project memory with obvious repo reality.
12a. Run Branch Strategy Check when branch evidence affects the current work. Compare accepted durable policy and Target Release Context with native repository guidance, current Git reality, and feature/plan/submit evidence. Recommendation is read-only; adoption and every Git mutation remain separately Human-gated.
13. Choose the next stage.

If `project.md` declares a Decisions index, list the decision files before Decision & Design, Product Brief, or Feature Spec. Read decisions already linked by the active requirement, `product.md`, or `spec.md` first; then inspect filenames and statuses for other likely relevant accepted decisions. Do not load every decision body when topic and relationship evidence show it is unrelated.

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

Default memory root for new projects is `.agent-loop/`. If legacy `agent-loop/` exists, use it for the current run and ask before migrating.

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

Post-Merge Memory Reconciliation is an internal Submit / Integrate method, not a canonical stage or message intent. Route to `references/memory-reconciliation.md` only after code integration has one stable full Merged Code SHA and fresh code-verification evidence, and when Base, Source, Target-before, Result, non-empty Source/Target Branch, Target Release Context, Customer Boundary, and the accepted memory root can be identified.

Before creating `.agent-loop/memory-merges/` or a report, present the Start Human Review and obtain explicit authorization for that one reconciliation. Scan is then read-only. The Agent accounts for every path through the Target Canonical Memory Spine and Path Accounting Ledger, resolves question-specific fact authority, and derives the Desired Target Memory Snapshot.

Before Apply, present every add/update/remove path, expected unchanged path, attention item, Human Decision, post-check, restore scope, and normalized Plan Hash. Apply is authorized only for that exact hash. Changed evidence, stale plan/scan, unexpected dirty memory, unresolved 🔴 or `暂不处理`, unsafe/unclassified paths, completed replay, or missing snapshot evidence fails closed and routes to Recovery rather than guessing.

While the report is `待确认` or `已恢复`, or while any transaction is unresolved, block memory commit, push, release/publish, and Source branch cleanup. `已完成` permits only presentation of the next independent Human Gate; it does not authorize commit, push, tag, release, publish, merge, branch deletion, or cleanup.

## Stage Order

Default order applies after Message Intent Classification. For `requirements-discussion`, use Requirements Discussion before Project Entry-driven feature stages.

Default order:

```text
Message Intent Classification
Chat Entry / Requirements Discussion if Needed
Project Entry
Remote Project Discovery if Needed
Re-Adopt Agent Loop Project if Needed
Feature Monthly Archive If Explicitly Requested
Code-Guided Operational Support if Needed
[internal] Lightweight Change Assessment for eligible ordinary non-Bug changes
Project Skill Creation / Update if Needed
Requirement Archive
Decision & Design If Needed
Product Brief if Needed
Brainstorm / Clarify if Needed
Feature Follow-up And Flow-back if Needed
Targeted Feature Scan if Needed
Feature Spec
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

Default is Strict Mode:

```text
Before stage: ask permission.
After stage: ask continue / revise / pause / submit / close.
```

For non-trivial gates, the approval prompt must include a Human Review Summary. The summary is the human-facing approval view; the full artifact files remain the source of truth.

Allowed modes:

| Mode | Authorization scope | When it can start | What it may do without another stage gate |
|---|---|---|---|
| Strict Mode | one stage at a time | default for all work | nothing beyond the confirmed stage |
| Feature Auto-Loop | current feature | after Feature Spec and Requirement Checklist are accepted and human explicitly enables it | advance Agent-ready stages and tasks for the feature |
| Task Auto-Run | one task or one story | after the task/story plan is accepted and human explicitly enables it | run Analyze Consistency, then complete that task/story through TDD, verification, review, drift, Task Done Gate, and task status update |

Feature Auto-Loop means:

```text
Feature Auto-Loop = give one feature a bounded release lane.
```

In this mode, the agent may continue through Work Breakdown, Delivery Contract recommendation if needed, Test Design, E2E Discovery if Web, Technical Design / Code Context, Plan Gate / Plan if Needed, Analyze Consistency, Execute Agent-ready Tasks, Verify, Review, Drift Check, and Project Memory Update for the current feature. It must not skip Plan Gate before execution. It must stop before Bug Resolution Path decisions, Bug close/reopen, Feature creation/reopen, Requirement creation/lifecycle reconciliation, Feature Monthly Archive or rehydrate and their Batch Human Gates, branch creation, switching, deletion, push, or tag, creating or materially updating a project-local skill, executing a project-local skill without a current invocation grant, creating or updating Delivery Contract files, contract acceptance, breaking contract changes, Submit / Integrate, and Pause / Close.

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

Before enabling either auto mode, perform a final clarification pass:

- list remaining assumptions
- list Human-gated tasks or decisions
- list likely risk points
- list stop conditions
- ask for explicit mode confirmation

## When To Offer Auto Modes

Offer auto modes proactively, without waiting for the human to know the terms:

- after Requirement Checklist passes and Feature Spec acceptance is recorded, offer `Feature Auto-Loop` for Agent-ready downstream work
- after a task/story plan is accepted, offer `Task Auto-Run` for that execution unit
- when the human says confirmation is too frequent, asks the agent to continue by default, or appears to be repeatedly approving low-risk stages
- when a feature has a clear spec, clear tests, Agent-ready tasks, and no unresolved product/design/architecture/security/data decisions

Recommended wording:

```text
Strict Mode is safest and asks before each stage. If you want fewer confirmations, I can enable Feature Auto-Loop for this feature, or Task Auto-Run just for the selected task/story. Auto modes still stop for Human-gated decisions, unclear decisions, risky changes, failed verification, drift needing approval, unrelated dirty work blocking progress, human original requirement changes, first-version exclusions, Delivery Contract creation/acceptance/breaking changes, Complex Artifact Mode detail directory creation, directory guidance changes, unapproved subagent dispatch, branch creation, switching, deletion, push, or tag, submit, pause, close, commit, PR, merge, release, and publish.
```

Do not offer an auto mode as a substitute for missing clarification. If scope, acceptance, test approach, data rules, or affected boundaries are unclear, clarify first.

Auto modes do not remove stop conditions. Stop and ask when:

- a task is `Human-gated`
- product, design, architecture, security, data, approval, or public-interface decisions are needed
- a stage would modify human original requirements
- a Delivery Contract needs creation, human acceptance, or an accepted contract needs a breaking change
- a Project Skill Candidate needs Gate 1 before creation or material update
- a project-local skill is ready to execute without a current invocation Execution Gate grant
- spec, product scope, or acceptance criteria would change
- code reality conflicts with project memory or feature docs
- unrelated dirty work blocks progress
- a new dependency, migration, destructive operation, credential, external service, or long-lived boundary directory is needed
- directory-level `AGENTS.md` creation/update is recommended
- Complex Artifact Mode detail directories (`tasks/`, `tests/`, `plans/`) would be created or the feature would switch from simple to complex artifact mode
- the work would require first-version exclusions
- Feature Monthly Archive or rehydrate is requested; scan may remain read-only, but exact plan SHA-256 confirmation is required before apply
- a Bug needs Resolution Path confirmation, close/reopen, Feature creation/reopen, Requirement creation/reconciliation, or another action-specific Human Gate
- Bug Index/README, duplicate/reopen, Status/Resolution, Resolution Target, Expected Behavior authority, or Fix Feature locator evidence is invalid or contradictory
- an archive row target is missing, an archived directory lacks a row, a flat/month Feature ID collides, a `rehydrated` row points to a month path, an incomplete `.archive-txn` exists, or verified apply leaves an old durable path
- TDD cannot be followed or verification repeatedly fails
- review finds behavior/scope/architecture changes
- subagents are needed but not yet approved
- branch creation, switching, deletion, push, or tag is requested
- submit, commit, PR, merge, release, publish, pause, or close is requested

Allowed replies:

```text
continue
revise
pause
submit
close
change scope
skip with reason
enable Feature Auto-Loop
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

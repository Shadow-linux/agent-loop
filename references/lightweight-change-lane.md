# Lightweight Change Lane

## Purpose And Position

Lightweight Change Lane is an internal route before Feature construction for an ordinary actionable non-Bug change that is bounded, reversible, and exactly verifiable. It is not a canonical stage, message intent, Feature Type, Bug Resolution Path, task status, lifecycle, or Auto Mode.

The lane avoids unnecessary long-term Feature artifacts without lowering completion evidence or action-specific Human Gates. It uses one response-local Lightweight Execution Card to control the disclosed local edit and verification.

## Intent And Precedence

Use this sequence before deciding that a small-looking request is Bug or Feature work:

```text
explicit Bug management intent
-> Human-Guided Bug Management

actionable non-Bug change
-> Lightweight Change Assessment
   -> clearly eligible -> Lightweight Execution Card
   -> Feature trigger -> Feature Construction
   -> uncertain -> Human Choice with Agent Recommendation
```

Explicit Bug Management wins before this assessment.

Generic words such as `fix`, “修一下”, “改一下”, “small tweak”, or “simple” do not by themselves establish Bug management intent or lightweight eligibility. Human intent, expected-versus-observed evidence, existing Feature ownership, and impact evidence decide the route.

When evidence clearly decides the route, the Agent owns the initial judgment. There is no separate “enable lightweight mode” gate. When evidence is insufficient, perform zero writes and use Uncertain Route Human Choice.

## Project Entry Boundary

Project Entry classification is required; creating or repairing long-term Agent Loop memory is not required solely to run this lane.

Before assessment, inspect the root guidance, current Git branch and dirty state, exact target scope, nearby references/consumers, safety boundaries, and available verification entrypoints. Protect unrelated dirty work.

When `.agent-loop/` or an accepted legacy memory root exists, read only the memory claims, active Feature evidence, Branch Strategy, Target Release Context, and Project Skill INDEX metadata needed for this change. If an active Feature clearly owns the work, continue inside that Feature. If a relied-on memory claim is stale, missing, or conflicts with code reality, stop and recommend Recovery, Feature Construction, or Human Choice as appropriate.

When no Agent Loop memory exists, do not initialize `.agent-loop/` for the card. Inspect root guidance, Git/dirty state, target files, nearby references, verification entrypoints, and rollback evidence. A missing memory root is not itself a Feature trigger when the impact can still be established safely.

## Lightweight Change Assessment

Assess the request by product meaning, boundary impact, scope, uncertainty, verification, reversibility, ownership, and tracking needs. File count, line count, elapsed time, and number of Plan steps are supporting evidence only; none independently decides the route.

Before choosing, enumerate:

- the concrete goal and completion criteria;
- every in-scope path, value, or internal branch;
- known consumers and excluded boundaries;
- impact and risk;
- the exact targeted verification and expected result;
- rollback;
- active Feature, explicit Bug, Project Skill, branch, sealed-release, and dirty-work evidence;
- every action-specific Human Gate that remains.

Choose exactly one result: `clearly eligible`, `Feature trigger`, or `uncertain`.

## Eligibility

`clearly eligible` requires every condition below:

1. Goal and completion criteria are clear.
2. The entire edit scope is enumerable and has clear ownership.
3. No new product or technical decision is required.
4. No public API, event, data meaning, persistence, state, permission, security, credential, or trust boundary changes.
5. No new dependency, service, migration, architecture boundary, or cross-module protocol is introduced.
6. Accurate, executable targeted verification exists.
7. The change is reversible and rollback is concrete.
8. The request does not require Bug identity or Feature-level long-term tracking.
9. The work does not require cross-session recovery, pause/resume, handoff, subagent execution, or complex evidence storage.
10. Current evidence is sufficient for the Agent to accept responsibility for the route judgment.

A concrete bounded change request authorizes only the local scope disclosed in the card and its disclosed local verification. It does not authorize external, production, paid, destructive, configuration-write, deployment, Git, submit, release, publish, or Bug lifecycle action.

## Feature Hard Triggers

Any one of these signals routes to Feature Construction or the existing owning workflow:

- new or changed user-visible behavior, acceptance criteria, product rule, or product concept;
- public API, event, schema, persistence, product data, state flow, permission, security, credential, or trust-boundary change;
- new dependency, service, migration, durable architecture boundary, or cross-module protocol;
- unknown consumers or impact that cannot be bounded;
- ADR, Delivery Contract, complex E2E, multi-environment release design, or long observation need;
- cross-session continuation, pause/resume, handoff, subagent, or long-term progress/evidence tracking;
- clear ownership by an active Feature;
- explicit human request to manage the work as Feature or Bug;
- scope expansion after the card is emitted.

Human wording such as “just one line” or “simple change” cannot override a hard trigger.

## Uncertain Route Human Choice

When route evidence is insufficient, stop before Feature creation, local edits, or external effects. Present only the few real routes available, with:

- the concrete evidence and unknown;
- the Lightweight and Feature/Bug consequences that actually apply;
- one Agent recommendation and its reason;
- the exact human choice needed.

Wait for the answer. A human preference for the lane cannot override safety, data, public-contract, sealed-release, customer-isolation, or action-specific Human Gates. Reassess if new evidence changes the route.

## Lightweight Execution Card

The card is response-local by default.

Render the complete card from `templates/lightweight-execution-card.md` before the first write. It records Background, Goal / Completion Criteria, Scope, Lane Rationale, Impact / Risk, Plan, Current Progress, Verification, Rollback, Human Gates, and Result / Residuals.

All fields are required. For a field that is genuinely not applicable, record `none` plus a concrete reason. Never leave an empty placeholder. Update Plan checkboxes and Current Progress while executing, then record fresh results and remaining work.

Do not create `.agent-loop/changes/`, `.agent-loop/quick-fixes/`, or another lightweight backlog.

Do not create `spec.md`, `tasks.md`, `tests.md`, `plan.md`, or `notes.md` for the card. If the work needs those artifacts or durable recovery, promote it to Feature.

## Adaptive Plan Depth

A Plan is always required, but its depth is adaptive.

- A single confirmed fact replacement usually names the file, exact old/new fact, reference scan, verification, diff review, and rollback in two to four steps.
- Multi-file mechanical synchronization adds discovery, a complete affected-path list, consistency checks, and residual scans.
- A small isolated internal logic change adds one meaningful failure case, expected RED/GREEN evidence, and a focused regression.
- Environment-related work records environment, entrypoint, impact, bounded local checks, and rollback; any real external effect keeps its own Human Gate.

The card Plan is current-context control, not a construction-grade zero-context Feature `plan.md`, and it never uses No-Plan Decision. If reliable execution requires a much longer plan, hidden decisions, or durable handoff, use Feature Construction instead.

## Targeted TDD And Verification

Choose evidence from the actual failure mode:

```text
behavior logic changed and isolatable
-> targeted RED
-> minimal GREEN
-> focused regression

fact/config/path/domain/docs changed
-> syntax / parse / reference / residual / bounded dry-run checks
-> focused regression when applicable
```

Do not invent a unit test for a mechanical string, path, version, domain, documentation, or configuration fact change when parsing, reference, residual, syntax, or dry-run checks prove the risk more directly. Do not use “lightweight” to skip a meaningful RED/GREEN for an isolatable behavior branch.

Production-related facts receive local/static checks first. Any real production read, write, paid call, configuration write, deploy, credential use, or external effect waits for its existing authorization.

## Project Skill And Helper Boundaries

When a reliable memory root exists, run Project Skill Discovery Guard before generic action or helper fallback. A matched active Project Skill must pass manifest validation, load, and its per-invocation Execution Gate before use. Project Skill discovery or execution cannot widen the card Scope.

Lightweight Change Lane does not enter the mandatory Plan Gate / Plan or Execute Task / Story helper-backed stages. The controller owns the response-local Plan and targeted verification selection. Optional method advice may not introduce helper-native directories, a Feature workspace, a construction-grade plan, or a new mode/gate. Promotion to Feature restores all normal mandatory helper protocols.

## Scope Expansion

Scope expansion stops the lane before broader edits.

Expansion includes newly discovered consumers outside Scope, a required product/technical choice, a verification failure revealing a broader defect, any hard-trigger boundary, a new dependency/migration/ADR/Contract, lost rollback confidence, cross-session/handoff/subagent need, or evidence that the work should be tracked as Bug.

On expansion:

1. stop broader writes;
2. preserve investigation, current diff, and verification evidence;
3. name the triggering fact;
4. recommend exactly one Bug Management, Requirements Discussion, or Feature Construction route;
5. ask the human before keeping, reverting, or extending partial edits;
6. carry the card evidence into the approved workflow.

## Completion

Do not claim completion until all are true:

- every Plan step is completed or its cancellation is explicit;
- targeted verification ran fresh and its result is reported honestly;
- diff review confirms only the disclosed authorized Scope changed;
- no unresolved hard trigger or scope expansion remains;
- rollback remains valid;
- durable memory impact is checked and is either `none` with reason or a permitted mechanical synchronization of an already accepted fact;
- Result / Residuals states what changed, what did not, and what remains;
- all later actions remain behind their own Human Gates.

If verification fails, diagnose whether the bounded route remains valid. Do not silently widen the fix or declare success.

## Memory, Branch, Submit, And External Gates

Project memory may mechanically synchronize an already human-confirmed durable fact only when the exact memory path is listed in Scope and the update introduces no new decision. New product, architecture, environment, or release facts leave the lane for their owning workflow. Do not store card history, lightweight backlog, or transient progress in `project.md`.

An adopted Branch Strategy, Target Release Context, sealed-release rule, customer isolation, and exact Branch Action/Cleanup gates still apply. The card authorizes no branch creation, switching, deletion, merge, push, or tag.

Card completion authorizes no Git, release, publish, production, or Bug lifecycle action.

Commit, push, PR, merge, tag, release, publish, deployment, production/external reads or writes, paid calls, configuration writes, destructive operations, Feature close, and Bug close/reopen retain their independent Human Gates.

## Forbidden Behavior

- Do not choose the lane because a diff looks small, changes one file, or has few steps.
- Do not let “simple” override Feature hard triggers.
- Do not omit Plan, progress, fresh verification, diff review, rollback, or memory-impact review.
- Do not manufacture meaningless RED evidence for a fact correction.
- Do not bypass explicit Bug Management or an owning active Feature.
- Do not write before an uncertain-route human answer.
- Do not continue broader edits after scope expansion.
- Do not create a default lightweight directory, backlog, lifecycle, status, Feature Type, Bug Resolution Path, canonical stage, or message intent.
- Do not infer Git, release, production, external, or Bug lifecycle authorization from the card.

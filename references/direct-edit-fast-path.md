# Direct Edit Fast Path

## Purpose And Position

`Direct Edit Fast Path` is the lowest-cost Agent-owned method for a genuinely trivial, deterministic, ordinary non-Bug edit. It sits before the persistent Lightweight Change Lane and may also operate inside an already authorized Feature when the edit stays inside that Feature's accepted write boundary.

It reduces ceremony and persistence, not correctness. An eligible Direct Edit creates no persistent Agent Loop artifact, does not create or enter a Feature, and does not manufacture test work. It still ends with one final diff inspection plus the minimum matched check that proves the intended edit and the mechanical validity of the changed artifact.

Direct Edit is not a canonical stage, message intent, status, lifecycle, Mode, Feature Type, Bug Resolution Path, artifact family, authorization, or completion claim. It creates no default directory, card, index, counter, parser, scanner, cache, or archive.

Use this reference only after the latest Human message has already made the requested result concrete. Requirements shaping, product/design decisions, debugging, broad repairs, and work whose evidence is not bounded do not become Direct Edit merely because their textual diff may be small.

## Precedence And Route

Route in this order:

```text
explicit Bug management intent
-> Human-Guided Bug Management

active Feature clearly owns the edit
-> current Feature write authorization valid?
   -> yes + every Direct Edit condition true -> Direct Edit inside the Feature
   -> otherwise -> owning Feature Execute / Review / Gate route

ordinary actionable non-Bug change
-> Direct Edit Assessment
   -> every eligibility condition true -> Direct Edit Fast Path
   -> persistence or recovery control needed -> Lightweight Change Lane
   -> any Feature hard trigger -> Feature Construction
   -> uncertain -> Human Choice with one Agent recommendation and zero writes
```

Explicit Bug management intent takes precedence even when the likely patch is one line. Active Feature ownership also takes precedence over creating a separate Change card: the eligible edit stays part of the Feature's existing diff and authorization.

Generic wording such as “改一下”, “调一下”, “fix”, “small”, or “one line” is not enough evidence. The Agent inspects the target, known consumers, current authority, dirty work, and the cheapest credible proof before selecting the route.

## Eligibility

Direct Edit is available only when every condition below is true:

1. The requested final result is explicit and unambiguous.
2. The exact target paths and intended replacement, correction, or bounded property are enumerable before writing.
3. The edit mechanically applies an already decided fact; it does not invent product, interaction, business, technical, architecture, or rollout meaning.
4. Known consumers and affected references are bounded enough for one immediate inexpensive check.
5. The edit changes no public API/event/schema, data meaning, persistence, state transition, permission, security, credential, trust boundary, dependency, migration, architecture boundary, or cross-module protocol.
6. It has no production or external side effect and requires no deployment, paid access, credential, remote write, or environment mutation.
7. Rollback is the exact inverse diff and is immediately available without touching unrelated Human work.
8. One inexpensive artifact-matched check can directly prove the intended result.
9. Work will finish in the current session without planned pause/resume, handoff, Subagent, long observation, or durable recovery evidence.
10. No explicit Bug management request or separate long-term Feature tracking need exists.
11. Existing dirty work remains protected and the Agent can attribute the Direct Edit diff precisely.
12. Current evidence is sufficient for the Agent to own the route decision without semantic guessing.

Line count, file count, and expected minutes are supporting facts, never eligibility rules. A mechanical synchronization across several fully enumerated files may qualify; a one-line change with unknown consumers may not.

An already-decided user-visible string or configuration value may qualify when the Human or an accepted authority provides the final value and the edit does not change the surrounding product result, flow, contract, rollout, or acceptance criteria.

## Hard Escalation Triggers

Any one of these facts exits Direct Edit before broader writes:

- a new or changed product result, acceptance rule, business rule, interaction flow, state, permission, or data meaning;
- a public API, event, schema, persistence, security, credential, trust, migration, dependency, service, architecture, or cross-module boundary;
- an unknown consumer or reference that cannot be bounded cheaply;
- an ADR, Delivery Contract, Bug identity, complex E2E, release design, production check, or long-observation need;
- reliable proof requires new test design or broader verification;
- an accepted Feature, ADR, Contract, Human instruction, Submit rule, or Release rule requires a test at this exact owning boundary;
- planned cross-session work, pause/resume, handoff, Subagent, or durable recovery evidence;
- active Feature ownership without a valid current write authorization;
- unrelated dirty work prevents exact diff attribution;
- scope expansion, unexpected files, failed minimum checking, or uncertainty after the first write;
- the Human explicitly requests Bug, Feature, or Lightweight Change management.

Choose the smallest route that owns the newly discovered responsibility:

```text
durable bounded control needed -> Lightweight Change Lane
new product meaning            -> Requirements Discussion
explicit defect identity       -> Human-Guided Bug Management
broader implementation         -> Feature Construction / owning Feature Gate
```

Do not silently convert partial Direct Edit work into a larger workflow. Preserve the current diff, explain the discovered trigger, recommend one route, and ask before keeping, reverting, or expanding the partial edit unless the correct action is fact-determined and already authorized.

## Minimum Read-Only Scope Check

Before the first write:

1. inspect current branch, full HEAD, target status, and relevant dirty diff;
2. locate the exact target and bounded references with project-native read-only search;
3. identify the accepted or Human-provided fact being applied;
4. name the cheapest credible post-edit proof;
5. confirm the inverse diff is sufficient rollback;
6. confirm no eligibility condition or hard trigger is unresolved.

Then disclose, in one concise response-local statement, the exact target, intended correction, minimum check, and rollback. This disclosure is not a Plan, No-Plan Decision, durable authorization record, or substitute for any existing Human Gate.

If classification remains uncertain, perform zero writes and return a small Human Choice with one Agent recommendation: Direct Edit, Lightweight Change, or Feature/Bug route as applicable.

## Execution Contract

Execute exactly this sequence:

```text
minimum read-only scope check
-> classify every eligibility condition
-> concise target / correction / check / rollback disclosure
-> apply only the bounded edit
-> inspect the exact attributed diff
-> run one minimum artifact-matched check
-> report result, evidence, and any escalation fact
```

The result report is response-local. It names the changed path/value, the exact minimum check and outcome, whether the diff stayed bounded, and any remaining owning-workflow obligation. It does not claim Feature completion, full verification, Submit readiness, release readiness, or permission for a later action.

Direct Edit never creates a Plan or No-Plan Decision. It does not enter the mandatory Plan or TDD helper stages. If the route escalates to initial Feature execution, explicit Bug repair, or another plan-owned path, the normal helper protocol resumes before those stage actions.

## Minimum Post-Edit Check

Select the cheapest proof that directly covers the changed failure mode:

| Edit kind | Minimum check |
|---|---|
| Plain text, comment, documentation, or label | Inspect the exact diff; confirm the intended new text and, when applicable, absence of the exact stale text. |
| Link, path, domain, command, or constant | Inspect the diff plus a bounded reference/residual search. Do not contact the endpoint merely to validate a textual replacement. |
| JSON, YAML, TOML, manifest, or configuration | Inspect the diff plus the available native parser or syntax validation. |
| Shell, Python, or another directly parseable script | Inspect the diff plus the language's inexpensive syntax/parse check when available. |
| Formatting or generated metadata | Inspect the diff plus the owning deterministic inexpensive formatter/checker when one exists. |
| Already-authorized Feature implementation adjustment | Inspect the diff plus the least-cost proof that the accepted behavior is represented; keep the Feature's normal accepted verification due at its existing boundary. |

The minimum check is not a new test suite. Do not write a new test, manufacture RED, run a full project suite merely because the edit exists, create a Regression Test Advisory solely for the edit, or rerun every Feature obligation after each temporary adjustment.

If a test is the only reliable proof, Direct Edit is not eligible. If an existing Human instruction or accepted Feature, ADR, Contract, Submit, or Release boundary already requires tests, keep that obligation at its owner. When a newly needed repository-wide run is material to the intended claim, stop before the claim and apply the Full Test Run Confirmation contract in `runtime.md`.

## Same-Scope Iterative Tuning

Repeated changes form one tuning loop only when they keep the same accepted Feature boundary and same tuning question:

```text
same accepted Feature boundary and same tuning question
-> Human requests one or more bounded value adjustments
-> Agent applies intermediate values inside the current write grant
-> no per-iteration test, card, Plan, notes, or formal verification
-> Human identifies the final acceptable value
-> one final diff inspection plus the minimum matched check
-> continue the owning Feature's existing final verification
```

Spacing, sizing, visual density, exact copy, or a non-business display multiplier may qualify when accepted product behavior is unchanged. A price, balance, quota, scoring, authorization, retry, accounting, persistence, allocation, or other business/runtime multiplier is not cosmetic merely because it is numeric.

The loop ends and the edit is reclassified when the target property, source of truth, accepted product behavior, risk boundary, consumer set, or verification question changes. An interrupted loop resumes as Direct Edit only when the exact scope and latest Human-selected value remain attributable; otherwise use the owning Feature or Lightweight route.

## Feature-Local Use

Inside an active Feature, every condition below is additionally required:

- Feature Context and the accepted execution boundary are current and reliable;
- current Execute or within-boundary Review repair authorization permits the target write;
- the edit is implementation-only and does not change Product Slice, Story, acceptance, ADR, Delivery Contract, risk, rollback, or verification obligations;
- all general Direct Edit eligibility conditions remain true.

The edit stays inside the owning Feature. Do not create a nested Lightweight Change card, new Task, another Gate, new test, or one notes row per temporary adjustment. The final diff and owning task/review summary naturally include the result, and the Feature's accepted verification, review, drift, Task Done, and Close rules remain due.

If definition or implementation boundary changes, use existing Gate 1/Gate 2 drift routing. If explicit Bug management begins, use Bug Management. If scope or proof cannot remain bounded, continue only through the owning Feature workflow.

## Zero-Artifact And Memory Boundary

Direct Edit creates no persistent Agent Loop artifact:

- no Feature workspace or Lightweight Execution Card;
- no `tasks.md`, `tests.md`, `plan.md`, No-Plan Decision, dedicated `notes.md` row, or handoff;
- no Change scanner row, pending count, age trigger, or Memory Review;
- no `project.md` or enterprise project-memory write;
- no test-debt item, Regression Test Advisory, Direct Edit log, index, cache, or archive.

Outside a Feature, only the response-local result preserves the immediate evidence. Inside a Feature, the normal final diff and existing owning task/review summary include the change without a separate per-edit record. A later independently authorized Git commit may naturally preserve the diff; Git is not required merely to record Direct Edit.

An edit that establishes a durable project fact future Agents must recover independently is not zero-artifact work. Route it to Lightweight Change, the owning Feature, or the appropriate project-memory workflow.

## Interruption And Failure

Direct Edit intentionally has no durable recovery contract. After interruption or context loss:

1. re-inspect branch, full HEAD, dirty diff, ownership, and target files;
2. continue only when the exact scope, accepted fact, latest Human-selected value, and rollback remain attributable;
3. otherwise stop before another write and route to Lightweight Change or the owning Feature.

If the minimum post-edit check fails, scope expands, unexpected files appear, or broader impact is discovered:

- make no completion or verification claim;
- do not silently add tests, files, consumers, or broad fixes;
- preserve and disclose the current exact diff;
- identify the hard trigger and recommend one owning route;
- ask before keeping, reverting, or expanding partial edits when evidence does not determine the action.

## Human Gates And Forbidden Behavior

Direct Edit uses only the authority already present in the concrete Human request or current accepted Feature write boundary. It creates no execution authorization and never replaces an existing Human Gate.

The following remain independently Human-gated: Requirement/Product/ADR/Delivery Contract decisions; Feature creation/reopen and Gate 1/2; Bug create/reopen/Resolution Path/close; branch create/switch/delete/merge/push/tag/cleanup; Commit, PR, Release, Publish, Seal, deployment, production/external actions, paid calls, configuration writes, destructive operations; and any new repository-wide full-test or full-validation execution not already exactly authorized.

Forbidden behavior includes:

- selecting Direct Edit from line count, file count, time estimate, urgency, or Human responsibility claims alone;
- using it to change product or technical meaning;
- treating skipped test creation as skipped checking;
- inventing a reusable bypass flag or durable full-run authorization cache;
- letting Direct Edit satisfy Task Done, Feature Close, Submit readiness, Release readiness, or another Gate;
- inheriting Commit, Push, Release, production, or external authority from the edit request;
- weakening any existing path boundary, exact plan hash, transaction journal, post-check, restore, rollback, Archive/Rehydrate, Full Memory Audit, or Checker Rescue constraint.

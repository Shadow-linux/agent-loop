# Human Review Summary

Use this before asking the human to approve or confirm an `agent-loop` stage.

## Purpose

Humans approve decisions, scope, risk, and next actions. They should not need to read a full execution document every time. The agent should present a compact approval view first, usually as Markdown tables, while keeping complete source-of-truth artifacts in files.

```text
human-facing = summary table first
agent-facing = full artifact files
evidence = always named or linked
risk / blocker / human decision = never hidden
```

## When To Use

Use before human confirmation for:

- Product Definition / Product Human Review, including cumulative internal Concept Foundation coverage when triggered
- Decision & Design record creation, acceptance, compatibility update, or superseding decision
- Project Entry / Project Entry Scan
- Branch Strategy recommendation/adoption and every requested Git action
- legacy onboarding-db reference cleanup
- Remote Project Discovery
- Requirement Archive
- Feature Spec
- Work Breakdown / Tasks
- Delivery Contract acceptance or breaking change
- Test Design
- E2E Discovery
- Plan approval
- Drift Check
- Project Memory Update
- Feature Completion Check
- Submit / Integrate
- Pause / Close
- directory-level `AGENTS.md` creation or update
- multi-file or multi-fact updates that should use Batch Human Review

For tiny one-line changes, a short 3-line summary is acceptable:

```text
Summary:
Evidence:
Decision:
```

Do not force a large table when it adds noise.

## Required Shape

Every Human Review Summary should include:

- stage name
- artifact paths that will be written or updated
- concise table of what changed or what will happen
- risk / blocker / open question column when relevant
- evidence column when facts are claimed
- explicit human decision requested
- recommended next stage

## Batch Human Review

Use Batch Human Review when the agent proposes to create or update multiple documents, multiple rows, multiple facts, or multiple long-term memory entries in one stage.

Required table:

| File / Item | Action | Change Summary | Source Evidence | Confidence | Affects Long-Term Memory | Suggested Action |
|---|---|---|---|---|---|---|

Allowed human choices:

```text
approve all
approve selected
revise selected
defer selected
skip this batch
```

Use Batch Human Review for:

- legacy onboarding-db reference cleanup when project memory or root guidance points to missing/stale docs
- project memory backfill with multiple facts
- AGENTS.md / CLAUDE.md or directory guidance updates
- drift check backfill
- feature close final document sync
- spec/tasks/tests/plan changes when multiple items are affected

High-confidence rows can be drafted, but cannot become reviewed or written as accepted long-term fact without human confirmation.

## Stage Table Patterns

### Product Definition Approval

Use after Product Definition Depth Scan and, for Standard, after the one-question-per-turn Human Grill Contract has resolved each blocker. This is the cumulative Product Human Review surface; internal Concept Foundation / Requirement Product Model methods do not add another approval stage.

| Review Item | Agent Recommendation | Source Evidence | Included / Not-Applicable Detail | Open Blocker / Risk | Human Decision |
|---|---|---|---|---|---|
| Profile | brief / standard with trigger |  |  | none / blocking | confirm / revise |
| Product Value / Scope | problem, outcome, in/out scope |  |  | none / blocking | confirm / revise |
| Concepts / Rules | cumulative accepted meanings |  | Concept IDs / rule anchors / not-applicable reason | none / blocking | confirm / revise |
| Relationships / Permissions | accepted boundaries |  | IDs / not-applicable reason | none / blocking | confirm / revise |
| Actions / Flow / State | accepted journey and terminals |  | IDs / not-applicable reason | none / blocking | confirm / revise |
| Product Facts / Exceptions | fact ownership and recovery |  | IDs / not-applicable reason | none / blocking | confirm / revise |
| Derived Visuals | current / stale / absent | source IDs + semantic digest | output or fallback | none / blocking | confirm / regenerate / omit |
| Design Readiness | none / candidate / required |  | candidate links | non-blocking / blocking | acknowledge / revise |

Add:

```text
Requirement Set path:
Effective Product Definition draft/source:
Product Definition Profile: brief | standard
Product Review decision: confirm | revise
Requirement lifecycle decision: separate / unchanged / explicitly <status>
Artifacts to write/update:
Recommended next stage: continue Requirements Discussion | Requirement Record / Archive | Design Readiness
```

This summary is cumulative confirmation of the current product baseline. It does not replace the strict one-question-per-turn Grill used to resolve blocking meanings. Product Human Review confirmation is non-bypassable for a new Effective Product Definition: `revise` or an unresolved row remains in Requirements Discussion. Product Review confirmation does not authorize Requirement acceptance, Feature start, ADR acceptance, code execution, or Git actions. Requirement Record / Archive still requires disclosure of exact files and byte-stable human sources.

### Decision & Design Approval

Use before creating, accepting, superseding, or materially updating a project / cross-feature Decision & Design record.

| Item | Review Content |
|---|---|
| Effective Requirement Source | Effective Product Definition path/Profile/Product Review, or legacy Effective Concept Foundation status, plus Last Compatibility Check and `current` / `review-required` |
| Requirement Model Scope | source total / in-scope / existing-decision / feature-local / proposed-decision / not-applicable / missing |
| Requirement Model Coverage | in-scope total / landed / existing-decision / feature-local / not-applicable / missing |
| Chosen Technical Decision | chosen option and the main rejected alternatives |
| Product Semantics Preserved | yes / no; list any product blocker that must return to Requirements Discussion |
| Migration / Compatibility / Rollout | triggered / not-triggered for each concern, with reason or linked section |
| Design Slice Ownership | planned / unassigned / deferred / out-of-scope, including affected Feature Specs |
| Verification | proof direction for every landed row and accepted-decision dependency |
| Human Decision | accept / revise / return to Requirements Discussion / require superseding ADR |

Add:

```text
ADR path:
Effective Product Source or legacy Effective Concept Source:
Upstream Compatibility: current | review-required
Artifacts to write/update:
Recommended next stage: Decision & Design If Needed | Feature Spec | Requirements Discussion
```

The summary must expose `not-applicable`, `feature-local`, deferred, out-of-scope, missing, and compatibility-review items. ADR acceptance still requires explicit human confirmation; the summary does not replace the complete decision record or authorize a changed accepted decision to be rewritten in place.

Before showing this summary, keep the ADR `proposed` and run structural preflight. If the human accepts, record `Decision: accepted`, `Confirmed By`, `Confirmed At`, and concrete `Evidence` in the ADR Human Review Evidence section, then rerun accepted-mode validation. Never infer acceptance from a validator pass or from the summary being displayed.

### Feature Spec Approval

| Item | Summary |
|---|---|
| Feature |  |
| Goal |  |
| In Scope |  |
| Out of Scope |  |
| Stories |  |
| Open Questions |  |
| Risks |  |
| Artifacts |  |
| Human Decision | Approve spec / revise / pause |

### Work Breakdown Approval

| Task | Story | Slice | Mode | Depends On | Verification | Risk / Gate |
|---|---|---|---|---|---|---|
| T001 | US1 | vertical | Agent-ready | none |  |  |

Add a short summary:

```text
Recommended execution: linear | parallel | barrier
Next recommended stage:
Auto mode option:
```

### Test Design Approval

| Type | Coverage | Execution | Command / Tool | Blocker | Evidence Location |
|---|---|---|---|---|---|
| Unit |  | automatic |  |  | notes.md |
| API |  | automatic |  |  | notes.md |
| E2E |  | existing-framework / browser / chrome / computer-use / manual / blocked |  |  | tests.md |

### Delivery Contract Approval

| Contract | Type | Producer | Consumers | Status | Interface Summary | Compatibility | Verification | Human Decision |
|---|---|---|---|---|---|---|---|---|
| API001 | API |  |  | draft |  | compatible / breaking | pending | accept / revise |

For breaking changes, list every affected consumer, scan evidence, compatibility option, migration action, and rollout order before asking for approval. A prior human request to "just change it" is not final approval; ask again after the impact table is shown.

### Plan Approval

| Item | Summary |
|---|---|
| Scope |  |
| Files |  |
| Interfaces |  |
| TDD RED |  |
| GREEN |  |
| Verification |  |
| Risks |  |
| Stop Conditions |  |
| Human Decision | Approve plan / revise / enable Task Auto-Run |

### Drift Check Approval

| Drift | Type | Impact | Backfill Location | Evidence | Human Decision |
|---|---|---|---|---|---|
|  | behavior | feature | spec.md |  | accept / revise / reject |
|  | long-term | project | project.md or project/*.md |  | accept / ignore |

### Project Memory Update Approval

| Update Area | Current | Proposed | Reason | Evidence | Human Decision |
|---|---|---|---|---|---|
| Test Commands |  |  |  |  | accept / skip |
| Capability |  |  |  |  | accept / skip |
| Directory Map |  |  |  |  | accept / skip |
| Domain Language |  |  |  |  | accept / skip |

### Project Entry Scan Approval

| Item | Summary | Evidence | Confidence | Human Decision |
|---|---|---|---|---|
| Scope | safe project memory / root guidance / commands / boundaries / uncertainties |  |  | approve / revise |
| Subagents | none / proposed lanes |  |  | approve / skip |
| Explicit Non-Goals | no onboarding-db / no deep dives / no onboarding diagrams |  |  | approve / revise |
| Write Plan | project memory / guidance |  |  | approve / revise |

### Branch Strategy Adoption

| Item | Current Evidence | Recommended Value | Risk / Reason | Human Decision |
|---|---|---|---|---|
| Adoption Status | unconfirmed | accepted / declined / not-needed | recommendation is not adoption | human only |
| Profile | existing-project / unclear / not-applicable | existing-project / human-guided-release / not-applicable | declined requires not-applicable plus a concrete reason | human only |
| Main / Release / Development Patterns |  |  | naming and release boundary | human only |
| Release Immutability |  | released / sealed | repairs require a new patch | human only |
| Customer Isolation |  | no wholesale reverse merge | protects standard product line | human only |
| Deletion Policy |  | temporary branch only after merge evidence | release branches retained | human only |
| Target Release Context |  | standard / customer pointer | no Git action authorization | human only |

### Legacy Onboarding-DB Reference Cleanup

| File / Item | Action | Change Summary | Source Evidence | Confidence | Affects Long-Term Memory | Suggested Action |
|---|---|---|---|---|---|---|

If subagent scan results conflict, include:

| Conflict | Finding A | Finding B | Evidence A | Evidence B | Current Judgment | Action |
|---|---|---|---|---|---|---|

### Feature Monthly Archive Batch Human Review

| Item | Summary | Evidence / Exact Value | Human Decision |
|---|---|---|---|
| Operation | archive / rehydrate |  | confirm / revise |
| Plan SHA-256 | expected exact hash |  | confirm exact batch |
| Selected Months / Feature IDs | explicit scope |  | confirm / revise |
| Eligible | closed and complete |  | include / exclude |
| Blocked | candidate plus blocker |  | acknowledge / resolve |
| Moves | source -> target |  | confirm |
| Reference Edits | path, old/new, occurrence, before/after hash |  | confirm |
| Unchanged Content | whole feature contents and immutable requirement sources |  | acknowledge |
| Transaction Journal / Restore | journal path, backups, reverse moves, post-check |  | acknowledge |
| Platform evidence | macOS / Windows actual or test-defined |  | acknowledge |
| Decision | apply exact hash / revise / stop |  | human only |

The scan is read-only. The Batch Human Gate authorizes only the displayed expected plan SHA-256; a stale plan requires a new scan and review. Feature Monthly Archive maintains `features/archive.md`; rehydrate before reopened execution.

### Bug Triage And Resolution Path Review

| Item | Status / Value | Evidence | Human Decision |
|---|---|---|---|
| Bug Identity | new / existing / duplicate-candidate / reopen-candidate / unclear | Bug Index + README + overlap evidence | confirm / investigate |
| Report Origin | person / customer / group / qa / monitoring / automated-test / agent / external-ticket / other / unknown | source reference or `unknown` | acknowledge |
| Observed Behavior | concise failure fact | reproduction/log/test/runtime evidence | acknowledge / revise |
| Expected Behavior | accepted / ambiguous / conflicting | Requirement / ADR / Contract / Feature / explicit human evidence | confirm / requirements discussion |
| Duplicate / Reopen | none / candidate / confirmed | canonical Bug or prior Close/Reopen evidence | confirm / investigate |
| Severity / Priority | evidence-backed / human-decided / unknown | impact + explicit priority evidence | confirm / revise |
| Requirement Impact | none / violates-accepted-behavior / ambiguity-found / change-required | related Requirement evidence | no change / reconcile / discuss |
| Recommended Resolution Path | investigate-first / flow-back / linked-feature / maintenance-fix / requirement / no-fix | Candidate Match Matrix + rationale | confirm / revise / stop |
| Target | exact Feature / Requirement / investigation / candidate Resolution | resolved locator/source | confirm / revise |
| Requested Authorization | exact Resolution Path only, plus separately named Feature/Requirement action if requested | current review | human only |
| Explicitly Not Authorized | Bug close/reopen, other Feature/Requirement actions, archive apply, branch, submit, commit, push, tag, release, publish unless separately named | gate inventory | acknowledge |
| Human Decision | exact bounded decision | current review | human only |

Unknown Origin does not block progress. Similar titles do not prove duplicate identity. Resolution Path approval cannot be reused as Feature creation/reopen, Requirement change, Bug close, or Git authorization.

### Bug Verification And Close Review

| Item | Status / Value | Evidence | Human Decision |
|---|---|---|---|
| Bug ID / Current Status | `verifying` / other | Bug README + Index | acknowledge / investigate |
| Candidate Resolution | fixed / duplicate / not-a-bug / cannot-reproduce / accepted-risk / superseded | required Resolution evidence | confirm / revise / keep-verifying |
| Fix Feature | exact Feature or no-fix | Feature Spec/notes and locator | acknowledge / revise |
| Original Reproduction / Substitute | pass / fail / incomplete | Bug Verification Matrix | accept / rerun |
| Regression / Safety Evidence | pass / fail / incomplete | fresh commands/results | accept / revise |
| Review / Drift | complete / missing / conflict | current records | proceed / stop |
| Remaining Risk | none / concrete risk | evidence and impact | accept / resolve |
| Bug Close Decision | confirm / revise / keep-verifying | Bug-specific closure evidence | human only |
| Feature Close Decision | confirm / continue / pause / revise-scope | Feature Completion Check | human only |
| Explicitly Not Authorized | Feature close, submit, branch, commit, push, tag, release, publish unless separately confirmed | gate inventory | acknowledge |

Bug Close and Feature Close may appear in one summary but remain separate decisions. Passing Feature tests is not the Bug Close Gate, and commit/push approval is not a close decision.

### Feature Completion Check

| Check | Status | Evidence | Issue |
|---|---|---|---|
| Tasks | pass / fail |  |  |
| Tests | pass / fail |  |  |
| Feature Close Review | pass / fail |  |  |
| Drift Check | pass / fail |  |  |
| Project Memory | pass / fail |  |  |
| Submit Status | done / skipped / needed |  |  |

Conclusion:

```text
Recommendation: close | continue | pause before new feature | update scope
Human Decision:
```

### Submit / Integrate

| Item | Status | Evidence |
|---|---|---|
| Verification | pass / fail |  |
| Drift Check | done / missing |  |
| Diff Review | clean / issues |  |
| Unrelated Changes | none / present |  |
| Action | prepare / commit / PR text / skip | human decision needed |

### Branch Strategy And Action Review

| Item | Status / Value | Evidence | Human Decision |
|---|---|---|---|
| Observed Policy / Git Evidence | coherent / conflicting / incomplete | native policy + Git evidence | acknowledge / investigate |
| Adoption Status / Profile |  | `project.md` | acknowledge / revise |
| Source Branch / Branch Class |  | Git + feature evidence | acknowledge / revise |
| Target Release Context / Target Branch |  | accepted policy + plan | acknowledge / revise |
| Sealed Check | open / released / sealed / unknown | release evidence | proceed / stop |
| Customer Isolation | pass / fail / unknown | branch ancestry and policy | proceed / stop |
| Verification / Review / Drift | pass / fail / missing | current feature evidence | proceed / stop |
| Merge Evidence / Deletion Policy | complete / missing / not-applicable | merge/submit evidence | delete / retain / stop |
| Requested Authorization | prepare / create / switch / commit / push / merge / delete / tag / release / publish | latest human request | human only |
| Explicitly Not Authorized | every action outside the request | review summary | acknowledge |
| Remaining Risk / Blocker | none / exact blocker | evidence and impact | accept / resolve / stop |
| Human Decision | exact bounded action or no action | current review | human only |

An accepted Branch Strategy, Target Release Context, plan, or auto mode is never action authorization. Creation or switching of one exact development branch uses the Branch Action Gate. Ask for the exact mutation after current evidence is shown; a cleanup decision must name the temporary branch and its merge evidence.

### Post-Merge Memory Reconciliation Start

Use before creating `memory-merges/` or a Memory Merge Report. The requested decision authorizes only this report and read-only fact reconciliation.

| Item | Observed value | Evidence | Risk / blocker | Human decision |
|---|---|---|---|---|
| Merge Base / Source / Target-before / Merged Code SHA | full SHAs | Git commits and HEAD | missing or unstable SHA stops | confirm / stop |
| Source / Target Branch |  | Git plus accepted Branch Context | Source evidence must remain available | confirm / revise |
| Target Release Context / Customer Boundary |  | accepted policy and plan | boundary ambiguity stops | confirm / revise |
| Code Verification | pass / fail | fresh bounded evidence | failure stops | acknowledge / stop |
| Memory Root | `.agent-loop` / `agent-loop` | existing accepted root | dual root or migration stops | confirm / recover |
| Proposed Report | `<memory-root>/memory-merges/MM-<short-sha>/README.md` | full SHA collision check | no directory before approval | create / stop |
| Explicitly Not Authorized | write business memory, Apply, commit, push, tag, release, publish, merge, branch delete, Source cleanup | gate boundary | none follows from Start | acknowledge |

Recommendation: start read-only reconciliation for this exact Merge Context or stop with the evidenced blocker.

### Post-Merge Memory Reconciliation Exact Rewrite Plan

Use after Fact Reconciliation and before Apply. The requested decision authorizes only the displayed normalized Plan Hash.

| Review group | Required content | Evidence | Human decision |
|---|---|---|---|
| 🔴 必须决定 | each unresolved semantic conflict, narrowed options, Agent recommendation, impact | question-specific authority | decide each / revise / stop |
| 🟡 建议复核 | grouped recommended actions and material impact | reconciled facts and diffs | accept group / revise selected |
| 🟢 普通变更汇总 | count and paths/stable IDs by action | deterministic ledger | acknowledge |
| Add / Update / Remove | every path, pre/post hash, mode, expected diff | exact operations | approve / revise |
| Expected Unchanged | every guarded path and hash | scan inventory | acknowledge / revise |
| Plan Hash | exact 64-character normalized SHA-256 | canonical plan JSON | approve exact hash / reject |
| Post-check | zero-change scan plus machine and Agent semantic checks | expected result | acknowledge / revise |
| Restore Scope | only this Apply's memory changes, exact backups, reverse order | transaction plan | acknowledge / revise |
| Explicitly Not Authorized | commit, push, tag, release, publish, merge, branch delete, Source cleanup | independent gates | acknowledge |

If any 🔴, `暂不处理`, unclassified path, blocker, stale scan, or changed plan remains, do not request Apply approval. A changed plan requires a new hash and a new review.

## Rules

- The table is not the source of truth. Update the owning artifact after confirmation.
- Do not hide uncertainty to make a table look clean.
- For complex artifacts, table rows may link to `tasks/*`, `tests/*`, or `plans/*` detail files.
- Delivery Contract rows may link to `contracts/*` detail files.
- Keep table cells concise. Put long reasoning in the artifact file, not the approval view.
- If a stage has both product and engineering implications, show both rather than compressing them into a vague summary.
- When asking for approval, prefer a concrete decision: "approve", "revise", "pause", "enable auto mode", "reject this backfill".

# Adaptive Product Definition

## Purpose And Ownership

Use this reference inside Requirements Discussion after `requirement-management.md`. The Agent inspects human source material and project evidence, recommends one depth, drafts one Requirement Product Definition, and presents it for Product Human Review. After the Requirement Record / Archive Gate, the current reviewed definition lives at:

```text
<memory-root>/requirements/<record-date>-<topic>/product.md
```

Human original source materials remain byte-stable. The Agent-authored `product.md` normalizes supported product meaning and points back to those sources; it never overwrites, edits, or silently replaces them.

Product Definition Profile is exactly:

```text
brief | standard
```

The Profile is documentation depth, not a stage, message intent, lifecycle status, Feature Type, or implementation authorization. New Feature work does not create another `product.md`; Feature `spec.md` records a Product Slice from the effective Requirement source.

## Product Definition Depth Scan

Choose `brief` only when every condition is true:

- product goal and observable outcome are clear;
- principal user or role is known;
- scope and non-goals are enumerable;
- no identity, relationship, fact ownership, lifecycle, permission, or shared rule is added or changed;
- no multi-step closure, asynchronous result, compensation, or recovery model is needed;
- acceptance direction is observable;
- available evidence contains no unresolved product-semantic conflict.

Any failed or uncertain condition prevents Brief. Choose `standard` when any of these signals appears:

- a complete capability or multi-step journey is introduced;
- several roles, tenants, customers, operators, or external systems participate;
- identity, relationship, source-of-truth, fact ownership, lifecycle, terminal meaning, permission, eligibility, pricing, quota, inventory, approval, or another shared product rule changes;
- asynchronous work, callback, retry, reconciliation, compensation, manual handling, or degradation matters;
- one Requirement needs multiple Delivery Phases or Features;
- source material, code, tests, historical behavior, or accepted product meaning conflicts;
- user success, operational closure, or acceptance cannot be expressed safely as a Brief;
- evidence is insufficient to prove that simplification is safe.

Sentence length, page count, file count, and the human calling something “small” do not select a Profile. Bug Management, Lightweight Change, active Feature ownership, and ordinary Chat retain their earlier routing precedence.

If new evidence reveals a Standard trigger while drafting Brief, disclose the trigger and affected views, then upgrade the same draft. Do not create another Requirement Set merely for the depth change. Do not downgrade a recorded Standard source without a concrete Human Review explanation.

## Brief Contract

Brief contains these product sections and no fabricated product-model views:

1. Problem / Background
2. Target User / Scenario
3. Goal / Expected Product Outcome
4. In Scope
5. Out Of Scope / Non-goals
6. Acceptance Direction
7. Source Evidence
8. Open Questions / Remaining Risk
9. Product Human Review Evidence

Brief reduces modeling depth only. It never removes source evidence, Human Review, scope, observable outcome, or remaining-risk disclosure.

## Standard Contract

Standard includes every Brief section and runs the Product Completeness Scan. It expands only evidence-backed product views. Do not add empty model tables or invent stable IDs to make the document look complete.

### Product View Applicability

Every Standard definition records exactly one row for each view:

| View | Allowed applicability | Included expression |
|---|---|---|
| Concepts | `included | not-applicable` | Concept Definitions with `C-*` |
| Relationships | `included | not-applicable` | Concept Relationships with `REL-*` |
| Permissions | `included | not-applicable` | Role / Permission Matrix with `PERM-*` |
| Actions / Outcomes | `included | not-applicable` | Commands / Events with `CMD-*` / `EVT-*` |
| Flow | `included | not-applicable` | Primary Business Flow with `FLOW-*` |
| State | `included | not-applicable` | Product State Model with `STATE-*` |
| Product Facts | `included | not-applicable` | Requirement Product Model with `PM-*` |
| Exceptions / Recovery | `included | not-applicable` | Exception Paths with `EX-*` |
| Product Rules | `included | not-applicable` | Product Rules with resolvable section anchors |

`included` requires concrete evidence, the named section, and all stable IDs owned by that view. `not-applicable` requires a concrete product reason and must not create a placeholder section or stable ID. Applicability is coverage, not lifecycle.

Product Rules are first-class product meaning but receive no new stable `RULE-*` namespace in this version. Reference them as `product.md#<rule-anchor>`.

## Product Completeness Scan

Before Product Human Review, inspect every dimension and record missing blockers or a reasoned not-applicable result:

| Dimension | Required question |
|---|---|
| Product Value | Do problem, outcome, scope, non-goals, and success direction agree? |
| User | Can each principal user reach an observable result from a real scenario? |
| Product Semantics | Are concepts, relationships, facts, rules, states, and permissions consistent? |
| Experience | Are feedback, empty/error states, notification, and manual paths defined when relevant? |
| Operations | Are review, recovery, observation, reconciliation, or manual handling needed? |
| Technical Readiness | Which shared decisions must go to Design Readiness / ADR? |
| Testability | Can success and failure directions be observed and verified? |

This scan is Agent reasoning plus Human Review. Automated validators check structure, sources, IDs, references, review evidence, and derived-view freshness only; they do not decide whether product semantics are correct.

## Human Grill Integration

When a Standard signal can change downstream meaning, keep the Human Grill Contract:

```text
inspect evidence
-> extract candidate concepts
-> recommend one definition and explain impact
-> ask the human one blocking question
```

一次只向人类确认一个阻塞问题。Do not ask the human to approve an internal method name. After the answer, revise the same `product.md` draft and present the cumulative confirmed meanings in Product Human Review.

Product Definition Depth Scan, Product Completeness Scan, Concept Foundation, Requirement Product Model, and derived visual generation are internal Requirements Discussion methods. They are not canonical stages or message intents. An unresolved identity, relationship, rule, lifecycle, state, permission, fact-ownership, terminal, or acceptance blocker stops Design Readiness, ADR, and Feature Spec.

## Product Human Review

Present a table-first summary containing:

- Profile recommendation and triggers;
- source evidence and any conflict;
- every Product View Applicability result;
- confirmed concepts, facts, rules, and observable outcomes;
- open blockers and remaining non-blocking risk;
- derived visual freshness when visuals exist;
- Design Readiness candidates;
- the explicit decision to confirm or revise the Product Definition.

The persisted evidence is:

```text
Decision: confirmed
Confirmed By: <human identity or human>
Confirmed At: YYYY-MM-DD
Evidence: <concrete review statement>
Implementation Authorized: no | separately-confirmed
```

Product Review confirmation does not authorize Requirement acceptance, Feature start, ADR acceptance, code execution, or Git actions. Requirement lifecycle, ADR acceptance, Feature Spec, Plan/Execute, submit, commit, push, release, and publish keep their own gates.

## Source Preservation And Append-Only Follow-up

Before Requirement Record / Archive, keep the draft response-local. At the gate, disclose the exact Requirement Set path, original files/references, generated `product.md`, README pointer, and unchanged sources. Only the confirmed scope may be written.

For a new material package, use `sources/` only when human files must be copied. Do not create an empty directory. Existing sources at Requirement Set root remain valid and are not moved automatically.

After a confirmed Product Definition is recorded, a material semantic change is append-only:

```text
product.md
YYYY-MM-DD-product-follow-up-<slug>.md
README.md -> Effective Product Definition -> current source
```

Preserve `Previous Source` and review evidence. If the goal, core rule, or acceptance direction is no longer recognizably the same Requirement, create a linked/superseding Requirement Set after Human Review. Never maintain two effective pointers in one README.

## PRD Helper Adapter Boundary

Available brainstorming or PRD helpers may improve discovery and drafting inside Requirements Discussion. Agent Loop remains the controller:

- translate helper output into the local Brief or Standard `product.md` draft;
- map a helper “Feature List” to Product Capability Scope, not Agent Loop Feature workspaces;
- write only through the Requirement Record / Archive Gate;
- keep technical architecture, database/API schema, tests, tasks, and plans out of product meaning;
- do not let the helper choose Profile, lifecycle, stage, or Product Review result;
- do not create native `feature_list.md`, `PRD.md`, Feature `product.md`, prototype deployment, or helper-owned output trees;
- do not install, publish, deploy, or call paid/external services without their own explicit authorization.

## Archify Scoped Confirmation

Archify is an optional derived-view method. Before each generation, disclose:

| Field | Required disclosure |
|---|---|
| Type | workflow, lifecycle, sequence, relationship, or equivalent |
| Source | exact effective `product.md` and stable IDs |
| Output | exact Requirement Set `visuals/` path |
| Review use | the product question the view helps the human inspect |
| Alternative | Markdown, table, Mermaid, or no visual |

Generate only after the human confirms that exact scope. Record source IDs, Product Semantic SHA-256, generation evidence, `Status: current`, and Human confirmation. A changed effective Product Definition makes the prior digest stale; do not present it as current until regenerated and reconfirmed. A derived view cannot introduce a product rule absent from the source.

Archify unavailable does not block Product Human Review. Use Markdown, tables, Mermaid, or another human-confirmed equivalent; do not install or sync a Skill merely to complete this method.

## Downstream Product Slice Handoff

After Product Review and Requirement lifecycle gates pass, run Design Readiness. ADR consumes the Effective Product Definition and owns only technical landing. Feature `spec.md` then records:

- Requirement Set path;
- Effective Product Definition path;
- Product Definition Profile and review evidence;
- Applicable Decisions;
- a Product Slice mapping source sections/IDs to Feature responsibility, acceptance, and coverage.

The Product Slice can narrow implementation scope but cannot rename, reverse, or locally redefine accepted product meaning. Out-of-scope items keep a visible Requirement Phase, another Feature, accepted Decision, or concrete not-applicable owner.

## Legacy Compatibility

Existing Requirement `requirement.md`, README `Effective Concept Foundation`, and Feature `product.md` remain readable during Resume, Follow-up, Review, Close, Recovery, and historical inspection. Do not bulk migrate, delete, rename, or synthesize a second effective source.

New work writes Requirement `product.md`. If legacy sources conflict or cannot be resolved uniquely, stop for Recovery / Requirement Conflict Review rather than guessing or rewriting history.

## Stop Rules

Stop before downstream work when:

- Brief eligibility is uncertain;
- human sources conflict with accepted product meaning;
- a draft would overwrite a human original;
- a product-semantic blocker remains;
- Product Review is not confirmed;
- two effective source pointers exist or the pointer is stale;
- a Product Slice references unknown/stale meaning or redefines the source;
- a derived visual is unconfirmed, unbound, or stale;
- a helper tries to create native artifacts, deploy, publish, or bypass a gate;
- safe legacy reading would require destructive migration;
- the change would introduce an unapproved profile, stage, message intent, lifecycle, stable ID family, executable schema, dependency, version change, or Git/release action.

Human urgency or an explicit request to continue does not bypass Product Human Review for a new Effective Product Definition. If no new product meaning exists, reclassify through the normal Bug or Lightweight eligibility rules; otherwise keep the minimum Brief/Standard draft in Requirements Discussion until confirmed.

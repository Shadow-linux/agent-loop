# Human-Guided Branch Management

Use this reference when existing branch rules are unclear, the target release is ambiguous, a customer boundary is at risk, or the human explicitly asks how to manage release branches. This is an optional Agent Loop profile, not mandatory Git Flow and not a canonical stage.

## Purpose And Optionality

Human-Guided Branch Management separates long-lived release aggregation from temporary development work while preserving project-native policy and Human Gates.

Use the profile only after evidence review and explicit human adoption. If a project already has a clear, human-maintained branch strategy with no material release or customer-isolation risk, record and follow that strategy as `Profile: existing-project`. If one maintained branch is sufficient and there is no release aggregation or customer line, the human may confirm `Adoption Status: not-needed`.

Do not force a project to rename existing branches, create release branches, or migrate its workflow merely because this reference is available.

A Lightweight Execution Card authorizes no branch action.

When the lane applies, still check an adopted strategy, Target Release Context, sealed-release state, customer isolation, and current Git reality as needed. The card's `Git Context` is evidence for its current branch and full HEAD only; it never proves another branch or release has the fact. The card cannot create, switch, merge, delete, push, or tag a branch and cannot satisfy Branch Action or Cleanup Gate.

An accidentally interrupted card may resume only after its branch, full HEAD, and dirty diff are revalidated with Scope/Plan/progress. Planned branch-to-branch continuation, worktree handoff, Subagent execution, or durable cross-session coordination remains Feature work.

## Evidence And Fact Precedence

Resolve branch policy in this order:

```text
human-confirmed native repository policy
-> accepted project.md Branch Strategy snapshot
-> current local and remote Git reality
-> Agent inference from branch names
```

Native policy includes human-maintained `CONTRIBUTING.md`, root `AGENTS.md`, release documentation, or another explicit project source. Git reality proves what currently exists; it does not by itself prove the allowed merge direction or release policy.

If these layers conflict, report the exact drift and recommend one smallest next action. Do not silently rewrite `project.md`, rename branches, or choose a merge target from name inference alone.

## Branch Strategy Check

Branch Strategy Check is an internal method used inside Project Entry, Project Entry Scan, Technical Design / Code Context, Plan Gate, Execute Task / Story, Drift Check, Project Memory Update, and Submit / Integrate. It does not add a canonical stage.

Run the check when any of these signals appears:

- multiple long-lived release branches exist without a maintained policy;
- a formal version contains multiple features or work items;
- the human introduces a customer-specific release;
- feature, bugfix, or hotfix work has no unambiguous Target Release Context;
- the current development branch does not match the intended aggregation target;
- a released version still appears to accept new work;
- customer code may flow into `main` or a standard release branch;
- multiple branches or worktrees lack stable release context;
- a branch name cannot uniquely identify work type, customer, and target version;
- the human asks about branch maintenance, release tracks, or customer versions.

Do not expand the check into a migration recommendation when:

- native policy is clear, maintained, and safe;
- the project uses one main branch and has no version aggregation or customer line;
- the human asks only for basic Git explanation in chat;
- evidence is insufficient to distinguish current reality from intended policy.

## Recommendation And Strategy Adoption Gate

Before recommending the profile:

1. inspect available native policy, project memory, current branch, relevant refs, and target-feature context;
2. state the observed fact and concrete risk;
3. recommend either `existing-project` or `human-guided-release` with the expected impact;
4. ask exactly one blocking question needed to resolve adoption, target version, or customer boundary.

Example shape:

```text
Current state: feature/user-login has no target version and both a standard and customer release exist.
Recommendation: adopt human-guided-release and bind this work to one Target Release Context.
Blocking question: should this work target release/v1.0.0 or customer/acme/v1.0.0?
```

The Strategy Adoption Gate records one human-confirmed result:

```text
Adoption Status: accepted | declined | not-needed
Profile: existing-project | human-guided-release | not-applicable
```

- `accepted`: record the complete actual strategy, scope, confirmer, date, and evidence.
- `declined`: record `Profile: not-applicable` and a concrete decline reason; do not copy the recommended profile as current policy.
- `not-needed`: record why the project remains lightweight so future Agents do not repeatedly recommend migration.

An unanswered recommendation stays response-local or in feature evidence. It must not be recorded as `accepted`.

Recommendation and adoption do not authorize branch creation, switching, merge, deletion, push, tag, release, or publish.

## Branch Classes And Naming Grammar

### Main Branch

The actual standard product main branch is durable and customer-neutral. Record its real name, such as `main` or `master`; do not force a rename.

### Release Aggregation Branches

Release aggregation branches identify a version, not an individual work topic:

```text
standard: release/v<semver>
customer: customer/<customer>/v<semver>
```

Examples:

```text
release/v1.0.0
customer/acme/v1.0.0
```

They are long-lived and retained for audit and maintenance. They never add a topic segment.

### Development Branches

Temporary development branches identify work type, Target Release Context, and one reviewable topic:

```text
standard: <work-type>/v<semver>/<topic>
customer: <work-type>/<customer>-v<semver>/<topic>
```

Allowed first-version work types:

```text
feature | bugfix | hotfix
```

Examples:

```text
feature/v1.0.0/user-login
bugfix/v1.0.0/login-timeout
hotfix/v1.0.1/login-security
feature/acme-v1.0.0/custom-login
bugfix/acme-v1.0.0/custom-timeout
hotfix/acme-v1.0.1/custom-security
```

`customer` and `topic` use stable lowercase kebab-case. A customer context is parsed from the final `-v<semver>` boundary; everything before it belongs to the customer slug. `topic` contains no additional `/`.

Invalid profile examples:

```text
release/v1.0.0/user-login       # release branch wrongly contains a topic
feature/user-login              # target release is missing
customer/acme/user-login        # customer version is missing
feature/v1.0.0/acme/custom-login # topic contains an extra path segment
```

An existing project may use another confirmed grammar. Record it as `existing-project`; do not silently rename branches to this profile.

## Target Release Context

Target Release Context connects a temporary development branch to exactly one aggregation target:

| Target Kind | Context | Unique Target Branch |
|---|---|---|
| standard | `vX.Y.Z` | `release/vX.Y.Z` |
| customer | `<customer>-vX.Y.Z` | `customer/<customer>/vX.Y.Z` |

The human decides the target version and how many development branches the version contains. One work item may use one development branch; a large version may use many. Agent Loop never creates extra branches to satisfy a quota.

When an adopted Branch Strategy or versioned/customer delivery applies, if Target Release Context or the unique Target Branch is unclear, stop dependent Plan, Execute, or Submit work, show evidence, recommend one target, and ask exactly one blocking question. A confirmed simple `not-needed` path is outside this requirement.

## Release Aggregation Lifecycle

```text
proposed
-> open
-> aggregating
-> release-candidate
-> released / sealed
-> retained

proposed | open | aggregating | release-candidate
-> abandoned only after human decision
```

- `proposed`: recommended but not created or human-confirmed.
- `open`: human confirmed the target release; branch creation remains a separate Long-Lived Branch Gate.
- `aggregating`: one or more matching development branches are being integrated.
- `release-candidate`: intended scope is aggregated and awaiting verification, review, drift, and Release Gate.
- `released / sealed`: formal release is immutable and accepts no more work for the same version.
- `retained`: release branch and release marker remain available for traceability.
- `abandoned`: human cancelled an unreleased target; deletion or cleanup remains separately gated.

Lifecycle evidence does not authorize any Git mutation.

## Development Branch Lifecycle

```text
proposed
-> active
-> review-ready
-> merged
-> deleted

active -> blocked -> active

proposed | active | blocked | review-ready
-> abandoned
-> deleted only after human confirmation
```

Feature and Task lifecycle remain authoritative for product work. A branch lifecycle never marks a Feature or Task complete and never replaces spec, tests, verification, review, drift, or close evidence.

## Standard Release Flow

1. Select a human-confirmed standard baseline and target version.
2. Use `release/vX.Y.Z` as the standard release aggregation branch when the profile is accepted.
3. Let the human decide scope and development-branch slicing.
4. Bind each standard development branch to the same version and only its matching release target.
5. Require fresh verification, Review, Drift Check, and the existing submit/release Human Gates before integration or release.
6. After formal release, mark the version `released / sealed`, retain its release branch, and synchronize only verified customer-neutral capability to the standard main branch through the separately approved integration action.
7. Recommend cleanup of merged temporary branches, then stop at the Cleanup Gate before local or remote deletion.

## Customer Release Flow And Isolation

1. The human selects a verified standard version as the customer baseline.
2. Use `customer/<customer>/vX.Y.Z` as that customer's release aggregation branch when accepted and separately created.
3. Bind every customer development branch to the matching customer and version.
4. Integrate customer development work only into its unique customer release branch.
5. Verify and release the customer version independently through existing Human Gates.
6. Retain the customer release branch; cleanup temporary customer branches only after merge/abandon evidence and Cleanup Gate confirmation.

Customer Isolation is required for the recommended profile:

- customer-specific code must not enter `main` or a standard `release/*` through a wholesale reverse merge;
- one customer's code must not enter another customer's release line;
- a matching topic across customers does not make their Target Release Context interchangeable;
- a customer baseline upgrade is an Upgrade Gate decision, not an automatic consequence of a new standard release.

If a customer implementation appears generally valuable:

```text
customer evidence
-> Human Product Decision
-> standard Requirement / Feature or Bug Flow-back
-> standard development branch
-> standard release
```

Do not use the existence of customer code as permission to merge the customer branch wholesale into the standard product.

## Sealed Release And Later Maintenance

A formally released version is immutable:

```text
v1.0.0 released / sealed
```

Later work uses a new human-confirmed version:

| Change | Recommended target |
|---|---|
| ordinary repair | `bugfix/v1.0.1/<topic>` -> `release/v1.0.1` |
| urgent repair | `hotfix/v1.0.1/<topic>` -> `release/v1.0.1` |
| new capability | `feature/v1.1.0/<topic>` -> `release/v1.1.0` |

Patch, minor, or major choice belongs to the human. Agent may recommend one with compatibility evidence but may not reopen `release/v1.0.0` or silently select the next number.

## Existing Strategy And Simple-Project Paths

For a clear native strategy:

```text
Adoption Status: accepted
Profile: existing-project
Evidence: CONTRIBUTING.md or another maintained policy plus human confirmation
```

For a simple project:

```text
Adoption Status: not-needed
Profile: existing-project
Reason: one maintained branch, no release aggregation, and no customer release line
```

These paths preserve Branch Strategy Check evidence without forcing release or customer branches.

A simple `not-needed` path does not require Target Release Context or Target Branch and must not block normal non-versioned work.

## Current Branch Context

For the current execution unit, record:

```text
Branch Class: main | standard-release | customer-release | development | unknown
Work Type: feature | bugfix | hotfix | not-applicable
Target Kind: standard | customer | not-applicable
Target Version: vX.Y.Z | not-applicable
Customer Slug: <customer> | not-applicable
Topic: <topic> | not-applicable
Source Branch:
Target Branch:
Lifecycle State:
Source Evidence:
Last Checked:
Human Decision:
```

Recheck the context before execution and submit when Git reality, target scope, or strategy evidence changed. `unknown` is a fail-closed value for dependent integration/release work when an adopted strategy or versioned/customer delivery applies. It does not turn a confirmed simple `not-needed` path into versioned delivery.

## Artifact Ownership

`project.md` stores durable, human-confirmed strategy:

```text
Adoption Status
Profile
Main Branch
Standard Release Pattern
Customer Release Pattern
Development Pattern
Release Immutability
Customer Isolation
Deletion Policy
Human Confirmed
Evidence
```

Its Current Work section stores only the active feature and current Target Release Context pointer.

Feature `notes.md` owns complete volatile Current Branch Context and decision evidence. The active `plan.md` cites that evidence and the target. Submit / Integrate records the checked source/target, boundaries, requested action, explicit authorization, and cleanup result.

Do not create a default `.agent-loop/branches/` directory.

No branch record replaces Requirement, Product Brief, Feature Spec, Decision / ADR, Delivery Contract, Test, Review, Drift, or lifecycle authority.

## Human Gates And Authorization Boundaries

| Gate | Human confirms |
|---|---|
| Strategy Adoption Gate | optional profile, existing strategy, decline, or not-needed result |
| Release Scope Gate | target version and human-selected work slicing |
| Customer Scope Gate | customer slug, standard baseline, and customization boundary |
| Long-Lived Branch Gate | creation of a specific release or customer branch |
| Branch Action Gate | creation or switching of one exact development branch |
| Target Branch Gate | one development branch's unique aggregation target |
| Integration Gate | exact commit, PR, merge, or integration action and scope |
| Cleanup Gate | exact local/remote temporary branches to delete |
| Release Gate | exact tag, push, release, publish, and sealed transition |
| Upgrade Gate | whether a customer moves to a new standard baseline/version |

Each gate is action- and scope-specific. A previous answer may satisfy another gate only when one Human Review Summary explicitly disclosed every combined action and the human confirmed the combined bounded scope.

Auto modes and external branch helpers do not cross these gates.

## Stage Integration

- Project Entry / Project Entry Scan: inspect evidence, classify optionality, and recommend only when triggered.
- Technical Design / Plan Gate: when an adopted Branch Strategy or versioned/customer delivery applies, resolve accepted strategy, Target Release Context, target branch, sealed status, and customer boundary before dependent work; otherwise record branch-specific checks as `not-applicable`.
- Execute Task / Story: recheck recorded context; branch creation or switching is never an implied execution step and requires its own Branch Action Gate.
- Drift Check: compare native policy, accepted strategy, feature context, and Git reality; strategy changes require Human Review.
- Project Memory Update: persist accepted/declined/not-needed durable results only after confirmation.
- Submit / Integrate: load this reference when triggered or adopted; apply branch-specific fail-closed conditions only to an adopted strategy or versioned/customer delivery, record them as `not-applicable` for a confirmed simple path, show the exact requested action, and ask the applicable Human Gate.

## Fail-Closed Conditions

Stop dependent integration/release work only when an adopted Branch Strategy or versioned/customer delivery applies and:

- Branch Class is `unknown`;
- Target Release Context or Target Branch is missing or non-unique;
- customer development work lacks a customer slug;
- current source/target conflicts with the human-confirmed strategy;
- the target release is `released / sealed`;
- customer code would enter main, standard release, or another customer line without a separate product/generalization decision;
- native policy conflicts with the recommended or recorded profile;
- required verification, Review, Drift Check, or Human Gate is missing;
- unrelated dirty work may be included;
- worktree ownership of source/target is unclear;
- branch creation, switch, merge, deletion, push, tag, release, or publish lacks exact authorization.

Report the conflict, evidence, and one smallest next action. Never bypass by force, rename, rewriting a sealed version, or treating adoption as mutation permission.

## Scope Exclusions

Bug Management owns Bug identity, lifecycle, and Resolution Path. Branch Management consumes only the Human-confirmed Fix Feature and Target Release Context.

`bugfix` and `hotfix` express branch work type only. Severity, Priority, Report Origin, Bug confirmation, accepted Requirement, Resolution Path, plan acceptance, and Auto Mode do not select a work type, create a patch context, or authorize a Git mutation. A sealed release remains immutable; any repair uses a separately human-confirmed new patch Target Release Context. Customer Origin does not infer a customer repair line; customer isolation is decided from confirmed scope and release context.

This capability does not implement Post-Merge Memory Reconciliation. It provides Source Branch, Target Branch, Target Release Context, Customer Boundary, lifecycle, and allowed direction to `memory-reconciliation.md`. Memory Reconciliation completion is evidence for later independent Git gates; it does not adopt a strategy, perform a Git action, authorize Source cleanup, or permit customer-specific memory/code to leak into `main` or a standard release.

It also does not add a branch database, executable YAML/JSON schema, branch-protection configuration, CODEOWNERS, automatic scheduling, or any automatic Git mutation.

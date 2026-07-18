# Post-Merge Memory Reconciliation

Use this reference only after code integration has produced a stable verified commit and Agent Loop memory may differ across Base, Source, Target-before, and Result. It is an internal Submit / Integrate method, not a canonical stage or message intent.

## Purpose And Boundary

Post-Merge Memory Reconciliation rewrites the Target memory root into the correct semantic state after code has already been merged. It reconciles facts and artifact ownership; it is not Markdown conflict resolution.

```text
Code Merge Complete
-> Scan
-> Fact Reconciliation
-> Desired Target Memory
-> Exact Rewrite Plan
-> Human Review
-> Apply
-> Post-check
-> Restore on failure
```

Memory Reconciliation does not perform the code merge.

Change files are evidence only after code merge is complete and verified. Their source-branch Memory Result, including `synced`, never instructs Target memory to overwrite itself.

It does not create, switch, merge, delete, push, or tag branches; create commits or PRs; release or publish; modify production; or authorize a later Git action. It changes only the accepted Target memory root after its own Human Gates.

## Entry Preconditions

Enter only when all of the following are known and evidenced:

- the code merge is complete at one stable, full Merged Code SHA and `HEAD` resolves to it;
- code verification for that result has completed and its bounded evidence is available;
- full Merge Base, Source, Target-before, and Merged Code SHAs are available;
- Source Branch, Target Branch, Target Release Context, and Customer Boundary are known;
- exactly one existing memory root, `.agent-loop/` or confirmed legacy `agent-loop/`, is accepted;
- Source and Target evidence remain readable; Source branch cleanup has not occurred;
- the human has passed the Start gate before a report directory or report is created.

If a precondition is absent or ambiguous, stop in Recovery. Do not infer a SHA, migrate a memory root, or manufacture missing branch evidence.

## Target Canonical Memory Spine

The **Target Canonical Memory Spine** is the actual Target branch's current artifact ownership, `project.md`, enterprise indexes, stable identities, and canonical locators. It determines scan order and the Target output structure baseline.

The spine is neither a fact priority nor a path allowlist. Source-only artifacts, new artifact families, absent paths, unchanged files, directories, and unknown paths are still accounted. Target claims remain claims until checked against the authority for the question being answered.

## Four Snapshot Claims

Every run records four snapshots with exact keys:

```text
base | source | target_before | result
```

- `base`: common history used to distinguish inherited facts from branch changes.
- `source`: Source branch memory and code claims before integration.
- `target_before`: Target branch memory and code claims before integration.
- `result`: merged-code worktree memory and project reality at the Merged Code SHA.

Git trees provide Base, Source, and Target-before. The current worktree provides Result so unresolved or already-written memory changes are visible. Each claim is evidence, not a winner selected for all questions.

## Path Accounting Ledger

The **Path Accounting Ledger** covers every memory-root-relative path found in any snapshot, including directories, regular files, symlinks, gitlinks, unchanged rows, and meaningful absence. Each row records:

- safe POSIX path and path kind;
- presence and SHA-256 for all four snapshots;
- semantic role and stable identity when known;
- selected Chinese action, attention level, authority/evidence, and rationale;
- matching operation ID when bytes must change;
- expected post-state and blocker details.

Paths must be relative POSIX text. Reject absolute paths, `.` or `..` components, backslashes, NUL, drive prefixes, symlink traversal, and casefold or Unicode-normalization collisions. Directory rows support accounting but never receive file rewrite operations. An unclassified path is visible and blocking until the Agent resolves its role or the human accepts a bounded `暂不处理` during review; a ready Apply plan cannot contain `暂不处理`.

Inventory `<memory-root>/changes/YYYY-MM/YYYY-MM-DD-<topic>.md` paths across Base, Source, Target-before, and Result like every other memory-root path. Classify each by its actual content and authority. A completed card is execution evidence/current evidence; it is not an accepted Requirement, ADR, project-memory fact owner, Target overwrite instruction, or automatic import request.

## Semantic Artifact Roles

The role vocabulary is exactly:

```text
human-source | accepted-authority | append-only-evidence | current-semantic-state | derived-index | validated-package | transaction-temporary | unclassified
```

- `human-source`: original requirement, prototype, feedback, screenshot, recording, or other human-supplied material. Preserve bytes; only retain or import.
- `accepted-authority`: accepted Requirement meaning, ADR, or explicit durable Human Decision. Preserve meaning and history; replace only through a separately accepted superseding artifact.
- `append-only-evidence`: histories, close/reopen records, verification or submit evidence whose earlier bytes/events must not disappear.
- `current-semantic-state`: Agent-maintained present-tense facts such as Current Work, current capability, lifecycle projection, environment claim, or locator target.
- `derived-index`: inventory, locator, mapping, or summary rebuilt from canonical owners.
- `validated-package`: package members whose content and manifest identity must remain coherent, such as a validated Project Skill.
- `transaction-temporary`: report-local journal and backups used only during Apply/Post-check/Restore.
- `unclassified`: discovered content whose owner or semantics are not yet proven. It blocks readiness.

Directory names and filename patterns are hints only. The Agent owns the semantic classification by reading the artifact and its referenced authority.

## Fact Authority By Question

There is no global source precedence. Use the authority that owns the question:

| Question | Primary authority | Required check |
|---|---|---|
| What did the human originally ask for? | immutable human source | byte identity and archive provenance |
| What product behavior is accepted? | effective accepted Requirement / PRD and Human Decisions | accepted status, stable IDs, supersession |
| What technical decision is accepted? | accepted ADR | dependency snapshot, supersession, current applicability |
| What is implemented now? | merged code, tests, config, generated/runtime evidence | Merged Code SHA and verification evidence |
| What is currently active or closed? | canonical lifecycle owners plus implementation evidence | cross-artifact invariant and dates/evidence |
| Where is an artifact located? | canonical artifact plus rebuilt locator/index | filesystem identity and stable ID |
| What is the environment truth? | bounded current environment evidence and accepted runbook/policy | freshness, scope, customer boundary |

Code can prove implementation reality; it cannot by itself prove product correctness. When implementation conflicts with accepted Requirement, ADR, or Human Decision, keep the accepted authority intact and raise the conflict for Human Review.

## Desired Target Memory

The Agent derives one **Desired Target Memory Snapshot**:

```text
Desired Target Memory
= merged code / test / config reality
+ immutable human sources
+ accepted product / technical decisions
+ valid Source and Target history
+ Target-appropriate current state
+ rebuilt derived indexes and locators
```

This is a semantic target, not concatenated Markdown. Source and Target artifacts may be retained, introduced, rewritten, recalculated, or have stale Agent-maintained claims removed according to ownership and facts. Branch-local Current Work is not automatically promoted to the Target. Customer-specific meaning remains isolated from the standard product line.

## Attention And Chinese Actions

Human attention has only three levels:

- `🔴`: facts cannot determine one safe outcome; the human must decide before a ready plan.
- `🟡`: the Agent has a recommended outcome but impact or confidence merits grouped review.
- `🟢`: fact-determined and summarized; no item-by-item decision is requested.

Actions are exactly:

```text
保留 | 引入 | 重写 | 重算 | 移除过时声明 | 暂不处理
```

`保留` creates no operation. `暂不处理` may describe a draft blocker but is forbidden in a ready plan. `引入` requires an absent Result preimage and a present postimage; `重写` requires an existing regular-file Result whose exact hash is the operation preimage; `重算` produces a present derived file from either an absent Result or that exact existing preimage; `移除过时声明` requires an exact existing preimage and an absent post-state. The checker rejects an action label whose actual mutation does not match these semantics.

Original human sources and accepted authorities permit only `保留 | 引入`. Their `引入` operation must copy a same-path `100644 | 100755` Git blob byte-for-byte from one recorded snapshot; inline payloads, trees, symlinks, path substitution, and overwrite-shaped imports are forbidden. Append-only evidence permits `保留 | 引入`; a generated append file may use `重写` only if the full preimage is preserved and the checker proves a strict append. `derived-index` uses `重算` when bytes change. `移除过时声明` applies only to current or derived Agent-maintained content.

## Memory Merge Report

For one Merged Code SHA, create on demand exactly one durable report at:

```text
<memory-root>/memory-merges/MM-<collision-safe-merged-code-short-sha>/README.md
```

Start with 12 lowercase SHA characters and extend one character at a time when an existing ID records a different full SHA. Reuse the existing report when its recorded full SHA is identical; a second report directory for the same full SHA fails closed before Apply. Never rename an older report. Do not create `memory-merges/` during Init Project or Project Entry.

Report statuses are exactly:

```text
待确认 | 已完成 | 已恢复
```

The report is the audit owner for Merge Context, four-snapshot inventory, Path Accounting Ledger, attention, Human Decisions, exact operations, normalized Plan Hash, expected unchanged paths, Apply evidence, post-check, restore, and remaining risk. It is not a project encyclopedia, Bug backlog, Feature execution system, or authority that replaces its cited artifacts.

## Scan

The read-only scanner:

1. resolves every input SHA to a full commit, requires `HEAD == merged_code_sha`, and rejects blank Source Branch, Target Branch, Target Release Context, or Customer Boundary values;
2. locates exactly one accepted memory root and refuses implicit root migration;
3. inventories all four snapshots, with full path kinds and hashes;
4. uses the Target Canonical Memory Spine for traversal order, not coverage;
5. excludes only the current report directory and its transaction data from Result business-memory comparison;
6. emits deterministic, sorted JSON with role hints, blockers, snapshot hashes, `scan_sha256`, and optional zero-change comparison;
7. performs no writes.

The Agent then deep-reads changed or affected records plus the canonical owners and references necessary to decide their meaning. Scan output is mechanical evidence, not the semantic decision.

When Change paths are present, re-run the dedicated read-only Lightweight Change scanner for the Result root, include pending and human-review inventory in the reconciliation evidence, and re-check every Source `synced` fact against Merged Code, Target context, accepted authorities, and the Target Canonical Memory Spine. Do not change the existing reconciliation report identity, Start gate, exact Plan Hash, transaction, Apply, post-check, restore, Memory Commit, Push, Release, or cleanup sequence.

## Fact Reconciliation

For every ledger row, the Agent:

1. identifies artifact identity and semantic role;
2. asks the ownership-specific fact question;
3. checks the applicable code, test, config, environment, product, governance, Requirement, ADR, Git, and Human Decision evidence;
4. distinguishes inherited, Source-only, Target-only, jointly changed, stale, duplicated, and derived claims;
5. proposes one action, attention level, intended post-state, and evidence-backed rationale;
6. exposes unresolved ambiguity rather than guessing.

Scripts may inventory, hash, validate, apply, and restore. They do not decide product meaning, accepted behavior, environment policy, governance, requirement compatibility, ADR intent, customer boundaries, or human choices.

## Exact Rewrite Plan And Plan Hash

The ready plan uses schema version `1` and records report identity, Merge Context, scan hash, the complete ledger, ordered rewrite operations, expected unchanged paths, Human Decisions, post-check expectations, and `plan_sha256`.

Each operation has one ledger owner and one safe relative file path. It records sequence, action, exact preimage SHA-256 or absence, exact postimage SHA-256 or absence, output mode, and a bounded content source. Content is either validated inline base64 (2 MiB per file, 8 MiB total) or a file blob from one recorded snapshot SHA. It cannot be a command, hook, URL fetch, shell expression, or arbitrary filesystem copy.

CLI JSON, PASS, and error output is UTF-8 regardless of the host console code page. On filesystems with POSIX executable bits, `100644` and `100755` remain distinct and are verified exactly. Native Windows cannot represent that executable-bit distinction in the worktree, so those two modes are equivalent only while checking the mode of an already-proven regular file; bytes, SHA-256, path, file kind, Git source mode, operation identity, and every other transaction invariant remain exact. `120000`, `160000`, directories, and other kinds never become mode-equivalent.

The normalized Plan Hash is SHA-256 over canonical UTF-8 JSON excluding only `plan_sha256`. The checker recomputes it. Every changed row that needs bytes has exactly one operation, every operation has exactly one row, expected unchanged paths are hashed, and no ready plan contains unresolved red items, blockers, unclassified content, or `暂不处理`.

## Human Review

There are two gates:

1. **Start**: before report creation, show merge identity, evidence availability, memory root, expected scope, customer/release boundary, and explicitly unauthorized Git actions. The human authorizes only creation of this report and read-only reconciliation work.
2. **Exact Rewrite Plan**: after facts are reconciled, show 🔴 decisions, grouped 🟡 reviews, 🟢 summary, every add/update/remove path, expected unchanged paths, normalized Plan Hash, semantic post-check, restore scope, and unauthorized Git actions. The human authorizes only that exact hash.

The Agent checks evidence, narrows choices, and gives a recommended decision before asking one blocking question. Changed evidence or plan bytes invalidate the old confirmation and require a new Plan Hash review.

## Apply

Apply accepts only the exact human-confirmed Plan Hash and a fresh successful pre-apply check. It rejects stale snapshots, unexpected dirty paths, unsafe paths, unresolved attention, incomplete accounting, prior success, or an existing unresolved transaction.

Before changing business memory, create a report-local transaction journal and exact backups. Apply operations in numeric order using atomic writes without symlink traversal. While machine and semantic checks are pending, keep the report `待确认` and the journal in checking state.

Memory Reconciliation scripts never execute commands or hooks stored in a report or memory artifact.

The Agent runs bounded domain/semantic verification separately and records the commands or procedures and their actual evidence in the report. Only finalize can mark the report `已完成`, after fresh post-apply validation proves the exact Plan Hash, evidence block, expected tree, expected unchanged paths, and zero-change result.

## Global Post-check

Post-check is not limited to changed files. It proves:

- the current HEAD and Merge Context remain identical;
- a repeat scan against the report yields zero business-memory changes;
- every path has the expected bytes, mode, kind, identity, and references;
- unchanged paths still match their pre-apply hashes;
- human sources, accepted authorities, append-only evidence, and validated packages retain their invariants;
- derived indexes and locators match canonical artifacts;
- no unresolved 🔴, `暂不处理`, unclassified path, broken reference, duplicate stable ID, stale current-state claim, or customer-boundary leak remains;
- recorded domain/semantic verification succeeded;
- transaction payload cleanup is safe.

Machine checks prove deterministic structure and bytes. The Agent remains responsible for semantic evidence and must not claim product correctness from hashes alone.

## Restore And Recovery

On Apply or post-check failure, restore only this run's memory operations in reverse order from verified backups. Prove original bytes, modes, absence, and unchanged-path hashes before removing transaction payloads. Record failure and restore evidence, then set the report to `已恢复`. If a process exits after the journal reaches internal `restored` but before report-status update or transaction cleanup, the same Restore command revalidates the restored tree and idempotently finishes only those remaining steps.

Restore does not run `git reset`, roll back merged code, alter unrelated dirty work, or perform branch actions. If identity, journal, backup scope, or restored hashes cannot be proven, retain the transaction and stop in Recovery. A failed or incomplete restore blocks all later Apply and Git actions.

## Single Successful Apply

One full Merged Code SHA has one durable report and at most one successful Apply. After `已完成`, Apply and replay are forbidden. Finalize may only resume or clean up the same verified transaction; it never reapplies operations. A completed report without its own verified residual transaction rejects Apply and Finalize replay.

A successful result must be idempotent in observation: scanning again for the same report and Merge Context reports zero change. New code integration creates a new full Merged Code SHA and therefore a new reconciliation identity.

## Git Gate Separation

The required order is:

```text
Code Merge Gate -> Post-Merge Memory Reconciliation -> Memory Commit Gate -> Push Gate -> Release Gate -> Source Branch Cleanup Gate
```

`待确认`, `已恢复`, an unresolved transaction, stale evidence, or missing report blocks memory commit, push, release/publish, and Source branch cleanup. `已完成` permits only presentation of the next independently authorized gate; it grants no commit, push, tag, release, publish, merge, branch deletion, or cleanup permission.

## Domain Ownership Boundaries

Reconciliation consumes existing ownership without redefining it:

- Requirement and PRD own product goals, accepted concepts, flows, states, and expected behavior.
- ADR owns accepted technical landing and compatibility; it cannot redefine Requirement semantics during reconciliation.
- Bug Record owns Bug identity, facts, evidence, lifecycle, Resolution Path, and closure; Feature owns code repair execution.
- Feature artifacts own work, verification, review, drift, and Submit evidence.
- Branch Management supplies accepted strategy and Merge Context; it does not perform reconciliation.
- Archive changes Feature location, never identity or ownership; locator rebuilding respects archived records.
- Project Skill manifests and bodies remain a validated package; reconciliation cannot silently mutate trust.
- `project.md` owns long-term/current pointers, not a copy of the report ledger or transaction.

Do not introduce new lifecycle states, canonical stages, message intents, artifact owners, or automatic policy changes through this method.

## Fail-Closed Conditions

Stop before write, or restore and stop after a partial write, when any of these occurs:

- HEAD, a recorded SHA, branch/release/customer context, memory-root identity, scan hash, Plan Hash, or report identity is missing or changed;
- Source/Base/Target-before/Result evidence is unavailable or cannot be read safely;
- an unaccounted, unsafe, colliding, symlink-traversing, gitlink, or unclassified path remains;
- ledger/operation cardinality, preimage/postimage, inline limits, content-source identity, expected unchanged path, or output mode fails validation;
- human source, accepted authority, append-only history, validated package, customer isolation, or ownership rules would be violated;
- the plan still contains a blocker, 🔴 item, `暂不处理`, or unrecorded Human Decision;
- the report is already `已完成`, is `已恢复` without a new reviewed plan, or has an unresolved transaction;
- unexpected dirty work overlaps the memory scope;
- machine post-check, Agent semantic verification, zero-change scan, or restore proof fails.

Report the exact evidence and the smallest safe next step. Never guess through a safety failure.

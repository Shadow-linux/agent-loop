# Post-Merge Memory Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use `executing-plans` to execute this plan task-by-task. Do not dispatch subagents unless the human separately authorizes one bounded dispatch. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the approved post-code-merge semantic reconciliation of Agent Loop memory so an Agent can use the actual Target memory as the primary scan spine, account for every Base / Source / Target / Result memory path, produce one Human-reviewed exact rewrite plan, apply it once, verify convergence, and restore safely on failure.

**Architecture:** Add one published `references/memory-reconciliation.md` procedure and four Python 3.10+ standard-library commands backed by one focused support module. The scanner inventories Git snapshots and the Result worktree without deciding product meaning; the Agent classifies semantic roles and writes the exact plan into the single durable Memory Merge Report; checker/apply/restore commands enforce complete path accounting, Plan Hash, preimages, bounded writes, transaction recovery, completed replay protection, and post-check convergence. Runtime/design remain the authority, and Memory Reconciliation stays an internal post-code-merge method of Submit / Integrate rather than a canonical stage.

**Tech Stack:** Markdown runtime/reference/template sources, Python 3.10+ standard library, Git CLI invoked without shell interpolation, `unittest`, Bash/Ruby focused contract assertions, existing checker/archive helpers where their contracts already fit, and the repository focused/full validation methods. No third-party package, database, service, merge driver, background daemon, or automatic Git action.

---

状态：Proposal / Implementation Plan 已批准；Task 0–11 与 Human Review 修复完成，待新的 Human Review
设计来源：`docs/proposal/v1.4.x/post-merge-memory-reconciliation.md`
计划日期：2026-07-16
计划基线：`alpha/v1.4.0` at `7eddf63`
实际执行日期：2026-07-17
实施证据：`docs/reports/post-merge-memory-reconciliation-feature-validation-2026-07-16.md`、`docs/reports/agent-loop-v1.4.0-post-merge-memory-reconciliation-full-validation-2026-07-16.md`

## Execution Constraints

- Work from the Agent Loop skill source-repository maintainer perspective.
- Do not create a repository-root `.agent-loop/` or simulate a target project outside isolated temporary test directories.
- Preserve all human-owned requirement sources, accepted Decision meaning, append-only history, unrelated workspace changes, and existing historical reports.
- Keep Skill version `1.4.0`; this plan does not authorize a version bump.
- Advance all 13 root managed blocks from `1.4.0-20260716` to `1.4.0-20260716.1` only when the approved one-line root routing reminder is added.
- Do not install or synchronize this source into Codex, Kimi Code, OpenCode, `.agents/skills/`, or any global Skill directory.
- Do not create/switch/delete a branch or worktree, merge code, tag, open a PR, release, publish, or modify external state.
- Do not stage, commit, push, merge, release, publish, or tag. Implementation completion leads to a separate Submit / Integrate Human Gate.
- Do not dispatch subagents without a new explicit human approval naming their tasks, files, stop conditions, and main-Agent review responsibility.
- Use `apply_patch` for manual source edits. Formatting-only commands may update mechanically generated output when their scope is already reviewed.
- Stop when an implementation file has unrelated overlapping dirty work, the branch/HEAD/version/root revision differs from the accepted baseline, a Proposal invariant cannot be implemented without redesign, or a test requires production/external access.

## Stage Helper Resolution

| Field | Resolution |
|---|---|
| Stage | Plan Gate / Plan |
| Canonical candidate | `superpowers:writing-plans` — not exposed by the current runtime |
| Alias candidate | `writing-plans` — loaded completely from `/Users/shaodowyd/.codex/skills/writing-plans/SKILL.md` |
| Status | `loaded` |
| Fallback | `no` |
| Method used | exact file responsibility map, interface/data contracts, bite-sized RED/GREEN tasks, exact commands, rollback and self-review |
| Agent Loop override | save beside the approved Proposal; no automatic worktree, subagent, implementation, commit, push, tag, release, publish, or target-project artifact |
| Persistence | response-local resolution recorded here because this source repository has no target-project Feature workspace |

## Observed Planning Baseline

- Branch: `alpha/v1.4.0`.
- HEAD: `7eddf63` (`fix(v1.4.0): 修复项目技能发现与回退顺序`).
- Skill/plugin/human version labels: `1.4.0`.
- Root managed-block revision: `1.4.0-20260716`, 13 blocks.
- Python baseline run on 2026-07-16: `98/98 PASS`.
- Shell baseline run on 2026-07-16: `37/37 PASS`.
- Dirty boundary at plan authoring: only the approved `docs/proposal/v1.4.x/post-merge-memory-reconciliation.md` was untracked before this plan was created.

The implementation Agent must re-run and record the live baseline. These counts are evidence, not permission to skip recounting.

## Non-Negotiable Invariants

1. Code integration completes first. Memory Reconciliation never performs, retries, reverts, or resolves the code merge.
2. The actual Target branch memory is the `Target Canonical Memory Spine`; `main` is used only when it is the real Target.
3. The Target spine controls scan order and output structure, not truth, authority, or coverage.
4. Base, Source, Target-before, and Result contribute Memory Claims. The Desired Target Memory is derived from applicable facts and accepted authority.
5. Every discovered memory path, including unchanged and absence claims, has its own Path Accounting Ledger row. A validated package may share one semantic judgment across its members, but it never hides their individual paths or hashes.
6. Directory names provide role hints only. Future/custom paths are classified from content, identity, owner, references, history, and rules; unresolved classification is 🔴 and blocks Apply.
7. Human original sources are preserved byte-for-byte or introduced byte-for-byte. They are never semantically rewritten by this capability.
8. Accepted Decision / ADR / Contract meaning is not changed in place. Implementation conflict is reported, not normalized into the decision.
9. Append-only Human Decisions, verification, Review, close/reopen history, and bounded evidence are never overwritten or dropped.
10. Derived Index / Locator / Mapping content is recomputed from canonical owners instead of text-merged.
11. Report attention is exactly `🟢 | 🟡 | 🔴`; report actions are exactly `保留 | 引入 | 重写 | 重算 | 移除过时声明 | 暂不处理`.
12. Human-visible report state is exactly `待确认 | 已完成 | 已恢复`. Internal journal states are implementation details and must not become new report lifecycle states.
13. One full Merged Code SHA identifies one report and permits at most one successful Apply. Completed replay is rejected.
14. Scan is read-only. Creating/updating the report requires Memory Reconciliation Start authorization. Apply requires confirmation of the exact Plan Hash.
15. The plan hash covers canonical JSON for Merge Context, scan snapshot hashes, every ledger row, every operation, Human Decisions, expected unchanged paths, and post-check expectations.
16. Apply modifies only exact planned paths inside the accepted memory root plus its current report/journal. It never changes business code, root guidance, Git refs, commits, remotes, or external systems.
17. Any preimage, SHA, decision, report plan block, branch context, customer boundary, or Target Release Context drift invalidates the reviewed plan. There is no force option.
18. Apply or post-check failure restores only this Memory Apply. Restore never uses `git reset`, rolls back code integration, deletes a branch, or removes unrelated work.
19. Memory Reconciliation must finish before push, release/publish, Source branch cleanup, or a claim that integration is complete.
20. The capability supports the accepted active memory root: `.agent-loop/` by default or existing legacy `agent-loop/`; simultaneous roots or implicit root migration fail closed.
21. Python code is standard-library-only, uses POSIX-normalized relative plan paths, rejects path/case/Unicode collisions, does not follow symlink parents, and runs natively on macOS and Windows.
22. CLI output is deterministic UTF-8. POSIX worktrees verify `100644` versus `100755` exactly; native Windows may treat only those two regular-file worktree modes as equivalent while keeping bytes, kind, Git source, path, identity, and transaction checks exact.
23. Proposal/report artifacts never become runtime authority. Published runtime/design/reference/template/test surfaces must agree before completion.
24. No Memory Reconciliation script executes a command, hook, validator, or code fragment stored in a report or memory artifact. The Agent runs semantic checks through the normal runtime/tooling boundary and records bounded evidence; scripts validate that evidence and deterministic filesystem/Git facts only.

## File Responsibility Map

### New Published Runtime And Template Files

- `references/memory-reconciliation.md` — canonical semantic procedure: entry, facts, Target spine, path accounting, role classification, report, gates, plan, apply, post-check, restore, recovery, and cross-capability boundaries.
- `templates/memory-merge-report.md` — one durable human report with three attention levels, three report states, Chinese action matrix, exact plan sentinels, results, and restore/risk sections.

### New Python Runtime Files

- `scripts/memory_reconciliation_support.py` — immutable data model, Git/tree/worktree inventory, memory-root resolution, path safety, plan/report parsing, canonical hash, validation, transaction apply/restore, and post-check primitives.
- `scripts/scan-memory-reconciliation.py` — read-only four-snapshot scan; emits canonical JSON inventory and optional post-Apply comparison against a report.
- `scripts/check-memory-reconciliation.py` — read-only `pre-apply | post-apply | restore` contract checker for a report and exact plan.
- `scripts/apply-memory-reconciliation.py` — exact-hash bounded apply with journal and automatic restore attempt on failure.
- `scripts/restore-memory-reconciliation.py` — standalone recovery for an interrupted/failed transaction.

### New Python Tests

- `tests/memory_reconciliation_test_support.py` — temporary Git repository builder, four-SHA merge fixture, command runner, report renderer, and byte-tree snapshot helper.
- `tests/test_memory_reconciliation_support.py` — root/path/tree/role/hash/report-plan unit contracts.
- `tests/test_memory_reconciliation_scan.py` — read-only Target-spine plus all-path inventory and post-Apply zero-change scan.
- `tests/test_memory_reconciliation_check.py` — full-ledger, semantic-role, immutable/append-only, plan-hash, unresolved, and post-check validation.
- `tests/test_memory_reconciliation_apply.py` — bounded writes, git-blob/inline content, stale plan, replay, failure injection, and auto-restore.
- `tests/test_memory_reconciliation_restore.py` — new-process restore, tamper/path safety, incomplete recovery, and report state.

### New Focused Contract And Reports

- `tests/validate-post-merge-memory-reconciliation.sh` — cross-surface positive/negative contract and canonical-order assertions.
- `.github/workflows/cross-platform-checkers.yml` — existing macOS/Windows and Python 3.10/3.x matrix extended with the five memory modules and four command entrypoints; CI definition is in scope, while a live remote Windows result remains separate evidence.
- `docs/reports/agent-loop-v1.4.0-post-merge-memory-reconciliation-red-baseline-2026-07-16.md` — preserved pre-implementation RED evidence.
- `docs/reports/post-merge-memory-reconciliation-feature-validation-2026-07-16.md` — five-domain focused score and pressure evidence.
- `docs/reports/agent-loop-v1.4.0-post-merge-memory-reconciliation-full-validation-2026-07-16.md` — six-domain full validation, final live test counts, issues, RED/GREEN evidence, and submission boundary.

### Core Authority Files To Modify

- `SKILL.md` — concise package-map entries, required routing, memory reconciliation stop conditions, and script inventory.
- `references/design.md` — Target Canonical Memory Spine, Desired Target Memory, semantic roles, authority boundaries, path-accounting and single-success invariants.
- `references/runtime.md` — post-code-merge entry inside Submit / Integrate, routing/precedence, Start and Plan Hash gates, blocker states, post-check/restore, and submit/cleanup restrictions.
- `references/concepts.md` — concise definitions without duplicating the procedure.
- `references/memory-reconciliation.md` — detailed owner of all procedure logic.

### Workflow And Ownership Files To Modify

- `references/artifact-rules.md` — Memory Merge Report ownership, current report identity, all-path accounting, immutable/append-only/derived rules, and no empty default directory.
- `references/project-memory-mode.md` — optional current report pointer, durable Target facts, simple/enterprise rewrite ownership, and report-detail exclusion.
- `references/branch-management.md` — replace future-input wording with actual consumer boundary; preserve independent Git action gates.
- `references/submit-and-integrate.md` — post-code-merge detection, report status blocker, Memory Commit Gate, push/release/cleanup ordering.
- `references/recovery-and-backfill.md` — distinguish ordinary stale-memory recovery from a known post-code-merge reconciliation with four SHAs.
- `references/stage-guides.md` — Submit / Integrate internal method and Recovery continuation.
- `references/workflow-checklists.md` — scan/plan/review/apply/post-check/restore checklists.
- `references/human-review-summary.md` — three attention levels, grouped red decisions, exact Plan Hash review, and explicit non-authorization.
- `references/external-skill-adapters.md` — finishing/Submit helpers cannot bypass reconciliation or inherit Git authority.
- `references/project-guidance.md` — one short downstream root routing reminder and managed-block refresh rule.
- `references/document-templates.md` — synchronize inline artifact-layout/report references with source templates.
- `references/validation-scenarios.md` — Proposal scenarios plus executable adversarial cases.

### Domain References To Review And Modify Only Where Needed

- `references/requirement-management.md` — original source and lifecycle/mapping authority boundary.
- `references/project-decisions.md` — accepted meaning/superseding-decision boundary.
- `references/delivery-contracts.md` — contract acceptance and breaking-change gates remain independent.
- `references/bug-management.md` — Bug verification/close and append-only history boundary.
- `references/feature-follow-up.md` — archived owner/rehydrate interaction and post-merge Source evidence.
- `references/project-skills.md` — validated package/manifest handling; merge never authorizes execution.
- `references/onboarding-knowledge-base.md` — targeted drift handling only; no full rewrite without evidence overlap.

Do not edit a domain reference merely to repeat generic memory rules. Add only the boundary needed to prevent an existing owner from being overridden.

### Human And Root Guidance Files To Modify

- `templates/root-AGENTS.md` — add one routing sentence only and advance all 13 managed blocks to `1.4.0-20260716.1`.
- `templates/project.md` — optional current Memory Merge Report pointer and blocker note; no matrix/detail copy.
- `README.md` — concise capability overview and link to Usage.
- `Usage.md` — human trigger phrases, lifecycle overview, and one Mermaid flow; no script-internals dump.
- `CHANGELOG.md` — v1.4.0 in-progress entry for the new capability and managed-block revision.

### Root-Revision Regression Files To Update Together

- `tests/test_root_agents_blocks.py`
- `tests/validate-root-agents-block-checker.sh`
- `tests/validate-root-agents-block-refresh.sh`
- `tests/validate-v1.2.4-root-stage-coverage.sh`
- `tests/validate-project-local-skills.sh`
- `tests/validate-requirement-lifecycle-backlog.sh`
- `tests/validate-branch-management-strategy.sh`
- `tests/validate-bug-management.sh`
- `tests/validate-project-skill-discovery-guard.sh`

Only update current-revision expectations. Historical proposal/report revision strings remain unchanged.

### Review-Only Unless A Contradiction Is Found

- `plugin.json` — remains `1.4.0`.
- `agents/openai.yaml` — metadata validation only.
- `templates/root-CLAUDE.md` — remains the short pointer to `AGENTS.md` unless the current template requires its revision reference updated.
- `examples/` — no mutation expected; temporary Git repositories provide executable coverage.
- Repository root `AGENTS.md` — maintainer policy already routes full validation and must not receive downstream runtime detail.

## Canonical Data Contract

Implement these frozen types in `scripts/memory_reconciliation_support.py`. Field names and literal values are contract values used by tests and plan hashing.

```python
from dataclasses import dataclass
from typing import Literal, Mapping, Sequence

SemanticRole = Literal[
    "human-source",
    "accepted-authority",
    "append-only-evidence",
    "current-semantic-state",
    "derived-index",
    "validated-package",
    "transaction-temporary",
    "unclassified",
]
Attention = Literal["🟢", "🟡", "🔴"]
Action = Literal[
    "保留",
    "引入",
    "重写",
    "重算",
    "移除过时声明",
    "暂不处理",
]
ReportStatus = Literal["待确认", "已完成", "已恢复"]
PathKind = Literal["missing", "directory", "file", "symlink", "gitlink"]
ContentSourceKind = Literal["none", "git-blob", "inline-base64"]

@dataclass(frozen=True)
class MergeContext:
    merge_base_sha: str
    source_sha: str
    target_before_sha: str
    merged_code_sha: str
    source_branch: str
    target_branch: str
    target_release_context: str
    customer_boundary: str
    memory_root: str

@dataclass(frozen=True)
class SnapshotEntry:
    state: Literal["present", "absent"]
    kind: PathKind
    git_mode: str | None
    git_oid: str | None
    sha256: str | None

@dataclass(frozen=True)
class PathLedgerRow:
    path: str
    snapshots: Mapping[str, SnapshotEntry]
    semantic_role: SemanticRole
    stable_identity: str
    owner: str
    attention: Attention
    action: Action
    fact_sources: Sequence[str]
    desired_value: str
    operation_id: str | None

@dataclass(frozen=True)
class ContentSource:
    kind: ContentSourceKind
    git_sha: str | None
    git_path: str | None
    inline_base64: str | None

@dataclass(frozen=True)
class RewriteOperation:
    operation_id: str
    sequence: int
    path: str
    action: Literal["引入", "重写", "重算", "移除过时声明"]
    preimage_sha256: str | None
    postimage_sha256: str | None
    post_mode: Literal["100644", "100755", "absent"]
    content_source: ContentSource

@dataclass(frozen=True)
class ReconciliationPlan:
    schema_version: int
    report_id: str
    context: MergeContext
    scan_sha256: str
    ledger: Sequence[PathLedgerRow]
    operations: Sequence[RewriteOperation]
    expected_unchanged_paths: Mapping[str, str]
    human_decisions: Sequence[Mapping[str, str]]
    post_check_expectations: Sequence[str]
    plan_sha256: str
```

Required plan rules:

- `schema_version` is `1`.
- `report_id` is `MM-<collision-safe-merged-code-short-sha>` and the report records the full SHA. Start with the first 12 lowercase hex characters; if that directory already records a different full SHA, extend the prefix one hex character at a time until it is unused. Reuse the directory only when its recorded full SHA is identical, and never rename an older report.
- Snapshot keys are exactly `base | source | target_before | result`.
- `path` is memory-root-relative POSIX text without `.` / `..`, backslash, NUL, drive prefix, absolute prefix, or Unicode/casefold collision.
- Directory rows exist for accounting but never receive a file RewriteOperation.
- `保留` rows have no operation. `暂不处理` is forbidden in a ready plan.
- `引入` requires an absent Result/preimage and a present regular-file postimage. `重写` requires the exact existing regular-file Result hash as preimage. `重算` may create an absent derived file or replace its exact existing preimage. `移除过时声明` requires an exact existing preimage and an absent post-state; labels cannot disguise a different mutation.
- `human-source` permits only `保留 | 引入`.
- `human-source | accepted-authority` introduction copies only a same-path `100644 | 100755` Git blob byte-for-byte from one recorded snapshot; inline/tree/symlink/path-substitution imports are rejected.
- `accepted-authority` permits `保留 | 引入`; replacement requires a separately accepted superseding artifact, never in-place rewrite.
- `append-only-evidence` permits `保留 | 引入`; a generated append file may use `重写` only when its preimage is preserved and the new bytes are a strict append verified by the checker.
- `derived-index` uses `重算` when bytes change.
- `移除过时声明` is allowed only for current/derived Agent-maintained content, never human-source, accepted-authority, append-only evidence, or validated package members.
- Every operation is referenced by exactly one ledger row; every changed row that needs bytes has exactly one operation.
- Inline payloads are base64-validated, capped at 2 MiB per file and 8 MiB total, and must hash to `postimage_sha256`.
- `git-blob` sources must use one of the four recorded SHAs, resolve to a file blob, remain under the recorded memory root, and hash to `postimage_sha256`.
- The normalized Plan Hash is SHA-256 over canonical UTF-8 JSON excluding only the `plan_sha256` member.

## Public Script Interface Contracts

### `scan-memory-reconciliation.py`

```text
python3 scripts/scan-memory-reconciliation.py \
  --project-root <absolute-or-relative-project-root> \
  --merge-base-sha <full-or-resolvable-sha> \
  --source-sha <full-or-resolvable-sha> \
  --target-before-sha <full-or-resolvable-sha> \
  --merged-code-sha <full-or-resolvable-sha> \
  --source-branch <name> \
  --target-branch <name> \
  --target-release-context <value> \
  --customer-boundary <value>
```

Optional post-Apply comparison:

```text
  --report <memory-root>/memory-merges/MM-<short-sha>/README.md
```

Behavior:

- resolves every SHA to a full commit and requires `HEAD == merged_code_sha`;
- reads Base/Source/Target-before from Git trees and Result memory from the worktree;
- requires one accepted memory root and rejects implicit `.agent-loop` ↔ `agent-loop` migration;
- excludes only the current report directory and its transaction data from Result business-memory accounting;
- emits sorted JSON containing Merge Context, Target spine identity, all directory/file/symlink/gitlink rows, role hints, snapshot hashes, blockers, `scan_sha256`, and `zero_change` when `--report` is supplied;
- never creates or changes a file.

### `check-memory-reconciliation.py`

```text
python3 scripts/check-memory-reconciliation.py \
  --project-root <root> \
  --report <memory-root>/memory-merges/MM-<short-sha>/README.md \
  --phase pre-apply|post-apply|restore \
  --expected-plan-sha256 <64-lowercase-hex>
```

Behavior:

- extracts exactly one JSON plan between the template sentinels;
- recomputes the canonical hash and scan inventory;
- validates report ID/full SHA/status, every ledger row, actions/roles, operations, pre/postimages, expected unchanged paths, Human Decisions, blockers, report-local dirty scope, and phase-specific state;
- performs no writes.

### `apply-memory-reconciliation.py`

```text
python3 scripts/apply-memory-reconciliation.py \
  --project-root <root> \
  --report <memory-root>/memory-merges/MM-<short-sha>/README.md \
  --mode apply|finalize \
  --expected-plan-sha256 <64-lowercase-hex>
```

Behavior:

- `--mode apply` runs the same pre-apply validation;
- `--mode apply` rejects `已完成`, unresolved 🔴/`暂不处理`, mismatched hashes, unexpected dirty paths, or an existing transaction;
- `--mode apply` creates a report-local `.memory-reconciliation-txn/<transaction-id>/journal.json` and exact backups;
- `--mode apply` applies operations in numeric sequence with atomic writes and no symlink traversal;
- `--mode apply` runs the machine post-check and records Apply evidence while the report remains `待确认` and the journal remains `checking`;
- `--mode finalize` is the only successful path that can change the report to `已完成`, mark the journal `verified`, and remove its transaction payload after a fresh post-apply check proves the exact Plan Hash, semantic-evidence block, zero-change result, and expected tree;
- finalization is crash-resumable: rerunning `--mode finalize` may finish or clean up the same `verified` transaction, but it never re-applies operations; a completed report without its own verified residual transaction rejects every Apply/Finalize replay;
- neither mode executes commands or hooks from the report; the Agent runs domain/semantic checks separately and records bounded evidence for validation;
- on Apply failure, the command attempts the same restore primitive used by the standalone command; it retains the journal if restore cannot prove exact recovery.

### `restore-memory-reconciliation.py`

```text
python3 scripts/restore-memory-reconciliation.py \
  --project-root <root> \
  --report <memory-root>/memory-merges/MM-<short-sha>/README.md \
  --transaction-id <YYYYMMDDTHHMMSSZ-12hex>
```

Behavior:

- verifies journal/report/plan identity and backup scope before any mutation;
- restores exact previous bytes/modes/absence in reverse operation order;
- verifies all restored hashes and unchanged paths;
- updates the report to `已恢复` while preserving failure evidence;
- deletes the transaction payload only after proven restoration; a failed restore keeps it and blocks all later Apply/Git actions.

## Exact Report Plan Block

`templates/memory-merge-report.md` must contain these sentinels exactly once:

````markdown
<!-- memory-reconciliation-plan:start -->
```json
{"schema_version":1,"report_id":"not-ready","plan_sha256":"not-ready"}
```
<!-- memory-reconciliation-plan:end -->
````

`not-ready` is a draft marker, not an accepted plan or placeholder for implementation. Pre-apply validation rejects it. After all 🔴 decisions are resolved, the Agent replaces the JSON with the complete canonical plan and displays the normalized Plan Hash for Human Review.

## Coordinated Synchronization Order

```text
clean live baseline
→ focused RED contract and saved RED report
→ runtime/design/reference semantic authority
→ report template and artifact ownership
→ Python support + read-only scan RED/GREEN
→ plan checker RED/GREEN
→ apply/restore transaction RED/GREEN
→ Submit/Branch/Recovery/domain integration
→ root/human docs and managed revision
→ validation scenarios and focused GREEN
→ five-domain feature validation
→ full suite and six-domain semantic audit
→ Proposal/plan evidence refresh
→ Human Review
→ separately authorized Submit / Integrate
```

Do not implement scripts before runtime/design semantics are fixed, and do not update root/human docs before the published owner surfaces exist.

## Task 0: Protect The Baseline And Enter Implementation Only After Plan Approval

**Files:**

- Read: `AGENTS.md`
- Read: `SKILL.md`
- Read: `references/runtime.md`
- Read: `references/design.md`
- Read: `docs/proposal/v1.4.x/post-merge-memory-reconciliation.md`
- Read: `docs/maintenance/full-validation-method.md`
- Read: `docs/maintenance/feature-validation-method.md`
- Modify only after Human Review: `docs/proposal/v1.4.x/post-merge-memory-reconciliation.md`

- [x] **Step 1: Reconfirm repository and authorization boundary.**

Run:

```bash
git status --short --branch
git rev-parse HEAD
git branch --show-current
rg -n 'Version: 1\.4\.0|"version": "1\.4\.0"|Current version:\*\* 1\.4\.0|版本：\*\* 1\.4\.0' SKILL.md plugin.json README.md Usage.md
rg -c 'block-version:1.4.0-20260716' templates/root-AGENTS.md
find tests -maxdepth 1 -type f -name '*.sh' | wc -l
```

Expected before implementation:

```text
branch: alpha/v1.4.0
HEAD: 7eddf63 unless the human has reviewed a newer baseline
version-bearing files: 1.4.0
root managed blocks at 1.4.0-20260716: 13
tests/*.sh observed at plan time: 37
dirty scope: approved Proposal plus this plan only
```

Stop if a changed file overlaps the implementation map or the baseline changed without Human Review.

- [x] **Step 2: Run the pre-change executable baseline.**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/agent-loop-memory-baseline-pyc \
  python3 -m unittest discover -s tests -p 'test_*.py' -v

for test_file in tests/*.sh; do
  bash "$test_file"
done
```

Expected at plan time: `98/98` Python PASS and `37/37` Shell PASS. Record the live count and stop on any unrelated failure.

- [x] **Step 3: Record the accepted implementation start in the Proposal.**

Only after the human approves this exact plan, change the Proposal status to:

```text
状态：Proposal 与 Implementation Plan 已由人类确认，实施中
```

Do not change confirmed semantics while changing status.

## Task 1: Add The Focused RED Contract And Preserve Evidence

**Files:**

- Create: `tests/validate-post-merge-memory-reconciliation.sh`
- Create after RED: `docs/reports/agent-loop-v1.4.0-post-merge-memory-reconciliation-red-baseline-2026-07-16.md`

- [x] **Step 1: Create the cross-surface focused contract before runtime implementation.**

Create `tests/validate-post-merge-memory-reconciliation.sh` with this complete assertion shape:

```bash
#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }
assert_file() { [ -f "$root/$1" ] || fail "missing required file: $1"; }
assert_contains() {
  local file=$1 text=$2
  grep -Fq -- "$text" "$root/$file" || fail "$file missing contract: $text"
}
assert_not_contains() {
  local file=$1 text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    fail "$file contains forbidden behavior: $text"
  fi
}

for file in \
  references/memory-reconciliation.md \
  templates/memory-merge-report.md \
  scripts/memory_reconciliation_support.py \
  scripts/scan-memory-reconciliation.py \
  scripts/check-memory-reconciliation.py \
  scripts/apply-memory-reconciliation.py \
  scripts/restore-memory-reconciliation.py; do
  assert_file "$file"
done

for file in SKILL.md references/design.md references/runtime.md \
  references/stage-guides.md references/workflow-checklists.md \
  references/submit-and-integrate.md references/branch-management.md; do
  assert_contains "$file" 'Post-Merge Memory Reconciliation'
done

for text in \
  'Target Canonical Memory Spine' \
  'Desired Target Memory Snapshot' \
  'Path Accounting Ledger' \
  'human-source | accepted-authority | append-only-evidence | current-semantic-state | derived-index | validated-package | transaction-temporary | unclassified' \
  '保留 | 引入 | 重写 | 重算 | 移除过时声明 | 暂不处理' \
  '待确认 | 已完成 | 已恢复' \
  'one Merged Code SHA' \
  'one successful Apply' \
  'Memory Reconciliation does not perform the code merge.'; do
  assert_contains references/memory-reconciliation.md "$text"
done

assert_contains references/runtime.md 'Code Merge Gate -> Post-Merge Memory Reconciliation -> Memory Commit Gate'
assert_contains references/submit-and-integrate.md 'Memory Reconciliation must complete before push, release, publish, or Source branch cleanup.'
assert_contains references/artifact-rules.md '.agent-loop/memory-merges/MM-<merged-code-short-sha>/README.md'
assert_contains templates/memory-merge-report.md '<!-- memory-reconciliation-plan:start -->'
assert_contains templates/memory-merge-report.md '<!-- memory-reconciliation-plan:end -->'
assert_contains templates/root-AGENTS.md 'After code integration, reconcile changed Agent Loop memory before push, release, or source-branch cleanup.'
assert_contains scripts/apply-memory-reconciliation.py '--mode'
assert_contains references/memory-reconciliation.md 'Memory Reconciliation scripts never execute commands or hooks stored in a report or memory artifact.'

for forbidden in \
  'Memory Reconciliation automatically merges code' \
  'Target memory always wins' \
  'unknown directories are ignored' \
  'Apply may run again after completion' \
  'Memory merge authorizes push'; do
  assert_not_contains references/memory-reconciliation.md "$forbidden"
done

python3 - "$root/references/runtime.md" <<'PY'
from pathlib import Path
import sys
text = Path(sys.argv[1]).read_text(encoding='utf-8')
tokens = [
    'Code Merge Gate',
    'Post-Merge Memory Reconciliation',
    'Memory Commit Gate',
    'Push Gate',
    'Release Gate',
    'Source Branch Cleanup Gate',
]
positions = [text.find(token) for token in tokens]
if any(position < 0 for position in positions):
    raise SystemExit('FAIL: runtime memory/Git gate order is incomplete')
if positions != sorted(positions):
    raise SystemExit('FAIL: runtime memory/Git gate order is incorrect')
PY

printf 'PASS: Post-Merge Memory Reconciliation contract is complete\n'
```

- [x] **Step 2: Run the focused contract and verify the intended RED.**

Run:

```bash
bash tests/validate-post-merge-memory-reconciliation.sh
```

Expected RED:

```text
FAIL: missing required file: references/memory-reconciliation.md
```

The failure must be caused by the missing capability, not shell syntax or an unrelated repository problem.

- [x] **Step 3: Save the RED report.**

The Chinese report records branch, HEAD, version, baseline counts, exact failing command/output, Proposal invariants, and forbidden side effects. Do not mark future GREEN results as already passing.

## Task 2: Publish The Canonical Semantic Model And Runtime Route

**Files:**

- Create: `references/memory-reconciliation.md`
- Modify: `SKILL.md`
- Modify: `references/design.md`
- Modify: `references/runtime.md`
- Modify: `references/concepts.md`

- [x] **Step 1: Add the detailed canonical reference.**

Write sections in this exact order:

```text
Purpose And Boundary
Entry Preconditions
Target Canonical Memory Spine
Four Snapshot Claims
Path Accounting Ledger
Semantic Artifact Roles
Fact Authority By Question
Desired Target Memory
Attention And Chinese Actions
Memory Merge Report
Scan
Fact Reconciliation
Exact Rewrite Plan And Plan Hash
Human Review
Apply
Global Post-check
Restore And Recovery
Single Successful Apply
Git Gate Separation
Domain Ownership Boundaries
Fail-Closed Conditions
```

Include the Proposal's confirmed flow exactly:

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

The reference must distinguish Agent semantic reasoning from script enforcement: scripts inventory/hash/apply/restore, while the Agent resolves product, environment, governance, requirement, ADR, and human-decision meaning.

- [x] **Step 2: Add concise core invariants to design.**

Add one section to `references/design.md` containing the Target spine, all-path accounting, semantic-role classification, Desired Target Memory, no-global-authority rule, and single-success rule. Do not copy the complete script CLI or report template.

- [x] **Step 3: Add executable routing and gates to runtime.**

Add an internal method under Submit / Integrate with this canonical order:

```text
Code Merge Gate -> Post-Merge Memory Reconciliation -> Memory Commit Gate -> Push Gate -> Release Gate -> Source Branch Cleanup Gate
```

Runtime must define:

- entry only after stable Merged Code SHA and code verification;
- Start authorization before report creation;
- exact Plan Hash Human Gate before Apply;
- `待确认` and `已恢复` block commit/push/release/cleanup;
- `已完成` permits only the next independently authorized gate;
- completed replay and stale plan fail closed;
- missing Source/Base/Target/Result evidence routes to Recovery rather than guessing.

- [x] **Step 4: Keep SKILL and concepts concise.**

Add package-map routes and required behavior without duplicating the detailed procedure. Add definitions for `Target Canonical Memory Spine`, `Desired Target Memory Snapshot`, `Memory Merge Report`, and `Path Accounting Ledger`.

- [x] **Step 5: Run targeted authority assertions.**

Run:

```bash
rg -n 'Target Canonical Memory Spine|Desired Target Memory Snapshot|Path Accounting Ledger' \
  SKILL.md references/design.md references/runtime.md references/concepts.md references/memory-reconciliation.md
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
```

Expected: every core term appears in the canonical owner and routed surfaces; YAML parsing exits `0`.

## Task 3: Add Report, Artifact Ownership, And Human Review Contracts

**Files:**

- Create: `templates/memory-merge-report.md`
- Modify: `references/artifact-rules.md`
- Modify: `references/project-memory-mode.md`
- Modify: `references/human-review-summary.md`
- Modify: `references/document-templates.md`
- Modify: `templates/project.md`

- [x] **Step 1: Create the report template.**

The template contains:

```text
Memory Merge ID
状态: 待确认 | 已完成 | 已恢复
Merge Context with all full SHAs
Code Verification
Customer Boundary
Target Release Context
Human Attention Summary
必须决定
建议复核
普通变更汇总
Memory Record Matrix
Human Decisions
Expected File Changes And Diffs
Exact Rewrite Plan with sentinels
Apply Result
Post-check Result
Restore / Remaining Risk
```

The matrix action column uses only the six approved Chinese values. Do not add item-level candidate/verified/blocked states.

- [x] **Step 2: Define artifact ownership and on-demand layout.**

Record exactly one durable report per full Merged Code SHA under:

```text
<memory-root>/memory-merges/MM-<collision-safe-short-sha>/README.md
```

Do not create `memory-merges/` during Init Project or Project Entry. The current report directory may contain `.memory-reconciliation-txn/` only while Apply/Post-check/Restore is active; successful completion or proven restore removes transaction payloads.

- [x] **Step 3: Define project memory pointer behavior.**

`project.md` may contain only the current report locator/status/blocker in Current Work. It must not copy the ledger, decisions, diffs, or transaction details. Enterprise detail files remain fact owners and are rewritten only when their durable facts are affected.

- [x] **Step 4: Add Human Review summaries.**

Add one table-first summary for Start and one for Exact Rewrite Plan. Exact Plan review shows red decisions, yellow reviews, green summary, every add/update/remove path, expected unchanged paths, Plan Hash, post-check, restore scope, and explicitly unauthorized Git actions.

- [x] **Step 5: Verify the template contract.**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
p = Path('templates/memory-merge-report.md')
t = p.read_text(encoding='utf-8')
assert t.count('<!-- memory-reconciliation-plan:start -->') == 1
assert t.count('<!-- memory-reconciliation-plan:end -->') == 1
for value in ('待确认', '已完成', '已恢复', '🟢', '🟡', '🔴', '保留', '引入', '重写', '重算', '移除过时声明', '暂不处理'):
    assert value in t, value
print('PASS: memory merge report template contract')
PY
```

Expected: the PASS line and exit `0`.

## Task 4: Implement The Data Model And Read-Only Scan With TDD

**Files:**

- Create: `scripts/memory_reconciliation_support.py`
- Create: `scripts/scan-memory-reconciliation.py`
- Create: `tests/memory_reconciliation_test_support.py`
- Create: `tests/test_memory_reconciliation_support.py`
- Create: `tests/test_memory_reconciliation_scan.py`
- Modify: `tests/test_python_checker_contract.py`

- [x] **Step 1: Create temporary Git fixture support.**

Provide these exact test helpers:

```python
@dataclass
class MemoryMergeWorkspace:
    project_root: Path
    merge_base_sha: str
    source_sha: str
    target_before_sha: str
    merged_code_sha: str

    @property
    def memory_root(self) -> Path: ...
    def write(self, relative: str, content: str | bytes, *, executable: bool = False) -> Path: ...
    def git(self, *arguments: str) -> subprocess.CompletedProcess[str]: ...
    def render_report(self, payload: dict[str, object]) -> Path: ...

def create_four_snapshot_workspace(root: Path) -> MemoryMergeWorkspace: ...
def run_memory_command(script: str, *args: str) -> subprocess.CompletedProcess[str]: ...
def tree_snapshot(root: Path, *, exclude_report_txn: bool = True) -> dict[str, str]: ...
```

Git fixtures configure local test-only author identity, use deterministic file contents, and never access remotes.

- [x] **Step 2: Write support-module RED tests.**

Add these test methods before the support module exists:

```text
test_resolve_memory_root_accepts_dot_agent_loop
test_resolve_memory_root_accepts_legacy_agent_loop
test_resolve_memory_root_rejects_both_roots
test_tree_inventory_includes_directories_files_and_symlinks_without_following
test_union_inventory_includes_source_only_target_only_and_absence_claims
test_casefold_collision_fails_closed
test_unicode_normalization_collision_fails_closed
test_canonical_plan_hash_is_root_independent
test_report_parser_requires_exactly_one_plan_block
test_safe_path_rejects_parent_absolute_backslash_and_symlink_parent
```

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/agent-loop-memory-red-pyc \
  python3 -m unittest tests.test_memory_reconciliation_support -v
```

Expected RED: import failure for `memory_reconciliation_support`.

- [x] **Step 3: Implement the frozen data model and safe primitives.**

Implement the types and plan rules from `Canonical Data Contract`. Reuse `checker_support.canonical_json_bytes`, `sha256_bytes`, and `atomic_write_bytes` only where their current signatures satisfy the contract. Do not duplicate or weaken their tested behavior.

Git calls use:

```python
subprocess.run(
    ["git", "-C", str(repo_root), *arguments],
    check=False,
    capture_output=True,
    text=False,
)
```

Never use `shell=True`. Parse `git ls-tree -r -t -z` as bytes and reject undecodable/NUL-invalid path data rather than silently replacing characters.

- [x] **Step 4: Write scan RED tests.**

Add:

```text
test_scan_is_read_only
test_scan_uses_actual_target_as_primary_spine
test_scan_accounts_for_every_path_in_four_snapshots
test_scan_includes_source_only_future_directory
test_scan_keeps_target_only_path_visible
test_scan_records_absence_as_claim
test_scan_rejects_missing_or_non_commit_sha
test_scan_rejects_head_different_from_merged_code_sha
test_scan_rejects_blank_merge_context_fields
test_scan_rejects_implicit_memory_root_migration
test_scan_excludes_only_current_report_transaction_scope
test_post_apply_scan_reports_zero_change_against_exact_plan
```

Representative assertion:

```python
before = tree_snapshot(workspace.project_root)
result = run_scan(workspace)
self.assertEqual(result.returncode, 0, result.stderr)
payload = json.loads(result.stdout)
self.assertIn("domain-snapshots/FLOW-01.md", {row["path"] for row in payload["paths"]})
self.assertEqual(tree_snapshot(workspace.project_root), before)
```

- [x] **Step 5: Implement the scan CLI minimally.**

Use `argparse`; missing/invalid arguments exit `2`, contract/safety failures exit `1`, success exits `0` and prints sorted indented UTF-8 JSON. Role hints are advisory values with `confidence` and `evidence`; the scanner never turns a hint into an accepted semantic role.

- [x] **Step 6: Extend Python checker inventory contracts.**

Assert all four new commands exist, reject unsupported Python, use only stdlib/local modules, and return usage exit `2` when required arguments are absent.

- [x] **Step 7: Run scan/support GREEN.**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/agent-loop-memory-green-pyc \
  python3 -m unittest \
    tests.test_memory_reconciliation_support \
    tests.test_memory_reconciliation_scan \
    tests.test_python_checker_contract -v
```

Expected: every listed test passes; no target fixture changes after read-only scans.

## Task 5: Implement Exact Plan Validation And Post-check With TDD

**Files:**

- Modify: `scripts/memory_reconciliation_support.py`
- Create: `scripts/check-memory-reconciliation.py`
- Create: `tests/test_memory_reconciliation_check.py`

- [x] **Step 1: Write the plan/checker RED matrix.**

Add:

```text
test_pre_check_accepts_complete_reviewed_plan_without_mutation
test_pre_check_rejects_missing_ledger_path
test_pre_check_rejects_unclassified_or_unresolved_red_row
test_pre_check_rejects_temporary_action_in_ready_plan
test_pre_check_rejects_human_source_rewrite
test_pre_check_rejects_accepted_authority_in_place_rewrite
test_pre_check_rejects_append_only_truncation
test_pre_check_rejects_changed_row_without_operation
test_pre_check_rejects_operation_without_ledger_owner
test_pre_check_rejects_wrong_or_self_inconsistent_plan_hash
test_pre_check_rejects_report_id_and_full_sha_mismatch
test_pre_check_rejects_second_report_for_same_merged_code_sha
test_pre_check_rejects_blank_merge_context_fields
test_plan_contract_rejects_action_state_mismatches
test_plan_contract_rejects_forged_human_source_import
test_plan_contract_accepts_recalculation_from_absent_result
test_pre_check_rejects_inline_payload_hash_or_size_mismatch
test_pre_check_rejects_git_blob_outside_recorded_context
test_pre_check_rejects_git_tree_as_blob_source
test_pre_check_rejects_unexpected_dirty_path
test_post_check_accepts_exact_postimages_and_unchanged_paths
test_post_check_rejects_missing_zero_change_evidence
test_restore_check_accepts_exact_pretransaction_state
```

Run the module and expect failure because the checker command does not exist.

- [x] **Step 2: Implement report/plan parsing and validation.**

Add these interfaces:

```python
def load_plan_from_report(report_path: Path) -> ReconciliationPlan: ...
def validate_plan_contract(plan: ReconciliationPlan) -> None: ...
def compute_plan_sha256(plan: ReconciliationPlan) -> str: ...
def validate_pre_apply(project_root: Path, report_path: Path, expected_hash: str) -> ValidationResult: ...
def validate_post_apply(project_root: Path, report_path: Path, expected_hash: str) -> ValidationResult: ...
def validate_restore_state(project_root: Path, report_path: Path, expected_hash: str) -> ValidationResult: ...
```

`ValidationResult` contains resolved context, sorted ledger, operations, report status, current hashes, blockers, and `zero_change`; it is not persisted as a new project artifact.

- [x] **Step 3: Enforce all-path accounting mechanically.**

Rebuild the four-snapshot union and require exact equality with ledger member paths after excluding only the current report/transaction scope. Validated packages may roll up semantic judgment, but their exact member paths/hashes remain ledger rows.

- [x] **Step 4: Implement the CLI.**

The CLI accepts only the documented phases and prints one PASS summary with report ID/phase/Plan Hash. It never changes report status or files.

- [x] **Step 5: Run checker GREEN and read-only proof.**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/agent-loop-memory-check-pyc \
  python3 -m unittest tests.test_memory_reconciliation_check -v
```

Expected: all plan contract and negative safety tests pass; tree snapshots before/after checker runs are identical.

## Task 6: Implement Apply, Post-check Finalization, And Restore With TDD

**Files:**

- Modify: `scripts/memory_reconciliation_support.py`
- Create: `scripts/apply-memory-reconciliation.py`
- Create: `scripts/restore-memory-reconciliation.py`
- Create: `tests/test_memory_reconciliation_apply.py`
- Create: `tests/test_memory_reconciliation_restore.py`

- [x] **Step 1: Write apply RED tests.**

Add:

```text
test_apply_writes_inline_utf8_bytes_and_mode_exactly
test_apply_copies_binary_git_blob_exactly
test_apply_removes_only_planned_stale_agent_content
test_apply_preserves_expected_unchanged_paths
test_apply_rejects_different_expected_plan_hash_without_writes
test_apply_rejects_preimage_drift_without_writes
test_apply_rejects_completed_report_replay
test_apply_rejects_path_escape_case_collision_and_symlink_parent
test_apply_rejects_existing_unrestored_transaction
test_injected_mid_apply_failure_restores_all_memory_bytes
test_apply_never_changes_business_code_git_refs_or_head
test_apply_never_executes_report_commands_or_hooks
```

Failure injection is accepted only when `AGENT_LOOP_TEST_FAILURE` is set and `AGENT_LOOP_ALLOW_TEST_HOOKS=1`; production use of the injection variable fails closed.

- [x] **Step 2: Implement journal creation and bounded operations.**

Use internal journal states:

```text
prepared -> applying -> checking -> verified
prepared | applying | checking -> restoring -> restored
restored -> idempotent restored-tree verification -> report status/transaction cleanup
```

These values never appear as report statuses. Before each mutation, persist the journal atomically with the planned operation, backup metadata, and completed-operation list. Record every created directory so restore removes it only when empty and created by this transaction.

- [x] **Step 3: Implement apply and automatic restore attempt.**

For every operation:

1. recheck exact preimage/absence and safe parent path;
2. materialize content into the transaction directory;
3. verify postimage hash before target mutation;
4. atomically replace/write/delete the exact path;
5. verify bytes/mode;
6. atomically append completed-operation evidence.

On any exception, call the same restore primitive. If restore succeeds, update the report to `已恢复`; if it fails, leave the journal in `restoring` and return failure with the exact blocker.

- [x] **Step 4: Write restore RED tests.**

Add:

```text
test_interrupted_transaction_restores_in_new_process
test_restore_recovers_write_completed_before_completion_record
test_restore_restores_deleted_file_and_mode
test_restore_rejects_tampered_backup_before_mutation
test_restore_rejects_journal_path_escape
test_restore_rejects_post_crash_unrelated_drift
test_incomplete_restore_keeps_journal_and_blocks_reapply
test_successful_restore_updates_report_to_restored
test_restore_resumes_after_restored_journal_before_or_after_status_update
test_regular_file_mode_matching_is_platform_aware
test_pre_check_emits_utf8_errors_under_ascii_host_stdio
```

- [x] **Step 5: Implement standalone restore.**

Restore validates every backup hash and current path state before the first reverse mutation. It never deletes an unplanned file to make room. A collision or unrelated post-crash edit keeps the journal and fails closed.

- [x] **Step 6: Define post-check finalization.**

After Apply, the Agent runs all domain/semantic checks named in the report and records their fresh evidence. Then `check-memory-reconciliation.py --phase post-apply` requires:

- exact postimages and unchanged paths;
- no unaccounted current memory path;
- no unresolved 🔴/`暂不处理`;
- report matrix counts match;
- an Agent-recorded semantic post-check evidence block;
- `scan --report` returns `zero_change: true`;
- the journal is in `checking`.

The Agent must not directly edit the status or delete transaction files. It runs:

```bash
python3 scripts/apply-memory-reconciliation.py \
  --project-root <root> \
  --report <memory-root>/memory-merges/MM-<short-sha>/README.md \
  --mode finalize \
  --expected-plan-sha256 <reviewed-64-lowercase-hex>
```

The finalizer repeats the post-apply validation, atomically advances the journal through `verified`, updates the report to `已完成`, and removes only its own transaction payload. It is resumable after a crash between those steps without re-applying memory operations. A second Apply is rejected, and a second Finalize is accepted only to clean up the same proven `verified` residual transaction.

Add:

```text
test_finalize_requires_semantic_evidence_and_zero_change
test_finalize_sets_completed_and_removes_only_own_transaction
test_finalize_resumes_verified_transaction_without_reapply
test_finalize_accepts_source_only_future_directory_import
test_finalize_rejects_completed_report_without_own_residual_transaction
test_finalize_never_executes_report_commands_or_hooks
```

- [x] **Step 7: Run apply/restore GREEN.**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/agent-loop-memory-apply-pyc \
  python3 -m unittest \
    tests.test_memory_reconciliation_apply \
    tests.test_memory_reconciliation_restore -v
```

Expected: all apply/restore tests pass, including process restart, tamper, path escape, stale hash, replay, and exact restoration.

## Task 7: Integrate Existing Owners, Submit Ordering, And Recovery

**Files:**

- Modify: `references/artifact-rules.md`
- Modify: `references/project-memory-mode.md`
- Modify: `references/branch-management.md`
- Modify: `references/submit-and-integrate.md`
- Modify: `references/recovery-and-backfill.md`
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/external-skill-adapters.md`
- Modify as needed: `references/requirement-management.md`
- Modify as needed: `references/project-decisions.md`
- Modify as needed: `references/delivery-contracts.md`
- Modify as needed: `references/bug-management.md`
- Modify as needed: `references/feature-follow-up.md`
- Modify as needed: `references/project-skills.md`
- Modify as needed: `references/onboarding-knowledge-base.md`

- [x] **Step 1: Connect Branch Context without expanding Git authority.**

Consume Source Branch, Target Branch, Target Release Context, Customer Boundary, lifecycle, and allowed direction. Replace only the old “future memory merge input” statement. Memory completion supplies evidence to later gates but never adopts strategy, performs Git actions, or permits customer-to-standard leakage.

- [x] **Step 2: Add Submit / Integrate blocker order.**

Define:

```text
no report + changed memory -> recommend/start reconciliation
待确认 -> block Memory Commit / push / release / cleanup
已恢复 -> block and return to new Plan or Recovery
unrestored transaction -> Recovery only
已完成 -> permit the next separately confirmed Memory Commit / push / release / cleanup gate
```

Code commit/merge authorization cannot be reused as Memory Start, Plan Hash, Memory Commit, Push, Release, or Cleanup authorization.

- [x] **Step 3: Distinguish Recovery routes.**

Ordinary stale-memory recovery uses code reality and human confirmation. Known post-merge reconciliation requires the four-SHA Merge Context and current report; if evidence is missing, Recovery attempts to recover evidence and never fabricates SHAs/branches.

- [x] **Step 4: Preserve domain owners.**

Add only these boundary statements where absent:

- Requirement owns original product meaning/lifecycle gates.
- Decision/ADR owns accepted technical meaning and supersession.
- Delivery Contract owns acceptance/breaking-change gates.
- Bug owns status/resolution/close/reopen; passing Feature tests do not close it.
- Feature Archive owns path movement/locator and rehydrate; reconciliation does not move directories to solve conflicts.
- Project Skill owns manifest and Execution Gate; merge does not authorize execution.
- onboarding-db is targeted by evidence overlap and never substitutes for project memory.

- [x] **Step 5: Run targeted ownership checks.**

Run:

```bash
rg -n 'Memory Reconciliation|Memory Merge Report|Desired Target Memory' \
  references/{artifact-rules,project-memory-mode,branch-management,submit-and-integrate,recovery-and-backfill,stage-guides,workflow-checklists,external-skill-adapters}.md
```

Expected: each owning surface contains its boundary; no new canonical stage or message-intent value appears.

## Task 8: Add Root Routing, Human Docs, Changelog, And Revision Sync

**Files:**

- Modify: `references/project-guidance.md`
- Modify: `templates/root-AGENTS.md`
- Modify: `templates/project.md`
- Modify: `references/document-templates.md`
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`
- Modify: listed root-revision regression files

- [x] **Step 1: Add exactly one root routing sentence.**

Use this sentence once in the appropriate managed block:

```text
After code integration, reconcile changed Agent Loop memory before push, release, or source-branch cleanup.
```

Do not copy states, actions, SHAs, report layout, script names, or algorithms into root guidance.

- [x] **Step 2: Advance all current managed blocks together.**

Change every current block to:

```text
block-version:1.4.0-20260716.1
```

Update only live-current revision expectations in the named tests. Preserve historical report/proposal strings.

- [x] **Step 3: Add concise human docs.**

README explains what the capability solves and that code merge happens first. Usage includes trigger phrases such as:

```text
代码已经合并，帮我合并 .agent-loop 记忆
校准 Source 和 Target 的项目记忆
生成记忆合并报告，先不要 Apply
继续已确认的 Memory Rewrite Plan
恢复失败的 Memory Reconciliation
```

Usage shows one Mermaid flow and the three attention levels without exposing machine JSON.

- [x] **Step 4: Add the v1.4.0 changelog entry.**

Record Target-spine scan, semantic role handling, report/gates, Python commands, exact restore, root revision, and validation coverage under the current v1.4.0 in-progress section. Do not create a new version heading.

- [x] **Step 5: Validate root revision and brevity.**

Run:

```bash
python3 scripts/check-root-agents-blocks.py --template templates/root-AGENTS.md
python3 - <<'PY'
from pathlib import Path
t = Path('templates/root-AGENTS.md').read_text(encoding='utf-8')
assert t.count('block-version:1.4.0-20260716.1') == 13
assert t.count('After code integration, reconcile changed Agent Loop memory before push, release, or source-branch cleanup.') == 1
print('PASS: root memory reconciliation routing is concise')
PY
```

Expected: both PASS and 13 current blocks.

## Task 9: Add Pressure Scenarios And Turn Focused RED Green

**Files:**

- Modify: `references/validation-scenarios.md`
- Modify: `tests/validate-post-merge-memory-reconciliation.sh`
- Create: `docs/reports/post-merge-memory-reconciliation-feature-validation-2026-07-16.md`

- [x] **Step 1: Add scenario coverage for all Proposal cases.**

At minimum preserve explicit scenarios for:

```text
Source-only Requirement/Feature
Target-only work
same Feature compatible append-only changes
conflicting current state
both memories wrong
code versus Requirement
code versus accepted ADR
environment unverifiable/verifiable
branch-local Current Work
Bug verifying not closed
archive locator recompute
original source protection
Human Decision conflict
Project Skill manifest conflict
semantic error without Git conflict
Source branch deleted
dirty Result memory
stale Plan Hash
Apply interruption/restore success
Restore failure
completed replay
zero-change integration
grouped/dependent red decisions
fast-forward/squash evidence
push before memory completion
customer boundary conflict
Source future directory
unclassified directory
Target not main
legacy memory root
case/Unicode/symlink path pressure
```

- [x] **Step 2: Run the original focused test as GREEN.**

Run:

```bash
bash tests/validate-post-merge-memory-reconciliation.sh
```

Expected:

```text
PASS: Post-Merge Memory Reconciliation contract is complete
```

- [x] **Step 3: Run the complete feature-scoped executable boundary.**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/agent-loop-memory-focused-pyc \
  python3 -m unittest \
    tests.test_memory_reconciliation_support \
    tests.test_memory_reconciliation_scan \
    tests.test_memory_reconciliation_check \
    tests.test_memory_reconciliation_apply \
    tests.test_memory_reconciliation_restore \
    tests.test_python_checker_contract \
    tests.test_root_agents_blocks -v

bash tests/validate-post-merge-memory-reconciliation.sh
bash tests/validate-branch-management-strategy.sh
bash tests/validate-bug-management.sh
bash tests/validate-project-local-skills.sh
bash tests/validate-project-skill-discovery-guard.sh
bash tests/validate-requirement-lifecycle-backlog.sh
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-root-agents-block-refresh.sh
bash tests/validate-v1.2.4-root-stage-coverage.sh
```

Expected: all selected Python and Shell tests pass. Record exact live counts.

- [x] **Step 4: Produce the five-domain focused report.**

Use `docs/maintenance/feature-validation-method.md`. Score Requirement/Scope, Logic/Gates, Cross-Surface, Pressure Resistance, and Evidence/Maintainability; list real unresolved severity findings. The report cannot claim full-suite PASS yet.

## Task 10: Run Full Validation And Repair Every Real Loophole

**Files:**

- Create/update: `docs/reports/agent-loop-v1.4.0-post-merge-memory-reconciliation-full-validation-2026-07-16.md`
- Modify implementation/test files only through new RED evidence when defects are found

- [x] **Step 1: Re-read the full-validation method and lock the audit object.**

Record branch, HEAD, version, working-tree scope, Proposal/plan paths, test inventory, and whether the audit targets the current workspace or a later commit.

- [x] **Step 2: Run the full Python and Shell suites.**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/agent-loop-memory-full-pyc \
  python3 -m unittest discover -s tests -p 'test_*.py' -v

passed=0
for test_file in tests/*.sh; do
  bash "$test_file"
  passed=$((passed + 1))
done
printf 'shell tests passed: %s\n' "$passed"
```

Expected: all live tests pass. Never copy the planning-time `98/37` counts into the final report.

- [x] **Step 3: Run mechanical and cross-platform checks.**

Run:

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
python3 -m json.tool plugin.json >/dev/null
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
python3 -m compileall -q scripts tests
python3 - <<'PY'
from pathlib import Path
for path in Path('.').rglob('*.md'):
    fences = [line for line in path.read_text(encoding='utf-8').splitlines() if line.lstrip().startswith('```')]
    if len(fences) % 2:
        raise SystemExit(f'unbalanced Markdown fence: {path}')
print('PASS: Markdown fences balanced')
PY
git diff --check
```

Remove any repository-local `__pycache__/` produced by the explicit compile check before final diff review; do not delete user files.

- [x] **Step 4: Execute the six-domain semantic audit.**

Audit:

- Logic Correctness: no code/memory/Git gate reuse, stale plan/replay/restore paths are closed.
- Autonomy: Agent classifies/recommends before asking humans; new directories do not require whitelist releases.
- Project Entry/Onboarding: capability does not run before reliable memory and does not broadly rewrite onboarding-db.
- Development/Test: RED/GREEN, report/plan, transaction, post-check, and recovery form a complete path.
- Memory: Target spine is baseline not truth; every path is accounted; immutable/history/derived ownership is preserved.
- Recommendation: one next action is produced for missing evidence, unresolved red, stale plan, apply failure, and restore failure.

- [x] **Step 5: Repair findings only through new RED assertions.**

For each Critical/High/Medium finding: save the exact failing scenario, add a focused failing test, verify RED, implement the smallest correction, rerun focused GREEN, then rerun the complete suites. Do not edit a report to hide an unresolved failure.

- [x] **Step 6: Write the Chinese full-validation report.**

Include score/grade, severity counts, live Python/Shell counts, six-domain results, Proposal scenario matrix, RED/GREEN/REFACTOR evidence, passed invariants, rejected suggestions, residual risk, and explicit statements:

```text
commit: not authorized
push: not authorized
tag: not authorized
release/publish: not authorized
installed Skill sync: not authorized
```

## Task 11: Self-Review, Proposal Evidence Refresh, And Human Review

**Files:**

- Modify: `docs/proposal/v1.4.x/post-merge-memory-reconciliation.md`
- Modify: this implementation plan status/evidence only
- Review: every file in the responsibility map

- [x] **Step 1: Run spec-to-plan and implementation coverage review.**

Create a checklist mapping all Proposal sections and 31 original pressure scenarios plus added legacy/path-safety and Human Review repair cases to runtime text, a test, or a reasoned non-executable Human Review scenario. Add missing coverage before claiming completion.

- [x] **Step 2: Run placeholder, type, and interface consistency review.**

Run:

```python
from pathlib import Path
import re

files = [
    Path("docs/proposal/v1.4.x/post-merge-memory-reconciliation-implementation-plan.md"),
    Path("references/memory-reconciliation.md"),
    Path("scripts/memory_reconciliation_support.py"),
    *sorted(Path("tests").glob("test_memory_reconciliation_*.py")),
]
parts = [
    ("T" + "BD"),
    ("TO" + "DO"),
    ("implement " + "later"),
    ("fill in " + "details"),
    ("add proper " + "error handling"),
    ("handle " + "edge cases"),
    ("write tests for " + "the above"),
    ("similar to " + "previous task"),
    ("use appropriate " + "helper"),
]
pattern = re.compile("|".join(re.escape(part) for part in parts), re.IGNORECASE)
findings = [
    f"{path}:{line_number}:{line}"
    for path in files
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
    if pattern.search(line)
]
if findings:
    raise SystemExit("\n".join(findings))
```

Run the snippet with the repository Python interpreter. Expected: no output and exit `0`. Then compare every dataclass field, CLI flag, mode, status, action, role, report sentinel, and Plan Hash rule across docs, scripts, templates, and tests.

- [x] **Step 3: Review the complete diff and unrelated-work boundary.**

Run:

```bash
git status --short
git diff --stat
git diff --check
git diff -- SKILL.md references scripts templates tests README.md Usage.md CHANGELOG.md docs/reports docs/proposal/v1.4.x/post-merge-memory-reconciliation.md
```

Do not stage. Separate unrelated work before requesting Human Review.

- [x] **Step 4: Refresh Proposal and plan status with real evidence only.**

After focused/full validation and primary-Agent review pass, update the Proposal to implementation-complete pending Human Review and link the focused/full reports. Update this plan's status/checkmarks to match work actually completed. Do not mark an unrun test or unresolved finding complete.

- [x] **Step 5: Present Human Review Summary and stop.**

Summarize:

- Proposal requirement coverage;
- files changed by category;
- exact RED/GREEN/full-validation counts;
- Critical/High/Medium/Low findings and repairs;
- current version/root revision;
- runtime capability versus target-project side effects actually performed;
- commit/push/tag/release/sync status;
- one recommended next stage: Submit / Integrate review.

Do not commit, push, tag, release, publish, or sync installed skills until the human separately confirms the matching action.

## Execution Evidence Refresh

本节只记录实际执行结果，不修改任务定义或验收标准。

| Task | 实际结果 |
|---|---|
| 0 | 基线锁定于 `alpha/v1.4.0` / `7eddf63195a266b7f107bc2d5ca0bf0095391922`；版本 `1.4.0`；pre-change `98/98` Python、`37/37` shell。 |
| 1 | focused contract 保存真实 RED：`FAIL: missing required file: references/memory-reconciliation.md`；RED 报告已保存。 |
| 2–3 | canonical reference、runtime/design/concepts、report/template/artifact/project-memory/human-review contracts 完成并通过 targeted checks。 |
| 4 | support/scan TDD GREEN；macOS 本地验证，Windows CI contract 定义。 |
| 5 | exact plan/check/post-check TDD GREEN。 |
| 6 | apply/finalize/restore TDD GREEN，包含跨进程恢复、tamper、replay、path safety 与 exact bytes/modes。 |
| 7–8 | Branch/Submit/Recovery/domain owners/root routing/human docs/changelog 协调；root revision `1.4.0-20260716.1` 为 `13/13`。 |
| 9 | 31 个 Proposal 场景映射到 `A–AC`，legacy/path-safety 为 `AD–AE`，Human Review 修复压力为 `AF–AJ`；Windows CI 修复后 focused `104/104` Python、`9/9` shell，feature score `99/100 · STRONG`。 |
| 10 | 首轮 full mechanical baseline `164/164` Python、`38/38` shell；Task 10 六域审计新增 7 个 RED，Human Review 补充审计再发现 7 类漏洞并用 8 个 RED/兼容性 RED 修复；Release Gate Windows CI 又以 2 个本地 RED 修复 UTF-8/mode 契约；最终 `182/182` Python、`38/38` shell、全部机械检查 PASS，full score `98/100 · STRONG`。 |
| 11 | placeholder、type/interface、spec-to-plan、36 场景、complete diff、unrelated boundary 和 authorization self-review 完成；修复后重新停在 Human Review。 |

Task 8 计划示例中的 root checker 缺少当前 CLI 必填的 `--target`，因此按当前已验证接口运行等价 self-check：

```bash
python3 scripts/check-root-agents-blocks.py \
  --template templates/root-AGENTS.md \
  --target templates/root-AGENTS.md \
  --no-source-check
```

该现实差异没有改变 Proposal 语义、root revision 或验收标准。

权限状态：

```text
commit: not authorized
push: not authorized
tag: not authorized
release/publish: not authorized
installed Skill sync: not authorized
```

## Plan Self-Review Checklist

- [x] Every confirmed Proposal principle maps to a task or invariant.
- [x] Target memory is a scan spine/baseline, not a global authority or whitelist.
- [x] Source-only, Target-only, unchanged, absence, future, custom, legacy, and package member paths are accounted.
- [x] Semantic reasoning remains Agent-owned; scripts own deterministic inventory, validation, bounded mutation, and recovery.
- [x] All public script flags, data fields, literal values, error boundaries, and expected tests are defined.
- [x] Report actions/status/attention values match the approved low-cognitive-load model.
- [x] Human original sources, accepted meaning, append-only history, domain gates, and customer isolation remain protected.
- [x] Exact Plan Hash, stale detection, one-success Apply, post-check, restart restore, and failed-restore blockers are covered.
- [x] macOS/Windows/Python-stdlib/path/symlink/case/Unicode constraints are explicit.
- [x] Root guidance remains one routing sentence and all managed-block revisions move together.
- [x] Focused and mandatory full validation are separate and both required.
- [x] No branch, worktree, subagent, implementation, commit, push, tag, release, publish, or install-sync permission is implied by this plan.

## Human Review Gate

Approval of this document authorizes entry into Task 0 and implementation of the listed repository files only. It does not authorize subagent dispatch, a new worktree/branch, commit, push, tag, PR, merge, release, publish, external-system writes, target-project `.agent-loop/` mutation, or installed-Skill synchronization.

After approval, the recommended execution method is inline `executing-plans` with checkpoints after Tasks 1, 4, 6, 9, and 10. A subagent-driven execution option may be proposed only through a separate bounded-dispatch Human Gate.

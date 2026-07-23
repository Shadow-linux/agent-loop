# Persistent Lightweight Execution Card And Change Memory Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Do not dispatch subagents unless the human separately authorizes one bounded dispatch.

**Goal:** Persist every clearly eligible Lightweight Execution Card under a stable monthly Change path, add a deterministic cross-platform pending-memory scanner, and make Agent-owned evidence-based memory consolidation recoverable without weakening Lightweight / Bug / Feature routing, verification, rollback, branch truth, or Human Gates.

**Architecture:** Replace the response-only card with one Markdown source of truth under the active Agent Loop memory root, partitioned at creation by `YYYY-MM` and never moved. Add a read-only Python 3.10+ standard-library scanner with a small testable support module; the scanner validates artifacts and computes `3 pending` / `older than 7 days`, while the Agent remains responsible for semantic memory classification and rewriting. Coordinate controller, runtime/design, artifact ownership, Project Entry, memory reconciliation, root guidance, human docs, focused regression, cross-platform CI, and mandatory full validation.

**Tech Stack:** Markdown skill sources and templates; Python 3.10+ standard library (`argparse`, `dataclasses`, `datetime`, `json`, `pathlib`, `re`); `unittest`; Bash focused contracts; Ruby standard-library structural checks; existing root-guidance checker and cross-platform GitHub Actions matrix. No third-party dependency, runtime daemon, scheduler, database, archive transaction, automatic memory writer, or new canonical stage.

---

状态：Implementation Plan 已执行完成，待最终 Human Review
设计来源：`docs/proposal/v1.5.x/persistent-lightweight-execution-card-and-memory-consolidation.md`
计划日期：2026-07-18
计划基线：`alpha/v1.5.0` at `200a23b85b5b0e3ebe68496f5f4a16d923d46788`
当前 Skill 版本：`1.5.0`
目标 Skill 版本：`1.5.0`，本轮不升级版本号

## Execution Boundary

- Repository perspective: maintain the Agent Loop skill source repository. Do not create a target-project `.agent-loop/` tree in this source repository.
- Approved design input: `docs/proposal/v1.5.x/persistent-lightweight-execution-card-and-memory-consolidation.md`.
- Existing implementation baseline: commit `200a23b85b5b0e3ebe68496f5f4a16d923d46788` implements the response-local Lightweight Change Lane that this follow-up intentionally supersedes.
- Expected planning-start dirty state: the approved Proposal and this plan are the only intended untracked files. Stop if another change appears or an overlapping file changes unexpectedly.
- Plan approval authorizes implementation only through the exact file/rule/test scope below. It does not authorize a branch/worktree action, subagent dispatch, installed-Skill synchronization, commit, push, PR, merge, tag, release, publish, deployment, production/external access, paid call, configuration write, or destructive operation.
- Do not update `SKILL.md`, `plugin.json`, `README.md`, or `Usage.md` away from version `1.5.0`. This is a same-version follow-up capability on `alpha/v1.5.0`.
- Refresh all 13 root managed blocks from `block-version:1.5.0-20260717` to `block-version:1.5.0-20260718` because the managed bootstrap reminder changes without a Skill version bump.
- Do not rewrite historical Proposal or Report evidence. Update only the new Proposal, this plan, a new RED report, a new 2026-07-18 full-validation report, and live runtime authority.
- Use `apply_patch` for manual edits. Formatting or executable-bit changes may use their normal focused commands.
- Preserve unrelated dirty work. Never use `git reset --hard`, `git checkout --`, or a bulk rewrite that can erase human changes.
- A Proposal or prior report is not runtime evidence. Re-run live tests and record actual totals.
- This changes artifact ownership, Project Entry root interpretation, recovery boundaries, Project Memory Update rules, root guidance, and post-merge memory inputs. Focused tests do not replace full validation.
- Stop at final Human Review with no staging or Git mutation beyond read-only inspection.

## Stage Helper Resolution

| Field | Resolution |
|---|---|
| Stage | Plan Gate / Plan |
| Canonical candidate | `superpowers:writing-plans` — not exposed by the current runtime |
| Alias candidate | `writing-plans` — loaded completely from `/Users/shaodowyd/.codex/skills/writing-plans/SKILL.md` |
| Status | `loaded` |
| Fallback | `no` |
| Method used | zero-context file map, exact CLI/data contracts, bite-sized RED/GREEN tasks, exact commands and expected outcomes, rollback and self-review |
| Agent Loop override | save beside the approved Proposal; no `docs/superpowers/`, automatic worktree, subagent, commit, push, tag, release, publish, or target-project fixture outside `tests/` |

No downstream Feature workspace exists in this source repository. Keep this resolution response-local and in this plan; do not create `.agent-loop/features/` merely to log helper use.

### Implementation Execution Evidence

| Helper | Resolution |
|---|---|
| `executing-plans` | `loaded`；已完整读取 `/Users/shaodowyd/.codex/skills/executing-plans/SKILL.md`，按 Task 0–8 顺序执行 |
| `test-driven-development` | `loaded`；已完整读取 `/Users/shaodowyd/.codex/skills/test-driven-development/SKILL.md`，先保留真实 RED 再进入 GREEN |
| `verification-before-completion` | `loaded`；已完整读取 `/Users/shaodowyd/.codex/skills/verification-before-completion/SKILL.md`，完成声明前执行实时验证 |
| `requesting-code-review` | `loaded`；最终 handoff 前已完整读取；其 reviewer Subagent 路径受本轮“不得派发 Subagent”边界覆盖，因此由主 Agent 按同一 Proposal/plan/diff/test 证据执行 self-review，未 dispatch |
| `systematic-debugging` | `loaded`；scanner 首轮 GREEN 暴露测试 fixture 的 age 预期错误后完整加载，根因是 7 月 17/18 两条记录的最早 age 应为 1；最小修复为让该 count-only 场景两条记录都在 7 月 18 日完成 |
| Fallback | `no`；当前所需 helper 均可用，未创建 Feature workspace 或 helper-native artifact |

## Branch Context Evidence

- Current Branch: `alpha/v1.5.0`.
- Baseline HEAD: `200a23b85b5b0e3ebe68496f5f4a16d923d46788`.
- Current Skill version: `1.5.0`.
- Target Release Context: continue the approved `v1.5.0` alpha line.
- Sealed Check: no released `v1.4.0` or stable tag content is edited.
- Customer Isolation: not applicable.
- Git actions authorized: none.

## Approved Decisions

1. Accuracy principle: the lane reduces ceremony and document depth, never correctness, evidence, scope control, rollback, or Human Gates.
2. Canonical path: `<memory-root>/changes/YYYY-MM/YYYY-MM-DD-<topic>.md`; a same-day same-topic collision uses the first free `-2`, `-3`, and later suffix without overwriting an existing record.
3. The month is a creation-time storage partition, not Archive state. A Change never moves after completion, memory review, commit, merge, or release.
4. Reuse the one accepted memory root: `.agent-loop/` by default or existing accepted legacy `agent-loop/`. Two roots fail closed. With no root, the first clearly eligible Change may create `.agent-loop/changes/YYYY-MM/` without claiming full project initialization.
5. Status remains small: `in-progress | completed | stopped`.
6. Memory axes remain separate: `Memory Review: pending | complete`; `Memory Result: pending | none | synced | human-review`.
7. Count trigger: `completed + Memory Review: pending >= 3`.
8. Age trigger: `as_of_date - oldest_completed_at > 7 days`; exactly 7 days does not trigger.
9. `in-progress`, `stopped`, and `Memory Review: complete` never count as pending.
10. `human-review` is surfaced separately until human resolution; it exits automatic pending count but cannot disappear from Project Entry, pre-release, or post-merge reporting.
11. The scanner is read-only and mechanical. It never classifies product meaning or writes project memory.
12. High-evidence memory synchronization is Agent-owned only when every evidence/ownership/no-new-decision condition passes and the exact target path/fact/evidence/rollback is disclosed before write.
13. A changes-only root cannot be expanded automatically into `project.md`, enterprise memory, or a memory-mode switch.
14. Accidental context loss may resume one card only after branch/HEAD/dirty-diff revalidation. Planned multi-session work, handoff, Subagent, or long tracking remains a Feature trigger.
15. Code merges first. Post-Merge Memory Reconciliation consumes Change files as evidence only after verified code integration; a Source Change never instructs Target memory to overwrite itself.
16. No Change README, INDEX, archive locator, move, rehydrate, restore transaction, scheduler, counter file, or automatic cold archive is added.

## File Responsibility Map

### Create

- `scripts/lightweight_change_support.py` — Change path/metadata/section parser, invariant validator, memory-root discovery, aggregation model, threshold calculation, deterministic payload construction, and contract errors.
- `scripts/scan-lightweight-changes.py` — thin Python 3.10+ read-only CLI that parses `--project-root` and `--as-of`, calls the support module, prints deterministic UTF-8 JSON, and maps usage/contract outcomes to exit codes.
- `tests/lightweight_change_test_support.py` — dynamic target-project fixture builder, canonical Change Markdown factory, CLI runner, JSON decoder, and read-only tree snapshot helper.
- `tests/test_lightweight_change_scan.py` — unit/CLI regression for roots, monthly layout, field/state validity, pending count/age, human-review visibility, deterministic output, and zero mutation.
- `docs/reports/agent-loop-v1.5.0-persistent-lightweight-change-red-baseline-2026-07-18.md` — live pre-implementation baseline and focused RED evidence.
- `docs/reports/agent-loop-v1.5.0-full-validation-2026-07-18.md` — fresh Chinese six-domain audit and actual full test totals after GREEN.

### Modify: Approved Design And Planning Evidence

- `docs/proposal/v1.5.x/persistent-lightweight-execution-card-and-memory-consolidation.md` — preserve accepted meaning; set implementation/validation status only as real evidence becomes available.
- `docs/proposal/v1.5.x/persistent-lightweight-execution-card-and-memory-consolidation-implementation-plan.md` — check boxes and record execution evidence without changing approved semantics.

### Modify: Controller And Core Runtime

- `SKILL.md` — replace response-local/default-no-artifact claims with persistent monthly card, changes-only root, scanner, accidental recovery, memory trigger, and stop rules; keep the entry concise.
- `references/runtime.md` — canonical create-before-target-write order, accepted/legacy root selection, no-root changes-only state, persistent card recovery, scanner triggers, human-review visibility, automatic-sync disclosure, and post-merge boundary.
- `references/design.md` — accuracy principle, persistent artifact ownership, non-archive monthly partition, evidence-based consolidation, branch fact scope, and no-new-stage/status/mode invariants.
- `references/concepts.md` — concise definitions and default layout.
- `references/lightweight-change-lane.md` — detailed authoritative behavior replacing every response-local/no-directory rule.

### Modify: Artifact, Memory, Recovery, And Integration Boundaries

- `references/artifact-rules.md` — Change file ownership/layout/status combinations, no archive/index, drift rules, sensitive evidence prohibition, and changes-only root semantics.
- `references/project-memory-mode.md` — Change history stays outside project memory; high-evidence sync conditions; pending/human-review handling; no implicit project memory init or mode switch.
- `references/memory-reconciliation.md` — after verified code merge, inventory Change evidence without treating Source `synced` as a Target overwrite instruction.
- `references/project-guidance.md` — one concise Agent-facing bootstrap requirement and root reliability distinction.
- `references/branch-management.md` — card branch/SHA context and current-branch truth do not authorize branch action or cross-branch memory writes.
- `references/submit-and-integrate.md` — Change and memory status join diff/review evidence but grant no Git action.

### Modify: Stage, Helper, Template, And Checklist Surfaces

- `references/stage-guides.md`
- `references/workflow-checklists.md`
- `references/document-templates.md`
- `references/implementation-planning.md`
- `references/skill-routing.md`
- `references/external-skill-adapters.md`
- `templates/lightweight-execution-card.md`

These files must say the card Plan remains adaptive and does not enter mandatory Feature Plan / Execute helper stages, while the card itself is persisted before the first target write. Do not change unrelated response-local rules for brainstorming, Project Skills, Concept reopening, or helper-resolution pending records.

### Modify: Root Guidance, Human Docs, Scenarios, Tests, And CI

- `templates/root-AGENTS.md`
- `README.md`
- `Usage.md`
- `CHANGELOG.md`
- `references/validation-scenarios.md`
- `tests/validate-lightweight-change-lane.sh`
- `tests/test_python_checker_contract.py`
- `.github/workflows/cross-platform-checkers.yml`

Root revision consumers that must move together from `1.5.0-20260717` to `1.5.0-20260718`:

- `tests/test_root_agents_blocks.py`
- `tests/validate-branch-management-strategy.sh`
- `tests/validate-bug-management.sh`
- `tests/validate-lightweight-change-lane.sh`
- `tests/validate-project-local-skills.sh`
- `tests/validate-project-skill-discovery-guard.sh`
- `tests/validate-requirement-lifecycle-backlog.sh`
- `tests/validate-root-agents-block-checker.sh`
- `tests/validate-root-agents-block-refresh.sh`
- `tests/validate-v1.2.4-root-stage-coverage.sh`
- `references/validation-scenarios.md`
- `references/workflow-checklists.md`
- `CHANGELOG.md`

Run a repository-wide exact search after edits; historical Proposal/Report evidence may retain old revisions only when it clearly describes an old snapshot.

## Scanner CLI Contract

Canonical macOS/POSIX command:

```bash
python3 scripts/scan-lightweight-changes.py \
  --project-root /absolute/or/relative/project \
  --as-of 2026-07-18
```

Canonical Windows PowerShell command:

```powershell
py -3 scripts\scan-lightweight-changes.py `
  --project-root C:\path\to\project `
  --as-of 2026-07-18
```

Use the established Python 3.10+ interpreter resolution from `references/project-guidance.md`: `python3` on macOS/POSIX and `py -3` or `python` on Windows. Tests invoke `sys.executable`; do not assume the `python3` command exists on Windows.

Exit classes:

```text
0 = valid scan; result is triggered or not-triggered
1 = invalid Change artifact, unsafe/ambiguous memory root, path/layout error, or inconsistent state
2 = usage error, invalid --as-of, missing project root, or unsupported Python
```

Valid stdout is deterministic, sorted, UTF-8 JSON with this exact top-level shape:

```json
{
  "as_of": "2026-07-18",
  "changes_root": ".agent-loop/changes",
  "counts": {
    "completed": 4,
    "human_review": 1,
    "in_progress": 0,
    "pending": 3,
    "stopped": 0,
    "total": 4
  },
  "human_review_changes": [
    {
      "completed_at": "2026-07-15",
      "path": ".agent-loop/changes/2026-07/2026-07-15-review-provider.md",
      "topic": "review-provider"
    }
  ],
  "memory_root": ".agent-loop",
  "oldest_pending": {
    "age_days": 8,
    "completed_at": "2026-07-10",
    "path": ".agent-loop/changes/2026-07/2026-07-10-update-domain.md",
    "topic": "update-domain"
  },
  "pending_changes": [
    {
      "age_days": 8,
      "completed_at": "2026-07-10",
      "path": ".agent-loop/changes/2026-07/2026-07-10-update-domain.md",
      "topic": "update-domain"
    },
    {
      "age_days": 7,
      "completed_at": "2026-07-11",
      "path": ".agent-loop/changes/2026-07/2026-07-11-refresh-host.md",
      "topic": "refresh-host"
    },
    {
      "age_days": 6,
      "completed_at": "2026-07-12",
      "path": ".agent-loop/changes/2026-07/2026-07-12-adjust-timeout.md",
      "topic": "adjust-timeout"
    }
  ],
  "result": "triggered",
  "schema_version": 1,
  "trigger_reasons": ["pending-age", "pending-count"]
}
```

Rules:

- `changes_root` and `memory_root` are project-relative POSIX paths or `null` when neither root exists.
- `pending_changes`, `human_review_changes`, and `trigger_reasons` are lexically sorted.
- `oldest_pending` is `null` when no pending Change exists.
- `pending-count` appears when `pending >= 3`.
- `pending-age` appears when oldest `age_days > 7`; exactly 7 does not trigger.
- `result` is `triggered` when at least one threshold reason exists; otherwise `not-triggered`.
- Runtime facts such as memory drift, pre-release context, and verified post-merge entry are Agent/controller event triggers. The scanner reports the underlying pending/human-review inventory and does not accept an event flag or invent semantic context.
- With neither memory root present, the scanner returns `not-triggered`, null roots, zero counts, empty arrays, and performs no write.
- Contract failures print deterministic JSON to stdout with `schema_version: 1`, `result: invalid`, and `error: {category, detail}`, then exit 1.
- argparse/unsupported-runtime failures exit 2 and write usage/capability text to stderr.
- Two valid runs against unchanged files must have identical stdout/stderr/exit code and identical project tree hashes.

## Change Parser Contract

`scripts/lightweight_change_support.py` must expose these public units:

```python
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Literal, Sequence

ChangeStatus = Literal["in-progress", "completed", "stopped"]
MemoryReview = Literal["pending", "complete"]
MemoryResult = Literal["pending", "none", "synced", "human-review"]


@dataclass(frozen=True)
class LightweightChangeContractError(Exception):
    category: str
    detail: str
    exit_code: int = 1


@dataclass(frozen=True)
class LightweightChange:
    path: str
    topic: str
    status: ChangeStatus
    created_at: date
    updated_at: date
    completed_at: date | None
    memory_review: MemoryReview
    memory_result: MemoryResult


@dataclass(frozen=True)
class LightweightChangeScan:
    schema_version: int
    as_of: date
    memory_root: str | None
    changes_root: str | None
    changes: Sequence[LightweightChange]
```

The implementation must additionally expose these exact callable interfaces:

| Callable | Signature | Responsibility |
|---|---|---|
| `LightweightChangeContractError.to_payload` | `(self) -> dict[str, object]` | Return exactly `schema_version: 1`, `result: invalid`, and `error: {category, detail}` for exit-1 contract failures |
| `LightweightChangeScan.to_payload` | `(self) -> dict[str, object]` | Derive deterministic counts, rows, oldest pending record, trigger reasons, and result from immutable parsed records |
| `discover_memory_root` | `(project_root: Path) -> Path | None` | Resolve one accepted root, return `None` when neither exists, and fail closed when both exist |
| `parse_change` | `(memory_root: Path, path: Path, *, as_of: date) -> LightweightChange` | Validate one path/content contract and return a normalized immutable record |
| `build_scan` | `(project_root: Path, *, as_of: date) -> LightweightChangeScan` | Discover the root, enumerate every month, parse every Change, and build the immutable scan model |

Required constants:

```python
MONTH_RE = re.compile(r"^\d{4}-(?:0[1-9]|1[0-2])$")
CHANGE_FILE_RE = re.compile(
    r"^(?P<date>\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]))-"
    r"(?P<topic>[a-z0-9][a-z0-9-]*)\.md$"
)
REQUIRED_SECTIONS = (
    "Background",
    "Goal / Completion Criteria",
    "Scope",
    "Lane Rationale",
    "Impact / Risk",
    "Plan",
    "Current Progress",
    "Verification",
    "Rollback",
    "Human Gates",
    "Result / Residuals",
    "Memory",
)
```

Validation table:

| Check | Required behavior |
|---|---|
| Project root | exists, is a real directory, and is not silently created |
| Memory roots | both `.agent-loop/` and `agent-loop/` present => `memory-root` error; one real directory present => use it; an accepted path that exists as a file or symlink fails; neither => empty valid scan |
| Changes root | absent => empty valid scan; present but not a real directory, or symlinked => fail; no writes |
| Layout | only month directories directly under `changes/` and matching Markdown files directly below them; any flat file, extra nesting, symlinked month/file, malformed month, or malformed Markdown filename fails |
| Month/date | month directory, filename date, and `Created At` `YYYY-MM-DD` must agree and be real calendar dates |
| Topic | H1 must be exactly `# Lightweight Change: <topic>` and equal the filename topic including collision suffix |
| Header metadata | exactly one each of `Record Version`, `Status`, `Created At`, `Updated At`, `Completed At`, `Git Context` before the first H2 |
| Record version | exactly `1` |
| Dates | `Created At <= Updated At <= as_of`; `completed` additionally requires `Created At <= Completed At <= Updated At`; non-completed uses `Completed At: none` |
| Git context | `no-git` or a nonblank branch followed by the final `@` and a full lowercase 40- or 64-hex SHA; a valid branch may itself contain `@` |
| Sections | every required H2 outside fenced Markdown occurs exactly once and has nonblank content; headings and metadata inside valid backtick/tilde fences are evidence only; `none` must include a concrete reason |
| Authoring markers | generated runtime cards reject template `<replace...>` markers outside valid fenced evidence; malformed fences cannot hide them |
| Memory metadata | exactly one nonblank value each for `Memory Review`, `Memory Result`, `Memory Evidence`, `Memory Target` inside `## Memory`; a not-applicable value uses `none: <concrete reason>`, never bare `none` |
| Initial pending markers | `pending: verification not complete` and `pending: classify at completion` are valid only for `in-progress`; `completed/pending` requires an actual verification locator and candidate target or concrete target-undecided reason |
| Memory combination | `pending/pending`; or `complete` with `none | synced | human-review`; all other pairs fail |
| Status/memory | `in-progress` requires `pending/pending`; `stopped` requires `complete/none`; `completed` allows either valid pair |
| As-of | a completed date after `--as-of` fails instead of producing negative age |
| Text | UTF-8, UTF-8 BOM, LF, and CRLF are accepted through `checker_support.read_text`; decode errors fail closed |
| File size | reject Change Markdown above 1 MiB to avoid unbounded evidence payloads |
| Ordering | sort by project-relative POSIX path; never depend on filesystem enumeration order |

Non-Markdown files inside a valid month directory are ignored by the Change scanner. The scanner must still reject Markdown files that attempt a second layout, README, INDEX, or archive locator because their names do not match the Change pattern.

Stable exit-1 error categories are owned as follows:

| Category | Owning failures |
|---|---|
| `memory-root` | dual accepted roots; accepted root exists as a file or symlink; ambiguous root ownership |
| `layout` | invalid changes-root shape, flat file, malformed month/name, extra depth, symlink/path escape, or directory enumeration failure |
| `metadata` | unreadable text, H1/topic mismatch, record version, duplicate/missing/blank metadata or sections |
| `state` | invalid Status/Memory values or combinations |
| `date` | invalid calendar value, path/date mismatch, reversed/future ordering |
| `size` | Markdown file exceeds 1 MiB |

Every error detail names the project-relative POSIX path and failing field/rule where one exists. Filesystem `OSError` from directory enumeration is normalized through the same contract. It must not emit an absolute temporary path, traceback, file body, secret, or raw evidence payload.

## Task 0: Re-establish Live Baseline And Protect Scope

**Files:**
- Read: `AGENTS.md`
- Read: `SKILL.md`
- Read: `references/runtime.md`
- Read: `references/design.md`
- Read: `docs/proposal/v1.5.x/persistent-lightweight-execution-card-and-memory-consolidation.md`
- Read: `docs/maintenance/full-validation-method.md`
- Create later: `docs/reports/agent-loop-v1.5.0-persistent-lightweight-change-red-baseline-2026-07-18.md`

- [x] **Step 0.1: Confirm exact branch, baseline, and dirty scope**

Run:

```bash
git status --short --branch
git rev-parse HEAD
git branch --show-current
git diff --stat
git ls-files --others --exclude-standard
```

Expected:

```text
branch = alpha/v1.5.0
HEAD = 200a23b85b5b0e3ebe68496f5f4a16d923d46788
only the approved Proposal and this plan are untracked
no unrelated tracked modification exists
```

Stop if reality differs. Do not hide an overlap by staging, reverting, or rewriting it.

- [x] **Step 0.2: Load required implementation and verification helpers**

Read completely before stage actions:

```text
references/skill-routing.md
references/external-skill-adapters.md
/Users/shaodowyd/.codex/skills/executing-plans/SKILL.md
/Users/shaodowyd/.codex/skills/test-driven-development/SKILL.md
/Users/shaodowyd/.codex/skills/systematic-debugging/SKILL.md when an unexpected failure occurs
/Users/shaodowyd/.codex/skills/verification-before-completion/SKILL.md before completion claims
/Users/shaodowyd/.codex/skills/requesting-code-review/SKILL.md before final handoff
```

Record actual availability and loaded/fallback status in this plan's execution evidence. Do not create a target-project Feature solely for helper logging.

- [x] **Step 0.3: Run the current untouched live baseline**

Run:

```bash
bash tests/validate-lightweight-change-lane.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
```

Expected before new RED tests:

```text
existing Lightweight Change focused contract = PASS
existing Python suite = PASS with a freshly reported count
```

Also record the current shell inventory without mutating files:

```bash
find tests -maxdepth 1 -type f -name '*.sh' | sort | wc -l
```

- [x] **Step 0.4: Create the RED baseline report shell**

Create `docs/reports/agent-loop-v1.5.0-persistent-lightweight-change-red-baseline-2026-07-18.md` with:

```markdown
# Agent Loop v1.5.0 Persistent Lightweight Change RED Baseline

日期：2026-07-18
分支：alpha/v1.5.0
基线：200a23b85b5b0e3ebe68496f5f4a16d923d46788
审计对象：当前工作区，RED 测试加入前后分别记录

## 设计缺口

- 当前卡片仅 response-local，任务重入后没有持久事实源。
- 当前运行面明确禁止 `.agent-loop/changes/`。
- 当前没有月份布局、状态校验、3 个 / 7 天累计扫描或记忆候选连续性。

## 既有基线

- Focused：记录 Step 0.3 实际命令、退出码、通过数和失败数。
- Python：记录 Step 0.3 实际命令、退出码、通过数和失败数。
- Shell inventory：记录 Step 0.3 实际命令与脚本数量。

## Focused RED

- 记录 Task 1 实际 focused 命令与退出码。
- 摘录第一条能够证明旧 response-local 契约仍存在的相关失败。

## Python RED

- 记录 Task 1 实际 Python 命令与退出码。
- 摘录第一条能够证明 scanner/support 尚不存在的相关失败。

## 保留边界

- Lightweight / Bug / Feature 路由和所有 Human Gate 不降低。
- 本报告不是 GREEN 或发布证据。
```

Replace each recording instruction with live command/output evidence before leaving Task 1. Do not copy the 2026-07-17 report's totals.

## Task 1: Add Focused And Python RED Contracts

**Files:**
- Create: `tests/lightweight_change_test_support.py`
- Create: `tests/test_lightweight_change_scan.py`
- Modify: `tests/validate-lightweight-change-lane.sh`
- Modify: `tests/test_python_checker_contract.py`
- Read: `.github/workflows/cross-platform-checkers.yml`
- Update: `docs/reports/agent-loop-v1.5.0-persistent-lightweight-change-red-baseline-2026-07-18.md`

- [x] **Step 1.1: Create the dynamic Change fixture helper**

Create `tests/lightweight_change_test_support.py` with these public helpers and the complete card factory:

```python
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from tests.checker_test_support import ROOT


CARD = """# Lightweight Change: {topic}

Record Version: 1
Status: {status}
Created At: {created_at}
Updated At: {updated_at}
Completed At: {completed_at}
Git Context: feature/v1.5.0/example@0123456789abcdef0123456789abcdef01234567

## Background

Bounded internal change with confirmed authority.

## Goal / Completion Criteria

Apply the declared change and pass the declared verification.

## Scope

- `scripts/example.py`

## Lane Rationale

Low risk, enumerable consumers, exact verification, and concrete rollback.

## Impact / Risk

Internal only; no public, data, permission, security, or architecture boundary.

## Plan

- [x] Inspect the exact change point.
- [x] Apply only the disclosed change.
- [x] Run targeted verification and review the diff.

## Current Progress

Implementation and verification complete.

## Verification

`python3 -m py_compile scripts/example.py` exited 0 in this run.

## Rollback

Restore the previous literal in `scripts/example.py` and rerun verification.

## Human Gates

Commit, push, release, and external effects remain separately gated.

## Result / Residuals

Declared internal change completed; no known residual.

## Memory

Memory Review: {memory_review}
Memory Result: {memory_result}
Memory Evidence: {memory_evidence}
Memory Target: {memory_target}
"""


@dataclass
class ChangeWorkspace:
    project_root: Path
    root_name: str = ".agent-loop"

    @property
    def memory_root(self) -> Path:
        return self.project_root / self.root_name

    def change(
        self,
        created_at: str,
        topic: str,
        *,
        status: str = "completed",
        updated_at: str | None = None,
        completed_at: str | None = None,
        memory_review: str = "pending",
        memory_result: str = "pending",
        memory_evidence: str = "verified code and focused test",
        memory_target: str = ".agent-loop/project.md Capabilities",
        month: str | None = None,
        filename: str | None = None,
    ) -> Path:
        updated = updated_at or created_at
        completed = completed_at or (created_at if status == "completed" else "none")
        actual_month = month or created_at[:7]
        name = filename or f"{created_at}-{topic}.md"
        path = self.memory_root / "changes" / actual_month / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            CARD.format(
                topic=topic,
                status=status,
                created_at=created_at,
                updated_at=updated,
                completed_at=completed,
                memory_review=memory_review,
                memory_result=memory_result,
                memory_evidence=memory_evidence,
                memory_target=memory_target,
            ),
            encoding="utf-8",
            newline="\n",
        )
        return path


def run_scan(project_root: Path, *, as_of: str = "2026-07-18") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/scan-lightweight-changes.py"),
            "--project-root",
            str(project_root),
            "--as-of",
            as_of,
        ],
        cwd=str(ROOT),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def json_output(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    return json.loads(result.stdout)


def tree_snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }
```

- [x] **Step 1.2: Add scanner RED tests before creating the scanner**

Create `tests/test_lightweight_change_scan.py`. Use `tempfile.TemporaryDirectory`, `ChangeWorkspace`, `run_scan`, `json_output`, and `tree_snapshot`. Implement these exact test methods and assertions:

| Test method | Required setup and observable result |
|---|---|
| `test_no_memory_root_is_empty_and_read_only` | Start without either accepted root; assert exit 0, null roots, zero counts, empty arrays, `not-triggered`, and an unchanged tree snapshot |
| `test_existing_root_without_changes_is_empty_and_read_only` | Start with exactly one accepted root but no `changes/`; assert exit 0, the selected root, null changes root, zero counts, and no directory creation |
| `test_two_pending_changes_do_not_trigger_count` | Write two completed/pending Changes; assert pending 2 and no `pending-count` reason |
| `test_three_pending_changes_across_months_trigger_count` | Write three completed/pending Changes in at least two month directories; assert pending 3 and exactly `pending-count` when all are younger than eight days |
| `test_exactly_seven_days_does_not_trigger_age` | Set `as_of - Completed At` to seven calendar days; assert no `pending-age` reason |
| `test_more_than_seven_days_triggers_age` | Set the difference to eight calendar days; assert exactly `pending-age` when pending count is below three |
| `test_in_progress_stopped_and_complete_do_not_count_pending` | Mix in-progress/pending, stopped/none, completed/none, and completed/synced; assert only completed/pending contributes |
| `test_human_review_is_reported_separately` | Write completed/complete/human-review; assert pending count 0 and the path appears in `human_review_changes` |
| `test_existing_legacy_root_is_reused` | Create only `agent-loop/`; assert the returned root is `agent-loop` and `.agent-loop/` is not created |
| `test_dual_memory_roots_fail_closed` | Create both accepted roots; assert exit 1, `result: invalid`, and a stable root-conflict category |
| `test_invalid_root_shapes_fail_closed` | Exercise accepted-root file/symlink and changes-root file/symlink; assert exit 1 and no mutation; skip only a symlink subcase when the host explicitly denies symlink creation |
| `test_month_filename_and_created_at_must_match` | Vary directory month, filename date, and `Created At`; assert every mismatch exits 1 with stable layout/date categories |
| `test_collision_suffix_is_part_of_topic_identity` | Write a valid `topic-2` filename/H1 pair, then a mismatched unsuffixed H1; assert the first passes and the second exits 1 |
| `test_flat_and_extra_nested_markdown_are_invalid` | Put a Markdown file directly under `changes/` and another below an extra directory level; assert exit 1 for both layouts |
| `test_non_markdown_month_companion_is_ignored` | Put one valid card and one non-Markdown regular file in a valid month; assert only the card is counted and neither file changes |
| `test_date_order_and_future_metadata_are_rejected` | Exercise future Created/Updated/Completed dates and reversed Created/Completed/Updated order; assert every invalid ordering exits 1 |
| `test_required_sections_and_memory_combinations_are_validated` | Remove each required section, exercise every valid/invalid state-memory pair, and try carrying initial pending markers into completed; assert valid pairs pass and invalid/unfinished combinations exit 1 |
| `test_invalid_as_of_is_usage_exit_two` | Pass a non-ISO date; assert exit 2, empty stdout, and argparse text on stderr |
| `test_missing_project_root_is_usage_exit_two` | Pass a missing path and a regular file; assert exit 2, empty stdout, and usage/capability text on stderr |
| `test_valid_scan_is_deterministic_and_read_only` | Run twice without edits; assert identical stdout/stderr/exit code and identical tree snapshots |
| `test_utf8_bom_and_crlf_are_accepted` | Write a valid card with BOM and CRLF; assert normalized parsing succeeds |
| `test_oversized_change_is_rejected` | Write a card larger than 1 MiB; assert exit 1 with the stable size category before unrestricted content parsing |
| `test_scanner_modules_use_only_stdlib_and_declared_local_support` | Parse imports from both new modules; assert the support module uses only stdlib plus `checker_support`, and the CLI uses only stdlib plus both declared local modules |

Key assertions must be literal, not snapshot-only:

```python
self.assertEqual(payload["result"], "triggered")
self.assertEqual(payload["trigger_reasons"], ["pending-count"])
self.assertEqual(payload["counts"]["pending"], 3)
self.assertEqual(payload["oldest_pending"]["age_days"], 0)
self.assertEqual(payload["memory_root"], ".agent-loop")
self.assertEqual(tree_snapshot(workspace.project_root), before)
```

For invalid artifact cases, require exit 1 plus JSON:

```python
self.assertEqual(result.returncode, 1)
payload = json_output(result)
self.assertEqual(payload["result"], "invalid")
self.assertIn(payload["error"]["category"], {"layout", "metadata", "state", "date", "memory-root", "size"})
```

Use a separate temporary directory per invalid subcase so one invalid artifact cannot mask another. Symlink coverage may skip only when the host refuses symlink creation; the production implementation must still reject symlinks.

- [x] **Step 1.3: Turn the focused shell contract RED**

Modify `tests/validate-lightweight-change-lane.sh` before runtime docs. Replace old positive assertions for response-local/no-directory behavior with positive assertions for:

```text
The card file is the execution source of truth.
<memory-root>/changes/YYYY-MM/YYYY-MM-DD-<topic>.md
pending_count >= 3
as_of_date - oldest_completed_at > 7 days
exactly 7 days does not trigger
monthly partition is not archive
code merge completes before Target memory reconciliation
scripts/scan-lightweight-changes.py
```

Add negative assertions that the Lightweight sections no longer contain:

```text
The card is response-local by default.
Do not create `.agent-loop/changes/`
no default `.agent-loop/changes/` directory
creates no persistent target-project artifact
```

Do not globally ban the phrase `response-local`; it remains correct for unrelated helper routing, Concept reopening, and chat drafts.

Require new files and scenario headings, but do not create implementation files yet. Keep existing Bug/Feature precedence, no-new-stage/status/mode, targeted RED/GREEN, scope-expansion, root block count, version `1.5.0`, source-repository no-`.agent-loop`, and Git gate assertions.

- [x] **Step 1.4: Register the future command and test in the checker contract**

Modify `tests/test_python_checker_contract.py`:

```python
LIGHTWEIGHT_CHANGE_COMMANDS = (
    "scripts/scan-lightweight-changes.py",
)
```

Add it to existence, stdlib/local-import, missing-arguments exit-2, supported-Python, CI inventory, and read-only deterministic checks. Allowed local imports are exactly:

```python
{"checker_support", "lightweight_change_support"}
```

Require `.github/workflows/cross-platform-checkers.yml` to contain `tests.test_lightweight_change_scan` and `scripts/scan-lightweight-changes.py`; do not update the workflow until GREEN Task 2.

- [x] **Step 1.5: Run and retain the real RED**

Run:

```bash
bash tests/validate-lightweight-change-lane.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_lightweight_change_scan \
  tests.test_python_checker_contract
```

Expected:

```text
focused shell = FAIL on the first missing persistent-card/scanner contract
Python = FAIL because scripts/scan-lightweight-changes.py and support behavior do not exist and CI is not registered
```

If either suite passes completely, strengthen the RED until it proves the approved gap. Record exact commands, exit codes, and first relevant failures in the RED report before implementation.

## Task 2: Implement The Read-Only Cross-Platform Scanner

**Files:**
- Create: `scripts/lightweight_change_support.py`
- Create: `scripts/scan-lightweight-changes.py`
- Modify: `.github/workflows/cross-platform-checkers.yml`
- Modify: `tests/test_python_checker_contract.py` only if RED exposed a contract mistake
- Test: `tests/test_lightweight_change_scan.py`
- Test: `tests/test_python_checker_contract.py`

- [x] **Step 2.1: Implement error, data, and payload models**

In `scripts/lightweight_change_support.py`:

- import only Python stdlib plus `checker_support.read_text`;
- define the public types from `Change Parser Contract`;
- normalize every emitted path with `relative_to(project_root).as_posix()`;
- make `to_payload()` derive counts, pending/human-review rows, oldest pending, age, reasons, and result from immutable parsed records;
- sort every list before serialization;
- do not store an independent pending counter.

Payload derivation must implement:

```python
pending = [
    item
    for item in changes
    if item.status == "completed" and item.memory_review == "pending"
]
human_review = [
    item
    for item in changes
    if item.status == "completed" and item.memory_result == "human-review"
]
reasons = []
if len(pending) >= 3:
    reasons.append("pending-count")
if pending and (as_of - min(item.completed_at for item in pending)).days > 7:
    reasons.append("pending-age")
```

Guard the type assumption: every counted pending item must already have a non-null `completed_at` from parser validation.

- [x] **Step 2.2: Implement memory-root and monthly-layout discovery**

`discover_memory_root()` must:

```text
resolve project_root without creating it
reject missing/non-directory project root as usage/capability exit 2
reject symlinked project root when it escapes the requested boundary
if either accepted root path exists as a file or symlink: memory-root error exit 1
if both .agent-loop and agent-loop are real directories: memory-root error exit 1
if exactly one real directory exists: return it
if neither exists: return None
never mkdir, touch, rename, or rewrite
```

`build_scan()` must inspect only `<memory-root>/changes` when present. Validate one month level and one Markdown file level. Reject any flat file under `changes/`, extra directories, symlinked directories/files, malformed months, invalid Change filenames, README/INDEX/archive Markdown, and path escape. Ignore non-Markdown regular files only when they are inside a valid month directory; do not execute or parse them.

- [x] **Step 2.3: Implement exact card parsing**

Parser order:

1. reject symlink/non-regular file and file size above `1024 * 1024` bytes;
2. read using `checker_support.read_text`;
3. parse H1 and top metadata only before the first H2;
4. require each top field exactly once;
5. require each H2 exactly once and nonblank;
6. parse Memory metadata only inside `## Memory` and require each exactly once;
7. parse real ISO dates;
8. check path month, filename date, topic, and Created At agreement;
9. check status/date/Git/memory combinations;
10. return an immutable `LightweightChange`.

Use bounded regular expressions and explicit duplicate counts. Do not reuse the first-match-only `checker_support.metadata()` for fields whose duplicate detection is required.

- [x] **Step 2.4: Implement the thin CLI**

Create executable `scripts/scan-lightweight-changes.py`:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from checker_support import configure_utf8_stdio, require_supported_python
from lightweight_change_support import (
    LightweightChangeContractError,
    build_scan,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scan persistent Lightweight Change cards without mutation"
    )
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--as-of", required=True)
    return parser


def main() -> int:
    configure_utf8_stdio()
    require_supported_python()
    arguments = build_parser().parse_args()
    try:
        as_of = date.fromisoformat(arguments.as_of)
    except ValueError:
        print("usage: --as-of must be YYYY-MM-DD", file=sys.stderr)
        return 2
    try:
        scan = build_scan(Path(arguments.project_root), as_of=as_of)
    except LightweightChangeContractError as error:
        if error.exit_code == 2:
            print(f"usage error: {error.detail}", file=sys.stderr)
        else:
            print(json.dumps(error.to_payload(), ensure_ascii=False, sort_keys=True, indent=2))
        return error.exit_code
    print(json.dumps(scan.to_payload(), ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Add `to_payload()` to the error class so failures use the invalid JSON contract. Then run:

```bash
chmod +x scripts/scan-lightweight-changes.py
PYTHONDONTWRITEBYTECODE=1 python3 -c '
from pathlib import Path
for name in ("scripts/lightweight_change_support.py", "scripts/scan-lightweight-changes.py"):
    compile(Path(name).read_text(encoding="utf-8"), name, "exec")
'
```

Expected: exit 0 and no `__pycache__`; this syntax check must not generate bytecode that later cleanup could accidentally confuse with a source change.

- [x] **Step 2.5: Add the native cross-platform CI entry**

Modify `.github/workflows/cross-platform-checkers.yml` in the existing macOS/Windows × Python 3.10/3.x job. Add `tests.test_lightweight_change_scan` to the existing `python -m unittest` module list. Add a separate native entrypoint step:

```yaml
      - name: Check Lightweight Change command entrypoint
        run: python scripts/scan-lightweight-changes.py --help
```

Do not create a new workflow, shell launcher, Ruby implementation, or platform branch. The Python test suite must run natively on Windows and macOS.

- [x] **Step 2.6: Reach scanner GREEN**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_lightweight_change_scan \
  tests.test_python_checker_contract
```

Expected: all selected tests PASS. Then run twice against one temporary fixture and prove identical stdout plus unchanged tree snapshot. Do not mark Task 2 complete if only direct module tests pass but CLI/CI contract fails.

## Task 3: Replace Response-Local Runtime Authority With The Persistent Card

**Files:**
- Modify: `references/lightweight-change-lane.md`
- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Modify: `references/concepts.md`
- Modify: `references/artifact-rules.md`
- Modify: `templates/lightweight-execution-card.md`
- Test: `tests/validate-lightweight-change-lane.sh`

- [x] **Step 3.1: Make the accuracy principle normative**

Add the approved principle to `references/design.md` and `references/lightweight-change-lane.md`:

```text
The lane reduces ceremony and document depth, not accuracy, scope control, verification strength, rollback, fact review, or Human Gates. Low risk, enumerable impact, and exact failure-matched verification are entry conditions.
```

Preserve all-of eligibility, any-of Feature hard triggers, explicit Bug precedence, active Feature ownership, uncertain zero-write Human Choice, and scope-expansion stop.

- [x] **Step 3.2: Define the persistent source of truth and create-before-write order**

Replace only Lightweight-specific response-local statements with:

```text
The persisted card file is the execution source of truth. The Agent may summarize it in the current response, but must create it after clearly-eligible routing and before the first target code/config/docs write.
```

Canonical flow:

```text
minimum Project Entry checks
-> Lightweight Change Assessment
-> clearly eligible
-> disclose Scope / Plan / Verification / Rollback / Gates
-> select the one accepted memory root, or default .agent-loop when neither exists
-> create changes/YYYY-MM/YYYY-MM-DD-topic.md
-> first target write
-> update progress and evidence
```

No write occurs for `uncertain`, explicit Bug, or Feature-hard-trigger routes.

- [x] **Step 3.3: Define monthly path and non-archive stability**

Across core authority, require:

```text
<memory-root>/changes/YYYY-MM/YYYY-MM-DD-<topic>.md
```

The month equals filename date and `Created At`. State/memory/commit/release changes never move the file. No `archive.md`, INDEX, README, move, rehydrate, archive state, or archive Human Gate exists. Pending scans cover every month.

Before creation, check the exact candidate path. If it exists, select the first unused numeric suffix (`-2`, then `-3`, and so on), use that suffixed topic in both filename and H1, and never truncate or overwrite an existing Change.

- [x] **Step 3.4: Define minimal states and completion invariants**

In `references/artifact-rules.md`, document the exact valid combinations from the parser contract. Keep status values distinct from Feature/task/Bug lifecycles. A `completed` card still requires Plan closure, fresh targeted verification, diff/scope review, concrete rollback, Result/Residuals, and a valid Memory Review state.

The initial `pending: verification not complete` / `pending: classify at completion` values are valid only while `Status: in-progress`. Before `completed`, replace them with the actual verification locator plus a concrete candidate target/reason, or finish classification as `none`, `synced`, or `human-review` with matching evidence and target.

Do not allow `completed` to mean code-only completion.

- [x] **Step 3.5: Replace the template with the persistent contract**

Rewrite `templates/lightweight-execution-card.md` to match the exact parser headings and metadata from the Proposal. Template fields may contain explicit authoring instructions, but every generated runtime artifact must replace them with concrete values before completion. Include every metadata line below, followed by all 12 required sections in `REQUIRED_SECTIONS` order:

```text
Record Version: 1
Status: in-progress
Created At:
Updated At:
Completed At: none
Git Context:
Memory Review: pending
Memory Result: pending
Memory Evidence: pending: verification not complete
Memory Target: pending: classify at completion
```

At the top, state the destination pattern and that the file must exist as a parser-valid artifact before the first target write. Require the Agent to replace every blank or authoring instruction, including Created/Updated/Git Context and every section body, before saving the generated card. Remove `Response-local by default` and `Do not copy this template into a target project by default`.

- [x] **Step 3.6: Preserve adaptive Plan and helper boundaries**

The card stays lightweight:

- no construction-grade Feature `plan.md`;
- no mandatory Plan Gate / Plan or Execute Task / Story helper resolution;
- no Feature tasks/tests/notes files;
- targeted TDD only for isolatable behavior logic;
- mechanical fact/config/docs changes use failure-matched checks;
- promotion to Feature restores normal helper/TDD protocol.

Run the focused shell test. It may remain RED on memory/root/human docs not yet updated, but no core response-local/no-directory assertion may survive.

## Task 4: Add Recovery, Memory Consolidation, And Post-Merge Semantics

**Files:**
- Modify: `references/project-memory-mode.md`
- Modify: `references/memory-reconciliation.md`
- Modify: `references/branch-management.md`
- Modify: `references/submit-and-integrate.md`
- Modify: `references/lightweight-change-lane.md`
- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Test: `tests/validate-lightweight-change-lane.sh`
- Test: `tests/test_lightweight_change_scan.py`

- [x] **Step 4.1: Distinguish accidental recovery from planned durable work**

Allow one interrupted `in-progress` card to resume only after re-checking:

```text
current branch
current full HEAD
dirty work
target files and consumers
persisted Scope / Plan / Progress
current eligibility, verification, and rollback
```

If any fact diverges, stop with Human Choice. Planned multi-session execution, pause/resume lifecycle, handoff, Subagent, long observation, or complex evidence remains a Feature hard trigger.

- [x] **Step 4.2: Define scan and trigger ownership**

At Project Entry when Changes exist, after every Change completion, and before release or memory reconciliation, the Agent must run:

```text
macOS/POSIX: python3 <skill-root>/scripts/scan-lightweight-changes.py --project-root <target-project-root> --as-of <current-local-date>
Windows: py -3 <skill-root>\scripts\scan-lightweight-changes.py --project-root <target-project-root> --as-of <current-local-date>
```

The controller interprets:

- scanner `pending-count` / `pending-age` => proactive Change Memory Consolidation;
- known memory drift + any relevant Change evidence => immediate consolidation/recovery routing;
- pre-release + pending/human-review => resolve/report before release recommendation;
- verified post-merge => Post-Merge Memory Reconciliation consumes Change evidence.

Do not add a canonical stage, message intent, scheduler, or background process.

- [x] **Step 4.3: Implement evidence-based automatic sync rules in prose**

Update `references/project-memory-mode.md` and the lane reference with all eleven Proposal conditions. Direct Agent sync requires an existing reliable accepted project memory structure, exact target path, verified stable fact, no conflict/new decision, branch/release/customer scope, pre-write disclosure, post-check, and rollback.

Only a changes-only root means:

```text
do not create project.md
do not create enterprise project/*.md
do not switch memory mode
classify no-value as none
route valuable candidate to Human Review / Project Entry recommendation
```

Project memory never stores card history, pending backlog, command logs, or copied Change bodies.

- [x] **Step 4.4: Keep unresolved human candidates visible**

Define `Memory Review: complete` + `Memory Result: human-review` as Agent classification complete / human decision outstanding. It does not count in automatic pending, but scanner and Agent reports keep surfacing it. Human resolution changes the result to `none` or `synced` with evidence, target, and decision locator.

Use Chinese table-first Human Review with only real choices and `高 | 一般` attention. Do not introduce icons, extra lifecycle, or a separate report file by default.

- [x] **Step 4.5: Preserve code-first merge order**

In `references/memory-reconciliation.md`:

- inventory monthly Change files in all four snapshots as evidence/artifact paths;
- treat Change execution evidence as append-only/current evidence according to actual content, not accepted Requirement/ADR authority;
- re-check Source `synced` claims against Merged Code and Target context;
- never import a Source memory fact only because its Change says `synced`;
- preserve the existing Start and Exact Plan Hash Human Gates, transaction, Apply, post-check, restore, Memory Commit, Push, Release, and cleanup sequence.

No existing memory-reconciliation Python operation is changed unless focused tests prove its path accounting excludes the new artifact family incorrectly. If code changes are necessary, add a new RED test before touching those scripts.

- [x] **Step 4.6: Add consolidation rollback and no-recursion rules**

Agent semantic consolidation must:

1. scan and validate;
2. group candidates by fact, not copy file bodies;
3. disclose target path/fact/evidence/impact/rollback before write;
4. update only owning memory files;
5. run format/reference/fact/residual checks;
6. restore only its own memory edits on failure;
7. leave sources pending on failure;
8. update source Memory fields after success;
9. never create a new Change merely to record consolidation.

## Task 5: Align Controller, Guides, Helpers, Root Guidance, And Human Docs

**Files:**
- Modify: `SKILL.md`
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/document-templates.md`
- Modify: `references/implementation-planning.md`
- Modify: `references/skill-routing.md`
- Modify: `references/external-skill-adapters.md`
- Modify: `references/project-guidance.md`
- Modify: `templates/root-AGENTS.md`
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`
- Modify: root revision-consuming tests/files listed in the File Responsibility Map
- Test: `tests/validate-lightweight-change-lane.sh`

- [x] **Step 5.1: Update the concise controller without copying the full reference**

In `SKILL.md`, update only Lightweight-specific lines:

- When To Use;
- package map;
- actionable non-Bug behavior;
- detailed reference load rule;
- working rules;
- stop conditions.

Mention the persistent monthly card, scanner, accidental resume, and memory consolidation briefly. Keep detailed eligibility and state combinations in `references/lightweight-change-lane.md`.

Do not modify unrelated response-local helper-resolution rules.

- [x] **Step 5.2: Update stage/checklist/template/helper boundaries**

Replace Lightweight-only response-local/no-directory assertions in the listed references. Preserve:

```text
card Plan is adaptive
card does not enter Feature Plan Gate
external writing-plans path does not apply
no docs/superpowers or Feature workspace
promotion restores mandatory helpers
scope expansion stops
all action-specific gates remain
```

Add checklist items for create-before-target-write, monthly path validation, status/progress update, scanner trigger check, memory result, sensitive evidence redaction, and no-archive stability.

- [x] **Step 5.3: Keep root guidance to one concise router line**

Replace bootstrap item 12a with one Agent-facing line equivalent to:

```text
Before creating a Feature for a bounded non-Bug change, assess Lightweight Change Lane; clearly eligible work persists one card under the active memory root at changes/YYYY-MM/YYYY-MM-DD-topic.md and the Agent checks pending memory consolidation, while unclear impact stops for a recommended human choice.
```

Keep the Stage Map row and detailed reference pointer. Do not copy the template, 3/7 matrix, state table, high-evidence conditions, or scanner JSON into root guidance.

Refresh every managed marker to:

```text
block-version:1.5.0-20260718
```

Update every live exact revision consumer listed earlier. Do not alter historical report/proposal snapshots solely to erase `20260717`.

- [x] **Step 5.4: Update human docs and current changelog section**

`README.md` and `Usage.md` should explain:

- the card is persisted before target writes;
- native scanner invocation uses `python3` on macOS/POSIX and `py -3` or `python` on Windows;
- monthly partition is stable and not archive;
- accidental recovery is possible but planned durable work is Feature;
- 3 pending / older than 7 days triggers proactive memory consolidation;
- high-evidence facts may sync, uncertain meaning goes to human;
- Git/production/external gates remain.

Update the existing `## 1.5.0 — 2026-07-17` Changelog section with a new subsection such as `### Persistent Lightweight Change Records`. Do not create `1.5.1`, change version surfaces, or rewrite the historical bullets that truthfully describe the first response-local implementation; add the follow-up behavior that supersedes it.

- [x] **Step 5.5: Verify same-version consistency**

Run:

```bash
rg -n 'Version:|"version"|Current version|版本：|## 1\.5\.0' \
  SKILL.md plugin.json README.md Usage.md CHANGELOG.md
rg -n '1\.5\.0-20260717|1\.5\.0-20260718' \
  SKILL.md README.md Usage.md CHANGELOG.md references templates tests
```

Expected:

```text
all current version surfaces remain 1.5.0
all 13 current root managed blocks and live tests use 1.5.0-20260718
old root revision appears only in clearly historical evidence or Changelog history
```

## Task 6: Expand Pressure Scenarios And Reach Focused GREEN

**Files:**
- Modify: `references/validation-scenarios.md`
- Modify: `tests/validate-lightweight-change-lane.sh`
- Test: `tests/test_lightweight_change_scan.py`
- Test: affected existing shell contracts

- [x] **Step 6.1: Add structured pressure scenarios**

Add scenarios with Prompt / Expected Route / Evidence / Required Action / Forbidden Action / Next for:

1. Persistent Card Exists Before First Target Write;
2. Monthly Partition Is Stable And Is Not Archive;
3. Same-Day Topic Collision Uses A Non-Overwriting Suffix;
4. Changes-Only Root Does Not Prove Initialization;
5. Accepted Legacy Root Is Reused;
6. Dual Memory Roots Stop In Recovery;
7. Accidental Context Loss Revalidates Card And Diff;
8. Planned Cross-Session Work Uses Feature;
9. Two Pending Changes Do Not Trigger Count;
10. Three Pending Changes Across Months Trigger Consolidation;
11. Exactly Seven Days Does Not Trigger;
12. Older Than Seven Days Triggers;
13. Human Review Candidate Remains Visible;
14. High-Evidence Sync Requires Existing Reliable Memory;
15. Automatic Sync Discloses Exact Memory Scope;
16. Scanner Does Not Perform Semantic Memory Writes;
17. Sensitive Evidence Is Redacted;
18. Source Change Does Not Override Target Before Code Merge;
19. Post-Merge Reconciliation Rechecks Change Evidence;
20. Scope Expansion Stops Persistent Card Execution;
21. Git Production And Release Gates Remain Separate.

Keep all prior Lightweight scenarios unless their response-local artifact expectation is superseded; update those expectations rather than duplicate contradictory scenarios.

- [x] **Step 6.2: Make focused assertions cross-surface and negative**

The focused shell test must verify at least:

- all new source/script/template/test files exist;
- canonical path and 3/7 exact inequalities occur in authority;
- same-day same-topic collisions allocate a suffix and never overwrite;
- monthly partition is not Archive;
- scanner is read-only/standard-library and not an automatic writer;
- changes-only and legacy/dual-root rules;
- status and memory combinations;
- accidental/planned cross-session distinction;
- high-evidence plus human-review boundary;
- post-merge code-first order;
- root reminder exactly once and 13/13 revision;
- no new canonical stage/message intent/Feature Type/Bug path/Auto Mode;
- no Change README/INDEX/archive transaction;
- no Git/external gate weakening;
- no stale Lightweight-only response-local/no-directory language in runtime authority.

Use path-scoped negative assertions so unrelated valid `response-local` text does not fail.

- [x] **Step 6.3: Run focused GREEN and affected regressions**

Run:

```bash
bash tests/validate-lightweight-change-lane.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_lightweight_change_scan \
  tests.test_python_checker_contract \
  tests.test_root_agents_blocks
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-root-agents-block-refresh.sh
bash tests/validate-v1.2.4-root-stage-coverage.sh
bash tests/validate-chat-requirements-entry.sh
bash tests/validate-bug-management.sh
bash tests/validate-branch-management-strategy.sh
bash tests/validate-project-local-skills.sh
bash tests/validate-project-skill-discovery-guard.sh
bash tests/validate-requirement-lifecycle-backlog.sh
bash tests/validate-mandatory-helper-routing.sh
```

Expected: every command PASS. If any unexpected failure appears, load `systematic-debugging`, reproduce the actual conflict, add a narrow RED assertion when the gap is real, and repair only the owning source.

## Task 7: Run Mandatory Full Validation And Refresh Reports

**Files:**
- Create: `docs/reports/agent-loop-v1.5.0-full-validation-2026-07-18.md`
- Update: `docs/reports/agent-loop-v1.5.0-persistent-lightweight-change-red-baseline-2026-07-18.md`
- Update after evidence: Proposal and this plan status blocks
- Read: `docs/maintenance/full-validation-method.md`

- [x] **Step 7.1: Run every shell test with live accounting**

Run:

```bash
shell_total=0
shell_pass=0
for test_file in tests/*.sh; do
  shell_total=$((shell_total + 1))
  if bash "$test_file"; then
    shell_pass=$((shell_pass + 1))
  else
    printf 'FAILED: %s\n' "$test_file" >&2
    exit 1
  fi
done
printf 'Shell: %s/%s PASS\n' "$shell_pass" "$shell_total"
```

Expected: every live `tests/*.sh` passes. Record the actual count; do not assume 39.

- [x] **Step 7.2: Run the complete Python suite**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
```

Expected: `OK` with a newly reported test count greater than the 182-test historical baseline because `test_lightweight_change_scan.py` is new.

- [x] **Step 7.3: Run mechanical checks**

Run:

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
python3 -m json.tool plugin.json >/dev/null
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
git diff --check
```

Run the repository Markdown fence balance check, include untracked Proposal/Plan/Report files, and confirm no `__pycache__`:

```bash
find . -type d -name '__pycache__' -print
```

Expected: YAML, JSON, every Shell syntax check, Markdown fences, diff whitespace, and pycache absence all PASS.

- [x] **Step 7.4: Run the six-domain semantic audit**

Follow `docs/maintenance/full-validation-method.md` and assess:

- Logic Correctness;
- Autonomy;
- Project Entry / Evidence Graph + DDD Onboarding;
- Development / Test Workflow;
- Memory;
- Recommendation.

Pressure at least:

```text
eligible small config fact -> persistent monthly card -> exact verification -> completed/pending
three pending across months -> proactive consolidation
seven-day boundary -> no off-by-one
changes-only root -> no false initialization
legacy root -> no dual root
accidental resume -> revalidation
planned handoff -> Feature
explicit Bug -> Bug Management
public/data/security change -> Feature
automatic memory sync -> exact evidence/no new decision
human-review -> remains visible
Source branch -> no Target overwrite before code merge
post-merge -> Change evidence rechecked
commit/release/production -> independent gate
```

Any Critical/High/Medium finding requires a real RED assertion, focused repair, and rerun of the full shell/Python/mechanical suites.

- [x] **Step 7.5: Write the fresh Chinese full-validation report**

Create `docs/reports/agent-loop-v1.5.0-full-validation-2026-07-18.md` with:

- date, branch, version, baseline and audit target;
- actual shell/Python totals;
- root block revision `1.5.0-20260718` and 13/13 count;
- six-domain score table and grade;
- RED baseline and GREEN closure;
- current findings by severity;
- passed invariants and pressure scenarios;
- scanner cross-platform/read-only evidence;
- remaining observation risk;
- explicit statement that commit/push/tag/release/publish and installed-Skill sync are unauthorized.

Do not overwrite or present the 2026-07-17 report as current.

## Task 8: Final Review, Artifact Status, And Development-Agent Stop

**Files:**
- Review: every changed/untracked file
- Update: `docs/proposal/v1.5.x/persistent-lightweight-execution-card-and-memory-consolidation.md`
- Update: this plan
- Update: RED/full reports only with live evidence

- [x] **Step 8.1: Run Proposal coverage review**

Map every Proposal acceptance criterion to:

```text
runtime/design/reference rule
template field/path
scanner behavior or explicit Agent semantic responsibility
focused assertion
Python/shell scenario
full-validation evidence
```

Do not claim coverage from Proposal prose alone.

- [x] **Step 8.2: Run final stale-rule and forbidden-artifact scans**

Run scoped searches:

```bash
rg -n 'response-local|Response-local|Do not create `\.agent-loop/changes|no default `\.agent-loop/changes|creates no persistent target-project artifact' \
  SKILL.md README.md Usage.md CHANGELOG.md \
  references templates tests

rg -n '\.agent-loop/changes/YYYY-MM-DD|changes/YYYY-MM-DD' \
  SKILL.md README.md Usage.md CHANGELOG.md \
  references templates tests

rg -n '1\.5\.0-20260717|1\.5\.0-20260718' \
  CHANGELOG.md references templates tests
```

Classify every remaining hit. Remove only stale Lightweight claims; preserve unrelated valid response-local rules and historical evidence.

Verify the source repository contains no generated target artifacts:

```bash
test ! -d .agent-loop
test ! -d templates/.agent-loop
```

- [x] **Step 8.3: Run final diff and scope review**

Run:

```bash
git status --short --branch
git diff --stat
git diff --check
git diff -- . ':(exclude)docs/reports/*'
git ls-files --others --exclude-standard
```

Confirm:

- every file belongs to the approved map;
- no version bump occurred;
- no secret/raw production evidence exists;
- no target `.agent-loop/` exists;
- no unresolved authoring marker exists;
- no installed Skill was synchronized;
- no Git action occurred.

- [x] **Step 8.4: Update statuses from real evidence only**

After focused/full validation passes:

- Proposal: `Proposal、实施、focused validation 与全量验证已完成，待最终 Human Review`;
- Plan: `Implementation Plan 已执行完成，待最终 Human Review`;
- check every plan box that actually completed;
- record actual test/report locators in the plan Handoff section.

If validation does not pass, keep truthful incomplete status and report the blocker. Do not mark implementation complete because time or budget ended.

- [x] **Step 8.5: Stop at Human Review**

Final development-Agent report must include:

- files created/modified;
- RED and GREEN evidence;
- actual focused/full totals;
- semantic audit result;
- remaining risk;
- worktree status;
- explicit no-stage/no-commit/no-push/no-tag/no-release/no-publish/no-installed-sync declaration;
- recommended next action: maintainer review, then separate Git gate if accepted.

Do not stage or commit.

## Rollback Strategy

During implementation:

- restore only files changed by the current task, using recorded pre-edit content or a narrow inverse `apply_patch`;
- never reset the worktree;
- keep RED tests/report even when implementation is rolled back, unless the human explicitly cancels the entire Proposal;
- if scanner implementation fails, remove only its new script/support/test files after confirming they are solely this task's work;
- if a root revision update is rolled back, restore all 13 blocks and every live revision consumer together;
- if full validation reveals a design conflict, stop and return to Proposal Human Review instead of weakening tests or gates.

## Plan Self-Review Checklist

- [x] Every Proposal section maps to at least one implementation task and one verification point.
- [x] Scanner types, field names, JSON keys, threshold inequality, and paths are consistent across Tasks 1-7.
- [x] The plan never asks the scanner to decide semantics or write memory.
- [x] The plan distinguishes no-root, legacy-root, dual-root, and changes-only states.
- [x] Monthly partition remains stable and is never called Archive lifecycle.
- [x] Exactly 7 days does not trigger; more than 7 does.
- [x] Three pending triggers; two does not.
- [x] `human-review` remains visible outside pending count.
- [x] Accidental resume does not permit planned cross-session work.
- [x] Code merge remains before Target memory reconciliation.
- [x] Root guidance stays concise and every managed revision moves together.
- [x] Skill version remains 1.5.0.
- [x] No task authorizes subagent/Git/release/external actions.
- [x] No unresolved implementation marker or undefined interface remains.

## Handoff

### 实施结果定位

- 基线：`alpha/v1.5.0`，`200a23b85b5b0e3ebe68496f5f4a16d923d46788`；Task 0 时仅本 Proposal 与本 Plan 未跟踪。
- RED：`docs/reports/agent-loop-v1.5.0-persistent-lightweight-change-red-baseline-2026-07-18.md`；focused Shell 先因缺持久卡契约失败，selected Python 42 tests 因 scanner/contract 缺口出现 59 failures、6 errors。
- 初始 GREEN：`tests/validate-lightweight-change-lane.sh` PASS；scanner/checker/root focused Python 50/50 PASS；计划列出的 affected Shell regressions 全部 PASS。
- 维护者验收修复：新增 6 个 scanner 回归方法，首轮 5 个方法产生 6 个预期失败，自审追加的无效 fence 用例再产生 1 个预期失败；目录错误归一化、authoring marker、fenced Markdown 和含 `@` 分支分别完成 RED → GREEN。
- 最终 GREEN：`tests/validate-lightweight-change-lane.sh` PASS；scanner/checker/root focused Python 56/56 PASS；计划列出的 affected Shell regressions 全部 PASS。
- Full validation：实时统计 `tests/*.sh` 为 39，39/39 PASS；Python 215/215 PASS；六域评分 98/100，未解决 Critical/High/Medium finding 为 0。
- 完整报告：`docs/reports/agent-loop-v1.5.0-full-validation-2026-07-18.md`；平台结论为 `macOS-verified / Windows-test-defined`。
- 停止点：Proposal、Plan 与报告均停在最终 Human Review；未 stage、commit、push、tag、PR、merge、release、publish，未同步 installed Skill。

Recommended execution Agent prompt after Plan Human Review:

```text
请在 agent-loop 源仓库的 alpha/v1.5.0 分支，严格执行 docs/proposal/v1.5.x/persistent-lightweight-execution-card-and-memory-consolidation-implementation-plan.md。

先读取仓库 AGENTS.md、Agent Loop controller、references/runtime.md、references/design.md、已确认 Proposal、计划和 full-validation 方法；解析并加载 executing-plans、test-driven-development、verification-before-completion、requesting-code-review，只有出现异常失败时才加载 systematic-debugging。

从 Task 0 开始，按 RED -> GREEN -> focused validation -> full validation 顺序执行。持久化卡路径必须是当前唯一 accepted memory root 下的 changes/YYYY-MM/YYYY-MM-DD-topic.md；扫描脚本只用 Python 3.10+ 标准库，只读、Windows/macOS 原生可用。保持 3 个 pending 或最早 pending 超过 7 天的触发规则，代码先合并、目标记忆后校准。不得降低 Lightweight / Bug / Feature 路由、验证、回滚或 Human Gate。

不要派发 Subagent，不要升级版本，不要同步到已安装 Skill，不要创建或切换分支/worktree，不要 stage、commit、push、tag、PR、merge、release、publish 或执行外部/生产动作。完成全部 focused/full validation、刷新 RED 和 2026-07-18 全量报告后，更新 Proposal/Plan 实施状态，停在最终 Human Review，等待维护者验收。
```

Plan writing complete condition: Proposal coverage, exact code/data/path contracts, RED/GREEN sequence, full validation, rollback, and Human Gates are explicit. Plan writing does not authorize execution.

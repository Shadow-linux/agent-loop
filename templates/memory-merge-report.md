# Memory Conflict Resolution Report

Memory Merge ID: MM-<merged-code-short-sha>-<conflict-topic>
状态: 待处理 | 待人类决定 | 已解决 | 已恢复
Created: YYYY-MM-DDTHH:MM:SSZ
Updated: YYYY-MM-DDTHH:MM:SSZ

> 仅列出观察到的冲突、为理解冲突所需的直接事实，以及实际重写结果。不要列出未变化文件、全目录哈希、缺失路径或机械性的“保留”决定。

## Merge Context

| Field | Value | Evidence |
|---|---|---|
| Merged Code SHA | `<full-sha>` | current verified HEAD |
| Source / Target | `<source>` → `<target>` | Git merge evidence |
| Memory Root | `.agent-loop` or `agent-loop` | accepted existing root |
| Conflict Locator | `<path, stable ID, or broken direct reference>` | observed conflict |

## Observed Memory Conflict

| Conflict ID | Conflicting claim | Why both cannot remain current | Directly affected owner / references |
|---|---|---|---|
| MC-001 |  |  |  |

## Minimum Direct Evidence

Only inspect evidence needed to decide the observed conflict.

| Evidence | Observed fact | Freshness / authority | Supports |
|---|---|---|---|
| merged code / test / config |  |  |  |
| accepted Requirement / ADR / Human Decision |  |  |  |
| current environment fact, when relevant |  |  |  |

## Agent Resolution

| Conflict ID | Resolution | Changed path | Exact preimage | Intended postimage | Direct references/indexes updated | Verification |
|---|---|---|---|---|---|---|
| MC-001 |  |  | `<sha256 or absent>` | `<sha256>` |  |  |

## Targeted Rollback

| Conflict ID | Rollback scope / backup evidence | Backup retention | Restore verification |
|---|---|---|---|
| MC-001 | only the changed preimage(s) | until targeted verification passes |  |

## Human Decision — Only If Still Unresolved

Do not ask the human to review fact-determined rewrites. If facts cannot select one valid meaning, present only the smallest concrete alternatives.

| Decision ID | Option A | Option B | Agent recommendation | Consequence | Human decision |
|---|---|---|---|---|---|
| none |  |  |  |  |  |

## Result

Resolution status: `resolved-by-agent | human-decision-required | resolved-after-human-decision | restored`

Targeted verification:

Remaining conflict or uncertainty:

Remaining risk:

Unrelated drift observed but not needed to resolve this conflict:

Explicitly unauthorized: commit, push, tag, release, publish, merge, branch deletion, Source branch cleanup, or any Git action outside a separate Human Gate.

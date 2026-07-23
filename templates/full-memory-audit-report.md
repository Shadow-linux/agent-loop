# Full Memory Audit / Recovery Report

Memory Merge ID: MM-<collision-safe-merged-code-short-sha>
状态: 待确认 | 已完成 | 已恢复
Created: YYYY-MM-DDTHH:MM:SSZ
Updated: YYYY-MM-DDTHH:MM:SSZ

## Merge Context

| Field | Value | Evidence |
|---|---|---|
| Merge Base SHA | `<full-sha>` | Git commit |
| Source SHA | `<full-sha>` | Git commit |
| Target-before SHA | `<full-sha>` | Git commit |
| Merged Code SHA | `<full-sha>` | current verified HEAD |
| Source Branch | `<branch>` | Git / accepted Branch Context |
| Target Branch | `<branch>` | Git / accepted Branch Context |
| Memory Root | `.agent-loop` or `agent-loop` | accepted existing root |

## Code Verification

| Check | Result | Evidence |
|---|---|---|
| Merged code verification | pass / fail | `<command or bounded procedure and actual result>` |
| HEAD equals Merged Code SHA | yes / no | `<full-sha>` |

## Customer Boundary

Value: `<standard | customer scope | none>`
Evidence:
Risk:

## Target Release Context

Value: `<accepted target release context | none>`
Evidence:

## Human Attention Summary

| Level | Meaning | Count | Recommended handling |
|---|---|---:|---|
| 🔴 | 必须决定 | 0 | resolve each or approved group before Plan review |
| 🟡 | 建议复核 | 0 | review as a bounded group |
| 🟢 | 普通变更汇总 | 0 | inspect summary |

### 必须决定

| Record / Path | Conflict | Evidence checked | Agent recommendation | Impact | Human decision |
|---|---|---|---|---|---|
| none |  |  |  |  |  |

### 建议复核

| Record / Path | Proposed action | Evidence | Recommendation / impact | Human decision |
|---|---|---|---|---|
| none |  |  |  |  |

### 普通变更汇总

| Action | Count | Paths / stable IDs | Evidence summary |
|---|---:|---|---|
| none | 0 |  |  |

## Memory Record Matrix

Action must be one of: 保留 | 引入 | 重写 | 重算 | 移除过时声明 | 暂不处理

Action and mutation must agree: 引入 starts absent; 重写 starts from the exact existing file preimage; 重算 may rebuild an absent derived file or replace its exact preimage; 移除过时声明 ends absent. Human-source and accepted-authority 引入 copies the same-path regular Git blob byte-for-byte.

| Record / Path | Semantic Role | Base | Source | Target-before | Result | Attention | Action | Intended Post-state | Authority / Evidence | Rationale | Operation ID |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  | 🟢 / 🟡 / 🔴 | 保留 / 引入 / 重写 / 重算 / 移除过时声明 / 暂不处理 |  |  |  | none |

## Human Decisions

| Decision ID | Blocking question | Agent recommendation | Human decision | Confirmed by | Confirmed at | Evidence / impact |
|---|---|---|---|---|---|---|
| none |  |  |  |  |  |  |

## Expected File Changes And Diffs

### Add / Introduce

| Path | Expected SHA-256 | Mode | Diff / source summary |
|---|---|---|---|

### Update / Rewrite / Recalculate

| Path | Preimage SHA-256 | Postimage SHA-256 | Mode | Expected diff summary |
|---|---|---|---|---|

### Remove Stale Agent-Maintained Claims

| Path | Preimage SHA-256 | Expected post-state | Expected diff summary |
|---|---|---|---|

### Expected Unchanged Paths

| Path | Expected SHA-256 | Reason / invariant |
|---|---|---|

## Exact Rewrite Plan

Normalized Plan Hash: `<64-lowercase-hex | not-ready>`

<!-- memory-reconciliation-plan:start -->
```json
{"schema_version":1,"report_id":"not-ready","plan_sha256":"not-ready"}
```
<!-- memory-reconciliation-plan:end -->

## Apply Result

Status: not-run | applied-checking | failed
Transaction ID:
Applied Plan Hash:
Operation evidence:
Unexpected effects:

## Post-check Result

Machine check: not-run | pass | fail
Zero-change rescan: not-run | pass | fail
Domain / semantic verification:
Expected unchanged paths:
Reference / identity / customer-boundary checks:
Finalization evidence:

## Restore / Remaining Risk

Restore status: not-needed | required | restored | failed
Restored transaction ID:
Restore evidence:
Remaining blocker / risk:
Explicitly unauthorized: commit, push, tag, release, publish, merge, branch deletion, Source branch cleanup, or any Git action outside a separate Human Gate.

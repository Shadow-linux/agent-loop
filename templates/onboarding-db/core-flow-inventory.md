# Core Flow Inventory

Document Language: 中文
Created:
Last Updated:
Last Verified:
Confidence:
Source Evidence:
Human Review Status: draft

## Purpose

从 Evidence Graph 识别需要 deep trace 的核心 flow，并区分 `required-core`、`supporting`、`unknown-core` 和 `not-core`。

## Core Flow Table

| Flow | Graph Node ID | Core Role | Why Core | Trigger | Entrypoints | Services | Data Read | Data Write | Async / External | Failure / Retry | Required Doc | Confidence | Completion Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Required Core Flow Rule

命中以下任一信号时，默认进入 `required-core`，除非写出证据理由并交给人类确认：

- 金额、余额、充值、退款、账单、扣费、手续费。
- 权限、身份、API Key、租户、用户组、折扣。
- 主请求路径、模型调用、provider 选择、usage 生成。
- 外部回调、异步消费、最终一致性、状态回写。
- 生产配置切换、配额、限流、计费、风控或发布风险。

## Deep Trace Priority

| Priority | Flow | Reason | Required Template | Target File | Blocker |
|---|---|---|---|---|---|
| P0 | | | `core-flow-deep-trace.md` | `flows/<core-flow>.md` | |

## Unknowns / Coverage Updates

| Flow | Unknown | Completion Impact | Coverage Matrix Row | Next Action |
|---|---|---|---|---|

# Change Impact Map

Document Language: 中文
Created:
Last Updated:
Last Verified:
Confidence:
Source Evidence:
Human Review Status: draft

## Purpose

Explain what may be affected when common files, modules, APIs, entities, jobs, or flows change.

## Impact Summary

| Change Area | Likely Affected Modules | APIs / Contracts | Data / State | Jobs / Async / External | Tests / Verification | Risk | Evidence |
|---|---|---|---|---|---|---|---|

## Common Change Paths

| If You Change | Check These Files | Check These Flows | Check These Tests | Manual / E2E Checks | Risk | Evidence | Confidence |
|---|---|---|---|---|---|---|---|

## How To Read

从左到右阅读这张影响地图。先定位你准备修改的文件、模块、API、实体、任务或流程，再顺着受影响模块、契约、数据/状态、异步/外部副作用和验证项继续检查。如果某一行置信度较低，把它当成风险处理，先查看 Evidence Chain 再开始修改。

## Step-by-Step Walkthrough: Change Propagation

```text
1. 【改动 MeetingService 的生成逻辑】首先检查 `modules/meeting-service.md` 中的 call chain 和依赖
2. 影响向上游传播：检查调用 MeetingService 的 API 路由和 Handler（API 层消费者）
3. 影响向下游传播：检查 MeetingService 调用的 Repository、External Service、Task Dispatcher（Data/External 层依赖）
4. 检查数据影响：Meeting 实体字段或状态是否受影响，是否需要数据库迁移
5. 检查异步影响：如果有后台任务依赖 MeetingService，检查 audio_tasks、minutes_tasks 是否需要更新
6. 检查测试影响：更新单元测试、集成测试，确认 E2E 场景仍通过
7. 检查边界影响：如果 MeetingService 暴露给外部系统，确认契约兼容性
8. 最终验证：运行受影响模块的测试，确认无回归
```

## Boundary Impact

| Boundary | Change Type | Downstream Consumers | Compatibility Risk | Suggested Contract / Handoff | Evidence | Confidence |
|---|---|---|---|---|---|---|

## Data / State Impact

| Entity / Field | Change Type | Writers | Readers / Consumers | State Trace | Tests | Evidence | Confidence |
|---|---|---|---|---|---|---|---|

## Evidence Chain

| File Path | Symbol / Object | Parameters / Fields | Description | Proves | Confidence |
|---|---|---|---|---|---|

## Unknowns

| Item | Why It Matters | Evidence | Suggested Follow-Up |
|---|---|---|---|

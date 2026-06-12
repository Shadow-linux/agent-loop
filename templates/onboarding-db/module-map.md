# Module Map

Document Language: 中文
Created:
Last Updated:
Last Verified:
Confidence:
Source Evidence:
Human Review Status: draft

## Purpose

## Module Relationship Map

Use a small relationship diagram for core modules or subsystems. Do not mirror the repo tree.

## How To Read

```text
这张模块关系图回答什么问题：
1. 项目的核心模块有哪些。
2. 模块之间谁调用谁、谁依赖谁。
3. 哪些区域只是 support-only，不需要独立模块详解。

怎么看：
- 先看入口模块。
- 顺着箭头看依赖方向。
- 再到 Core Module Index 找每个模块的一句话职责和详情文档。
- 不要把它当成完整目录树。
```

## Step-by-Step Walkthrough: Dependency Flow

```text
1. 请求从 User / Client 进入 API / Gateway 模块（入口层）
2. API 模块同步调用 Auth / Permission 模块进行身份校验
3. 校验通过后，API 模块同步调用 Meeting Service 模块处理业务
4. Meeting Service 同步调用 Meeting Repository 模块读写数据库
5. Meeting Service 异步触发 Audio Processing 模块处理录音（后台任务）
6. Audio Processing 模块异步调用 External ASR Service（外部服务）
7. ASR 回调回来后，Audio Processing 模块通知 Subtitle Service 生成字幕
8. Subtitle Service 同步调用 Subtitle Repository 写入字幕数据
9. 用户请求纪要时，Minutes Service 读取 Meeting + Subtitle 数据生成纪要
10. Minutes Service 同步调用 Minutes Repository 保存生成的纪要
```

## Core Module Index

| Module | Responsibility | Type | Detail Doc | Main Entrypoints | Related Flows | Key Data / Side Effects | Confidence |
|---|---|---|---|---|---|---|---|

## Support Areas

| Area | Responsibility | Why Not A Core Module Doc | Evidence | Confidence |
|---|---|---|---|---|

## Module Dependencies

| From | To | Direction | Why | Contract / Interface | Evidence | Confidence |
|---|---|---|---|---|---|---|

## Module Coverage

| Module | Has Detail Doc | Has Call Chain Diagram | Has Evidence Chain | Missing / Follow-Up |
|---|---|---|---|---|

## Evidence Chain

| File Path | Symbol / Object | Parameters / Fields | Description | Proves | Confidence |
|---|---|---|---|---|---|

## Unknowns

| Item | Why It Matters | Evidence | Suggested Follow-Up |
|---|---|---|---|

## Project Memory Backfill

| Candidate Fact | Backfill Target | Reason | Evidence | Confidence |
|---|---|---|---|---|

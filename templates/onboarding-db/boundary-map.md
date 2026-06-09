# Boundary Map

Document Language: 中文
Created:
Last Updated:
Last Verified:
Confidence:
Source Evidence:
Human Review Status: draft

## Purpose

Explain the project boundaries and call direction across UI, API, domain, DB, jobs, external services, auth, generated/shared packages, and runtime infrastructure.

## Boundary Diagram

Use a small diagram that shows boundary ownership and call direction. Do not draw every package or function.

## How To Read

```text
这张边界图回答什么问题：
1. UI、API、Domain、Data、Jobs、External 等边界分别负责什么。
2. 调用方向从哪里到哪里，哪些边界不能反向依赖。
3. 哪些跨边界接口可能需要 Delivery Contract 或兼容性说明。

怎么看：
- 先找外部入口。
- 顺着实线看同步调用。
- 顺着虚线看异步、队列、任务或回调。
- 对照 Boundary Index 查看证据和置信度。
```

## Step-by-Step Walkthrough: Boundary Call Flow

```text
1. 用户 / Client（UserLayer）发起请求，进入 UI / Browser / Mobile App 边界
2. 请求穿越 UI 边界，到达 API / Gateway 边界（API Layer）
3. API Gateway 进行认证/鉴权，然后转发到 Domain / Service 边界（Domain Layer）
4. Domain Service 执行业务规则，同步调用 Data / Repository 边界（Data Layer）读写数据
5. Domain Service 异步触发 Job / Worker / Queue（Runtime Layer），虚线箭头表示异步穿越
6. Worker 穿越 External / Third-Party 边界（External Layer）调用外部服务
7. 外部服务返回结果给 Worker，Worker 更新 Data Layer 状态
8. 最终响应沿原路返回：Data Layer → Domain Layer → API Layer → UserLayer
```

## Boundary Index

| Boundary | Responsibility | Owned By | Entrypoints | Depends On | Called By | Evidence | Confidence |
|---|---|---|---|---|---|---|---|

## Cross-Boundary Contracts

| From | To | Contract / Interface | Data / Event / API | Compatibility Risk | Evidence | Confidence |
|---|---|---|---|---|---|---|

## External Services

| Service | Purpose | Call Site | Config / Credential Source | Failure Impact | Evidence | Confidence |
|---|---|---|---|---|---|---|

## Boundary Risks / Unknowns

| Item | Why It Matters | Evidence | Suggested Follow-Up |
|---|---|---|---|

## Evidence Chain

| File Path | Symbol / Object | Parameters / Fields | Description | Proves | Confidence |
|---|---|---|---|---|---|

## Project Memory Backfill

| Candidate Fact | Backfill Target | Reason | Evidence | Confidence |
|---|---|---|---|---|

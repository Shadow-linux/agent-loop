# Evidence Graph

Evidence Graph 是代码证据索引，不是项目摘要。先建立它，再写 Onboarding Spec 和正式文档。

证据要求：关键 claim 必须带具体文件路径、符号/函数/类/配置键（能找到时）、调用方向或数据流方向、Confidence。没有证据的候选项放进 Unknowns，不进入正式 Module / Flow Plan。

## Deployable Units

| Unit | Entry | Config | Depends On | Called By | Evidence | Confidence |
|---|---|---|---|---|---|---|

## Bounded Context Candidates

| Context | Modules | Core Objects | Responsibilities | Evidence | Confidence |
|---|---|---|---|---|---|

## Module Candidates

| Module | Why It Is A Module | APIs | Data Objects | Use Cases | Evidence | Confidence |
|---|---|---|---|---|---|---|

## Flow Candidates

| Flow | Trigger | Participants | State Changes | External Dependencies | Evidence | Risk |
|---|---|---|---|---|---|---|

## Relationship Wireframe

多模块 / 多服务项目必须画关系线框图。表格不能替代这张图。

```text
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ caller   │───▶│ gateway  │───▶│ router   │───▶│ provider │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                    │               │               │
                    ▼               ▼               ▼
              ┌──────────┐    ┌──────────┐    ┌──────────┐
              │ logs     │    │ cache/mq │    │ database │
              └──────────┘    └──────────┘    └──────────┘
```

## Data Object Inventory

| Object | Kind | Owner | Key Fields / State | Used By | Evidence |
|---|---|---|---|---|---|

## Async / Job / Callback Inventory

| Name | Trigger | Consumer / Handler | State Changed | Retry / Compensation | Evidence |
|---|---|---|---|---|---|

## Infra / Dependency Inventory

| Dependency | Kind | Used By | Purpose | Config Source | Failure Symptom | Evidence |
|---|---|---|---|---|---|---|

## Gateway / Runtime Inventory

当项目包含 Nginx、OpenResty、ingress、API gateway、reverse proxy、sidecar 或 runtime routing scripts 时必须填写。

| Gateway / Runtime | Route / Match | Auth / Rate Limit | Headers | Timeout / Retry / Upstream | Logs | Evidence |
|---|---|---|---|---|---|---|

## High-Risk Areas

| Area | Why Risky | Evidence | Required Docs |
|---|---|---|---|

## Unknowns

| Question | Why It Matters | Evidence Missing | Human Needed? |
|---|---|---|---|

## Evidence Readiness Gate

- [ ] 每个 Module Candidate 都有具体 evidence，不能只有目录名。
- [ ] 每个 Flow Candidate 都有 trigger、participants、state changes 和 evidence。
- [ ] 多模块 / 多服务项目已有 Relationship Wireframe。
- [ ] 没有证据的候选项已移入 Unknowns。
- [ ] 没有 `<...>`、TBD、TODO、待补充、空 required row 或“看代码/see code”占位证据。

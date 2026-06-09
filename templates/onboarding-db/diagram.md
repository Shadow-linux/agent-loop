# Diagram: <name>

Document Language: 中文
Last Verified:
Diagram Type:
Question Answered:
Scope:
Source Evidence:
Confidence:
Human Review Status: draft

## Diagram Style Guide

All onboarding diagrams must follow this unified style. Deep Scan diagrams should be as complete as possible.

### Flowchart Style

- **Layer separation**: Use `subgraph` to separate layers:
  - `UserLayer` — human, browser, client
  - `APILayer` — API route, controller, WebSocket handler
  - `DomainLayer` — service, use case, domain logic
  - `DataLayer` — database, ORM model, cache, file storage
  - `RuntimeLayer` — job, worker, queue, scheduler
  - `ExternalLayer` — third-party service, object storage, remote runtime
- **Color classes** (mandatory when 4+ node types):
  - `user` (#f3e5f5 / purple) — human/client
  - `api` (#e1f5ff / blue) — API entry
  - `domain` (#fff8e1 / yellow) — business logic
  - `task` (#fff3e0 / orange) — async job/worker
  - `db` (#e8f5e9 / green) — database/persistent store
  - `external` (#ffebee / red) — external service
  - `state` (#fffde7 / amber) — status transition, failure state
- **Node shapes**:
  - API/Route: `"POST /path"` (rounded rectangle, `api` color)
  - Service/UseCase: `"Service: method()"` (rectangle, `domain` color)
  - Domain Rule / Branch: `{"check permission"}` (diamond, `domain` color, only for decisions)
  - Database/Model: `[(TableName / Model)]` (cylinder, `db` color)
  - Job/Worker: `"Task: task_name()"` (rounded rectangle, `task` color)
  - External Service: `"External: api_name()"` (rounded rectangle, `external` color)
  - State/Status: `"Status: PENDING"` (rounded rectangle, `state` color)
- **Arrows**:
  - Synchronous call: `-->` (solid)
  - Async trigger / callback: `-.->` (dashed)
  - Data return: `-->>` (implied bidirectional, or add note)
- **Naming**: Node labels must contain **specific names**. Use `POST /meetings/{id}/generate` instead of `API`. Use `MinutesService.generate()` instead of `Service`.

### Sequence Diagram Style

- **Participant naming**: `participant X as "Layer: SpecificName()"`
  - Example: `participant API as "API: POST /meetings/{id}/generate"`
  - Example: `participant S as "Service: generate_minutes(id)"`
- **Message format**: `Source->>Target: action(param)` with specific function and key params
- **Auto-numbering**: Use `autonumber` for all sequence diagrams
- **Notes**: Use `Note over X,Y:` or `Note right of X:` for key conditions, exceptions, retry policies
- **Async callback**: Dashed line `-->>` with label `async callback`
- **Branches**: Use `alt` / `else` / `end` for success/failure paths

### Diagram Naming Convention

- Module call chain: `module-<name>-call-chain`
- Module sequence: `module-<name>-sequence`
- Flow overview: `flow-<name>-overview`
- Data entity relationship: `data-entity-relationship`
- Model usage flow: `model-usage-flow`
- Entity lifecycle: `entity-<name>-lifecycle`

## Diagram

```mermaid
flowchart TB
  subgraph UserLayer["用户 / Client"]
    USER([用户 / Client])
  end

  subgraph APILayer["API / Entry"]
    API["API: POST /resource/action"]
  end

  subgraph DomainLayer["Domain / Service"]
    SERVICE["Service: action_resource()"]
    DOMAIN{"校验 / 业务规则"}
  end

  subgraph DataLayer["Data / State"]
    DB[(TableName / ORM Model)]
    STATE["Status: PENDING → COMPLETED"]
  end

  subgraph RuntimeLayer["Jobs / External"]
    TASK["Task: process_async()"]
    EXT["External: call_third_party()"]
  end

  USER --> API --> SERVICE --> DOMAIN
  DOMAIN --> DB
  SERVICE -.-> TASK
  TASK --> EXT
  TASK --> STATE

  classDef user fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px,color:#000
  classDef api fill:#e1f5ff,stroke:#01579b,stroke-width:2px,color:#000
  classDef domain fill:#fff8e1,stroke:#f9a825,stroke-width:2px,color:#000
  classDef task fill:#fff3e0,stroke:#ef6c00,stroke-width:2px,color:#000
  classDef db fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
  classDef external fill:#ffebee,stroke:#c62828,stroke-width:2px,color:#000
  classDef state fill:#fffde7,stroke:#f9a825,stroke-width:2px,color:#000

  class USER user
  class API api
  class SERVICE,DOMAIN domain
  class DB db
  class TASK task
  class EXT external
  class STATE state
```

## Sequence Diagram Example

Use this for async callbacks, WebSocket lifecycles, external API interactions, retry/compensation, or any scenario where exact call order matters.

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant API as API: POST /resource/action
    participant S as Service: action_resource(id, payload)
    participant R as Repository: find_by_id(id)
    participant T as TaskDispatcher: dispatch(task_type, data)
    participant W as Worker: process_task(data)
    participant Ext as ExternalService: call_api(data)

    C->>API: request {id, payload}
    API->>S: invoke action_resource(id, payload)
    S->>R: find_by_id(id)
    R-->>S: resource object
    S->>T: dispatch(ASYNC_TASK, resource_data)
    S-->>API: response: {status: accepted}
    API-->>C: 202 Accepted

    T->>W: trigger process_task(resource_data)
    W->>Ext: call_api(resource_data)
    Ext-->>W: callback / response

    alt 成功
        W->>R: update_status(id, COMPLETED)
        Note over W,R: 成功后更新状态并通知
    else 失败 / 重试超限
        W->>R: update_status(id, FAILED)
        W->>T: retry_count++ or DLQ
        Note over W,T: 失败时进入重试队列或死信队列
    end
```

## How To Read

**Every diagram must include a "How To Read" section.** Explain:
1. What question this diagram answers
2. What each color means
3. What each shape means
4. What solid vs dashed arrows mean
5. How to trace a specific path through the diagram

If a diagram lacks "How To Read", it is considered incomplete.

## Step-by-Step Walkthrough

**Every diagram must also include a "Step-by-Step Walkthrough" section.** A picture alone is not enough; newcomers need text that walks them through the diagram in execution order.

### Format Rules

- Use numbered list (1, 2, 3...)
- Each step must mention the **specific node name** as it appears in the diagram
- Each step must say **which layer** the node belongs to (API / Domain / Data / Runtime / External)
- Each step must say whether the call is **synchronous** or **asynchronous**
- Each step should mention **key parameters, state changes, or side effects** when evidenced
- Walkthrough must cover the **happy path** first, then mention **failure/retry branches** if they exist in the diagram

### Flowchart Walkthrough Example

```text
1. 用户 / Client（UserLayer）发起请求，调用 `POST /resource/action`（API 层，蓝色）
2. API 路由接收请求，同步调用 `Service: action_resource(id, payload)`（Domain 层，黄色）
3. Service 执行权限校验 / 业务规则（Domain 层，黄色，菱形判断节点）
4. 校验通过后，Service 同步调用 `Repository: find_by_id(id)`（Data 层，绿色）
5. Repository 从数据库返回 resource object 给 Service（Data 层 → Domain 层，同步返回）
6. Service 异步触发 `TaskDispatcher: dispatch(ASYNC_TASK, resource_data)`（Runtime 层，橙色，虚线箭头）
7. Service 立即返回 `{status: accepted}` 给 API 层（Domain 层 → API 层，同步返回）
8. API 返回 202 Accepted 给用户 / Client（API 层 → UserLayer，同步返回）
9. 后台：Worker 异步处理任务，调用 `ExternalService: call_api(resource_data)`（External 层，红色）
10. 外部服务返回结果后，Worker 更新数据库状态为 COMPLETED 或 FAILED（Data 层，绿色）
```

### Sequence Diagram Walkthrough Example

```text
1. Client 发送 request {id, payload} 到 API: POST /resource/action（同步请求）
2. API 同步调用 Service: action_resource(id, payload)，传入 id 和 payload
3. Service 同步调用 Repository: find_by_id(id) 查询资源
4. Repository 返回 resource object 给 Service（同步返回）
5. Service 同步调用 TaskDispatcher: dispatch(ASYNC_TASK, resource_data) 提交异步任务
6. Service 返回 {status: accepted} 给 API（同步返回）
7. API 返回 202 Accepted 给 Client（同步返回，此时后台任务尚未完成）
8. TaskDispatcher 异步触发 Worker: process_task(resource_data)（后台开始执行）
9. Worker 同步调用 ExternalService: call_api(resource_data)（调用第三方）
10. ExternalService 返回 callback / response 给 Worker（同步返回）
11. 【成功分支】Worker 调用 Repository 更新状态为 COMPLETED
12. 【失败分支】Worker 调用 Repository 更新状态为 FAILED，并将任务重新投递或送入死信队列
```

If a diagram lacks "Step-by-Step Walkthrough", it is considered incomplete.

## Notes

## Evidence Chain

| Node / Edge | File Path | Symbol / Object | Parameters / Fields | Description | Confidence |
|---|---|---|---|---|---|

## Unknowns

| Item | Why It Matters | Evidence | Suggested Follow-Up |
|---|---|---|---|

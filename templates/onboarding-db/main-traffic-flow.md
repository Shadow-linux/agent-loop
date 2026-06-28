# Main Traffic Flow

Document Language: 中文
Created:
Last Updated:
Last Verified:
Confidence:
Source Evidence:
Human Review Status: draft

## Purpose

解释项目主流量路径：请求、事件或人类操作从哪里进入，经过哪些核心领域、服务、数据和外部依赖，在哪里结束。

## Scope

| Included | Excluded | Why |
|---|---|---|

## Colored Flowchart

```mermaid
flowchart LR
  User([User / Client]):::entry --> Gateway["Gateway / Entrypoint"]:::entry
  Gateway --> Orchestrator["Orchestrator / Use Case"]:::domain
  Orchestrator --> Domain["Core Domain"]:::domain
  Domain --> Fact[(Fact Source DB)]:::data
  Domain -.-> Async{{Queue / Worker}}:::async
  Async --> Derived[(Derived View)]:::data
  Domain --> External["External Provider"]:::external
  Domain --> Risk{{Risk Point}}:::risk

  classDef entry fill:#e1f5ff,stroke:#01579b,stroke-width:2px,color:#000
  classDef domain fill:#fff8e1,stroke:#f9a825,stroke-width:2px,color:#000
  classDef data fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
  classDef async fill:#fff3e0,stroke:#ef6c00,stroke-width:2px,color:#000
  classDef external fill:#ffebee,stroke:#c62828,stroke-width:2px,color:#000
  classDef risk fill:#fce4ec,stroke:#ad1457,stroke-width:3px,color:#000
```

## How To Read

## Step-by-Step Walkthrough

1.

## Main Flow Evidence Trace

| Step ID | Graph Edge | File | Symbol | Data / State | Sync / Async | Risk | Evidence | Confidence |
|---|---|---|---|---|---|---|---|---|

## Related Required Core Flows

| Flow | Why It Matters | Target Deep Trace Doc | Completion Status |
|---|---|---|---|

## Verification / Observability

| Signal | Where | What It Proves | Evidence | Confidence |
|---|---|---|---|---|

## Unknowns

| Unknown | Impact | Next Action |
|---|---|---|

# Graph Slice: <scope>

Document Language: 中文
Created:
Last Updated:
Last Verified:
Scope:
Confidence:
Source Evidence:
Human Review Status: draft

## Purpose

Targeted Onboarding Scan 使用这个模板记录某个领域、flow、module、async path、deployment path 或问题区域的局部 Evidence Graph。

## Included Nodes

| Node ID | Type | Name | Core Role | Evidence | Confidence | Completion Status |
|---|---|---|---|---|---|---|

## Included Edges

| Edge ID | Source Node ID | Edge Type | Target Node ID | Sync / Async | Data / State | Required For Complete | Evidence | Confidence |
|---|---|---|---|---|---|---|---|---|

## Excluded But Related

| Node / Edge | Why Excluded | Risk | Follow-up |
|---|---|---|---|

## Slice Diagram

```mermaid
flowchart LR
  Scope["Target Scope"]:::domain --> Fact[(Fact Source)]:::data
  Scope --> Flow["Focused Flow"]:::entry
  Flow -.-> Async{{Async / External}}:::async
  Scope --> Risk{{Risk}}:::risk

  classDef entry fill:#e1f5ff,stroke:#01579b,stroke-width:2px,color:#000
  classDef domain fill:#fff8e1,stroke:#f9a825,stroke-width:2px,color:#000
  classDef data fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
  classDef async fill:#fff3e0,stroke:#ef6c00,stroke-width:2px,color:#000
  classDef risk fill:#fce4ec,stroke:#ad1457,stroke-width:3px,color:#000
```

## Local Completion Decision

```text
Targeted onboarding complete for <scope>.
Full Deep onboarding remains incomplete unless global gates pass.
```

## Global Coverage Impact

| Global Coverage Row | Local Update | Does This Change Deep Completion? | Reason |
|---|---|---|---|

## Focused Output Proposal

| File / Item | Action | Why | Evidence | Confidence |
|---|---|---|---|---|

## Unknowns / Follow-up

| Unknown | Impact | Next Action |
|---|---|---|

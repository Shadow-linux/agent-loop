# Flow: <name>

Document Language: 中文
Created:
Last Updated:
Last Verified:
Confidence:
Source Evidence:
Human Review Status: draft

## Purpose

## One Diagram To Understand The Flow

Use a small layered flowchart that answers one flow question. Do not start with a sequence diagram. Use `sequenceDiagram` only later for a narrow interaction detail after this flowchart exists.

```mermaid
flowchart TB
  subgraph API_Entry["① API / Entry"]
    USER([用户 / Client])
    API["API / Route / Trigger"]
  end

  subgraph DomainLayer["② Domain / Service"]
    SERVICE["Service / Use Case"]
    DOMAIN["Domain Rule"]
  end

  subgraph DataLayer["③ Data / State"]
    DB[(Database / Model)]
    STATE["State Change"]
  end

  subgraph RuntimeLayer["④ Jobs / External"]
    TASK["Job / Worker / Queue"]
    EXT["External Service / Storage"]
  end

  USER --> API --> SERVICE --> DOMAIN
  SERVICE --> DB
  SERVICE --> STATE
  SERVICE -.-> TASK
  TASK --> EXT
  TASK --> DB

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

## Main Flow Quick Notes

```text
Start
-> entrypoint receives request or trigger
-> service or use case applies business rule
-> state is written or job is triggered
-> async / external steps if any
-> final state or side effect
```

## Call Chain Details

| Stage | Trigger | File Path | Function / Object | Parameters / Fields | What It Does | Next Step | Evidence | Confidence |
|---|---|---|---|---|---|---|---|---|

## API Entrypoints

| API / Route | Method | File Path | Handler / Object | Request Fields | Response / Side Effect | Evidence | Confidence |
|---|---|---|---|---|---|---|---|

## Task / Job Entrypoints

| Task / Job | Trigger | Queue / Scheduler | File Path | Function / Object | Parameters / Fields | Retry / Recovery | Evidence | Confidence |
|---|---|---|---|---|---|---|---|---|

## Module / Service Responsibility Boundaries

| Module / Service | Responsibility In This Flow | Not Responsible For | Evidence | Confidence |
|---|---|---|---|---|

## Key State Changes

| Object / Entity | Field | Transition | Writer | Trigger / Guard | Side Effects | Evidence | Confidence |
|---|---|---|---|---|---|---|---|

## Retry / Compensation / Failure Paths

| Failure / Delay | Where It Happens | Retry / Compensation | User / System Impact | Evidence | Confidence |
|---|---|---|---|---|---|

## Code Reading Order

| Order | File / Symbol | Why Read This | Next |
|---|---|---|---|

## Common Misunderstandings

| Misunderstanding | Correct Reading | Evidence |
|---|---|---|

## Verification Hints

| Check | Command / File / Scenario | What It Proves | Evidence | Confidence |
|---|---|---|---|---|

## Evidence Chain

| File Path | Symbol / Object | Parameters / Fields | Description | Proves | Confidence |
|---|---|---|---|---|---|

## Risks And Unknowns

| Item | Why It Matters | Evidence | Confidence | Suggested Follow-Up |
|---|---|---|---|---|

## Project Memory Backfill

| Candidate Fact | Backfill Target | Reason | Evidence | Confidence |
|---|---|---|---|---|

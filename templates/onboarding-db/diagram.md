# Diagram: <name>

Document Language: 中文
Last Verified:
Diagram Type:
Question Answered:
Scope:
Source Evidence:
Confidence:
Human Review Status: draft

## Diagram

Onboarding diagrams are flowchart-first. Use `sequenceDiagram` only for narrow interaction details after a module/process flowchart already exists.

```mermaid
flowchart TB
  subgraph UserLayer["用户 / Client"]
    USER([用户 / Client])
  end

  subgraph APILayer["API / Entry"]
    API["API / Route / UI Action"]
  end

  subgraph DomainLayer["Domain / Service"]
    SERVICE["Service / Use Case"]
    DOMAIN["Domain Rule"]
  end

  subgraph DataLayer["Data / State"]
    DB[(Database / Model)]
    STATE["State Change"]
  end

  subgraph RuntimeLayer["Jobs / External"]
    TASK["Job / Worker"]
    EXT["External Service"]
  end

  USER --> API --> SERVICE --> DOMAIN
  SERVICE --> DB
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

## How To Read

## Notes

## Evidence Chain

| Node / Edge | File Path | Symbol / Object | Parameters / Fields | Description | Confidence |
|---|---|---|---|---|---|

## Unknowns

| Item | Why It Matters | Evidence | Suggested Follow-Up |
|---|---|---|---|

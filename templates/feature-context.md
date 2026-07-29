# Feature Context: <Feature Name>

Derived Context: yes
Authority: Requirement README -> Effective Product Definition -> accepted ADRs
Independent Product Truth: no

Requirement Set: .agent-loop/requirements/<requirement-id>/README.md
Requirement Lifecycle: accepted | in-progress | partially-implemented | implemented
Resolved Product Source: .agent-loop/requirements/<requirement-id>/product.md
Product Definition Profile: brief | standard | legacy
Product Review: confirmed | accepted | concept-foundation-not-needed
Product Source SHA-256:
Applicable Decisions: none | .agent-loop/decisions/<decision>.md
Decision Source SHA-256: none | .agent-loop/decisions/<decision>.md=<sha256>
Product Slice References:
Verified At: <ISO-8601 timestamp with timezone>
Freshness: current | changed | blocked

This optional file expands the derived Snapshot for one complex Feature. It has no independent product, Requirement lifecycle, approval, task, test, plan, code-fact, or execution authority. Its source identity and digests must exactly match `spec.md`, and all source paths are project-root-relative. Generate Product and Decision Markdown SHA-256 values after canonicalizing `CRLF` and lone `CR` to `LF`; legacy raw LF/CRLF digests remain reader-compatible. Legacy `refresh-required` values remain readable as changed evidence and must be refreshed through Agent assessment rather than treated as checker authorization.

## Product Outcome

## Actors, Permissions, And Core Journey

## Product Rules And Invariants

## States And Terminals

## Exceptions, Recovery, And Manual Handling

## Feature Boundary And Acceptance Context

## Product Slice Trace

Link each expanded context item to the corresponding Product Slice responsibility, accepted source ID or `product.md#<anchor>`, and applicable accepted ADR.

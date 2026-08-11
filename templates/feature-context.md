# Feature Context: <Feature Name>

Derived Context: yes
Authority: resolved Feature Authority -> applicable source facts
Independent Product Truth: no

Authority Type: <descriptive authority label>
Authority Adapter: <detected open family or named custom adapter>
Primary Authority Reference:
Supporting Authority References: none | <references>
Authority Applicability: applicable | advisory | not-applicable
Authority Facts: <resolver-emitted facts in deterministic semicolon-separated order, including Authority Summary>
Authority Source SHA-256: none | <project-local source>=<sha256>

Requirement Product Definition fields when applicable:

Requirement Set: .agent-loop/requirements/<requirement-id>/README.md
Requirement Lifecycle: accepted | in-progress | partially-implemented | implemented
Resolved Product Source: .agent-loop/requirements/<requirement-id>/product.md
Product Definition Profile: brief | standard | legacy
Product Review: confirmed | accepted | concept-foundation-not-needed
Product Source SHA-256:
Applicable Decisions: none | .agent-loop/decisions/<decision>.md
Decision Source SHA-256: none | .agent-loop/decisions/<decision>.md=<sha256>
Product Slice References:

Bug Authority fields when applicable:

Bug ID:
Expected Behavior Evidence Locator:
Resolution Path / Fix Feature Locator:
Feature Location: flat | archived:<YYYY-MM>

Human/custom authority fields when applicable:

Evidence Locator:
Agent Review Required: yes | no

Verified At: <ISO-8601 timestamp with timezone>
Freshness: current | changed | blocked

This optional file expands the derived Snapshot for one complex Feature. It has no independent product, Requirement lifecycle, Bug lifecycle, approval, task, test, plan, code-fact, or execution authority. Include only adapter-applicable fields; its source identity, deterministic semicolon-separated `Authority Facts`, and digests must exactly match `spec.md`. `Authority Facts` includes the resolved Authority Summary and must be refreshed rather than paraphrased after any source fact changes. Project-local paths are project-root-relative, while external/ticket/Human locators remain evidence strings. Generate applicable Markdown SHA-256 values after canonicalizing `CRLF` and lone `CR` to `LF`; legacy raw LF/CRLF digests remain reader-compatible. Legacy `refresh-required` values remain readable as changed evidence and must be assessed rather than treated as Checker authorization.

## Product Outcome

## Actors, Permissions, And Core Journey

## Product Rules And Invariants

## States And Terminals

## Exceptions, Recovery, And Manual Handling

## Feature Boundary And Acceptance Context

## Product Slice Trace

Link each expanded context item to the corresponding Product Slice responsibility, accepted source ID or `product.md#<anchor>`, and applicable accepted ADR.

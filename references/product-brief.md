# Legacy Feature Product Brief Compatibility

## Purpose

This reference is reader-only compatibility for an existing Feature `product.md`. New Product Definition authoring belongs to `references/product-definition.md` and writes Requirement `product.md` only through Product Human Review plus Requirement Record / Archive.

Read an existing Feature Product Brief during Resume, Follow-up, Review, Close, or Recovery. Do not create `feature/product.md` for new work.

If it conflicts with the Effective Product Definition, stop for Requirement conflict/recovery; do not rewrite either source silently.

Do not create `feature/product.md` for new work. Do not copy `templates/product.md` into a Feature; that template now belongs to Requirement Product Definition.

Existing Feature Product Briefs remain valid historical/working evidence during:

- Resume;
- Feature Follow-up / Flow-back discovery;
- Review and Drift Check;
- Feature Completion / Close Review;
- Recovery / Backfill;
- audit of behavior that predates Adaptive Product Definition.

## Legacy Read Order

When a Feature already contains `product.md`:

1. read Feature `spec.md` and its Requirement links;
2. resolve Requirement README `Effective Product Definition` when present;
3. otherwise resolve legacy `Effective Concept Foundation` / reviewed `requirement.md`;
4. read Feature `product.md` as a historical Feature view;
5. compare its concept/model meaning and Applicable Decisions with the effective Requirement source;
6. continue only when the sources agree or the disagreement has a Human-reviewed Recovery owner.

The Requirement source outranks a Feature-local paraphrase for product meaning. Feature `product.md` may provide user journey, story, scope, tradeoff, and historical context, but it cannot redefine accepted identity, relationship, lifecycle, state, permission, invariant, fact ownership, terminal meaning, or Product Rule.

## Conflict And Drift

If an existing Feature Product Brief conflicts with the Effective Product Definition, stop for Requirement conflict/recovery; do not rewrite either source silently.

Use these outcomes:

| Evidence | Route |
|---|---|
| legacy Feature view is merely narrower | keep it as historical Feature scope and use current `spec.md` Product Slice for new work |
| Requirement source changed after the Feature closed | record drift/compatibility evidence; do not rewrite closed history |
| open Feature depends on stale product meaning | stop Feature Spec / Plan / Execute and return to Requirements Discussion / ADR compatibility review |
| no reliable Requirement source exists | Recovery / Backfill Human Review before changing product meaning |
| same goal has confirmed new meaning | append-only Requirement Product Definition follow-up; then refresh Product Slice after its own gate |

Do not automatically delete, move, rename, migrate, or synthesize a Requirement `product.md` from a legacy Feature Product Brief.

## Human Gate Boundary

Reading a legacy Product Brief needs no new gate. Any write still uses its owning action gate:

- Requirement Product Definition or follow-up: Product Human Review plus Requirement Record / Archive;
- Requirement lifecycle: Requirement lifecycle Human Gate;
- Feature Spec Product Slice: Feature Spec Human Review;
- ADR compatibility/technical landing: Decision & Design Human Review;
- source movement or migration: explicit bounded migration approval;
- commit, push, tag, release, or publish: each independent Git/release gate.

Legacy Product Brief presence, status, or earlier human acceptance grants none of these actions.

## Completion And Close Compatibility

For a legacy Feature, Feature Close Review still compares implementation and `spec.md` against the existing Product Brief when present. For new Features, compare implementation against the Requirement Product Definition via `spec.md` Product Slice; absence of Feature `product.md` is expected and is not drift.

## Stop Rules

Stop when:

- Requirement and Feature sources disagree on product semantics;
- one Requirement README exposes both new and legacy effective pointers;
- an open Feature Product Slice references a stale source;
- resolving history would require rewriting human originals or accepted records;
- a proposed compatibility fix would recreate Feature Product Brief authoring for new work;
- a migration, source move, or Git/release action lacks its own authorization.

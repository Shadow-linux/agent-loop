# Proposal: Light-Gate Authority Alias Repair

**Version:** 1.5.3
**Status:** implemented and validated; awaiting Human Review
**Human Review:** approved in conversation on 2026-07-29

## Problem

Whole-project chaos testing found three authority-boundary defects:

1. an archived Feature directory represented by an internal symlink could be planned as an ordinary Rehydrate move, then fail after mutation and resist rollback;
2. an internal `.agent-loop` memory-root alias was resolved to its physical target, causing plans to expose `.memory/...` paths and disagree with Feature Context and Lightweight Change scanners;
3. the root AGENTS checker could report managed blocks as current after an `agent-loop-skill` block body changed without a revision change.

## Accepted Boundary

- Scanners collect deterministic facts; the Agent judges meaning, coverage, conflict, and whether to continue.
- The human confirms only the existing exact Archive/Rehydrate plan or root-guidance update. No new Human Gate is added.
- Archive/Rehydrate Apply still enforces the exact approved plan, project confinement, pre-transaction path shape, transaction journal, post-check, and rollback.
- A Feature entry symlink is reported as `feature-entry-symlink`, is not planned as an ordinary directory move, and does not trigger Checker Recovery.
- An internal, resolvable, non-cyclic, single-authority `.agent-loop` or legacy alias may act as a logical memory-root name. Generated artifact paths remain under the logical root; alias target evidence remains hash-bound. Broken, cyclic, external, dual, or non-directory roots remain physical failures.
- Root AGENTS results are `STRUCTURAL_CURRENT / 0`, `STRUCTURAL_CHANGED / 0`, or `STRUCTURAL_INVALID / 1`. Only malformed/ambiguous marker structure and path escape are hard structural failures. Agent Loop-owned block bodies are compared to the template; project-owned body semantics remain Agent-reviewed.

## Non-Goals

- no symlink traversal during reference discovery;
- no `--force`, automatic repair, extra lifecycle, canonical stage, or authorization status;
- no weakening of exact-plan hash, execution confinement, transaction, post-check, restore, Feature Context, or root-guidance Human Review;
- no version change.

## Validation

Focused RED/GREEN must cover Feature-entry symlink planning, pre-transaction Apply rejection, internal memory-root alias across Archive/Feature Context/Lightweight Change, alias retargeting, broken/cyclic/external aliases, Agent Loop-owned root body drift, project-owned body handling, and invalid marker/path controls. Completion requires all Shell/Python tests, mechanical checks, and the six-domain full validation.

## Implementation Result

- Focused RED reproduced all seven original gaps; focused GREEN and negative controls now pass.
- Final executable validation: Shell `48 / 48`, Python `344 / 344`.
- Archive preserves logical root paths, hash-binds alias evidence, excludes Feature-entry symlinks from moves, and validates current plan plus real move paths before transaction creation.
- Feature Context and Lightweight Change reuse the same accepted-root authority resolver.
- Root guidance returns factual `STRUCTURAL_*` results while retaining the existing Human Review for writes.
- Platform status: `macOS-verified / Windows-test-defined`.
- No commit, push, tag, release, publish, or installed-Skill synchronization was performed.

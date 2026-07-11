# Project Skills Index

Updated: YYYY-MM-DD

This index is the lifecycle and discovery source for project-local skills. Only `active` entries participate in normal routing.

| Skill | Status | Load Policy | Triggers | Scope | Helper Resolution | Evidence | Updated |
|---|---|---|---|---|---|---|---|
| `<skill-name>` | `proposed | active | disabled | deprecated` | `bootstrap | on-demand` | `<trigger summary>` | `<bounded project scope>` | `<writing-skills, skill-creator, or fallback>` | `<skill-path>/validation.md` | YYYY-MM-DD |

## Rules

- Gate 1 is required before creating a new entry or materially updating an active skill.
- Validation success automatically changes `proposed` to `active`; validation failure keeps `proposed`.
- `disabled` and `deprecated` entries are not loaded or executed.
- Loading an active skill does not authorize execution; every invocation requires the Execution Gate.
- The Evidence link must contain a SHA-256 Validated Content Manifest for this exact INDEX row plus current instruction-bearing and executable files.
- Missing paths, missing manifests, manifest mismatches, or unsupported active claims are project-skill drift and must be reconciled before reliance.

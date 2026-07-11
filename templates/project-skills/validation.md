# Project Skill Validation

Skill: `<skill-name>`
Status: `proposed | active | disabled | deprecated`
Load Policy: `bootstrap | on-demand`
Updated: YYYY-MM-DD

## Candidate And Gate 1

- Human request or proactive candidate:
- Confirmed scope:
- File tree:
- Gate 1 evidence:
- Secrets and environment review:

## Helper Resolution

- `superpowers:writing-skills` / `writing-skills`: `loaded | unavailable | load-failed`
- `skill-creator`: `loaded | unavailable | load-failed`
- Fallback:
- Path override: `.agent-loop/skills/<skill-name>/`

## RED Baseline

| Scenario | Without skill result | Exact failure or rationalization |
|---|---|---|
| `<realistic scenario>` | `<observed result>` | `<verbatim evidence>` |

## GREEN And REFACTOR

| Scenario | With skill result | Loophole found | Correction | Final result |
|---|---|---|---|---|
| `<same scenario>` | `<observed result>` | `<new rationalization or none>` | `<rule change or none>` | `PASS | FAIL` |

## Structural And Resource Checks

- Frontmatter validation:
- Description trigger review:
- Script tests:
- Reference and asset checks:
- Sensitive-value scan:
- External-path and symlink scan:

## Activation Result

- Required scenarios passed:
- Remaining failures:
- INDEX updated:
- Final status: `active | proposed`
- Evidence summary:

## Validated Content Manifest

Record SHA-256 after all GREEN/REFACTOR edits and before changing status to `active`.

| Relative Path | SHA-256 | Purpose |
|---|---|---|
| `.agent-loop/skills/INDEX.md::<exact-skill-row>` | `<sha256-of-exact-UTF-8-row>` | lifecycle, load policy, triggers, scope, and evidence binding |
| `SKILL.md` | `<sha256>` | primary instructions |
| `<scripts-or-instruction-resource>` | `<sha256>` | `<purpose>` |

## Execution Gate Forward Test

- Invocation scope:
- Human confirmation evidence:
- Scope expansion behavior:
- Auto-mode / prior-authorization rejection:
- Manifest mismatch behavior:
- Invocation end and retry behavior:
- Combined applicable-gate behavior:
- Result: `PASS | FAIL`

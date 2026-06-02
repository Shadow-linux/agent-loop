# Delivery Contracts: Project Invite Permissions

Created: 2026-05-26
Updated: 2026-05-26
Status: accepted

## Contract Index

| ID | Type | Name | Producer | Consumers | Status | Detail | Verification | Compatibility |
|---|---|---|---|---|---|---|---|---|
| API001 | API | Create Project Invite | Backend invite API | Web project members page | accepted | `contracts/API001-create-project-invite.md` | API002 pending | non-breaking |

## Decisions Needed

| ID | Decision | Affected Consumers | Impact | Recommended Answer | Human Decision |
|---|---|---|---|---|---|
| API001 | Confirm response shape before frontend implementation | Web project members page | Frontend depends on invite status and permission error fields | Accept current response shape | accepted |

## Drift Notes

| Date | Contract | Code Reality | Contract Change | Consumer Impact | Decision | Evidence |
|---|---|---|---|---|---|---|
| 2026-05-26 | API001 | Planned API not implemented yet | none | Frontend should use accepted draft shape | accepted | Spec US2, tests API002 |


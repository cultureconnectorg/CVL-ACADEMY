# WAL-27 — Financial Incident & Kill-Switch Operations

```
Prerequisite: WAL-19. UPGRADED 2026-09-06 from BLOCKED_PRODUCT_
DEPENDENCY — see wal22/REFERENTIAL.md's header note, same discipline.
```

## Repo truth

`djsayd/CVLN-Wallet/backend/server.py` (re-read directly this
session): a real global kill-switch, `PUT /admin/kill-switch`,
admin-only, with **exactly 3 named switches** — `"withdrawals"`,
`"card"`, `"agents"` — validated against that exact set (any other
name is rejected with 400); every toggle is audited
(`audit(... "KillSwitch.Toggled" ...)`). Separately, a real per-user
card control: `POST /card/freeze` / `POST /card/unfreeze` (distinct
from the global kill-switch — freezing one user's card does not touch
the global `"card"` switch, and vice versa).

**This is a real capability of the external CVLN Wallet product —
absent entirely from this Academy's own `backend/wallet/`** (which has
no incident/kill-switch mechanism of any kind — the same gap this
Academy's own WAL-27 formation originally flagged, now resolved by
citing the real external product instead).

## Prerequisites

WAL-19.

## Objectives

1. Name the exact 3 global kill-switches and what each is meant to
   halt (`withdrawals`, `card`, `agents`) — never invent a 4th.
2. Explain the real distinction between the **global** kill-switch
   (`"card"`, affects all users) and the **per-user** card freeze
   (`/card/freeze`, affects one account) — these are two different
   mechanisms operating at different scopes, never conflated.
3. Explain why every kill-switch toggle is audited, and what that
   audit trail (`KillSwitch.Toggled`) would need to contain to support
   a real incident post-mortem.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | Global kill-switch literacy | `PUT /admin/kill-switch`, the 3 named switches | Table: switch name → real scope → what it halts |
| M2 | Global vs. per-user scope discipline | `/admin/kill-switch` (`"card"`) vs. `/card/freeze`/`unfreeze` | Written note distinguishing the two, with a worked example of when each is the correct tool |
| M3 | Audit-trail literacy | `audit(..., "KillSwitch.Toggled", ...)` | Written note on what a real incident review would need from this trail |

## Assessment

Per `../CERTIFICATION_MODEL.md`. M2 is a strong discriminator — a
candidate who conflates the global switch with the per-user freeze
has not understood the real system.

## Evidence / certification / mission eligibility

Same general pattern as WAL-19/20/21. Mission eligibility: none — no
real operational access to `djsayd/CVLN-Wallet`'s admin surface exists
for any Academy candidate.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.

# WAL-22 — Coffres & Allocation Operations

```
Prerequisite: WAL-19. UPGRADED 2026-09-06 from BLOCKED_PRODUCT_
DEPENDENCY after a Founder checkpoint: this Academy's own
backend/wallet/ has no vault concept, but the real external
djsayd/CVLN-Wallet product does — grounded there instead, per the
"repo not yet audited != capability does not exist" discipline.
```

## Repo truth

`djsayd/CVLN-Wallet/backend/server.py` (re-read directly this
session, commit `359aaee1`): a real "coffres" (vault) system.
`GET /coffres` (list a user's vaults), `POST /coffres` (create, with
`name`/`icon`/`goal_cc`/`color`, `amount_cc` starts at 0),
`POST /coffres/{coffre_id}/move` (atomic move in/out — moving cash
*into* a coffre spends available balance via `atomic_spend`; moving
cash *out* credits it back via `apply_user_balance`; every move is
posted to the double-entry ledger via `ledger_post`), `DELETE
/coffres/{coffre_id}` (closing a non-empty coffre refunds its balance
to the user before deletion).

**This is a real capability of the external CVLN Wallet product —
absent entirely from this Academy's own `backend/wallet/`.** No
integration between the two repos is observed; this formation teaches
literacy of the real product's operator surface, never real
operational access to it.

## Prerequisites

WAL-19.

## Objectives

1. Explain the coffre lifecycle (create → move funds in/out → close)
   using the real routes and their exact semantics (in-move = spend
   from available balance; out-move = credit back; close refunds any
   remaining balance).
2. Explain why every coffre move is ledger-posted (`ledger_post`) as a
   balanced double-entry between the user's cash account and the
   coffre's own account — never a silent balance mutation.
3. Never claim a real Academy candidate can create or move funds in a
   real user's `djsayd/CVLN-Wallet` coffre — this formation teaches
   the mechanism, not operational access.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | Coffre lifecycle literacy | `GET/POST /coffres`, `POST /coffres/{id}/move`, `DELETE /coffres/{id}` | Annotated route table: verb → effect on `amount_cc` and available balance |
| M2 | Ledger-posting discipline | `ledger_post` calls inside `move_coffre`/`delete_coffre` | Written note: why a vault move is a balanced ledger entry, not a raw field update |
| M3 | Boundary discipline | Absence of any vault concept in this Academy's own `backend/wallet/` | Explicit note: real product capability, no Academy runtime access |

## Assessment

Per `../CERTIFICATION_MODEL.md`.

## Evidence / certification / mission eligibility

Same general pattern as WAL-19/20/21. Mission eligibility: none — no
real operational access to `djsayd/CVLN-Wallet` exists for any
candidate.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_WAL22` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Grounded in the repo-truth
already directly verified against `djsayd/CVLN-Wallet` (commit
`359aaee1`) — not re-audited here, per this corpus's own discipline of
reusing an already-verified finding rather than re-cloning the repo on
every subsequent pass. Not yet delivered to a real candidate —
`FULLY_COMPLETE` still requires that verification, per
`../QUALITY_GATES.md`.

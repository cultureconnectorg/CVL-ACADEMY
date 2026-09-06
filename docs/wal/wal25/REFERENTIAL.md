# WAL-25 — CVLN Marketplace Operations

```
Prerequisite: WAL-19. UPGRADED 2026-09-06 from BLOCKED_PRODUCT_
DEPENDENCY — see wal22/REFERENTIAL.md's header note, same discipline.
```

## Repo truth

`djsayd/CVLN-Wallet/backend/server.py` (re-read directly this
session): a real, seeded marketplace catalog (`MARKETPLACE_ITEMS`, 8
items) spanning the actual CVLN ecosystem — e.g. "Pack Certification
FREK" (seller FREKCORE), "Beat exclusif — DJ Sayd" (seller Factory
Maker Studio), "Pass Culture Connect 2026," "Crédits IA Laurentia,"
"Mission culturelle" (seller Kiltikonet), "Abonnement KORA Premium,"
"Formation Production" (seller Factory Maker Academy), "Licence CVLN
OS." `GET /marketplace` lists the catalog; `POST /marketplace/buy`
executes a real idempotent purchase (`idem_begin`/`idem_finish`,
`atomic_spend` against the buyer's available balance, a transaction
record via `add_transaction`).

**This is a real capability of the external CVLN Wallet product —
absent entirely from this Academy's own `backend/wallet/`.**

## Prerequisites

WAL-19.

## Objectives

1. Explain the marketplace catalog's real shape (item fields: `item_
   id`, `title`, `seller`, `price_cc`, `category`, `tag`) and that it
   is currently a static, seeded list, not a dynamic listing system.
2. Explain the buy flow's idempotency guarantee — a repeated `POST
   /marketplace/buy` with the same idempotency key never double-charges.
3. Recognize that the catalog's sellers are real named CVLN ecosystem
   entities (FREKCORE, Factory Maker Studio/Academy, Culture Connect,
   Laurentia, Kiltikonet, KORA, CVLN OS) — never invent a seller not in
   the real seeded list.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | Catalog literacy | `MARKETPLACE_ITEMS`, `GET /marketplace` | Annotated table of the real 8 items and their fields |
| M2 | Idempotent buy-flow literacy | `POST /marketplace/buy`, `idem_begin`/`idem_finish`, `atomic_spend` | Sequence diagram: idempotency check → item lookup → atomic spend → transaction record |
| M3 | Boundary discipline | Absence of any marketplace concept in `backend/wallet/` | Explicit note: real product capability, no Academy runtime access |

## Assessment

Per `../CERTIFICATION_MODEL.md`.

## Evidence / certification / mission eligibility

Same general pattern as WAL-19/20/21. Mission eligibility: none.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.

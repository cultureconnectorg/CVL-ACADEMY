# WAL-01→13, 16→18 — Fintech-Engineering Professional Pathway (external/market, 16 rows)

## Grounding

Per `WALLET_CVE_RECONCILIATION.md`: coverage `NONE` in Academy today
(`KOR-10` taught Wallet/JCC only from the *application/usage* angle
for a KORA creator — not the *systems-engineering* angle these
candidates require; the two never overlap, no duplication risk).
`DISTINCT_PROFESSION` for all 18 rows in the WAL-01→18 set (standard,
real fintech-engineering career specializations — ledger engineer,
payments ops, card ops, compliance, treasury, etc.). Action:
`NEW_EXTERNAL`. Zero rejected. **This referential covers 16 of the 18
rows** — `WAL-14` (Payment Security, Fraud & Risk) resolves separately
via `docs/wal/EXTEND_EXISTING_NOTE.md` (→ `CYB-31→42`, same G8
resolution as `FRK-48-51/KLT-17`) and `WAL-15` (Financial Compliance &
Audit) via `docs/wal/NEEDS_EXPERT_REVIEW.md` (financial regulation,
never a universal recipe).

**Best-grounded rows** (real worked examples from this Academy's own
`backend/wallet/` or the wider ecosystem):

- **WAL-03** (Digital Ledger & Double-Entry Accounting) — `PARTIAL`:
  the real ledger (`backend/wallet/`) exists but is **single-entry
  additive**, not double-entry. Teaches the real double-entry
  standard, then explicitly marks CVL-ACADEMY's own ledger as a
  simplified `CAPABILITY_PARTIAL` case study, never implied as
  double-entry.
- **WAL-08** (Payment Infrastructure & Provider Integration) —
  `PARTIAL` via cross-ecosystem: this Academy's own Wallet has no PSP
  integration, but `gmfest972/goodmooddjsayd` has a **real, working
  Stripe integration** (`/payments/checkout`, `/stripe/webhook`,
  cited already in `docs/gmd/gmd28/`) — the one genuinely real
  payment-provider precedent anywhere in the ecosystem. Used as the
  worked case, never re-derived.
- **WAL-10** (Apple/Google Wallet & Tokenized Card Operations) —
  `SUBSTANTIAL`, the **best-grounded WAL-01→18 candidate**: real,
  correctly-shaped pass payloads exist for both platforms
  (`passes.py`) — teaches the real code and its honest unsigned-pass
  boundary directly (HTTP 200 + `"status": "unsigned"`, never a
  literal 501 — see the repo-truth correction already documented in
  `docs/wal/wal24/`).
- **WAL-13** (Financial API & Embedded Finance) — `PARTIAL`: a real,
  minimal, read-only Wallet API exists (`api/wallet.py`) — small but
  genuine worked example.

**All other 12 rows** (WAL-01/02/04/05/06/07/09/11/12/16/17/18):
`NEW_EXTERNAL`, `CAPABILITY_NOT_IMPLEMENTED` beyond the ledger/API
above — pure market-general fintech-engineering knowledge, never
claiming a CVLN capability that does not exist.

## Objectives

Teach the real, standard fintech-engineering career specializations
this cluster covers, citing real worked examples where they exist,
never inventing a capability beyond `backend/wallet/`'s real (simple,
additive-only) ledger:

- Digital ledger design and double-entry accounting standards.
- Payment infrastructure and provider integration.
- Card operations and tokenization.
- Embedded finance APIs.
- Treasury, risk, and the other market-general fintech disciplines
  with no repo touchpoint.

## Modules

1. Digital ledger fundamentals — worked example: this Academy's own
   real, additive-only `backend/wallet/` ledger, explicitly marked
   `CAPABILITY_PARTIAL` against the real double-entry standard.
2. Payment infrastructure and provider integration — worked example:
   `docs/gmd/gmd28/`'s real Stripe checkout+webhook.
3. Card operations and tokenization — worked example: `passes.py`'s
   real unsigned Apple/Google pass payloads.
4. Embedded finance APIs — worked example: `api/wallet.py`'s real
   read-only routes.
5. Treasury, risk, sales/growth, and the remaining market-general
   fintech disciplines — pure industry knowledge, no repo touchpoint.
6. Boundary discipline — never claims `backend/wallet/` implements
   holds, double-entry pairs, reversals/refunds, idempotency keys,
   transfer-between-users, marketplace/escrow, a fee engine, or a
   kill-switch (all real capabilities of the external `djsayd/
   CVLN-Wallet` product, already cited for `WAL-22/23/25/26/27` in
   `docs/wal/wal2{2,3,5,6,7}/`, never conflated with this Academy's
   own thin ledger).

## Assessment

A discipline-literacy exam graded against real fintech-engineering
practice, with an eliminatory check on claiming `backend/wallet/`
implements a capability it does not have (double-entry, holds,
transfers, marketplace, settlement, kill-switch).

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.

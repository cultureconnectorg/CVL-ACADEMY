# WAL-19→28 — Canonical Education Map

## Shared competency skeleton

Every WAL-2X formation follows the same shape:
`PROFESSIONAL_ROLE → ACTIVITIES → COMPETENCIES`, grounded in a named
file/function in `backend/wallet/` or `backend/api/wallet.py`, or an
explicit `GAP.md` where no such grounding exists.

## Dependency graph

```
WAL-19 (umbrella, prerequisite for all)
  ├── WAL-20 (CC/JCC monetary operations)
  ├── WAL-21 (ledger operator)
  │     └── WAL-28 (audit, reads the same append-only ledger)
  ├── WAL-24 (card operations — pass payloads)
  ├── WAL-22 (GAP — coffres/allocation)
  ├── WAL-23 (GAP — transfers)
  ├── WAL-25 (GAP — marketplace)
  ├── WAL-26 (GAP — settlement/reconciliation)
  └── WAL-27 (GAP — kill-switch)
```

## Anti-footprint verification (mandatory before certifying any WAL-2X)

Before crediting a candidate with any WAL-2X competency, verify the
claimed capability against the actual file cited in the corresponding
`REFERENTIAL.md` — never against a memorized summary of what a
"typical wallet system" would have. This corpus's own genuine finding
(the 501-claimed-but-never-raised discrepancy in `passes.py`) is the
reason this rule exists: even this Academy's own code comments can
describe behavior slightly differently from what the code actually
does.

## Boundary note — never merge with the real `djsayd/CVLN-Wallet` product

WAL-19→28 certifies operation of **this Academy's own** ledger
(`backend/wallet/`) — a simple, additive, single-entry system. The
real external `djsayd/CVLN-Wallet` product (holds/authorization/
capture, maker-checker, idempotency, virtual cards — see
`WALLET_CVE_RECONCILIATION.md`'s repo-truth delta) is cited only as
market/context grounding for WAL-01→18 (external, market-general
formations), never as something a WAL-2X candidate can operate — no
integration between the two repos is observed.

## Certification / mission eligibility doctrine

Certification eligibility follows the same N1/N2/assessment structure
as `CERTIFICATION_MODEL.md`. Mission eligibility for any WAL-2X role
requires the corresponding capability to exist in the real ledger —
WAL-22/23/25/26/27 have **no** mission eligibility path today, by
construction, until the underlying capability is built (tracked as
product debt, not invented).

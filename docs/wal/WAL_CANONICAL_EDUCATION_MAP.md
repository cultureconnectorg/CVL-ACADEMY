# WAL-19→28 — Canonical Education Map

## Shared competency skeleton

Every WAL-2X formation follows the same shape:
`PROFESSIONAL_ROLE → ACTIVITIES → COMPETENCIES`, grounded in a named
file/function in `backend/wallet/` or `backend/api/wallet.py`, or an
explicit `GAP.md` where no such grounding exists.

## Dependency graph

```
WAL-19 (umbrella, prerequisite for all)
  ├── WAL-20 (CC/JCC monetary operations — this Academy's ledger)
  ├── WAL-21 (ledger operator — this Academy's ledger)
  │     ├── WAL-28 (audit, reads the same append-only ledger)
  │     └── WAL-26 (settlement/reconciliation — real djsayd/CVLN-Wallet,
  │           ledger literacy transfers to reading a real settlement trail)
  ├── WAL-24 (card operations — this Academy's pass payloads)
  ├── WAL-22 (coffres/allocation — real djsayd/CVLN-Wallet)
  ├── WAL-23 (transfers — real djsayd/CVLN-Wallet)
  ├── WAL-25 (marketplace — real djsayd/CVLN-Wallet)
  └── WAL-27 (kill-switch — real djsayd/CVLN-Wallet)
```

**Corrected 2026-09-06:** WAL-22/23/25/26/27 are no longer gaps — each
is grounded directly in the real external `djsayd/CVLN-Wallet` product
(re-verified this session), while WAL-19/20/21/24/28 remain grounded in
this Academy's own `backend/wallet/`. A formation's real grounding
(this Academy vs. the external product) is stated explicitly in its own
`REFERENTIAL.md` — never blended or left ambiguous.

## Anti-footprint verification (mandatory before certifying any WAL-2X)

Before crediting a candidate with any WAL-2X competency, verify the
claimed capability against the actual file cited in the corresponding
`REFERENTIAL.md` — never against a memorized summary of what a
"typical wallet system" would have. This corpus's own genuine finding
(the 501-claimed-but-never-raised discrepancy in `passes.py`) is the
reason this rule exists: even this Academy's own code comments can
describe behavior slightly differently from what the code actually
does.

## Boundary note — two real grounding sources, never blended, never operated live

WAL-19→28 splits across two real, distinct grounding sources —
**stated explicitly per formation, never blended**:

- **This Academy's own** ledger (`backend/wallet/`) — a simple,
  additive, single-entry system — grounds WAL-19/20/21/24/28.
- The real external **`djsayd/CVLN-Wallet`** product (holds/
  authorization/capture, maker-checker, idempotency, virtual cards,
  and — corrected 2026-09-06 — coffres, transfers, marketplace,
  settlement/reconciliation, kill-switch) grounds WAL-22/23/25/26/27
  directly, in addition to serving as market/context for WAL-01→18.

**No integration between the two repos is observed either way.** A
WAL-2X candidate is certified on literacy of whichever real system
their formation cites — never granted live operational access to
either `backend/wallet/` in production or to `djsayd/CVLN-Wallet`,
regardless of which one grounds their formation.

## Certification / mission eligibility doctrine

Certification eligibility follows the same N1/N2/assessment structure
as `CERTIFICATION_MODEL.md`. Mission eligibility for any WAL-2X role
requires the corresponding capability to exist in the real ledger —
WAL-22/23/25/26/27 have **no** mission eligibility path today, by
construction, until the underlying capability is built (tracked as
product debt, not invented).

# docs/fdc/ — Fondation Cœurvolan Corpus (W6 Wave 15, Rail 1 priority 5)

```
Domain: Fondation Cœurvolan (FDC-01→48, MEM-01→10, TRN-01→07,
FDC-X-01→09) — 74 rows.
Reconciliation source: docs/cvln_academy_master/30_INTERNAL/
                        FOUNDER_CEO_GROUP_FONDATION_RECONCILIATION.md
                        (0 rejected across all 158 rows in the parent
                        reconciliation).
```

## Real grounding + entity-identity discipline

`CIP-01` (legacy, `backend/seed_data.py`, "Standardisation, archivage
et gouvernance culturelle", 30h, badge "CIP Referent") is real,
delivered curriculum — cited here as market-context only. Per
`FD-CIP-001` (Founder decision, closed): **`CIP Foundation` and
`Fondation Cœurvolan` are two distinct objects, never merged.**
`FDC-01→48` builds independently of `CIP-01` — no shared anchor, no
cross-reuse implied by this decision.

## Structure

- **`external/fdc_heritage/`** — FDC-01→20 + MEM-01→10 + TRN-01→07 (37
  rows), heritage/memory/transmission disciplines, France Travail K1602
  alignment cited, cross-referenced against `CIP-01` and Kiltikonet
  `KLT-05`/`KLT-06` without duplicating either.
- **`FDC_X_BRIDGE_NOTE.md`** — FDC-X-01→09 (9 rows), citation-only
  bridges to already-reconciled domains.
- **`NEEDS_EXPERT_REVIEW.md`** — FDC-21→35 (15 rows), philanthropic/
  non-profit governance requiring named jurisdiction + real expert.
- **`BLOCKED_CANDIDATES.md`** — FDC-36→48 (13 rows), internal-
  restricted foundation operations, no archive/grant/governance system
  exists.

## Status

| Set | Rows | Depth |
|---|---|---|
| FDC heritage (`external/fdc_heritage/`) | 37 | `MODULE_CONTENT_DRAFTED` |
| FDC-X bridges (`FDC_X_BRIDGE_NOTE.md`) | 9 | Citation-only index, no separate formation |
| `NEEDS_EXPERT_REVIEW.md` | 15 | `NEEDS_EXPERT_REVIEW`, no content |
| `BLOCKED_CANDIDATES.md` | 13 | `BLOCKED_PRODUCT_DEPENDENCY` |

**37 + 9 + 15 + 13 = 74.** All 74 rows accounted for. 0/74
`PACKAGE_COMPLETE` (no flagship this wave — legacy `CIP-01` is runtime
content, not rebuilt), 37/74 `MODULE_CONTENT_DRAFTED`, 9/74
citation-only, 15/74 `NEEDS_EXPERT_REVIEW`, 13/74
`BLOCKED_PRODUCT_DEPENDENCY`.

**Canonical state — never summarized otherwise:** this corpus is
**not** `PACKAGE_COMPLETE`, never merges `CIP Foundation`'s identity
with `Fondation Cœurvolan`'s (`FD-CIP-001`), and never simulates a
real foundation archive/grant/governance system.

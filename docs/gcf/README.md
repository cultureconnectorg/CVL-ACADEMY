# docs/gcf/ — Gala Cook & Food Corpus (W6 Wave 10, Rail 1 priority 4)

```
Domain: Gala Cook & Food (GCF-01→30, GCF-X-01→08) — 38 rows.
Reconciliation source: docs/cvln_academy_master/20_EXTERNAL/
                        CYBERSECURE_BLOCKCHAIN_GALA_HOSPITALITY_
                        LABELOS_RECONCILIATION.md (0 rejected).
```

## Real grounding

`AGR-01` (legacy, `backend/seed_data.py`, "Transformation
agroalimentaire et branding caribéen", 40h) is **adjacent, not
overlapping**: production/filière transformation and branding, not
restaurant/culinary service delivery. It is never rebuilt here — only
cited as the real Agro-side grounding for `GCF-X-01`.

## Structure

- **`external/gcf01_18/`** — GCF-01→18, the culinary/restaurant/
  catering industry pathway (chef, pastry, restaurant ops, catering,
  menu engineering, food branding), `NEW_EXTERNAL`.
- **`GCF_X_BRIDGE_NOTE.md`** — GCF-X-01→08: 3 real bridges build now
  (×Agro, ×Hospitality, ×Good Mood), 1 converges on `MISSIONS_
  PIPELINES.md`, 1 partial-citable on Wallet/CVE, 3 fully blocked.
- **`BLOCKED_CANDIDATES.md`** — GCF-19→30 (internal operator, 12 rows,
  no kitchen/restaurant/catering system exists anywhere audited) + the
  3 fully-blocked GCF-X rows.

## Status

| Set | Rows | Depth |
|---|---|---|
| GCF-01→18 (`external/gcf01_18/`) | 18 | `MODULE_CONTENT_DRAFTED` |
| GCF-X-01/02/03/07/08 (`GCF_X_BRIDGE_NOTE.md`) | 5 | Bridge index (3 real citations + 1 converged + 1 partial), no separate formation |
| GCF-19→30 + GCF-X-04/05/06 (`BLOCKED_CANDIDATES.md`) | 15 | `BLOCKED_PRODUCT_DEPENDENCY` |

**18 + 5 + 15 = 38.** All 38 rows accounted for. 0/38
`PACKAGE_COMPLETE` (no flagship this wave), 18/38
`MODULE_CONTENT_DRAFTED`, 20/38 not independently built (15 blocked +
5 bridge-index).

**Canonical state — never summarized otherwise:** this corpus is
**not** `PACKAGE_COMPLETE` as a domain, and never conflates its
culinary/restaurant scope with `AGR-01`'s adjacent production scope.

# docs/cyb/ — CVLN CyberSecure Corpus (W6 Wave 8, Rail 1 priority 4)

```
Domain: CVLN CyberSecure (CYB-01→42) — 42 rows.
Reconciliation source: docs/cvln_academy_master/20_EXTERNAL/
                        CYBERSECURE_BLOCKCHAIN_GALA_HOSPITALITY_
                        LABELOS_RECONCILIATION.md (0 rejected).
Resolves Gap Register G8 (security boundary).
```

## Structure

- **`external/cyb01_30/`** — CYB-01→30, 30 rows, real
  security-engineering career specializations, taught as
  industry-general knowledge (`MODULE_CONTENT_DRAFTED`).
- **`internal/cyb32/`** — CYB-32 (IAM), the one internal-operator row
  buildable now, grounded directly in `backend/auth.py`'s real
  JWT/bcrypt/refresh-token-rotation architecture (`PACKAGE_COMPLETE`,
  this wave's flagship).
- **`BLOCKED_CANDIDATES.md`** — CYB-31, CYB-33→42 (11 rows), genuinely
  `BLOCKED_PRODUCT_DEPENDENCY` — no corresponding CVLN system exists
  to operate (no secrets manager, SOC, red-team program, etc.).
- **`EXTEND_EXISTING_NOTE.md`** — cross-domain security rows already
  flagged elsewhere (`FRK-48/49/50/51/70`, `KLT-17`, `WAL-14`) that
  point here rather than re-teaching security fundamentals per
  product.

## Status

| Set | Rows | Depth |
|---|---|---|
| CYB-01→30 (`external/cyb01_30/`) | 30 | `MODULE_CONTENT_DRAFTED` |
| CYB-32 (`internal/cyb32/`) | 1 | `PACKAGE_COMPLETE` (flagship) |
| CYB-31, CYB-33→42 (`BLOCKED_CANDIDATES.md`) | 11 | `BLOCKED_PRODUCT_DEPENDENCY` |

**30 + 1 + 11 = 42.** All 42 rows accounted for. 1/42 `PACKAGE_COMPLETE`,
30/42 `MODULE_CONTENT_DRAFTED`, 11/42 `BLOCKED_PRODUCT_DEPENDENCY`.

**Canonical state — never summarized otherwise:** this corpus is
**not** `PACKAGE_COMPLETE` as a domain. Only CYB-32 is.

# GCF-X-01→08 — Gala Cook & Food Cross-Ecosystem Bridges

Per the reconciliation:

| Row | Bridge | Resolution |
|---|---|---|
| GCF-X-01 | × CVL Agro | `PARTIAL` — real `AGR-01` (legacy, `backend/seed_data.py`) grounds the Agro side. Best-grounded GCF bridge. `NEW_CROSS_ECOSYSTEM` — cites `AGR-01` by reference, never rebuilds it. |
| GCF-X-02 | × Hospitality | `PARTIAL` — real legacy `HOS-01` grounds the Hospitality side. `NEW_CROSS_ECOSYSTEM` — cites `docs/hos/` by reference. |
| GCF-X-03 | × Good Mood | `PARTIAL` — real Good Mood repo (`GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`, `docs/gmd/`) grounds the Good Mood side. `NEW_CROSS_ECOSYSTEM`. |
| GCF-X-04 | × Kiltikonet | `BLOCKED_PRODUCT_DEPENDENCY` — inherits Kiltikonet's own domain block status for this bridge. |
| GCF-X-05 | × KORA | `BLOCKED_PRODUCT_DEPENDENCY` — inherits KORA's own status. |
| GCF-X-06 | × FREK | `BLOCKED_PRODUCT_DEPENDENCY` — inherits FREK's own status. |
| GCF-X-07 | × Wallet/CVE | `PARTIAL` — unblocked since `FD-CVE-001`, still gated on Wallet richness; cites `docs/wal/` and `docs/cve/`. |
| GCF-X-08 | × Academy (pipeline) | `EXTEND_EXISTING` — reuses `MISSIONS_PIPELINES.md`'s "Learning-to-Opportunity" pattern verbatim, same convergence discipline as `KOR-X-06`. |

**3 rows build now** (GCF-X-01/02/03, real bridges — cite the counterpart
domain's real grounding, never re-derive it), **1 row converges**
(GCF-X-08, `EXTEND_EXISTING` on `MISSIONS_PIPELINES.md`), **1 row is
partial-citable** (GCF-X-07, on `FD-CVE-001` + Wallet), **3 rows are
fully `BLOCKED_PRODUCT_DEPENDENCY`** (GCF-X-04/05/06).

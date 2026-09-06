# GMD-X-01→09 — Good Mood Cross-Ecosystem Bridges (9 rows)

Per the reconciliation:

| Row | Bridge | Resolution |
|---|---|---|
| GMD-X-01 | × FREK | `SUBSTANTIAL` — real `frek_service.py` outbox (env-gated, persistent retry queue, backoffs `[30s,2m,10m,1h,6h]`). `NEW_CROSS_ECOSYSTEM`, buildable now — same bridge pattern as `FRK-56`/`KOR-X-01`, cross-linked to `docs/gmd/gmd31/` rather than re-derived. |
| GMD-X-02 | × Wallet | `SUBSTANTIAL` — real `wallet_service.py` outbox, same pattern. `NEW_CROSS_ECOSYSTEM`, buildable now — cross-linked to `docs/gmd/gmd32/` and the `WAL-X` cluster (`docs/wal/`). |
| GMD-X-03 | × CVE | `NONE` product-level footprint, but methodology now `FORMALIZED_METHODOLOGY` (`FD-CVE-001`). `NEW_CROSS_ECOSYSTEM` — unblocked, citing `docs/cve/`; `CALIBRATION_PENDING` where the bridge touches uncalibrated parameters. |
| GMD-X-04 | × Kiltikonet | `BLOCKED_PRODUCT_DEPENDENCY` — no Kiltikonet repo named for this specific bridge. |
| GMD-X-05 | × KORA | `BLOCKED_PRODUCT_DEPENDENCY` — live-to-media pipeline is conceptual; can cite `docs/kor/kor03/` by reference once a real bridge exists. |
| GMD-X-06 | × FMS | `PARTIAL` — both sides real (this repo + `fms-os/fms`). `NEW_CROSS_ECOSYSTEM` — the artist/production pipeline cites `FMS_07_18_RECONCILIATION.md`'s FMS-07 umbrella by reference. |
| GMD-X-07 | × LabelOS | `BLOCKED_PRODUCT_DEPENDENCY` — inherits `G3` (no LabelOS repo named), see `docs/los/`. |
| GMD-X-08 | × Gala Cook & Food | `BLOCKED_PRODUCT_DEPENDENCY` — inherits `G7`, see `docs/gcf/`. |
| GMD-X-09 | × Academy (mission-to-experience) | `EXTEND_EXISTING` — reuses `80_MISSIONS/MISSIONS_PIPELINES.md` verbatim, don't re-derive (same convergence discipline as `KOR-X-06`). |

**5 rows build/reuse now** (GMD-X-01/02/03/06/09, each citing real code
or already-`DECIDED`/`FORMALIZED` doctrine, never fabricating a wired
integration beyond what exists), **4 rows fully `BLOCKED_PRODUCT_
DEPENDENCY`** (GMD-X-04/05/07/08, each inheriting its counterpart
domain's own block status).

## Summary

| Row | Resolution | New content |
|---|---|---|
| GMD-X-01 | Real `frek_service.py` outbox | Yes (bridge module) |
| GMD-X-02 | Real `wallet_service.py` outbox | Yes (bridge module) |
| GMD-X-03 | Unblocked on `FD-CVE-001` | Yes (bridge module, `CALIBRATION_PENDING` noted) |
| GMD-X-04 | `BLOCKED_PRODUCT_DEPENDENCY` | None |
| GMD-X-05 | `BLOCKED_PRODUCT_DEPENDENCY` | None |
| GMD-X-06 | Cites `FMS-07` | Yes (bridge module) |
| GMD-X-07 | `BLOCKED_PRODUCT_DEPENDENCY` | None |
| GMD-X-08 | `BLOCKED_PRODUCT_DEPENDENCY` | None |
| GMD-X-09 | Converges to `MISSIONS_PIPELINES.md` | None |

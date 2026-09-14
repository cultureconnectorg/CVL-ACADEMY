# docs/kor_op/ — KORA Internal Operator & Cross-Ecosystem Layer (KOR-OP/KOR-X, W6 Wave 7)

```
Domain: KOR-OP-01→12 (internal operator roles, 12 rows) + KOR-X-01→07
(cross-ecosystem bridges, 7 rows) — 19 rows total, Rail 1 priority 3
("KORA interne/cross").
Reconciliation source: docs/cvln_academy_master/30_INTERNAL/
                        KORA_OP_X_RECONCILIATION.md (0 rejected).
```

## Why this corpus looks different from FREK/AGF

Per the reconciliation's own finding: unlike FMS/KLT (where the market
and internal layers are separate Master 2D candidates against an
existing market corpus), KORA's 19 rows map **almost entirely onto the
already-built `docs/kor/kor01→15` corpus** — each of those 15
formations already carries a real internal-facing `§6 KORA_PRODUCT_GAP`
section and a `§5` boundary section covering most of what these 19
rows ask for. Building 19 new parallel formations here would violate
`NO_DUPLICATE_CURRICULUM` — the reconciliation's own verdict is that
this is **mostly an indexing exercise, not a fresh audit or a fresh
build.**

So this corpus contains, deliberately, three different things:

- **`KOR_OP_FRAMING_NOTES.md`** — 11 short (~1 page each) internal-role
  framing notes for KOR-OP-01→11, each **pointing to** the existing
  `docs/kor/korXX/` formation and module(s) that already teach the
  competency, rather than re-teaching it. `EXTEND_EXISTING`, per the
  reconciliation.
- **`kor_op12/`** — one genuinely new, narrow formation (KOR-OP-12,
  Release Operations) — the single row without a clean 1:1 existing
  anchor. Built to full canonical package depth (`PACKAGE_COMPLETE`).
- **`KOR_X_BRIDGE_INDEX.md`** — one converged index for the 7
  cross-ecosystem rows (KOR-X-01→07), explicitly de-duplicating
  against bridges already built under a *different* Master 2D row
  number in another domain (`FRK-56`, `LOS-X-03`, `WAL-X-01`) rather
  than re-describing the same relationship a second or third time.

## What this corpus does NOT do

- It does **not** touch or rebuild `docs/kor/kor01→15` — that corpus
  stays exactly as it is (`CORE_BUILD = COMPLETE` visé for KOR-01→10,
  `STATUS = PROPOSED` for KOR-11→15, per each formation's own
  `REFERENTIAL.md` — untouched here).
- It does **not** invent a KOR-OP framing note for KOR-OP-12 — that row
  gets a real new formation instead, because no existing module covers
  it.
- It does **not** re-describe KOR-X-01/02/03 as if they were novel —
  each is explicitly flagged as *the same real relationship* already
  documented under `FRK-56`, `LOS-X-03`, `WAL-X-01` respectively.
- It never claims `FULLY_COMPLETE` for KOR-OP-12 or for this corpus as
  a whole — `PACKAGE_COMPLETE` means the package exists and is
  repo-truth-grounded, not that a real candidate has been assessed.

## Status

| Set | Rows | Depth |
|---|---|---|
| KOR-OP-01→11 (`KOR_OP_FRAMING_NOTES.md`) | 11 | `EXTEND_EXISTING`, framing notes complete, no separate formation |
| KOR-OP-12 (`kor_op12/`) | 1 | `PACKAGE_COMPLETE` — new, narrow, full canonical package |
| KOR-X-01→07 (`KOR_X_BRIDGE_INDEX.md`) | 7 | Converged index complete — 6 rows point to already-documented bridges (4 of them literally the *same* bridge as `FRK-56`/`LOS-X-03`/`WAL-X-01`), 1 row (KOR-X-04, KORA×CVE) newly indexed on `FD-CVE-001`'s closed methodology |

**11 + 1 + 7 = 19.** All 19 rows accounted for. 12/19 rows resolve to
`EXTEND_EXISTING`/converged-index (11 KOR-OP + 6 KOR-X, no new content
beyond the index/framing note itself, per the reconciliation's own
"genuinely light work" characterization), 1/19 is a genuinely new
`PACKAGE_COMPLETE` formation (KOR-OP-12).

**Canonical state — never summarized otherwise:** this closes Rail 1's
"KORA interne/cross" priority. It does **not** make the 15-formation
`docs/kor/` corpus itself any more complete than it already was — see
`docs/kor/README.md`'s own `FULLY_COMPLETE = FALSE` standing notice.

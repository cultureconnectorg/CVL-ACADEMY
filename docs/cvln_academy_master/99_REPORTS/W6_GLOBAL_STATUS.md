# W6 Global Status — Real State Per Domain (established 2026-09-06)

```
Built entirely from existing files and their own declared statuses —
no re-audit of the 812-row reconciliation, no doctrine change, no
rebuild of already-terminated phases. Purpose: pick the next W6 wave
on real, current evidence rather than an arbitrary domain choice.

Taxonomy (per Founder instruction, 2026-09-06):
NOT_STARTED        — no reconciliation and no corpus exist yet (none
                      of the 812 rows are in this state — all 812 are
                      reconciled; kept in the taxonomy for completeness)
RECONCILED_NOT_BUILT — reconciliation exists (verdict per row), zero
                      W6 pedagogical corpus (no docs/<domain>/ folder)
DRAFTED            — a corpus exists, at referential+modules depth
                      (MODULE_CONTENT_DRAFTED in the per-corpus files)
PARTIAL_PACKAGE    — a corpus exists with some but not all of the full
                      canonical package elements per formation (mixed
                      depth within the domain, or explicit
                      STRUCTURAL_STATUS=PARTIAL in its own files)
PACKAGE_COMPLETE   — every formation in the domain has the full
                      canonical package (référentiel + N1/N2 + assessment/
                      rubric + evidence model + 3 guides + integration
                      note) — never implies FULLY_COMPLETE (no formation
                      anywhere in this Master Package has had a real
                      candidate pass yet)
BLOCKED            — construction cannot proceed without something
                      external: a Founder/governance authorization gate
                      (Kiltikonet's own STOP=TRUE), or a genuine product
                      gap with no real capability to teach (GMD-34)
```

## Pre-existing canon (predates the 812-row Master 2D reconciliation)

| Domain | Rows | Corpus | Real state (from files) |
|---|---|---|---|
| KOR-01/02 (KORA core professions) | 2 | `docs/kor/kor01/`, `kor02/` | `PACKAGE_COMPLETE` — deepest corpus in the estate (2,741 / 2,271 lines across référentiel/modules/case/guides/skills/templates/assessments) |
| KOR-03→10 (KORA professions) | 8 | `docs/kor/kor03→10/` | `PARTIAL_PACKAGE` — same folder shape as KOR-01/02 (référentiel/modules/case/guides/skills/templates) but substantially lighter (1,295–1,616 lines each); no explicit `PACKAGE_COMPLETE` self-declaration found in these files |
| KOR-11→15 (KORA professions) | 5 | `docs/kor/kor11→15/` | `DRAFTED` — each `REFERENTIAL.md` self-declares `STATUS = PROPOSED`; lightest of the KOR corpus (887–1,021 lines) |
| KLT-01→05 (Kiltikonet core professions) | 5 | `docs/klt/klt01→05/` | `PACKAGE_COMPLETE` — deep corpus (1,816–2,457 lines, 27-30 files each) |
| KLT-06→08 (Kiltikonet professions) | 3 | `docs/klt/klt06→08/` | `PARTIAL_PACKAGE` — each file **explicitly self-declares** `STRUCTURAL_STATUS = PARTIAL` (5/7, 6/7, 6/7 compétences construites) |
| FMS-01→06 (Factory Maker Studio core) | 6 | `backend/fms_canonical/`, `backend/fms_import/` (real runtime-bound corpus, not a `docs/` markdown corpus) | `PACKAGE_COMPLETE`-equivalent — real, running product content (distinct delivery mode from the markdown corpora; verified in ACA-0002→0006 per this repo's own history) |

**Governance note, unchanged, never touched this session:** Kiltikonet's own `docs/klt/README.md` declares `STOP = TRUE` after the KLT-01→08 delivery ("intégration runtime Academy et tout nouveau chantier ACA restent NOT_AUTHORIZED"). KLT-09→20 (below) inherits this as a `BLOCKED` (authorization-gated) status, not merely `RECONCILED_NOT_BUILT` — construction requires a Founder authorization this session has not received and does not request.

## The 812-row Master 2D reconciliation — 10 domain batches

| Domain | Rows | Corpus | Real state (from files) |
|---|---|---|---|
| Good Mood + DJ Sayd | 94 | `docs/gmd/` (GMD-21→34) | `PACKAGE_COMPLETE` for GMD-21→33 (13/13, closed this session — see `docs/gmd/QUALITY_GATES.md`); `BLOCKED` for GMD-34 (product gap, `gmd34/GAP.md`, by design, never simulated). DJ Sayd's own external/market rows (the other ~51/94) remain `RECONCILED_NOT_BUILT` — no W6 corpus started for the DJ Sayd market-professional side yet. |
| Wallet + CVE | 52 | `docs/wal/` (WAL-19→28), `docs/cve/` (CVE-01→15) | `PACKAGE_COMPLETE` for WAL-19, CVE-02 (2/25 formations across both corpora); `DRAFTED` for the other 23 (WAL-20/21/22/23/24/25/26/27/28, CVE-01/03→15) — corrected this session, `0/25` `BLOCKED` (WAL-22/23/25/26/27 un-blocked via the `djsayd/CVLN-Wallet` checkpoint). WAL-01→18 (external/market side, 18 rows) remain `RECONCILED_NOT_BUILT`. WAL-X-01→09 (9 rows) remain `RECONCILED_NOT_BUILT`. |
| KORA (interne/cross) | 19 | none | `RECONCILED_NOT_BUILT` — `KORA_OP_X_RECONCILIATION.md` verdicts exist (KOR-OP-01→12, KOR-X-01→07), no `docs/kor_op/` or equivalent corpus started. |
| FREK (FRK-01→75) | 75 | `docs/frk/` — **full domain, 75/75 accounted for** | `PARTIAL_PACKAGE` (was `RECONCILED_NOT_BUILT`) — 54/75 `PACKAGE_COMPLETE` (full deepening pass across Batches A→I this session, every formation without a real blocker or `NEEDS_EXPERT_REVIEW` flag, plus FRK-16 reclassified post-pass on new repo-truth from `Cvln-ios-v.1`'s own governance corpus — MetaCVLN's real Notary & Public Audit + OpenTimestamps anchoring); 3/75 `MODULE_CONTENT_DRAFTED` (FRK-10 EUDI/eIDAS2, FRK-14 chain-of-custody, FRK-73 applied cryptography — all `NEEDS_EXPERT_REVIEW`, 8/8 supporting files written but never promoted without a real named expert's review); 10/75 `BLOCKED_PRODUCT_DEPENDENCY` (`GAP.md`, genuine repo/spec gaps, re-verified against `Cvln-ios-v.1` and confirmed unchanged, no invention); 8/75 `EXTEND_EXISTING` (fold into a sibling or an existing Master Package doc — FRK-05, FRK-45/46, FRK-48/49/50/51/70 — no separate formation, per the reconciliation's own verdict). See `docs/frk/README.md` and `docs/frk/QUALITY_GATES.md`. |
| Agent Factory/AF-X/Laurentia/IOS/Brain/CMD/Intelligent Operations | 109 | `docs/agf/` — `external/` (53 rows) + `internal/` (6 formations, CMD-15 flagship) | `PARTIAL_PACKAGE` (was `RECONCILED_NOT_BUILT`) — CMD-15 `PACKAGE_COMPLETE` (grounded on `MetaCVLN`'s real `/command-center/*` routes, Wave-2-corrected maturity); 58/109 `MODULE_CONTENT_DRAFTED` (53 external market-general + 5 other internal, each internal one grounded strictly on `CVLNAgentfactory`/`Cvln-ios-v.1`/`Laurent.ia`/`MetaCVLN`, never extrapolated); 39/109 `BLOCKED_PRODUCT_DEPENDENCY` (unchanged by Wave 2 — real repos exist but none wired to `CVL-ACADEMY`); 11/109 `EXTEND_EXISTING` (AF-22, SYS-01→10, no separate file). See `docs/agf/README.md`/`QUALITY_GATES.md`. |
| CyberSecure+Blockchain+Tokenomics+Gala+Hospitality+LabelOS | 214 | none | `RECONCILED_NOT_BUILT` — `CYBERSECURE_BLOCKCHAIN_GALA_HOSPITALITY_LABELOS_RECONCILIATION.md` verdicts exist, no pedagogical corpus started. Real legacy anchors already exist for 4 sub-domains (CyberSecure `CYB-31→42` on real `backend/auth.py`, Blockchain `BCH-01`, Hospitality `HOS-01`, LabelOS `LOS-01`) — these are the best-grounded starting rows in this domain. |
| Founder/CEO+CVLN Group+Fondation Cœurvolan | 158 | none | `RECONCILED_NOT_BUILT` — `FOUNDER_CEO_GROUP_FONDATION_RECONCILIATION.md` verdicts exist (incl. `FD-CIP-001` closure), no pedagogical corpus started. `NEEDS_EXPERT_REVIEW` rows (legal/fiscal/philanthropic, ~25 rows) stay explicitly unbuildable without a real expert, by design — never a universal recipe. |
| Kiltikonet (KLT-09→20) | 12 | none | `BLOCKED` — reconciled (`KLT_09_20_RECONCILIATION.md`), but inherits `docs/klt/`'s own `STOP=TRUE` authorization gate; this session's repo-truth delta additionally flags that KLT-06/07's old `BLOCKED` sub-verdicts (Observatory/Network) should be re-checked against `Kiltikonet-Aout2026` (now canonical) before any future authorized wave, not assumed still accurate. |
| FMS (FMS-07→18) | 12 | `docs/fms/` (9 formations after merges: FMS-07 absorbs 14/16, FMS-18 absorbs 17) | `PARTIAL_PACKAGE` (corrected this session, was `RECONCILED_NOT_BUILT`) — FMS-07 (umbrella, flagship) `PACKAGE_COMPLETE`; FMS-08/09/10/11/12/13/15/18 `MODULE_CONTENT_DRAFTED`; 0/9 `BLOCKED`. FMS-07/15/18 grounded directly in the real, re-read `fms-os/fms/backend/server.py`; FMS-08/09/11 anchored by reference on the Founder-gated FMS-01→06 canon; FMS-10/12/13 new professions with explicit cross-reference boundaries. See `docs/fms/QUALITY_GATES.md`. |
| Cross-CVLN (XCV-01→67) | 67 | none | `RECONCILED_NOT_BUILT`, mostly `EXTEND_EXISTING` — `XCV_TRANSVERSAL_RECONCILIATION.md` merges `XCV-57→66` into the Agent Factory cluster's own `SYS-01→10` pipeline (no separate build needed for those 10); the remaining ~57 rows (`XCV-01→56`) still need their own W6 pass once `80_MISSIONS/MISSIONS_PIPELINES.md` exists to anchor them. |

## Summary — real, current W6 depth across all 27 domains + pre-existing canon

| State | Domains / sub-domains in this state |
|---|---|
| `PACKAGE_COMPLETE` | KOR-01/02, KLT-01→05, FMS-01→06 (pre-existing canon); GMD-21→33 (13/13); WAL-19; CVE-02; FMS-07; FRK-01/03/06/13/56/58/59/68 (8); CMD-15 |
| `PARTIAL_PACKAGE` | KOR-03→10 (8), KLT-06→08 (3); FMS-07→18 (9, 1/9 `PACKAGE_COMPLETE`, 8/9 `DRAFTED`); FREK (75, 54/75 `PACKAGE_COMPLETE`, 3/75 `DRAFTED` (`NEEDS_EXPERT_REVIEW`), 10/75 `BLOCKED`, 8/75 `EXTEND_EXISTING`); Agent Factory cluster (109, 1/109 `PACKAGE_COMPLETE`, 58/109 `DRAFTED`, 39/109 `BLOCKED`, 11/109 `EXTEND_EXISTING`) |
| `DRAFTED` | KOR-11→15 (5); WAL-20/21/22/23/24/25/26/27/28 (9); CVE-01,03→15 (14); FMS-08/09/10/11/12/13/15/18 (8); FRK (47 — see `docs/frk/README.md`); AGF (58 — see `docs/agf/README.md`) |
| `BLOCKED` | GMD-34 (product gap); Kiltikonet KLT-09→20 (governance gate); FRK-16/19/21/22/24/39/57/64/65/66/67 (11, `docs/frk/*/GAP.md`); AF-18/19/20/21/23/25/24, AF-X-01/02/04/05/06/07/08/09, IOS-01→06/08→25 (39, `docs/agf/BLOCKED_CANDIDATES.md`) |
| `RECONCILED_NOT_BUILT` | Good Mood/DJ Sayd external-market rows (~51); WAL-01→18 + WAL-X (27); KORA interne/cross (19); CyberSecure+Blockchain+Gala+Hospitality+LabelOS (214); Founder/CEO+Group+Fondation (158); Cross-CVLN XCV-01→56 (~57) |

## What this changes, and what it does not

This document is a **status survey**, not a reconciliation. It does not
reopen, re-verdict, or rebuild anything above `RECONCILED_NOT_BUILT` —
KOR-01→15, KLT-01→08, FMS-01→06, GMD-21→34, WAL-19→28, and CVE-01→15
all keep exactly the status their own files declare. It exists so the
next W6 wave is chosen on real, current evidence (which domains are
`RECONCILED_NOT_BUILT` with no corpus at all vs. which are mid-depth
and could be deepened) rather than arbitrarily.

## Status

`STATUS = LIVE SURVEY`, to be re-read (not re-derived from scratch)
before each future wave-selection decision, and updated in place as
domains move between states.

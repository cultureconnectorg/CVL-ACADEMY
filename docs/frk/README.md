# docs/frk/ — FREK Pedagogical Corpus (W6 Wave 5, first slice of FRK-01→75)

```
Domain: FREK / FREKCORE — cultural trust & provenance infrastructure
Reconciliation source: docs/cvln_academy_master/20_EXTERNAL/
                        FREK_01_75_RECONCILIATION.md (75-row candidate
                        map, 0 rejected, FRK-71 Founder decision closed)
Repo grounding: this Academy's own backend/services/frek_core.py
                (re-read in full this session, 142 lines), plus the
                real FREK_PROOF_MAPPING headers already carried by
                every docs/kor/ module, plus Good Mood's two real
                outbox clients (frek_service.py, wallet_service.py,
                already cited in docs/gmd/gmd31, gmd32).
```

## Why only 8 of 75 this wave

`FREK_01_75_RECONCILIATION.md` explicitly sequences a 75-candidate
domain by "solidité d'ancrage," not by code order. This wave builds
exactly its **tier 1-3 build priority** — the formations buildable
today on real, re-verified code, without inventing anything for the
`CAPABILITY_NOT_IMPLEMENTED`/`BLOCKED_PRODUCT_DEPENDENCY` majority of
the domain (`.fk` format, FREKANSLA, notary, watchdog, production ops
— all left untouched, exactly as reconciled):

| Tier | Formations | Why first |
|---|---|---|
| 1 — best-grounded | FRK-01, FRK-58 | Entry point + the one integration that already exists in code |
| 2 — internal operator | FRK-03, FRK-06, FRK-13 (internal half), FRK-68 | Buildable on real `frek_core.py` usage today |
| 3 — cross-ecosystem bridges | FRK-56, FRK-59 | Partial real grounding (KOR docs, Good Mood's two outboxes) |

The remaining 67 candidates (market-general clusters, the FRK-71→75
architecture cluster, and everything `BLOCKED_PRODUCT_DEPENDENCY`)
stay `RECONCILED_NOT_BUILT` — a future wave, not this one.

## Repo-truth table

| Formation | Real grounding | Cited source |
|---|---|---|
| FRK-01 (Foundations, flagship) | `backend/services/frek_core.py` (full contract, re-read this session) | `mint_frek_id()`, `emit_signal()`/`VALID_SIGNALS` (8 types), `issue_proof()` (stub), `resolve_stade()`/`STADE_THRESHOLDS` (6 tiers), `is_remote_enabled()` |
| FRK-58 (FREK × CVLN Academy Integration) | `backend/services/frek_core.py` — this formation **is** the entire real FREK footprint in this repo | same file, integration framing |
| FRK-03 (FREK Operator) | Real usage of `emit_signal`/`mint_frek_id`/`resolve_stade` across FMS/KLT/KOR modules | `FREK_PROOF_MAPPING` headers in every `docs/kor/korXX/modules/*.md` |
| FRK-06 (FREK-ID Operations) | `mint_frek_id()` — sequential counter, `db.counters`, format `FREK-042` | `frek_core.py` lines 80-95 |
| FRK-13 (FREK Proof Engine, internal half) | `issue_proof()` — **stub only**, random UUID, no crypto, no chain-of-custody | `frek_core.py` lines 116-133 |
| FRK-68 (FREK Auditor) | `db.frek_signals` (real, written by `emit_signal`) + Good Mood's outbox tables (`db.frek_outbox`, `db.wallet_outbox`) as real inspectable audit surfaces | `frek_core.py` + `docs/gmd/gmd31`, `gmd32` |
| FRK-56 (FREK × KORA Integration) | Every `docs/kor/korXX/` module already carries a real `FREK_PROOF_MAPPING` header, `READY_FOR_FREK_PROOF = FALSE` everywhere (no external verifiable anchor exists) | `docs/kor/kor01/skills/EVIDENCE_MODEL.md` |
| FRK-59 (FREK × CVLN Wallet Integration) | Good Mood's `frek_service.py` + `wallet_service.py` — **two independent, real, env-gated outbox clients, never linked to each other** | `docs/gmd/gmd31/REFERENTIAL.md`, `gmd32/REFERENTIAL.md` |

**Cross-domain contamination guards already in force, restated here:**
- This Academy's `frek_core.py` (Academy-internal client) is never
  confused with `cultureconnectorg/frekcoreAout2026`'s `frek_v3/`
  architecture cluster (FRK-71→75, a different, more mature,
  not-yet-production layer of the same eventual product).
- Good Mood's `frek_service.py`/`wallet_service.py` (outbound clients
  to an *external* FREK-ID/Wallet URL) are never confused with this
  Academy's own `frek_core.py`/`backend/wallet/` — same *pattern*
  (env-gated outbox, local fallback), never the same *channel*. This
  is the single most-repeated boundary in this whole corpus.

## Status (this wave)

| Formation | Status |
|---|---|
| FRK-01 | `PACKAGE_COMPLETE` — flagship, deepened this wave |
| FRK-03, FRK-06, FRK-13, FRK-56, FRK-58, FRK-59, FRK-68 | `MODULE_CONTENT_DRAFTED` — full référentiel written; N1/N2 banks and full guide set not yet built |

**1/8 `PACKAGE_COMPLETE`, 7/8 `MODULE_CONTENT_DRAFTED`, 0/8
`BLOCKED`.** No formation in this slice is blocked — every one of the
8 has real, re-verified grounding. The other 67 FRK-01→75 candidates
remain exactly as `FREK_01_75_RECONCILIATION.md` classified them —
this wave neither reopens nor promotes any of them.

## What this corpus does NOT do

- Does not claim `issue_proof()` produces a real cryptographic proof —
  it is a random UUID stub, taught explicitly as such (FRK-13's
  central teaching point).
- Does not claim any `READY_FOR_FREK_PROOF = TRUE` anywhere — no
  external verifiable anchor exists in this repo for any formation.
- Does not imply Good Mood's two outboxes are wired to each other or
  to this Academy's own `frek_core.py`/`backend/wallet/` — none of
  that integration is observed anywhere.
- Does not touch the FRK-71→75 architecture cluster, the market-general
  clusters, or anything `BLOCKED_PRODUCT_DEPENDENCY` — left for a
  future wave, per the reconciliation's own sequencing.

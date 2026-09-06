# docs/frk/ — FREK Pedagogical Corpus (W6 Wave 5, full domain, 75/75)

```
Domain: FREK / FREKCORE — cultural trust & provenance infrastructure
Reconciliation source: docs/cvln_academy_master/20_EXTERNAL/
                        FREK_01_75_RECONCILIATION.md (75-row candidate
                        map, 0 rejected, FRK-71 Founder decision closed)
Repo grounding: this Academy's own backend/services/frek_core.py
                (re-read in full this session, 142 lines); the real
                FREK_PROOF_MAPPING headers already carried by every
                docs/kor/ module; Good Mood's two real, unlinked outbox
                clients (frek_service.py/wallet_service.py, already
                cited in docs/gmd/gmd31,32); frekcoreAout2026's real
                frek_v3/ architecture corpus + reference_verifier/
                (already audited this session, REPO_REGISTRY.md).
```

## Full domain accounting — 75/75

`FREK_01_75_RECONCILIATION.md` classified all 75 candidates with 0
rejections. This corpus now accounts for every one of them, at the
depth its own real grounding (or genuine absence of grounding)
supports — **never** built past that depth. This section reflects the
completed deepening pass (Batches A→I, this pass): every formation not
held by a `NEEDS_EXPERT_REVIEW` flag or a genuine `GAP`/`EXTEND_
EXISTING` verdict has been deepened to a full 9-file `PACKAGE_
COMPLETE` package.

| Depth | Count | Candidates |
|---|---|---|
| `PACKAGE_COMPLETE` | 53 | FRK-01,02,03,04,06,07,08,09,11,12,13,15,17,18,20,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,40,41,42,43,44,47,52,53,54,55,56,58,59,60,61,62,63,68,69,71,72,74,75 — full canonical package (référentiel + N1/N2 banks + assessment/rubric + evidence model + 3 guides + integration note) |
| `MODULE_CONTENT_DRAFTED` (`NEEDS_EXPERT_REVIEW`, held) | 3 | FRK-10 (EUDI/eIDAS2, EU-jurisdiction-specific), FRK-14 (chain-of-custody, forensic/legal-adjacent), FRK-73 (applied cryptography) — all 8 supporting files written, but never promoted past `MODULE_CONTENT_DRAFTED` without a real, named human expert's documented review |
| `BLOCKED_PRODUCT_DEPENDENCY` (`GAP.md`, no invented content) | 11 | FRK-16,19,21,22,24,39,57,64,65,66,67 |
| `EXTEND_EXISTING` (folds into a sibling or an existing Master Package doc — no separate file) | 8 | FRK-05 (intro to FRK-56→60), FRK-45/46 (reuse `AUTHORIZATION_MODEL.md`), FRK-48/49/50/51/70 (point to `CYB-31→42`, itself not yet built) |

**53 + 3 + 11 + 8 = 75.** Zero candidates left unaccounted for; zero
built past their real evidence. The 3 `NEEDS_EXPERT_REVIEW` exceptions
are the only formations correctly held below `PACKAGE_COMPLETE` among
those with real, teachable content — they stay there until a real,
named human expert (forensic/legal for FRK-14, EU-jurisdiction legal
for FRK-10, applied cryptography for FRK-73) documents a review.

## Build-priority tiers actually used (per the reconciliation's own
sequencing)

1. Best-grounded: FRK-01, FRK-58.
2. Internal operator (real `frek_core.py` usage): FRK-03, FRK-06,
   FRK-13, FRK-68.
3. Cross-ecosystem bridges (partial real grounding): FRK-56, FRK-59.
4. Market-general clusters (real, teachable industry-standard
   knowledge independent of any CVLN implementation gap): FRK-02, 04,
   07-12, 14-15, 17-18, 20, 23, 25-38, 40-44, 47, 52-55, 60-63, 69.
5. FREK v3 architecture cluster (`SOURCE_OBSERVED` on
   `frekcoreAout2026`, `ARCHITECTURE_LEVEL_2`): FRK-71→75.
6. `BLOCKED_PRODUCT_DEPENDENCY` (held until a real repo/spec is
   named — never built on invention): FRK-16,19,21,22,24,39,57,
   64-67.

## Cross-domain contamination guards restated across the full domain

- `frek_core.py` (this Academy's client) ≠ `frek_v3/` architecture
  cluster (FRK-71→75, a different, more mature, still-not-production
  layer of the same eventual product).
- Good Mood's `frek_service.py`/`wallet_service.py` (outbound clients)
  ≠ this Academy's own `frek_core.py`/`backend/wallet/` — same
  pattern, never the same channel.
- `services/integrations/registry.py` (this Academy's ecosystem-
  integrations config registry) ≠ a FREK cultural-object registry
  (FRK-24, blocked — no such registry exists anywhere).
- `events.py` (this Academy's own in-process pub/sub) ≠ a FREK event
  registry/bus (FRK-28, FRK-54 — used only as a real, non-FREK-branded
  worked example, never implied to be FREK infrastructure).
- FRK-29/30's "cultural fingerprint" (broad concept) ≠ FRK-74's "DSP
  fingerprint" (narrow, audio-signal-processing-specific, and
  explicitly unfinished per the v3 corpus's own `CE_QUI_MANQUE.md`).
- The `VALID_SIGNALS` real 8-value vocabulary (`frek_core.py`) ≠
  FRK-31/32's market-general "affinity/resonance/cadence/context/
  device/consent" signal vocabulary — never conflated.
- FRK-34/35/40/41's provenance-proof formations ≠ LabelOS's
  catalog/rights record (LabelOS itself unfound, `REPO_REGISTRY.md`)
  and ≠ FMS-03/08's production craft (Founder-gated canon, by
  reference only).

## Status (full domain)

**53/75 `PACKAGE_COMPLETE`, 3/75 `MODULE_CONTENT_DRAFTED`
(`NEEDS_EXPERT_REVIEW`: FRK-10/14/73), 11/75
`BLOCKED_PRODUCT_DEPENDENCY`, 8/75 `EXTEND_EXISTING` (no separate
formation).** No candidate was promoted past what its own real
grounding supports; no `BLOCKED` candidate was built on an invented
capability; no `NEEDS_EXPERT_REVIEW` formation was promoted without a
real human expert's documented review. Never summarize this as "FREK
terminé/complete" — the 3 held exceptions and the 11+8 non-
`PACKAGE_COMPLETE` candidates remain real, permanent facts of this
domain's status, not a temporary gap to round away.

## What this corpus does NOT do

- Does not claim `issue_proof()` produces a real cryptographic proof —
  stub, taught explicitly (FRK-13).
- Does not claim any `READY_FOR_FREK_PROOF = TRUE` anywhere.
- Does not imply Good Mood's two outboxes, or this Academy's own
  systems, are wired to each other where no such wiring is observed.
- Does not build FRK-16/19/21/22/24/39/57/64/65/66/67 past a declared
  `GAP.md` — every one is a genuine product-dependency gap, not a
  drafting oversight.
- Does not build separate formations for FRK-05/45/46/48/49/50/51/70 —
  each folds into a sibling or an existing Master Package document,
  per the reconciliation's own `EXTEND_EXISTING` verdict.
- Does not claim FRK-71/72/74/75's real architecture corpus is
  hardware-proven or production-integrated — `ARCHITECTURE_LEVEL_2`
  stated explicitly on every one.
- Does not promote FRK-10, FRK-14, or FRK-73 to `PACKAGE_COMPLETE` —
  all three carry their `NEEDS_EXPERT_REVIEW` flag forward unresolved,
  even though all 8 supporting files exist for each; no assessment is
  administered on any of them until a real, named human expert
  documents a review.

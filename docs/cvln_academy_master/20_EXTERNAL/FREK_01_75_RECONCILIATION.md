# FRK-01→75 — FREKCORE Deep Audit & Reconciliation

```
RULE APPLIED: same corrected method as FMS_07_18_RECONCILIATION.md v2
— curriculum coverage × occupational distinctness, CONTENT_OVERLAP !=
PROFESSIONAL_DUPLICATE. FRK-01→75 remains, per the Founder's own
directive (§6), a CANDIDATE MAP — this document does not freeze it
canonical. It reconciles it against verified repo truth and existing
Academy doctrine so the next W6 wave knows exactly what is real, what
is market-general knowledge, and what is blocked.
```

## Repo truth — the entire real FREK footprint

`backend/services/frek_core.py` (142 lines) is the **sole** FREK
implementation in `cultureconnectorg/CVL-ACADEMY` itself. Real
capabilities, verbatim:

| Method | Real behavior |
|---|---|
| `mint_frek_id()` | Sequential counter (`db.counters`), format `FREK-042`. Remote-first with local fallback (`FREK_CORE_BASE_URL` env-gated). |
| `emit_signal(user_id, signal, meta)` | 8 signal types only: `FREK-TIME/WORK/SCORE/LINK/CERT/CONTRIB/SHARE/MISSION`. Writes to `db.frek_signals` + increments a counter on `db.users`. Best-effort remote mirror. |
| `issue_proof(user_id, kind, meta)` | **Stub only** — local fallback is a random UUID (`PROOF-XXXXXXXXXX`), no cryptographic signature, no chain-of-custody, no timestamp anchoring. |
| `resolve_stade(cc_credits)` | Maps a credit count to one of 6 named progression tiers (graine→pousse→racine→branches→arbre→forêt). |
| `is_remote_enabled()` | Returns whether `FREK_CORE_BASE_URL` is set (it is not, by default). |

## Repo truth — `cultureconnectorg/frekcoreAout2026` (FREK v3 architecture corpus)

A **second, real, verified FREK footprint** exists — audited at commit
`fb272f1d491b09a6d068fb3f6c9c75d407bb0626`, `frek_v3/`:

| Artifact | What it is |
|---|---|
| `docs/FREK_V3_Architecture_Review_Final.md` | The architecture's own maturity ladder — **verbatim, teach it as written**: `1. Concept (dépassé) → 2. Architecture (✅ on est ici, verrouillé) → 3. Engineering (⏳ prochaine phase, RTL/bits exacts/résultats expérimentaux)`. FPGA named explicitly as the bridge between Level 2 and Level 3 — not yet built. |
| `docs/FREK_Attestation_Protocol_v0.1.md` (FRK-72) | A specified 283-byte binary attestation protocol, L0/L1/L2 levels. |
| `docs/FREK_Cryptographic_Architecture_Review_v0.1.md` (FRK-73) | `PUF → HKDF → DRK → AK/FK/CK` key-derivation chain, ECDSA P-256, raw-signature + canonical-message-encoding design. |
| `docs/FREK_DSP_Fingerprint_Specification_v0.1.md` (FRK-74) | Explicitly **unfinished** per the corpus's own `CE_QUI_MANQUE.md` — FFT window size, hop size, band count, and the fingerprint algorithm itself are named as still-open product decisions. |
| `reference_verifier/` (FRK-75) | **Real, working Python implementation** — `frek_constants.py`, `frek_types.py`, `frek_crypto.py`, `frek_parser.py`, `frek_registry.py`, `frek_verifier.py`, `frek_device_sim.py`, plus `test_frek_verifier.py` (16 passing tests against golden vectors). The corpus's own `CE_QUI_MANQUE.md` names the **single-implementation limitation** explicitly: a Rust cross-implementation is the named next step to prove the *spec* correct, not just this Python code — teach that limitation, never imply it's resolved. |

**Standing classification for all of FRK-71→75: `ARCHITECTURE_LEVEL_2`
/ `SOURCE_OBSERVED`.** Per the Founder's explicit correction: real
architecture-level existence is never inflated into
`NOT_FULL_ENGINEERING` (no RTL/timings), `NOT_HARDWARE_PROVEN` (no
FPGA prototype), or `NOT_PRODUCTION_INTEGRATED` (no binding to any
live FREKCORE, this Academy's `frek_core.py` included) being complete.
This is the same real-vs-aspirational discipline already applied to
`frek_core.py` itself (`issue_proof()` = stub, no real crypto) — a
different, more mature layer of the same product, still short of
production.

**Everything else the Master 2D candidate map names** (DID/VC, EUDI/
SD-JWT, provenance graphs, `.fk` object format, cultural fingerprint,
FREKRAW, FREKANSLA, chain-of-custody, notary/timestamping, Bitcoin/
OpenTimestamps, offline transport, chain watchdog, production ops,
observability, backup/restore) — still **zero code footprint**,
confirmed by exhaustive grep across `backend/`, `docs/`,
`frekcoreAout2026`, and both external repos audited earlier
(`fms-os/fms`, `gmfest972/goodmooddjsayd`).

Already-established Academy doctrine (from KOR-01→15, reused here, not
reinvented): `READY_FOR_FREK_PROOF = FALSE` on every evidence model in
`docs/kor/`; `FREK_PROOF_MAPPING` headers already exist on every KOR
module; the Academy↔FREK boundary is already the most-documented
cross-ecosystem relationship in the whole repo.

## Reconciliation table (75 rows)

Columns: **Coverage** = curriculum coverage against real Academy
content today · **Distinctness** = occupational distinctness ·
**Action** = 12-way verdict · **Note** = repo truth / cross-domain flag.

| Code | Intitulé | Coverage | Distinctness | Action | Note |
|---|---|---|---|---|---|
| FRK-01 | FREK Foundations & Cultural Trust Infrastructure | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | Entry-point formation, same role as KOR-01/KLT-01 baseline. Highest priority to build first — everything else sequences off it. |
| FRK-02 | FREKCORE Architecture & Ecosystem | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | Content must stay bounded to what `frek_core.py` actually does (signal/ID/proof-stub/stade) — never invent DID/VC architecture as if built. |
| FRK-03 | FREK Operator | NONE (curriculum) / PARTIAL (repo) | DISTINCT_OPERATOR_ROLE | NEW_INTERNAL | Buildable now: real usage patterns of `emit_signal`/`mint_frek_id`/`resolve_stade` across FMS/KLT/KOR modules are a real, inspectable operator surface. |
| FRK-04 | Cultural Provenance & Digital Trust | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | Market-general provenance concepts; CVLN-specific implementation `CAPABILITY_NOT_IMPLEMENTED`. |
| FRK-05 | FREK Ecosystem Integration | NONE | DISTINCT_SPECIALIZATION (of FRK-56→60) | EXTEND_EXISTING | Becomes the shared introduction to the 5 FRK-56→60 bridge formations, not a 6th parallel one. |
| FRK-06 | FREK-ID Operations | PARTIAL (repo) | DISTINCT_OPERATOR_ROLE | NEW_INTERNAL | Grounded in real `mint_frek_id()` — scope honestly to sequential-ID minting/counter management, not a full identity architecture. |
| FRK-07 | Digital Identity Engineering | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | Market-general IAM skill, teachable independent of a real FREKCORE repo (industry-standard knowledge). |
| FRK-08 | DID & Verifiable Credentials | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | Market-general (W3C DID/VC standards) — real, teachable, but `CAPABILITY_NOT_IMPLEMENTED` for any CVLN-specific claim. |
| FRK-09 | Identity Lifecycle, Recovery & Reconciliation | NONE | DISTINCT_SPECIALIZATION (of FRK-08) | NEW_EXTERNAL | Sequenced after FRK-08 as prerequisite, not merged into it — real, separately-practiced IAM discipline. |
| FRK-10 | EUDI, SD-JWT & Interoperable Identity | NONE | DISTINCT_SPECIALIZATION | NEW_EXTERNAL | `NEEDS_EXPERT_REVIEW` — EU regulatory-specific (eIDAS2/EUDI Wallet), never taught as universal without jurisdiction caveat. |
| FRK-11 | Digital Provenance Specialist | NONE | DISTINCT_SPECIALIZATION (of FRK-04) | SPECIALIZE_EXISTING | The practitioner/advanced track built on FRK-04, same pattern as FMS-08/09 on FMS-03. |
| FRK-12 | Evidence Engineering | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | |
| FRK-13 | FREK Proof Engine | PARTIAL (repo — `issue_proof()` stub) | DISTINCT_PROFESSION + DISTINCT_INTERNAL_ROLE | NEW_EXTERNAL (market concept) + NEW_INTERNAL (operator, current stub) | Must explicitly teach the gap between "proof engine" as a concept and today's UUID-stub reality. |
| FRK-14 | Chain of Custody & Evidence Semantics | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | `NEEDS_EXPERT_REVIEW` (forensic/legal-adjacent). |
| FRK-15 | Technical Evidence Reports & Verification | NONE | DISTINCT_SPECIALIZATION (of FRK-12/14) | NEW_EXTERNAL | Sequenced after FRK-12/14. |
| FRK-16 | FREK Digital Notary | NONE | DISTINCT_INTERNAL_ROLE | NEW_INTERNAL | `BLOCKED_PRODUCT_DEPENDENCY` — no real notarization/timestamping mechanism exists to operate. |
| FRK-17 | Trusted Timestamping & Anchoring | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | Market-general (RFC 3161 etc.), real and teachable independent of CVLN's own (nonexistent) implementation. |
| FRK-18 | Bitcoin / OpenTimestamps Proof Operations | NONE | DISTINCT_SPECIALIZATION | NEW_EXTERNAL | OpenTimestamps is a real, external open protocol — teachable generically; CVLN's own usage `CAPABILITY_NOT_IMPLEMENTED`. |
| FRK-19 | Chain Monitoring, Resilience & Watchdog | NONE | DISTINCT_OPERATOR_ROLE | NEW_INTERNAL | `BLOCKED_PRODUCT_DEPENDENCY`. |
| FRK-20 | Offline Proof & Verification | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | `CAPABILITY_NOT_IMPLEMENTED`. |
| FRK-21 | .fk Cultural Object Format | NONE | DISTINCT_SPECIALIZATION | NEW_EXTERNAL | `BLOCKED_PRODUCT_DEPENDENCY` — the `.fk` format is not defined anywhere in this repo; needs the real FREKCORE spec before any format-accurate content is written. |
| FRK-22 | .fk Packaging & Validation | NONE | DISTINCT_SPECIALIZATION (of FRK-21) | NEW_EXTERNAL | Same blocker as FRK-21. |
| FRK-23 | Cultural Object Modeling | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | |
| FRK-24 | FREK Registry & Object Operations | NONE | DISTINCT_OPERATOR_ROLE | NEW_INTERNAL | `BLOCKED_PRODUCT_DEPENDENCY` — no registry exists (`registry.py` in this repo is the unrelated ecosystem-integrations registry, see boundary note below). |
| FRK-25 | Schemas, Taxonomies & Object Standards | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | |
| FRK-26 | Relationship & Provenance Graphs | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | |
| FRK-27 | Cultural Knowledge Graph Engineering | NONE | DISTINCT_SPECIALIZATION (of FRK-26) | NEW_EXTERNAL | |
| FRK-28 | Event Registry & Event-Driven Provenance | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | Cross-reference `backend/services/events.py` (real, but Academy-internal pub/sub, not a provenance event registry) — do not conflate. |
| FRK-29 | Cultural Fingerprint Foundations | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | |
| FRK-30 | Cultural Fingerprint Engineering | NONE | DISTINCT_SPECIALIZATION (of FRK-29) | NEW_EXTERNAL | |
| FRK-31 | Affinity, Resonance & Cadence Signals | NONE | DISTINCT_SPECIALIZATION | NEW_EXTERNAL | Boundary: this is a *different* signal vocabulary from the real `VALID_SIGNALS` set (`FREK-TIME/WORK/SCORE/...`) — never conflate the two in content. |
| FRK-32 | Context, Device & Consent Signals | NONE | DISTINCT_SPECIALIZATION | NEW_EXTERNAL | Same boundary note as FRK-31; "consent" also touches Fondation Cœurvolan doctrine (§18) — cross-reference, don't duplicate. |
| FRK-33 | Creative Lifecycle & Cultural Memory | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | Cross-reference Fondation Cœurvolan (memory/heritage domain) — FREK owns technical lifecycle tracking, Fondation owns consent/community-rights doctrine. Not a merge. |
| FRK-34 | Works, Tracks, Albums & Creative Identity | NONE | DISTINCT_SPECIALIZATION | NEW_EXTERNAL | Cross-domain boundary with LabelOS (LOS-02 Metadata & Catalog) — FREK proves/tracks identity of the work, LabelOS manages its catalog/rights record. Not a duplicate, needs an explicit boundary statement when built. |
| FRK-35 | Versions, Derivatives, Credits & Contributions | NONE | DISTINCT_SPECIALIZATION | NEW_EXTERNAL | Same LabelOS boundary as FRK-34. |
| FRK-36 | FREKRAW & Authentic Media Capture | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | `CAPABILITY_NOT_IMPLEMENTED`, `NEEDS_REPO_AUDIT` (FREKRAW is a named sub-product with zero visibility here). |
| FRK-37 | Source & Device Attestation | NONE | DISTINCT_SPECIALIZATION | NEW_EXTERNAL | |
| FRK-38 | Media Integrity & Anti-Tamper Verification | NONE | DISTINCT_SPECIALIZATION | NEW_EXTERNAL | |
| FRK-39 | FREKANSLA Operator | NONE | DISTINCT_INTERNAL_ROLE | NEW_INTERNAL | `BLOCKED_PRODUCT_DEPENDENCY`, `NEEDS_REPO_AUDIT` — FREKANSLA has zero footprint or definition anywhere accessible this session. |
| FRK-40 | DAW Provenance & Creative Session Tracking | NONE | DISTINCT_SPECIALIZATION | NEW_EXTERNAL | Cross-reference FMS-03 (DAW basics) and FMS-08 (Recording Engineering specialization, `FMS_07_18_RECONCILIATION.md`) — FMS teaches the craft, FRK teaches the provenance layer on top. Explicit boundary required, not a merge. |
| FRK-41 | Stems, Versions, Credits & Music Proof | NONE | DISTINCT_SPECIALIZATION | NEW_EXTERNAL | Same FMS-03/08 boundary as FRK-40. |
| FRK-42 | Offline Proof Transport | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | `CAPABILITY_NOT_IMPLEMENTED`. |
| FRK-43 | Store-and-Forward Cultural Infrastructure | NONE | DISTINCT_SPECIALIZATION | NEW_EXTERNAL | Conceptually close to the real outbox pattern (`frek_id_outbox` in Good Mood, `WalletTransaction` ledger in CVL-ACADEMY) — reuse those as real worked examples of "store-and-forward," even though neither is FREK-branded. |
| FRK-44 | Offline Recovery, Synchronization & Reconciliation | NONE | DISTINCT_SPECIALIZATION | NEW_EXTERNAL | |
| FRK-45 | FREK Roles, Permissions & Delegation | NONE | DISTINCT_INTERNAL_ROLE | EXTEND_EXISTING | Reuse `00_GOVERNANCE/AUTHORIZATION_MODEL.md` (already built in this Master Package) rather than reinvent a parallel roles/permissions doctrine. |
| FRK-46 | Trust Governance & Policy Enforcement | NONE | DISTINCT_INTERNAL_ROLE | EXTEND_EXISTING | Same reuse as FRK-45; also cross-reference `docs/kor/kor11/` (KOR-11 already disambiguated "gouvernance éditoriale" vs "gouvernance FREK" — reuse that boundary language verbatim, never re-derive it). |
| FRK-47 | Audit Trail & Institutional Accountability | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | |
| FRK-48 | FREK Security Foundations | NONE | DISTINCT_PROFESSION | `EXTEND_EXISTING` | CyberSecure boundary resolved (`G8`) — points at `CYB-31→42` (`CYBERSECURE_BLOCKCHAIN_GALA_HOSPITALITY_LABELOS_RECONCILIATION.md`) rather than a parallel generic security curriculum. |
| FRK-49 | Zero Trust & Infrastructure Hardening | NONE | DISTINCT_SPECIALIZATION | `EXTEND_EXISTING` | Same CyberSecure boundary as FRK-48, resolved via `G8` — points at `CYB-31→42`. |
| FRK-50 | Cryptographic Keys, Secrets & Trust Operations | NONE | DISTINCT_SPECIALIZATION | `EXTEND_EXISTING` | Same CyberSecure boundary, resolved via `G8` — points at `CYB-31→42`; also `NEEDS_EXPERT_REVIEW` (applied cryptography). |
| FRK-51 | Threat Modeling & Incident Response | NONE | DISTINCT_SPECIALIZATION | `EXTEND_EXISTING` | Same CyberSecure boundary, resolved via `G8` — points at `CYB-31→42`. |
| FRK-52 | FREK API Engineering | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | Market-general API engineering; `frek_core.py` exposes no public API today (internal Python client only) — CVLN-specific claims `CAPABILITY_NOT_IMPLEMENTED`. |
| FRK-53 | FREK SDK Engineering | NONE | DISTINCT_SPECIALIZATION | NEW_EXTERNAL | Same caveat as FRK-52. |
| FRK-54 | Event Bus, Webhooks & Integration Contracts | NONE (curriculum) / PARTIAL (repo, `services/events.py`) | DISTINCT_PROFESSION | NEW_EXTERNAL | Real, generic in-process pub/sub exists in this repo (`events.py`, powers `academy.certification.passed`) — usable as a genuine (small) worked example, but it is Academy's own event bus, not a FREK one; boundary must be explicit. |
| FRK-55 | API, Event, Error & Versioning Standards | NONE | DISTINCT_SPECIALIZATION | NEW_EXTERNAL | |
| FRK-56 | FREK × KORA Integration | NONE (formal) / SUBSTANTIAL (documented boundary) | CROSS_ECOSYSTEM_ROLE | NEW_CROSS_ECOSYSTEM | Richly grounded: every `docs/kor/korXX/` module already carries a `FREK_PROOF_MAPPING` header (`READY_FOR_FREK_PROOF = FALSE`) — reuse this documentation as the worked case, don't re-derive. |
| FRK-57 | FREK × LabelOS Integration | NONE | CROSS_ECOSYSTEM_ROLE | NEW_CROSS_ECOSYSTEM | `BLOCKED_PRODUCT_DEPENDENCY` — LabelOS itself has zero repo footprint (see `RECONCILIATION_MATRIX.md`); this bridge cannot be built with real specifics until LabelOS is. |
| FRK-58 | FREK × CVLN Academy Integration | SUBSTANTIAL (this IS `frek_core.py`) | CROSS_ECOSYSTEM_ROLE | NEW_CROSS_ECOSYSTEM | **Best-grounded of all 75 candidates** — the entire real FREK footprint in this repo *is* this integration. Build first among the bridges. |
| FRK-59 | FREK × CVLN Wallet Integration | PARTIAL | CROSS_ECOSYSTEM_ROLE | NEW_CROSS_ECOSYSTEM | Real precedent exists at Good Mood (`frek_service.py` + `wallet_service.py`, two independent outboxes, **not yet linked to each other**) — teach this exact gap (two decoupled outboxes is not yet an "integration") rather than implying a wired pipeline that doesn't exist. CVL-ACADEMY's own `backend/wallet/` does not call `frek_core` at all today. |
| FRK-60 | FREK × Intelligence OS & Agent Infrastructure | NONE | CROSS_ECOSYSTEM_ROLE | NEW_CROSS_ECOSYSTEM | Both sides are generic stubs (`registry.py`) — build as a conceptual bridge only, explicitly flagged `CAPABILITY_NOT_IMPLEMENTED` on both ends. |
| FRK-61 | Cultural Digital Archiving & Preservation | NONE | DISTINCT_PROFESSION | NEW_EXTERNAL | Cross-reference Fondation Cœurvolan (§18 doctrine) — FREK owns technical integrity of archived objects, Fondation owns consent/community-rights. Explicit boundary, not a merge. |
| FRK-62 | Heritage Records & Long-Term Integrity | NONE | DISTINCT_SPECIALIZATION | NEW_EXTERNAL | Same Fondation boundary as FRK-61. |
| FRK-63 | Geo Evidence & Territorial Provenance | NONE | DISTINCT_SPECIALIZATION | NEW_EXTERNAL | Cross-reference KOR-15 (territorial distribution strategy) — different altitude (FREK proves geo-provenance of an evidence object; KOR-15 does market/rights strategy for a territory), no merge. |
| FRK-64 | FREKCORE Production Operations | NONE | DISTINCT_INTERNAL_ROLE | NEW_INTERNAL | `BLOCKED_PRODUCT_DEPENDENCY` — nothing to operate; `frek_core.py` is a lightweight client, not a production service. |
| FRK-65 | Observability, Health & Reliability | NONE | DISTINCT_OPERATOR_ROLE | NEW_INTERNAL | `BLOCKED_PRODUCT_DEPENDENCY`. |
| FRK-66 | Backup, Restore & Disaster Recovery | NONE | DISTINCT_OPERATOR_ROLE | NEW_INTERNAL | `BLOCKED_PRODUCT_DEPENDENCY`. |
| FRK-67 | Performance, Capacity & Failure Engineering | NONE | DISTINCT_OPERATOR_ROLE | NEW_INTERNAL | `BLOCKED_PRODUCT_DEPENDENCY`. |
| FRK-68 | FREK Auditor | NONE (curriculum) / PARTIAL (repo) | DISTINCT_INTERNAL_ROLE | NEW_INTERNAL | Buildable now at a procedural level: `db.frek_signals` and the outbox tables (Good Mood) are real, inspectable audit surfaces even without cryptographic depth. |
| FRK-69 | Evidence & Provenance Audit | NONE | DISTINCT_SPECIALIZATION (of FRK-68) | NEW_INTERNAL | Sequenced after FRK-68. |
| FRK-70 | Security, Permission & Compliance Audit | NONE | DISTINCT_SPECIALIZATION | `EXTEND_EXISTING` | Same CyberSecure boundary as FRK-48→51, resolved via `G8` — points at `CYB-31→42`. |
| FRK-71 | FREK v3 Architecture | **PARTIAL — SOURCE_OBSERVED** | DISTINCT_PROFESSION | `NEW_EXTERNAL` | **CLOSED, no longer a Founder decision.** Repo truth verified: `cultureconnectorg/frekcoreAout2026`, commit `fb272f1d491b09a6d068fb3f6c9c75d407bb0626`, `frek_v3/` — a real, internally-consistent architecture corpus (`FREK_V3_Architecture_Review_Final.md`, `FREK_Architecture_Integree_v0.2.md`, `FREK_V3_Engineering_Exploded_View_v0.2.md`, `FREK_V3_Reconciliation_Architecture_v0.2.md`, `CE_QUI_MANQUE.md`). Status per the corpus's **own explicit maturity ladder**: `ARCHITECTURE_LEVEL_2` ("hardware + crypto + DSP + Core cohérent ensemble" — verrouillé) — **not** `NOT_FULL_ENGINEERING` (no RTL/bit-exact timings), **not** `NOT_HARDWARE_PROVEN` (no FPGA prototype — the doc names FPGA as the explicit bridge to Level 3, not yet crossed), **not** `NOT_PRODUCTION_INTEGRATED` (no binding to this Academy's or any product's live FREKCORE). Teach the real architecture and its own honest maturity ladder — never assert FPGA/ASIC or production FREKCORE integration is complete. |
| FRK-72 | FREK Attestation Protocol | **PARTIAL — SOURCE_OBSERVED** | DISTINCT_PROFESSION | `NEW_EXTERNAL` | Real, verified: `frek_v3/docs/FREK_Attestation_Protocol_v0.1.md` — a specified 283-byte binary attestation protocol (L0/L1/L2 levels), **and** a working Python reference implementation (`reference_verifier/`, 16 passing tests, golden test vectors). `ARCHITECTURE_LEVEL_2` per FRK-71's ladder — real and testable, not yet hardware-proven. |
| FRK-73 | FREK Cryptographic Architecture | **PARTIAL — SOURCE_OBSERVED** | DISTINCT_PROFESSION | `NEW_EXTERNAL` | Real, verified: `frek_v3/docs/FREK_Cryptographic_Architecture_Review_v0.1.md` + `reference_verifier/frek_crypto.py` (real P-256/ECDSA primitives, `PUF → HKDF → DRK → AK/FK/CK` key-derivation chain, raw `r\|\|s` signatures, canonical-message encoding). Still `NEEDS_EXPERT_REVIEW` (applied cryptography, never taught as production-audited without a named cryptographer's review) — that caution stands independent of `ARCHITECTURE_LEVEL_2` status. |
| FRK-74 | FREK DSP Fingerprint | **PARTIAL — SOURCE_OBSERVED, explicitly unfinished** | DISTINCT_SPECIALIZATION | `NEW_EXTERNAL` | Real, verified: `frek_v3/docs/FREK_DSP_Fingerprint_Specification_v0.1.md`. Per the corpus's own `CE_QUI_MANQUE.md`: this spec is explicitly the **least resolved** part (band count, FFT window, hop size, and the fingerprint algorithm itself are named as still-open product decisions, not yet locked). Teach it as an architecture-in-progress, never as a finished spec. "DSP" = digital signal processing (audio fingerprinting) here, a different technical domain from FRK-29/30's broader "cultural fingerprint" — kept distinct, cross-referenced. |
| FRK-75 | FREK Reference Verifier Engineering | **SUBSTANTIAL — SOURCE_OBSERVED, real working code** | DISTINCT_PROFESSION | `NEW_EXTERNAL` | Best-grounded of the FRK-71→75 cluster: `reference_verifier/` is a real, structured Python package (`frek_constants.py`, `frek_types.py`, `frek_crypto.py`, `frek_parser.py`, `frek_registry.py`, `frek_verifier.py`, `frek_device_sim.py`) with 16 passing unit tests against golden vectors — genuinely teachable as a worked engineering example. Its own docs flag the **single-implementation limitation** honestly: a Rust cross-implementation is explicitly named as the next required step to prove the spec (not just the Python) is correct — teach that limitation, never imply the protocol is proven implementation-agnostic yet. The verifier counterpart to FRK-13 (Proof Engine) — sequence after it. |

## Summary

| Verdict | Count |
|---|---|
| `NEW_EXTERNAL` (market-general or CVLN-applied, buildable as pure curriculum) | 56 (51 + FRK-71→75, all now `SOURCE_OBSERVED`) |
| `NEW_INTERNAL` | 12 |
| `NEW_CROSS_ECOSYSTEM` | 5 (FRK-56→60) |
| `SPECIALIZE_EXISTING` | 1 (FRK-11) |
| `EXTEND_EXISTING` (reuse Master Package governance / merge into a sibling) | 3 (FRK-05, FRK-45, FRK-46) |
| `EXTEND_EXISTING` (CyberSecure boundary, resolved via `G8`) | 5 (FRK-48, 49, 50, 51, 70) |
| `NEEDS_FOUNDER_DECISION` | **0** — FRK-71 closed (repo verified, `ARCHITECTURE_LEVEL_2`/`SOURCE_OBSERVED`, maturity preserved exactly, never inflated to production-proven). |
| `REJECT_TRUE_DUPLICATE` | 0 |

**Zero rejections** — every candidate carries real professional or
architectural weight, consistent with the corrected method. What
changes from a naive "build all 75 as full formations": FRK-05 and
FRK-45/46 fold into siblings rather than standing alone, FRK-11
becomes a specialization not a parallel formation, and **6 candidates
around FREK security explicitly need a Founder call** on whether they
live inside CyberSecure (recommended) or stand alone — flagged, not
decided unilaterally, per the instruction to escalate only genuine
Founder decisions.

## Build priority (given `CAPABILITY_NOT_IMPLEMENTED` dominates this domain)

1. **FRK-01, FRK-58** — best-grounded, highest-value: foundations +
   the one integration that already exists in code and is already
   documented across `docs/kor/`.
2. **FRK-03, FRK-06, FRK-13 (internal half), FRK-68** — internal
   operator paths buildable on real `frek_core.py` usage today.
3. **FRK-56, FRK-59** — cross-ecosystem bridges with partial real
   grounding (KOR docs, Good Mood's two outboxes).
4. Market-general clusters (FRK-07/08/09/10, FRK-12/14/15,
   FRK-17/18, FRK-52/53/54/55) — real, teachable industry-standard
   knowledge independent of any CVLN implementation gap.
5. **FRK-71→75** — the FREK v3 architecture cluster, `SOURCE_OBSERVED`
   on `frekcoreAout2026`, buildable now at `ARCHITECTURE_LEVEL_2`
   (FRK-75's `reference_verifier/` is real working code with passing
   tests — the best-grounded of the five).
6. Everything still `BLOCKED_PRODUCT_DEPENDENCY` (`.fk` format,
   FREKANSLA, notary, watchdog, production ops) — held until a real
   FREKCORE production repo or Founder specification is named. Not
   built on invention.

## Status

`STATUS = RECONCILED_NOT_BUILT`, `SOURCE_STATUS = CANDIDATE` (unchanged
— per the Founder's own rule, this map is never frozen canonical by a
reconciliation pass alone). No code, seed, or runtime touched. Next
action: W4 (competency map) on the `NEW_EXTERNAL`/`NEW_INTERNAL`/
`NEW_CROSS_ECOSYSTEM` items not `BLOCKED_PRODUCT_DEPENDENCY`, starting
with the priority order above.

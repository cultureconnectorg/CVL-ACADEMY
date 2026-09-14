# FRK-01→75 — Canonical Education Map (full domain)

## Shared competency skeleton

Every formation in this slice follows the same shape:
`PROFESSIONAL_ROLE → ACTIVITIES → COMPETENCIES`, each competency
grounded in a named method/route/table of `backend/services/
frek_core.py`, or in a real cross-repo artifact (`FREK_PROOF_MAPPING`
headers in `docs/kor/`, Good Mood's two outbox clients).

## Dependency graph

```
FRK-01 (Foundations, umbrella — entry point, same role as KOR-01/KLT-01)
  ├── FRK-58 (FREK × CVLN Academy Integration — this IS frek_core.py)
  ├── FRK-03 (FREK Operator — real cross-module usage patterns)
  │     └── FRK-06 (FREK-ID Operations — mint_frek_id() specialization)
  ├── FRK-13 (FREK Proof Engine, internal half — issue_proof() stub)
  ├── FRK-68 (FREK Auditor — db.frek_signals + outbox tables)
  ├── FRK-56 (FREK × KORA Integration — FREK_PROOF_MAPPING headers)
  └── FRK-59 (FREK × CVLN Wallet Integration — Good Mood's two outboxes)
```

## Boundary notes (mandatory cross-reference discipline)

- **`frek_core.py` (this Academy) vs `frek_v3/` (FRK-71→75,
  `cultureconnectorg/frekcoreAout2026`):** two real, distinct layers of
  the same eventual product. `frek_core.py` is a thin, local-fallback
  client (`ARCHITECTURE_LEVEL` unspecified, production-shaped);
  `frek_v3/` is a real, more mature architecture corpus with a working
  Python reference verifier, self-declared `ARCHITECTURE_LEVEL_2`.
  Never merged — FRK-71→75 is a separate, future wave.
- **Good Mood's `frek_service.py`/`wallet_service.py` vs this
  Academy's `frek_core.py`/`backend/wallet/`:** same *pattern*
  (env-gated outbox client, `NOT_CONNECTED` local fallback), never the
  same *channel*. `frek_service.py` posts to Good Mood's own
  `FREK_ID_URL`; `frek_core.py` posts to this Academy's own
  `FREK_CORE_BASE_URL`. No integration is observed between any of
  these systems.
- **FRK-13 "FREK Proof Engine" as a market concept vs. today's
  `issue_proof()` stub:** taught as two altitudes explicitly — the
  professional concept of a proof engine (chain-of-custody, timestamp
  anchoring, cryptographic signature) is real, teachable,
  market-general knowledge; today's actual implementation in this repo
  is a random UUID with none of that. Never conflated.
- **FRK-56's `FREK_PROOF_MAPPING` headers vs `READY_FOR_FREK_PROOF`:**
  the header existing on a KOR module means the module *references*
  the FREK signal stack conceptually — it does not mean a real,
  externally-verifiable proof exists. `READY_FOR_FREK_PROOF = FALSE`
  on every KOR module, without exception, is itself the teaching
  point, not a gap to explain away.
- **FRK-68's audit surfaces:** `db.frek_signals` (this Academy) and
  Good Mood's `db.frek_outbox`/`db.wallet_outbox` are three *separate*
  real tables in three separate systems — an auditor candidate must
  never imply they form one unified audit trail.

## Anti-footprint verification (mandatory before certifying any of these 8)

Before crediting a candidate with any competency in this slice, verify
the claim against the actual method/table cited in the corresponding
`REFERENTIAL.md` — never against a memorized summary of "what a FREK
system probably does." `issue_proof()`'s random-UUID reality is the
canonical example of why this matters.

## Certification / mission eligibility doctrine

Same N1/N2/assessment structure as `CERTIFICATION_MODEL.md`. No
mission eligibility exists yet for FRK-13's proof-engine internal
half — issuing a "proof" today produces no verifiable artifact, so no
mission can depend on it being one.

## Full-domain map (75/75)

**Specialization/sequencing chains** (base → specialization, reused by
reference, never re-authored): FRK-04→FRK-11 (Digital Provenance
Specialist), FRK-08→FRK-09 (Identity Lifecycle), FRK-12+FRK-14→FRK-15
(Technical Evidence Reports), FRK-26→FRK-27 (Cultural Knowledge
Graph), FRK-29→FRK-30 (Cultural Fingerprint Engineering),
FRK-34→FRK-35 (Versions/Derivatives), FRK-36→FRK-37→FRK-38 (media
capture → attestation → integrity), FRK-40→FRK-41 (DAW provenance →
music proof), FRK-43→FRK-44 (store-and-forward → recovery), FRK-52→
FRK-53→FRK-55 (API → SDK → cross-cutting standards), FRK-61→FRK-62
(archiving → heritage records), FRK-68→FRK-69 (auditor → evidence
audit), FRK-71→FRK-72/73/74/75 (v3 architecture → attestation/crypto/
DSP/verifier).

**`EXTEND_EXISTING` — folds into a sibling or existing doc, no
separate formation built:**
- FRK-05 (FREK Ecosystem Integration) → becomes the shared
  introduction to the FRK-56→60 bridge formations, not a 6th parallel
  one.
- FRK-45 (Roles/Permissions/Delegation), FRK-46 (Trust Governance) →
  reuse `00_GOVERNANCE/AUTHORIZATION_MODEL.md` (FRK-46 also reuses
  `docs/kor/kor11/`'s own governance-boundary language verbatim,
  never re-derived).
- FRK-48/49/50/51/70 (FREK Security Foundations, Zero Trust, Crypto
  Keys, Threat Modeling, Security/Compliance Audit) → all point to
  `CYB-31→42` (`CYBERSECURE_BLOCKCHAIN_GALA_HOSPITALITY_LABELOS_
  RECONCILIATION.md`, real anchor `backend/auth.py`) rather than a
  parallel generic security curriculum — itself not yet built as a
  `docs/cyb/` corpus, so these 5 remain pointers to a future domain,
  not present content.

**`BLOCKED_PRODUCT_DEPENDENCY` (`GAP.md`, no repo/spec exists):**
FRK-16 (Digital Notary), FRK-19 (Chain Watchdog), FRK-21/22 (`.fk`
format + packaging), FRK-24 (Registry & Object Operations, distinct
from `services/integrations/registry.py`), FRK-39 (FREKANSLA
Operator), FRK-57 (FREK×LabelOS, LabelOS itself unfound), FRK-64/65/
66/67 (Production Ops/Observability/Backup/Performance — no
production FREKCORE service to operate).

**Market-general clusters, standalone (no CVLN-specific implementation
required to teach, `CAPABILITY_NOT_IMPLEMENTED` stated where a CVLN
claim would otherwise be implied):** FRK-02, 07, 17, 18, 20, 23, 25,
28, 31, 32, 33, 42, 47, 54, 60, 63 and the sequencing chains above.

**`NEEDS_EXPERT_REVIEW`, never resolved by this drafting pass:**
FRK-10 (EUDI/eIDAS2 — EU jurisdiction-specific), FRK-14 (chain of
custody — forensic/legal-adjacent), FRK-73 (applied cryptography).

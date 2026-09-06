# FRK-01/58/03/06/13/56/59/68 — Canonical Education Map

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

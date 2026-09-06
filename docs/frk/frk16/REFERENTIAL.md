# FRK-16 — FREK Digital Notary

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: initially `BLOCKED_PRODUCT_
DEPENDENCY` — no notarization/timestamping mechanism was found in
`frekcoreAout2026`, `gmfest972/goodmooddjsayd`, or `fms-os/fms`.
**Reclassified this pass** after directly auditing
`cultureconnectorg/Cvln-ios-v.1` (its own cross-repo governance/audit
corpus, `cvln-intelligence-os/`), which documents a real, `IMPLEMENTED`
notarization system in **MetaCVLN** (`backend/server.py`):

- `COMPONENT-MATRIX.md` row: "Notary & Public Audit | META |
  `backend/server.py` | Verifiable audit trail | Notarisations with
  verify and export, public read surface | `/notarizations`,
  `/public/notarizations` | `IMPLEMENTED` | Ed25519 keys | external
  verifiers | none | Notary private key stored unencrypted at rest."
- `proof/EXTERNAL-ANCHORING.md`: real OpenTimestamps external
  anchoring of a `chain_hash` (SHA-256 digest), provider model
  (`ots` `IMPLEMENTED`, `rfc3161` `TARGET`), real states (`pending`/
  `confirmed`/`offline`/`unavailable`), real endpoints
  (`GET /api/docs/anchor/providers`, `GET /api/docs/anchors`,
  `POST /api/docs/anchor/{baseline}`,
  `POST /api/docs/anchor/{digest}/upgrade`,
  `GET /api/docs/anchor/{digest}/verify`), real stored artefacts
  (`audit/anchors/index.json` + per-digest `.ots` files, 3 observed).
  Decision `D-020`; config `OTS_CALENDARS`, `OTS_TIMEOUT_SECONDS`.
- `proof/NOTARIAL-BOUNDARY.md`: **mandatory disclosure carried
  verbatim** — "The word 'notary' in the audited MetaCVLN code names a
  signing key role. It does not denote a legal notary." (Decision
  `D-007`.) Legal attestation is permanently out of scope; only digital
  evidence (integrity + attribution, cryptographic recomputation) is in
  scope.

## Objectives

- Teach real audit-trail/notarization system design — signing-key-based
  document notarization with a public, verifiable read surface, plus
  external anchoring of a corpus digest via OpenTimestamps — using
  MetaCVLN's real, `IMPLEMENTED` system as the worked example.
- Mandatory, permanent boundary (carried from the source corpus
  itself): "notary" here is a signing-key role, never a legal notary;
  `legal_effect` stays `"none"`; OpenTimestamps proves temporal
  existence and integrity, never qualified/eIDAS legal timestamping.
- Mandatory, permanent boundary vs. this Academy's own FREK layer:
  MetaCVLN's Notary & Public Audit system is not FREK-branded and is
  never implied to be `frek_core.py`/`issue_proof()` (FRK-13) — the
  two are unrelated systems in different repos; FRK-13's stub remains
  a UUID with no cryptographic signing or anchoring of any kind.
- Teach the honestly-disclosed limitation as part of the discipline:
  "Notary private key stored unencrypted at rest" is a documented
  finding in the source corpus's own `COMPONENT-MATRIX.md`, not a
  weakness to hide.

## Modules

1. Signing-key-based notarization design (Ed25519, verify/export,
   public read surface) — grounded in MetaCVLN's real system.
2. External anchoring via OpenTimestamps — digest-only anchoring,
   provider-neutral model, state machine (`pending`/`confirmed`/
   `offline`/`unavailable`), what it proves and what it explicitly does
   not (grounded in `proof/EXTERNAL-ANCHORING.md`).
3. Notarial-boundary discipline — "notary" as a signing-key role vs. a
   legal notary; boundary vs. `issue_proof()` (FRK-13) and `frek_core.py`.

## Assessment

A design/reading exercise: candidate reads a real notarization system
description and must correctly state what it proves (integrity,
attribution, temporal existence via anchoring) vs. what it never
proves (legal effect, qualified timestamp status) — eliminatory
failure for claiming legal attestation or for presenting this system as
FREK-branded/`frek_core.py`-integrated.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package, built this pass
after reclassification from `BLOCKED_PRODUCT_DEPENDENCY` on real,
independently-audited repo-truth (`Cvln-ios-v.1`'s own governance
corpus). Never implies `FULLY_COMPLETE`.

# FRK-20 — Offline Proof & Verification

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`. `CAPABILITY_NOT_
IMPLEMENTED` for any CVLN-specific claim — taught as market-general
practice (offline-first verification design patterns).

## Objectives

A candidate who completes FRK-20 can design a real offline-first
verification flow, using `frek_core.py`'s real network-toggle nature
as a precisely-stated counter-example, never as an implementation of
the subject:

- Explain what "offline-first" verification is and why it differs from
  simple local caching of a server result: offline-first verification
  relies on local cryptographic guarantees (a signature check, a
  hash-chain walk) — never on a temporary copy of a result already
  validated elsewhere, which offers no guarantee once stale.
- Explain the store-and-forward pattern precisely: a proof artifact can
  be verified locally the moment it's received, and its record
  synchronized to a remote system later, without any loss of
  verification guarantee — the local check is complete and
  self-sufficient, sync is a separate, non-blocking concern.
- Explain why local cryptographic verification (signature check,
  hash-chain) must remain possible with zero network access for a
  system to be genuinely offline-first: without it, the system
  silently depends on the network whenever the check actually matters
  — contradicting the "offline-first" claim outright.
- Confirm `frek_core.py`'s real nature precisely: `is_remote_enabled()`
  is a plain boolean network-availability toggle
  (`bool(FREK_CORE_BASE_URL)`, false by default) — not a cryptographic
  verification mechanism of any kind. It decides whether a remote call
  is attempted; it proves nothing about an artifact's validity, locally
  or otherwise.
- Design a concrete offline-first flow: verify a signed artifact
  locally with zero network calls, then queue its record for deferred
  sync — with the cryptographic guarantee established entirely at the
  local-verification step, never deferred to the sync step.

## Modules

1. **Offline-first verification design patterns** — the store-and-
   forward pattern, and why local cryptographic checks (not caching)
   are the real foundation of "offline-first."
2. **Local cryptographic-check practice** — signature verification and
   hash-chain walking as concrete, network-free checks.
3. **CVLN-gap discipline** — `is_remote_enabled()`'s real nature (a
   plain network-availability boolean, never a cryptographic check)
   stated precisely, cited as a counter-example, never as an
   implementation of offline verification.

## Assessment

A design exercise: candidate designs a store-and-forward verification
flow for a signed artifact (local verification, deferred sync) with
the cryptographic guarantee established entirely offline, then explains
why `is_remote_enabled()` does not constitute offline verification in
this formation's sense — graded against real offline-verification
patterns, with an eliminatory check on making the proof guarantee
depend on a synchronous network call.

## Evidence / certification / mission eligibility

`FRK20.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.

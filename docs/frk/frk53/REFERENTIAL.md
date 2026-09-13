# FRK-53 — FREK SDK Engineering

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION`, action `NEW_EXTERNAL`. Same caveat as
FRK-52 — `frek_core.py` exposes no public API today (internal Python
client only, called in-process, no HTTP surface), so no SDK can exist
for it either. Never a description of a CVLN capability.

## Prerequisites

FRK-52 (recommended).

## Objectives

A candidate who completes FRK-53 can design a real SDK (client
library), building on but never re-authoring FRK-52's API-design
fundamentals:

- Explain what a SDK is and how its engineering differs from the API
  it wraps (FRK-52): an SDK provides an idiomatic, language-native
  interface over an API's raw HTTP/RPC surface — method calls instead
  of manually constructed requests, typed return values instead of
  raw JSON, and language-appropriate error handling instead of status
  codes.
- Design typed request/response models so consumers get compile-time
  or editor-time feedback instead of discovering a malformed request
  only at runtime.
- Design actionable error handling: an SDK should translate a raw API
  error (a status code + a JSON error body) into a typed exception or
  result with enough context (what failed, why, and often what to do
  about it) that a developer doesn't have to go read the raw API docs
  to debug it — the difference between "400 Bad Request" and
  "InvalidFieldError: `email` must be a valid address" is exactly
  the DX FRK-53 teaches.
- Design retry and idempotency handling at the SDK layer: which
  failures are safe to retry automatically (network timeouts,
  5xx), which are never safe to retry blindly (a non-idempotent write
  that may have already succeeded), and how the SDK should expose
  that distinction to the caller rather than hiding it.
- Explain why good SDK developer experience (DX) drives adoption: a
  SDK with unclear types and unhelpful errors pushes integrators to
  abandon the integration or fall back to raw HTTP calls, defeating
  the SDK's purpose.
- Same mandatory gap discipline as FRK-52: no public FREK API/SDK
  surface exists today — this is taught as market-general SDK-
  engineering practice, applied to a hypothetical or generic API,
  never claimed as something built for `frek_core.py`.
- Reuse FRK-52's API-design fundamentals by reference — never
  re-author them here; cite `docs/frk/frk52/REFERENTIAL.md` instead.

## Modules

1. **SDK/client-library design fundamentals** — the SDK-vs-API
   distinction, typed request/response models, and the idiomatic
   interface pattern.
2. **Developer-experience patterns** — actionable error translation
   (typed exceptions with context, not raw status codes), and
   retry/idempotency handling exposed clearly to the caller.
3. **CVLN-gap discipline (inherited from FRK-52)** — no FREK SDK or
   public API surface exists today; the discipline and its rationale
   are inherited by reference, never re-derived.

## Assessment

An SDK-design exercise: candidate designs a client library (typed
models, actionable error handling, retry/idempotency policy) for a
generic API, citing FRK-52 by reference for the underlying API-design
fundamentals — graded against real SDK-engineering practice, with an
eliminatory check on claiming a public FREK SDK exists.

## Evidence / certification / mission eligibility

`FRK53.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.

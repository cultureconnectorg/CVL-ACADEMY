# FRK-52 — FREK API Engineering

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`. Market-general API
engineering; `frek_core.py` exposes **no public API today** (internal
Python client only, called in-process — no HTTP routes of its own) —
CVLN-specific claims `CAPABILITY_NOT_IMPLEMENTED`.

## Objectives

A candidate who completes FRK-52 can design a real REST API, using
`frek_core.py`'s real internal-only nature as a precisely-stated
counter-example, never as a description of a public API:

- Confirm `frek_core.py`'s real nature precisely: it is a
  `FrekCoreClient`, an internal Python client called in-process by
  this Academy's own backend — it has no HTTP routes of its own and
  exposes nothing publicly. This fact is the foundation of the
  formation's entire CVLN-gap discipline.
- Design real API versioning: explain why a version scheme (e.g. a
  `/v1/` path segment or a version header) is indispensable from a
  real API's very first production release — without it, any future
  interface change silently breaks every existing integrator, because
  there is no way to signal "this is a different contract" to
  consumers still on the old shape.
- Design real API error handling: semantic HTTP status codes (4xx for
  client error, 5xx for server error, with specific codes chosen
  meaningfully — 404 vs. 409 vs. 422 are not interchangeable) plus a
  consistent error-body structure (code, message, detail) — and
  explain why their absence breaks developer experience: without them
  an integrator must guess the cause of a failure instead of handling
  it programmatically.
- Explain precisely why claiming `frek_core.py` "exposes a REST API"
  would be an eliminatory error in any copy: it would assert a
  technical capability that does not exist — the CVLN-gap discipline
  explicitly forbids this kind of invention, regardless of how
  plausible it might sound.

## Modules

1. **API design fundamentals** — REST resource modeling, request/
   response design, as real industry-general practice.
2. **Versioning/error-handling standards (market-general)** — a real
   version scheme and a real, consistent error-handling structure
   (semantic status codes + structured error body).
3. **CVLN-gap discipline** — `frek_core.py`'s real internal-only
   nature (a `FrekCoreClient` called in-process, no HTTP routes of its
   own) stated precisely as the formation's grounding fact, cited as a
   counter-example, never as an implementation of the subject taught.

## Assessment

An API-design exercise: candidate designs a REST API with a real
versioning scheme and consistent error handling, as a market-general
exercise with no reference to any specific CVLN system, then writes a
note confirming `frek_core.py` has no public HTTP surface today —
graded against real industry API-design practice, with an eliminatory
check on claiming `frek_core.py` exposes a public API.

## Evidence / mission eligibility

No mission eligibility path exists yet. `FRK52.SKILL.API_ENGINEERING.L1`
reserved once deepened (see `EVIDENCE_MODEL.md`).

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package (référentiel +
N1/N2 + assessment/rubric + evidence model + 3 guides + integration
note), deepened this pass. Never implies `FULLY_COMPLETE`.

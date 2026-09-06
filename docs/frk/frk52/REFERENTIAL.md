# FRK-52 — FREK API Engineering

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`. Market-general API
engineering; `frek_core.py` exposes **no public API today** (internal
Python client only, called in-process — no HTTP routes of its own) —
CVLN-specific claims `CAPABILITY_NOT_IMPLEMENTED`.

## Objectives

- Teach real API-engineering practice (REST/versioning/error-handling
  design) as an industry-general discipline.
- Never claim `frek_core.py` exposes a public API today — it is an
  internal Python client, called in-process by this Academy's own
  backend, with no HTTP surface of its own.

## Modules

1. API design fundamentals.
2. Versioning/error-handling standards (market-general).
3. CVLN-gap discipline — `frek_core.py`'s real internal-only nature.

## Assessment

An API-design exercise graded against real industry API-design
practice, with an eliminatory check on claiming `frek_core.py` exposes
a public API.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.

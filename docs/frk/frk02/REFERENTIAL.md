# FRK-02 — FREKCORE Architecture & Ecosystem

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_PROFESSION`, action `NEW_EXTERNAL`. Explicit repo-truth
constraint: content must stay bounded to what `frek_core.py` actually
does (mint/signal/proof-stub/stade) — **never** invent a DID/VC/
provenance-graph architecture as if it were built, even though those
concepts appear in the wider Master 2D candidate map.

## Objectives

- Explain FREKCORE's real architecture *as this Academy's client sees
  it*: a thin, remote-first/local-fallback service boundary, not a
  full distributed identity network.
- Distinguish the client-side view (FRK-01/58's territory) from the
  ecosystem-level architecture question this formation actually
  addresses: how FREKCORE is positioned conceptually among CVLN's
  other systems (Wallet, KORA, Agent Factory) — without asserting any
  wiring between them that isn't observed.
- Never claim DID/VC, provenance graphs, or `.fk` object format are
  implemented anywhere in this repo — they are real candidate concepts
  in the Master 2D map, not shipped architecture.

## Modules

1. Client-boundary architecture (grounded in `frek_core.py`'s own
   docstring: "the sole boundary through which the app talks to
   FrekCore").
2. Ecosystem positioning — how FREKCORE-as-client relates conceptually
   to Wallet/KORA/Agent Factory, citing only observed (non-)wiring.
3. Scope discipline — explicit list of what is NOT implemented
   anywhere in this repo (DID/VC, provenance graphs, `.fk` format).

## Assessment

A positioning brief: candidate explains FREKCORE's real architecture
to a new hire without overstating scope — eliminatory failure for
asserting any unimplemented capability as real.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.

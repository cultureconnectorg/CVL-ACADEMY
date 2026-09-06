# FRK-74 — FREK DSP Fingerprint

## Repo truth this formation is built on

Grounded in `frek_v3/docs/FREK_DSP_Fingerprint_Specification_v0.1.md`
— already audited this session, `REPO_REGISTRY.md`. Per the corpus's
own `CE_QUI_MANQUE.md`: this spec is explicitly the **least resolved**
part of the v3 cluster — band count, FFT window size, hop size, and
the fingerprint algorithm itself are named as **still-open product
decisions**, not yet locked.

Per `FREK_01_75_RECONCILIATION.md`: coverage `PARTIAL — SOURCE_
OBSERVED, explicitly unfinished`, distinctness `DISTINCT_
SPECIALIZATION`, action `NEW_EXTERNAL`.

## Prerequisites

FRK-71.

## Objectives

- Teach the real DSP fingerprint specification **as an
  architecture-in-progress**, never as a finished spec — the open
  decisions (FFT window, hop size, band count, algorithm) are the
  central teaching point, not a gap to smooth over.
- Explicit boundary vs. FRK-29/30's broader "cultural fingerprint"
  concept: "DSP" here means digital signal processing (audio
  fingerprinting specifically) — a different, narrower technical
  domain, kept distinct and cross-referenced.

## Modules

1. DSP fingerprint specification literacy (what is locked so far).
2. Open-decision literacy (FFT window/hop size/band count/algorithm —
   explicitly unresolved).
3. Boundary discipline vs. FRK-29/30.

## Assessment

A specification-status exercise: candidate must correctly identify
which parts of the spec are locked vs. still open — eliminatory
failure for presenting the spec as finished.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.

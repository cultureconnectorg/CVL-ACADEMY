# FRK-75 — FREK Reference Verifier Engineering

## Repo truth this formation is built on

Grounded in `frek_v3/reference_verifier/` — a real, structured Python
package (`frek_constants.py`, `frek_types.py`, `frek_crypto.py`,
`frek_parser.py`, `frek_registry.py`, `frek_verifier.py`,
`frek_device_sim.py`) with **16 passing unit tests against golden
vectors** — already audited this session, `REPO_REGISTRY.md`. **Best-
grounded of the FRK-71→75 cluster.**

Per `FREK_01_75_RECONCILIATION.md`: coverage `SUBSTANTIAL — SOURCE_
OBSERVED, real working code`, distinctness `DISTINCT_PROFESSION`,
action `NEW_EXTERNAL`. The verifier counterpart to FRK-13 (Proof
Engine) — sequenced after it.

## Prerequisites

FRK-71, FRK-13 (recommended).

## Objectives

- Teach real reference-verifier engineering practice using this
  genuinely working, tested Python package as the worked example.
- Carry the corpus's own honestly-disclosed **single-implementation
  limitation**: a Rust cross-implementation is explicitly named as the
  next required step to prove the *spec* (not just this Python code)
  is correct — teach this limitation explicitly, **never imply the
  protocol is proven implementation-agnostic yet**.
- Explicit boundary vs. FRK-13: FRK-13 teaches this Academy's own
  `issue_proof()` stub reality; FRK-75 teaches this separate, more
  mature, real verifier engineering in the `frek_v3/` cluster — never
  conflated.

## Modules

1. Reference-verifier package structure literacy (7 real modules).
2. Golden-vector test-suite literacy (16 passing tests).
3. Single-implementation-limitation discipline — the Rust
   cross-implementation gap, explicitly taught, never smoothed over.

## Assessment

A verifier-engineering exercise: candidate reads real test output and
correctly states what is proven (this Python implementation passes its
own golden vectors) vs. not yet proven (implementation-agnostic
correctness, pending a Rust cross-implementation) — eliminatory
failure for claiming the protocol itself is proven.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package, deepened this
pass. Never implies `FULLY_COMPLETE`.

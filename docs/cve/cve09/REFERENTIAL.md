# CVE-09 — UVC Allocation & Distribution

```
Prerequisite: CVE-04, CVE-05, CVE-07 (consumes their outputs).
```

## Repo truth

§5 (Layer 4 — Allocation):
`UVC_i,c = ( CVI_i,c / Σ_j CVI_j,c ) · MD_c` — a work's Unit of
Value/Contribution share, proportional to its CVI share of the
cycle's total CVI, scaled by the distributable mass `MD_c`. Unit value:
`value_UVC,c = MD_c / Σ_i CVI_i,c`.

## Prerequisites

CVE-04 (CVI), CVE-05 (ρ inside CVI), CVE-07 (N, one of CVI's inputs).

## Objectives

1. Correctly derive `UVC_i,c` from `CVI_i,c` and `MD_c`, and explain
   why it is a **proportional share** mechanism, not an absolute
   valuation.
2. Explain `value_UVC,c` and how it relates to `UVC_i,c` (dividing the
   fixed mass `MD_c` by total CVI, then multiplying by a work's own
   CVI recovers the same `UVC_i,c`).
3. State the fixed-budget constraint this implies (§6, C1:
   `Σ_i UVC_i,c = MD_c`) and why it matters for interpreting any single
   work's allocation (it is always relative to the whole cycle's
   catalog, never an absolute score).

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | UVC formula literacy | §5 | Worked numeric example with illustrative CVI values |
| M2 | Unit-value literacy | `value_UVC,c` formula | Written derivation connecting the two formulas |
| M3 | Fixed-budget constraint | §6, C1 | Written note: why UVC is always relative, never absolute |

## Assessment

Per `../CERTIFICATION_MODEL.md`.

## Evidence / certification / mission eligibility

Same general pattern as CVE-01. Cross-reference CVE-10/CVE-11 — same
underlying formula, different framing; never re-derived independently
in those two formations.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_CVE09` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Grounded in a direct re-read
this session of §5 and §6 C1 (locally available, `kora2024/kora-app/
memory/`). Not yet delivered to a real candidate — `FULLY_COMPLETE`
still requires that verification, per `../QUALITY_GATES.md`.

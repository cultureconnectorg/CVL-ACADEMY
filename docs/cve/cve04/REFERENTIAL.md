# CVE-04 — CES & Cultural Engagement Signals

```
Prerequisite: CVE-01, CVE-02.
```

## Repo truth

§3.1 (CES Aggregation): `CVI_i,c = ( Σ_a w_a,c · x̂_i,c,a^ρ_c )^(1/ρ_c)`,
where `a ∈ {S, E, F, C, CHL_integrated, N}`, `Σ_a w_a,c = 1`,
`w_a,c ≥ 0`. This is the Constant Elasticity of Substitution (CES)
aggregation combining Layer 1's normalized components into a single
Cultural Value Index.

## Prerequisites

CVE-01, CVE-02 (the `S,E,F,C` raw/normalized components this formula
consumes).

## Objectives

1. Correctly write and explain the CES formula, including which 6
   components it aggregates (`S, E, F, C, CHL_integrated, N`) — note
   that `CHL_integrated` and `N` are themselves derived elsewhere
   (§3.3, §3.2) and must be cross-referenced, not re-derived here.
2. State the weight-normalization constraint (`Σ_a w_a,c = 1`,
   `w_a,c ≥ 0`) and why it matters (the aggregation stays a genuine
   weighted combination, not an arbitrary sum).
3. Explain the role of `ρ_c` in this formula at a literacy level
   (cross-reference CVE-05 for the parameter's own deep dive — never
   duplicate that content here).

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | CES formula literacy | §3.1 | Annotated formula, each symbol traced to its source layer |
| M2 | Weight-constraint discipline | `Σ_a w_a,c = 1`, `w_a,c ≥ 0` | Written note on why this constraint matters for interpretability |
| M3 | Cross-reference discipline | §3.1's dependency on §3.2 (N), §3.3 (CHL) | Dependency map — never re-derive N or CHL_integrated inside this formation |

## Assessment

Per `../CERTIFICATION_MODEL.md`.

## Evidence / certification / mission eligibility

Same general pattern as CVE-01.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_CVE04` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Grounded in a direct re-read
this session of §3.1 (locally available, `kora2024/kora-app/memory/`).
Not yet delivered to a real candidate — `FULLY_COMPLETE` still
requires that verification, per `../QUALITY_GATES.md`.

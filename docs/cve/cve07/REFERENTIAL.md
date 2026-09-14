# CVE-07 — Nebula Cultural Value Modeling

```
Prerequisite: CVE-01, CVE-02.
```

## Repo truth

§3.2 (Nebula Score — Cultural Circulation). For each axis
`k ∈ {language, territory, diaspora, generation, style,
collaboration}`: `H_k(i,c) = − Σ_j p_{i,j,k} · log(p_{i,j,k})`
(Shannon entropy over listening proportions), then
`N_i,c = Σ_k H_k(i,c) · ν_k(i,c) · φ(i,c)`, where `ν_k(i,c) ∈ [0.3,1]`
is a novelty coefficient (1 = first-time penetration of a category,
0.3 = already reached) and `φ(i,c) = 1 + (Δ_axis_coverage/Δt)`
normalized to `[1, φ_max]` is a velocity factor.

## Prerequisites

CVE-01, CVE-02.

## Objectives

1. Correctly compute and explain the entropy term `H_k` for a given
   axis, and what high vs. low entropy means for cultural circulation
   on that axis.
2. Name all 6 real axes and explain `ν_k`'s two named calibration
   points (1 = first-time, 0.3 = already reached) precisely — never
   invent additional axes or intermediate values not given.
3. Explain the velocity factor `φ(i,c)` and its normalization bound
   `[1, φ_max]`.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | Entropy formula literacy | `H_k(i,c)` formula | Worked numeric example with illustrative proportions summing to 1 |
| M2 | 6-axis + novelty coefficient literacy | The 6 named axes, `ν_k` bounds | Table: axis → meaning → novelty interpretation |
| M3 | Velocity factor literacy | `φ(i,c)` formula and bound | Written explanation of what "coverage velocity" measures |

## Assessment

Per `../CERTIFICATION_MODEL.md`.

## Evidence / certification / mission eligibility

Same general pattern as CVE-01.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_CVE07` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Grounded in a direct re-read
this session of §3.2 (locally available, `kora2024/kora-app/memory/`).
Not yet delivered to a real candidate — `FULLY_COMPLETE` still
requires that verification, per `../QUALITY_GATES.md`.

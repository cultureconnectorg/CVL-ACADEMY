# CVE-05 — ρ / Cultural Relationship & Value Dynamics

```
Prerequisite: CVE-04 (the CES formula this parameter lives inside).
```

## Repo truth

§3.1's `ρ_c ∈ (-∞, 1]`: substitution elasticity parameter, "calibrated
empirically per cycle (Hypothesis H2: ρ constant within a cycle,
re-estimated between cycles within the same bounds as the weights,
§5.3)." Three named special cases: `ρ_c → 1` (weighted sum, perfect
substitutability), `ρ_c → 0` (Cobb-Douglas form,
`CVI_i,c = Π_a x̂_i,c,a^{w_a,c}`), `ρ_c → -∞` (Leontief,
`CVI_i,c = min_a(x̂_i,c,a)`, total complementarity).

## Prerequisites

CVE-04.

## Objectives

1. Explain what "substitution elasticity" means economically for
   this specific formula: how freely one component (e.g. engagement
   `E`) can compensate for a weakness in another (e.g. attribution
   `C`) as `ρ_c` varies.
2. Correctly state and interpret all 3 named special cases and what
   each implies about component substitutability.
3. State Hypothesis H2 precisely (ρ constant within a cycle,
   re-estimated between cycles) and recognize this is a **hypothesis
   to be tested in chantier 2**, not an established empirical fact —
   never present it as validated.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | ρ parameter literacy | §3.1 | Written explanation of substitution elasticity for this formula specifically |
| M2 | Special-cases literacy | The 3 named limits | Table: ρ value → form → substitutability interpretation |
| M3 | Hypothesis-status discipline | H2 (§3.1, cross-ref §5.3) | Written note distinguishing "hypothesis stated" from "hypothesis validated" |

## Assessment

Per `../CERTIFICATION_MODEL.md`.

## Evidence / certification / mission eligibility

Same general pattern as CVE-01.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_CVE05` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Grounded in a direct re-read
this session of §3.1 (locally available, `kora2024/kora-app/memory/`).
Not yet delivered to a real candidate — `FULLY_COMPLETE` still
requires that verification, per `../QUALITY_GATES.md`.

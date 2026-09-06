# CVE-13 — CVE Simulation & Scenario Analysis

```
Prerequisite: CVE-01→12 (this formation teaches the roadmap for
calibrating and testing everything those formations formalize).
```

## Repo truth

The spec's own status line: "This is chantier 1 of the proof roadmap
— a prerequisite for simulation (chantier 2) and prototyping
(chantier 3)." Named parameters explicitly flagged as needing
empirical determination: the concave-transformation choice (§2.1, "to
be empirically decided during chantier 2"), `ρ_c` (§3.1, Hypothesis
H2), `N_min` for CHL peak detection (§3.3, Hypothesis H3), and every
`w_a,c`/`τ_fraude`/threshold the Governance Protocol (§6, C7) requires
to be "published + justified + archived" per cycle.

## Prerequisites

CVE-01→12 (the formulas this formation's simulation roadmap would
calibrate).

## Objectives

1. State precisely that chantier 2 (simulation) and chantier 3
   (prototyping) have **not been performed** — this formation teaches
   what that work would involve, never a result as if it had happened.
2. Enumerate the specific parameters/hypotheses the spec itself names
   as requiring empirical determination (H1 §2.1, H2 §3.1, H3 §3.3,
   plus `τ_fraude` and all `w_a,c`/`ρ_c` values).
3. Describe, at a methodology level, how a simulation against real
   listening/transaction logs (per H0's own reproducibility
   requirement) would validate or reject each named hypothesis —
   without claiming any such simulation has been run.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | Chantier status literacy | The spec's own status line | Written statement of exactly what stage this methodology is at |
| M2 | Named-hypothesis inventory | H1, H2, H3, and every "calibrated empirically" parameter | Complete table: hypothesis/parameter → section → what would validate it |
| M3 | Simulation-methodology literacy (never a claimed result) | H0 (reproducibility from raw logs) | Written methodology sketch, explicitly labeled as not-yet-performed |

## Assessment

Per `../CERTIFICATION_MODEL.md`. **A response that presents any
simulated or empirical result as if chantier 2 had occurred is
eliminatory** — this is the single most important discipline this
formation teaches.

## Evidence / certification / mission eligibility

Same general pattern as CVE-01. Mission eligibility: none — no real
simulation infrastructure exists to operate.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.

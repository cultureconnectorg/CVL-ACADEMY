# CVE-15 — CVE Governance & Economic Policy

```
Prerequisite: CVE-01, CVE-09, CVE-14.
```

## Repo truth

§6 (Fundamental Law — Complete Optimization Program):
`Maximize: Σ_i VCF_i^{corrected}(t)`, subject to 8 named constraints
`C1`→`C8`: fixed budget (C1), fraud resistance via `τ_fraude` (C2),
cycle-to-cycle stability bounds on weights/`ρ_c` (C3), a diversity
floor (C4), cultural neutrality (C5), auditability (C6), governance
publication requirement (C7: "∀ change in θ, published + justified +
archived"), and forecast/allocation separation (C8:
`Ŷ_i(t+Δ) ∉ inputs(UVC)`).

## Prerequisites

CVE-01, CVE-09 (allocation, constrained by this Fundamental Law),
CVE-14 (auditability, one of the 8 constraints).

## Objectives

1. Name and correctly explain all 8 constraints (C1→C8) — this is the
   formation's core deliverable, and no constraint may be paraphrased
   incorrectly or omitted.
2. Explain C8 specifically (forecast/allocation separation) and why it
   matters as a governance safeguard: Layer 3's forecasting output
   (`Ŷ`, §4) must never influence Layer 4's real allocation (`UVC`,
   §5) — a structural firewall against speculative bias entering
   actual value distribution.
3. Explain C7's publication requirement and connect it to real
   governance practice: any parameter change must be published,
   justified, and archived — never silently adjusted.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | The 8 constraints, precisely | §6 C1→C8 | Complete annotated table: constraint → formal statement → plain-language meaning |
| M2 | Forecast/allocation firewall (C8) | §4 (`Ŷ_i(t+Δ) ∉ inputs(Allocation)`), §6 C8 | Written explanation of why this separation exists as a governance safeguard |
| M3 | Governance publication discipline (C7) | §6 C7 | Written note on what "published + justified + archived" requires in practice |

## Assessment

Per `../CERTIFICATION_MODEL.md`. M1 must score every constraint
individually — a candidate who gets 6/8 right is not "mostly correct,"
each constraint is graded on its own.

## Evidence / certification / mission eligibility

Same general pattern as CVE-01. Mission eligibility: none — no
candidate is ever authorized to set live `θ` parameters through this
certification (per `../CERTIFICATION_MODEL.md` §Authorization gate).

## Status

`STATUS = PACKAGE_COMPLETE_FOR_CVE15` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Grounded in a direct re-read
this session of §6 (locally available, `kora2024/kora-app/memory/`).
**This closes task #183: all 14 formations (CVE-01, CVE-03→15) are
now at full canonical package depth, alongside the already-flagship
CVE-02 — 15/15 of the CVE corpus.** Not yet delivered to a real
candidate — `FULLY_COMPLETE` still requires that verification, per
`../QUALITY_GATES.md`.

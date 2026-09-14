# CVE-10 — Cultural Revenue Allocation

```
Prerequisite: CVE-09 (same formula, revenue-distribution framing).
```

## Repo truth

Same §5 formulas as CVE-09 (`UVC_i,c`, `value_UVC,c`), viewed from the
angle of `MD_c` as a real distributable revenue mass per cycle, and
constraint C1 (§6, `Σ_i UVC_i,c = MD_c`) as the budget-conservation
rule that makes this a genuine revenue-allocation (not just a scoring)
mechanism.

## Prerequisites

CVE-09 — this formation does not re-derive the UVC formula, it applies
it to the revenue-distribution question specifically.

## Objectives

1. Explain how `MD_c` (distributable mass) would be set for a real
   revenue cycle, and that the spec itself does not define how `MD_c`'s
   real-world monetary value is determined — only how it is
   distributed once fixed.
2. Explain the fixed-budget guarantee (C1) as the mechanism that makes
   this allocation zero-sum within a cycle — one work's larger share
   necessarily reduces others' relative to a fixed pool.
3. Cross-reference CVE-09's formula explicitly rather than
   re-deriving it — this formation's value is in the revenue-policy
   framing, not a second derivation.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | `MD_c` as a real revenue pool | §5, §6 C1 | Written note on what the spec defines (distribution) vs. leaves open (how MD_c's € value is set) |
| M2 | Zero-sum-within-cycle discipline | C1 | Written explanation with a numeric illustration |
| M3 | Cross-reference to CVE-09 | Same §5 formula | Explicit "see CVE-09" note — no re-derivation |

## Assessment

Per `../CERTIFICATION_MODEL.md`.

## Evidence / certification / mission eligibility

Same general pattern as CVE-01.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_CVE10` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Grounded in a direct re-read
this session of §5 and §6 C1 (locally available, `kora2024/kora-app/
memory/`), applied to the revenue-policy framing without re-deriving
CVE-09's formula. Not yet delivered to a real candidate —
`FULLY_COMPLETE` still requires that verification, per
`../QUALITY_GATES.md`.

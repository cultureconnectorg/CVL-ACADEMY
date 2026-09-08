# CVE-08 — VCF — Value/Contribution Framework

```
Prerequisite: CVE-01, CVE-04. FORMALIZATION_PENDING — see repo truth.
```

## Repo truth

**Direct verification this session:** `VCF` (Value/Contribution
Framework, or "Value Creation Function") is **referenced but never
derived** in `KORA_CVE_Specification_Mathematique_v1.0.md`. It appears
in two places: §3.3's Cultural Half-Life derivation
(`v_i(t) = dVCF_i/dt`, "instantaneous rate of incremental value
creation") and §6's Fundamental Law
(`Maximize: Σ_i VCF_i^{corrected}(t)`). Both usages **assume** VCF as
a given input function — no equation defining VCF itself (in terms of
`S,E,F,C,N` or any other primitive) appears anywhere in this document.

## Prerequisites

CVE-01, CVE-04 (CES/CVI, the closest defined analog).

## Objectives

1. Correctly quote both real appearances of VCF in the spec (§3.3,
   §6) and state precisely what each usage assumes about VCF (a
   differentiable function of time whose rate feeds CHL peak
   detection; an objective function maximized subject to constraints).
2. State clearly that no defining equation for VCF itself exists in
   this frozen document — this is a genuine formalization gap, not an
   oversight to paper over.
3. Explain the most defensible working hypothesis a candidate could
   reason with (e.g., `VCF_i(t) ≈ CVI_i,c` at the cycle level, since
   CVI is the closest fully-defined "value" quantity) **while
   explicitly labeling it a hypothesis, never presenting it as
   something the spec itself states.**

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | VCF's two real appearances | §3.3, §6 | Quoted, annotated citations of both usages |
| M2 | Formalization-gap verification | Absence of a VCF-defining equation anywhere in the document | Written verification note, same discipline as CVE-06/M2 |
| M3 | Working-hypothesis discipline | CVI (§3.1) as the closest defined proxy | Written note, explicitly labeled `HYPOTHESIS, NOT SPEC` |

## Assessment

Per `../CERTIFICATION_MODEL.md`. **M2 is eliminatory**: presenting an
invented VCF formula as KORA methodology fails this formation
regardless of other scores. A correctly-labeled hypothesis in M3 is
not a violation — the label is what matters.

## Evidence / certification / mission eligibility

Same general pattern as CVE-06.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_CVE08` (`FORMALIZATION_PENDING` still
applies to a defining VCF equation — this package teaches the two real
citations, the verified gap, and a clearly-labeled working hypothesis,
never an invented equation) — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Grounded in a direct re-read
this session of §3.3 and §6 (locally available, `kora2024/kora-app/
memory/`). Not yet delivered to a real candidate — `FULLY_COMPLETE`
still requires that verification, per `../QUALITY_GATES.md`.

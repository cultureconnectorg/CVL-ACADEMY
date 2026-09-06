# CVE-02 — Cultural Value Measurement

```
Prerequisite: CVE-01.
```

## Repo truth

`kora2024/Kora-app/memory/KORA_CVE_Specification_Mathematique_v1.0.md`
§1 (Layer 1 — Measurement, Raw Signals):

- §1.1 Trust Score: `TS_i(t) = w_id·sig_id(t) + w_comp·sig_comp(t) +
  w_net·sig_net(t) + w_hist·sig_hist(t)`, `w_id+w_comp+w_net+w_hist=1`,
  each `sig ∈ [0,1]`, indicative calibration `w_id=0.4, w_comp=0.3,
  w_net=0.2, w_hist=0.1`. Validation Filter: an event `e` is retained
  if `TS_i(t_e) ≥ τ_fraude` (a per-cycle, published threshold).
- §1.2 Normalized Raw Components (`S,E,F,C,L` — for each work `i` and
  cycle `c`): `S_i,c` (validated streams, percentile-normalized),
  `E_i,c` (engagement: weighted duration/re-listen/playlist-add
  proxy), `F_i,c` (fidelity: active-week fraction, Premium-weighted),
  `C_i,c` (attribution: 14-day-window conversion value share),
  `L_i,c` (legacy — replaced by the CHL integral, §3.3, a *derived*
  not raw component).
- §2.1 Concave transformation: `x̂ = log(1+x)` or `x̂ = x^0.5`, choice
  deferred to chantier 2 (Hypothesis H1: same form for every component
  within a cycle).

## Prerequisites

CVE-01 (notation, H0).

## Objectives

By the end of CVE-02, a candidate can:
1. Write and explain the Trust Score formula exactly, including its
   4 named weights and their indicative calibration values, and state
   the Validation Filter's role (fraud-resistance gate before any
   event counts toward measurement).
2. Write and explain all 5 raw component formulas (`S,E,F,C,L`),
   correctly noting that `L` is uniquely *derived* (from CHL, §3.3)
   rather than raw like the other 4.
3. Explain the concave saturation transformation (§2.1) and correctly
   state that the choice between its two named forms is explicitly
   **not yet decided** — deferred to chantier 2 — never presented as
   settled.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | Trust Score formula + Validation Filter | §1.1 | Annotated formula + worked numeric example with illustrative `sig` values summing the weighted terms |
| M2 | Five raw components (`S,E,F,C,L`) | §1.2 | Table: component → formula → what real signal it measures → raw or derived |
| M3 | Saturation transformation + its open-decision status | §2.1, Hypothesis H1 | Written note: both forms stated, explicitly flagged as undecided pending chantier 2 |
| M4 | Boundary to Layer 2 | §3.1 (cross-reference only, not re-derived) | One-paragraph hand-off note: these 5 (transformed) components feed the CES aggregation taught in CVE-04 |

## Assessment

Per `../CERTIFICATION_MODEL.md`. N1: formula-recall + worked-example
quiz. N2: "a stakeholder asks why an event with `TS_i(t_e) < τ_fraude`
doesn't count — explain the Validation Filter's purpose without
overstating what it guarantees" plus a case distinguishing raw (`S,E,
F,C`) from derived (`L`) components. Assessment: M1+M2 worked
deliverables, graded against the real spec.

## Evidence / certification / mission eligibility

Evidence = M1 worked example + M2 table + M3 written note, all
checkable against the real spec section by section. Certification
eligibility: pass Assessment at N2+. Mission eligibility: none directly
— no real calibrated CVE system exists to operate (chantier 2/3 not
performed); a certified CVE-02 candidate is qualified to teach or
review the methodology, never to set live parameters.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_CVE02` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Not yet delivered to a real
candidate — `FULLY_COMPLETE` still requires that verification, per
`../QUALITY_GATES.md`.

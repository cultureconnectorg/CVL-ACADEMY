# CVE-06 — Shapley Value for Cultural Contribution

```
Prerequisite: CVE-03. FORMALIZATION_PENDING — see repo truth below.
```

## Repo truth

**Direct verification this session: the term "Shapley" does not
appear anywhere in `KORA_CVE_Specification_Mathematique_v1.0.md`.**
The document's own real attribution mechanism is the simple 14-day
conversion-window `C_i,c` formula (§1.2, taught in CVE-03) — a
proportional, not game-theoretic, allocation. This formation's name
promises a specific method (Shapley value — a cooperative game theory
concept for fairly distributing credit among multiple contributors)
that the frozen v1.0 spec neither names nor formalizes.

## Prerequisites

CVE-03 (the real attribution mechanism that exists today).

## Objectives

1. Explain what a Shapley value is, as a general market-standard
   concept in cooperative game theory and multi-touch attribution
   (`NEW_EXTERNAL`-flavored content, defensible on its own market
   merits) — clearly separated from any claim that KORA's CVE
   implements it.
2. State precisely, with the direct verification method (a full-text
   search of the frozen spec), that no Shapley-value formula exists in
   `KORA_CVE_Specification_Mathematique_v1.0.md` today.
3. Never present a Shapley-value formula as if it were part of the
   KORA CVE methodology — that would be exactly the `FAKE_PROOF`
   failure mode this Master Package exists to prevent, applied to
   mathematics.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | Shapley value — general concept (market-standard) | Standard cooperative game theory literature (not KORA-specific) | Written explanation of the general method, clearly labeled as external/market knowledge |
| M2 | Verification of absence in the KORA spec | Direct full-text check of `KORA_CVE_Specification_Mathematique_v1.0.md` | Written verification note: "Shapley" does not appear; `C_i,c` (CVE-03) is the real mechanism today |
| M3 | What a future formalization would require | §1.2's own attribution mechanism as the starting point | Honest gap note: what work (chantier 2/3, or a new spec revision) would be needed before a real Shapley-based CVE attribution could be taught as KORA methodology |

## Assessment

Per `../CERTIFICATION_MODEL.md`. **M2 is eliminatory**: a candidate who
presents a Shapley-value formula as existing KORA methodology fails
this formation regardless of other scores.

## Evidence / certification / mission eligibility

Evidence = M1 (general, correctly scoped) + M2 (verification note) +
M3 (honest gap). Certification eligibility: pass Assessment at N2+.
Mission eligibility: none — this concept has no real KORA
implementation to operate.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_CVE06` (`FORMALIZATION_PENDING` still
applies to the KORA-specific Shapley content — this package teaches
the general concept, the verified absence, and the honest gap, never
an invented KORA formula) — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Grounded in a direct re-read
this session of the full spec (full-text search confirms "Shapley"
appears nowhere in it). Not yet delivered to a real candidate —
`FULLY_COMPLETE` still requires that verification, per
`../QUALITY_GATES.md`.

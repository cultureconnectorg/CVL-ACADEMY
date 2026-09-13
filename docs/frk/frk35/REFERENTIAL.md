# FRK-35 — Versions, Derivatives, Credits & Contributions

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION`, action `NEW_EXTERNAL`. Same LabelOS
boundary as FRK-34 (LOS-02 Metadata & Catalog) — inherited, never
re-derived. LabelOS itself has zero repo footprint per
`REPO_REGISTRY.md`.

## Prerequisites

FRK-34 (recommended, not strict).

## Objectives

A candidate who completes FRK-35 can design real version/derivative/
credit tracking for a creative work, extending FRK-34's identity-
tracking base:

- Explain how version/derivative/credit tracking extends FRK-34's
  work-identity tracking: FRK-34 identifies the work itself; FRK-35
  traces its evolution over time (versions, derivatives) and who
  contributed to each stage technically.
- Distinguish a contribution credit from a copyright/rights decision
  precisely: a contribution credit documents a fact (who did what,
  in what technical role, at what time) — a purely provenance-level
  record; copyright/rights decisions determine the legal consequences
  of that fact (ownership share, royalty split, licensing terms) — a
  distinct layer this formation never enters.
- Design a version/derivative chain: each version or derivative gets
  a distinct identifier that references its source (original →
  derivative → derivative-of-derivative), so the evolution of a work
  is traceable without ambiguity.
- Design a contribution-credit record: bind a named contributor to a
  specific version/derivative and a technical role (e.g. "remixer",
  "mastering engineer") as a purely factual, technical record — never
  a rights or royalty determination.
- Keep the inherited LabelOS boundary explicit: this formation
  documents technical provenance facts about versions/derivatives/
  credits, never LabelOS's catalog/rights-record management (LOS-02) —
  the same boundary FRK-34 established, applied unchanged here.
- Reuse FRK-34's identity-tracking fundamentals by reference — never
  re-author them here; cite `docs/frk/frk34/REFERENTIAL.md` instead.

## Modules

1. **Version & derivative tracking fundamentals** — the identifier/
   reference chain that traces a work's evolution, and its
   relationship to FRK-34's work-identity base.
2. **Contribution-credit provenance practice** — the credit-vs-rights
   distinction, and binding a contributor to a version/role as a
   purely technical record.
3. **Boundary discipline vs. LabelOS (inherited from FRK-34)** — never
   LabelOS's catalog/rights-record function (LOS-02); reuse FRK-34 by
   reference, never redefine it.

## Assessment

A version-tracking exercise: candidate designs a version/derivative
chain with contribution credits (original → derivative, contributor +
technical role per stage), citing FRK-34 by reference for the
underlying work-identity fundamentals, then explains why the credits
modeled never constitute a copyright or royalty-split decision —
graded with the same eliminatory boundary check as FRK-34.

## Evidence / certification / mission eligibility

`FRK35.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.

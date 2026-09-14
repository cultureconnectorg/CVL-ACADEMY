# FRK-63 — Geo Evidence & Territorial Provenance

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION`, action `NEW_EXTERNAL`. Cross-reference
KOR-15 (territorial distribution strategy) — different altitude (FREK
proves geo-provenance of an evidence object; KOR-15 does market/rights
strategy for a territory), no merge.

## Objectives

A candidate who completes FRK-63 can design a real geo-evidence proof
mechanism, kept at a strictly different altitude from any territorial
business strategy:

- Explain what geo-evidence/territorial provenance is (proving the
  geographic origin/movement of a cultural asset technically) and how
  it radically differs from KOR-15 (market/rights strategy per
  territory): FRK-63 technically proves *where* an object was
  created/moved (a proof); KOR-15 would decide a commercial/rights
  strategy *for* a territory (a decision) — two completely different
  altitudes.
- Explain why both subjects touch "territory" without ever
  overlapping: FRK-63 is a technical proof discipline; KOR-15 would be
  a business-strategy discipline — the word "territory" is shared, the
  subject is not.
- Design a real technical geo-evidence mechanism: signed GPS
  coordinates captured at the moment of creation, cryptographically
  bound to the asset's hash and a timestamp — and state precisely what
  this guarantees (the location claim wasn't falsified after the
  fact) and what it does NOT guarantee (anything about the content
  itself, or any right to exploit the asset in that location).
- Explain precisely why this formation stays teachable even if KOR-15
  is never built: FRK-63 is an independent technical proof discipline,
  teachable with zero dependency on any territorial commercial
  strategy existing.
- Keep the boundary absolute: a geo-evidence mechanism must remain
  identical regardless of what territorial commercial strategy is
  chosen (or whether one exists at all) — that is the proof the two
  subjects are genuinely independent.

## Modules

1. **Geo-evidence proof fundamentals** — signed-coordinate capture,
   and the precise guarantee it provides (location authenticity, not
   content authenticity or rights).
2. **Territorial-provenance practice** — real mechanism design binding
   coordinates + timestamp + asset hash cryptographically.
3. **Boundary discipline vs. KOR-15** — the altitude distinction
   (technical proof vs. business strategy); a valid mechanism needs
   zero dependency on KOR-15 existing.

## Assessment

A geo-provenance exercise: candidate designs a signed-coordinate
geo-evidence mechanism for a cultural asset with no reference to any
commercial strategy, then explains why that mechanism would remain
identical regardless of the territorial commercial strategy chosen (or
the absence of KOR-15 entirely) — graded against real practice, never
against an invented CVLN capability.

## Evidence / certification / mission eligibility

`FRK63.SKILL.*` Skill IDs reserved (see `EVIDENCE_MODEL.md`).
`READY_FOR_FREK_PROOF = FALSE` — no mission eligibility path exists
for this formation today.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass. Never
implies `FULLY_COMPLETE` — that requires a real candidate pass, per
`../QUALITY_GATES.md`.

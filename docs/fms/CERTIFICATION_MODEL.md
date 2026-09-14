# FMS-07→18 — Certification Model (shared)

## Evidence chain

Same shape as `docs/gmd/CERTIFICATION_MODEL.md` and
`docs/wal/CERTIFICATION_MODEL.md`: référentiel modules → N1 (formative
bank) → N2 (applied cases) → assessment artifact → correcteur → (jury
on borderline scores) → Skill ID record.

## N1/N2/assessment structure

- **N1**: formative quiz bank, one per formation, sourced strictly
  against the cited route/model (FMS-07/15/18) or by-reference module
  (FMS-08/09/11) in that formation's `REFERENTIAL.md`.
- **N2**: 2-3 applied cases per formation, each with an eliminatory
  rule for any invented capability — a candidate who claims a KPI
  `fms-os/fms` explicitly reports as `INSUFFICIENT_DATA` (e.g.
  `revenue_mtd`) fails the case, by design.
- **Assessment**: a real artifact (annotated booking/session log, a
  studio-ops KPI reading exercise against the real `command_center`
  payload shape, a recording/mix session review) checkable against the
  real code or the Founder-gated FMS-01→06 canon it cites — never
  against invented facts.

## Skill ID namespace

`FMS07.SKILL.*` → `FMS18.SKILL.*`, reserved in
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md` once each formation is deepened.
FMS-08/09's Skill IDs are explicitly namespaced as specialization
tracks (`FMS08.SPEC.*`, `FMS09.SPEC.*`) distinct from the base
`FMS03.SKILL.*` IDs they build on — never merged with the base
certification's own Skill IDs.

## Authorization gate

Passing an FMS-07/15/18 assessment never grants real write access to
`fms-os/fms` in production — certification is on literacy of its data
model and workflow, per `00_GOVERNANCE/AUTHORIZATION_MODEL.md`.
FMS-08/09/11 specialization certification never re-opens or
re-authors the Founder-gated FMS-01→06 canon — it is graded on the
specialization's own added material only, referencing the base
module's competency as an assumed prerequisite (verified via the
candidate's already-recorded FMS-03/FMS-04 certification, not
re-tested).

## Renewal cycle

Standard 24 months for all 9 formations. No FMS-0X formation handles
sensitive financial/ledger integrity the way WAL-21/28 or GMD-28/33 do,
so no formation in this wave is flagged for the 12-month sensitive
cycle — a Founder/governance call to revisit if `fms-os/fms` gains a
real payment/invoicing capability (today explicitly
`INSUFFICIENT_DATA`/`NOT_CONNECTED` in its own code).

## Never claim FULLY_COMPLETE

No FMS-0X formation is `FULLY_COMPLETE` until a real candidate has been
assessed, a jury/corrector verification performed, and evidence
actually recorded — none of which this drafting pass performs, even
for FMS-07 (this wave's `PACKAGE_COMPLETE` flagship).

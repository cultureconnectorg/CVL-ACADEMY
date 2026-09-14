# FRK-01/58/03/06/13/56/59/68 — Certification Model (shared)

## Evidence chain

Same shape as `docs/gmd/CERTIFICATION_MODEL.md`,
`docs/wal/CERTIFICATION_MODEL.md`, `docs/fms/CERTIFICATION_MODEL.md`:
référentiel modules → N1 (formative bank) → N2 (applied cases) →
assessment artifact → correcteur → (jury on borderline scores) →
Skill ID record.

## N1/N2/assessment structure

- **N1**: formative quiz bank, sourced strictly against
  `frek_core.py`'s real methods/constants or the cross-repo artifacts
  cited in each `REFERENTIAL.md`.
- **N2**: 2-3 applied cases, each with an eliminatory rule for any
  invented capability — a candidate who claims `issue_proof()` produces
  a cryptographically verifiable proof, or that Good Mood's two
  outboxes are linked to each other, fails the case by design.
- **Assessment**: a real artifact (annotated signal-emission log, a
  `mint_frek_id()` counter trace, an outbox-monitoring reading
  exercise) checkable against the real code — never against invented
  facts.

## Skill ID namespace

`FRK01.SKILL.*`, `FRK58.SKILL.*`, `FRK03.SKILL.*`, `FRK06.SKILL.*`,
`FRK13.SKILL.*`, `FRK56.SKILL.*`, `FRK59.SKILL.*`, `FRK68.SKILL.*`,
reserved in `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md` once each formation
is deepened. `READY_FOR_FREK_PROOF = FALSE` on every evidence model in
this slice — same discipline as every `docs/kor/` module, never
promoted to `TRUE` without a real external verifiable anchor, which
does not exist anywhere in this repo today.

## Authorization gate

Passing any assessment in this slice never grants real write access to
`frek_core.py`, `db.frek_signals`, or any outbox table in production —
certification is on literacy, per
`00_GOVERNANCE/AUTHORIZATION_MODEL.md`.

## Renewal cycle

Standard 24 months for all 8 formations. None handle sensitive
financial/ledger integrity directly (that stays WAL-21/28's domain),
so no formation here is flagged for the 12-month sensitive cycle.

## Never claim FULLY_COMPLETE

No formation in this slice is `FULLY_COMPLETE` until a real candidate
has been assessed, a jury/corrector verification performed, and
evidence actually recorded — none of which this drafting pass
performs, even for FRK-01 (this wave's `PACKAGE_COMPLETE` flagship).

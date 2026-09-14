# WAL-19→28 — Certification Model (shared)

## Evidence chain

Same shape as `docs/gmd/CERTIFICATION_MODEL.md`: référentiel modules →
N1 (formative bank) → N2 (applied cases) → assessment artifact →
correcteur → (jury on borderline 2.0–2.5) → Skill ID record.

## N1/N2/assessment structure

- **N1**: formative quiz bank, one per formation, sourced strictly
  against the cited file(s) in that formation's `REFERENTIAL.md`.
- **N2**: 2-3 applied cases per formation, each with an eliminatory
  rule for any invented capability.
- **Assessment**: a real artifact (annotated field table, executed
  runbook, or written diagnostic) checkable against the real code —
  never against invented facts.

## Skill ID namespace

`WAL19.SKILL.*` → `WAL28.SKILL.*`, reserved in
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md` once each formation is deepened.
No Skill ID is reserved prematurely for WAL-22/23/25/26/27 — reserving
a Skill ID for a capability that doesn't exist would itself be a
`FAKE_PROOF` risk.

## Authorization gate

Passing a WAL-2X assessment never grants real write access to
`backend/wallet/` in production, nor any access whatsoever to the real
external `djsayd/CVLN-Wallet` product — that stays a separate,
human-governed decision, per `00_GOVERNANCE/AUTHORIZATION_MODEL.md`.

## Renewal cycle

Standard 24 months, except WAL-21 (Ledger Operator) and WAL-28 (Audit
& Evidence Operations), which handle the ledger's integrity directly —
recommend the 12-month sensitive cycle (`ECO-042`), same pattern as
GMD-28/33; a Founder/governance call, not decided unilaterally here.

## Never claim FULLY_COMPLETE

No WAL-2X formation is `FULLY_COMPLETE` until a real candidate has
been assessed, a jury/corrector verification performed, and evidence
actually recorded — none of which this drafting pass performs.

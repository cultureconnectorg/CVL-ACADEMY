# CVE-01→15 — Certification Model (shared)

## Evidence chain

Same shape as `docs/gmd/CERTIFICATION_MODEL.md` and
`docs/wal/CERTIFICATION_MODEL.md`: référentiel → N1 (formative bank)
→ N2 (applied cases) → assessment artifact → correcteur → (jury on
borderline 2.0–2.5) → Skill ID record.

## N1/N2/assessment structure

- **N1**: formative quiz bank per formation, sourced strictly against
  the cited section(s) of `KORA_CVE_Specification_Mathematique_
  v1.0.md`.
- **N2**: 2-3 applied cases per formation, each with an eliminatory
  rule for any invented formula, parameter, or result not in the real
  spec (including a fabricated Shapley/VCF derivation for CVE-06/08).
- **Assessment**: a real, checkable artifact (annotated formula
  derivation, worked numeric example using only named/illustrative
  weights, written diagnostic) — never a claimed empirical result,
  since the spec's own chantier 2 (simulation) has not been performed.

## Skill ID namespace

`CVE01.SKILL.*` → `CVE15.SKILL.*`, reserved in
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md` once each formation is
deepened. No Skill ID reserved prematurely.

## Authorization gate

Passing a CVE-0X assessment never grants authority to set or modify
live CVE parameters (`θ`, weights, `ρ_c`, `τ_fraude`) in any real
system — per the spec's own Governance Protocol (§6, C7: "any change
in θ published + justified + archived"), that stays a separate,
human-governed decision.

## Renewal cycle

Standard 24 months for all 15 — none of these formations grant
operational financial authority the way GMD-28/33 or WAL-21/28 do;
this is methodology literacy, not an operator role over live money.

## Never claim FULLY_COMPLETE

No CVE-0X formation is `FULLY_COMPLETE` until a real candidate has
been assessed and verified — none of which this drafting pass
performs. Separately: no CVE-0X formation may ever claim the KORA
methodology's own chantier 2 (simulation) or chantier 3 (prototyping)
has occurred — the spec's own status line says neither has, and this
corpus must not imply otherwise regardless of a candidate's
certification status.

# FRK-10 — EUDI, SD-JWT & Interoperable Identity

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION`, action `NEW_EXTERNAL`,
**`NEEDS_EXPERT_REVIEW`** — EU regulatory-specific (eIDAS2/EUDI
Wallet). **Never taught as universal without an explicit jurisdiction
caveat**, and never presented as something CVLN implements today.

This gate is deliberate, not an oversight: unlike most FRK formations,
this one teaches a live, still-evolving EU regulatory framework. A
factual error here is a compliance error, not just a pedagogical one.
Literacy content below is expanded to real technical depth; assessment,
rubric, evidence model, and certification stay deferred until a named
regulatory/legal expert has reviewed the content — this stays
deliberately below `PACKAGE_COMPLETE` for that reason, even after this
deepening pass.

## Objectives

A candidate who completes the literacy track can explain, accurately
and with the jurisdiction caveat always attached:

- **The eIDAS2 framework.** Regulation (EU) 2024/1183, amending the
  original 2014 eIDAS Regulation, entered into force in May 2024. It
  requires every EU Member State to make at least one European Digital
  Identity Wallet (EUDI Wallet) available to citizens and residents,
  on a rollout timeline set by implementing acts under the Architecture
  Reference Framework (ARF) published by the European Commission.
- **What the EUDI Wallet actually holds.** Person Identification Data
  (PID — the baseline identity attributes a Member State issues) and
  electronic attestations of attributes (EAA), including qualified
  electronic attestations of attributes (QEAA) issued by
  qualified/certified providers. The wallet is a holder-controlled
  container, not a central identity database.
- **The presentation model.** A relying party requests specific
  attributes; the holder consents per request; the wallet returns only
  what was requested and consented to — never the full underlying
  credential by default.
- **SD-JWT as a technical format.** Selective Disclosure JWT (an IETF
  specification): the issuer creates a JWT whose individual claims are
  each committed to as a hashed "disclosure" rather than inlined
  directly; the holder can reveal a subset of disclosures to a verifier
  along with a key-binding JWT proving possession, without exposing
  undisclosed claims. SD-JWT VC (SD-JWT-based Verifiable Credentials)
  is the concrete profile being standardized for EUDI Wallet
  attestations.
- **The jurisdiction boundary, explicitly.** This entire framework is
  an EU regulatory instrument. It has no legal force outside the EU/EEA
  and must never be taught, cited, or applied as a universal identity
  standard — a candidate who generalizes it without the EU-specific
  caveat has failed the one discipline this formation actually
  certifies today.

## Modules

1. eIDAS2/EUDI Wallet regulatory framework (EU-specific).
2. SD-JWT technical format literacy.
3. Jurisdiction-caveat discipline.

## Module depth

See §Objectives above for the real technical content behind each
module title — Regulation (EU) 2024/1183, the PID/EAA/QEAA attribute
model, the ARF rollout structure, and the SD-JWT hashed-disclosure /
key-binding mechanism.

## Assessment

Deferred pending `NEEDS_EXPERT_REVIEW` — no certification assessment
is administered until a named regulatory/legal expert has reviewed
this content. A literacy-only check (not a certification) exists in
`BANQUE_N1.md`/`BANQUE_N2.md` to confirm factual accuracy and
jurisdiction discipline; it does not issue any Skill ID or
certification credit (see `EVIDENCE_MODEL.md`).

## Status

`STATUS = MODULE_CONTENT_DRAFTED`, `NEEDS_EXPERT_REVIEW` unresolved —
literacy content deepened this pass to real eIDAS2/EUDI/SD-JWT
technical depth. Never promoted to `PACKAGE_COMPLETE`: no certification
track opens until a named regulatory expert reviews this content, per
standing doctrine — this stays deliberately below the other formations
deepened in this pass, by design.

# FRK-32 — Context, Device & Consent Signals

## Grounding

Per `FREK_01_75_RECONCILIATION.md`: coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION`, action `NEW_EXTERNAL`. Same boundary note
as FRK-31 (not the real `VALID_SIGNALS`); "consent" also touches
Fondation Cœurvolan doctrine (§18) — cross-reference, don't duplicate.

## Objectives

A candidate who completes FRK-32 can use real context/device/consent-
signal vocabulary while respecting two independent, mandatory
boundaries:

- Explain what a context/device signal is (e.g. device type, access
  channel) and why it stays distinct from the real `VALID_SIGNALS` set
  in `frek_core.py` — the exact 8 values `FREK-TIME`, `FREK-WORK`,
  `FREK-SCORE`, `FREK-LINK`, `FREK-CERT`, `FREK-CONTRIB`, `FREK-SHARE`,
  `FREK-MISSION` — the same mandatory boundary FRK-31 already
  established for its own vocabulary.
- Explain what technical consent-signal capture is, and why this
  formation covers ONLY the technical side (recording that a consent
  event happened: timestamp, channel, version of terms presented) —
  never consent governance itself (who may consent, for what, under
  what legal conditions).
- Explain what Fondation Cœurvolan §18 doctrine says about consent at
  a boundary level, and why this formation references it without ever
  duplicating it: §18 governs consent in the community/legal sense —
  this formation cites it as the boundary, never re-derives or
  paraphrases its content.
- Explain precisely why conflating technical signal capture with
  consent governance would be eliminatory here: it would let a
  technical capture competency masquerade as governance compliance —
  a serious methodological gap, not just an imprecision.
- Design a technical consent-capture flow (timestamp, channel, terms
  version) that takes zero governance decisions, and confirm on a
  concrete example that this vocabulary is neither `VALID_SIGNALS` nor
  Fondation Cœurvolan's governance doctrine — three genuinely distinct
  things.

## Modules

1. **Context/device signal concepts** — device type, access channel,
   and similar market-general context signals, kept distinct from
   `frek_core.py`'s real `VALID_SIGNALS` set.
2. **Consent-signal capture practice (technical side only)** — the
   timestamp/channel/terms-version capture flow, with zero governance
   decisions taken.
3. **Cross-reference discipline vs. Fondation Cœurvolan §18 and vs.
   real `VALID_SIGNALS`** — two independent, mandatory boundaries,
   each checked separately, neither ever merged into this formation's
   content.

## Assessment

A concept exam: candidate designs a technical consent-signal capture
flow with zero governance content, then explains on a concrete example
why this vocabulary is neither `VALID_SIGNALS` (`frek_core.py`) nor
Fondation Cœurvolan's §18 governance doctrine — with an eliminatory
check on conflating either boundary.

## Evidence / mission eligibility

No mission eligibility path exists yet. `FRK32.SKILL.
CONTEXT_DEVICE_CONSENT_SIGNALS.L1` reserved once deepened (see
`EVIDENCE_MODEL.md`).

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package (référentiel +
N1/N2 + assessment/rubric + evidence model + 3 guides + integration
note), deepened this pass. Never implies `FULLY_COMPLETE`.

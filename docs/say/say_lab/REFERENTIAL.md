# SAY-LAB — DJ Sayd Lab (capstone bridge, flagship)

## Grounding

Per `GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`: the correct point of
connection between the Good Mood and DJ Sayd domains — an applied
capstone case lab that follows one artist (the DJ Sayd persona)
through the specialization paths above, **using the real Good Mood
OS platform as its literal applied backend**:

- **`GMD-22`** (Catalogue Operator — real `Volume` model, `/catalogue`,
  `/admin/catalogue`).
- **`GMD-24`** (Ticket Type & Sales Operator — real `TicketType`,
  `/tickets/{tid}`, `/tickets/{tid}/qr.png`).
- **`GMD-27`** (Merch & Store Operator — real `Product` model,
  `/merch`, `/admin/merch/*`).
- **`GMD-28`** (Orders & Payment Operations — real Stripe:
  `/payments/checkout`, `/stripe/webhook`).

This is the same "reuse by reference, never duplicate" discipline
already applied to FMS-11/FMS-18 — `NEW_BRIDGE` (capstone), not a
formation of its own in the sense of teaching new technical
competency; it is the **worked proof** that Good Mood and DJ Sayd are
one coherent story told from two sides, not two parallel Academies.

## Boundary

- Never re-teaches `GMD-22`/`24`/`27`/`28`'s own competencies — cites
  their real routes/models as the applied backend a candidate reads
  against, exactly as already documented in `docs/gmd/gmd22/`,
  `gmd24/`, `gmd27/`, `gmd28/`.
- Never re-teaches the DJ Sayd specialization tracks (`docs/say/
  SAY_SPECIALIZE_EXISTING_NOTES.md`, `docs/say/external/say_new/`) —
  cites them as the artist-side competency the candidate must already
  hold.
- Never claims a live, wired integration between the DJ Sayd persona
  and the real Good Mood OS beyond what a case study can simulate on
  paper — `gmfest972/goodmooddjsayd` is a read-only-audited repo, not
  a runtime this Academy operates.

## Prerequisites

At least one formation from `docs/say/SAY_SPECIALIZE_EXISTING_NOTES.md`
or `docs/say/external/say_new/` (artist-side competency), literacy of
`docs/gmd/gmd22/`, `gmd24/`, `gmd27/`, `gmd28/` (platform-side
competency).

## Objectives

- Follow one artist (the DJ Sayd persona) through a full release/
  event cycle: catalogue entry (`GMD-22`) → ticketed event (`GMD-24`)
  → merch (`GMD-27`) → payment settlement (`GMD-28`).
- Demonstrate that the artist-side (DJ Sayd) and platform-side (Good
  Mood) competencies are complementary, never overlapping — reading
  the real routes/models as a platform operator would, while reasoning
  as the artist whose career depends on them.
- Precisely distinguish, for every decision point in the cycle, which
  side owns it: the artist decides creative and commercial direction
  (which tracks to release, what merch to design, pricing intent for
  tickets); the operator configures and maintains the platform
  mechanics that carry those decisions out (catalogue entry format,
  webhook configuration, QR generation, Stripe checkout flow).
- Never claim mission eligibility beyond literacy — this is a
  capstone case lab, not a real production deployment.
- Explain precisely why this capstone reuses `GMD-22/24/27/28` by
  reference rather than re-deriving a fictional backend: the real repo
  `gmfest972/goodmooddjsayd` has already been audited and documented at
  each of those four formations — inventing a parallel fictional
  backend here would fork the truth into two inconsistent versions of
  the same real system.
- Explain precisely why inventing a platform capability that neither
  Good Mood nor DJ Sayd actually has (a loyalty engine, a royalty-split
  calculator, an analytics dashboard) would be an eliminatory error:
  it would claim the real repo does something it does not, undermining
  the entire "worked proof" nature of this capstone.

## Modules

1. Catalogue entry as the artist's discography (reads `GMD-22`'s real
   `Volume` model).
2. Ticketed event planning (reads `GMD-24`'s real `TicketType`/QR
   flow).
3. Merch line planning (reads `GMD-27`'s real `Product` model).
4. Payment/settlement literacy (reads `GMD-28`'s real Stripe
   checkout→webhook flow).
5. Capstone synthesis — the candidate produces a documented
   end-to-end release/event plan citing all 4 real touchpoints,
   without inventing a capability neither Good Mood nor DJ Sayd
   actually has.

## Assessment

A capstone case-lab exercise: candidate is given the real route/model
shapes from `GMD-22/24/27/28` and must produce a documented artist
release/event plan that correctly uses each, with an eliminatory
failure for inventing a platform capability (e.g. a loyalty engine,
a royalty-split calculator) that does not exist in the real repo, or
for attributing an artist decision to the operator side or vice versa.

## Evidence / mission eligibility

`SAYLAB.SKILL.CAPSTONE_RELEASE_EVENT_CYCLE.L1` reserved once deepened.
No mission eligibility path exists today — this is a documentary
capstone, not a live integration.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package (référentiel +
N1/N2 + assessment/rubric + evidence model + 3 guides + integration
note), built this pass as the Good Mood/DJ Sayd domain's flagship
capstone. Never implies `FULLY_COMPLETE` — no real candidate has been
assessed yet.

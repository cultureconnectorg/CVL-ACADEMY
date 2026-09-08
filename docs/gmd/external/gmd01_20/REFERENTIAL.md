# GMD-01→20 — Live-Events/Festival Industry Pathway (external/market)

## Grounding

Per `GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`: coverage `NONE` — the
live-events/festival-industry side (promoter, production manager,
ticketing ops, sponsorship, festival marketing) is a real, standard
career track genuinely distinct from FMS's artist-side canon (Academy
currently teaches artist development/business/production/branding/
management, but has **no formation from the event-organizer/promoter/
venue side**). Action: `NEW_EXTERNAL` for all 20 — zero duplication
risk.

**Best-grounded rows** (real worked examples from `gmfest972/
goodmooddjsayd`, already audited for the internal-operator layer
`GMD-21→33`): GMD-05 (Ticketing Ops), GMD-06 (Sales/Revenue), GMD-07
(CRM), GMD-08 (Merchandising), GMD-11 (Content/Media Ops — QR/
reporting), GMD-13 (Data & Analytics — event report endpoint), GMD-14
(Finance — Stripe), GMD-15 (Safety/Access — real door-scan), GMD-16
(Multilingual — real bilingual newsletter copy), GMD-19 (Reporting).
Each cites its `GMD-2x` internal-operator counterpart (`docs/gmd/
gmd2x/`) as the worked example, never re-deriving it.

**Pure market-knowledge rows** (no repo touchpoint, `CAPABILITY_NOT_
IMPLEMENTED`): GMD-18 (Artist Hospitality), GMD-20 (International
Festival & Tour Development).

## Objectives

Teach the real, standard live-events/festival-industry professional
disciplines this cluster covers, as market-general knowledge, citing
the real Good Mood OS platform where a worked example exists:

- Festival/event production and promotion.
- Ticketing operations, sales/revenue management, sponsorship.
- Festival marketing, CRM, merchandising, content/media operations.
- Data & analytics, finance (real Stripe integration as worked
  example), safety/access management, multilingual operations,
  reporting.
- Artist hospitality and international/tour development
  (market-general, no repo touchpoint).

## Modules

1. Festival/event production and promotion fundamentals.
2. Ticketing operations and sales/revenue management — worked example:
   `docs/gmd/gmd24/` (real `TicketType` model, QR generation).
3. CRM and merchandising — worked example: `docs/gmd/gmd26/`/`gmd27/`.
4. Content/media operations, data & analytics — worked example:
   `docs/gmd/gmd30/` (real event-report endpoint).
5. Finance — worked example: `docs/gmd/gmd28/` (real Stripe checkout +
   webhook).
6. Safety/access management — worked example: `docs/gmd/gmd25/` (real
   door-scan).
7. Multilingual operations — worked example: `docs/gmd/gmd29/` (real
   bilingual newsletter copy).
8. Artist hospitality, international/tour development — pure
   market-general knowledge, no repo touchpoint, never claimed as a
   Good Mood capability.
9. Boundary discipline — never claims the real Good Mood OS platform
   (`gmfest972/goodmooddjsayd`) implements a capability beyond what
   `docs/gmd/gmd2x/` already documents; never re-derives the internal-
   operator layer's own content, only cites it as a worked example.

## Assessment

A discipline-literacy exam graded against real festival/live-events
industry practice, with an eliminatory check on claiming a Good Mood
platform capability beyond what the real internal-operator layer
(`GMD-21→33`) already documents.

## Status

`STATUS = MODULE_CONTENT_DRAFTED` for 17/20 rows (this combined
referential). **3 rows deepened to individual full canonical packages
as flagships of this cluster (task #184, 2026-09-08):** `gmd05/`
(Ticketing Operations, citing GMD-24), `gmd14/` (Finance, citing
GMD-28's real Stripe integration), `gmd15/` (Safety/Access, citing
GMD-25). These 3 were chosen as the best-grounded rows with a
distinct, real, non-duplicative worked-example touchpoint. The
remaining 17 rows stay at this combined `MODULE_CONTENT_DRAFTED`
depth — an honest intermediate state for market-general content
without a unique per-row repo touchpoint, never deepened by
fabricating a repo-truth that doesn't exist.

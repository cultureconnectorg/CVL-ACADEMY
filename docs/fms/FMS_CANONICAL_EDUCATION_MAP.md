# FMS-07→18 — Canonical Education Map

## Shared competency skeleton

Every FMS-0X formation in this wave follows the same shape:
`PROFESSIONAL_ROLE → ACTIVITIES → COMPETENCIES`, each competency
grounded either in a named route/model in `fms-os/fms/backend/server.py`
(operator-role formations: FMS-07, FMS-15, FMS-18) or in a named,
by-reference module of the Founder-gated FMS-01→06 canon
(specialization/hybrid formations: FMS-08, FMS-09, FMS-11) or in
general, industry-standard professional practice with no repo to cite
(genuinely new external professions: FMS-10, FMS-12, FMS-13).

## Dependency graph

```
FMS-01→06 (Founder-gated canon, cited by reference only)
  ├── FMS-08 (Recording Engineering — anchored on FMS-03/M06,M11)
  ├── FMS-09 (Mixing & Mastering — anchored on FMS-03/M07,M12,M14)
  └── FMS-11 (Creative Direction & Visual Production — anchored on
        FMS-04/M04,M09, extended beyond FMS-04's brand-asset scope)

FMS-07 (Studio Operations & Session Management — umbrella)
  absorbs FMS-14 (Production Coordination, by ref. FMS-05/M05,M10)
  absorbs FMS-16 (Booking & Resource Planning)
  grounded in fms-os/fms: /os/bookings, /os/services

FMS-18 (FMS Ecosystem Operations — internal/cross-métier)
  absorbs FMS-17 (Creative Content & Portfolio Operations, by ref.
    FMS-04 content/campaign blocks)
  grounded in fms-os/fms: /os/command-center, /os/integrations,
    /os/audit-log

FMS-15 (Studio Client & Commercial Operations — standalone)
  grounded in fms-os/fms: /os/clients, /os/leads

FMS-10 (Audiovisual Production — standalone, new)
  cross-references FMS-03 at the audio-mixing boundary only

FMS-12 (Event Creative Direction & Live Production — standalone, new)
  cross-references FMS-11 at their shared boundary, kept SEPARATE

FMS-13 (A&R & Talent Scouting — standalone, new)
  no overlap with FMS-01 (works with an artist who already exists) or
  FMS-05 (does not source new talent)
```

## Boundary notes (mandatory cross-reference discipline)

- **FMS-08 vs FMS-03 "Music Production":** Recording Engineer (signal
  chain, mic technique, tracking sessions) is a distinct professional
  specialization from Music Producer (creative direction of a
  project). FMS-08 never re-teaches FMS-03's generalist producer
  modules — it cites M06/M11 by reference and builds the
  signal-chain-depth material FMS-03 does not cover.
- **FMS-09 vs FMS-03/M14:** FMS-03's own M14 ("Mixage & Mastering
  avancés, production multi-styles") is already framed by the
  canonical corpus itself as an advanced/optional specialization
  module — FMS-09 is that specialization's formal certification track,
  not a duplicate formation.
- **FMS-11 vs FMS-04 "Artist Branding":** FMS-04/M04,M09 teach
  brand-visual-direction inside a branding strategy; FMS-11's scope is
  broader (video/live visual direction, briefing/managing other
  creative specialists) and is explicitly NOT a re-reading of FMS-04 —
  it extends beyond it.
- **FMS-11 vs FMS-10 (Audiovisual Production):** FMS-11 does not
  re-teach audiovisual technique (camera, edit, grade) — that is
  FMS-10's competency territory.
- **FMS-11 vs FMS-12 (Event Creative Direction & Live Production):**
  kept deliberately separate. A Creative Director who also directs a
  live show is the exception, never the assumed default in either
  formation's référentiel without direct evidence from a candidate's
  own portfolio.
- **FMS-14 (merged into FMS-07) vs FMS-05 "Coordination" block:** FMS-05
  teaches artist-career-side coordination (an Artist Manager's duties
  across an artist's whole career); the FMS-07 block teaches
  studio/production-project-side coordination (one recording project,
  liaising engineers/artists/label for that project only) — reuses
  FMS-05's transferable coordination pedagogy by reference, adds
  session budget tracking, cross-department liaison, deliverable
  tracking as the studio-side-specific additions.
- **FMS-17 (merged into FMS-18) vs FMS-04 content/campaign blocks:**
  FMS-18's content-ops block reuses FMS-04's content/campaign literacy
  by reference; it does not re-teach campaign design craft — it
  teaches operating a portfolio of creative assets across projects
  (digital-asset/content-ops function), a different competency.
- **FMS-18's own `/os/command-center` route vs CVLN's ecosystem
  "Command Center"/"CVL Brain":** unrelated systems that happen to
  share a name — `fms-os/fms`'s command-center is a studio-operations
  KPI dashboard (projects/artists/clients/leads/bookings counts); CVLN's
  ecosystem Command Center (referenced elsewhere in this Master
  Package, e.g. the Agent Factory cluster) is a different system
  entirely. Never merged, per the standing cross-domain-contamination
  guard already recorded in `REPO_REGISTRY.md`.

## Anti-footprint verification (mandatory before certifying any FMS-0X)

Before crediting a candidate with any FMS-07/15/18 competency, verify
the claimed capability against the actual route/model cited in the
corresponding `REFERENTIAL.md` — never against a memorized summary of
"what a studio-ops tool would probably have." `fms-os/fms`'s own
`command_center` endpoint is the canonical example of why this
matters: its `revenue_mtd` KPI explicitly returns
`{"value": None, "source": "INSUFFICIENT_DATA"}` in the real code —
a candidate is certified on recognizing and escalating that gap, never
on an assumed working revenue dashboard.

## Certification / mission eligibility doctrine

Same N1/N2/assessment structure as `CERTIFICATION_MODEL.md`. Mission
eligibility for FMS-07/15/18 (operator roles) requires literacy of the
real `fms-os/fms` data model and workflow — never live operational
credentials to that system in production. FMS-08/09/11 mission
eligibility (freelance recording/mixing/mastering gigs, creative
direction briefs) is granted on the specialization assessment alone,
independent of the base FMS-03/FMS-04 certification.

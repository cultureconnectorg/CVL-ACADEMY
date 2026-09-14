# FMS-07→18 — Reconciliation Against Existing Canonical Corpus (v2 — occupational distinctness)

```
RULE APPLIED: UPGRADE_EXISTING = TRUE, REBUILD_FROM_ZERO = FALSE, and
the correction: CONTENT_OVERLAP != PROFESSIONAL_DUPLICATE. Every
candidate evaluated on TWO independent dimensions (curriculum coverage
+ occupational distinctness) before any action is decided — never
rejected on curriculum overlap alone. Supersedes v1 of this document
(which stopped at curriculum coverage only and wrongly treated 3
candidates as flat duplicates).

IMPORTANT BOUNDARY (unchanged from v1): the canonical FMS-01→06 corpus
itself is under a prior Founder gate (docs/ACADEMY_FMS_CANONICAL_
DELTA_MATRIX.md, G2/G3=NOT_AUTHORIZED, STOP_AFTER_DELIVERY=TRUE). This
document reads it read-only and never reopens that gate. Existing
modules are REUSED BY REFERENCE, never re-authored.
```

## Method — 9 checks per candidate

1. Repo capability check (`fms-os/fms`, this repo)
2. Existing curriculum check (FMS-01→06, 95 modules)
3. Competency overlap check (which modules, how much)
4. Occupational distinctness check (is this a real, separately-named
   professional identity in the industry — specialization, distinct
   profession, internal/operator role, or cross-ecosystem role?)
5. Internal role check
6. Operator role check
7. Authorization check
8. Cross-ecosystem check
9. Mission/applied-work check

## Canonical FMS-01→06 — verified block structure (unchanged reference)

| Métier | Blocs de compétence | Modules |
|---|---|---|
| FMS-01 Artist Development | Diagnostic · Identité & Univers · Positionnement · Storytelling · Roadmap | 15 |
| FMS-02 Music Business | Analyse marché · Droits & Contrats · Business Model · Distribution · Structuration juridique | 16 |
| FMS-03 Music Production | DAW/composition/arrangement · Production sonore · Enregistrement & Édition · **Mixage & Mastering** | 16 |
| FMS-04 Artist Branding | Brand Platform · **Direction visuelle** · Stratégie éditoriale · Réseaux sociaux · Campagnes | 16 |
| FMS-05 Artist Management | Planning · Négociation · **Coordination** · Budget · Arbitrage | 16 |
| FMS-06 Executive/Cultural Production | Conception de projet · Financement · Gouvernance · Risques · Portefeuille | 16 |

## Per-candidate reconciliation (corrected)

### FMS-07 — Studio Operations & Session Management
- **Curriculum coverage**: `NONE`. **Occupational distinctness**:
  `DISTINCT_PROFESSION` — studio operations/session management is a
  recognized, separately-employed role (studio manager) distinct from
  every one of the 6 creative métiers. Grounded in `fms-os/fms`
  (`/os/bookings`, `/os/services`).
- **Action**: `NEW_EXTERNAL`. Becomes the umbrella formation absorbing
  the studio-operations-adjacent candidates below (see FMS-14, FMS-16)
  as competency blocks rather than three separate thin formations —
  this is a `MERGE`-into-blocks decision, not a rejection of FMS-14/16
  as professions.

### FMS-08 — Recording Engineering
- **Curriculum coverage**: `SUBSTANTIAL` (FMS-03/M06 "Enregistrement &
  Édition encadrés", M11 "sous pression").
- **Occupational distinctness**: `DISTINCT_SPECIALIZATION` — in real
  studio practice, "Recording Engineer" (signal chain, mic technique,
  tracking sessions) is a distinct professional specialization from
  "Music Producer" (creative direction of a project); many working
  producers are not skilled recording engineers and vice versa.
- **Action**: `SPECIALIZE_EXISTING`. Build a Recording Engineering
  specialization path anchored on FMS-03/M06,M11 **by reference**
  (never re-authored), adding what a working recording engineer needs
  beyond the generalist producer module: signal-chain depth, mic
  technique library, session-under-real-constraints assessment,
  dedicated competency profile and Skill IDs for the "Recording
  Engineer" role.

### FMS-09 — Mixing & Mastering
- **Curriculum coverage**: `COMPLETE` (FMS-03/M07 encadré, M12 sous
  pression, **M14 avancé/optionnel — already framed by the canonical
  corpus itself as an advanced specialization module**).
- **Occupational distinctness**: `DISTINCT_PROFESSION` — Mixing
  Engineer and Mastering Engineer are long-established, frequently
  fully independent careers in the real industry (freelance mastering
  houses, dedicated mix engineers who never produce), not a mere
  deeper reading of Music Production.
- **Action**: `SPECIALIZE_EXISTING` — **not** a duplicate, **not** a
  fresh 15-module formation either. FMS-03/M14 ("Mixage & Mastering
  avancés, production multi-styles") becomes the anchor of a formal
  Mixing & Mastering specialization/certification track: reuse
  M07/M12/M14 by reference, add a dedicated specialization assessment
  (own A0x-spec, own rubric), a distinct competency profile and Skill
  IDs for "Mixing Engineer"/"Mastering Engineer", and mission/role
  eligibility (freelance mixing gigs, mastering-for-hire) that a
  generic Music Production certification does not confer today. This
  corrects v1, which wrongly rejected this as `CANDIDATE_NOT_JUSTIFIED`.

### FMS-10 — Audiovisual Production
- **Curriculum coverage**: `NONE` (FMS-03 is audio-only).
- **Occupational distinctness**: `DISTINCT_PROFESSION`.
- **Action**: `NEW_EXTERNAL`. Cross-reference FMS-03 explicitly at the
  audio-mixing boundary to avoid re-teaching audio inside it.

### FMS-11 — Creative Direction & Visual Production
- **Curriculum coverage**: `SUBSTANTIAL` for the brand-visual slice
  (FMS-04/M04 "Direction visuelle encadrée", M09 "défendue") — but the
  candidate's scope is **broader** than FMS-04's brand-asset framing:
  it extends into video/live visual direction, which FMS-04 does not
  cover and which touches FMS-10/FMS-12 territory.
- **Occupational distinctness**: `DISTINCT_PROFESSION` when scoped at
  its full breadth (a Creative Director bridging brand, video, and
  campaign visuals is a recognized, separately-titled role distinct
  from "Artist Branding specialist," who owns positioning/identity
  more than visual execution across media).
- **Action**: `EXTEND_EXISTING` + `NEW_EXTERNAL` (hybrid): reuse
  FMS-04/M04,M09 by reference for the brand-visual-direction
  foundation, then build the genuinely new material this candidate
  adds beyond FMS-04's scope (directing visuals across video/campaign
  media, briefing/managing other creative specialists). Explicitly
  cross-referenced with FMS-10 (does not re-teach audiovisual
  technique) and FMS-12 (does not re-teach live/event staging). This
  corrects v1, which wrongly rejected this as a duplicate of FMS-04
  alone.

### FMS-12 — Event Creative Direction & Live Production
- **Curriculum coverage**: `NONE`.
- **Occupational distinctness**: `DISTINCT_SPECIALIZATION` relative to
  FMS-11 — live/event show direction (staging, lighting, live visual
  cues) is recognized as related to but distinct from brand/video
  creative direction; some professionals cross over, many do not.
- **Action**: `NEW_EXTERNAL`, kept **separate** from FMS-11 (not
  merged) but required to cross-reference it explicitly at their
  shared boundary (a Creative Director who also directs a live show is
  the exception, not the assumed default — never assumed without
  evidence in either formation's referential).

### FMS-13 — A&R & Talent Scouting
- **Curriculum coverage**: `NONE` (FMS-01 works with an artist who
  already exists; FMS-05 does not source new talent).
- **Occupational distinctness**: `DISTINCT_PROFESSION`.
- **Action**: `NEW_EXTERNAL`. Unchanged from v1.

### FMS-14 — Artist Project & Production Coordination
- **Curriculum coverage**: `SUBSTANTIAL` (FMS-05 Coordination block,
  M05/M10) — but that block teaches **artist-career-side** coordination
  (an Artist Manager's coordination duties across an artist's career),
  not **studio/production-project-side** coordination (a Production
  Coordinator scheduling and tracking a specific recording project,
  liaising engineers/artists/label for that project only).
- **Occupational distinctness**: `DISTINCT_OPERATOR_ROLE` — Production
  Coordinator is a recognized, separately-employed studio-side role,
  distinct from Artist Manager even though both coordinate.
- **Action**: `EXTEND_EXISTING` — **merged into FMS-07** (Studio
  Operations & Session Management) as a competency block, reusing
  FMS-05's transferable coordination pedagogy **by reference**, adding
  the studio/production-project-specific competencies (session budget
  tracking, cross-department liaison for one production, deliverable
  tracking) FMS-05 does not cover. This corrects v1, which wrongly
  rejected this as a duplicate of FMS-05 with no further action.

### FMS-15 — Studio Client & Commercial Operations
- **Curriculum coverage**: `NONE`. **Occupational distinctness**:
  `DISTINCT_PROFESSION` (studio sales/commercial ops). Grounded in
  `fms-os/fms` (`/os/clients`, `/os/leads`).
- **Action**: `NEW_EXTERNAL`. Unchanged from v1.

### FMS-16 — Booking, Resource & Studio Planning
- **Curriculum coverage**: `NONE`.
- **Occupational distinctness**: `DISTINCT_OPERATOR_ROLE`, but in real
  small/mid studio operations this role and Session Management
  (FMS-07) are frequently the same person — `fms-os/fms` itself serves
  both bookings and session-adjacent services from one `/os` layer.
- **Action**: `MERGE` into FMS-07 as a competency block (Booking &
  Resource Planning), not a 13th separate formation. Larger operations
  where this genuinely splits into a dedicated scheduler role are
  served by an internal specialization/operator path within FMS-07,
  not a parallel external formation.

### FMS-17 — Creative Content & Portfolio Operations
- **Curriculum coverage**: `PARTIAL` (overlaps FMS-04 campaign/content
  blocks for the content-creation side).
- **Occupational distinctness**: `DISTINCT_OPERATOR_ROLE` — managing a
  portfolio of creative assets/content operationally across projects
  is closer to a digital-asset/content-ops function than a campaign
  design craft.
- **Action**: `EXTEND_EXISTING` — folded into FMS-18 (FMS Ecosystem
  Operations, internal) as an operator role/block, reusing FMS-04's
  content/campaign literacy by reference rather than rebuilt as a
  separate external formation.

### FMS-18 — FMS Ecosystem Operations
- **Curriculum coverage**: `NONE`. **Occupational distinctness**:
  `DISTINCT_INTERNAL_ROLE`/`CROSS_ECOSYSTEM_ROLE` — grounded in
  `fms-os/fms`'s own `/os` layer (command-center, integrations,
  audit-log), a real, distinct internal/cross-métier operations layer.
- **Action**: `NEW_INTERNAL`, `context=INTERNAL`. Absorbs FMS-17 as a
  block (above).

## Corrected summary

| Verdict | Candidates |
|---|---|
| `NEW_EXTERNAL` (standalone) | FMS-10, FMS-12, FMS-13, FMS-15 |
| `NEW_EXTERNAL` (hybrid, extends FMS-04 by reference) | FMS-11 |
| `NEW_INTERNAL` | FMS-18 (absorbs FMS-17 as a block) |
| `SPECIALIZE_EXISTING` (anchored on existing modules, own certification track) | FMS-08 (→ FMS-03), FMS-09 (→ FMS-03/M14) |
| `EXTEND_EXISTING` / `MERGE` into FMS-07 as competency blocks | FMS-14, FMS-16 |
| `EXTEND_EXISTING` / `MERGE` into FMS-18 as a block | FMS-17 |
| `REJECT_TRUE_DUPLICATE` | **none** — v1's 3 rejections were wrong; corrected here |

**Result: 12/12 candidates carry real professional weight.** None are
discarded. What changes from a naive read of the spreadsheet: FMS-14
and FMS-16 become blocks of FMS-07 rather than standalone formations
(3→1), and FMS-17 becomes a block of FMS-18 rather than standalone
(1→0 as external) — so the portfolio lands at **9 formations/paths**
covering all 12 candidates faithfully: FMS-07 (absorbing 14, 16),
FMS-08 (specialization), FMS-09 (specialization), FMS-10, FMS-11
(hybrid), FMS-12, FMS-13, FMS-15, FMS-18 (absorbing 17) — richer than
either "build all 12 separately" (inflated) or v1's "reject 5"
(under-counted real professions).

## Status

`STATUS = RECONCILED_V2`. Still `RECONCILED_NOT_BUILT` — no W6
référentiel written yet. Next action for this domain: W4 (competency
map) on the 9 confirmed paths above, in the order FMS-07 (umbrella,
unblocks 14/16) → FMS-18 (unblocks 17) → FMS-08/09 (specializations,
fastest to build given canonical anchor already exists) → FMS-10/11/
12/13/15 (genuinely new content).

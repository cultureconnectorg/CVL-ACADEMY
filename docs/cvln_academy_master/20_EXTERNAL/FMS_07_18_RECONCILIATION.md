# FMS-07→18 — Reconciliation Against Existing Canonical Corpus

```
RULE APPLIED: UPGRADE_EXISTING = TRUE, REBUILD_FROM_ZERO = FALSE
(Founder directive). Every Master 2D FMS-07→18 candidate classified
against the REAL canonical FMS-01→06 corpus (95 modules, 6 métiers,
extracted from FMS_Chantier_Complet_20260822.zip — the same archive
already analyzed in docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md) and
against fms-os/fms (real business platform, cloned this session).

IMPORTANT BOUNDARY: the canonical FMS-01→06 corpus itself is under a
prior Founder gate — docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md records
G2=NOT_AUTHORIZED, G3=NOT_AUTHORIZED, STOP_AFTER_DELIVERY=TRUE for its
integration/mutation. This document does NOT touch that corpus, its
runtime binding, or reopen that gate — it only reads it (read-only) to
classify NEW Master 2D candidates against it. No FMS-01→06 file is
modified by this document.
```

## Canonical FMS-01→06 — verified block structure (for reference)

| Métier | Blocs de compétence (A→E) | Modules |
|---|---|---|
| FMS-01 Artist Development | Diagnostic artistique · Identité & Univers · Positionnement stratégique · Storytelling · Roadmap & Trajectoire | 15 |
| FMS-02 Music Business | Analyse économique & marché · Droits & Contrats · Business Model & Financement · Distribution & Stratégie de sortie · Structuration juridique | 16 |
| FMS-03 Music Production | (DAW/composition/arrangement) · Production sonore · Enregistrement & Édition · **Mixage & Mastering** | 16 |
| FMS-04 Artist Branding | Réception identité & Brand Platform · **Direction visuelle** · Stratégie éditoriale · Réseaux sociaux · Campagnes | 16 |
| FMS-05 Artist Management | Réception du cadre & Planning · Négociation opérationnelle · **Coordination** · Budget opérationnel · Arbitrage d'opportunités | 16 |
| FMS-06 Executive/Cultural Production | Conception de projet · Financement · Gouvernance · Gestion des risques · Arbitrage de portefeuille | 16 |

None of the six métiers has a block for: studio/session logistics,
talent scouting/A&R sourcing, business/commercial operations (clients,
leads, quoting), booking/resource planning, or a cross-métier
"ecosystem operations" layer. This bounds what genuinely counts as
`NEW_GAP` below.

## Classification per candidate (9-way framework)

| Candidate | Classification | Decision |
|---|---|---|
| **FMS-07** Studio Operations & Session Management | `NEW_GAP` | No canonical block covers studio/session logistics. Grounded in `fms-os/fms` (`/os/bookings`, `/os/services`). **CREATE NEW**, positioned as a distinct operational métier (not a specialization of any of the 6 creative métiers). |
| **FMS-08** Recording Engineering | `ALREADY_EXISTS_PARTIAL` — **FMS-03/M06 "Enregistrement & Édition encadrés"** (+ M11 "sous pression") already teaches this. | **DO NOT CREATE.** If a deeper standalone track is wanted, it is a **SPECIALIZE** extension of FMS-03 (an optional advanced module, same pattern as FMS-03/M14 "Mixage & Mastering avancés"), not a new formation. |
| **FMS-09** Mixing & Mastering | `ALREADY_EXISTS_COMPLETE` — **FMS-03/M07, M12, M14** already cover this end-to-end (encadré → sous pression → avancé/optionnel). | **DO NOT CREATE.** Zero justification for a parallel formation — this is the clearest `CANDIDATE_NOT_JUSTIFIED` in the batch. |
| **FMS-10** Audiovisual Production | `NEW_GAP` (partial) | FMS-03 is music-only (audio). Audiovisual/video production is a distinct craft. **CREATE NEW**, but cross-reference FMS-03 explicitly to avoid re-teaching audio mixing inside it (boundary, not duplication). |
| **FMS-11** Creative Direction & Visual Production | `EXISTS_UNDER_ANOTHER_NAME` — **FMS-04/M04 "Direction visuelle encadrée"** (+ M09 "défendue"). | **DO NOT CREATE** as a separate formation. If a cross-métier "creative direction" role is genuinely distinct from Artist Branding's visual direction (e.g., direction for live events, not just brand assets), that is an **ADD BRIDGE** or **ADD INTERNAL/CROSS-ECOSYSTEM MODULE** onto FMS-04, not a new métier. |
| **FMS-12** Event Creative Direction & Live Production | `NEW_GAP` (narrow) | Live/event creative direction is not covered by FMS-04 (brand assets) nor FMS-05 (management/logistics). Genuine gap, but **narrow** — likely a specialization module rather than a full 15-16-module formation. **CREATE NEW at reduced scope**, or fold into FMS-10 (Audiovisual Production) as a live-production block — decision needed at W4 (competency map), not here. |
| **FMS-13** A&R & Talent Scouting | `NEW_GAP` (confirmed) | Neither FMS-01 (works with an artist who already exists) nor FMS-05 covers sourcing/discovering new talent. **CREATE NEW.** |
| **FMS-14** Artist Project & Production Coordination | `EXISTS_UNDER_ANOTHER_NAME` — **FMS-05 Artist Management** (Coordination block, M05/M10) already covers this. | **DO NOT CREATE** as a duplicate. If "production coordination" is meaningfully distinct from "artist management" (e.g., studio-side production scheduling vs artist-side career coordination), that is an **ADD INTERNAL OPERATOR PATH** onto FMS-07 (Studio Operations) or a **SPECIALIZE** of FMS-05 — needs a W3 boundary ticket, not a new formation by default. |
| **FMS-15** Studio Client & Commercial Operations | `NEW_GAP` | No canonical métier covers client/lead/commercial ops. Grounded in `fms-os/fms` (`/os/clients`, `/os/leads`). **CREATE NEW.** |
| **FMS-16** Booking, Resource & Studio Planning | `NEW_GAP` | Grounded in `fms-os/fms` (`/os/bookings`, `/os/services`). **CREATE NEW**, likely merged with FMS-07 (Studio Operations) rather than a 13th separate formation — both are studio-logistics-shaped. Decision needed at W4. |
| **FMS-17** Creative Content & Portfolio Operations | `EXISTS_UNDER_ANOTHER_NAME` (partial) — overlaps FMS-04's campaign/content blocks. | Needs a closer W3 boundary check before deciding CREATE vs EXTEND — provisionally `ALREADY_EXISTS_PARTIAL`. |
| **FMS-18** FMS Ecosystem Operations | `NEW_GAP` | Grounded in `fms-os/fms`'s own `/os` layer (command-center, integrations, audit-log) — a real, distinct internal/cross-métier operations layer none of the 6 creative métiers cover. **CREATE NEW**, `context=INTERNAL` (this is CVLN's own FMS platform operations, not a market-transferable craft). |

## Summary

| Verdict | Count | Candidates |
|---|---|---|
| `CREATE NEW` (confirmed) | 5 | FMS-07, FMS-10, FMS-13, FMS-15, FMS-18 |
| `CREATE NEW` (narrow/needs scoping) | 1 | FMS-12 |
| `EXISTS_UNDER_ANOTHER_NAME` / `DO NOT CREATE` | 3 | FMS-09, FMS-11, FMS-14 |
| `ALREADY_EXISTS_PARTIAL` (specialize instead) | 2 | FMS-08, FMS-17 |
| `NEW_GAP`, merge candidate | 1 | FMS-16 (likely merges into FMS-07) |

**Result: at most 6-7 genuinely new FMS formations (not 12).** Building
all 12 candidates as separate formations would have produced 3
duplicate formations (FMS-09, FMS-11, FMS-14) directly re-teaching
already-canonical FMS-03/FMS-04/FMS-05 content — exactly the mistake
the Founder's upgrade-not-rebuild rule exists to prevent.

## Status

`STATUS = RECONCILED_NOT_BUILT`. This document changes no runtime
behavior and creates no new referential/module content — it is the
required W3 boundary-check gate that must pass before any FMS-07→18
`W6 (référentiel)` work begins. Per `00_GOVERNANCE/BUILD_METHOD.md`,
the next action for this domain is W4 (competency map) on the 6-7
confirmed `NEW_GAP` items only.

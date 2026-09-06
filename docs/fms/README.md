# docs/fms/ — FMS-07→18 Pedagogical Corpus (W6 Wave)

```
Domain: Factory Maker Studio — extended professions (FMS-07→18)
Reconciliation source: docs/cvln_academy_master/20_EXTERNAL/
                        FMS_07_18_RECONCILIATION.md (v2, corrected)
Repo grounding: fms-os/fms (real, audited — see REPO_REGISTRY.md),
                cloned/read directly this session at
                /home/user/fms-os/fms/backend/server.py
Founder gate: the canonical FMS-01→06 corpus itself
              (docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md) stays
              G2/G3=NOT_AUTHORIZED, STOP_AFTER_DELIVERY=TRUE — this
              corpus reuses FMS-01→06 modules BY REFERENCE only,
              never re-authors them.
```

## Why this corpus exists

`FMS_07_18_RECONCILIATION.md` (v2) evaluated 12 spreadsheet candidates
on two independent dimensions — curriculum coverage AND occupational
distinctness — and found all 12 carry real professional weight, none
rejected. Two merge decisions collapse 12 candidates into **9
formations/paths**:

- **FMS-14** (Artist Project & Production Coordination) and **FMS-16**
  (Booking, Resource & Studio Planning) merge into **FMS-07** as
  competency blocks (not standalone formations) — `fms-os/fms` itself
  serves bookings and session-adjacent services from one `/os` layer,
  matching the real-world pattern where these are the same person in
  small/mid studio operations.
- **FMS-17** (Creative Content & Portfolio Operations) merges into
  **FMS-18** (FMS Ecosystem Operations) as an operator block.

The remaining 7 stand alone: FMS-08/FMS-09 are `SPECIALIZE_EXISTING`
tracks anchored on the already-built, Founder-gated FMS-03 (reused by
reference, never re-authored); FMS-10/11/12/13/15 are genuinely new
external professions.

## Repo-truth table

| Formation | Real grounding | Cited routes/models (`fms-os/fms/backend/server.py`) |
|---|---|---|
| FMS-07 (absorbs FMS-14, FMS-16) | `fms-os/fms` `/os` layer | `GET/POST /os/bookings`, `PATCH /os/bookings/{id}/status`, `GET/POST /os/services`, `ClientCreate`/`BookingCreate`/`ServiceCreate` models |
| FMS-08 | FMS-03 (Founder-gated canon, by reference) | FMS-03/M06 "Enregistrement & Édition encadrés", M11 "sous pression" |
| FMS-09 | FMS-03 (Founder-gated canon, by reference) | FMS-03/M07 encadré, M12 sous pression, **M14 avancé/optionnel** (already framed by the canonical corpus itself as a specialization module) |
| FMS-10 | none (genuinely new professional domain) | cross-references FMS-03 at the audio-mixing boundary only |
| FMS-11 | FMS-04 (by reference, hybrid) | FMS-04/M04 "Direction visuelle encadrée", M09 "défendue" — extended beyond FMS-04's brand-asset scope |
| FMS-12 | none | cross-references FMS-11 at their shared boundary |
| FMS-13 | none | — |
| FMS-15 | `fms-os/fms` `/os` layer | `GET/POST /os/clients`, `GET /os/leads`, `LeadCreate`/`ClientCreate` models |
| FMS-18 (absorbs FMS-17) | `fms-os/fms` `/os` layer | `GET /os/command-center`, `GET/POST /os/integrations`, `POST /os/integrations/{key}/test`, `GET /os/audit-log`, `ECOSYSTEM_INTEGRATIONS` registry, `IntegrationConfigUpdate` model |

**Cross-domain contamination guard (already recorded in
`REPO_REGISTRY.md`):** `fms-os/fms`'s own `/os/command-center` route is
a studio-operations KPI dashboard, unrelated to CVLN's own "Command
Center"/"CVL Brain" ecosystem systems referenced elsewhere in this
Master Package — never conflated, even though both use the words
"command center."

## Status (this wave)

| Formation | Status |
|---|---|
| FMS-07 | `PACKAGE_COMPLETE` — flagship, deepened this wave (référentiel + N1/N2 + assessment/rubric + evidence model + 3 guides + integration note) |
| FMS-08, FMS-09, FMS-10, FMS-11, FMS-12, FMS-13, FMS-15, FMS-18 | `MODULE_CONTENT_DRAFTED` — full référentiel (professional role, activities, competencies, modules, assessment sketch, grounding) written; N1/N2 banks and full guide set not yet built |

**1/9 `PACKAGE_COMPLETE`, 8/9 `MODULE_CONTENT_DRAFTED`, 0/9
`BLOCKED`.** No formation in this wave is blocked — the two candidates
originally flagged as repo-dependent (FMS-07, FMS-15/18) all confirm
real capability in `fms-os/fms`, directly re-read this session, never
cited from memory.

## What this corpus does NOT do

- Does not reopen, re-author, or duplicate a single module of the
  Founder-gated FMS-01→06 canon — FMS-08/09/11 cite it by reference
  only (module number + what it teaches), never reproduce its content.
- Does not claim `FULLY_COMPLETE` for any formation — no candidate has
  sat a real assessment under this corpus yet.
- Does not grant live operational access to `fms-os/fms` in production
  — certification is on literacy of the real system's data model and
  workflow, not operational credentials.
- Does not invent capability: where `fms-os/fms` genuinely lacks
  something (e.g. no real payment/invoicing — `command_center`'s own
  `revenue_mtd` KPI reports `"source": "INSUFFICIENT_DATA"` verbatim in
  its code), the corresponding competency is framed around reading and
  escalating that gap, never around a fabricated feature.

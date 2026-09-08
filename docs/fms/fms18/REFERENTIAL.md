# FMS-18 — FMS Ecosystem Operations (absorbs FMS-17, internal)

## Repo truth this formation is built on

Grounded directly in the real, audited `fms-os/fms` (re-read this
session, `backend/server.py`):
- `GET /os/command-center` — aggregate studio-ops KPIs
  (`projects_active`, `projects_total`, `artists_total`,
  `artists_dev`, `clients_total`, `leads_new`, `bookings_upcoming`,
  each with a stated `source`/`formula`, and `revenue_mtd` explicitly
  `{"value": None, "source": "INSUFFICIENT_DATA"}`).
- `GET/POST /os/integrations`, `POST /os/integrations/{key}/test` —
  the real `ECOSYSTEM_INTEGRATIONS` registry (7 named CVLN ecosystem
  adapters: Frek-ID, FREKCORE, FREKANSLA, KORA, CVLN Wallet, CVL Brain,
  Laurentia — every one explicitly `"status": "NOT_CONNECTED"` in the
  real code today), `IntegrationConfigUpdate` model
  (`base_url`/`api_key`/`entity_id`/`auth_type`/`notes`).
- `GET /os/audit-log` — real append-style audit trail
  (`db.audit_log`, sorted by `timestamp`, capped at 500).
- FMS-17's content/portfolio-ops competency absorbed as a block, by
  reference to FMS-04's content/campaign blocks (per
  `FMS_07_18_RECONCILIATION.md`'s own merge verdict).

Per that reconciliation: FMS-18's own curriculum coverage `NONE`,
occupational distinctness `DISTINCT_INTERNAL_ROLE`/
`CROSS_ECOSYSTEM_ROLE`, action `NEW_INTERNAL`, `context=INTERNAL`.

## Cross-domain contamination guard

`fms-os/fms`'s `/os/command-center` is a **studio-operations** KPI
dashboard, unrelated to CVLN's own ecosystem "Command Center"/"CVL
Brain" systems referenced elsewhere in this Master Package (e.g. the
Agent Factory cluster) — two different systems that happen to share a
name. Never merged, per the standing guard already recorded in
`REPO_REGISTRY.md`.

## Prerequisites

FMS-07 literacy recommended (same `/os` layer), not strictly required.

## Objectives

FMS Ecosystem Operations is the internal/cross-métier operations layer
of a Factory Maker Studio-type operation — running the studio's own
command-center reporting, managing its ecosystem-integration
configuration, and maintaining audit-trail discipline, plus (absorbed
from FMS-17) operating its portfolio of creative content/assets across
projects:

- Command-center KPI literacy: reading real aggregate metrics and
  their stated formulas, distinguishing a populated metric from one
  explicitly marked `INSUFFICIENT_DATA`.
- Ecosystem-integration operations: managing the real
  `ECOSYSTEM_INTEGRATIONS` registry — recognizing `NOT_CONNECTED`
  status honestly, configuring connection parameters
  (`base_url`/`api_key`/`entity_id`/`auth_type`) without ever claiming
  a connection is live when the record says otherwise.
- Audit-log discipline: reading and using the real `/os/audit-log`
  trail for operational accountability.
- Content/portfolio operations (absorbed FMS-17 block): operating a
  portfolio of creative content/assets across projects, by reference
  to FMS-04's content/campaign literacy — a digital-asset/content-ops
  function, not a campaign-design craft.

## Modules

1. **Command-center KPI literacy** — grounded in the real
   `command_center` payload shape, including its honest
   `INSUFFICIENT_DATA` reporting.
2. **Ecosystem-integration operations** — grounded in the real
   `ECOSYSTEM_INTEGRATIONS` registry and `IntegrationConfigUpdate`
   model; explicit discipline against ever claiming `NOT_CONNECTED`
   integrations as live.
3. **Audit-log & accountability discipline** — grounded in the real
   `/os/audit-log` endpoint.
4. **Content/portfolio operations block (absorbed FMS-17)** — by
   reference to FMS-04's content/campaign blocks; operating a content
   portfolio across projects rather than designing individual
   campaigns.

## Assessment

An ecosystem-operations review: candidate is given a representative
`command_center`/`integrations`/`audit-log` payload set and must
produce an operational report distinguishing live data from
`INSUFFICIENT_DATA`/`NOT_CONNECTED` fields, plus a content-portfolio
operations note (FMS-17 block) — graded against the real data model,
never an invented "fully connected ecosystem" state.

## Evidence / certification / mission eligibility

`FMS18.SKILL.*` Skill IDs, reserved once this formation is deepened to
full package. Mission eligibility requires literacy of the real
`fms-os/fms` `/os` layer — never live production write access to that
system, and never a claim that any of the 7 ecosystem integrations are
connected when the real registry says `NOT_CONNECTED`.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`, deepened this pass, grounded
in the real `fms-os/fms` command-center/integrations/audit-log
layer. **This closes task #187: all 9/9 FMS-07→18 formations are now
at full canonical package depth.** Not yet delivered to a real
candidate — `FULLY_COMPLETE` still requires that verification, per
`../QUALITY_GATES.md`.

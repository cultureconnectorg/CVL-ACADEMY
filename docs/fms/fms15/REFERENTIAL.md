# FMS-15 — Studio Client & Commercial Operations

## Repo truth this formation is built on

Grounded directly in the real, audited `fms-os/fms` (re-read this
session, `backend/server.py`):
- `GET /os/clients`, `POST /os/clients` — `ClientCreate` model:
  `name`, `email`, `phone`, `company`, `type` (default `"individual"`),
  `status` (`lead`, `qualified`, `prospect`, `client`, `repeat_client`,
  `vip`).
- `GET /os/leads` (populated via the public `POST /public/leads` —
  `LeadCreate` model: `name`, `email`, `phone`, `company`,
  `project_type`, `objective`, `description`, `budget_range`,
  `timeline`).

Per `FMS_07_18_RECONCILIATION.md`'s own verdict: curriculum coverage
`NONE`, occupational distinctness `DISTINCT_PROFESSION` (studio
sales/commercial ops), action `NEW_EXTERNAL`.

## Prerequisites

None (standalone external formation, though FMS-07 literacy is
recommended context since both operate against the same `fms-os/fms`
`/os` layer).

## Objectives

Studio commercial operations — converting inbound leads into clients,
managing the client relationship lifecycle (`lead → qualified →
prospect → client → repeat_client → vip`) — is a distinct professional
function from creative/production work, grounded in the real client/
lead data model:

- Lead qualification literacy: reading a real lead's fields
  (`project_type`, `objective`, `budget_range`, `timeline`) to decide
  qualification, not guessing at unstated criteria.
- Client lifecycle management: recognizing and progressing a client
  through the real `status` field's 6 stages, and what commercial
  action each transition implies.
- Commercial reporting discipline: reading the real
  `command_center`'s `clients_total`/`leads_new` KPIs (and their stated
  `source`/`formula`) rather than an invented commercial dashboard.

## Modules

1. **Lead qualification** — grounded in `LeadCreate`'s real fields;
   qualifying a lead against stated project_type/objective/budget/
   timeline data.
2. **Client lifecycle management** — grounded in `ClientCreate`'s real
   `status` enum (`lead`/`qualified`/`prospect`/`client`/
   `repeat_client`/`vip`); what commercial action each transition
   implies.
3. **Commercial reporting discipline** — grounded in `command_center`'s
   real `clients_total`/`leads_new` KPI fields, including recognizing
   when a KPI (e.g. `revenue_mtd`) is explicitly `INSUFFICIENT_DATA`
   rather than assuming it is populated.

## Assessment

A lead-to-client exercise: candidate is given a representative lead
record (real field shape) and must produce a qualification decision,
a client-status progression plan, and a commercial report reading —
graded against the real data model, never an invented CRM feature.

## Evidence / certification / mission eligibility

`FMS15.SKILL.*` Skill IDs, reserved once this formation is deepened to
full package. Mission eligibility requires literacy of the real
`fms-os/fms` client/lead data model — never live production write
access to that system.

## Status

`STATUS = MODULE_CONTENT_DRAFTED` — référentiel and module outline
written this pass; N1/N2 banks, full assessment/rubric, evidence
model, and the 3 guides are a future deepening pass, not performed
here.

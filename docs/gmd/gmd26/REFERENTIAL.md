# GMD-26 — Fan CRM Operator

```
Prerequisite: GMD-21. Fed by GMD-24 (a purchase creates/updates a fan record).
```

## Repo truth

`/admin/fans` route, fan-upsert-on-purchase logic (`server.py:611`
region). This is the operator role for Good Mood's real, minimal fan
database — not a full marketing-CRM product, an upsert table keyed on
purchase activity.

## Prerequisites

GMD-21.

## Objectives

1. Read and interpret the real fan record (what it captures, what it
   does not — no purchase-history analytics beyond what the raw table
   holds).
2. Explain when a fan record is created vs updated (purchase-triggered
   upsert, not manual entry as the primary path).
3. Correctly answer a "how many fans do we have from city X" question
   using only the real fields available, never inventing segments the
   data doesn't support.

## Modules

| # | Module | Deliverable |
|---|---|---|
| M1 | Fan record field literacy | Field table + upsert-trigger note |
| M2 | Fan-record query practice | Written answers to 3 realistic operator questions, each traced to the real field(s) that answer it (or explicitly flagged as unanswerable with current fields) |
| M3 | Data-honesty discipline | Short case: a stakeholder asks for a segment the schema can't produce — the correct answer is "not currently trackable," never a fabricated number |

## Assessment

Per `../CERTIFICATION_MODEL.md`. Graded specifically on M3 — this
formation's core competency is refusing to fabricate data the real
schema doesn't hold, directly mirroring this Master Package's own
`UNPROVEN_FEATURE`/`FAKE_PROOF` discipline applied at the operator
level.

## Evidence / certification / mission eligibility

Same general pattern as GMD-22.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.

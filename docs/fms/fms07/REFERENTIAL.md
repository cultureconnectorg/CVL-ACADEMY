# FMS-07 — Studio Operations & Session Management (umbrella, flagship)

## Repo truth this formation is built on

Grounded directly in the real, audited `fms-os/fms` (re-read this
session, `backend/server.py`):
- `GET/POST /os/bookings` — `BookingCreate` model: `service_id`,
  `service_name`, `client_id`, `client_name`, `client_email`,
  `project_id`, `date`, `start_time`, `end_time`; on create, server
  sets `status="confirmed"`, `payment_status="unpaid"`.
- `PATCH /os/bookings/{booking_id}/status` — real status enum
  enforced server-side: `requested`, `pending`, `confirmed`,
  `in_progress`, `completed`, `cancelled`, `rescheduled`, `no_show`
  (any other value rejected with HTTP 400).
- `GET/POST /os/services` — `ServiceCreate` model: `name`,
  `description`, `category`, `duration_hours`, `price`, `currency`
  (default `"EUR"`), `location`, `active`, `visible`.

Absorbs, as competency blocks (per `FMS_07_18_RECONCILIATION.md`'s own
merge verdict), **not** as separate formations:
- **FMS-14** (Artist Project & Production Coordination) — studio/
  production-project-side coordination, by reference to FMS-05's
  transferable coordination pedagogy (M05/M10), extended with
  session-specific competencies FMS-05 does not cover.
- **FMS-16** (Booking, Resource & Studio Planning) — same real
  `/os/bookings`/`/os/services` grounding; in real small/mid studio
  operations this is frequently the same person as Session Management,
  matching `fms-os/fms`'s own single `/os` layer serving both.

## Prerequisites

None (standalone external formation, umbrella of this wave).

## Objectives

Studio operations/session management (studio manager) is a
recognized, separately-employed role distinct from every one of the 6
creative FMS-01→06 métiers — running the day-to-day operational
machinery a creative production depends on:

- Session lifecycle management: booking creation through the real
  8-state status enum (`requested → pending → confirmed → in_progress
  → completed`, with `cancelled`/`rescheduled`/`no_show` as real
  exception states), never inventing a status the real API would
  reject.
- Service catalogue operations: managing what a studio offers
  (`ServiceCreate`'s real fields — duration, price, currency,
  location, active/visible flags) as a real commercial and scheduling
  input, not an abstract exercise.
- Studio/production-project coordination (absorbed FMS-14 block):
  session budget tracking, cross-department liaison for one
  production, deliverable tracking — distinct from an Artist Manager's
  career-long coordination duties (FMS-05), reusing FMS-05's
  transferable pedagogy by reference.
- Booking & resource planning (absorbed FMS-16 block): scheduling
  discipline across services/resources, recognizing when this splits
  into a dedicated scheduler role in larger operations vs. staying
  folded into Session Management in smaller ones.

## Modules

1. **Session lifecycle management** — grounded in the real
   `BookingCreate` model and the real 8-state status enum enforced by
   `PATCH /os/bookings/{id}/status`; candidate must recognize which
   status transitions are valid and what each implies operationally.
2. **Service catalogue operations** — grounded in the real
   `ServiceCreate` model; managing duration/price/currency/location/
   active/visible as real scheduling and commercial levers.
3. **Studio/production-project coordination (FMS-14 block)** — by
   reference to FMS-05/M05,M10 for transferable coordination pedagogy;
   adds session budget tracking, cross-department liaison for one
   production, and deliverable tracking as the studio-side-specific
   material FMS-05 does not cover.
4. **Booking & resource planning (FMS-16 block)** — scheduling
   discipline across the real bookings/services data model; explicit
   recognition of when this splits into a dedicated scheduler role
   (larger operations) vs. staying folded into Session Management
   (smaller ones, matching `fms-os/fms`'s own single `/os` layer
   design).

## Assessment

A studio-day operations exercise: candidate is given a representative
set of booking requests, service catalogue entries, and a
production-coordination brief, and must (a) process each booking
through valid status transitions only, (b) make a service-catalogue
recommendation, and (c) produce a coordination/scheduling plan —
graded against the real data model's actual constraints (e.g. an
invalid status transition is a real, gradeable error, not a stylistic
one).

## Evidence / certification / mission eligibility

`FMS07.SKILL.*` Skill IDs, reserved in
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`. Mission eligibility requires
literacy of the real `fms-os/fms` bookings/services data model — never
live production write access to that system in production.

## Status

`STATUS = PACKAGE_COMPLETE` — full canonical package (référentiel +
N1/N2 + assessment/rubric + evidence model + 3 guides + integration
note), deepened this pass as the FMS-07→18 wave's flagship. Never
implies `FULLY_COMPLETE` — no real candidate has been assessed yet.

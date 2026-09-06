# GMD-0001 — Good Mood Internal Operator: Canonical Education Map

```
STATUS = DECIDED. Defines the shared competency skeleton every
gmdNN/REFERENTIAL.md instantiates, so no two formations restate the
same base competency (rule §26 — registries, not narrative).
```

## PROFESSIONAL_ROLE → ACTIVITIES → COMPETENCIES (shared skeleton)

Every GMD-2X/3X role is a specialization of one base role:

```
PROFESSIONAL_ROLE: Good Mood OS Operator (umbrella, GMD-21)
  ACTIVITY: Operate a specific subsystem of the real Good Mood OS
    COMPETENCY C1 — Read the subsystem's real data model correctly
    COMPETENCY C2 — Execute the subsystem's real operator actions (CRUD, scan, export, dispatch) without error
    COMPETENCY C3 — Diagnose a subsystem failure using only what the real API/logs expose (never invented telemetry)
    COMPETENCY C4 (where applicable) — Reconcile the subsystem's state against a cross-system outbox (FREK/Wallet)
```

Each specialization (GMD-22→33) instantiates this skeleton against its
own real route cluster (table in `README.md`) — a `REFERENTIAL.md`
never re-derives C1-C4 in the abstract, it grounds them in the
specific models/endpoints named in its own repo-truth table.

## Dependency graph

```
GMD-21 (umbrella, orientation) → prerequisite for all of GMD-22→33
GMD-22 (Catalogue) ─┐
GMD-23 (Event) ──────┼─→ GMD-24 (Ticket Type & Sales) — sales needs both a catalogue item and an event
GMD-23 (Event) ──────┴─→ GMD-25 (Door Scan) — scanning needs an event to scan into
GMD-26 (Fan CRM) ← fed by GMD-24 (purchase creates/updates a fan record)
GMD-27 (Merch) — independent subsystem, no hard dependency
GMD-28 (Orders & Payment) ← depends on GMD-24 (ticket sale) and GMD-27 (merch sale) as its two real revenue sources
GMD-29 (Newsletter & Campaign) ← reads the fan base built by GMD-26
GMD-30 (Reporting) ← reads GMD-23/24/25 (event, ticket, scan data)
GMD-31 (FREK Outbox) ← triggered by GMD-24/25 (purchase, entry scan — the two real interaction_types emitted)
GMD-32 (Wallet Outbox) ← triggered by GMD-24 (ticket purchase)
GMD-33 (Admin & Security) — prerequisite for any operator role requiring admin auth (all of GMD-22→32 sit behind `get_current_admin`)
GMD-34 (Incident & Recovery) — BLOCKED, no dependents can complete until it exists
```

## Anti-footprint verification (repeated from `GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`, re-confirmed here before building)

Every competency built in this corpus is checked against the real
route/model table in `README.md` before being written — no competency
in any `gmdNN/REFERENTIAL.md` describes a capability absent from that
table. `CROSS_DOMAIN_CONTAMINATION` check: this corpus never conflates
Good Mood's real backend with any other CVLN product of a similar
name; it never asserts a CVE, Kiltikonet, KORA, or LabelOS touchpoint
beyond the FREK/Wallet outbox pattern already verified.

## Boundary with DJ Sayd (SAY-*)

Per `GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`: DJ Sayd carries zero
operator-role rows. This corpus is exhaustive for Good Mood's real
internal-operator layer — no SAY-* competency will ever appear here.

## Certification eligibility (shared across GMD-21→33)

An operator becomes eligible for `Certification Academy` (`ECO-010`,
`100_ECONOMY/ECONOMIC_MODEL.md`) on this corpus only once:
1. GMD-21 (orientation) is complete, and
2. the specific specialization's own modules are complete, and
3. its assessment (rubric in `gmdNN/REFERENTIAL.md` §Assessment) is
   passed at N2 threshold or above.

Certification here is `INTERNAL_QUALIFICATION` (per the economic
mapping — `NOT_FOR_SALE`, `PRODUCT_VERIFIED + ROLE_DEFINED` gate) —
never a public Academy offer. `CERTIFICATION != AUTHORIZATION`: passing
this corpus's assessments never grants runtime access to the real
`gmfest972/goodmooddjsayd` admin panel — that is a separate, governed
authorization decision (see `CERTIFICATION_MODEL.md` §Authorization
gate).

## Mission eligibility

A GMD-21→33-certified operator becomes eligible for a real Good Mood
operations mission (per `Learning-to-Work`, `100_ECONOMY/
ECONOMIC_MODEL.md`) only once a genuine Good Mood/DJ Sayd operational
need exists and the human authority responsible for that product signs
off — this corpus never asserts a mission exists on its own authority.

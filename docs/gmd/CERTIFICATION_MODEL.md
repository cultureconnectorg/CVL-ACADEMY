# GMD-21→33 — Shared Certification Model

```
Applies to all 13 buildable formations in this corpus. One model,
never restated per formation (rule §26).
```

## Evidence chain (per `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`)

```
COMPETENCY → MODULE → ASSESSMENT → EVIDENCE → SKILL_ID → QUALIFICATION
```

`READY_FOR_FREK_PROOF = FALSE` — no evidence produced by this corpus
is wired to `frek_core.issue_proof()` yet (that binding is itself
`BLOCKED_PRODUCT_DEPENDENCY` for Good Mood specifically, since the
Good Mood repo's own FREK outbox (`GMD-31`) is a client of a *different*
FREK endpoint (`FREK_ID_URL`, Good Mood's own env var) than this
Academy's `frek_core.py` — the two must never be conflated as the same
proof channel).

## N1 / N2 / Assessment structure

- **N1 (formative)**: per-module quiz over the real data model and
  routes named in that module (e.g. "what does `POST /scan/check`
  return on a duplicate scan?" — answerable only by reading the real
  route, never invented).
- **N2 (applied case)**: a written incident/change scenario grounded
  in the real repo (e.g. "a fan reports their ticket QR won't scan —
  trace the real code path from `/tickets/{tid}/qr.png` through
  `/scan/check` and identify where it could fail").
- **Assessment (certificatif)**: a graded walkthrough of the
  specialization's real API surface with a corrector rubric (0-4
  scale per competency, per `docs/kor/*/CERTIFICATION_MODEL.md`
  precedent) — eliminatory below 2/4 on any competency, mention caps
  per overall average, matching the FMS canonical rubric convention
  already used across this Academy.

## Skill ID namespace

`GMD21.SKILL.*` → `GMD33.SKILL.*`, one namespace per formation,
`PROPOSED` status (first Skill IDs ever reserved for this corpus —
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`'s Skill ID Namespace Map is
updated by this commit to record it, no collision with `KOR*`/`KLT*`).

## Authorization gate (never automatic)

Passing the Assessment produces a `QUALIFICATION`, never an
`AUTHORIZATION`. Per `00_GOVERNANCE/AUTHORIZATION_MODEL.md` and the
Master Package's `CERTIFICATION_AUTHORIZATION_CONFUSION = 0` gate: a
human with real administrative authority over `gmfest972/
goodmooddjsayd` must separately grant runtime access (e.g. an actual
admin login) — this corpus's certification is evidence a candidate
*could* be trusted with that access, never the access itself.

## Renewal

Per `ECO-041` (`100_ECONOMY/ECONOMIC_MODEL.md`): standard 24-month
requalification, except GMD-33 (Admin & Security Operations), which
inherits the 12-month sensitive-qualification cycle (`ECO-042`) since
it covers authentication/session-security competencies.

## Status

`STATUS = RECONCILED_NOT_BUILT` at the Master 2D level remains the
formal status of GMD-21→33 as *cartography rows*; this document and
each `gmdNN/REFERENTIAL.md` are the first real W6 content built for
them. No claim of `FULLY_COMPLETE` is made — see `README.md`.

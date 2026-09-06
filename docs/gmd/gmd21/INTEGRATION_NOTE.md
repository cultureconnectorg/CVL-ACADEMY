# GMD-21 — Integration Academy Package Note

## What is real vs. what this package assumes

**Real (verified this session):** `gmfest972/goodmooddjsayd/backend/
server.py` and its full route table, the auth boundary
(`get_current_admin`), the FREK/Wallet outbox pattern. All of GMD-21's
content is checkable against this real code.

**Assumed by this package (not yet verified):** that this Academy's
own runtime will ever bind a real candidate account to a
`GMD21.SKILL.*` record. No such binding exists today — `docs/gmd/` is
a pedagogical corpus, not a wired feature. Binding it into the real
Academy runtime (`backend/certification/`) is a separate, future
integration task, explicitly not performed by this commit
(`NO_RUNTIME_BINDING`).

## Dependencies

- `docs/cvln_academy_master/20_EXTERNAL/GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`
  — the reconciliation this formation was built from; never
  re-audited or contradicted here.
- `docs/cvln_academy_master/70_EVIDENCE/EVIDENCE_ARCHITECTURE.md` —
  Skill ID namespace registration.
- `docs/cvln_academy_master/100_ECONOMY/ECONOMIC_MODEL.md` — pricing
  context (`INTERNAL_QUALIFICATION`, `NOT_FOR_SALE`).

## What a future integration would need

1. A `GMD21` entry in this Academy's certification/skill registry
   (currently `docs/kor/`/`docs/klt/`-scoped only).
2. A real candidate-facing delivery surface (this corpus is
   markdown-only; the Academy's actual module/quiz/assessment runtime
   would need to ingest it, the same way `fms_import/` ingests FMS
   ZIPs).
3. A decision on whether `gmfest972/goodmooddjsayd` admin credentials
   are ever provisioned to a certified operator — an explicit,
   separate authorization decision, never automatic.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD21` — competencies, prerequisites,
objectives, modules, outcomes/deliverables, N1 bank, N2 bank,
assessment, rubric, evidence model, 3 guides, this integration note,
and the corpus-level quality gates (`../QUALITY_GATES.md`) all exist
for GMD-21 specifically. `FULLY_COMPLETE` still requires a real
candidate pass — not claimed here.

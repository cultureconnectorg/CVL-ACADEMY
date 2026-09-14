# ACA-0020 — Assessment/Proof Chain to Real Runtime: FRK Rubric Binding

```
STATUS: EXECUTED (2026-09-08), fourth and final planned domain through
the ACA-0020 pattern. Closes the rubric/grading half of the chain for
54/57 real FRK formations with a built ASSESSMENT_AND_RUBRIC.md — the
remaining 3 (FRK-10/14/73) are explicitly, correctly excluded (see
below), not a gap.
```

## What this closes

Same real gap as KOR/KLT/FMS-07..18: `start_attempt`'s
`get_rubric(certification_code)` would 404 for any FRK formation — zero
`Rubric` documents ever existed for this domain, even though `frk_
canonical`'s own filesystem-native import pipeline already persists
every real `docs/frk/frkNN/ASSESSMENT_AND_RUBRIC.md` into `db.
frk_resources` (`type="assessment_and_rubric"` — `frk_canonical/
parser.py`'s own filename table already recognizes this exact filename,
unlike `fms_import`'s classifier, which didn't for the equivalent FMS
files — see the FMS-spec report). This module reads that already-
populated collection, the same as KOR/KLT.

## Real corpus shape — genuinely more heterogeneous than the first three domains

A filesystem sweep of all 57 real `ASSESSMENT_AND_RUBRIC.md` files
(FRK-01..75, only 57 of the 75 possible codes have a built one) before
writing any parser code found:

1. **Named-competency shape** (16/57) — a `| Cn | Description |` table
   naming each competency, sometimes under an explicit heading,
   sometimes with none at all (the file goes straight from its intro
   line into the table). Parsed by scanning every line for the row
   shape itself rather than gating on a heading — the row is
   unambiguous either way (the sibling level-meaning table's first
   cell is always a bare digit, never `Cn`).
2. **Single global grille shape** (41/57, the actual majority) — no
   named competency list at all, one shared `## Grille (0–4)` table
   for the whole formation. Reduces to exactly **one**
   `RubricCriterion` — never fabricating a specific competency name
   the document doesn't state.
3. **Explicitly non-certifiable / formative-only** (3/57 — FRK-10,
   FRK-14, FRK-73, confirmed by grep sweep) — the document itself says
   no certification can be delivered yet, pending a named human expert
   review (`NEEDS_EXPERT_REVIEW`). `import_rubric_for_formation`
   checks for this marker **before** attempting to parse and refuses
   (returns `None`) for these three, regardless of shape — importing a
   live gradable `Rubric` for one would directly contradict what the
   formation's own real content states about itself.

## What was built

- **`backend/frk_canonical/rubric_import.py`** (new) —
  `parse_rubric_criteria` (both real shapes), `certification_code_for`,
  `import_rubric_for_formation` (reads `db.frk_resources`, refuses
  formative-only formations, defensive threshold-marker check).
- **`backend/frk_canonical/__init__.py`** — exports
  `FRK_RUBRIC_PASS_THRESHOLD_PCT`, `certification_code_for`,
  `import_rubric_for_formation`.
- **`backend/api/frk_canonical.py`** — new admin endpoint
  `POST /frk-canonical/formations/{formation_code}/rubric/import`,
  with a 404 message that honestly distinguishes "not imported yet"
  from "explicitly not certifiable yet" rather than conflating them.

## Verification

- `python -m pytest tests/test_frk_rubric_import.py -v` —
  **68/68 passed**: parses all 57 real files (asserting `max_score=4.0`
  / `bloc="A01"` / `is_eliminatory=True` on every resulting criterion
  for the 54 certifiable ones), a dedicated named-competency-shape
  proof (FRK-09, 2 criteria), a dedicated single-grille-shape proof
  (FRK-23, exactly 1 criterion — never 0, never fabricated), the
  certification-code convention, explicit refusal of a formative-only
  formation (FRK-14) with a real assertion that nothing gets written to
  `db.certification_rubrics` for it, rejection of an unimported/wrong-
  domain/nonexistent code, import/idempotency, and two real-engine
  grading proofs (one per shape).
- Full backend suite: `python -m pytest tests/ -q
  --ignore=tests/backend_test.py` — **446 passed** (up from 378 before
  this pass), zero regressions.
- `python -m flake8 .` — clean.

## What remains open

1. **N1/N2 question-bank binding** — same open item as every prior
   ACA-0020 pass; not attempted for any domain yet.
2. **The 3 formative-only formations stay correctly ungraded** —
   FRK-10/14/73 will 404 on rubric import until their real
   `NEEDS_EXPERT_REVIEW` blocker is lifted by an actual named expert
   (per their own `REFERENTIAL.md`) and their `ASSESSMENT_AND_RUBRIC.md`
   is updated to state a real, certifiable rubric — this is a content
   decision for the Founder/domain expert, not something this pass can
   or should route around.
3. **No admin UI trigger** — same open item as every prior domain.
4. **Not run against a live MongoDB** — same disclosed limitation as
   every prior ACA-0020 pass.
5. **ACA-0020's originally-scoped 4-domain sweep is now complete**
   (KOR, KLT, FMS-07..18, FRK) — the task itself remains marked
   in-progress at the platform level pending the N1/N2 question-bank
   and admin-UI-trigger items above, which are real, larger follow-on
   work beyond rubric/grading binding.

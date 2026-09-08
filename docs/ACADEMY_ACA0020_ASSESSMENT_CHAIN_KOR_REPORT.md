# ACA-0020 — Assessment/Proof Chain to Real Runtime: KOR Rubric Binding

```
STATUS: PARTIAL, real and verified for its scope. Closes the rubric/
grading half of the chain for KOR (proof-of-pattern, 15/15 formations).
Eligibility was already real (RAIL 2). N1/N2 question-bank binding,
KLT/FRK/FMS-canonical rubric import, and jury-facing UI surfacing of
canonical attempts remain open — see "What remains" below.
```

## The real gap this closes

`certification/service.py`'s `check_full_eligibility` already read real
canonical progress (`content_viewed_at`, RAIL 2) to decide whether a
candidate could attempt a certification for a KOR/KLT/FMS-canonical
formation. But `start_attempt` also calls `get_rubric(certification_code)`
first, and **zero `Rubric` documents ever existed for any canonical
formation** — `db.certification_rubrics` only ever held legacy-FMS
content. Every canonical certification attempt would 404 on the rubric
lookup before eligibility was even reached. The real grading criteria
already existed as real, human-authored content
(`docs/kor/korXX/assessments/RUBRIC.md`, already parsed and classified
`type="rubric"` into `db.kor_resources` by `kor_canonical`'s own import
pipeline) — they were simply never turned into the structured, gradable
`Rubric` the certification engine can score against.

## What was built

### `backend/kor_canonical/rubric_import.py` (new)
- `parse_rubric_criteria(body_markdown) -> List[RubricCriterion]` — pure
  parser for the real markdown table
  (`| # | Critère | <seuil> | Éliminatoire si 0 ? |`).
- `certification_code_for(formation_code)` — `"KOR-09"` → `"KOR09-A01"`,
  the exact convention every real file's own `# KORxx-A01` heading
  already uses.
- `import_rubric_for_formation(formation_code)` — reads the real,
  already-imported `type="rubric"` resource from `db.kor_resources`,
  parses it, and upserts a real `Rubric` into `db.certification_rubrics`
  (same collection/shape legacy-FMS rubrics use).

### `backend/api/kor_canonical.py`
New admin endpoint `POST /kor-canonical/formations/{formation_code}/rubric/import`
— idempotent (upsert by `certification_code`), 404 if the formation's
docs haven't been imported yet or genuinely has no `RUBRIC.md`.

### Verification the parser is correct against the REAL corpus, not a synthetic fixture
Before writing the parser, every one of the 15 real
`docs/kor/kor01..15/assessments/RUBRIC.md` files was inspected directly
(not assumed): identical 4-column table shape, identical global pass
rule ("moyenne ≥ 2,5" — every single one of the 15 files, no exception),
exactly 3 real eliminatory-cell strings (`"non"`, `"**oui**"`,
`"**oui si non conforme**"`). `tests/test_kor_rubric_import.py` then
parses **all 15 real files off disk** (not a copy) and asserts sane
output for each; a dedicated by-hand cross-check on KOR-09 confirms the
parser's eliminatory-criterion output (`C7`, `C10`) matches what a human
reading the real file concludes.

### Verification the result is genuinely gradable, not just a data-shape match
`test_imported_rubric_is_scored_by_the_real_engine` feeds an imported
KOR-09 `Rubric` into the SAME, unmodified `certification.scoring.
compute_scores` every legacy-FMS attempt uses: a candidate scoring
near-perfect everywhere except the real eliminatory criterion C7 (raw 0)
is correctly `eliminated=True, passed=False`; the same candidate scoring
C7 at 4 instead passes at `score_global=100.0` against the imported
`pass_threshold_pct=62.5` (the real 2,5/4 threshold every file states).

## What was deliberately NOT attempted (disclosed, not silently worked around)

- **Per-criterion "Seuil" text** (e.g. "≥2", "4 (binaire)") is real jury
  guidance for what a raw score *means* for that criterion — the engine
  has no field for a criterion-local pass/fail beyond eliminatory-if-
  zero, so it is not imported. The compound "Seuil global" rule (average
  ≥ 2,5 AND named criteria non-zero) reduces, without loss, to
  `pass_threshold_pct=62.5` plus each named criterion's own
  `is_eliminatory=True` — logically the same gate the engine already
  enforces.
- **No `skill_id` linkage.** Correlating a rubric criterion's free-text
  label to a specific real Skill ID (`skills/SKILL_ID_REGISTRY.md`)
  would need fuzzy text matching with no explicit textual anchor in
  either document — exactly the invented correlation this codebase's
  doctrine forbids. `skill_id` stays `None`; `bloc` is the constant
  `"A01"` (these rubrics are one flat pass, not FMS-01's multi-bloc
  structure).

## Verification

- `python -m pytest tests/test_kor_rubric_import.py -v` — 21/21 passed
  (15 real-file parametrized + 6 targeted: hand-cross-check, naming
  convention, import/upsert/idempotency/404, real-engine grading).
- Full backend suite: `python -m pytest tests/ -q --ignore=tests/backend_test.py`
  — **344 passed**, zero regressions.
- `python -m flake8 .` — clean (this repo's actual CI gate).
- `black --check` / `isort --check-only` — both clean on every touched
  file.
- Manual import verified against every one of the 15 real files
  (`python -c "..."` sweep, not just the test suite) before writing the
  test — criteria counts and eliminatory sets both plausible and
  hand-verified for KOR-01 and KOR-09 against the real markdown text.

## What remains open (this is a PARTIAL closure, not a claim of FULLY_COMPLETE)

1. **KLT-canonical and FMS-canonical rubric import** — `klt_canonical/`
   and `fms_canonical/` classify the exact same resource kinds
   (`rubric`, `certification_assessment`, `N1_QUESTION_BANK`,
   `N2_EVALUATIONS`) via their own parsers (confirmed by direct grep of
   `klt_canonical/parser.py`/`fms_canonical/module_map_extract.py`), so
   the same pattern this pass proves for KOR should port with minor
   changes (collection name, formation-code convention) — not yet done.
   `frk_canonical` has not yet been checked for the same convention.
2. **N1/N2 question-bank binding** — `N1_QUESTION_BANK.md`/
   `N2_EVALUATIONS.md` are real, already-classified resources
   (`db.kor_resources`, `type` field distinguishes them from `rubric`)
   but this pass only converts the A01 rubric. A real N1/N2 quiz-taking
   flow for canonical formations (parsing question banks into a
   gradable quiz structure, analogous to `quiz.py`'s legacy-FMS
   `build_quiz`) is unbuilt.
3. **No admin UI trigger** — the import endpoint exists and is real,
   but nothing in `AdminDashboard.js` calls it yet; today it must be
   invoked directly (e.g. via the API or a script) after
   `POST /kor-canonical/import`.
4. **Not run against the live formations yet** — this pass proves the
   pipeline is correct and gradable; it has not been executed against
   a real running MongoDB with the full KOR corpus already imported
   (this sandbox has no live Mongo instance — see every prior report's
   disclosed "no live preview" limitation). The idempotent-upsert design
   means running `POST /kor-canonical/import` then `POST .../rubric/
   import` for each of the 15 formations, whenever a real environment
   is available, is the remaining operational step, not a code gap.

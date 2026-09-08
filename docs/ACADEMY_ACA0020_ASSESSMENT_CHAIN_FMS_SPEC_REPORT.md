# ACA-0020 — Assessment/Proof Chain to Real Runtime: FMS-07..18 Rubric Binding

```
STATUS: EXECUTED (2026-09-08), third domain through the ACA-0020
pattern, but with a real architectural difference from KOR/KLT —
see "Why this needed its own module" below. Closes the rubric/grading
half of the chain for all 9 real FMS-07..18 specialization formations
that carry a built docs/fms/fmsXX/ASSESSMENT_AND_RUBRIC.md.
```

## What this closes

The same real gap KOR and KLT already had: a candidate for an FMS-07..18
specialization certification would 404 on `start_attempt`'s
`get_rubric(certification_code)` — zero `Rubric` documents ever existed
for these 9 formations, even though their real grading content
(`docs/fms/fmsXX/ASSESSMENT_AND_RUBRIC.md`) has existed since the
FMS-08→18 deepening pass.

## Why this needed its own module, not a straight KOR/KLT port

Two real differences, both discovered by direct inspection before
writing any code, not assumed:

1. **No `db.fms_resources` entry exists for these files at all.**
   `fms_canonical/import_pipeline.py` only wraps `fms_import.
   import_fms_zip`, scoped to the one uploaded FMS-01..06 archive
   (`FMS_Chantier_Complet_20260822.zip`). FMS-07..18 live natively in
   `docs/fms/fmsXX/` (same shape as `docs/kor/`, `docs/klt/`), never
   packaged into that ZIP. Worse: even if they were run through
   `fms_import`'s own classifier, `ASSESSMENT_AND_RUBRIC.md` matches
   none of `FILENAME_TYPE_HINTS`' filename fragments — confirmed by
   tracing `_infer_type` — so the file would be silently dropped with a
   warning-level `ImportIssue`, not an error. Building a KOR/KLT-style
   rubric_import that reads from a `db.*_resources` collection would
   therefore find nothing, no matter how correct the parser was.
   **Fix**: `fms_canonical/spec_rubric_import.py` reads the real file
   directly off the server filesystem — the same trust boundary
   `kor_canonical`/`klt_canonical`'s own import pipelines already read
   `docs/kor/`/`docs/klt/` from, just without an intermediate
   classify-and-persist step (out of scope for this pass — see "What
   remains open").

2. **The document's own table shape is different.** KOR/KLT's
   `RUBRIC.md` files carry one 4-column table with an explicit
   per-criterion "Éliminatoire si 0 ?" cell. FMS-07..18's
   `ASSESSMENT_AND_RUBRIC.md` instead carries a `## Compétences
   évaluées` table (competency id + description) and a *separate*,
   *shared* `## Rubric (0–4 par compétence)` table (generic level
   meanings, identical text reused across every competency) — verified
   identical in structure across all 9 real files before writing the
   parser. The eliminatory rule isn't per-row at all: every one of the
   9 files' `## Seuil de passage` states, verbatim, `"Moyenne ≥ 2.5/4,
   aucune compétence à 0 par élimination"` — i.e. **every** competency
   is eliminatory-if-zero, stated once globally rather than marked per
   criterion. `parse_rubric_criteria` reflects this: it parses the
   competency table (no eliminatory column to read) and sets
   `is_eliminatory=True` unconditionally on every resulting criterion,
   with a defensive regex check (`_SEUIL_MARKER_RE`) that raises rather
   than silently importing a wrong threshold if a future file (e.g. an
   eventual FMS-14/16/17) doesn't state the same global rule.

## What was built

- **`backend/fms_canonical/spec_rubric_import.py`** (new) —
  `FMS_SPEC_FORMATION_CODES` (the 9 real, filesystem-confirmed
  formations — explicitly excludes FMS-14/16/17, named in the shared
  `docs/fms/CERTIFICATION_MODEL.md` range but not yet built, and
  excludes FMS-01..06, which use the separate ZIP-import path),
  `parse_rubric_criteria`, `certification_code_for`,
  `import_rubric_for_formation`.
- **`backend/fms_canonical/__init__.py`** — exports
  `FMS_SPEC_FORMATION_CODES`, `spec_certification_code_for`,
  `import_spec_rubric_for_formation`.
- **`backend/api/canonical.py`** — new admin endpoint
  `POST /canonical/formations/{formation_code}/rubric/import`
  (idempotent, 404 for any code outside the real 9).

## Verification

- `python -m pytest tests/test_fms_spec_rubric_import.py -v` —
  **18/18 passed**: 9 real-file parametrized parses (asserting every
  criterion is `max_score=4.0`, `bloc="A01"`, `is_eliminatory=True`),
  a by-hand cross-check on FMS-09, the certification-code convention,
  an explicit assertion that FMS-14/16/17/FMS-01/KOR-01 are all
  correctly rejected, import/idempotency, an all-9-formations import
  sweep, and two real-engine grading proofs (any competency at 0 fails
  the attempt; all competencies at 4 passes at `score_global=100.0`).
- `python -m pytest tests/test_fms_spec_rubric_import.py tests/
  test_kor_rubric_import.py tests/test_klt_rubric_import.py -q` —
  **55/55 passed**, zero cross-domain regression.
- Full backend suite: `python -m pytest tests/ -q
  --ignore=tests/backend_test.py` — **378 passed** (up from 360 before
  this pass), zero regressions.
- `python -m flake8 .` — clean (the repo's actual CI gate).
- `black`/`isort` — clean on every touched file except the same
  pre-existing repo-wide isort/black profile conflict already disclosed
  in the KOR report (no `profile=black` configured; confirmed via
  `git stash` in that earlier pass to predate this session's changes;
  not part of the actual CI gate, which runs flake8+pytest only). New
  files match the existing repo's own multi-line-parens import style,
  not the conflicting one.

## What remains open

1. **N1/N2 question-bank binding** — same open item as KOR/KLT;
   `BANQUE_N1.md`/`BANQUE_N2.md` exist per formation but are not parsed
   into a gradable quiz structure.
2. **No filesystem-native resource-classification package for
   FMS-07..18** — unlike KOR/KLT (which have a full `import_kor_docs`/
   `import_klt_docs` pipeline persisting every resource type, not just
   the rubric, into a queryable `db.*_resources` collection with
   content-view progress tracking), this pass only closes the rubric
   half for FMS-07..18 by reading the one needed file directly. A full
   `fms07_18`-style companion package (mirroring `kor_canonical`/
   `klt_canonical` in scope) is real, disclosed follow-on work, not
   attempted here — the certification/eligibility chain does not
   require it (canonical progress-gated eligibility for FMS-07..18 was
   not part of this pass's scope either).
3. **No admin UI trigger** — same open item as KOR/KLT; the endpoint
   exists and is real but nothing in `AdminDashboard.js` calls it yet.
4. **`frk_canonical` rubric import remains unbuilt** — the fourth and
   final domain named in the original ACA-0020 KOR report's "what
   remains open" list; not yet even inspected for the same convention.
5. **Not run against a live MongoDB** — same disclosed limitation as
   every prior ACA-0020 pass (this sandbox has none); the idempotent-
   upsert design means running the new endpoint for each of the 9
   formations is the remaining operational step, not a code gap.

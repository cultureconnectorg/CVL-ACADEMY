# ACA-0020 — Assessment/Proof Chain to Real Runtime: KLT Rubric Binding

```
STATUS: EXECUTED (2026-09-08), second domain through the pattern
docs/ACADEMY_ACA0020_ASSESSMENT_CHAIN_KOR_REPORT.md established for
KOR. Closes the rubric/grading half of the chain for all 10 real
Kiltikonet (KLT) formations that carry an assessments/RUBRIC.md.
```

## What this closes

Same real gap as the KOR pass, same domain shape: `certification/
service.py`'s `check_full_eligibility` already reads real canonical
KLT progress (`_check_canonical_eligibility`'s `klt_canonical` branch,
confirmed present before this pass) to gate certification attempts, but
zero `Rubric` documents ever existed for any KLT-canonical formation —
`start_attempt`'s `get_rubric` would 404 before eligibility was even
reached, exactly the same failure mode the KOR report documents.

## What was built

### `backend/klt_canonical/rubric_import.py` (new)
A direct port of `kor_canonical/rubric_import.py`: `parse_rubric_
criteria`, `certification_code_for`, `import_rubric_for_formation`,
reading from `db.klt_resources` instead of `db.kor_resources`. See that
file's own docstring (and the KOR report) for the reasoning this reuses
verbatim rather than re-deriving.

### `backend/api/klt_canonical.py`
New admin endpoint `POST /klt-canonical/formations/{formation_code}/
rubric/import`, same contract as the KOR one (idempotent, 404 if
unimported or genuinely rubric-less).

### The one real difference this port had to account for
Before writing the parser, every one of the 10 real
`docs/klt/kltXX/assessments/RUBRIC.md` files was inspected directly:
same 4-column table shape, same "Moyenne ≥ 2,5" global rule (all 10, no
exceptions) — but the eliminatory-cell wording is **not** identical to
KOR's. KLT-01→04 use `"**oui si non conforme**"` (matching KOR); KLT-05/
06/07/08/13/18 instead use `"**oui si absent**"` — a wording KOR never
uses. The KOR module's original parser matched an *enumerated set* of
exact strings (`{"**oui**", "**oui si non conforme**"}`), which would
have silently undercounted KLT's eliminatory criteria. Both
`kor_canonical/rubric_import.py` and this new
`klt_canonical/rubric_import.py` were generalized to match the real,
underlying document convention instead — any cell starting with the
bold `"**oui"` marker, regardless of its qualifier — which is correct
for both domains and doesn't silently break on a next domain's own
wording variant. `tests/test_klt_rubric_import.py`'s
`test_eliminatory_prefix_matches_both_real_klt_wordings` proves both
variants resolve correctly; `tests/test_kor_rubric_import.py`'s
existing 21 tests were re-run and still pass unchanged (KOR's own
strings both still match the more general prefix rule).

### Formations confirmed real but out of scope (not silently dropped)
`KLT-09/10/11/12/14/15/16/17/19/20` have **no** `assessments/RUBRIC.md`
at all — confirmed by a direct filesystem sweep before writing the
parametrized test list, not assumed. `import_rubric_for_formation`
correctly returns `None` for these (proven by
`test_import_returns_none_for_formation_without_rubric`), the same
honest "not available yet" signal the KOR module already gives for an
un-imported formation — never a fabricated empty rubric.

## Verification

- `python -m pytest tests/test_klt_rubric_import.py -v` — **16/16
  passed**: 10 real-file parametrized parses, a by-hand cross-check on
  KLT-05 (chosen specifically because it's the first formation using
  the `"si absent"` wording), the certification-code convention, the
  eliminatory-prefix regression test, import/idempotency/404 checks,
  and a real-engine grading proof (eliminatory criterion at 0 correctly
  fails the attempt).
- `python -m pytest tests/test_kor_rubric_import.py -v` — still **21/21
  passed** after generalizing the shared detection logic — no
  regression to the first domain.
- Full backend suite: `python -m pytest tests/ -q --ignore=tests/backend_test.py`
  — **360 passed**, zero regressions.
- `python -m flake8 .` — clean. `black`/`isort` — clean on every
  touched file.

## What remains open

Same list the KOR report already carries, now updated: FMS-canonical
and FRK-canonical rubric import (same pattern, not yet ported); N1/N2
question-bank binding for any domain; no admin UI trigger for either
KOR's or KLT's import endpoint; not yet run against a live MongoDB
(this sandbox has none — the idempotent-upsert design means running
both domains' import endpoints, whenever a real environment is
available, is the remaining operational step, not a code gap).

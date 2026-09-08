"""ACA-0020 — real N1/N2/A01 assessment-chain runtime binding for
canonical KORA formations.

**The gap this closes, precisely**: `certification/service.py`'s
`check_full_eligibility` already reads real canonical progress
(`content_viewed_at` across every real module) to gate whether a
candidate can start a certification attempt for a KOR-canonical
formation — that part of the chain was already real (RAIL 2). But
`start_attempt` also calls `get_rubric(certification_code)`, and
**zero `Rubric` documents were ever created for any canonical
formation** — `db.certification_rubrics` only ever held legacy-FMS
content (`seed_data.py`), so every canonical certification attempt
would 404 before the eligibility check is even reached. The real
grading criteria already exist as real, human-authored content —
`docs/kor/korXX/assessments/RUBRIC.md`, already parsed and classified
`type="rubric"` by `import_pipeline.py` into `db.kor_resources` — they
were simply never turned into a structured, gradable `Rubric` the
certification engine can score against.

This module is that missing conversion: parse the real markdown table
already sitting in `db.kor_resources` into `certification.models`'
`RubricCriterion`/`RubricInput`, using ONLY fields the markdown itself
states — never inventing a weight, a bloc, or a skill_id the text
doesn't name.

**Format verified across all 15 real files**
(`docs/kor/kor01..15/assessments/RUBRIC.md`) before writing this
parser, not assumed: every one carries an identical 4-column table
(`| # | Critère | <threshold text> | Éliminatoire si 0 ? |`, the
threshold column's exact header wording varies but its position and
meaning never do) and an identical global pass rule
("Moyenne ≥ 2,5" / "moyenne ≥ 2,5", every one of the 15 files, no
exceptions) — see `docs/ACADEMY_ACA0020_ASSESSMENT_CHAIN_KOR_REPORT.md`
for the verification evidence. The eliminatory cell is always exactly
one of three real strings: `"non"`, `"**oui**"`,
`"**oui si non conforme**"` — anything else is left `is_eliminatory=
False` rather than guessed, and the row is still kept (never silently
dropped) so a format drift is visible in the resulting criteria count,
not hidden.

**What is deliberately NOT attempted** (disclosed, not silently
worked around):
- **Per-criterion "Seuil" text** (e.g. "≥2", "4 (binaire)") is real
  jury guidance for what a given raw score *means* for that specific
  criterion — it has no field in `RubricCriterion` to hold it (the
  engine grades a raw 0-4 score per criterion, not a criterion-local
  pass/fail), so it is not imported. The one criterion-level rule the
  engine *does* model — eliminatory-if-zero — is imported; the
  compound "Seuil global" rule (average ≥ 2,5 AND named criteria
  non-zero) reduces, without loss, to `pass_threshold_pct=62.5`
  (2,5/4) plus each named criterion's own `is_eliminatory=True` — the
  two are logically the same gate this engine already enforces
  (`scoring.py`'s eliminatory-criterion short-circuit).
- **No `skill_id` linkage is attempted.** Correlating a rubric
  criterion's free-text label to a specific real Skill ID (per-
  formation `skills/SKILL_ID_REGISTRY.md`) would require fuzzy text
  matching with no explicit textual anchor in either document — exactly
  the kind of invented correlation this codebase's doctrine forbids.
  `skill_id` stays `None` on every imported criterion; `bloc` is set to
  the constant `"A01"` (these rubrics are one flat certification pass,
  not FMS-01's multi-bloc structure — there is no real bloc subdivision
  to preserve).
"""

from __future__ import annotations

import re
from typing import List, Optional

from certification.models import RubricCriterion, RubricInput
from db import db, utc_now_iso

# Matches a real criterion row, e.g.:
#   | 7 | Rétention traitée à égalité avec l'acquisition | ≥3 | **oui** |
# Deliberately requires exactly 4 real columns (5 pipes) so it can never
# match the *other* real 2-column table every RUBRIC.md also carries
# ("Échelle générale (par critère)", Niveau/Définition) — that table's
# rows have only 3 pipes and never match this pattern.
_CRITERION_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|(.+)\|([^|]*)\|([^|]*)\|\s*$")

_ELIMINATORY_STRINGS = {"**oui**", "**oui si non conforme**"}

# The one real global threshold every one of the 15 real RUBRIC.md
# files states, verified (see module docstring) rather than assumed —
# 2,5 on the real 0-4 Rubric Master scale.
KOR_RUBRIC_PASS_THRESHOLD_PCT = 62.5  # 2.5 / 4.0 * 100


def parse_rubric_criteria(body_markdown: str) -> List[RubricCriterion]:
    """Pure parse — no I/O. Returns criteria in the real document's own
    order; a formation whose file doesn't match this convention at all
    (none observed, but never assumed universal) simply yields an empty
    list rather than raising, so an importer can report 0 criteria
    honestly instead of crashing the whole batch."""
    criteria: List[RubricCriterion] = []
    for line in body_markdown.splitlines():
        m = _CRITERION_ROW_RE.match(line.strip())
        if not m:
            continue
        num, label, _threshold_text, eliminatory_raw = m.groups()
        label = label.strip()
        eliminatory_raw = eliminatory_raw.strip()
        criteria.append(
            RubricCriterion(
                id=f"C{num}",
                label=label,
                bloc="A01",
                skill_id=None,
                weight=1.0,
                max_score=4.0,
                is_eliminatory=eliminatory_raw in _ELIMINATORY_STRINGS,
            )
        )
    return criteria


def certification_code_for(formation_code: str) -> str:
    """ "KOR-09" -> "KOR09-A01" — the exact convention every real
    RUBRIC.md's own `# KORxx-A01` heading already uses (no dash before
    the 2-digit number), not a new naming scheme invented here."""
    return f"{formation_code.replace('-', '')}-A01"


async def import_rubric_for_formation(formation_code: str) -> Optional[RubricInput]:
    """Reads the one real `type="rubric"` resource already stored for
    `formation_code` in `db.kor_resources` (persisted by
    `import_pipeline.import_kor_docs` — this function never reads the
    filesystem itself, only the already-imported read model), parses
    it, and upserts a real `Rubric` document into
    `db.certification_rubrics` — the same collection/shape
    `api/certification.py`'s admin-authored rubrics already use, so
    every downstream consumer (`start_attempt`, `grade_attempt`,
    attestation) treats a KOR-canonical rubric identically to a legacy
    FMS one.

    Returns the `RubricInput` actually written, or `None` if no
    `type="rubric"` resource exists yet for this formation (it hasn't
    been imported via `POST /kor-canonical/import`, or genuinely
    doesn't have one) — the caller decides whether that's an error.
    """
    resource = await db.kor_resources.find_one(
        {"formation_code": formation_code, "type": "rubric"}, {"_id": 0}
    )
    if not resource:
        return None

    criteria = parse_rubric_criteria(resource.get("body_markdown", ""))
    rubric_input = RubricInput(
        level="A01",
        formation_code=formation_code,
        version="1.0",
        pass_threshold_pct=KOR_RUBRIC_PASS_THRESHOLD_PCT,
        criteria=criteria,
        cap_rules=[],
        mention_thresholds=[],
        assessment_kind="certification",
    )

    certification_code = certification_code_for(formation_code)
    payload = {"certification_code": certification_code, **rubric_input.model_dump()}
    payload["updated_at"] = utc_now_iso()
    await db.certification_rubrics.update_one(
        {"certification_code": certification_code},
        {"$set": payload},
        upsert=True,
    )
    return rubric_input

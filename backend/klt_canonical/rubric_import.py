"""ACA-0020 — real N1/N2/A01 assessment-chain runtime binding for
canonical Kiltikonet (KLT) formations.

Second domain through this pattern, after `kor_canonical/rubric_import.py`
(see `docs/ACADEMY_ACA0020_ASSESSMENT_CHAIN_KOR_REPORT.md` for the full
reasoning this file reuses verbatim — the gap it closes, what a
`Rubric` document unlocks downstream, and what's deliberately not
attempted). This module is the direct port: same table shape, same
`certification.models.RubricInput`/`RubricCriterion` target, same
`db.<domain>_resources` -> `db.certification_rubrics` conversion — read
from `db.klt_resources` (persisted by `klt_canonical.import_klt_docs`)
instead of `db.kor_resources`.

**Format verified across all 10 real files with a RUBRIC.md**
(`docs/klt/klt01/02/03/04/05/06/07/08/13/18/assessments/RUBRIC.md` —
KLT-09→12/14→17/19/20 have no `assessments/RUBRIC.md` at all, confirmed
by a direct filesystem sweep, so they are simply never importable by
this module, not a bug) before writing this: the same 4-column table
shape, and the same real global pass rule ("Moyenne ≥ 2,5", all 10
files, no exceptions) as KOR. One real difference this port had to
account for: KLT's eliminatory cell uses `"**oui si absent**"`
(KLT-05/06/07/08/13/18) alongside the plain `"**oui**"`
(KLT-01/02/03/04), never KOR's own `"**oui si non conforme**"` wording
— which is exactly why the shared-in-spirit detection matches the
`"**oui"` prefix rather than an enumerated string set (see
`kor_canonical/rubric_import.py`'s own `_is_eliminatory_cell`
docstring, which this file's logic mirrors rather than duplicates a
second inconsistent copy of).
"""

from __future__ import annotations

import re
from typing import List, Optional

from certification.models import RubricCriterion, RubricInput
from db import db, utc_now_iso

# Same shape as kor_canonical/rubric_import.py's own — see that file's
# docstring for why this deliberately can't match the OTHER real
# 2-column table every RUBRIC.md also carries.
_CRITERION_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|(.+)\|([^|]*)\|([^|]*)\|\s*$")

# The one real global threshold every one of the 10 real KLT RUBRIC.md
# files states — 2,5 on the real 0-4 Rubric Master scale, same as KOR.
KLT_RUBRIC_PASS_THRESHOLD_PCT = 62.5  # 2.5 / 4.0 * 100


def _is_eliminatory_cell(raw: str) -> bool:
    """See `kor_canonical.rubric_import._is_eliminatory_cell`'s own
    docstring — this is the same real-document convention (bold "oui",
    any qualifier), duplicated rather than imported across the two
    canonical packages to avoid a cross-domain dependency neither
    otherwise has, not because the logic differs."""
    return raw.startswith("**oui")


def parse_rubric_criteria(body_markdown: str) -> List[RubricCriterion]:
    """Pure parse — no I/O. See `kor_canonical.rubric_import.
    parse_rubric_criteria`'s own docstring for the full contract this
    mirrors exactly (order preserved, empty list rather than raising on
    a non-matching format)."""
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
                is_eliminatory=_is_eliminatory_cell(eliminatory_raw),
            )
        )
    return criteria


def certification_code_for(formation_code: str) -> str:
    """ "KLT-06" -> "KLT06-A01" — the exact convention every real
    RUBRIC.md's own `# KLTxx-A01` heading already uses."""
    return f"{formation_code.replace('-', '')}-A01"


async def import_rubric_for_formation(formation_code: str) -> Optional[RubricInput]:
    """See `kor_canonical.rubric_import.import_rubric_for_formation`'s
    own docstring for the full contract — this is the same function
    against `db.klt_resources`/the KLT domain."""
    resource = await db.klt_resources.find_one(
        {"formation_code": formation_code, "type": "rubric"}, {"_id": 0}
    )
    if not resource:
        return None

    criteria = parse_rubric_criteria(resource.get("body_markdown", ""))
    rubric_input = RubricInput(
        level="A01",
        formation_code=formation_code,
        version="1.0",
        pass_threshold_pct=KLT_RUBRIC_PASS_THRESHOLD_PCT,
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

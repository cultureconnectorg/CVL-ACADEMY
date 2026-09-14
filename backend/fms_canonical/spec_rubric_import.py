"""ACA-0020 — real N1/N2/A01 assessment-chain runtime binding for the 9
real FMS-07..18 specialization formations
(`docs/fms/fms07../ASSESSMENT_AND_RUBRIC.md`).

**Why this is a separate module from `fms_canonical`'s own ZIP-driven
import, not an extension of it**: `fms_canonical/import_pipeline.py`
wraps `fms_import.import_fms_zip` — it only ever ingests the one
uploaded archive (`FMS_Chantier_Complet_20260822.zip`, DEC-002), whose
scope is FMS-01..06 (see `docs/ACADEMY_FMS_CANONICAL_RUNTIME_BINDING_
REPORT.md`). FMS-07..18 were never part of that archive — they are a
later, filesystem-native addition (task "FMS-08→18: deepen 8 MODULE_
CONTENT_DRAFTED rows", same build wave as `kor_canonical`/`klt_
canonical`'s own domains), living directly under `docs/fms/fmsXX/` —
same shape as KOR/KLT's `docs/kor/korXX/`, `docs/klt/kltXX/` trees, not
a ZIP payload.

A second, real reason this can't reuse `fms_import`'s own resource
classifier: `fms_import/models.py`'s `FILENAME_TYPE_HINTS` matches on
filename fragments (`"rubric_master"`, `"referentiel"`, ...), but the
real FMS-07..18 files are named `ASSESSMENT_AND_RUBRIC.md` — a fragment
`_infer_type` does not recognize (confirmed: running the existing
classifier against this filename returns `None`, which `parser.py`
turns into a silent "unrecognized type, file ignored" warning, not an
error — so this gap was invisible without directly tracing the
classifier). Reusing that pipeline for FMS-07..18 would need touching
`fms_import`'s own filename-hint table for an unrelated, non-ZIP corpus
— this module instead reads the real file directly off the server
filesystem (exactly the same trust boundary `kor_canonical.import_
pipeline`/`klt_canonical.import_pipeline` already read `docs/kor/`,
docs/klt/` from), scoped ONLY to the one file type needed to close the
rubric/grading gap. A full FMS-07..18 resource-classification/progress-
tracking package (mirroring `kor_canonical`/`klt_canonical` in full) is
real, disclosed follow-on work — not attempted here.

**Format verified across all 9 real files** (`docs/fms/fms{07,08,09,
10,11,12,13,15,18}/ASSESSMENT_AND_RUBRIC.md`) before writing this
parser: every one carries an identical structure —
  `## Compétences évaluées` — a 2-column table (`| Compétence |
  Description |`) naming each competency (C1, C2, ... — always the
  formation's real, formation-specific competency list, 3 or 4 rows
  depending on the formation);
  `## Rubric (0–4 par compétence)` — a SHARED 0-4 level-meaning table
  (`| Niveau | Description |`), the same generic scale text applied to
  every competency, not a per-criterion threshold the way KOR/KLT's
  own rubrics carry one;
  `## Règle éliminatoire` — formation-specific prose;
  `## Seuil de passage` — every one of the 9 files states the identical
  `"Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination."` — i.e.
  the global pass rule already states outright that EVERY competency is
  eliminatory-if-zero (unlike KOR/KLT, which mark eliminatory status
  per-row); there is no per-competency "eliminatory: yes/no" distinction
  to parse here because the document itself makes it universal.

**What is deliberately NOT attempted** (disclosed, not silently worked
around) — same two exclusions the KOR/KLT parsers already disclose, for
the same reasons: no per-criterion "Seuil" text import (none exists
here — the 0-4 scale is shared, not per-criterion), no `skill_id`
linkage (`docs/fms/CERTIFICATION_MODEL.md` reserves `FMS0X.SKILL.*`/
`FMS0X.SPEC.*` namespaces but does not name a specific ID per
competency row — fuzzy-matching free text to a reserved namespace would
be an invented correlation).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional

from certification.models import RubricCriterion, RubricInput
from db import db, utc_now_iso

# The 9 real formations confirmed (by filesystem sweep) to have a built
# docs/fms/fmsXX/ directory with an ASSESSMENT_AND_RUBRIC.md. FMS-14/16/17
# are named in docs/fms/CERTIFICATION_MODEL.md's "FMS-07→18" range but do
# not yet exist as built directories — never assumed present.
FMS_SPEC_FORMATION_CODES: List[str] = [
    "FMS-07",
    "FMS-08",
    "FMS-09",
    "FMS-10",
    "FMS-11",
    "FMS-12",
    "FMS-13",
    "FMS-15",
    "FMS-18",
]

_DOCS_FMS_ROOT = Path(__file__).resolve().parents[2] / "docs" / "fms"

# Matches one real competency row, e.g.:
#   | C1 | Session lifecycle réel (statuts, transitions valides, rejet serveur) |
# under the "## Compétences évaluées" heading. Requires the id cell to
# start with "C" + digits so it never accidentally matches the sibling
# "## Rubric (0–4 par compétence)" table's `| Niveau | Description |`
# rows (whose first cell is a bare digit 0-4, not "Cn").
_COMPETENCY_ROW_RE = re.compile(r"^\|\s*(C\d+)\s*\|(.+)\|\s*$")

# The one real global threshold every one of the 9 real files states
# (verified, see module docstring), identical to KOR's/KLT's own 2,5/4
# threshold — reusing the same numeric value, not a coincidence: all
# three domains share the real 0-4 Rubric Master doctrine
# (`certification/models.py`'s own docstring).
FMS_SPEC_RUBRIC_PASS_THRESHOLD_PCT = 62.5  # 2.5 / 4.0 * 100

# Defensive check (see import_rubric_for_formation): every real file
# states this exact global rule. A future FMS-14/16/17 file that omits
# it, or states a different threshold, should surface loudly rather
# than silently import a wrong pass_threshold_pct.
_SEUIL_MARKER_RE = re.compile(r"2[.,]5\s*/\s*4")


def parse_rubric_criteria(body_markdown: str) -> List[RubricCriterion]:
    """Pure parse — no I/O. Every named competency becomes one
    `RubricCriterion`, `is_eliminatory=True` on all of them — the
    document's own "Seuil de passage" line ("aucune compétence à 0 par
    élimination") makes this universal, not a per-row distinction to
    infer. Returns criteria in the real document's own order; a body
    that doesn't match this convention yields an empty list rather than
    raising, so a caller can report 0 criteria honestly."""
    criteria: List[RubricCriterion] = []
    in_competency_table = False
    for line in body_markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("## Compétences évaluées"):
            in_competency_table = True
            continue
        if in_competency_table and stripped.startswith("## "):
            break
        if not in_competency_table:
            continue
        m = _COMPETENCY_ROW_RE.match(stripped)
        if not m:
            continue
        comp_id, label = m.groups()
        label = label.strip()
        if comp_id == "Compétence" or label == "Description":
            continue  # header row
        criteria.append(
            RubricCriterion(
                id=comp_id,
                label=label,
                bloc="A01",
                skill_id=None,
                weight=1.0,
                max_score=4.0,
                is_eliminatory=True,
            )
        )
    return criteria


def certification_code_for(formation_code: str) -> str:
    """ "FMS-09" -> "FMS09-A01" — the same convention `kor_canonical`/
    `klt_canonical` already use for their own one-flat-pass
    certifications; the real files here don't state a `# FMSxx-A01`
    heading themselves (they open with a plain title,
    e.g. "# FMS-09 — Assessment & Rubric"), so this is derived, not
    read off the document — kept identical to the sibling domains'
    convention rather than inventing a new one."""
    return f"{formation_code.replace('-', '')}-A01"


async def import_rubric_for_formation(formation_code: str) -> Optional[RubricInput]:
    """Reads the real `docs/fms/fmsXX/ASSESSMENT_AND_RUBRIC.md` file
    directly off the server filesystem — there is no `db.fms_resources`
    entry for it to read instead (see module docstring for why) — parses
    it, and upserts a real `Rubric` into `db.certification_rubrics`, the
    same collection/shape every other domain's imported rubric uses.

    Returns the `RubricInput` actually written, or `None` if
    `formation_code` is not one of the 9 real FMS-07..18 formations that
    have a built `ASSESSMENT_AND_RUBRIC.md` (including a formation code
    outside FMS-07..18 entirely) — the caller decides whether that's an
    error.
    """
    if formation_code not in FMS_SPEC_FORMATION_CODES:
        return None

    num = formation_code.split("-")[-1]
    path = _DOCS_FMS_ROOT / f"fms{num}" / "ASSESSMENT_AND_RUBRIC.md"
    if not path.exists():
        return None

    body = path.read_text(encoding="utf-8")
    if not _SEUIL_MARKER_RE.search(body):
        raise ValueError(
            f"{formation_code}: ASSESSMENT_AND_RUBRIC.md ne contient pas le "
            f"seuil global attendu (2,5/4) — import refusé plutôt que "
            f"silencieusement incorrect."
        )

    criteria = parse_rubric_criteria(body)
    rubric_input = RubricInput(
        level="A01",
        formation_code=formation_code,
        version="1.0",
        pass_threshold_pct=FMS_SPEC_RUBRIC_PASS_THRESHOLD_PCT,
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

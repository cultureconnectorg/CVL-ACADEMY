"""ACA-0020 — real N1/N2/A01 assessment-chain runtime binding for
canonical FREK (FRK-01..75) formations.

**The gap this closes**: same shape as KOR/KLT/FMS-07..18 — `start_
attempt`'s `get_rubric(certification_code)` would 404 for any FRK
formation, since zero `Rubric` documents ever existed for this domain,
even though `frk_canonical`'s own filesystem-native import pipeline
already persists every real `docs/frk/frkNN/ASSESSMENT_AND_RUBRIC.md`
into `db.frk_resources` with `type="assessment_and_rubric"` (unlike
FMS-07..18, whose files `fms_import`'s classifier didn't recognize —
`frk_canonical/parser.py`'s own filename table maps the exact filename
`"ASSESSMENT_AND_RUBRIC.md"` to `"assessment_and_rubric"` already, so
this module reads `db.frk_resources`, the same as KOR/KLT, not the raw
filesystem).

**Real corpus shape, verified across all 57 real files with a built
`ASSESSMENT_AND_RUBRIC.md` before writing this parser** — this domain
is genuinely more heterogeneous than KOR/KLT/FMS-07..18, and this
parser is written against what was actually found, not one assumed
template:

1. **Named-competency shape** (16/57 files — some carry an explicit
   `## Compétences évaluées` heading, others go straight from the
   intro line into the same `| Cn | Description |` table with no
   heading at all). Parsed identically either way: this module scans
   every line for a `| Cn | ... |` row rather than gating on a
   heading, since the row shape itself is what's unambiguous (the
   sibling `| Niveau | Description |` table's first cell is always a
   bare digit 0-4, never `Cn`, so this can never cross-match).
2. **Single global grille shape** (41/57 files, the majority — e.g.
   `docs/frk/frk23/ASSESSMENT_AND_RUBRIC.md`) — no named competency
   list at all, just one shared `## Grille (0–4)` table applying to
   the whole formation. There is nothing to name multiple criteria
   from, so this becomes exactly **one** `RubricCriterion`
   (`id="C1"`, a generic-but-honest label — never inventing a
   specific competency name the document doesn't state).
3. **Explicitly non-certifiable / formative-only formations** (3/57
   real files — FRK-10, FRK-14, FRK-73 — confirmed by grep sweep, not
   assumed rare) state outright that no certification can be
   administered yet (`"NEEDS_EXPERT_REVIEW"`, `"formatif seul"`,
   `"inapplicable aujourd'hui"`) pending a named human expert review.
   Importing a live, gradable `Rubric` for one of these would
   contradict the document's own stated status, so
   `import_rubric_for_formation` refuses (returns `None`) for any
   formation whose body matches this marker — checked BEFORE parsing,
   regardless of which of the two shapes above the file otherwise
   uses.

**What is deliberately NOT attempted** — same two exclusions KOR/KLT/
FMS-07..18 already disclose, for the same reasons: no per-criterion
"Seuil" text import, no `skill_id` linkage (`docs/frk/` reserves
`FRK0X.SKILL.*`-style namespaces per formation without naming a
specific ID per competency row).
"""

from __future__ import annotations

import re
from typing import List, Optional

from certification.models import RubricCriterion, RubricInput
from db import db, utc_now_iso
from frk_canonical.models import FRK_FORMATION_CODES

# Matches a real named-competency row, e.g.:
#   | C1 | Littératie DID/VC W3C |
# Deliberately unanchored to any heading — see module docstring point 1.
_COMPETENCY_ROW_RE = re.compile(r"^\|\s*(C\d+)\s*\|(.+)\|\s*$")

# The single global grille shape carries a "## Grille..." heading
# ("Grille (0–4)", "Grille indicative (0–4, usage formatif)", ...) with
# no per-competency breakdown.
_GRILLE_HEADING_RE = re.compile(r"^#{1,3}\s*Grille", re.MULTILINE)

# The one real global threshold every parseable real file states —
# identical value to KOR/KLT/FMS-07..18 (2,5 on the shared 0-4 Rubric
# Master scale), wording varies ("Moyenne ≥ 2.5/4, ..." vs "**Seuil de
# passage :** ≥2.5/4.") but the numeric marker itself never does.
_SEUIL_MARKER_RE = re.compile(r"2[.,]5\s*/\s*4")

# The real, verified marker for "this formation cannot be certified
# yet" (FRK-10/14/73) — checked before any parsing is attempted, so a
# formative-only formation can never accidentally get a live gradable
# Rubric just because its table happens to parse cleanly.
_NOT_CERTIFIABLE_RE = re.compile(
    r"NEEDS_EXPERT_REVIEW|formatif seul|inapplicable aujourd.hui|"
    r"pas de certification",
    re.IGNORECASE,
)

FRK_RUBRIC_PASS_THRESHOLD_PCT = 62.5  # 2.5 / 4.0 * 100


def parse_rubric_criteria(body_markdown: str) -> List[RubricCriterion]:
    """Pure parse — no I/O, and deliberately does not itself check the
    non-certifiable marker (that's `import_rubric_for_formation`'s job,
    so this function stays a plain "what does this text parse to").
    Tries the named-competency shape first; falls back to the single
    global grille shape (exactly one criterion) if no competency rows
    are found but a `## Grille...` heading is present; returns an empty
    list if the body matches neither real shape, so a caller can report
    0 criteria honestly rather than guessing."""
    criteria: List[RubricCriterion] = []
    for line in body_markdown.splitlines():
        m = _COMPETENCY_ROW_RE.match(line.strip())
        if not m:
            continue
        comp_id, label = m.groups()
        label = label.strip()
        if comp_id == "Compétence" or label == "Description":
            continue  # header row, in the rare file lacking a blank divider
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
    if criteria:
        return criteria

    if _GRILLE_HEADING_RE.search(body_markdown):
        return [
            RubricCriterion(
                id="C1",
                label=(
                    "Grille globale de la formation (0-4) — le document ne "
                    "nomme pas de compétences distinctes, un seul critère "
                    "couvre l'ensemble de l'évaluation"
                ),
                bloc="A01",
                skill_id=None,
                weight=1.0,
                max_score=4.0,
                is_eliminatory=True,
            )
        ]
    return []


def certification_code_for(formation_code: str) -> str:
    """ "FRK-09" -> "FRK09-A01" — same convention KOR/KLT/FMS-07..18
    already use for a one-flat-pass certification."""
    return f"{formation_code.replace('-', '')}-A01"


async def import_rubric_for_formation(formation_code: str) -> Optional[RubricInput]:
    """Reads the real `type="assessment_and_rubric"` resource already
    stored for `formation_code` in `db.frk_resources` (persisted by
    `frk_canonical.import_pipeline` — this function never reads the
    filesystem itself), parses it, and upserts a real `Rubric` into
    `db.certification_rubrics`.

    Returns `None` in three real, distinct cases the caller cannot
    currently tell apart (documented, not silently conflated into a
    single misleading message — see `api/frk_canonical.py`'s own error
    text): no `assessment_and_rubric` resource exists yet for this
    formation (not imported, or genuinely has none); the resource
    exists but explicitly states it is formative-only / not yet
    certifiable (FRK-10/14/73 today); or the resource exists but its
    body matches neither real parseable shape.
    """
    if formation_code not in FRK_FORMATION_CODES:
        return None

    resource = await db.frk_resources.find_one(
        {"formation_code": formation_code, "type": "assessment_and_rubric"},
        {"_id": 0},
    )
    if not resource:
        return None

    body = resource.get("body_markdown", "")
    if _NOT_CERTIFIABLE_RE.search(body):
        return None

    if not _SEUIL_MARKER_RE.search(body):
        raise ValueError(
            f"{formation_code}: assessment_and_rubric ne contient pas le "
            f"seuil global attendu (2,5/4) — import refusé plutôt que "
            f"silencieusement incorrect."
        )

    criteria = parse_rubric_criteria(body)
    if not criteria:
        return None

    rubric_input = RubricInput(
        level="A01",
        formation_code=formation_code,
        version="1.0",
        pass_threshold_pct=FRK_RUBRIC_PASS_THRESHOLD_PCT,
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

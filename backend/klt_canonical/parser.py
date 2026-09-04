"""Pure, read-only parsing of the real `docs/klt/kltXX/` file
conventions — established across KLT-0004 (KLT-01) through KLT-0011
(KLT-08) and verified identical in every module header block this
session wrote. No network, no DB access; every function here takes text
in and returns structured data out.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional

MODULE_FILENAME_RE = re.compile(r"^M(\d{2})_")
FORMATION_DIR_RE = re.compile(r"^klt(\d{2})/")

# The fenced header block every module carries, e.g.:
#   MODULE_ID: KLT06-M01
#   COMPETENCY_ID: C1 — Comprendre l'objet et la méthode d'un observatoire...
#   PREREQUISITES: aucun
#   ASSESSMENT_LEVEL: N1
#   KILTIKONET_DEPENDENCY: Observatory — NOT_CONNECTED...
#   ROLE_BOUNDARIES: ...
#   FREK_PROOF_MAPPING: ...
#   ORIGIN: ...
_HEADER_FIELD_RE = re.compile(
    r"^(MODULE_ID|COMPETENCY_ID|PREREQUISITES|ASSESSMENT_LEVEL|"
    r"KILTIKONET_DEPENDENCY|ROLE_BOUNDARIES|FREK_PROOF_MAPPING|ORIGIN):\s*(.*)$"
)

_TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
# "# KLT-06 — M01 — Qu'est-ce qu'un observatoire..." -> module title only.
_MODULE_TITLE_SPLIT_RE = re.compile(r"^KLT-?\d{2}\s*—\s*M\d{2}\s*—\s*(.+)$")


def formation_code_from_path(relative_path: str) -> Optional[str]:
    """ "klt06/modules/M01_x.md" -> "KLT-06". None if the path isn't
    rooted under a kltNN/ directory."""
    m = FORMATION_DIR_RE.match(relative_path)
    return f"KLT-{m.group(1)}" if m else None


def module_number_from_filename(filename: str) -> Optional[str]:
    m = MODULE_FILENAME_RE.match(filename)
    return f"M{m.group(1)}" if m else None


def classify_resource_type(relative_path: str) -> Optional[str]:
    """Classifies a real docs/klt/kltXX/... file by its path convention.
    Returns None for a path this convention doesn't recognize (e.g. the
    top-level README.md, or MODULES_STATUS.md, which is real but not a
    learner/staff resource) — the caller records that as
    unparsed_no_type_match, never drops it silently."""
    parts = relative_path.split("/")
    if len(parts) < 2 or not FORMATION_DIR_RE.match(relative_path):
        return None
    tail = "/".join(parts[1:])
    filename = parts[-1]

    if tail.startswith("modules/") and MODULE_FILENAME_RE.match(filename):
        return "module"
    if tail.startswith("modules/MODULES_STATUS.md"):
        return "modules_status"
    if tail.startswith("case/CAS_FIL_ROUGE.md"):
        return "case_fil_rouge"
    if tail.startswith("case/CAS_ANGLE"):
        return "case_angle"
    if tail.startswith("case/CASE_COMPETENCY_MATRIX.md"):
        return "case_competency_matrix"
    if tail.startswith("assessments/N1_QUESTION_BANK.md"):
        return "n1_question_bank"
    if tail.startswith("assessments/N2_EVALUATIONS.md"):
        return "n2_evaluations"
    if tail.startswith("assessments/") and filename.startswith("A01"):
        return "certification_assessment"
    if tail.startswith("assessments/RUBRIC.md"):
        return "rubric"
    if tail.startswith("skills/SKILL_ID_REGISTRY.md"):
        return "skill_id_registry"
    if tail.startswith("skills/EVIDENCE_MODEL.md"):
        return "evidence_model"
    if tail.startswith("guides/CANDIDATE_GUIDE.md"):
        return "candidate_guide"
    if tail.startswith("guides/CORRECTOR_GUIDE.md"):
        return "corrector_guide"
    if tail.startswith("guides/JURY_GUIDE.md"):
        return "jury_guide"
    if tail.startswith("templates/TEMPLATES.md"):
        return "templates"
    if tail in ("00_REFERENTIEL_ET_BLUEPRINTS.md", "00_BLUEPRINTS.md"):
        return "referentiel_blueprints"
    if tail == "CERTIFICATION_MODEL.md":
        return "certification_model"
    if tail == "INTEGRATION_ACADEMY_PACKAGE_NOTE.md":
        return "integration_note"
    if tail == "QUALITY_GATES.md":
        return "quality_gates"
    return None


def extract_module_title(text: str) -> Optional[str]:
    m = _TITLE_RE.search(text)
    if not m:
        return None
    heading = m.group(1)
    split = _MODULE_TITLE_SPLIT_RE.match(heading)
    return split.group(1) if split else heading


def extract_module_header(text: str) -> Dict[str, str]:
    """Parses the fenced ```...``` block's `KEY: value` lines. Only
    fields the real convention defines are ever returned — an unknown
    key inside the fence (should never happen, confirmed identical
    across all 76 real module files this session wrote) is ignored, not
    guessed at."""
    fields: Dict[str, str] = {}
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "```":
            if in_fence:
                break  # end of the header fence
            in_fence = True
            continue
        if not in_fence:
            continue
        m = _HEADER_FIELD_RE.match(stripped)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def parse_module_file(relative_path: str, text: str) -> Dict[str, Optional[str]]:
    header = extract_module_header(text)
    competency_raw = header.get("COMPETENCY_ID", "")
    competency_id, _, competency_label = competency_raw.partition("—")
    return {
        "module_code": header.get("MODULE_ID"),
        "title": extract_module_title(text),
        "competency_id": competency_id.strip() or None,
        "competency_label": competency_label.strip() or None,
        "prerequisites_raw": header.get("PREREQUISITES"),
        "assessment_level": header.get("ASSESSMENT_LEVEL"),
        "kiltikonet_dependency": header.get("KILTIKONET_DEPENDENCY"),
        "role_boundaries": header.get("ROLE_BOUNDARIES"),
        "frek_proof_mapping": header.get("FREK_PROOF_MAPPING"),
        "origin": header.get("ORIGIN"),
        "content_markdown": text,
    }


# Skill registry table rows — two real shapes exist in this repo:
#   5 columns (KLT-01..05, every skill BUILT, no status column):
#     | `KLT01.SKILL.C01` | Compétence | Module | Assessment | Evidence |
#   6 columns (KLT-06..08, partial, explicit status column):
#     | `KLT06.SKILL.C01` | Compétence | Module | Assessment | Evidence | `BUILT` |
#     | `KLT06.SKILL.C05` | Compétence | Module | — | — | `BLOCKED` — non construit |
_SKILL_ROW_START_RE = re.compile(r"^\|\s*`(KLT\d{2}\.SKILL\.[A-Za-z0-9]+)`\s*\|")
_MODULE_CELL_RE = re.compile(r"^M\d{2}$")


def parse_skill_registry(text: str) -> List[Dict[str, Optional[str]]]:
    """Returns one dict per real skill row: skill_id, label, module_code,
    status ("BUILT" unless some cell literally carries the `BLOCKED`
    marker), blocked_reason. Splits each row on `|` directly (robust to
    trailing-pipe/no-trailing-pipe variation) rather than trying to
    regex-match a fixed column count, since the real registries use two
    different column counts (5 for KLT-01..05, 6 for KLT-06..08)."""
    rows: List[Dict[str, Optional[str]]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not _SKILL_ROW_START_RE.match(stripped):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 3:
            continue
        skill_id = cells[0].strip("` ")
        label = cells[1].strip("` ")
        module_code = cells[2] if _MODULE_CELL_RE.match(cells[2]) else None

        status = "BUILT"
        reason: Optional[str] = None
        for cell in cells[3:]:
            if "`BLOCKED`" in cell:
                status = "BLOCKED"
                _, _, tail = cell.partition("`BLOCKED`")
                reason = tail.lstrip(" —-").strip() or None
                break
            if "`BUILT`" in cell:
                status = "BUILT"
                break

        rows.append(
            {
                "skill_id": skill_id,
                "label": label,
                "module_code": module_code,
                "status": status,
                "blocked_reason": reason,
            }
        )
    return rows

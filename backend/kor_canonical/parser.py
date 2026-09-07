"""Pure, read-only parsing of the real `docs/kor/korXX/` file
conventions — established across KOR-0003 (KOR-01) and confirmed
identical in every module header block and skill registry this session
read (KOR-01, KOR-02, KOR-03 spot-checked). No network, no DB access;
every function here takes text in and returns structured data out.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional

MODULE_FILENAME_RE = re.compile(r"^M(\d{2})_")
FORMATION_DIR_RE = re.compile(r"^kor(\d{2})/")

# The fenced header block every module carries, e.g.:
#   MODULE_ID: KOR01-M04
#   COMPETENCY_ID: C4 — Préparer et conduire une interview adaptée
#   PREREQUISITES: M03
#   ASSESSMENT_LEVEL: N2
#   KORA_DEPENDENCY: aucune
#   ROLE_BOUNDARIES: ...
#   FREK_PROOF_MAPPING: ...
#   ORIGIN: ...
_HEADER_FIELD_RE = re.compile(
    r"^(MODULE_ID|COMPETENCY_ID|PREREQUISITES|ASSESSMENT_LEVEL|"
    r"KORA_DEPENDENCY|ROLE_BOUNDARIES|FREK_PROOF_MAPPING|ORIGIN):\s*(.*)$"
)

_TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
# "# KOR-01 — M04 — Conduire une interview" -> module title only.
_MODULE_TITLE_SPLIT_RE = re.compile(r"^KOR-?\d{2}\s*—\s*M\d{2}\s*—\s*(.+)$")


def extract_heading_title(text: str) -> Optional[str]:
    """The raw `# ...` H1 heading of any real docs/kor/ file, unsplit —
    used for every non-module resource type (module files get the
    further module-specific split in `extract_module_title`)."""
    m = _TITLE_RE.search(text)
    return m.group(1) if m else None


# A bare prerequisite value is always exactly one prior module number in
# this corpus (confirmed across all 14 KOR-01 module files this
# session): "Aucun" (no prerequisite) or "M03" (never "KOR01-M03", never
# a French phrase, never more than one module).
_BARE_MODULE_RE = re.compile(r"^(M\d{2})$")


def formation_code_from_path(relative_path: str) -> Optional[str]:
    """ "kor01/modules/M01_x.md" -> "KOR-01". None if the path isn't
    rooted under a korNN/ directory."""
    m = FORMATION_DIR_RE.match(relative_path)
    return f"KOR-{m.group(1)}" if m else None


def module_number_from_filename(filename: str) -> Optional[str]:
    m = MODULE_FILENAME_RE.match(filename)
    return f"M{m.group(1)}" if m else None


def canonical_module_code(formation_code: str, module_number: str) -> str:
    """ "KOR-01", "M04" -> "KOR01-M04" — the exact convention each real
    module's own MODULE_ID header field already uses (no dash after the
    métier number, matching FMS's and Kiltikonet's convention)."""
    metier_no = formation_code.split("-")[-1]
    return f"KOR{metier_no}-{module_number}"


def resolve_prerequisite_module_code(
    formation_code: str, prerequisites_raw: Optional[str]
) -> Optional[str]:
    """"Aucun" -> None. "M03" -> "KOR01-M03" (this module's own
    formation). Any other free text -> None, never guessed — this
    corpus's real convention never uses free text here, so a value that
    doesn't match is either a genuine gap or a future format this parser
    hasn't been taught yet; both cases must surface as "unresolved", not
    a fabricated dependency."""
    if not prerequisites_raw:
        return None
    text = prerequisites_raw.strip()
    if text.lower() == "aucun":
        return None
    m = _BARE_MODULE_RE.match(text)
    if not m:
        return None
    return canonical_module_code(formation_code, m.group(1))


def classify_resource_type(relative_path: str) -> Optional[str]:
    """Classifies a real docs/kor/korXX/... file by its path convention.
    Returns None for a path this convention doesn't recognize — the
    caller records that as unparsed_no_type_match, never drops it
    silently. Deliberately conservative: only the exact filenames this
    session confirmed real in KOR-01 are matched; a formation using a
    different real filename (e.g. KOR-03's `REFERENTIAL.md`, `case/
    CASE.md`) is left unmatched rather than guessed at, since only
    KOR-01 has been driven end-to-end through this runtime binding."""
    parts = relative_path.split("/")
    if len(parts) < 2 or not FORMATION_DIR_RE.match(relative_path):
        return None
    tail = "/".join(parts[1:])
    filename = parts[-1]

    if tail.startswith("modules/") and MODULE_FILENAME_RE.match(filename):
        return "module"
    if tail.startswith("case/CAS_FIL_ROUGE.md"):
        return "case_fil_rouge"
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
    if tail == "00_BLUEPRINTS.md":
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
    fields the real convention defines are ever returned."""
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
    formation_code = formation_code_from_path(relative_path)
    prerequisites_raw = header.get("PREREQUISITES")
    prerequisite_module_code = (
        resolve_prerequisite_module_code(formation_code, prerequisites_raw)
        if formation_code
        else None
    )
    return {
        "module_code": header.get("MODULE_ID"),
        "title": extract_module_title(text),
        "competency_id": competency_id.strip() or None,
        "competency_label": competency_label.strip() or None,
        "prerequisites_raw": prerequisites_raw,
        "prerequisite_module_code": prerequisite_module_code,
        "assessment_level": header.get("ASSESSMENT_LEVEL"),
        "kora_dependency": header.get("KORA_DEPENDENCY"),
        "role_boundaries": header.get("ROLE_BOUNDARIES"),
        "frek_proof_mapping": header.get("FREK_PROOF_MAPPING"),
        "origin": header.get("ORIGIN"),
        "content_markdown": text,
    }


# Skill registry table rows — the one real shape confirmed across
# KOR-01/02/03's own SKILL_ID_REGISTRY.md (5 columns, no BUILT/BLOCKED
# status column — unlike KLT-06/07/08):
#   | `KOR01.SKILL.C04` | Compétence | M04 | N2 (`E-N2-02`) | Evidence text |
_SKILL_ROW_START_RE = re.compile(r"^\|\s*`(KOR\d{2}\.SKILL\.[A-Za-z0-9]+)`\s*\|")
_MODULE_CELL_RE = re.compile(r"^M\d{2}$")


def parse_skill_registry(text: str) -> List[Dict[str, Optional[str]]]:
    """Returns one dict per real skill row: skill_id, label,
    module_code_raw (bare "M04", never converted here — conversion needs
    the formation code, which read_model.py already has in context),
    assessment_ref_raw, evidence_expected. Splits each row on `|`
    directly (robust to trailing-pipe/no-trailing-pipe variation)."""
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
        module_code_raw = cells[2] if _MODULE_CELL_RE.match(cells[2]) else None
        assessment_ref_raw = cells[3] if len(cells) > 3 and cells[3] else None
        evidence_expected = cells[4] if len(cells) > 4 and cells[4] else None

        rows.append(
            {
                "skill_id": skill_id,
                "label": label,
                "module_code_raw": module_code_raw,
                "assessment_ref_raw": assessment_ref_raw,
                "evidence_expected": evidence_expected,
            }
        )
    return rows

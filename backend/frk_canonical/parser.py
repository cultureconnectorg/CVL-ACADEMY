"""Pure, read-only parsing of the real `docs/frk/frkNN/` file
conventions — spot-checked across frk01 (best-grounded flagship),
frk10 (NEEDS_EXPERT_REVIEW), frk16 (post-pass reclassification) and
frk58 this session. No network, no DB access; every function here
takes text in and returns structured data out.
"""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

FORMATION_DIR_RE = re.compile(r"^frk(\d{2})/")
_TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)

# "# FRK-01 — FREK Foundations & Cultural Trust Infrastructure (umbrella,
# flagship)" -> "FREK Foundations & Cultural Trust Infrastructure
# (umbrella, flagship)". Real heading shape, confirmed across frk01/
# frk10/frk58. Falls back to the raw heading when it doesn't split
# cleanly — never fabricated.
_FORMATION_TITLE_SPLIT_RE = re.compile(r"^FRK-?\d{2}\s*—\s*(.+)$")

_SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

_STATUS_RE = re.compile(r"STATUS\s*=\s*([A-Z_]+)")

# "1. **Title** — description..." or "1. Plain sentence." — both real
# shapes confirmed (frk01 uses the former, frk10 the latter).
_MODULE_ITEM_START_RE = re.compile(r"^(\d+)\.\s+(.*)$")
_MODULE_BOLD_SPLIT_RE = re.compile(r"^\*\*(.+?)\*\*\s*(?:[—-]\s*)?(.*)$")


def formation_code_from_path(relative_path: str) -> Optional[str]:
    """ "frk01/REFERENTIAL.md" -> "FRK-01". None if the path isn't
    rooted under a frkNN/ directory."""
    m = FORMATION_DIR_RE.match(relative_path)
    return f"FRK-{m.group(1)}" if m else None


def canonical_module_code(formation_code: str, order_index: int) -> str:
    """ "FRK-01", 1 -> "FRK01-M01" — same "no dash after the number"
    convention FMS/KLT/KOR canonical module codes already use."""
    metier_no = formation_code.split("-")[-1]
    return f"FRK{metier_no}-M{order_index:02d}"


def classify_resource_type(relative_path: str) -> Optional[str]:
    """Classifies a real docs/frk/frkNN/... file by its exact, confirmed
    filename convention (flat — no subdirectories, unlike KOR/KLT).
    Returns None for a path this convention doesn't recognize — the
    caller records that as unparsed_no_type_match, never drops it
    silently."""
    parts = relative_path.split("/")
    if len(parts) != 2 or not FORMATION_DIR_RE.match(relative_path):
        return None
    filename = parts[-1]

    return {
        "REFERENTIAL.md": "referential",
        "BANQUE_N1.md": "n1_question_bank",
        "BANQUE_N2.md": "n2_evaluations",
        "ASSESSMENT_AND_RUBRIC.md": "assessment_and_rubric",
        "EVIDENCE_MODEL.md": "evidence_model",
        "GUIDE_CANDIDAT.md": "candidate_guide",
        "GUIDE_CORRECTEUR.md": "corrector_guide",
        "GUIDE_JURY.md": "jury_guide",
        "INTEGRATION_NOTE.md": "integration_note",
        "GAP.md": "gap",
    }.get(filename)


def extract_heading_title(text: str) -> Optional[str]:
    """The raw `# ...` H1 heading of any real docs/frk/ file, unsplit."""
    m = _TITLE_RE.search(text)
    return m.group(1) if m else None


def extract_formation_title(text: str) -> Optional[str]:
    m = _TITLE_RE.search(text)
    if not m:
        return None
    heading = m.group(1)
    split = _FORMATION_TITLE_SPLIT_RE.match(heading)
    return split.group(1) if split else heading


def _section_text(text: str, heading: str) -> Optional[str]:
    """Raw text between "## {heading}" and the next "## " heading (or
    EOF), whitespace-normalized (line breaks collapsed to single
    spaces, matching how this corpus wraps prose at ~72 columns —
    never meant as separate lines). None if the section isn't present
    at all."""
    sections = list(_SECTION_RE.finditer(text))
    for i, m in enumerate(sections):
        if m.group(1).strip().lower() != heading.lower():
            continue
        start = m.end()
        end = sections[i + 1].start() if i + 1 < len(sections) else len(text)
        body = text[start:end].strip()
        if not body:
            return None
        # Collapse soft-wrapped lines into one flowing string, but keep
        # numbered-list item boundaries (used by parse_modules_section
        # separately, on the unflattened text) — this helper is only
        # used for prose sections (Prerequisites/Objectives/Assessment).
        lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
        return " ".join(lines)
    return None


def extract_prerequisites(text: str) -> Optional[str]:
    return _section_text(text, "Prerequisites")


def extract_objectives(text: str) -> Optional[str]:
    return _section_text(text, "Objectives")


def extract_assessment_summary(text: str) -> Optional[str]:
    return _section_text(text, "Assessment")


def extract_status(text: str) -> Tuple[Optional[str], bool]:
    """Returns (status, needs_expert_review). `needs_expert_review` is
    True whenever the literal token `NEEDS_EXPERT_REVIEW` appears
    anywhere in the "## Status" section — real corpus convention
    confirmed on FRK-10/14/73."""
    body = _section_text(text, "Status")
    if not body:
        return None, False
    m = _STATUS_RE.search(body)
    status = m.group(1) if m else None
    return status, "NEEDS_EXPERT_REVIEW" in body


def parse_modules_section(text: str) -> List[dict]:
    """The real "## Modules" numbered list -> one dict per item
    (order_index, title, description, raw_text). Handles both real
    shapes this corpus uses: "N. **Title** — description" (frk01/frk58)
    and "N. Plain sentence." (frk10) — the latter's whole sentence
    becomes `title`, `description=None`, never invented."""
    sections = list(_SECTION_RE.finditer(text))
    body = None
    for i, m in enumerate(sections):
        if m.group(1).strip().lower() != "modules":
            continue
        start = m.end()
        end = sections[i + 1].start() if i + 1 < len(sections) else len(text)
        body = text[start:end]
        break
    if body is None:
        return []

    items: List[Tuple[int, List[str]]] = []
    current_index: Optional[int] = None
    current_lines: List[str] = []
    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        item_match = _MODULE_ITEM_START_RE.match(line.strip())
        if item_match:
            if current_index is not None:
                items.append((current_index, current_lines))
            current_index = int(item_match.group(1))
            current_lines = [item_match.group(2).strip()]
        elif line.strip() and current_index is not None:
            current_lines.append(line.strip())
    if current_index is not None:
        items.append((current_index, current_lines))

    results: List[dict] = []
    for order_index, lines in items:
        raw_text = " ".join(lines).strip()
        bold = _MODULE_BOLD_SPLIT_RE.match(raw_text)
        if bold:
            title = bold.group(1).strip()
            description = bold.group(2).strip() or None
        else:
            title = raw_text
            description = None
        results.append(
            {
                "order_index": order_index,
                "title": title,
                "description": description,
                "raw_text": raw_text,
            }
        )
    return results


def parse_referential(relative_path: str, text: str) -> dict:
    formation_code = formation_code_from_path(relative_path)
    status, needs_expert_review = extract_status(text)
    return {
        "formation_code": formation_code,
        "title": extract_formation_title(text),
        "status": status,
        "needs_expert_review": needs_expert_review,
        "prerequisites": extract_prerequisites(text),
        "objectives": extract_objectives(text),
        "assessment_summary": extract_assessment_summary(text),
        "modules": parse_modules_section(text),
    }

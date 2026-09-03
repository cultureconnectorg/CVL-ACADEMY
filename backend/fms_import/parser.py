"""Markdown parser for FMS resource files — classifies from filename +
first heading (the real convention), never raises.

**Why filename-based, not frontmatter-based:** see models.py's module
docstring — reconciled against the real 225-file FMS ZIP, which carries no
frontmatter anywhere. Frontmatter parsing is kept as an optional
affordance (if a file *does* start with a `---` block, its `type:`/`code:`/
etc. still win over the filename inference) so nothing regresses if a
future file happens to use it, but nothing in the real archive relies on
it.

Never raises on malformed input — always returns a (resource_or_None,
issues) pair so a bad file in a 200+ file ZIP doesn't abort the whole
import (see importer.py).
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

import yaml

from .models import (
    FILENAME_TYPE_HINTS,
    METIER_LETTER_TO_FORMATION,
    FmsResource,
    FmsResourceType,
    ImportIssue,
)

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n?", re.DOTALL)

# Every type a filename hint can produce — also the set a legacy
# frontmatter `type:` value is validated against, so a garbage value can
# never reach FmsResource's Literal field and raise instead of warn.
VALID_TYPES = {rtype for _, rtype in FILENAME_TYPE_HINTS}

# Real files reference Skill IDs inline, in prose and in tables, always in
# this exact canonical form (see 27_FMS01_Skill_IDs_Registry.md: "FMS01-A1
# est l'identifiant canonique"). Collecting every occurrence is indexing —
# a literal substring already in the text — never fabrication.
SKILL_ID_RE = re.compile(r"\bFMS0\d-[A-F]\d+\b")

# FMS0<n> (module/métier) or FMS-<Lettre> (référentiel) anywhere in the
# filename — used to derive formation_code.
FORMATION_NUM_RE = re.compile(r"FMS[_-]?0?(\d)", re.IGNORECASE)
REFERENTIEL_LETTER_RE = re.compile(r"FMS[_-]([A-F])(?:[_-]|$)", re.IGNORECASE)

# Module number inside a filename, e.g. "..._M07_..." -> "M07".
MODULE_NUM_RE = re.compile(r"_M(\d{2})_", re.IGNORECASE)
# Certification number, e.g. "..._A01_..." -> "A01".
CERT_NUM_RE = re.compile(r"_A(\d{2})_", re.IGNORECASE)

VERSION_RE = re.compile(r"V(\d+(?:\.\d+)?)", re.IGNORECASE)


def _normalize_for_match(filename: str) -> str:
    stem = filename.rsplit("/", 1)[-1]
    stem = re.sub(r"\.md$", "", stem, flags=re.IGNORECASE)
    return re.sub(r"[^a-z0-9]+", "_", stem.lower()).strip("_")


def _split_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    match = FRONTMATTER_RE.match(content)
    if not match:
        return {}, content
    raw_yaml = match.group(1)
    body = content[match.end() :]
    try:
        parsed = yaml.safe_load(raw_yaml)
    except yaml.YAMLError:
        return {}, content
    return (parsed if isinstance(parsed, dict) else {}), body


def _infer_type(
    normalized: str, frontmatter_type: Optional[str]
) -> Optional[FmsResourceType]:
    if frontmatter_type and frontmatter_type in VALID_TYPES:
        return frontmatter_type  # type: ignore[return-value]
    for hint, rtype in FILENAME_TYPE_HINTS:
        if hint in normalized:
            return rtype  # type: ignore[return-value]
    return None


def _infer_formation_code(filename: str, rtype: Optional[str]) -> Optional[str]:
    """FMS01 -> FMS-01 ; FMS-A -> FMS-01 (via the gabarit's letter map).
    Cross-métier documents (index/gabarit/matrice_pedagogique) have none."""
    if rtype in ("index", "gabarit", "matrice_pedagogique"):
        return None
    letter_match = REFERENTIEL_LETTER_RE.search(filename)
    if letter_match:
        return METIER_LETTER_TO_FORMATION.get(letter_match.group(1).upper())
    num_match = FORMATION_NUM_RE.search(filename)
    if num_match:
        return f"FMS-{int(num_match.group(1)):02d}"
    return None


def _infer_code(
    filename: str,
    rtype: FmsResourceType,
    formation_code: Optional[str],
    frontmatter_code: Optional[str],
) -> str:
    if frontmatter_code:
        return str(frontmatter_code)

    module_match = MODULE_NUM_RE.search(filename)
    cert_match = CERT_NUM_RE.search(filename)

    if rtype == "module" and formation_code and module_match:
        return f"{formation_code}-M{module_match.group(1)}"
    if rtype == "blueprint" and formation_code and module_match:
        return f"{formation_code}-M{module_match.group(1)}-BLUEPRINT"

    # Everything else: <formation_or_none>-<TYPE-IN-CAPS>[-A0n], stable and
    # collision-free across a métier's ~30 non-module files — except the
    # one real case where a métier keeps both a superseded draft and its
    # locked version of the same document (observed once in the real
    # archive: FMS-01's A01 grille has both `..._Brouillon.md` and
    # `..._V1.md`) — the filename's own "Brouillon" marker is carried into
    # the code so it doesn't collide with, and isn't upserted over, the
    # locked version.
    type_slug = rtype.upper().replace("_", "-")
    parts = [formation_code] if formation_code else []
    if cert_match:
        parts.append(f"A{cert_match.group(1)}")
    parts.append(type_slug)
    if "brouillon" in filename.lower():
        parts.append("BROUILLON")
    return "-".join(p for p in parts if p) or _normalize_for_match(filename).upper()


def _infer_title(body: str, fallback: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.lstrip("#").strip()
    return fallback


def _infer_version(filename: str, body: str) -> str:
    match = VERSION_RE.search(filename) or VERSION_RE.search(body[:2000])
    return match.group(1) if match else "1.0"


def extract_skill_ids(body: str) -> List[str]:
    """Every canonical Skill ID (FMS0<n>-<Bloc><n>) mentioned in a
    document's body — for indexing/cross-linking, not curriculum authority."""
    return sorted(set(SKILL_ID_RE.findall(body)))


def parse_markdown_file(
    filename: str, content: str, import_id: str
) -> Tuple[Optional[FmsResource], List[ImportIssue]]:
    """Parse one Markdown file into an FmsResource. Returns issues instead
    of raising — a file that can't be classified becomes a warning, not a
    crash."""
    issues: List[ImportIssue] = []
    frontmatter, body = _split_frontmatter(content)
    normalized = _normalize_for_match(filename)

    rtype = _infer_type(normalized, frontmatter.get("type"))
    if rtype is None:
        issues.append(
            ImportIssue(
                level="warning",
                file=filename,
                message=(
                    "Type de ressource FMS non reconnu (aucun indice dans le nom "
                    "de fichier, pas de `type:` en frontmatter) — fichier ignoré."
                ),
            )
        )
        return None, issues

    formation_code = frontmatter.get("formation_code") or _infer_formation_code(
        filename, rtype
    )
    code = _infer_code(filename, rtype, formation_code, frontmatter.get("code"))
    title = _infer_title(body, fallback=frontmatter.get("title") or code)

    resource = FmsResource(
        import_id=import_id,
        source_file=filename,
        type=rtype,
        code=code,
        formation_code=formation_code,
        title=title,
        prerequisites=[],
        skill_ids=extract_skill_ids(body),
        version=frontmatter.get("version") or _infer_version(filename, body),
        frontmatter=frontmatter,
        body_markdown=body.strip(),
    )
    return resource, issues

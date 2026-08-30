"""Robust Markdown + YAML-frontmatter parser for FMS resource files.

Never raises on malformed input — always returns a (resource_or_None,
issues) pair so a bad file in a 200-file ZIP doesn't abort the whole
import (see importer.py).
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

import yaml

from .models import FILENAME_TYPE_HINTS, FmsResource, FmsResourceType, ImportIssue

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n?", re.DOTALL)

VALID_TYPES = {
    "referentiel",
    "learning_map",
    "module_map",
    "blueprint",
    "module",
    "qcm",
    "cas_n2",
    "assessment",
    "template",
    "guide",
}


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
    filename: str, frontmatter_type: Optional[str]
) -> Optional[FmsResourceType]:
    if frontmatter_type and frontmatter_type in VALID_TYPES:
        return frontmatter_type  # type: ignore[return-value]
    lower = filename.lower()
    for hint, rtype in FILENAME_TYPE_HINTS:
        if hint in lower:
            return rtype  # type: ignore[return-value]
    return None


def _infer_code(filename: str, frontmatter_code: Optional[str]) -> str:
    if frontmatter_code:
        return str(frontmatter_code)
    # Fall back to the filename stem, uppercased, dashes normalized —
    # e.g. "fms-01-m03 module.md" -> "FMS-01-M03-MODULE".
    stem = filename.rsplit("/", 1)[-1]
    stem = re.sub(r"\.md$", "", stem, flags=re.IGNORECASE)
    stem = re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-")
    return stem.upper()


def _as_str_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return []


def parse_markdown_file(
    filename: str, content: str, import_id: str
) -> Tuple[Optional[FmsResource], List[ImportIssue]]:
    """Parse one Markdown file into an FmsResource. Returns issues instead
    of raising — a file that can't be classified becomes a warning, not a
    crash."""
    issues: List[ImportIssue] = []
    frontmatter, body = _split_frontmatter(content)

    rtype = _infer_type(filename, frontmatter.get("type"))
    if rtype is None:
        issues.append(
            ImportIssue(
                level="warning",
                file=filename,
                message=(
                    "Type de ressource FMS non reconnu (ni `type:` en frontmatter, "
                    "ni indice dans le nom de fichier) — fichier ignoré."
                ),
            )
        )
        return None, issues

    code = _infer_code(filename, frontmatter.get("code"))
    title = str(frontmatter.get("title") or code)
    if not frontmatter.get("title"):
        issues.append(
            ImportIssue(
                level="warning",
                file=filename,
                message=f"Pas de `title:` en frontmatter — utilisation du code « {code} ».",
            )
        )

    resource = FmsResource(
        import_id=import_id,
        source_file=filename,
        type=rtype,
        code=code,
        formation_code=frontmatter.get("formation_code"),
        title=title,
        prerequisites=_as_str_list(frontmatter.get("prerequisites")),
        skill_ids=_as_str_list(frontmatter.get("skill_ids")),
        version=str(frontmatter.get("version", "1.0")),
        frontmatter=frontmatter,
        body_markdown=body.strip(),
    )
    return resource, issues

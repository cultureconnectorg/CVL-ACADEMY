"""FMS resource schema — the shape every parsed Markdown file becomes.

Documented convention (see docs/DEVELOPER_GUIDE.md § FMS ZIP format): every
source file is Markdown with a YAML frontmatter block:

    ---
    type: module
    code: FMS-01-M03
    formation_code: FMS-01
    title: Poser son univers artistique
    prerequisites: [FMS-01-M02]
    skill_ids: [FMS.N1.B2.S3]
    version: "1.0"
    ---
    # Body...

This is Academy's own convention for the FMS-01..FMS-06 ZIPs that arrive
after this mission — not something reverse-engineered from a real ZIP,
since none exists yet. The parser is deliberately lenient (falls back to
filename-based type/code inference) so a ZIP that doesn't perfectly match
still imports as much as it can and reports the rest as issues rather than
failing the whole batch.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

FmsResourceType = Literal[
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
]

RESOURCE_TYPE_LABELS: Dict[str, str] = {
    "referentiel": "Référentiel",
    "learning_map": "Learning Map",
    "module_map": "Module Map",
    "blueprint": "Blueprint",
    "module": "Module complet",
    "qcm": "QCM",
    "cas_n2": "Cas N2",
    "assessment": "Assessment",
    "template": "Template",
    "guide": "Guide",
}

# Filename fragments used to infer a resource's type when its frontmatter
# omits `type:` (case-insensitive, checked in this order).
FILENAME_TYPE_HINTS: List[tuple] = [
    ("referentiel", "referentiel"),
    ("learning-map", "learning_map"),
    ("learning_map", "learning_map"),
    ("module-map", "module_map"),
    ("module_map", "module_map"),
    ("blueprint", "blueprint"),
    ("qcm", "qcm"),
    ("cas-n2", "cas_n2"),
    ("cas_n2", "cas_n2"),
    ("assessment", "assessment"),
    ("template", "template"),
    ("guide", "guide"),
    ("module", "module"),
]


def _uid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ImportIssue(BaseModel):
    level: Literal["error", "warning"]
    file: str
    message: str


class FmsResource(BaseModel):
    """One parsed FMS artifact, ready to persist to db.fms_resources."""

    id: str = Field(default_factory=_uid)
    import_id: str
    source_file: str
    type: FmsResourceType
    code: str
    formation_code: Optional[str] = None
    title: str
    prerequisites: List[str] = Field(default_factory=list)
    skill_ids: List[str] = Field(default_factory=list)
    version: str = "1.0"
    frontmatter: Dict[str, Any] = Field(default_factory=dict)
    body_markdown: str = ""
    imported_at: str = Field(default_factory=_now)


class ImportReport(BaseModel):
    id: str = Field(default_factory=_uid)
    filename: str
    status: Literal["success", "partial", "failed"]
    resources_created: int = 0
    resources_by_type: Dict[str, int] = Field(default_factory=dict)
    issues: List[ImportIssue] = Field(default_factory=list)
    created_by: Optional[str] = None
    created_at: str = Field(default_factory=_now)

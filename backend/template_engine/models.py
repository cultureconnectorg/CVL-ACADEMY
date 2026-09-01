"""Template Engine — Diagnostic, Univers, Positionnement, Storytelling,
Roadmap, Dossier. Fillable, autosaved, versioned, exportable (MD/PDF/DOCX).

A TemplateDefinition is the form shape (admin-editable via the CMS later);
a TemplateDocument is one user's filled instance of it, versioned on every
save so nothing is ever silently lost.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

TemplateType = Literal[
    "diagnostic",
    "univers",
    "positionnement",
    "storytelling",
    "roadmap",
    "dossier",
    # 7th type, confirmed by the real FMS ZIP's Templates_Etudiants files
    # (e.g. 53_FMS01_Templates_Etudiants.md, Template 7 — "Pitch oral") —
    # every métier's parcours ends with a spoken pitch, distinct enough
    # from "dossier" (the written assembly) to warrant its own type.
    "pitch",
]
FieldType = Literal["text", "textarea", "number", "select", "list"]
DocumentStatus = Literal["draft", "final"]
ExportFormat = Literal["md", "pdf", "docx"]


def _uid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class TemplateFieldDef(BaseModel):
    key: str
    label: str
    field_type: FieldType = "text"
    required: bool = False
    options: List[str] = Field(default_factory=list)  # for "select"
    help_text: Optional[str] = None


class TemplateDefinition(BaseModel):
    type: TemplateType
    version: str = "1.0"
    title: str
    description: str = ""
    fields: List[TemplateFieldDef] = Field(default_factory=list)


class TemplateDocument(BaseModel):
    id: str = Field(default_factory=_uid)
    user_id: str
    template_type: TemplateType
    definition_version: str
    formation_code: Optional[str] = None
    module_code: Optional[str] = None
    title: str
    values: Dict[str, Any] = Field(default_factory=dict)
    status: DocumentStatus = "draft"
    version: int = 1
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)


class TemplateDocumentVersion(BaseModel):
    id: str = Field(default_factory=_uid)
    document_id: str
    version: int
    values: Dict[str, Any]
    status: DocumentStatus
    saved_at: str = Field(default_factory=_now)


class CreateDocumentInput(BaseModel):
    template_type: TemplateType
    title: str
    formation_code: Optional[str] = None
    module_code: Optional[str] = None
    values: Dict[str, Any] = Field(default_factory=dict)


class SaveDocumentInput(BaseModel):
    """Autosave payload — partial or full values, optional status change."""

    values: Dict[str, Any]
    status: Optional[DocumentStatus] = None

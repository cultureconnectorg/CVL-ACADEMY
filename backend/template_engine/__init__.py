"""Template Engine — see service.py (CRUD/autosave/versioning) and
export.py (MD/PDF/DOCX) for the public entry points."""

from .export import to_docx, to_markdown, to_pdf
from .models import (
    CreateDocumentInput,
    SaveDocumentInput,
    TemplateDefinition,
    TemplateDocument,
)
from .service import (
    create_document,
    get_definition,
    get_document,
    list_definitions,
    list_document_versions,
    list_user_documents,
    save_document,
    seed_default_definitions,
)

__all__ = [
    "seed_default_definitions",
    "list_definitions",
    "get_definition",
    "create_document",
    "get_document",
    "list_user_documents",
    "save_document",
    "list_document_versions",
    "to_markdown",
    "to_pdf",
    "to_docx",
    "TemplateDefinition",
    "TemplateDocument",
    "CreateDocumentInput",
    "SaveDocumentInput",
]

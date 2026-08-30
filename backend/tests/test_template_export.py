"""Pure unit tests for template export (MD/PDF/DOCX) — no DB required."""

from __future__ import annotations

from template_engine.export import to_docx, to_markdown, to_pdf
from template_engine.models import (
    TemplateDefinition,
    TemplateDocument,
    TemplateFieldDef,
)

DEFINITION = TemplateDefinition(
    type="diagnostic",
    title="Diagnostic",
    fields=[
        TemplateFieldDef(
            key="situation", label="Situation actuelle", field_type="textarea"
        ),
        TemplateFieldDef(key="forces", label="Forces", field_type="list"),
    ],
)

DOCUMENT = TemplateDocument(
    user_id="u1",
    template_type="diagnostic",
    definition_version="1.0",
    title="Mon diagnostic",
    values={"situation": "Je débute.", "forces": ["créativité", "discipline"]},
)


class TestToMarkdown:
    def test_includes_title_and_field_values(self):
        md = to_markdown(DOCUMENT, DEFINITION)
        assert "# Mon diagnostic" in md
        assert "Je débute." in md
        assert "- créativité" in md
        assert "- discipline" in md

    def test_empty_field_shows_placeholder(self):
        empty_doc = DOCUMENT.model_copy(update={"values": {}})
        md = to_markdown(empty_doc, DEFINITION)
        assert "_(vide)_" in md


class TestToPdf:
    def test_produces_valid_pdf_bytes(self):
        pdf = to_pdf(DOCUMENT, DEFINITION)
        assert pdf.startswith(b"%PDF")
        assert len(pdf) > 200


class TestToDocx:
    def test_produces_valid_docx_bytes(self):
        docx_bytes = to_docx(DOCUMENT, DEFINITION)
        assert docx_bytes[:2] == b"PK"  # docx is a zip container
        assert len(docx_bytes) > 1000

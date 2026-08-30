"""Template engine API — definitions, documents, autosave, export."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from auth import get_current_user
from models import User
from template_engine import (
    CreateDocumentInput,
    SaveDocumentInput,
    TemplateDefinition,
    TemplateDocument,
    create_document,
    get_document,
    list_definitions,
    list_document_versions,
    list_user_documents,
    save_document,
    to_docx,
    to_markdown,
    to_pdf,
)
from template_engine.models import TemplateDocumentVersion
from template_engine.service import get_definition

router = APIRouter(prefix="/templates", tags=["templates"])

EXPORT_MEDIA_TYPES = {
    "md": "text/markdown",
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


@router.get("/definitions", response_model=List[TemplateDefinition])
async def get_definitions():
    return await list_definitions()


@router.post("/documents", response_model=TemplateDocument)
async def new_document(
    inp: CreateDocumentInput, current: User = Depends(get_current_user)
):
    return await create_document(current.id, inp)


@router.get("/documents/mine", response_model=List[TemplateDocument])
async def my_documents(current: User = Depends(get_current_user)):
    return await list_user_documents(current.id)


@router.get("/documents/{document_id}", response_model=TemplateDocument)
async def read_document(document_id: str, current: User = Depends(get_current_user)):
    return await get_document(document_id, current.id)


@router.patch("/documents/{document_id}", response_model=TemplateDocument)
async def autosave_document(
    document_id: str, inp: SaveDocumentInput, current: User = Depends(get_current_user)
):
    return await save_document(document_id, current.id, inp)


@router.get(
    "/documents/{document_id}/versions", response_model=List[TemplateDocumentVersion]
)
async def document_versions(
    document_id: str, current: User = Depends(get_current_user)
):
    return await list_document_versions(document_id, current.id)


@router.get("/documents/{document_id}/export")
async def export_document(
    document_id: str,
    export_format: str = Query("md", alias="format"),
    current: User = Depends(get_current_user),
):
    if export_format not in EXPORT_MEDIA_TYPES:
        raise HTTPException(
            status_code=400, detail="Format d'export invalide (md | pdf | docx)"
        )
    document = await get_document(document_id, current.id)
    definition = await get_definition(document.template_type)

    if export_format == "md":
        content: bytes = to_markdown(document, definition).encode("utf-8")
    elif export_format == "pdf":
        content = to_pdf(document, definition)
    else:
        content = to_docx(document, definition)

    filename = f"{document.title.replace(' ', '_')}.{export_format}"
    return Response(
        content=content,
        media_type=EXPORT_MEDIA_TYPES[export_format],
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

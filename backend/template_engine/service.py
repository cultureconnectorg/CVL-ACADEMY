"""Template document CRUD + autosave + version history."""

from __future__ import annotations

from typing import List

from fastapi import HTTPException

from db import db, utc_now_iso

from .defaults import DEFAULT_DEFINITIONS
from .models import (
    CreateDocumentInput,
    SaveDocumentInput,
    TemplateDefinition,
    TemplateDocument,
    TemplateDocumentVersion,
)


async def seed_default_definitions() -> None:
    for definition in DEFAULT_DEFINITIONS:
        await db.template_definitions.update_one(
            {"type": definition.type}, {"$set": definition.model_dump()}, upsert=True
        )


async def list_definitions() -> List[TemplateDefinition]:
    docs = await db.template_definitions.find({}, {"_id": 0}).to_list(50)
    return [TemplateDefinition(**d) for d in docs]


async def get_definition(template_type: str) -> TemplateDefinition:
    doc = await db.template_definitions.find_one({"type": template_type}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Type de template inconnu")
    return TemplateDefinition(**doc)


async def create_document(user_id: str, inp: CreateDocumentInput) -> TemplateDocument:
    definition = await get_definition(inp.template_type)
    document = TemplateDocument(
        user_id=user_id,
        template_type=inp.template_type,
        definition_version=definition.version,
        formation_code=inp.formation_code,
        module_code=inp.module_code,
        title=inp.title,
        values=inp.values,
    )
    await db.template_documents.insert_one(document.model_dump())
    return document


async def _get_document(document_id: str) -> TemplateDocument:
    doc = await db.template_documents.find_one({"id": document_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Document introuvable")
    return TemplateDocument(**doc)


async def list_user_documents(user_id: str) -> List[TemplateDocument]:
    docs = (
        await db.template_documents.find({"user_id": user_id}, {"_id": 0})
        .sort("updated_at", -1)
        .to_list(500)
    )
    return [TemplateDocument(**d) for d in docs]


async def get_document(document_id: str, user_id: str) -> TemplateDocument:
    document = await _get_document(document_id)
    if document.user_id != user_id:
        raise HTTPException(
            status_code=403, detail="Ce document ne vous appartient pas"
        )
    return document


async def save_document(
    document_id: str, user_id: str, inp: SaveDocumentInput
) -> TemplateDocument:
    document = await get_document(document_id, user_id)
    new_version = document.version + 1
    now = utc_now_iso()
    updates = {
        "values": inp.values,
        "version": new_version,
        "updated_at": now,
    }
    if inp.status:
        updates["status"] = inp.status
    await db.template_documents.update_one({"id": document_id}, {"$set": updates})

    # Version history — append-only, so nothing is ever lost to a bad autosave.
    history_entry = TemplateDocumentVersion(
        document_id=document_id,
        version=new_version,
        values=inp.values,
        status=inp.status or document.status,
    )
    await db.template_document_versions.insert_one(history_entry.model_dump())

    return await get_document(document_id, user_id)


async def list_document_versions(
    document_id: str, user_id: str
) -> List[TemplateDocumentVersion]:
    await get_document(document_id, user_id)  # ownership check
    docs = (
        await db.template_document_versions.find(
            {"document_id": document_id}, {"_id": 0}
        )
        .sort("version", -1)
        .to_list(500)
    )
    return [TemplateDocumentVersion(**d) for d in docs]

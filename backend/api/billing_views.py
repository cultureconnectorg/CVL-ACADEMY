"""Read-only billing discovery surfaces for authenticated Academy users."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends

from auth import get_current_user
from db import db
from models import User

router = APIRouter(prefix="/billing", tags=["billing"])


def _public_invoice(document: dict) -> dict:
    clean = dict(document)
    clean.pop("_id", None)
    artifact = clean.pop("artifact", None)
    if artifact:
        clean["artifact"] = {
            "format": artifact.get("format"),
            "xml_sha256": artifact.get("xml_sha256"),
            "pdf_sha256": artifact.get("pdf_sha256"),
            "xml_size": artifact.get("xml_size"),
            "pdf_size": artifact.get("pdf_size"),
            "xsd_validation": artifact.get("xsd_validation"),
            "schematron_validation": artifact.get("schematron_validation"),
        }
    return clean


@router.get("/invoices/mine")
async def my_invoices(
    economy_code: Optional[str] = None,
    current: User = Depends(get_current_user),
):
    query = {"user_id": current.id, "document_type": "INVOICE"}
    if economy_code:
        query["economy_code"] = economy_code
    documents = await db.billing_documents.find(query).sort("created_at", -1).to_list(100)
    return [_public_invoice(document) for document in documents]

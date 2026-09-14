"""Canonical document-registry adapter for Protocol Master integrations.

The Protocol workbook names one shared Document Registry. Academy already owns
legal document/version runtime; this adapter exposes that existing truth instead
of creating a parallel document store.
"""
from services import legal_documents

BOUNDARY = "services.legal_documents"
service = legal_documents

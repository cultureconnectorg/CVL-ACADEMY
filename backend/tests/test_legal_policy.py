"""Regression checks for the Academy legal bundle contract."""

from legal_policy import (
    DOCUMENT_BY_ID,
    LEGAL_BUNDLE_VERSION,
    PUBLIC_LEGAL_DOCUMENTS,
    REQUIRED_DOCUMENT_IDS,
)


def test_legal_bundle_has_unique_required_documents():
    ids = [doc["id"] for doc in PUBLIC_LEGAL_DOCUMENTS]
    assert ids == list(REQUIRED_DOCUMENT_IDS)
    assert len(ids) == len(set(ids))
    assert set(ids) == {"cgu", "reglement-academy", "charte-ia", "confidentialite"}


def test_legal_documents_are_versioned_and_hashed():
    assert LEGAL_BUNDLE_VERSION
    for doc in PUBLIC_LEGAL_DOCUMENTS:
        assert doc["version"]
        assert len(doc["sha256"]) == 64
        assert doc["mode"] in {"accept", "acknowledge"}
        assert doc["url"].startswith("/legal/")
        assert "canonical" not in doc
        assert DOCUMENT_BY_ID[doc["id"]] == doc


def test_privacy_is_acknowledgement_not_blanket_consent():
    assert DOCUMENT_BY_ID["confidentialite"]["mode"] == "acknowledge"
    assert DOCUMENT_BY_ID["cgu"]["mode"] == "accept"
    assert DOCUMENT_BY_ID["reglement-academy"]["mode"] == "accept"

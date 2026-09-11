from __future__ import annotations

from datetime import datetime, timezone

import pytest
from mongomock_motor import AsyncMongoMockClient

import qualification.service as qualification_service
from qualification.models import QualificationDefinitionInput


@pytest.fixture
async def qualification_db(monkeypatch):
    client = AsyncMongoMockClient()
    db = client["economy_qualification_policy"]
    monkeypatch.setattr(qualification_service, "db", db)
    return db


def _months_between(start_iso: str, end_iso: str) -> int:
    start = datetime.fromisoformat(start_iso.replace("Z", "+00:00"))
    end = datetime.fromisoformat(end_iso.replace("Z", "+00:00"))
    return (end.year - start.year) * 12 + end.month - start.month


@pytest.mark.asyncio
async def test_standard_qualification_expires_after_24_months(qualification_db):
    await qualification_service.register_definition(
        "QUAL-STANDARD",
        QualificationDefinitionInput(
            label="Standard",
            certification_codes=["CERT-STANDARD"],
            validity_class="standard",
        ),
    )
    issued = await qualification_service.maybe_issue_qualification(
        "u1",
        "CERT-STANDARD",
        "attempt-1",
    )
    assert len(issued) == 1
    qualification = issued[0]
    assert qualification.validity_months == 24
    assert qualification.validity_class == "standard"
    assert qualification.expires_at is not None
    assert _months_between(
        qualification.issued_at,
        qualification.expires_at,
    ) == 24


@pytest.mark.asyncio
async def test_sensitive_qualification_expires_after_12_months(qualification_db):
    await qualification_service.register_definition(
        "QUAL-SENSITIVE",
        QualificationDefinitionInput(
            label="Sensitive",
            certification_codes=["CERT-SENSITIVE"],
            validity_class="sensitive",
        ),
    )
    issued = await qualification_service.maybe_issue_qualification(
        "u2",
        "CERT-SENSITIVE",
        "attempt-1",
    )
    qualification = issued[0]
    assert qualification.validity_months == 12
    assert qualification.validity_class == "sensitive"
    assert qualification.expires_at is not None
    assert _months_between(
        qualification.issued_at,
        qualification.expires_at,
    ) == 12


@pytest.mark.asyncio
async def test_expired_fact_is_preserved_and_new_pass_appends_requalification(
    qualification_db,
):
    await qualification_service.register_definition(
        "QUAL-SENSITIVE",
        QualificationDefinitionInput(
            label="Sensitive",
            certification_codes=["CERT-SENSITIVE"],
            validity_class="sensitive",
        ),
    )
    await qualification_db.qualifications.insert_one(
        {
            "id": "old-qualification",
            "user_id": "u3",
            "qualification_code": "QUAL-SENSITIVE",
            "source_certification_code": "CERT-SENSITIVE",
            "source_attempt_id": "old-attempt",
            "sha256": "a" * 64,
            "issued_at": "2024-01-01T00:00:00+00:00",
            "expires_at": "2025-01-01T00:00:00+00:00",
            "validity_class": "sensitive",
            "validity_months": 12,
        }
    )

    assert await qualification_service.is_qualified(
        "u3",
        "QUAL-SENSITIVE",
    ) is False

    issued = await qualification_service.maybe_issue_qualification(
        "u3",
        "CERT-SENSITIVE",
        "new-attempt",
    )
    assert len(issued) == 1
    assert issued[0].source_attempt_id == "new-attempt"
    assert await qualification_db.qualifications.count_documents(
        {
            "user_id": "u3",
            "qualification_code": "QUAL-SENSITIVE",
        }
    ) == 2
    assert await qualification_service.is_qualified(
        "u3",
        "QUAL-SENSITIVE",
    ) is True


@pytest.mark.asyncio
async def test_legacy_qualification_without_expiry_gets_policy_effective_expiry(
    qualification_db,
):
    await qualification_service.register_definition(
        "QUAL-STANDARD",
        QualificationDefinitionInput(
            label="Standard",
            validity_class="standard",
        ),
    )
    await qualification_db.qualifications.insert_one(
        {
            "id": "legacy",
            "user_id": "u4",
            "qualification_code": "QUAL-STANDARD",
            "source_certification_code": "CERT-OLD",
            "source_attempt_id": "old-attempt",
            "sha256": "b" * 64,
            "issued_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    qualifications = await qualification_service.list_user_qualifications("u4")
    assert len(qualifications) == 1
    assert qualifications[0].validity_months == 24
    assert qualifications[0].expires_at is not None

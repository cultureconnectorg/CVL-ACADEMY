from services.requirement_registry import merge_ingested_requirement


def _base(source_hash: str = "hash-v1") -> dict:
    return {
        "requirement_id": "CATALOGUE_2D:FMS-TEST",
        "family": "CATALOGUE_2D",
        "code": "FMS-TEST",
        "source": {"path": "master.csv", "row": 2},
        "source_hash": source_hash,
        "runtime_collection": "academy_catalogue_master",
        "runtime_key": {"code": "FMS-TEST"},
        "runtime_importer": "services.catalogue_importer.import_catalogue_master",
        "test_ref": "backend/tests/test_master_importers.py",
    }


def test_verified_requirement_survives_idempotent_master_sync():
    existing = {
        **_base(),
        "status": "VERIFIED",
        "verified": True,
        "verification_evidence": "ci://run/123",
        "verified_by": "founder-1",
    }
    merged, unset = merge_ingested_requirement(_base(), existing)

    assert merged["status"] == "VERIFIED"
    assert merged["verified"] is True
    assert merged["verification_evidence"] == "ci://run/123"
    assert merged["verified_by"] == "founder-1"
    assert unset == []


def test_source_change_invalidates_old_verification_evidence():
    existing = {
        **_base("hash-v1"),
        "status": "VERIFIED",
        "verified": True,
        "verification_evidence": "ci://run/123",
        "verified_by": "founder-1",
    }
    merged, unset = merge_ingested_requirement(_base("hash-v2"), existing)

    assert merged["status"] == "INGESTED_RUNTIME"
    assert merged["verified"] is False
    assert set(unset) == {"verification_evidence", "verified_by", "verified_at"}


def test_unverified_requirement_stays_ingested_on_same_source():
    existing = {**_base(), "status": "INGESTED_RUNTIME", "verified": False}
    merged, unset = merge_ingested_requirement(_base(), existing)

    assert merged["status"] == "INGESTED_RUNTIME"
    assert merged["verified"] is False
    assert "verification_evidence" in unset

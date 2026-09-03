"""ACA-0005 — Module Lineage tests.

Exercises `fms_lineage/` against a real Motor-shaped mock
(`mongomock_motor.AsyncMongoMockClient`) rather than pure Python objects,
because several of the required guarantees here — a unique-index
rejection, an idempotent upsert, a fail-safe read of a corrupt document —
are genuinely database behaviors, not application logic. No live MongoDB
is available in this sandbox (same constraint noted in
`docs/FMS_IMPORT_VALIDATION_REPORT.md` §6); mongomock_motor is the
closest thing to a real Motor client this environment can offer, and its
unique-index/upsert semantics were spot-checked against real pymongo
error types (`DuplicateKeyError`) before being relied on here.

Every test gets its own fresh in-memory client (`lineage_db` fixture,
function-scoped) — no shared state between tests, safe under this repo's
`-n 2 --dist loadscope` xdist config.
"""

from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient
from pymongo.errors import DuplicateKeyError

import fms_lineage.initial_matrix as initial_matrix_module
import fms_lineage.service as service_module
import infra_indexes
from fms_lineage.initial_matrix import build_initial_records, seed_initial_matrix
from fms_lineage.models import (
    CANONICAL_VERSION_CURRENT,
    LineageCreateInput,
    LineageUpdateInput,
)
from fms_lineage.service import (
    LineageError,
    create_lineage,
    get_lineage_for_canonical_module,
    get_lineage_for_legacy_module,
    list_lineage_for_formation,
    resolve_canonical_target,
    update_lineage,
)


@pytest.fixture
async def lineage_db(monkeypatch):
    """A fresh mock DB per test, wired into every module that holds its
    own `from db import db` binding (module-level names don't follow a
    later reassignment of `db.db` itself, so each is patched directly)."""
    client = AsyncMongoMockClient()
    mock_db = client["cvln_test"]
    monkeypatch.setattr(service_module, "db", mock_db)
    monkeypatch.setattr(initial_matrix_module, "db", mock_db)
    monkeypatch.setattr(infra_indexes, "db", mock_db)
    await infra_indexes.ensure_indexes()
    return mock_db


def _input(**overrides) -> LineageCreateInput:
    base = dict(
        legacy_formation_code="FMS-01",
        legacy_module_code="FMS-01-M01",
        canonical_formation_code="FMS-01",
        canonical_module_code="FMS01-M01",
        canonical_version=CANONICAL_VERSION_CURRENT,
        relation="NO_EQUIVALENCE",
    )
    base.update(overrides)
    return LineageCreateInput(**base)


# ---------------------------------------------------------------------
# 1-3. Creation of each simple relation type
# ---------------------------------------------------------------------


async def test_create_no_equivalence(lineage_db):
    record = await create_lineage(
        _input(relation="NO_EQUIVALENCE"), created_by="admin-1"
    )
    assert record.relation == "NO_EQUIVALENCE"
    stored = await lineage_db.module_lineage.find_one({"lineage_id": record.lineage_id})
    assert stored is not None
    assert stored["relation"] == "NO_EQUIVALENCE"


async def test_create_related_with_evidence(lineage_db):
    record = await create_lineage(
        _input(
            relation="RELATED",
            canonical_module_code="FMS01-M04",
            evidence="Both cover artist-universe positioning, real textual overlap.",
        ),
        created_by="admin-1",
    )
    assert record.relation == "RELATED"
    assert record.evidence


async def test_create_superseded_by(lineage_db):
    record = await create_lineage(
        _input(
            relation="SUPERSEDED_BY", notes="Canonical M01 is the active replacement."
        ),
        created_by="admin-1",
    )
    assert record.relation == "SUPERSEDED_BY"


# ---------------------------------------------------------------------
# 4. MANUAL_EQUIVALENCE governance
# ---------------------------------------------------------------------


async def test_manual_equivalence_rejected_without_evidence_or_approval(lineage_db):
    with pytest.raises(ValueError):
        await create_lineage(
            _input(relation="MANUAL_EQUIVALENCE"), created_by="admin-1"
        )

    with pytest.raises(ValueError):
        await create_lineage(
            _input(
                relation="MANUAL_EQUIVALENCE",
                evidence="Pedagogy team review, minutes #12",
            ),
            created_by="admin-1",
        )  # evidence present, approved_by still missing


async def test_manual_equivalence_accepted_with_both(lineage_db):
    record = await create_lineage(
        _input(
            relation="MANUAL_EQUIVALENCE",
            evidence="Pedagogy team review, minutes #12",
            approved_by="founder@cvln",
            approved_at="2026-09-03T00:00:00Z",
            scope="FMS-01 M01 legacy portfolio work folded into canonical M04-M05",
        ),
        created_by="admin-1",
    )
    assert record.relation == "MANUAL_EQUIVALENCE"
    assert record.approved_by == "founder@cvln"


async def test_update_cannot_strip_evidence_from_manual_equivalence(lineage_db):
    record = await create_lineage(
        _input(
            relation="MANUAL_EQUIVALENCE",
            evidence="Pedagogy team review",
            approved_by="founder@cvln",
        ),
        created_by="admin-1",
    )
    with pytest.raises(ValueError):
        await update_lineage(record.lineage_id, LineageUpdateInput(evidence=""))


# ---------------------------------------------------------------------
# 5-7. No positional/pedagogical inference, codes stay distinct strings
# ---------------------------------------------------------------------


def test_no_automatic_equivalence_from_shared_module_number():
    records = build_initial_records()
    assert (
        len(records) == 53
    )  # 12+10+8+8+8+7, docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md §1
    assert all(r.relation == "NO_EQUIVALENCE" for r in records)


def test_legacy_and_canonical_m01_are_distinct_identities():
    records = build_initial_records()
    fms01_m01 = next(
        r
        for r in records
        if r.legacy_formation_code == "FMS-01" and r.legacy_module_code == "FMS-01-M01"
    )
    assert fms01_m01.legacy_module_code == "FMS-01-M01"
    assert fms01_m01.canonical_module_code == "FMS01-M01"
    assert fms01_m01.legacy_module_code != fms01_m01.canonical_module_code
    assert fms01_m01.relation == "NO_EQUIVALENCE"


def test_no_code_normalization_ever_applied():
    records = build_initial_records()
    for r in records:
        assert (
            "-" in r.legacy_module_code
        )  # e.g. FMS-01-M01, always the hyphenated form
        # canonical form has no hyphen right after "FMS0<n>"
        assert not r.canonical_module_code.startswith("FMS-")
    # No record's legacy and canonical codes were ever coerced to match.
    assert all(r.legacy_module_code != r.canonical_module_code for r in records)


# ---------------------------------------------------------------------
# 8-9. Non-mutation / non-deletion of legacy data
# ---------------------------------------------------------------------


async def test_no_mutation_of_module_progress(lineage_db):
    progress_doc = {
        "id": "p1",
        "user_id": "u1",
        "formation_code": "FMS-01",
        "module_code": "FMS-01-M01",
        "completed": True,
        "score": 0.9,
    }
    await lineage_db.progress.insert_one(dict(progress_doc))

    await create_lineage(
        _input(
            relation="RELATED",
            canonical_module_code="FMS01-M04",
            evidence="Univers artistique overlap",
        ),
        created_by="admin-1",
    )
    await seed_initial_matrix()
    await resolve_canonical_target("FMS-01", "FMS-01-M01")

    stored = await lineage_db.progress.find_one({"id": "p1"}, {"_id": 0})
    assert stored == progress_doc
    assert await lineage_db.progress.count_documents({}) == 1


async def test_no_deletion_of_legacy_formation_content(lineage_db):
    formation_doc = {
        "code": "FMS-01",
        "modules": [
            {"code": "FMS-01-M01", "name": "Identité artistique et culturelle"}
        ],
    }
    await lineage_db.formations.insert_one(dict(formation_doc))

    await seed_initial_matrix()
    await create_lineage(
        _input(relation="SUPERSEDED_BY", canonical_module_code="FMS01-M05"),
        created_by="admin-1",
    )

    stored = await lineage_db.formations.find_one({"code": "FMS-01"}, {"_id": 0})
    assert stored == formation_doc
    assert await lineage_db.formations.count_documents({}) == 1


# ---------------------------------------------------------------------
# 10-11. Lookups both directions
# ---------------------------------------------------------------------


async def test_lookup_legacy_to_canonical(lineage_db):
    await create_lineage(_input(), created_by="admin-1")
    found = await get_lineage_for_legacy_module("FMS-01", "FMS-01-M01")
    assert len(found) == 1
    assert found[0].canonical_module_code == "FMS01-M01"


async def test_lookup_canonical_to_legacy(lineage_db):
    await create_lineage(_input(), created_by="admin-1")
    found = await get_lineage_for_canonical_module("FMS-01", "FMS01-M01")
    assert len(found) == 1
    assert found[0].legacy_module_code == "FMS-01-M01"


async def test_list_lineage_for_formation_both_sides(lineage_db):
    await create_lineage(_input(), created_by="admin-1")
    found = await list_lineage_for_formation("FMS-01", side="both")
    assert len(found) == 1


# ---------------------------------------------------------------------
# 12-13. Multiple legitimate RELATED, but exact duplicates rejected
# ---------------------------------------------------------------------


async def test_multiple_related_targets_allowed(lineage_db):
    await create_lineage(
        _input(
            relation="RELATED",
            canonical_module_code="FMS01-M04",
            evidence="Univers artistique overlap",
        ),
        created_by="admin-1",
    )
    await create_lineage(
        _input(
            relation="RELATED",
            canonical_module_code="FMS01-M05",
            evidence="Positionnement overlap",
        ),
        created_by="admin-1",
    )
    found = await get_lineage_for_legacy_module("FMS-01", "FMS-01-M01")
    assert {r.canonical_module_code for r in found} == {"FMS01-M04", "FMS01-M05"}


async def test_inconsistent_duplicate_pair_rejected(lineage_db):
    await create_lineage(_input(relation="NO_EQUIVALENCE"), created_by="admin-1")
    with pytest.raises(DuplicateKeyError):
        await create_lineage(
            _input(relation="RELATED", evidence="different claim, same pair"),
            created_by="admin-2",
        )


# ---------------------------------------------------------------------
# 14. Canonical version preserved / coexists across versions
# ---------------------------------------------------------------------


async def test_canonical_version_preserved_across_versions(lineage_db):
    v1 = await create_lineage(
        _input(canonical_version="FMS_20260822_V1"), created_by="admin-1"
    )
    v2 = await create_lineage(
        _input(canonical_version="FMS_FUTURE_V2"), created_by="admin-1"
    )
    assert v1.canonical_version == "FMS_20260822_V1"
    assert v2.canonical_version == "FMS_FUTURE_V2"
    # V2 existing never rewrote V1's own record.
    reread_v1 = await lineage_db.module_lineage.find_one(
        {"lineage_id": v1.lineage_id}, {"_id": 0}
    )
    assert reread_v1["canonical_version"] == "FMS_20260822_V1"


# ---------------------------------------------------------------------
# 15. Fail-safe on unknown/invalid relation
# ---------------------------------------------------------------------


async def test_service_fails_safe_on_corrupt_relation_value(lineage_db):
    await lineage_db.module_lineage.insert_one(
        {
            "lineage_id": "corrupt-1",
            "legacy_formation_code": "FMS-02",
            "legacy_module_code": "FMS-02-M01",
            "canonical_formation_code": "FMS-02",
            "canonical_module_code": "FMS02-M01",
            "canonical_version": CANONICAL_VERSION_CURRENT,
            "relation": "SOMETHING_UNRECOGNIZED",
            "status": "active",
            "created_at": "x",
            "updated_at": "x",
            "created_by": "test",
        }
    )
    found = await get_lineage_for_legacy_module("FMS-02", "FMS-02-M01")
    assert found == []  # dropped, not raised

    resolved = await resolve_canonical_target("FMS-02", "FMS-02-M01")
    assert resolved.relation is None
    assert resolved.credit_transfer is False


async def test_resolve_unmapped_module_is_safe(lineage_db):
    resolved = await resolve_canonical_target("FMS-06", "FMS-06-M07")
    assert resolved.relation is None
    assert resolved.canonical_module_code is None
    assert resolved.credit_transfer is False


async def test_update_missing_lineage_raises_lineage_error(lineage_db):
    with pytest.raises(LineageError):
        await update_lineage("does-not-exist", LineageUpdateInput(notes="x"))


# ---------------------------------------------------------------------
# resolve_canonical_target — credit_transfer always False, and relation
# priority / qualification behave as documented.
# ---------------------------------------------------------------------


async def test_resolve_manual_equivalence_is_qualified_but_never_credits(lineage_db):
    await create_lineage(
        _input(
            relation="MANUAL_EQUIVALENCE",
            evidence="Reviewed",
            approved_by="founder@cvln",
        ),
        created_by="admin-1",
    )
    resolved = await resolve_canonical_target("FMS-01", "FMS-01-M01")
    assert resolved.relation == "MANUAL_EQUIVALENCE"
    assert resolved.qualified is True
    assert resolved.credit_transfer is False


async def test_resolve_related_is_never_qualified_or_credited(lineage_db):
    await create_lineage(
        _input(relation="RELATED", evidence="Thematic overlap only"),
        created_by="admin-1",
    )
    resolved = await resolve_canonical_target("FMS-01", "FMS-01-M01")
    assert resolved.relation == "RELATED"
    assert resolved.qualified is False
    assert resolved.credit_transfer is False


# ---------------------------------------------------------------------
# Idempotent seeding
# ---------------------------------------------------------------------


async def test_seed_initial_matrix_is_idempotent(lineage_db):
    inserted_1, skipped_1 = await seed_initial_matrix()
    assert inserted_1 == 53
    assert skipped_1 == 0

    inserted_2, skipped_2 = await seed_initial_matrix()
    assert inserted_2 == 0
    assert skipped_2 == 53
    assert await lineage_db.module_lineage.count_documents({}) == 53


async def test_seed_initial_matrix_never_overwrites_a_human_edit(lineage_db):
    await seed_initial_matrix()
    all_records = await list_lineage_for_formation("FMS-01", side="legacy")
    target = next(r for r in all_records if r.legacy_module_code == "FMS-01-M01")
    edited = await update_lineage(
        target.lineage_id,
        LineageUpdateInput(relation="RELATED", evidence="Human-reviewed real overlap"),
    )
    assert edited.relation == "RELATED"

    await seed_initial_matrix()  # re-run — must not clobber the edit
    reread = await lineage_db.module_lineage.find_one(
        {"lineage_id": target.lineage_id}, {"_id": 0}
    )
    assert reread["relation"] == "RELATED"
    assert reread["evidence"] == "Human-reviewed real overlap"


# ---------------------------------------------------------------------
# 16. Admin permissions on the API surface
# ---------------------------------------------------------------------


def _allowed_roles(dependency_callable):
    freevars = dependency_callable.__code__.co_freevars
    if "allowed" not in freevars:
        return None
    idx = freevars.index("allowed")
    return dependency_callable.__closure__[idx].cell_contents


def test_write_routes_require_admin_roles_only():
    from api.fms_lineage import router
    from models import ADMIN_ROLES

    write_paths = {("/fms/lineage", "POST"), ("/fms/lineage/{lineage_id}", "PATCH")}
    checked = 0
    for route in router.routes:
        for method in route.methods:
            if (route.path, method) in write_paths:
                roles = next(
                    (
                        _allowed_roles(dep.call)
                        for dep in route.dependant.dependencies
                        if _allowed_roles(dep.call) is not None
                    ),
                    None,
                )
                assert (
                    roles == ADMIN_ROLES
                ), f"{route.path} {method} must require ADMIN_ROLES only"
                checked += 1
    assert checked == 2


def test_read_routes_require_at_least_staff_roles():
    from api.fms_lineage import router
    from models import ADMIN_ROLES, STAFF_ROLES

    checked = 0
    for route in router.routes:
        if "GET" not in route.methods:
            continue
        roles = next(
            (
                _allowed_roles(dep.call)
                for dep in route.dependant.dependencies
                if _allowed_roles(dep.call) is not None
            ),
            None,
        )
        assert roles == STAFF_ROLES, f"{route.path} must require STAFF_ROLES"
        # every admin role is itself staff — the permission set is a real
        # superset, not an accidental narrower/wider list.
        assert set(ADMIN_ROLES).issubset(set(roles))
        checked += 1
    assert checked == 4

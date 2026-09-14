"""SEC-01/SEC-02 (Audit Chirurgical 2026-09-07) — invitation privilege
escalation and invitation ownership.

Real, exploitable gaps this suite closes and proves closed:

  - SEC-01: `POST /invitations` is reachable by `trainer` as well as
    ADMIN_ROLES, but before this fix `InvitationInput.role` was
    accepted verbatim regardless of who created the invitation — a
    trainer could mint role="founder" and `_apply_invitation` would
    grant it on signup with zero server-side check. Fixed by
    `models.INVITER_ALLOWED_INVITED_ROLES`, enforced in
    `api/orgs.create_invitation`.
  - SEC-01 (org scope): a non-admin inviter must be scoped to their own
    organisation — never another org, never org-less.
  - SEC-02: the public `GET /invitations/{code}` preview used to leak
    the invitation's target email to anyone holding (or guessing) the
    code; `_apply_invitation` never checked the registering email
    against it, so possession of the code was sufficient regardless of
    who it was meant for.

DB-backed pieces run against `mongomock_motor.AsyncMongoMockClient` —
same convention as every other suite in this repo (no live MongoDB in
this sandbox).
"""

from __future__ import annotations

import pytest
from fastapi import HTTPException
from mongomock_motor import AsyncMongoMockClient

import auth as auth_root_module
import api.auth as auth_module
import api.orgs as orgs_module
import services.frek_core as frek_core_module
import services.notifications as notifications_module
from api.auth import _apply_invitation, register
from api.orgs import create_invitation, get_invitation
from models import InvitationInput, RegisterInput, User


@pytest.fixture
async def inv_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_invitations_test"]
    # register() (api/auth.py) reaches into the root auth.py (next_frek_id,
    # token issuance) and the frek_core/notifications services — every one
    # of those modules holds its own `db` reference, same pattern as
    # test_rail2_kor01_e2e.py's rail2_db fixture.
    for module in (
        orgs_module,
        auth_module,
        auth_root_module,
        frek_core_module,
        notifications_module,
    ):
        monkeypatch.setattr(module, "db", mock_db)
    return mock_db


def _user(role: str, *, org_id=None, email="staff@example.com") -> User:
    return User(
        frek_id=f"FREK-{role.upper()}",
        email=email,
        display_name=role.title(),
        password_hash="x",
        role=role,
        org_id=org_id,
    )


async def _seed_org(db, org_id="org-1", name="CVLN Test Org"):
    await db.organisations.insert_one({"id": org_id, "name": name, "slug": "cvln-test-org"})


# --------------------------------------------------------------------
# SEC-01 — role escalation via invitation
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_trainer_can_only_invite_student(inv_db):
    await _seed_org(inv_db)
    trainer = _user("trainer", org_id="org-1")

    inv = await create_invitation(
        InvitationInput(role="student", org_id="org-1"), current=trainer
    )
    assert inv.role == "student"
    assert inv.org_id == "org-1"


@pytest.mark.asyncio
@pytest.mark.parametrize("elevated_role", ["trainer", "corrector", "jury", "admin", "super_admin", "founder"])
async def test_trainer_cannot_invite_elevated_roles(inv_db, elevated_role):
    await _seed_org(inv_db)
    trainer = _user("trainer", org_id="org-1")

    with pytest.raises(HTTPException) as exc:
        await create_invitation(
            InvitationInput(role=elevated_role, org_id="org-1"), current=trainer
        )
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_admin_can_invite_up_to_admin_never_super_admin_or_founder(inv_db):
    admin = _user("admin")
    for ok_role in ("student", "trainer", "corrector", "jury", "admin"):
        inv = await create_invitation(InvitationInput(role=ok_role), current=admin)
        assert inv.role == ok_role

    for forbidden in ("super_admin", "founder"):
        with pytest.raises(HTTPException) as exc:
            await create_invitation(InvitationInput(role=forbidden), current=admin)
        assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_nobody_can_mint_a_founder_invitation(inv_db):
    """Not even founder — the role is manual/seed-only, never self-service."""
    founder = _user("founder")
    with pytest.raises(HTTPException) as exc:
        await create_invitation(InvitationInput(role="founder"), current=founder)
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_super_admin_can_invite_admin_and_super_admin_never_founder(inv_db):
    super_admin = _user("super_admin")
    inv = await create_invitation(InvitationInput(role="admin"), current=super_admin)
    assert inv.role == "admin"
    inv2 = await create_invitation(InvitationInput(role="super_admin"), current=super_admin)
    assert inv2.role == "super_admin"

    with pytest.raises(HTTPException) as exc:
        await create_invitation(InvitationInput(role="founder"), current=super_admin)
    assert exc.value.status_code == 403


# --------------------------------------------------------------------
# SEC-01 — organisational scope for non-admin inviters
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_trainer_cannot_invite_into_another_org(inv_db):
    await _seed_org(inv_db, "org-1")
    await _seed_org(inv_db, "org-2", "Other Org")
    trainer = _user("trainer", org_id="org-1")

    with pytest.raises(HTTPException) as exc:
        await create_invitation(
            InvitationInput(role="student", org_id="org-2"), current=trainer
        )
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_trainer_without_org_cannot_invite(inv_db):
    trainer = _user("trainer", org_id=None)
    with pytest.raises(HTTPException) as exc:
        await create_invitation(InvitationInput(role="student"), current=trainer)
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_trainer_org_id_is_forced_from_own_membership_not_trusted_from_body(inv_db):
    """Even if a trainer omits org_id, the effective org is their own —
    never left unset, never derived from anything client-supplied."""
    await _seed_org(inv_db, "org-1")
    trainer = _user("trainer", org_id="org-1")
    inv = await create_invitation(InvitationInput(role="student"), current=trainer)
    assert inv.org_id == "org-1"


@pytest.mark.asyncio
async def test_admin_stays_platform_wide_across_orgs(inv_db):
    await _seed_org(inv_db, "org-1")
    await _seed_org(inv_db, "org-2", "Other Org")
    admin = _user("admin", org_id="org-1")
    inv = await create_invitation(
        InvitationInput(role="student", org_id="org-2"), current=admin
    )
    assert inv.org_id == "org-2"


@pytest.mark.asyncio
async def test_cohort_must_belong_to_the_effective_org(inv_db):
    await _seed_org(inv_db, "org-1")
    await _seed_org(inv_db, "org-2", "Other Org")
    await inv_db.cohorts.insert_one({"id": "cohort-2", "org_id": "org-2", "name": "C2"})
    trainer = _user("trainer", org_id="org-1")

    with pytest.raises(HTTPException) as exc:
        await create_invitation(
            InvitationInput(role="student", cohort_id="cohort-2"), current=trainer
        )
    assert exc.value.status_code == 400


# --------------------------------------------------------------------
# SEC-02 — public preview never leaks the target email
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_public_preview_never_returns_raw_email(inv_db):
    await inv_db.invitations.insert_one(
        {
            "id": "i1",
            "code": "SECRET123",
            "email": "target@example.com",
            "role": "student",
            "org_id": None,
            "cohort_id": None,
            "invited_by": "u1",
            "used_by": None,
            "used_at": None,
            "expires_at": None,
            "created_at": "2026-09-07T00:00:00Z",
        }
    )
    preview = await get_invitation("SECRET123")
    assert "email" not in preview
    assert preview["email_required"] is True


@pytest.mark.asyncio
async def test_public_preview_email_required_false_when_open(inv_db):
    await inv_db.invitations.insert_one(
        {
            "id": "i2",
            "code": "OPEN456",
            "email": None,
            "role": "student",
            "org_id": None,
            "cohort_id": None,
            "invited_by": "u1",
            "used_by": None,
            "used_at": None,
            "expires_at": None,
            "created_at": "2026-09-07T00:00:00Z",
        }
    )
    preview = await get_invitation("OPEN456")
    assert preview["email_required"] is False


# --------------------------------------------------------------------
# SEC-02 — invitation ownership at consumption
# --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_email_scoped_invitation_rejects_mismatched_registering_email(inv_db):
    await inv_db.users.insert_one({"id": "target-user", "email": "target@example.com"})
    await inv_db.invitations.insert_one(
        {
            "id": "i3",
            "code": "TARGETED",
            "email": "target@example.com",
            "role": "student",
            "org_id": None,
            "cohort_id": None,
            "invited_by": "u1",
            "used_by": None,
            "used_at": None,
            "expires_at": None,
            "created_at": "2026-09-07T00:00:00Z",
        }
    )

    with pytest.raises(HTTPException) as exc:
        await _apply_invitation("target-user", "TARGETED", "attacker@example.com")
    assert exc.value.status_code == 400

    # The failed, mismatched attempt must never burn the invitation —
    # a real holder of the code can still consume it correctly.
    stored = await inv_db.invitations.find_one({"code": "TARGETED"}, {"_id": 0})
    assert stored["used_by"] is None


@pytest.mark.asyncio
async def test_email_scoped_invitation_accepts_matching_email_case_insensitive(inv_db):
    await inv_db.users.insert_one({"id": "target-user", "email": "target@example.com"})
    await inv_db.invitations.insert_one(
        {
            "id": "i4",
            "code": "TARGETED2",
            "email": "Target@Example.com",
            "role": "trainer",
            "org_id": None,
            "cohort_id": None,
            "invited_by": "u1",
            "used_by": None,
            "used_at": None,
            "expires_at": None,
            "created_at": "2026-09-07T00:00:00Z",
        }
    )

    await _apply_invitation("target-user", "TARGETED2", "target@example.com")
    stored_user = await inv_db.users.find_one({"id": "target-user"}, {"_id": 0})
    assert stored_user["role"] == "trainer"
    stored_inv = await inv_db.invitations.find_one({"code": "TARGETED2"}, {"_id": 0})
    assert stored_inv["used_by"] == "target-user"


@pytest.mark.asyncio
async def test_open_invitation_still_usable_by_anyone_holding_the_code(inv_db):
    """No email set -> the pre-existing "possession of the code"
    behavior is unchanged (not a regression, a deliberate scope)."""
    await inv_db.users.insert_one({"id": "some-user", "email": "whoever@example.com"})
    await inv_db.invitations.insert_one(
        {
            "id": "i5",
            "code": "OPENCODE",
            "email": None,
            "role": "student",
            "org_id": None,
            "cohort_id": None,
            "invited_by": "u1",
            "used_by": None,
            "used_at": None,
            "expires_at": None,
            "created_at": "2026-09-07T00:00:00Z",
        }
    )
    await _apply_invitation("some-user", "OPENCODE", "whoever@example.com")
    stored = await inv_db.invitations.find_one({"code": "OPENCODE"}, {"_id": 0})
    assert stored["used_by"] == "some-user"


@pytest.mark.asyncio
async def test_end_to_end_register_with_mismatched_targeted_invite_rejected(inv_db):
    """Full register() path — SEC-02 exploit reproduced end to end:
    someone else obtains a targeted invite code and tries to register
    with their own email instead of the invited one."""
    await inv_db.invitations.insert_one(
        {
            "id": "i6",
            "code": "REGCODE",
            "email": "victim@example.com",
            "role": "trainer",
            "org_id": None,
            "cohort_id": None,
            "invited_by": "u1",
            "used_by": None,
            "used_at": None,
            "expires_at": None,
            "created_at": "2026-09-07T00:00:00Z",
        }
    )

    with pytest.raises(HTTPException) as exc:
        await register(
            RegisterInput(
                email="attacker@example.com",
                password="hunter22",
                display_name="Attacker",
                invite_code="REGCODE",
            )
        )
    assert exc.value.status_code == 400

    # No account and no invitation-consumption trace left behind by the
    # rejected attempt (register() inserts the user first, then applies
    # the invite — the failed apply must not leave the role escalated).
    attacker = await inv_db.users.find_one({"email": "attacker@example.com"}, {"_id": 0})
    assert attacker is not None
    assert attacker["role"] == "student"  # never promoted to "trainer"
    stored_inv = await inv_db.invitations.find_one({"code": "REGCODE"}, {"_id": 0})
    assert stored_inv["used_by"] is None

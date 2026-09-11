import os

import pytest
from fastapi import HTTPException

os.environ.setdefault("JWT_SECRET", "test-secret")

from api.orgs import _assert_invitation_role_allowed  # noqa: E402
from models import EXTERNAL_STAKEHOLDER_ROLES, User  # noqa: E402


def make_user(role: str, org_id: str = "org-a") -> User:
    return User(
        frek_id=f"FREK-{role}",
        email=f"{role}@example.test",
        display_name=role,
        password_hash="unused",
        role=role,
        org_id=org_id,
    )


def test_partner_and_institution_are_first_class_roles():
    assert EXTERNAL_STAKEHOLDER_ROLES == ("partner", "institution")
    assert make_user("partner").role == "partner"
    assert make_user("institution").role == "institution"


def test_trainer_can_invite_student_only():
    trainer = make_user("trainer")
    _assert_invitation_role_allowed(trainer, "student")

    with pytest.raises(HTTPException) as exc:
        _assert_invitation_role_allowed(trainer, "partner")
    assert exc.value.status_code == 403

    with pytest.raises(HTTPException) as exc:
        _assert_invitation_role_allowed(trainer, "institution")
    assert exc.value.status_code == 403


def test_admin_can_assign_external_stakeholder_roles():
    admin = make_user("admin")
    _assert_invitation_role_allowed(admin, "partner")
    _assert_invitation_role_allowed(admin, "institution")

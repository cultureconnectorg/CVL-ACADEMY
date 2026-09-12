"""Pure CareOps policy tests."""

from __future__ import annotations

import os

os.environ.setdefault("MONGO_URL", "mongodb://localhost:27017")
os.environ.setdefault("DB_NAME", "cvln_academy_test")

from services.careops import autonomy_policy, classify_message, make_fingerprint
from services.careops_incidents import INCIDENT_THRESHOLD, incident_action_type


def test_regular_question_goes_to_support():
    result = classify_message("Comment télécharger mon attestation ?")
    assert result.kind == "support"
    assert result.priority == "P3"
    assert result.queue == "support"


def test_access_problem_goes_to_support_queue():
    result = classify_message("Impossible de me connecter à mon compte")
    assert result.kind == "access"
    assert result.queue == "support"


def test_bug_goes_to_maintenance():
    result = classify_message("Le module ne fonctionne plus, erreur 500")
    assert result.kind == "maintenance"
    assert result.queue == "maintenance"


def test_claim_is_policy_guarded_without_founder_dependency():
    result = classify_message("Je conteste ce paiement et demande un remboursement")
    policy = autonomy_policy(result)
    assert result.kind == "claim"
    assert policy["mode"] == "policy_guarded"
    assert policy["founder_required"] is False
    assert policy["can_auto_close"] is False


def test_security_is_p0_and_specialist_routed():
    result = classify_message("Mon compte a été piraté")
    policy = autonomy_policy(result)
    assert result.kind == "security"
    assert result.priority == "P0"
    assert policy["review_queue"] == "security"


def test_fingerprint_is_stable_for_same_report():
    a = make_fingerprint("academy", "maintenance", "Erreur 500 sur le module 4")
    b = make_fingerprint("academy", "maintenance", "Erreur 500 sur le module 4")
    assert a == b
    assert len(a) == 24


def test_incident_threshold_is_explicit_and_conservative():
    assert INCIDENT_THRESHOLD == 3


def test_incident_domain_routing_is_not_all_technical_maintenance():
    assert incident_action_type("maintenance") == "technical_maintenance"
    assert incident_action_type("claim") == "claims_review"
    assert incident_action_type("payment") == "billing_investigation"
    assert incident_action_type("security") == "security_response"
    assert incident_action_type("support") == "service_recovery"

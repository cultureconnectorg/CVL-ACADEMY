"""Canonical Legal Core adapter for Protocol Master integrations."""
from services import legal_ops, legal_protocols, regulatory_applicability

BOUNDARIES = (
    "services.legal_ops",
    "services.legal_protocols",
    "services.regulatory_applicability",
)
services = (legal_ops, legal_protocols, regulatory_applicability)

"""Canonical Privacy Core adapter for Protocol Master integrations."""
from services import privacy_compliance, privacy_protocols

BOUNDARIES = (
    "services.privacy_compliance",
    "services.privacy_protocols",
)
services = (privacy_compliance, privacy_protocols)

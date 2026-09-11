"""Canonical Security Core adapter for Protocol Master integrations."""
from services import security_incident_protocol, security_verification

BOUNDARIES = (
    "services.security_verification",
    "services.security_incident_protocol",
)
services = (security_verification, security_incident_protocol)

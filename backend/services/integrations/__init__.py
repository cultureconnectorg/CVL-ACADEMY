"""Ecosystem integration interfaces — see base.py (the generic client),
registry.py (one instance per CVLN system + `all_integrations()` status),
and subscribers.py (wires them to domain events)."""

from .base import EcosystemIntegration, IntegrationNotConfigured
from .registry import all_integrations

__all__ = ["EcosystemIntegration", "IntegrationNotConfigured", "all_integrations"]

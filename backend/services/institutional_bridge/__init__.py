"""Institutional interoperability layer for CVLN Academy.

The bridge is additive: it does not replace existing organisation/cohort
features and it never claims a live institutional connection unless a
connector explicitly declares and implements one.
"""

from .registry import connector_registry, describe_connectors, prepare_case

__all__ = ["connector_registry", "describe_connectors", "prepare_case"]

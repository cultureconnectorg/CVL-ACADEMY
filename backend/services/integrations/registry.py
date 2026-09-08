"""The full CVLN ecosystem — rule 9's list, each as a decoupled interface.

FrekCore and CVLN Agent Factory already had their own richer clients
(services/frek_core.py, services/agent_factory.py — real local fallback
behavior, not just a gate) before this pass; they're included in
`all_integrations()` for one unified status view without being redefined
here as generic clients.
"""

from __future__ import annotations

from typing import Any, Dict, List

from services.agent_factory import agent_factory
from services.frek_core import frek_core

from .base import EcosystemIntegration

intelligence_os = EcosystemIntegration("CVLN Intelligence OS", "CVLN_INTELLIGENCE_OS")
brain = EcosystemIntegration("CVLN Brain", "CVLN_BRAIN")
command_center = EcosystemIntegration("CVLN Command Center", "CVLN_COMMAND_CENTER")
laurentia = EcosystemIntegration("Laurent.ia", "LAURENTIA")
kora = EcosystemIntegration("KORA", "KORA")
factory_maker_studio = EcosystemIntegration(
    "Factory Maker Studio", "FACTORY_MAKER_STUDIO"
)
good_mood = EcosystemIntegration("Good Mood", "GOOD_MOOD")
culture_connect = EcosystemIntegration("Culture Connect", "CULTURE_CONNECT")
kiltikonet = EcosystemIntegration("Kiltikonet", "KILTIKONET")
# ACA-0029 — the real external djsayd/CVLN-Wallet product (its own
# repo, its own backend/server.py — see docs/wal/README.md and the
# WAL-2X formations grounded directly against it), distinct from
# `backend/wallet/`, Academy's own internal CC/JCC ledger (rule 10,
# already documented in docs/INTEGRATIONS_REPORT.md as "CVLN Wallet
# (interne)") — that module stays exactly as-is, untouched by this
# integration. Named "djsayd" here, deliberately not the shorter "CVLN
# Wallet" the internal ledger's own doc row already uses, so the two
# are never confused for the same system. This is the outbound handoff
# *to* the real external product whenever Academy's own ledger records
# something worth reflecting there (see subscribers.py's
# `_on_badge_awarded`).
wallet = EcosystemIntegration("CVLN Wallet (djsayd, external)", "CVLN_WALLET")

_GENERIC = [
    intelligence_os,
    brain,
    command_center,
    laurentia,
    kora,
    factory_maker_studio,
    good_mood,
    culture_connect,
    kiltikonet,
    wallet,
]


def all_integrations() -> List[Dict[str, Any]]:
    """One row per ecosystem system — what the Admin dashboard and
    docs/INTEGRATIONS_REPORT.md both read from, so the report can never
    drift from what's actually wired."""
    rows = [g.describe() for g in _GENERIC]
    rows.append(
        {
            "name": "FrekCore",
            "configured": frek_core.is_remote_enabled(),
            "env_vars": ["FREK_CORE_BASE_URL", "FREK_CORE_API_KEY"],
        }
    )
    rows.append(
        {
            "name": "CVLN Agent Factory",
            "configured": agent_factory.is_remote_enabled(),
            "env_vars": ["CVLN_AGENT_FACTORY_URL", "CVLN_AGENT_FACTORY_API_KEY"],
        }
    )
    return rows

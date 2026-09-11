"""The full CVLN ecosystem — rule 9's list, each as a decoupled interface.

FrekCore, CVLN Agent Factory and CVLN Wallet have richer clients because they
own real runtime contracts. The generic integrations remain env-gated status
interfaces only.
"""

from __future__ import annotations

from typing import Any, Dict, List

from services.agent_factory import agent_factory
from services.cvln_wallet import cvln_wallet
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
]


def all_integrations() -> List[Dict[str, Any]]:
    """One row per ecosystem system for the Admin integration status view."""
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
    rows.append(cvln_wallet.describe())
    return rows

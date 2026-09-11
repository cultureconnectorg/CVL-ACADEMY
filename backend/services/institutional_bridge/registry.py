"""Capability registry for institutional interoperability.

A connector describes what CVLN can safely prepare today. It must not claim a
live write path merely because an institution exists or because credentials may
be added later. Live writes remain false until a target-specific adapter is
implemented and verified against an official/contractual interface.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

from .models import Capability, ConnectorDescriptor, FundingCase, PreparedEnvelope


class UnknownConnector(ValueError):
    pass


class UnsupportedCapability(ValueError):
    pass


@dataclass(frozen=True)
class ConnectorDefinition:
    code: str
    name: str
    connection_mode: str
    capabilities: Tuple[Capability, ...]
    notes: str
    credential_env_vars: Tuple[str, ...] = ()
    live_write_implemented: bool = False

    def configured(self) -> bool:
        if not self.credential_env_vars:
            return self.connection_mode not in {"UNAVAILABLE"}
        return all(bool(os.environ.get(name)) for name in self.credential_env_vars)

    def describe(self) -> ConnectorDescriptor:
        return ConnectorDescriptor(
            code=self.code,
            name=self.name,
            connection_mode=self.connection_mode,
            capabilities=list(self.capabilities),
            live_write_implemented=self.live_write_implemented,
            credential_env_vars=list(self.credential_env_vars),
            configured=self.configured(),
            notes=self.notes,
        )


_DEFINITIONS: Tuple[ConnectorDefinition, ...] = (
    ConnectorDefinition(
        code="edof",
        name="Mon Compte Formation / EDOF",
        connection_mode="STANDARD_FILE",
        capabilities=("CATALOG_EXPORT", "DOCUMENT_EXPORT"),
        notes="Preparation/export only. No live submission API is assumed.",
    ),
    ConnectorDefinition(
        code="france_travail",
        name="France Travail / KAIROS",
        connection_mode="PORTAL_ASSISTED",
        capabilities=("APPLICATION_PREPARE", "DOCUMENT_EXPORT"),
        notes="CVLN prepares a canonical case; portal submission remains a human/institutional action.",
    ),
    ConnectorDefinition(
        code="afdas",
        name="Afdas",
        connection_mode="PORTAL_ASSISTED",
        capabilities=("APPLICATION_PREPARE", "DOCUMENT_EXPORT", "INVOICE_PREPARE"),
        notes="No generic Afdas API is assumed. A contractual adapter can be added later without changing domain data.",
    ),
    ConnectorDefinition(
        code="agefma",
        name="AGEFMA / FORMANOO",
        connection_mode="PORTAL_ASSISTED",
        capabilities=("CATALOG_EXPORT", "DOCUMENT_EXPORT"),
        notes="Catalogue preparation is supported; no unauthorised portal automation is performed.",
    ),
    ConnectorDefinition(
        code="chorus_pro",
        name="Chorus Pro",
        connection_mode="OFFICIAL_API",
        capabilities=("INVOICE_PREPARE", "DOCUMENT_EXPORT"),
        credential_env_vars=("CHORUS_PRO_CLIENT_ID", "CHORUS_PRO_CLIENT_SECRET"),
        notes="Credentials may be detected; live writes stay disabled until a verified adapter exists.",
    ),
    ConnectorDefinition(
        code="demarche_numerique",
        name="Démarche numérique",
        connection_mode="OFFICIAL_API",
        capabilities=("STATUS_READ", "DOCUMENT_EXPORT"),
        credential_env_vars=("DEMARCHE_NUMERIQUE_API_TOKEN",),
        notes="Read capability is declared; no dossier mutation endpoint is invented.",
    ),
    ConnectorDefinition(
        code="france_competences",
        name="France compétences",
        connection_mode="OPEN_DATA",
        capabilities=("REFERENCE_DATA_READ",),
        notes="Use official/open reference data as source material; this is not a funding submission connector.",
    ),
    ConnectorDefinition(
        code="ladom",
        name="LADOM",
        connection_mode="PORTAL_ASSISTED",
        capabilities=("APPLICATION_PREPARE", "DOCUMENT_EXPORT"),
        notes="Preparation only until a documented/contractual machine interface exists for CVLN.",
    ),
    ConnectorDefinition(
        code="ctm_fse",
        name="CTM / FSE+ Martinique",
        connection_mode="MANUAL",
        capabilities=("APPLICATION_PREPARE", "DOCUMENT_EXPORT", "REPORTING"),
        notes="Canonical preparation/reporting only; programme-specific submission stays external.",
    ),
    ConnectorDefinition(
        code="agora",
        name="AGORA",
        connection_mode="UNAVAILABLE",
        capabilities=(),
        notes="No direct CVLN capability is claimed. Financeur-side interoperability requires a contract.",
    ),
)

connector_registry: Dict[str, ConnectorDefinition] = {
    item.code: item for item in _DEFINITIONS
}


def describe_connectors() -> Iterable[ConnectorDescriptor]:
    return [connector.describe() for connector in _DEFINITIONS]


def require_capability(
    connector_code: str, capability: Capability
) -> ConnectorDefinition:
    connector = connector_registry.get(connector_code)
    if connector is None:
        raise UnknownConnector(connector_code)
    if capability not in connector.capabilities:
        raise UnsupportedCapability(f"{connector_code} does not support {capability}")
    return connector


def prepare_case(
    funding_case: FundingCase,
    connector_code: str,
    capability: Capability = "APPLICATION_PREPARE",
) -> PreparedEnvelope:
    """Build a non-submitting envelope from the canonical FundingCase.

    The payload intentionally remains CVLN_CANONICAL_V1. A target schema mapper
    must be implemented from official evidence before this function may emit a
    financeur-specific format.
    """
    require_capability(connector_code, capability)
    return PreparedEnvelope(
        case_id=funding_case.id,
        connector_code=connector_code,
        capability=capability,
        payload=funding_case.model_dump(),
    )

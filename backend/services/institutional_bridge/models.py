"""Canonical models for institutional funding and interoperability.

These models deliberately describe CVLN's own canonical data. Target-system
payloads belong in explicit adapters once an institution publishes or grants
a real contract/API/schema.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


def _uid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


ConnectionMode = Literal[
    "OFFICIAL_API",
    "PARTNER_PRIVATE_API",
    "OPEN_DATA",
    "STANDARD_FILE",
    "PORTAL_ASSISTED",
    "MANUAL",
    "UNAVAILABLE",
]

Capability = Literal[
    "CATALOG_EXPORT",
    "REFERENCE_DATA_READ",
    "ELIGIBILITY_LOOKUP",
    "APPLICATION_PREPARE",
    "APPLICATION_SUBMIT",
    "STATUS_READ",
    "ATTENDANCE_EXPORT",
    "DOCUMENT_EXPORT",
    "INVOICE_PREPARE",
    "INVOICE_SUBMIT",
    "REPORTING",
    "WEBHOOK",
]

InstitutionType = Literal[
    "FUNDER",
    "PUBLIC_INSTITUTION",
    "EMPLOYER",
    "TRAINING_PROVIDER",
    "TERRITORIAL_PARTNER",
    "OTHER",
]

FundingCaseStatus = Literal[
    "DRAFT",
    "READY",
    "SUBMITTED",
    "APPROVED",
    "PARTIALLY_APPROVED",
    "REJECTED",
    "CLOSED",
]


class ConnectorDescriptor(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    name: str
    connection_mode: ConnectionMode
    capabilities: List[Capability] = Field(default_factory=list)
    live_write_implemented: bool = False
    credential_env_vars: List[str] = Field(default_factory=list)
    configured: bool = False
    notes: str


class InstitutionProfileInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    institution_type: InstitutionType
    territories: List[str] = Field(default_factory=list)
    sectors: List[str] = Field(default_factory=list)
    connector_codes: List[str] = Field(default_factory=list)
    notes: Optional[str] = Field(default=None, max_length=2000)


class InstitutionProfile(InstitutionProfileInput):
    org_id: str
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)


class FundingCaseInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    org_id: str
    beneficiary_user_id: Optional[str] = None
    formation_code: str = Field(min_length=1, max_length=80)
    territory: str = Field(min_length=1, max_length=120)
    funding_scheme: str = Field(min_length=1, max_length=160)
    amount_requested_eur: Optional[float] = Field(default=None, ge=0)
    cofunding_eur: Optional[float] = Field(default=None, ge=0)
    documents: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FundingCase(FundingCaseInput):
    id: str = Field(default_factory=_uid)
    status: FundingCaseStatus = "DRAFT"
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)


class PreparedEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    connector_code: str
    capability: Capability
    format: Literal["CVLN_CANONICAL_V1"] = "CVLN_CANONICAL_V1"
    generated_at: str = Field(default_factory=_now)
    payload: Dict[str, Any]
    live_submission_performed: Literal[False] = False

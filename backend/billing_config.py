"""Production readiness gate for CVLN Academy billing.

No issuer identity or tax treatment is inferred. Production starts only when
explicit deployment configuration is sufficient for legal invoice issuance.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

from billing import BillingPolicyError, issuer_profile
from billing_einvoice import tax_policy

PRODUCTION_ENVIRONMENTS = {"prod", "production"}

ISSUER_ENV_BY_FIELD = {
    "legal_name": "ACADEMY_BILLING_LEGAL_NAME",
    "country": "ACADEMY_BILLING_COUNTRY",
    "registration_id": "ACADEMY_BILLING_REGISTRATION_ID",
    "address_line1": "ACADEMY_BILLING_ADDRESS_LINE1",
    "city": "ACADEMY_BILLING_CITY",
    "postal_code": "ACADEMY_BILLING_POSTAL_CODE",
    "invoice_series": "ACADEMY_BILLING_INVOICE_SERIES",
}

TAX_ENV_VARS = (
    "ACADEMY_BILLING_TAX_MODE",
    "ACADEMY_BILLING_TAX_RATE_PERCENT",
)


def academy_environment() -> str:
    return os.environ.get("ACADEMY_ENV", "development").strip().lower()


def production_billing_required() -> bool:
    return academy_environment() in PRODUCTION_ENVIRONMENTS


def billing_production_status() -> Dict[str, Any]:
    profile = issuer_profile()
    missing_issuer: List[str] = [
        env_name
        for field, env_name in ISSUER_ENV_BY_FIELD.items()
        if not str(profile.get(field) or "").strip()
    ]

    missing_tax = [name for name in TAX_ENV_VARS if not os.environ.get(name, "").strip()]
    tax_error = None
    tax_ready = False
    if not missing_tax:
        try:
            tax_policy()
            tax_ready = True
        except BillingPolicyError as exc:
            tax_error = str(exc)

    profile_supported = profile.get("einvoice_profile") == "FACTUR-X_EN16931"
    ready = not missing_issuer and not missing_tax and tax_ready and profile_supported
    return {
        "environment": academy_environment(),
        "required": production_billing_required(),
        "ready": ready,
        "issuer_ready": not missing_issuer,
        "tax_ready": tax_ready,
        "einvoice_profile_ready": profile_supported,
        "missing_env": sorted(set(missing_issuer + missing_tax)),
        "tax_error": tax_error,
        "einvoice_profile": profile.get("einvoice_profile"),
    }


def assert_billing_production_ready() -> Dict[str, Any]:
    status = billing_production_status()
    if not status["required"]:
        return status
    if status["ready"]:
        return status

    details = []
    if status["missing_env"]:
        details.append("missing=" + ",".join(status["missing_env"]))
    if status["tax_error"]:
        details.append("tax=" + str(status["tax_error"]))
    if not status["einvoice_profile_ready"]:
        details.append("einvoice_profile=FACTUR-X_EN16931 required")
    detail = "; ".join(details) or "unknown billing configuration error"
    raise RuntimeError(f"BILLING_PRODUCTION_NOT_READY: {detail}")

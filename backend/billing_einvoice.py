"""Factur-X / EN16931 invoice artifact generation for CVLN Academy.

The commercial amount comes from the immutable Economy 3D order snapshot.
Tax treatment and issuer identity are explicit deployment policy. No legal or
tax datum is inferred from a learner profile.
"""

from __future__ import annotations

import base64
import hashlib
import io
import os
from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Dict, Tuple

from facturx import generate_from_binary, generate_xml, xml_check_xsd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from billing import BillingNotReady, BillingPolicyError, issuer_profile

MONEY = Decimal("0.01")


def _money(value: Any) -> Decimal:
    return Decimal(str(value)).quantize(MONEY, rounding=ROUND_HALF_UP)


def _service_delivery_at(document: Dict[str, Any]) -> datetime:
    """Use the exact Academy access-activation event as digital delivery date.

    The commercial runtime grants the entitlement at the same `paid_at` event;
    therefore this is system evidence, not an inferred or invented service date.
    """
    raw = str(document.get("paid_at") or "").strip()
    if not raw:
        raise BillingNotReady("Paid order is missing access delivery timestamp")
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise BillingNotReady("Invalid paid_at delivery timestamp") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def tax_policy() -> Dict[str, Any]:
    mode = os.environ.get("ACADEMY_BILLING_TAX_MODE", "").strip().upper()
    rate_raw = os.environ.get("ACADEMY_BILLING_TAX_RATE_PERCENT", "").strip()
    category = os.environ.get("ACADEMY_BILLING_TAX_CATEGORY", "").strip().upper()
    exemption_reason = os.environ.get(
        "ACADEMY_BILLING_TAX_EXEMPTION_REASON", ""
    ).strip()
    if mode not in {"STANDARD", "EXEMPT"}:
        raise BillingNotReady("ACADEMY_BILLING_TAX_MODE must be STANDARD or EXEMPT")
    if not rate_raw:
        raise BillingNotReady("ACADEMY_BILLING_TAX_RATE_PERCENT is required")
    try:
        rate = Decimal(rate_raw)
    except Exception as exc:  # pragma: no cover - defensive parsing
        raise BillingNotReady("Invalid ACADEMY_BILLING_TAX_RATE_PERCENT") from exc
    if mode == "STANDARD":
        if rate <= 0:
            raise BillingNotReady("STANDARD tax mode requires a positive tax rate")
        category = category or "S"
    else:
        if rate != 0:
            raise BillingNotReady("EXEMPT tax mode requires a zero tax rate")
        category = category or "E"
        if not exemption_reason:
            raise BillingNotReady(
                "EXEMPT tax mode requires ACADEMY_BILLING_TAX_EXEMPTION_REASON"
            )
    return {
        "mode": mode,
        "rate": rate,
        "category": category,
        "exemption_reason": exemption_reason,
    }


def buyer_profile_ready(profile: Dict[str, Any]) -> bool:
    return all(
        str(profile.get(key) or "").strip()
        for key in ("legal_name", "address_line1", "city", "postal_code", "country")
    )


def assert_buyer_profile_ready(profile: Dict[str, Any]) -> None:
    if not buyer_profile_ready(profile):
        raise BillingNotReady(
            "Buyer billing profile requires legal_name, address_line1, city, postal_code, country"
        )


def invoice_breakdown(gross_eur: Any) -> Dict[str, Decimal]:
    gross = _money(gross_eur)
    if gross <= 0:
        raise BillingPolicyError("Invoice total must be positive")
    policy = tax_policy()
    if policy["mode"] == "STANDARD":
        divisor = Decimal("1") + (policy["rate"] / Decimal("100"))
        net = (gross / divisor).quantize(MONEY, rounding=ROUND_HALF_UP)
        tax = (gross - net).quantize(MONEY, rounding=ROUND_HALF_UP)
    else:
        net = gross
        tax = Decimal("0.00")
    return {"gross": gross, "net": net, "tax": tax, "rate": policy["rate"]}


def build_en16931_data(
    document: Dict[str, Any], buyer: Dict[str, Any], issued_at: datetime
) -> Dict[str, Any]:
    assert_buyer_profile_ready(buyer)
    issuer = issuer_profile()
    number = str(document.get("legal_invoice_number") or "").strip()
    if not number:
        raise BillingNotReady("Legal invoice number is required before XML generation")
    breakdown = invoice_breakdown(document["amount_eur"])
    policy = tax_policy()
    delivery_at = _service_delivery_at(document)
    item_name = str(
        document.get("pricing_snapshot", {}).get("economy_code")
        or document.get("economy_code")
        or "CVLN Academy"
    )

    data: Dict[str, Any] = {
        "BT-1": number,
        "BT-2": issued_at,
        "BT-3": "380",
        "BT-5": "EUR",
        "BT-20": "Paid via CVLN Wallet",
        "BT-27": issuer["legal_name"],
        "BT-30": issuer["registration_id"],
        "BT-30-1": issuer.get("registration_scheme") or "0002",
        "BT-35": issuer["address_line1"],
        "BT-37": issuer["city"],
        "BT-38": issuer["postal_code"],
        "BT-40": issuer["country"],
        "BT-44": buyer["legal_name"],
        "BT-50": buyer["address_line1"],
        "BT-52": buyer["city"],
        "BT-53": buyer["postal_code"],
        "BT-55": str(buyer["country"]).upper(),
        "BT-58": buyer.get("email"),
        "BT-72": delivery_at,
        "BG-23": [
            {
                "BT-116": str(breakdown["net"]),
                "BT-117": str(breakdown["tax"]),
                "BT-118": policy["category"],
                "BT-119": str(policy["rate"]),
                **(
                    {"BT-120": policy["exemption_reason"]}
                    if policy["mode"] == "EXEMPT"
                    else {}
                ),
            }
        ],
        "BT-106": str(breakdown["net"]),
        "BT-109": str(breakdown["net"]),
        "BT-110": str(breakdown["tax"]),
        "BT-110-1": "EUR",
        "BT-112": str(breakdown["gross"]),
        "BT-115": "0.00",
        "BG-25": [
            {
                "BT-126": "1",
                "BT-127": f"CVLN Academy {item_name}",
                "BT-153": item_name,
                "BT-146": str(breakdown["net"]),
                "BT-129": "1",
                "BT-130": "C62",
                "BT-151": policy["category"],
                "BT-152": str(policy["rate"]),
                "BT-131": str(breakdown["net"]),
                **(
                    {"BT-161": policy["exemption_reason"]}
                    if policy["mode"] == "EXEMPT"
                    else {}
                ),
            }
        ],
    }
    if issuer.get("vat_id"):
        data["BT-31"] = issuer["vat_id"]
    if buyer.get("vat_id"):
        data["BT-48"] = buyer["vat_id"]
    if buyer.get("registration_id"):
        data["BT-47"] = buyer["registration_id"]
        data["BT-47-1"] = buyer.get("registration_scheme") or "0002"
    return {key: value for key, value in data.items() if value not in (None, "")}


def _render_regular_pdf(
    document: Dict[str, Any], buyer: Dict[str, Any], issued_at: datetime
) -> bytes:
    issuer = issuer_profile()
    breakdown = invoice_breakdown(document["amount_eur"])
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    _, height = A4
    y = height - 55
    c.setFont("Helvetica-Bold", 18)
    c.drawString(48, y, f"FACTURE {document['legal_invoice_number']}")
    y -= 28
    c.setFont("Helvetica", 9)
    c.drawString(48, y, f"Émise le {issued_at.date().isoformat()}")
    y -= 28
    c.setFont("Helvetica-Bold", 10)
    c.drawString(48, y, "Émetteur")
    c.drawString(310, y, "Client")
    y -= 15
    c.setFont("Helvetica", 9)
    for left, right in zip(
        [
            issuer["legal_name"],
            issuer["address_line1"],
            f"{issuer['postal_code']} {issuer['city']}",
            issuer["country"],
            f"ID: {issuer['registration_id']}",
        ],
        [
            buyer["legal_name"],
            buyer["address_line1"],
            f"{buyer['postal_code']} {buyer['city']}",
            str(buyer["country"]).upper(),
            buyer.get("email") or "",
        ],
    ):
        c.drawString(48, y, str(left))
        c.drawString(310, y, str(right))
        y -= 13
    y -= 20
    c.setFont("Helvetica-Bold", 9)
    c.drawString(48, y, "Description")
    c.drawRightString(545, y, "Montant TTC")
    y -= 18
    c.setFont("Helvetica", 9)
    description = f"CVLN Academy — {document.get('economy_code', '')}"
    c.drawString(48, y, description)
    c.drawRightString(545, y, f"{breakdown['gross']} EUR")
    y -= 28
    c.drawRightString(545, y, f"HT: {breakdown['net']} EUR")
    y -= 13
    c.drawRightString(545, y, f"Taxe: {breakdown['tax']} EUR")
    y -= 13
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(545, y, f"Total payé: {breakdown['gross']} EUR")
    y -= 28
    c.setFont("Helvetica", 8)
    c.drawString(48, y, f"Order: {document.get('order_id')}")
    y -= 11
    c.drawString(48, y, f"Payment attempt: {document.get('payment_attempt_id')}")
    y -= 11
    c.drawString(48, y, f"FREK-ID: {document.get('user_frek_id')}")
    y -= 11
    c.drawString(48, y, "Paiement confirmé via CVLN Wallet.")
    c.showPage()
    c.save()
    return buf.getvalue()


def generate_invoice_artifacts(
    document: Dict[str, Any], buyer: Dict[str, Any], issued_at: datetime | None = None
) -> Dict[str, Any]:
    issued = issued_at or datetime.now(timezone.utc)
    data = build_en16931_data(document, buyer, issued)
    xml_bytes = generate_xml(data, flavor="factur-x", level="en16931")
    xml_check_xsd(xml_bytes, flavor="factur-x", level="en16931")
    regular_pdf = _render_regular_pdf(document, buyer, issued)
    facturx_pdf = generate_from_binary(
        regular_pdf,
        xml_bytes,
        flavor="factur-x",
        level="en16931",
        check_xsd=True,
        check_schematron=False,
        lang="fr-FR",
    )
    if not isinstance(facturx_pdf, bytes) or not facturx_pdf.startswith(b"%PDF"):
        raise BillingPolicyError("Factur-X generator did not return a PDF")
    return {
        "format": "FACTUR-X_EN16931",
        "xml_b64": base64.b64encode(xml_bytes).decode("ascii"),
        "pdf_b64": base64.b64encode(facturx_pdf).decode("ascii"),
        "xml_sha256": hashlib.sha256(xml_bytes).hexdigest(),
        "pdf_sha256": hashlib.sha256(facturx_pdf).hexdigest(),
        "xml_size": len(xml_bytes),
        "pdf_size": len(facturx_pdf),
        "xsd_validation": "PASS",
        "schematron_validation": "NOT_RUN",
        "issued_at": issued.isoformat(),
    }


def decode_artifact(document: Dict[str, Any], kind: str) -> Tuple[bytes, str]:
    artifact = document.get("artifact") or {}
    if kind == "pdf":
        payload = artifact.get("pdf_b64")
        media_type = "application/pdf"
    elif kind == "xml":
        payload = artifact.get("xml_b64")
        media_type = "application/xml"
    else:
        raise BillingPolicyError("Unsupported artifact kind")
    if not payload:
        raise BillingPolicyError("Invoice artifact is missing")
    return base64.b64decode(payload), media_type

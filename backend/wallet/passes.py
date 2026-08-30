"""Apple Wallet / Google Wallet pass payloads.

"Compatible" (rule 10) means: the pass *data* is built in each platform's
documented shape. Turning that into an installable pass still needs a
signed .pkpass (Apple — requires an Apple Developer WWDR certificate +
Pass Type ID) or a signed JWT save link (Google — requires a Google Wallet
Issuer account). Neither exists yet, so signing is explicitly left as a
501 rather than shipping something that looks installable but silently
isn't — see api/wallet.py.
"""

from __future__ import annotations

from typing import Any, Dict

from .models import WalletAccount


def build_apple_pass_payload(
    user_frek_id: str, display_name: str, account: WalletAccount
) -> Dict[str, Any]:
    """Shape of an Apple PassKit `generic.pass.json` (unsigned)."""
    return {
        "formatVersion": 1,
        "passTypeIdentifier": "pass.io.cvln.academy",  # placeholder — needs a real Pass Type ID
        "serialNumber": user_frek_id,
        "organizationName": "CVLN Academy",
        "description": "CVLN Academy — Carte FREK",
        "generic": {
            "primaryFields": [
                {"key": "frek_id", "label": "FREK-ID", "value": user_frek_id}
            ],
            "secondaryFields": [
                {"key": "name", "label": "Nom", "value": display_name},
                {"key": "jcc", "label": "JCC", "value": str(account.jcc_balance)},
            ],
            "auxiliaryFields": [
                {"key": "badges", "label": "Badges", "value": str(len(account.badges))}
            ],
        },
        "barcode": {
            "format": "PKBarcodeFormatQR",
            "message": user_frek_id,
            "messageEncoding": "iso-8859-1",
        },
    }


def build_google_pass_payload(
    user_frek_id: str, display_name: str, account: WalletAccount
) -> Dict[str, Any]:
    """Shape of a Google Wallet `genericObject` (unsigned — normally wrapped
    in a signed JWT for the "Add to Google Wallet" save link)."""
    return {
        "id": f"cvln-academy.{user_frek_id}",
        "classId": "cvln-academy.generic-class",
        "genericType": "GENERIC_TYPE_UNSPECIFIED",
        "cardTitle": {"defaultValue": {"language": "fr", "value": "CVLN Academy"}},
        "subheader": {"defaultValue": {"language": "fr", "value": display_name}},
        "header": {"defaultValue": {"language": "fr", "value": user_frek_id}},
        "textModulesData": [
            {"header": "JCC", "body": str(account.jcc_balance)},
            {"header": "Badges", "body": str(len(account.badges))},
        ],
        "barcode": {"type": "QR_CODE", "value": user_frek_id},
    }

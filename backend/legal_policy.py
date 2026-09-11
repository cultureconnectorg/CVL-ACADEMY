"""Versioned legal bundle required before an Academy journey can start.

Keep this module deliberately small and immutable. Whenever the substantive
content of a required document changes, bump the document version and the
LEGAL_BUNDLE_VERSION. Existing users will then be asked to acknowledge the
new bundle before continuing.
"""

from __future__ import annotations

import hashlib
import json

LEGAL_BUNDLE_VERSION = "2026-09-11.1"

# Privacy is acknowledged, not "consented to": the lawful basis for processing
# is determined per processing purpose and is not replaced by a checkbox.
LEGAL_DOCUMENTS = [
    {
        "id": "cgu",
        "version": "2026-09-11.1",
        "label": "Conditions générales d’utilisation",
        "mode": "accept",
        "url": "/legal/cgu",
        "canonical": "Usage loyal; sécurité; droits des tiers; interdiction fraude, usurpation, extraction abusive, code malveillant, harcèlement et contenus illicites; règles de suspension, responsabilité, propriété intellectuelle et litiges selon l’entité contractante.",
    },
    {
        "id": "reglement-academy",
        "version": "2026-09-11.1",
        "label": "Règlement & accord Academy",
        "mode": "accept",
        "url": "/legal/reglement-academy",
        "canonical": "Assiduité; sécurité; respect; locaux et équipements; confidentialité; propriété intellectuelle; IA responsable; fraude; évaluations; sanctions; réclamations; parcours financés; contrôle humain des décisions engageantes.",
    },
    {
        "id": "charte-ia",
        "version": "2026-09-11.1",
        "label": "Charte IA & transparence",
        "mode": "acknowledge",
        "url": "/legal/charte-ia",
        "canonical": "Transparence des interactions IA lorsque requise; Human Authority; aucune décision finale autonome d’admission, certification, sanction, finance ou contrat; signalement des contenus générés/manipulés lorsque requis.",
    },
    {
        "id": "confidentialite",
        "version": "2026-09-11.1",
        "label": "Politique de confidentialité",
        "mode": "acknowledge",
        "url": "/legal/confidentialite",
        "canonical": "Information RGPD sur finalités, bases juridiques, droits, minimisation, conservation, destinataires, sous-traitants, transferts éventuels et contrôle humain; cette prise de connaissance n’est pas un consentement global au traitement.",
    },
]


def _digest(doc: dict) -> str:
    payload = json.dumps(
        {"id": doc["id"], "version": doc["version"], "canonical": doc["canonical"]},
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


PUBLIC_LEGAL_DOCUMENTS = [
    {k: v for k, v in doc.items() if k != "canonical"} | {"sha256": _digest(doc)}
    for doc in LEGAL_DOCUMENTS
]
DOCUMENT_BY_ID = {doc["id"]: doc for doc in PUBLIC_LEGAL_DOCUMENTS}
REQUIRED_DOCUMENT_IDS = tuple(doc["id"] for doc in PUBLIC_LEGAL_DOCUMENTS)

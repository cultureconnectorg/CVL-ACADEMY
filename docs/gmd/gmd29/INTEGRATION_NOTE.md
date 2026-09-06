# GMD-29 — Integration Academy Package Note

## Réel vs. supposé

**Réel (vérifié cette session) :** `POST /newsletter`, `GET
/admin/newsletter`, `GET /admin/newsletter/export`
(`server.py:241-252`), `send_newsletter_welcome`'s real `copy` dict
(`email_service.py:64-82`) — 4 keys `fr/en/es/kr`, `"kr"` mislabeled
(content is Haitian Creole, not Korean), fallback to `fr` for any
unimplemented key. No unsubscribe route exists in the audited code.

**Supposé :** un lien `GMD29.SKILL.*` réel dans le runtime de cette
Academy — inexistant.

## Dépendances

- `GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`, `EVIDENCE_ARCHITECTURE.md`,
  `ECONOMIC_MODEL.md`, GMD-21/26 (prérequis).

## Ce qu'une future intégration exigerait

1. Entrée `GMD29` dans le registre de certification.
2. Surface candidat réelle.
3. Décision séparée sur les identifiants admin réels.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD29`. `FULLY_COMPLETE` non déclaré.

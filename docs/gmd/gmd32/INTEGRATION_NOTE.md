# GMD-32 — Integration Academy Package Note

## Réel vs. supposé

**Réel (vérifié cette session, fichier lu en entier) :**
`wallet_service.py` — `push_ticket()`, `_post()`, `retry_loop()`,
mêmes 5 backoffs que GMD-31, payload `wallet_action: "push_ticket"` +
`ticket{}`, endpoint `{WALLET_URL}/wallet/tickets`, `GET /admin/
outbox/wallet` (`server.py:770-773`). Le fichier lui-même documente
son propre statut provisoire ("Payload contract to be finalised with
wallet team"). Confirmé distinct de `backend/wallet/` de cette
Academy.

**Supposé :** un lien `GMD32.SKILL.*` réel dans le runtime de cette
Academy — inexistant.

## Dépendances

- `GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`, `WALLET_CVE_RECONCILIATION.md`
  (décrit le vrai ledger `backend/wallet/` de cette Academy),
  `EVIDENCE_ARCHITECTURE.md`, `ECONOMIC_MODEL.md`, GMD-21/24
  (prérequis).

## Ce qu'une future intégration exigerait

1. Entrée `GMD32` dans le registre de certification.
2. Surface candidat réelle.
3. Décision séparée sur les identifiants admin réels.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD32`. `FULLY_COMPLETE` non déclaré.

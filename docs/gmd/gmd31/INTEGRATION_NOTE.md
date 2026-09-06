# GMD-31 — Integration Academy Package Note

## Réel vs. supposé

**Réel (vérifié cette session, fichier lu en entier) :**
`frek_service.py` — `emit()`, `_post()`, `retry_loop()`, les 5
backoffs exacts, `GET /admin/outbox/frek-id` (`server.py:765-768`).
Confirmé : ce système est distinct de `backend/services/frek_core.py`
de cette Academy — aucune connexion entre les deux observée.

**Supposé :** un lien `GMD31.SKILL.*` réel dans le runtime de cette
Academy — inexistant.

## Dépendances

- `GOOD_MOOD_DJ_SAYD_RECONCILIATION.md` (cite déjà cette distinction),
  `EVIDENCE_ARCHITECTURE.md`, `ECONOMIC_MODEL.md`, GMD-21 (prérequis).

## Ce qu'une future intégration exigerait

1. Entrée `GMD31` dans le registre de certification.
2. Surface candidat réelle.
3. Décision séparée sur les identifiants admin réels.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD31`. `FULLY_COMPLETE` non déclaré.

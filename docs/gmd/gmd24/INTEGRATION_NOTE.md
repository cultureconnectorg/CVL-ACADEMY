# GMD-24 — Integration Academy Package Note

## Réel vs. supposé

**Réel (vérifié cette session) :** `TicketTypeIn`/`TicketType`
(`server.py:115-131`), la formule `remaining = quota - sold`, le
check-au-checkout non atomique, l'incrément `$inc` atomique + upsert
fan dans `_issue_tickets_for_session` (`server.py:574-620`), la route
QR (`server.py:706-713`).

**Supposé :** un lien `GMD24.SKILL.*` réel dans le runtime de cette
Academy — inexistant (`NO_RUNTIME_BINDING`).

## Dépendances

- `GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`, `EVIDENCE_ARCHITECTURE.md`,
  `ECONOMIC_MODEL.md`, GMD-21, GMD-23 (prérequis).

## Ce qu'une future intégration exigerait

1. Entrée `GMD24` dans le registre de certification.
2. Surface candidat réelle.
3. Décision séparée sur les identifiants admin réels.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD24`. `FULLY_COMPLETE` non déclaré.

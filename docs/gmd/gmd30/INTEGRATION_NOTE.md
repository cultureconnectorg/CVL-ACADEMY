# GMD-30 — Integration Academy Package Note

## Réel vs. supposé

**Réel (vérifié cette session) :** `admin_event_tickets`,
`admin_event_report` (`server.py:389-410`) — calcul exact de
`revenue_cents` (théorique, `sold × price_cents`), `fill_rate` (garde
contre division par zéro), `checked_in`, et les deux caps distincts
(2000 sur les tickets bruts, 5000 sur l'agrégation).

**Supposé :** un lien `GMD30.SKILL.*` réel dans le runtime de cette
Academy — inexistant.

## Dépendances

- `GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`, `EVIDENCE_ARCHITECTURE.md`,
  `ECONOMIC_MODEL.md`, GMD-21/23/24/25 (prérequis), GMD-28 (source
  réelle des paiements confirmés, distincte de ce rapport).

## Ce qu'une future intégration exigerait

1. Entrée `GMD30` dans le registre de certification.
2. Surface candidat réelle.
3. Décision séparée sur les identifiants admin réels.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD30`. `FULLY_COMPLETE` non déclaré.

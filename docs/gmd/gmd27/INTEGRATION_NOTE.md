# GMD-27 — Integration Academy Package Note

## Réel vs. supposé

**Réel (vérifié cette session) :** `ProductIn`/`Product`
(`server.py:133-150`), les 4 routes admin merch + route publique
filtrée `active` (`server.py:255`, `440-467`), `_sync_stripe_item`
avec préfixe `"gm"` (`server.py:165-188`, `192`) distinct du préfixe
`"gmtt"` des ticket types.

**Supposé :** un lien `GMD27.SKILL.*` réel dans le runtime de cette
Academy — inexistant.

## Dépendances

- `GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`, `EVIDENCE_ARCHITECTURE.md`,
  `ECONOMIC_MODEL.md`, GMD-21 (prérequis), GMD-28 (aval).

## Ce qu'une future intégration exigerait

1. Entrée `GMD27` dans le registre de certification.
2. Surface candidat réelle.
3. Décision séparée sur les identifiants admin réels.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD27`. `FULLY_COMPLETE` non déclaré.

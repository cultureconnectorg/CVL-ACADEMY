# GMD-26 — Integration Academy Package Note

## Réel vs. supposé

**Réel (vérifié cette session) :** `upsert_fan`
(`ticketing_service.py:24-70`) — champs `purchases`, `total_events`,
`cities`, `segments` (`primo`/`recurring`/`vip`), `external_id`
(collision possible sur le local-part d'email, un vrai edge case de
qualité de données). Ce fait corrige une sous-estimation initiale du
`REFERENTIAL.md` ("no analytics beyond raw table") — corrigé dans ce
package.

**Supposé :** un lien `GMD26.SKILL.*` réel dans le runtime de cette
Academy — inexistant.

## Dépendances

- `GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`, `EVIDENCE_ARCHITECTURE.md`,
  `ECONOMIC_MODEL.md`, GMD-21 (prérequis), GMD-24 (source des achats).

## Ce qu'une future intégration exigerait

1. Entrée `GMD26` dans le registre de certification.
2. Surface candidat réelle.
3. Décision séparée sur les identifiants admin réels.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD26`. `FULLY_COMPLETE` non déclaré.

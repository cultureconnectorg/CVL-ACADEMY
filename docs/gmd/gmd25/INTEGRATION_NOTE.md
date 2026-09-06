# GMD-25 — Integration Academy Package Note

## Réel vs. supposé

**Réel (vérifié cette session) :** `POST /scan/check`, `GET /scan/
counter/{eid}` (`server.py:715-753`), les 3 vrais résultats, l'emit
FREK sur scan valide (best-effort, try/except), l'absence confirmée de
tout mécanisme d'incident/rollback (GMD-34).

**Supposé :** un lien `GMD25.SKILL.*` réel dans le runtime de cette
Academy — inexistant.

## Dépendances

- `GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`, `EVIDENCE_ARCHITECTURE.md`,
  `ECONOMIC_MODEL.md`, GMD-21/23/24 (prérequis), `gmd34/GAP.md`
  (limite explicite citée dans M3).

## Ce qu'une future intégration exigerait

1. Entrée `GMD25` dans le registre de certification.
2. Surface candidat réelle (idéalement un simulateur de scan-night,
   pas seulement du markdown).
3. Une vraie procédure d'incident (GMD-34) avant que cette formation
   puisse enseigner autre chose que l'escalade pure.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_GMD25`. `FULLY_COMPLETE` non déclaré.

# FRK-32 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** `VALID_SIGNALS` (`frek_core.py`) reste les 8 valeurs
strictes (`FREK-TIME`, `FREK-WORK`, `FREK-SCORE`, `FREK-LINK`,
`FREK-CERT`, `FREK-CONTRIB`, `FREK-SHARE`, `FREK-MISSION`) ; aucune
gouvernance de consentement n'est implémentée par cette formation —
elle référence Fondation Cœurvolan §18 sans la dupliquer.

**Supposé :** `FRK32.SKILL.*` réel — inexistant.

## Dépendances

`FREK_01_75_RECONCILIATION.md`, `backend/services/frek_core.py`
(frontière obligatoire, source du fait `VALID_SIGNALS`), doctrine
Fondation Cœurvolan §18 (référencée, jamais dupliquée),
`docs/frk/frk31/REFERENTIAL.md` (même discipline de frontière
`VALID_SIGNALS`).

## Ce qu'une future intégration exigerait

1. Une entrée `FRK32` dans le registre de certification de cette
   Academy.
2. Une surface candidat réelle (ce corpus est markdown seul).
3. Un registre de consentement réel géré par Fondation Cœurvolan,
   référencé (jamais porté) par la capture technique — inexistant
   aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment
+ rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.

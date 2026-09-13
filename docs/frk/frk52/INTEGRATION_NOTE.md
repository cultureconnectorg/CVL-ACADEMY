# FRK-52 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** `frek_core.py` = `FrekCoreClient`, client Python interne
appelé en-process par le backend Academy, sans route HTTP propre. La
discipline réelle d'ingénierie d'API (versionnage, gestion d'erreur)
comme pratique marché-générale.

**Supposé :** `FRK52.SKILL.*` réel — inexistant ; toute API publique
FREK — non implémentée (`CAPABILITY_NOT_IMPLEMENTED`).

## Dépendances

`FREK_01_75_RECONCILIATION.md`, `backend/services/frek_core.py`
(contre-exemple cité, source du fait), `docs/frk/frk53/
REFERENTIAL.md` (spécialisation avale, réutilisée par référence).

## Ce qu'une future intégration exigerait

1. Une API FREK publique réelle avant que ce sujet ait une application
   CVLN concrète.
2. Une entrée `FRK52` dans le registre de certification de cette
   Academy, namespace distinct de `FRK53.SKILL.*`.
3. Un vrai design d'API à évaluer par un correcteur humain —
   inexistant aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment
+ rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.

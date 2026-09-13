# FRK-20 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** la discipline réelle de conception offline-first
(store-and-forward, vérification cryptographique locale) comme
pratique marché-générale. `is_remote_enabled()` (`frek_core.py`) est
une simple bascule de disponibilité réseau
(`bool(FREK_CORE_BASE_URL)`, faux par défaut).

**Supposé :** `FRK20.SKILL.*` réel dans le runtime de cette Academy —
inexistant (`NO_RUNTIME_BINDING`). Toute vérification offline CVLN
réelle — jamais accordée (`CAPABILITY_NOT_IMPLEMENTED`).

## Dépendances

`FREK_01_75_RECONCILIATION.md`, `backend/services/frek_core.py`
(contre-exemple cité, jamais présenté comme implémentation du sujet),
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `FRK20` dans le registre de certification de cette
   Academy.
2. Une surface candidat réelle (ce corpus est markdown seul).
3. Un vrai flux offline-first à évaluer par un correcteur humain —
   inexistant aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment
+ rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.

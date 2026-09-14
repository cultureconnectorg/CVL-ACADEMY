# FRK-09 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** la discipline de cycle de vie d'identité réelle (émission,
rotation, révocation) et de récupération/réconciliation comme pratique
IAM distincte de la littératie fondamentale DID/VC de FRK-08. Le fait
vérifiable que `mint_frek_id()` (dans `backend/services/frek_core.py`)
n'a aucun des trois mécanismes de cycle de vie.

**Supposé :** un lien `FRK09.SKILL.*` réel dans le runtime de cette
Academy — inexistant (`NO_RUNTIME_BINDING`). Tout mécanisme de
rotation, révocation, ou récupération pour FREK-ID — jamais accordé
(`CAPABILITY_NOT_IMPLEMENTED`).

## Dépendances

- `FREK_01_75_RECONCILIATION.md`, `docs/frk/frk08/REFERENTIAL.md`
  (prérequis, jamais dupliqué), `backend/services/frek_core.py`
  (source du fait `mint_frek_id()` sans cycle de vie), `70_EVIDENCE/
  EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `FRK09` dans le registre de certification de cette
   Academy, namespace distinct de `FRK08.SKILL.*`.
2. Une surface candidat réelle (ce corpus est markdown seul).
3. Un vrai design de cycle de vie à évaluer par un correcteur humain —
   inexistant aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment
+ rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.

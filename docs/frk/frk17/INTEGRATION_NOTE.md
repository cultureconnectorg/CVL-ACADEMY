# FRK-17 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** le standard RFC 3161 réel (modèle TSA-tierce, structure de
jeton, vérification par signature) comme littératie technique
marché-générale. Le fait vérifiable que `issue_proof()` (`frek_core.py`)
reste un stub UUID sans lien cryptographique temporel.

**Supposé :** `FRK17.SKILL.*` réel dans le runtime de cette Academy —
inexistant (`NO_RUNTIME_BINDING`). Tout ancrage RFC 3161 CVLN — jamais
accordé (`CAPABILITY_NOT_IMPLEMENTED`).

## Dépendances

- `FREK_01_75_RECONCILIATION.md`, `docs/frk/frk13/REFERENTIAL.md`
  (frontière, jamais fusionné), `backend/services/frek_core.py`
  (source du fait `issue_proof()` = stub UUID).

## Ce qu'une future intégration exigerait

1. Une entrée `FRK17` dans le registre de certification de cette
   Academy, namespace distinct de `FRK13.SKILL.*`.
2. Une surface candidat réelle (ce corpus est markdown seul).
3. Un vrai jeton RFC 3161 à évaluer par un correcteur humain —
   inexistant aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment
+ rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.

# FRK-38 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** la pratique réelle de vérification d'intégrité média
post-capture (analyse de cohérence de compression, détection
d'artefacts d'édition) comme troisième maillon d'une chaîne de
confiance à trois moments, distincte de FRK-36 (capture) et FRK-37
(attestation).

**Supposé :** aucune vérification d'intégrité média CVLN complète
observée. `FRK38.SKILL.*` réel dans le runtime de cette Academy —
inexistant (`NO_RUNTIME_BINDING`).

## Dépendances

- `FREK_01_75_RECONCILIATION.md`, `docs/frk/frk36/REFERENTIAL.md`,
  `docs/frk/frk37/REFERENTIAL.md` (référencés, jamais dupliqués),
  `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `FRK38` dans le registre de certification de cette
   Academy, namespace distinct de `FRK36.SKILL.*`/`FRK37.SKILL.*`.
2. Une surface candidat réelle (ce corpus est markdown seul).
3. Un vrai actif média à vérifier par un correcteur humain —
   inexistant aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment
+ rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.

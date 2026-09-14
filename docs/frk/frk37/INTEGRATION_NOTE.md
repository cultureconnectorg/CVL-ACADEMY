# FRK-37 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** la pratique réelle d'attestation de source/dispositif
(racine de confiance matérielle/cryptographique, certificat signé,
chaîne de vérification) comme discipline marché-générale, distincte
de la capture authentique générale (FRK-36) et de l'intégrité
post-capture (FRK-38).

**Supposé :** aucune attestation de source/dispositif CVLN observée.
`FRK37.SKILL.*` réel dans le runtime de cette Academy — inexistant
(`NO_RUNTIME_BINDING`).

## Dépendances

- `FREK_01_75_RECONCILIATION.md`, `docs/frk/frk36/REFERENTIAL.md`
  (contexte, réutilisé par référence), `70_EVIDENCE/
  EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `FRK37` dans le registre de certification de cette
   Academy, namespace distinct de `FRK36.SKILL.*`.
2. Une surface candidat réelle (ce corpus est markdown seul).
3. Un vrai mécanisme d'attestation à évaluer par un correcteur
   humain — inexistant aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment
+ rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.

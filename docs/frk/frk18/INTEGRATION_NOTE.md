# FRK-18 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** le protocole OpenTimestamps réel et externe (ancrage
Bitcoin, arbre de Merkle, vérification indépendante) comme littératie
technique marché-générale. Aucun ancrage OpenTimestamps CVLN observé.

**Supposé :** `FRK18.SKILL.*` réel dans le runtime de cette Academy —
inexistant (`NO_RUNTIME_BINDING`). Tout usage CVLN d'OpenTimestamps —
jamais accordé (`CAPABILITY_NOT_IMPLEMENTED`), malgré la proximité
conceptuelle avec `issue_proof()`.

## Dépendances

- `FREK_01_75_RECONCILIATION.md`, `docs/frk/frk17/REFERENTIAL.md`
  (discipline d'horodatage voisine, jamais fusionnée), `70_EVIDENCE/
  EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `FRK18` dans le registre de certification de cette
   Academy, namespace distinct de `FRK17.SKILL.*`.
2. Une surface candidat réelle (ce corpus est markdown seul).
3. Une vraie preuve `.ots` à évaluer par un correcteur humain —
   inexistant aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment
+ rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.

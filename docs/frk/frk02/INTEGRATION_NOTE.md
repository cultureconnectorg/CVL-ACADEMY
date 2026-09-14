# FRK-02 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** `frek_core.py` re-lu cette session — frontière client
unique, docstring « the sole boundary through which the app talks to
FrekCore ».

**Supposé :** un lien `FRK02.SKILL.*` réel dans le runtime de cette
Academy — inexistant ; une architecture DID/VC/provenance-graphe —
tous deux inexistants (`NO_RUNTIME_BINDING`,
`CAPABILITY_NOT_IMPLEMENTED`).

## Dépendances

`FREK_01_75_RECONCILIATION.md`, `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`,
`docs/frk/frk01/REFERENTIAL.md`, `docs/frk/frk58/REFERENTIAL.md`
(prérequis).

## Ce qu'une future intégration exigerait

1. Une entrée `FRK02` dans le registre de certification de cette
   Academy.
2. Une architecture DID/VC/provenance-graphe réellement construite —
   inexistante aujourd'hui.
3. Un correcteur humain évaluant un vrai diagramme construit — ce
   corpus est markdown seul.

## Status

`STATUS = PACKAGE_COMPLETE` — package complet construit cette passe.
`FULLY_COMPLETE` requiert un passage réel vérifié par un humain.

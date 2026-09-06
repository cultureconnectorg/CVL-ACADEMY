# FRK-01 — Integration Academy Package Note

## Réel vs. supposé

**Réel (vérifié cette session, fichier relu en entier) :**
`backend/services/frek_core.py` — 5 méthodes publiques, 8 signaux
valides, 6 paliers de progression, `issue_proof()` confirmé stub
(UUID aléatoire, aucune garantie cryptographique).

**Supposé :** un lien `FRK01.SKILL.*` réel dans le runtime de cette
Academy — inexistant (`NO_RUNTIME_BINDING`).

## Dépendances

- `docs/cvln_academy_master/20_EXTERNAL/FREK_01_75_RECONCILIATION.md`
  (jamais re-audité ni contredit ici), `70_EVIDENCE/
  EVIDENCE_ARCHITECTURE.md`, `100_ECONOMY/ECONOMIC_MODEL.md` (statut
  économique à trancher séparément — non décidé ici).

## Ce qu'une future intégration exigerait

1. Une entrée `FRK01` dans le registre de certification/compétences
   de cette Academy.
2. Une surface candidat réelle (ce corpus est markdown-only).
3. Une décision séparée sur l'octroi d'accès write réel à
   `frek_core.py` en production — jamais automatique.

## Status

`STATUS = PACKAGE_COMPLETE` — compétences, prérequis, objectifs,
modules, banques N1/N2, assessment, rubric, evidence model, 3 guides,
cette note d'intégration, et les quality gates du corpus existent
tous. `FULLY_COMPLETE` requiert encore un passage réel vérifié par un
humain — non revendiqué ici.

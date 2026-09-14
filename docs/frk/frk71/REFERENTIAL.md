# FRK-71 — FREK v3 Architecture

## Repo truth this formation is built on

Grounded in `cultureconnectorg/frekcoreAout2026`, commit
`fb272f1d491b09a6d068fb3f6c9c75d407bb0626`, `frek_v3/` — un corpus
d'architecture réel, cohérent en interne (déjà audité cette session,
`REPO_REGISTRY.md`, clôture G5/FD) : `FREK_V3_Architecture_
Review_Final.md`, `FREK_Architecture_Integree_v0.2.md`,
`FREK_V3_Engineering_Exploded_View_v0.2.md`,
`FREK_V3_Reconciliation_Architecture_v0.2.md`, `CE_QUI_MANQUE.md`.

Per `FREK_01_75_RECONCILIATION.md` : coverage `PARTIAL — SOURCE_
OBSERVED`, distinctness `DISTINCT_PROFESSION`, action `NEW_EXTERNAL`.
**`NEEDS_FOUNDER_DECISION` = 0 — clos** sur la maturité vérifiée par
dépôt.

## Prerequisites

FRK-01 (contexte recommandé — couche différente, plus mature, du même
produit éventuel).

## Objectives

Un candidat qui complète FRK-71 sait classer précisément la maturité
réelle de l'architecture FREK v3 contre son échelle propre, sans
jamais l'inflater :

- Enseigner l'architecture réelle FREK v3 et sa **propre échelle de
  maturité explicite** — verbatim, jamais adoucie ni inflatée :
  `1. Concept (dépassé) → 2. Architecture (✅ on est ici, verrouillé)
  → 3. Engineering (⏳ prochaine phase, RTL/bits exacts/résultats
  expérimentaux)`.
- Citer précisément le FPGA comme pont nommé explicitement par le
  corpus lui-même entre le Niveau 2 et le Niveau 3 — **pas encore
  franchi** — et expliquer pourquoi cette précision matérielle est
  déterminante : sans franchissement FPGA, aucune preuve matérielle
  n'existe, la classification reste Level 2 tant que ce pont n'est pas
  traversé.
- Maintenir la classification permanente, jamais dérogée :
  `ARCHITECTURE_LEVEL_2` / `SOURCE_OBSERVED`. L'existence réelle au
  niveau architecture n'est jamais inflatée en `NOT_FULL_ENGINEERING`
  (absence de RTL/timings) devenant complet, en `NOT_HARDWARE_PROVEN`
  (absence de prototype FPGA) devenant prouvé, ou en `NOT_PRODUCTION_
  INTEGRATED` (aucun lien à un FREKCORE en production, y compris le
  `frek_core.py` de cette Academy) devenant intégré.
- Ne jamais confondre cette couche avec le `frek_core.py` propre de
  cette Academy (FRK-01/58) — même produit éventuel, couche
  différente, plus mature, toujours pas en production : les confondre
  fausserait la maturité réelle de chacune.
- Expliquer précisément pourquoi valider toute affirmation de niveau 3
  (ingénierie/matériel prouvé) pour FREK v3 serait une erreur
  éliminatoire : il manque le RTL, les timings exacts et des résultats
  expérimentaux — l'architecture est verrouillée conceptuellement, pas
  encore prouvée en ingénierie ni en matériel.

## Modules

1. **Littératie du corpus d'architecture FREK v3** (les 5 documents
   réels nommés).
2. **Littératie de l'échelle de maturité** — modèle verbatim à 3
   niveaux, FPGA comme pont nommé non franchi vers le Niveau 3.
3. **Discipline de frontière vs. `frek_core.py`** (FRK-01/58).

## Assessment

Un exercice de classification de maturité : le candidat reçoit une
affirmation de capacité réelle sur FREK v3 et doit la classer
correctement contre l'échelle propre du corpus — échec éliminatoire
pour toute affirmation d'un statut de Niveau 3
(ingénierie/matériel prouvé).

## Evidence / mission eligibility

`FRK71.SKILL.FREK_V3_ARCHITECTURE.L1` réservé une fois approfondi.
Aucun chemin d'éligibilité mission aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment +
rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.

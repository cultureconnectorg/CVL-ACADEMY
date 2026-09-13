# FRK-74 — FREK DSP Fingerprint

## Repo truth this formation is built on

Grounded in `frek_v3/docs/FREK_DSP_Fingerprint_Specification_v0.1.md`
— déjà audité cette session, `REPO_REGISTRY.md`. Per le
`CE_QUI_MANQUE.md` du corpus lui-même : cette spec est explicitement
la **moins résolue** du cluster v3 — nombre de bandes, taille de
fenêtre FFT, hop size, et l'algorithme d'empreinte lui-même sont
nommés comme **décisions produit encore ouvertes**, non verrouillées.

Per `FREK_01_75_RECONCILIATION.md` : coverage `PARTIAL — SOURCE_
OBSERVED, explicitement inachevée`, distinctness `DISTINCT_
SPECIALIZATION`, action `NEW_EXTERNAL`.

## Prerequisites

FRK-71.

## Objectives

Un candidat qui complète FRK-74 sait lire et raisonner sur une
spécification technique DSP explicitement en cours, sans jamais la
présenter comme finalisée :

- Enseigner la spécification réelle DSP Fingerprint **comme une
  architecture en cours**, jamais comme une spécification terminée —
  les décisions ouvertes (fenêtre FFT, hop size, nombre de bandes,
  algorithme) constituent le point pédagogique central, pas un défaut
  à masquer.
- Expliquer précisément pourquoi le document `CE_QUI_MANQUE.md` du
  corpus lui-même qualifie cette spécification de « la moins
  résolue » du cluster : l'honnêteté de cette auto-évaluation est la
  source de vérité pédagogique, pas une faiblesse à corriger.
- Citer précisément les décisions produit explicitement encore
  ouvertes : taille de fenêtre FFT, hop size, nombre de bandes,
  algorithme d'empreinte lui-même — et expliquer pourquoi les
  enseigner comme « ouvertes » forme une compétence réelle
  d'ingénierie : distinguer une architecture verrouillée d'une
  architecture encore en cours de décision.
- Frontière explicite vis-à-vis du concept plus large « empreinte
  culturelle » de FRK-29/30 : « DSP » signifie ici traitement
  numérique du signal (empreinte audio spécifiquement) — un domaine
  technique différent, plus étroit, conservé distinct et
  cross-référencé, malgré le mot « empreinte » partagé.
- Expliquer précisément pourquoi présenter cette spécification comme
  « finalisée » dans une copie serait une erreur éliminatoire : cela
  masquerait le statut réel du travail en cours, contredisant la
  discipline même du corpus qui déclare cette spec inachevée.

## Modules

1. **Littératie de spécification DSP fingerprint** (ce qui est
   verrouillé à ce jour).
2. **Littératie des décisions ouvertes** — fenêtre FFT, hop size,
   nombre de bandes, algorithme — explicitement non résolues.
3. **Discipline de frontière vs. FRK-29/30** — domaine technique
   distinct malgré la terminologie partagée.

## Assessment

Un exercice de statut de spécification : le candidat doit identifier
correctement quelles parties de la spécification sont verrouillées et
lesquelles restent ouvertes — échec éliminatoire pour toute
présentation de la spécification comme terminée.

## Evidence / mission eligibility

Aucun chemin d'éligibilité mission aujourd'hui.
`FRK74.SKILL.DSP_FINGERPRINT.L1` réservé une fois approfondi (voir
`EVIDENCE_MODEL.md`).

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment +
rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.

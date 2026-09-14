# FRK-15 — Technical Evidence Reports & Verification

## Grounding

Per `FREK_01_75_RECONCILIATION.md` : coverage `NONE`, distinctness
`DISTINCT_SPECIALIZATION (of FRK-12/14)`, action `NEW_EXTERNAL`,
séquencée après FRK-12/14.

## Prerequisites

FRK-12, FRK-14 (maîtrise réelle, pas seulement lecture).

## Objectives

Un candidat qui complète FRK-15 sait rédiger et vérifier un rapport de
preuve technique réel, en s'appuyant structurellement sur FRK-12 et
FRK-14 sans jamais les recopier :

- Enseigner la rédaction et la vérification réelles de rapports de
  preuve technique, en s'appuyant sur la discipline d'ingénierie de
  FRK-12 et les principes de chaîne de custody de FRK-14.
- Réutiliser les deux par référence — jamais en les re-rédigeant :
  chaque brique amont reste la source unique de vérité pour son sujet,
  éviter toute duplication ou risque de divergence.
- Distinguer précisément « vérifier un rapport » (comparer contre un
  standard externe déjà défini) et « produire un rapport » (construire
  ce standard) — deux disciplines distinctes malgré leur proximité,
  toutes deux couvertes séparément par cette formation.
- Expliquer précisément pourquoi omettre la section chaîne de custody
  d'un rapport de preuve technique n'est jamais un choix de périmètre
  acceptable : un rapport sans cette section est incomplet par
  construction (FRK-14), c'est un vide de méthode, pas une
  simplification.
- Expliquer pourquoi cette formation ne peut être validée sans une
  maîtrise réelle de FRK-12 ET FRK-14 (prérequis structurels, pas de
  simples suggestions) : sans ces deux fondations, la
  « vérification » enseignée ici resterait une coquille vide, sans
  méthode réelle à appliquer.
- Traiter explicitement la frontière avec FRK-13 lorsqu'un artefact
  cité s'appuie sur `frek_core.py`/`issue_proof()` : ce stub ne peut
  jamais être présenté comme une preuve techniquement vérifiée dans un
  rapport produit ou vérifié sous FRK-15.

## Modules

1. **Structure & standards de rapport technique** — ce qui rend un
   rapport de preuve complet et vérifiable.
2. **Méthodologie de vérification** — comparer une conclusion contre
   un standard externe documenté, jamais l'accepter sans méthode.
3. **Intégration des compétences FRK-12/14** (par référence) —
   discipline de citation stricte, jamais de fusion ou de re-rédaction.

## Assessment

Un exercice de rédaction de rapport de preuve technique complet
(méthodologie, chaîne de custody, conclusion appuyée), citant FRK-12
et FRK-14 par référence — noté contre la pratique réelle de preuve
technique, avec règle éliminatoire sur toute conclusion sans
méthodologie documentée ou toute omission de la chaîne de custody sans
justification.

## Evidence / mission eligibility

Prérequis structurel : les preuves de FRK-12 et FRK-14 (une fois
celle-ci levée de `NEEDS_EXPERT_REVIEW`) doivent être référencées,
jamais recopiées. `FRK15.SKILL.TECH_EVIDENCE_REPORT.L1` réservé une
fois approfondi.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment +
rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.

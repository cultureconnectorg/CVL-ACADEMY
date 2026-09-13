# AF-04→15 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives — en particulier la liste des 12
disciplines et le contre-exemple systématique `agent_factory.py`.

## Ce que tu vérifies en priorité

1. Le candidat affirme-t-il, même au conditionnel ou comme intention
   future, qu'un système CVLN implémente l'une des 12 disciplines ?
   Éliminatoire si oui.
2. La conception marché-générale proposée est-elle réaliste et ne
   présuppose-t-elle aucune infrastructure CVLN inexistante ?
3. Le candidat distingue-t-il correctement des disciplines proches
   (sécurité vs. sûreté, usage d'outils vs. orchestration) ?
4. Si un système externe (ex. `CVLNAgentfactory`) est cité, est-il
   clairement qualifié de séparé et non câblé à cette Academy ?

## Ce que tu ne fais pas

Tu ne notes jamais sur une conception qui serait "presque" correcte
architecturalement si elle affirme malgré tout une capacité CVLN
inexistante — la règle éliminatoire prime toujours sur la qualité de
conception.

## Score

Utilise la grille 0–4 et le tableau de compétences de
`ASSESSMENT_AND_RUBRIC.md`. Le seuil de passage est ≥2.5/4.

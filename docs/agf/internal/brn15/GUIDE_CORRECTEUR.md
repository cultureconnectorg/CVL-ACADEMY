# BRN-15 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier la
trace exacte de l'événement et la double frontière (touchpoint unique
réel vs. `/brain/ask` externe jamais câblé).

## Ce que tu vérifies en priorité

1. La trace de l'événement est-elle exacte et complète :
   `certification/service.py:140` → `events.py` → `subscribers.py` →
   `/academy/certification-passed` ? Toute étape inventée
   (analyse, enrichissement contextuel) est éliminatoire.
2. Le candidat affirme-t-il, même implicitement, qu'un moteur de
   raisonnement/contexte/mémoire existe ? Éliminatoire si oui.
3. Le candidat affirme-t-il un câblage entre cet événement et
   `/brain/ask` de `MetaCVLN` ? Éliminatoire si oui.
4. Si le candidat propose une architecture d'intégration hypothétique
   (Cas 3 de `BANQUE_N2.md`), la qualifie-t-il explicitement comme
   telle, sans la confondre avec l'état actuel du système ?

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle de ce qu'un "Brain"
devrait faire architecturalement — seulement sur l'exactitude de la
trace réelle et le respect strict de la double frontière. Tu n'assouplis
jamais la règle éliminatoire pour une formulation habile qui reste
ambiguë sur le câblage.

## Score

Utilise la grille 0–4 et le tableau de compétences de
`ASSESSMENT_AND_RUBRIC.md`. Le seuil de passage est ≥2.5/4.

# FRK-42 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier la
frontière FRK-20/FRK-42 et les défis d'intégrité/ordre.

## Ce que tu vérifies en priorité

1. L'artefact conçu reste-t-il vérifiable après transit hors réseau
   (signature embarquée ou détachée) ?
2. Le candidat traite-t-il l'intégrité en transit ET l'ordre/gap pour
   les séquences multi-artefacts, pas seulement l'un des deux ?
3. Affirme-t-il, explicitement ou implicitement, qu'un système CVLN
   implémente ce transport ? Applique la règle éliminatoire sans
   exception si oui.

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle du transport de
données — seulement sur l'auto-vérifiabilité réelle de l'artefact
conçu et sur l'absence de système CVLN inventé.

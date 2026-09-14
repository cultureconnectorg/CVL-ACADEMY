# FRK-17 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier la
structure du jeton RFC 3161 et la frontière FRK-13.

## Ce que tu vérifies en priorité

1. Le candidat vérifie-t-il réellement la signature de l'autorité, ou
   se contente-t-il de lire les champs du jeton ?
2. Distingue-t-il correctement « vérifier un ancrage » et « faire
   confiance à une date affichée » ?
3. Affirme-t-il, explicitement ou implicitement, que `issue_proof()`
   équivaut à un horodatage de confiance ? Applique la règle
   éliminatoire sans exception si oui.

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle des horodatages —
seulement sur la vérification réelle de signature et sur l'exactitude
de la frontière FRK-13 articulée.

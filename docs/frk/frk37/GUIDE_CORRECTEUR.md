# FRK-37 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier la
racine de confiance attendue et la frontière avec FRK-38.

## Ce que tu vérifies en priorité

1. Le mécanisme d'attestation proposé a-t-il une racine de confiance
   réelle (matérielle ou cryptographique) ?
2. Le candidat identifie-t-il correctement les limites du mécanisme
   (ne prouve pas l'intégrité post-capture) ?
3. Affirme-t-il, explicitement ou implicitement, qu'une attestation de
   source suffit à garantir l'intégrité complète du média ? Applique
   la règle éliminatoire sans exception si oui.

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle de l'attestation
matérielle — seulement sur la présence réelle d'une racine de
confiance et sur l'exactitude des limites articulées.

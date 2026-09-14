# FRK-53 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier la
frontière FRK-52/FRK-53 et les principes de DX/retry attendus.

## Ce que tu vérifies en priorité

1. Le design SDK proposé inclut-il des modèles typés et des erreurs
   traduites en exceptions actionnables ?
2. La politique de retry distingue-t-elle correctement erreurs
   sûres/non sûres à retenter (idempotence) ?
3. Affirme-t-il, explicitement ou implicitement, l'existence d'un SDK
   FREK public ? Applique la règle éliminatoire sans exception si oui.
4. Redéfinit-il FRK-52 au lieu d'y référer ? Signale-le, applique la
   règle éliminatoire si c'est franc et systématique.

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle du design de SDK —
seulement sur la pratique réelle (DX, retry/idempotence) et sur
l'absence de SDK FREK inventé.

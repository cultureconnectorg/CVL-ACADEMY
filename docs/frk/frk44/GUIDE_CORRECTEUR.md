# FRK-44 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier les
stratégies de réconciliation attendues et la frontière FRK-43.

## Ce que tu vérifies en priorité

1. Le mécanisme proposé détecte-t-il réellement une divergence d'état,
   pas seulement une absence de livraison ?
2. Le compromis de la stratégie choisie est-il explicitement identifié ?
3. FRK-43 est-il cité par référence, ou redéfini ? Signale-le, applique
   la règle éliminatoire si c'est franc et systématique.

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle de la synchronisation
— seulement sur la solidité réelle du mécanisme de détection et sur
l'exactitude du compromis identifié.

# FRK-18 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier le
modèle de confiance Bitcoin et la mécanique de l'arbre de Merkle.

## Ce que tu vérifies en priorité

1. Le candidat vérifie-t-il réellement le chemin Merkle jusqu'à la
   transaction Bitcoin, ou saute-t-il cette étape ?
2. Distingue-t-il correctement le modèle de confiance OpenTimestamps
   (Bitcoin public) de celui de RFC 3161 (autorité tierce) ?
3. Affirme-t-il, explicitement ou implicitement, qu'un système CVLN
   utilise OpenTimestamps ? Applique la règle éliminatoire sans
   exception si oui.

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle de Bitcoin — seulement
sur la vérification réelle du chemin Merkle et sur l'absence d'usage
CVLN affirmé.

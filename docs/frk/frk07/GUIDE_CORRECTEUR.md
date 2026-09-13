# FRK-07 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier le
rôle IdP, le modèle OAuth2/OIDC, et la frontière FRK-06/FRK-07 précise.

## Ce que tu vérifies en priorité

1. Le candidat restitue-t-il correctement le rôle IdP et la
   distinction authentification/autorisation ?
2. Le design IAM proposé applique-t-il des patterns réels
   (OAuth2/OIDC, cycle de vie des credentials) sans les attribuer à
   `frek_core.py` ?
3. Affirme-t-il, explicitement ou implicitement, que `mint_frek_id()`
   est un IdP complet ? Applique la règle éliminatoire sans exception
   si oui.

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle de l'IAM — seulement
sur les standards réels (OAuth2/OIDC, cycle de vie des credentials) et
sur l'exactitude de la frontière FRK-06 articulée.

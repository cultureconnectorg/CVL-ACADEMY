# FRK-07 — Banque N1

## IAM fondamentaux (M1)

1. FRK-07 enseigne-t-il une architecture IAM CVLN réelle ? (Non —
   discipline marché-générale uniquement, jamais une description de
   `frek_core.py`)
2. Que fait un IdP dans une architecture d'authentification ? (Il
   authentifie un sujet, émet des tokens/assertions, et entretient une
   relation de confiance avec les relying parties)
3. Quelle est la différence entre authentification et autorisation ?
   (Authentification = prouver qui on est ; autorisation = déterminer
   ce qu'on a le droit de faire, une fois identifié)

## OAuth2/OIDC (M2)

4. Cite les quatre rôles OAuth2. (Resource owner, client, authorization
   server, resource server)
5. Que décrit le flow "authorization code" ? (Le client redirige
   l'utilisateur vers l'authorization server, reçoit un code
   d'autorisation, puis l'échange contre un token via un canal
   back-channel)
6. Qu'ajoute OIDC par-dessus OAuth2 ? (Une couche d'identité : ID
   token, endpoint UserInfo, document de découverte)
7. `frek_core.py` implémente-t-il OAuth2/OIDC ? (Non — aucune trace ;
   OAuth2/OIDC sont enseignés comme standards externes réels)

## Cycle de vie des credentials (M3)

8. Cite les quatre étapes du cycle de vie d'une credential. (Émission,
   rotation, révocation, expiration)
9. Un système sans rotation ni révocation peut-il être appelé un
   système de gestion de credentials ? (Non — c'est au mieux un
   générateur d'identifiants)

## Frontière FRK-06/FRK-07 (M4)

10. Quelle est la frontière avec FRK-06 ? (FRK-06 = minting séquentiel
    étroit d'un identifiant ; FRK-07 = architecture IAM complète,
    marché-générale)
11. Un candidat peut-il affirmer que `mint_frek_id()` est un IdP
    complet ? (Non — élimination automatique si affirmé)

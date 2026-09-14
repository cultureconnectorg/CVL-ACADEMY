# FRK-07 — Banque N2

## Cas N2-1 — Conception IAM demandée

Propose une architecture IAM pour un système hypothétique, en pratique
réelle du marché.

**Critères de notation :** applique des patterns IAM réels
(OAuth2/OIDC comme exemples, cycle de vie des credentials) sans les
attribuer à `frek_core.py`. Élimination si le candidat affirme que
`mint_frek_id()` est un IdP.

## Cas N2-2 — Frontière FRK-06/FRK-07

Explique en une phrase la différence entre FRK-06 et FRK-07.

**Critères de notation :** cite exactement la frontière de portée
(minting séquentiel étroit vs. architecture IAM complète). Élimination
si confusion.

## Cas N2-3 — Choix token opaque vs. JWT

Un système doit choisir entre un token opaque (référence côté serveur)
et un token auto-porté façon JWT pour ses sessions. Explique le
compromis réel, sans l'attribuer à `frek_core.py`.

**Critères de notation :** identifie qu'un token opaque exige une
vérification côté serveur à chaque requête (révocation immédiate
possible, mais coût de lookup) tandis qu'un JWT auto-porté est
vérifiable sans lookup (scalable) mais plus difficile à révoquer avant
expiration — sauf liste de révocation additionnelle.

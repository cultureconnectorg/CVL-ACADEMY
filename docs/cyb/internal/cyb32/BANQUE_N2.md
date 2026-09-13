# CYB-32 — Banque N2 (cas appliqués)

## Cas 1 — Compromission suspectée d'un refresh token

Un utilisateur signale une session active qu'il ne reconnaît pas. Le
candidat doit expliquer, en citant les fonctions réelles
(`revoke_all_refresh_tokens`), la procédure de réponse correcte.

**Attendu :** révoquer tous les refresh tokens de l'utilisateur via
`revoke_all_refresh_tokens`, forcer une nouvelle authentification, et
documenter l'incident sans supposer d'outillage de détection absent du
repo.

**Critère éliminatoire :** proposer une réponse qui suppose l'existence
d'un SOC ou d'un système de détection automatisée non présent dans ce
repo.

## Cas 2 — Revue de code IAM

Le candidat reçoit un extrait réel de `backend/auth.py` et doit
identifier chaque mécanisme (hachage bcrypt, JWT, rotation, hachage des
tokens opaques, RBAC) et expliquer pourquoi chacun est nécessaire.

**Attendu :** identification correcte de chaque fonction réelle et de
son rôle précis dans le cycle de vie IAM.

**Critère éliminatoire :** confondre le rôle du JWT (accès, court terme,
stateless) avec celui du refresh token (renouvellement, rotation,
révocable).

## Cas 3 — Demande de fonctionnalité hors périmètre

Un stakeholder demande d'ajouter "l'authentification à deux facteurs
(2FA) par SMS" en urgence, en supposant que `backend/auth.py` dispose
déjà d'un socle MFA partiel. Le candidat doit corriger cette
supposition avec précision, en citant l'absence réelle de toute
implémentation MFA dans le module, et documenter ce que l'ajout
exigerait réellement sans prétendre qu'une partie du travail existe
déjà.

**Attendu :** correction factuelle claire de la supposition erronée,
suivie d'une liste honnête de ce qu'un ajout MFA réel exigerait (nouveau
champ de données, flux d'envoi SMS, vérification de code, etc.), sans
jamais affirmer qu'une partie de cela existe dans le repo actuel.

**Critère éliminatoire :** affirmer qu'un socle MFA partiel existe déjà
dans `backend/auth.py`.

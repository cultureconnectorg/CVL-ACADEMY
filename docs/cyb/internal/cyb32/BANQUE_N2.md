# CYB-32 — Banque N2 (cas appliqués)

## Cas 1 — Compromission suspectée d'un refresh token

Un utilisateur signale une session active qu'il ne reconnaît pas. Le
candidat doit expliquer, en citant les fonctions réelles
(`revoke_all_refresh_tokens`), la procédure de réponse correcte.

**Critère éliminatoire :** proposer une réponse qui suppose l'existence
d'un SOC ou d'un système de détection automatisée non présent dans ce
repo.

## Cas 2 — Revue de code IAM

Le candidat reçoit un extrait réel de `backend/auth.py` et doit
identifier chaque mécanisme (hachage bcrypt, JWT, rotation, hachage des
tokens opaques, RBAC) et expliquer pourquoi chacun est nécessaire.

**Critère éliminatoire :** confondre le rôle du JWT (accès, court terme,
stateless) avec celui du refresh token (renouvellement, rotation,
révocable).

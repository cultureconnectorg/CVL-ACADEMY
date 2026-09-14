# GMD-33 — Guide Candidat

## Avant de commencer

GMD-21 requis — toutes les autres formations du cluster reposent sur
cette frontière d'authentification.

## Ce que tu dois savoir faire

Tracer le cycle d'auth réel, auditer la frontière public/admin route
par route, et reconnaître un incident de sécurité **sans jamais
inventer** un mécanisme de réponse (aucune révocation de token
n'existe dans ce code).

## Comment réviser

1. Lis `server.py` lignes 36-70 et 261-278 toi-même.
2. Fais les 10 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`, en particulier N2-1.

## Piège le plus fréquent

Croire que `POST /auth/logout` invalide le token partout — il efface
seulement le cookie local, jamais le token lui-même.

## Règle absolue

N'invente jamais une route de révocation de token, un mécanisme de
dérogation de rôle, ou un partage de session avec cette Academy —
élimination automatique.

# CYB-32 — Guide Candidat

## Avant de commencer

Aucun prérequis. Apprends le cycle de vie IAM réel de `backend/
auth.py` : hachage bcrypt, JWT, rotation de refresh token, hachage des
tokens opaques, RBAC.

## Ce que tu dois savoir faire

Expliquer précisément chaque mécanisme réel (hachage bcrypt, émission/
vérification JWT, rotation et révocation de refresh token, hachage des
tokens de reset/vérification, `require_role`) et distinguer clairement
le rôle du JWT d'accès de celui du refresh token. Répondre à un
scénario d'incident en citant uniquement les fonctions réelles
disponibles.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 6 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Pièges les plus fréquents

1. Affirmer que ce module est un SSO, un MFA, ou un coffre de secrets
   — élimination automatique, même en passant.
2. Confondre le rôle du JWT d'accès avec celui du refresh token.
3. Supposer qu'un SOC ou un système de détection automatisée existe —
   élimination automatique.
4. Concéder qu'un socle MFA partiel existe déjà quand un stakeholder
   le suppose à tort.

## Règle absolue

Ce module n'est ni un SSO, ni un MFA, ni un coffre de secrets, ni un
SOC. C'est un module d'authentification à service unique, réel et en
production, avec rotation de token — rien de plus.

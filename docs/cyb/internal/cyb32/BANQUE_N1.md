# CYB-32 — Banque N1 (formatif)

Réserve `CYB32.SKILL.IAM_OPERATOR.L1`.

1. Pourquoi `backend/auth.py` hache les mots de passe avec bcrypt
   plutôt que de les stocker en clair ou avec un hash simple (SHA-256
   seul) ?
2. Que signifie « rotation » pour un refresh token, et pourquoi
   empêche-t-elle le rejeu d'un token volé ?
3. Pourquoi `_hash_opaque_token` hache-t-il aussi les tokens de
   réinitialisation de mot de passe et de vérification d'email, alors
   qu'ils ne sont utilisés qu'une seule fois ?
4. Pourquoi serait-il une erreur éliminatoire d'affirmer que ce module
   est une plateforme IAM d'entreprise (SSO, MFA, coffre de secrets) ?
5. Quelle est la différence de rôle entre le JWT d'accès
   (`make_token`/`decode_token`) et le refresh token, et pourquoi
   cette distinction importe-t-elle en cas de compromission ?
6. Que fait exactement `require_role(*roles)`, et en quoi illustre-t-il
   un patron d'injection de dépendance à moindre privilège dans
   FastAPI ?

## Corrigé indicatif

1. Bcrypt inclut un sel et un facteur de coût réglable, résistant aux
   attaques par table arc-en-ciel et par force brute — un hash simple
   ne protège pas contre ces deux menaces.
2. Chaque utilisation d'un refresh token émet un nouveau token et
   invalide l'ancien (`rotate_refresh_token`) — si un attaquant rejoue
   un ancien token, le système peut détecter l'incohérence et révoquer
   la session.
3. Un token en clair dans la base de données serait exploitable en cas
   de fuite de la base, même si le token n'a qu'une fenêtre de vie
   courte — le hachage protège même les tokens à usage unique.
4. Le module réel n'implémente ni fédération SSO/SAML/OIDC, ni MFA/2FA,
   ni coffre de secrets — l'affirmer inventerait une capacité
   inexistante dans `backend/auth.py`.
5. Le JWT d'accès est de courte durée et stateless (vérifié sans appel
   base de données) ; le refresh token est révocable et sert à obtenir
   de nouveaux JWT — en cas de compromission, révoquer les refresh
   tokens (`revoke_all_refresh_tokens`) coupe l'accès futur, tandis que
   les JWT déjà émis restent valides jusqu'à expiration naturelle.
6. `require_role` vérifie que l'utilisateur courant possède l'un des
   rôles autorisés avant d'exécuter la route — un candidat ne reçoit
   que l'accès strictement nécessaire à son rôle, illustrant le
   principe de moindre privilège appliqué via l'injection de
   dépendance FastAPI plutôt qu'une vérification manuelle dispersée
   dans chaque route.

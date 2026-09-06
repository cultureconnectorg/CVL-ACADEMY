# CYB-32 — Banque N1 (formatif)

Réserve `CYB32.SKILL.*`.

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

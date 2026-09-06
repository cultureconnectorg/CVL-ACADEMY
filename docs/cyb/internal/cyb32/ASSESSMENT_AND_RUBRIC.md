# CYB-32 — Assessment & Rubric

## Grille (0–4)

| Niveau | Critère |
|---|---|
| 0 | Affirme que le module est une plateforme IAM d'entreprise (SSO/MFA/coffre de secrets), ou confond JWT et refresh token. |
| 1 | Évite ces erreurs, explication incomplète du cycle de vie des tokens. |
| 2 | Explique correctement un mécanisme (hachage, rotation, ou RBAC) sans vue d'ensemble. |
| 3 | Explique correctement l'ensemble du cycle de vie IAM réel. |
| 4 | Niveau 3 + réponse correcte et bornée au Cas 1 (compromission). |

**Règle éliminatoire :** affirmer une capacité IAM inexistante dans
`backend/auth.py` (SSO, MFA, coffre de secrets, SOC).

**Seuil de passage :** ≥2.5/4.

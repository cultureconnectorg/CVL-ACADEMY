# CYB-32 — Assessment & Rubric

## Grille (0–4)

| Niveau | Critère |
|---|---|
| 0 | Affirme que le module est une plateforme IAM d'entreprise (SSO/MFA/coffre de secrets), ou confond JWT et refresh token. |
| 1 | Évite ces erreurs, explication incomplète du cycle de vie des tokens. |
| 2 | Explique correctement un mécanisme (hachage, rotation, ou RBAC) sans vue d'ensemble. |
| 3 | Explique correctement l'ensemble du cycle de vie IAM réel. |
| 4 | Niveau 3 + réponse correcte et bornée au Cas 1 (compromission) + corrige correctement une supposition erronée de capacité (Cas 3). |

**Règle éliminatoire :** affirmer une capacité IAM inexistante dans
`backend/auth.py` (SSO, MFA, coffre de secrets, SOC).

**Seuil de passage :** ≥2.5/4.

## Compétences évaluées

| Compétence | Ce qu'elle vérifie | Niveau minimal exigé |
|---|---|---|
| Littératie du cycle de vie IAM | Explique hachage, JWT, rotation, RBAC correctement | 3 |
| Distinction JWT/refresh token | Ne confond jamais les deux rôles | 2 (éliminatoire sinon) |
| Discipline de frontière de maturité | N'affirme jamais SSO/MFA/coffre de secrets/SOC | 2 (éliminatoire sinon) |
| Réponse à incident bornée au réel | Propose une réponse citant uniquement les fonctions réelles | 4 |
| Correction de supposition erronée | Corrige une fausse prémisse sans concéder de capacité inexistante | 4 |

## Note de correction

Une explication technique excellente du cycle de vie IAM qui, dans un
paragraphe annexe, affirme malgré tout l'existence d'un SSO ou d'un
coffre de secrets reste à 0 — la règle éliminatoire s'applique à toute
affirmation, même isolée dans une réponse par ailleurs solide.

# CYB-32 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier la
frontière de maturité (module d'auth à service unique, jamais une
plateforme IAM d'entreprise).

## Ce que tu vérifies en priorité

1. Le candidat confond-il JWT et refresh token ? Éliminatoire si oui.
2. Le candidat affirme-t-il, même en passant, une capacité SSO/MFA/
   coffre de secrets/SOC ? Éliminatoire si oui.
3. La réponse au scénario d'incident (Cas 1) cite-t-elle uniquement
   les fonctions réelles disponibles ?
4. Le candidat corrige-t-il correctement une supposition erronée de
   capacité (Cas 3), sans concéder qu'elle existe partiellement ?

## Ce que tu ne fais pas

Tu ne notes jamais sur une explication technique par ailleurs
excellente qui affirme malgré tout, même dans un paragraphe annexe,
une capacité IAM d'entreprise — la règle éliminatoire s'applique
partout dans la réponse.

## Score

Utilise la grille 0–4 et le tableau de compétences de
`ASSESSMENT_AND_RUBRIC.md`. Le seuil de passage est ≥2.5/4.

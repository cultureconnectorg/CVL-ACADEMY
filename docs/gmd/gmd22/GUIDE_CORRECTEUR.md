# GMD-22 — Guide Correcteur

## Avant de noter

Ouvre `server.py` (lignes 80-98 et 219-305) à côté de la copie. Chaque
affirmation du candidat doit être vérifiable contre ce code, pas
contre ton souvenir du produit.

## Ce que tu vérifies en priorité

1. **Le candidat distingue-t-il `GET /catalogue` (public, cap 200) de
   `GET /admin/catalogue` (admin, cap 500) ?** C'est le piège le plus
   fréquent — une confusion ici dégrade la note même si le reste est
   correct.
2. **Le candidat a-t-il inventé un mécanisme ?** (batch reorder, merge
   de doublons, flag "featured", distinction save/publish) — si oui,
   applique la règle éliminatoire de `ASSESSMENT_AND_RUBRIC.md` sans
   exception, même si la copie est par ailleurs excellente.
3. **Le M2 runbook est-il vérifié**, pas seulement décrit ? Une copie
   qui affirme "j'ai créé le volume" sans preuve (capture/log/
   raisonnement code complet) reste au niveau 1-2, jamais 3-4.

## Ce que tu ne fais pas

Tu ne notes pas sur la base d'un jugement produit ("c'est ce que ferait
un vrai CMS") — seulement sur la base du code réel cité ci-dessus.

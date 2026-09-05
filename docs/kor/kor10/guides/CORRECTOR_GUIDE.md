# KOR-10 — Guide du Correcteur

## Posture

Vous corrigez une capacité à raisonner en économie du streaming avec
rigueur, pas une performance financière réelle du fil rouge KORA.

## Points de vigilance par module

- **M04 (ARPU/LTV)** : rejeter tout calcul sans hypothèses explicites,
  même si le résultat final "semble" correct. Critère 4 éliminatoire.
- **M05 (partage de valeur)** : vérifier explicitement que la
  contribution de Man Rosa (témoignage, non technique) est incluse et
  valorisée à sa juste place. Ne jamais accepter une exclusion motivée
  par "ce n'est pas un travail technique". Critère 5 éliminatoire.
- **M08 (Wallet/JCC)** : vérifier que le candidat cite fidèlement les
  fichiers réels (`wallet/models.py`, `wallet/service.py`,
  `wallet/passes.py`) et n'invente pas de fonctionnalité Wallet
  inexistante.
- **M09 (CVE)** : rejeter toute définition inventée de CVE, même
  plausible. Seule réponse acceptée : statut `NOT_AUDITED`. Critère 9
  éliminatoire.
- **M06 (royalties)** : vérifier la cohérence avec les incertitudes
  posées en `KOR-07` (jamais un chiffre présenté comme certain là où
  `KOR-07` documente une incertitude ouverte).

## Utilisation de la grille

Voir `assessments/RUBRIC.md`. Seuil global : moyenne ≥ 2,5 **et**
critères 4, 5, 9 conformes. Un dossier qui échoue sur un seul critère
éliminatoire est refusé même si la moyenne dépasse le seuil.

## Erreurs de correction à éviter

- Valider un chiffre "rond" et convaincant sans vérifier ses
  hypothèses.
- Confondre l'aisance de présentation avec la rigueur du raisonnement.
- Laisser passer une définition de CVE parce qu'elle est "raisonnable".

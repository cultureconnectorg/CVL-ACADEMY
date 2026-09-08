# WAL-22 — Banque N2 (cas appliqués)

## Cas N2-1 — Un utilisateur demande d'ouvrir un coffre "gratuit"

**Situation** : un utilisateur du produit externe `djsayd/CVLN-Wallet`
demande si créer un coffre lui donne des fonds supplémentaires "en plus"
de son solde existant.

**Décision attendue** : non — `amount_cc` démarre à 0 ; tout montant
déplacé vers le coffre est dépensé depuis le solde disponible via
`atomic_spend`, jamais créé ex nihilo. Un coffre est une réallocation,
pas un bonus.

**Critères de notation** : cite `atomic_spend` et le démarrage à 0
(50%, éliminatoire si absent), explique la réallocation vs création de
valeur (30%), ne prétend jamais avoir un accès opérationnel réel au
produit externe (20%).

## Cas N2-2 — Fermeture d'un coffre non vide

**Situation** : un manager s'inquiète qu'un utilisateur perde l'argent
restant dans un coffre s'il le ferme par erreur.

**Décision attendue** : rassurer — `DELETE /coffres/{id}` rembourse
automatiquement le solde restant à l'utilisateur avant la suppression ;
fermer un coffre non vide ne détruit jamais de valeur.

**Critères de notation** : cite le remboursement automatique avant
suppression (50%, éliminatoire si absent), explique que ceci est
enregistré via `ledger_post` comme toute autre mouvement (30%), ne
propose jamais une action Academy réelle sur le vrai produit (20%).

---

**Couverture** : 2 cas, couvrant M1 (cycle de vie) et M2 (discipline de
ledger).

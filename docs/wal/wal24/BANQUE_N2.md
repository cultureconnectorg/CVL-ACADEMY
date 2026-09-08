# WAL-24 — Banque N2 (cas appliqués)

## Cas N2-1 — Un utilisateur signale une "erreur 501"

**Situation** : un utilisateur rapporte avoir lu dans la documentation
interne que l'ajout au portefeuille renvoie "une erreur 501" et
s'inquiète que la fonctionnalité soit cassée.

**Décision attendue** : corriger l'information — la route réelle
renvoie un HTTP 200 avec `{"status": "unsigned", ...}`, jamais une
erreur 501 ; ce n'est pas une panne, c'est le comportement voulu tant
qu'aucune carte signée n'existe.

**Critères de notation** : cite le comportement HTTP réel vérifié (200,
pas 501) (50%, éliminatoire si absent), explique que ce n'est pas un
bug mais un état honnête (30%), ne blâme pas le commentaire du code
sans le corriger publiquement (20%).

## Cas N2-2 — Demande de "juste activer la signature"

**Situation** : un product manager demande "juste d'activer la
signature" pour que les cartes Apple/Google soient réellement
installables.

**Décision attendue** : expliquer précisément ce qui manque pour
chaque plateforme (certificat WWDR + Pass Type ID réel pour Apple,
compte Google Wallet Issuer pour signer le JWT) — ce n'est pas un
interrupteur à activer dans le code, ce sont des dépendances externes
réelles à obtenir d'abord.

**Critères de notation** : nomme précisément les deux dépendances
manquantes (50%, éliminatoire si absent), refuse de présenter la
signature comme un simple changement de code (30%), propose les
étapes réelles pour obtenir ces dépendances si demandé (20%).

---

**Couverture** : 2 cas, couvrant M2 (comportement HTTP réel) et M3
(littéracie de l'écart de signature).

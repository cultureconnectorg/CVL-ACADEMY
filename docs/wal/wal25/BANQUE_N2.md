# WAL-25 — Banque N2 (cas appliqués)

## Cas N2-1 — Double-clic sur "Acheter"

**Situation** : un utilisateur signale avoir cliqué deux fois sur
"Acheter" pour le même article par accident, et s'inquiète d'avoir été
débité deux fois.

**Décision attendue** : rassurer — tant que les deux clics envoient la
même clé d'idempotence, `idem_begin`/`idem_finish` garantit qu'un seul
débit réel a lieu ; le second appel renvoie le résultat du premier sans
débiter à nouveau.

**Critères de notation** : cite `idem_begin`/`idem_finish` comme
garantie réelle (50%, éliminatoire si absent), explique la condition
(même clé d'idempotence) (30%), ne prétend jamais un accès
opérationnel réel Academy (20%).

## Cas N2-2 — Demande d'ajouter un article au catalogue

**Situation** : un partenaire demande d'ajouter son propre produit au
catalogue marketplace via cette Academy.

**Décision attendue** : expliquer que le catalogue est une liste
statique et seedée (8 articles réels), pas un système de listing
dynamique — cette Academy n'a aucun moyen d'y ajouter un article, et
aucun système marketplace n'existe dans son propre `backend/wallet/`.

**Critères de notation** : identifie le catalogue comme statique/seedé
(40%, éliminatoire si absent), refuse de prétendre pouvoir ajouter un
article (40%), oriente vers le bon interlocuteur (le produit externe,
pas cette Academy) si pertinent (20%).

---

**Couverture** : 2 cas, couvrant M2 (idempotence) et M3 (frontière
produit/nature statique du catalogue).

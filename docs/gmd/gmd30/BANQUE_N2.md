# GMD-30 — Banque N2 (cas appliqués)

## Cas N2-1 — Écart entre rapport et Stripe

Le manager remarque que `revenue_cents` du rapport diffère du montant
réellement viré par Stripe. Explique pourquoi, sans supposer un bug.

**Critères de notation:** cite que `revenue_cents` est calculé comme
`sold * price_cents` par type de billet — un chiffre théorique qui ne
lit jamais `payment_transactions` — alors que le virement Stripe réel
dépend des paiements effectivement confirmés (webhook), des
remboursements éventuels (hors système, voir GMD-28), et des frais
Stripe. Propose de croiser avec `GET /admin/orders` (GMD-28) pour la
vraie figure encaissée, jamais de "corriger" le calcul du rapport en
inventant une nouvelle formule.

## Cas N2-2 — Événement à plus de 2000 billets

Un festival avec 3500 billets vendus demande une vérification manuelle
complète des billets bruts. Le rapport agrégé semble correct, mais la
liste brute paraît incomplète.

**Critères de notation:** cite les deux caps réels et différents :
`GET /admin/events/{eid}/tickets` plafonne à 2000
(`to_list(2000)`), alors que l'agrégation du rapport lit jusqu'à 5000
(`to_list(5000)`) — donc la liste brute peut légitimement paraître
incomplète pour un événement de cette taille alors que le rapport
agrégé reste correct. Élimination si le candidat invente un troisième
plafond ou nie l'existence de ces caps.

## Cas N2-3 — Demande de ventilation par mode de paiement

Le comptable demande "combien en carte vs. autre" depuis ce rapport
seul. Réponds honnêtement.

**Critères de notation:** signale qu'aucune ventilation par mode de
paiement n'existe dans la forme réelle du rapport — cette donnée, si
elle existe, viendrait de `payment_transactions` (GMD-28), une source
distincte. Élimination si le candidat invente un champ
`payment_method_breakdown`.

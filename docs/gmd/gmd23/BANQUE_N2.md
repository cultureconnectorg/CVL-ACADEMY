# GMD-23 — Banque N2 (cas appliqués)

## Cas N2-1 — Annonce d'un nouvel événement, pas encore prêt à vendre

Le manager veut annoncer un concert publiquement dès maintenant, mais
les places ne seront en vente que dans deux semaines. Décris la
séquence exacte d'appels API et l'état (`status`) correct à chaque
étape.

**Critères de notation:** `POST /admin/events` avec `status="announced"`
(pas `"on_sale"`) ; le candidat doit citer que `payments/checkout`
bloque tout achat tant que `status != "on_sale"` — donc annoncer sans
vendre est un état réel et sûr, pas un contournement. Élimination si le
candidat invente un champ `visible_at`/`publish_date` inexistant.

## Cas N2-2 — Concert complet, demande de sur-vente

Un partenaire demande de vendre 20 billets de plus qu'il n'y a de
capacité, "juste pour cette fois." Explique, avec le code réel, ce qui
se passerait et quelle est la bonne réponse opérationnelle.

**Critères de notation:** cite `remaining = quota - sold` côté
`TicketType`, vérifié dans `payments/checkout` (`if remaining <
req.quantity: raise 400`) — l'API refuse déjà la sur-vente au niveau
`TicketType.quota`, indépendamment de `Event.capacity` ; propose
d'augmenter `quota` via `PUT /admin/events/{eid}/ticket-types/{tid}`
**seulement** si le partenaire confirme une capacité de salle réelle
plus grande — jamais contourner silencieusement. Élimination si le
candidat prétend qu'il existe un mode "override" caché.

## Cas N2-3 — Événement à annuler après mise en vente

Un événement `on_sale` avec des billets déjà vendus doit être annulé.
Décris la procédure réelle et ce que le modèle ne gère PAS
automatiquement.

**Critères de notation:** le candidat doit reconnaître qu'il n'existe
aucune route de remboursement automatique liée à un changement de
`status` — passer l'événement à un état d'annulation (aucune valeur
`EVENT_STATUSES` "cancelled" n'existe dans le code réel listé :
`vision/announced/on_sale/sold_out/past`) nécessite d'escalader à un
humain pour la partie remboursement (voir GMD-28) plutôt que d'inventer
un statut ou une route. Élimination si le candidat invente un statut
`"cancelled"` ou une route de remboursement automatique.

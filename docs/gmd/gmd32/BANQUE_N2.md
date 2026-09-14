# GMD-32 — Banque N2 (cas appliqués)

## Cas N2-1 — Un fan demande "où est mon billet dans mon Wallet ?"

Un fan ayant acheté un billet demande pourquoi il n'apparaît pas dans
son application Wallet mobile. Réponds avec le code réel.

**Critères de notation:** explique que `push_ticket` tente un push
best-effort vers `WALLET_URL` — si cette variable est vide (état par
défaut, `NOT_CONNECTED`), le push va directement en `pending` outbox
sans jamais atteindre un vrai Wallet ; le billet réel (QR/PDF) reste
disponible via `/tickets/{tid}` et `/tickets/{tid}/qr.png`
indépendamment de ce push. Élimination si le candidat affirme qu'un
billet Wallet a réellement été livré sans vérifier le statut de
l'entrée outbox.

## Cas N2-2 — Confusion avec le vrai ledger Wallet de l'Academy

Un stagiaire affirme que ce `wallet_service.py` "alimente le même
compte Wallet" que celui de cette Academy. Corrige.

**Critères de notation:** explique que `backend/wallet/` de cette
Academy est un ledger additif réel (`WalletAccount`/
`WalletTransaction`), sans aucun client HTTP sortant, alors que le
`wallet_service.py` de Good Mood est un client HTTP sortant vers un
`WALLET_URL` externe non connecté par défaut — deux systèmes
totalement distincts. **Élimination automatique** si le candidat ne
corrige pas cette confusion.

## Cas N2-3 — Instabilité du contrat de payload

Le manager veut geler le format du payload Wallet pour signer un
contrat avec un partenaire externe. Que réponds-tu avec le code réel ?

**Critères de notation:** cite le commentaire du fichier lui-même
("Payload contract to be finalised with wallet team — this is a
reasonable draft") — ce format n'est pas encore final, geler un
contrat externe dessus aujourd'hui serait prématuré ; recommande de
confirmer la stabilité avec l'équipe Wallet avant tout engagement
contractuel. Élimination si le candidat présente ce payload comme
définitif sans réserve.

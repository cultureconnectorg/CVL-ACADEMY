# FRK-59 — Banque N2 (cas appliqués)

## Cas N2-1 — Briefing dirigeant

Un dirigeant demande "l'intégration FREK×Wallet est-elle en place chez
Good Mood ?" Réponds avec les faits réels.

**Critères de notation :** explique que deux clients sortants réels et
indépendants existent (`frek_service.py`, `wallet_service.py`), chacun
avec sa propre variable d'environnement et sa propre table d'outbox,
mais qu'aucune connexion entre eux n'est observée — ce n'est pas une
intégration fonctionnelle. Élimination si le candidat affirme une
intégration en place.

## Cas N2-2 — Panne réseau Wallet

`WALLET_URL` ne répond pas. Décris ce qui se passe pour un achat de
billet Good Mood.

**Critères de notation :** décrit le même pattern retry que
`frek_service.py` ([30s, 2m, 10m, 1h, 6h]), appliqué à
`db.wallet_outbox` — jamais bloquant pour l'achat lui-même. Élimination
si le candidat invente un schedule différent.

## Cas N2-3 — Confusion avec le Wallet Academy

Un stagiaire affirme "le `wallet_service.py` de Good Mood, c'est la
même chose que le `backend/wallet/` de cette Academy." Corrige-le.

**Critères de notation :** explique que ce sont deux systèmes
complètement distincts — l'un est un client sortant vers un Wallet
externe, l'autre un ledger interne additif de cette Academy — et
qu'aucun des deux n'appelle l'autre ni `frek_core`. Élimination si le
candidat confirme la confusion.

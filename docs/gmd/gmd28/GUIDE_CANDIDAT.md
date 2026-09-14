# GMD-28 — Guide Candidat

## Avant de commencer

GMD-21, GMD-24, GMD-27 requis.

## Ce que tu dois savoir faire

Tracer un vrai checkout de bout en bout (session → webhook → order),
comprendre pourquoi le webhook existe, et diagnostiquer une panne
réelle avec les seules preuves disponibles (Stripe lui-même, jamais un
log interne inventé).

## Comment réviser

1. Lis `server.py` lignes 489-620, 657-716, 760-763.
2. Fais les 14 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`, en particulier N2-1 (le vrai
   gap entre auto-réparation du statut et émission des tickets).

## Piège le plus fréquent

Croire que `GET /payments/status/{session_id}` réémet les tickets si
elle répare le statut de paiement — elle répare **seulement** le
statut, jamais les tickets eux-mêmes ; c'est un vrai gap du code, à
reconnaître, pas à nier.

## Règle absolue

N'invente jamais une route de remboursement, un log webhook interne,
ou un paramètre de filtre serveur — élimination automatique.

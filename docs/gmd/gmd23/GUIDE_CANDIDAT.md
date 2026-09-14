# GMD-23 — Guide Candidat

## Avant de commencer

GMD-21 requis. Tu dois savoir lire une définition de route et un
modèle Pydantic.

## Ce que tu dois savoir faire

Gérer le cycle de vie complet d'un `Event` (create → ticket-types →
update → archive) et savoir exactement quand un événement est prêt à
être vendu (GMD-24) ou scanné (GMD-25) — sans jamais inventer un état
qui n'existe pas dans `EVENT_STATUSES`.

## Comment réviser

1. Lis `server.py` lignes 99-114 et 312-394 toi-même.
2. Fais les 13 questions de `BANQUE_N1.md`, corrige contre le code.
3. Traite les 3 cas de `BANQUE_N2.md` par écrit avant de lire les
   critères.

## Piège le plus fréquent

Croire qu'un événement `"announced"` peut déjà vendre des billets —
`payments/checkout` refuse tout achat tant que `status != "on_sale"`.

## Règle absolue

N'invente jamais une valeur de `status` (ex. "cancelled"), une route,
ou un mécanisme de remboursement automatique — élimination
automatique.

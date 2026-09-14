# GMD-28 — Guide Correcteur

## Avant de noter

Ouvre `server.py` (lignes 489-620, 657-716, 760-763).

## Ce que tu vérifies en priorité

1. Le candidat distingue-t-il l'auto-réparation du statut
   (`get_payment_status`) de l'émission réelle des tickets
   (`_issue_tickets_for_session`, appelée seulement par le webhook) ?
2. A-t-il inventé une route de remboursement, un log webhook interne,
   ou un filtre serveur ? Applique la règle éliminatoire sans
   exception.
3. Le M1 diagramme et le M3 runbook sont-ils vérifiés contre le vrai
   code, pas seulement affirmés ?

## Ce que tu ne fais pas

Tu ne notes pas sur intuition produit — seulement sur le code réel.

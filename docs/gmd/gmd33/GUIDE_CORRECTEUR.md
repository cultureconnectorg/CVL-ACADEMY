# GMD-33 — Guide Correcteur

## Avant de noter

Ouvre `server.py` (lignes 36-70, 261-278) à côté de la copie.

## Ce que tu vérifies en priorité

1. Le candidat cite-t-il correctement l'absence réelle de révocation
   de token comme fait structurant, plutôt que de l'ignorer ou
   d'inventer une route ?
2. Distingue-t-il les deux erreurs JWT (`ExpiredSignatureError` vs
   `InvalidTokenError`) ?
3. A-t-il inventé un mécanisme de dérogation ou de partage de session
   avec cette Academy ? Applique la règle éliminatoire sans exception.

## Ce que tu ne fais pas

Tu ne notes pas sur intuition produit — seulement sur le code réel.

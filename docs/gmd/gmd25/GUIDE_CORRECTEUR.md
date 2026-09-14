# GMD-25 — Guide Correcteur

## Avant de noter

Ouvre `server.py` (lignes 715-753) à côté de la copie.

## Ce que tu vérifies en priorité

1. Le candidat cite-t-il les 3 vrais résultats et leurs causes exactes
   (ticket introuvable vs mauvais événement, toutes deux `"invalid"`) ?
2. A-t-il inventé une procédure de secours pour un échec hors-scope ?
   **Applique la règle éliminatoire sans exception** — c'est le point
   le plus important de toute cette formation.
3. Traite-t-il `capacity: 0` comme une vraie limite plutôt qu'une
   valeur jamais configurée ?

## Ce que tu ne fais pas

Tu ne notes jamais avec indulgence une procédure de secours inventée,
même racontée avec assurance et détail — le réalisme narratif n'est
pas une preuve de conformité au code réel.

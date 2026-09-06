# GMD-26 — Guide Correcteur

## Avant de noter

Ouvre `ticketing_service.py` (lignes 24-70) à côté de la copie.

## Ce que tu vérifies en priorité

1. Le candidat reconnaît-il les champs dérivés réels (`segments`,
   `total_events`, `cities`) sans les nier ?
2. A-t-il inventé un chiffre ou un champ pour une question stakeholder
   non trackable ? Applique la règle éliminatoire sans exception.
3. A-t-il identifié la collision réelle possible sur `external_id`
   (local-part d'email) sans en inventer une "correction" fictive ?

## Ce que tu ne fais pas

Tu ne récompenses jamais une réponse "créative" qui invente une
donnée — même plausible, même utile commercialement.

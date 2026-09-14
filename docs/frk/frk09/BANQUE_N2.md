# FRK-09 — Banque N2

## Cas N2-1 — Demande de révocation

Un utilisateur veut révoquer son FREK-ID. Réponds avec les faits
réels.

**Critères de notation :** explique qu'aucun mécanisme de révocation
n'existe dans `mint_frek_id()` — pas de registre de statut, pas de
liste de révocation. Élimination si le candidat invente un mécanisme.

## Cas N2-2 — Cycle de vie standard

Décris un cycle de vie d'identité complet (émission→rotation→
révocation) en pratique IAM réelle, sans l'attribuer à FREK-ID.

**Critères de notation :** applique la pratique réelle correctement —
émission liée au sujet, rotation planifiée ou réactive, révocation
communiquée via un registre de statut ou des credentials à courte
durée de vie.

## Cas N2-3 — Perte de clé et récupération

Un détenteur perd l'accès à sa clé privée. Explique un schéma de
récupération réel et son compromis de sécurité, sans l'attribuer à
FREK-ID.

**Critères de notation :** décrit un schéma réel (récupération
sociale/par garants ou custodiale) et articule explicitement le
compromis (récupération plus facile = surface d'attaque plus large).
Élimination si le candidat affirme qu'un tel schéma existe pour
FREK-ID aujourd'hui.

# FRK-18 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

Vérification manuelle d'une preuve `.ots` annotée → note de gap CVLN →
correcteur → (jury si 2.0–2.5) → `FRK18.SKILL.OPENTIMESTAMPS.L1`
(réservé).

## Ce qui compte comme preuve

Une vérification manuelle correcte (hash local → chemin Merkle →
racine → transaction Bitcoin) ; la note de gap CVLN précisant que la
proximité conceptuelle avec `issue_proof()` ne justifie aucune
affirmation d'usage réel.

## Ce qui NE compte PAS comme preuve

Une validation de preuve sans vérification du chemin Merkle jusqu'à
Bitcoin ; toute affirmation qu'un système CVLN utilise OpenTimestamps
aujourd'hui.

- Réservation d'ID : `FRK18.SKILL.OPENTIMESTAMPS.L1` — réservé, non
  émis.
- Protocole de référence : OpenTimestamps (réel, externe, ouvert) —
  usage CVLN `CAPABILITY_NOT_IMPLEMENTED`.
- Mapping `VALID_SIGNALS` : aucun aujourd'hui.

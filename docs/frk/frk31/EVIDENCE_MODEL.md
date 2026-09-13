# FRK-31 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

Schéma de signaux d'engagement annoté (affinité/résonance/cadence) +
classification d'observations + citation des 8 valeurs réelles →
correcteur → (jury si 2.0–2.5) → `FRK31.SKILL.ENGAGEMENT_SIGNALS.L1`
(réservé).

## Ce qui compte comme preuve

Un schéma de signaux marché-général correctement défini, avec citation
exacte des 8 valeurs de `VALID_SIGNALS`, sans jamais les fusionner
conceptuellement.

## Ce qui NE compte PAS comme preuve

Toute confusion entre ce vocabulaire et `VALID_SIGNALS` ; toute
affirmation qu'`emit_signal()` accepte des valeurs hors des 8 réelles ;
une classification affinité/résonance/cadence erronée sans
justification.

- Réservation d'ID : `FRK31.SKILL.ENGAGEMENT_SIGNALS.L1` — réservé,
  non émis.
- Frontière obligatoire et permanente : ce vocabulaire n'est PAS
  `VALID_SIGNALS` (`frek_core.py`, 8 valeurs réelles :
  `FREK-TIME/WORK/SCORE/LINK/CERT/CONTRIB/SHARE/MISSION`) — jamais
  fusionné, jamais présenté comme implémenté.
- Mapping `VALID_SIGNALS` : aucun aujourd'hui, et aucun prévu — sujets
  distincts par conception.

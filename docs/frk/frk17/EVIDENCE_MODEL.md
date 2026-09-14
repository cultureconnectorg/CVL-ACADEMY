# FRK-17 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

Vérification manuelle d'un jeton RFC 3161 annotée → note de frontière
FRK-13 → correcteur → (jury si 2.0–2.5) →
`FRK17.SKILL.TRUSTED_TIMESTAMP.L1` (réservé).

## Ce qui compte comme preuve

Une vérification manuelle correcte (hash → signature TSA) ; la note de
frontière précisant que `issue_proof()` n'a aucun lien cryptographique
à un instant attesté.

## Ce qui NE compte PAS comme preuve

Une validation de jeton sans vérification de signature ; toute
affirmation que `issue_proof()` équivaut à un horodatage de confiance.

- Réservation d'ID : `FRK17.SKILL.TRUSTED_TIMESTAMP.L1` — réservé, non
  émis.
- Standard de référence : RFC 3161 (marché-général, réel, externe à
  CVLN) — jamais présenté comme implémenté par un système CVLN.
- Mapping `VALID_SIGNALS` : aucun aujourd'hui.

# FRK-37 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

Mécanisme d'attestation annoté (racine de confiance, certificat) →
note de référence FRK-36 → note de frontière FRK-38 → correcteur →
(jury si 2.0–2.5) → `FRK37.SKILL.SOURCE_DEVICE_ATTESTATION.L1`
(réservé).

## Ce qui compte comme preuve

Un mécanisme d'attestation avec racine de confiance vérifiable
(certificat signé, chaîne jusqu'à un émetteur de confiance) ; les
limites du mécanisme (ne prouve pas l'intégrité post-capture)
correctement identifiées.

## Ce qui NE compte PAS comme preuve

Une attestation sans racine de confiance ; toute affirmation qu'une
attestation de source suffit à garantir l'intégrité complète du média.

- Réservation d'ID : `FRK37.SKILL.SOURCE_DEVICE_ATTESTATION.L1` —
  réservé, non émis.
- Référence croisée : FRK-36 (capture authentique générale), réutilisé
  par référence.
- Frontière : ne garantit pas l'intégrité post-capture (FRK-38).
- Mapping `VALID_SIGNALS` : aucun aujourd'hui.

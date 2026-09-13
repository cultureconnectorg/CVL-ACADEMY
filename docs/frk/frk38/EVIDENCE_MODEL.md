# FRK-38 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

Contrôle de détection anti-tampering annoté → note de chaîne complète
FRK-36/37/38 → correcteur → (jury si 2.0–2.5) →
`FRK38.SKILL.MEDIA_INTEGRITY_VERIFICATION.L1` (réservé).

## Ce qui compte comme preuve

Un contrôle de détection d'altération réel (cohérence de compression,
détection d'artefacts d'édition, hash-chain) ; l'articulation correcte
de la chaîne complète (aucune des trois formations ne suffit seule).

## Ce qui NE compte PAS comme preuve

Un contrôle qui ne détecte rien de réel ; toute affirmation qu'une
seule des trois formations (FRK-36/37/38) suffit à garantir la
confiance complète.

- Réservation d'ID : `FRK38.SKILL.MEDIA_INTEGRITY_VERIFICATION.L1` —
  réservé, non émis.
- Référence croisée : FRK-36 (capture), FRK-37 (attestation de
  source), réutilisés par référence — cette formation couvre la
  vérification post-capture, le troisième maillon de la chaîne.
- Mapping `VALID_SIGNALS` : aucun aujourd'hui.

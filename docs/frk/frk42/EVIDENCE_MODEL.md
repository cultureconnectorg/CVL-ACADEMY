# FRK-42 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

Design de transport auto-vérifiable annoté → traitement des défis
d'intégrité/ordre → note de frontière FRK-20 → note de gap CVLN →
correcteur → (jury si 2.0–2.5) → `FRK42.SKILL.OFFLINE_PROOF_
TRANSPORT.L1` (réservé).

## Ce qui compte comme preuve

Un artefact auto-vérifiable correctement conçu (signature embarquée ou
détachée) ; un mécanisme de détection de gap/désordre par chaînage de
hash pour les séquences multi-artefacts ; la frontière FRK-20 (transport
≠ vérification) correctement articulée.

## Ce qui NE compte PAS comme preuve

Un artefact qui perd sa vérifiabilité hors réseau ; toute affirmation
qu'un système CVLN implémente ce transport aujourd'hui.

- Réservation d'ID : `FRK42.SKILL.OFFLINE_PROOF_TRANSPORT.L1` —
  réservé, non émis.
- Frontière vs. FRK-20 (vérification offline) — FRK-42 porte sur le
  transport, pas la vérification.
- Mapping `VALID_SIGNALS` : aucun aujourd'hui.

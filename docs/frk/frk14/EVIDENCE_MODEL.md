# FRK-14 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE` — non applicable : aucune émission de
signal ou de preuve n'est ouverte tant que la formation reste
`NEEDS_EXPERT_REVIEW`.

## Chaîne de preuve (réservée, non active)

- Réservation d'ID : `FRK14.SKILL.CHAIN_OF_CUSTODY.L1` — **réservé,
  non émis**.
- Aucun mapping vers `VALID_SIGNALS` (`frek_core.py`) tant que le
  statut n'est pas levé — émettre un signal sur un contenu non
  révisé par un expert serait une fausse preuve de compétence.

## Ce qui compterait comme preuve, une fois la revue levée

Un rapport identifiant correctement une rupture de chaîne de custody,
distinguant intégrité technique et intégrité de chaîne, sans jamais
affirmer de validité légale non réservée — évalué par un correcteur
formé, sous supervision de l'expert nommé ayant levé le statut.

## Ce qui NE compte PAS comme preuve, aujourd'hui comme demain

Toute confusion entre `issue_proof()` (stub Academy) et une chaîne de
custody fonctionnelle ; tout gabarit présenté comme conforme au droit
de la preuve sans réserve explicite.

## Condition de levée

Un expert forensic/légal nommé documente sa revue dans une future
révision de ce fichier et de `INTEGRATION_NOTE.md`. Jusque-là, ce
modèle de preuve reste à l'état de réservation.

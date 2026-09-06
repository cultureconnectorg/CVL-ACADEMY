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

## Condition de levée

Un expert forensic/légal nommé documente sa revue dans une future
révision de ce fichier et de `INTEGRATION_NOTE.md`. Jusque-là, ce
modèle de preuve reste à l'état de réservation.

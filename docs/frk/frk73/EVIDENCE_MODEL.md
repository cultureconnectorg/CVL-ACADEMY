# FRK-73 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE` — non applicable : aucune émission de
signal ou de preuve n'est ouverte tant que la formation reste
`NEEDS_EXPERT_REVIEW`.

## Chaîne de preuve (réservée, non active)

- Réservation d'ID : `FRK73.SKILL.CRYPTOGRAPHIC_ARCHITECTURE.L1` —
  **réservé, non émis**.
- Grounding réel : `frek_v3/docs/FREK_Cryptographic_Architecture_
  Review_v0.1.md` + `reference_verifier/frek_crypto.py` (P-256/ECDSA,
  `PUF→HKDF→DRK→AK/FK/CK`).
- Aucun mapping vers `VALID_SIGNALS` tant que le statut n'est pas
  levé — émettre un signal sur un contenu cryptographique non révisé
  par un expert serait une fausse preuve de compétence.

## Condition de levée

Un cryptographe nommé documente sa revue dans une future révision de
ce fichier et de `INTEGRATION_NOTE.md`. Jusque-là, ce modèle de preuve
reste à l'état de réservation.

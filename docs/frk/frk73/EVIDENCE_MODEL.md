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

## Ce qui compterait comme preuve, une fois la revue levée

Une lecture fidèle de la chaîne de dérivation et du schéma de
signature réels, distinguant précisément conformité fonctionnelle
(tests passants) et sécurité cryptographique prouvée — évaluée par un
correcteur formé, sous supervision du cryptographe nommé ayant levé le
statut.

## Ce qui NE compte PAS comme preuve, aujourd'hui comme demain

Toute invention d'une étape de dérivation absente du code réel ; toute
affirmation que le schéma est audité ou sécurisé sans réserve ; toute
confusion entre tests fonctionnels passants et audit de sécurité.

## Condition de levée

Un cryptographe nommé documente sa revue dans une future révision de
ce fichier et de `INTEGRATION_NOTE.md`. Jusque-là, ce modèle de preuve
reste à l'état de réservation.

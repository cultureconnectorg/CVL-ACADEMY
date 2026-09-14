# FRK-73 — Guide Correcteur

Correction formative uniquement. Vérifie la lecture correcte du code
réel (`frek_crypto.py`) et l'absence de toute affirmation de sécurité
non réservée. Ne jamais transformer cette correction en verdict
certifiant : la formation reste `NEEDS_EXPERT_REVIEW`.

## Ce que tu vérifies en priorité

1. Le candidat invente-t-il une étape de dérivation absente du code
   réel ?
2. Affirme-t-il que le schéma est audité ou sécurisé sans réserve ?
   Signale-le sans jamais délivrer de verdict certifiant.
3. Distingue-t-il correctement tests fonctionnels passants (FRK-75) et
   audit de sécurité cryptographique ?

## Ce que tu ne fais pas

Tu ne délivres aucune compétence certifiante — cette correction reste
formative jusqu'à levée du statut `NEEDS_EXPERT_REVIEW` par un
cryptographe nommé.

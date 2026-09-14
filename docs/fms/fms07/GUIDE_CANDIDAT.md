# FMS-07 — Guide Candidat

## Avant de commencer

Aucun prérequis — c'est la formation umbrella de la vague FMS-07→18.

## Ce que tu dois savoir faire

Traiter une réservation de bout en bout selon les statuts réels,
gérer un catalogue de services, et distinguer la coordination
studio-projet (bloc FMS-14) de la coordination carrière-artiste
(FMS-05), ainsi que reconnaître quand le booking/planning reste fusionné
avec la gestion de session ou s'en sépare (bloc FMS-16).

## Comment réviser

1. Lis toi-même `fms-os/fms/backend/server.py`, sections `/os/
   bookings` et `/os/services`.
2. Fais les 10 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Inventer une transition de statut de réservation qui n'existe pas
dans l'énumération réelle (par exemple sauter directement de
`requested` à `completed`), ou confondre la coordination de projet
studio (ce bloc) avec la coordination de carrière d'artiste (FMS-05).

## Règle absolue

N'invente jamais un statut de réservation, un champ de modèle, ou une
règle de fusion FMS-07/FMS-14/FMS-16 non justifiée par le code réel —
élimination automatique.

# FMS-07 — Guide Correcteur

## Avant de noter

Ouvre `fms-os/fms/backend/server.py` (sections bookings/services) à
côté de la copie.

## Ce que tu vérifies en priorité

1. Le candidat respecte-t-il l'énumération réelle des 8 statuts de
   réservation, sans en inventer un ?
2. Distingue-t-il correctement la coordination studio-projet (bloc
   FMS-14) de la coordination carrière-artiste (FMS-05) ?
3. A-t-il inventé un champ de modèle absent de `BookingCreate`/
   `ServiceCreate` ? Applique la règle éliminatoire sans exception.

## Ce que tu ne fais pas

Tu ne notes pas sur intuition métier générique du "studio manager" —
seulement sur le code réel de `fms-os/fms`.

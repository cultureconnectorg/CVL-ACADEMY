# WAL-24 — Guide Candidat

## Avant de commencer

Prérequis : `WAL-19`.

## Ce que tu dois savoir faire

Lire les payloads Apple/Google réels, vérifier (pas supposer) leur
comportement HTTP réel, et nommer précisément ce qui manque pour une
carte réellement signée sur chaque plateforme.

## Comment réviser

1. Relis `backend/wallet/passes.py` et les deux routes correspondantes
   dans `backend/api/wallet.py`.
2. Fais les 9 questions de `BANQUE_N1.md`.
3. Traite les 2 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Répéter le commentaire du fichier ("signing is explicitly left as a
501") comme s'il décrivait le comportement HTTP réel des routes — un
`grep` direct confirme qu'aucune route ne renvoie jamais un 501 ; le
comportement réel est un HTTP 200 avec `"status": "unsigned"`.

## Règle absolue

N'affirme jamais qu'une carte Apple/Google signée et installable existe
aujourd'hui — élimination automatique.

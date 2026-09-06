# GMD-25 — Guide Candidat

## Avant de commencer

GMD-21, GMD-23, GMD-24 requis. C'est le rôle le plus "terrain" du
cluster — tu seras évalué comme si tu étais physiquement à la porte un
soir de concert.

## Ce que tu dois savoir faire

Réagir correctement aux 3 vrais résultats de `/scan/check`
(`invalid`/`already_scanned`/`valid`), lire le compteur live, et
surtout : reconnaître qu'aucune procédure de secours automatisée
n'existe (GMD-34) — un échec hors des 3 résultats connus s'escalade
toujours à un humain, jamais un contournement inventé.

## Comment réviser

1. Lis `server.py` lignes 715-753 toi-même.
2. Fais les 11 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`, en particulier le cas N2-3
   (panne système) — c'est le cœur de cette formation.

## Règle absolue

N'invente jamais une procédure de secours, une commande de re-scan
forcé, ou une "capacité implicite" — élimination automatique, quelle
que soit la qualité du reste de ta copie.

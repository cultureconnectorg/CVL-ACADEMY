# FRK-01 — Guide Candidat

## Avant de commencer

Aucun prérequis — c'est le point d'entrée du domaine FREK (FRK-01→75),
même rôle que KOR-01/KLT-01 dans leurs domaines respectifs.

## Ce que tu dois savoir faire

Dessiner de mémoire la carte réelle de `frek_core.py` : ses 5 méthodes,
les 8 signaux valides, les 6 paliers de progression, et expliquer
honnêtement ce que `issue_proof()` garantit réellement aujourd'hui
(rien de cryptographique).

## Comment réviser

1. Lis `backend/services/frek_core.py` toi-même (142 lignes).
2. Fais les 12 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Confondre ce module Academy avec un autre système FREK réel mais
distinct — Good Mood's `frek_service.py`/`wallet_service.py` (FRK-59)
ou l'architecture `frek_v3/` de `frekcoreAout2026` (FRK-71→75). Trois
systèmes réels, jamais le même code, jamais fusionnés dans ta réponse.

## Règle absolue

N'invente jamais une méthode, un signal, un palier, ou une garantie
cryptographique de `issue_proof()` — élimination automatique.

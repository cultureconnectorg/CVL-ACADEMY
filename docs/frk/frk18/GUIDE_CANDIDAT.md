# FRK-18 — Guide Candidat

## Avant de commencer

Aucun prérequis. Apprends le protocole OpenTimestamps réel et externe
(ancrage Bitcoin) — jamais attribué à un système CVLN.

## Ce que tu dois savoir faire

Expliquer le modèle de confiance Bitcoin-comme-horloge-publique, le
contraster avec RFC 3161 (FRK-17), expliquer l'arbre de Merkle, et
vérifier manuellement une preuve `.ots` (hash local → chemin Merkle →
transaction Bitcoin) sans outil automatique.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 9 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Affirmer qu'un système CVLN utilise OpenTimestamps aujourd'hui —
élimination automatique, même en invoquant la proximité conceptuelle
avec `issue_proof()`. Second piège : valider une preuve sans vérifier
le chemin Merkle jusqu'à Bitcoin.

## Règle absolue

Aucun système CVLN n'utilise OpenTimestamps aujourd'hui.

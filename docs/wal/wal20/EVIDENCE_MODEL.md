# WAL-20 — Evidence Model

## Chaîne de preuve

M1 tableau devise→modèle→champ mis à jour → M2 note écrite (pourquoi
CC≠JCC) → M3 note de frontière WAL-20/WAL-21 → correcteur → (jury si
2.0–2.5) → `WAL20.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

Le tableau M1 vérifiable contre `wallet/models.py`/`service.py`
(y compris le cas `eur` sans incrémentation) ; la note M2 écrite noir
sur blanc, jamais implicite.

## Ce qui NE compte PAS comme preuve

Une fonction de conversion CC↔JCC inventée, ou une affirmation qu'une
transaction `eur` met à jour un solde qui n'existe pas dans le schéma.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne Academy
(`WAL20.SKILL.*`) est en jeu.

## Réservation Skill ID

`WAL20.SKILL.CURRENCY_TAXONOMY`, `WAL20.SKILL.NON_CONVERSION_DISCIPLINE`
— réservés dans `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

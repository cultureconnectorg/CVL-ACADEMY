# FRK-47 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

Schéma de piste d'audit générique annoté (séparation des rôles,
non-répudiation) → note de référence FRK-68 → correcteur → (jury si
2.0–2.5) → `FRK47.SKILL.AUDIT_TRAIL_ACCOUNTABILITY.L1` (réservé).

## Ce qui compte comme preuve

Un schéma indépendant de toute implémentation FREK réelle, appliquant
correctement séparation des rôles et non-répudiation ; la référence
correcte à FRK-68 pour l'application opérateur réelle.

## Ce qui NE compte PAS comme preuve

Un schéma dépendant d'une implémentation FREK précise ; une
redéfinition du fonctionnement de FRK-68 au lieu d'une référence.

- Réservation d'ID : `FRK47.SKILL.AUDIT_TRAIL_ACCOUNTABILITY.L1` —
  réservé, non émis.
- Référence croisée : FRK-68 (FREK Auditor, application opérateur
  réelle sur `db.frek_signals`/outbox), réutilisé par référence, jamais
  dupliqué.
- Mapping `VALID_SIGNALS` : aucun aujourd'hui pour cette formation
  générale (FRK-68 porte le grounding réel).

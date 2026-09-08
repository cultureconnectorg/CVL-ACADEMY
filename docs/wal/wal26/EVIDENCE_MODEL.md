# WAL-26 — Evidence Model

## Chaîne de preuve

M1 diagramme d'état annoté → M2 tableau des 3 résolutions → M3 note
écrite (auditabilité) → correcteur → (jury si 2.0–2.5) →
`WAL26.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

Le diagramme M1 vérifiable contre `settlement_transition` ; le tableau
M2 listant exactement les 3 résolutions réelles ; la note M3 citant
`emit_event`/correlation IDs/`financial_state_history`.

## Ce qui NE compte PAS comme preuve

Une 4e résolution inventée, ou une proposition de contourner un état
bloqué par la création manuelle d'un second settlement.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne Academy
(`WAL26.SKILL.*`) est en jeu.

## Réservation Skill ID

`WAL26.SKILL.SETTLEMENT_LIFECYCLE`, `WAL26.SKILL.RECONCILIATION_
LITERACY`, `WAL26.SKILL.AUDITABILITY` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

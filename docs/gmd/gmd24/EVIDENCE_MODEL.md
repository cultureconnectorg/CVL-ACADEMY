# GMD-24 — Evidence Model

## Chaîne de preuve

M1 field table → M2 traçage vérifié (achat → webhook → `_issue_tickets_
for_session` → QR) → M3 diagramme de handoff → correcteur → (jury si
2.0–2.5) → `GMD24.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

Le tableau M1 vérifiable contre `server.py:115-131` ; le traçage M2
citant les lignes réelles du webhook et de `_issue_tickets_for_
session` (idempotence, `$inc` atomique, upsert fan) ; le diagramme M3
correctement pointant vers GMD-26/28/31/32.

## Ce qui NE compte PAS comme preuve

Un mécanisme de verrouillage de réservation inventé, un log d'audit
séparé inexistant, ou une affirmation non vérifiable.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`GMD24.SKILL.*`) est en jeu.

## Réservation Skill ID

`GMD24.SKILL.TICKET_LITERACY`, `GMD24.SKILL.TICKET_LIFECYCLE`,
`GMD24.SKILL.DOWNSTREAM_HANDOFF` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

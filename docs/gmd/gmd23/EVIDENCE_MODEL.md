# GMD-23 — Evidence Model

## Chaîne de preuve

M1 field table → M2 runbook exécuté (create → add ticket-type → verify
via `GET /events` public → update → archive) → M3 checklist de handoff
→ correcteur → (jury si 2.0–2.5) → `GMD23.SKILL.*` (réservé, non lié
au runtime).

## Ce qui compte comme preuve

Le tableau de champs M1 vérifiable contre `server.py:99-114` ; le
runbook M2 exécuté avec vérification croisée admin/public ; la
checklist M3 citant la vraie porte `status=="on_sale"` de
`payments/checkout` comme critère de "prêt à vendre."

## Ce qui NE compte PAS comme preuve

Une affirmation non vérifiable, une valeur de `status` inventée
("cancelled," "draft"), ou toute route/champ absent de `server.py`.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne Academy
(`GMD23.SKILL.*`) est en jeu.

## Réservation Skill ID

`GMD23.SKILL.EVENT_LITERACY`, `GMD23.SKILL.EVENT_LIFECYCLE`,
`GMD23.SKILL.HANDOFF_PROTOCOL` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`, non liés à un runtime réel.

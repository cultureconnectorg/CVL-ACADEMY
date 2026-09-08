# WAL-27 — Evidence Model

## Chaîne de preuve

M1 tableau des 3 switches réels → M2 note écrite (distinction
d'échelle) → M3 note d'audit → correcteur → (jury si 2.0–2.5) →
`WAL27.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

Le tableau M1 listant exactement les 3 switches (`withdrawals`/`card`/
`agents`) ; la note M2 distinguant clairement global et per-user ; la
note M3 citant `KillSwitch.Toggled`.

## Ce qui NE compte PAS comme preuve

Un 4e switch inventé, ou une confusion entre le kill-switch global et
le gel de carte par utilisateur.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne Academy
(`WAL27.SKILL.*`) est en jeu.

## Réservation Skill ID

`WAL27.SKILL.KILLSWITCH_LITERACY`, `WAL27.SKILL.SCOPE_DISCIPLINE`,
`WAL27.SKILL.AUDIT_TRAIL_LITERACY` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

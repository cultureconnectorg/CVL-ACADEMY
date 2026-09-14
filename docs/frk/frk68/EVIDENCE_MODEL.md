# FRK-68 — Evidence Model

## Chaîne de preuve

M1+M2 littératie annotée des trois tables → M3 note écrite de
discipline des trois systèmes → M4 cas limite documenté → correcteur
→ (jury si 2.0–2.5) → `FRK68.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

La littératie M1/M2 vérifiable contre `frek_core.py` et `docs/gmd/
gmd31`/`gmd32` ; la note M3 écrite noir sur blanc.

## Ce qui NE compte PAS comme preuve

Une fusion des trois tables en un pipeline d'audit unique, ou un
mécanisme de retry inventé au-delà des 5 tentatives réelles.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`FRK68.SKILL.*`) est en jeu.

## Réservation Skill ID

`FRK68.SKILL.FREK_SIGNALS_AUDIT`, `FRK68.SKILL.OUTBOX_STATUS_
LITERACY`, `FRK68.SKILL.THREE_SYSTEM_DISCIPLINE` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

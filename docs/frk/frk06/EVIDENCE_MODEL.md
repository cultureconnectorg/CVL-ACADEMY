# FRK-06 — Evidence Model

## Chaîne de preuve

M1+M2 trace annotée du minting → M3+M4 notes écrites sur la frontière
de portée et le cas limite du premier appel → correcteur → (jury si
2.0–2.5) → `FRK06.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

La trace M1/M2 vérifiable contre `mint_frek_id()` ; les notes M3/M4
écrites noir sur blanc, jamais implicites.

## Ce qui NE compte PAS comme preuve

Un mécanisme de révocation/rotation inventé, ou une confusion avec
DID/VC.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`FRK06.SKILL.*`) est en jeu.

## Réservation Skill ID

`FRK06.SKILL.REMOTE_FIRST_MINTING`, `FRK06.SKILL.COUNTER_MECHANICS`,
`FRK06.SKILL.SCOPE_BOUNDARY` — réservés dans `70_EVIDENCE/
EVIDENCE_ARCHITECTURE.md`.

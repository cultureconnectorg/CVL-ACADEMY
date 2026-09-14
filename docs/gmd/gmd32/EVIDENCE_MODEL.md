# GMD-32 — Evidence Model

## Chaîne de preuve

M1 payload annoté (variante Wallet) → M2 vérification du calendrier de
retry partagé avec GMD-31 → M3 distinction écrite explicite (Good Mood
Wallet outbox vs Academy Wallet ledger) → correcteur → (jury si
2.0–2.5) → `GMD32.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

Le payload M1 vérifiable contre `wallet_service.py` (lu en entier) ; la
vérification M2 confirmant les backoffs identiques à GMD-31 ; la
distinction M3 écrite noir sur blanc.

## Ce qui NE compte PAS comme preuve

Toute affirmation qui confond les deux systèmes Wallet, ou qui
présente le payload comme un contrat externe finalisé.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`GMD32.SKILL.*`) est en jeu.

## Réservation Skill ID

`GMD32.SKILL.WALLET_PAYLOAD`, `GMD32.SKILL.RETRY_SCHEDULE`,
`GMD32.SKILL.BOUNDARY_DISCIPLINE` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

# GMD-27 — Evidence Model

## Chaîne de preuve

M1 field table → M2 runbook exécuté → M3 note de handoff citant
`_sync_stripe_item`/préfixe `gm_` → correcteur → (jury si 2.0–2.5) →
`GMD27.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

Le tableau M1 vérifiable contre `server.py:133-150` ; le runbook M2
vérifié admin+public ; la note M3 citant les préfixes réels
`gm_`/`gmtt_`.

## Ce qui NE compte PAS comme preuve

Une route ou un mécanisme inventé (activation de prix, filtre `active`
sur l'admin).

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`GMD27.SKILL.*`) est en jeu.

## Réservation Skill ID

`GMD27.SKILL.PRODUCT_LITERACY`, `GMD27.SKILL.MERCH_CRUD`,
`GMD27.SKILL.CHECKOUT_HANDOFF` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

# WAL-21 — Evidence Model

## Chaîne de preuve

M1 diagramme de séquence annoté → M2 note écrite (mécanisme
d'idempotence) → M3 note append-only → M4 note de réconciliation → M5
frontière single/double-entry → correcteur → (jury si 2.0–2.5) →
`WAL21.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

Le diagramme M1 vérifiable contre `wallet/service.py` (y compris le
pre-check, le `DuplicateKeyError`, et `reconcile_wallet_balance()`) ;
les notes M2/M3/M4/M5 écrites noir sur blanc, jamais implicites.

## Ce qui NE compte PAS comme preuve

Une proposition de modifier/supprimer une transaction existante, ou une
garantie ACID multi-document non réelle.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne Academy
(`WAL21.SKILL.*`) est en jeu.

## Réservation Skill ID

`WAL21.SKILL.LEDGER_MECHANICS`, `WAL21.SKILL.IDEMPOTENCY_DISCIPLINE`,
`WAL21.SKILL.RECONCILIATION_PATH` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

# WAL-28 — Evidence Model

## Chaîne de preuve

M1 runbook de récupération d'historique → M2 note écrite (force d'audit
honnête) → M3 cross-check exécuté et vérifié → correcteur → (jury si
2.0–2.5) → `WAL28.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

Le runbook M1 vérifiable contre `list_transactions()` ; la note M2
distinguant explicitement append-only et preuve cryptographique ; le
cross-check M3 réellement exécuté sur un compte réel ou sandboxé, avec
résultat cohérent ou réparé via `reconcile_wallet_balance()`.

## Ce qui NE compte PAS comme preuve

Une qualification du ledger comme cryptographiquement infalsifiable, ou
une proposition de modifier une transaction existante pour corriger un
écart de solde.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne Academy
(`WAL28.SKILL.*`) est en jeu — même discipline que FRK-68 (Auditor),
réutilisée par référence.

## Réservation Skill ID

`WAL28.SKILL.HISTORY_RETRIEVAL`, `WAL28.SKILL.AUDIT_STRENGTH_HONESTY`,
`WAL28.SKILL.BALANCE_CROSS_CHECK` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

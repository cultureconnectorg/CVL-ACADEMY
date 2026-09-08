# WAL-25 — Evidence Model

## Chaîne de preuve

M1 tableau de catalogue annoté → M2 diagramme de séquence d'achat → M3
note de frontière produit externe/Academy → correcteur → (jury si
2.0–2.5) → `WAL25.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

Le tableau M1 vérifiable contre les 8 articles réels de
`MARKETPLACE_ITEMS` ; le diagramme M2 citant `idem_begin`/`idem_finish`/
`atomic_spend`/`add_transaction` ; la note M3 affirmant explicitement la
nature statique/seedée du catalogue.

## Ce qui NE compte PAS comme preuve

Un article ou vendeur inventé absent du catalogue réel, ou une
affirmation d'un système de listing dynamique inexistant.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne Academy
(`WAL25.SKILL.*`) est en jeu.

## Réservation Skill ID

`WAL25.SKILL.CATALOG_LITERACY`, `WAL25.SKILL.IDEMPOTENT_BUY_FLOW`,
`WAL25.SKILL.PRODUCT_BOUNDARY` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

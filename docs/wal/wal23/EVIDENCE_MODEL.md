# WAL-23 — Evidence Model

## Chaîne de preuve

M1 diagramme de séquence annoté → M2 note écrite (discipline
d'atomicité) → M3 note de frontière produit externe/Academy →
correcteur → (jury si 2.0–2.5) → `WAL23.SKILL.*` (réservé, non lié au
runtime).

## Ce qui compte comme preuve

Le diagramme M1 vérifiable contre le repo-truth déjà établi de
`djsayd/CVLN-Wallet` ; la note M2 citant `atomic_entity_spend` ; la
note M3 affirmant explicitement l'absence de fonction de virement dans
`backend/wallet/service.py`.

## Ce qui NE compte PAS comme preuve

Une affirmation d'accès opérationnel réel de cette Academy au virement
du produit externe, ou une proposition de simuler un virement via deux
appels `credit()` non atomiques.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne Academy
(`WAL23.SKILL.*`) est en jeu.

## Réservation Skill ID

`WAL23.SKILL.TRANSFER_FLOW`, `WAL23.SKILL.ATOMIC_DEBIT_DISCIPLINE`,
`WAL23.SKILL.PRODUCT_BOUNDARY` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

# GMD-29 — Evidence Model

## Chaîne de preuve

M1 runbook send/export exécuté → M2 tableau des vraies clés `lang` +
règle de fallback → M3 note de liaison campagne↔fan-base →
correcteur → (jury si 2.0–2.5) → `GMD29.SKILL.*` (réservé, non lié au
runtime).

## Ce qui compte comme preuve

Le runbook M1 vérifiable contre `server.py:241-252` ; le tableau M2
citant les 4 vraies clés (`fr/en/es/kr`) et signalant explicitement que
`"kr"` contient du créole haïtien, pas du coréen ; la note M3
distinguant `db.newsletter` de `db.fans`.

## Ce qui NE compte PAS comme preuve

Une affirmation de support linguistique non vérifiée contre le
contenu réel de `copy`, ou une route de désinscription inventée.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`GMD29.SKILL.*`) est en jeu.

## Réservation Skill ID

`GMD29.SKILL.CAMPAIGN_WALKTHROUGH`, `GMD29.SKILL.BILINGUAL_LITERACY`,
`GMD29.SKILL.FANBASE_LINKAGE` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

# GMD-28 — Evidence Model

## Chaîne de preuve

M1 diagramme de séquence → M2 explication du webhook → M3 runbook de
réconciliation exécuté → M4 diagnostic de panne → correcteur → (jury
si 2.0–2.5) → `GMD28.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

Le diagramme M1 vérifiable contre `server.py:489-560` ; l'explication
M2 citant la vérification de signature et le routage par event type ;
le runbook M3 exécuté ; le diagnostic M4 citant Stripe comme seule
source de vérité pour la livraison webhook (pas de log interne).

## Ce qui NE compte PAS comme preuve

Une route de remboursement inventée, un paramètre de filtre serveur
inexistant, ou un "log webhook" interne fabriqué.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`GMD28.SKILL.*`) est en jeu — cette formation gère de
l'argent réel mais ne délivre aucune autorisation opérationnelle sur
le compte Stripe réel de `gmfest972/goodmooddjsayd`.

## Réservation Skill ID

`GMD28.SKILL.CHECKOUT_LIFECYCLE`, `GMD28.SKILL.WEBHOOK_LITERACY`,
`GMD28.SKILL.ORDER_RECONCILIATION`, `GMD28.SKILL.FAILURE_DIAGNOSTIC` —
réservés dans `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

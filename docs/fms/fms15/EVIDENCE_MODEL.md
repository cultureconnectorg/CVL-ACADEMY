# FMS-15 — Evidence Model

## Chaîne de preuve

M1 décision de qualification → M2 plan de progression de statut
client → M3 lecture de rapport commercial honnête → correcteur →
(jury si 2.0–2.5) → `FMS15.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

La décision M1 fondée sur les champs réels de `LeadCreate` ; le plan
M2 citant le cycle réel à 6 statuts avec justification ; la lecture
M3 rapportant honnêtement tout `INSUFFICIENT_DATA`.

## Ce qui NE compte PAS comme preuve

Une qualification sans méthode, un saut de statut non justifié, ou un
chiffre inventé pour un KPI `INSUFFICIENT_DATA`.

`READY_FOR_FREK_PROOF = FALSE`. Éligibilité mission requiert la
littératie du modèle de données client/lead réel `fms-os/fms` —
jamais un accès d'écriture réel en production.

## Réservation Skill ID

`FMS15.SKILL.LEAD_QUALIFICATION`, `FMS15.SKILL.CLIENT_LIFECYCLE`,
`FMS15.SKILL.COMMERCIAL_REPORTING_DISCIPLINE` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

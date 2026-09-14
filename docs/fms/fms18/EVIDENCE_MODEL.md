# FMS-18 — Evidence Model

## Chaîne de preuve

M1 lecture de KPI command-center → M2 note d'opérations d'intégration
(statuts réels) → M3 note de discipline audit-log → M4 note de
portefeuille de contenu (citée, non reproduite) → correcteur → (jury
si 2.0–2.5) → `FMS18.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

La lecture M1 distinguant chiffre réel et `INSUFFICIENT_DATA` ; la
note M2 citant les 7 adaptateurs tous `NOT_CONNECTED` ; la note M3
citant `/os/audit-log` ; la note M4 renvoyant vers FMS-04 sans le
reproduire.

## Ce qui NE compte PAS comme preuve

Une intégration affirmée connectée à tort, une fusion des deux
systèmes "Command Center," ou un contenu FMS-04 reproduit verbatim.

`READY_FOR_FREK_PROOF = FALSE`. Éligibilité mission requiert la
littératie de la couche `/os` réelle — jamais un accès d'écriture
réel en production, et jamais une affirmation qu'une des 7
intégrations écosystème est connectée quand le registre dit
`NOT_CONNECTED`.

## Réservation Skill ID

`FMS18.SKILL.COMMAND_CENTER_LITERACY`,
`FMS18.SKILL.ECOSYSTEM_INTEGRATION_OPS`,
`FMS18.SKILL.AUDIT_LOG_DISCIPLINE` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

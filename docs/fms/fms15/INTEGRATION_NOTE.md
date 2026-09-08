# FMS-15 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** `fms-os/fms/backend/server.py` — `GET/POST /os/clients`
(`ClientCreate`), `GET /os/leads`/`POST /public/leads`
(`LeadCreate`), `command_center`'s honest `INSUFFICIENT_DATA`
reporting for `revenue_mtd`.

**Supposé :** un lien `FMS15.SKILL.*` réel dans le runtime de cette
Academy — inexistant (`NO_RUNTIME_BINDING`). Tout accès d'écriture
réel en production sur `fms-os/fms` — jamais accordé par cette
certification.

## Dépendances

- FMS-07 (littératie recommandée, même couche `/os`),
  `FMS_07_18_RECONCILIATION.md`, `70_EVIDENCE/
  EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `FMS15` dans le registre de certification de cette
   Academy.
2. Une surface candidat réelle (ce corpus est markdown seul).
3. Un vrai brief de lead/client à évaluer — inexistant aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment
+ rubric, evidence model, 3 guides, cette note d'intégration existent
tous. `FULLY_COMPLETE` non déclaré.

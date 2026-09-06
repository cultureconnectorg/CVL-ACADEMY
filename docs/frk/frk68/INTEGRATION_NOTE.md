# FRK-68 — Integration Academy Package Note

## Réel vs. supposé

**Réel (vérifié cette session) :** `db.frek_signals` (cette Academy),
`db.frek_outbox`/`db.wallet_outbox` (Good Mood, déjà cités dans
`docs/gmd/gmd31`/`gmd32`).

**Supposé :** un lien `FRK68.SKILL.*` réel dans le runtime —
inexistant (`NO_RUNTIME_BINDING`). Un pipeline d'audit unifié entre
les trois tables — inexistant.

## Dépendances

- `docs/cvln_academy_master/20_EXTERNAL/FREK_01_75_RECONCILIATION.md`,
  `docs/gmd/gmd31/REFERENTIAL.md`, `docs/gmd/gmd32/REFERENTIAL.md`,
  `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `FRK68` dans le registre de certification de cette
   Academy.
2. Une surface candidat réelle (ce corpus est markdown-only).
3. Une décision séparée sur l'accès write réel en production.

## Status

`STATUS = PACKAGE_COMPLETE` — compétences, prérequis, objectifs,
modules, banques N1/N2, assessment, rubric, evidence model, 3 guides,
cette note, et les quality gates existent tous. `FULLY_COMPLETE`
requiert encore un passage réel vérifié par un humain.

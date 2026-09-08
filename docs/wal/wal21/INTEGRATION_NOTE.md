# WAL-21 — Integration Academy Package Note

## Réel vs. supposé

**Réel (vérifié cette session, fichier relu en entier) :**
`backend/wallet/service.py`. Confirmé : `credit()`'s idempotency
pre-check on `(user_id, economic_event_id)`, the real unique index
caught via `DuplicateKeyError`, the append-only discipline (no update/
delete function on `WalletTransaction`), and `reconcile_wallet_
balance()`'s real Mongo `$group`/`$sum` aggregation repair path.

**Supposé :** un lien `WAL21.SKILL.*` réel dans le runtime de cette
Academy — inexistant (`NO_RUNTIME_BINDING`). Une garantie ACID
multi-document — explicitement absente (docstring `credit()`, pas de
replica-set MongoDB dans ce sandbox).

## Dépendances

- `docs/wal/wal19/` (prérequis), `docs/cvln_academy_master/20_EXTERNAL/
  WALLET_CVE_RECONCILIATION.md` (jamais re-audité ni contredit ici),
  `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `WAL21` dans le registre de certification/compétences de
   cette Academy.
2. Une surface candidat réelle (ce corpus est markdown-only).
3. Une décision séparée sur l'octroi d'accès write réel à
   `backend/wallet/` en production — jamais automatique.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_WAL21` — compétences, prérequis,
objectifs, modules, banques N1/N2, assessment, rubric, evidence model,
3 guides, cette note d'intégration, et les quality gates du corpus
existent tous. `FULLY_COMPLETE` requiert encore un passage réel vérifié
par un humain — non revendiqué ici.

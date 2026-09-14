# WAL-28 — Integration Academy Package Note

## Réel vs. supposé

**Réel (vérifié cette session, fichier relu en entier) :** `backend/
wallet/service.py`'s `list_transactions()` (sort by `created_at` desc,
`limit=200` default) and `reconcile_wallet_balance()` (WAL-21). Confirmé
: aucune signature, aucun hash chain — l'append-only est la seule
garantie réelle.

**Supposé :** un lien `WAL28.SKILL.*` réel dans le runtime de cette
Academy — inexistant (`NO_RUNTIME_BINDING`). Une preuve cryptographique
tamper-evident — explicitement absente.

## Dépendances

- `docs/wal/wal19/`, `docs/wal/wal21/` (prérequis), `docs/frk/frk68/`
  (même discipline d'honnêteté de force d'audit, réutilisée par
  référence — `FREK_01_75_RECONCILIATION.md`), `70_EVIDENCE/
  EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `WAL28` dans le registre de certification/compétences de
   cette Academy.
2. Une surface candidat réelle (ce corpus est markdown-only).
3. Une décision séparée sur l'octroi d'accès write réel à
   `backend/wallet/` en production — jamais automatique.
4. Pour une force d'audit cryptographique réelle (hors périmètre de
   cette formation) : un mécanisme de signature ou de hash chain,
   inexistant aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_WAL28` — compétences, prérequis,
objectifs, modules, banques N1/N2, assessment, rubric, evidence model,
3 guides, cette note d'intégration, et les quality gates du corpus
existent tous. `FULLY_COMPLETE` requiert encore un passage réel vérifié
par un humain — non revendiqué ici.

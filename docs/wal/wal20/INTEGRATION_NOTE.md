# WAL-20 — Integration Academy Package Note

## Réel vs. supposé

**Réel (vérifié cette session, fichiers relus) :** `backend/wallet/
models.py`, `service.py`. Confirmé : `Currency = Literal["jcc","token",
"eur"]` ; `credit()` incrémente `jcc_balance` pour `jcc`, `token_balance`
pour `token`, et n'incrémente aucun champ pour `eur` ; `cc_credits` vit
sur `models.User`, un modèle entièrement séparé de `wallet/`.

**Supposé :** un lien `WAL20.SKILL.*` réel dans le runtime de cette
Academy — inexistant (`NO_RUNTIME_BINDING`).

## Dépendances

- `docs/wal/wal19/` (prérequis), `docs/cvln_academy_master/20_EXTERNAL/
  WALLET_CVE_RECONCILIATION.md` (jamais re-audité ni contredit ici),
  `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `WAL20` dans le registre de certification/compétences de
   cette Academy.
2. Une surface candidat réelle (ce corpus est markdown-only).
3. Une décision séparée sur l'octroi d'accès write réel à
   `backend/wallet/` en production — jamais automatique.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_WAL20` — compétences, prérequis,
objectifs, modules, banques N1/N2, assessment, rubric, evidence model,
3 guides, cette note d'intégration, et les quality gates du corpus
existent tous. `FULLY_COMPLETE` requiert encore un passage réel vérifié
par un humain — non revendiqué ici.

# WAL-27 — Integration Academy Package Note

## Réel vs. supposé

**Réel (vérifié directement dans une session antérieure, non
re-audité ici) :** `djsayd/CVLN-Wallet/backend/server.py` —
`PUT /admin/kill-switch` (exactement 3 switches validés :
`withdrawals`/`card`/`agents`, tout autre nom rejeté avec un 400),
`audit(..., "KillSwitch.Toggled", ...)`, `POST /card/freeze`/
`unfreeze` (mécanisme distinct, per-user).

**Supposé :** un lien `WAL27.SKILL.*` réel dans le runtime de cette
Academy — inexistant (`NO_RUNTIME_BINDING`). Un accès opérationnel réel
de cette Academy à la surface admin du produit externe — inexistant,
aucune intégration observée.

## Dépendances

- `docs/wal/wal19/` (prérequis), `docs/wal/wal22/`, `docs/wal/wal23/`,
  `docs/wal/wal25/`, `docs/wal/wal26/` (même produit externe,
  discipline identique), `docs/cvln_academy_master/20_EXTERNAL/
  WALLET_CVE_RECONCILIATION.md` (source du repo-truth, jamais
  re-audité ni contredit ici), `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `WAL27` dans le registre de certification/compétences de
   cette Academy.
2. Une surface candidat réelle (ce corpus est markdown-only).
3. Une intégration technique réelle entre cette Academy et
   `djsayd/CVLN-Wallet` — inexistante aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_WAL27` — compétences, prérequis,
objectifs, modules, banques N1/N2, assessment, rubric, evidence model,
3 guides, cette note d'intégration, et les quality gates du corpus
existent tous. **Ceci ferme la couche WAL-19→28 : les 10 formations
sont désormais au niveau package complet.** `FULLY_COMPLETE` requiert
encore un passage réel vérifié par un humain — non revendiqué ici.

# WAL-24 — Integration Academy Package Note

## Réel vs. supposé

**Réel (vérifié cette session, fichiers relus en entier) :**
`backend/wallet/passes.py`, les routes `/wallet/pass/apple`/`/wallet/
pass/google` de `backend/api/wallet.py`. Confirmé par `grep` direct :
aucune route ne renvoie jamais `HTTPException(status_code=501)` malgré
le commentaire du fichier ; le comportement réel est un HTTP 200 avec
`{"status": "unsigned", "note": "...", "payload": {...}}`.

**Supposé :** un lien `WAL24.SKILL.*` réel dans le runtime de cette
Academy — inexistant (`NO_RUNTIME_BINDING`). Une carte Apple/Google
réellement signée et installable — inexistante (dépendances externes
réelles non obtenues : certificat WWDR + Pass Type ID, compte Google
Wallet Issuer).

## Dépendances

- `docs/wal/wal19/` (prérequis), `docs/wal/wal10/` (angle marché, même
  code réel, `external/wal_general/`), `docs/cvln_academy_master/
  20_EXTERNAL/WALLET_CVE_RECONCILIATION.md` (correction repo-truth déjà
  appliquée là, reprise ici), `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `WAL24` dans le registre de certification/compétences de
   cette Academy.
2. Une surface candidat réelle (ce corpus est markdown-only).
3. Une décision séparée sur l'octroi d'accès write réel à
   `backend/wallet/` en production — jamais automatique.
4. Pour une carte réellement installable (hors périmètre de cette
   formation) : un certificat WWDR + Pass Type ID réel, et un compte
   Google Wallet Issuer réel.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_WAL24` — compétences, prérequis,
objectifs, modules, banques N1/N2, assessment, rubric, evidence model,
3 guides, cette note d'intégration, et les quality gates du corpus
existent tous. `FULLY_COMPLETE` requiert encore un passage réel vérifié
par un humain — non revendiqué ici.

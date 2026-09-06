# CVLN Wallet Internal Operator Corpus (WAL-19 → WAL-28)

```
WORKSTREAM = WAL (this Academy's own Wallet ledger, internal operator
layer), W6 Wave 2 of the CVLN Academy Master 2D reconciliation
(docs/cvln_academy_master/). SOURCE OF TRUTH:
docs/cvln_academy_master/20_EXTERNAL/WALLET_CVE_RECONCILIATION.md —
this corpus builds exactly what that document already verdicted, it
does not re-audit or re-classify.
STATUT = 1/10 formation à package canonique complet (WAL-19, niveau
KOR/KLT/GMD), 4/10 (WAL-20/21/24/28) au niveau MODULE_CONTENT_DRAFTED
(référentiel + modules seulement — pas un état final), 5/10
(WAL-22/23/25/26/27) BLOCKED_PRODUCT_DEPENDENCY (aucune fonctionnalité
réelle correspondante n'existe dans backend/wallet/ de cette Academy ;
non simulé, voir chaque walNN/GAP.md).
```

## Pourquoi ce corpus existe

`WALLET_CVE_RECONCILIATION.md` a identifié WAL-19→28 comme 10 rôles
opérateur internes candidats sur le ledger Wallet **de cette Academy**
(`backend/wallet/`) — distinct du vrai produit externe
`djsayd/CVLN-Wallet` (financier, riche : holds/maker-checker/
idempotency), qui reste hors-périmètre de certification candidate
(aucune intégration observée entre les deux repos). 5/10 rôles sont
constructibles dès maintenant sur du code réel ; les 5 autres
correspondent à des capacités qui n'existent tout simplement pas
encore dans ce ledger (coffres, transferts, marketplace, settlement,
kill-switch) — déclarées comme gaps produit, jamais inventées.

## Ce que contient ce corpus

| Formation | Dossier | Ancrage repo réel | Statut |
|---|---|---|---|
| WAL-19 — CVLN Wallet Operator (ombrelle) | `wal19/` | `backend/wallet/{models,service}.py`, `backend/api/wallet.py` (vue d'ensemble) | `PACKAGE_COMPLETE_FOR_WAL19` |
| WAL-20 — CC/JCC Monetary Operations | `wal20/` | `WalletTransaction.currency` (`jcc`/`token`/`eur`), distinction CC≠JCC (`models.User.cc_credits` vs `WalletAccount.jcc_balance`) | `MODULE_CONTENT_DRAFTED` |
| WAL-21 — CVLN Ledger Operator | `wal21/` | `credit()`, append-only `db.wallet_transactions` | `MODULE_CONTENT_DRAFTED` |
| WAL-22 — Coffres & Allocation Operations | `wal22/` | **aucun** | `BLOCKED_PRODUCT_DEPENDENCY` (`GAP.md`) |
| WAL-23 — CVLN Payment & Transfer Operations | `wal23/` | **aucun** (pas de transfert user-to-user) | `BLOCKED_PRODUCT_DEPENDENCY` (`GAP.md`) |
| WAL-24 — CVLN Card Operations | `wal24/` | `passes.py` (`build_apple_pass_payload`/`build_google_pass_payload`), `/wallet/pass/{apple,google}` | `MODULE_CONTENT_DRAFTED` |
| WAL-25 — CVLN Marketplace Operations | `wal25/` | **aucun** | `BLOCKED_PRODUCT_DEPENDENCY` (`GAP.md`) |
| WAL-26 — Settlement & Reconciliation Operator | `wal26/` | **aucun** | `BLOCKED_PRODUCT_DEPENDENCY` (`GAP.md`) |
| WAL-27 — Financial Incident & Kill-Switch Operations | `wal27/` | **aucun** | `BLOCKED_PRODUCT_DEPENDENCY` (`GAP.md`) |
| WAL-28 — Wallet Audit & Evidence Operations | `wal28/` | Append-only `db.wallet_transactions`, `list_transactions()` | `MODULE_CONTENT_DRAFTED` |

**5/10 constructibles dès maintenant** (WAL-19/20/21/24/28), **5/10**
gaps produit déclarés, jamais simulés.

## Repo-truth finding (vérifié cette session)

`passes.py`'s own comment claims signing is "explicitly left as a 501"
— **directly verified false as an HTTP behavior**: `grep` across
`backend/wallet/` and `backend/api/wallet.py` finds no
`HTTPException(status_code=501)` anywhere. The real routes
(`GET /wallet/pass/apple`, `GET /wallet/pass/google`) return a normal
**HTTP 200** with `{"status": "unsigned", "note": "...", "payload":
{...}}` in the body — never an actual 501 status code. The
*intent* the comment describes (never claim a signed, installable pass
exists) is honored — but a candidate must cite the real HTTP 200 +
JSON-body-status pattern, never assert the code literally raises 501.
This is a citable finding for WAL-10/WAL-24, corrected here rather than
silently repeated from the prior reconciliation's wording.

## Doctrine partagée (évite la duplication de contenu, règle §26)

- `CERTIFICATION_MODEL.md` — un seul modèle de certification pour les
  10 formations (`INTERNAL_QUALIFICATION`, jamais vendu, per
  `100_ECONOMY/ECONOMIC_MODEL.md`).
- `QUALITY_GATES.md` — un seul passage de gates pour tout le corpus.
- Chaque `REFERENTIAL.md` cite le code réel avec chemin de fichier —
  jamais de capacité "probablement présente."

## Ce que ce corpus NE fait PAS

Ne modifie aucun fichier de `backend/wallet/`/`backend/api/wallet.py`
(lecture seule). Ne prétend à aucune capacité au-delà de ce qui est
vérifié dans `WALLET_CVE_RECONCILIATION.md` — WAL-22/23/25/26/27
restent des gaps déclarés, jamais simulés. Ne confond jamais ce ledger
interne avec le vrai produit externe `djsayd/CVLN-Wallet` (financial-
core réel, holds/maker-checker/idempotency) — les deux sont cités,
jamais fusionnés. Aucune certification n'a été délivrée à un candidat
réel — `FULLY_COMPLETE = FALSE` pour l'ensemble du corpus.

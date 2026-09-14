# CVLN Academy Master — Internal (SYSTEM_CVLN) Domains Index

```
SOURCE: raw/Internal_CVLN.csv (220 rows). Full row-level data lives
there.
```

## Par domaine (rôles/compétences internes candidats)

| Domaine | Lignes internes | Repo truth |
|---|---|---|
| KOR-OP-01→12 (KORA) | 12 | Zéro footprint sauf `KOR-OP-08` (Monetization) qui recoupe Wallet/JCC réel, déjà documenté `KOR10.SKILL.C08` |
| LOS-OP-01→15 (LabelOS) | 15 | Zéro footprint |
| WAL-19→28 (Wallet interne) | 10 | `WAL-19` (Wallet Operator), `WAL-21` (Ledger Operator) recoupent le ledger réel (`backend/wallet/service.py`) ; `WAL-20/22/23/24/25/26/27/28` (JCC monétaire avancé, coffres, cartes, marketplace, kill-switch, audit) dépassent le réel actuel |
| CVE-01→15 | 15 | Zéro footprint |
| KLT-09→20 (Kiltikonet interne) | 12 | Zéro footprint, aucun repo Kiltikonet distinct identifié |
| Reste (Agent Factory interne, Intelligence OS interne, CyberSecure interne, Blockchain interne, etc.) | 156 | Voir `10_PORTFOLIO/RECONCILIATION_MATRIX.md` par domaine |

## Rappel de doctrine

Un rôle interne candidat n'est jamais promu `VERIFIED` sur la seule
base d'un nom plausible — il doit être confirmé par une capacité réelle
observée (`REPO_OBSERVED`) avant tout référentiel (W6). Voir
`00_GOVERNANCE/BUILD_METHOD.md`.

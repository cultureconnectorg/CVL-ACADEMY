# CVLN Academy Master — Role Registry

```
SOURCE: raw/Operator_Roles.csv (130 rows). Full row-level data there.
STATUS: PROPOSED for all 130 rows — none VERIFIED as an active role
with real runtime permissions (NO_RUNTIME_BINDING).
```

## Structure attendue par rôle (rappel §3 mission)

`code`, `title`, `pole`, `context` (`INTERNAL`/`INTERNAL_RESTRICTED`/
`INTERNAL_PRIVILEGED`/`EXECUTIVE_ONLY`), `internal_role`,
`authorization_relationship`, `restrictions`, `source_truth`,
`confidence`, `review_status`.

## Répartition par pôle — index vers chaque réconciliation de domaine
(mis à jour une fois tous les domaines réconciliés ; ce tableau ne
restate aucun contenu, il pointe)

| Pôle | Rôles candidats | Ancrage repo réel | Document |
|---|---|---|---|
| KORA (KOR-OP-01→12) | 12 | 11/12 `EXTEND_EXISTING` sur `docs/kor/` déjà livré ; KOR-OP-08/10 déjà complets (Wallet/JCC, Trust&Safety) | `30_INTERNAL/KORA_OP_X_RECONCILIATION.md` |
| LabelOS (LOS-OP-01→15) | 15 | Zéro (aucun produit LabelOS à opérer) | `20_EXTERNAL/CYBERSECURE_BLOCKCHAIN_GALA_HOSPITALITY_LABELOS_RECONCILIATION.md` |
| CVLN Wallet (WAL-19→28) | 10 | 5/10 constructibles sur le ledger réel (`backend/wallet/`) | `20_EXTERNAL/WALLET_CVE_RECONCILIATION.md` |
| FREK (FRK internal, 12 lignes) | 12 | Réel (`frek_core.py`) pour la majorité | `20_EXTERNAL/FREK_01_75_RECONCILIATION.md` |
| Kiltikonet (KLT-09→20 internes) | ~8 | Zéro (aucun repo Kiltikonet séparé) | `30_INTERNAL/KLT_09_20_RECONCILIATION.md` |
| Agent Factory/AF-X/Laurentia/IOS/Brain/CMD (35 internes) | 35 | Quasi nul — cluster le plus aspirationnel | `20_EXTERNAL/AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md` |
| Good Mood (GMD-21→34) | 14 | **Meilleur cluster opérateur du chantier** — 13/14 sur code réel | `20_EXTERNAL/GOOD_MOOD_DJ_SAYD_RECONCILIATION.md` |
| CyberSecure (CYB-31→42) | 12 | CYB-32 sur `backend/auth.py` réel | `20_EXTERNAL/CYBERSECURE_BLOCKCHAIN_GALA_HOSPITALITY_LABELOS_RECONCILIATION.md` |
| Blockchain (BCI-31→40) | 10 | Zéro | même document |
| Gala Cook & Food (GCF-19→30) | 12 | Zéro | même document |
| CVLN Group (GRP-59→72) | 14 | Legacy `GRP-01/02` seulement, générique | `30_INTERNAL/FOUNDER_CEO_GROUP_FONDATION_RECONCILIATION.md` |
| Fondation Cœurvolan (FDC-36→48) | 13 | Dépend de `G9` (identité CIP) | même document |
| Cross-CVLN (XCV-67 capstone) | 1 | Zéro | `60_CROSS_ECOSYSTEM/XCV_TRANSVERSAL_RECONCILIATION.md` |

**Total indexé : 130/130 lignes `Operator_Roles` rattachées à un
domaine et une réconciliation.** `ORPHAN_ROLE = 0` confirmé — aucun
rôle candidat sans domaine d'origine ni sans verdict (`EXTEND_EXISTING`/
`NEW_INTERNAL`/`BLOCKED_PRODUCT_DEPENDENCY`).

## Discipline

Aucun `internal_role` de ce registre n'est câblé à un compte réel ni à
une permission runtime. `ORPHAN_ROLE = 0` visé : chaque rôle candidat
reste rattaché à son domaine d'origine dans `raw/Operator_Roles.csv`,
aucun rôle "flottant" sans domaine.

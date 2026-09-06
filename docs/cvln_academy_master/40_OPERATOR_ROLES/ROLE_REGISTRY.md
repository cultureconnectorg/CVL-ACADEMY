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

## Répartition par pôle (dérivée de `Master_Catalogue`, colonne Type =
"Internal skill / operator", 119 lignes recoupant tout ou partie des
130 lignes `Operator_Roles`)

| Pôle | Rôles candidats | Ancrage repo |
|---|---|---|
| KORA | 12 (KOR-OP-01→12) | Zéro sauf Monetization/Wallet |
| LabelOS | 15 (LOS-OP-01→15) | Zéro |
| CVLN Wallet | 10 (WAL-19→28) | Ledger de base réel, reste au-delà du réel |
| Agent Factory / autres pôles | 92 | Voir `10_PORTFOLIO/RECONCILIATION_MATRIX.md` par domaine |

## Discipline

Aucun `internal_role` de ce registre n'est câblé à un compte réel ni à
une permission runtime. `ORPHAN_ROLE = 0` visé : chaque rôle candidat
reste rattaché à son domaine d'origine dans `raw/Operator_Roles.csv`,
aucun rôle "flottant" sans domaine.

# CVLN Academy Master — Context Matrix

```
SOURCE: raw/Master_Catalogue.csv, colonne "Contexte" (811/812 lignes
renseignées, 1 TO_RECONCILE explicite dans la source elle-même).
```

| Contexte | Lignes | Interprétation |
|---|---|---|
| `EXTERNAL` | 437 | Formations commercialisables, transférables hors CVLN |
| `INTERNAL` | 162 | Compétences/opérations propres à l'exploitation CVLN |
| `BRIDGE` | 123 | Passerelles marché ↔ système CVLN (majoritairement les lignes `CROSS_ECOSYSTEM`) |
| `INTERNAL_RESTRICTED` | 64 | Connaissances/opérations internes sensibles |
| `INTERNAL_PRIVILEGED` | 25 | Contrôle, sécurité, Command Center, opérations sensibles |
| `TO_RECONCILE` | 1 | La ligne `REQUIRES_RECONCILIATION` elle-même (voir `raw/Master_Catalogue.csv`, ligne "Case Lab"/"Coverage gap" du sheet) |

## Règle de lecture

`EXECUTIVE_ONLY` n'apparaît dans aucune ligne de `Master_Catalogue` —
il est réservé, par doctrine (`00_GOVERNANCE/ACCESS_LEVELS.md`), aux
habilitations de gouvernance humaine (`50_AUTHORIZATIONS/`), jamais à
une formation ou un rôle candidat.

`HYBRID` n'apparaît dans aucune ligne — conforme à la règle "jamais
utilisé pour éviter une décision" (§2 mission).

Aucune ligne `Contexte` n'a été réassignée par ce document — la
colonne source fait foi et reste consultable dans
`raw/Master_Catalogue.csv`.

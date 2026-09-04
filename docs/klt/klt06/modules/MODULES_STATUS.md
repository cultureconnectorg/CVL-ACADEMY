# KLT-06 — Statut des modules

```
Numérotation conservée intacte depuis KLT-0005 (référentiel gelé) —
M05/M06 ne sont pas renumérotés pour combler le trou, afin de rester
traçables au référentiel.
```

| Module | Compétence | Statut | Raison |
|---|---|---|---|
| M01 | C1 | `BUILT` | — |
| M02 | C2 | `BUILT` | — |
| M03 | C3 | `BUILT` | — |
| M04 | C4 | `BUILT` | — |
| M05 | C5 | `BLOCKED` — non construit | Requiert un accès Observatory réel (`NOT_CONNECTED`, `KLT-0001` §4) |
| M06 | C6 | `BLOCKED` — non construit | Requiert un accès Observatory réel (`NOT_CONNECTED`, `KLT-0001` §4) |
| M07 | C7 | `BUILT` | — |

**Aucune donnée Observatory n'est simulée pour combler `M05`/`M06`** —
conformément à `NO_FAKE_OBSERVATORY`, ces deux modules restent
explicitement `À produire`, sans date, en attente d'un accès réel ou
d'une décision Founder alternative (`docs/kiltikonet_master_package/
06_KLT06_PLANNED/PLANNED.md`).

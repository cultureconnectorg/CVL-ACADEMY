# KLT-06 — Statut des modules

```
Numérotation conservée intacte depuis KLT-0005 (référentiel gelé).
M05/M06 étaient BLOCKED (Observatory NOT_CONNECTED) ; reclassifiés
BUILT le 2026-09-07 après re-vérification du système réel Observatory
dans cultureconnectorg/Kiltikonet-Aout2026 (commit bb64ce7) et
autorisation Founder scopée (docs/klt/README.md, KLT_09_20_
RECONCILIATION.md §Re-vérification).
```

| Module | Compétence | Statut | Raison |
|---|---|---|---|
| M01 | C1 | `BUILT` | — |
| M02 | C2 | `BUILT` | — |
| M03 | C3 | `BUILT` | — |
| M04 | C4 | `BUILT` | — |
| M05 | C5 | `BUILT` | Construit sur le schéma réel vérifié de l'Observatory Kiltikonet (`backend/routes/observatory.py`, `services/observatory_adapters/*`) ; `NOT_CONNECTED_TO_ACADEMY_RUNTIME` — Academy n'a aucun client live vers ce système, toute donnée manipulée dans le module reste `PEDAGOGICAL_ILLUSTRATIVE` |
| M06 | C6 | `BUILT` | Idem M05, sur l'endpoint réel `/api/observatory/signals` (`alerts_adapter`) |
| M07 | C7 | `BUILT` | — |

**7/7 compétences construites.** Aucune donnée Observatory réelle n'est
simulée comme si elle était disponible en direct dans Academy — M05/M06
enseignent l'architecture réelle vérifiée (endpoints, RBAC, collections,
discipline de lineage `OBSERVED`/`NOT_CONFIGURED`), jamais une connexion
live fabriquée. Voir `docs/cvln_academy_master/30_INTERNAL/
KLT_09_20_RECONCILIATION.md` §Re-vérification (2026-09-07) pour le détail
complet de la vérification et `docs/klt/README.md` pour l'autorisation
Founder scopée qui l'a rendue possible.

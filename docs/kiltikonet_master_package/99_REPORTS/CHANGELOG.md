# Changelog — Workstream Kiltikonet

```
Historique des tickets, du cadrage initial à ce Master Package.
```

| Ticket | Objet | Livrable |
|---|---|---|
| `KLT-0001` | Cartographie éducative canonique — 8 formations, frontières, dépendances | `docs/KILTIKONET_KLT0001_CANONICAL_EDUCATION_MAP.md` |
| `KLT-0002` | Réconciliation Legacy → Canonique pour `KLT-01`→`05` | `docs/KILTIKONET_KLT0002_LEGACY_CANONICAL_RECONCILIATION.md` |
| `KLT-0003` | Référentiel canonique `KLT-01` (gelé) | `docs/KILTIKONET_KLT0003_KLT01_CANONICAL_REFERENTIAL.md` |
| `KLT-0004` | Build pédagogique complet `KLT-01` (27 documents) | `docs/KILTIKONET_KLT0004_KLT01_PEDAGOGICAL_BUILD_REPORT.md` + `docs/klt/klt01/` |
| *(continuation de session)* | Build pédagogique complet `KLT-02`→`05` (112 documents) | `docs/klt/klt02/` à `klt05/` |
| *(continuation de session)* | Export et livraison du corpus complet | `CVLN_Kiltikonet_Canonical_Corpus_KLT01-05.zip` + `docs/klt/README.md` |
| *(continuation)* | Master Package v1 — consolidation, sans reconstruction | `docs/kiltikonet_master_package/` + `docs/KILTIKONET_MASTER_PACKAGE_V1_REPORT.md` |
| `KLT-0005` | Référentiel canonique `KLT-06` (Observatory) — compétences + structure indicative uniquement | `docs/KILTIKONET_KLT0005_KLT06_CANONICAL_REFERENTIAL.md` |
| `KLT-0006` | Référentiel canonique `KLT-07` (déploiement territorial) — frontière `KLT-04`/M11 résolue | `docs/KILTIKONET_KLT0006_KLT07_CANONICAL_REFERENTIAL.md` |
| `KLT-0007` | Référentiel canonique `KLT-08` (qualité/conformité/audit réseau) — frontière `KLT-04`/M12-M13 résolue | `docs/KILTIKONET_KLT0007_KLT08_CANONICAL_REFERENTIAL.md` |
| `KLT-0008` | Décision déléguée : `contexts` (`EXTERNAL`/`INTERNAL`/`INTERNAL`) + périmètre buildable pour `KLT-06`/`07`/`08` | `docs/KILTIKONET_KLT0008_KLT06_08_CONTEXT_AND_SCOPE_DECISION.md` |
| `KLT-0009` | Build pédagogique partiel `KLT-06` (5/7 compétences, 22 documents) | `docs/klt/klt06/` |
| `KLT-0010` | Build pédagogique partiel `KLT-07` (6/7 compétences, 23 documents) | `docs/klt/klt07/` |
| **Ce ticket (`KLT-0011`)** | **Build pédagogique partiel `KLT-08` (6/7 compétences, 23 documents) + mise à jour `docs/klt/README.md` et pointeurs Master Package** | `docs/klt/klt08/` |

## Correction de cadrage explicite (Master Package v1)

Le Founder a corrigé une instruction précédente de cette même session
qui aurait pu laisser penser que `KLT-02`→`05` restaient à construire.
**Ce n'est pas le cas** : ils existaient déjà, livrés dans le ZIP relu
par le Founder avant ce ticket. Ce ticket ne reconstruit rien — il
consolide.

## Ce qui reste ouvert après ce ticket

- Validation experte/terrain (`91_VALIDATION/`) — non commencée, pour
  les 8 formations.
- Intégration runtime Academy — non commencée (`NO_RUNTIME_BINDING`
  respecté partout).
- `KLT-06`/`07`/`08` — build pédagogique `PARTIAL` livré (`KLT-0009`/
  `0010`/`0011`, 17/21 modules indicatifs construits). 4 compétences (2
  `KLT-06`, 1 `KLT-07`, 1 `KLT-08`) restent `BLOCKED` sur un accès réel à
  Observatory/Network/Compliance — non simulées.
- Les documents transversaux du Master Package v1 (`KILTIKONET_MASTER_
  PORTFOLIO_MAP.md`, `CROSS_KLT_COMPETENCY_MAP.md`, `KILTIKONET_MASTER_
  SKILL_REGISTRY.md`, `MASTER_EVIDENCE_MODEL.md`, `CERTIFICATION_
  ARCHITECTURE.md`, `MASTER_ASSESSMENT_ARCHITECTURE.md`, `93_QUALITY/
  MASTER_QUALITY_GATES.md`) datent d'avant le build `KLT-06`→`08` et ne
  reflètent pas encore les 17 nouveaux skill IDs/modules — une
  actualisation ("Master Package v2") reste un ticket distinct, non fait
  ici.

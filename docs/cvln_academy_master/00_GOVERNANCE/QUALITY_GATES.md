# CVLN Academy Master — Quality Gates (method)

```
SOURCE: mission directive §25 (Founder). STATUS: DECIDED (method).
Application status per domain: 95_GAPS/GAP_REGISTER.md.
```

## Gates à valider à chaque niveau de portfolio

`COMPETENCY_COVERAGE`, `ROLE_COVERAGE`, `ASSESSMENT_COVERAGE`,
`EVIDENCE_COVERAGE`, `AUTHORIZATION_TRACEABILITY`,
`CROSS_SYSTEM_BOUNDARY_COVERAGE`, `SOURCE_TRUTH_COVERAGE`.

## Défauts à détecter systématiquement

`ORPHAN_SKILL`, `ORPHAN_ROLE`, `ORPHAN_AUTHORIZATION`,
`UNPROVEN_FEATURE`, `FAKE_PROOF`, `DUPLICATE_CURRICULUM`,
`CROSS_DOMAIN_CONTAMINATION`, `UNAUTHORIZED_AUTHORITY`,
`EXTERNAL_INTERNAL_CONFUSION`, `CERTIFICATION_AUTHORIZATION_CONFUSION`.

## Application au tronc commun (ce Master Package)

| Gate | Résultat |
|---|---|
| `SOURCE_TRUTH_COVERAGE` | 812/812 lignes de la cartographie provenancées (`SOURCE`/`CONFIDENCE`/`VERIFICATION`, voir `10_PORTFOLIO/RECONCILIATION_MATRIX.md`) |
| `UNPROVEN_FEATURE` | 0 — aucune capacité candidate n'est présentée comme construite ; toutes restent `CANDIDATE` sauf 30 `PARTIAL_RETRIEVAL` (CVLN Hospitality) et 1 `REQUIRES_RECONCILIATION` |
| `DUPLICATE_CURRICULUM` | Signalé une fois : "Good Mood" (43 lignes) et "DJ Sayd" (51 lignes) sont deux domaines distincts dans la cartographie mais **un seul repo réel** (`gmfest972/goodmooddjsayd`) — à réconcilier avant tout référentiel (voir `GAP_REGISTER.md`) |
| `EXTERNAL_INTERNAL_CONFUSION` | 0 détecté dans la cartographie source (`Contexte` renseigné pour 811/812 lignes, 1 `TO_RECONCILE` explicite) |
| `CERTIFICATION_AUTHORIZATION_CONFUSION` | 0 — aucune ligne de `Habilitations` n'est présentée comme acquise par certification seule |

## Never claim FULLY_COMPLETE

Aucun domaine de cette cartographie n'est `FULLY_COMPLETE` — la totalité
des 812 lignes reste `CANDIDATE`/`PARTIAL_RETRIEVAL` par construction de
la source elle-même. `FULLY_COMPLETE` ne pourra être déclaré, domaine
par domaine, qu'après W6-W11 (référentiel → certification) et une
vérification humaine — jamais par ce document seul.

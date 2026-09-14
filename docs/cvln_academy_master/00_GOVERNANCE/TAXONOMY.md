# CVLN Academy Master — Taxonomy

```
SOURCE: CVLN_Academy_Cartographie_2D_Master.xlsx, sheet "Taxonomy" (9 rows)
STATUS: DECIDED (adopted as-is, no reconciliation needed — this is a
        vocabulary contract, not a content claim)
```

## Contexte (`context`)

| Code | Sens |
|---|---|
| `EXTERNAL` | Compétence utile hors CVLN ; commercialisable. |
| `INTERNAL` | Compétence propre à l'exploitation de CVLN. |
| `BRIDGE` | Relie marché/apprentissage à un système, une mission ou une opportunité CVLN. |
| `INTERNAL_RESTRICTED` | Connaissances/opérations internes sensibles. |
| `INTERNAL_PRIVILEGED` | Contrôle, sécurité, Command Center, opérations sensibles. |
| `EXECUTIVE_ONLY` | Gouvernance/autorité humaine ; jamais conférée automatiquement par Academy. |
| `HYBRID` | Utilisé **uniquement** si démontré et explicitement décomposé en `external_surface` / `internal_extension` — jamais pour éviter une décision. |

## Dimension

| Code | Sens |
|---|---|
| `MARKET` | Métiers et compétences externes. |
| `SYSTEM_CVLN` | Compétences internes et rôles opérateurs. |
| `CROSS_ECOSYSTEM` | Compétences de handoff et chaînes entre systèmes. |

## Règle centrale (rappel, jamais renégociable)

```
MARKET != CVLN_SYSTEM
EXTERNAL != INTERNAL
FORMATION != ROLE
CERTIFICATION != AUTHORIZATION
SKILL != PERMISSION
KNOWLEDGE != AUTHORITY
CURRICULUM != DELIVERY
DELIVERY != COMMERCIAL_OFFER
PROOF != AUTHORIZATION
```

Toute confusion entre ces paires, dans n'importe quel document produit
par ce chantier, est un défaut de qualité (`EXTERNAL_INTERNAL_CONFUSION`
ou `CERTIFICATION_AUTHORIZATION_CONFUSION`, voir `QUALITY_GATES.md`).

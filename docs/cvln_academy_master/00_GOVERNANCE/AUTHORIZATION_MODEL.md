# CVLN Academy Master — Authorization Model

```
SOURCE: mission directive §20-21 (Founder). STATUS: DECIDED (doctrine),
per-role instances remain PROPOSED (see 50_AUTHORIZATIONS/).
```

## Principe

`CERTIFICATION != AUTHORIZATION`. Une certification Academy prouve une
compétence ; elle n'accorde jamais, seule, un accès à un système réel,
une capacité d'approbation, ou un niveau d'`Access_Levels` supérieur à
`L0`/`L1`.

## Champs obligatoires de toute habilitation (`authorization_id`)

| Champ | Rôle |
|---|---|
| `authorization_id` | identifiant stable |
| `required_skill_ids` | compétences Academy prouvées, condition nécessaire jamais suffisante |
| `required_assessment` | évaluation dont la preuve est exigée |
| `required_certification` | certification Academy correspondante |
| `evidence_required` | type de preuve (voir `70_EVIDENCE/`) |
| `human_approval_required` | `TRUE` par défaut pour tout accès à `INTERNAL_RESTRICTED`/`INTERNAL_PRIVILEGED`/`EXECUTIVE_ONLY` |
| `expiry / renewal` | si applicable |
| `revocation_conditions` | toujours définies |
| `restricted_systems` | liste explicite des systèmes concernés |
| `audit_requirements` | traçabilité minimale exigée |

## Interdictions absolues

- Aucune habilitation `INTERNAL_PRIVILEGED` ou `EXECUTIVE_ONLY` n'est
  accordée automatiquement par la seule réussite d'un A01 Academy.
- Aucun rôle "Agent" ne reçoit d'autorité de gouvernance déléguée :
  `AGENT != AUTHORITY`, `AGENT != SELF-CERTIFYING`,
  `AUTONOMY != UNLIMITED PERMISSION`, `TOOL ACCESS != SYSTEM ACCESS`,
  `MISSION != DELEGATION OF GOVERNANCE` (mission directive §11).
- `L6 EXECUTIVE_AUTHORITY` (voir `ACCESS_LEVELS.md`) n'est jamais
  attribué par Academy.

## Statut d'implémentation

`STATUS = PROPOSED` pour les 71 lignes candidates du registre
`Habilitations` (voir `50_AUTHORIZATIONS/AUTHORIZATION_REGISTRY.md`) —
aucune n'est câblée dans le runtime Academy (`NO_RUNTIME_BINDING`).

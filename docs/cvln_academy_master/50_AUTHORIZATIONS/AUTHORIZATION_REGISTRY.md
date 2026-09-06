# CVLN Academy Master — Authorization Registry

```
SOURCE: raw/Habilitations.csv (71 rows: Domaine, Habilitation,
Sensibilité, Principe, Statut). STATUS: PROPOSED for all 71 —
none IMPLEMENTED, none bound to runtime permissions.
```

## Champs source

`Domaine`, `Habilitation` (nom), `Sensibilité`, `Principe` (règle
d'octroi), `Statut` (`CANDIDATE` pour la totalité).

## Enrichissement requis avant toute implémentation (par habilitation)

Chaque ligne doit recevoir, avant `W13` (voir `00_GOVERNANCE/
BUILD_METHOD.md`) : `authorization_id`, `required_skill_ids`,
`required_assessment`, `required_certification`, `evidence_required`,
`human_approval_required`, `expiry/renewal`, `revocation_conditions`,
`restricted_systems`, `audit_requirements` — voir
`00_GOVERNANCE/AUTHORIZATION_MODEL.md` pour le modèle complet.

## Règle absolue (rappel)

`CERTIFICATION != AUTHORIZATION`. Aucune des 71 habilitations
candidates n'est aujourd'hui accordée par une certification Academy —
`ORPHAN_AUTHORIZATION` et `CERTIFICATION_AUTHORIZATION_CONFUSION` sont
tous deux à 0 dans ce registre : chaque ligne reste un candidat, jamais
présentée comme opérationnelle.

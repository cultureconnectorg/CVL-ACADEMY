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

## Convergence post-réconciliation (mise à jour)

Chaque domaine réconcilié qui produit un rôle opérateur (`40_OPERATOR_
ROLES/ROLE_REGISTRY.md`) implique potentiellement une habilitation
correspondante dans ce registre — le lien reste `authorization_
relationship = CANDIDATE`, jamais accordé. Deux convergences
notables trouvées pendant les réconciliations de domaine :

- **Frontière sécurité (`G8`, résolue)** : toute habilitation touchant
  la sécurité applicative d'un produit (ex. accès WAL-14, KLT-17,
  FRK-48→51) doit référencer le modèle d'habilitation déjà construit
  pour `CYB-31→42` plutôt que d'inventer une habilitation par produit —
  `EXTEND_EXISTING`, jamais dupliqué.
- **Autorité humaine transversale** : `XCV-09` (Human Authority &
  Escalation, `60_CROSS_ECOSYSTEM/XCV_TRANSVERSAL_RECONCILIATION.md`)
  et `AF-22` (`AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md`)
  pointent tous deux vers `00_GOVERNANCE/AUTHORIZATION_MODEL.md` comme
  source unique de la doctrine d'escalade — jamais réécrite par
  domaine.

Aucune des 71 lignes n'est promue au-delà de `CANDIDATE` par cette
mise à jour ; elle documente seulement quels domaines réconciliés s'y
rattacheront au niveau W13.

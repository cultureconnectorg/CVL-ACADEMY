# M12 — Gérer un incident UX

```
SKILL_ID: KOR14.SKILL.C12
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
```

## Objectif
Gérer un incident d'ergonomie (interface confuse après mise à jour),
distinct d'un incident de disponibilité (`KOR-06`).

## Contenu
- Diagnostic : est-ce un incident de disponibilité (serveur, lecture
  impossible → `KOR-06`) ou d'ergonomie (navigation confuse,
  fonctionnalité introuvable → `KOR-14`) ?
- Réponse : correctif rapide, communication aux utilisateurs affectés.

## Cas fil rouge
Épisode D — la mise à jour casse la navigation du player pour une
partie des utilisateurs.

## Exercice
Produire le rapport d'incident UX avec diagnostic et correctif proposé.

## Évaluation
N2 — `E-N2-06`.

## Évidence
Rapport d'incident (`EVIDENCE_TYPE = UX_INCIDENT_REPORT`).

## Boundary check
Un incident de disponibilité classé à tort comme incident UX (ou
l'inverse) échoue ce critère.

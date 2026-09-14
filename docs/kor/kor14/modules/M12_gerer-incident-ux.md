# KOR-14 — M12 — Gérer un incident UX

```
MODULE_ID: KOR14-M12
COMPETENCY_ID: C12 — Gérer un incident UX
PREREQUISITES: M11
ASSESSMENT_LEVEL: N2
KORA_DEPENDENCY: aucune ; distinct d'un incident de disponibilité (KOR-06)
ROLE_BOUNDARIES: un incident de disponibilité classé à tort comme incident UX (ou l'inverse) échoue ce critère
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

Une mise à jour casse la navigation du player pour une partie des
utilisateurs — Djems doit d'abord diagnostiquer s'il s'agit d'un
incident d'ergonomie (son mandat) ou de disponibilité (`KOR-06`) avant
d'agir.

## Objectifs d'apprentissage

- Gérer un incident d'ergonomie distinct d'un incident de
  disponibilité.
- Diagnostiquer correctement la nature de l'incident avant de répondre.

## Notions essentielles

Le **diagnostic** distingue un incident de **disponibilité** (serveur,
lecture impossible → `KOR-06`) d'un incident d'**ergonomie**
(navigation confuse, fonctionnalité introuvable → `KOR-14`). La
**réponse** combine un correctif rapide et une communication aux
utilisateurs affectés.

## Méthode

1. Diagnostiquer si l'incident est de disponibilité (`KOR-06`) ou
   d'ergonomie (`KOR-14`).
2. Proposer un correctif rapide adapté à la nature réelle de
   l'incident.
3. Communiquer aux utilisateurs affectés.

## Exemples

Après la mise à jour, le player fonctionne (lecture possible) mais le
bouton de navigation vers la file d'attente a changé de place sans
prévenir — un incident d'ergonomie (`KOR-14`), pas de disponibilité.
À l'inverse, si le player ne parvenait plus à lire aucun contenu après
la mise à jour, ce serait un incident de disponibilité relevant de
`KOR-06` — le classer comme un problème d'ergonomie masquerait sa
vraie cause technique.

## Cas

Épisode D — la mise à jour casse la navigation du player pour une
partie des utilisateurs (`case/CASE.md`).

## Erreurs fréquentes

- Classer un incident de disponibilité comme un incident d'ergonomie,
  ou l'inverse.
- Proposer un correctif sans diagnostic préalable de la vraie cause.
- Omettre de communiquer aux utilisateurs affectés.

## Activité

Diagnostic de la nature réelle de l'incident (disponibilité vs
ergonomie).

## Exercice

Produire le rapport d'incident UX avec diagnostic et correctif
proposé.

## Livrable

Rapport d'incident (`EVIDENCE_TYPE = UX_INCIDENT_REPORT`).

## Critères de réussite

- Le diagnostic distingue correctement disponibilité et ergonomie.
- Le correctif proposé est adapté à la vraie cause.
- Les utilisateurs affectés sont informés.

## Preuve

Rapport d'incident, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Ai-je correctement distingué un incident d'ergonomie d'un incident
de disponibilité, ou les ai-je confondus ?*

## Passage au module suivant

Les enseignements de cet incident et des tests (M10) alimentent le
plan d'amélioration continue conçu en M13.

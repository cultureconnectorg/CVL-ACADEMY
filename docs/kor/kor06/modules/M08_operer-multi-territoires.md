# KOR-06 — M08 — Opérer à l'échelle multi-territoires

```
MODULE_ID: KOR06-M08
COMPETENCY_ID: C8 — Opérer à l'échelle multi-territoires
PREREQUISITES: M07
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: FREK-WORK
ORIGIN: net-new
```

## Situation professionnelle

Le public de *Rasin* est dispersé (Caraïbe, Amérique du Nord, Europe) —
une infrastructure pensée pour un seul territoire dessert mal les
auditeurs les plus éloignés.

## Objectifs d'apprentissage

- Identifier les contraintes propres à une audience multi-territoires
  (latence, fuseaux horaires pour la maintenance).
- Documenter des adaptations réalistes pour une structure de taille
  moyenne.

## Notions essentielles

Une **audience multi-territoires** pose des contraintes de latence
(distance aux serveurs) et de fenêtre de maintenance (un créneau de
maintenance à 3h du matin pour un territoire est en pleine journée pour
un autre). Une structure de taille moyenne ne peut pas dupliquer son
infrastructure partout, mais peut prioriser les territoires les plus
représentés.

## Méthode

1. Identifier les territoires réels du public de *Rasin*.
2. Documenter les contraintes de latence et de maintenance pour chacun.
3. Proposer une priorisation réaliste (pas une couverture totale
   immédiate).

## Exemple

Un créneau de maintenance choisi en pleine nuit pour les Caraïbes
affecterait la journée en Europe — un compromis (créneau à faible
audience pour les deux zones) doit être trouvé.

## Cas

L'analyse porte sur la dispersion réelle du public de *Rasin* (`case/
CASE.md`).

## Erreurs fréquentes

- Ignorer les fuseaux horaires dans la planification de maintenance.
- Proposer une couverture infrastructurelle totale non réaliste pour
  la taille de la structure.

## Activité

Identification des territoires réels et de leurs contraintes.

## Exercice

Proposer une priorisation réaliste et un créneau de maintenance
compromis.

## Livrable

Note multi-territoires.

## Critères de réussite

- Les contraintes de fuseaux horaires sont prises en compte.
- La priorisation reste réaliste pour la taille d'Anba Tonèl Host.

## Preuve

Note, signal `FREK-WORK`.

## Auto-évaluation

*Ma proposition est-elle réaliste pour une structure de taille moyenne,
ou suppose-t-elle des moyens disproportionnés ?*

## Passage au module suivant

L'ensemble des opérations (M01-M08) est maintenant complet — M09 exige
de l'articuler et de le défendre.

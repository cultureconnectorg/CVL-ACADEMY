# KOR-05 — M09 — Gérer un incident et produire un reporting

```
MODULE_ID: KOR05-M09
COMPETENCY_ID: C9 — Gérer un incident et produire un reporting opérationnel
PREREQUISITES: M08
ASSESSMENT_LEVEL: N2
KORA_DEPENDENCY: aucune
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: FREK-SCORE
ORIGIN: net-new
```

## Situation professionnelle

Un fichier de *Rasin* a été écrasé par erreur par une version plus
ancienne — conséquence directe d'une absence de convention de
versionnement stricte (M03). L'incident doit être géré et communiqué
honnêtement.

## Objectifs d'apprentissage

- Réagir à un incident (identifier, restaurer si possible, communiquer).
- Produire un reporting honnête, y compris sur ses propres limites.

## Notions essentielles

Un **incident** bien géré ne se limite pas à "réparer discrètement" —
il implique de communiquer avec le créateur affecté et de comprendre la
cause pour éviter une répétition (ici, renforcer la convention de M03).

## Méthode

1. Identifier l'ampleur réelle de l'incident (quelle version est
   perdue, laquelle reste disponible).
2. Restaurer si possible, ou communiquer clairement si impossible.
3. Documenter la cause et une mesure corrective (liée à M03).

## Exemple

Une version antérieure de *Rasin* écrase la version finale ; Kessy
identifie qu'une copie de sauvegarde existe, restaure, informe le
Lanbi Collective de l'incident et renforce la convention de
versionnement.

## Cas

L'incident porte sur le fichier réel du cas (`case/CASE.md`).

## Erreurs fréquentes

- Cacher l'incident au créateur affecté.
- Réparer sans comprendre ni traiter la cause.

## Activité

Identification de l'ampleur de l'incident et des options de
restauration.

## Exercice

Rédiger le rapport d'incident, cause et mesure corrective incluses.

## Livrable

Rapport d'incident complet.

## Critères de réussite

- Le créateur affecté est informé honnêtement.
- La cause est identifiée et une mesure corrective proposée.

## Preuve

Rapport d'incident, signal `FREK-SCORE`.

## Auto-évaluation

*Ai-je communiqué honnêtement avec le créateur affecté, ou tenté de
minimiser l'incident ?*

## Passage au module suivant

L'ensemble des opérations (M01-M09) est maintenant complet — M10 exige
de l'articuler et de le défendre.

# KOR-06 — M06 — Gérer un incident et l'escalade

```
MODULE_ID: KOR06-M06
COMPETENCY_ID: C6 — Gérer un incident et l'escalade
PREREQUISITES: M05
ASSESSMENT_LEVEL: N2
KORA_DEPENDENCY: aucune
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: FREK-SCORE
ORIGIN: net-new
```

## Situation professionnelle

Un pic de trafic inattendu sature les serveurs et rend *Rasin*
indisponible pendant une publication importante — l'incident central
du cas.

## Objectifs d'apprentissage

- Réagir à un incident en temps réel (diagnostic, communication,
  résolution).
- Décider quand et comment escalader vers un niveau supérieur.

## Notions essentielles

Un **incident géré correctement** suit un cycle : détecter,
diagnostiquer, communiquer (au créateur affecté, à l'équipe),
résoudre, documenter. L'**escalade** (faire intervenir un niveau
supérieur) doit se décider sur des critères explicites (durée,
gravité), pas par réflexe ni par évitement.

## Méthode

1. Diagnostiquer la cause de la saturation (pic de trafic externe, pas
   *Rasin* lui-même).
2. Communiquer immédiatement avec le Lanbi Collective sur l'état réel.
3. Décider si l'incident nécessite une escalade, selon des critères
   liés au SLA/SLO de M05.

## Exemple

Une indisponibilité de 5 minutes reste sous le seuil du SLO — gérée
sans escalade. Une indisponibilité de 2 heures dépasserait le seuil et
justifierait une escalade formelle.

## Cas

L'incident porte sur la saturation réelle touchant *Rasin* (`case/
CASE.md`).

## Erreurs fréquentes

- Ne pas communiquer avec le créateur affecté pendant l'incident.
- Escalader systématiquement ou jamais, sans critère lié au SLA/SLO.

## Activité

Diagnostic de la cause de l'incident.

## Exercice

Décider et justifier une escalade ou non, selon le SLA/SLO.

## Livrable

Rapport d'incident.

## Critères de réussite

- La communication avec le créateur affecté est documentée.
- La décision d'escalade (ou non) est justifiée par le SLA/SLO.

## Preuve

Rapport, signal `FREK-SCORE`.

## Auto-évaluation

*Ma décision d'escalade repose-t-elle sur un critère explicite, ou sur
une impression ?*

## Passage au module suivant

Cet incident révèle un besoin de monitoring amélioré, traité en M07.

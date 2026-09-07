# KOR-14 — M06 — Concevoir le placement UX de recommandations

```
MODULE_ID: KOR14-M06
COMPETENCY_ID: C6 — Concevoir le placement UX de recommandations (sans moteur réel)
PREREQUISITES: M05
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune ; aucun moteur de recommandation KORA n'existe (cohérent avec KOR-12)
ROLE_BOUNDARIES: toute affirmation qu'un moteur de recommandation existe aujourd'hui échoue ce critère
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

Naïma se demande où *Rasin* apparaîtrait si une recommandation existait
un jour — Djems doit concevoir l'emplacement possible, à un niveau
purement UX, sans jamais laisser croire que l'algorithme existe déjà.

## Objectifs d'apprentissage

- Concevoir où et comment une recommandation apparaîtrait dans
  l'interface.
- Confirmer explicitement qu'aucun moteur de recommandation KORA
  n'existe aujourd'hui.

## Notions essentielles

Les **emplacements typiques** d'une recommandation incluent le home, la
fin de lecture, la recherche. Ce module conçoit l'**emplacement**, pas
l'**algorithme** — cohérent avec `KOR-12`, aucun moteur de
recommandation KORA n'existe aujourd'hui, et cette note doit le
rappeler explicitement.

## Méthode

1. Identifier les emplacements où une recommandation apparaîtrait si
   elle existait.
2. Documenter les hypothèses explicites (ce que l'emplacement
   supposerait comme données disponibles).
3. Confirmer explicitement l'absence de tout moteur réel aujourd'hui.

## Exemples

La note propose un emplacement en fin de lecture de *Rasin*
("Puisque vous avez terminé cet épisode..."), en précisant explicitement
que ce placement suppose un moteur qui n'existe pas encore. À
l'inverse, présenter une maquette avec des recommandations déjà
affichées comme si elles fonctionnaient réellement laisserait croire à
une capacité KORA inexistante — l'emplacement doit rester hypothétique
tant que l'algorithme n'existe pas.

## Cas

Épisode A, suite — où *Rasin* apparaîtrait-il si une recommandation
existait un jour ? (`case/CASE.md`)

## Erreurs fréquentes

- Affirmer qu'un moteur de recommandation existe aujourd'hui.
- Présenter une maquette qui simule des recommandations déjà
  fonctionnelles.
- Omettre de documenter les hypothèses explicites du placement proposé.

## Activité

Identification des emplacements où une recommandation apparaîtrait.

## Exercice

Produire la note de placement UX avec ses hypothèses explicites.

## Livrable

Note de placement (`EVIDENCE_TYPE = RECOMMENDATION_PLACEMENT_NOTE`).

## Critères de réussite

- Les emplacements proposés sont cohérents avec l'expérience globale.
- Les hypothèses sont explicitement documentées.
- L'absence de moteur réel aujourd'hui est confirmée explicitement.

## Preuve

Note de placement, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Ma note confirme-t-elle explicitement qu'aucun moteur n'existe
aujourd'hui, ou ai-je laissé une ambiguïté ?*

## Passage au module suivant

Cette expérience doit rester accessible à tous, y compris à faible
littératie numérique, traité en M07.

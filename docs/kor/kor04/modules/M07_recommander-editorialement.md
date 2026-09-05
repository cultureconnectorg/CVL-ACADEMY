# KOR-04 — M07 — Recommander éditorialement (curation humaine)

```
MODULE_ID: KOR04-M07
COMPETENCY_ID: C7 — Recommander éditorialement (curation humaine)
PREREQUISITES: M06
ASSESSMENT_LEVEL: N2
KORA_DEPENDENCY: aucune ; frontière explicite avec KOR-12 (recommandation data, non construit)
ROLE_BOUNDARIES: ce module n'implique aucun système de recommandation algorithmique réel
FREK_PROOF_MAPPING: FREK-SCORE
ORIGIN: net-new
```

## Situation professionnelle

*Rézo Kilti* affiche des recommandations "à découvrir aussi" à côté de
chaque contenu programmé. Naïma les rédige elle-même — rien n'est
généré par un système de données réel.

## Objectifs d'apprentissage

- Rédiger des recommandations éditoriales assumées comme des choix
  humains.
- Ne jamais présenter une recommandation humaine comme si elle
  provenait d'une analyse de données réelle.

## Notions essentielles

Une **recommandation éditoriale humaine** est un jugement assumé
("nous pensons que...") — la confondre avec une recommandation
algorithmique ("les données montrent que...") sans en avoir la preuve
serait une fausse déclaration (cohérent avec `NO_FAKE_KORA_CAPABILITY`,
frontière avec `KOR-12`, non construit).

## Méthode

1. Rédiger chaque recommandation à la première personne du curateur,
   jamais au nom d'un système.
2. Justifier chaque recommandation par un critère éditorial explicite,
   pas par une statistique inventée.
3. Vérifier qu'aucune formulation ne suggère une donnée réelle
   inexistante.

## Exemple

Formulation correcte : « Notre choix : après *Rasin*, on vous
recommande *Gwo Siwo* pour sa richesse musicale. » Formulation à
proscrire : « 87% des auditeurs de *Rasin* ont aussi aimé *Gwo Siwo* »
(chiffre fabriqué, aucune donnée réelle).

## Cas

Les recommandations portent sur le catalogue réel du cas (`case/
CASE.md`).

## Erreurs fréquentes

- Fabriquer une statistique pour crédibiliser une recommandation
  humaine.
- Cacher que la recommandation est un choix humain assumé.

## Activité

Rédaction de recommandations pour chaque contenu programmé.

## Exercice

Vérifier chaque recommandation contre le risque de fausse donnée.

## Livrable

Recommandations éditoriales assumées.

## Critères de réussite

- Aucune recommandation ne prétend s'appuyer sur une donnée réelle
  inexistante.
- Chaque recommandation est justifiée par un critère éditorial
  explicite.

## Preuve

Recommandations, signal `FREK-SCORE`.

## Auto-évaluation

*Ai-je fabriqué une statistique pour rendre ma recommandation plus
crédible ?*

## Passage au module suivant

La programmation complète est maintenant testée par un événement de
clôture mesuré en M08.

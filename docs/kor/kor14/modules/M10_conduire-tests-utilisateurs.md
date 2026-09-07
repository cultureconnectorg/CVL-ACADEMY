# KOR-14 — M10 — Conduire des tests utilisateurs

```
MODULE_ID: KOR14-M10
COMPETENCY_ID: C10 — Conduire des tests utilisateurs
PREREQUISITES: M09
ASSESSMENT_LEVEL: N2
KORA_DEPENDENCY: aucune
ROLE_BOUNDARIES: aucune
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

Le nouveau parcours de découverte de *Rasin* (M01-M02) a été conçu sur
la seule intuition de Djems — un test utilisateur structuré est
nécessaire pour vérifier qu'il fonctionne réellement pour l'audience
visée.

## Objectifs d'apprentissage

- Conduire un test utilisateur structuré sur le nouveau parcours.
- En tirer des conclusions actionnables, sans sur-interpréter un petit
  échantillon.

## Notions essentielles

La **méthode** de test suit un protocole avec des tâches précises,
observe sans suggérer la réponse attendue. L'**analyse des résultats**
doit rester prudente face à un petit échantillon — une conclusion
tirée de quelques observations ne vaut pas une généralité.

## Méthode

1. Définir un protocole de test avec des tâches précises.
2. Observer sans suggérer la réponse attendue au participant.
3. Analyser les résultats en reconnaissant les limites de
   l'échantillon.

## Exemples

Le protocole demande "Retrouvez le dernier épisode de Rasin" sans
indiquer où chercher, révélant que plusieurs participants cherchent
d'abord dans la mauvaise section — un résultat actionnable. À
l'inverse, orienter la consigne ("Cliquez sur l'icône bibliothèque
pour retrouver Rasin") révélerait seulement que les participants
savent suivre une instruction, pas s'ils auraient trouvé le chemin par
eux-mêmes — le test perdrait toute valeur diagnostique.

## Cas

Épisode E — tests utilisateurs sur le nouveau parcours de découverte
de *Rasin* (`case/CASE.md`).

## Erreurs fréquentes

- Suggérer la réponse attendue dans la consigne du test.
- Généraliser un résultat observé sur un échantillon trop petit.
- Ignorer un résultat inattendu qui contredit la conception initiale.

## Activité

Définition du protocole de test avec des tâches précises non
orientées.

## Exercice

Produire le rapport de tests utilisateurs avec conclusions et limites.

## Livrable

Rapport de tests (`EVIDENCE_TYPE = USER_TESTING_REPORT`).

## Critères de réussite

- Le protocole ne suggère pas la réponse attendue.
- Les conclusions restent proportionnées à la taille de l'échantillon.
- Un résultat inattendu, s'il existe, est rapporté honnêtement.

## Preuve

Rapport de tests, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Mon protocole a-t-il orienté la réponse, ou ai-je observé un
comportement réellement spontané ?*

## Passage au module suivant

Ces résultats de tests se recoupent avec les analytics produit
analysés en M11.

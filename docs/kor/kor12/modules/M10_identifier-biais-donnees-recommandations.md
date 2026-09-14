# KOR-12 — M10 — Identifier des biais dans données et recommandations

```
MODULE_ID: KOR12-M10
COMPETENCY_ID: C10 — Identifier des biais dans les données et recommandations
PREREQUISITES: M09
ASSESSMENT_LEVEL: N2
KORA_DEPENDENCY: aucune ; hypothétique, aucun système réel à évaluer aujourd'hui
ROLE_BOUNDARIES: NEEDS_EXPERT_REVIEW — biais algorithmiques réels, toute application doit être validée par une expertise externe
FREK_PROOF_MAPPING: READY_FOR_FREK_PROOF = FALSE
ORIGIN: net-new
```

## Situation professionnelle

Si un système de recommandation existait un jour pour *Rasin*
(scénario hypothétique de M09), quels biais faudrait-il vérifier avant
de le déployer — en particulier ceux qui sous-représenteraient des
contenus en langue créole/minoritaire ?

## Objectifs d'apprentissage

- Identifier des biais potentiels dans un jeu de données ou un système
  de recommandation hypothétique.
- Repérer en particulier les biais qui sous-représenteraient des
  contenus en langue créole/minoritaire.

## Notions essentielles

Les **sources de biais** incluent un échantillon non représentatif, et
une boucle de rétroaction où les contenus déjà populaires sont
davantage recommandés, invisibilisant les nouveaux. Un **biais culturel
spécifique** existe : un système entraîné sur un corpus majoritairement
non-créole sous-représenterait *Rasin* et ses semblables, précisément
les contenus que ce système est censé aider à découvrir.

## Méthode

1. Identifier les sources de biais génériques (échantillon, boucle de
   rétroaction).
2. Évaluer spécifiquement le risque de sous-représentation culturelle.
3. Marquer explicitement l'analyse comme hypothétique, aucun système
   réel n'existant à évaluer aujourd'hui.

## Exemples

Un système hypothétique entraîné majoritairement sur des podcasts en
anglais/français sous-représenterait *Rasin* dans ses recommandations,
même si sa qualité de contenu est équivalente — un biais culturel
documenté à anticiper avant tout déploiement. À l'inverse, se limiter
à vérifier un biais générique d'échantillon sans jamais examiner
spécifiquement la représentation des contenus créoles laisserait
passer le risque le plus pertinent pour *Rasin*.

## Cas

Épisode D, suite — si un système de recommandation existait un jour,
quels biais faudrait-il vérifier avant de le déployer pour *Rasin* ?
(`case/CASE.md`).

## Erreurs fréquentes

- Analyser uniquement les biais génériques sans examiner le biais
  culturel spécifique.
- Présenter l'analyse comme si un système réel existait à évaluer.
- Ignorer la boucle de rétroaction (populaire devient plus
  recommandé, invisibilisant le nouveau).

## Activité

Identification des sources de biais génériques et du biais culturel
spécifique.

## Exercice

Produire un rapport de biais anticipés (hypothétique, explicitement
marqué comme tel).

## Livrable

Rapport de biais (`EVIDENCE_TYPE = BIAS_ASSESSMENT_REPORT`).

## Critères de réussite

- Le rapport identifie le biais culturel spécifique, pas seulement
  générique.
- Le caractère hypothétique de l'analyse est explicitement marqué.
- La boucle de rétroaction est mentionnée comme risque distinct.

## Preuve

Rapport de biais, `READY_FOR_FREK_PROOF = FALSE`.

## Auto-évaluation

*Mon rapport identifie-t-il le risque de sous-représentation
culturelle spécifique, ou s'arrête-t-il aux biais génériques ?*

## Passage au module suivant

Au-delà des chiffres, une intelligence culturelle réelle doit être
produite à partir de ces données — traité en M11.

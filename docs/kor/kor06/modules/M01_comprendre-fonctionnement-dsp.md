# KOR-06 — M01 — Comprendre le fonctionnement d'un DSP

```
MODULE_ID: KOR06-M01
COMPETENCY_ID: C1 — Comprendre le fonctionnement d'un DSP
PREREQUISITES: Aucun
ASSESSMENT_LEVEL: N1
KORA_DEPENDENCY: aucune — véhicule générique Anba Tonèl Host, distinct de KORA
ROLE_BOUNDARIES: ce module ne couvre pas la négociation de droits (KOR-07, non construit)
FREK_PROOF_MAPPING: FREK-WORK
ORIGIN: net-new
```

## Situation professionnelle

Le candidat rejoint l'équipe d'exploitation d'Anba Tonèl Host sans
connaître en détail les composants d'un DSP (Digital Service
Provider) — hébergement, catalogue, flux RSS, distribution aux
applications d'écoute.

## Objectifs d'apprentissage

- Identifier les composants principaux d'un DSP.
- Comprendre le rôle de chaque composant dans la chaîne de service.

## Notions essentielles

Un **DSP** combine un hébergement de fichiers, un catalogue (métadonnées
des créateurs et épisodes), un système de flux (RSS ou équivalent), et
une distribution vers les applications d'écoute — chaque composant peut
tomber en panne indépendamment des autres.

## Méthode

1. Cartographier les composants d'Anba Tonèl Host.
2. Identifier ce qui dépend de quoi (le flux dépend du catalogue, la
   distribution dépend du flux).
3. Documenter cette cartographie.

## Exemples

Une panne de l'hébergement de fichiers rend les épisodes existants
inaccessibles même si le catalogue et les flux fonctionnent — les
composants sont liés mais distincts. À l'inverse, une panne du
catalogue (métadonnées manquantes) peut sembler identique à une panne
d'hébergement du point de vue de l'auditeur (contenu absent) — pourtant
les corriger nécessite d'intervenir sur des composants entièrement
différents.

## Cas

La cartographie porte sur Anba Tonèl Host réellement (`case/CASE.md`).

## Erreurs fréquentes

- Traiter le DSP comme une boîte noire unique sans composants
  distincts.
- Ignorer les dépendances entre composants.
- Diagnostiquer une panne par son seul symptôme visible (contenu
  manquant) sans identifier lequel des composants distincts en est la
  cause réelle.

## Activité

Cartographie des composants d'Anba Tonèl Host.

## Exercice

Documenter les dépendances entre composants.

## Livrable

Note de fonctionnement du DSP.

## Critères de réussite

- Les composants principaux sont identifiés.
- Les dépendances entre eux sont documentées.

## Preuve

Note, signal `FREK-WORK`.

## Auto-évaluation

*Ma cartographie couvre-t-elle vraiment tous les composants, ou
seulement ceux visibles de l'extérieur ?*

## Passage au module suivant

Cette cartographie sert de base à la modélisation de la chaîne
ingestion→delivery en M02.

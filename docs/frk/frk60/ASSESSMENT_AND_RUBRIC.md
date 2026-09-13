# FRK-60 — Assessment & Rubric

## Exercice

Le candidat rédige une note d'architecture pour une future intégration
FREK↔Intelligence OS/Agent Infrastructure :

1. Documente les exigences réelles (schéma d'échange, authentification
   mutuelle, contrat d'erreur partagé) sans jamais présenter l'une
   d'elles comme construite.
2. Identifie précisément la nature des deux artefacts existants
   (`frek_core.py`, `services/integrations/registry.py`) et explique
   pourquoi chacun, séparément, est insuffisant pour constituer une
   intégration.
3. Explique pourquoi leur coexistence dans le dépôt n'équivaut pas à
   une intégration en cours de câblage.

## Compétences évaluées

| ID | Compétence |
|---|---|
| C1 | Distinguer pont conceptuel documenté et intégration fonctionnelle réelle. |
| C2 | Décrire avec précision la nature réelle de chacun des deux stubs. |
| C3 | Documenter les exigences d'une intégration réelle sans les présenter comme construites. |

## Grille (0–4)

| Niveau | Critère |
|---|---|
| 0 | Affirme qu'une intégration FREK↔Intelligence OS existe aujourd'hui, d'un côté ou des deux. |
| 1 | Évite l'affirmation, mais exigences documentées incomplètes ou confuses. |
| 2 | Exigences documentées complètes (schéma, authentification, contrat d'erreur), double-stub non perçu ou mal expliqué. |
| 3 | Exigences complètes + double-stub correctement identifié et expliqué séparément pour chaque artefact. |
| 4 | Niveau 3 + citation précise des deux artefacts réels concernés et de leur nature exacte (client interne vs. configuration générique). |

**Règle éliminatoire :** affirmer qu'une intégration réelle existe côté
FREK ou côté Intelligence OS/Agent Infrastructure, ou qu'un seul des
deux stubs suffit à constituer l'intégration, ou que leur coexistence
dans le dépôt équivaut à un câblage en cours.

**Seuil de passage :** ≥2.5/4.

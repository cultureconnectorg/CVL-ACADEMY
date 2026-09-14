# FRK-16 — Assessment & Rubric

## Exercice

Le candidat lit une description d'état d'ancrage OpenTimestamps réel,
en explique précisément la garantie, rédige les deux frontières
obligatoires (légale, FREK), puis évalue honnêtement la limite de la
clé de notaire non chiffrée au repos.

## Compétences évaluées

| ID | Compétence |
|---|---|
| C1 | Décrire précisément ce que prouve la notarisation par signature Ed25519 et l'ancrage OpenTimestamps. |
| C2 | Maintenir les deux frontières obligatoires : jamais un effet légal, jamais une capacité FREK. |
| C3 | Évaluer honnêtement une limite documentée sans la minimiser ni l'exagérer. |

## Grille (0–4)

| Niveau | Critère |
|---|---|
| 0 | Affirme un effet légal, ou fusionne avec `frek_core.py`/FRK-13. |
| 1 | Évite ces deux erreurs, description technique incomplète. |
| 2 | Description technique correcte (signature + ancrage), frontières implicites. |
| 3 | Description complète + les deux frontières (légale, FREK) explicites. |
| 4 | Niveau 3 + cite correctement la limite documentée (clé non chiffrée
    au repos) sans la minimiser. |

**Règle éliminatoire :** affirmer un effet légal/notarial réel, ou
présenter ce système comme une infrastructure FREK/`frek_core.py`.

**Seuil de passage :** ≥2.5/4.

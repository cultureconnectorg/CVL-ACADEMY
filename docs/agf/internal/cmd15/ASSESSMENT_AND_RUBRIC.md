# CMD-15 — Assessment & Rubric

Structure identique à `docs/frk/frk01/ASSESSMENT_AND_RUBRIC.md` (N1
40% / N2 30% / livrable 30%, même `../../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Littératie des routes réelles `/command-center/overview`/`/timeline` (`MetaCVLN`) |
| C2 | Frontière de maturité (`PARTIAL`/`PRODUCT_DEPENDENCY`, jamais `BLOCKED` ni `DEPLOYED_RUNTIME`) |
| C3 | Discipline des trois systèmes (`fms-os/fms` vs `MetaCVLN` vs discipline SRE/ICS marché) |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Affirme un accès opérationnel réel à `MetaCVLN`, ou fusionne `fms-os/fms` avec le vrai Command Center |
| 1 | Confond maturité `PARTIAL` avec `BLOCKED` ou avec `DEPLOYED_RUNTIME` |
| 2 | Littératie des routes correcte mais frontière de maturité imprécise |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `REPO_REGISTRY.md`/la correction Wave 2 ligne par ligne |

## Règle éliminatoire

Toute affirmation d'accès réel à `MetaCVLN`, ou toute fusion des trois
systèmes distincts, entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.

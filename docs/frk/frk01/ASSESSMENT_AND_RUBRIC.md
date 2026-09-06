# FRK-01 — Assessment & Rubric

Structure identique à `docs/wal/wal19/ASSESSMENT_AND_RUBRIC.md` (N1
40% / N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | System map réel (5 méthodes, remote/local fallback) |
| C2 | Vocabulaire de signal (8 valeurs réelles, rejet silencieux) |
| C3 | Paliers de progression (6 réels, seuils exacts) |
| C4 | Réalité honnête de `issue_proof()` (stub, aucune garantie crypto) |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente une méthode, un signal, un palier, ou affirme une garantie cryptographique inexistante |
| 1 | Confond ce module avec un autre système FREK (Good Mood, `frek_v3/`) |
| 2 | System map correct mais imprécision sur le comportement de fallback |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `frek_core.py` ligne par ligne |

## Règle éliminatoire

Toute capacité inventée (méthode, signal, palier, garantie
cryptographique de `issue_proof()`) entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.

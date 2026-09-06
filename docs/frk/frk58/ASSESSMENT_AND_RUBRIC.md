# FRK-58 — Assessment & Rubric

Structure identique à `docs/frk/frk01/ASSESSMENT_AND_RUBRIC.md` (N1
40% / N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Pattern remote/local fallback (`_remote_post`, `is_remote_enabled`) |
| C2 | Émission et validation de signal (`VALID_SIGNALS`, rejet silencieux) |
| C3 | Résolution des paliers de progression (`STADE_THRESHOLDS`) |
| C4 | Frontière avec `frek_v3`/FRK-71→75 et absence d'intégration observée |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente un comportement d'erreur, un signal accepté hors liste, ou affirme une intégration inexistante |
| 1 | Confond `frek_core.py` avec `frekcoreAout2026`/`frek_v3` |
| 2 | Comportement correct mais imprécision sur le timing/fallback |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `frek_core.py` ligne par ligne |

## Règle éliminatoire

Toute capacité inventée ou toute intégration affirmée à tort entraîne
un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.

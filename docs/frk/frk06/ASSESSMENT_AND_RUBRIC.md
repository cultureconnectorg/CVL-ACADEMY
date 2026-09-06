# FRK-06 — Assessment & Rubric

Structure identique à `docs/frk/frk01/ASSESSMENT_AND_RUBRIC.md` (N1
40% / N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Minting remote-first (`_remote_post`, condition `frek_id`) |
| C2 | Mécanique du compteur local (`db.counters`, format `FREK-{seq:03d}`) |
| C3 | Discipline de frontière (jamais DID/VC/révocation) |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente un mécanisme de révocation/rotation, ou confond avec DID/VC |
| 1 | Format d'identifiant incorrect ou mécanique du compteur imprécise |
| 2 | Comportement correct mais frontière de portée non énoncée |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `mint_frek_id()` ligne par ligne |

## Règle éliminatoire

Toute capacité de révocation/rotation inventée, ou toute confusion
avec DID/VC, entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
